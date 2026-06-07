# Relationship & Semantic Intelligence Constitution v1.0

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — governance only. Implementation requires Director Decision SD-AMEND-1. |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |

---

## Precondition — Strategic Direction Amendment Required

The Strategic Direction v1 (ratified 2026-06-07) lists the following as frozen permanent
elements: PostgreSQL, MinIO, FastAPI, Docker Compose. It explicitly excludes new databases,
Neo4j, and vector databases. The Wireframe Constitution v1 (ratified 2026-06-07) confirmed
that neither Neo4j nor pgvector is present in any migration file.

**This Constitution is ratified as governance doctrine. Its implementation is not authorized
until Director Decision SD-AMEND-1 is recorded, amending the Strategic Direction v1 frozen
stack clause to permit:**

- Neo4j as a projection-only Relationship Intelligence layer
- pgvector as a projection-only Semantic Intelligence layer

Director Decision SD-AMEND-1 must include:
- Rationale for each addition
- Explicit confirmation that PostgreSQL remains the sole authority for all canonical state
- Reference to this Constitution as the governing framework
- Second-human approval

All articles in this Constitution are governance-effective immediately. Implementation
is blocked until SD-AMEND-1 is recorded.

---

## Preamble

This Constitution establishes the governance model for the Relationship Intelligence Layer
(Neo4j) and the Semantic Intelligence Layer (pgvector) of Nature & Culture.

These are projection systems. They are not authorities. They are not write paths. They are
derived state computed from and fully traceable to PostgreSQL. Every relationship that
Neo4j claims to know is a fact already recorded in PostgreSQL tables. Every semantic
similarity that pgvector computes is derived from content whose canonical record lives in
PostgreSQL or MinIO.

The governing principle of this Constitution: **projection systems serve discovery and
enrichment. PostgreSQL serves truth.**

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity
Doctrine, and the Universal Media Substrate Constitution. It is senior to any worker
configuration, API contract, or application logic that uses relationship or semantic
intelligence data.

---

## Part I — Foundations

### Article 1 — Identity and Constitutional Role

**1.1** The Relationship Intelligence Layer is Neo4j. Its role is exactly and only this:
provide efficient multi-hop traversal of relationships that already exist in PostgreSQL,
projected into a graph model for discovery enrichment, related-content surfacing, and
recommendation support.

**1.2** The Semantic Intelligence Layer is pgvector. Its role is exactly and only this:
provide efficient approximate nearest-neighbor search over dense vector embeddings of
content whose canonical text and metadata live in PostgreSQL, for discovery enrichment
and semantic search support.

**1.3** Neither layer is an authority. Neither layer is a write path for canonical state.
Neither layer participates in rights verification, activation approval, quality scoring,
or any other governed pipeline decision without a constitutional amendment to the relevant
governing constitution.

**1.4** Both layers are expendable. The platform continues to function in all canonical
operations — acquisition, rights verification, scoring, activation, commerce, collection
building, and publication — when either or both layers are unavailable. Unavailability
of Neo4j or pgvector is degraded discovery, not platform failure.

**1.5** Both layers are rebuildable. Given only PostgreSQL and MinIO, the complete state
of both layers can be reconstructed from scratch. Rebuild is always possible. Rebuild is
the recovery path for any inconsistency, failure, or schema migration.

### Article 2 — Scope

This Constitution governs:

| Entity | Layer | Role |
|---|---|---|
| Neo4j node types | Relationship Intelligence | Projection targets for PostgreSQL entities |
| Neo4j relationship types | Relationship Intelligence | Projection targets for PostgreSQL relationships |
| Projection schema registry | Relationship Intelligence | Governs Neo4j schema versions |
| pgvector vector spaces | Semantic Intelligence | Named embedding spaces for specific use cases |
| pgvector model registry | Semantic Intelligence | Governs embedding model versions |
| Projection event records | Both | Provenance records for projection operations |

This Constitution does not govern: PostgreSQL schema, MinIO key conventions, IIIF delivery,
commerce scoring formulas, rights verification, or any governed entity in the Media Substrate
Constitution.

### Article 3 — Authority Hierarchy

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Universal Media Substrate Constitution v1.2
            └─ Relationship & Semantic Intelligence Constitution v1.0  ← this document
                 └─ [All downstream constitutions]

Authority hierarchy within the stack:

  PostgreSQL  ←── SOLE AUTHORITY for all canonical state
  MinIO       ←── Evidence storage (file content)
  Neo4j       ←── Projection layer (relationship traversal only)
  pgvector    ←── Projection layer (semantic similarity only)
  FastAPI     ←── Query gateway
