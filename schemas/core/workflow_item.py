from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import Field

from .base import NCRecord


class Capability(StrEnum):
    DISCOVERY = "discovery"
    INGESTION = "ingestion"
    PRESERVATION = "preservation"
    KNOWLEDGE_MODELING = "knowledge_modeling"
    SEARCH = "search"
    INTELLIGENCE = "intelligence"
    RESEARCH = "research"
    TRANSLATION = "translation"
    PUBLISHING = "publishing"
    PRODUCT_GENERATION = "product_generation"
    GOVERNANCE = "governance"


class WorkflowStatus(StrEnum):
    PENDING = "pending"           # waiting for worker or human
    IN_PROGRESS = "in_progress"   # worker actively processing
    AWAITING_REVIEW = "awaiting_review"  # worker done, human must act
    APPROVED = "approved"         # human approved; ready to promote/activate
    REJECTED = "rejected"         # human rejected
    FLAGGED = "flagged"           # needs attention before proceeding
    COMPLETED = "completed"       # terminal success
    FAILED = "failed"             # terminal failure
    CANCELLED = "cancelled"       # explicitly cancelled


class RejectionReason(StrEnum):
    DUPLICATE = "duplicate"
    OUT_OF_SCOPE = "out_of_scope"
    DATA_QUALITY = "data_quality"
    POLICY = "policy"
    SENSITIVITY = "sensitivity"
    OTHER = "other"


class WorkflowItem(NCRecord):
    """
    A unit of work moving through the pipeline.
    One item per entity per capability transition.
    PostgreSQL is the sole authority for workflow state.
    """

    # What this item is about
    capability: Capability
    entity_type: str                    # "place", "asset", "ingested_record", etc.
    entity_id: UUID

    # Lineage — the item that caused this one to be created
    parent_item_id: UUID | None = None

    # Queue
    priority: int = 50                  # 0 = highest, 99 = lowest
    scheduled_at: str | None = None     # ISO 8601; None = immediate

    # Status
    status: WorkflowStatus = WorkflowStatus.PENDING
    status_reason: str | None = None    # free text for failed / flagged

    # Worker execution
    worker_id: str | None = None        # identity of the worker that claimed this item
    started_at: str | None = None       # ISO 8601
    completed_at: str | None = None     # ISO 8601
    attempt: int = 1
    max_attempts: int = 3
    last_error: str | None = None

    # Human review
    reviewed_by: str | None = None      # human identity
    reviewed_at: str | None = None      # ISO 8601
    rejection_reason: RejectionReason | None = None
    review_notes: str | None = None

    # Agent advisory output attached to this item
    agent_suggestions: dict[str, Any] = Field(default_factory=dict)

    # Arbitrary metadata for the capability (source-specific run config, etc.)
    context: dict[str, Any] = Field(default_factory=dict)
