"""NC-INSTITUTIONS-100 replay tests."""

from services.data.institution_factory import build_institution_factory_runtime


def test_nc_institutions_100_runtime_is_candidate_only() -> None:
    runtime = build_institution_factory_runtime()

    assert runtime["runtime_version"] == "NC-INSTITUTIONS-100-v1"
    assert runtime["asset_factory_version"] == "NC-ASSETS-1000000-v1"
    assert runtime["canonical_institution_created"] is False
    assert runtime["canonical_publication_created"] is False
    assert runtime["summary"]["candidate_only"] is True
    assert all(record["canonical_institution_created"] is False for record in runtime["institution_registry"])


def test_nc_institutions_100_exposes_required_factory_surfaces() -> None:
    runtime = build_institution_factory_runtime()

    assert len(runtime["institution_registry"]) == 8
    assert set(runtime["institution_readiness"]) == set(runtime["institution_asset_counts"])
    assert set(runtime["institution_readiness"]) == set(runtime["institution_collection_counts"])
    assert runtime["summary"]["asset_count"] == 8
    assert runtime["summary"]["collection_mapping_count"] == 9
    assert runtime["institution_readiness"]["nasa"]["state"] == "ready"
    assert runtime["institution_readiness"]["noaa"]["state"] == "review"
