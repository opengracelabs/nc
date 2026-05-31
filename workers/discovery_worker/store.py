import json
import logging
from io import BytesIO
from typing import Any

import asyncpg

log = logging.getLogger(__name__)


async def upsert_candidate(conn: asyncpg.Connection, record: dict[str, Any]) -> tuple[str, bool]:
    """
    Insert or update a discovery candidate.
    Returns (id, created) where created=False means an existing record was updated.

    PostgreSQL owns the concurrency boundary via UNIQUE (source, source_id),
    so parallel discovery workers cannot race between SELECT and INSERT.
    """
    centroid_wkt = None
    if c := record.get("centroid"):
        lon, lat = c["coordinates"]
        centroid_wkt = f"SRID=4326;POINT({lon} {lat})"

    row = await conn.fetchrow(
        """
        INSERT INTO discovery_candidates (
            source, source_id, wikidata_qid,
            name, description, country_codes,
            heritage_type, ouv_criteria, inscription_year,
            centroid, confidence_score, provenance,
            status
        ) VALUES (
            $1, $2, $3,
            $4, $5, $6,
            $7, $8, $9,
            ST_GeomFromEWKT($10), $11, $12,
            'pending'
        )
        ON CONFLICT (source, source_id) DO UPDATE SET
            wikidata_qid     = EXCLUDED.wikidata_qid,
            name             = EXCLUDED.name,
            description      = EXCLUDED.description,
            country_codes    = EXCLUDED.country_codes,
            heritage_type    = EXCLUDED.heritage_type,
            ouv_criteria     = EXCLUDED.ouv_criteria,
            inscription_year = EXCLUDED.inscription_year,
            centroid         = EXCLUDED.centroid,
            confidence_score = EXCLUDED.confidence_score,
            provenance       = EXCLUDED.provenance,
            updated_at       = NOW()
        RETURNING id, (xmax = 0) AS created
        """,
        record["source"],
        record["source_id"],
        record.get("wikidata_qid"),
        json.dumps(record.get("name", {})),
        json.dumps(record.get("description", {})),
        record.get("country_codes") or [],
        record.get("heritage_type"),
        record.get("ouv_criteria") or [],
        record.get("inscription_year"),
        centroid_wkt,
        record.get("confidence_score"),
        json.dumps(record.get("provenance", {})),
    )
    created = bool(row["created"])
    action = "Created" if created else "Updated"
    log.debug("%s candidate source=%s source_id=%s", action, record["source"], record["source_id"])
    return str(row["id"]), created


async def store_raw(
    minio_client: Any,
    bucket: str,
    source: str,
    run_id: str,
    raw_bytes: bytes,
) -> str:
    path = f"discovery/{source}/{run_id}/response.json"
    await minio_client.put_object(
        bucket_name=bucket,
        object_name=path,
        data=BytesIO(raw_bytes),
        length=len(raw_bytes),
        content_type="application/json",
    )
    return path
