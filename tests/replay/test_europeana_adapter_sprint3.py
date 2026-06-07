import json
from pathlib import Path

from workers.europeana_adapter.store import write_record

_FIXTURE = Path("tests/fixtures/europeana/yellowstone_launch_metadata_v1_record.json")


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

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args):
        self._count += 1
        table = _table_name(sql)
        self.sql_order.append(table)
        return {"id": f"{table}-{self._count}"}

    async def execute(self, sql: str, *args):
        self.sql_order.append(_table_name(sql))
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


def _yellowstone_payload() -> dict:
    return json.loads(_FIXTURE.read_text())


async def test_europeana_sprint3_replay_is_deterministic_for_same_yellowstone_payload() -> None:
    left_conn = ReplayConn()
    right_conn = ReplayConn()

    left = await write_record(
        left_conn,
        _yellowstone_payload(),
        source_id="source-europeana",
        media_type_id="map",
    )
    right = await write_record(
        right_conn,
        _yellowstone_payload(),
        source_id="source-europeana",
        media_type_id="map",
    )

    assert left["raw_payload_hash"] == right["raw_payload_hash"]
    assert left["technical_content_hash"] == right["technical_content_hash"]
    assert left_conn.sql_order == right_conn.sql_order == [
        "BEGIN",
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "preservation_event",
        "media_technical_metadata",
        "source_item",
        "COMMIT",
    ]


async def test_europeana_sprint3_replay_blocks_uncleared_rights_without_source_record() -> None:
    payload = _yellowstone_payload()
    payload["object"]["rights"] = ["https://creativecommons.org/licenses/by/4.0/"]
    conn = ReplayConn()

    result = await write_record(conn, payload, source_id="source-europeana", media_type_id="map")

    assert result["status"] == "rejected"
    assert result["reason"] == "blocked_rights_statement"
    assert conn.sql_order == []
