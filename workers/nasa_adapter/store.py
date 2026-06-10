"""M36 substrate write path for NASA Image and Video Library records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .config import RIGHTS_POLICY_ID, SCHEMA_STANDARD, SOURCE_SLUG
from .normalize import build_rights_evidence, normalize_record
from .rights import classify_rights
from .technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "nasa_adapter:sprint3"
ANCHOR_TYPE = "geographic"
REVIEW_REQUIRED_PILOT_EXCLUSION = "review_required_pilot_exclusion"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    """Return adapter-owned NASA rights evidence extension fields."""
    return {key: value for key, value in normalized.items() if key.startswith("nasa_")}


def _runtime() -> StoreRuntime:
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
        rights_policy_id=RIGHTS_POLICY_ID,
        workflow_record_id_key="nasa_id",
        anchor_type=ANCHOR_TYPE,
    )


def _rejected_result(record: dict[str, Any] | None) -> dict[str, Any]:
    rights = classify_rights(record)
    evidence = build_rights_evidence(record)
    reason = rights.get("rights_basis")
    if rights.get("decision") == "REVIEW_REQUIRED":
        reason = REVIEW_REQUIRED_PILOT_EXCLUSION
    elif rights.get("allowed"):
        reason = "missing_media_candidate"
    return {
        "status": "rejected",
        "reason": reason,
        "record_id": evidence.get("nasa_id"),
        "writes": 0,
    }


async def write_record(
    conn: Any,
    record: dict[str, Any] | None,
    *,
    source_id: str,
    media_type_id: str,
    asset_manifest: dict[str, Any] | None = None,
    metadata_location: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write one NASA record into M36 tables only when Rights Class 10 allows it."""
    rights = classify_rights(record)
    if rights.get("decision") == "REVIEW_REQUIRED":
        return _rejected_result(record)
    if rights.get("decision") == "BLOCKED":
        return _rejected_result(record)

    normalized_candidates = normalize_record(
        record,
        asset_manifest=asset_manifest,
        metadata_location=metadata_location,
    )
    if not normalized_candidates:
        return _rejected_result(record)

    normalized = normalized_candidates[0]
    if normalized.get("rights_decision") != "ALLOWED":
        return _rejected_result(record)

    return await write_normalized_record(
        conn,
        runtime=_runtime(),
        raw_payload={
            "record": record,
            "asset_manifest": asset_manifest,
            "metadata_location": metadata_location,
        },
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
