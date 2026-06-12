"""FastAPI router for NC-AI-001."""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.ai.grounding import (
    GroundingError,
    GroundingSource,
    collect_attribution_requirements,
    validate_grounding_sources,
)
from services.ai.policies import TASK_POLICIES, PolicyError, route_decision, route_task_policy
from services.ai.prompts import get_prompt_template, stable_hash
from services.ai.providers import PROVIDER_CLASSES
from services.ai.providers.local import DeterministicMockProvider
from services.ai.retrieval import assemble_context
from services.api.dependencies import DB, Auth

router = APIRouter(prefix="/ai", tags=["ai"])


class GroundingSourcePayload(BaseModel):
    source_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_record_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    evidence: dict[str, Any]
    attribution: dict[str, Any]
    url: str | None = None
    rights_status: str | None = None
    allowed_use: str = "grounding"
    provenance: dict[str, Any] = Field(default_factory=dict)


class GenerateRequest(BaseModel):
    task_type: str = Field(min_length=1)
    actor: str = Field(min_length=1)
    inputs: dict[str, Any] = Field(default_factory=dict)
    grounding_sources: list[GroundingSourcePayload] = Field(default_factory=list)


class PageGenerationRequest(BaseModel):
    page_type: str = Field(min_length=1)
    anchor_slug: str = Field(min_length=1)
    retrieval_package: dict[str, Any]
    generation_purpose: str = Field(min_length=1)
    actor: str = Field(min_length=1)


class PageGenerationApprovalRequest(BaseModel):
    reviewer: str = Field(min_length=1)
    notes: str | None = None


class PageGenerationRollbackRequest(BaseModel):
    target_snapshot_id: UUID
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)


def model_registry() -> list[dict[str, Any]]:
    return [
        {
            "provider": provider,
            "class_name": provider_class.__name__,
            "model_name": getattr(provider_class, "model_name", f"{provider}-stub"),
            "external_calls_allowed": False,
        }
        for provider, provider_class in sorted(PROVIDER_CLASSES.items())
    ]


def task_registry() -> list[dict[str, Any]]:
    return [
        {
            "task_type": policy.task_type,
            "provider_policy": policy.provider_policy,
            "default_provider": policy.default_provider,
            "default_model": policy.default_model,
            "human_review_required": policy.human_review_required,
            "grounding_required": policy.grounding_required,
            "publication_allowed_by_default": policy.publication_allowed_by_default,
            "cite_sources_required": policy.cite_sources_required,
        }
        for policy in TASK_POLICIES.values()
    ]


def generate_advisory_content(payload: GenerateRequest) -> dict[str, Any]:
    try:
        policy = route_task_policy(payload.task_type)
    except PolicyError as exc:
        raise HTTPException(422, str(exc)) from exc

    sources = [GroundingSource.from_dict(item.model_dump()) for item in payload.grounding_sources]
    try:
        validate_grounding_sources(
            payload.task_type,
            sources,
            grounding_required=policy.grounding_required,
        )
    except GroundingError as exc:
        raise HTTPException(422, str(exc)) from exc

    template = get_prompt_template(payload.task_type)
    rendered_prompt = template.render(payload.inputs, sources)
    context = assemble_context(sources, task_type=payload.task_type, inputs=payload.inputs)
    provider = DeterministicMockProvider()
    provider_output = provider.generate(rendered_prompt, context)
    output_sha256 = stable_hash(provider_output)
    attribution = collect_attribution_requirements(sources)
    decision = route_decision(payload.task_type)
    audit_event = {
        "event_type": "ai_generation_mocked",
        "actor": payload.actor,
        "task_type": payload.task_type,
        "selected_provider": decision["selected_provider"],
        "execution_provider": provider.provider,
        "output_sha256": output_sha256,
        "external_api_calls": 0,
    }

    return {
        "task_type": payload.task_type,
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
        "attribution_requirements": attribution,
        "publication_allowed": False,
        "human_review_required": True,
        "audit_event": audit_event,
        "audit_event_sha256": stable_hash(audit_event),
    }


