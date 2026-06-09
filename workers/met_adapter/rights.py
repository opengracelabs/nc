"""Metropolitan Museum of Art Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

MET_RIGHTS_POLICY_ID = "met_rights_matrix_v1"


def _present_image(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one Met API object with Met Rights Matrix v1."""
    if not isinstance(record, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": MET_RIGHTS_POLICY_ID,
        }

    if "isPublicDomain" not in record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": MET_RIGHTS_POLICY_ID,
        }

    is_public_domain = record.get("isPublicDomain")
    if is_public_domain is not True:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "not_public_domain",
            "rights_policy_id": MET_RIGHTS_POLICY_ID,
        }

    if not _present_image(record.get("primaryImage")):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_image_url",
            "rights_policy_id": MET_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "met_is_public_domain",
        "rights_policy_id": MET_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when the Met Rights Matrix permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])

