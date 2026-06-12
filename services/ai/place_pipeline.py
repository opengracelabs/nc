"""NC-AI-006 deterministic place generation pipeline."""

from __future__ import annotations

from typing import Any

from services.ai.earthrise_demo import NASA_NONENDORSEMENT
from services.ai.page_generation import (
    CANONICAL_ATTRIBUTION_REGISTRY,
    PageGenerationError,
    PageGenerationInput,
    generate_grounded_page,
)
from services.ai.page_review import build_review_queue_item
from services.ai.prompts import stable_hash

PAGE_TYPES = ("homepage", "story", "product", "education", "tourism")

PILOT_PLACE_SOURCE_RECORDS: dict[str, dict[str, str]] = {
    "yellowstone": {
        "title": "Yellowstone",
        "source_record_id": "NC-NASA-026",
        "rights_status": "verified_pd",
        "rights_basis": "17 U.S.C. § 105",
        "url": "https://www.nasa.gov",
        "asset_credit": CANONICAL_ATTRIBUTION_REGISTRY["yellowstone"]["asset_credit"],
        "product_title": "Yellowstone from Orbit",
    },
    "grand-canyon": {
        "title": "Grand Canyon",
        "source_record_id": "NC-NASA-027",
        "rights_status": "verified_pd",
        "rights_basis": "17 U.S.C. § 105",
        "url": "https://www.nasa.gov",
        "asset_credit": CANONICAL_ATTRIBUTION_REGISTRY["grand-canyon"]["asset_credit"],
        "product_title": "Grand Canyon from Orbit",
    },
    "great-barrier-reef": {
        "title": "Great Barrier Reef",
        "source_record_id": "NC-NASA-029",
        "rights_status": "verified_pd",
        "rights_basis": "17 U.S.C. § 105",
        "url": "https://www.nasa.gov",
        "asset_credit": CANONICAL_ATTRIBUTION_REGISTRY["great-barrier-reef"]["asset_credit"],
        "product_title": "Great Barrier Reef Satellite View",
    },
}


def build_place_retrieval_package(anchor_slug: str) -> dict[str, Any]:
    try:
        record = PILOT_PLACE_SOURCE_RECORDS[anchor_slug]
    except KeyError as exc:
        raise PageGenerationError(f"Unsupported pilot place anchor: {anchor_slug}") from exc

    source_record = {
        "source": "nasa",
        "source_record_id": record["source_record_id"],
        "title": record["title"],
        "rights_status": record["rights_status"],
        "rights_basis": record["rights_basis"],
        "url": record["url"],
    }
    return {
        "source_record": source_record,
        "product_metadata": {
            "title": record["product_title"],
            "manual_provider_only": True,
            "publication_state": "review_required",
        },
        "attribution": record["asset_credit"],
        "nonendorsement": NASA_NONENDORSEMENT,
        "source_references": [
            {
                "source_type": "nasa",
                "source_id": "nasa",
                "source_record_id": record["source_record_id"],
                "title": record["title"],
                "url": record["url"],
                "rights_status": record["rights_status"],
            }
        ],
    }


def generate_place_pipeline(anchor_slug: str, actor: str = "nc-ai-006-pipeline") -> dict[str, Any]:
    retrieval_package = build_place_retrieval_package(anchor_slug)
    pages: dict[str, dict[str, Any]] = {}
    review_queue: dict[str, dict[str, Any]] = {}

    for page_type in PAGE_TYPES:
        page = generate_grounded_page(
            PageGenerationInput(
                page_type=page_type,
                anchor_slug=anchor_slug,
                retrieval_package=retrieval_package,
                generation_purpose=f"{anchor_slug}:{page_type}",
            )
        )
        generation_id = stable_hash(
            {"anchor_slug": anchor_slug, "page_type": page_type, "kind": "generation"}
        )
        snapshot_id = stable_hash(
            {
                "anchor_slug": anchor_slug,
                "page_type": page_type,
                "page_copy_sha256": page["page_copy_sha256"],
            }
        )
        pages[page_type] = page
        review_queue[page_type] = build_review_queue_item(
            generation_id,
            snapshot_id,
            actor=actor,
        )

    return {
        "anchor_slug": anchor_slug,
        "provider": "deterministic-mock-v1",
        "external_api_calls": 0,
        "retrieval_package": retrieval_package,
        "homepage": pages["homepage"],
        "story": pages["story"],
        "product": pages["product"],
        "education": pages["education"],
        "tourism": pages["tourism"],
        "review_queue": review_queue,
        "publication_allowed": False,
        "human_review_required": True,
    }
