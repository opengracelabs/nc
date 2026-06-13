"""NC-TAXON-001 replay tests."""

from services.data.taxon_factory import build_taxon_factory_runtime


def test_nc_taxon_001_runtime_is_candidate_only() -> None:
    runtime = build_taxon_factory_runtime()

    assert runtime["runtime_version"] == "NC-TAXON-001-v1"
    assert runtime["candidate_only"] is True
    assert runtime["canonical_taxon_created"] is False
    assert runtime["canonical_publication_created"] is False
    assert all(candidate["candidate_only"] is True for candidate in runtime["taxon_candidates"])
    assert all(candidate["canonical_taxon_created"] is False for candidate in runtime["taxon_candidates"])


def test_nc_taxon_001_exposes_factory_surfaces_and_supported_sources() -> None:
    runtime = build_taxon_factory_runtime()

    assert len(runtime["taxon_candidates"]) == 2
    assert set(runtime["taxon_readiness"]) == set(runtime["taxon_collection_mapping"])
    assert set(runtime["taxon_readiness"]) == set(runtime["taxon_product_mapping"])
    assert runtime["summary"]["supported_sources"] == ["GBIF", "BHL", "Darwin Core"]
    assert runtime["summary"]["source_system_counts"] == {"BHL": 2, "Darwin Core": 2, "GBIF": 2}
    assert runtime["summary"]["readiness_counts"] == {"ready": 2}
