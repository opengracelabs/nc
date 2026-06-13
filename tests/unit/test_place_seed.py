import pytest

from services.data.place_seed import (
    PlaceSeedError,
    export_candidate_summary,
    group_by_place_type,
    load_first_100_candidates,
    normalize_place_slug,
    validate_place_seed,
)


def test_normalize_place_slug_handles_display_names():
    assert normalize_place_slug("Great Barrier Reef") == "great-barrier-reef"
    assert normalize_place_slug("  Giant's Causeway  ") == "giant-s-causeway"
    assert normalize_place_slug("Papahanaumokuakea") == "papahanaumokuakea"


def test_load_first_100_candidates_returns_valid_candidate_records():
    records = load_first_100_candidates()

    assert len(records) == 100
    assert len({record["place_slug"] for record in records}) == 100
    assert {record["candidate_status"] for record in records} == {"candidate"}
    assert {record["authority_status"] for record in records} == {"unverified"}
    assert {"yellowstone", "grand-canyon", "great-barrier-reef", "earthrise"}.issubset(
        {record["place_slug"] for record in records}
    )


def test_group_by_place_type_returns_editorial_buckets():
    records = load_first_100_candidates()
    grouped = group_by_place_type(records)

    assert "national_park" in grouped
    assert any(record["place_slug"] == "yellowstone" for record in grouped["national_park"])
    assert sum(len(bucket) for bucket in grouped.values()) == 100


def test_export_candidate_summary_keeps_canonical_work_deferred():
    summary = export_candidate_summary(load_first_100_candidates())

    assert summary["total_candidates"] == 100
    assert summary["candidate_status_counts"] == {"candidate": 100}
    assert summary["authority_status_counts"] == {"unverified": 100}
    assert summary["canonical_identity_written"] is False
    assert summary["product_pages_created"] is False
    assert summary["neo4j_canonical_nodes_created"] is False


def test_validate_place_seed_rejects_canonical_fields():
    record = dict(load_first_100_candidates()[0])
    record["geonames_id"] = "5843591"

    with pytest.raises(PlaceSeedError, match="forbidden canonical fields"):
        validate_place_seed([record])


def test_validate_place_seed_rejects_authority_ratification():
    record = dict(load_first_100_candidates()[0])
    record["authority_status"] = "ratified"

    with pytest.raises(PlaceSeedError, match="authority_status must remain unverified"):
        validate_place_seed([record])


def test_validate_place_seed_rejects_non_normalized_slug():
    record = dict(load_first_100_candidates()[0])
    record["place_slug"] = "Yellowstone"

    with pytest.raises(PlaceSeedError, match="place_slug must be normalized"):
        validate_place_seed([record])
