"""Sprint 4 remediation replay tests — V1, V2, V3."""
import json
from pathlib import Path

from workers.rijksmuseum_adapter.store import write_record

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")


class _Transaction:
    def __init__(self, conn: "ReplayConn") -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.sql_order.append("BEGIN")

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.conn.sql_order.append("COMMIT")


class ReplayConn:
    def __init__(self) -> None:
        self.sql_order = []
        self._count = 0
        self.args_by_table: dict[str, tuple] = {}

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args):
        self._count += 1
        table = _table_name(sql)
        self.sql_order.append(table)
        self.args_by_table[table] = args
        return {"id": f"{table}-{self._count}"}

    async def execute(self, sql: str, *args):
        table = _table_name(sql)
        self.sql_order.append(table)
        self.args_by_table[f"execute:{table}"] = args
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


def _search_response() -> dict:
    return {
        "orderedItems": [
            {"id": "https://id.rijksmuseum.nl/200343467", "title": "Yellowstone National Park"}
        ]
    }


def _xml() -> str:
    return _FIXTURE.read_text()


def _xml_with_set_spec(set_spec: str) -> str:
    return _xml().replace(
        "<datestamp>2025-07-08T18:28:45Z</datestamp>",
        f"<datestamp>2025-07-08T18:28:45Z</datestamp>\n        <setSpec>{set_spec}</setSpec>",
    )


# V1 ──────────────────────────────────────────────────────────────────────────

async def test_sprint4_v1_absent_rights_blocked_without_source_record() -> None:
    xml = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    conn = ReplayConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "missing_rights_uri"
    assert result["writes"] == 0
    assert conn.sql_order == []


async def test_sprint4_v1_absent_rights_rejection_is_deterministic() -> None:
    xml = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    left = ReplayConn()
    right = ReplayConn()

    left_result = await write_record(
        left, _search_response(), xml,
        source_id="source-rijksmuseum", media_type_id="image",
    )
    right_result = await write_record(
        right, _search_response(), xml,
        source_id="source-rijksmuseum", media_type_id="image",
    )

    assert left_result == right_result
    assert left.sql_order == right.sql_order == []


# V2 ──────────────────────────────────────────────────────────────────────────


async def test_sprint4_v2_anchor_type_is_derived_from_pilot_set_261222() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        _search_response(),
        _xml_with_set_spec("261222"),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert conn.args_by_table["source_item"][5] == "biological"

async def test_sprint4_v2_biological_anchor_type_written_for_set_261222() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )

    assert result["status"] == "written"
    source_item_args = conn.args_by_table["source_item"]
    assert source_item_args[5] == "biological"


async def test_sprint4_v2_cultural_default_anchor_type_is_stable_across_runs() -> None:
    left = ReplayConn()
    right = ReplayConn()

    await write_record(
        left, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )
    await write_record(
        right, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )

    assert left.args_by_table["source_item"][5] == "cultural"
    assert right.args_by_table["source_item"][5] == "cultural"
    assert left.sql_order == right.sql_order


# V3 ──────────────────────────────────────────────────────────────────────────

async def test_sprint4_v3_evidence_contains_all_required_fields_for_pdm_record() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "rijksmuseum"
    assert evidence["edm_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"
    assert evidence["oai_pmh_identifier"] == "https://id.rijksmuseum.nl/200343467"
    assert evidence["worker_classified_status"] == "classified_pd"
    assert evidence["evidence_status"] == "pending_human_review"
    assert len(evidence["raw_payload_hash"]) == 64


async def test_sprint4_v3_evidence_is_stable_across_runs() -> None:
    left = ReplayConn()
    right = ReplayConn()

    await write_record(
        left, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )
    await write_record(
        right, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )

    left_evidence = json.loads(left.args_by_table["media_rights"][2])
    right_evidence = json.loads(right.args_by_table["media_rights"][2])

    assert left_evidence == right_evidence


async def test_sprint4_v3_evidence_review_required_classification_for_noc_cr() -> None:
    xml = _xml().replace(
        "http://creativecommons.org/publicdomain/mark/1.0/",
        "https://rightsstatements.org/vocab/NoC-CR/1.0/",
    )
    conn = ReplayConn()

    await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["rights_matrix_classification"] == "review_required"
    assert evidence["edm_rights_uri"] == "https://rightsstatements.org/vocab/NoC-CR/1.0/"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"


# Cross-violation ──────────────────────────────────────────────────────────────

async def test_sprint4_full_write_path_with_all_three_fixes_applied() -> None:
    xml_no_rights = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    conn_blocked = ReplayConn()
    blocked_result = await write_record(
        conn_blocked,
        _search_response(),
        xml_no_rights,
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )
    assert blocked_result["status"] == "rejected"
    assert blocked_result["reason"] == "missing_rights_uri"
    assert conn_blocked.sql_order == []

    conn_written = ReplayConn()
    written_result = await write_record(
        conn_written,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )
    assert written_result["status"] == "written"
    assert conn_written.args_by_table["source_item"][5] == "biological"
    evidence = json.loads(conn_written.args_by_table["media_rights"][2])
    assert "edm_rights_uri" in evidence
    assert "rights_matrix_classification" in evidence
    assert "applying_policy" in evidence
    assert "oai_pmh_identifier" in evidence
