"""
Discovery worker entry point.

Usage:
    python -m workers.discovery_worker.main --source unesco_whc
    python -m workers.discovery_worker.main --source wikidata
    python -m workers.discovery_worker.main --all
"""
import argparse
import asyncio
import json
import logging
import uuid
from datetime import UTC, datetime

import asyncpg
from miniopy_async import Minio

from .config import settings
from .normalize import normalize
from .score import score
from .sources import REGISTRY
from .store import store_raw, upsert_candidate

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("discovery_worker")


def _build_provenance(source: str, run_id: str, source_id: str) -> dict:
    return {
        "prov:wasGeneratedBy": {
            "prov:type": "discovery_worker",
            "nc:source": source,
            "nc:run_id": run_id,
            "nc:source_id": source_id,
            "prov:startedAtTime": datetime.now(UTC).isoformat(),
        }
    }


async def read_source(conn: asyncpg.Connection, source_id: str) -> dict:
    row = await conn.fetchrow(
        "SELECT source_id, config, status FROM sources WHERE source_id = $1",
        source_id,
    )
    if not row:
        raise ValueError(f"Source not registered: {source_id}")
    if row["status"] not in ("active", "degraded"):
        raise ValueError(f"Source {source_id} is {row['status']} — skipping")
    config = json.loads(row["config"]) if isinstance(row["config"], str) else dict(row["config"])
    log.info("Loaded source config source=%s", source_id)
    return config


async def run_discovery(source_id: str) -> None:
    fetcher = REGISTRY.get(source_id)
    if not fetcher:
        raise ValueError(f"No fetcher registered for: {source_id}")

    run_id = str(uuid.uuid4())
    log.info("Starting discovery run source=%s run_id=%s", source_id, run_id)

    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=5)
    minio = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )

    async with pool.acquire() as conn:
        # 1. Read source config from PostgreSQL
        config = await read_source(conn, source_id)

        # 2. Fetch records from source
        result = await fetcher.fetch(config, run_id)
        log.info(
            "Fetched source=%s total=%d errors=%d",
            source_id,
            result.total,
            len(result.errors),
        )

        # 3. Store raw response in MinIO
        raw_path = await store_raw(
            minio,
            settings.minio_bucket_raw,
            source_id,
            run_id,
            result.raw_bytes,
        )
        log.info("Stored raw response path=%s", raw_path)

        # 4. Normalize, score, and store each record as a discovery candidate
        created = updated = skipped = failed = 0

        for raw_record in result.records:
            try:
                normalized = normalize(source_id, raw_record)
                normalized["confidence_score"] = score(normalized)
                normalized["provenance"] = _build_provenance(
                    source_id,
                    run_id,
                    raw_record.source_id,
                )

                candidate_id, is_new = await upsert_candidate(conn, normalized)
                if settings.discovery_auto_approve:
                    await conn.execute(
                        """
                        UPDATE discovery_candidates
                        SET status = 'approved', updated_at = NOW()
                        WHERE id = $1 AND status IN ('pending', 'approved')
                        """,
                        candidate_id,
                    )

                if is_new:
                    created += 1
                    log.debug("Created candidate id=%s", candidate_id)
                else:
                    # upsert_candidate returns False for both updated and unchanged
                    updated += 1

            except Exception as exc:
                log.error("Failed to process record source_id=%s: %s", raw_record.source_id, exc)
                failed += 1

        # 5. Update source fetch state
        if result.errors:
            await conn.execute(
                """
                UPDATE sources
                SET last_fetched_at = NOW(), last_error = $2, updated_at = NOW()
                WHERE source_id = $1
                """,
                source_id,
                "; ".join(result.errors),
            )
        else:
            await conn.execute(
                """
                UPDATE sources
                SET last_fetched_at = NOW(), last_error = NULL, updated_at = NOW()
                WHERE source_id = $1
                """,
                source_id,
            )

    await minio.close_session()
    await pool.close()

    log.info(
        "Discovery run complete source=%s run_id=%s created=%d updated=%d skipped=%d failed=%d",
        source_id, run_id, created, updated, skipped, failed,
    )


async def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source", help="Run discovery for a single source")
    group.add_argument(
        "--all",
        action="store_true",
        help="Run discovery for all registered sources",
    )
    args = parser.parse_args()

    sources = list(REGISTRY.keys()) if args.all else [args.source]
    for source_id in sources:
        try:
            await run_discovery(source_id)
        except Exception as exc:
            log.error("Discovery run failed source=%s: %s", source_id, exc)


if __name__ == "__main__":
    asyncio.run(main())
