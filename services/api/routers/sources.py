
import json

from fastapi import APIRouter, HTTPException, Query

from ..dependencies import DB, Auth

router = APIRouter(prefix="/sources", tags=["sources"])

_JSON_FIELDS = {"rate_limit", "config"}


def _decode_row(row) -> dict:
    item = dict(row)
    for field in _JSON_FIELDS:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item

_COLS = """
    id, source_id, name, description, institution, base_url,
    fetch_strategy, auth_type, rate_limit, entity_types, standards,
    status, priority, schema_version, last_fetched_at, last_error,
    config, created_at, updated_at
"""


@router.get("")
async def list_sources(
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
    fetch_strategy: str | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []

    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if fetch_strategy:
        args.append(fetch_strategy)
        filters.append(f"fetch_strategy = ${len(args)}")

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]

    rows = await conn.fetch(
        f"SELECT {_COLS} FROM sources {where} ORDER BY priority, source_id"
        f" LIMIT ${len(args)-1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode_row(r) for r in rows]


@router.get("/{source_id}")
async def get_source(source_id: str, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_COLS} FROM sources WHERE source_id = $1", source_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="Source not found")
    return _decode_row(row)
