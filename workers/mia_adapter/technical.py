"""Technical metadata extraction for Mia substrate intake."""
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

from .config import SCHEMA_STANDARD, SOURCE_SLUG
from .normalize import mandatory_field_warnings

TECHNICAL_SCHEMA_VERSION = "mia-collection-technical-v1"
VALIDATOR_NAME = "mia_adapter.technical"
VALIDATOR_VERSION = "v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Mia record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
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
