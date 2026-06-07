# Foundation Model Runtime Architecture v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Architecture only |
| Scope | AI-Native Intelligence Fabric foundation model runtime |
| Current stack | PostgreSQL, PostGIS, Neo4j, pgvector, MinIO |
| Authority posture | PostgreSQL remains sole canonical authority |

## Mission

Design the foundation model runtime for the AI-Native Intelligence Fabric.

The runtime must allow models to retrieve, rank, summarize, draft, classify, explain, and propose
without ever replacing PostgreSQL authority.

The core rule:

> Foundation models produce governed evidence, drafts, explanations, and proposals. PostgreSQL
> records truth, approvals, replay state, and canonical outcomes.

## Runtime Boundary

```text
PostgreSQL authority
  -> canonical entities, rights, activation, catalog, publication, review, replay

PostGIS
  -> authoritative spatial predicates inside PostgreSQL

Neo4j
  -> derived relationship traversal candidates

pgvector
  -> derived semantic retrieval candidates

MinIO
  -> file evidence, source payloads, media, transcripts, derivatives

Foundation model runtime
  -> intent parsing, explanation, drafting, summarization, classification proposals
  -> no canonical writes
```

The foundation model runtime writes only to PostgreSQL tables that are explicitly marked as
registry, invocation, retrieval, candidate, draft, proposal, review, or audit tables. Promotion
from a model proposal into canonical state happens only through existing governed workflow APIs.

## Runtime Flow

```text
workflow intent
  -> model/prompt eligibility check
  -> retrieval plan
  -> PostgreSQL entity resolution
  -> PostGIS spatial retrieval
  -> pgvector semantic retrieval
  -> Neo4j relationship retrieval
  -> PostgreSQL rehydration and eligibility gate
  -> context pack
  -> foundation model invocation
  -> output validation
  -> candidate/proposal/draft record
  -> human review when consequential
  -> approved canonical write through governed workflow only
```

## 1. Model Registry

`foundation_model_registry` is the PostgreSQL authority for allowed foundation models.

It governs which models may be called, for which task classes, under which review policy.

Required fields:

| Field | Requirement |
|---|---|
| `model_key` | Stable internal key, immutable. |
| `provider` | `openai`, `anthropic`, `google`, `local`, `other`. |
| `provider_model_id` | Exact provider model identifier. |
| `model_family` | Text, multimodal, vision, audio, embedding-capable, reasoning. |
| `capabilities` | JSONB list: classify, summarize, draft, explain, extract, plan, caption. |
| `allowed_task_types` | JSONB task allowlist. |
| `disallowed_task_types` | JSONB task denylist. |
| `input_modalities` | Text, image, audio, video, file metadata. |
| `output_modalities` | Text, JSON, structured extraction, rationale. |
| `max_context_tokens` | Runtime safety limit. |
| `determinism_profile` | deterministic, low_variance, nondeterministic. |
| `data_policy` | Whether source context may leave the local stack/provider boundary. |
| `status` | draft, approved, active, paused, retired. |
| `approved_by` | Human approval identity. |
| `approved_at` | Activation timestamp. |
| `retired_at` | Retirement timestamp. |

Model rules:

- No model invocation may use an unregistered model.
- Model changes are replay-relevant and require registry versioning.
- A provider model ID change is a new registry version, not a silent update.
- Local models and hosted models follow the same registry contract.
- A model may be active for drafting but disallowed for classification proposals.

## 2. Prompt Registry

`prompt_registry` is the PostgreSQL authority for governed prompts.

Prompts are runtime policy, not incidental strings in workers.

Required fields:

| Field | Requirement |
|---|---|
| `prompt_key` | Stable prompt identity. |
| `prompt_version` | Immutable semantic version. |
| `task_type` | classify, summarize, draft, explain, extract, plan, review_assist. |
| `system_prompt` | Governed system instruction. |
| `developer_prompt` | Governed worker instruction, if applicable. |
| `input_contract` | JSON Schema for accepted inputs. |
| `output_contract` | JSON Schema for required output. |
| `retrieval_contract_key` | FK to allowed retrieval contract. |
| `review_policy_key` | FK to human review policy. |
| `allowed_model_keys` | Model allowlist. |
| `forbidden_claims` | Rights, activation, publication, or other prohibited claims. |
| `citation_policy` | Required citation/source ID rules. |
| `status` | draft, approved, active, paused, retired. |
| `approved_by` | Human approval identity. |
| `approved_at` | Activation timestamp. |

