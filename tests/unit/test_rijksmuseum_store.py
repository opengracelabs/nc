import json
from pathlib import Path
from uuid import UUID

from workers.rijksmuseum_adapter.store import build_raw_payload, write_record

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")


class _Transaction:
    def __init__(self, conn: "FakeConn") -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.events.append(("transaction_enter", None, ()))

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.conn.events.append(("transaction_exit", None, ()))


class FakeConn:
    def __init__(self) -> None:
        self.events = []
        self._count = 0

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args):
        self._count += 1
        table = _table_name(sql)
        row_id = f"{table}-{self._count}"
        self.events.append(("fetchrow", table, args))
        return {"id": row_id}

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


def _search_response() -> dict:
    return {
        "orderedItems": [
            {
                "id": "https://id.rijksmuseum.nl/200343467",
                "title": "Yellowstone National Park",
                "type": "IMAGE",
            }
        ]
    }


async def test_write_record_creates_m36_substrate_write_path() -> None:
    conn = FakeConn()

    result = await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result == {
        "status": "written",
        "record_id": "https://id.rijksmuseum.nl/200343467",
        "source_item_id": "source_item-1",
        "source_record_id": "source_record-2",
        "media_file_id": "media_file-3",
        "media_rights_id": "media_rights-4",
        "technical_metadata_id": "media_technical_metadata-6",
        "workflow_item_id": None,
        "raw_payload_hash": result["raw_payload_hash"],
        "technical_content_hash": result["technical_content_hash"],
        "writes": 7,
    }
    assert [event[1] for event in conn.events if event[0] in {"fetchrow", "execute"}] == [
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "preservation_event",
        "media_technical_metadata",
        "source_item",
    ]


def test_build_raw_payload_preserves_search_and_oai_context() -> None:
    raw_payload = build_raw_payload(_search_response(), _xml())

    assert raw_payload["search_response"]["orderedItems"][0]["id"] == (
        "https://id.rijksmuseum.nl/200343467"
    )
    assert "GetRecord" in raw_payload["oai_getrecord_xml"]


async def test_write_record_rejects_blocked_rights_before_database_writes() -> None:
    xml = _xml().replace(
        "http://creativecommons.org/publicdomain/mark/1.0/",
        "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    )
    conn = FakeConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "blocked_rights_statement",
        "record_id": "https://id.rijksmuseum.nl/200343467",
        "writes": 0,
    }
    assert conn.events == []


async def test_write_record_rejects_invalid_technical_metadata_before_database_writes() -> None:
    xml = _xml().replace("https://iiif.micr.io/example/full/max/0/default.jpg", "")
    xml = xml.replace("https://www.rijksmuseum.nl/en/collection/RP-F-2001-7-1062", "")
    xml = xml.replace("https://iiif.micr.io/example/full/400,/0/default.jpg", "")
    conn = FakeConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "invalid_technical_metadata",
        "record_id": "https://id.rijksmuseum.nl/200343467",
        "writes": 0,
    }
    assert conn.events == []


async def test_media_rights_payload_records_pending_human_review_evidence() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    media_rights_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "media_rights"
    )
    evidence = json.loads(media_rights_args[2])
    assert evidence["source"] == "rijksmuseum"
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "verified_pd"
    assert evidence["rights_basis"] == "public_domain_mark"
    assert media_rights_args[1] == "https://creativecommons.org/publicdomain/mark/1.0/"


async def test_review_required_rights_enter_pipeline_with_workflow_item() -> None:
    xml = _xml().replace(
        "http://creativecommons.org/publicdomain/mark/1.0/",
        "https://rightsstatements.org/vocab/NoC-OKLR/1.0/",
    )
    conn = FakeConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["workflow_item_id"] == "workflow_items-7"
    assert result["writes"] == 8
    assert [event[1] for event in conn.events if event[0] in {"fetchrow", "execute"}] == [
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "preservation_event",
        "media_technical_metadata",
        "source_item",
        "workflow_items",
    ]


async def test_write_record_serializes_database_uuid_ids_in_json_evidence() -> None:
    class UUIDConn(FakeConn):
        async def fetchrow(self, sql: str, *args):
            self._count += 1
            table = _table_name(sql)
            self.events.append(("fetchrow", table, args))
            return {"id": UUID(f"00000000-0000-0000-0000-{self._count:012d}")}

    conn = UUIDConn()

    result = await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["status"] == "written"
    media_rights_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "media_rights"
    )
    evidence = json.loads(media_rights_args[2])
    assert evidence["source_record_id"] == "00000000-0000-0000-0000-000000000002"
