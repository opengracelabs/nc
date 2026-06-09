"""Technical metadata extraction for AIC substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "aic-technical-v1"
VALIDATOR_NAME = "aic_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "aic"
SCHEMA_STANDARD = "aic_openaccess_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized AIC record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "aic_image_id": normalized.get("aic_image_id"),
            "aic_manifest_url": normalized.get("aic_manifest_url"),
            "aic_is_public_domain": normalized.get("aic_is_public_domain"),
            "aic_copyright_notice": normalized.get("aic_copyright_notice"),
            "aic_api_link": normalized.get("aic_api_link"),
            "additional_images": normalized.get("additional_images") or [],
            "alt_image_ids": normalized.get("alt_image_ids") or [],
            "date_start": normalized.get("date_start"),
            "date_end": normalized.get("date_end"),
            "artist_title": normalized.get("artist_title"),
            "place_of_origin": normalized.get("place_of_origin"),
            "department": normalized.get("department"),
            "department_id": normalized.get("department_id"),
            "medium": normalized.get("medium"),
            "style_titles": normalized.get("style_titles") or [],
            "classification_titles": normalized.get("classification_titles") or [],
            "accession_number": normalized.get("accession_number"),
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

