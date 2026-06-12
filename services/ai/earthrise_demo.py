"""NC-AI-002 Earthrise grounded generation demonstration."""

from __future__ import annotations

from typing import Any

from services.ai.grounding import (
    GroundingSource,
    collect_attribution_requirements,
    validate_grounding_sources,
)
from services.ai.policies import route_decision, route_task_policy
from services.ai.prompts import get_prompt_template, stable_hash
from services.ai.providers.local import DeterministicMockProvider
from services.ai.retrieval import assemble_context

NASA_EARTHRISE_ATTRIBUTION = (
    "NASA: Photograph by William Anders, Apollo 8, December 24, 1968. "
    "§ 105 — public domain."
)
NASA_NONENDORSEMENT = "Image credit: NASA. NASA does not endorse this product."

NASA_SOURCE_RECORD = {
    "source": "nasa",
    "source_record_id": "AS08-14-2383",
    "title": "Earthrise",
    "creator": "William Anders",
    "mission": "Apollo 8",
    "date": "1968-12-24",
    "rights_status": "verified_pd",
    "rights_basis": "17 U.S.C. § 105",
    "url": "https://images.nasa.gov/details-AS08-14-2383",
}

EARTHRISE_PRODUCT_METADATA = {
    "product_codes": ["NC-PROD-001", "NC-PROD-008"],
    "title": "Earthrise",
    "manual_provider_only": True,
    "phase": "Phase 0",
    "purchase_path": "manual_purchase",
    "publication_state": "review_required",
}


def earthrise_grounding_source() -> GroundingSource:
    return GroundingSource(
        source_type="nasa",
        source_id="nasa",
        source_record_id=NASA_SOURCE_RECORD["source_record_id"],
        title=NASA_SOURCE_RECORD["title"],
        url=NASA_SOURCE_RECORD["url"],
        rights_status=NASA_SOURCE_RECORD["rights_status"],
        allowed_use="product_safe",
        attribution={
            "statement": NASA_NONENDORSEMENT,
            "asset_credit": NASA_EARTHRISE_ATTRIBUTION,
            "url": "https://www.nasa.gov",
        },
        evidence={
            "source_record": NASA_SOURCE_RECORD,
            "product_metadata": EARTHRISE_PRODUCT_METADATA,
            "required_attribution": NASA_EARTHRISE_ATTRIBUTION,
            "required_nonendorsement": NASA_NONENDORSEMENT,
        },
    )


def _base_inputs(output_kind: str) -> dict[str, Any]:
    return {
        "output_kind": output_kind,
        "nasa_source_record": NASA_SOURCE_RECORD,
        "product": EARTHRISE_PRODUCT_METADATA,
        "attribution": NASA_EARTHRISE_ATTRIBUTION,
        "nonendorsement": NASA_NONENDORSEMENT,
    }


def _generate(task_type: str, output_kind: str) -> dict[str, Any]:
    sources = [earthrise_grounding_source()]
    inputs = _base_inputs(output_kind)
    policy = route_task_policy(task_type)
    validate_grounding_sources(
        task_type,
        sources,
        grounding_required=policy.grounding_required,
    )
    template = get_prompt_template(task_type)
    rendered_prompt = template.render(inputs, sources)
    context = assemble_context(sources, task_type=task_type, inputs=inputs)
    provider = DeterministicMockProvider()
    provider_output = provider.generate(rendered_prompt, context)
    output_sha256 = stable_hash(provider_output)
    decision = route_decision(task_type)
    audit_event = {
        "event_type": "ai_generation_mocked",
        "actor": "nc-ai-002-demo",
        "task_type": task_type,
        "selected_provider": decision["selected_provider"],
        "execution_provider": provider.provider,
        "output_sha256": output_sha256,
        "external_api_calls": 0,
    }
    return {
        "task_type": task_type,
        "policy": {
            "human_review_required": policy.human_review_required,
            "grounding_required": policy.grounding_required,
            "publication_allowed": policy.publication_allowed_by_default,
            "cite_sources_required": policy.cite_sources_required,
        },
        "route_decision": decision,
        "provider": provider.provider,
        "model_name": provider.model_name,
        "prompt_template": {
            "template_key": template.template_key,
            "template_version": template.template_version,
            "template_sha256": template.template_sha256,
        },
        "prompt_sha256": stable_hash(rendered_prompt),
        "output": provider_output,
        "output_sha256": output_sha256,
        "source_references": context["source_references"],
        "attribution_requirements": collect_attribution_requirements(sources),
        "publication_allowed": False,
        "human_review_required": True,
        "audit_event": audit_event,
        "audit_event_sha256": stable_hash(audit_event),
    }


def _pending_review(result: dict[str, Any], output_kind: str) -> dict[str, Any]:
    review = {
        "review_status": "pending",
        "review_required": True,
        "publication_allowed": False,
        "output_kind": output_kind,
        "checks": {
            "grounding_sources_present": bool(result["source_references"]),
            "attribution_preserved": bool(result["attribution_requirements"]),
            "external_api_calls": result["audit_event"]["external_api_calls"],
            "no_auto_publish": result["publication_allowed"] is False,
        },
    }
    return {**review, "review_sha256": stable_hash(review)}


def _review_for_demo(review: dict[str, Any]) -> dict[str, Any]:
    reviewed = {
        **review,
        "review_status": "approved_for_demo_not_publication",
        "reviewed_by": "nc-ai-002-demo-reviewer",
        "publication_allowed": False,
    }
    return {**reviewed, "review_sha256": stable_hash(reviewed)}


def run_earthrise_demo() -> dict[str, Any]:
    """Run retrieval -> grounding -> generation -> review for Earthrise."""
    generations = {
        "product_description": _generate("product_copy", "product_description"),
        "story_variant": _generate("place_story", "story_variant"),
        "educational_summary": _generate("education_module", "educational_summary"),
    }
    pending_reviews = {
        key: _pending_review(result, key) for key, result in generations.items()
    }
    reviewed = {key: _review_for_demo(review) for key, review in pending_reviews.items()}

    return {
        "demo": "NC-AI-002",
        "provider": "deterministic-mock-v1",
        "external_api_calls": 0,
        "retrieval": {
            "input_records": {
                "nasa_source_record": NASA_SOURCE_RECORD,
                "product_metadata": EARTHRISE_PRODUCT_METADATA,
            },
            "grounding_source_count": 1,
        },
        "grounding": {
            "source_record_id": NASA_SOURCE_RECORD["source_record_id"],
            "rights_status": NASA_SOURCE_RECORD["rights_status"],
            "attribution": NASA_EARTHRISE_ATTRIBUTION,
            "nonendorsement": NASA_NONENDORSEMENT,
        },
        "generation": generations,
        "review_workflow": {
            "pending": pending_reviews,
            "reviewed_for_demo": reviewed,
            "publication_allowed": False,
        },
    }