```

**3.1** PostgreSQL is the sole authority. When any other system disagrees with PostgreSQL,
PostgreSQL is correct. The other system is stale and must be rebuilt.

**3.2** MinIO holds file evidence. When pgvector embeddings are derived from file content,
MinIO is the authoritative source of that content.

**3.3** Neo4j and pgvector hold derived state. Derived state may lag PostgreSQL by the
projection latency period defined in Article 16. During the lag period, Neo4j and pgvector
are stale but not incorrect — stale is an expected operational state. Divergent is never
acceptable.

**3.4** No worker, API, or application logic may treat Neo4j or pgvector as a source of
truth for any entity governed by a NC constitution.

### Article 4 — The Four Constitutional Invariants

These four invariants are the governing constraints of this Constitution. They may not be
weakened by Director Decision, worker configuration, or API contract. They may only be
changed by constitutional amendment.

**Invariant P-1: The Projection Invariant.**
Neo4j and pgvector may contain only what PostgreSQL authorizes. A Neo4j node or
relationship, or a pgvector embedding, that has no corresponding record in PostgreSQL
is a constitutional violation. Projection workers must not create novel entities.

**Invariant P-2: The Availability Invariant.**
All platform functions except discovery enrichment must operate when Neo4j and pgvector
are unavailable. Any API endpoint that fails entirely when these layers are unavailable
(rather than falling back to PostgreSQL-only queries) violates this invariant.

**Invariant P-3: The Rebuild Invariant.**
A complete rebuild of Neo4j from PostgreSQL, and a complete rebuild of pgvector spaces
from PostgreSQL and MinIO, must be executable at any time by a Director Decision. The
rebuild produces state that is functionally equivalent to the pre-rebuild state. Workers
must be designed such that this rebuild is possible.

**Invariant P-4: The Score Gate Invariant.**
No relationship signal from Neo4j and no similarity signal from pgvector may enter the
NC commerce scoring pipeline (`commerce_opportunities`, `csm_score`, `commerce_opportunity_score`)
without a ratified amendment to the Commerce Intelligence Constitution. This invariant
cannot be relaxed by Director Decision alone.

---

## Part II — Relationship Intelligence Layer (Neo4j)

### Article 5 — Neo4j Governed Node Types

Each node type in Neo4j is a projection of a specific PostgreSQL table. The node type
vocabulary is constitutional. New node types require a constitutional amendment.

| Node Label | PostgreSQL source | Projection condition | Node identity key |
|---|---|---|---|
| `:Place` | `places` | `status = 'active'` | `places.id` |
| `:SourceItem` | `illustration_opportunities` / `source_items` | `status = 'activated'` | `id` |
| `:Creator` | `creator_authority_registry` | `governance_state = 'active'` | `creator_id` |
| `:Institution` | `sources` | `governance_state = 'active'` | `source_id` |
| `:MediaType` | `media_type_registry` | `status = 'active'` | `media_type_id` |
| `:SubjectTerm` | TGM vocabulary (from `media_technical_metadata.content.subject_terms`) | value present in any active SourceItem | `term_value` |
| `:Collection` | `collections` | `status = 'published'` | `collections.id` |
| `:Concept` | `concepts` | FK from a `biological` anchor SourceItem | `concepts.id` |

**5.1** Each node carries a projection metadata property set:

```
{
  pg_id: "...",           // PostgreSQL row UUID
  pg_table: "...",        // Source table name
  schema_version: "...",  // Projection schema version (from projection_schema_registry)
  projected_at: "..."     // Timestamp of last projection
}
```

**5.2** If a PostgreSQL row that is projected into Neo4j is subsequently modified, the
corresponding Neo4j node must be updated or removed in the next projection cycle. A node
that reflects a deleted PostgreSQL row is a Invariant P-1 violation.

**5.3** Only `status = 'activated'` SourceItems are projected. SourceItems in `proposed`,
`acquired`, `rights_verified`, or `activation_eligible` status are substrate-layer entities
and are not visible in the relationship layer.

### Article 6 — Neo4j Governed Relationship Types

Each relationship type in Neo4j is derived from a specific PostgreSQL table, column, or
governed derivation rule. The relationship vocabulary is constitutional.

| Relationship | From → To | PostgreSQL derivation | Key properties |
|---|---|---|---|
| `[:LOCATED_IN]` | `:Place → :Place` | `places.continent`, country hierarchy | `level` (continent/country/region) |
| `[:PROXIMATE_TO]` | `:Place ↔ :Place` | PostGIS `ST_Distance` on `places.centroid`, ≤ 500km | `distance_km` |
| `[:SHARES_CRITERIA]` | `:Place ↔ :Place` | Overlap in `places.ouv_criteria` arrays | `shared_criteria: []` |
| `[:SAME_HERITAGE_TYPE]` | `:Place ↔ :Place` | `places.heritage_type` equality | `heritage_type` |
| `[:DEPICTS]` | `:SourceItem → :Place` | `illustration_opportunity_places` | `relevance_score`, `link_type` |
| `[:CREATED_BY]` | `:SourceItem → :Creator` | `illustration_opportunities.illustrator` (authority-resolved) | `era` |
| `[:HELD_BY]` | `:SourceItem → :Institution` | `illustration_opportunities.source` | `source_id` |
| `[:OF_TYPE]` | `:SourceItem → :MediaType` | `media_type` field | — |
| `[:TAGGED]` | `:SourceItem → :SubjectTerm` | `media_technical_metadata.content.subject_terms` | `vocabulary: 'tgm'` |
| `[:DEPICTS_TAXON]` | `:SourceItem → :Concept` | `illustration_opportunities.concept_id` (biological only) | `anchor_type: 'biological'` |
| `[:IN_COLLECTION]` | `:SourceItem → :Collection` | `collection_assets.opportunity_id` | `sequence`, `role` |
| `[:FEATURES]` | `:Collection → :Place` | `collection_places` | `role` (primary/supporting) |
| `[:CONTEMPORARY_WITH]` | `:Creator ↔ :Creator` | Derived: era year overlap ≥ 10 years | `overlap_years` |
| `[:ASSOCIATED_WITH]` | `:Creator → :Institution` | Derived: Institution holds ≥ 3 SourceItems by this Creator | `item_count` |

**6.1** Derived relationships (`[:PROXIMATE_TO]`, `[:CONTEMPORARY_WITH]`, `[:ASSOCIATED_WITH]`,
`[:SHARES_CRITERIA]`, `[:SAME_HERITAGE_TYPE]`) are computed by projection workers, not
by a worker reading a specific FK. Their derivation rule is part of this article and is
constitutional. Changing the derivation rule (e.g., changing the proximity radius from
500km, or the contemporary era overlap threshold) requires a constitutional amendment.

**6.2** Derived relationships do not claim to be authoritative facts — they are traversal
aids. Whenever a derived relationship is surfaced in an API response, the response must
include `derived: true` and `derivation_rule` identifying the governing article and rule.

**6.3** The relationship vocabulary is governed by a no-DELETE-from-vocabulary rule. Retired
relationship types are marked `status = 'retired'` in the `projection_schema_registry`.
Retired types stop being projected but are not removed from existing nodes until a full
rebuild.

### Article 7 — Neo4j Schema Registry

**7.1** Every distinct version of the Neo4j node and relationship type vocabulary is
registered in a PostgreSQL table `projection_schema_registry`. This table is the authority
for what version of the graph schema is currently active.

**7.2** Required fields per schema version:

| Field | Governance requirement |
|---|---|
| `schema_id` | Canonical identifier. Immutable. |
| `schema_version` | Semantic version string (e.g., `1.0.0`). |
| `node_types` | JSONB array of governed node labels. |
| `relationship_types` | JSONB array of governed relationship types with derivation rules. |
| `status` | `pending` → `active` → `retired`. |
| `constitutional_ref` | The amendment authorizing this version. |
| `activated_by` | Second-human approval required for `status = 'active'`. |
| `activated_at` | Timestamp of activation. |

**7.3** Only one schema version may have `status = 'active'` at a time.

**7.4** When a schema version is activated, all existing Neo4j nodes and relationships
projected under a prior version must be rebuilt under the new schema before the old version
is marked `retired`. A partial rebuild (new relationships alongside old) is not permitted.

### Article 8 — Traversal Query Boundary

**8.1** Traversal queries against Neo4j are permitted for the following use cases:
discovery enrichment, related-content suggestions, creator network exploration, and
place relationship surfacing.

**8.2** Traversal queries against Neo4j are not permitted as the sole source for the
following: rights status, activation status, commerce score, product eligibility,
collection membership (canonical), or any other governed entity state. These must be
read from PostgreSQL.

**8.3** Any API response that combines traversal results (from Neo4j) with canonical
state (from PostgreSQL) must label the provenance of each field. Fields derived from
Neo4j traversal must carry `source: 'relationship_layer'` in the response metadata.
Fields derived from PostgreSQL must carry `source: 'authority'`.

---

## Part III — Semantic Intelligence Layer (pgvector)

### Article 9 — pgvector Model Registry

**9.1** The embedding model used to generate any vector space in NC is a governed entity.
Every model must be registered before any embedding it generates may be stored. The model
registry is a PostgreSQL table `pgvector_model_registry`.

**9.2** Required fields per model registration:

| Field | Governance requirement |
|---|---|
| `model_id` | Canonical identifier. Immutable (e.g., `text-embedding-3-small-1536`). |
| `provider` | The model provider (e.g., `openai`, `cohere`, `sentence-transformers`). |
| `dimension` | Vector dimension. Immutable once `status = 'active'`. |
| `status` | `pending` → `active` → `retired`. |
| `activation_director_decision` | DD-X reference. Director Decision required before `status = 'active'`. |
| `activated_at` | Timestamp of activation. |
| `retired_at` | Timestamp of retirement, if applicable. |
| `rebuild_required_on_retirement` | Boolean. If TRUE, all spaces using this model must be rebuilt when it retires. |

**9.3** A model may not be activated (`status = 'active'`) without a Director Decision
(Article 25). A model change is not a minor operational decision — it changes the semantic
space and makes all existing embeddings incomparable. A model activation Director Decision
must explicitly acknowledge that a full rebuild of affected vector spaces will be required.

**9.4** The model registry is governed by a no-DELETE rule. Retired models are marked
`status = 'retired'`. The row is never removed. Retired model IDs are permanently reserved.

### Article 10 — pgvector Governed Vector Spaces

Each vector space is a named, governed collection of embeddings for a specific use case.
The vector space vocabulary is constitutional. New spaces require a constitutional amendment.

| Space name | Source entity | Embedding input | Use case |
|---|---|---|---|
| `source_item_semantic` | SourceItem (activated only) | `title \|\| subject_terms \|\| publication_title \|\| taxon_name \|\| primary_place_names` | Asset-to-asset semantic similarity; search-to-asset matching |
| `place_semantic` | Place (active only) | `ouv_statement \|\| description \|\| heritage_type \|\| continent \|\| top_subject_terms` | Place-to-place thematic similarity; search-to-place matching |
| `story_semantic` | Story (NC-authored, published only) | `title \|\| body_text_summary` | Story-to-asset similarity (future) |

**10.1** The `story_semantic` space is a future space. It is registered here but must not
be populated until NC-authored stories exist in production. Its registration does not
authorize implementation.

**10.2** Each embedding record must carry:

```
{
  pg_id: "...",            // PostgreSQL row UUID of the source entity
  pg_table: "...",         // Source PostgreSQL table
  model_id: "...",         // FK to pgvector_model_registry.model_id
  schema_version: "...",   // FK to projection_schema_registry.schema_version
  source_hash: "...",      // SHA-256 of the input text, to detect content staleness
  embedded_at: "..."       // Timestamp
}
```

**10.3** An embedding whose `source_hash` does not match the current SHA-256 of the
same input text is stale and must be refreshed in the next projection cycle.

**10.4** An embedding for an entity that no longer satisfies its projection condition
(e.g., a SourceItem whose `status` changed from `activated` to `retracted`) must be
deleted in the next projection cycle. This is the only permitted deletion in the pgvector
layer.

### Article 11 — Semantic Query Boundary

**11.1** Semantic similarity queries (approximate nearest-neighbor search) are permitted
for the following use cases: discovery enrichment, "similar to this item" suggestions,
semantic search result ranking, and editorial recommendation support.

**11.2** Semantic similarity queries are not permitted as a scoring signal in the commerce
pipeline without a Commerce Intelligence Constitution amendment (Invariant P-4).

**11.3** Any API response that includes semantic similarity results must label each result:
`similarity_source: 'semantic_layer'`, `model_id`, `schema_version`. Users and downstream
consumers must be able to determine which model produced the result.

**11.4** Semantic similarity results are advisory. They must never be used to override,
replace, or suppress a PostgreSQL-authoritative classification (rights status, quality tier,
activation status, collection membership).

---

## Part IV — Projection Rules

### Article 12 — Projection Doctrine

**12.1** Projection is the process by which PostgreSQL state is transformed into Neo4j
graph state or pgvector embedding state. Projection is one-directional: PostgreSQL → Neo4j,
PostgreSQL → pgvector. There is no reverse projection path. Neo4j and pgvector do not write
to PostgreSQL.

**12.2** Projection workers are the only authorized agents for writing to Neo4j and pgvector.
No human, API endpoint, or other worker may write to Neo4j or pgvector directly. All writes
to these layers are mediated by projection workers.

**12.3** Projection workers must validate that every entity they project has a corresponding
active record in PostgreSQL before writing to Neo4j or pgvector. A projection worker that
writes an entity absent from PostgreSQL is a constitutional violation.

**12.4** Projection is not real-time by constitutional requirement. A projection latency
period of up to 15 minutes is acceptable for operational projection cycles. Longer latency
requires a worker alert. Latency exceeding 24 hours triggers a Director notification.

### Article 13 — Projection Event Records

**13.1** Every projection cycle — full rebuild or incremental update — must produce a
`projection_event` record in PostgreSQL. This is the provenance record for the projection
layer.

**13.2** Required fields per projection event:

| Field | Governance requirement |
|---|---|
| `projection_event_id` | UUID. PostgreSQL authority. |
| `layer` | `neo4j` or `pgvector`. |
| `space_or_schema` | Space name (pgvector) or schema version (Neo4j). |
| `event_type` | `full_rebuild` / `incremental_update` / `stale_refresh` / `deletion`. |
| `entities_projected` | Count of nodes/embeddings written. |
| `entities_deleted` | Count of nodes/embeddings removed. |
| `schema_version` | Active schema version at projection time. |
| `model_id` | Active model at projection time (pgvector only; NULL for Neo4j). |
| `worker_id` | Identity of the projection worker. |
| `started_at` | Timestamp. |
| `completed_at` | Timestamp. |
| `outcome` | `success` / `partial` / `failure`. |
| `error_detail` | JSONB. NULL on success. |

**13.3** The `projection_event` table is append-only. No UPDATE or DELETE is permitted.

**13.4** A `partial` or `failure` outcome triggers a worker alert and must be visible to
the human operator. A `failure` that persists across two consecutive projection cycles
triggers a Director notification.

### Article 14 — Projection Currency

**14.1** "Currency" is the measure of how closely Neo4j and pgvector reflect the current
state of PostgreSQL. Full currency means zero stale entities. Operational currency means
all stale entities are within the projection latency period.

**14.2** The following PostgreSQL events must trigger an incremental projection update
within the governed latency period:

| PostgreSQL event | Neo4j impact | pgvector impact |
|---|---|---|
| `source_item.status → 'activated'` | Add `:SourceItem` node and all relationships | Add to `source_item_semantic` space |
| `source_item.status → 'retracted'` | Remove `:SourceItem` node and all its relationships | Delete from `source_item_semantic` space |
| `collection.status → 'published'` | Add `:Collection` node and `[:IN_COLLECTION]` relationships | — |
| `collection.status → 'retracted'` | Remove `:Collection` node | — |
| `place.status → 'active'` | Add `:Place` node and location relationships | Add to `place_semantic` space |
| `creator_authority_registry` INSERT with `governance_state = 'active'` | Add `:Creator` node | — |
| `media_technical_metadata` update (subject_terms changed) | Update `[:TAGGED]` relationships | Refresh `source_item_semantic` embedding |
| `illustration_opportunity_places` INSERT | Add/update `[:DEPICTS]` relationship | — |

**14.3** No incremental projection event triggers a full rebuild. A full rebuild is
triggered only by: schema version change (Article 7.4), model change (Article 9.3),
Rebuild Protocol execution (Articles 19-20), or Director Decision.

---

## Part V — Replayability

### Article 15 — Replay Requirements for Relationship-Derived Signals

**15.1** If a relationship traversal result (Neo4j) is used to inform a discovery workflow
(e.g., a suggested `bhl_search_target` generated by traversing creator relationships), the
traversal path must be recorded in the relevant entity's `provenance` or `agent_notes` JSONB:

```json
{
  "relationship_traversal": {
    "query": "Cypher query or query type label",
    "schema_version": "...",
    "traversal_depth": 2,
    "result_count": 14,
    "traversal_at": "..."
  }
}
```

**15.2** If a relationship traversal result is used in any scoring computation that produces
a value stored in `commerce_opportunities`, the traversal metadata (schema_version, result
count, traversal rule) must be stored in `commerce_opportunities.score_inputs`. This rule
applies only if the Score Gate Invariant (P-4) is lifted by a CI Constitution amendment.

**15.3** A replay that reconstructs a past scoring decision must be able to reproduce the
same relationship traversal result using only PostgreSQL (via recursive CTEs substituting
for Neo4j), given the same PostgreSQL state at the time of the original computation.

### Article 16 — Replay Requirements for Semantic Similarity Signals

**16.1** If a semantic similarity result (pgvector) is used in any scoring computation,
the following must be stored in `commerce_opportunities.score_inputs` at scoring time:

```json
{
  "semantic_similarity": {
    "model_id": "...",
    "schema_version": "...",
    "space_name": "...",
    "query_entity_id": "...",
    "similarity_score": 0.84,
    "ranked_position": 3,
    "embedded_at": "..."
  }
}
```

**16.2** A replay that must reconstruct a past similarity-based scoring decision must be
able to: (a) identify the model used from `score_inputs.semantic_similarity.model_id`;
(b) confirm whether that model is still active or has been retired; (c) if retired,
acknowledge that the embedding space has changed and the similarity result is not exactly
reproducible, and record this as a replay caveat. Replay caveats do not invalidate the
original decision but must be flagged in audit output.

**16.3** This is the one replayability exception in NC's governance: embedding similarity
is not perfectly reproducible after a model change. The governing response is to record
the model version at scoring time and acknowledge the caveat on replay — not to prohibit
model changes.

---

## Part VI — Rebuild Requirements

### Article 17 — Rebuild Requirements for Neo4j

**17.1** The rebuild protocol for Neo4j is:

```
1. Director Decision recorded in PostgreSQL (project_events or equivalent)
2. Neo4j graph is cleared (all nodes and relationships)
3. Projection worker reads all projection-eligible entities from PostgreSQL
4. Projection worker writes all nodes under the current schema_version
5. Projection worker writes all relationships under the current schema_version
6. Projection worker writes all derived relationships (PROXIMATE_TO, etc.)
   using the current derivation rules
