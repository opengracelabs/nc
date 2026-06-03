"""Storage operations for approved BHL illustration asset ingestion."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from io import BytesIO
from typing import Any

import asyncpg
from miniopy_async import Minio

from .config import settings

_WORKER_ID = "bhl_asset_ingestion_worker:v0.3.1"
_ALLOWED_RIGHTS = {"Public Domain", "CC0"}

_OPPORTUNITY_COLS = """
    o.id, o.concept_id, o.source, o.source_record_id, o.source_url,
    o.bhl_item_id, o.bhl_page_id, o.taxon_name, o.title, o.publication_title,
    o.illustrator, o.publication_year, o.rights_status, o.rights_source_url,
    o.rights_verified_by, o.rights_verified_at, o.provenance, o.score_components
"""


def verify_opportunity_rights(opportunity: dict[str, Any]) -> bool:
    return (
        opportunity.get("rights_status") in _ALLOWED_RIGHTS
        and bool(opportunity.get("rights_verified_by"))
    )


def bhl_image_url(opportunity: dict[str, Any]) -> str:
    return settings.bhl_page_image_url_template.format(
        bhl_page_id=opportunity["bhl_page_id"],
        bhl_item_id=opportunity["bhl_item_id"],
    )


def bhl_asset_raw_path(opportunity: dict[str, Any], content_type: str) -> str:
    suffix = "jpg"
    if "webp" in content_type:
        suffix = "webp"
    elif "png" in content_type:
        suffix = "png"
    elif "tif" in content_type or "tiff" in content_type:
        suffix = "tif"
    return (
        f"bhl/illustrations/{opportunity['concept_id']}/"
        f"{opportunity['id']}/{opportunity['bhl_page_id']}.{suffix}"
    )


def checksum_sha256(raw_bytes: bytes) -> str:
    return hashlib.sha256(raw_bytes).hexdigest()


async def claim_approved_opportunities(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        f"""
        SELECT {_OPPORTUNITY_COLS}
        FROM illustration_opportunities o
        WHERE o.status = 'approved'
          AND o.rights_status IN ('Public Domain','CC0')
          AND o.rights_verified_by IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM illustration_opportunity_assets oa
              WHERE oa.opportunity_id = o.id
          )
        ORDER BY o.opportunity_score DESC, o.created_at
        LIMIT $1
        """,  # noqa: S608
        batch_size,
    )
    return [dict(row) for row in rows]


async def store_raw_asset(
    minio: Minio,
    opportunity: dict[str, Any],
    raw_bytes: bytes,
    content_type: str,
) -> tuple[str, str]:
    path = bhl_asset_raw_path(opportunity, content_type)
    checksum = checksum_sha256(raw_bytes)
    await minio.put_object(
        bucket_name=settings.minio_bucket_raw,
        object_name=path,
        data=BytesIO(raw_bytes),
        length=len(raw_bytes),
        content_type=content_type,
    )
    return path, checksum


async def create_bhl_asset(
    conn: asyncpg.Connection,
    opportunity: dict[str, Any],
    raw_path: str,
    raw_bytes: bytes,
    checksum: str,
    content_type: str,
    image_url: str,
) -> Any:
    if not verify_opportunity_rights(opportunity):
        raise ValueError("approved BHL opportunity lacks explicit Public Domain or CC0 rights")

    ingest_id = f"bhl:{opportunity['bhl_page_id']}"
    now = datetime.now(UTC).isoformat()
    provenance = {
        "prov:wasGeneratedBy": _WORKER_ID,
        "prov:generatedAtTime": now,
        "nc:opportunity_id": str(opportunity["id"]),
        "nc:concept_id": str(opportunity["concept_id"]),
        "nc:bhl_item_id": opportunity["bhl_item_id"],
        "nc:bhl_page_id": opportunity["bhl_page_id"],
        "nc:source_record_id": opportunity["source_record_id"],
        "nc:rights_status": opportunity["rights_status"],
        "nc:rights_verified_by": opportunity["rights_verified_by"],
        "nc:rights_source_url": opportunity.get("rights_source_url"),
        "nc:raw_path": raw_path,
        "nc:checksum_sha256": checksum,
    }

    async with conn.transaction():
        row = await conn.fetchrow(
            """
            INSERT INTO assets (
                concept_id, source_id, ingest_id, asset_type, mime_type,
                raw_path, checksum_sha256, size_bytes, status, source_url, fetched_at,
                premis_object_id, premis_original_name, premis_creating_application,
                provenance
            ) VALUES (
                $1, 'bhl', $2, 'bhl_illustration', $3,
                $4, $5, $6, 'fetched', $7, NOW(),
                $8, $9, $10, $11::jsonb
            )
            RETURNING id
            """,
            opportunity["concept_id"],
            ingest_id,
            content_type,
            raw_path,
            checksum,
            len(raw_bytes),
            image_url,
            f"bhl-page-{opportunity['bhl_page_id']}",
            f"bhl_page_{opportunity['bhl_page_id']}",
            _WORKER_ID,
            json.dumps(provenance, sort_keys=True),
        )
        asset_id = row["id"]
        await conn.execute(
            """
            INSERT INTO asset_rights (
                asset_id, rights_status, rights_source_url, rights_statement,
                verified_by, provenance
            ) VALUES ($1, $2, $3, $4, $5, $6::jsonb)
            ON CONFLICT (asset_id)
            DO UPDATE SET
                rights_status = EXCLUDED.rights_status,
                rights_source_url = EXCLUDED.rights_source_url,
                rights_statement = EXCLUDED.rights_statement,
                verified_by = EXCLUDED.verified_by,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            """,
            asset_id,
            opportunity["rights_status"],
            opportunity.get("rights_source_url"),
            f"BHL metadata verified as {opportunity['rights_status']}",
            opportunity["rights_verified_by"],
            json.dumps(provenance, sort_keys=True),
        )
        await conn.execute(
            """
            INSERT INTO illustration_opportunity_assets (
                opportunity_id, asset_id, link_type, provenance
            ) VALUES ($1, $2, 'source_asset', $3::jsonb)
            ON CONFLICT (opportunity_id, link_type)
            DO UPDATE SET
                asset_id = EXCLUDED.asset_id,
                provenance = EXCLUDED.provenance
            """,
            opportunity["id"],
            asset_id,
            json.dumps(provenance, sort_keys=True),
        )
    return asset_id
