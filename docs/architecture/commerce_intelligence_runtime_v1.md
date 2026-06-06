# v0.5.0 Commerce Intelligence Runtime Design

## Mission

Design the v0.5.0 Commerce Intelligence Runtime for Nature & Culture.

This document is architecture only. It does not implement migrations, routers,
workers, or tests.

Commerce Intelligence decides what is worth making. It does not create Shopify
products, publish Etsy listings, submit fulfillment orders, mutate source rights,
or approve collections automatically.

## Commerce Intelligence Constitution

1. PostgreSQL is authoritative for all commerce intelligence state.
2. Recommendations are derived, versioned, explainable, and replayable.
3. Source records, rights records, assets, collections, and governance facts remain
   authoritative inputs; commerce intelligence never rewrites them.
4. Public-domain and CC0 rights gates are non-overridable for commercial activation.
5. AI may enrich, rank, or draft rationale, but humans approve consequential actions.
6. Every score must carry policy version, worker version, score components, input
   snapshot, input hash, and audit log evidence.
7. Stale recommendations are preserved for audit but cannot drive downstream product
   generation.
8. Regeneration creates new derived records or marks records stale/superseded; it
   does not silently mutate historical scoring evidence.

## Runtime Scope

Designed tables:

- `commerce_policy`
- `commerce_opportunities`
- `score_audit_log`
- `product_recommendations`
- `collection_recommendations`

Existing upstream authorities:

- `assets`
- `asset_rights`
- `illustration_opportunities`
- `illustration_opportunity_places`
- `illustration_opportunity_assets`
- `collections`
- `collection_assets`
- `collection_places`
- `collection_product_profiles`, when introduced by the product profile runtime

Downstream consumers:

- product generation plan workers
- Shopify catalog sync
- Etsy syndication
- provider routing

## PostgreSQL Schema

The schema is additive. No v0.5.0 commerce intelligence table should replace the
existing asset, opportunity, collection, or rights tables.

### commerce_policy

`commerce_policy` is the versioned scoring and gating contract. It allows replay
to prove that the same inputs under the same policy produce the same score.

```sql
CREATE TABLE commerce_policy (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_key          TEXT NOT NULL,
    policy_version      TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'draft',
    applies_to          TEXT NOT NULL,
    rules               JSONB NOT NULL DEFAULT '{}',
    score_weights       JSONB NOT NULL DEFAULT '{}',
    gates               JSONB NOT NULL DEFAULT '{}',
    reviewer_policy     JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_by          TEXT NOT NULL,
    approved_by         TEXT,
    approved_at         TIMESTAMPTZ,
    effective_from      TIMESTAMPTZ,
    effective_until     TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_commerce_policy_status CHECK (
        status IN ('draft','approved','active','paused','retired')
    ),
    CONSTRAINT chk_commerce_policy_applies_to CHECK (
        applies_to IN (
            'commerce_opportunity',
            'product_recommendation',
            'collection_recommendation',
            'global'
        )
    ),
    UNIQUE (policy_key, policy_version)
);
```

### commerce_opportunities

`commerce_opportunities` are durable evaluations of commercial potential for an
asset, illustration opportunity, or collection.

