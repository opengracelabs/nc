# AI-Native Intelligence Fabric v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Architecture design only |
| Scope | PostGIS + Neo4j + pgvector + foundation models |
| Governing posture | PostgreSQL remains sole canonical authority |

## Executive Position

The AI-native intelligence fabric should be a coordinated set of derived intelligence services
around PostgreSQL, not a replacement for PostgreSQL.

The design principle:

> AI may retrieve, rank, summarize, draft, explain, and propose. Only PostgreSQL records approved
> canonical state.

PostGIS, Neo4j, pgvector, and foundation models each provide a different intelligence capability:

| Runtime | Intelligence role | Authority posture |
|---|---|---|
| PostgreSQL | Canonical facts, governance, approvals, replay, audit, IDs. | Sole authority. |
| PostGIS | Spatial predicates, geometry, containment, distance, map filtering. | Authoritative extension of PostgreSQL. |
| Neo4j | Multi-hop relationship traversal over projected PostgreSQL facts. | Derived projection. |
| pgvector | Semantic similarity over governed embedding spaces. | Derived projection inside PostgreSQL. |
| Foundation models | Natural language reasoning, summarization, classification drafts, query planning, explanation. | Advisory model output only. |

The fabric becomes safe when every non-PostgreSQL result is treated as a signal with provenance,
not as truth.

## Core Invariants

### Invariant 1: PostgreSQL Owns Identity

Every entity returned by the fabric must resolve to a PostgreSQL identity:

- `place_id`
- `source_item_id`
- `media_file_id`
- `activation_target_id`
- `collection_id`
- `story_id`
- `creator_id`
- `institution_id`
- `product_family_id`

No model-generated entity can become canonical until PostgreSQL records it through the governed
creation path.

### Invariant 2: PostgreSQL Owns Eligibility

Before any result reaches a public or downstream workflow, PostgreSQL must recheck:

- rights status
- activation status
- publication status
- media type phase
- collection membership
- catalog/product eligibility
- visibility and retraction state

Neo4j, pgvector, and foundation models may suggest candidates. They cannot approve candidates.

### Invariant 3: PostgreSQL Owns Replay

Every intelligence result that affects a stored decision must write replay metadata to PostgreSQL:

- source entity IDs
- input snapshot hash
- projection schema version
- vector space and model version
- prompt/template version
- foundation model ID
- worker version
- result payload
- reviewer decision, when consequential

If it cannot be replayed or audited, it cannot drive a governed decision.

### Invariant 4: Models Never Mutate Canonical State Directly

Foundation models do not write canonical tables. They write only to proposed, derived, draft, or
audit tables. Human or governed worker approval promotes a proposal into canonical PostgreSQL state.

### Invariant 5: Derived Layers Are Disposable

Neo4j, pgvector indexes, and model output caches must be rebuildable from PostgreSQL and MinIO.
Loss of any derived layer degrades discovery, but does not stop ingestion, rights verification,
commerce, catalog, publication, or replay.

## Fabric Topology

```text
                        +----------------------+
                        |   Foundation Models  |
                        | summarize / draft /  |
                        | explain / plan       |
                        +----------+-----------+
                                   |
                                   v
                         model_output_proposal
                                   |
                                   v
+----------------+        +--------+---------+        +----------------+
|     MinIO      | -----> |   PostgreSQL     | <----- |    PostGIS     |
| file evidence  |        | canonical state  |        | spatial truth  |
+----------------+        | governance       |        +----------------+
                          | replay / audit   |
                          +---+----------+---+
                              |          |
                 projection   |          | embedding input
                              v          v
                         +----+--+    +--+---------+
                         | Neo4j |    | pgvector   |
                         | graph |    | vectors    |
                         +---+---+    +-----+------+
                             |              |
                             +------+-------+
                                    v
                            Intelligence Gateway
                                    |
                                    v
                   PostgreSQL rehydration + eligibility check
                                    |
                                    v
                            API / UI / workers
```

## The Four Intelligence Modes

### 1. Spatial Intelligence: PostGIS

PostGIS answers questions about space:

- What assets are inside or near this place?
- Which places are within a route, polygon, bounding box, or radius?
- Which media should appear in a map viewport?
- Which candidate items are geographically relevant to a tourism or education page?

Rules:

- Geometry and distance remain PostgreSQL authority.
- Neo4j may project spatial relationships such as `PROXIMATE_TO`, but those edges are derived
  from PostGIS and must be rebuildable.
- Foundation models may translate natural language into spatial intent, but the actual spatial
  predicate executes in PostGIS.

Example:

```text
User asks: "Show historic maps near Yellowstone."
Model parses intent -> media_type=map, place=Yellowstone, radius=derived default.
PostgreSQL resolves place_id.
PostGIS executes spatial filter.
PostgreSQL checks rights/publication.
pgvector optionally ranks semantically.
API returns PostgreSQL-backed records.
```

