"""GBIF evidence rights classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

from .config import RIGHTS_POLICY_ID

CC_BY_URI = "https://creativecommons.org/licenses/by/4.0/"
CC_BY_NC_URI = "https://creativecommons.org/licenses/by-nc/4.0/"


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_license(value: str | None) -> str | None:
    """Normalize GBIF license strings to canonical URI form where possible."""
    text = _string(value)
    if not text:
        return None
    lowered = text.lower().replace("http://", "https://", 1)
    if "publicdomain/zero" in lowered or lowered in {"cc0", "cc0 1.0"}:
        return CC0_URI
    if "licenses/by-nc/" in lowered or lowered in {"cc-by-nc", "cc by-nc", "cc by nc"}:
        return CC_BY_NC_URI
    if "licenses/by/" in lowered or lowered in {"cc-by", "cc by"}:
        return CC_BY_URI
    if lowered.endswith("/"):
        return lowered
    if lowered.startswith("https://creativecommons.org/"):
        return f"{lowered}/"
    return text


def classify_license(value: str | None) -> dict[str, Any]:
    """Classify GBIF license evidence under SA-GBIF-001."""
    license_uri = normalize_license(value)
    if license_uri == CC0_URI:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "license_uri": license_uri,
            "rights_statement_uri": license_uri,
            "rights_status": "evidence_allowed",
            "rights_basis": "cc0_evidence",
            "rights_policy_id": RIGHTS_POLICY_ID,
            "attribution_required": False,
            "commercial_media_allowed": False,
        }
    if license_uri == CC_BY_URI:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "license_uri": license_uri,
            "rights_statement_uri": license_uri,
            "rights_status": "evidence_allowed",
            "rights_basis": "cc_by_evidence_attribution_required",
            "rights_policy_id": RIGHTS_POLICY_ID,
            "attribution_required": True,
            "commercial_media_allowed": False,
        }
    if license_uri == CC_BY_NC_URI:
        return {
            "decision": RightsDecision.REVIEW_REQUIRED.value,
            "allowed": False,
            "license_uri": license_uri,
            "rights_statement_uri": license_uri,
            "rights_status": "non_commercial_evidence_only",
            "rights_basis": "cc_by_nc_non_commercial",
            "rights_policy_id": RIGHTS_POLICY_ID,
            "attribution_required": True,
            "commercial_media_allowed": False,
        }
    if license_uri is None:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "license_uri": None,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_license",
            "rights_policy_id": RIGHTS_POLICY_ID,
            "attribution_required": False,
            "commercial_media_allowed": False,
        }
    return {
        "decision": RightsDecision.REVIEW_REQUIRED.value,
        "allowed": False,
        "license_uri": license_uri,
        "rights_statement_uri": license_uri,
        "rights_status": "pending_verification",
        "rights_basis": "unknown_license",
        "rights_policy_id": RIGHTS_POLICY_ID,
        "attribution_required": True,
        "commercial_media_allowed": False,
    }


def is_allowed_evidence(value: str | None) -> bool:
    """Return true for GBIF licenses allowed as evidence inputs."""
    return bool(classify_license(value)["allowed"])

