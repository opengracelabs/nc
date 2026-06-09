"""National Gallery of Art Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

NGA_RIGHTS_POLICY_ID = "nga_rights_matrix_v1"


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def classify_rights(image_row: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one NGA published_images row with NGA Rights Matrix v1."""
    if not isinstance(image_row, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_published_image",
            "rights_policy_id": NGA_RIGHTS_POLICY_ID,
        }

    if _string(image_row.get("openaccess")) != "1":
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "not_open_access",
            "rights_policy_id": NGA_RIGHTS_POLICY_ID,
        }

    if not _string(image_row.get("iiifurl")):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_iiif_url",
            "rights_policy_id": NGA_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "nga_open_access_cc0",
        "rights_policy_id": NGA_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(image_row: dict[str, Any] | None) -> bool:
    """Return true only when NGA Rights Matrix permits ingest consideration."""
    return bool(classify_rights(image_row)["allowed"])
