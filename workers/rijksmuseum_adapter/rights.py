"""Rijksmuseum rights classification.

Rijksmuseum uses the same governed rights statement vocabulary as the Europeana
adapter. Keep this module as a thin source-specific wrapper so future
Rijksmuseum-specific rights policy can be added without changing callers.
"""
from __future__ import annotations

from workers.europeana_adapter.rights import (
    RightsDecision,
    classify_rights,
    is_allowed_rights,
    normalize_rights_uri,
)

__all__ = [
    "RightsDecision",
    "classify_rights",
    "is_allowed_rights",
    "normalize_rights_uri",
]
