# v0.5.0 Commerce Intelligence Build Order

## Mission

Execution plan for building the Commerce Intelligence Runtime after architecture
freeze.

This is planning only. It does not implement migrations, schemas, routers,
workers, tests, or Mission Control integration.

Authoritative inputs:

- `docs/governance/commerce_intelligence_constitution_v1.md`
- `docs/architecture/commerce_intelligence_runtime_v1.md`
- existing PostgreSQL authority model
- existing FastAPI governance gateway pattern
- existing worker and replay-test pattern

## Build Principles

1. PostgreSQL lands before application code.
2. Governed vocabularies and policy rows land before scoring workers.
3. Audit protection lands before any write path can generate scores.
4. SQLAlchemy and Pydantic mirror PostgreSQL constraints; they do not invent
   alternate vocabularies.
5. FastAPI can review and trigger work, but workers compute.
6. Replay tests must pass before workers are considered activatable.
7. Mission Control is visibility and review, not authority.

## Build Order Summary

| Order | Workstream | Complexity | Activation Gate |
|---:|---|---|---|
| 1 | PostgreSQL migrations | High | Schema, vocabularies, policies, audit protections replay cleanly |
| 2 | SQLAlchemy models | Medium | Models reflect DB constraints and relationships |
| 3 | Pydantic schemas | Medium | Request/response contracts reject invalid vocabularies |
| 4 | FastAPI routers | Medium | Governance endpoints write audit and enforce reviewer identity |
| 5 | Workers | High | Deterministic scoring with no direct API dependency |
| 6 | Replay workers | High | Recompute and hash-chain verification work from fixtures |
| 7 | Tests | High | Unit, API, migration, replay, and governance tests pass |
| 8 | Mission Control integration | Medium | Review queues and stale/audit views expose DB state |

## Phase 1: PostgreSQL Migrations

Complexity: High

### 1.1 Add Migration File

Create:

```text
infrastructure/postgres/init/19_commerce_intelligence_runtime.sql
```

Scope:

- additive schema only
- no destructive edits to upstream asset, opportunity, or collection tables
- no worker activation

Complexity: Low

### 1.2 Seed Governed Vocabularies

Add explicit reference rows or governed checks for constitution vocabularies:

- `policy_status`
- `commerce_tier`
- `hard_gate_status`
- `computation_trigger`
- `curator_decision`
- `curator_review_reason`
- `recommendation_status`
- `collection_gap_type`
- `audit_event_type`
- `actor_type`
- required signal vocabularies such as `taxon_commercial_tier`,
  `color_profile`, `resolution_tier`, `place_tier`, and `anchor_type`

Build rule:

- absence of required scoring vocabulary must block scoring, not ingestion.

Complexity: Medium

### 1.3 Create `commerce_policy`

Create the authoritative runtime scoring policy table.

Must support:

- policy key and semantic version
- formula specification
- score weights
- hard gates
- status lifecycle
- approver fields
- effective dates
- provenance

Initial statuses should follow the Constitution vocabulary:

```text
draft, pending_approval, active, superseded, retired
```

Complexity: Medium

### 1.4 Create `commerce_opportunities`

Create scored commercial state for one upstream opportunity or asset anchor.

Must store:

- upstream identifiers
- commerce tier
- hard gate status
- score inputs
- score outputs
- input hash
- policy version reference
- curator decision fields
- staleness fields
- provenance

Build rule:

- rights gates must be enforced at DB and worker level.
- ambiguous rights must not pass.

Complexity: High

### 1.5 Create `product_recommendations`

Create derived product-surface routing for curator review.

Must store:

- parent commerce opportunity
- product family and type
- provider/channel recommendation
- recommendation status
- score inputs and outputs
- generation constraints
- curator decision fields
- staleness fields

Build rule:

- no product recommendation can be generated from blocked or stale commerce
  opportunities.

Complexity: Medium

### 1.6 Create `collection_recommendations`

Create derived collection placement recommendations.

Must store:

- place/concept/collection anchors
- candidate opportunity IDs
- candidate asset IDs
- gap type
- recommendation status
- score inputs and outputs
- curator decision fields
- staleness fields

Build rule:

- collection recommendations do not create collections automatically.

Complexity: Medium

### 1.7 Create `score_audit_log`

Create append-only audit table.

Must include:

- event type
- entity type and ID
- policy version ID
- trigger
- actor type and actor ID
- score inputs
- score outputs
- input hash
- previous entry checksum
- entry checksum
- event timestamp
- actor notes where required

Complexity: High

### 1.8 Add Audit Protection

Add database-level protections:

