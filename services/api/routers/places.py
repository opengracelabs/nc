import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from ..dependencies import DB, Auth

router = APIRouter(prefix="/places", tags=["places"])

_JSON_FIELDS = {"name", "description", "centroid", "boundary", "agent_notes", "provenance"}


def _decode_row(row) -> dict:
    item = dict(row)
    for field in _JSON_FIELDS:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item

_COLS = """
    id, wikidata_qid, geonames_id, osm_relation_id, source_id, source,
    name, description, heritage_type, ouv_criteria, category_skos,
    country_codes, continent,
    ST_AsGeoJSON(centroid)::jsonb  AS centroid,
    ST_AsGeoJSON(boundary)::jsonb  AS boundary,
    area_ha, inscription_year, inscription_date, endangered_since,
    status, confidence_score, agent_notes, provenance,
    created_at, updated_at
"""


@router.get("")
async def list_places(
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
    heritage_type: str | None = Query(None),
    country_code: str | None = Query(None),
    ouv_criterion: str | None = Query(None),
    inscription_year: int | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []

    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if heritage_type:
        args.append(heritage_type)
        filters.append(f"heritage_type = ${len(args)}")
    if country_code:
        args.append(country_code)
        filters.append(f"${len(args)} = ANY(country_codes)")
    if ouv_criterion:
        args.append(ouv_criterion)
        filters.append(f"${len(args)} = ANY(ouv_criteria)")
    if inscription_year:
        args.append(inscription_year)
        filters.append(f"inscription_year = ${len(args)}")

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]

    rows = await conn.fetch(
        f"SELECT {_COLS} FROM places {where} ORDER BY updated_at DESC"
        f" LIMIT ${len(args)-1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode_row(r) for r in rows]


@router.get("/{place_id}")
async def get_place(place_id: UUID, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_COLS} FROM places WHERE id = $1", place_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="Place not found")
    return _decode_row(row)


@router.get("/{place_id}/assets")
async def list_place_assets(
    place_id: UUID,
    auth: Auth,
    conn: DB,
    asset_type: str | None = Query(None),
    status: str | None = Query(None),
) -> list[dict]:
    filters = ["place_id = $1"]
    args: list = [place_id]

    if asset_type:
        args.append(asset_type)
        filters.append(f"asset_type = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")

    where = f"WHERE {' AND '.join(filters)}"
    rows = await conn.fetch(
        f"SELECT id, asset_type, mime_type, language, raw_path, normalized_path,"
        f" checksum_sha256, size_bytes, status, validation_warnings,"
        f" source_url, fetched_at, created_at"
        f" FROM assets {where} ORDER BY fetched_at DESC",
        *args,
    )
    return [dict(r) for r in rows]