```sql
CREATE TABLE commerce_opportunities (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_type               TEXT NOT NULL,
    subject_id                 UUID NOT NULL,
    place_id                   UUID,
    concept_id                 UUID,
    source                     TEXT NOT NULL,
    opportunity_type           TEXT NOT NULL,

    rights_status              TEXT NOT NULL,
    rights_readiness_score     NUMERIC(4,3) NOT NULL CHECK (rights_readiness_score BETWEEN 0 AND 1),
    visual_quality_score       NUMERIC(4,3) NOT NULL CHECK (visual_quality_score BETWEEN 0 AND 1),
    place_relevance_score      NUMERIC(4,3) NOT NULL CHECK (place_relevance_score BETWEEN 0 AND 1),
    provenance_score           NUMERIC(4,3) NOT NULL CHECK (provenance_score BETWEEN 0 AND 1),
    collection_fit_score       NUMERIC(4,3) NOT NULL CHECK (collection_fit_score BETWEEN 0 AND 1),
    commercial_value_score     NUMERIC(4,3) NOT NULL CHECK (commercial_value_score BETWEEN 0 AND 1),
    commerce_score             NUMERIC(4,3) NOT NULL CHECK (commerce_score BETWEEN 0 AND 1),

    status                     TEXT NOT NULL DEFAULT 'candidate',
    policy_id                  UUID NOT NULL REFERENCES commerce_policy(id),
    worker_version             TEXT NOT NULL,
    input_hash                 TEXT NOT NULL,
    score_components           JSONB NOT NULL DEFAULT '{}',
    input_snapshot             JSONB NOT NULL DEFAULT '{}',
    stale_reason               TEXT,
    superseded_by              UUID REFERENCES commerce_opportunities(id),
    provenance                 JSONB NOT NULL DEFAULT '{}',

    reviewed_by                TEXT,
    reviewed_at                TIMESTAMPTZ,
    rejection_reason           TEXT,
    override_reason            TEXT,

    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_commerce_opportunity_subject CHECK (
        subject_type IN ('asset','illustration_opportunity','collection')
    ),
    CONSTRAINT chk_commerce_opportunity_status CHECK (
        status IN ('candidate','recommended','approved','rejected','stale','superseded')
    ),
    CONSTRAINT chk_commerce_opportunity_rights CHECK (
        rights_status IN ('Public Domain','CC0')
    )
);
```

Recommended indexes:

```sql
CREATE INDEX idx_commerce_opportunities_status_score
    ON commerce_opportunities(status, commerce_score DESC);
CREATE INDEX idx_commerce_opportunities_subject
    ON commerce_opportunities(subject_type, subject_id);
CREATE INDEX idx_commerce_opportunities_place_score
    ON commerce_opportunities(place_id, commerce_score DESC);
CREATE INDEX idx_commerce_opportunities_concept_score
    ON commerce_opportunities(concept_id, commerce_score DESC);
CREATE INDEX idx_commerce_opportunities_policy
    ON commerce_opportunities(policy_id);
CREATE UNIQUE INDEX uniq_commerce_opportunity_active_input
    ON commerce_opportunities(subject_type, subject_id, policy_id, input_hash)
    WHERE status IN ('candidate','recommended','approved');
```

### product_recommendations

`product_recommendations` are concrete sellable product recommendations. They are
not generated products.

```sql
CREATE TABLE product_recommendations (
    id                                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    commerce_opportunity_id              UUID NOT NULL REFERENCES commerce_opportunities(id),
    collection_id                         UUID,
    asset_id                              UUID,
    opportunity_id                        UUID,

    product_family                        TEXT NOT NULL,
    product_type                          TEXT NOT NULL,
    provider_route                        TEXT,
    channel_policy                        JSONB NOT NULL DEFAULT '{}',

    product_family_fit_score              NUMERIC(4,3) NOT NULL CHECK (product_family_fit_score BETWEEN 0 AND 1),
    asset_product_fit_score               NUMERIC(4,3) NOT NULL CHECK (asset_product_fit_score BETWEEN 0 AND 1),
    expected_margin_score                 NUMERIC(4,3) NOT NULL CHECK (expected_margin_score BETWEEN 0 AND 1),
    provider_readiness_score              NUMERIC(4,3) NOT NULL CHECK (provider_readiness_score BETWEEN 0 AND 1),
    channel_fit_score                     NUMERIC(4,3) NOT NULL CHECK (channel_fit_score BETWEEN 0 AND 1),
    demand_signal_score                   NUMERIC(4,3) NOT NULL CHECK (demand_signal_score BETWEEN 0 AND 1),
    operational_complexity_score          NUMERIC(4,3) NOT NULL CHECK (operational_complexity_score BETWEEN 0 AND 1),
    recommendation_score                  NUMERIC(4,3) NOT NULL CHECK (recommendation_score BETWEEN 0 AND 1),

    generation_policy                     JSONB NOT NULL DEFAULT '{}',
    variant_plan                          JSONB NOT NULL DEFAULT '{}',
    qa_gates                              JSONB NOT NULL DEFAULT '{}',

    status                                TEXT NOT NULL DEFAULT 'candidate',
    policy_id                             UUID NOT NULL REFERENCES commerce_policy(id),
    worker_version                        TEXT NOT NULL,
    input_hash                            TEXT NOT NULL,
    score_components                      JSONB NOT NULL DEFAULT '{}',
    input_snapshot                        JSONB NOT NULL DEFAULT '{}',
    stale_reason                          TEXT,
    superseded_by                         UUID REFERENCES product_recommendations(id),
    provenance                            JSONB NOT NULL DEFAULT '{}',

    reviewed_by                           TEXT,
    reviewed_at                           TIMESTAMPTZ,
    rejection_reason                      TEXT,
    override_reason                       TEXT,

    created_at                            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_product_recommendation_status CHECK (
        status IN (
            'candidate','plan_ready','sample_required','approved',
            'rejected','generated','stale','superseded','retired'
        )
    )
);
```

