"""
Ingestion worker.

Pipeline per approved candidate:
    1. Load candidate from PostgreSQL
    2. Validate
    3. Fetch raw evidence from source
    4. Store raw evidence in MinIO
    5. Insert Place in PostgreSQL

Usage:
    python -m workers.ingestion_worker.main               # continuous poll
    python -m workers.ingestion_worker.main --candidate <uuid>  # single run
"""
import argparse
import asyncio
import json
import logging
import uuid

import asyncpg
from miniopy_async import Minio

from .config import settings
from .fetch import fetch_raw
from .store import insert_place, store_raw_evidence
from .validate import validate_candidate

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("ingestion_worker")

_CANDIDATE_COLS = """
    id, source, source_id, wikidata_qid,
    name, description, country_codes, heritage_type,
    ouv_criteria, inscription_year,
    ST_AsGeoJSON(centroid)::text AS centroid,
    confidence_score, status, promoted_place_id
"""


async def load_candidate(conn: asyncpg.Connection, candidate_id: str) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_CANDIDATE_COLS} FROM discovery_candidates WHERE id = $1",
        candidate_id,
    )
    if not row:
        raise ValueError(f"Candidate not found: {candidate_id}")

    candidate = dict(row)
    # Parse JSONB fields returned as strings by asyncpg
    for field in ("name", "description"):
        if isinstance(candidate[field], str):
            candidate[field] = json.loads(candidate[field])
    if isinstance(candidate.get("centroid"), str):
        candidate["centroid"] = json.loads(candidate["centroid"])
    return candidate


async def load_source_config(conn: asyncpg.Connection, source_id: str) -> dict:
    row = await conn.fetchrow(
        "SELECT config FROM sources WHERE source_id = $1", source_id
    )
    if not row:
        return {}
    cfg = row["config"]
    return json.loads(cfg) if isinstance(cfg, str) else dict(cfg)


async def ingest_candidate(
    conn: asyncpg.Connection,
    minio: Minio,
    candidate_id: str,
) -> str | None:
    ingest_id = str(uuid.uuid4())

    # Step 1 — load candidate
    candidate = await load_candidate(conn, candidate_id)
    log.info("Loaded candidate id=%s source=%s source_id=%s",
             candidate["id"], candidate["source"], candidate["source_id"])

    # Step 2 — validate
    errors = validate_candidate(candidate)
    if errors:
        log.error("Candidate failed validation id=%s errors=%s", candidate_id, errors)
        await conn.execute(
            """
            UPDATE discovery_candidates
            SET status = 'flagged', updated_at = NOW()
            WHERE id = $1
            """,
            candidate_id,
        )
        return None

    # Step 3 — fetch raw evidence
    source_config = await load_source_config(conn, candidate["source"])
    try:
        raw_bytes, source_url = await fetch_raw(
            candidate["source"],
            candidate["source_id"],
            source_config,
        )
    except Exception as exc:
        log.error("Fetch failed candidate_id=%s: %s", candidate_id, exc)
        await conn.execute(
            "UPDATE sources SET last_error = $1 WHERE source_id = $2",
            str(exc), candidate["source"],
        )
        return None

    # Step 4 — store raw evidence in MinIO
    # Use a temporary place_id prefix for the path (real place_id assigned in step 5)
    temp_prefix = str(uuid.uuid4())
    raw_path, checksum = await store_raw_evidence(minio, raw_bytes, temp_prefix, ingest_id)

    # Step 5 — insert Place in PostgreSQL
    place_id = await insert_place(
        conn, candidate, ingest_id, raw_path, checksum, source_url
    )

    return place_id


async def poll_approved_candidates(
    conn: asyncpg.Connection,
    minio: Minio,
    batch_size: int = 10,
) -> int:
    """Claim and process a batch of approved candidates. Returns count processed."""
    rows = await conn.fetch(
        """
        SELECT id FROM discovery_candidates
        WHERE status = 'approved' AND promoted_place_id IS NULL
        ORDER BY discovered_at ASC
        LIMIT $1
        FOR UPDATE SKIP LOCKED
        """,
        batch_size,
    )

    if not rows:
        return 0

    # Mark claimed so other worker instances skip them
    ids = [str(r["id"]) for r in rows]
    await conn.execute(
        "UPDATE discovery_candidates SET status = 'ingesting', updated_at = NOW() WHERE id = ANY($1::uuid[])",
        ids,
    )

    processed = 0
    for candidate_id in ids:
        try:
            place_id = await ingest_candidate(conn, minio, candidate_id)
            if place_id:
                processed += 1
        except Exception as exc:
            log.error("Ingestion error candidate_id=%s: %s", candidate_id, exc, exc_info=True)

    return processed


async def run_once(candidate_id: str) -> None:
    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=3)
    minio = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    async with pool.acquire() as conn:
        place_id = await ingest_candidate(conn, minio, candidate_id)
        if place_id:
            log.info("Done place_id=%s", place_id)
        else:
            log.error("Ingestion produced no Place for candidate_id=%s", candidate_id)
    await pool.close()


async def run_continuous() -> None:
    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=2, max_size=5)
    minio = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    log.info("Ingestion worker polling every %ds", settings.poll_interval_seconds)
    try:
        while True:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    n = await poll_approved_candidates(conn, minio)
            if n:
                log.info("Processed %d candidates", n)
            else:
                await asyncio.sleep(settings.poll_interval_seconds)
    finally:
        await pool.close()


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", help="Ingest a single candidate by UUID")
    args = parser.parse_args()

    if args.candidate:
        await run_once(args.candidate)
    else:
        await run_continuous()


if __name__ == "__main__":
    asyncio.run(main())
