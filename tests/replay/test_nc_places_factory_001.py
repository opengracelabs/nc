import json
from pathlib import Path

from services.data.place_factory import (
    export_place_batch,
    ingest_place_source,
    summarize_place_factory,
)

SOURCE_DIR = Path("data/curated/place_sources")
CANDIDATE_DIR = Path("data/curated/place_candidates")
SMOKE_SOURCE = SOURCE_DIR / "factory_smoke_places.json"


def test_nc_places_factory_001_directories_exist():
    assert SOURCE_DIR.exists()
    assert CANDIDATE_DIR.exists()


def test_nc_places_factory_001_ingests_smoke_source():
    candidates = ingest_place_source(SMOKE_SOURCE)

    assert {candidate["designation_family"] for candidate in candidates} == {
        "UNESCO",
        "Biosphere",
        "Geopark",
        "Ramsar",
        "ICH",
        "Dark Sky",
        "Marine Protected Area",
    }
    assert {candidate["place_slug"] for candidate in candidates} >= {
        "yellowstone",
        "okavango-delta",
        "pacific-wayfinding",
    }
    assert all(candidate["authority_status"] == "unverified" for candidate in candidates)


def test_nc_places_factory_001_candidates_have_required_schema_fields():
    required = {
        "source_list",
        "designation_type",
        "display_name",
        "country",
        "region",
        "latitude",
        "longitude",
        "source_url",
        "authority_status",
        "product_potential_score",
        "story_potential_score",
        "collection_potential_score",
        "ich_connections",
        "public_domain_source_hints",
        "place_family",
        "designation_family",
        "collection_family",
        "discovery_family",
        "collection_readiness",
        "graph_readiness",
        "product_readiness",
    }

    for candidate in ingest_place_source(SMOKE_SOURCE):
        assert required.issubset(candidate)
        assert "canonical_place_id" not in candidate
        assert "geonames_id" not in candidate
        assert "wikidata_qid" not in candidate


def test_nc_places_factory_001_exports_candidate_batch_without_canonical_identity(tmp_path):
    candidates = ingest_place_source(SMOKE_SOURCE)
    output = export_place_batch(candidates, "NC Places Factory 001 Smoke", tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert len(payload) == 7
    assert all(candidate["authority_status"] == "unverified" for candidate in payload)
    assert all("canonical_identity" not in candidate for candidate in payload)
    assert all("canonical_place_id" not in candidate for candidate in payload)


def test_nc_places_factory_001_summary_keeps_canonical_identity_deferred():
    summary = summarize_place_factory(ingest_place_source(SMOKE_SOURCE))

    assert summary["total_candidates"] == 7
    assert summary["source_list_counts"] == {"factory_smoke_places": 7}
    assert summary["scale_target"] == 10000
    assert summary["canonical_identity_written"] is False