Prompt rules:

- Prompt text is immutable after activation.
- Prompt changes create a new version.
- Every persisted model output records prompt key and version.
- Prompts must declare whether output is `draft`, `proposal`, `explanation`, or
  `advisory_signal`.
- Prompts must prohibit rights approval, activation approval, publication approval, or canonical
  relationship creation unless a future constitution explicitly authorizes it.

## 3. Agent Invocation Contract

`agent_invocation` records every persisted model run.

It is append-only and replay-critical.

Required fields:

| Field | Requirement |
|---|---|
| `agent_invocation_id` | UUID primary identity. |
| `agent_key` | Worker/agent identity. |
| `agent_version` | Worker/agent version. |
| `task_type` | classify, summarize, draft, explain, extract, plan, caption. |
| `model_key` | FK to `foundation_model_registry`. |
| `provider_model_id` | Provider model at invocation time. |
| `prompt_key` | FK to `prompt_registry`. |
| `prompt_version` | Exact prompt version. |
| `retrieval_contract_key` | Retrieval contract used. |
| `input_entity_refs` | PostgreSQL IDs used as primary subject. |
| `input_snapshot` | JSONB compact authoritative input snapshot. |
| `input_hash` | SHA-256 of normalized input snapshot. |
| `context_pack_id` | FK to retrieved context pack. |
| `parameters` | Temperature, top-p, max tokens, response format, seed if available. |
| `output_raw` | Raw provider/local model output. |
| `output_structured` | Parsed output under `output_contract`. |
| `output_hash` | SHA-256 of normalized structured output. |
| `validation_status` | valid, invalid, partially_valid. |
| `output_status` | draft, proposed, approved, rejected, superseded, expired. |
| `started_at` | Invocation start. |
| `completed_at` | Invocation completion. |
| `error_detail` | Provider/runtime error, if any. |

Invocation rules:

- The model worker may not write canonical domain tables.
- Invalid outputs cannot become proposals.
- Invocation output must be preserved even when rejected, unless security policy requires redaction.
- Consequential tasks require a review workflow before downstream use.

## 4. Retrieval Contract

`retrieval_contract` defines what evidence a model may see.

Retrieval is not free-form browsing. It is a governed context assembly process.

Required fields:

| Field | Requirement |
|---|---|
| `retrieval_contract_key` | Stable identity. |
| `retrieval_version` | Immutable version. |
| `task_type` | Task class. |
| `allowed_entity_types` | Place, SourceItem, MediaFile, Collection, Story, Creator, Institution. |
| `allowed_sources` | PostgreSQL, PostGIS, Neo4j, pgvector, MinIO metadata. |
| `required_postgres_filters` | Rights, activation, publication, visibility, media phase. |
| `allowed_vector_spaces` | pgvector spaces usable for semantic retrieval. |
| `allowed_graph_traversals` | Neo4j traversal query keys. |
| `allowed_spatial_predicates` | PostGIS predicates and parameter bounds. |
| `max_candidates` | Upper bound before rehydration. |
| `max_context_items` | Upper bound passed to model. |
| `context_template` | How evidence is serialized into the prompt. |
| `citation_requirement` | Required PostgreSQL IDs/source references per claim. |
| `status` | draft, approved, active, retired. |

Retrieval sequence:

```text
1. Resolve query subject in PostgreSQL.
2. Apply required PostgreSQL eligibility filters.
3. Execute PostGIS predicates for spatial constraints.
4. Execute pgvector retrieval for semantic candidates.
5. Execute Neo4j traversal for relationship candidates.
6. Merge by PostgreSQL ID.
7. Rehydrate canonical records from PostgreSQL.
8. Drop ineligible or stale records.
9. Build context pack with citations and source hashes.
10. Pass only the context pack to the model.
```

Retrieval rules:

