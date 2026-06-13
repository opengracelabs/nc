# NC-AI-001 Technical Architecture Plan

| Field | Value |
|---|---|
| Document | NC-AI-001 |
| Status | Sprint 1 implemented |
| Scope | First AI infrastructure layer for Nature & Culture |
| Depends on | Mission Control, NC-WEB-001, NC-PILOT-001, NC-PRODUCT-001, FastAPI, Postgres |

## 1. Core Rule

Graph and source evidence are authoritative. LLM output is advisory until it is grounded, attributed, persisted as a generation result, and approved by a human review flow where policy requires review.

No model may invent rights status, source provenance, publication eligibility, product safety, or attribution requirements. Any generated claim that affects public website copy, product copy, education content, rights/governance, or user-facing assistant answers must cite source records.

## 2. Architecture

Sprint 1 adds `services/ai` as a policy and grounding layer in front of future model calls.

```text
services/ai/
  router.py          FastAPI API surface
  policies.py        task routing and publication policy
  grounding.py       grounding-source validation contract
  retrieval.py       deterministic context assembly
  prompts.py         deterministic prompt template rendering/versioning
  providers/         provider class registry and local mock provider
```

The service records:

- model registry entries
- task policies
- prompt templates
- generation requests
- generation results
- grounding sources
- model route decisions
- human review requirements
- audit events

## 3. Provider Policy

Sprint 1 does not call real providers. Provider classes are stubs except for the deterministic local mock.

Routing policy:

- `rights_governance`: Claude policy, human review required
- `place_story`: Gemini/GPT/open-model narrative policy, human review required
- `product_copy`: Gemini/GPT/open-model narrative policy, human review required
- `education_module`: Gemini/GPT/open-model narrative policy, human review required
- `code_generation`: Codex policy, human review required before operational use
- `public_website_copy`: grounded narrative policy, publication review required
- `user_assistant`: grounded assistant policy, source citations required

Actual Sprint 1 execution uses `DeterministicMockProvider`, even when the policy route says Claude, Gemini, OpenAI, or Codex. This guarantees tests and local development make no external calls.

## 4. Grounding Contract

Grounding sources must include:

- `source_type`
- `source_id`
- `source_record_id`
- `title`
- `url` when available
- `rights_status` when rights/product/public copy is involved
- `attribution` requirements
- evidence payload or summary

Rejected source conditions:

- missing evidence for tasks that require grounding
- missing attribution requirements
- missing rights status for product/public/rights tasks
- GBIF media
- Wikidata Commons media as product-safe evidence
- OSM data except display-reference policy

## 5. Publication Policy

Generated content is never published automatically.

Every generation result carries:

- `publication_allowed = false`
- `human_review_required = true` for governed task classes
- source references
- attribution requirements
- deterministic prompt template version
- audit event

Publication requires a later human review record and a separate publication workflow outside Sprint 1.

## 6. API Surface

Sprint 1 exposes:

- `GET /ai/models`
- `GET /ai/tasks`
- `POST /ai/generate`
- `POST /ai/generate/place-story`
- `POST /ai/generate/product-copy`
- `POST /ai/generate/education-module`
- `GET /ai/requests/{id}`
- `GET /ai/audit-events`

## 7. Database

Sprint 1 creates:

- `ai_model_registry`
- `ai_task_policy`
- `ai_prompt_template`
- `ai_generation_request`
- `ai_generation_result`
- `ai_grounding_source`
- `ai_model_route_decision`
- `ai_human_review`
- `ai_audit_event`

Postgres remains the authoritative state store. Generated text is advisory payload, not source truth.

## 8. Sprint 1 Verification

Sprint 1 tests must prove:

- policy router selects the expected provider policy
- rights/governance cannot auto-publish
- product copy requires grounding sources
- generation without evidence is rejected
- mock generation emits an audit event
- prompt template versioning is deterministic
- tests make no external API calls
- attribution requirements are preserved in results
