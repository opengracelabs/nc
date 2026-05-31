"""
Ingestion worker.

Pipeline per approved candidate:
    1. Claim approved candidates in PostgreSQL
    2. Load and validate the claimed candidate
    3. Fetch raw evidence from source outside database transactions
    4. Store raw evidence in MinIO
    5. Promote the candidate to a canonical Place in PostgreSQL

Usage:
    python -m workers.ingestion_worker.main
    python -m workers.ingestion_worker.main --candidate <uuid>
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
    id, source, source_id, wikidata_qid, unesco_ref_id,
    name, description, statement_of_ouv, justification,
    country_codes, heritage_type, transboundary,
    ouv_criteria, inscription_year,
    ST_AsGeoJSON(centroid)::text AS centroid,
    core_area_ha, buffer_area_ha, spatial_precision,
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
    for field in ("name", "description", "statement_of_ouv", "justification"):
        if field in candidate and candidate[field] and isinstance(candidate[field], str):
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


async def mark_candidate_status(
    conn: asyncpg.Connection,
    candidate_id: str,
    status: str,
    status_reason: str | None = None,
) -> None:
    await conn.execute(
        """
        UPDATE discovery_candidates
        SET status = $2, agent_suggestions = agent_suggestions || $3::jsonb, updated_at = NOW()
        WHERE id = $1
        """,
        candidate_id,
        status,
        json.dumps({"status_reason": status_reason} if status_reason else {}),
    )


async def ingest_candidate(
    conn: asyncpg.Connection,
    minio: Minio,
    candidate_id: str,
) -> str | None:
    ingest_id = str(uuid.uuid4())
    place_id = str(uuid.uuid4())

    candidate = await load_candidate(conn, candidate_id)
    log.info(
        "Loaded candidate id=%s source=%s source_id=%s",
        candidate["id"],
        candidate["source"],
        candidate["source_id"],
    )

    errors = validate_candidate(candidate)
    if errors:
        message = "; ".join(errors)
        log.error("Candidate failed validation id=%s errors=%s", candidate_id, errors)
        await mark_candidate_status(conn, candidate_id, "flagged", message)
        return None

    source_config = await load_source_config(conn, candidate["source"])
    try:
        raw_bytes, source_url = await fetch_raw(
            candidate["source"],
            candidate["source_id"],
            source_config,
        )
    except Exception as exc:
        log.error("Fetch failed candidate_id=%s: %s", candidate_id, exc)
        await mark_candidate_status(conn, candidate_id, "approved", f"fetch failed: {exc}")
        await conn.execute(
            "UPDATE sources SET last_error = $1, updated_at = NOW() WHERE source_id = $2",
            str(exc),
            candidate["source"],
        )
        return None

    raw_path, checksum = await store_raw_evidence(minio, raw_bytes, place_id, ingest_id)

    return await insert_place(
        conn,
        candidate,
        ingest_id,
        place_id,
        raw_path,
        checksum,
        source_url,
        len(raw_bytes),
    )


async def reset_stale_ingesting(
    conn: asyncpg.Connection,
    timeout_seconds: int | None = None,
) -> int:
    """Return stale claimed candidates to the approved queue."""
    timeout = timeout_seconds or settings.ingesting_timeout_seconds
    result = await conn.execute(
        """
        UPDATE discovery_candidates
        SET status = 'approved', updated_at = NOW()
        WHERE status = 'ingesting'
          AND promoted_place_id IS NULL
          AND updated_at < NOW() - ($1::int * interval '1 second')
        """,
        timeout,
    )
    return int(result.rsplit(" ", 1)[-1])


async def claim_approved_candidates(
    conn: asyncpg.Connection,
    batch_size: int = 10,
) -> list[str]:
    """Claim approved candidates in one short database statement."""
    rows = await conn.fetch(
        """
        WITH next_candidates AS (
            SELECT id
            FROM discovery_candidates
            WHERE status = 'approved' AND promoted_place_id IS NULL
            ORDER BY discovered_at ASC
            LIMIT $1
            FOR UPDATE SKIP LOCKED
        )
        UPDATE discovery_candidates AS dc
        SET status = 'ingesting', updated_at = NOW()
        FROM next_candidates
        WHERE dc.id = next_candidates.id
        RETURNING dc.id
        """,
        batch_size,
    )
    return [str(r["id"]) for r in rows]


async def poll_approved_candidates(
    pool: asyncpg.Pool,
    minio: Minio,
    batch_size: int = 10,
) -> int:
    """Claim and process a batch of approved candidates. Returns count processed."""
    async with pool.acquire() as conn:
        await reset_stale_ingesting(conn)
        ids = await claim_approved_candidates(conn, batch_size)

    if not ids:
        return 0

    processed = 0
    for candidate_id in ids:
        try:
            async with pool.acquire() as conn:
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
    await minio.close_session()
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
            n = await poll_approved_candidates(pool, minio)
            if n:
                log.info("Processed %d candidates", n)
            else:
                await asyncio.sleep(settings.poll_interval_seconds)
    finally:
        await minio.close_session()
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
