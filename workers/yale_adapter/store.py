"""M36 substrate write path for Yale LUX records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .normalize import normalize_record
from .rights import YALE_RIGHTS_POLICY_ID
from .technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "yale_adapter:sprint3"


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from Yale metadata."""
    if media_type_id == "map":
        return "geographic"
    text = " ".join(
        str(value).lower()
        for value in (
            normalized.get("yale_collection"),
            normalized.get("title"),
            normalized.get("description"),
        )
        if value
    )
    if any(token in text for token in ("view", "landscape", "topograph", "map")):
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    source_slug = str(normalized.get("yale_source_slug") or "").strip()
    evidence = {
        "yale_object_id": normalized.get("yale_object_id"),
        "yale_iiif_manifest": normalized.get("yale_iiif_manifest"),
        "yale_image_service": normalized.get("yale_image_service"),
    }
    if source_slug == "ycba":
        evidence["ycba_rights_uri"] = normalized.get("ycba_rights_uri")
        evidence["ycba_attribution"] = normalized.get("ycba_attribution")
    if source_slug == "yuag":
        evidence["yuag_rights_uri"] = normalized.get("yuag_rights_uri")
    return evidence


def _runtime(source_slug: str, anchor_type: str) -> StoreRuntime:
    return StoreRuntime(
        worker_id=WORKER_ID,
        source_slug=source_slug,
        schema_standard=SCHEMA_STANDARD,
        technical_schema_version=TECHNICAL_SCHEMA_VERSION,
        validator_name=VALIDATOR_NAME,
        validator_version=VALIDATOR_VERSION,
        build_technical_metadata=_build_technical_metadata,
        validation_status=validation_status,
        build_evidence_extension=_build_evidence_extension,
        rights_policy_id=YALE_RIGHTS_POLICY_ID,
        workflow_record_id_key="yale_object_id",
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
    """Write one Yale record into M36 tables when Yale Rights Matrix v1 allows it."""
    normalized = normalize_record(record, manifest=manifest)
    if normalized.get("rights_decision") == "BLOCKED":
        return {
            "status": "rejected",
            "reason": normalized.get("yale_rights_basis"),
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    source_slug = str(normalized.get("yale_source_slug") or "").strip()
    if source_slug not in {"ycba", "yuag"}:
        return {
            "status": "rejected",
            "reason": "unsupported_yale_source",
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    derived_anchor_type = (
        anchor_type if anchor_type is not None else derive_anchor_type(normalized, media_type_id)
    )
    return await write_normalized_record(
        conn,
        runtime=_runtime(source_slug, derived_anchor_type),
        raw_payload={
            "object": record,
            "iiif_manifest": manifest,
        },
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
