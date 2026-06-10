"""M36 substrate write path for Metropolitan Museum of Art records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .normalize import normalize_record
from .rights import MET_RIGHTS_POLICY_ID
from .technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "met_adapter:sprint3"
SOURCE_SLUG = "met"


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from Met metadata."""
    subject_terms = " ".join(str(term).lower() for term in normalized.get("subject_terms", []))
    if media_type_id == "map":
        return "geographic"
    if any(token in subject_terms for token in ("bird", "fish", "flower", "botanical")):
        return "biological"
    if normalized.get("country") or normalized.get("region") or normalized.get("city"):
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "met_is_public_domain": normalized.get("met_is_public_domain"),
    }


def _runtime(anchor_type: str) -> StoreRuntime:
    return StoreRuntime(
        worker_id=WORKER_ID,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        technical_schema_version=TECHNICAL_SCHEMA_VERSION,
        validator_name=VALIDATOR_NAME,
        validator_version=VALIDATOR_VERSION,
        build_technical_metadata=_build_technical_metadata,
        validation_status=validation_status,
        build_evidence_extension=_build_evidence_extension,
        rights_policy_id=MET_RIGHTS_POLICY_ID,
        workflow_record_id_key="met_object_id",
        anchor_type=anchor_type,
    )


async def write_record(
    conn: Any,
    raw_payload: dict[str, Any],
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Write one Met record into M36 tables when Met Rights Matrix v1 allows it."""
    normalized = normalize_record(raw_payload)
    if normalized.get("rights_decision") == "BLOCKED":
        return {
            "status": "rejected",
            "reason": normalized.get("met_rights_basis"),
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    derived_anchor_type = anchor_type if anchor_type is not None else derive_anchor_type(
        normalized,
        media_type_id,
    )
    return await write_normalized_record(
        conn,
        runtime=_runtime(derived_anchor_type),
        raw_payload=raw_payload,
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )

