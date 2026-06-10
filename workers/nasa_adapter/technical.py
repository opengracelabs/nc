"""Technical metadata extraction for NASA discovery candidates."""
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

TECHNICAL_SCHEMA_VERSION = "nasa-images-technical-v1"
VALIDATOR_NAME = "nasa_adapter.technical"
VALIDATOR_VERSION = "v1"

NASA_EVIDENCE_FIELDS = (
    "nasa_id",
    "nasa_center",
    "nasa_media_type",
    "nasa_rights_uri",
    "nasa_rights_basis",
    "nasa_asset_manifest_url",
    "nasa_metadata_url",
    "nasa_original_url",
    "nasa_large_url",
    "nasa_preview_url",
    "nasa_selected_asset_url",
    "nasa_photographer",
    "nasa_secondary_creator",
    "nasa_keywords",
    "nasa_album",
    "nasa_partner_markers",
    "nasa_copyright_detected",
    "nasa_publicity_risk_detected",
    "nasa_source_api",
    "nasa_rights_policy_id",
    "nasa_schema_standard",
    "nasa_source_slug",
)

def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized NASA candidate."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update({field: normalized.get(field) for field in NASA_EVIDENCE_FIELDS})
    content["content_hash"] = content_hash(content)
    return content


__all__ = [
    "NASA_EVIDENCE_FIELDS",
    "TECHNICAL_SCHEMA_VERSION",
    "VALIDATOR_NAME",
    "VALIDATOR_VERSION",
    "build_technical_metadata",
    "content_hash",
    "quality_flag",
    "validation_status",
]
