"""GeoNames place evidence normalization helpers."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import normalize_geonames_id
from .config import API_VERSION, GEONAMES_BASE_URL, SCHEMA_STANDARD, SOURCE_NAME, SOURCE_ROLE
from .rights import build_attribution, evidence_rights

EVIDENCE_FIELDS = (
    "source",
    "source_role",
    "schema_standard",
    "geonames_id",
    "name",
    "toponym_name",
    "alternate_names",
    "coordinates",
    "feature_class",
    "feature_code",
    "country_code",
    "country_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "population",
    "timezone",
    "hierarchy",
    "source_url",
    "api_version",
    "rights_decision",
    "rights_basis",
    "license_uri",
    "attribution_required",
    "attribution",
    "raw_payload_hash",
)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def canonical_json_hash(payload: Any) -> str:
    """Hash GeoNames payloads for replay-stable provenance."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def build_source_url(geonames_id: str | int | None) -> str | None:
    """Build a public GeoNames feature URL."""
    normalized_id = normalize_geonames_id(geonames_id)
    return f"{GEONAMES_BASE_URL}/{normalized_id}" if normalized_id else None


def normalize_alternate_names(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Normalize GeoNames alternateNames records."""
    if not isinstance(payload, dict):
        return []
    names = payload.get("alternateNames")
    if not isinstance(names, list):
        return []
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str | None, str]] = set()
    for item in names:
        if not isinstance(item, dict):
            continue
        name = _string(item.get("name"))
        if not name:
            continue
        language = _string(item.get("lang") or item.get("language"))
        key = (language, name)
        if key in seen:
            continue
        seen.add(key)
        normalized.append(
            {
                "name": name,
                "language": language,
                "preferred": bool(item.get("isPreferredName")),
                "short": bool(item.get("isShortName")),
            }
        )
    return normalized


def normalize_hierarchy_payload(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Normalize GeoNames hierarchyJSON records."""
    if not isinstance(payload, dict):
        return []
    records = payload.get("geonames")
    if not isinstance(records, list):
        return []
    hierarchy: list[dict[str, Any]] = []
    for item in records:
        if not isinstance(item, dict):
            continue
        geonames_id = normalize_geonames_id(item.get("geonameId"))
        if not geonames_id:
            continue
        hierarchy.append(
            {
                "geonames_id": geonames_id,
                "name": _string(item.get("name") or item.get("toponymName")),
                "feature_class": _string(item.get("fcl") or item.get("featureClass")),
                "feature_code": _string(item.get("fcode") or item.get("featureCode")),
                "country_code": _string(item.get("countryCode")),
                "admin1_code": _string(item.get("adminCode1")),
                "admin2_code": _string(item.get("adminCode2")),
            }
        )
    return hierarchy


def normalize_place_payload(
    payload: dict[str, Any] | None,
    *,
    hierarchy_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize one GeoNames place record as identity/geographic evidence."""
    data = payload if isinstance(payload, dict) else {}
    geonames_id = normalize_geonames_id(data.get("geonameId"))
    latitude = _float(data.get("lat"))
    longitude = _float(data.get("lng"))
    rights = evidence_rights()
    hash_payload = {
        "place": data,
        "hierarchy": hierarchy_payload if isinstance(hierarchy_payload, dict) else {},
    }
    evidence = {
        "source": SOURCE_NAME,
        "source_role": SOURCE_ROLE,
        "schema_standard": SCHEMA_STANDARD,
        "geonames_id": geonames_id,
        "name": _string(data.get("name")),
        "toponym_name": _string(data.get("toponymName")),
        "alternate_names": normalize_alternate_names(data),
        "coordinates": (
            {"latitude": latitude, "longitude": longitude}
            if latitude is not None and longitude is not None
            else None
        ),
        "feature_class": _string(data.get("fcl") or data.get("featureClass")),
        "feature_code": _string(data.get("fcode") or data.get("featureCode")),
        "country_code": _string(data.get("countryCode")),
        "country_name": _string(data.get("countryName")),
        "admin1_code": _string(data.get("adminCode1")),
        "admin1_name": _string(data.get("adminName1")),
        "admin2_code": _string(data.get("adminCode2")),
        "admin2_name": _string(data.get("adminName2")),
        "population": _int(data.get("population")),
        "timezone": _string(data.get("timezone", {}).get("timeZoneId"))
        if isinstance(data.get("timezone"), dict)
        else _string(data.get("timezone")),
        "hierarchy": normalize_hierarchy_payload(hierarchy_payload),
        "source_url": build_source_url(geonames_id),
        "api_version": API_VERSION,
        "rights_decision": rights["decision"],
        "rights_basis": rights["rights_basis"],
        "license_uri": rights["license_uri"],
        "attribution_required": rights["attribution_required"],
        "attribution": build_attribution(geonames_id),
        "raw_payload_hash": canonical_json_hash(hash_payload),
    }
    return evidence


def build_place_identity_evidence(
    payload: dict[str, Any] | None,
    *,
    hierarchy_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build replay-stable GeoNames place identity evidence."""
    return normalize_place_payload(payload, hierarchy_payload=hierarchy_payload)