Recommended indexes:

```sql
CREATE INDEX idx_product_recommendations_status_score
    ON product_recommendations(status, recommendation_score DESC);
CREATE INDEX idx_product_recommendations_opportunity
    ON product_recommendations(commerce_opportunity_id);
CREATE INDEX idx_product_recommendations_collection
    ON product_recommendations(collection_id, recommendation_score DESC);
CREATE INDEX idx_product_recommendations_family_score
    ON product_recommendations(product_family, recommendation_score DESC);
CREATE INDEX idx_product_recommendations_policy
    ON product_recommendations(policy_id);
```

### collection_recommendations

`collection_recommendations` recommend new collections, collection extensions,
campaign drops, bundles, or editorial campaigns.

```sql
CREATE TABLE collection_recommendations (
    id                               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id                         UUID,
    concept_id                       UUID,
    existing_collection_id           UUID,
    recommendation_type              TEXT NOT NULL,

    title                            JSONB NOT NULL DEFAULT '{}',
    rationale                        TEXT NOT NULL,
    candidate_asset_ids              UUID[] NOT NULL DEFAULT '{}',
    candidate_opportunity_ids        UUID[] NOT NULL DEFAULT '{}',

    thematic_coherence_score         NUMERIC(4,3) NOT NULL CHECK (thematic_coherence_score BETWEEN 0 AND 1),
    asset_depth_score                NUMERIC(4,3) NOT NULL CHECK (asset_depth_score BETWEEN 0 AND 1),
    rights_readiness_score           NUMERIC(4,3) NOT NULL CHECK (rights_readiness_score BETWEEN 0 AND 1),
    product_breadth_score            NUMERIC(4,3) NOT NULL CHECK (product_breadth_score BETWEEN 0 AND 1),
    editorial_value_score            NUMERIC(4,3) NOT NULL CHECK (editorial_value_score BETWEEN 0 AND 1),
    commerce_potential_score         NUMERIC(4,3) NOT NULL CHECK (commerce_potential_score BETWEEN 0 AND 1),
    provenance_score                 NUMERIC(4,3) NOT NULL CHECK (provenance_score BETWEEN 0 AND 1),
    collection_score                 NUMERIC(4,3) NOT NULL CHECK (collection_score BETWEEN 0 AND 1),

    recommended_product_families     JSONB NOT NULL DEFAULT '{}',

    status                           TEXT NOT NULL DEFAULT 'candidate',
    policy_id                        UUID NOT NULL REFERENCES commerce_policy(id),
    worker_version                   TEXT NOT NULL,
    input_hash                       TEXT NOT NULL,
    score_components                 JSONB NOT NULL DEFAULT '{}',
    input_snapshot                   JSONB NOT NULL DEFAULT '{}',
    stale_reason                     TEXT,
    superseded_by                    UUID REFERENCES collection_recommendations(id),
    provenance                       JSONB NOT NULL DEFAULT '{}',

    reviewed_by                      TEXT,
    reviewed_at                      TIMESTAMPTZ,
    rejection_reason                 TEXT,
    override_reason                  TEXT,

    created_at                       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_collection_recommendation_type CHECK (
        recommendation_type IN (
            'new_collection','extend_collection','seasonal_drop',
            'product_bundle','editorial_campaign'
        )
    ),
    CONSTRAINT chk_collection_recommendation_status CHECK (
        status IN (
            'candidate','recommended','approved','rejected',
            'converted_to_collection','stale','superseded'
        )
    )
);
```

