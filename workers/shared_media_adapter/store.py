"""Shared M36 substrate write path for institution media adapters."""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from .rights import RIGHTS_POLICY_ID, RightsDecision, classify_rights

ALLOWED_ANCHOR_TYPES = {"biological", "geographic", "cultural", "mixed"}


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class StoreRuntime:
    """Institution-specific values required by the shared M36 write path."""

    worker_id: str
    source_slug: str
    technical_schema_version: str
    validator_name: str
    validator_version: str
    build_technical_metadata: Callable[[dict[str, Any], str], dict[str, Any]]
    validation_status: Callable[[dict[str, Any]], str]
    schema_standard: str = "edm"
    rights_policy_id: str = RIGHTS_POLICY_ID
    workflow_record_id_key: str = "source_record_id"
    anchor_type: str = "cultural"
    generated_at_time: str | None = None

    def __post_init__(self) -> None:
        required_values = {
            "worker_id": self.worker_id,
            "source_slug": self.source_slug,
            "schema_standard": self.schema_standard,
            "technical_schema_version": self.technical_schema_version,
            "validator_name": self.validator_name,
            "validator_version": self.validator_version,
            "rights_policy_id": self.rights_policy_id,
            "workflow_record_id_key": self.workflow_record_id_key,
        }
        empty = [name for name, value in required_values.items() if not value]
        if empty:
            raise ValueError(f"missing_store_runtime_fields:{','.join(sorted(empty))}")
        if self.anchor_type not in ALLOWED_ANCHOR_TYPES:
            raise ValueError(f"invalid_anchor_type:{self.anchor_type}")
        if not callable(self.build_technical_metadata):
            raise ValueError("build_technical_metadata_not_callable")
        if not callable(self.validation_status):
            raise ValueError("validation_status_not_callable")


def build_provenance(normalized: dict[str, Any], runtime: StoreRuntime) -> dict[str, Any]:
    return {
        "prov:wasGeneratedBy": runtime.worker_id,
        "prov:generatedAtTime": runtime.generated_at_time or _now_iso(),
        "nc:source": runtime.source_slug,
        "nc:source_identifier": normalized.get("record_id"),
        "nc:raw_payload_hash": normalized.get("raw_payload_hash"),
    }


