"""Grounding contracts for AI generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class GroundingError(ValueError):
    """Raised when generation evidence violates NC-AI-001 policy."""


@dataclass(frozen=True)
class GroundingSource:
    source_type: str
    source_id: str
    source_record_id: str
    title: str
    evidence: dict[str, Any]
    attribution: dict[str, Any]
    url: str | None = None
    rights_status: str | None = None
    allowed_use: str = "grounding"
    provenance: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> GroundingSource:
        return cls(
            source_type=str(payload.get("source_type") or payload.get("source") or ""),
            source_id=str(payload.get("source_id") or ""),
            source_record_id=str(payload.get("source_record_id") or ""),
            title=str(payload.get("title") or ""),
            url=payload.get("url"),
            rights_status=payload.get("rights_status"),
            attribution=dict(payload.get("attribution") or {}),
            evidence=dict(payload.get("evidence") or {}),
            allowed_use=str(payload.get("allowed_use") or "grounding"),
            provenance=dict(payload.get("provenance") or {}),
        )

    def to_reference(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "source_id": self.source_id,
            "source_record_id": self.source_record_id,
            "title": self.title,
            "url": self.url,
            "rights_status": self.rights_status,
            "allowed_use": self.allowed_use,
        }


RIGHTS_REQUIRED_TASKS = {
    "rights_governance",
    "product_copy",
    "public_website_copy",
}


def _contains_media_reference(value: dict[str, Any]) -> bool:
    encoded = repr(value).lower()
    return any(token in encoded for token in ("media", "image", "identifier", "thumbnail"))


def validate_grounding_sources(
    task_type: str,
    sources: list[GroundingSource],
    *,
    grounding_required: bool,
) -> None:
    if grounding_required and not sources:
        raise GroundingError("generation requires grounding evidence")

    for source in sources:
        missing = [
            field_name
            for field_name in ("source_type", "source_id", "source_record_id", "title")
            if not getattr(source, field_name)
        ]
        if missing:
            raise GroundingError(f"grounding source missing required fields: {', '.join(missing)}")
        if not source.evidence:
            raise GroundingError("grounding source requires evidence")
        if not source.attribution:
            raise GroundingError("grounding source requires attribution requirements")
        if task_type in RIGHTS_REQUIRED_TASKS and not source.rights_status:
            raise GroundingError("rights-governed generation requires rights_status")
        if source.source_type == "gbif" and _contains_media_reference(source.evidence):
            raise GroundingError("GBIF media may not be used")
        if (
            source.source_type == "wikidata"
            and source.allowed_use == "product_safe"
            and "commons" in repr(source.evidence).lower()
        ):
            raise GroundingError("Wikidata Commons media may not be product-safe evidence")
        if source.source_type == "osm" and source.allowed_use != "display_reference":
            raise GroundingError("OSM data is allowed only under display-reference policy")


def collect_attribution_requirements(sources: list[GroundingSource]) -> list[dict[str, Any]]:
    requirements: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for source in sources:
        statement = str(source.attribution.get("statement") or "")
        key = (source.source_id, statement)
        if key in seen:
            continue
        seen.add(key)
        requirements.append(
            {
                "source_id": source.source_id,
                "source_record_id": source.source_record_id,
                "statement": statement,
                "url": source.attribution.get("url") or source.url,
                "license": source.attribution.get("license"),
            }
        )
    return requirements
