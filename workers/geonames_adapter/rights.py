"""GeoNames evidence attribution and license classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import RightsDecision

from .config import ATTRIBUTION_SHORT, CC_BY_4_URI, GEONAMES_BASE_URL, RIGHTS_POLICY_ID


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_license(value: str | None) -> str | None:
    """Normalize GeoNames license strings to canonical URI form."""
    text = _string(value)
    if not text:
        return None
    lowered = text.lower().replace("http://", "https://", 1)
    if "licenses/by/4.0" in lowered or lowered in {"cc-by-4.0", "cc by 4.0", "cc-by"}:
        return CC_BY_4_URI
    if lowered.endswith("/"):
        return lowered
    if lowered.startswith("https://creativecommons.org/"):
        return f"{lowered}/"
    return text


def build_attribution(geonames_id: str | int | None = None) -> dict[str, Any]:
    """Build governed GeoNames attribution metadata."""
    return {
        "name": "GeoNames",
        "url": GEONAMES_BASE_URL,
        "license": CC_BY_4_URI,
        "geonames_id": str(geonames_id) if geonames_id is not None else None,
        "statement": ATTRIBUTION_SHORT,
    }


def classify_license(value: str | None = CC_BY_4_URI) -> dict[str, Any]:
    """Classify GeoNames data licensing under DD-GEONAMES-001."""
    license_uri = normalize_license(value)
    if license_uri == CC_BY_4_URI:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "license_uri": license_uri,
            "rights_statement_uri": license_uri,
            "rights_status": "evidence_allowed",
            "rights_basis": "cc_by_4_attribution_required",
            "rights_policy_id": RIGHTS_POLICY_ID,
            "attribution_required": True,
            "commercial_media_allowed": False,
        }
    return {
        "decision": RightsDecision.BLOCKED.value,
        "allowed": False,
        "license_uri": license_uri,
        "rights_statement_uri": license_uri,
        "rights_status": "blocked",
        "rights_basis": "non_cc_by_4_geonames_evidence",
        "rights_policy_id": RIGHTS_POLICY_ID,
        "attribution_required": False,
        "commercial_media_allowed": False,
    }


def evidence_rights() -> dict[str, Any]:
    """Return the governed rights decision for GeoNames place evidence."""
    return classify_license(CC_BY_4_URI)


def is_allowed_evidence(value: str | None = CC_BY_4_URI) -> bool:
    """Return true only for governed CC BY 4.0 GeoNames evidence."""
    return bool(classify_license(value)["allowed"])

