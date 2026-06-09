"""Art Institute of Chicago Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

AIC_RIGHTS_POLICY_ID = "aic_rights_matrix_v1"


def _present_image_id(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one AIC artwork with AIC Rights Matrix v1."""
    if not isinstance(record, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": AIC_RIGHTS_POLICY_ID,
        }

    if "is_public_domain" not in record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": AIC_RIGHTS_POLICY_ID,
        }

    if record.get("is_public_domain") is not True:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "not_public_domain",
            "rights_policy_id": AIC_RIGHTS_POLICY_ID,
        }

    if not _present_image_id(record.get("image_id")):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_image_id",
            "rights_policy_id": AIC_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "aic_is_public_domain",
        "rights_policy_id": AIC_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when the AIC Rights Matrix permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])