def build_rights_evidence(
    *,
    runtime: StoreRuntime,
    source_record_id: str,
    normalized: dict[str, Any],
    rights: dict[str, str | bool | None],
) -> dict[str, Any]:
    worker_classified_status = rights["rights_status"]
    if runtime.source_slug in {
        "met",
        "aic",
        "cma",
        "nga",
        "smk",
        "walters",
        "ycba",
        "yuag",
        "getty",
    }:
        worker_classified_status = {
            "verified_cc0": "classified_cc0",
            "verified_pd": "classified_pd",
        }.get(str(worker_classified_status), worker_classified_status)

    evidence = {
        "source": runtime.source_slug,
        "schema_standard": runtime.schema_standard,
        "source_record_id": source_record_id,
        "edm_rights_uri": rights["rights_statement_uri"],
        "rights_matrix_classification": str(rights["decision"]).lower(),
        "applying_policy": runtime.rights_policy_id,
        "oai_pmh_identifier": normalized.get("record_id"),
        "rights_basis": rights["rights_basis"],
        "rights_statement_uri": rights["rights_statement_uri"],
        "raw_payload_hash": normalized["raw_payload_hash"],
        "worker_classified_status": worker_classified_status,
        "evidence_status": "pending_human_review",
    }
    if runtime.source_slug == "met":
        evidence["met_is_public_domain"] = normalized.get("met_is_public_domain")
    if runtime.source_slug == "aic":
        evidence["aic_is_public_domain"] = normalized.get("aic_is_public_domain")
        evidence["aic_copyright_notice"] = normalized.get("aic_copyright_notice")
        evidence["aic_manifest_url"] = normalized.get("aic_manifest_url")
    if runtime.source_slug == "smk":
        evidence["smk_public_domain"] = normalized.get("smk_public_domain")
        evidence["smk_object_number"] = normalized.get("smk_object_number")
        evidence["smk_manifest_url"] = normalized.get("smk_manifest_url")
        evidence["smk_image_rights"] = normalized.get("smk_image_rights")
    if runtime.source_slug == "cma":
        evidence["cma_share_license_status"] = normalized.get("cma_share_license_status")
        evidence["cma_copyright"] = normalized.get("cma_copyright")
        evidence["cma_accession_number"] = normalized.get("accession_number")
        evidence["cma_image_web_url"] = normalized.get("cma_image_web_url")
        evidence["cma_image_print_url"] = normalized.get("cma_image_print_url")
        evidence["cma_image_full_url"] = normalized.get("cma_image_full_url")
    if runtime.source_slug == "nga":
        evidence["nga_openaccess"] = normalized.get("nga_openaccess")
        evidence["nga_image_uuid"] = normalized.get("nga_image_uuid")
        evidence["nga_iiifurl"] = normalized.get("nga_iiifurl")
        evidence["nga_iiif_thumb_url"] = normalized.get("nga_iiif_thumb_url")
        evidence["nga_viewtype"] = normalized.get("nga_viewtype")
        evidence["nga_objectid"] = normalized.get("nga_objectid")
        evidence["nga_accessionnum"] = normalized.get("nga_accessionnum")
    if runtime.source_slug == "walters":
        evidence["walters_object_id"] = normalized.get("walters_object_id")
        evidence["walters_object_number"] = normalized.get("walters_object_number")
        evidence["walters_image_url"] = normalized.get("walters_image_url")
        evidence["walters_media_xref_id"] = normalized.get("walters_media_xref_id")
        evidence["walters_is_primary"] = normalized.get("walters_is_primary")
        evidence["walters_collection_ids"] = normalized.get("walters_collection_ids")
        evidence["walters_collection_names"] = normalized.get("walters_collection_names")
    if runtime.source_slug == "ycba":
        evidence["ycba_rights_uri"] = normalized.get("ycba_rights_uri")
        evidence["ycba_attribution"] = normalized.get("ycba_attribution")
        evidence["yale_object_id"] = normalized.get("yale_object_id")
        evidence["yale_iiif_manifest"] = normalized.get("yale_iiif_manifest")
        evidence["yale_image_service"] = normalized.get("yale_image_service")
    if runtime.source_slug == "yuag":
        evidence["yuag_rights_uri"] = normalized.get("yuag_rights_uri")
        evidence["yale_object_id"] = normalized.get("yale_object_id")
        evidence["yale_iiif_manifest"] = normalized.get("yale_iiif_manifest")
        evidence["yale_image_service"] = normalized.get("yale_image_service")
    if runtime.source_slug == "getty":
        evidence["getty_object_id"] = normalized.get("getty_object_id")
        evidence["getty_rights_uri"] = normalized.get("getty_rights_uri")
        evidence["getty_manifest_uri"] = normalized.get("getty_manifest_uri")
        evidence["getty_image_service"] = normalized.get("getty_image_service")
        evidence["getty_accession_number"] = normalized.get("getty_accession_number")
    return evidence


async def upsert_source_item(
    conn: Any,
    *,
    runtime: StoreRuntime,
    source_id: str,
    normalized: dict[str, Any],
    media_type_id: str,
) -> Any:
    sql = """
    INSERT INTO source_item (
        source_id, source_identifier, media_type_id, canonical_source_url,
        title, status, anchor_type, provenance, created_at, updated_at
    ) VALUES (
        $1, $2, $3, $4, $5, 'proposed', $6, $7::jsonb, NOW(), NOW()
    )
    ON CONFLICT (source_id, source_identifier)
    DO UPDATE SET
        media_type_id = EXCLUDED.media_type_id,
        canonical_source_url = EXCLUDED.canonical_source_url,
        title = EXCLUDED.title,
        updated_at = NOW()
    RETURNING id
    """
    args = (
        source_id,
        normalized["record_id"],
        media_type_id,
        normalized.get("source_url"),
        normalized.get("title"),
        runtime.anchor_type,
        _json(build_provenance(normalized, runtime)),
    )
    row = await conn.fetchrow(sql, *args)
    return row["id"]


