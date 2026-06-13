from services.api.main import app
from services.data.taxon_factory import (
    SUPPORTED_TAXON_SOURCES,
    TAXON_FACTORY_VERSION,
    build_taxon_candidates,
    build_taxon_collection_mapping,
    build_taxon_factory_runtime,
    build_taxon_product_mapping,
    build_taxon_readiness,
)


def test_taxon_factory_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/taxa/factory" in paths
    assert "/taxa/factory/candidates" in paths
    assert "/taxa/factory/summary" in paths


def test_taxon_candidates_are_derived_from_gbif_bhl_and_darwin_core() -> None:
    candidates = build_taxon_candidates()

    assert len(candidates) == 2
    assert {candidate["canonical_name"] for candidate in candidates} == {"Acanthaster planci", "Bison bison"}
    assert all(candidate["candidate_status"] == "candidate" for candidate in candidates)
    assert all(candidate["source_systems"] == list(SUPPORTED_TAXON_SOURCES) for candidate in candidates)
    assert all(candidate["darwin_core_mapping"]["scientific_name"] == "dwc:scientificName" for candidate in candidates)
    assert all(candidate["canonical_taxon_created"] is False for candidate in candidates)
    assert all(candidate["canonical_publication_created"] is False for candidate in candidates)


def test_taxon_readiness_requires_gbif_bhl_and_darwin_core_evidence() -> None:
    candidates = build_taxon_candidates()
    readiness = build_taxon_readiness(candidates)

    assert set(readiness) == {candidate["taxon_candidate_id"] for candidate in candidates}
    assert all(item["state"] == "ready" for item in readiness.values())
    assert all(item["gbif_ready"] is True for item in readiness.values())
    assert all(item["bhl_ready"] is True for item in readiness.values())
    assert all(item["darwin_core_ready"] is True for item in readiness.values())
    assert all(item["candidate_only"] is True for item in readiness.values())


def test_taxon_collection_and_product_mappings_are_candidate_only() -> None:
    candidates = build_taxon_candidates()
    collection_mapping = build_taxon_collection_mapping(candidates)
    product_mapping = build_taxon_product_mapping(candidates)

    assert all(collection_mapping[candidate["taxon_candidate_id"]] for candidate in candidates)
    assert all(product_mapping[candidate["taxon_candidate_id"]] for candidate in candidates)
    assert any(
        item["collection_slug"] == "great-barrier-reef"
        for mappings in collection_mapping.values()
        for item in mappings
    )
    assert any(
        item["product_type"] == "fine_art_print"
        for mappings in product_mapping.values()
        for item in mappings
    )
    assert all(
        item["mapping_status"] == "candidate"
        for mappings in collection_mapping.values()
        for item in mappings
    )
    assert all(
        item["mapping_status"] == "candidate"
        for mappings in product_mapping.values()
        for item in mappings
    )


def test_taxon_factory_runtime_returns_required_surfaces() -> None:
    runtime = build_taxon_factory_runtime()

    assert runtime["runtime_version"] == TAXON_FACTORY_VERSION
    assert runtime["bhl_runtime_version"] == "NC-BHL-001-v1"
    assert runtime["candidate_only"] is True
    assert runtime["canonical_taxon_created"] is False
    assert runtime["canonical_publication_created"] is False
    assert set(runtime) >= {
        "taxon_candidates",
        "taxon_readiness",
        "taxon_collection_mapping",
        "taxon_product_mapping",
        "summary",
    }
    assert runtime["summary"] == {
        "runtime_version": "NC-TAXON-001-v1",
        "total_candidates": 2,
        "supported_sources": ["GBIF", "BHL", "Darwin Core"],
        "source_system_counts": {"BHL": 2, "Darwin Core": 2, "GBIF": 2},
        "taxon_rank_counts": {"SPECIES": 2},
        "readiness_counts": {"ready": 2},
        "collection_mapping_count": 4,
        "product_mapping_count": 10,
        "candidate_only": True,
        "canonical_taxon_created": False,
        "canonical_publication_created": False,
    }
