import json

import pytest

from services.data.place_factory import (
    PlaceFactoryError,
    assign_place_families,
    batch_import_place_sources,
    export_place_batch,
    ingest_place_source,
    normalize_place_candidate,
    score_place_candidate,
    summarize_place_factory,
    validate_authority_fields,
)


def test_normalize_place_candidate_maps_required_schema_fields():
    candidate = normalize_place_candidate(
        {
            "source_list": "unit",
            "designation_type": "UNESCO_WH",
            "display_name": "Great Barrier Reef",
            "country": "Australia",
            "region": "Oceania",
            "latitude": -18.2871,
            "longitude": 147.6992,
            "source_url": "https://whc.unesco.org/en/list/",
            "authority_status": "unverified",
            "ich_connections": ["sea country knowledge"],
            "public_domain_source_hints": ["nasa", "noaa", "gbif"],
        }
    )

    assert candidate["place_slug"] == "great-barrier-reef"
    assert candidate["source_list"] == "unit"
    assert candidate["authority_status"] == "unverified"
    assert candidate["product_potential_score"] > 0
    assert candidate["story_potential_score"] > 0
    assert candidate["collection_potential_score"] > 0
    assert candidate["place_family"] == "heritage_place"
    assert candidate["designation_family"] == "UNESCO"
    assert candidate["collection_family"] == "world_heritage_collection"
    assert candidate["discovery_family"] == "heritage_discovery"
    assert candidate["collection_readiness"] in {"ready", "review", "hold"}
    assert candidate["graph_readiness"] in {"ready", "review", "hold"}
    assert candidate["product_readiness"] in {"ready", "review", "hold"}


def test_score_place_candidate_is_deterministic_and_bounded():
    base = {
        "designation_type": "UNESCO_WH",
        "latitude": 44.6,
        "longitude": -110.5,
        "ich_connections": ["seasonal practice"],
        "public_domain_source_hints": ["nara", "loc", "usgs"],
    }

    first = score_place_candidate(base)
    second = score_place_candidate(base)

    assert first == second
    assert all(0 <= value <= 100 for value in first.values())


def test_validate_authority_fields_rejects_canonical_identity():
    with pytest.raises(PlaceFactoryError, match="canonical authority fields"):
        validate_authority_fields(
            {
                "authority_status": "unverified",
                "canonical_place_id": "geonames:5843591",
            }
        )


def test_validate_authority_fields_rejects_ratified_status():
    with pytest.raises(PlaceFactoryError, match="authority_status"):
        validate_authority_fields({"authority_status": "ratified"})


def test_ingest_place_source_loads_object_payload(tmp_path):
    source_path = tmp_path / "source.json"
    source_path.write_text(
        json.dumps(
            {
                "source_list": "unit_source",
                "records": [
                    {
                        "designation_type": "UNESCO_Geopark",
                        "display_name": "Test Geopark",
                        "country": "Testland",
                        "region": "Europe",
                        "latitude": "40.1",
                        "longitude": "12.2",
                        "source_url": "https://example.test/source",
                        "authority_status": "source_observed",
                        "ich_connections": [],
                        "public_domain_source_hints": ["europeana"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    candidates = ingest_place_source(source_path)

    assert len(candidates) == 1
    assert candidates[0]["place_slug"] == "test-geopark"
    assert candidates[0]["latitude"] == 40.1
    assert candidates[0]["longitude"] == 12.2


def test_export_place_batch_writes_sorted_candidate_json(tmp_path):
    candidates = [
        normalize_place_candidate(
            {
                "source_list": "unit",
                "designation_type": "Ramsar",
                "display_name": "Beta Wetland",
                "country": "B",
                "region": "Africa",
                "latitude": None,
                "longitude": None,
                "source_url": "https://example.test/beta",
                "authority_status": "unverified",
                "ich_connections": [],
                "public_domain_source_hints": ["gbif"],
            }
        ),
        normalize_place_candidate(
            {
                "source_list": "unit",
                "designation_type": "DarkSky",
                "display_name": "Alpha Sky",
                "country": "A",
                "region": "North America",
                "latitude": 10,
                "longitude": 20,
                "source_url": "https://example.test/alpha",
                "authority_status": "unverified",
                "ich_connections": [],
                "public_domain_source_hints": ["nasa"],
            }
        ),
    ]

    output = export_place_batch(candidates, "Unit Batch", tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert output.name == "unit-batch.json"
    assert [item["place_slug"] for item in payload] == ["alpha-sky", "beta-wetland"]
    assert "canonical_place_id" not in payload[0]


def test_summarize_place_factory_reports_no_canonical_write():
    candidates = ingest_place_source("data/curated/place_sources/factory_smoke_places.json")
    summary = summarize_place_factory(candidates)

    assert summary["total_candidates"] == 7
    assert summary["authority_status_counts"] == {"unverified": 7}
    assert summary["designation_family_counts"] == {
        "Biosphere": 1,
        "Dark Sky": 1,
        "Geopark": 1,
        "ICH": 1,
        "Marine Protected Area": 1,
        "Ramsar": 1,
        "UNESCO": 1,
    }
    assert summary["scale_target"] == 10000
    assert summary["canonical_identity_written"] is False


def test_assign_place_families_supports_required_designation_systems():
    expected = {
        "UNESCO": "UNESCO",
        "Biosphere": "Biosphere",
        "Geopark": "Geopark",
        "Ramsar": "Ramsar",
        "ICH": "ICH",
        "Dark Sky": "Dark Sky",
        "Marine Protected Area": "Marine Protected Area",
    }

    for designation_type, designation_family in expected.items():
        families = assign_place_families({"designation_type": designation_type})

        assert families["designation_family"] == designation_family
        assert families["place_family"]
        assert families["collection_family"]
        assert families["discovery_family"]


def test_batch_import_place_sources_deduplicates_across_files(tmp_path):
    source_a = tmp_path / "a.json"
    source_b = tmp_path / "b.json"
    payload = {
        "records": [
            {
                "designation_type": "UNESCO",
                "display_name": "Duplicate Place",
                "country": "A",
                "region": "North America",
                "latitude": 1,
                "longitude": 2,
                "source_url": "https://example.test",
                "authority_status": "unverified",
                "ich_connections": [],
                "public_domain_source_hints": ["nasa"],
            }
        ]
    }
    source_a.write_text(json.dumps({"source_list": "a", **payload}), encoding="utf-8")
    source_b.write_text(json.dumps({"source_list": "b", **payload}), encoding="utf-8")

    with pytest.raises(PlaceFactoryError, match="duplicate place candidate across batch"):
        batch_import_place_sources([source_a, source_b])
