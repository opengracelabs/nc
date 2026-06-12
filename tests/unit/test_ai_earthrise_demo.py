from services.ai.earthrise_demo import (
    NASA_NONENDORSEMENT,
    NASA_SOURCE_RECORD,
    run_earthrise_demo,
)
from services.api.main import app


def test_earthrise_demo_route_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/ai/demos/earthrise" in paths


def test_earthrise_demo_generates_three_grounded_outputs() -> None:
    demo = run_earthrise_demo()

    assert demo["demo"] == "NC-AI-002"
    assert demo["provider"] == "deterministic-mock-v1"
    assert set(demo["generation"]) == {
        "product_description",
        "story_variant",
        "educational_summary",
    }
    assert demo["retrieval"]["grounding_source_count"] == 1
    assert demo["grounding"]["source_record_id"] == NASA_SOURCE_RECORD["source_record_id"]


def test_earthrise_demo_preserves_attribution_and_nonendorsement() -> None:
    demo = run_earthrise_demo()

    for result in demo["generation"].values():
        statements = {item["statement"] for item in result["attribution_requirements"]}
        assert NASA_NONENDORSEMENT in statements
        assert result["source_references"][0]["source_record_id"] == "AS08-14-2383"
        assert result["publication_allowed"] is False
        assert "NARA" not in result["output"]["text"]
        assert "Verified by NASA" not in result["output"]["text"]


def test_earthrise_demo_review_workflow_does_not_publish() -> None:
    demo = run_earthrise_demo()
    review = demo["review_workflow"]

    assert review["publication_allowed"] is False
    for pending in review["pending"].values():
        assert pending["review_status"] == "pending"
        assert pending["checks"]["external_api_calls"] == 0
        assert pending["checks"]["no_auto_publish"] is True
    for reviewed in review["reviewed_for_demo"].values():
        assert reviewed["review_status"] == "approved_for_demo_not_publication"
        assert reviewed["publication_allowed"] is False
