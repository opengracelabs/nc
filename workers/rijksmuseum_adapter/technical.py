"""Technical metadata extraction for Rijksmuseum substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "rijksmuseum-edm-technical-v1"
VALIDATOR_NAME = "rijksmuseum_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "rijksmuseum"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Rijksmuseum record."""
    return _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        mandatory_warnings=mandatory_field_warnings,
    )


__all__ = [
    "TECHNICAL_SCHEMA_VERSION",
    "VALIDATOR_NAME",
    "VALIDATOR_VERSION",
    "build_technical_metadata",
    "content_hash",
    "quality_flag",
    "validation_status",
]
