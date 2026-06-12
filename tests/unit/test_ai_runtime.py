import inspect
import socket

import pytest
from fastapi import HTTPException

from services.ai import router
from services.ai.policies import route_task_policy
from services.ai.prompts import get_prompt_template
from services.ai.providers import get_provider_class
from services.ai.providers.claude import ClaudeProvider
from services.ai.providers.openai import CodexProvider, OpenAIProvider
from services.api.main import app


def _earthrise_source() -> router.GroundingSourcePayload:
    return router.GroundingSourcePayload(
        source_type="nasa",
        source_id="nasa",
        source_record_id="AS08-14-2383",
        title="Earthrise",
        url="https://images.nasa.gov/details-AS08-14-2383",
        rights_status="verified_pd",
        allowed_use="product_safe",
        attribution={
            "statement": "Image credit: NASA. NASA does not endorse this product.",
            "url": "https://www.nasa.gov",
        },
        evidence={
            "rights_basis": "17 U.S.C. § 105",
            "human_verified": True,
            "source_record": "AS08-14-2383",
        },
    )


def test_ai_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/ai/models" in paths
    assert "/ai/tasks" in paths
    assert "/ai/generate" in paths
    assert "/ai/generate/place-story" in paths
    assert "/ai/generate/product-copy" in paths
    assert "/ai/generate/education-module" in paths
    assert "/ai/requests/{request_id}" in paths
    assert "/ai/audit-events" in paths


def test_model_router_selects_correct_provider_class_by_task() -> None:
    rights_policy = route_task_policy("rights_governance")
    product_policy = route_task_policy("product_copy")
    code_policy = route_task_policy("code_generation")

    assert get_provider_class(rights_policy.default_provider) is ClaudeProvider
    assert get_provider_class(product_policy.default_provider) is OpenAIProvider
    assert get_provider_class(code_policy.default_provider) is CodexProvider


def test_rights_task_cannot_auto_publish() -> None:
    policy = route_task_policy("rights_governance")

    assert policy.human_review_required is True
    assert policy.publication_allowed_by_default is False


def test_product_copy_requires_grounding_sources() -> None:
    payload = router.GenerateRequest(task_type="product_copy", actor="unit-test")

    with pytest.raises(HTTPException) as exc:
        router.generate_advisory_content(payload)

    assert exc.value.status_code == 422
    assert "grounding evidence" in str(exc.value.detail)


def test_generation_without_evidence_is_rejected() -> None:
    source = _earthrise_source().model_copy(update={"evidence": {}})
    payload = router.GenerateRequest(
        task_type="product_copy",
        actor="unit-test",
        grounding_sources=[source],
    )

    with pytest.raises(HTTPException) as exc:
        router.generate_advisory_content(payload)

    assert exc.value.status_code == 422
    assert "requires evidence" in str(exc.value.detail)


def test_mock_provider_output_records_audit_event() -> None:
    payload = router.GenerateRequest(
        task_type="product_copy",
        actor="unit-test",
        inputs={"subject": "Earthrise"},
        grounding_sources=[_earthrise_source()],
    )

    result = router.generate_advisory_content(payload)

    assert result["provider"] == "local"
    assert result["model_name"] == "deterministic-mock-v1"
    assert result["audit_event"]["event_type"] == "ai_generation_mocked"
    assert result["audit_event"]["external_api_calls"] == 0
    assert result["publication_allowed"] is False
    assert result["human_review_required"] is True


def test_prompt_template_versioning_is_deterministic() -> None:
    first = get_prompt_template("product_copy")
    second = get_prompt_template("product_copy")

    assert first.template_key == "product_copy_v1"
    assert first.template_version == "1"
    assert first.template_sha256 == second.template_sha256
    assert len(first.template_sha256) == 64


def test_no_external_api_calls_in_generation(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_network(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("network calls are not allowed in NC-AI-001 Sprint 1 tests")

    monkeypatch.setattr(socket, "create_connection", fail_network)
    payload = router.GenerateRequest(
        task_type="place_story",
        actor="unit-test",
        inputs={"subject": "Earthrise"},
        grounding_sources=[_earthrise_source()],
    )

    result = router.generate_advisory_content(payload)

    assert result["audit_event"]["external_api_calls"] == 0


def test_all_outputs_preserve_attribution_requirements() -> None:
    payload = router.GenerateRequest(
        task_type="product_copy",
        actor="unit-test",
        inputs={"subject": "Earthrise"},
        grounding_sources=[_earthrise_source()],
    )

    result = router.generate_advisory_content(payload)

    statements = {item["statement"] for item in result["attribution_requirements"]}
    assert "Image credit: NASA. NASA does not endorse this product." in statements
    assert result["source_references"][0]["source_record_id"] == "AS08-14-2383"


def test_provider_stubs_do_not_import_http_clients() -> None:
    import services.ai.providers.claude as claude
    import services.ai.providers.gemini as gemini
    import services.ai.providers.local as local
    import services.ai.providers.openai as openai

    source = "\n".join(
        inspect.getsource(module) for module in (claude, gemini, local, openai)
    )

    assert "httpx" not in source
    assert "import requests" not in source