- no `UPDATE` on `score_audit_log`
- no `DELETE` on `score_audit_log`
- hash-chain fields
- checksum verification support
- role privilege separation plan

Build rule:

- audit protection must be in place before scoring workers are enabled.

Complexity: High

### 1.9 Add Indexes and Triggers

Add:

- status and score indexes
- upstream anchor indexes
- policy version indexes
- staleness indexes
- audit entity and event indexes
- updated-at triggers on mutable tables

Do not add updated-at trigger to append-only audit rows.

Complexity: Medium

### 1.10 Seed Draft Policies

Seed draft or pending policies:

- `commerce-opportunity:v1`
- `product-recommendation:v1`
- `collection-recommendation:v1`

Build rule:

- policies stay non-active until replay tests pass.

Complexity: Low

## Phase 2: SQLAlchemy Models

Complexity: Medium

### 2.1 Add Model Module

Create:

```text
services/api/models/commerce.py
```

or follow the existing project model location if a different pattern is present
at implementation time.

Models:

- `CommercePolicy`
- `CommerceOpportunity`
- `ProductRecommendation`
- `CollectionRecommendation`
- `ScoreAuditLog`

Complexity: Low

### 2.2 Encode Relationships

Relationships:

- policy to scored records
- commerce opportunity to product recommendations
- upstream IDs as explicit UUID fields
- audit log by polymorphic entity type and entity ID

Build rule:

- do not use ORM cascade delete for audit records.

Complexity: Medium

### 2.3 Mirror Constraints

Model layer must reflect:

- governed status values
- recommendation status values
- actor types
- audit event types
- numeric score bounds
- required JSON fields

Complexity: Medium

## Phase 3: Pydantic Schemas

Complexity: Medium

### 3.1 Add Schema Module

Create:

```text
schemas/core/commerce_intelligence.py
```

Schemas:

- `CommercePolicyRead`
- `CommerceOpportunityRead`
- `ProductRecommendationRead`
- `CollectionRecommendationRead`
- `ScoreAuditLogRead`
- governance action requests
- worker trigger requests

Complexity: Low

### 3.2 Add Governed Enums

Enums should match the Constitution exactly.

Required enum groups:

- policy status
- commerce tier
- hard gate status
- computation trigger
- curator decision
- recommendation status
- collection gap type
- audit event type
- actor type

Complexity: Medium

### 3.3 Add Governance Request Schemas

Requests:

- approve
- reject
- escalate
- mark stale
- manual recompute
- signal update
- override curator decision

Required fields:

- actor ID
- actor type
- reason
- notes where required

Complexity: Medium

### 3.4 Add Public and Admin Response Shapes

Public shape:

- approved or curator-approved records only
- no internal score snapshots unless explicitly public-safe

Admin shape:

- full score inputs
- score outputs
- audit references
- staleness reasons
- replay status

Complexity: Medium

## Phase 4: FastAPI Routers

Complexity: Medium

### 4.1 Add Router Module

Create:

```text
services/api/routers/commerce.py
```

Register it in:

```text
services/api/main.py
```

Complexity: Low

### 4.2 Read Endpoints

Endpoints:

```text
GET /commerce/policies
GET /commerce/policies/{policy_id}
GET /commerce/opportunities
GET /commerce/opportunities/{id}
GET /commerce/product-recommendations
GET /commerce/product-recommendations/{id}
GET /commerce/collection-recommendations
GET /commerce/collection-recommendations/{id}
GET /commerce/score-audit-log
GET /commerce/score-audit-log/{entity_type}/{entity_id}
```

Complexity: Medium

### 4.3 Governance Endpoints

Endpoints:

```text
POST /commerce/opportunities/{id}/review
POST /commerce/product-recommendations/{id}/review
POST /commerce/collection-recommendations/{id}/review
POST /commerce/opportunities/{id}/mark-stale
POST /commerce/product-recommendations/{id}/mark-stale
POST /commerce/collection-recommendations/{id}/mark-stale
```

Build rule:

- each governance mutation writes `score_audit_log`.
- FastAPI validates actor type and reviewer identity.

Complexity: High

### 4.4 Worker Trigger Endpoints

Endpoints:

```text
POST /commerce/evaluate/opportunity/{opportunity_id}
POST /commerce/evaluate/asset/{asset_id}
POST /commerce/evaluate/collection/{collection_id}
POST /commerce/recompute/stale
POST /commerce/recompute/policy/{policy_id}
```

Build rule:

- endpoint queues work; it does not compute synchronously unless explicitly in a
  replay/test mode.

Complexity: Medium

### 4.5 API Filtering and Pagination

Filters:

