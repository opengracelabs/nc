"""Technical metadata extraction for CMA substrate intake."""
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

TECHNICAL_SCHEMA_VERSION = "cma-technical-v1"
VALIDATOR_NAME = "cma_adapter.technical"
VALIDATOR_VERSION = "v1"
SOURCE_SLUG = "cma"
SCHEMA_STANDARD = "cma_openaccess_v1"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized CMA record."""
    content = _build_technical_metadata(
        normalized,
        media_type_id=media_type_id,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        mandatory_warnings=mandatory_field_warnings,
    )
    content.update(
        {
            "cma_share_license_status": normalized.get("cma_share_license_status"),
            "cma_copyright": normalized.get("cma_copyright"),
            "cma_image_web_url": normalized.get("cma_image_web_url"),
            "cma_image_print_url": normalized.get("cma_image_print_url"),
            "cma_image_full_url": normalized.get("cma_image_full_url"),
            "accession_number": normalized.get("accession_number"),
            "additional_images": normalized.get("additional_images") or [],
            "alternate_images": normalized.get("alternate_images") or [],
            "creation_date_earliest": normalized.get("creation_date_earliest"),
            "creation_date_latest": normalized.get("creation_date_latest"),
            "creators": normalized.get("creators") or [],
            "culture": normalized.get("culture"),
            "department": normalized.get("department"),
            "collection": normalized.get("collection"),
            "technique": normalized.get("technique"),
            "find_spot": normalized.get("find_spot"),
            "creditline": normalized.get("creditline"),
            "is_highlight": normalized.get("is_highlight"),
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
