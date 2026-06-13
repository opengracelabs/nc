import json

from services.data.place_coverage import (
    coverage_region,
    load_candidate_places,
    summarize_place_coverage,
)


def test_load_candidate_places_keeps_batch_candidate_only():
    candidates = load_candidate_places()

    assert len(candidates) == 218
    assert {candidate["authority_status"] for candidate in candidates} == {"source_observed"}
    assert all("canonical_place_id" not in candidate for candidate in candidates)


def test_summarize_place_coverage_reports_map_regions_and_gaps():
    summary = summarize_place_coverage(load_candidate_places())

    assert summary["total_candidates"] == 218
    assert summary["mapped_candidates"] == 175
    assert summary["authority_gap_counts"]["missing_coordinates"] == 43
    assert summary["designation_family_counts"] == {
        "Biosphere": 42,
        "Geopark": 45,
        "ICH": 43,
        "Ramsar": 45,
        "UNESCO": 43,
    }
    assert summary["region_counts"]["Europe"] == 96
    assert summary["region_counts"]["Asia"] == 48
    assert summary["collection_family_gaps"]["missing_expected_families"] == [
        "dark_sky_collection",
        "marine_collection",
    ]
    assert summary["canonical_identity_written"] is False


def test_coverage_region_derives_from_country_when_source_region_is_global():
    candidate = load_candidate_places()[0]
    candidate = dict(candidate, country="Japan", region="Global")

    assert coverage_region(candidate) == "Asia"


def test_exported_coverage_summary_matches_candidate_batch():
    with open(
        "data/curated/place_candidates/nc-places-250-coverage-summary.json",
        encoding="utf-8",
    ) as handle:
        summary = json.load(handle)

    assert summary["total_candidates"] == 218
    assert summary["mapped_candidates"] == 175
    assert summary["authority_gap_counts"]["source_observed_only"] == 218
