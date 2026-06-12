"""Grounded AI page generation for NC-AI-004."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services.ai.earthrise_demo import (
    EARTHRISE_PRODUCT_METADATA,
    NASA_EARTHRISE_ATTRIBUTION,
    NASA_NONENDORSEMENT,
    NASA_SOURCE_RECORD,
)
from services.ai.grounding import GroundingSource, validate_grounding_sources
from services.ai.prompts import stable_hash

CANONICAL_ATTRIBUTION_REGISTRY: dict[str, dict[str, str]] = {
    "earthrise": {
        "source_id": "nasa",
        "source_record_id": "AS08-14-2383",
        "asset_credit": NASA_EARTHRISE_ATTRIBUTION,
        "nonendorsement": NASA_NONENDORSEMENT,
    },
    "yellowstone": {
        "source_id": "nasa",
        "source_record_id": "NC-NASA-026",
        "asset_credit": "NASA: Yellowstone from Orbit. § 105 — public domain.",
        "nonendorsement": NASA_NONENDORSEMENT,
    },
    "grand-canyon": {
        "source_id": "nasa",
        "source_record_id": "NC-NASA-027",
        "asset_credit": "NASA: Grand Canyon from Orbit. § 105 — public domain.",
        "nonendorsement": NASA_NONENDORSEMENT,
    },
    "great-barrier-reef": {
        "source_id": "nasa",
        "source_record_id": "NC-NASA-029",
        "asset_credit": "NASA: Great Barrier Reef satellite view. § 105 — public domain.",
        "nonendorsement": NASA_NONENDORSEMENT,
    },
}

PROHIBITED_PHRASES = (
    "NARA",
    "National Archives",
    "Verified by NASA",
    "NASA-approved",
    "NASA certified",
    "NASA-certified",
    "Moran",
    "Smithsonian",
    "Canaletto",
    "de' Barbari",
    "ESA/Copernicus",
    "Collector's Edition",
)


class PageGenerationError(ValueError):
    """Raised when page generation violates NC-AI-004 policy."""


@dataclass(frozen=True)
class PageGenerationInput:
    page_type: str
    anchor_slug: str
    retrieval_package: dict[str, Any]
    generation_purpose: str


def earthrise_retrieval_package() -> dict[str, Any]:
    return {
        "nasa_source_record": NASA_SOURCE_RECORD,
        "product_metadata": EARTHRISE_PRODUCT_METADATA,
        "attribution": NASA_EARTHRISE_ATTRIBUTION,
        "nonendorsement": NASA_NONENDORSEMENT,
        "source_references": [
            {
                "source_type": "nasa",
                "source_id": "nasa",
                "source_record_id": "AS08-14-2383",
                "title": "Earthrise",
                "url": NASA_SOURCE_RECORD["url"],
                "rights_status": "verified_pd",
            }
        ],
    }


def _grounding_source_from_package(package: dict[str, Any]) -> GroundingSource:
    source_record = package.get("nasa_source_record") or package.get("source_record") or {}
    return GroundingSource(
        source_type="nasa",
        source_id="nasa",
        source_record_id=str(source_record.get("source_record_id") or ""),
        title=str(source_record.get("title") or ""),
        url=source_record.get("url"),
        rights_status=source_record.get("rights_status"),
        allowed_use="product_safe",
        attribution={
            "statement": package.get("nonendorsement"),
            "asset_credit": package.get("attribution"),
            "url": "https://www.nasa.gov",
        },
        evidence={
            "source_record": source_record,
            "product_metadata": package.get("product_metadata") or {},
            "required_attribution": package.get("attribution"),
            "required_nonendorsement": package.get("nonendorsement"),
        },
    )


def validate_prohibited_phrases(page_copy: dict[str, Any]) -> None:
    text = " ".join(str(value) for value in page_copy.values())
    for phrase in PROHIBITED_PHRASES:
        if phrase in text:
            raise PageGenerationError(f"Generated page copy contains prohibited phrase: {phrase}")


def validate_attribution(anchor_slug: str, page_copy: dict[str, Any]) -> None:
    registry = CANONICAL_ATTRIBUTION_REGISTRY.get(anchor_slug)
    if not registry:
        raise PageGenerationError(f"No canonical attribution registry entry for {anchor_slug}")
    attribution_block = str(page_copy.get("attribution_block") or "")
    if registry["asset_credit"] not in attribution_block:
        raise PageGenerationError("NASA attribution is required")
    if registry["nonendorsement"] not in attribution_block:
        raise PageGenerationError("NASA nonendorsement is required")


def generate_grounded_page(payload: PageGenerationInput) -> dict[str, Any]:
    source = _grounding_source_from_package(payload.retrieval_package)
    validate_grounding_sources("public_website_copy", [source], grounding_required=True)
    source_references = payload.retrieval_package.get("source_references")
    if source_references is None:
        source_references = [source.to_reference()]
    if not source_references:
        raise PageGenerationError("page generation requires source references")

    source_record = (
        payload.retrieval_package.get("nasa_source_record")
        or payload.retrieval_package["source_record"]
    )
    product = payload.retrieval_package["product_metadata"]
    attribution = payload.retrieval_package["attribution"]
    nonendorsement = payload.retrieval_package["nonendorsement"]
    attribution_block = f"{attribution}\n{nonendorsement}"

    title = str(source_record.get("title") or product.get("title") or payload.anchor_slug)
    page_label = payload.page_type.replace("_", " ")

    page_copy = {
        "hero_text": title,
        "story_text": (
            f"{title} {page_label} copy is grounded in source record "
            f"{source_record['source_record_id']} and remains subject to human review."
        ),
        "product_text": (
            f"{product['title']} is presented through manual review only, "
            "with source credit and nonendorsement kept visible."
        ),
        "education_text": (
            f"Educational note: {title} is presented as a public-domain United States "
            f"Government Work under {source_record['rights_basis']}."
        ),
        "tourism_text": (
            f"Tourism note: {title} copy is generated as contextual orientation only; "
            "it does not create map-tile, booking, or itinerary claims."
        ),
        "attribution_block": attribution_block,
        "source_references": source_references,
        "review_status": "pending",
        "publication_allowed": False,
        "human_review_required": True,
        "provider": "deterministic-mock-v1",
        "generation_purpose": payload.generation_purpose,
    }
    validate_prohibited_phrases(page_copy)
    validate_attribution(payload.anchor_slug, page_copy)
    return {**page_copy, "page_copy_sha256": stable_hash(page_copy)}
