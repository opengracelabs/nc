"""Europeana EDM normalization for substrate intake."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .rights import classify_rights, normalize_rights_uri


def _first(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw Europeana payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _record_object(raw: dict[str, Any]) -> dict[str, Any]:
    obj = raw.get("object")
    if isinstance(obj, dict):
        return obj
    return raw


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract the stable Europeana record identifier."""
    item = _record_object(raw)
    value = item.get("id") or item.get("about") or raw.get("id")
    return str(value).strip() if value else None


def normalize_edm_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize EDM fields used by rights, technical metadata, and substrate gates."""
    item = _record_object(raw)
    rights_uri = normalize_rights_uri(_first(item.get("rights") or item.get("edmRights")))
    rights = classify_rights(rights_uri)
    representative_url = _first(item.get("isShownBy") or item.get("object"))

    return {
        "record_id": extract_record_id(raw),
        "title": _first(item.get("title") or item.get("dcTitle")),
        "description": _first(item.get("description") or item.get("dcDescription")),
        "date": _first(item.get("date") or item.get("dcDate")),
        "creator": _first(item.get("creator") or item.get("dcCreator")),
        "subject_terms": _list(item.get("subject") or item.get("dcSubject")),
        "rights_uri": rights_uri,
        "provider": _first(item.get("provider")),
        "dataProvider": _first(item.get("dataProvider")),
        "edm_type": _first(item.get("type") or item.get("edmType")),
        "source_url": _first(item.get("isShownAt") or item.get("guid")),
        "representative_media_url": representative_url,
        "preview_urls": _list(item.get("edmPreview") or item.get("preview")),
        "width_px": _first(item.get("width") or item.get("width_px")),
        "height_px": _first(item.get("height") or item.get("height_px")),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "raw_payload_hash": canonical_json_hash(raw),
    }


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the Europeana substrate gate."""
    warnings: list[str] = []
    if not normalized.get("record_id"):
        warnings.append("missing_record_id")
    if not normalized.get("title"):
        warnings.append("missing_title")
    if not normalized.get("rights_uri"):
        warnings.append("missing_rights_uri")
    if not normalized.get("description"):
        warnings.append("missing_description")
    if not normalized.get("date"):
        warnings.append("missing_date")
    if not normalized.get("provider"):
        warnings.append("missing_provider")
    if not normalized.get("dataProvider"):
        warnings.append("missing_data_provider")
    return warnings
