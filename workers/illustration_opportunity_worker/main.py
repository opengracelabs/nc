"""Illustration Opportunity Discovery worker.

BHL is the primary discovery source. GBIF and Wikidata are not crawled here;
their prior taxon-discovery evidence is used only as validation/context.
"""
import argparse
import asyncio
import logging
from typing import Any

import asyncpg
import httpx

from .config import settings
from .discover import build_illustration_opportunity
from .store import claim_bhl_search_targets, mark_target_searched, upsert_illustration_opportunity

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("illustration_opportunity_worker")


async def fetch_bhl_page_candidates(client: httpx.AsyncClient, query: str) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "op": "PageSearch",
        "searchterm": query,
        "format": "json",
    }
    if settings.bhl_api_key:
        params["apikey"] = settings.bhl_api_key
    response = await client.get(settings.bhl_api_base_url, params=params)
    response.raise_for_status()
    payload = response.json()
    result = payload.get("Result") or []
    if isinstance(result, dict):
        return [result]
    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]
    return []


async def process_target(
    pool: asyncpg.Pool,
    client: httpx.AsyncClient,
    target: dict[str, Any],
) -> int:
    candidates = await fetch_bhl_page_candidates(client, target["query"])
    written = 0
    async with pool.acquire() as conn:
        for record in candidates:
            opportunity = build_illustration_opportunity(
                place_id=target["place_id"],
                concept_id=target["concept_id"],
                taxon_name=target["scientific_name"],
                bhl_record=record,
                gbif_validation={
                    "source_url": (
                        f"https://www.gbif.org/species/{target['gbif_taxon_key']}"
                        if target.get("gbif_taxon_key")
                        else "https://www.gbif.org"
                    ),
                    "gbif_taxon_key": target.get("gbif_taxon_key"),
                    "place_relevance_score": float(target.get("place_relevance_score") or 0),
                    "role": "validation_only",
                },
                wikidata_context={
                    "source_url": (
                        f"https://www.wikidata.org/wiki/{target['wikidata_qid']}"
                        if target.get("wikidata_qid")
                        else "https://www.wikidata.org"
                    ),
                    "wikidata_qid": target.get("wikidata_qid"),
                    "role": "context_only",
                },
            )
            if opportunity is None:
                continue
            await upsert_illustration_opportunity(conn, opportunity)
            written += 1
        await mark_target_searched(conn, target["id"])
    return written


async def run_once(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        targets = await claim_bhl_search_targets(conn, settings.batch_size)
    if not targets:
        return 0
    written = 0
    async with httpx.AsyncClient(timeout=30) as client:
        for target in targets:
            try:
                written += await process_target(pool, client, target)
            except Exception as exc:  # noqa: BLE001
                log.error(
                    "illustration_opportunity_error target=%s error=%s",
                    target.get("id"),
                    exc,
                )
    return written


async def run_continuous(pool: asyncpg.Pool) -> None:
    log.info("Illustration opportunity worker polling every %ds", settings.poll_interval_seconds)
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
