import pytest

from services.ai.page_generation import (
    PageGenerationInput,
    earthrise_retrieval_package,
    generate_grounded_page,
)
from services.ai.page_review import (
    PageReviewError,
    approve_generation,
    build_review_queue_item,
    rollback_generation,
)
from services.api.main import app


def _generation() -> dict:
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "page_type": "story",
        "anchor_slug": "earthrise",
    }


def _snapshot(snapshot_id: str = "00000000-0000-0000-0000-000000000002") -> dict:
    page = generate_grounded_page(
        PageGenerationInput(
            page_type="story",
            anchor_slug="earthrise",
            retrieval_package=earthrise_retrieval_package(),
            generation_purpose="unit-test",
        )
    )
    return {
        "id": snapshot_id,
        "page_copy": page,
        "page_copy_sha256": page["page_copy_sha256"],
        "attribution_block": page["attribution_block"],
        "source_references": page["source_references"],
    }


def test_ai_page_review_routes_are_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/ai/page-review-queue" in paths
    assert "/ai/page-generation/{generation_id}/approve" in paths
    assert "/ai/page-generation/{generation_id}/rollback" in paths
    assert "/ai/page-generation/{generation_id}/history" in paths


def test_review_queue_item_defaults_pending_and_unpublished() -> None:
    item = build_review_queue_item("generation-1", "snapshot-1", actor="reviewer")

    assert item["review_status"] == "pending"
    assert item["publication_allowed"] is False
    assert item["human_review_required"] is True
    assert len(item["queue_item_sha256"]) == 64


def test_approve_generation_marks_publication_allowed_after_review() -> None:
    approved = approve_generation(_generation(), _snapshot(), reviewer="human-reviewer")

    assert approved["event_type"] == "approved_generation"
    assert approved["review_status"] == "approved"
    assert approved["publication_allowed"] is True
    assert approved["human_review_required"] is True
    assert approved["reviewed_by"] == "human-reviewer"
    assert len(approved["event_sha256"]) == 64


def test_approve_generation_rejects_missing_reviewer() -> None:
    with pytest.raises(PageReviewError):
        approve_generation(_generation(), _snapshot(), reviewer="")


def test_rollback_generation_restores_target_snapshot() -> None:
    target = _snapshot("00000000-0000-0000-0000-000000000003")
    current = {"id": "00000000-0000-0000-0000-000000000004"}

    rollback = rollback_generation(
        _generation(),
        current,
        target,
        actor="human-reviewer",
        reason="restore prior approved copy",
    )

    assert rollback["event_type"] == "rollback_generation"
    assert rollback["publication_allowed"] is True
    assert rollback["target_snapshot_id"] == target["id"]
    assert rollback["from_publication_snapshot_id"] == current["id"]
    assert len(rollback["event_sha256"]) == 64


def test_rollback_generation_requires_reason() -> None:
    with pytest.raises(PageReviewError):
        rollback_generation(
            _generation(), {"id": "current"}, _snapshot(), actor="reviewer", reason=""
        )