async def insert_source_record(
    conn: Any,
    *,
    runtime: StoreRuntime,
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
            $1, $2, $3, $4, $5::jsonb, $6, $7::jsonb, NOW(), $8, $9::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        source_id,
        normalized["record_id"],
        runtime.schema_standard,
        _json(raw_payload),
        normalized["raw_payload_hash"],
        _json(normalized),
        runtime.worker_id,
        _json(build_provenance(normalized, runtime)),
    )
    return row["id"]


async def insert_media_file(
    conn: Any,
    *,
    runtime: StoreRuntime,
    source_item_id: str,
    source_record_id: str,
    media_type_id: str,
    normalized: dict[str, Any],
) -> Any:
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
        _json(build_provenance(normalized, runtime)),
    )
    return row["id"]


async def insert_media_rights(
    conn: Any,
    *,
    runtime: StoreRuntime,
    source_item_id: str,
    source_record_id: str,
    normalized: dict[str, Any],
    rights: dict[str, str | bool | None],
) -> Any:
    evidence = build_rights_evidence(
        runtime=runtime,
        source_record_id=source_record_id,
        normalized=normalized,
        rights=rights,
    )
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
        runtime.worker_id,
        _json(build_provenance(normalized, runtime)),
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
    runtime: StoreRuntime,
    source_item_id: str,
    media_type_id: str,
    normalized: dict[str, Any],
) -> Any:
    content = runtime.build_technical_metadata(normalized, media_type_id)
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
        runtime.technical_schema_version,
        _json(content),
        runtime.validation_status(content),
        runtime.worker_id,
        runtime.validator_name,
        runtime.validator_version,
        content["content_hash"],
        _json(build_provenance(normalized, runtime)),
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
    runtime: StoreRuntime,
    source_item_id: str,
    source_record_id: str,
    media_rights_id: str,
    normalized: dict[str, Any],
    raw_payload: dict[str, Any],
    rights_basis: str,
) -> Any:
    context = {
        "item_type": "rights_review",
        "item_payload": {
            runtime.workflow_record_id_key: normalized.get("record_id"),
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
        runtime.worker_id,
        _json(context),
        _json(build_provenance(normalized, runtime)),
    )
    return row["id"]


async def write_normalized_record(
    conn: Any,
    *,
    runtime: StoreRuntime,
    raw_payload: dict[str, Any],
    normalized: dict[str, Any],
    source_id: str,
    media_type_id: str,
) -> dict[str, Any]:
    if not normalized.get("rights_uri"):
        return {
            "status": "rejected",
            "reason": "missing_rights_uri",
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    rights = classify_rights(normalized.get("rights_uri"))
    if rights["decision"] == RightsDecision.BLOCKED:
        return {
            "status": "rejected",
            "reason": rights["rights_basis"],
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    content = runtime.build_technical_metadata(normalized, media_type_id)
    if runtime.validation_status(content) != "valid":
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
            runtime=runtime,
            source_id=source_id,
            normalized=normalized,
            media_type_id=media_type_id,
        )
        source_record_id = await insert_source_record(
            conn,
            runtime=runtime,
            source_item_id=source_item_id,
            source_id=source_id,
            raw_payload=raw_payload,
            normalized=normalized,
        )
        media_file_id = await insert_media_file(
            conn,
            runtime=runtime,
            source_item_id=source_item_id,
            source_record_id=source_record_id,
            media_type_id=media_type_id,
            normalized=normalized,
        )
        media_rights_id = await insert_media_rights(
            conn,
            runtime=runtime,
            source_item_id=source_item_id,
            source_record_id=source_record_id,
            normalized=normalized,
            rights=rights,
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
                "worker_id": runtime.worker_id,
            },
            agent_id=runtime.worker_id,
        )
        technical_metadata_id = await insert_media_technical_metadata(
            conn,
            runtime=runtime,
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
                runtime=runtime,
                source_item_id=source_item_id,
                source_record_id=source_record_id,
                media_rights_id=media_rights_id,
                normalized=normalized,
                raw_payload=raw_payload,
                rights_basis=str(rights["rights_basis"]),
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
