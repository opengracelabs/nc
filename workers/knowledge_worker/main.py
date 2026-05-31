"""Knowledge worker: extracts facts and relationships from active places.

Pipeline:
    claim active places (FOR UPDATE SKIP LOCKED)
    → extract_facts (field mapping, pure function)
    → build_place_concept_relationships (derived, pure function)
    → upsert_facts (supersede on value change, skip exact duplicates)
    → upsert_relationships (ON CONFLICT DO NOTHING)
    → build_co_inscribed_relationships (join query across all active facts)
    → release place (mark extraction complete)
"""
import argparse
import asyncio
import logging

import asyncpg

from .config import settings
from .extract import build_place_concept_relationships, extract_facts
from .store import (
    build_co_inscribed_relationships,
    claim_places_for_extraction,
    release_place,
    reset_stale_extracting,
    upsert_facts,
    upsert_relationships,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("knowledge_worker")


async def process_place(pool: asyncpg.Pool, place: dict) -> None:
    place_id = place["id"]
    source = place.get("source", "unknown")

    facts = extract_facts(place)
    rels = build_place_concept_relationships(place_id, facts, source)

    async with pool.acquire() as conn:
        written, superseded = await upsert_facts(conn, facts)
        rel_written = await upsert_relationships(conn, rels)
        await release_place(conn, place_id)

    log.info(
        "place_id=%s facts_written=%d superseded=%d relationships=%d",
        place_id, written, superseded, rel_written,
    )


async def poll_active_places(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        await reset_stale_extracting(conn)
        places = await claim_places_for_extraction(conn, settings.batch_size)

    if not places:
        return 0

    for place in places:
        try:
            await process_place(pool, place)
        except Exception as exc:
            log.error("Extraction error place_id=%s: %s", place.get("id"), exc, exc_info=True)
            async with pool.acquire() as conn:
                await release_place(conn, place["id"])

    async with pool.acquire() as conn:
        co = await build_co_inscribed_relationships(conn)
    if co:
        log.info("Built %d co_inscribed_with relationships", co)

    return len(places)


async def run_once(pool: asyncpg.Pool) -> int:
    return await poll_active_places(pool)


async def run_continuous(pool: asyncpg.Pool) -> None:
    log.info("Knowledge worker polling every %ds", settings.poll_interval_seconds)
    while True:
        n = await run_once(pool)
        if not n:
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
