"""Taxon discovery worker placeholder.

The network collectors are intentionally separate from ranking so replay tests can
exercise the deterministic commercial ranking without live GBIF/Wikidata calls.
"""
import argparse
import asyncio
import logging

import asyncpg

from .config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("taxon_discovery_worker")


async def run_once(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        places = await conn.fetch(
            "SELECT id FROM places WHERE status = 'active' ORDER BY updated_at LIMIT 0"
        )
    log.info("taxon_discovery_ready places=%d", len(places))
    return 0


async def run_continuous(pool: asyncpg.Pool) -> None:
    log.info("Taxon discovery worker polling every %ds", settings.poll_interval_seconds)
    while True:
        await run_once(pool)
        await asyncio.sleep(settings.poll_interval_seconds)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one batch and exit")
    args = parser.parse_args()

    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=5)
    try:
        if args.once:
            await run_once(pool)
        else:
            await run_continuous(pool)
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
