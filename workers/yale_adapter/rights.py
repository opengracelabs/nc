"""Yale Rights Matrix v1 classification for LUX Linked Art records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.rights import RightsDecision

from .client import CC0_URI, NOC_US_URI, detect_source_slug, extract_subject_to_uris

YALE_RIGHTS_POLICY_ID = "yale_rights_matrix_v1"


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None]:
    """Classify one Yale LUX Linked Art object with Yale Rights Matrix v1."""
    if not isinstance(record, dict):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_object",
            "rights_policy_id": YALE_RIGHTS_POLICY_ID,
            "source_slug": None,
        }

    source_slug = detect_source_slug(record)
    if "subject_to" not in record:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_subject_to",
            "rights_policy_id": YALE_RIGHTS_POLICY_ID,
            "source_slug": source_slug,
        }

    rights_uris = extract_subject_to_uris(record)
    if not rights_uris:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "no_rights_statement",
            "rights_policy_id": YALE_RIGHTS_POLICY_ID,
            "source_slug": source_slug,
        }

    matched_uri = next((uri for uri in rights_uris if uri in (CC0_URI, NOC_US_URI)), None)
    if matched_uri is None:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": rights_uris[0],
            "rights_status": "blocked",
            "rights_basis": "unknown_rights_uri",
            "rights_policy_id": YALE_RIGHTS_POLICY_ID,
            "source_slug": source_slug,
        }

    if matched_uri == CC0_URI:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": matched_uri,
            "rights_status": "pending_verification",
            "rights_basis": "ycba_cc0",
            "rights_policy_id": YALE_RIGHTS_POLICY_ID,
            "source_slug": source_slug,
        }

    return {
        "decision": RightsDecision.ALLOWED.value,
        "allowed": True,
        "rights_statement_uri": matched_uri,
        "rights_status": "pending_verification",
        "rights_basis": "yuag_noc_us",
        "rights_policy_id": YALE_RIGHTS_POLICY_ID,
        "source_slug": source_slug,
    }


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when Yale Rights Matrix permits ingest consideration."""
    return bool(classify_rights(record)["allowed"])

