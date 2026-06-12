# NC-AI-002: Earthrise Grounded Generation Review

| Field | Value |
|---|---|
| Document | NC-AI-002 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Scope | `services/ai/earthrise_demo.py` · `services/ai/grounding.py` · `services/ai/policies.py` · `services/ai/prompts.py` · `services/ai/providers/local.py` · `services/ai/router.py` · `services/ai/retrieval.py` · `infrastructure/postgres/init/43_nc_ai_001_runtime.sql` |
| Sprint | Sprint 1 — deterministic mock, zero external API calls |
| **Decision** | **APPROVED** |

---

## I. Scope

This review verifies the Earthrise grounded generation pipeline against the 5 criteria specified by the Principal Architect. The pipeline covers three task types: `product_copy`, `place_story`, and `education_module`, all executed against the NASA Earthrise source record (`AS08-14-2383`).

Sprint 1 executes no external API calls. All generation is performed by `DeterministicMockProvider` (`deterministic-mock-v1`). This review governs the structural correctness of the grounding/generation/review chain — not the quality of the generated text.

---

## II. Verification Matrix

### Criterion 1 — No Rights Hallucination

**Result: PASS**

| Check | Finding |
|---|---|
| `rights_status` field in model output | NOT PRESENT — `rights_status` is injected as input context (`"rights_status": "verified_pd"` in `NASA_SOURCE_RECORD`), never requested as a model output field |
| Prompt template rules | `"Do not invent rights status."` — present in every rendered prompt (`prompts.py:53`) |
| Generated text | `DeterministicMockProvider.generate()` — all three output texts reference `rights_basis` from injected context; none assert a rights determination |
| DB schema | `chk_ai_result_no_autopublish` and `chk_ai_request_no_autopublish` do not address rights assertion in text, but the deterministic mock produces no rights claims |

**Finding F-1 (medium — pre-API activation):** No output validation layer scans generated text for rights assertion patterns (e.g., "is public domain", "rights cleared", "PD confirmed"). This is the NC-AI-001 C-5 gap. The prohibition is enforced structurally in Sprint 1 by the deterministic mock, but must be enforced by the prohibited phrases validator before any live model (Claude, OpenAI, Gemini) is activated. **Does not block Sprint 1. Blocks live API activation.**

---

### Criterion 2 — No NASA Endorsement Language

**Result: PASS**

| Check | Finding |
|---|---|
| `NASA_NONENDORSEMENT` constant | `"Image credit: NASA. NASA does not endorse this product."` — defined in `earthrise_demo.py:21` as a module-level constant |
| Generated text — "Verified by NASA" | ABSENT — confirmed by test `test_earthrise_demo_preserves_attribution_and_nonendorsement`: `assert "Verified by NASA" not in result["output"]["text"]` |
| Generated text — "NARA" | ABSENT — same test: `assert "NARA" not in result["output"]["text"]` |
| Generated text — "NASA-endorsed", "NASA-certified", "Official NASA product" | ABSENT in `DeterministicMockProvider` output — confirmed by code inspection |

**Finding F-2 (low — test gap):** The test covers "Verified by NASA" and "NARA" but does not assert absence of the full NC-AI-001 §X.3 prohibited phrase set: `"NASA-endorsed"`, `"NASA-certified"`, `"Official NASA product"`. These phrases do not appear in the mock output, but the absence is not tested. The test should be extended to cover the full prohibited phrase register.

---

### Criterion 3 — Attribution Preserved

**Result: PASS**

| Check | Finding |
|---|---|
| `NASA_EARTHRISE_ATTRIBUTION` injection | Injected into `_base_inputs()` as `inputs["attribution"]` → rendered in prompt body as `INPUT:` JSON → grounding source `attribution.asset_credit` |
| `NASA_NONENDORSEMENT` injection | Injected into `_base_inputs()` as `inputs["nonendorsement"]` → grounding source `attribution.statement` |
| `collect_attribution_requirements()` | Extracts `statement` from every grounding source; deduplicated by `(source_id, statement)` key |
| Every generation result | `result["attribution_requirements"]` contains `{"statement": "Image credit: NASA. NASA does not endorse this product.", "source_id": "nasa", ...}` |
| Test verification | `test_earthrise_demo_preserves_attribution_and_nonendorsement`: `assert NASA_NONENDORSEMENT in statements` — PASSES for all three task types |
| `_pending_review()` gate | `"attribution_preserved": bool(result["attribution_requirements"])` — confirms requirements are non-empty before review proceeds |

**Finding F-3 (medium — provenance risk):** `NASA_NONENDORSEMENT` and `NASA_EARTHRISE_ATTRIBUTION` are defined independently in both `services/ai/earthrise_demo.py` (Python) and `apps/web/lib/governed-content.ts` (TypeScript). These are two separate string definitions. They are identical today. If one is ever edited without updating the other, attribution drift will occur silently — no test or schema constraint cross-validates them.