async def _persist_generation(conn: DB, payload: GenerateRequest, result: dict[str, Any]) -> dict:
    request_row = await conn.fetchrow(
        """
        INSERT INTO ai_generation_request (
            task_type, requested_by, request_payload, grounding_required,
            human_review_required, status, provenance
        )
        VALUES ($1, $2, $3::jsonb, $4, $5, 'generated', $6::jsonb)
        RETURNING id
        """,
        payload.task_type,
        payload.actor,
        json.dumps(payload.model_dump(mode="json")),
        result["policy"]["grounding_required"],
        result["human_review_required"],
        json.dumps({"authority": "NC-AI-001", "sprint": "1"}),
    )
    request_id = request_row["id"]

    for source in payload.grounding_sources:
        await conn.execute(
            """
            INSERT INTO ai_grounding_source (
                generation_request_id, source_type, source_id, source_record_id, title,
                url, rights_status, attribution, evidence, allowed_use, provenance
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9::jsonb, $10, $11::jsonb)
            """,
            request_id,
            source.source_type,
            source.source_id,
            source.source_record_id,
            source.title,
            source.url,
            source.rights_status,
            json.dumps(source.attribution),
            json.dumps(source.evidence),
            source.allowed_use,
            json.dumps(source.provenance),
        )

    await conn.execute(
        """
        INSERT INTO ai_model_route_decision (
            generation_request_id, task_type, selected_provider, selected_model,
            execution_provider, decision
        )
        VALUES ($1, $2, $3, $4, $5, $6::jsonb)
        """,
        request_id,
        payload.task_type,
        result["route_decision"]["selected_provider"],
        result["route_decision"]["selected_model"],
        result["route_decision"]["execution_provider"],
        json.dumps(result["route_decision"]),
    )

    result_row = await conn.fetchrow(
        """
        INSERT INTO ai_generation_result (
            generation_request_id, provider, model_name, prompt_sha256, output,
            output_sha256, source_references, attribution_requirements,
            publication_allowed, human_review_required, provenance
        )
        VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7::jsonb, $8::jsonb, FALSE, TRUE, $9::jsonb)
        RETURNING id
        """,
        request_id,
        result["provider"],
        result["model_name"],
        result["prompt_sha256"],
        json.dumps(result["output"]),
        result["output_sha256"],
        json.dumps(result["source_references"]),
        json.dumps(result["attribution_requirements"]),
        json.dumps({"authority": "NC-AI-001", "provider_policy_recorded": True}),
    )
    result_id = result_row["id"]

    await conn.execute(
        """
        INSERT INTO ai_human_review (generation_result_id, review_status, provenance)
        VALUES ($1, 'pending', $2::jsonb)
        """,
        result_id,
        json.dumps({"authority": "NC-AI-001", "auto_publish": False}),
    )

    await conn.execute(
        """
        INSERT INTO ai_audit_event (
            generation_request_id, generation_result_id, event_type, actor, event, event_sha256
        )
        VALUES ($1, $2, $3, $4, $5::jsonb, $6)
        ON CONFLICT (event_sha256) DO NOTHING
        """,
        request_id,
        result_id,
        result["audit_event"]["event_type"],
        payload.actor,
        json.dumps(result["audit_event"]),
        result["audit_event_sha256"],
    )

    return {"request_id": str(request_id), "result_id": str(result_id), **result}


@router.get("/models")
async def list_ai_models(auth: Auth) -> list[dict[str, Any]]:
    return model_registry()


@router.get("/tasks")
async def list_ai_tasks(auth: Auth) -> list[dict[str, Any]]:
    return task_registry()


@router.post("/generate")
async def generate(payload: GenerateRequest, auth: Auth, conn: DB) -> dict:
    result = generate_advisory_content(payload)
    return await _persist_generation(conn, payload, result)


@router.post("/generate/place-story")
async def generate_place_story(payload: GenerateRequest, auth: Auth, conn: DB) -> dict:
    scoped = payload.model_copy(update={"task_type": "place_story"})
    result = generate_advisory_content(scoped)
    return await _persist_generation(conn, scoped, result)


@router.post("/generate/product-copy")
async def generate_product_copy(payload: GenerateRequest, auth: Auth, conn: DB) -> dict:
    scoped = payload.model_copy(update={"task_type": "product_copy"})
    result = generate_advisory_content(scoped)
    return await _persist_generation(conn, scoped, result)


@router.post("/generate/education-module")
async def generate_education_module(payload: GenerateRequest, auth: Auth, conn: DB) -> dict:
    scoped = payload.model_copy(update={"task_type": "education_module"})
    result = generate_advisory_content(scoped)
    return await _persist_generation(conn, scoped, result)



