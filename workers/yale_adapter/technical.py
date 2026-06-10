"""Technical metadata extraction for Yale LUX substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "yale-lux-technical-v1"
VALIDATOR_NAME = "yale_adapter.technical"
VALIDATOR_VERSION = "v1"
SCHEMA_STANDARD = "yale_lux_linked_art_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Yale record."""
    source_slug = str(normalized.get("yale_source_slug") or "yale_lux")
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=source_slug,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "yale_object_id": normalized.get("yale_object_id"),
            "yale_rights_uri": normalized.get("yale_rights_uri"),
            "yale_collection": normalized.get("yale_collection"),
            "yale_iiif_manifest": normalized.get("yale_iiif_manifest"),
            "yale_image_service": normalized.get("yale_image_service"),
            "ycba_rights_uri": normalized.get("ycba_rights_uri"),
            "ycba_attribution": normalized.get("ycba_attribution"),
            "yuag_rights_uri": normalized.get("yuag_rights_uri"),
            "yale_source_slug": normalized.get("yale_source_slug"),
        }
    )
    content["content_hash"] = content_hash(content)
    return content


__all__ = [
    "SCHEMA_STANDARD",
    "TECHNICAL_SCHEMA_VERSION",
    "VALIDATOR_NAME",
    "VALIDATOR_VERSION",
    "build_technical_metadata",
    "content_hash",
    "quality_flag",
    "validation_status",
]
