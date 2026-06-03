"""Deterministic scoring for public-domain illustration opportunities.

The output object is an Illustration Opportunity. Taxa are context only. Rights
must be explicitly verified as Public Domain or CC0 before an opportunity can
enter the commercial pipeline.
"""
from __future__ import annotations

from typing import Any

_ALLOWED_RIGHTS = {"Public Domain", "CC0"}
_SCORING_VERSION = "illustration_opportunity:v1"
_GOLDEN_AGE_START = 1750
_GOLDEN_AGE_END = 1900
_PRIORITY_ILLUSTRATORS = {
    "audubon",
    "gould",
    "merian",
    "redoute",
    "redouté",
    "lear",
    "nodder",
    "haeckel",
    "wolf",
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _round(value: float) -> float:
    return round(_clamp(value), 3)


def _presence(value: Any) -> float:
    return 1.0 if value else 0.0


def _golden_age_priority(year: Any) -> float:
    if year is None:
        return 0.0
    try:
        value = int(year)
    except (TypeError, ValueError):
        return 0.0
    if _GOLDEN_AGE_START <= value <= _GOLDEN_AGE_END:
        return 1.0
    if 1600 <= value < _GOLDEN_AGE_START or _GOLDEN_AGE_END < value <= 1930:
        return 0.45
    return 0.0


def _priority_illustrator(illustrator: Any) -> float:
    if not illustrator:
        return 0.0
    normalized = str(illustrator).lower()
    return 1.0 if any(name in normalized for name in _PRIORITY_ILLUSTRATORS) else 0.0


def verify_commercial_rights(candidate: dict[str, Any]) -> bool:
    return (
        candidate.get("rights_status") in _ALLOWED_RIGHTS
        and bool(candidate.get("rights_verified_by"))
    )


def score_illustration_opportunity(candidate: dict[str, Any]) -> dict[str, Any] | None:
    if not verify_commercial_rights(candidate):
        return None

    illustration_quality = _round(float(candidate.get("illustration_quality_score", 0)))
    place_relevance = _round(float(candidate.get("place_relevance_score", 0)))
    historical = _round(
        0.50 * float(candidate.get("historical_significance_score", 0))
        + 0.30 * _golden_age_priority(candidate.get("publication_year"))
        + 0.20 * _priority_illustrator(candidate.get("illustrator"))
    )
    commercial = _round(float(candidate.get("commercial_value_score", 0)))
    provenance = _round(
        0.35 * _presence(candidate.get("source_url"))
        + 0.25 * _presence(candidate.get("publication_title"))
        + 0.20 * _presence(candidate.get("publication_year"))
        + 0.20 * _presence(candidate.get("illustrator"))
    )
    rights_certainty = 1.0

    score = _round(
        0.22 * rights_certainty
        + 0.22 * illustration_quality
        + 0.18 * place_relevance
        + 0.14 * historical
        + 0.16 * commercial
        + 0.08 * provenance
    )

    score_components = {
        "rights_certainty_score": rights_certainty,
        "illustration_quality_score": illustration_quality,
        "place_relevance_score": place_relevance,
        "historical_significance_score": historical,
        "commercial_value_score": commercial,
        "provenance_score": provenance,
        "golden_age_priority_score": _round(
            _golden_age_priority(candidate.get("publication_year"))
        ),
        "priority_illustrator_score": _round(
            _priority_illustrator(candidate.get("illustrator"))
        ),
    }

    return {
        "taxon_name": candidate["taxon_name"],
        "publication_title": candidate["publication_title"],
        "illustrator": candidate.get("illustrator"),
        "publication_year": candidate.get("publication_year"),
        "rights_status": candidate["rights_status"],
        "rights_source_url": candidate.get("rights_source_url"),
        "illustration_quality_score": illustration_quality,
        "place_relevance_score": place_relevance,
        "historical_significance_score": historical,
        "commercial_value_score": commercial,
        "provenance_score": provenance,
        "golden_age_priority_score": score_components["golden_age_priority_score"],
        "priority_illustrator_score": score_components["priority_illustrator_score"],
        "opportunity_score": score,
        "score_components": score_components,
        "provenance": {
            "prov:wasGeneratedBy": _SCORING_VERSION,
            "optimization_target": "high_value_public_domain_illustration_opportunity",
            "taxon_role": "metadata_semantic_anchor_search_handle",
        },
    }
