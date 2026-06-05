"""Collections API: governed commercial groupings of verified assets."""

import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from workers.collection_export_worker.export import build_collection_export_manifest

from ..dependencies import DB, Auth

router = APIRouter(prefix="/collections", tags=["collections"])

_COLLECTION_COLS = """
    id, slug, title, summary, collection_type, status, reviewed_by, reviewed_at,
    published_at, export_version, provenance, agent_notes, created_at, updated_at
"""

_COLLECTION_LIST_COLS = """
    c.id, c.slug, c.title, c.summary, c.collection_type, c.status, c.reviewed_by,
    c.reviewed_at, c.published_at, c.export_version, c.provenance, c.agent_notes,
    c.created_at, c.updated_at
"""

_ASSET_COLS = """
    ca.id, ca.collection_id, ca.asset_id, ca.opportunity_id, ca.sequence, ca.role,
    ca.title, ca.caption, ca.credit_line, ca.provenance, ca.created_at, ca.updated_at,
    a.asset_type, a.status AS asset_status, a.raw_path, a.normalized_path,
    a.checksum_sha256, ar.rights_status, ar.rights_source_url,
    io.source_url, io.bhl_page_id
"""

_PLACE_COLS = """
    cp.id, cp.collection_id, cp.place_id, cp.role, cp.provenance, cp.created_at,
    p.name
"""

_EXPORT_COLS = """
    id, collection_id, export_format, export_path, checksum_sha256, size_bytes,
    status, created_by, provenance, created_at
"""

_JSON_DECODE = {"provenance", "agent_notes", "name"}

_TRANSITIONS = {
    "approve": ("approved", {"draft"}),
    "publish": ("published", {"approved"}),
    "reject": ("rejected", {"draft"}),
    "dispute": ("disputed", {"approved", "published"}),
    "retract": ("retracted", {"disputed"}),
}


class CollectionAction(BaseModel):
    action: str
    reviewer: str
    reason: str | None = None


class CollectionExportRequest(BaseModel):
    created_by: str


def _decode(row) -> dict:
    item = dict(row)
    for field in _JSON_DECODE:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


async def _collection_detail(conn: DB, collection_id: UUID) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_COLLECTION_COLS} FROM collections WHERE id = $1",
        collection_id,
    )
    if not row:
        raise HTTPException(404, "Collection not found")
    collection = _decode(row)
    assets = await conn.fetch(
        f"""
        SELECT {_ASSET_COLS}
        FROM collection_assets ca
        JOIN assets a ON a.id = ca.asset_id
        JOIN asset_rights ar ON ar.asset_id = a.id
        LEFT JOIN illustration_opportunities io ON io.id = ca.opportunity_id
        WHERE ca.collection_id = $1
        ORDER BY ca.sequence, ca.asset_id
        """,
        collection_id,
    )
    places = await conn.fetch(
        f"""
        SELECT {_PLACE_COLS}
        FROM collection_places cp
        JOIN places p ON p.id = cp.place_id
        WHERE cp.collection_id = $1
        ORDER BY cp.role, cp.place_id
        """,
        collection_id,
    )
    exports = await conn.fetch(
        f"SELECT {_EXPORT_COLS} FROM collection_exports WHERE collection_id = $1 "
        "ORDER BY created_at DESC",
        collection_id,
    )
    collection["assets"] = [_decode(asset) for asset in assets]
    collection["places"] = [_decode(place) for place in places]
    collection["exports"] = [_decode(export) for export in exports]
    return collection


@router.get("")
async def list_collections(
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
    place_id: UUID | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []
    join = ""
    if status:
        args.append(status)
        filters.append(f"c.status = ${len(args)}")
    if place_id:
        join = "JOIN collection_places cp ON cp.collection_id = c.id"
        args.append(place_id)
        filters.append(f"cp.place_id = ${len(args)}")
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT DISTINCT {_COLLECTION_LIST_COLS} FROM collections c {join} {where} "
        f"ORDER BY c.updated_at DESC LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(row) for row in rows]


@router.get("/{collection_id}")
async def get_collection(collection_id: UUID, auth: Auth, conn: DB) -> dict:
    return await _collection_detail(conn, collection_id)


@router.patch("/{collection_id}")
async def act_on_collection(
    collection_id: UUID,
    body: CollectionAction,
    auth: Auth,
    conn: DB,
) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")
    if body.action not in _TRANSITIONS:
        raise HTTPException(422, f"action must be one of: {sorted(_TRANSITIONS)}")
    if body.action in {"reject", "dispute", "retract"} and not body.reason:
        raise HTTPException(422, f"reason is required for {body.action}")

    new_status, allowed_from = _TRANSITIONS[body.action]
    audit = {"action": body.action, "reviewer": body.reviewer, "reason": body.reason}
    async with conn.transaction():
        row = await conn.fetchrow(
            "SELECT status FROM collections WHERE id = $1 FOR UPDATE",
            collection_id,
        )
        if not row:
            raise HTTPException(404, "Collection not found")
        if row["status"] not in allowed_from:
            raise HTTPException(
                422,
                f"Cannot '{body.action}' a collection with status '{row['status']}'. "
                f"Allowed from: {sorted(allowed_from)}",
            )
        await conn.execute(
            """
            UPDATE collections
            SET status = $1,
                reviewed_by = $2,
                reviewed_at = NOW(),
                published_at = CASE WHEN $1 = 'published' THEN NOW() ELSE published_at END,
                agent_notes = agent_notes || $3::jsonb,
                updated_at = NOW()
            WHERE id = $4
            """,
            new_status,
            body.reviewer,
            json.dumps({"governance": audit}),
            collection_id,
        )
    return {"id": str(collection_id), "status": new_status, "reviewed_by": body.reviewer}


@router.post("/{collection_id}/exports/manifest")
async def create_collection_manifest_export(
    collection_id: UUID,
    body: CollectionExportRequest,
    auth: Auth,
    conn: DB,
) -> dict:
    if not body.created_by.strip():
        raise HTTPException(422, "created_by is required")

    collection = await _collection_detail(conn, collection_id)
    if collection["status"] not in {"approved", "published"}:
        raise HTTPException(422, "collection must be approved or published before export")
    if not collection["assets"]:
        raise HTTPException(422, "collection has no assets to export")

    manifest = build_collection_export_manifest(
        collection,
        collection["assets"],
        collection["places"],
    )
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    export_path = (
        f"exports/collections/{collection_id}/manifest-"
        f"{manifest['checksum_sha256']}.json"
    )
    row = await conn.fetchrow(
        """
        INSERT INTO collection_exports (
            collection_id, export_format, export_path, checksum_sha256,
            size_bytes, created_by, provenance
        ) VALUES ($1, 'manifest_json', $2, $3, $4, $5, $6::jsonb)
        ON CONFLICT (collection_id, export_format, checksum_sha256)
        DO UPDATE SET status = collection_exports.status
        RETURNING id
        """,
        collection_id,
        export_path,
        manifest["checksum_sha256"],
        len(encoded),
        body.created_by,
        json.dumps(manifest["provenance"]),
    )
    return {
        "id": str(row["id"]),
        "collection_id": str(collection_id),
        "export_path": export_path,
        "checksum_sha256": manifest["checksum_sha256"],
        "size_bytes": len(encoded),
        "manifest": manifest,
    }
