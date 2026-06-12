import socket

import pytest

from services.ai.earthrise_demo import NASA_NONENDORSEMENT
from services.ai.place_pipeline import PAGE_TYPES, generate_place_pipeline
from services.api.main import app

PILOT_PLACES = ("yellowstone", "grand-canyon", "great-barrier-reef")


def test_place_generation_route_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/ai/place-generation/{anchor_slug}" in paths


@pytest.mark.parametrize("anchor_slug", PILOT_PLACES)
def test_place_pipeline_generates_required_page_outputs(anchor_slug: str) -> None:
    result = generate_place_pipeline(anchor_slug)

    assert result["anchor_slug"] == anchor_slug
    assert result["provider"] == "deterministic-mock-v1"
    assert result["external_api_calls"] == 0
    assert result["publication_allowed"] is False
    assert result["human_review_required"] is True
    for page_type in PAGE_TYPES:
        assert page_type in result
        assert result[page_type]["hero_text"]
        assert result[page_type]["story_text"]
        assert result[page_type]["product_text"]
        assert result[page_type]["education_text"]
        assert result[page_type]["tourism_text"]
        assert result[page_type]["source_references"]
        assert result[page_type]["review_status"] == "pending"
        assert result[page_type]["publication_allowed"] is False
        assert result[page_type]["human_review_required"] is True


@pytest.mark.parametrize("anchor_slug", PILOT_PLACES)
def test_place_pipeline_preserves_attribution_and_review_queue(anchor_slug: str) -> None:
    result = generate_place_pipeline(anchor_slug)

    for page_type in PAGE_TYPES:
        page = result[page_type]
        queue_item = result["review_queue"][page_type]
        assert NASA_NONENDORSEMENT in page["attribution_block"]
        assert page["source_references"][0]["source_record_id"]
        assert queue_item["review_status"] == "pending"
        assert queue_item["publication_allowed"] is False
        assert queue_item["human_review_required"] is True


@pytest.mark.parametrize("anchor_slug", PILOT_PLACES)
def test_place_pipeline_blocks_prohibited_terms(anchor_slug: str) -> None:
    result = generate_place_pipeline(anchor_slug)
    combined = " ".join(
        str(result[page_type][field])
        for page_type in PAGE_TYPES
        for field in ("hero_text", "story_text", "product_text", "education_text", "tourism_text")
    )

    assert "NARA" not in combined
    assert "Verified by NASA" not in combined
    assert "Moran" not in combined
    assert "Smithsonian" not in combined


def test_place_pipeline_makes_no_external_api_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_network(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("network calls are not allowed in NC-AI-006")

    monkeypatch.setattr(socket, "create_connection", fail_network)
    result = generate_place_pipeline("yellowstone")

    assert result["external_api_calls"] == 0
