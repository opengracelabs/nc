"""Getty Rights Matrix v1 classification for Linked Art records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import RightsDecision

from .client import CC0_URI, extract_rights_uris
from .config import RIGHTS_POLICY_ID

GETTY_RIGHTS_POLICY_ID = RIGHTS_POLICY_ID


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _has_subject_to(record: dict[str, Any]) -> bool:
    for statement in _as_list(record.get("referred_to_by")):
        if isinstance(statement, dict) and "subject_to" in statement:
            return True
    return False


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one Getty Linked Art object with Getty Rights Matrix v1."""
    if not isinstance(record, dict) or not record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_object",
            "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
        }

    if "referred_to_by" not in record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_referred_to_by",
            "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
        }

    if not _has_subject_to(record):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_subject_to",
            "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
        }

    rights_uris = extract_rights_uris(record)
    if not rights_uris:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_rights_statement",
            "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
        }

    if CC0_URI in rights_uris:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": CC0_URI,
            "rights_status": "pending_verification",
            "rights_basis": "getty_cc0",
            "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
        }

    return {
        "decision": RightsDecision.BLOCKED.value,
        "allowed": False,
        "rights_statement_uri": rights_uris[0],
        "rights_status": "blocked",
        "rights_basis": "unknown_rights_uri",
        "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when Getty Rights Matrix permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])

