import json

from services.data.place_activation import (
    activation_place,
    load_activation_candidates,
    summarize_activation_dashboard,
    top_activation_places,
)


def test_top_activation_places_returns_ranked_top_25():
    top_places = top_activation_places(load_activation_candidates())

    assert len(top_places) == 25
    assert top_places[0]["activation_score"] >= top_places[-1]["activation_score"]
    assert all(place["authority_readiness"] == "Review" for place in top_places)
    assert all("place_slug" in place for place in top_places)


def test_activation_place_derives_publishing_readiness_from_readiness_columns():
    candidate = load_activation_candidates()[0]
    place = activation_place(candidate)

    assert place["authority_readiness"] == "Review"
    assert place["publishing_readiness"] in {"Review", "Hold"}
    assert isinstance(place["activation_score"], int)


def test_summarize_activation_dashboard_reports_all_readiness_groups():
    summary = summarize_activation_dashboard(load_activation_candidates())

    assert summary["total_candidates"] == 218
    assert summary["top_place_count"] == 25
    assert summary["authority_readiness_counts"] == {"Review": 218}
    assert set(summary["collection_readiness_counts"]) == {"Ready", "Review"}
    assert set(summary["product_readiness_counts"]) == {"Hold", "Review"}
    assert set(summary["graph_readiness_counts"]) == {"Ready", "Review"}
    assert set(summary["publishing_readiness_counts"]) == {"Hold", "Review"}
    assert summary["canonical_identity_written"] is False


def test_exported_activation_dashboard_summary_matches_top_25_contract():
    with open(
        "data/curated/place_candidates/nc-activation-001-dashboard.json",
        encoding="utf-8",
    ) as handle:
        summary = json.load(handle)

    assert summary["top_place_count"] == 25
    assert len(summary["top_places"]) == 25
    assert summary["canonical_identity_written"] is False