### 2. Relationship Intelligence: Neo4j

Neo4j answers questions about connections:

- What creators, institutions, places, subjects, and collections connect this item?
- What else is held by the same institution and depicts nearby places?
- Which stories connect botanical art, a taxon, a place, and a collection?
- Which assets explain why a product family or education module is relevant?

Rules:

- Neo4j nodes and relationships are projections from PostgreSQL.
- Relationship vocabulary is governed by `projection_schema_registry`.
- Neo4j traversal returns candidate IDs and paths, not canonical facts.
- Every graph response must include schema version, projection run ID, and path provenance.
- PostgreSQL rehydrates and filters every candidate before public use.

### 3. Semantic Intelligence: pgvector

pgvector answers questions about meaning:

- Which source items are semantically similar to this item?
- Which places match a natural language query?
- Which collections support a lesson topic?
- Which media objects match a story paragraph or curator brief?

Rules:

- Vector spaces are named and governed.
- Embedding model ID, model version, vector dimension, input schema, and input hash are stored.
- Embeddings are invalid when the source hash changes.
- Similarity is advisory and may be nondeterministic after model or index changes.
- Semantic signals cannot enter commerce scoring without constitutional amendment.

### 4. Generative Intelligence: Foundation Models

Foundation models answer questions that require language, synthesis, or planning:

- Draft a story summary from approved source material.
- Explain why two assets are related.
- Generate a natural language search plan.
- Normalize query intent into filters.
- Draft alt text, captions, collection rationale, or education prompts.
- Propose missing metadata for human review.

Rules:

- Model output is not authoritative.
- Model output is stored as `draft`, `proposal`, `explanation`, or `advisory_signal`.
- Models must cite PostgreSQL IDs or source evidence references used as context.
- Models cannot infer rights, approve activation, create canonical relationships, or publish content.
- Consequential outputs require human or governed approval.

## Intelligence Gateway

The Intelligence Gateway is the orchestration layer. It decides which runtime to ask, but it never
overrides PostgreSQL.

Gateway sequence:

```text
1. Receive user/workflow intent.
2. Resolve known entities from PostgreSQL.
3. Build query plan:
   - PostGIS for spatial constraints.
   - Neo4j for relationship expansion.
   - pgvector for semantic candidate retrieval.
   - foundation model for intent parsing, explanation, or draft synthesis.
4. Execute derived queries.
5. Merge candidates by PostgreSQL ID.
6. Rehydrate canonical records from PostgreSQL.
7. Apply eligibility gates.
8. Attach derived signal metadata.
9. Return response or write proposal/audit record.
```

The gateway should expose four classes of output:

| Output class | Description | Can drive canonical change? |
|---|---|---|
| `retrieval_result` | Read-only candidate list. | No. |
| `advisory_signal` | Similarity, relationship, or spatial signal. | No, unless governance allows. |
| `draft_output` | Model-generated text or explanation. | No. |
| `proposal` | Suggested canonical change awaiting approval. | Only after governed approval writes PostgreSQL state. |

## Foundation Model Runtime Contract

Foundation model calls must be versioned like workers.

Required model invocation record:

| Field | Purpose |
|---|---|
| `model_invocation_id` | Stable audit ID. |
| `model_provider` | Provider or local runtime. |
| `model_id` | Exact model identifier. |
| `model_version` | Version if available. |
| `task_type` | classify, summarize, explain, draft, plan, extract. |
| `prompt_template_id` | Governed prompt template. |
| `prompt_template_version` | Replay boundary. |
| `input_entity_ids` | PostgreSQL entities used as context. |
| `input_snapshot_hash` | Hash of retrieved context. |
| `retrieval_context` | IDs from PostGIS/Neo4j/pgvector used in context. |
| `output_hash` | Hash of model result. |
| `output_status` | draft/proposed/approved/rejected/superseded. |
| `created_by_worker` | Worker identity. |
| `reviewed_by` | Human/governed reviewer when required. |

No model call should be hidden inside a worker without this record when its output is persisted.

## Retrieval-Augmented Generation Pattern

Foundation models should use retrieval-augmented generation, but retrieval must be authority-aware.

```text
Query
  -> PostgreSQL entity resolution
  -> PostGIS spatial filter
  -> pgvector semantic candidates
  -> Neo4j relationship expansion
  -> PostgreSQL eligibility recheck
  -> context pack with source IDs and citations
  -> foundation model draft/explanation
  -> PostgreSQL model invocation record
  -> human/governed approval if consequential
```

The model sees only context that PostgreSQL has authorized for the task. The model cannot browse
or invent new authority in the middle of a governed workflow.

## Write Boundaries

