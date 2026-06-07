"""Europeana adapter live retrieval entry point."""
from __future__ import annotations

import argparse
import asyncio
import json
from typing import TYPE_CHECKING, Any

import asyncpg

from . import client
from .config import settings
from .store import write_record

if TYPE_CHECKING:
    from types import TracebackType

YELLOWSTONE_RECORD_ID = "/9200518/ark__12148_btv1b530248434"
YELLOWSTONE_MEDIA_TYPE_ID = "map"
SOURCE_ID = "europeana"


class _DryRunTransaction:
    def __init__(self, conn: DryRunConnection) -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.events.append({"operation": "transaction", "table": None, "phase": "begin"})

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.conn.events.append({"operation": "transaction", "table": None, "phase": "commit"})


class DryRunConnection:
    """Async connection double that records the SQL write path for live dry-runs."""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self._count = 0

    def transaction(self) -> _DryRunTransaction:
        return _DryRunTransaction(self)

    async def fetchrow(self, sql: str, *args: Any) -> dict[str, str]:
        self._count += 1
        table = _table_name(sql)
        row_id = f"{table}-{self._count}"
        self.events.append({"operation": "fetchrow", "table": table, "id": row_id})
        return {"id": row_id}

    async def execute(self, sql: str, *args: Any) -> str:
        self.events.append({"operation": "execute", "table": _table_name(sql), "id": None})
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


async def fetch_live_asset(record_id: str = YELLOWSTONE_RECORD_ID) -> dict[str, Any]:
    """Fetch one full Europeana record from the Record API."""
    return await client.fetch_record(record_id)


async def ingest_live_asset(
    *,
    record_id: str = YELLOWSTONE_RECORD_ID,
    source_id: str = SOURCE_ID,
    media_type_id: str = YELLOWSTONE_MEDIA_TYPE_ID,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Fetch one live Europeana asset and run the M36 substrate write path."""
    raw_payload = await fetch_live_asset(record_id)

    if dry_run:
        conn = DryRunConnection()
        result = await write_record(
            conn,
            raw_payload,
            source_id=source_id,
            media_type_id=media_type_id,
        )
        return {"mode": "dry_run", "result": result, "events": conn.events}

    conn = await asyncpg.connect(settings.postgres_dsn)
    try:
        result = await write_record(
            conn,
            raw_payload,
            source_id=source_id,
            media_type_id=media_type_id,
        )
        return {"mode": "write", "result": result, "events": []}
    finally:
        await conn.close()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and ingest one Europeana record")
    parser.add_argument(
        "command",
        choices=("fetch-yellowstone", "ingest-record"),
        help="Live Europeana command to run",
    )
    parser.add_argument("--record-id", default=YELLOWSTONE_RECORD_ID)
    parser.add_argument("--source-id", default=SOURCE_ID)
    parser.add_argument("--media-type-id", default=YELLOWSTONE_MEDIA_TYPE_ID)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write to PostgreSQL instead of dry-run",
    )
    return parser


async def _run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "fetch-yellowstone":
        raw_payload = await fetch_live_asset(YELLOWSTONE_RECORD_ID)
        return {"mode": "fetch", "record_id": YELLOWSTONE_RECORD_ID, "raw_payload": raw_payload}

    return await ingest_live_asset(
        record_id=args.record_id,
        source_id=args.source_id,
        media_type_id=args.media_type_id,
        dry_run=not args.write,
    )


def main() -> None:
    args = _parser().parse_args()
    result = asyncio.run(_run(args))
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
