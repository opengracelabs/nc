"""Technical evidence helpers for NOAA discovery records.

This module is intentionally read-only. It builds a replay-stable technical
evidence envelope and does not call any M36 store path.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .config import SCHEMA_STANDARD, SOURCE_SLUG
from .normalize import REQUIRED_EVIDENCE_FIELDS, mandatory_evidence_warnings

TECHNICAL_SCHEMA_VERSION = "noaa-discovery-technical-v1"
VALIDATOR_NAME = "noaa_adapter.technical"
VALIDATOR_VERSION = "v1"

NOAA_TECHNICAL_EVIDENCE_FIELDS = (
    "source_system",
    "source_record_id",
    "source_url",
    "image_url",
    "title",
    "description",
    "creator",
    "credit",
    "owner_name",
    "license_id",
    "license_label",
    "rights_statement_uri",
    "rights_decision",
    "rights_basis",
    "rights_policy_id",
    "partner_markers",
    "contributor_markers",
    "blocked_markers",
    "raw_payload_hash",
    "retrieved_at",
    "noaa_rights_class",
    "noaa_rights_policy_id",
    "noaa_schema_standard",
    "noaa_source_slug",
)


def _int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def content_hash(content: dict[str, Any]) -> str:
    """Return a replay-stable hash for NOAA technical evidence."""
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def quality_flag(width_px: int | None, height_px: int | None) -> str:
    """Classify a basic visual quality baseline for discovery candidates."""
    if width_px is None and height_px is None:
        return "unknown_dimensions"
    if max(width_px or 0, height_px or 0) < 400:
        return "below_minimum"
    return "meets_minimum"


def build_technical_metadata(
    normalized: dict[str, Any],
    media_type_id: str | None = None,
) -> dict[str, Any]:
    """Build discovery-only technical metadata for a normalized NOAA candidate."""
    width_px = _int(normalized.get("width_px"))
    height_px = _int(normalized.get("height_px"))
    content = {
        "source": SOURCE_SLUG,
        "schema_standard": SCHEMA_STANDARD,
        "technical_schema_version": TECHNICAL_SCHEMA_VERSION,
        "validator_name": VALIDATOR_NAME,
        "validator_version": VALIDATOR_VERSION,
        "record_id": normalized.get("record_id"),
        "title": normalized.get("title"),
        "description": normalized.get("description"),
        "creator": normalized.get("creator"),
        "source_url": normalized.get("source_url"),
        "representative_media_url": normalized.get("representative_media_url"),
        "width_px": width_px,
        "height_px": height_px,
        "quality_flag": quality_flag(width_px, height_px),
        "mandatory_evidence_warnings": mandatory_evidence_warnings(normalized),
        "required_evidence_fields": list(REQUIRED_EVIDENCE_FIELDS),
    }
    if media_type_id is not None:
        content["media_type_id"] = media_type_id
    content.update({field: normalized.get(field) for field in NOAA_TECHNICAL_EVIDENCE_FIELDS})
    content["content_hash"] = content_hash(content)
    return content


def validation_status(content: dict[str, Any]) -> str:
    """Return a validation status for NOAA discovery technical evidence."""
    if not content.get("record_id") or not content.get("title"):
        return "invalid"
    if not content.get("representative_media_url") and not content.get("source_url"):
        return "invalid"
    if content.get("mandatory_evidence_warnings"):
        return "warning"
    return "valid"


__all__ = [
    "NOAA_TECHNICAL_EVIDENCE_FIELDS",
    "TECHNICAL_SCHEMA_VERSION",
    "VALIDATOR_NAME",
    "VALIDATOR_VERSION",
    "build_technical_metadata",
    "content_hash",
    "quality_flag",
    "validation_status",
]

