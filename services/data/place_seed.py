"""Candidate-only place seed utilities for NC-PLACES-001."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypedDict

FIRST_100_SEED_PATH = Path("data/curated/places/first_100_places_seed.json")

REQUIRED_FIELDS = (
    "place_slug",
    "display_name",
    "place_type",
    "country",
    "region",
    "collection_theme",
    "candidate_status",
    "authority_status",
    "public_domain_potential",
    "source_hints",
    "risk_level",
)

FORBIDDEN_FIELDS = {
    "canonical_identity",
    "canonical_place_id",
    "geonames_id",
    "geonames_place_id",
    "wikidata_qid",
    "gbif_place_key",
    "product_page_slug",
    "neo4j_node_id",
}

VALID_CANDIDATE_STATUS = {"candidate"}
VALID_AUTHORITY_STATUS = {"unverified"}
VALID_PUBLIC_DOMAIN_POTENTIAL = {"high", "medium", "low"}
VALID_RISK_LEVEL = {"low", "medium", "high"}


class PlaceSeedError(ValueError):
    """Raised when the first-100 place seed is malformed or over-authoritative."""


class PlaceSeedRecord(TypedDict):
    place_slug: str
    display_name: str
    place_type: str
    country: str
    region: str
    collection_theme: str
    candidate_status: str
    authority_status: str
    public_domain_potential: str
    source_hints: list[str]
    risk_level: str


def normalize_place_slug(value: str) -> str:
    """Normalize a display name or proposed slug into the seed slug convention."""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    if not normalized:
        raise PlaceSeedError("place slug cannot be empty after normalization")
    return normalized


def _require_string(record: dict[str, Any], field: str, index: int) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise PlaceSeedError(f"record {index} field {field} must be a non-empty string")
    return value.strip()


def _validate_source_hints(record: dict[str, Any], index: int) -> list[str]:
    hints = record.get("source_hints")
    if not isinstance(hints, list) or not hints:
        raise PlaceSeedError(f"record {index} source_hints must be a non-empty list")
    normalized_hints = []
    for hint in hints:
        if not isinstance(hint, str) or not hint.strip():
            raise PlaceSeedError(f"record {index} source_hints must contain strings")
        normalized_hints.append(hint.strip())
    return normalized_hints


def validate_place_seed(records: Iterable[dict[str, Any]]) -> list[PlaceSeedRecord]:
    """Validate first-100 candidate seed records without ratifying authority."""
    validated: list[PlaceSeedRecord] = []
    seen_slugs: set[str] = set()

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise PlaceSeedError(f"record {index} must be a JSON object")

        fields = set(record)
        missing = set(REQUIRED_FIELDS) - fields
        if missing:
            raise PlaceSeedError(f"record {index} missing fields: {sorted(missing)}")
        forbidden = fields & FORBIDDEN_FIELDS
        if forbidden:
            raise PlaceSeedError(
                f"record {index} contains forbidden canonical fields: {sorted(forbidden)}"
            )

        place_slug = _require_string(record, "place_slug", index)
        normalized_slug = normalize_place_slug(place_slug)
        if place_slug != normalized_slug:
            raise PlaceSeedError(f"record {index} place_slug must be normalized: {place_slug}")
        if normalized_slug in seen_slugs:
            raise PlaceSeedError(f"duplicate place_slug: {normalized_slug}")
        seen_slugs.add(normalized_slug)

        candidate_status = _require_string(record, "candidate_status", index)
        authority_status = _require_string(record, "authority_status", index)
        public_domain_potential = _require_string(record, "public_domain_potential", index)
        risk_level = _require_string(record, "risk_level", index)

        if candidate_status not in VALID_CANDIDATE_STATUS:
            raise PlaceSeedError(f"record {index} candidate_status must remain candidate")
        if authority_status not in VALID_AUTHORITY_STATUS:
            raise PlaceSeedError(f"record {index} authority_status must remain unverified")
        if public_domain_potential not in VALID_PUBLIC_DOMAIN_POTENTIAL:
            raise PlaceSeedError(f"record {index} invalid public_domain_potential")
        if risk_level not in VALID_RISK_LEVEL:
            raise PlaceSeedError(f"record {index} invalid risk_level")

        validated.append(
            PlaceSeedRecord(
                place_slug=normalized_slug,
                display_name=_require_string(record, "display_name", index),
                place_type=_require_string(record, "place_type", index),
                country=_require_string(record, "country", index),
                region=_require_string(record, "region", index),
                collection_theme=_require_string(record, "collection_theme", index),
                candidate_status=candidate_status,
                authority_status=authority_status,
                public_domain_potential=public_domain_potential,
                source_hints=_validate_source_hints(record, index),
                risk_level=risk_level,
            )
        )

    if not validated:
        raise PlaceSeedError("place seed must contain at least one candidate")
    return validated


def load_first_100_candidates(path: Path | str = FIRST_100_SEED_PATH) -> list[PlaceSeedRecord]:
    """Load and validate the NC-PLACES-001 first-100 candidate seed file."""
    seed_path = Path(path)
    payload = json.loads(seed_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise PlaceSeedError("first-100 place seed must be a JSON array")
    records = validate_place_seed(payload)
    if len(records) != 100:
        raise PlaceSeedError(f"first-100 place seed must contain 100 records, got {len(records)}")
    return records


def group_by_place_type(records: Iterable[PlaceSeedRecord]) -> dict[str, list[PlaceSeedRecord]]:
    """Group candidate seed rows by place_type for editorial queue planning."""
    grouped: dict[str, list[PlaceSeedRecord]] = defaultdict(list)
    for record in records:
        grouped[record["place_type"]].append(record)
    return dict(sorted(grouped.items()))


def export_candidate_summary(records: Iterable[PlaceSeedRecord]) -> dict[str, Any]:
    """Export aggregate counts while keeping all authority canonicalization deferred."""
    materialized = list(records)
    return {
        "total_candidates": len(materialized),
        "candidate_status_counts": dict(
            Counter(record["candidate_status"] for record in materialized)
        ),
        "authority_status_counts": dict(
            Counter(record["authority_status"] for record in materialized)
        ),
        "place_type_counts": dict(
            sorted(Counter(record["place_type"] for record in materialized).items())
        ),
        "region_counts": dict(sorted(Counter(record["region"] for record in materialized).items())),
        "risk_level_counts": dict(
            sorted(Counter(record["risk_level"] for record in materialized).items())
        ),
        "public_domain_potential_counts": dict(
            sorted(Counter(record["public_domain_potential"] for record in materialized).items())
        ),
        "canonical_identity_written": False,
        "product_pages_created": False,
        "neo4j_canonical_nodes_created": False,
    }
