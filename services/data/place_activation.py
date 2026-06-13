"""Activation readiness summaries for candidate-only place batches."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Literal, TypedDict

from services.data.place_coverage import (
    DEFAULT_COVERAGE_BATCH,
    coverage_region,
    load_candidate_places,
)
from services.data.place_factory import PlaceFactoryCandidate, validate_authority_fields

ActivationState = Literal["Ready", "Review", "Hold"]


class ActivationPlace(TypedDict):
    place_slug: str
    display_name: str
    country: str
    region: str
    designation_family: str
    collection_family: str
    authority_readiness: ActivationState
    collection_readiness: ActivationState
    product_readiness: ActivationState
    graph_readiness: ActivationState
    publishing_readiness: ActivationState
    activation_score: int


def _title_readiness(value: str) -> ActivationState:
    if value == "ready":
        return "Ready"
    if value == "review":
        return "Review"
    return "Hold"


def authority_readiness(candidate: PlaceFactoryCandidate) -> ActivationState:
    validate_authority_fields(candidate)
    if candidate["authority_status"] == "source_observed":
        return "Review"
    if candidate["authority_status"] == "unverified":
        return "Hold"
    if candidate["authority_status"] == "needs_review":
        return "Review"
    return "Hold"


def publishing_readiness(
    authority: ActivationState,
    collection: ActivationState,
    product: ActivationState,
    graph: ActivationState,
) -> ActivationState:
    states = {authority, collection, product, graph}
    if "Hold" in states:
        return "Hold"
    if states == {"Ready"}:
        return "Ready"
    return "Review"


def activation_score(candidate: PlaceFactoryCandidate) -> int:
    readiness_bonus = {"ready": 12, "review": 5, "hold": 0}
    coordinate_bonus = (
        8
        if candidate["latitude"] is not None and candidate["longitude"] is not None
        else 0
    )
    return min(
        100,
        round(
            candidate["collection_potential_score"] * 0.35
            + candidate["story_potential_score"] * 0.25
            + candidate["product_potential_score"] * 0.2
            + readiness_bonus[candidate["collection_readiness"]]
            + readiness_bonus[candidate["graph_readiness"]]
            + readiness_bonus[candidate["product_readiness"]]
            + coordinate_bonus
        ),
    )


def activation_place(candidate: PlaceFactoryCandidate) -> ActivationPlace:
    authority = authority_readiness(candidate)
    collection = _title_readiness(candidate["collection_readiness"])
    product = _title_readiness(candidate["product_readiness"])
    graph = _title_readiness(candidate["graph_readiness"])
    return {
        "place_slug": candidate["place_slug"],
        "display_name": candidate["display_name"],
        "country": candidate["country"],
        "region": coverage_region(candidate),
        "designation_family": candidate["designation_family"],
        "collection_family": candidate["collection_family"],
        "authority_readiness": authority,
        "collection_readiness": collection,
        "product_readiness": product,
        "graph_readiness": graph,
        "publishing_readiness": publishing_readiness(authority, collection, product, graph),
        "activation_score": activation_score(candidate),
    }


def top_activation_places(
    candidates: Iterable[PlaceFactoryCandidate],
    limit: int = 25,
) -> list[ActivationPlace]:
    ranked = [activation_place(candidate) for candidate in candidates]
    return sorted(
        ranked,
        key=lambda item: (
            item["activation_score"],
            item["graph_readiness"] == "Ready",
            item["collection_readiness"] == "Ready",
            item["display_name"],
        ),
        reverse=True,
    )[:limit]


def summarize_activation_dashboard(
    candidates: Iterable[PlaceFactoryCandidate],
    limit: int = 25,
) -> dict[str, Any]:
    materialized = list(candidates)
    top_places = top_activation_places(materialized, limit)
    all_places = [activation_place(candidate) for candidate in materialized]
    return {
        "total_candidates": len(materialized),
        "top_place_count": len(top_places),
        "top_places": top_places,
        "authority_readiness_counts": dict(
            sorted(Counter(p["authority_readiness"] for p in all_places).items())
        ),
        "collection_readiness_counts": dict(
            sorted(Counter(p["collection_readiness"] for p in all_places).items())
        ),
        "product_readiness_counts": dict(
            sorted(Counter(p["product_readiness"] for p in all_places).items())
        ),
        "graph_readiness_counts": dict(
            sorted(Counter(p["graph_readiness"] for p in all_places).items())
        ),
        "publishing_readiness_counts": dict(
            sorted(Counter(p["publishing_readiness"] for p in all_places).items())
        ),
        "canonical_identity_written": False,
    }


def export_activation_dashboard_summary(
    candidates: Iterable[PlaceFactoryCandidate],
    output_path: Path | str,
    limit: int = 25,
) -> Path:
    summary = summarize_activation_dashboard(candidates, limit)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_activation_candidates(
    path: Path | str = DEFAULT_COVERAGE_BATCH,
) -> list[PlaceFactoryCandidate]:
    return load_candidate_places(path)
