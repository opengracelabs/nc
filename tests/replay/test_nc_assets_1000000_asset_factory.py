"""NC-ASSETS-1000000 replay tests."""

from services.data.asset_factory import asset_ingestion_pipeline


def test_nc_assets_1000000_asset_factory_runtime_is_candidate_only() -> None:
    runtime = asset_ingestion_pipeline(["data/curated/asset_sources/factory_smoke_assets.json"])

    assert runtime["runtime_version"] == "NC-ASSETS-1000000-v1"
    assert runtime["summary"]["scale_target"] == 1000000
    assert runtime["canonical_publication_created"] is False
    assert all(c["candidate_status"] == "candidate" for c in runtime["asset_candidates"])
    assert all(c["canonical_publication_created"] is False for c in runtime["asset_candidates"])


def test_nc_assets_1000000_asset_factory_supports_required_sources_and_mappings() -> None:
    runtime = asset_ingestion_pipeline(["data/curated/asset_sources/factory_smoke_assets.json"])

    assert set(runtime["summary"]["source_system_counts"]) == {
        "Europeana",
        "Smithsonian",
        "Rijksmuseum",
        "NHM",
        "BHL",
        "NASA",
        "NOAA",
        "NARA",
    }
    assert len(runtime["asset_readiness"]) == 8
    assert len(runtime["asset_collection_mapping"]) == 8
    assert len(runtime["asset_product_mapping"]) == 8