- The model never decides which rights or activation filters apply.
- PostGIS executes spatial truth; the model may only parse spatial intent.
- Neo4j returns paths and candidate IDs, not authority.
- pgvector returns similarity candidates, not classifications.
- MinIO content enters context only through authorized extraction or metadata snapshots.

## 5. Candidate Recording Contract

`model_candidate_record` stores the candidates a model or retrieval plan considered.

This is distinct from final model output. It preserves why a candidate appeared.

Required fields:

| Field | Requirement |
|---|---|
| `candidate_record_id` | UUID primary identity. |
| `agent_invocation_id` | FK to invocation. |
| `candidate_set_id` | Groups candidates for a retrieval pass. |
| `candidate_entity_type` | Place, SourceItem, Collection, Story, ProductFamily, etc. |
| `candidate_entity_id` | PostgreSQL ID. |
| `candidate_source` | postgres, postgis, neo4j, pgvector, model_suggested. |
| `retrieval_rank` | Rank before model call. |
| `model_rank` | Rank after model output, if model ranked it. |
| `score` | Similarity, distance score, graph score, or model confidence. |
| `score_type` | spatial_distance, vector_similarity, graph_depth, model_confidence. |
| `evidence` | JSONB provenance: path, vector space, spatial predicate, source IDs. |
| `eligibility_snapshot` | Rights/activation/publication result at candidate time. |
| `candidate_status` | considered, selected, rejected, stale, ineligible. |
| `created_at` | Timestamp. |

Candidate rules:

- Candidate records are append-only.
- A `model_suggested` candidate must still resolve to PostgreSQL before it can be selected.
- Ineligible candidates may be recorded for audit but must not enter context or outputs.
- Candidate evidence must distinguish spatial, graph, semantic, and model-derived signals.

## 6. Replay Model

Foundation model replay reconstructs the governed decision path. It does not promise perfect
byte-for-byte reproduction when provider models are nondeterministic or retired.

Replay package:

| Component | Required replay evidence |
|---|---|
| Canonical inputs | PostgreSQL entity snapshots and input hash. |
| Spatial retrieval | PostGIS predicate, geometry IDs, distance/bounds parameters. |
| Graph retrieval | Neo4j schema version, projection run ID, traversal query key, path evidence. |
| Semantic retrieval | Vector space, model ID, input hash, similarity scores, ANN index version if available. |
| Context pack | Context pack ID, item IDs, citations, context hash. |
| Model invocation | Model key, provider model ID, prompt version, parameters, output hash. |
| Candidate set | Candidate records, ranks, scores, eligibility snapshots. |
| Review | Reviewer identity, decision, reason, timestamp, promoted target record if any. |

Replay outcome classes:

| Outcome | Meaning |
|---|---|
| `exact` | Input, prompt, deterministic model/runtime, and output hash match. |
| `equivalent` | Candidate set and approved result match, but model output wording differs. |
| `caveated` | Model/vector/provider version changed; historical result is explainable but not exactly reproducible. |
| `failed` | Missing input, prompt, model, context, candidate, or review evidence. |

Replay rules:

- Exact replay is required for deterministic workers, not for nondeterministic hosted models.
- Nondeterministic model output must be replayable as evidence through stored input/output hashes.
- If a model is retired, replay must identify the retired model and mark the result caveated.
- Stored approvals remain valid if their original evidence is complete, even when exact model
  reproduction is impossible.

## 7. Human Review Workflow

Human review promotes model proposals into governed outcomes.

Review states:

```text
draft
  -> proposed
  -> needs_revision
  -> approved
  -> rejected
  -> superseded
  -> expired
```

Review contract fields:

| Field | Requirement |
|---|---|
| `review_id` | UUID identity. |
| `agent_invocation_id` | Model run under review. |
| `proposal_type` | caption, story_summary, collection_rationale, metadata_suggestion, classification_suggestion. |
| `target_entity_type` | Canonical entity type affected. |
| `target_entity_id` | PostgreSQL canonical entity ID, if existing. |
| `review_policy_key` | Governing review policy. |
| `review_status` | draft, proposed, needs_revision, approved, rejected, superseded, expired. |
| `reviewer_id` | Human reviewer. |
| `reviewer_role` | Curator, director, editor, engineer, rights reviewer. |
| `review_notes` | Required for rejection, override, or material edit. |
| `material_changes` | JSONB diff from model proposal to approved output. |
| `approved_payload` | Payload eligible for governed promotion. |
| `promoted_record_ref` | PostgreSQL canonical record created/updated by governed workflow. |
| `reviewed_at` | Timestamp. |

