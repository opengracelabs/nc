"""Replay helpers for shared media adapter tests."""
from __future__ import annotations

from typing import Any

M36_WRITE_ORDER = [
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

M36_REVIEW_REQUIRED_WRITE_ORDER = [
    "BEGIN",
    "source_item",
    "source_record",
    "media_file",
    "media_rights",
    "preservation_event",
    "media_technical_metadata",
    "source_item",
    "workflow_items",
    "COMMIT",
]


def table_name(sql: str) -> str:
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


class _Transaction:
    def __init__(self, conn: ReplayConn) -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.sql_order.append("BEGIN")

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.conn.sql_order.append("COMMIT")


class ReplayConn:
    def __init__(self) -> None:
        self.sql_order: list[str] = []
        self.events: list[tuple[str, str, tuple[Any, ...]]] = []
        self.args_by_table: dict[str, tuple[Any, ...]] = {}
        self._count = 0

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args: Any):
        self._count += 1
        table = table_name(sql)
        row_id = f"{table}-{self._count}"
        self.sql_order.append(table)
        self.events.append(("fetchrow", table, args))
        self.args_by_table[table] = args
        return {"id": row_id}

    async def execute(self, sql: str, *args: Any):
        table = table_name(sql)
        self.sql_order.append(table)
        self.events.append(("execute", table, args))
        self.args_by_table[f"execute:{table}"] = args
        return "UPDATE 1"


REQUIRED_RIGHTS_EVIDENCE_FIELDS = {
    "source",
    "source_record_id",
    "edm_rights_uri",
    "rights_matrix_classification",
    "applying_policy",
    "oai_pmh_identifier",
    "raw_payload_hash",
    "worker_classified_status",
    "evidence_status",
}


def assert_m36_write_order(conn: ReplayConn, *, review_required: bool = False) -> None:
    expected = M36_REVIEW_REQUIRED_WRITE_ORDER if review_required else M36_WRITE_ORDER
    assert conn.sql_order == expected


def assert_no_writes(conn: ReplayConn) -> None:
    assert conn.sql_order == []
    assert conn.events == []


def assert_rights_evidence_contract(evidence: dict[str, Any], *, source: str) -> None:
    assert REQUIRED_RIGHTS_EVIDENCE_FIELDS.issubset(evidence.keys())
    assert evidence["source"] == source
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["rights_matrix_classification"] in {"allowed", "review_required", "blocked"}
    assert isinstance(evidence["raw_payload_hash"], str)
    assert len(evidence["raw_payload_hash"]) == 64