**Resolution required before Phase 1:** The governed attribution constants must have a single canonical source. Options:
1. A `canonical_attribution_strings` table in PostgreSQL from which both the API layer and the web layer read
2. A shared Python package that `services/ai/earthrise_demo.py` imports instead of defining locally
3. A cross-layer test that compares both definitions at CI time

None of these are blocking for Sprint 1 (both strings are identical). **Must be resolved before any attribution-bearing content is generated by a live model.**

---

### Criterion 4 — Retrieval Sources Preserved

**Result: PASS**

| Check | Finding |
|---|---|
| `GroundingSource` construction | `earthrise_grounding_source()` builds a fully-populated `GroundingSource` with `source_record_id = "AS08-14-2383"`, `source_type = "nasa"`, `rights_status = "verified_pd"`, full `attribution` and `evidence` dicts |
| `validate_grounding_sources()` | Called before model execution; raises `GroundingError` if sources are empty or missing required fields. For Earthrise: 1 source, all required fields populated — validation passes |
| `assemble_context()` | Returns `source_references` (lightweight) and `source_evidence` (full) for all sources; `evidence_authority` set to `"Graph and source evidence are authoritative."` |
| Generation result | `result["source_references"]` contains `[{"source_type": "nasa", "source_id": "nasa", "source_record_id": "AS08-14-2383", ...}]` |
| DB persistence | `_persist_generation()` writes: `ai_grounding_source` (full source record) + `ai_generation_result.source_references` (JSONB snapshot) + `ai_model_route_decision` — all three layers for the same generation request |
| DB constraints | `chk_ai_grounding_evidence CHECK (evidence <> '{}'::jsonb)` + `chk_ai_grounding_attribution CHECK (attribution <> '{}'::jsonb)` — database rejects grounding sources with empty evidence or attribution |
| Test verification | `test_earthrise_demo_preserves_attribution_and_nonendorsement`: `assert result["source_references"][0]["source_record_id"] == "AS08-14-2383"` — PASSES for all three task types |

**Finding F-4 (low — schema note):** `ai_generation_result.source_references` is a JSONB snapshot of `ai_grounding_source` records. The two representations can diverge if `ai_grounding_source` is amended post-generation. For Sprint 1 (no post-generation amendments), this is not a risk. At scale, the JSONB snapshot is the audit-immutable record — this is correct behavior (the record reflects what was used at generation time, not what exists now).

---

### Criterion 5 — Human Review Enforced

**Result: PASS — enforced at three independent layers**

**Layer 1: Application code (hardcoded)**

`router.py:124–125`:
```python
"publication_allowed": False,
"human_review_required": True,
```

These are hardcoded overrides applied after `generate_advisory_content()` returns. Even if the policy returned `publication_allowed_by_default = True` (which none do), these lines prevent autopublication.

**Layer 2: Policy layer**

`policies.py` — every `AITaskPolicy` in `TASK_POLICIES` has:
```python
human_review_required=True,
publication_allowed_by_default=False,
```

Verified for all 7 task types: `rights_governance`, `place_story`, `product_copy`, `education_module`, `code_generation`, `public_website_copy`, `user_assistant`.

**Layer 3: Database constraints (constitutional)**

`43_nc_ai_001_runtime.sql`:

| Constraint | Location | Enforces |
|---|---|---|
| `chk_ai_task_no_autopublish` | `ai_task_policy` | `publication_allowed_by_default = FALSE` — cannot seed a policy that allows auto-publish |
| `chk_ai_request_no_autopublish` | `ai_generation_request` | `human_review_required = TRUE` — every request row requires human review |
| `chk_ai_result_no_autopublish` | `ai_generation_result` | `publication_allowed = FALSE AND human_review_required = TRUE` — result cannot be stored as publishable |
| `chk_ai_model_no_paid_calls` | `ai_model_registry` | `external_calls_allowed = FALSE` — Sprint 1 models cannot make external calls |
| `chk_ai_task_grounded_public` | `ai_task_policy` | Public-facing tasks (`product_copy`, `place_story`, etc.) must have `grounding_required = TRUE AND cite_sources_required = TRUE` |

**Layer 4: Review workflow**

`_persist_generation()` creates an `ai_human_review` row with `review_status = 'pending'` for every generated result. A result exists in `pending` state until a human reviewer explicitly sets it to `approved`, `rejected`, or `changes_requested`.

**`DeterministicMockProvider` output** — all three task types return `"publication_allowed": False` in the raw output before application-layer overrides are applied.

**Test verification:**
- `test_earthrise_demo_review_workflow_does_not_publish`: `assert review["publication_allowed"] is False` · `assert pending["checks"]["no_auto_publish"] is True` · `assert reviewed["publication_allowed"] is False` — PASSES

