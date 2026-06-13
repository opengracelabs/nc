"""NC-IO-001 replay tests."""

from services.data.io_factory import build_io_factory_runtime


def test_nc_io_001_runtime_is_candidate_only() -> None:
    runtime = build_io_factory_runtime()

    assert runtime["runtime_version"] == "NC-IO-001-v1"
    assert runtime["candidate_only"] is True
    assert runtime["canonical_publication_created"] is False
    assert all(
        opportunity["candidate_only"] is True
        for opportunity in runtime["illustration_opportunities"]
    )
    assert all(
        opportunity["canonical_publication_created"] is False
        for opportunity in runtime["illustration_opportunities"]
    )


def test_nc_io_001_exposes_required_factory_surfaces() -> None:
    runtime = build_io_factory_runtime()

    assert len(runtime["illustration_opportunities"]) == 2
    assert set(runtime["io_readiness"]) == set(runtime["io_collection_mapping"])
    assert set(runtime["io_readiness"]) == set(runtime["io_product_mapping"])
    assert runtime["summary"]["uses_asset_factory"] is True
    assert runtime["summary"]["uses_taxon_factory"] is True
    assert runtime["summary"]["uses_place_factory"] is True
    assert runtime["summary"]["readiness_counts"] == {"ready": 2}
