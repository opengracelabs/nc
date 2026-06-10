"""M36 substrate write path for Walters Art Museum records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .client import (
    WaltersDataset,
    get_creators_for_object,
    get_images_for_object,
    get_primary_image,
)
from .normalize import normalize_dataset_record
from .rights import WALTERS_RIGHTS_POLICY_ID
from .technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "walters_adapter:sprint3"
SOURCE_SLUG = "walters"
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
    "zoological",
)
GEOGRAPHIC_ANCHOR_TOKENS = (
    "byzantine",
    "egyptian",
    "etruscan",
    "french",
    "greek",
    "islamic",
    "japanese",
    "roman",
)
GEOGRAPHIC_COLLECTION_CODES = {
    "AME",
    "ANE",
    "BYZ",
    "CHN",
    "EGY",
    "ETH",
    "GRK",
    "IND",
    "ISL",
    "JAP",
    "SEA",
}


def derive_anchor_type(normalized: dict[str, Any], media_type_id: str) -> str:
    """Derive a governed source_item anchor type from Walters metadata."""
    classification = str(normalized.get("classification") or normalized.get("edm_type") or "")
    object_name = str(normalized.get("object_name") or "")
    manuscript_text = f"{classification} {object_name}".lower()
    if media_type_id == "map":
        return "geographic"
    if "manuscript" in manuscript_text or "book" in manuscript_text:
        return "geographic"
    if normalized.get("culture"):
        return "geographic"
    if normalized.get("creator_nationality"):
        return "geographic"

    subject_text = " ".join(
        str(term).lower() for term in normalized.get("subject_terms", [])
    )
    metadata_text = " ".join(
        str(value).lower()
        for value in (
            normalized.get("title"),
            normalized.get("description"),
            normalized.get("object_name"),
            " ".join(normalized.get("walters_collection_names") or []),
        )
        if value
    )
    combined = f"{subject_text} {metadata_text}"
    if any(token in combined for token in BIOLOGICAL_ANCHOR_TOKENS):
        return "biological"
    if any(
        str(code).upper() in GEOGRAPHIC_COLLECTION_CODES
        for code in normalized.get("walters_collection_ids", [])
    ):
        return "geographic"
    if any(token in combined for token in GEOGRAPHIC_ANCHOR_TOKENS):
        return "geographic"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "walters_object_id": normalized.get("walters_object_id"),
        "walters_object_number": normalized.get("walters_object_number"),
        "walters_image_url": normalized.get("walters_image_url"),
        "walters_media_xref_id": normalized.get("walters_media_xref_id"),
        "walters_is_primary": normalized.get("walters_is_primary"),
        "walters_collection_ids": normalized.get("walters_collection_ids"),
        "walters_collection_names": normalized.get("walters_collection_names"),
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
        rights_policy_id=WALTERS_RIGHTS_POLICY_ID,
        workflow_record_id_key="walters_object_id",
        anchor_type=anchor_type,
    )


async def write_record(
    conn: Any,
    dataset: WaltersDataset,
    object_id: int | str,
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Write one Walters record into M36 tables when Walters Rights Matrix v1 allows it."""
    cleaned_object_id = str(object_id).strip()
    object_row = dataset.objects_by_id.get(cleaned_object_id)
    images = get_images_for_object(dataset, cleaned_object_id)
    selected_image = get_primary_image(dataset, cleaned_object_id)
    creators = get_creators_for_object(dataset, cleaned_object_id)

    normalized = normalize_dataset_record(dataset, object_id)
    if normalized.get("rights_decision") == "BLOCKED":
        return {
            "status": "rejected",
            "reason": normalized.get("walters_rights_basis"),
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
            "creators": creators,
        },
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
