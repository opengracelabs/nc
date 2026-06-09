"""Technical metadata extraction for SMK substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "smk-technical-v1"
VALIDATOR_NAME = "smk_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "smk"
SCHEMA_STANDARD = "smk_openaccess_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized SMK record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "smk_public_domain": normalized.get("smk_public_domain"),
            "smk_manifest_url": normalized.get("smk_manifest_url"),
            "smk_image_rights": normalized.get("smk_image_rights"),
            "smk_object_number": normalized.get("smk_object_number"),
            "smk_image_native": normalized.get("smk_image_native"),
            "smk_image_iiif_id": normalized.get("smk_image_iiif_id"),
            "smk_image_thumbnail": normalized.get("smk_image_thumbnail"),
            "image_mime_type": normalized.get("image_mime_type"),
            "image_hq": normalized.get("image_hq"),
            "artist": normalized.get("artist") or [],
            "production": normalized.get("production") or [],
            "object_names": normalized.get("object_names") or [],
            "materials": normalized.get("materials") or [],
            "techniques": normalized.get("techniques") or [],
            "dimensions": normalized.get("dimensions") or [],
            "images": normalized.get("images") or [],
            "content_subject": normalized.get("content_subject") or [],
            "frontend_url": normalized.get("frontend_url"),
            "object_url": normalized.get("object_url"),
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
