"""
Store raw evidence in MinIO and promote a candidate to a canonical Place.
"""
import hashlib
import json
import logging
from datetime import UTC, datetime
from io import BytesIO
from typing import Any

import asyncpg
from miniopy_async import Minio

from .config import settings

log = logging.getLogger(__name__)


def _raw_path(place_id: str, ingest_id: str) -> str:
    return f"ingestion/{place_id}/{ingest_id}/source_record.json"


async def store_raw_evidence(
    minio: Minio,
    raw_bytes: bytes,
    place_id: str,
    ingest_id: str,
) -> tuple[str, str]:
    """Write raw bytes to MinIO. Returns (path, sha256)."""
    path = _raw_path(place_id, ingest_id)
    checksum = hashlib.sha256(raw_bytes).hexdigest()
    await minio.put_object(
        bucket_name=settings.minio_bucket_raw,
        object_name=path,
        data=BytesIO(raw_bytes),
        length=len(raw_bytes),
        content_type="application/json",
    )
    log.info("Stored raw evidence path=%s sha256=%s", path, checksum[:12])
    return path, checksum


def _centroid_wkt(candidate: dict[str, Any]) -> str | None:
    centroid = candidate.get("centroid")
    if isinstance(centroid, str):
        centroid = json.loads(centroid)
    if not centroid or not centroid.get("coordinates"):
        return None
    lon, lat = centroid["coordinates"]
    return f"SRID=4326;POINT({lon} {lat})"


async def insert_place(
    conn: asyncpg.Connection,
    candidate: dict[str, Any],
    ingest_id: str,
    place_id: str,
    raw_path: str,
    checksum: str,
    source_url: str,
    size_bytes: int,
) -> str:
    """
    Promote an approved discovery candidate to a canonical Place.

    All writes are inside one transaction. The candidate row is locked first
    so concurrent worker instances cannot produce duplicate places.
    """
    now = datetime.now(UTC).isoformat()
    centroid_wkt = _centroid_wkt(candidate)

    provenance = {
        "prov:wasGeneratedBy": {
            "prov:type": "ingestion_worker",
            "nc:candidate_id": str(candidate["id"]),
            "nc:ingest_id": ingest_id,
            "nc:source": candidate["source"],
            "nc:source_id": candidate["source_id"],
            "nc:raw_path": raw_path,
            "nc:checksum_sha256": checksum,
            "nc:source_url": source_url,
            "prov:generatedAtTime": now,
        }
    }

    async with conn.transaction():
        # Lock the candidate row — prevents duplicate promotion under concurrent workers.
        locked = await conn.fetchrow(
            "SELECT promoted_place_id FROM discovery_candidates WHERE id = $1 FOR UPDATE",
            candidate["id"],
        )
        if not locked:
            raise ValueError(f"Candidate disappeared during promotion: {candidate['id']}")
        if locked["promoted_place_id"]:
            log.info(
                "Candidate already promoted candidate_id=%s place_id=%s",
                candidate["id"], locked["promoted_place_id"],
            )
            return str(locked["promoted_place_id"])

        await conn.execute(
            """
            INSERT INTO places (
                id, wikidata_qid, source_id, source, unesco_ref_id,
                name, description, statement_of_ouv, justification,
                heritage_type, ouv_criteria, transboundary,
                country_codes, inscription_year,
                centroid, core_area_ha, buffer_area_ha, spatial_precision,
                status, confidence_score, provenance
            ) VALUES (
                $1, $2, $3, $4, $5,
                $6, $7, $8, $9,
                $10, $11, $12,
                $13, $14,
                ST_GeomFromEWKT($15), $16, $17, $18,
                'candidate', $19, $20
            )
            """,
            place_id,
            candidate.get("wikidata_qid"),
            candidate["source_id"],
            candidate["source"],
            candidate.get("unesco_ref_id"),
            json.dumps(candidate.get("name") or {}),
            json.dumps(candidate.get("description") or {}),
            json.dumps(candidate.get("statement_of_ouv") or {}),
            json.dumps(candidate.get("justification") or {}),
            candidate.get("heritage_type"),
            candidate.get("ouv_criteria") or [],
            candidate.get("transboundary") or False,
            candidate.get("country_codes") or [],
            candidate.get("inscription_year"),
            centroid_wkt,
            candidate.get("core_area_ha"),
            candidate.get("buffer_area_ha"),
            candidate.get("spatial_precision"),
            candidate.get("confidence_score"),
            json.dumps(provenance),
        )

        await conn.execute(
            """
            INSERT INTO assets (
                place_id, source_id, ingest_id,
                asset_type, mime_type,
                raw_path, checksum_sha256, size_bytes,
                status, source_url, fetched_at,
                premis_object_id, premis_original_name, premis_creating_application,
                provenance
            ) VALUES (
                $1, $2, $3,
                'site_record', 'application/json',
                $4, $5, $6,
                'fetched', $7, NOW(),
                $8, $9, 'ingestion_worker/0.1.0',
                $10
            )
            """,
            place_id,
            candidate["source"],
            ingest_id,
            raw_path,
            checksum,
            size_bytes,
            source_url,
            ingest_id,
            f"{candidate['source']}_{candidate['source_id']}.json",
            json.dumps(provenance),
        )

        await conn.execute(
            """
            INSERT INTO ingested_records (
                place_id, ingest_id, source,
                status, artifact_count, provenance
            ) VALUES ($1, $2, $3, 'staged', 1, $4)
            """,
            place_id,
            ingest_id,
            candidate["source"],
            json.dumps(provenance),
        )

        await conn.execute(
            """
            UPDATE discovery_candidates
            SET promoted_place_id = $1, status = 'promoted', updated_at = NOW()
            WHERE id = $2
            """,
            place_id,
            candidate["id"],
        )

    log.info("Promoted candidate_id=%s → place_id=%s", candidate["id"], place_id)
    return place_id
