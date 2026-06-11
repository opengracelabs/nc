"""Wikidata structured-data evidence rights classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

from .config import RIGHTS_POLICY_ID


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_license(value: str | None) -> str | None:
    """Normalize Wikidata evidence license strings to canonical URI form."""
    text = _string(value)
    if not text:
        return None
    lowered = text.lower().replace("http://", "https://", 1)
    if "publicdomain/zero" in lowered or lowered in {"cc0", "cc0 1.0", "cc0 1.0 universal"}:
        return CC0_URI
    if lowered.endswith("/"):
        return lowered
    if lowered.startswith("https://creativecommons.org/"):
        return f"{lowered}/"
    return text


def classify_license(value: str | None = "CC0") -> dict[str, Any]:
    """Classify Wikidata structured data licensing under DD-WIKIDATA-001."""
    license_uri = normalize_license(value)
    if license_uri == CC0_URI:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "license_uri": license_uri,
            "rights_statement_uri": license_uri,
            "rights_status": "evidence_allowed",
            "rights_basis": "cc0_structured_data",
            "rights_policy_id": RIGHTS_POLICY_ID,
            "commercial_media_allowed": False,
        }
    return {
        "decision": RightsDecision.BLOCKED.value,
        "allowed": False,
        "license_uri": license_uri,
        "rights_statement_uri": license_uri,
        "rights_status": "blocked",
        "rights_basis": "non_cc0_wikidata_evidence",
        "rights_policy_id": RIGHTS_POLICY_ID,
        "commercial_media_allowed": False,
    }


def evidence_rights() -> dict[str, Any]:
    """Return the governed rights decision for Wikidata structured evidence."""
    return classify_license("CC0")


def is_allowed_evidence(value: str | None = "CC0") -> bool:
    """Return true only for CC0 Wikidata structured evidence."""
    return bool(classify_license(value)["allowed"])