Recommended indexes:

```sql
CREATE INDEX idx_collection_recommendations_status_score
    ON collection_recommendations(status, collection_score DESC);
CREATE INDEX idx_collection_recommendations_place_score
    ON collection_recommendations(place_id, collection_score DESC);
CREATE INDEX idx_collection_recommendations_concept_score
    ON collection_recommendations(concept_id, collection_score DESC);
CREATE INDEX idx_collection_recommendations_existing_collection
    ON collection_recommendations(existing_collection_id);
CREATE INDEX idx_collection_recommendations_policy
    ON collection_recommendations(policy_id);
```

### score_audit_log

`score_audit_log` is append-only evidence for score creation, recomputation,
staleness transitions, approvals, rejections, and overrides.

```sql
CREATE TABLE score_audit_log (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type         TEXT NOT NULL,
    entity_id           UUID NOT NULL,
    policy_id           UUID REFERENCES commerce_policy(id),
    worker_version      TEXT,
    score_name          TEXT NOT NULL,
    previous_score      NUMERIC(4,3),
    new_score           NUMERIC(4,3),
    previous_status     TEXT,
    new_status          TEXT,
    input_hash          TEXT,
    score_components    JSONB NOT NULL DEFAULT '{}',
    input_snapshot      JSONB NOT NULL DEFAULT '{}',
    reason              TEXT NOT NULL,
    generated_by        TEXT NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_score_audit_entity_type CHECK (
        entity_type IN (
            'commerce_opportunity',
            'product_recommendation',
            'collection_recommendation'
        )
    )
);
```

Recommended indexes:

```sql
CREATE INDEX idx_score_audit_log_entity
    ON score_audit_log(entity_type, entity_id, generated_at DESC);
CREATE INDEX idx_score_audit_log_policy
    ON score_audit_log(policy_id, generated_at DESC);
CREATE INDEX idx_score_audit_log_reason
    ON score_audit_log(reason, generated_at DESC);
```

## Migration Plan

Recommended migration name:

```text
19_commerce_intelligence_runtime.sql
```

Migration sequence:

1. Create `commerce_policy`.
2. Seed inactive or draft default policies:
   - `commerce-opportunity:v1`
   - `product-recommendation:v1`
   - `collection-recommendation:v1`
3. Create `commerce_opportunities`.
4. Create `product_recommendations`.
5. Create `collection_recommendations`.
6. Create `score_audit_log`.
7. Add indexes.
8. Add `set_updated_at` triggers for all mutable tables.
9. Add replay tests before activating worker writes.
10. Move default policies from `draft` to `active` only after replay proves
    deterministic outputs.

Rollback posture:

- Drop workers and API routes first.
- Preserve tables unless the migration is being reverted before any production
  scoring.
- If tables contain audit records, retire policies instead of deleting scoring
  history.

## Score Computation

All scores are rounded to three decimal places and bounded to `0.000` through
`1.000`.

### commerce_score

```text
commerce_score =
  0.24 * rights_readiness_score
+ 0.20 * visual_quality_score
+ 0.16 * place_relevance_score
+ 0.14 * provenance_score
+ 0.14 * collection_fit_score
+ 0.12 * commercial_value_score
```

Hard gates:

- `rights_status IN ('Public Domain','CC0')`
- source asset or opportunity exists
- source asset has provenance
- source media is usable
- parent opportunity, asset, and collection are not rejected, disputed, retracted,
  stale, or quarantined