- status
- policy version
- place ID
- concept ID
- collection ID
- opportunity ID
- product family
- stale reason
- minimum score
- event type

Complexity: Medium

## Phase 5: Workers

Complexity: High

### 5.1 Add Worker Package

Create:

```text
workers/commerce_intelligence_worker/
```

Modules:

- `config.py`
- `main.py`
- `policy.py`
- `score.py`
- `store.py`
- `staleness.py`
- `audit.py`

Complexity: Medium

### 5.2 Implement Policy Loader

Responsibilities:

- load one active policy per scoring domain
- fail closed if no active policy exists
- fail closed if multiple active policies exist without explicit scope
- expose formula spec and weight map

Complexity: Medium

### 5.3 Implement Score Engine

Responsibilities:

- normalize authoritative inputs
- derive signal vocabulary values
- apply hard gates
- compute score inputs
- compute score outputs
- produce deterministic input hash
- round scores consistently

Complexity: High

### 5.4 Implement Commerce Opportunity Scoring

Inputs:

- upstream illustration opportunities
- assets
- asset rights
- place relevance
- source provenance

Outputs:

- `commerce_opportunities`
- `score_audit_log`

Complexity: High

### 5.5 Implement Product Recommendation Scoring

Inputs:

- non-stale commerce opportunities
- product profile policy
- provider/channel policy
- QA policy

Outputs:

- `product_recommendations`
- `score_audit_log`

Complexity: High

### 5.6 Implement Collection Recommendation Scoring

Inputs:

- commerce opportunities
- existing collections
- portfolio gaps
- place/concept grouping

Outputs:

- `collection_recommendations`
- `score_audit_log`

Complexity: High

### 5.7 Implement Staleness Detection

Detect changes in:

- rights
- asset status
- asset derivative or checksum
- opportunity status
- place relevance
- collection membership
- policy version
- worker version
- provider/channel/QA/pricing policy

Outputs:

- mark records stale
- write audit event
- enqueue recompute

Complexity: High

### 5.8 Add Worker Entry Point

Modes:

- evaluate opportunity
- evaluate asset
- evaluate collection
- recompute stale
- recompute policy
- verify audit chain

Complexity: Medium

## Phase 6: Replay Workers

Complexity: High

### 6.1 Add Replay Worker Mode

Replay mode must:

- use pinned fixtures
- use pinned policy versions
- avoid live provider calls
- avoid wall-clock-dependent scoring except stored timestamps
- compare exact score outputs

Complexity: Medium

### 6.2 Add Input Hash Replay

Assertions:

- same fixture and same policy produce same input hash
- changed rights fixture changes hash
- changed policy fixture changes hash or policy reference

Complexity: Medium

### 6.3 Add Audit Chain Replay

Assertions:

- audit entries are append-only
- `previous_entry_checksum` matches prior entry
- tampered entry fails verification
- replay worker writes `replay_verified` or `replay_failure`

Complexity: High

### 6.4 Add Staleness Replay

Assertions:

- rights change marks dependent rows stale
- policy change marks dependent rows stale
- stale rows cannot drive product recommendations
- replacement rows can supersede stale rows

Complexity: High

## Phase 7: Tests

Complexity: High

### 7.1 Migration Tests

Add replay tests for:

- all five tables exist
- constraints exist
- status vocabularies enforced
- score bounds enforced
- audit table blocks update and delete
- required indexes exist

Complexity: Medium

### 7.2 Model Tests

Add tests for:

- ORM mapping
- JSON fields
- relationships
- enum/value validation where applicable

Complexity: Medium

### 7.3 Pydantic Schema Tests

Add tests for:

- invalid status rejection
- invalid actor type rejection
- missing review reason rejection
- public/admin response shape separation

Complexity: Medium

### 7.4 FastAPI Tests

Add tests for:

- list endpoints
- detail endpoints
- governance review endpoints
- worker trigger endpoints
- audit log write on mutation
- stale records excluded from actionable responses

Complexity: High

### 7.5 Worker Unit Tests

Add tests for:

- hard gates
- scoring formulas
- score rounding
- input hash determinism
- policy loader failure modes
- staleness detection
- audit event creation

Complexity: High

### 7.6 Replay Tests

Add tests under:

```text
tests/replay/
```

Suggested files:

```text
test_migration_019_commerce_intelligence_runtime.py
test_milestone_050_commerce_policy.py
test_milestone_050_commerce_scoring.py
test_milestone_050_commerce_replay.py
test_milestone_050_score_audit_log.py
test_milestone_050_staleness.py
```

Complexity: High

### 7.7 Integration Tests

Add tests for:

- API to PostgreSQL state
- worker to PostgreSQL state
- replay worker verification
- Mission Control read model compatibility

