"""Technical metadata extraction for NGA substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "nga-technical-v1"
VALIDATOR_NAME = "nga_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "nga"
SCHEMA_STANDARD = "nga_openaccess_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized NGA record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "nga_openaccess": normalized.get("nga_openaccess"),
            "nga_image_uuid": normalized.get("nga_image_uuid"),
            "nga_iiifurl": normalized.get("nga_iiifurl"),
            "nga_iiif_thumb_url": normalized.get("nga_iiif_thumb_url"),
            "nga_viewtype": normalized.get("nga_viewtype"),
            "nga_objectid": normalized.get("nga_objectid"),
            "nga_accessionnum": normalized.get("nga_accessionnum"),
            "accession_number": normalized.get("accession_number"),
            "classification": normalized.get("classification"),
            "subclassification": normalized.get("subclassification"),
            "department_abbr": normalized.get("department_abbr"),
            "wikidataid": normalized.get("wikidataid"),
            "is_virtual": normalized.get("is_virtual"),
            "parent_id": normalized.get("parent_id"),
            "school": normalized.get("school"),
            "place_executed": normalized.get("place_executed"),
            "creator_nationality": normalized.get("creator_nationality"),
            "images": normalized.get("images") or [],
            "terms": normalized.get("terms") or [],
            "constituents": normalized.get("constituents") or [],
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
