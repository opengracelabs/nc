import json
from pathlib import Path

from workers.rijksmuseum_adapter.store import write_record

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")


class _Transaction:
    def __init__(self, conn: "ComplianceConn") -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.events.append(("transaction_enter", None, ()))

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.conn.events.append(("transaction_exit", None, ()))


class ComplianceConn:
    def __init__(self) -> None:
        self.events = []
        self._count = 0

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args):
        self._count += 1
        table = _table_name(sql)
        self.events.append(("fetchrow", table, args))
        return {"id": f"{table}-{self._count}"}

    async def execute(self, sql: str, *args):
        self.events.append(("execute", _table_name(sql), args))
        return "UPDATE 1"


def _table_name(sql: str) -> str:
    compact = " ".join(sql.split()).lower()
    for table in (
        "workflow_items",
        "preservation_event",
        "media_technical_metadata",
        "media_rights",
        "media_file",
        "source_record",
        "source_item",
    ):
        if f"insert into {table}" in compact or f"update {table}" in compact:
            return table
    return "unknown"


def _xml() -> str:
    return _FIXTURE.read_text()


def _xml_without_rights() -> str:
    return _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )


def _xml_with_set_spec(set_spec: str) -> str:
    return _xml().replace(
        "<datestamp>2025-07-08T18:28:45Z</datestamp>",
        f"<datestamp>2025-07-08T18:28:45Z</datestamp>\n        <setSpec>{set_spec}</setSpec>",
    )


def _search_response() -> dict:
    return {
        "orderedItems": [
            {"id": "https://id.rijksmuseum.nl/200343467", "title": "Yellowstone National Park"}
        ]
    }


def _fetchrow_args(conn: ComplianceConn, table: str) -> tuple:
    return next(
        args
        for kind, event_table, args in conn.events
        if kind == "fetchrow" and event_table == table
    )


async def test_v1_missing_edm_rights_uses_shared_review_workflow() -> None:
    conn = ComplianceConn()

    result = await write_record(
        conn,
        _search_response(),
        _xml_without_rights(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["workflow_item_id"] == "workflow_items-7"
    assert result["writes"] == 8
    evidence = json.loads(_fetchrow_args(conn, "media_rights")[2])
    assert evidence["edm_rights_uri"] is None
    assert evidence["rights_basis"] == "missing_rights"
    assert evidence["rights_matrix_classification"] == "review_required"


async def test_v2_pilot_set_261222_derives_biological_anchor_type() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _search_response(),
        _xml_with_set_spec("261222"),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert _fetchrow_args(conn, "source_item")[5] == "biological"


async def test_v2_default_anchor_type_derives_cultural() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _search_response(),
        _xml_with_set_spec("260239"),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert _fetchrow_args(conn, "source_item")[5] == "cultural"


async def test_v3_rights_evidence_contains_article_3f_dictionary() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    evidence = json.loads(_fetchrow_args(conn, "media_rights")[2])
    assert evidence["source"] == "rijksmuseum"
    assert evidence["source_record_id"] == "source_record-2"
    assert evidence["edm_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"
    assert evidence["oai_pmh_identifier"] == "https://id.rijksmuseum.nl/200343467"
    assert len(evidence["raw_payload_hash"]) == 64
    assert evidence["worker_classified_status"] == "verified_pd"
    assert evidence["evidence_status"] == "pending_human_review"
