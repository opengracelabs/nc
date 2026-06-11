"""M36 substrate write path for NOAA discovery records.

NOAA Sprint 3 uses the shared M36 writer for ALLOWED records only. REVIEW_REQUIRED
records are pilot-excluded by final governance decision; BLOCKED records produce
zero writes.
"""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .client import flickr_record_to_discovery_payload, photolib_record_to_discovery_payload
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

WORKER_ID = "noaa_adapter:sprint3"
ANCHOR_TYPE = "geographic"
REVIEW_REQUIRED_PILOT_EXCLUSION = "review_required_pilot_exclusion"

NOAA_EVIDENCE_EXTENSION_FIELDS = (
    "source_system",
    "source_record_id",
    "source_url",
    "image_url",
    "title",
    "description",
    "creator",
    "credit",
    "owner_name",
    "license_id",
    "license_label",
    "rights_decision",
    "rights_basis",
    "partner_markers",
    "contributor_markers",
    "blocked_markers",
    "retrieved_at",
)


def _source_record(record: dict[str, Any] | None) -> dict[str, Any]:
    """Return the NOAA discovery payload shape expected by rights/normalize."""
    if not isinstance(record, dict):
        return {}
    if record.get("source_system"):
        return record
    if record.get("owner") or record.get("license") or record.get("url_z"):
        return flickr_record_to_discovery_payload(record)
    if record.get("url") or record.get("image_url") or record.get("credit"):
        return photolib_record_to_discovery_payload(record)
    return record


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    """Return adapter-owned NOAA rights evidence extension fields."""
    extension = {
        f"noaa_{field}": normalized.get(field)
        for field in NOAA_EVIDENCE_EXTENSION_FIELDS
    }
    extension.update({key: value for key, value in normalized.items() if key.startswith("noaa_")})
    return extension


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
        workflow_record_id_key="source_record_id",
        anchor_type=ANCHOR_TYPE,
    )


def _rejected_result(record: dict[str, Any] | None, *, reason: str | None = None) -> dict[str, Any]:
    source_record = _source_record(record)
    rights = classify_rights(source_record)
    evidence = build_rights_evidence(source_record)
    rejection_reason = reason or str(rights.get("rights_basis") or "missing_media_candidate")
    if rights.get("decision") == "REVIEW_REQUIRED":
        rejection_reason = REVIEW_REQUIRED_PILOT_EXCLUSION
    return {
        "status": "rejected",
        "reason": rejection_reason,
        "record_id": evidence.get("source_record_id"),
        "writes": 0,
    }


async def write_record(
    conn: Any,
    record: dict[str, Any] | None,
    *,
    source_id: str,
    media_type_id: str,
) -> dict[str, Any]:
    """Write one NOAA record into M36 only when NOAA Rights Class 9 allows it."""
    source_record = _source_record(record)
    rights = classify_rights(source_record)

    if rights.get("decision") == "REVIEW_REQUIRED":
        return _rejected_result(source_record)
    if rights.get("decision") == "BLOCKED":
        return _rejected_result(source_record)

    normalized_candidates = normalize_record(source_record)
    if not normalized_candidates:
        return _rejected_result(source_record, reason="missing_media_candidate")

    normalized = normalized_candidates[0]
    if normalized.get("rights_decision") != "ALLOWED":
        return _rejected_result(source_record)

    return await write_normalized_record(
        conn,
        runtime=_runtime(),
        raw_payload=source_record,
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )

