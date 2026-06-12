"""Review, approval, publication snapshot, and rollback contracts for AI pages."""

from __future__ import annotations

from typing import Any

from services.ai.page_generation import validate_attribution, validate_prohibited_phrases
from services.ai.prompts import stable_hash


class PageReviewError(ValueError):
    """Raised when an AI page review transition is invalid."""


def build_review_queue_item(
    page_generation_id: str,
    snapshot_id: str,
    *,
    actor: str,
) -> dict[str, Any]:
    item = {
        "page_generation_id": page_generation_id,
        "snapshot_id": snapshot_id,
        "review_status": "pending",
        "assigned_to": actor,
        "publication_allowed": False,
        "human_review_required": True,
    }
    return {**item, "queue_item_sha256": stable_hash(item)}


def approve_generation(
    page_generation: dict[str, Any],
    snapshot: dict[str, Any],
    *,
    reviewer: str,
    notes: str | None = None,
) -> dict[str, Any]:
    if not reviewer:
        raise PageReviewError("reviewer is required")
    page_copy = dict(snapshot.get("page_copy") or {})
    anchor_slug = str(page_generation.get("anchor_slug") or "")
    if not page_copy:
        raise PageReviewError("snapshot page_copy is required")
    if not snapshot.get("source_references"):
        raise PageReviewError("snapshot source references are required")

    validate_prohibited_phrases(page_copy)
    validate_attribution(anchor_slug, page_copy)

    approved = {
        "event_type": "approved_generation",
        "page_generation_id": str(page_generation["id"]),
        "snapshot_id": str(snapshot["id"]),
        "page_type": page_generation["page_type"],
        "anchor_slug": anchor_slug,
        "review_status": "approved",
        "publication_allowed": True,
        "human_review_required": True,
        "reviewed_by": reviewer,
        "notes": notes,
        "page_copy_sha256": snapshot["page_copy_sha256"],
        "source_references": snapshot["source_references"],
    }
    return {**approved, "event_sha256": stable_hash(approved)}


def rollback_generation(
    page_generation: dict[str, Any],
    current_publication: dict[str, Any],
    target_snapshot: dict[str, Any],
    *,
    actor: str,
    reason: str,
) -> dict[str, Any]:
    if not actor:
        raise PageReviewError("rollback actor is required")
    if not reason:
        raise PageReviewError("rollback reason is required")
    page_copy = dict(target_snapshot.get("page_copy") or {})
    anchor_slug = str(page_generation.get("anchor_slug") or "")
    if not page_copy:
        raise PageReviewError("target snapshot page_copy is required")

    validate_prohibited_phrases(page_copy)
    validate_attribution(anchor_slug, page_copy)

    rollback = {
        "event_type": "rollback_generation",
        "page_generation_id": str(page_generation["id"]),
        "from_publication_snapshot_id": str(current_publication["id"]),
        "target_snapshot_id": str(target_snapshot["id"]),
        "page_type": page_generation["page_type"],
        "anchor_slug": anchor_slug,
        "review_status": "approved",
        "publication_allowed": True,
        "human_review_required": True,
        "rolled_back_by": actor,
        "reason": reason,
        "page_copy_sha256": target_snapshot["page_copy_sha256"],
    }
    return {**rollback, "event_sha256": stable_hash(rollback)}
