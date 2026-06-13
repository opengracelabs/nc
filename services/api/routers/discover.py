import json

from fastapi import APIRouter, HTTPException, Query

from ..dependencies import DB

router = APIRouter(prefix="/discover", tags=["discover"])

_SPATIAL_SELECT = """
    p.slug,
    p.name,
    p.place_type,
    p.region_slug,
    ST_AsGeoJSON(p.centroid)::jsonb AS centroid,
    ST_AsGeoJSON(p.geom)::jsonb AS geometry
"""


async def _place_exists(conn: DB, slug: str) -> bool:
    return bool(await conn.fetchval("SELECT 1 FROM place_geometry WHERE slug = $1", slug))


def _decode_spatial_row(row) -> dict:
    item = dict(row)
    for field in ("centroid", "geometry"):
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


@router.get("/nearby")
async def nearby_places(
    conn: DB,
    slug: str = Query(..., min_length=1),
    radius_km: float = Query(1500, gt=0, le=20000),
    limit: int = Query(10, ge=1, le=50),
) -> dict:
    if not await _place_exists(conn, slug):
        raise HTTPException(status_code=404, detail="Place geometry not found")

    rows = await conn.fetch(
        f"""
        SELECT
            target.slug,
            target.name,
            target.place_type,
            target.region_slug,
            ST_Distance(origin.centroid::geography, target.centroid::geography) / 1000
                AS distance_km,
            ST_AsGeoJSON(target.centroid)::jsonb AS centroid
        FROM place_geometry origin
        JOIN place_geometry target ON target.slug <> origin.slug
        WHERE origin.slug = $1
          AND ST_DWithin(origin.centroid::geography, target.centroid::geography, $2 * 1000)
        ORDER BY distance_km ASC
        LIMIT $3
        """,
        slug,
        radius_km,
        limit,
    )
    return {
        "slug": slug,
        "radius_km": radius_km,
        "places": [_decode_spatial_row(row) for row in rows],
    }


@router.get("/within-region")
async def places_within_region(
    conn: DB,
    region_slug: str | None = Query(None, min_length=1),
    slug: str | None = Query(None, min_length=1),
    limit: int = Query(50, ge=1, le=100),
) -> dict:
    if not region_slug and not slug:
        raise HTTPException(status_code=422, detail="region_slug or slug is required")

    if slug and not region_slug:
        row = await conn.fetchrow(
            """
            SELECT r.slug, r.name
            FROM place_geometry p
            JOIN region_geometry r ON ST_Within(p.centroid, r.geom)
            WHERE p.slug = $1
            ORDER BY r.slug
            LIMIT 1
            """,
            slug,
        )
        if not row:
            raise HTTPException(status_code=404, detail="Containing region not found")
        region_slug = row["slug"]

    region = await conn.fetchrow(
        """
        SELECT slug, name, region_type, ST_AsGeoJSON(geom)::jsonb AS geometry
        FROM region_geometry
        WHERE slug = $1
        """,
        region_slug,
    )
    if not region:
        raise HTTPException(status_code=404, detail="Region geometry not found")

    rows = await conn.fetch(
        f"""
        SELECT {_SPATIAL_SELECT}
        FROM place_geometry p
        JOIN region_geometry r ON r.slug = $1
        WHERE ST_Within(p.centroid, r.geom)
        ORDER BY p.name
        LIMIT $2
        """,
        region_slug,
        limit,
    )
    return {
        "region": _decode_spatial_row(region),
        "places": [_decode_spatial_row(row) for row in rows],
    }


@router.get("/intersects")
async def intersects(
    conn: DB,
    slug: str = Query(..., min_length=1),
    target: str = Query("protected_area", pattern="^(protected_area|region|place)$"),
    limit: int = Query(50, ge=1, le=100),
) -> dict:
    if not await _place_exists(conn, slug):
        raise HTTPException(status_code=404, detail="Place geometry not found")

    if target == "protected_area":
        rows = await conn.fetch(
            """
            SELECT
                pa.slug,
                pa.name,
                pa.protected_type AS type,
                pa.place_slug,
                ST_Area(pa.geom::geography) / 1000000 AS area_km2,
                ST_AsGeoJSON(pa.geom)::jsonb AS geometry
            FROM place_geometry p
            JOIN protected_area_geometry pa ON ST_Intersects(p.geom, pa.geom)
            WHERE p.slug = $1
            ORDER BY pa.name
            LIMIT $2
            """,
            slug,
            limit,
        )
    elif target == "region":
        rows = await conn.fetch(
            """
            SELECT
                r.slug,
                r.name,
                r.region_type AS type,
                NULL::text AS place_slug,
                ST_Area(r.geom::geography) / 1000000 AS area_km2,
                ST_AsGeoJSON(r.geom)::jsonb AS geometry
            FROM place_geometry p
            JOIN region_geometry r ON ST_Intersects(p.geom, r.geom)
            WHERE p.slug = $1
            ORDER BY r.name
            LIMIT $2
            """,
            slug,
            limit,
        )
    else:
        rows = await conn.fetch(
            """
            SELECT
                p2.slug,
                p2.name,
                p2.place_type AS type,
                p2.slug AS place_slug,
                ST_Area(p2.geom::geography) / 1000000 AS area_km2,
                ST_AsGeoJSON(p2.geom)::jsonb AS geometry
            FROM place_geometry p1
            JOIN place_geometry p2 ON p2.slug <> p1.slug AND ST_Intersects(p1.geom, p2.geom)
            WHERE p1.slug = $1
            ORDER BY p2.name
            LIMIT $2
            """,
            slug,
            limit,
        )

    return {
        "slug": slug,
        "target": target,
        "intersections": [_decode_spatial_row(row) for row in rows],
    }