**Finding F-5 (medium — future sprint):** `ai_human_review.review_status = 'approved'` has no downstream FK constraint blocking a publication write until it is set. The schema tracks review state but there is no `ai_generation_result.publication_allowed = TRUE` write gate that enforces `review_status = 'approved'` as a prerequisite. If a publication worker were introduced, it could technically write without checking review status. This is outside Sprint 1 scope (no publication workers exist). Must be addressed before any publication path is implemented.

---

## III. Policy Alignment Findings

### F-6 — `product_copy` default provider: `openai` (medium)

`policies.py:46–54` routes `product_copy` to `default_provider = "openai"`. NC-AI-001 §IX.3 requires Zero Data Retention agreement before OpenAI is activated (C-3). Sprint 1 routes all execution to `DeterministicMockProvider` regardless of policy provider, so this is currently harmless. However, the policy as written could mislead a future developer into activating OpenAI without completing the DD-AI-003 gate.

**Resolution:** Before `openai` is activated as a live provider, DD-AI-003 must be filed and ratified. The policy should additionally be updated to prefer `claude` as the primary provider for `product_copy` (NC-AI-001 §VIII.3).

### F-7 — `code_generation` default provider: `codex` (medium)

`policies.py:65–74` names `codex` as the default provider for `code_generation`. NC-AI-001 §IX.3 notes that the Codex standalone product is deprecated by OpenAI — code generation routes to Claude or DeepSeek Coder, not a Codex endpoint. The `CodexProvider` stub in `providers/__init__.py` exists as a registry entry but should be relabeled or replaced.

**Resolution:** Update `code_generation` policy to `default_provider = "claude"` with `deepseek` as fallback. Retire the `codex` provider stub label before live provider activation.

### F-8 — No `qwen` provider file inconsistency (low)

`providers/__pycache__/qwen.cpython-312.pyc` exists alongside `providers/qwen.py`. Qwen is correctly classified as LOCAL ONLY in NC-AI-001. The stub file is present. No inconsistency — this is confirming that the registry includes Qwen.

---

## IV. Verification Summary

| Criterion | Result | Findings |
|---|---|---|
| 1. No rights hallucination | **PASS** | F-1: output validator not yet built (C-5 gap, blocks API activation) |
| 2. No NASA endorsement language | **PASS** | F-2: test covers 2 of N prohibited phrases; full register not tested |
| 3. Attribution preserved | **PASS** | F-3: two independent string definitions; single-source resolution required before API activation |
| 4. Retrieval sources preserved | **PASS** | F-4: JSONB snapshot / FK divergence is low risk, correct behavior for audit |
| 5. Human review enforced | **PASS** | F-5: no publication write gate on `review_status = 'approved'` (future sprint) |

**Additional policy findings:** F-6 (`product_copy` → OpenAI, DD-AI-003 required before activation), F-7 (`code_generation` → Codex label deprecated), F-8 (low, no action required).

---

## V. Pre-API-Activation Requirements

The following must be completed before any live model (Claude, OpenAI, Gemini, or any API provider) is activated for Earthrise generation:

1. **F-1 / C-5:** Implement prohibited phrases validator covering at minimum: rights assertion patterns + full NASA endorsement phrase set from NC-AI-001 §X.3 + NARA/Earthrise attribution patterns. Must run on every model output before it enters the human review queue.
2. **F-3:** Establish a single canonical source for `NASA_NONENDORSEMENT` and `NASA_EARTHRISE_ATTRIBUTION`. Options: PostgreSQL canonical table, shared Python package, or cross-layer CI test.
3. **F-6:** File and ratify DD-AI-003 (OpenAI Zero Data Retention) before `product_copy` routes to a live OpenAI endpoint.
4. **F-7:** Update `code_generation` policy to `claude` primary + `deepseek` fallback before code generation goes live.

---

## VI. Decision

**APPROVED**

The Earthrise grounded generation pipeline is structurally sound for Sprint 1. All 5 verification criteria are satisfied. The generation chain enforces grounding before model execution, injects attribution as governed constants, blocks publication at three independent layers (application, policy, database), and produces no rights hallucinations or NASA endorsement language.

The 8 findings are documented above. None are blocking for Sprint 1 (deterministic mock, zero external API calls). Findings F-1 and F-3 are hard blockers before any live model is activated for Earthrise generation. Finding F-5 must be addressed before any publication worker is built.

The pipeline is cleared for continued Sprint 1 development against the deterministic mock. NC-AI-001 C-2 (DD-AI-001 — Claude activation gate) governs the transition to live API execution.

---

*NC-AI-002 v1.0 — drafted 2026-06-12. Pending ratification.*
*Reviewed against: NC-AI-001 · Foundation Model Constitution v1.0 · NC-FIRST-SALE (FS-001) · NC-WEB-001*
