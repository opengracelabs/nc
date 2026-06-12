import socket

import pytest

from services.ai.earthrise_demo import NASA_NONENDORSEMENT
from services.ai.page_generation import (
    PageGenerationError,
    PageGenerationInput,
    earthrise_retrieval_package,
    generate_grounded_page,
    validate_prohibited_phrases,
)
from services.api.main import app


def _earthrise_input(
    retrieval_package: dict | None = None,
    anchor_slug: str = "earthrise",
) -> PageGenerationInput:
    return PageGenerationInput(
        page_type="story",
        anchor_slug=anchor_slug,
        retrieval_package=retrieval_package or earthrise_retrieval_package(),
        generation_purpose="public_story_page",
    )


def test_ai_page_generation_routes_are_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/ai/page-generation" in paths
    assert "/ai/page-generation/{page_type}/{anchor_slug}" in paths


def test_earthrise_generated_page_copy_preserves_nasa_attribution() -> None:
    page = generate_grounded_page(_earthrise_input())

    assert "NASA: Photograph by William Anders" in page["attribution_block"]
    assert NASA_NONENDORSEMENT in page["attribution_block"]
    assert page["source_references"][0]["source_record_id"] == "AS08-14-2383"


def test_earthrise_generated_page_copy_blocks_nara() -> None:
    with pytest.raises(PageGenerationError):
        validate_prohibited_phrases({"story_text": "NARA source copy"})


def test_earthrise_generated_page_copy_blocks_verified_by_nasa() -> None:
    with pytest.raises(PageGenerationError):
        validate_prohibited_phrases({"story_text": "Verified by NASA"})


def test_page_generation_requires_source_references() -> None:
    package = earthrise_retrieval_package()
    package["source_references"] = []

    with pytest.raises(PageGenerationError) as exc:
        generate_grounded_page(_earthrise_input(package))

    assert "source references" in str(exc.value)


def test_page_generation_requires_human_review() -> None:
    page = generate_grounded_page(_earthrise_input())

    assert page["review_status"] == "pending"
    assert page["human_review_required"] is True
    assert page["publication_allowed"] is False


def test_page_generation_no_external_api_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_network(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("network calls are not allowed in NC-AI-004")

    monkeypatch.setattr(socket, "create_connection", fail_network)
    page = generate_grounded_page(_earthrise_input())

    assert page["provider"] == "deterministic-mock-v1"
    assert page["publication_allowed"] is False
