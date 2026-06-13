"""Candidate-only Illustration Opportunity Runtime."""

from __future__ import annotations

from collections import Counter
from typing import Any, TypedDict

from services.data.asset_factory import ASSET_FACTORY_VERSION, ingest_asset_source
from services.data.bhl_connector import build_bhl_runtime
from services.data.place_factory import ingest_place_source
from services.data.place_seed import normalize_place_slug
from services.data.taxon_factory import TAXON_FACTORY_VERSION, build_taxon_factory_runtime

IO_FACTORY_VERSION = "NC-IO-001-v1"
DEFAULT_ASSET_SOURCE = "data/curated/asset_sources/factory_smoke_assets.json"
DEFAULT_PLACE_SOURCE = "data/curated/place_sources/factory_smoke_places.json"


class IllustrationOpportunity(TypedDict):
    illustration_opportunity_id: str
    candidate_status: str
    title: str
    source_system: str
    source_record_id: str
    asset_candidate_id: str
    taxon_candidate_id: str
    place_slug: str
    canonical_name: str
    collection_hints: list[str]
    product_hints: list[str]
    source_url: str
    evidence: dict[str, Any]
    candidate_only: bool
    canonical_publication_created: bool


def _asset_by_source_record(asset_candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {candidate["source_record_id"]: candidate for candidate in asset_candidates}


def _taxon_by_bhl_source_record(taxon_candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    linked = {}
    for candidate in taxon_candidates:
        for record_id in candidate["bhl_source_records"]:
            linked[record_id] = candidate
    return linked


def _place_by_slug(place_candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {candidate["place_slug"]: candidate for candidate in place_candidates}


def _readiness_state(score: int) -> str:
    if score >= 82:
        return "ready"
    if score >= 58:
        return "review"
    return "hold"


def build_illustration_opportunities(
    *,
    bhl_runtime: dict[str, Any] | None = None,
    taxon_runtime: dict[str, Any] | None = None,
    asset_candidates: list[dict[str, Any]] | None = None,
    place_candidates: list[dict[str, Any]] | None = None,
) -> list[IllustrationOpportunity]:
    bhl = bhl_runtime or build_bhl_runtime()
    taxa = taxon_runtime or build_taxon_factory_runtime(bhl)
    assets = asset_candidates or bhl["asset_factory_feed"]["asset_candidates"]
    places = place_candidates or ingest_place_source(DEFAULT_PLACE_SOURCE)

    assets_by_record = _asset_by_source_record(assets)
    taxa_by_record = _taxon_by_bhl_source_record(taxa["taxon_candidates"])
    places_by_slug = _place_by_slug(places)

    opportunities: list[IllustrationOpportunity] = []
    for illustration in bhl["illustration_candidate_extraction"]:
        record_id = illustration["source_record_id"]
        asset = assets_by_record.get(record_id)
        taxon = taxa_by_record.get(record_id)
        place = places_by_slug.get(illustration["place_slug"])
        if asset is None or taxon is None:
            continue
        opportunity_id = f"io-{normalize_place_slug(record_id)}"
        opportunities.append(
            {
                "illustration_opportunity_id": opportunity_id,
                "candidate_status": "candidate",
                "title": illustration["title"],
                "source_system": illustration["source_system"],
                "source_record_id": record_id,
                "asset_candidate_id": asset["asset_candidate_id"],
                "taxon_candidate_id": taxon["taxon_candidate_id"],
                "place_slug": illustration["place_slug"],
                "canonical_name": taxon["canonical_name"],
                "collection_hints": sorted(dict.fromkeys(asset["collection_hints"] + taxon["collection_hints"])),
                "product_hints": sorted(dict.fromkeys(asset["product_hints"] + taxon["product_hints"])),
                "source_url": illustration["source_url"],
                "evidence": {
                    "asset_factory_version": ASSET_FACTORY_VERSION,
                    "taxon_factory_version": TAXON_FACTORY_VERSION,
                    "bhl_runtime_version": bhl["runtime_version"],
                    "asset_readiness_state": asset["asset_readiness"]["state"],
                    "gbif_taxon_key": taxon["gbif_taxon_key"],
                    "darwin_core_mapping": taxon["darwin_core_mapping"],
                    "place_factory_match": bool(place),
                    "place_collection_family": place.get("collection_family") if place else "unmatched_place_candidate",
                    "place_product_readiness": place.get("product_readiness") if place else "review",
                },
                "candidate_only": True,
                "canonical_publication_created": False,
            }
        )
    return sorted(opportunities, key=lambda item: item["illustration_opportunity_id"])


def build_io_readiness(opportunities: list[IllustrationOpportunity]) -> dict[str, dict[str, Any]]:
    readiness = {}
    for opportunity in opportunities:
        evidence = opportunity["evidence"]
        missing = []
        if evidence["asset_readiness_state"] != "ready":
            missing.append("ready_asset_candidate")
        if not evidence["gbif_taxon_key"]:
            missing.append("gbif_taxon_key")
        if not evidence["darwin_core_mapping"]:
            missing.append("darwin_core_mapping")
        if not evidence["place_factory_match"]:
            missing.append("place_factory_match")
        if not opportunity["collection_hints"]:
            missing.append("collection_mapping")
        if not opportunity["product_hints"]:
            missing.append("product_mapping")
        score = max(0, 100 - len(missing) * 16)
        readiness[opportunity["illustration_opportunity_id"]] = {
            "state": _readiness_state(score) if missing else "ready",
            "readiness_score": score,
            "missing": missing,
            "asset_ready": evidence["asset_readiness_state"] == "ready",
            "taxon_ready": bool(evidence["gbif_taxon_key"] and evidence["darwin_core_mapping"]),
            "place_ready": bool(evidence["place_factory_match"]),
            "candidate_only": True,
        }
    return readiness


def build_io_collection_mapping(opportunities: list[IllustrationOpportunity]) -> dict[str, list[dict[str, Any]]]:
    return {
        opportunity["illustration_opportunity_id"]: [
            {
                "mapping_status": "candidate",
                "collection_slug": normalize_place_slug(collection),
                "fit_score": min(100, 74 + index * 5),
                "evidence": ["asset_factory", "taxon_factory", "place_factory"],
            }
            for index, collection in enumerate(opportunity["collection_hints"][:6])
        ]
        for opportunity in opportunities
    }


def build_io_product_mapping(opportunities: list[IllustrationOpportunity]) -> dict[str, list[dict[str, Any]]]:
    return {
        opportunity["illustration_opportunity_id"]: [
            {
                "mapping_status": "candidate",
                "product_type": product,
                "fit_score": min(100, 78 + index * 4),
                "requires_review": False,
            }
            for index, product in enumerate(opportunity["product_hints"][:8])
        ]
        for opportunity in opportunities
    }


def summarize_io_factory(
    opportunities: list[IllustrationOpportunity],
    readiness: dict[str, dict[str, Any]],
    collection_mapping: dict[str, list[dict[str, Any]]],
    product_mapping: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    return {
        "runtime_version": IO_FACTORY_VERSION,
        "total_opportunities": len(opportunities),
        "candidate_status_counts": dict(sorted(Counter(o["candidate_status"] for o in opportunities).items())),
        "source_system_counts": dict(sorted(Counter(o["source_system"] for o in opportunities).items())),
        "readiness_counts": dict(sorted(Counter(item["state"] for item in readiness.values()).items())),
        "collection_mapping_count": sum(len(items) for items in collection_mapping.values()),
        "product_mapping_count": sum(len(items) for items in product_mapping.values()),
        "uses_asset_factory": True,
        "uses_taxon_factory": True,
        "uses_place_factory": True,
        "candidate_only": True,
        "canonical_publication_created": False,
    }


def build_io_factory_runtime() -> dict[str, Any]:
    bhl = build_bhl_runtime()
    taxa = build_taxon_factory_runtime(bhl)
    asset_candidates = bhl["asset_factory_feed"]["asset_candidates"]
    # Load the broader Asset Factory source as an input dependency without forcing every asset into IO.
    ingest_asset_source(DEFAULT_ASSET_SOURCE)
    place_candidates = ingest_place_source(DEFAULT_PLACE_SOURCE)
    opportunities = build_illustration_opportunities(
        bhl_runtime=bhl,
        taxon_runtime=taxa,
        asset_candidates=asset_candidates,
        place_candidates=place_candidates,
    )
    readiness = build_io_readiness(opportunities)
    collection_mapping = build_io_collection_mapping(opportunities)
    product_mapping = build_io_product_mapping(opportunities)
    return {
        "runtime_version": IO_FACTORY_VERSION,
        "asset_factory_version": ASSET_FACTORY_VERSION,
        "taxon_factory_version": TAXON_FACTORY_VERSION,
        "place_factory_source": DEFAULT_PLACE_SOURCE,
        "illustration_opportunities": opportunities,
        "io_readiness": readiness,
        "io_collection_mapping": collection_mapping,
        "io_product_mapping": product_mapping,
        "candidate_only": True,
        "canonical_publication_created": False,
        "summary": summarize_io_factory(opportunities, readiness, collection_mapping, product_mapping),
    }