@router.post("/page-generation")
async def generate_page_copy(payload: PageGenerationRequest, auth: Auth, conn: DB) -> dict:
    from services.ai.page_generation import (
        PageGenerationError,
        PageGenerationInput,
        generate_grounded_page,
    )

    try:
        page_copy = generate_grounded_page(
            PageGenerationInput(
                page_type=payload.page_type,
                anchor_slug=payload.anchor_slug,
                retrieval_package=payload.retrieval_package,
                generation_purpose=payload.generation_purpose,
            )
        )
    except PageGenerationError as exc:
        raise HTTPException(422, str(exc)) from exc

    generation_row = await conn.fetchrow(
        """
        INSERT INTO ai_page_generation (
            page_type, anchor_slug, generation_purpose, retrieval_package,
            source_references, provider, review_status, publication_allowed,
            human_review_required, provenance
        )
        VALUES ($1, $2, $3, $4::jsonb, $5::jsonb, $6, $7, FALSE, TRUE, $8::jsonb)
        RETURNING id
        """,
        payload.page_type,
        payload.anchor_slug,
        payload.generation_purpose,
        json.dumps(payload.retrieval_package),
        json.dumps(page_copy["source_references"]),
        page_copy["provider"],
        page_copy["review_status"],
        json.dumps({"authority": "NC-AI-004", "actor": payload.actor}),
    )
    generation_id = generation_row["id"]
    snapshot_row = await conn.fetchrow(
        """
        INSERT INTO ai_page_generation_snapshot (
            page_generation_id, snapshot_version, page_copy, page_copy_sha256,
            attribution_block, source_references, review_status, publication_allowed,
            human_review_required, generated_by
        )
        VALUES ($1, $2, $3::jsonb, $4, $5, $6::jsonb, $7, FALSE, TRUE, $8)
        RETURNING id
        """,
        generation_id,
        "nc-ai-004-v1",
        json.dumps(page_copy),
        page_copy["page_copy_sha256"],
        page_copy["attribution_block"],
        json.dumps(page_copy["source_references"]),
        page_copy["review_status"],
        payload.actor,
    )
    return await _queue_page_generation_response(
        conn, generation_id, snapshot_row["id"], payload.actor, page_copy
    )


@router.get("/page-generation/{page_type}/{anchor_slug}")
async def get_reviewed_page_copy(
    page_type: str, anchor_slug: str, auth: Auth, conn: DB
) -> dict:
    row = await conn.fetchrow(
        """
        SELECT s.page_copy, s.review_status, s.publication_allowed, s.created_at
          FROM ai_page_generation_snapshot s
          JOIN ai_page_generation g ON g.id = s.page_generation_id
         WHERE g.page_type = $1
           AND g.anchor_slug = $2
           AND s.review_status = $3
           AND s.publication_allowed = TRUE
         ORDER BY s.created_at DESC
         LIMIT 1
        """,
        page_type,
        anchor_slug,
        "approved",
    )
    if not row:
        raise HTTPException(404, "Reviewed AI page copy not found")
    page_copy = row["page_copy"]
    if isinstance(page_copy, str):
        page_copy = json.loads(page_copy)
    return {
        **page_copy,
        "review_status": row["review_status"],
        "publication_allowed": row["publication_allowed"],
    }


@router.get("/demos/earthrise")
async def get_earthrise_demo(auth: Auth) -> dict:
    from services.ai.earthrise_demo import run_earthrise_demo

    return run_earthrise_demo()


@router.get("/requests/{request_id}")
async def get_ai_request(request_id: UUID, auth: Auth, conn: DB) -> dict:
    request = await conn.fetchrow("SELECT * FROM ai_generation_request WHERE id = $1", request_id)
    if not request:
        raise HTTPException(404, "AI generation request not found")
    result = await conn.fetchrow(
        "SELECT * FROM ai_generation_result WHERE generation_request_id = $1", request_id
    )
    return {"request": dict(request), "result": dict(result) if result else None}


@router.get("/audit-events")
async def list_ai_audit_events(auth: Auth, conn: DB) -> list[dict]:
    rows = await conn.fetch("SELECT * FROM ai_audit_event ORDER BY created_at DESC LIMIT 100")
    return [dict(row) for row in rows]


