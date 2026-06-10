"""M36 substrate write path for Gallica records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .edm import normalize_edm_record
from .technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "gallica_adapter:sprint3"
SOURCE_SLUG = "gallica"
SCHEMA_STANDARD = "gallica_api_profile_v1"
GALLICA_DEACTIVATION_REASON = "gallica_deprecated_restricted"


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from Gallica media signals."""
    subject_terms = " ".join(str(term).lower() for term in normalized.get("subject_terms", []))
    edm_type = str(normalized.get("edm_type") or "").lower()
    if media_type_id == "map" or "carte" in subject_terms or "map" in subject_terms:
        return "geographic"
    if "natural history" in subject_terms or "histoire naturelle" in subject_terms:
        return "biological"
    if "map" in edm_type or "carte" in edm_type:
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    return {}


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
        workflow_record_id_key="gallica_record_id",
        anchor_type=anchor_type,
    )


async def _write_record_unchecked(
    conn: Any,
    raw_payload: dict[str, Any],
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Retained research-only Gallica M36 writer; not used by production entrypoint."""
    normalized = normalize_edm_record(raw_payload)
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


async def write_record(
    conn: Any,
    raw_payload: dict[str, Any],
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Reject Gallica production writes under DD-GALLICA-003 deactivation."""
    return {
        "status": "rejected",
        "reason": GALLICA_DEACTIVATION_REASON,
        "record_id": None,
        "writes": 0,
    }
