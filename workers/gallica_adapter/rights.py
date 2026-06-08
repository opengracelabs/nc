"""Gallica rights classification addendum."""
from __future__ import annotations

import re
import unicodedata
from typing import Any

from workers.shared_media_adapter.rights import (
    NKC_URI,
    PDM_URI,
    RightsDecision,
    normalize_rights_uri,
)
from workers.shared_media_adapter.rights import (
    classify_rights as classify_shared_rights,
)

GALLICA_RIGHTS_ADDENDUM_ID = "gallica_rights_addendum_v1"

_URI_RE = re.compile(r"https?://[^\s<>\"]+")
_BLOCKED_TEXT = (
    ("droits reserves", "reserved_rights_text"),
    ("droits réservés", "reserved_rights_text"),
    ("usage non-commercial", "noncommercial_use_text"),
    ("usage non commercial", "noncommercial_use_text"),
    ("non-commercial", "noncommercial_use_text"),
    ("non commercial", "noncommercial_use_text"),
)
_ALLOWED_TEXT = (
    ("domaine public", "gallica_domaine_public_text"),
    ("public domain", "gallica_public_domain_text"),
    ("libre de reutilisation", "gallica_free_reuse_text"),
    ("libre de réutilisation", "gallica_free_reuse_text"),
    ("usage commercial autorise", "gallica_commercial_use_authorized_text"),
    ("usage commercial autorisé", "gallica_commercial_use_authorized_text"),
)


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_rights_text(value: str | None) -> str | None:
    """Normalize French Gallica rights text for deterministic classification."""
    if value is None:
        return None
    compact = " ".join(str(value).strip().split()).lower()
    return compact or None


def extract_rights_uri(value: Any) -> str | None:
    """Extract the first URI-like rights statement from a raw value."""
    if value is None:
        return None
    if isinstance(value, list):
        for item in value:
            uri = extract_rights_uri(item)
            if uri:
                return uri
        return None
    if isinstance(value, dict):
        for item in value.values():
            uri = extract_rights_uri(item)
            if uri:
                return uri
        return None

    match = _URI_RE.search(str(value))
    if not match:
        return None
    return normalize_rights_uri(match.group(0).rstrip(".,;)"))


def classify_rights(value: Any) -> dict[str, str | bool | None]:
    """Classify URI and French Gallica rights values under Addendum v1."""
    uri = extract_rights_uri(value)
    if uri:
        result = classify_shared_rights(uri)
        return {
            **result,
            "rights_policy_id": GALLICA_RIGHTS_ADDENDUM_ID,
            "rights_source": "uri",
            "source_text": str(value),
        }

    text = normalize_rights_text(str(value)) if value is not None else None
    if text is None:
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "blocked",
            "rights_basis": "missing_gallica_rights",
            "rights_policy_id": GALLICA_RIGHTS_ADDENDUM_ID,
            "rights_source": "missing",
            "source_text": None,
        }

    accentless = _strip_accents(text)
    for token, basis in _BLOCKED_TEXT:
        if token in text or _strip_accents(token) in accentless:
            return {
                "decision": RightsDecision.BLOCKED.value,
                "allowed": False,
                "rights_statement_uri": None,
                "rights_status": "blocked",
                "rights_basis": basis,
                "rights_policy_id": GALLICA_RIGHTS_ADDENDUM_ID,
                "rights_source": "gallica_french_text",
                "source_text": text,
            }

    if "domaine public revisite" in accentless:
        return {
            "decision": RightsDecision.REVIEW_REQUIRED.value,
            "allowed": False,
            "rights_statement_uri": NKC_URI,
            "rights_status": "pending_verification",
            "rights_basis": "gallica_public_domain_revisited",
            "rights_policy_id": GALLICA_RIGHTS_ADDENDUM_ID,
            "rights_source": "gallica_french_text",
            "source_text": text,
        }

    for token, basis in _ALLOWED_TEXT:
        if token in text or _strip_accents(token) in accentless:
            return {
                "decision": RightsDecision.ALLOWED.value,
                "allowed": True,
                "rights_statement_uri": PDM_URI,
                "rights_status": "verified_pd",
                "rights_basis": basis,
                "rights_policy_id": GALLICA_RIGHTS_ADDENDUM_ID,
                "rights_source": "gallica_french_text",
                "source_text": text,
            }

    return {
        "decision": RightsDecision.REVIEW_REQUIRED.value,
        "allowed": False,
        "rights_statement_uri": None,
        "rights_status": "pending_verification",
        "rights_basis": "unknown_gallica_rights_text",
        "rights_policy_id": GALLICA_RIGHTS_ADDENDUM_ID,
        "rights_source": "gallica_french_text",
        "source_text": text,
    }


def is_allowed_rights(value: Any) -> bool:
    """Return true only for Gallica rights classified as allowed."""
    return bool(classify_rights(value)["allowed"])

