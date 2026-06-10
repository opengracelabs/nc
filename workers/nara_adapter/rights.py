"""NARA Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import PDM_URI, RightsDecision

from .client import extract_use_restriction
from .config import RIGHTS_POLICY_ID

NARA_RIGHTS_POLICY_ID = RIGHTS_POLICY_ID
PUBLIC_DOMAIN_MARK_URI = PDM_URI


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one NARA Catalog record with NARA Rights Matrix v1."""
    if not isinstance(record, dict) or not record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_object",
            "rights_policy_id": NARA_RIGHTS_POLICY_ID,
        }

    use_restriction = extract_use_restriction(record)
    if use_restriction == "Unrestricted":
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": PUBLIC_DOMAIN_MARK_URI,
            "rights_status": "pending_verification",
            "rights_basis": "nara_unrestricted",
            "rights_policy_id": NARA_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.BLOCKED.value,
        "allowed": False,
        "rights_statement_uri": None,
        "rights_status": "blocked",
        "rights_basis": "missing_use_restriction"
        if use_restriction is None
        else "restricted_use",
        "rights_policy_id": NARA_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when NARA Rights Matrix v1 permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])
