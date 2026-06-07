"""M36 substrate write path for Europeana records."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from .edm import normalize_edm_record
from .rights import RightsDecision, classify_rights
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
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


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
            $1, $2, $3, $4, $5, 'proposed', 'mixed', $6::jsonb, NOW(), NOW()
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


async def insert_media_file(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    media_type_id: str,
    normalized: dict[str, Any],
) -> Any:
    """Create the EDM WebResource shell before binary retrieval."""
    row = await conn.fetchrow(
        """
        INSERT INTO media_file (
            source_item_id, source_record_id, media_type_id,
            file_role, sequence_position, source_url,
            original_filename, minio_bucket, minio_key,
            mime_type, byte_size, checksum_sha256,
            preservation_status, ingestion_event_id,
            provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3,
            'primary', 1, $4,
            NULL, NULL, NULL,
            NULL, NULL, NULL,
            'pending_retrieval', NULL,
            $5::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        source_record_id,
        media_type_id,
        normalized.get("representative_media_url"),
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
        "worker_classified_status": rights["rights_status"],
        "evidence_status": "pending_human_review",
    }
    row = await conn.fetchrow(
        """
        INSERT INTO media_rights (
            source_item_id, rights_status, rights_statement_uri, rights_evidence,
            commercial_reuse_permitted, modification_permitted,
            authored_by, provenance, created_at, updated_at
        ) VALUES (
            $1, 'pending_verification', $2, $3::jsonb, FALSE, FALSE,
            $4, $5::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        rights["rights_statement_uri"],
        _json(evidence),
        WORKER_ID,
        _json(build_provenance(normalized)),
    )
    return row["id"]


async def insert_preservation_event(
    conn: Any,
    *,
    subject_type: str,
    subject_id: str,
    event_type: str,
    event_outcome: str,
    event_detail: dict[str, Any],
    agent_id: str,
    media_file_id: str | None = None,
    media_derivative_id: str | None = None,
) -> Any:
    row = await conn.fetchrow(
        """
        INSERT INTO preservation_event (
            subject_type, subject_id, media_file_id, media_derivative_id,
            event_type, event_datetime, event_outcome, event_detail,
            agent_type, agent_id, created_at
        ) VALUES (
            $1, $2, $3, $4, $5, NOW(), $6, $7::jsonb, 'worker', $8, NOW()
        )
        RETURNING id
        """,
        subject_type,
        subject_id,
        media_file_id,
        media_derivative_id,
        event_type,
        event_outcome,
        _json(event_detail),
        agent_id,
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
            updated_at = NOW()
        WHERE id = $1
        """,
        source_item_id,
        source_record_id,
        media_rights_id,
        technical_metadata_id,
    )


async def insert_workflow_item(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    media_rights_id: str,
    normalized: dict[str, Any],
    raw_payload: dict[str, Any],
    rights_basis: str,
) -> Any:
    """Open a human rights review workflow item for REVIEW REQUIRED records."""
    context = {
        "item_type": "rights_review",
        "item_payload": {
            "europeana_record_id": normalized.get("record_id"),
            "edm_rights_uri": normalized.get("rights_uri"),
            "matrix_classification": "review_required",
            "matrix_rule": rights_basis,
            "raw_edm_payload": raw_payload,
            "source_record_id": source_record_id,
            "media_rights_id": media_rights_id,
        },
    }
    row = await conn.fetchrow(
        """
        INSERT INTO workflow_items (
            capability, entity_type, entity_id, priority, scheduled_at,
            status, status_reason, worker_id, context, provenance,
            created_at, updated_at
        ) VALUES (
            'rights_review', 'source_item', $1, 40, NOW(),
            'pending', $2, $3, $4::jsonb, $5::jsonb,
            NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        rights_basis,
        WORKER_ID,
        _json(context),
        _json(build_provenance(normalized)),
    )
    return row["id"]


async def write_record(
    conn: Any,
    raw_payload: dict[str, Any],
    *,
    source_id: str,
    media_type_id: str,
) -> dict[str, Any]:
    """Write one non-blocked Europeana record into the M36 substrate tables."""
    normalized = normalize_edm_record(raw_payload)
    rights = classify_rights(normalized.get("rights_uri"))
    if rights["decision"] == RightsDecision.BLOCKED:
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

    workflow_item_id = None
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
        media_file_id = await insert_media_file(
            conn,
            source_item_id=source_item_id,
            source_record_id=source_record_id,
            media_type_id=media_type_id,
            normalized=normalized,
        )
        media_rights_id = await insert_media_rights(
            conn,
            source_item_id=source_item_id,
            source_record_id=source_record_id,
            normalized=normalized,
        )
        await insert_preservation_event(
            conn,
            subject_type="media_rights",
            subject_id=media_rights_id,
            media_file_id=media_file_id,
            event_type="rights_verification",
            event_outcome="pending_human_review",
            event_detail={
                "rights_basis": rights["rights_basis"],
                "rights_statement_uri": rights["rights_statement_uri"],
                "decision": rights["decision"],
                "raw_payload_hash": normalized["raw_payload_hash"],
                "worker_id": WORKER_ID,
            },
            agent_id=WORKER_ID,
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
        if rights["decision"] == RightsDecision.REVIEW_REQUIRED:
            workflow_item_id = await insert_workflow_item(
                conn,
                source_item_id=source_item_id,
                source_record_id=source_record_id,
                media_rights_id=media_rights_id,
                normalized=normalized,
                raw_payload=raw_payload,
                rights_basis=rights["rights_basis"],
            )

    writes = 8 if workflow_item_id else 7
    return {
        "status": "written",
        "record_id": normalized["record_id"],
        "source_item_id": source_item_id,
        "source_record_id": source_record_id,
        "media_file_id": media_file_id,
        "media_rights_id": media_rights_id,
        "technical_metadata_id": technical_metadata_id,
        "workflow_item_id": workflow_item_id,
        "raw_payload_hash": normalized["raw_payload_hash"],
        "technical_content_hash": content["content_hash"],
        "writes": writes,
    }
