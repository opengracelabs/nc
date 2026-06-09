"""Statens Museum for Kunst Rights Matrix v1 classification."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

SMK_RIGHTS_POLICY_ID = "smk_rights_matrix_v1"


def _present_image(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def has_usable_image(record: dict[str, Any]) -> bool:
    """Return true when the SMK record exposes a usable image reference."""
    if _present_image(record.get("image_native")):
        return True
    images = record.get("images")
    if not isinstance(images, list) or not images:
        return False
    first_image = images[0]
    return isinstance(first_image, dict) and _present_image(first_image.get("url"))


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one SMK API object with SMK Rights Matrix v1."""
    if not isinstance(record, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": SMK_RIGHTS_POLICY_ID,
        }

    if "public_domain" not in record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights_field",
            "rights_policy_id": SMK_RIGHTS_POLICY_ID,
        }

    if record.get("public_domain") is not True:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "not_public_domain",
            "rights_policy_id": SMK_RIGHTS_POLICY_ID,
        }

    if not has_usable_image(record):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_image_url",
            "rights_policy_id": SMK_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "smk_public_domain",
        "rights_policy_id": SMK_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when the SMK Rights Matrix permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])