| Actor | May write canonical PostgreSQL? | May write derived/audit PostgreSQL? | May write Neo4j? | May write pgvector? |
|---|---:|---:|---:|---:|
| Human reviewer | Yes, through governed APIs. | Yes. | No. | No. |
| Ingestion worker | Yes, to substrate tables. | Yes. | No. | No. |
| Projection worker | Only projection/audit tables. | Yes. | Yes. | Yes. |
| Foundation model worker | No. | Yes, proposals/drafts/invocations only. | No. | No. |
| API gateway | No direct canonical mutation except approved workflow endpoints. | Yes. | No. | No. |
| Commerce worker | Yes, to governed commerce tables only. | Yes. | No. | No. |

## Decision Classes

| Decision | Runtime may assist | Authority |
|---|---|---|
| Spatial containment/proximity | PostGIS, model query parsing | PostgreSQL/PostGIS |
| Related assets | Neo4j, pgvector, model explanation | PostgreSQL after rehydration |
| Similar assets | pgvector, Neo4j context | PostgreSQL after rehydration |
| Rights eligibility | None as authority; model may draft notes | PostgreSQL rights records |
| Activation approval | Model may draft rationale | PostgreSQL governed approval |
| Commerce scoring | Existing Commerce Intelligence only | PostgreSQL commerce tables |
| Story draft | Model may draft from approved context | Human/governed publication approval |
| Collection recommendation | Neo4j/pgvector/model may recommend | PostgreSQL recommendation + approval |
| Product routing | Model may explain route | PostgreSQL routing policy |

## Replay Model

Replay must reconstruct the decision path, not merely the final answer.

Replay package:

```json
{
  "canonical_inputs": ["postgresql entity snapshots"],
  "spatial_inputs": ["postgis predicate, geometry ids, distance thresholds"],
  "graph_inputs": ["neo4j schema version, projection run id, traversal path"],
  "semantic_inputs": ["vector space, model id, input hash, similarity scores"],
  "model_inputs": ["prompt template version, model id, context hash"],
  "output": ["draft/proposal/result hash"],
  "approval": ["reviewer, timestamp, decision, reason"]
}
```

Replay outcome classes:

| Outcome | Meaning |
|---|---|
| `exact` | PostgreSQL inputs and deterministic worker output match. |
| `functionally_equivalent` | Derived layer rebuilt but produces equivalent candidate set. |
| `caveated` | Model/vector version changed; historical result is explainable but not exactly reproducible. |
| `invalid` | Required input, model metadata, or approval record is missing. |

## Guardrails

1. Every public result is rehydrated from PostgreSQL.
2. Every derived signal has provenance.
3. Every foundation model output has prompt/model/context metadata.
4. Every consequential model output is reviewed or governed before promotion.
5. Every vector space is versioned.
6. Every graph schema is versioned.
7. Every spatial predicate executes in PostGIS, not in model text.
8. Every rights and publication check executes in PostgreSQL.
9. Every derived layer has a rebuild path.
10. Every degraded derived layer falls back to PostgreSQL-only behavior.

## Recommended Architecture

Build the fabric in this order:

1. Projection governance: schema registry, vector space registry, projection events.
2. Intelligence Gateway: PostgreSQL-first orchestration and candidate rehydration.
3. PostGIS query planner: model-assisted intent parsing but SQL-owned predicates.
4. Neo4j relationship projection: graph traversal as advisory discovery.
5. pgvector semantic spaces: source item and place spaces first.
6. Foundation model invocation registry: prompt/model/context/output audit.
7. RAG context packer: only PostgreSQL-authorized context.
8. Draft/proposal tables: model output stored outside canonical tables.
9. Human/governed approval flow: promote only approved proposals.
10. Replay harness: reconstruct spatial, graph, vector, and model paths.

## Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Foundation model output treated as truth | Critical | Store as draft/proposal only; require PostgreSQL approval path. |
| Model invents unsupported facts | Critical | RAG context must cite PostgreSQL IDs; unsupported claims rejected. |
| Derived result bypasses rights gate | Critical | PostgreSQL eligibility recheck before every public response. |
| Graph/vector/model signals enter commerce scoring silently | Critical | Commerce tests and governance gates; no reads from derived layers without amendment. |
| Prompt/model version drift harms replay | High | Invocation registry with template/model/context hashes. |
| Vector/model nondeterminism | High | Replay caveats, top-N snapshots for consequential decisions. |
| Neo4j relationship drift | High | Drift audit and full rebuild from PostgreSQL. |
| Spatial hallucination by model | High | Models parse intent only; PostGIS executes spatial truth. |
| Context leakage to model | High | Context packer filters by PostgreSQL rights/publication/visibility. |
| Over-orchestration latency | Medium | Gateway query budget, staged retrieval, cache advisory outputs with hashes. |

## Final Architecture Rule

The intelligence fabric is not a brain replacing the database.

It is a set of governed lenses around PostgreSQL:

- PostGIS sees where things are.
- Neo4j sees how things connect.
- pgvector sees what things mean.
- Foundation models explain, draft, and plan.
- PostgreSQL decides what is true.