Complexity: High

## Phase 8: Mission Control Integration

Complexity: Medium

### 8.1 Add Commerce Intelligence Queues

Mission Control views:

- pending commerce opportunities
- pending product recommendations
- pending collection recommendations
- stale recommendation queue
- audit integrity alerts
- policy activation queue

Complexity: Medium

### 8.2 Add Review Surfaces

Each review surface should show:

- score
- tier
- hard gate status
- score inputs
- score outputs
- active policy version
- replay/audit status
- curator decision controls

Complexity: Medium

### 8.3 Add Staleness and Supersession Views

Views:

- stale by reason
- stale by policy version
- stale by upstream entity
- superseded lineage

Complexity: Medium

### 8.4 Add Audit Views

Views:

- audit event timeline per opportunity
- hash-chain status
- replay verification status
- suspected integrity failures

Complexity: High

### 8.5 Add Operational Metrics

Metrics:

- scored opportunities count
- hard-gate blocked count
- recommendation pending review count
- stale recommendation count
- replay failures
- audit integrity failures
- policy activation events

Complexity: Medium

## Recommended Milestone Cuts

### Cut 1: Schema and Governance Foundation

Includes:

- PostgreSQL migration
- seeded vocabularies
- draft policies
- audit protection
- migration replay tests

Complexity: High

Exit criteria:

- migration tests pass
- audit table cannot update or delete
- draft policies visible in PostgreSQL

### Cut 2: API Read and Governance Layer

Includes:

- SQLAlchemy models
- Pydantic schemas
- read endpoints
- review endpoints
- audit writes from FastAPI

Complexity: Medium

Exit criteria:

- API tests pass
- invalid vocabularies rejected
- review actions write audit log

### Cut 3: Scoring Workers

Includes:

- policy loader
- score engine
- commerce opportunity worker
- product recommendation worker
- collection recommendation worker

Complexity: High

Exit criteria:

- worker unit tests pass
- hard gates fail closed
- deterministic input hash confirmed

### Cut 4: Replay and Staleness

Includes:

- replay worker
- audit chain verification
- staleness worker
- recompute strategy
- replay tests

Complexity: High

Exit criteria:

- same inputs reproduce same scores
- policy changes mark stale
- audit tampering fails verification

### Cut 5: Mission Control

Includes:

- review queues
- stale queues
- audit timeline
- policy activation visibility
- operational metrics

Complexity: Medium

Exit criteria:

- curators can see pending, stale, rejected, approved, and superseded records
- audit integrity status is visible
- no Mission Control action bypasses FastAPI governance

## Dependency Order

```text
PostgreSQL migration
    ↓
Migration replay tests
    ↓
SQLAlchemy models
    ↓
Pydantic schemas
    ↓
FastAPI read endpoints
    ↓
FastAPI governance endpoints
    ↓
Audit log write path
    ↓
Policy loader
    ↓
Score engine
    ↓
Commerce opportunity worker
    ↓
Product recommendation worker
    ↓
Collection recommendation worker
    ↓
Staleness worker
    ↓
Replay worker
    ↓
Full replay tests
    ↓
Mission Control integration
```

## Activation Checklist

Before activating v0.5.0 scoring:

- PostgreSQL migration replay passes.
- governed vocabularies are seeded.
- exactly one active policy exists per scoring domain.
- audit table is append-only and checksum protected.
- rights gates are tested.
- score formulas are deterministic.
- stale records are excluded from downstream action.
- FastAPI review endpoints require actor identity and reason.
- replay worker verifies hash chain.
- Mission Control displays pending review and audit integrity state.

## Complexity Rollup

| Area | Complexity | Reason |
|---|---|---|
| PostgreSQL migrations | High | Five governed entities, vocabularies, hard gates, audit immutability, hash chain |
| SQLAlchemy models | Medium | Mostly direct mapping, but audit and policy relationships need care |
| Pydantic schemas | Medium | Governed enums and admin/public separation |
| FastAPI routers | Medium | CRUD is simple; review/audit semantics add risk |
| Workers | High | Deterministic scoring, fail-closed gates, policy loading, recompute |
| Replay workers | High | Hash-chain verification and stale/superseded replay |
| Tests | High | Cross-layer governance and determinism coverage |
| Mission Control | Medium | Mostly read/review surfaces, but audit integrity UI is sensitive |

## Non-Goals

This build plan does not include:

- Shopify product creation
- Etsy listing publication
- Gelato, Printful, or Lulu ordering
- product generation plans
- AI-generated copy
- new upstream rights normalization
- mutation of existing asset or collection governance rules
