"""M36 substrate write path for Europeana records."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from .edm import normalize_edm_record
from .rights import classify_rights
from .technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "europeana_adapter:sprint3"
SOURCE_SLUG = "europeana"
SCHEMA_STANDARD = "edm"


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def build_provenance(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "prov:wasGeneratedBy": WORKER_ID,
        "prov:generatedAtTime": _now_iso(),
        "nc:source": SOURCE_SLUG,
        "nc:source_identifier": normalized.get("record_id"),
        "nc:raw_payload_hash": normalized.get("raw_payload_hash"),
    }


async def upsert_source_item(
    conn: Any,
    *,
    source_id: str,
    normalized: dict[str, Any],
    media_type_id: str,
) -> Any:
    """Create or update the Europeana source_item shell."""
    row = await conn.fetchrow(
        """
        INSERT INTO source_item (
            source_id, source_identifier, media_type_id, canonical_source_url,
            title, status, anchor_type, provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3, $4, $5, 'proposed', 'europeana_record', $6::jsonb, NOW(), NOW()
        )
        ON CONFLICT (source_id, source_identifier)
        DO UPDATE SET
            media_type_id = EXCLUDED.media_type_id,
            canonical_source_url = EXCLUDED.canonical_source_url,
            title = EXCLUDED.title,
            updated_at = NOW()
        RETURNING id
        """,
        source_id,
        normalized["record_id"],
        media_type_id,
        normalized.get("source_url"),
        normalized.get("title"),
        _json(build_provenance(normalized)),
    )
    return row["id"]


async def insert_source_record(
    conn: Any,
    *,
    source_item_id: str,
    source_id: str,
    raw_payload: dict[str, Any],
    normalized: dict[str, Any],
) -> Any:
    row = await conn.fetchrow(
        """
        INSERT INTO source_record (
            source_item_id, institution_id, source_identifier, schema_standard,
            raw_payload, raw_payload_hash, normalized_payload, fetched_at,
            fetched_by, provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3, 'edm', $4::jsonb, $5, $6::jsonb, NOW(), $7, $8::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        source_id,
        normalized["record_id"],
        _json(raw_payload),
        normalized["raw_payload_hash"],
        _json(normalized),
        WORKER_ID,
        _json(build_provenance(normalized)),
    )
    return row["id"]


async def insert_media_rights(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    normalized: dict[str, Any],
) -> Any:
    rights = classify_rights(normalized.get("rights_uri"))
    evidence = {
        "source": SOURCE_SLUG,
        "schema_standard": SCHEMA_STANDARD,
        "source_record_id": source_record_id,
        "rights_basis": rights["rights_basis"],
        "rights_statement_uri": rights["rights_statement_uri"],
        "raw_payload_hash": normalized["raw_payload_hash"],
        "automated_allowlist": ["CC0", "PDM", "NoC-US"],
    }
    row = await conn.fetchrow(
        """
        INSERT INTO media_rights (
            source_item_id, rights_status, rights_statement_uri, rights_evidence,
            commercial_reuse_permitted, modification_permitted, verified_by,
            verified_at, authored_by, provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3, $4::jsonb, TRUE, TRUE, $5, NOW(), $5, $6::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        rights["rights_status"],
        rights["rights_statement_uri"],
        _json(evidence),
        WORKER_ID,
        _json(build_provenance(normalized)),
    )
    return row["id"]


async def insert_media_technical_metadata(
    conn: Any,
    *,
    source_item_id: str,
    media_type_id: str,
    normalized: dict[str, Any],
) -> Any:
    content = build_technical_metadata(normalized, media_type_id=media_type_id)
    row = await conn.fetchrow(
        """
        INSERT INTO media_technical_metadata (
            source_item_id, media_type_id, schema_version, content,
            validation_status, validated_by, validated_at, validator_name,
            validator_version, content_hash, provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3, $4::jsonb, $5, $6, NOW(), $7, $8, $9, $10::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        media_type_id,
        TECHNICAL_SCHEMA_VERSION,
        _json(content),
        validation_status(content),
        WORKER_ID,
        VALIDATOR_NAME,
        VALIDATOR_VERSION,
        content["content_hash"],
        _json(build_provenance(normalized)),
    )
    return row["id"]


async def pin_current_substrate_records(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    media_rights_id: str,
    technical_metadata_id: str,
) -> None:
    await conn.execute(
        """
        UPDATE source_item
        SET current_source_record_id = $2,
            current_media_rights_id = $3,
            current_technical_metadata_id = $4,
            status = 'activation_eligible',
            updated_at = NOW()
        WHERE id = $1
        """,
        source_item_id,
        source_record_id,
        media_rights_id,
        technical_metadata_id,
    )


async def write_record(
    conn: Any,
    raw_payload: dict[str, Any],
    *,
    source_id: str,
    media_type_id: str,
) -> dict[str, Any]:
    """Write one rights-cleared Europeana record into the M36 substrate tables."""
    normalized = normalize_edm_record(raw_payload)
    rights = classify_rights(normalized.get("rights_uri"))
    if not rights["allowed"]:
        return {
            "status": "rejected",
            "reason": rights["rights_basis"],
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    content = build_technical_metadata(normalized, media_type_id=media_type_id)
    if validation_status(content) != "valid":
        return {
            "status": "rejected",
            "reason": "invalid_technical_metadata",
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    async with conn.transaction():
        source_item_id = await upsert_source_item(
            conn,
            source_id=source_id,
            normalized=normalized,
            media_type_id=media_type_id,
        )
        source_record_id = await insert_source_record(
            conn,
            source_item_id=source_item_id,
            source_id=source_id,
            raw_payload=raw_payload,
            normalized=normalized,
        )
        media_rights_id = await insert_media_rights(
            conn,
            source_item_id=source_item_id,
            source_record_id=source_record_id,
            normalized=normalized,
        )
        technical_metadata_id = await insert_media_technical_metadata(
            conn,
            source_item_id=source_item_id,
            media_type_id=media_type_id,
            normalized=normalized,
        )
        await pin_current_substrate_records(
            conn,
            source_item_id=source_item_id,
            source_record_id=source_record_id,
            media_rights_id=media_rights_id,
            technical_metadata_id=technical_metadata_id,
        )

    return {
        "status": "written",
        "record_id": normalized["record_id"],
        "source_item_id": source_item_id,
        "source_record_id": source_record_id,
        "media_rights_id": media_rights_id,
        "technical_metadata_id": technical_metadata_id,
        "raw_payload_hash": normalized["raw_payload_hash"],
        "technical_content_hash": content["content_hash"],
        "writes": 5,
    }
