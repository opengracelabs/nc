"""Technical metadata extraction for Getty substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "getty-linked-art-technical-v1"
VALIDATOR_NAME = "getty_adapter.technical"
VALIDATOR_VERSION = "v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Getty record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "getty_object_id": normalized.get("getty_object_id"),
            "getty_rights_uri": normalized.get("getty_rights_uri"),
            "getty_manifest_uri": normalized.get("getty_manifest_uri"),
            "getty_image_service": normalized.get("getty_image_service"),
            "getty_accession_number": normalized.get("getty_accession_number"),
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