7. projection_event record written: event_type = 'full_rebuild', outcome = 'success'
8. Director notified of completion
```

**17.2** The rebuild is idempotent. Running the full rebuild protocol twice produces the
same Neo4j state. No UUID or identity values in Neo4j may change between rebuild runs for
the same PostgreSQL row.

**17.3** During a rebuild, the platform continues operating. Discovery enrichment returns
empty/degraded results (Invariant P-2). A `degraded_mode` flag is set in the application
layer and visible to users as: "Enhanced discovery is temporarily unavailable."

**17.4** A rebuild must complete within 12 hours for a production-scale dataset. If it
does not complete within 12 hours, the Director is notified and the partial result is
discarded — a fresh full rebuild begins.

### Article 18 — Rebuild Requirements for pgvector

**18.1** The rebuild protocol for pgvector is:

```
1. Director Decision recorded, specifying: which space(s), which model, reason
2. The target vector space is cleared
3. Embedding worker reads projection-eligible entities from PostgreSQL
4. For each entity: construct the governed input text (Article 10)
5. Compute embedding using the active model (pgvector_model_registry.model_id)
6. Store embedding with full metadata (pg_id, model_id, schema_version, source_hash)
7. projection_event record written: event_type = 'full_rebuild', outcome = 'success'
8. Director notified
```

**18.2** A model change (new model activation) triggers a full rebuild of all spaces that
used the prior model. The rebuild must be complete before the prior model is marked
`status = 'retired'`. A model and its dependent spaces may not be in different version
states simultaneously (new model active + old model's embeddings in production = violation).

**18.3** The rebuild is idempotent. The same input text + same model + same model version
produces the same embedding. Source hash verification (Article 10.3) confirms this.

**18.4** During a rebuild, semantic search returns no results or degraded results. The
platform continues operating. A `degraded_mode` flag is set per Article 17.3.

---

## Part VII — Human Governance

### Article 19 — Stack Activation Gate

**19.1** Before Neo4j or pgvector may be deployed to any environment (development,
staging, or production), Director Decision SD-AMEND-1 must be recorded (see Precondition).

**19.2** Initial deployment of Neo4j requires:
- SD-AMEND-1 recorded
- `projection_schema_registry` initial entry created (schema version 1.0.0)
- Second-human approval of the initial schema version
- Full rebuild protocol executed in staging before production deployment
- Director sign-off that staging rebuild completed successfully

**19.3** Initial deployment of pgvector requires:
- SD-AMEND-1 recorded
- Initial embedding model registered in `pgvector_model_registry`
- Director Decision authorizing the model (SD-AMEND-1 may include this, or a separate DD)
- Full rebuild of all initial vector spaces completed in staging
- Director sign-off

### Article 20 — Schema Amendment Gate (Neo4j)

**20.1** A Neo4j schema amendment is any of the following:
- Adding a new node label
- Adding a new relationship type
- Changing the derivation rule for an existing relationship
- Changing the `projection_condition` for an existing node type

**20.2** All of the above require:
- A constitutional amendment to this Constitution
- A new schema version entry in `projection_schema_registry`
- Second-human approval of the new schema version
- Full rebuild of Neo4j under the new schema version

**20.3** Changing the properties stored on existing nodes or relationships (not their
vocabulary, just their JSONB content) does not require a constitutional amendment — it
requires a schema version update (new version, backward-compatible) and a projection event.

### Article 21 — Embedding Model Change Gate (pgvector)

**21.1** A model change is the activation of a new `pgvector_model_registry` entry with a
different `dimension` or `provider` than the currently active model.

**21.2** All model changes require:
- Director Decision recorded in PostgreSQL
- Full rebuild of all affected vector spaces (Article 18)
- Confirmation that no scoring signal (Article 16) is actively using the prior model
  in the production scoring pipeline
- Mark prior model `status = 'retired'` only after rebuild is confirmed complete

**21.3** A model change for operational reasons (same provider, patch version, same
dimension) may be authorized by Director Decision alone. A model change to a different
provider or dimension is a substantial semantic space shift and requires Director Decision
plus an acknowledgment that past replay caveats (Article 16.2) will increase.

### Article 22 — Score Gate Approval (Invariant P-4 Lift)

**22.1** Lifting Invariant P-4 — allowing a Neo4j or pgvector signal to enter the commerce
scoring pipeline — is the most consequential governance action in this Constitution.

**22.2** Lifting Invariant P-4 requires:
- A ratified amendment to the Commerce Intelligence Constitution naming the specific signal
- The signal must be described with its weight in the scoring formula
- The replay requirements of Article 15 or 16 must be confirmed implemented before scoring
  begins
- Second-human approval of the first scoring run that uses the new signal
- Director Decision authorizing the lift, referencing the CI Constitution amendment

**22.3** A signal approved for scoring under one CI Constitution version is not
automatically approved under a subsequent version. Each CI Constitution version that
includes a relationship or semantic signal requires a new lift authorization.

### Article 23 — Worker Authority Boundaries

**23.1** Projection workers are authorized to:
- Read from PostgreSQL (all governed entities)
- Read from MinIO (content for embedding generation)
- Write nodes and relationships to Neo4j
- Write embeddings to pgvector
- Delete stale or retracted entities from Neo4j and pgvector
- Write `projection_event` records to PostgreSQL

**23.2** Projection workers are not authorized to:
- Write to any PostgreSQL table other than `projection_event`
- Override canonical state in PostgreSQL
- Create new Neo4j node types or relationship types not in the current `projection_schema_registry`
- Use an embedding model not active in `pgvector_model_registry`
- Execute a full rebuild without a Director Decision (incremental updates are worker-authorized; full rebuilds require Director authorization)

**23.3** The second-human rule applies to all Director Decisions in this Constitution.
A Director may not approve their own decision records.

---

## Part VIII — Reference Model Alignment

### Article 24 — Reference Models: Adopted Governance Rules

NC formally adopts the following governance principles from each reference model.

**24.1 — Google Knowledge Graph**

Adopted: Entity-centric graph model. Every governed entity in NC (Place, SourceItem, Creator,
Institution) corresponds to a canonical node with a stable, immutable identifier. Relationships
between entities are typed and explicitly governed. The "entity with facts" model directly
governs the `:Place`, `:SourceItem`, and `:Creator` node definitions in Article 5.

Rejected: Automatic fact extraction from external web sources without human review. NC's
graph contains only relationships derivable from governed PostgreSQL state. NC does not extract
new relational claims from external sources and project them without human authorization.

**24.2 — Wikidata**

Adopted: Stable entity identifiers as graph node keys. NC's `places.wikidata_qid` and
`taxon_candidates.wikidata_qid` are Wikidata entity references. These identifiers are the
canonical link between NC's graph and external knowledge systems. Wikidata QID links are
surfaced in Neo4j `:Place` and `:Concept` nodes as `wikidata_qid` properties.

Adopted: Open data linking philosophy. NC's graph schema is designed for potential future
federation with external knowledge graphs via shared identifiers.

Rejected: Community-edited authority model. NC's graph is governed by constitutional
authority and human approval. Wikidata's open-editing model does not apply.

**24.3 — Smithsonian**

Adopted: Object-relationship network model for cultural heritage. Smithsonian's approach to
linking physical objects across collections, creators, and geographies informs NC's
`[:CREATED_BY]`, `[:HELD_BY]`, and `[:DEPICTS]` relationship types.

Adopted: Institutional authority as a graph property. The `:Institution` node and
`[:HELD_BY]` relationship model Smithsonian's multi-institution relationship pattern.

Rejected: Internal collection management system relationships (accession numbers, storage
locations, condition notes). NC's graph represents discoverable commercial relationships,
not institutional inventory management.

**24.4 — Europeana**

Adopted: Cross-institutional aggregation relationship model. The EDM `ore:Aggregation`
pattern (source_item aggregates source_record + media_file) is reflected in the `:SourceItem`
node's `[:HELD_BY]` and provenance structure.

Adopted: EDM's `edm:isRelatedTo` concept informs the `[:SIMILAR_TO]` relationship pattern
(reserved for future constitutional amendment — not in the v1.0 relationship vocabulary).

Rejected: Full EDM entity model. Europeana's `edm:Agent`, `edm:Event`, and `edm:PhysicalThing`
entity types are not projected into Neo4j. NC maps these to W3C PROV (Media Substrate
Constitution v1.2, Article 22) not to dedicated graph nodes.

**24.5 — Library of Congress**

Adopted: Authority file concept for creator nodes. The `:Creator` node model follows LOC's
creator authority file philosophy: one canonical node per creator, with controlled identity
resolution. The `creator_authority_registry` in PostgreSQL is the authority file. Neo4j
projects it.

Adopted: Subject thesaurus as graph traversal vocabulary. The `:SubjectTerm` node and
`[:TAGGED]` relationship implement LOC's TGM subject-term linking, enabling graph traversal
from asset to subject term to other assets.

Rejected: Full MARC authority file relationships. LOC's authority relationships (broader term /
narrower term / related term hierarchies for LCSH) are not projected into Neo4j in v1.0.
This is a future amendment if subject hierarchy traversal becomes a discovery requirement.

**24.6 — Amazon Recommendation Systems**

Adopted: Item-to-item content similarity model. Amazon's item-based collaborative filtering
principle — "customers who viewed X also viewed Y" — informs the `source_item_semantic`
vector space design. NC adapts this to content-based similarity (shared subject terms,
place, era, creator) rather than behavioral similarity (no user history at launch).

Adopted: Recommendation as a discovery enrichment layer, not a mandatory navigation element.
Amazon's recommendation system is advisory. NC's semantic similarity results are likewise
advisory and do not constrain or redirect user navigation.

Rejected: Behavioral tracking and purchase-history personalization. NC does not track user
behavior as a scoring or recommendation input. User privacy is preserved: discovery
enrichment is content-based, not behavior-based.

Rejected: A/B testing of recommendation algorithms as a production governance mechanism.
NC's recommendation signals are constitutionally governed. Changes require amendment, not
experiment.

**24.7 — Palantir**

Adopted: Provenance on every relationship edge. Palantir's ontology model requires that
every edge in the knowledge graph carry provenance (source, confidence, timestamp). NC's
`projected_at`, `schema_version`, and `pg_id` properties on every Neo4j node implement
this principle. Every relationship is traceable to a PostgreSQL row.

Adopted: Versioned ontology as a governance primitive. Palantir's ontology versioning
pattern directly informs NC's `projection_schema_registry` (Article 7).

Rejected: Access-control tiering within the graph (Palantir's security model marks some
nodes and edges as restricted to specific users or roles). NC's graph contains only
activated, publicly available assets. Internal governance state (rights evidence, scoring
signals) lives in PostgreSQL, not in Neo4j.

Rejected: Temporal edge versioning (Palantir tracks when a relationship was true vs.
false over time). NC's approach is simpler: a relationship either exists or does not in
the current projection. Historical projection state is captured in `projection_event`
records, not in edge versioning.

**24.8 — NASA Knowledge Systems**

Adopted: Versioned schema governance. NASA's mission data management model — where the
schema version governing a dataset is always recorded alongside the data — is the basis
for `projection_schema_registry` and the `schema_version` property required on every
Neo4j node and pgvector embedding.

Adopted: Full rebuild as a normal operational tool, not a catastrophe response. NASA's
data pipeline governance treats full reprocessing of a dataset as routine when input data
or processing logic changes. NC treats full rebuild of Neo4j and pgvector spaces the same
way: routine, governed, and automated.

Rejected: Telemetry-oriented and sensor-fusion data models. NASA's graph systems are
designed for continuous sensor data and mission telemetry. NC's knowledge graph is
asset-centered and change-sparse. Real-time sensor integration patterns do not apply.

### Article 25 — Governance Rules Explicitly Rejected

**25.1 — No projection system may be a write path for canonical state.** Regardless of
what any reference model does with its graph or embedding system, NC's canonical state
lives exclusively in PostgreSQL. This is the governing constraint that overrides all
reference model patterns.

**25.2 — No autonomous relationship creation.** Reference models that allow autonomous
extraction of new relationships from external sources (Google KG, Wikidata) inform NC's
entity model but not its relationship creation model. All relationships in Neo4j must be
derivable from existing PostgreSQL data. A worker may not traverse the web, parse external
sources, or call external APIs to create new relationships without a constitutional
amendment and Director Decision.

**25.3 — No behavioral personalization.** Amazon's recommendation model includes user
behavior tracking. NC does not track user behavior for discovery or recommendation purposes.
The semantic layer is content-based. This prohibition is permanent and may not be lifted
by Director Decision — it requires a constitutional amendment with explicit rationale for
why user behavior tracking aligns with NC's mission.

**25.4 — No relationship or similarity score in commerce without CI amendment.** This
repeats Invariant P-4 as an explicit rejection: no reference model's recommendation or
similarity pattern may enter the commerce scoring pipeline without a ratified CI Constitution
amendment. This is the most important commercial governance boundary in this document.

---

## Open Questions

| OQ | Question | Recommended resolution |
|---|---|---|
| OQ-1 | What is the correct Neo4j deployment model — embedded (within the FastAPI container), managed service, or separate Docker Compose service? | Separate Docker Compose service, consistent with the frozen stack constraint. Neo4j Community Edition is Docker-deployable without external dependencies. A separate `neo4j` service in `docker-compose.yml` is the correct deployment. This is an implementation decision requiring Director approval (SD-AMEND-1). |
| OQ-2 | Which embedding model should be the initial registered model in `pgvector_model_registry`? | This is a Director Decision (part of SD-AMEND-1 or a separate DD). Candidates: `text-embedding-3-small` (OpenAI, 1536-dim, cost-efficient), `all-MiniLM-L6-v2` (sentence-transformers, 384-dim, self-hosted). The self-hosted option preserves stack independence. Both are valid. The Director Decision must name the specific model and commit to a rebuild plan. |
| OQ-3 | Should `[:SIMILAR_TO]` (SourceItem → SourceItem) be a Neo4j relationship or a pgvector query result? | pgvector. Score-based structural similarity (shared subject terms, place, creator, era) belongs in Neo4j as `[:TAGGED]` and `[:DEPICTS]` traversal. Embedding-based semantic similarity belongs in pgvector. The two are additive: "structurally similar" (Neo4j traversal) + "semantically similar" (pgvector) are different signals. `[:SIMILAR_TO]` as a Neo4j relationship would require a derivation rule that is already better served by pgvector. Reserve `[:SIMILAR_TO]` for a future amendment if structural similarity needs its own relationship type. |
| OQ-4 | How should the `projection_event` table relate to the `preservation_event` table in the Media Substrate Constitution? | They are separate tables with different purposes. `preservation_event` governs file lifecycle in MinIO. `projection_event` governs projection operations to Neo4j and pgvector. They should not be merged. Both are append-only. The `projection_event` table is governed by this Constitution; `preservation_event` is governed by the Media Substrate Constitution. |
