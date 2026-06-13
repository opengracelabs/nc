"""Masterpiece Registry runtime for ranked collection-worthy works."""

from __future__ import annotations

from collections import Counter
from typing import Any, TypedDict

from services.data.io_factory import IO_FACTORY_VERSION, build_io_factory_runtime
from services.data.place_seed import normalize_place_slug

MASTERPIECE_RUNTIME_VERSION = "NC-MASTERPIECES-001-v1"


class MasterpieceRegistryRecord(TypedDict):
    masterpiece_slug: str
    title: str
    source_system: str
    source_record_id: str
    registry_status: str
    masterpiece_score: int
    collection_slugs: list[str]
    product_types: list[str]
    primary_collection: str
    place_slug: str
    taxon_name: str
    rights_status: str
    readiness_state: str
    source_url: str
    candidate_only: bool
    canonical_publication_created: bool


def score_masterpiece(record: dict[str, Any]) -> int:
    base = int(record.get("base_score") or 0)
    readiness_bonus = 12 if record.get("readiness_state") == "ready" else 5
    collection_bonus = min(16, len(record.get("collection_slugs") or []) * 4)
    product_bonus = min(12, len(record.get("product_types") or []) * 2)
    rights_bonus = 12 if record.get("rights_status") in {"verified_pd", "public_domain"} else 4
    return max(0, min(100, base + readiness_bonus + collection_bonus + product_bonus + rights_bonus))


def _earthrise_record() -> MasterpieceRegistryRecord:
    working = {
        "base_score": 58,
        "readiness_state": "ready",
        "collection_slugs": ["earthrise", "space-earth-observation", "planetary-stewardship"],
        "product_types": ["fine_art_print", "framed_print", "digital_download", "educational_pack"],
        "rights_status": "public_domain",
    }
    return {
        "masterpiece_slug": "earthrise",
        "title": "Earthrise",
        "source_system": "NASA",
        "source_record_id": "AS08-14-2383",
        "registry_status": "published",
        "masterpiece_score": score_masterpiece(working),
        "collection_slugs": working["collection_slugs"],
        "product_types": working["product_types"],
        "primary_collection": "earthrise",
        "place_slug": "earthrise",
        "taxon_name": "",
        "rights_status": working["rights_status"],
        "readiness_state": working["readiness_state"],
        "source_url": "https://www.nasa.gov/image-article/apollo-8-earthrise/",
        "candidate_only": False,
        "canonical_publication_created": True,
    }


def build_masterpiece_registry(io_runtime: dict[str, Any] | None = None) -> list[MasterpieceRegistryRecord]:
    io = io_runtime or build_io_factory_runtime()
    readiness = io["io_readiness"]
    records: list[MasterpieceRegistryRecord] = [_earthrise_record()]
    for opportunity in io["illustration_opportunities"]:
        readiness_state = readiness[opportunity["illustration_opportunity_id"]]["state"]
        working = {
            "base_score": 44,
            "readiness_state": readiness_state,
            "collection_slugs": opportunity["collection_hints"],
            "product_types": opportunity["product_hints"],
            "rights_status": "verified_pd",
        }
        records.append(
            {
                "masterpiece_slug": normalize_place_slug(opportunity["title"]),
                "title": opportunity["title"],
                "source_system": opportunity["source_system"],
                "source_record_id": opportunity["source_record_id"],
                "registry_status": "candidate",
                "masterpiece_score": score_masterpiece(working),
                "collection_slugs": opportunity["collection_hints"],
                "product_types": opportunity["product_hints"],
                "primary_collection": opportunity["collection_hints"][0],
                "place_slug": opportunity["place_slug"],
                "taxon_name": opportunity["canonical_name"],
                "rights_status": working["rights_status"],
                "readiness_state": readiness_state,
                "source_url": opportunity["source_url"],
                "candidate_only": True,
                "canonical_publication_created": False,
            }
        )
    return sorted(records, key=lambda item: (-item["masterpiece_score"], item["title"]))


def build_masterpiece_collections(registry: list[MasterpieceRegistryRecord]) -> dict[str, list[dict[str, Any]]]:
    collections: dict[str, list[dict[str, Any]]] = {}
    for record in registry:
        for collection_slug in record["collection_slugs"]:
            collections.setdefault(collection_slug, []).append(
                {
                    "masterpiece_slug": record["masterpiece_slug"],
                    "title": record["title"],
                    "masterpiece_score": record["masterpiece_score"],
                    "registry_status": record["registry_status"],
                }
            )
    return {slug: sorted(items, key=lambda item: (-item["masterpiece_score"], item["title"])) for slug, items in sorted(collections.items())}


def build_masterpiece_runtime(io_runtime: dict[str, Any] | None = None) -> dict[str, Any]:
    io = io_runtime or build_io_factory_runtime()
    registry = build_masterpiece_registry(io)
    collections = build_masterpiece_collections(registry)
    score = {record["masterpiece_slug"]: record["masterpiece_score"] for record in registry}
    return {
        "runtime_version": MASTERPIECE_RUNTIME_VERSION,
        "io_runtime_version": io["runtime_version"],
        "masterpiece_score": score,
        "masterpiece_registry": registry,
        "masterpiece_collections": collections,
        "summary": {
            "runtime_version": MASTERPIECE_RUNTIME_VERSION,
            "total_masterpieces": len(registry),
            "top_100_count": min(100, len(registry)),
            "registry_status_counts": dict(sorted(Counter(record["registry_status"] for record in registry).items())),
            "source_system_counts": dict(sorted(Counter(record["source_system"] for record in registry).items())),
            "collection_count": len(collections),
            "candidate_count": sum(1 for record in registry if record["candidate_only"]),
            "published_count": sum(1 for record in registry if not record["candidate_only"]),
        },
    }