`rights_readiness_score`:

- `1.000` for explicit `Public Domain` or `CC0` with evidence.
- no other value may enter commerce intelligence v1.

`visual_quality_score`:

- derived from dimensions, file integrity, print derivative presence, composition
  flags, and manual QA where available.

`place_relevance_score`:

- inherited from `illustration_opportunity_places`, collection-place links, or
  reviewed source mappings.

`provenance_score`:

- source URL, source record ID, checksum, preserved object, creator/date metadata,
  and worker provenance.

`collection_fit_score`:

- whether the subject fits an existing or candidate collection without duplication
  or weak theme matching.

### product recommendation score

```text
recommendation_score =
  0.20 * product_family_fit_score
+ 0.18 * asset_product_fit_score
+ 0.16 * expected_margin_score
+ 0.16 * provider_readiness_score
+ 0.12 * channel_fit_score
+ 0.10 * demand_signal_score
+ 0.08 * (1 - operational_complexity_score)
```

Hard gates:

- parent `commerce_opportunity` is not stale, rejected, or superseded
- product family is allowed by policy or an approved collection product profile
- provider route exists for the product type
- variant plan is within caps
- QA gates are defined
- product generation does not exceed collection or channel policy caps

### collection recommendation score

```text
collection_score =
  0.20 * thematic_coherence_score
+ 0.18 * asset_depth_score
+ 0.18 * rights_readiness_score
+ 0.14 * product_breadth_score
+ 0.14 * editorial_value_score
+ 0.12 * commerce_potential_score
+ 0.04 * provenance_score
```

Hard gates:

- at least one verified commercial asset
- clear place or concept relationship
- no unresolved rights conflict
- no duplicate of an existing published collection unless type is
  `extend_collection`

## Recompute Strategy

Every worker builds a normalized input snapshot and a deterministic `input_hash`.
The hash should include authoritative input IDs, important source fields, policy
version, and worker scoring version.

Recompute algorithm:

```text
load active policy
load authoritative inputs
build normalized input_snapshot
compute input_hash
find existing active record for subject/policy/input_hash
if found: no-op, optionally append heartbeat audit in replay mode
if same subject/policy but different hash: mark old record stale
compute new scores
insert new candidate or recommended record
append score_audit_log
if reviewer accepts replacement: set stale record superseded_by = new id
```

Regeneration triggers:

- rights status or rights evidence changes
- asset status changes
- asset media, checksum, derivative, or QA state changes
- illustration opportunity score or status changes
- place relevance changes
- collection membership changes
- collection lifecycle changes
- collection product profile changes
- provider route policy changes
- channel policy changes
- pricing or margin policy changes
- scoring policy version changes
- worker version changes

Manual overrides:

- do not become score inputs
- must be preserved in audit history
- must be reviewed again after regeneration if the underlying recommendation is
  stale

## Staleness Handling

Stale records are preserved and excluded from downstream generation.

Allowed stale reasons:

```text
rights_changed
asset_changed
asset_status_changed
asset_derivative_changed
opportunity_changed
place_relevance_changed
collection_changed
collection_status_changed
product_profile_changed
provider_policy_changed
pricing_policy_changed
qa_policy_changed
policy_changed
worker_version_changed
manual_review_required
```

Rules:

- `stale` records cannot be approved.
- `stale` product recommendations cannot be used by product generation.
- approved records that become stale require renewed approval on the regenerated
  record.
- a stale record becomes `superseded` only after a replacement exists.
- stale records with no valid replacement remain stale with a clear reason.
- stale transitions always write `score_audit_log`.

## Policy Version Strategy

Policy identity:

```text
{policy_key}:{policy_version}
```

Initial versions:

```text
commerce-opportunity:v1
product-recommendation:v1
collection-recommendation:v1
```

Worker versions:

```text
commerce_opportunity_worker:v0.5.0
product_recommendation_worker:v0.5.0
collection_recommendation_worker:v0.5.0
commerce_staleness_worker:v0.5.0
commerce_replay_worker:v0.5.0
```

