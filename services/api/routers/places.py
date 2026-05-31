import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..dependencies import DB, Auth

router = APIRouter(prefix="/places", tags=["places"])

_VALID_PLACE_TRANSITIONS: dict[str, set[str]] = {
    "candidate":  {"activate", "delist", "deprecate"},
    "active":     {"endanger", "delist", "deprecate"},
    "endangered": {"activate", "delist", "deprecate"},
    "delisted":   {"deprecate"},
}

_PLACE_ACTION_STATUS = {
    "activate":  "active",
    "endanger":  "endangered",
    "delist":    "delisted",
    "deprecate": "deprecated",
}


class PlaceAction(BaseModel):
    action: str        # activate | endanger | delist | deprecate
    reviewer: str
    reason: str | None = None

_JSON_FIELDS = {
    "name",
    "description",
    "statement_of_ouv",
    "justification",
    "centroid",
    "boundary",
    "agent_notes",
    "provenance",
}

_COLS = """
    id, wikidata_qid, geonames_id, osm_relation_id, source_id, source, unesco_ref_id,
    name, description, statement_of_ouv, justification,
    heritage_type, ouv_criteria, category_skos, transboundary,
    country_codes, continent,
    ST_AsGeoJSON(centroid)::jsonb AS centroid,
    ST_AsGeoJSON(boundary)::jsonb AS boundary,
    area_ha, core_area_ha, buffer_area_ha, spatial_precision,
    inscription_year, inscription_date, endangered_since,
    status, confidence_score, agent_notes, provenance,
    created_at, updated_at
"""


def _decode_row(row) -> dict:
    item = dict(row)
    for field in _JSON_FIELDS:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


def _append_place_filters(
    filters: list[str],
    args: list,
    *,
    status: str | None = None,
    heritage_type: str | None = None,
    country: str | None = None,
    criterion: str | None = None,
    inscription_year: int | None = None,
    q: str | None = None,
) -> None:
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if heritage_type:
        args.append(heritage_type)
        filters.append(f"heritage_type = ${len(args)}")
    if country:
        args.append(country.upper())
        filters.append(f"${len(args)} = ANY(country_codes)")
    if criterion:
        args.append(criterion.lower())
        filters.append(f"${len(args)} = ANY(ouv_criteria)")
    if inscription_year:
        args.append(inscription_year)
        filters.append(f"inscription_year = ${len(args)}")
    if q:
        args.append(f"%{q}%")
        filters.append(
            f"(name::text ILIKE ${len(args)} OR description::text ILIKE ${len(args)})"
        )


async def _fetch_places(
    conn: DB,
    *,
    status: str | None = None,
    heritage_type: str | None = None,
    country: str | None = None,
    criterion: str | None = None,
    inscription_year: int | None = None,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    filters: list[str] = []
    args: list = []
    _append_place_filters(
        filters,
        args,
        status=status,
        heritage_type=heritage_type,
        country=country,
        criterion=criterion,
        inscription_year=inscription_year,
        q=q,
    )

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_COLS} FROM places {where} ORDER BY updated_at DESC"
        f" LIMIT ${len(args)-1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode_row(r) for r in rows]


@router.get("")
async def list_places(
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
    heritage_type: str | None = Query(None),
    country: str | None = Query(None),
    country_code: str | None = Query(None),
    criterion: str | None = Query(None),
    ouv_criterion: str | None = Query(None),
    inscription_year: int | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    return await _fetch_places(
        conn,
        status=status,
        heritage_type=heritage_type,
        country=country or country_code,
        criterion=criterion or ouv_criterion,
        inscription_year=inscription_year,
        limit=limit,
        offset=offset,
    )


@router.get("/search")
async def search_places(
    auth: Auth,
    conn: DB,
    q: str = Query(..., min_length=1),
    country: str | None = Query(None),
    heritage_type: str | None = Query(None),
    criterion: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    return await _fetch_places(
        conn,
        q=q,
        country=country,
        heritage_type=heritage_type,
        criterion=criterion,
        limit=limit,
        offset=offset,
    )


@router.get("/{place_id}")
async def get_place(place_id: UUID, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_COLS} FROM places WHERE id = $1",
        place_id,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Place not found")
    return _decode_row(row)


@router.patch("/{place_id}")
async def act_on_place(
    place_id: UUID,
    body: PlaceAction,
    auth: Auth,
    conn: DB,
) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")

    row = await conn.fetchrow("SELECT status FROM places WHERE id = $1", place_id)
    if not row:
        raise HTTPException(404, "Place not found")

    allowed = _VALID_PLACE_TRANSITIONS.get(row["status"], set())
    if body.action not in allowed:
        raise HTTPException(
            422,
            f"Cannot '{body.action}' a place with status '{row['status']}'. "
            f"Allowed: {sorted(allowed) or 'none'}",
        )

    new_status = _PLACE_ACTION_STATUS[body.action]
    audit = {"action": body.action, "reviewer": body.reviewer, "reason": body.reason}
    await conn.execute(
        """UPDATE places SET
               status = $1,
               agent_notes = agent_notes || $2::jsonb,
               updated_at = NOW()
           WHERE id = $3""",
        new_status,
        json.dumps({"governance": audit}),
        place_id,
    )
    return {"id": str(place_id), "status": new_status, "reviewer": body.reviewer}


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
