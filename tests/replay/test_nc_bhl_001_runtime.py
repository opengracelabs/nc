"""NC-BHL-001 replay tests."""

from services.data.bhl_connector import build_bhl_runtime


def test_nc_bhl_001_runtime_is_candidate_only() -> None:
    runtime = build_bhl_runtime()

    assert runtime["runtime_version"] == "NC-BHL-001-v1"
    assert runtime["asset_factory_version"] == "NC-ASSETS-1000000-v1"
    assert runtime["summary"]["candidate_only"] is True
    assert runtime["canonical_publication_created"] is False
    assert all(
        candidate["canonical_publication_created"] is False
        for candidate in runtime["asset_factory_feed"]["asset_candidates"]
    )


def test_nc_bhl_001_supports_required_connector_surfaces() -> None:
    runtime = build_bhl_runtime()

    assert runtime["summary"]["title_count"] == 2
    assert runtime["summary"]["page_count"] == 3
    assert runtime["summary"]["illustration_candidate_count"] == 2
    assert runtime["summary"]["gbif_mapping_count"] == 2
    assert runtime["summary"]["taxonomic_enrichment_count"] == 2
    assert set(runtime["gbif_mapping"]) == {
        "bhl-item-1001:page:page-2001",
        "bhl-item-1002:page:page-2002",
    }
    assert set(runtime["asset_factory_feed"]["summary"]["media_type_counts"]) == {"illustration"}
