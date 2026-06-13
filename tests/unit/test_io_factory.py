from services.api.main import app
from services.data.io_factory import (
    IO_FACTORY_VERSION,
    build_illustration_opportunities,
    build_io_collection_mapping,
    build_io_factory_runtime,
    build_io_product_mapping,
    build_io_readiness,
)


def test_io_factory_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/io/factory" in paths
    assert "/io/candidates" in paths
    assert "/io/summary" in paths


def test_illustration_opportunities_join_asset_taxon_and_place_candidates() -> None:
    opportunities = build_illustration_opportunities()

    assert len(opportunities) == 2
    assert {opportunity["canonical_name"] for opportunity in opportunities} == {
        "Acanthaster planci",
        "Bison bison",
    }
    assert all(opportunity["candidate_status"] == "candidate" for opportunity in opportunities)
    assert all(opportunity["source_system"] == "BHL" for opportunity in opportunities)
    assert all(opportunity["asset_candidate_id"].startswith("bhl-") for opportunity in opportunities)
    assert all(opportunity["taxon_candidate_id"].startswith("taxon-") for opportunity in opportunities)
    assert {opportunity["evidence"]["place_factory_match"] for opportunity in opportunities} == {False, True}
    assert any(
        opportunity["place_slug"] == "yellowstone" and opportunity["evidence"]["place_factory_match"] is True
        for opportunity in opportunities
    )
    assert any(
        opportunity["place_slug"] == "great-barrier-reef"
        and opportunity["evidence"]["place_factory_match"] is False
        for opportunity in opportunities
    )
    assert all(opportunity["canonical_publication_created"] is False for opportunity in opportunities)


def test_io_readiness_uses_asset_taxon_and_place_evidence() -> None:
    opportunities = build_illustration_opportunities()
    readiness = build_io_readiness(opportunities)

    assert set(readiness) == {opportunity["illustration_opportunity_id"] for opportunity in opportunities}
    assert all(item["state"] == "ready" for item in readiness.values())
    assert all(item["asset_ready"] is True for item in readiness.values())
    assert all(item["taxon_ready"] is True for item in readiness.values())
    assert {item["place_ready"] for item in readiness.values()} == {False, True}
    assert all(item["candidate_only"] is True for item in readiness.values())


def test_io_collection_and_product_mappings_are_candidate_only() -> None:
    opportunities = build_illustration_opportunities()
    collection_mapping = build_io_collection_mapping(opportunities)
    product_mapping = build_io_product_mapping(opportunities)

    assert all(collection_mapping[opportunity["illustration_opportunity_id"]] for opportunity in opportunities)
    assert all(product_mapping[opportunity["illustration_opportunity_id"]] for opportunity in opportunities)
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


def test_io_factory_runtime_returns_required_surfaces() -> None:
    runtime = build_io_factory_runtime()

    assert runtime["runtime_version"] == IO_FACTORY_VERSION
    assert runtime["asset_factory_version"] == "NC-ASSETS-1000000-v1"
    assert runtime["taxon_factory_version"] == "NC-TAXON-001-v1"
    assert runtime["candidate_only"] is True
    assert runtime["canonical_publication_created"] is False
    assert set(runtime) >= {
        "illustration_opportunities",
        "io_readiness",
        "io_collection_mapping",
        "io_product_mapping",
        "summary",
    }
    assert runtime["summary"] == {
        "runtime_version": "NC-IO-001-v1",
        "total_opportunities": 2,
        "candidate_status_counts": {"candidate": 2},
        "source_system_counts": {"BHL": 2},
        "readiness_counts": {"ready": 2},
        "collection_mapping_count": 4,
        "product_mapping_count": 10,
        "uses_asset_factory": True,
        "uses_taxon_factory": True,
        "uses_place_factory": True,
        "candidate_only": True,
        "canonical_publication_created": False,
    }
