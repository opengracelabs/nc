"""Rijksmuseum rights compatibility wrapper."""
from __future__ import annotations

from workers.shared_media_adapter.rights import (
    RIGHTS_POLICY_ID,
    RightsDecision,
    classify_rights,
    is_allowed_rights,
    normalize_rights_uri,
)

__all__ = [
    "RIGHTS_POLICY_ID",
    "RightsDecision",
    "classify_rights",
    "is_allowed_rights",
    "normalize_rights_uri",
]
