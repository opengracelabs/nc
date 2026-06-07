"""Shared rights normalization and classification for media adapters."""
from __future__ import annotations

from enum import StrEnum

RIGHTS_POLICY_ID = "europeana_rights_matrix_v1.0"


class RightsDecision(StrEnum):
    ALLOWED = "ALLOWED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"


CC0_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
PDM_URI = "https://creativecommons.org/publicdomain/mark/1.0/"
NOC_US_URI = "https://rightsstatements.org/vocab/NoC-US/1.0/"
NOC_CR_URI = "https://rightsstatements.org/vocab/NoC-CR/1.0/"
NOC_OKLR_URI = "https://rightsstatements.org/vocab/NoC-OKLR/1.0/"
NKC_URI = "https://rightsstatements.org/vocab/NKC/1.0/"

_ALLOWED_RIGHTS = {
    CC0_URI: {"rights_status": "verified_cc0", "rights_basis": "cc0_statement"},
    PDM_URI: {"rights_status": "verified_pd", "rights_basis": "public_domain_mark"},
    NOC_US_URI: {"rights_status": "verified_pd", "rights_basis": "noc_us_statement"},
}

_REVIEW_REQUIRED_URIS = {NOC_CR_URI, NOC_OKLR_URI, NKC_URI}

_BLOCKED_TOKENS = (
    "/InC/",
    "/InC-EDU/",
    "/InC-NC/",
    "/CNE/",
    "creativecommons.org/licenses/",
)


def normalize_rights_uri(value: str | None) -> str | None:
    """Normalize rights values to canonical URI form."""
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
    """Classify rights for the shared adapter ingest gate."""
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
            "rights_status": "pending_verification",
            "rights_basis": "missing_rights",
        }

    if uri in _REVIEW_REQUIRED_URIS:
        return {
            "decision": RightsDecision.REVIEW_REQUIRED.value,
            "allowed": False,
            "rights_statement_uri": uri,
            "rights_status": "pending_verification",
            "rights_basis": "review_required_statement",
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
        "rights_status": "pending_verification",
        "rights_basis": "unknown_rights_statement",
    }


def is_allowed_rights(value: str | None) -> bool:
    """Return true only for the governed ingest allowlist."""
    return bool(classify_rights(value)["allowed"])

