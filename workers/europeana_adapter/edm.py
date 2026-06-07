"""Minimal Europeana EDM normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .rights import classify_rights, normalize_rights_uri


def _first(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


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
    """Normalize the Sprint 2 EDM fields used by rights and substrate gates."""
    item = _record_object(raw)
    rights_uri = normalize_rights_uri(_first(item.get("rights") or item.get("edmRights")))
    rights = classify_rights(rights_uri)

    return {
        "record_id": extract_record_id(raw),
        "title": _first(item.get("title") or item.get("dcTitle")),
        "rights_uri": rights_uri,
        "provider": _first(item.get("provider")),
        "dataProvider": _first(item.get("dataProvider")),
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
    if not normalized.get("provider"):
        warnings.append("missing_provider")
    if not normalized.get("dataProvider"):
        warnings.append("missing_data_provider")
    return warnings
