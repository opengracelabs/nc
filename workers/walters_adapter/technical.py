"""Technical metadata extraction for Walters substrate intake."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.technical import (
    build_technical_metadata as _build_technical_metadata,
)
from workers.shared_media_adapter.technical import (
    content_hash,
    quality_flag,
    validation_status,
)

from .normalize import mandatory_field_warnings

TECHNICAL_SCHEMA_VERSION = "walters-technical-v1"
VALIDATOR_NAME = "walters_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "walters"
SCHEMA_STANDARD = "walters_opendata_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Walters record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "walters_object_id": normalized.get("walters_object_id"),
            "walters_object_number": normalized.get("walters_object_number"),
            "walters_image_url": normalized.get("walters_image_url"),
            "walters_media_xref_id": normalized.get("walters_media_xref_id"),
            "walters_is_primary": normalized.get("walters_is_primary"),
            "walters_collection_ids": normalized.get("walters_collection_ids") or [],
            "walters_collection_names": normalized.get("walters_collection_names") or [],
            "accession_number": normalized.get("accession_number"),
            "object_name": normalized.get("object_name"),
            "classification": normalized.get("classification"),
            "medium": normalized.get("medium"),
            "culture": normalized.get("culture"),
            "style": normalized.get("style"),
            "dynasty": normalized.get("dynasty"),
            "credit_line": normalized.get("credit_line"),
            "provenance": normalized.get("provenance"),
            "date_start": normalized.get("date_start"),
            "date_end": normalized.get("date_end"),
            "creator_nationality": normalized.get("creator_nationality"),
            "images": normalized.get("images") or [],
            "creators": normalized.get("creators") or [],
        }
    )
    content["content_hash"] = content_hash(content)
    return content


__all__ = [
    "TECHNICAL_SCHEMA_VERSION",
    "VALIDATOR_NAME",
    "VALIDATOR_VERSION",
    "build_technical_metadata",
    "content_hash",
    "quality_flag",
    "validation_status",
]
