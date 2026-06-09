"""M36 substrate write path for Art Institute of Chicago records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .normalize import normalize_record
from .rights import AIC_RIGHTS_POLICY_ID
from .technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "aic_adapter:sprint3"
SOURCE_SLUG = "aic"
BIOLOGICAL_ANCHOR_TOKENS = (
    "bird",
    "fish",
    "flower",
    "botanical",
    "plant",
    "animal",
    "insect",
    "mammal",
    "reptile",
    "amphibian",
)


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from AIC metadata."""
    subject_terms = " ".join(str(term).lower() for term in normalized.get("subject_terms", []))
    if media_type_id == "map":
        return "geographic"
    if any(token in subject_terms for token in BIOLOGICAL_ANCHOR_TOKENS):
        return "biological"
    if normalized.get("place_of_origin"):
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


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
        rights_policy_id=AIC_RIGHTS_POLICY_ID,
        workflow_record_id_key="aic_artwork_id",
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
    """Write one AIC record into M36 tables when AIC Rights Matrix v1 allows it."""
    normalized = normalize_record(raw_payload)
    if normalized.get("rights_decision") == "BLOCKED":
        return {
            "status": "rejected",
            "reason": normalized.get("aic_rights_basis"),
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

