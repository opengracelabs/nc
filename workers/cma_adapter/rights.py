"""Cleveland Museum of Art Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

CMA_RIGHTS_POLICY_ID = "cma_rights_matrix_v1"


def _present_image(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _image_tier_url(record: dict[str, Any], tier: str) -> str | None:
    images = record.get("images")
    if not isinstance(images, dict):
        return None
    image = images.get(tier)
    if not isinstance(image, dict):
        return None
    value = image.get("url")
    return value if _present_image(value) else None


def has_usable_image(record: dict[str, Any]) -> bool:
    """Return true when the CMA record exposes a web-deliverable image URL."""
    return (
        _image_tier_url(record, "print") is not None
        or _image_tier_url(record, "web") is not None
    )


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one CMA API object with CMA Rights Matrix v1."""
    if not isinstance(record, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": CMA_RIGHTS_POLICY_ID,
        }

    if "share_license_status" not in record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": CMA_RIGHTS_POLICY_ID,
        }

    if record.get("share_license_status") != "CC0":
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "not_cc0",
            "rights_policy_id": CMA_RIGHTS_POLICY_ID,
        }

    if not has_usable_image(record):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_image_url",
            "rights_policy_id": CMA_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "cma_share_license_status_cc0",
        "rights_policy_id": CMA_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when the CMA Rights Matrix permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])

