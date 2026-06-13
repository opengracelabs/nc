import json

import pytest

from services.api.main import app
from services.data.asset_factory import (
    ASSET_FACTORY_VERSION,
    SUPPORTED_ASSET_SOURCES,
    AssetFactoryError,
    asset_ingestion_pipeline,
    export_asset_candidates,
    ingest_asset_source,
    normalize_asset_candidate,
    summarize_asset_factory,
    validate_candidate_only,
)


def test_asset_factory_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/assets/factory" in paths
    assert "/assets/factory/candidates" in paths
    assert "/assets/factory/summary" in paths


def test_normalize_asset_candidate_maps_required_candidate_surfaces() -> None:
    candidate = normalize_asset_candidate(
        {
            "source_system": "NASA",
            "source_record_id": "AS08-14-2383",
            "title": "Earthrise",
            "source_url": "https://www.nasa.gov/image-article/apollo-8-earthrise/",
            "asset_url": "/images/earthrise-as08-14-2383.jpg",
            "iiif_manifest_url": "https://images-assets.nasa.gov/image/AS08-14-2383/manifest.json",
            "rights_status": "verified_pd",
            "rights_statement_uri": "https://rightsstatements.org/vocab/NoC-US/1.0/",
            "place_slug": "earthrise",
            "media_type": "satellite",
            "width_px": 6000,
            "height_px": 6000,
            "collection_hints": ["earthrise"],
        }
    )

    assert candidate["asset_candidate_id"] == "nasa-as08-14-2383"
    assert candidate["candidate_status"] == "candidate"
    assert candidate["asset_readiness"]["state"] == "ready"
    assert candidate["asset_collection_mapping"][0]["collection_slug"] == "earthrise"
    assert {m["product_type"] for m in candidate["asset_product_mapping"]} >= {
        "fine_art_print",
        "digital_download",
    }
    assert candidate["canonical_publication_created"] is False


def test_validate_candidate_only_rejects_canonical_publication_fields() -> None:
    with pytest.raises(AssetFactoryError, match="canonical publication fields"):
        validate_candidate_only({"candidate_status": "candidate", "canonical_publication_id": "pub-1"})


def test_ingest_asset_source_supports_required_sources() -> None:
    candidates = ingest_asset_source("data/curated/asset_sources/factory_smoke_assets.json")

    assert len(candidates) == 8
    assert {candidate["source_system"] for candidate in candidates} == set(SUPPORTED_ASSET_SOURCES)
    assert all(candidate["canonical_publication_created"] is False for candidate in candidates)


def test_asset_ingestion_pipeline_returns_runtime_surfaces() -> None:
    runtime = asset_ingestion_pipeline(["data/curated/asset_sources/factory_smoke_assets.json"])

    assert runtime["runtime_version"] == ASSET_FACTORY_VERSION
    assert len(runtime["asset_candidates"]) == 8
    assert len(runtime["asset_readiness"]) == 8
    assert len(runtime["asset_collection_mapping"]) == 8
    assert len(runtime["asset_product_mapping"]) == 8
    assert runtime["canonical_publication_created"] is False


def test_export_asset_candidates_writes_candidate_only_json(tmp_path) -> None:
    candidates = ingest_asset_source("data/curated/asset_sources/factory_smoke_assets.json")
    output = export_asset_candidates(candidates, "asset factory unit", tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert output.name == "asset-factory-unit.json"
    assert len(payload) == 8
    assert all(item["canonical_publication_created"] is False for item in payload)
    assert "canonical_asset_id" not in payload[0]


def test_summarize_asset_factory_reports_scale_and_no_publication() -> None:
    summary = summarize_asset_factory(
        ingest_asset_source("data/curated/asset_sources/factory_smoke_assets.json")
    )

    assert summary["total_candidates"] == 8
    assert summary["scale_target"] == 1000000
    assert summary["canonical_publication_created"] is False
    assert summary["source_system_counts"] == {source: 1 for source in sorted(SUPPORTED_ASSET_SOURCES)}
    assert summary["collection_mapping_count"] >= 8
    assert summary["product_mapping_count"] >= 8
