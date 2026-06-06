"""Commerce Replay Worker entry point."""
from __future__ import annotations

import argparse
import asyncio

import asyncpg

from .config import settings
from .replay import run_once


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one replay batch and exit")
    args = parser.parse_args()

    conn = await asyncpg.connect(settings.postgres_dsn)
    try:
        if args.once:
            await run_once(conn, settings.batch_size)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
