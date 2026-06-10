"""Mia Rights Matrix v2 classification.

Rights Matrix v2 treats ``rights_type`` as the sole rights authority. Metadata
CC0, ``restricted``, and ``public_access`` are evidence only.
"""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import NOC_US_URI, PDM_URI, RightsDecision

from .config import RIGHTS_POLICY_ID

MIA_RIGHTS_POLICY_ID = RIGHTS_POLICY_ID
PUBLIC_DOMAIN_MARK_URI = PDM_URI
NO_COPYRIGHT_US_URI = NOC_US_URI
PUBLIC_DOMAIN_RIGHTS_TYPE = "Public Domain"
NO_COPYRIGHT_US_RIGHTS_TYPE = "No Copyright–United States"

OBSERVED_RIGHTS_TYPES: tuple[str, ...] = (
    "Public Domain",
    "In Copyright",
    "Unknown",
    "Not Evaluated",
    "In Copyright–Educational Use",
    "Copyright Not Evaluated",
    "No Known Copyright",
    "No Copyright–United States",
    "In Copyright–Non-Commercial Use",
)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def extract_rights_type(record: dict[str, Any] | None) -> str | None:
    """Extract Mia's authoritative rights_type value."""
    if not isinstance(record, dict):
        return None
    return _string(record.get("rights_type"))


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one Mia object with Rights Matrix v2."""
    if not isinstance(record, dict) or not record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_object",
            "rights_policy_id": MIA_RIGHTS_POLICY_ID,
        }

    rights_type = extract_rights_type(record)
    if rights_type is None:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_type",
            "rights_policy_id": MIA_RIGHTS_POLICY_ID,
        }

    if rights_type == PUBLIC_DOMAIN_RIGHTS_TYPE:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": PUBLIC_DOMAIN_MARK_URI,
            "rights_status": "pending_verification",
            "rights_basis": "mia_public_domain",
            "rights_policy_id": MIA_RIGHTS_POLICY_ID,
        }

    if rights_type == NO_COPYRIGHT_US_RIGHTS_TYPE:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": NO_COPYRIGHT_US_URI,
            "rights_status": "pending_verification",
            "rights_basis": "mia_no_copyright_us",
            "rights_policy_id": MIA_RIGHTS_POLICY_ID,
        }

    basis = (
        "blocked_observed_rights_type"
        if rights_type in OBSERVED_RIGHTS_TYPES
        else "blocked_unrecognized_rights_type"
    )
    return {
        "decision": RightsDecision.BLOCKED.value,
        "allowed": False,
        "rights_statement_uri": None,
        "rights_status": "blocked",
        "rights_basis": basis,
        "rights_policy_id": MIA_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when Mia Rights Matrix v2 permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])
