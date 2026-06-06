"""Commerce Opportunity Worker entry point."""
from __future__ import annotations

import argparse
import asyncio
import logging

import asyncpg

from .config import settings
from .store import claim_approved_opportunities, score_opportunity

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("commerce_opportunity_worker")


async def run_once(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        opportunities = await claim_approved_opportunities(conn, settings.batch_size)
    written = 0
    for opportunity in opportunities:
        try:
            async with pool.acquire() as conn:
                await score_opportunity(conn, opportunity)
            written += 1
        except Exception as exc:  # noqa: BLE001
            log.error("commerce_opportunity_error opportunity=%s error=%s", opportunity.get("opportunity_id"), exc)
    return written


async def run_continuous(pool: asyncpg.Pool) -> None:
    log.info("Commerce opportunity worker polling every %ds", settings.poll_interval_seconds)
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
