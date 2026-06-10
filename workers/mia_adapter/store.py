"""M36 substrate write path for Mia collection records."""
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

WORKER_ID = "mia_adapter:sprint3"


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from Mia metadata."""
    if media_type_id == "map":
        return "geographic"
    text = " ".join(
        str(value).lower()
        for value in (
            normalized.get("title"),
            normalized.get("description"),
            " ".join(normalized.get("subject_terms") or []),
            " ".join(normalized.get("geographic_subjects") or []),
        )
        if value
    )
    if any(token in text for token in ("map", "view", "landscape", "cityscape")):
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "mia_object_id": normalized.get("mia_object_id"),
        "mia_rights_type": normalized.get("mia_rights_type"),
        "mia_rights_uri": normalized.get("mia_rights_uri"),
        "mia_rights_image_display": normalized.get("mia_rights_image_display"),
        "mia_image": normalized.get("mia_image"),
        "mia_public_access": normalized.get("mia_public_access"),
        "mia_restricted": normalized.get("mia_restricted"),
        "mia_primary_rendition_number": normalized.get("mia_primary_rendition_number"),
        "mia_cache_location": normalized.get("mia_cache_location"),
        "mia_image_width": normalized.get("mia_image_width"),
        "mia_image_height": normalized.get("mia_image_height"),
        "mia_accession_number": normalized.get("mia_accession_number"),
        "mia_source_record_uri": normalized.get("mia_source_record_uri"),
        "mia_image_url": normalized.get("mia_image_url"),
        "mia_iiif_manifest_url": normalized.get("mia_iiif_manifest_url"),
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
        rights_policy_id=RIGHTS_POLICY_ID,
        workflow_record_id_key="mia_object_id",
        anchor_type=anchor_type,
    )


def _rejected_result(record: dict[str, Any] | None) -> dict[str, Any]:
    rights = classify_rights(record)
    evidence = build_rights_evidence(record)
    reason = rights.get("rights_basis")
    if rights.get("allowed"):
        reason = "missing_media_candidate"
    return {
        "status": "rejected",
        "reason": reason,
        "record_id": evidence.get("mia_object_id"),
        "writes": 0,
    }


async def write_record(
    conn: Any,
    record: dict[str, Any] | None,
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Write one Mia record into M36 tables when Rights Matrix v2 allows it."""
    normalized_candidates = normalize_record(record)
    if not normalized_candidates:
        return _rejected_result(record)

    normalized = normalized_candidates[0]
    if normalized.get("mia_rights_type") not in {"Public Domain", "No Copyright–United States"}:
        return {
            "status": "rejected",
            "reason": "non_public_domain_rights_type",
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    derived_anchor_type = (
        anchor_type if anchor_type is not None else derive_anchor_type(normalized, media_type_id)
    )
    return await write_normalized_record(
        conn,
        runtime=_runtime(derived_anchor_type),
        raw_payload={"object": record},
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