Review rules:

- Rights, activation, publication, and commerce scoring decisions require existing domain review
  workflows. The model runtime cannot invent a parallel approval path.
- Low-risk text drafts may be approved by editorial review.
- Metadata suggestions require curator review before canonical update.
- Classification suggestions require evidence citations and domain review.
- Model-generated captions or alt text require source citation and visual/metadata consistency
  review before publication.
- Human edits are recorded as material changes, not hidden rewrites of model output.

## Task Classes

| Task | Model may do | Required authority check |
|---|---|---|
| Search intent parsing | Convert natural language into query plan. | PostgreSQL/PostGIS execute filters. |
| Relationship explanation | Explain Neo4j path in human language. | Path must come from governed graph projection. |
| Semantic recommendation rationale | Explain pgvector candidate relevance. | Candidate must be rehydrated and eligible. |
| Caption/alt text draft | Draft text from approved context. | Human review before publication. |
| Metadata extraction | Propose fields from source record/media evidence. | Curator review before canonical write. |
| Collection rationale | Draft collection explanation. | Collection governance approval. |
| Education prompt | Draft learning activity. | Editorial/education review. |
| Commerce rationale | Draft rationale only. | Commerce Intelligence remains scoring authority. |

## Runtime Tables: Conceptual Set

This is architecture only, not DDL.

| Conceptual table | Purpose |
|---|---|
| `foundation_model_registry` | Allowed models and capabilities. |
| `prompt_registry` | Versioned prompts and output contracts. |
| `retrieval_contract_registry` | Governed retrieval scopes. |
| `context_pack` | Authorized retrieved evidence passed to models. |
| `agent_invocation` | Append-only model run record. |
| `model_candidate_record` | Candidate evidence and rankings. |
| `model_output_proposal` | Draft/proposal/explanation/advisory output. |
| `model_review` | Human review decisions. |
| `model_replay_audit` | Replay runs and outcomes. |

## Worker Sequence

1. `model_registry_seed_worker`
2. `prompt_registry_seed_worker`
3. `retrieval_contract_seed_worker`
4. `retrieval_planner_worker`
5. `context_pack_builder_worker`
6. `agent_invocation_worker`
7. `model_output_validator_worker`
8. `candidate_recording_worker`
9. `proposal_writer_worker`
10. `human_review_gateway`
11. `approved_promotion_worker`
12. `model_replay_audit_worker`

## Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Model output treated as canonical truth | Critical | Models write only proposal/draft/audit records; promotion requires governed workflow. |
| Unsupported model claims | Critical | Citation policy; output validation; reject claims without PostgreSQL/source evidence. |
| Rights or activation bypass | Critical | Required PostgreSQL eligibility gate before context and before response. |
| Prompt drift breaks replay | High | Prompt registry, immutable versions, prompt hash in invocation. |
| Provider model drift breaks replay | High | Model registry, provider model ID, output hash, caveated replay class. |
| Hidden retrieval changes alter behavior | High | Retrieval contract versioning and context pack hash. |
| Candidate provenance lost | High | Candidate recording contract before model output. |
| Human edits obscure model contribution | Medium | Material change diff and approved payload recorded. |
| Context leakage | High | Retrieval contracts and PostgreSQL visibility filters before context pack. |
| Over-reliance on confidence scores | Medium | Confidence is advisory; review and PostgreSQL gates decide. |

## GO / NO-GO

GO for architecture.

NO-GO for implementation until:

- The foundation model registry and prompt registry are approved as governed PostgreSQL
  authorities for model use.
- Retrieval contracts are defined for each task class.
- Candidate recording and invocation audit are required for persisted outputs.
- Human review policy is mapped to each consequential task.
- Existing PostgreSQL authority boundaries are explicitly preserved.

The runtime is AI-native because models participate throughout retrieval, explanation, drafting,
and proposal generation. It remains governed because only PostgreSQL authority and human/domain
review can convert a proposal into platform truth.
