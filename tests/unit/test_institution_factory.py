from services.api.main import app
from services.data.asset_factory import ingest_asset_source
from services.data.institution_factory import (
    INSTITUTION_FACTORY_VERSION,
    build_institution_asset_counts,
    build_institution_collection_counts,
    build_institution_factory_runtime,
    build_institution_readiness,
    build_institution_registry,
)


def _candidates():
    return ingest_asset_source("data/curated/asset_sources/factory_smoke_assets.json")


def test_institution_factory_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/assets/institutions/factory" in paths
    assert "/assets/institutions/factory/summary" in paths


def test_build_institution_registry_groups_asset_candidates_by_source_institution() -> None:
    registry = build_institution_registry(_candidates())

    assert len(registry) == 8
    assert {record["institution_slug"] for record in registry} >= {
        "nasa",
        "rijksmuseum",
        "biodiversity-heritage-library",
        "national-archives-and-records-administration",
    }
    assert all(record["candidate_status"] == "candidate" for record in registry)
    assert all(record["authority_status"] == "source_observed" for record in registry)
    assert all(record["canonical_institution_created"] is False for record in registry)


def test_institution_counts_surfaces_expose_assets_and_collection_mappings() -> None:
    candidates = _candidates()
    asset_counts = build_institution_asset_counts(candidates)
    collection_counts = build_institution_collection_counts(candidates)

    assert asset_counts["nasa"]["total_assets"] == 1
    assert asset_counts["nasa"]["media_type_counts"] == {"satellite": 1}
    assert asset_counts["nasa"]["rights_status_counts"] == {"verified_pd": 1}
    assert collection_counts["nasa"]["collections"] == ["earthrise"]
    assert collection_counts["biodiversity-heritage-library"]["collection_count"] == 2
    assert collection_counts["biodiversity-heritage-library"]["mapping_count"] == 2


def test_institution_readiness_preserves_candidate_only_review_state() -> None:
    readiness = build_institution_readiness(_candidates())

    assert readiness["nasa"]["state"] == "ready"
    assert readiness["nasa"]["readiness_score"] == 100.0
    assert readiness["national-archives-and-records-administration"]["state"] == "review"
    assert readiness["natural-history-museum"]["state"] == "review"
    assert readiness["noaa"]["state"] == "review"
    assert all(record["candidate_only"] is True for record in readiness.values())


def test_institution_factory_runtime_returns_required_surfaces() -> None:
    runtime = build_institution_factory_runtime(_candidates())

    assert runtime["runtime_version"] == INSTITUTION_FACTORY_VERSION
    assert runtime["canonical_institution_created"] is False
    assert runtime["canonical_publication_created"] is False
    assert set(runtime) >= {
        "institution_registry",
        "institution_readiness",
        "institution_asset_counts",
        "institution_collection_counts",
        "summary",
    }
    assert runtime["summary"] == {
        "institution_count": 8,
        "asset_count": 8,
        "collection_mapping_count": 9,
        "ready_institutions": 5,
        "review_institutions": 3,
        "hold_institutions": 0,
        "candidate_only": True,
    }
