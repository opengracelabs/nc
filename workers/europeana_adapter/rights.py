"""Rights normalization and classification for Europeana records."""
from __future__ import annotations

from enum import StrEnum


class RightsDecision(StrEnum):
    ALLOWED = "ALLOWED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"


CC0_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
PDM_URI = "https://creativecommons.org/publicdomain/mark/1.0/"
NOC_US_URI = "https://rightsstatements.org/vocab/NoC-US/1.0/"

_ALLOWED_RIGHTS = {
    CC0_URI: {"rights_status": "verified_cc0", "rights_basis": "cc0_statement"},
    PDM_URI: {"rights_status": "verified_pd", "rights_basis": "public_domain_mark"},
    NOC_US_URI: {"rights_status": "verified_pd", "rights_basis": "noc_us_statement"},
}

_BLOCKED_TOKENS = (
    "/InC/",
    "/InC-EDU/",
    "/InC-NC/",
    "/NoC-OKLR/",
    "/CNE/",
    "creativecommons.org/licenses/",
)


def normalize_rights_uri(value: str | None) -> str | None:
    """Normalize Europeana rights values to canonical URI form."""
    if not value:
        return None
    uri = value.strip()
    if not uri:
        return None
    uri = uri.replace("http://", "https://", 1)
    if not uri.endswith("/"):
        uri = f"{uri}/"
    return uri


def classify_rights(value: str | None) -> dict[str, str | bool | None]:
    """Classify Europeana rights for the adapter ingest gate."""
    uri = normalize_rights_uri(value)
    if uri in _ALLOWED_RIGHTS:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": uri,
            **_ALLOWED_RIGHTS[uri],
        }

    if uri is None:
        return {
            "decision": RightsDecision.REVIEW_REQUIRED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_rights",
        }

    if any(token.lower() in uri.lower() for token in _BLOCKED_TOKENS):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": uri,
            "rights_status": "blocked",
            "rights_basis": "blocked_rights_statement",
        }

    return {
        "decision": RightsDecision.REVIEW_REQUIRED.value,
        "allowed": False,
        "rights_statement_uri": uri,
        "rights_status": "blocked",
        "rights_basis": "unknown_rights_statement",
    }


def is_allowed_rights(value: str | None) -> bool:
    """Return true only for the Europeana Sprint 2 ingest allowlist."""
    return bool(classify_rights(value)["allowed"])