Policy lifecycle:

```text
draft -> approved -> active -> paused -> retired
```

Rules:

- only one active policy per `applies_to` should exist unless a controlled A/B or
  backfill run explicitly scopes by policy ID.
- activating a new policy marks affected recommendations stale or queues
  regeneration.
- retired policies remain queryable for replay and audit.
- policy JSON must store score weights and hard gates so historical scores remain
  explainable without checking code history.

## FastAPI Routers

Recommended router:

```text
services/api/routers/commerce.py
```

Read endpoints:

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

Recommended filters:

```text
status
place_id
concept_id
collection_id
asset_id
subject_type
subject_id
product_family
product_type
policy_id
min_score
stale_reason
created_after
updated_after
```

Governance endpoints:

```text
POST /commerce/opportunities/{id}/approve
POST /commerce/opportunities/{id}/reject
POST /commerce/opportunities/{id}/mark-stale
POST /commerce/opportunities/{id}/override-score

POST /commerce/product-recommendations/{id}/approve
POST /commerce/product-recommendations/{id}/reject
POST /commerce/product-recommendations/{id}/mark-sample-required
POST /commerce/product-recommendations/{id}/mark-stale
POST /commerce/product-recommendations/{id}/override-score

POST /commerce/collection-recommendations/{id}/approve
POST /commerce/collection-recommendations/{id}/reject
POST /commerce/collection-recommendations/{id}/mark-stale
POST /commerce/collection-recommendations/{id}/override-score
```

Worker trigger endpoints:

```text
POST /commerce/evaluate/opportunity/{opportunity_id}
POST /commerce/evaluate/asset/{asset_id}
POST /commerce/evaluate/collection/{collection_id}
POST /commerce/regenerate/stale
POST /commerce/regenerate/policy/{policy_id}
```

Router rules:

- public APIs should expose approved or recommended non-stale records only.
- admin APIs may expose candidate, rejected, stale, superseded, and audit records.
- approval requires authenticated reviewer identity.
- rejection requires reason.
- score override requires reviewer identity, reason, and audit log record.
- no API endpoint may bypass rights gates.

## Worker Architecture

### commerce_opportunity_worker

Inputs:

- `illustration_opportunities`
- `illustration_opportunity_places`
- `illustration_opportunity_assets`
- `assets`
- `asset_rights`
- `collections`
- `collection_assets`

Responsibilities:

- discover commerce opportunity candidates
- apply rights and provenance hard gates
- compute `commerce_score`
- write `commerce_opportunities`
- write `score_audit_log`
- mark replaced records stale or superseded

### product_recommendation_worker

Inputs:

- approved or recommended `commerce_opportunities`
- collection product profiles
- provider route policy
- channel policy
- pricing policy
- QA policy

Responsibilities:

- produce product family and product type recommendations
- enforce family, type, variant, channel, and provider caps
- compute `recommendation_score`
- classify records as `candidate`, `plan_ready`, or `sample_required`
- never create Shopify products

### collection_recommendation_worker

Inputs:

- commerce opportunities grouped by place, concept, collection, source, period, or
  visual theme
- existing collections
- portfolio gaps
- campaign calendar, when available

Responsibilities:

- recommend new collections, collection extensions, seasonal drops, product
  bundles, and editorial campaigns
- compute `collection_score`
- avoid duplicate published collections
- write audit events for generated recommendations

### commerce_staleness_worker

Inputs:

- change events or polling deltas from upstream authoritative tables
- policy activation events
- worker version changes

Responsibilities:

- detect affected derived records
- mark records stale with reason
- queue recomputation
- append audit events

### commerce_replay_worker

Inputs:

- frozen replay fixtures
- active or pinned commerce policies

Responsibilities:

- recompute deterministic score fixtures
- assert expected statuses
- assert stale and superseded transitions
- assert audit log writes
- compare input hashes and score components

## Replay Tests

Replay tests should be added before activating worker writes.

Required replay cases:

