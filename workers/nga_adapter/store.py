"""M36 substrate write path for National Gallery of Art records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .client import (
    NgaDataset,
    get_constituents_for_object,
    get_images_for_object,
    get_primary_image,
    get_terms_for_object,
)
from .normalize import normalize_dataset_record
from .rights import NGA_RIGHTS_POLICY_ID
from .technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "nga_adapter:sprint3"
SOURCE_SLUG = "nga"
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
GEOGRAPHIC_ANCHOR_TOKENS = (
    "map",
    "landscape",
    "france",
    "japan",
    "china",
    "italy",
    "bridge",
)


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from NGA metadata."""
    subject_text = " ".join(
        str(term).lower() for term in normalized.get("subject_terms", [])
    )
    metadata_text = " ".join(
        str(value).lower()
        for value in (
            normalized.get("title"),
            normalized.get("description"),
            normalized.get("creator"),
            normalized.get("classification"),
            normalized.get("subclassification"),
            normalized.get("school"),
            normalized.get("place_executed"),
            normalized.get("creator_nationality"),
        )
        if value
    )
    combined = f"{subject_text} {metadata_text}"
    if media_type_id == "map":
        return "geographic"
    if normalized.get("place_executed"):
        return "geographic"
    if any(token in combined for token in BIOLOGICAL_ANCHOR_TOKENS):
        return "biological"
    if normalized.get("school"):
        return "geographic"
    if normalized.get("creator_nationality"):
        return "geographic"
    if any(token in combined for token in GEOGRAPHIC_ANCHOR_TOKENS):
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
        rights_policy_id=NGA_RIGHTS_POLICY_ID,
        workflow_record_id_key="nga_objectid",
        anchor_type=anchor_type,
    )


async def write_record(
    conn: Any,
    dataset: NgaDataset,
    object_id: int | str,
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Write one NGA record into M36 tables when NGA Rights Matrix v1 allows it."""
    cleaned_object_id = str(object_id).strip()
    object_row = dataset.objects_by_id.get(cleaned_object_id)
    images = get_images_for_object(dataset, cleaned_object_id)
    selected_image = get_primary_image(dataset, cleaned_object_id)
    terms = get_terms_for_object(dataset, cleaned_object_id)
    constituents = get_constituents_for_object(dataset, cleaned_object_id)

    normalized = normalize_dataset_record(dataset, object_id)
    if normalized.get("rights_decision") == "BLOCKED":
        return {
            "status": "rejected",
            "reason": normalized.get("nga_rights_basis"),
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
        raw_payload={
            "object": object_row,
            "selected_image": selected_image,
            "images": images,
            "terms": terms,
            "constituents": constituents,
        },
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
