"""Technical metadata extraction for Gallica substrate intake."""
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

from .edm import mandatory_field_warnings

TECHNICAL_SCHEMA_VERSION = "gallica-technical-v1"
VALIDATOR_NAME = "gallica_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "gallica"
SCHEMA_STANDARD = "gallica_api_profile_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Gallica record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "gallica_ark": normalized.get("record_id"),
            "iiif_manifest_url": normalized.get("iiif_manifest_url"),
            "iiif_image_service_url": normalized.get("iiif_image_service_url"),
            "pagination_pages": normalized.get("pagination_pages"),
            "selected_page": normalized.get("selected_page"),
            "iiif_region": normalized.get("iiif_region"),
            "gallica_rights_basis": normalized.get("gallica_rights_basis"),
            "gallica_rights_source": normalized.get("gallica_rights_source"),
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

