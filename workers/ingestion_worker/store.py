"""
Store raw evidence in MinIO and insert the canonical Place in PostgreSQL.
"""
import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
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


async def insert_place(
    conn: asyncpg.Connection,
    candidate: dict[str, Any],
    ingest_id: str,
    raw_path: str,
    checksum: str,
    source_url: str,
) -> str:
    """
    Insert a Place from an approved discovery candidate.
    If a Place already exists for this candidate (promoted_place_id set), skip.
    Returns the place_id.
    """
    # Check if already promoted
    existing_place_id = candidate.get("promoted_place_id")
    if existing_place_id:
        log.info("Candidate already promoted candidate_id=%s place_id=%s",
                 candidate["id"], existing_place_id)
        return str(existing_place_id)

    place_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    centroid_wkt = None
    if c := candidate.get("centroid"):
        if isinstance(c, str):
            import json as _json
            c = _json.loads(c)
        if c and c.get("coordinates"):
            lon, lat = c["coordinates"]
            centroid_wkt = f"SRID=4326;POINT({lon} {lat})"

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
        await conn.execute(
            """
            INSERT INTO places (
                id, wikidata_qid, geonames_id, osm_relation_id,
                source_id, source,
                name, description,
                heritage_type, ouv_criteria,
                country_codes, inscription_year,
                centroid, status, confidence_score,
                provenance
            ) VALUES (
                $1, $2, $3, $4,
                $5, $6,
                $7, $8,
                $9, $10,
                $11, $12,
                ST_GeomFromEWKT($13), 'candidate', $14,
                $15
            )
            """,
            place_id,
            candidate.get("wikidata_qid"),
            None,   # geonames_id resolved in enrichment phase
            None,   # osm_relation_id resolved in enrichment phase
            candidate["source_id"],
            candidate["source"],
            json.dumps(candidate.get("name") or {}),
            json.dumps(candidate.get("description") or {}),
            candidate.get("heritage_type"),
            candidate.get("ouv_criteria") or [],
            candidate.get("country_codes") or [],
            candidate.get("inscription_year"),
            centroid_wkt,
            candidate.get("confidence_score"),
            json.dumps(provenance),
        )

        # Register the asset (raw evidence)
        await conn.execute(
            """
            INSERT INTO assets (
                place_id, source_id, ingest_id,
                asset_type, mime_type,
                raw_path, checksum_sha256, size_bytes,
                status, source_url, fetched_at,
                provenance
            ) VALUES (
                $1, $2, $3,
                'site_record', 'application/json',
                $4, $5, $6,
                'fetched', $7, NOW(),
                $8
            )
            """,
            place_id,
            candidate["source"],
            ingest_id,
            raw_path,
            checksum,
            0,          # size_bytes: set post-store; acceptable here
            source_url,
            json.dumps(provenance),
        )

        # Register ingested_record
        await conn.execute(
            """
            INSERT INTO ingested_records (
                place_id, ingest_id, source,
                status, artifact_count,
                checksum_manifest, provenance
            ) VALUES (
                $1, $2, $3,
                'staged', 1,
                $4, $5
            )
            """,
            place_id,
            ingest_id,
            candidate["source"],
            json.dumps({raw_path: checksum}),
            json.dumps(provenance),
        )

        # Mark candidate as promoted
        await conn.execute(
            """
            UPDATE discovery_candidates
            SET promoted_place_id = $1, updated_at = NOW()
            WHERE id = $2
            """,
            place_id,
            candidate["id"],
        )

    log.info("Inserted place place_id=%s candidate_id=%s", place_id, candidate["id"])
    return place_id
