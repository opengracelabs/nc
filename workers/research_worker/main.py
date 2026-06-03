"""Research worker: composes governed research outputs from evidence-backed knowledge."""
import argparse
import asyncio
import logging

import asyncpg

from .compose import build_research_output
from .config import settings
from .store import claim_places_for_research, fetch_research_inputs, upsert_research_output

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("research_worker")


async def process_place(pool: asyncpg.Pool, place: dict) -> bool:
    async with pool.acquire() as conn:
        full_place, facts, relationships = await fetch_research_inputs(conn, place["id"])
        output = build_research_output(
            full_place,
            facts,
            relationships,
            output_version=settings.research_version,
            output_type=settings.research_output_type,
        )
        if output is None:
            log.info("place=%s research_skipped=unsupported", place["id"])
            return False
        output_id = await upsert_research_output(conn, output)
        if output_id is None:
            log.info("place=%s research_skipped=governed_output_exists", place["id"])
            return False
        log.info(
            "place=%s research_output=%s statements=%d",
            place["id"],
            output_id,
            len(output["statements"]),
        )
        return True


async def run_once(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        places = await claim_places_for_research(conn, settings.batch_size)
    written = 0
    for place in places:
        if await process_place(pool, place):
            written += 1
    return written


async def run_continuous(pool: asyncpg.Pool) -> None:
    log.info("Research worker polling every %ds", settings.poll_interval_seconds)
    while True:
        written = await run_once(pool)
        if not written:
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
