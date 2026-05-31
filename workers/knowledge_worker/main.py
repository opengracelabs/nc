"""Knowledge worker: extracts facts and relationships from active places.

Pipeline:
    claim active places (FOR UPDATE SKIP LOCKED)
    → extract_facts (field mapping, pure function)
    → build_place_concept_relationships (derived, pure function)
    → upsert_facts + upsert_relationships + release_places (single transaction)
    → build_co_inscribed_relationships (bounded to current batch)
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
    release_places,
    reset_stale_extracting,
    upsert_facts,
    upsert_relationships,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("knowledge_worker")


async def process_places(pool: asyncpg.Pool, places: list[dict]) -> None:
    all_facts = []
    all_rels = []
    place_ids = [p["id"] for p in places]

    for place in places:
        facts = extract_facts(place)
        rels = build_place_concept_relationships(place["id"], facts, place.get("source", "unknown"))
        all_facts.extend(facts)
        all_rels.extend(rels)

    async with pool.acquire() as conn:
        async with conn.transaction():
            written, superseded = await upsert_facts(conn, all_facts)
            rel_written = await upsert_relationships(conn, all_rels)
            await release_places(conn, place_ids)

    log.info(
        "places=%d facts_written=%d superseded=%d relationships=%d",
        len(places), written, superseded, rel_written,
    )


async def poll_active_places(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        await reset_stale_extracting(conn)
        places = await claim_places_for_extraction(conn, settings.batch_size)

    if not places:
        return 0

    place_ids = [p["id"] for p in places]

    try:
        await process_places(pool, places)
    except Exception as exc:
        log.error("Extraction batch error: %s", exc, exc_info=True)
        async with pool.acquire() as conn:
            await release_places(conn, place_ids)

    async with pool.acquire() as conn:
        co = await build_co_inscribed_relationships(conn, place_ids)
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
