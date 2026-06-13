"""Candidate-only Taxon Factory runtime for GBIF, BHL, and Darwin Core evidence."""

from __future__ import annotations

from collections import Counter
from typing import Any, TypedDict

from services.data.bhl_connector import BHL_RUNTIME_VERSION, build_bhl_runtime
from services.data.place_seed import normalize_place_slug

TAXON_FACTORY_VERSION = "NC-TAXON-001-v1"
SUPPORTED_TAXON_SOURCES = ("GBIF", "BHL", "Darwin Core")


class TaxonCandidate(TypedDict):
    taxon_candidate_id: str
    candidate_status: str
    scientific_name: str
    canonical_name: str
    accepted_scientific_name: str
    taxon_rank: str
    gbif_taxon_key: str
    accepted_taxon_key: str
    source_systems: list[str]
    bhl_source_records: list[str]
    place_slugs: list[str]
    common_names: list[str]
    collection_hints: list[str]
    product_hints: list[str]
    darwin_core_mapping: dict[str, str]
    taxonomic_enrichment: dict[str, Any]
    candidate_only: bool
    canonical_taxon_created: bool
    canonical_publication_created: bool


def _first_string(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _candidate_id(enrichment: dict[str, Any], gbif_mapping: dict[str, Any]) -> str:
    key = _first_string(gbif_mapping.get("accepted_taxon_key"), gbif_mapping.get("gbif_taxon_key"))
    name = _first_string(enrichment.get("canonical_name"), enrichment.get("scientific_name"), key)
    return f"taxon-{normalize_place_slug(key or name)}"


def build_taxon_candidates(bhl_runtime: dict[str, Any] | None = None) -> list[TaxonCandidate]:
    runtime = bhl_runtime or build_bhl_runtime()
    grouped: dict[str, dict[str, Any]] = {}
    for illustration in runtime["illustration_candidate_extraction"]:
        gbif_mapping = illustration["gbif_mapping"]
        enrichment = illustration["taxonomic_enrichment"]
        candidate_id = _candidate_id(enrichment, gbif_mapping)
        grouped.setdefault(
            candidate_id,
            {
                "taxon_candidate_id": candidate_id,
                "candidate_status": "candidate",
                "scientific_name": _first_string(
                    gbif_mapping.get("scientific_name"), enrichment.get("scientific_name")
                ),
                "canonical_name": _first_string(enrichment.get("canonical_name"), gbif_mapping.get("scientific_name")),
                "accepted_scientific_name": _first_string(enrichment.get("accepted_scientific_name")),
                "taxon_rank": _first_string(enrichment.get("taxon_rank")),
                "gbif_taxon_key": _first_string(gbif_mapping.get("gbif_taxon_key")),
                "accepted_taxon_key": _first_string(gbif_mapping.get("accepted_taxon_key")),
                "source_systems": set(),
                "bhl_source_records": set(),
                "place_slugs": set(),
                "common_names": set(),
                "collection_hints": set(),
                "product_hints": set(),
                "darwin_core_mapping": gbif_mapping.get("darwin_core_mapping") or {},
                "taxonomic_enrichment": enrichment,
                "candidate_only": True,
                "canonical_taxon_created": False,
                "canonical_publication_created": False,
            },
        )
        record = grouped[candidate_id]
        record["source_systems"].update({"GBIF", "BHL", "Darwin Core"})
        record["bhl_source_records"].add(illustration["source_record_id"])
        record["place_slugs"].add(illustration["place_slug"])
        record["collection_hints"].update(illustration["collection_hints"])
        record["product_hints"].update(illustration["product_hints"])
        for hint in illustration["species_hints"]:
            if hint != record["scientific_name"]:
                record["common_names"].add(hint)

    return [
        {
            **record,
            "source_systems": [source for source in SUPPORTED_TAXON_SOURCES if source in record["source_systems"]],
            "bhl_source_records": sorted(record["bhl_source_records"]),
            "place_slugs": sorted(record["place_slugs"]),
            "common_names": sorted(record["common_names"]),
            "collection_hints": sorted(record["collection_hints"]),
            "product_hints": sorted(record["product_hints"]),
        }
        for record in sorted(grouped.values(), key=lambda item: item["taxon_candidate_id"])
    ]


def build_taxon_readiness(candidates: list[TaxonCandidate]) -> dict[str, dict[str, Any]]:
    readiness = {}
    for candidate in candidates:
        missing = []
        if not candidate["gbif_taxon_key"]:
            missing.append("gbif_taxon_key")
        if not candidate["darwin_core_mapping"]:
            missing.append("darwin_core_mapping")
        if not candidate["bhl_source_records"]:
            missing.append("bhl_source_record")
        if not candidate["collection_hints"]:
            missing.append("collection_mapping")
        if not candidate["product_hints"]:
            missing.append("product_mapping")
        score = 100 - len(missing) * 18
        readiness[candidate["taxon_candidate_id"]] = {
            "state": "ready" if score >= 82 and not missing else "review" if score >= 55 else "hold",
            "readiness_score": max(score, 0),
            "missing": missing,
            "gbif_ready": bool(candidate["gbif_taxon_key"]),
            "bhl_ready": bool(candidate["bhl_source_records"]),
            "darwin_core_ready": bool(candidate["darwin_core_mapping"]),
            "candidate_only": True,
        }
    return readiness


def build_taxon_collection_mapping(candidates: list[TaxonCandidate]) -> dict[str, list[dict[str, Any]]]:
    mapping = {}
    for candidate in candidates:
        mapping[candidate["taxon_candidate_id"]] = [
            {
                "mapping_status": "candidate",
                "collection_slug": normalize_place_slug(collection),
                "fit_score": min(100, 72 + index * 6),
                "evidence": ["bhl_source_record", "gbif_taxon", "darwin_core_taxon"],
            }
            for index, collection in enumerate(candidate["collection_hints"][:6])
        ]
    return mapping


def build_taxon_product_mapping(candidates: list[TaxonCandidate]) -> dict[str, list[dict[str, Any]]]:
    mapping = {}
    for candidate in candidates:
        mapping[candidate["taxon_candidate_id"]] = [
            {
                "mapping_status": "candidate",
                "product_type": product,
                "fit_score": min(100, 76 + index * 4),
                "requires_review": False,
            }
            for index, product in enumerate(candidate["product_hints"][:8])
        ]
    return mapping


def summarize_taxon_factory(candidates: list[TaxonCandidate], readiness: dict[str, dict[str, Any]]) -> dict[str, Any]:
    readiness_counts = Counter(item["state"] for item in readiness.values())
    return {
        "runtime_version": TAXON_FACTORY_VERSION,
        "total_candidates": len(candidates),
        "supported_sources": list(SUPPORTED_TAXON_SOURCES),
        "source_system_counts": dict(sorted(Counter(source for c in candidates for source in c["source_systems"]).items())),
        "taxon_rank_counts": dict(sorted(Counter(c["taxon_rank"] for c in candidates).items())),
        "readiness_counts": dict(sorted(readiness_counts.items())),
        "collection_mapping_count": sum(len(c["collection_hints"]) for c in candidates),
        "product_mapping_count": sum(len(c["product_hints"]) for c in candidates),
        "candidate_only": True,
        "canonical_taxon_created": False,
        "canonical_publication_created": False,
    }


def build_taxon_factory_runtime(bhl_runtime: dict[str, Any] | None = None) -> dict[str, Any]:
    runtime = bhl_runtime or build_bhl_runtime()
    candidates = build_taxon_candidates(runtime)
    readiness = build_taxon_readiness(candidates)
    collection_mapping = build_taxon_collection_mapping(candidates)
    product_mapping = build_taxon_product_mapping(candidates)
    return {
        "runtime_version": TAXON_FACTORY_VERSION,
        "bhl_runtime_version": runtime["runtime_version"],
        "taxon_candidates": candidates,
        "taxon_readiness": readiness,
        "taxon_collection_mapping": collection_mapping,
        "taxon_product_mapping": product_mapping,
        "candidate_only": True,
        "canonical_taxon_created": False,
        "canonical_publication_created": False,
        "summary": summarize_taxon_factory(candidates, readiness),
    }
