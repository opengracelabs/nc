from services.api.main import app
from services.data.bhl_connector import (
    BHL_RUNTIME_VERSION,
    build_bhl_runtime,
    build_gbif_mapping,
    build_taxonomic_enrichment,
    extract_illustration_candidates,
    feed_asset_factory,
    ingest_bhl_pages,
    ingest_bhl_titles,
    load_bhl_source,
)


def _payload():
    return load_bhl_source("data/curated/asset_sources/bhl_connector_seed.json")


def test_bhl_connector_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/assets/bhl/runtime" in paths
    assert "/assets/bhl/candidates" in paths
    assert "/assets/bhl/summary" in paths


def test_bhl_title_and_page_ingestion_are_deterministic() -> None:
    payload = _payload()
    titles = ingest_bhl_titles(payload)
    pages = ingest_bhl_pages(payload)

    assert len(titles) == 2
    assert len(pages) == 3
    assert titles[0]["item_id"] == "bhl-item-1001"
    assert pages[0]["page_id"] == "page-2001"
    assert pages[2]["has_illustration"] is False


def test_bhl_illustration_candidate_extraction_filters_non_illustrated_pages() -> None:
    payload = _payload()
    candidates = extract_illustration_candidates(ingest_bhl_titles(payload), ingest_bhl_pages(payload))

    assert len(candidates) == 2
    assert {candidate["bhl_page_id"] for candidate in candidates} == {"page-2001", "page-2002"}
    assert all(candidate["candidate_status"] == "candidate" for candidate in candidates)
    assert all(candidate["media_type"] == "illustration" for candidate in candidates)
    assert all(candidate["source_institution"] == "Biodiversity Heritage Library" for candidate in candidates)


def test_bhl_gbif_mapping_and_taxonomic_enrichment_are_candidate_evidence() -> None:
    page = ingest_bhl_pages(_payload())[0]
    mapping = build_gbif_mapping(page)
    enrichment = build_taxonomic_enrichment(page)

    assert mapping["mapping_status"] == "candidate"
    assert mapping["gbif_taxon_key"] == "2279059"
    assert mapping["darwin_core_mapping"]["scientific_name"] == "dwc:scientificName"
    assert enrichment["enrichment_status"] == "candidate"
    assert enrichment["canonical_name"] == "Acanthaster planci"
    assert enrichment["family"] == "Acanthasteridae"
    assert enrichment["candidate_only"] is True


def test_bhl_connector_feeds_asset_factory_candidate_only() -> None:
    payload = _payload()
    illustration_candidates = extract_illustration_candidates(ingest_bhl_titles(payload), ingest_bhl_pages(payload))
    asset_candidates = feed_asset_factory(illustration_candidates)

    assert len(asset_candidates) == 2
    assert all(candidate["source_system"] == "BHL" for candidate in asset_candidates)
    assert all(candidate["candidate_status"] == "candidate" for candidate in asset_candidates)
    assert all(candidate["canonical_publication_created"] is False for candidate in asset_candidates)
    assert {candidate["place_slug"] for candidate in asset_candidates} == {"great-barrier-reef", "yellowstone"}
    assert all(candidate["asset_readiness"]["candidate_only"] is True for candidate in asset_candidates)


def test_bhl_runtime_returns_required_surfaces() -> None:
    runtime = build_bhl_runtime("data/curated/asset_sources/bhl_connector_seed.json")

    assert runtime["runtime_version"] == BHL_RUNTIME_VERSION
    assert runtime["canonical_publication_created"] is False
    assert set(runtime) >= {
        "title_ingestion",
        "page_ingestion",
        "illustration_candidate_extraction",
        "gbif_mapping",
        "taxonomic_enrichment",
        "asset_factory_feed",
    }
    assert runtime["summary"] == {
        "title_count": 2,
        "page_count": 3,
        "illustration_candidate_count": 2,
        "asset_candidate_count": 2,
        "gbif_mapping_count": 2,
        "taxonomic_enrichment_count": 2,
        "candidate_only": True,
        "canonical_publication_created": False,
    }
    assert runtime["asset_factory_feed"]["summary"]["source_system_counts"] == {"BHL": 2}