1. valid public-domain asset creates a commerce opportunity.
2. CC0 asset creates a commerce opportunity.
3. missing rights blocks commerce opportunity creation.
4. `No known copyright restrictions` does not pass the v1 rights gate unless
   normalized upstream to `Public Domain` with evidence.
5. same input and same policy produce same score and same input hash.
6. changed policy marks existing recommendations stale.
7. changed asset checksum or derivative marks dependent recommendations stale.
8. changed collection membership marks dependent collection recommendations stale.
9. regeneration creates a new candidate and preserves old audit history.
10. stale product recommendation cannot be approved.
11. manual override requires reviewer and reason.
12. every score creation, status transition, stale mark, and override writes
    `score_audit_log`.

Replay fixtures:

- one verified BHL illustration opportunity
- one verified asset with `Public Domain`
- one verified asset with `CC0`
- one invalid asset with ambiguous rights
- one collection with enough assets for wall art and cards
- one collection with insufficient assets for books/calendars
- one policy update fixture
- one manual override fixture

## Audit Logging

Audit events are mandatory for:

- initial score creation
- score recomputation
- status transition
- stale transition
- supersession
- approval
- rejection
- sample-required transition
- manual score override
- policy activation

Audit `reason` examples:

```text
initial_score
recomputed_same_policy
policy_changed
rights_changed
asset_changed
status_approved
status_rejected
manual_override
marked_stale
superseded
```

Audit log should never be updated after insert except by administrative repair
under an explicit incident procedure.

## Governance Workflow

Opportunity lifecycle:

```text
candidate -> recommended -> approved
candidate -> rejected
recommended -> rejected
approved -> stale
stale -> superseded
```

Product recommendation lifecycle:

```text
candidate -> plan_ready -> approved
candidate -> sample_required -> approved
candidate/plan_ready/sample_required -> rejected
approved -> generated
approved/generated -> stale
stale -> superseded
generated -> retired
```

Collection recommendation lifecycle:

```text
candidate -> recommended -> approved -> converted_to_collection
candidate/recommended -> rejected
approved -> stale
stale -> superseded
```

Approval rules:

- rights gates are non-overridable.
- stale records cannot be approved.
- superseded records cannot be approved.
- product recommendations require a non-stale parent commerce opportunity.
- collection recommendations require all candidate assets to remain rights-valid.
- conversion from recommendation to collection is a separate governed action.

## Runtime Sequence Diagram

```text
Authoritative Inputs
  assets
  asset_rights
  illustration_opportunities
  collections
  collection_assets
        |
        v
commerce_opportunity_worker
  - load active commerce-opportunity policy
  - build input snapshot
  - compute input hash
  - apply hard gates
  - compute commerce_score
        |
        v
commerce_opportunities
score_audit_log
        |
        v
product_recommendation_worker
  - load active product-recommendation policy
  - load collection product profile and provider/channel policy
  - compute recommendation_score
  - enforce caps and QA gates
        |
        v
product_recommendations
score_audit_log
        |
        v
collection_recommendation_worker
  - group opportunities by place/concept/theme
  - compute collection_score
  - avoid duplicate published collections
        |
        v
collection_recommendations
score_audit_log
        |
        v
FastAPI Governance Gateway
  - approve
  - reject
  - mark stale
  - override with reason
        |
        v
Approved non-stale product recommendations
        |
        v
Downstream product generation plan
  - outside Commerce Intelligence Runtime
```

## Non-Goals

v0.5.0 Commerce Intelligence Runtime does not:

- create product generation plans
- create Shopify products
- publish products
- submit fulfillment jobs
- create Etsy listings
- infer rights beyond upstream verified values
- replace collection product profiles
- replace collection governance
- make AI output authoritative

## Launch Recommendation

Default posture for v0.5.0:

- `commerce-opportunity:v1`: active after replay passes.
- `product-recommendation:v1`: active in advisory mode.
- `collection-recommendation:v1`: active in advisory mode.
- all product recommendations default to manual or assisted governance.
- only approved, non-stale product recommendations may be consumed by downstream
  product planning.