async def _queue_page_generation_response(
    conn: DB,
    generation_id: UUID,
    snapshot_id: UUID,
    actor: str,
    page_copy: dict[str, Any],
) -> dict:
    from services.ai.page_review import build_review_queue_item

    queue_item = build_review_queue_item(str(generation_id), str(snapshot_id), actor=actor)
    await conn.execute(
        """
        INSERT INTO ai_page_review_queue (
            page_generation_id, snapshot_id, review_status, assigned_to,
            publication_allowed, human_review_required, queue_item_sha256
        )
        VALUES ($1, $2, 'pending', $3, FALSE, TRUE, $4)
        ON CONFLICT (page_generation_id, snapshot_id) DO UPDATE SET
            review_status = EXCLUDED.review_status,
            assigned_to = EXCLUDED.assigned_to,
            queue_item_sha256 = EXCLUDED.queue_item_sha256,
            updated_at = NOW()
        """,
        generation_id,
        snapshot_id,
        actor,
        queue_item["queue_item_sha256"],
    )
    await conn.execute(
        """
        INSERT INTO ai_page_version_history (
            page_generation_id, snapshot_id, event_type, actor, event, event_sha256
        )
        VALUES ($1, $2, 'queued_generation', $3, $4::jsonb, $5)
        ON CONFLICT (event_sha256) DO NOTHING
        """,
        generation_id,
        snapshot_id,
        actor,
        json.dumps(queue_item),
        queue_item["queue_item_sha256"],
    )
    return {
        "page_generation_id": str(generation_id),
        "snapshot_id": str(snapshot_id),
        "review_queue": queue_item,
        **page_copy,
    }


