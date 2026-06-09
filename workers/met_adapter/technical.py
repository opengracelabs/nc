"""Technical metadata extraction for Met substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "met-technical-v1"
VALIDATOR_NAME = "met_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "met"
SCHEMA_STANDARD = "met_openaccess_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Met record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "met_object_id": normalized.get("met_object_id"),
            "met_is_public_domain": normalized.get("met_is_public_domain"),
            "met_rights_basis": normalized.get("met_rights_basis"),
            "primary_image": normalized.get("primary_image"),
            "additional_images": normalized.get("additional_images") or [],
            "department": normalized.get("department"),
            "culture": normalized.get("culture"),
            "period": normalized.get("period"),
            "country": normalized.get("country"),
            "region": normalized.get("region"),
            "subregion": normalized.get("subregion"),
            "city": normalized.get("city"),
            "geography_type": normalized.get("geography_type"),
            "artist_wikidata_url": normalized.get("artist_wikidata_url"),
            "artist_ulan_url": normalized.get("artist_ulan_url"),
            "object_wikidata_url": normalized.get("object_wikidata_url"),
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

