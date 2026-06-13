"""Coverage summaries for candidate-only place factory batches."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from services.data.place_factory import (
    COLLECTION_FAMILY_BY_DESIGNATION_FAMILY,
    PLACE_CANDIDATES_DIR,
    PlaceFactoryCandidate,
    validate_authority_fields,
)

DEFAULT_COVERAGE_BATCH = PLACE_CANDIDATES_DIR / "nc-places-250-source-ingestion.json"

COUNTRY_REGION = {
    "Albania": "Europe",
    "Andorra": "Europe",
    "Argentina": "South America",
    "Australia": "Oceania",
    "Austria": "Europe",
    "Azerbaijan": "Asia",
    "Bangladesh": "Asia",
    "Belgium": "Europe",
    "Bolivia": "South America",
    "Brazil": "South America",
    "Bulgaria": "Europe",
    "Canada": "North America",
    "Colombia": "South America",
    "Costa Rica": "Central America",
    "Croatia": "Europe",
    "Czech Republic": "Europe",
    "Democratic Republic of the Congo": "Africa",
    "Eswatini": "Africa",
    "France": "Europe",
    "Galicia": "Europe",
    "Germany": "Europe",
    "Ghana": "Africa",
    "Greece": "Europe",
    "Guatemala": "Central America",
    "Hungary": "Europe",
    "Iceland": "Europe",
    "India": "Asia",
    "Indonesia": "Asia",
    "Iran": "Asia",
    "Ireland": "Europe",
    "Italy": "Europe",
    "Ivory Coast": "Africa",
    "Japan": "Asia",
    "Jordan": "Asia",
    "Kazakhstan": "Asia",
    "Libya": "Africa",
    "Malaysia": "Asia",
    "Mexico": "North America",
    "Morocco": "Africa",
    "Mozambique": "Africa",
    "Myanmar": "Asia",
    "Netherlands": "Europe",
    "North Korea": "Asia",
    "Pakistan": "Asia",
    "People's Republic of China": "Asia",
    "Peru": "South America",
    "Portugal": "Europe",
    "Russia": "Eurasia",
    "Saudi Arabia": "Asia",
    "Slovenia": "Europe",
    "South Africa": "Africa",
    "South Korea": "Asia",
    "Spain": "Europe",
    "São Tomé and Príncipe": "Africa",
    "Sweden": "Europe",
    "Switzerland": "Europe",
    "Tanzania": "Africa",
    "Thailand": "Asia",
    "Turkey": "Eurasia",
    "Uganda": "Africa",
    "United Kingdom": "Europe",
    "United States": "North America",
    "Vietnam": "Asia",
    "Yemen": "Asia",
    "Zimbabwe": "Africa",
}


def load_candidate_places(
    path: Path | str = DEFAULT_COVERAGE_BATCH,
) -> list[PlaceFactoryCandidate]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("coverage batch must be a list of candidate places")
    for candidate in payload:
        if not isinstance(candidate, dict):
            raise ValueError("coverage batch entries must be objects")
        validate_authority_fields(candidate)
    return payload


def coverage_region(candidate: PlaceFactoryCandidate) -> str:
    region = str(candidate.get("region") or "").strip()
    if region and region != "Global":
        return region
    country = str(candidate.get("country") or "").strip()
    if country == "Multiple":
        return "Transregional"
    return COUNTRY_REGION.get(country, "Unmapped")


def summarize_place_coverage(
    candidates: Iterable[PlaceFactoryCandidate],
) -> dict[str, Any]:
    materialized = list(candidates)
    expected_families = set(COLLECTION_FAMILY_BY_DESIGNATION_FAMILY.values())
    present_families = {candidate["collection_family"] for candidate in materialized}
    missing_coordinates = [
        candidate
        for candidate in materialized
        if candidate["latitude"] is None or candidate["longitude"] is None
    ]
    authority_status_counts = Counter(c["authority_status"] for c in materialized)
    collection_gap_counts: dict[str, int] = defaultdict(int)
    for candidate in materialized:
        if candidate["collection_readiness"] != "ready":
            collection_gap_counts[candidate["collection_family"]] += 1

    map_points = [
        {
            "place_slug": candidate["place_slug"],
            "display_name": candidate["display_name"],
            "designation_family": candidate["designation_family"],
            "latitude": candidate["latitude"],
            "longitude": candidate["longitude"],
        }
        for candidate in materialized
        if candidate["latitude"] is not None and candidate["longitude"] is not None
    ]

    return {
        "total_candidates": len(materialized),
        "mapped_candidates": len(map_points),
        "missing_coordinate_candidates": len(missing_coordinates),
        "region_counts": dict(
            sorted(Counter(coverage_region(c) for c in materialized).items())
        ),
        "designation_family_counts": dict(
            sorted(Counter(c["designation_family"] for c in materialized).items())
        ),
        "authority_gap_counts": {
            "source_observed_only": authority_status_counts.get("source_observed", 0),
            "unverified": authority_status_counts.get("unverified", 0),
            "needs_review": authority_status_counts.get("needs_review", 0),
            "missing_coordinates": len(missing_coordinates),
        },
        "collection_family_counts": dict(
            sorted(Counter(c["collection_family"] for c in materialized).items())
        ),
        "collection_family_gaps": {
            "missing_expected_families": sorted(expected_families - present_families),
            "review_or_hold_by_family": dict(sorted(collection_gap_counts.items())),
        },
        "map_points": sorted(map_points, key=lambda p: p["display_name"]),
        "canonical_identity_written": False,
    }


def export_place_coverage_summary(
    candidates: Iterable[PlaceFactoryCandidate],
    output_path: Path | str,
) -> Path:
    summary = summarize_place_coverage(candidates)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
