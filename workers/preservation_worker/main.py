"""Preservation worker for fetched MinIO assets.

Milestone flow:
    asset.status=fetched -> verify object exists -> verify checksum -> verify size -> valid
    any verification failure -> quarantined
"""
import argparse
import asyncio
import hashlib
import logging
from dataclasses import dataclass
from typing import Any

import asyncpg
from miniopy_async import Minio
from miniopy_async.error import S3Error

from .config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("preservation_worker")

_ASSET_COLS = """
    id, place_id, source_id, ingest_id, raw_path, checksum_sha256, size_bytes, status
"""

_ASSET_RETURNING_COLS = """
    a.id, a.place_id, a.source_id, a.ingest_id,
    a.raw_path, a.checksum_sha256, a.size_bytes, a.status
"""


@dataclass(frozen=True)
class VerificationResult:
    status: str
    warnings: list[str]


def _sha256(raw_bytes: bytes) -> str:
    return hashlib.sha256(raw_bytes).hexdigest()


async def reset_stale_preserving(conn: asyncpg.Connection) -> int:
    """Return stale claimed assets to the fetched queue."""
    result = await conn.execute(
        """
        UPDATE assets
        SET status = 'fetched', updated_at = NOW()
        WHERE status = 'preserving'
          AND updated_at < NOW() - ($1::int * interval '1 second')
        """,
        settings.preservation_timeout_seconds,
    )
    count = int(result.rsplit(" ", 1)[-1])
    if count:
        log.info("Reset %d stale preserving assets", count)
    return count


async def claim_fetched_assets(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    """Claim fetched assets in one short database statement."""
    rows = await conn.fetch(
        f"""
        WITH next_assets AS (
            SELECT id
            FROM assets
            WHERE status = 'fetched' AND raw_path IS NOT NULL
            ORDER BY fetched_at NULLS LAST, created_at
            LIMIT $1
            FOR UPDATE SKIP LOCKED
        )
        UPDATE assets AS a
        SET status = 'preserving', updated_at = NOW()
        FROM next_assets
        WHERE a.id = next_assets.id
        RETURNING {_ASSET_RETURNING_COLS}
        """,
        batch_size,
    )
    return [dict(row) for row in rows]


async def load_asset(conn: asyncpg.Connection, asset_id: str) -> dict[str, Any]:
    row = await conn.fetchrow(f"SELECT {_ASSET_COLS} FROM assets WHERE id = $1", asset_id)
    if not row:
        raise ValueError(f"Asset not found: {asset_id}")
    return dict(row)


async def _read_minio(minio: Minio, path: str) -> tuple[bytes, int]:
    stat = await minio.stat_object(settings.minio_bucket_raw, path)
    response = await minio.get_object(settings.minio_bucket_raw, path)
    try:
        raw_bytes = await response.read()
    finally:
        release = response.release()
        if asyncio.iscoroutine(release):
            await release
    return raw_bytes, stat.size or 0


def _verify(raw_bytes: bytes, object_size: int, asset: dict[str, Any]) -> VerificationResult:
    warnings: list[str] = []
    expected_checksum = asset.get("checksum_sha256")
    if expected_checksum and _sha256(raw_bytes) != expected_checksum:
        warnings.append("checksum_sha256 mismatch")

    expected_size = asset.get("size_bytes")
    if expected_size is not None and int(expected_size) != object_size:
        warnings.append(f"size_bytes mismatch: expected {expected_size} got {object_size}")

    if warnings:
        return VerificationResult("quarantined", warnings)
    return VerificationResult("valid", [])


async def verify_asset_object(minio: Minio, asset: dict[str, Any]) -> VerificationResult:
    """Verify that the raw MinIO object exists and matches asset integrity metadata."""
    raw_path = asset.get("raw_path")
    if not raw_path:
        return VerificationResult("quarantined", ["raw_path missing"])

    try:
        raw_bytes, object_size = await _read_minio(minio, raw_path)
    except S3Error as exc:
        return VerificationResult("quarantined", [f"object unavailable: {exc.code}"])

    return _verify(raw_bytes, object_size, asset)


async def update_asset_verification(
    conn: asyncpg.Connection,
    asset_id: Any,
    result: VerificationResult,
) -> None:
    await conn.execute(
        """
        UPDATE assets
        SET status = $2, validation_warnings = $3::text[], updated_at = NOW()
        WHERE id = $1
        """,
        asset_id,
        result.status,
        result.warnings,
    )


async def preserve_asset(
    conn: asyncpg.Connection,
    minio: Minio,
    asset: dict[str, Any],
) -> bool:
    result = await verify_asset_object(minio, asset)
    await update_asset_verification(conn, asset["id"], result)
    log.info(
        "Preserved asset_id=%s status=%s warnings=%d",
        asset["id"],
        result.status,
        len(result.warnings),
    )
    return result.status == "valid"


async def poll_fetched_assets(pool: asyncpg.Pool, minio: Minio) -> int:
    async with pool.acquire() as conn:
        await reset_stale_preserving(conn)
        assets = await claim_fetched_assets(conn, settings.batch_size)

    preserved = 0
    for asset in assets:
        try:
            async with pool.acquire() as conn:
                ok = await preserve_asset(conn, minio, asset)
            if ok:
                preserved += 1
        except Exception as exc:
            log.error("Preservation error asset_id=%s: %s", asset.get("id"), exc, exc_info=True)
    return preserved


async def run_once(asset_id: str | None = None) -> None:
    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=3)
    minio = Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    try:
        if asset_id:
            async with pool.acquire() as conn:
                asset = await load_asset(conn, asset_id)
            async with pool.acquire() as conn:
                await preserve_asset(conn, minio, asset)
        else:
            await poll_fetched_assets(pool, minio)
    finally:
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
    log.info("Preservation worker polling every %ds", settings.poll_interval_seconds)
    try:
        while True:
            n = await poll_fetched_assets(pool, minio)
            if n:
                log.info("Validated %d assets", n)
            else:
                await asyncio.sleep(settings.poll_interval_seconds)
    finally:
        await minio.close_session()
        await pool.close()


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", help="Preserve a single asset by UUID")
    parser.add_argument("--once", action="store_true", help="Run one batch and exit")
    args = parser.parse_args()

    if args.asset or args.once:
        await run_once(args.asset)
    else:
        await run_continuous()


if __name__ == "__main__":
    asyncio.run(main())
