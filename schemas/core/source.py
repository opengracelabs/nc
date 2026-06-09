from enum import StrEnum
from typing import Any

from pydantic import Field

from .base import NCBase, NCRecord


class FetchStrategy(StrEnum):
    API = "api"           # structured REST or SPARQL endpoint
    FILE = "file"         # binary file download
    SCRAPE = "scrape"     # HTML scrape (last resort)


class AuthType(StrEnum):
    NONE = "none"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"


class SourceStatus(StrEnum):
    ACTIVE = "active"
    DEGRADED = "degraded"       # reachable but returning errors or partial data
    UNAVAILABLE = "unavailable"
    DEPRECATED = "deprecated"   # replaced by another source


class GovernanceState(StrEnum):
    PROPOSED   = "proposed"    # registered, under review, no ingestion permitted
    APPROVED   = "approved"    # human-approved, adapter in development
    ACTIVE     = "active"      # adapter validated, ingestion permitted
    SUSPENDED  = "suspended"   # temporarily halted, rights or legal review
    DEPRECATED = "deprecated"  # replaced, no new ingestion
    RETIRED    = "retired"     # permanently removed from pipeline


class CommercialStatus(StrEnum):
    UNRESTRICTED = "unrestricted"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"


class OperationalStatus(StrEnum):
    HEALTHY     = "healthy"     # last fetch succeeded within expected window
    DEGRADED    = "degraded"    # reachable but returning errors or partial data
    UNAVAILABLE = "unavailable" # unreachable or no fetch attempted yet


class RateLimit(NCBase):  # NCBase
    requests_per_second: float = 1.0
    burst: int = 5
    retry_max: int = 3
    retry_backoff: str = "exponential"   # "exponential" | "fixed"
    timeout_seconds: int = 30


class Source(NCRecord):
    """Registered external data source."""

    # Identity
    source_id: str                          # slug: "unesco_whc", "wikidata", "osm"
    name: str
    description: str | None = None
    institution: str | None = None          # "UNESCO", "Wikimedia Foundation", etc.

    # Access
    base_url: str
    fetch_strategy: FetchStrategy
    auth_type: AuthType = AuthType.NONE
    rate_limit: RateLimit = Field(default_factory=RateLimit)

    # Coverage
    entity_types: list[str] = Field(default_factory=list)  # ["site", "occurrence"]
    coverage_notes: str | None = None

    # Standards
    standards: list[str] = Field(default_factory=list)     # e.g. ["darwin_core", "prov_o"]

    # Governance (human-managed lifecycle)
    governance_state: GovernanceState = GovernanceState.PROPOSED
    # Operational health (system-monitored)
    operational_status: OperationalStatus = OperationalStatus.UNAVAILABLE
    commercial_status: CommercialStatus = CommercialStatus.UNKNOWN
    # Legacy status field — kept for backward compatibility; governance_state supersedes it
    status: SourceStatus = SourceStatus.ACTIVE
    last_fetched_at: str | None = None      # ISO 8601
    last_error: str | None = None

    # Schema pinning
    schema_version: str | None = None      # e.g. "v2"
    schema_path: str | None = None         # "schemas/core/sources/unesco_whc_v2.json"

    # Priority in source hierarchy (lower = higher priority)
    priority: int = 99

    # Additional config passed through to the fetch client
    config: dict[str, Any] = Field(default_factory=dict)
