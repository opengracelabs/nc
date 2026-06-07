"""Technical metadata extraction for Rijksmuseum substrate intake."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .edm import mandatory_field_warnings

TECHNICAL_SCHEMA_VERSION = "rijksmuseum-edm-technical-v1"
VALIDATOR_NAME = "rijksmuseum_adapter.technical"
VALIDATOR_VERSION = "v1"
_MINIMUM_VISUAL_LONG_EDGE_PX = 400


def _int(value: Any) -> int | None:
    if isinstance(value, list):
        value = value[0] if value else None
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def content_hash(content: dict[str, Any]) -> str:
    """Return a replay-stable hash for technical metadata content."""
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def quality_flag(width_px: int | None, height_px: int | None) -> str:
    """Classify the visual quality baseline from MSC v1.2 Article 29.2(d)."""
    if width_px is None and height_px is None:
        return "unknown_dimensions"
    longest_edge = max(width_px or 0, height_px or 0)
    if longest_edge < _MINIMUM_VISUAL_LONG_EDGE_PX:
        return "below_minimum"
    return "meets_minimum"


def build_technical_metadata(normalized: dict[str, Any], *, media_type_id: str) -> dict[str, Any]:
    """Build media_technical_metadata.content for a normalized Rijksmuseum record."""
    width_px = _int(normalized.get("width_px"))
    height_px = _int(normalized.get("height_px"))
    content = {
        "source": "rijksmuseum",
        "schema_standard": "edm",
        "record_id": normalized.get("record_id"),
        "media_type_id": media_type_id,
        "edm_type": normalized.get("edm_type"),
        "title": normalized.get("title"),
        "description": normalized.get("description"),
        "date": normalized.get("date"),
        "creator": normalized.get("creator"),
        "provider": normalized.get("provider"),
        "data_provider": normalized.get("dataProvider"),
        "rights_uri": normalized.get("rights_uri"),
        "source_url": normalized.get("source_url"),
        "representative_media_url": normalized.get("representative_media_url"),
        "preview_urls": normalized.get("preview_urls") or [],
        "width_px": width_px,
        "height_px": height_px,
        "quality_flag": quality_flag(width_px, height_px),
        "subject_terms": [
            {"term": term, "controlled_vocabulary": False}
            for term in normalized.get("subject_terms", [])
        ],
        "mandatory_field_warnings": mandatory_field_warnings(normalized),
    }
    content["content_hash"] = content_hash(content)
    return content


def validation_status(content: dict[str, Any]) -> str:
    """Return the worker validation status for current visual metadata."""
    if not content.get("record_id") or not content.get("title"):
        return "invalid"
    if not content.get("representative_media_url") and not content.get("source_url"):
        return "invalid"
    return "valid"