@router.get("/page-review-queue")
async def list_page_review_queue(auth: Auth, conn: DB) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT * FROM ai_page_review_queue
         WHERE review_status = 'pending'
         ORDER BY created_at ASC
        """
    )
    return [dict(row) for row in rows]


@router.post("/page-generation/{generation_id}/approve")
async def approve_page_generation(
    generation_id: UUID,
    payload: PageGenerationApprovalRequest,
    auth: Auth,
    conn: DB,
) -> dict:
    from services.ai.page_review import PageReviewError, approve_generation

    generation = await conn.fetchrow(
        "SELECT * FROM ai_page_generation WHERE id = ", generation_id
    )
    if not generation:
        raise HTTPException(404, "AI page generation not found")
    snapshot = await conn.fetchrow(
        """
        SELECT * FROM ai_page_generation_snapshot
         WHERE page_generation_id = $1
         ORDER BY created_at DESC
         LIMIT 1
        """,
        generation_id,
    )
    if not snapshot:
        raise HTTPException(404, "AI page generation snapshot not found")

    generation_dict = dict(generation)
    snapshot_dict = dict(snapshot)
    for key in ("page_copy", "source_references"):
        if isinstance(snapshot_dict.get(key), str):
            snapshot_dict[key] = json.loads(snapshot_dict[key])
    try:
        approved = approve_generation(
            generation_dict,
            snapshot_dict,
            reviewer=payload.reviewer,
            notes=payload.notes,
        )
    except PageReviewError as exc:
        raise HTTPException(422, str(exc)) from exc

    async with conn.transaction():
        await conn.execute(
            """
            UPDATE ai_page_generation
               SET review_status = 'approved', publication_allowed = TRUE, updated_at = NOW()
             WHERE id = $1
            """,
            generation_id,
        )
        await conn.execute(
            """
            UPDATE ai_page_generation_snapshot
               SET review_status = 'approved', publication_allowed = TRUE
             WHERE id = $1
            """,
            snapshot["id"],
        )
        await conn.execute(
            """
            UPDATE ai_page_review_queue
               SET review_status = 'completed', reviewed_by = $2, reviewed_at = NOW(),
                   notes = $3, publication_allowed = TRUE, updated_at = NOW()
             WHERE page_generation_id = $1 AND snapshot_id = $4
            """,
            generation_id,
            payload.reviewer,
            payload.notes,
            snapshot["id"],
        )
        publication_row = await conn.fetchrow(
            """
            INSERT INTO ai_page_publication_snapshot (
                page_generation_id, source_snapshot_id, publication_version, page_copy,
                page_copy_sha256, attribution_block, source_references, publication_status,
                approved_by, approval_event_sha256
            )
            VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7::jsonb, 'active', $8, $9)
            RETURNING id
            """,
            generation_id,
            snapshot["id"],
            "approved-" + str(snapshot["id"]),
            json.dumps(snapshot_dict["page_copy"]),
            snapshot["page_copy_sha256"],
            snapshot["attribution_block"],
            json.dumps(snapshot_dict["source_references"]),
            payload.reviewer,
            approved["event_sha256"],
        )
        await conn.execute(
            """
            INSERT INTO ai_page_version_history (
                page_generation_id, snapshot_id, publication_snapshot_id,
                event_type, actor, event, event_sha256
            )
            VALUES ($1, $2, $3, 'approved_generation', $4, $5::jsonb, $6)
            ON CONFLICT (event_sha256) DO NOTHING
            """,
            generation_id,
            snapshot["id"],
            publication_row["id"],
            payload.reviewer,
            json.dumps(approved),
            approved["event_sha256"],
        )

    return {**approved, "publication_snapshot_id": str(publication_row["id"])}


@router.post("/page-generation/{generation_id}/rollback")
async def rollback_page_generation(
    generation_id: UUID,
    payload: PageGenerationRollbackRequest,
    auth: Auth,
    conn: DB,
) -> dict:
    from services.ai.page_review import PageReviewError, rollback_generation

    generation = await conn.fetchrow(
        "SELECT * FROM ai_page_generation WHERE id = ", generation_id
    )
    if not generation:
        raise HTTPException(404, "AI page generation not found")
    current = await conn.fetchrow(
        """
        SELECT * FROM ai_page_publication_snapshot
         WHERE page_generation_id = $1 AND publication_status = 'active'
         ORDER BY created_at DESC
         LIMIT 1
        """,
        generation_id,
    )
    if not current:
        raise HTTPException(404, "Active AI page publication snapshot not found")
    target = await conn.fetchrow(
        "SELECT * FROM ai_page_generation_snapshot WHERE id = $1", payload.target_snapshot_id
    )
    if not target:
        raise HTTPException(404, "Rollback target snapshot not found")

    generation_dict = dict(generation)
    current_dict = dict(current)
    target_dict = dict(target)
    for key in ("page_copy", "source_references"):
        if isinstance(target_dict.get(key), str):
            target_dict[key] = json.loads(target_dict[key])
    try:
        rollback = rollback_generation(
            generation_dict,
            current_dict,
            target_dict,
            actor=payload.actor,
            reason=payload.reason,
        )
    except PageReviewError as exc:
        raise HTTPException(422, str(exc)) from exc

    async with conn.transaction():
        await conn.execute(
            """
            UPDATE ai_page_publication_snapshot
               SET publication_status = 'rolled_back'
             WHERE id = $1
            """,
            current["id"],
        )
        publication_row = await conn.fetchrow(
            """
            INSERT INTO ai_page_publication_snapshot (
                page_generation_id, source_snapshot_id, publication_version, page_copy,
                page_copy_sha256, attribution_block, source_references, publication_status,
                approved_by, approval_event_sha256, rollback_of_publication_snapshot_id
            )
            VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7::jsonb, 'active', $8, $9, $10)
            RETURNING id
            """,
            generation_id,
            target["id"],
            "rollback-" + str(target["id"]),
            json.dumps(target_dict["page_copy"]),
            target["page_copy_sha256"],
            target["attribution_block"],
            json.dumps(target_dict["source_references"]),
            payload.actor,
            rollback["event_sha256"],
            current["id"],
        )
        await conn.execute(
            """
            INSERT INTO ai_page_version_history (
                page_generation_id, snapshot_id, publication_snapshot_id,
                event_type, actor, event, event_sha256
            )
            VALUES ($1, $2, $3, 'rollback_generation', $4, $5::jsonb, $6)
            ON CONFLICT (event_sha256) DO NOTHING
            """,
            generation_id,
            target["id"],
            publication_row["id"],
            payload.actor,
            json.dumps(rollback),
            rollback["event_sha256"],
        )

    return {**rollback, "publication_snapshot_id": str(publication_row["id"])}


@router.get("/page-generation/{generation_id}/history")
async def get_page_generation_history(generation_id: UUID, auth: Auth, conn: DB) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT * FROM ai_page_version_history
         WHERE page_generation_id = $1
         ORDER BY created_at ASC
        """,
        generation_id,
    )
    return [dict(row) for row in rows]


@router.post("/place-generation/{anchor_slug}")
async def generate_place_pages(anchor_slug: str, auth: Auth) -> dict:
    from services.ai.page_generation import PageGenerationError
    from services.ai.place_pipeline import generate_place_pipeline

    try:
        return generate_place_pipeline(anchor_slug)
    except PageGenerationError as exc:
        raise HTTPException(422, str(exc)) from exc
