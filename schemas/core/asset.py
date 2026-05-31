from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import Field

from .base import NCRecord


class AssetType(StrEnum):
    # Descriptive
    SITE_RECORD = "site_record"
    OUV_STATEMENT = "ouv_statement"
    NOMINATION_DOSSIER = "nomination_dossier"
    DESCRIPTION = "description"
    BIBLIOGRAPHY = "bibliography"

    # Spatial
    BOUNDARY = "boundary"
    CENTROID = "centroid"

    # Media
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

    # Scientific
    OCCURRENCE_RECORD = "occurrence_record"
    SPECIES_LIST = "species_list"

    # Administrative
    DECISION_DOCUMENT = "decision_document"
    STATE_OF_CONSERVATION = "state_of_conservation"

    UNKNOWN = "unknown"


class AssetStatus(StrEnum):
    FETCHED = "fetched"           # raw stored, not yet validated
    VALID = "valid"               # passed validation
    NORMALIZED = "normalized"     # normalized artifact written
    ACTIVE = "active"             # in use by downstream capabilities
    QUARANTINED = "quarantined"   # failed validation or sensitivity flag
    SUPERSEDED = "superseded"     # replaced by a newer ingest
    MISSING = "missing"           # HTTP 404 at source


class Asset(NCRecord):
    """A stored artifact — raw or normalized — for a Place."""

    # Ownership
    place_id: UUID
    source_id: str                  # FK → Source.source_id
    ingest_id: str                  # ingestion run that produced this asset

    # Classification
    asset_type: AssetType = AssetType.UNKNOWN
    mime_type: str | None = None    # e.g. "application/json", "image/jpeg"
    language: str | None = None     # ISO 639-1; None = language-neutral

    # Storage — MinIO paths
    raw_path: str | None = None         # raw/ingestion/{place_id}/{ingest_id}/{name}
    normalized_path: str | None = None  # normalized/ingestion/{place_id}/{ingest_id}/{name}

    # Integrity
    checksum_sha256: str | None = None
    size_bytes: int | None = None

    # PREMIS preservation fields
    premis_object_id: str | None = None
    premis_original_name: str | None = None
    premis_creating_application: str | None = None

    # Status
    status: AssetStatus = AssetStatus.FETCHED

    # Validation
    validation_warnings: list[str] = Field(default_factory=list)
    schema_version: str | None = None   # pinned schema version used for normalization

    # Agent advisory
    agent_notes: dict[str, Any] = Field(default_factory=dict)

    # Source URL at time of fetch (for provenance)
    source_url: str | None = None
    fetched_at: str | None = None       # ISO 8601
