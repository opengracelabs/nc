"""BHL asset ingestion worker.

Consumes approved Illustration Opportunities and creates concept-owned BHL assets.
"""
from __future__ import annotations

import argparse
import asyncio
import logging

import asyncpg
import httpx
from miniopy_async import Minio

from .config import settings
from .store import (
    bhl_image_url,
    claim_approved_opportunities,
    create_bhl_asset,
    store_raw_asset,
    verify_opportunity_rights,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("bhl_asset_ingestion_worker")


async def fetch_bhl_asset(client: httpx.AsyncClient, image_url: str) -> tuple[bytes, str]:
    response = await client.get(image_url, follow_redirects=True)
    response.raise_for_status()
    raw = response.content
    if len(raw) > settings.fetch_max_bytes:
        raise ValueError(f"BHL asset exceeds fetch_max_bytes: {len(raw)}")
    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip()
    if not content_type.startswith("image/"):
        raise ValueError(f"BHL asset response is not an image: {content_type or 'missing'}")
    return raw, content_type


async def ingest_opportunity(
    conn: asyncpg.Connection,
    minio: Minio,
    client: httpx.AsyncClient,
    opportunity: dict,
) -> bool:
    if not verify_opportunity_rights(opportunity):
        return False
    image_url = bhl_image_url(opportunity)
    raw_bytes, content_type = await fetch_bhl_asset(client, image_url)
    raw_path, checksum = await store_raw_asset(
        minio, opportunity, raw_bytes, content_type
    )
    await create_bhl_asset(
        conn, opportunity, raw_path, raw_bytes, checksum, content_type, image_url
    )
    return True


async def run_once(pool: asyncpg.Pool, minio: Minio) -> int:
    async with pool.acquire() as conn:
        opportunities = await claim_approved_opportunities(conn, settings.batch_size)
    if not opportunities:
        return 0

    ingested = 0
    timeout = httpx.Timeout(settings.fetch_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for opportunity in opportunities:
            try:
                async with pool.acquire() as conn:
                    if await ingest_opportunity(conn, minio, client, opportunity):
                        ingested += 1
            except Exception as exc:  # noqa: BLE001
                log.error(
                    "bhl_asset_ingestion_error opportunity=%s error=%s",
                    opportunity.get("id"),
                    exc,
                )
    return ingested


async def run_continuous(pool: asyncpg.Pool, minio: Minio) -> None:
    log.info("BHL asset ingestion worker polling every %ds", settings.poll_interval_seconds)
    while True:
        ingested = await run_once(pool, minio)
        if not ingested:
            await asyncio.sleep(settings.poll_interval_seconds)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one batch and exit")
    args = parser.parse_args()

    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=5)
    minio = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    try:
        if args.once:
            await run_once(pool, minio)
        else:
            await run_continuous(pool, minio)
    finally:
        await minio.close_session()
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
