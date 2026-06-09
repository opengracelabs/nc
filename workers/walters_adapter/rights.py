"""Walters Art Museum Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

WALTERS_RIGHTS_POLICY_ID = "walters_rights_matrix_v1"


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def classify_rights(
    object_row: dict[str, Any] | None,
    image_row: dict[str, Any] | None,
) -> dict[str, str | bool | None]:
    """Classify one joined Walters object/image pair with Walters Rights Matrix v1."""
    if not isinstance(object_row, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_object_record",
            "rights_policy_id": WALTERS_RIGHTS_POLICY_ID,
        }

    if not isinstance(image_row, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_primary_image",
            "rights_policy_id": WALTERS_RIGHTS_POLICY_ID,
        }

    if not _string(image_row.get("ImageURL")):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_image_url",
            "rights_policy_id": WALTERS_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "walters_institution_cc0",
        "rights_policy_id": WALTERS_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(
    object_row: dict[str, Any] | None,
    image_row: dict[str, Any] | None,
) -> bool:
    """Return true only when Walters Rights Matrix permits ingest consideration."""
    return bool(classify_rights(object_row, image_row)["allowed"])
