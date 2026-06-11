"""NOAA Sprint 1 discovery normalization."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from .client import (
    extract_flickr_photos,
    flickr_record_to_discovery_payload,
)
from .config import RIGHTS_POLICY_ID, SCHEMA_STANDARD, SOURCE_SLUG
from .rights import classify_rights

REQUIRED_EVIDENCE_FIELDS = (
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
)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def canonical_json_hash(payload: Any) -> str:
    """Hash NOAA source payloads for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _retrieved_at(value: str | None = None) -> str:
    if value:
        return value
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_rights_evidence(
    record: dict[str, Any] | None,
    *,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Build the required NOAA Sprint 1 evidence envelope."""
    data = _as_dict(record)
    rights = classify_rights(data)
    return {
        "source_system": _string(data.get("source_system")),
        "source_record_id": _string(data.get("source_record_id") or data.get("id")),
        "source_url": _string(data.get("source_url")),
        "image_url": _string(data.get("image_url")),
        "title": _string(data.get("title")),
        "description": _string(data.get("description")),
        "creator": _string(data.get("creator")),
        "credit": _string(data.get("credit")),
        "owner_name": _string(data.get("owner_name") or data.get("ownername")),
        "license_id": _string(data.get("license_id") or data.get("license")),
        "license_label": _string(data.get("license_label")),
        "rights_statement_uri": rights["rights_statement_uri"],
        "rights_decision": rights["decision"],
        "rights_basis": rights["rights_basis"],
        "rights_policy_id": rights["rights_policy_id"],
        "partner_markers": rights["partner_markers"],
        "contributor_markers": rights["contributor_markers"],
        "blocked_markers": rights["blocked_markers"],
        "raw_payload_hash": canonical_json_hash(data),
        "retrieved_at": _retrieved_at(retrieved_at),
    }


def normalize_record(
    record: dict[str, Any] | None,
    *,
    retrieved_at: str | None = None,
) -> list[dict[str, Any]]:
    """Normalize one NOAA source record into zero or one discovery candidate."""
    data = _as_dict(record)
    evidence = build_rights_evidence(data, retrieved_at=retrieved_at)
    rights = classify_rights(data)
    if not rights["allowed"]:
        return []
    if not evidence["source_record_id"] or not evidence["source_url"] or not evidence["image_url"]:
        return []
    return [
        {
            "record_id": evidence["source_record_id"],
            "source_record_id": evidence["source_record_id"],
            "source_slug": SOURCE_SLUG,
            "schema_standard": SCHEMA_STANDARD,
            "title": evidence["title"],
            "description": evidence["description"],
            "creator": evidence["creator"] or evidence["credit"],
            "rights_uri": evidence["rights_statement_uri"],
            "source_url": evidence["source_url"],
            "representative_media_url": evidence["image_url"],
            "width_px": _int(data.get("width_px") or data.get("width") or data.get("o_width")),
            "height_px": _int(data.get("height_px") or data.get("height") or data.get("o_height")),
            "rights_decision": evidence["rights_decision"],
            "rights_allowed": rights["allowed"],
            "noaa_rights_class": "rights_class_9",
            "noaa_rights_policy_id": RIGHTS_POLICY_ID,
            "noaa_schema_standard": SCHEMA_STANDARD,
            "noaa_source_slug": SOURCE_SLUG,
            **evidence,
        }
    ]


def normalize_flickr_search_payload(
    payload: dict[str, Any] | None,
    *,
    retrieved_at: str | None = None,
) -> list[dict[str, Any]]:
    """Normalize a Flickr public-photo page into allowed NOAA discovery candidates."""
    candidates: list[dict[str, Any]] = []
    for photo in extract_flickr_photos(payload):
        source_record = flickr_record_to_discovery_payload(photo)
        candidates.extend(normalize_record(source_record, retrieved_at=retrieved_at))
    return candidates


def mandatory_evidence_warnings(evidence: dict[str, Any]) -> list[str]:
    """Return missing-field warnings for the required NOAA evidence envelope."""
    return [field for field in REQUIRED_EVIDENCE_FIELDS if field not in evidence]

