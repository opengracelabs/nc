"""Institution Factory Runtime derived from candidate-only Asset Factory output."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, TypedDict

from services.data.asset_factory import (
    ASSET_FACTORY_VERSION,
    ASSET_SOURCES_DIR,
    AssetCandidate,
    asset_ingestion_pipeline,
    ingest_asset_source,
)
from services.data.place_seed import normalize_place_slug

INSTITUTION_FACTORY_VERSION = "NC-INSTITUTIONS-100-v1"
DEFAULT_ASSET_SOURCE = ASSET_SOURCES_DIR / "factory_smoke_assets.json"


class InstitutionRegistryRecord(TypedDict):
    institution_slug: str
    display_name: str
    source_systems: list[str]
    candidate_status: str
    authority_status: str
    canonical_institution_created: bool


def _readiness_state(ready_count: int, review_count: int, hold_count: int) -> str:
    if hold_count:
        return "hold"
    if review_count:
        return "review"
    if ready_count:
        return "ready"
    return "review"


def build_institution_registry(candidates: list[AssetCandidate]) -> list[InstitutionRegistryRecord]:
    grouped: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        name = candidate["source_institution"]
        slug = normalize_place_slug(name)
        grouped.setdefault(
            slug,
            {
                "institution_slug": slug,
                "display_name": name,
                "source_systems": set(),
                "candidate_status": "candidate",
                "authority_status": "source_observed",
                "canonical_institution_created": False,
            },
        )
        grouped[slug]["source_systems"].add(candidate["source_system"])
    return [
        {**record, "source_systems": sorted(record["source_systems"])}
        for record in sorted(grouped.values(), key=lambda item: item["institution_slug"])
    ]


def build_institution_asset_counts(candidates: list[AssetCandidate]) -> dict[str, dict[str, Any]]:
    counts: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        slug = normalize_place_slug(candidate["source_institution"])
        counts.setdefault(
            slug,
            {
                "total_assets": 0,
                "media_type_counts": Counter(),
                "rights_status_counts": Counter(),
                "readiness_counts": Counter(),
            },
        )
        counts[slug]["total_assets"] += 1
        counts[slug]["media_type_counts"][candidate["media_type"]] += 1
        counts[slug]["rights_status_counts"][candidate["rights_status"]] += 1
        counts[slug]["readiness_counts"][candidate["asset_readiness"]["state"]] += 1
    return {
        slug: {
            "total_assets": item["total_assets"],
            "media_type_counts": dict(sorted(item["media_type_counts"].items())),
            "rights_status_counts": dict(sorted(item["rights_status_counts"].items())),
            "readiness_counts": dict(sorted(item["readiness_counts"].items())),
        }
        for slug, item in sorted(counts.items())
    }


def build_institution_collection_counts(candidates: list[AssetCandidate]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(lambda: {"collections": set(), "mapping_count": 0})
    for candidate in candidates:
        slug = normalize_place_slug(candidate["source_institution"])
        for mapping in candidate["asset_collection_mapping"]:
            grouped[slug]["collections"].add(mapping["collection_slug"])
            grouped[slug]["mapping_count"] += 1
    return {
        slug: {
            "collection_count": len(item["collections"]),
            "mapping_count": item["mapping_count"],
            "collections": sorted(item["collections"]),
        }
        for slug, item in sorted(grouped.items())
    }


def build_institution_readiness(candidates: list[AssetCandidate]) -> dict[str, dict[str, Any]]:
    asset_counts = build_institution_asset_counts(candidates)
    collection_counts = build_institution_collection_counts(candidates)
    readiness: dict[str, dict[str, Any]] = {}
    for slug, counts in asset_counts.items():
        readiness_counts = counts["readiness_counts"]
        ready = int(readiness_counts.get("ready", 0))
        review = int(readiness_counts.get("review", 0))
        hold = int(readiness_counts.get("hold", 0))
        total = int(counts["total_assets"])
        mapped_collections = collection_counts.get(slug, {}).get("collection_count", 0)
        readiness[slug] = {
            "state": _readiness_state(ready, review, hold),
            "ready_assets": ready,
            "review_assets": review,
            "hold_assets": hold,
            "total_assets": total,
            "collection_count": mapped_collections,
            "readiness_score": round(((ready * 100) + (review * 62) + (hold * 20)) / total, 2)
            if total
            else 0.0,
            "candidate_only": True,
        }
    return readiness


def build_institution_factory_runtime(candidates: list[AssetCandidate] | None = None) -> dict[str, Any]:
    materialized = candidates if candidates is not None else ingest_asset_source(DEFAULT_ASSET_SOURCE)
    registry = build_institution_registry(materialized)
    readiness = build_institution_readiness(materialized)
    asset_counts = build_institution_asset_counts(materialized)
    collection_counts = build_institution_collection_counts(materialized)
    return {
        "runtime_version": INSTITUTION_FACTORY_VERSION,
        "asset_factory_version": ASSET_FACTORY_VERSION,
        "institution_registry": registry,
        "institution_readiness": readiness,
        "institution_asset_counts": asset_counts,
        "institution_collection_counts": collection_counts,
        "canonical_institution_created": False,
        "canonical_publication_created": False,
        "summary": {
            "institution_count": len(registry),
            "asset_count": len(materialized),
            "collection_mapping_count": sum(item["mapping_count"] for item in collection_counts.values()),
            "ready_institutions": sum(1 for item in readiness.values() if item["state"] == "ready"),
            "review_institutions": sum(1 for item in readiness.values() if item["state"] == "review"),
            "hold_institutions": sum(1 for item in readiness.values() if item["state"] == "hold"),
            "candidate_only": True,
        },
    }


def institution_factory_from_asset_pipeline(paths: list[str]) -> dict[str, Any]:
    asset_runtime = asset_ingestion_pipeline(paths)
    return build_institution_factory_runtime(asset_runtime["asset_candidates"])
