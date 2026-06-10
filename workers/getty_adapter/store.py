"""M36 substrate write path for Getty Linked Art records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .config import RIGHTS_POLICY_ID, SCHEMA_STANDARD, SOURCE_SLUG
from .normalize import normalize_record
from .technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "getty_adapter:sprint3"


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from Getty metadata."""
    if media_type_id == "map":
        return "geographic"
    text = " ".join(
        str(value).lower()
        for value in (
            normalized.get("title"),
            normalized.get("description"),
            " ".join(normalized.get("subject_terms") or []),
        )
        if value
    )
    if any(token in text for token in ("map", "view", "landscape", "cityscape", "topograph")):
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "getty_object_id": normalized.get("getty_object_id"),
        "getty_rights_uri": normalized.get("getty_rights_uri"),
        "getty_manifest_uri": normalized.get("getty_manifest_uri"),
        "getty_image_service": normalized.get("getty_image_service"),
        "getty_accession_number": normalized.get("getty_accession_number"),
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
        workflow_record_id_key="getty_object_id",
        anchor_type=anchor_type,
    )


async def write_record(
    conn: Any,
    record: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None = None,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Write one Getty record into M36 tables when Getty Rights Matrix v1 allows it."""
    normalized = normalize_record(record, manifest=manifest)
    if normalized.get("rights_decision") == "BLOCKED":
        return {
            "status": "rejected",
            "reason": normalized.get("getty_rights_basis"),
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }
    if not normalized.get("getty_manifest_uri") or not normalized.get("getty_image_service"):
        return {
            "status": "rejected",
            "reason": "missing_iiif_evidence",
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    derived_anchor_type = (
        anchor_type if anchor_type is not None else derive_anchor_type(normalized, media_type_id)
    )
    return await write_normalized_record(
        conn,
        runtime=_runtime(derived_anchor_type),
        raw_payload={
            "object": record,
            "iiif_manifest": manifest,
        },
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )

