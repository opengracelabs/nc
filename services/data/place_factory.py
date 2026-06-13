"""Scalable candidate-only place factory for NC-PLACES-FACTORY-001."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypedDict

from services.data.place_seed import normalize_place_slug

PLACE_SOURCES_DIR = Path("data/curated/place_sources")
PLACE_CANDIDATES_DIR = Path("data/curated/place_candidates")

REQUIRED_FACTORY_FIELDS = (
    "source_list",
    "designation_type",
    "display_name",
    "country",
    "region",
    "latitude",
    "longitude",
    "source_url",
    "authority_status",
    "product_potential_score",
    "story_potential_score",
    "collection_potential_score",
    "ich_connections",
    "public_domain_source_hints",
    "place_family",
    "designation_family",
    "collection_family",
    "discovery_family",
    "collection_readiness",
    "graph_readiness",
    "product_readiness",
)

FORBIDDEN_AUTHORITY_FIELDS = {
    "canonical_identity",
    "canonical_place_id",
    "canonical_geonames_id",
    "geonames_id",
    "geonames_place_id",
    "wikidata_qid",
    "gbif_place_key",
    "wdpa_id",
    "unesco_site_id",
    "neo4j_node_id",
    "product_page_slug",
}

VALID_AUTHORITY_STATUS = {
    "unverified",
    "source_observed",
    "needs_review",
    "rejected",
}

DESIGNATION_WEIGHTS = {
    "UNESCO": 34,
    "UNESCO_WH": 34,
    "UNESCO_WH_Mixed": 38,
    "Biosphere": 26,
    "UNESCO_Biosphere": 26,
    "Geopark": 24,
    "UNESCO_Geopark": 24,
    "Ramsar": 22,
    "ICH": 20,
    "DarkSky": 18,
    "Dark Sky": 18,
    "Marine Protected Area": 24,
    "WDPA_NationalPark": 26,
    "WDPA_MPA": 24,
    "UNESCO_ICH": 20,
    "CulturalLandscape": 20,
}

PD_HINT_WEIGHTS = {
    "nasa": 18,
    "nara": 16,
    "loc": 16,
    "noaa": 14,
    "usgs": 14,
    "europeana": 12,
    "gallica": 12,
    "met": 10,
    "getty": 10,
    "smithsonian": 10,
    "bhl": 10,
    "gbif": 6,
    "wikimedia": 5,
}

HIGH_STORY_DESIGNATIONS = {
    "UNESCO",
    "UNESCO_WH",
    "UNESCO_WH_Mixed",
    "ICH",
    "UNESCO_ICH",
    "CulturalLandscape",
}

DESIGNATION_FAMILY_BY_TYPE = {
    "UNESCO": "UNESCO",
    "UNESCO_WH": "UNESCO",
    "UNESCO_WH_Mixed": "UNESCO",
    "Biosphere": "Biosphere",
    "UNESCO_Biosphere": "Biosphere",
    "Geopark": "Geopark",
    "UNESCO_Geopark": "Geopark",
    "Ramsar": "Ramsar",
    "ICH": "ICH",
    "UNESCO_ICH": "ICH",
    "DarkSky": "Dark Sky",
    "Dark Sky": "Dark Sky",
    "Marine Protected Area": "Marine Protected Area",
    "WDPA_MPA": "Marine Protected Area",
    "WDPA_NationalPark": "UNESCO",
    "CulturalLandscape": "UNESCO",
}

PLACE_FAMILY_BY_DESIGNATION_FAMILY = {
    "UNESCO": "heritage_place",
    "Biosphere": "living_landscape",
    "Geopark": "earth_science",
    "Ramsar": "wetland_water",
    "ICH": "intangible_heritage",
    "Dark Sky": "sky_landscape",
    "Marine Protected Area": "marine_place",
}

COLLECTION_FAMILY_BY_DESIGNATION_FAMILY = {
    "UNESCO": "world_heritage_collection",
    "Biosphere": "biosphere_collection",
    "Geopark": "geopark_collection",
    "Ramsar": "wetland_collection",
    "ICH": "ich_collection",
    "Dark Sky": "dark_sky_collection",
    "Marine Protected Area": "marine_collection",
}

DISCOVERY_FAMILY_BY_DESIGNATION_FAMILY = {
    "UNESCO": "heritage_discovery",
    "Biosphere": "ecology_discovery",
    "Geopark": "geology_discovery",
    "Ramsar": "water_discovery",
    "ICH": "culture_discovery",
    "Dark Sky": "astronomy_discovery",
    "Marine Protected Area": "ocean_discovery",
}


class PlaceFactoryError(ValueError):
    """Raised when a place factory source or candidate violates factory rules."""


class PlaceFactoryCandidate(TypedDict):
    place_slug: str
    source_list: str
    designation_type: str
    display_name: str
    country: str
    region: str
    latitude: float | None
    longitude: float | None
    source_url: str
    authority_status: str
    product_potential_score: int
    story_potential_score: int
    collection_potential_score: int
    ich_connections: list[str]
    public_domain_source_hints: list[str]
    place_family: str
    designation_family: str
    collection_family: str
    discovery_family: str
    collection_readiness: str
    graph_readiness: str
    product_readiness: str


def _as_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PlaceFactoryError(f"{field} must be a non-empty string")
    return value.strip()


def _as_optional_float(value: Any, field: str) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        raise PlaceFactoryError(f"{field} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise PlaceFactoryError(f"{field} must be numeric") from exc
    return number


def _as_string_list(value: Any, field: str) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise PlaceFactoryError(f"{field} must be a list")
    result = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise PlaceFactoryError(f"{field} must contain strings")
        result.append(item.strip())
    return result


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


def assign_place_families(record: dict[str, Any]) -> dict[str, str]:
    """Assign place, designation, collection, and discovery families."""
    designation = str(record.get("designation_type") or "")
    designation_family = DESIGNATION_FAMILY_BY_TYPE.get(designation, "Other")
    return {
        "place_family": PLACE_FAMILY_BY_DESIGNATION_FAMILY.get(
            designation_family,
            "general_place",
        ),
        "designation_family": designation_family,
        "collection_family": COLLECTION_FAMILY_BY_DESIGNATION_FAMILY.get(
            designation_family,
            "general_collection",
        ),
        "discovery_family": DISCOVERY_FAMILY_BY_DESIGNATION_FAMILY.get(
            designation_family,
            "general_discovery",
        ),
    }


def _readiness_from_score(score: int, ready: int, review: int) -> str:
    if score >= ready:
        return "ready"
    if score >= review:
        return "review"
    return "hold"


def assign_readiness(record: dict[str, Any]) -> dict[str, str]:
    """Assign collection, graph, and product readiness without canonical promotion."""
    authority_status = str(record.get("authority_status") or "unverified")
    has_coordinates = record.get("latitude") is not None and record.get("longitude") is not None
    collection_score = int(record.get("collection_potential_score") or 0)
    product_score = int(record.get("product_potential_score") or 0)
    story_score = int(record.get("story_potential_score") or 0)

    graph_readiness = "ready" if has_coordinates and story_score >= 55 else "review"
    if not has_coordinates and story_score < 45:
        graph_readiness = "hold"

    product_readiness = _readiness_from_score(product_score, ready=72, review=50)
    if authority_status in {"needs_review", "rejected"}:
        product_readiness = "hold"

    return {
        "collection_readiness": _readiness_from_score(
            collection_score,
            ready=70,
            review=50,
        ),
        "graph_readiness": graph_readiness,
        "product_readiness": product_readiness,
    }


def validate_authority_fields(record: dict[str, Any]) -> None:
    """Reject canonical authority/product/graph fields before candidate export."""
    forbidden = set(record) & FORBIDDEN_AUTHORITY_FIELDS
    if forbidden:
        raise PlaceFactoryError(f"canonical authority fields are not allowed: {sorted(forbidden)}")
    status = record.get("authority_status", "unverified")
    if status not in VALID_AUTHORITY_STATUS:
        raise PlaceFactoryError(f"authority_status must be one of {sorted(VALID_AUTHORITY_STATUS)}")


def score_place_candidate(record: dict[str, Any]) -> dict[str, int]:
    """Score product, story, and collection potential from candidate-only signals."""
    designation = str(record.get("designation_type") or "")
    hints = [
        hint.lower()
        for hint in _as_string_list(
            record.get("public_domain_source_hints"),
            "public_domain_source_hints",
        )
    ]
    ich_connections = _as_string_list(record.get("ich_connections"), "ich_connections")
    has_coordinates = record.get("latitude") is not None and record.get("longitude") is not None

    designation_score = DESIGNATION_WEIGHTS.get(designation, 12)
    pd_score = min(42, sum(PD_HINT_WEIGHTS.get(hint, 4) for hint in set(hints)))
    coordinate_bonus = 8 if has_coordinates else 0
    ich_bonus = min(15, len(ich_connections) * 5)

    product = _clamp_score(20 + pd_score + coordinate_bonus + min(10, designation_score // 4))
    story = _clamp_score(
        28
        + designation_score
        + ich_bonus
        + (8 if designation in HIGH_STORY_DESIGNATIONS else 0)
    )
    collection = _clamp_score(
        22 + designation_score + pd_score // 2 + ich_bonus + coordinate_bonus
    )

    return {
        "product_potential_score": product,
        "story_potential_score": story,
        "collection_potential_score": collection,
    }


def normalize_place_candidate(
    raw: dict[str, Any],
    source_list: str | None = None,
) -> PlaceFactoryCandidate:
    """Normalize one raw source record to the place factory candidate schema."""
    if not isinstance(raw, dict):
        raise PlaceFactoryError("place source record must be an object")
    validate_authority_fields(raw)

    display_name = _as_string(
        raw.get("display_name") or raw.get("source_name") or raw.get("name"),
        "display_name",
    )
    latitude = _as_optional_float(
        raw.get("latitude") if "latitude" in raw else raw.get("source_lat"),
        "latitude",
    )
    longitude = _as_optional_float(
        raw.get("longitude") if "longitude" in raw else raw.get("source_lon"),
        "longitude",
    )
    if latitude is not None and not -90 <= latitude <= 90:
        raise PlaceFactoryError("latitude must be between -90 and 90")
    if longitude is not None and not -180 <= longitude <= 180:
        raise PlaceFactoryError("longitude must be between -180 and 180")

    candidate: dict[str, Any] = {
        "place_slug": normalize_place_slug(str(raw.get("place_slug") or display_name)),
        "source_list": _as_string(raw.get("source_list") or source_list, "source_list"),
        "designation_type": _as_string(raw.get("designation_type"), "designation_type"),
        "display_name": display_name,
        "country": _as_string(raw.get("country") or raw.get("source_country"), "country"),
        "region": _as_string(raw.get("region"), "region"),
        "latitude": latitude,
        "longitude": longitude,
        "source_url": _as_string(raw.get("source_url"), "source_url"),
        "authority_status": _as_string(
            raw.get("authority_status", "unverified"),
            "authority_status",
        ),
        "ich_connections": _as_string_list(raw.get("ich_connections"), "ich_connections"),
        "public_domain_source_hints": _as_string_list(
            raw.get("public_domain_source_hints"),
            "public_domain_source_hints",
        ),
    }
    validate_authority_fields(candidate)
    candidate.update(score_place_candidate(candidate))
    candidate.update(assign_place_families(candidate))
    candidate.update(assign_readiness(candidate))
    return PlaceFactoryCandidate(**candidate)


def ingest_place_source(path: Path | str) -> list[PlaceFactoryCandidate]:
    """Load a source-list JSON file and normalize every candidate record."""
    source_path = Path(path)
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        source_list = _as_string(payload.get("source_list") or source_path.stem, "source_list")
        records = payload.get("records")
    else:
        source_list = source_path.stem
        records = payload
    if not isinstance(records, list):
        raise PlaceFactoryError("place source must be a list or an object with records")

    candidates = [normalize_place_candidate(record, source_list) for record in records]
    slugs = [candidate["place_slug"] for candidate in candidates]
    duplicates = sorted(slug for slug, count in Counter(slugs).items() if count > 1)
    if duplicates:
        raise PlaceFactoryError(f"duplicate place candidates in source: {duplicates}")
    return candidates


def batch_import_place_sources(paths: Iterable[Path | str]) -> list[PlaceFactoryCandidate]:
    """Import multiple source-list files into one deduplicated candidate batch."""
    candidates: list[PlaceFactoryCandidate] = []
    seen_slugs: set[str] = set()
    for path in paths:
        for candidate in ingest_place_source(path):
            slug = candidate["place_slug"]
            if slug in seen_slugs:
                raise PlaceFactoryError(f"duplicate place candidate across batch: {slug}")
            candidates.append(candidate)
            seen_slugs.add(slug)
    return candidates


def export_place_batch(
    candidates: Iterable[PlaceFactoryCandidate],
    batch_name: str,
    output_dir: Path | str = PLACE_CANDIDATES_DIR,
) -> Path:
    """Export a normalized candidate batch without writing canonical identity."""
    materialized = sorted(list(candidates), key=lambda item: item["place_slug"])
    if not materialized:
        raise PlaceFactoryError("cannot export an empty place batch")
    for candidate in materialized:
        validate_authority_fields(candidate)
        missing = set(REQUIRED_FACTORY_FIELDS) - set(candidate)
        if missing:
            raise PlaceFactoryError(f"candidate missing required fields: {sorted(missing)}")

    output_path = Path(output_dir) / f"{normalize_place_slug(batch_name)}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(materialized, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def summarize_place_factory(candidates: Iterable[PlaceFactoryCandidate]) -> dict[str, Any]:
    """Summarize a candidate batch and state the non-canonical factory contract."""
    materialized = list(candidates)
    return {
        "total_candidates": len(materialized),
        "source_list_counts": dict(
            sorted(Counter(c["source_list"] for c in materialized).items())
        ),
        "designation_type_counts": dict(
            sorted(Counter(c["designation_type"] for c in materialized).items())
        ),
        "authority_status_counts": dict(
            sorted(Counter(c["authority_status"] for c in materialized).items())
        ),
        "region_counts": dict(sorted(Counter(c["region"] for c in materialized).items())),
        "place_family_counts": dict(
            sorted(Counter(c["place_family"] for c in materialized).items())
        ),
        "designation_family_counts": dict(
            sorted(Counter(c["designation_family"] for c in materialized).items())
        ),
        "collection_family_counts": dict(
            sorted(Counter(c["collection_family"] for c in materialized).items())
        ),
        "collection_readiness_counts": dict(
            sorted(Counter(c["collection_readiness"] for c in materialized).items())
        ),
        "graph_readiness_counts": dict(
            sorted(Counter(c["graph_readiness"] for c in materialized).items())
        ),
        "product_readiness_counts": dict(
            sorted(Counter(c["product_readiness"] for c in materialized).items())
        ),
        "scale_target": 10000,
        "average_product_potential_score": round(
            sum(c["product_potential_score"] for c in materialized) / len(materialized),
            2,
        )
        if materialized
        else 0.0,
        "average_story_potential_score": round(
            sum(c["story_potential_score"] for c in materialized) / len(materialized),
            2,
        )
        if materialized
        else 0.0,
        "average_collection_potential_score": round(
            sum(c["collection_potential_score"] for c in materialized) / len(materialized),
            2,
        )
        if materialized
        else 0.0,
        "canonical_identity_written": False,
    }
