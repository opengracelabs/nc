# Migration 19-21 Final Specifications

## Mission

Ready-for-implementation executable specifications for Commerce Intelligence Migrations 19, 20, and 21 after Director Decisions in `docs/governance/commerce_intelligence_constitution_v1.1.md`.

This document is specification only. It does not create migration files and does not modify PostgreSQL.

## Director Decisions Applied

| Decision | Applied Result |
|---|---|
| B-1 | `score_audit_log` hybrid schema is deferred to Migration 22, not included in M19-21. Migration 21 only references the future audit requirement as a deferred replay gate. |
| B-2 | `commerce_policy.status` uses six states: `draft`, `pending_approval`, `active`, `paused`, `superseded`, `retired`. |
| B-3 | LOC source constraint amendment is mandatory before scoring. Migration 19 includes the `illustration_opportunities.source` amendment to allow `bhl` and `loc`. |
| B-4 | Role-level privilege separation is descoped for v0.5.0. No `CREATE ROLE`, `GRANT`, or `REVOKE` specifications appear in M19-21. |
| H-1 | Scoring is two-pass: Pass 1 COS with five model subscores; Pass 2 CSM advisory score and tier. |
| H-2 | `collection_fit_score` and `commercial_value_score` are not runtime columns. Migration 21 uses `museum_score`, `retail_score`, `publishing_score`, `tourism_score`, and `reference_score`. |
| D-1 | Input hash is SHA-256 lowercase hex over canonical JSON with alpha-sorted keys and JSON nulls retained. |
| D-2 | Staleness is polling-based using `commerce_opportunities.last_scored_at` and `commerce_policy.max_score_age_days`. |
| D-3/D-5 | `taxon_commercial_tier` and `place_iconic_taxa` are governed tables with independent lifecycle, not embedded policy JSONB. |

## Migration Boundaries

| Migration | File | Scope |
|---|---|---|
| 19 | `infrastructure/postgres/init/19_commerce_governed_vocabulary.sql` | Mandatory LOC source amendment plus governed vocabulary tables and seed rows. |
| 20 | `infrastructure/postgres/init/20_commerce_policy.sql` | `commerce_policy`, policy constraints, triggers, and draft v1.0.0 policy seed. |
| 21 | `infrastructure/postgres/init/21_commerce_opportunities.sql` | `commerce_opportunities`, COS/CSM runtime columns, staleness fields, indexes, and constraints. |

`score_audit_log` is Migration 22. `product_recommendations` and `collection_recommendations` are Migration 23. Do not include those tables in M19-21.

## Global Requirements

- Migrations are additive except for the required source-check replacement in Migration 19.
- PostgreSQL remains authoritative.
- All migrations must be idempotent where PostgreSQL supports it.
- Existing upstream tables must not be weakened except the approved `illustration_opportunities.source` expansion from `bhl` to `bhl | loc`.
- Workers remain disabled until M22 audit and replay requirements are complete.
- Replay tests must verify schema behavior, not just table existence.

## Migration 19: Governed Vocabulary and Source Amendment

### Purpose

Prepare Commerce Intelligence scoring inputs and remove the BHL-only source blocker so approved LOC illustration opportunities can be represented before scoring.

### Tables

#### Existing Table Amendment: `illustration_opportunities`

Required operation:

```sql
ALTER TABLE illustration_opportunities
    DROP CONSTRAINT IF EXISTS chk_illustration_opportunity_source;

ALTER TABLE illustration_opportunities
    ADD CONSTRAINT chk_illustration_opportunity_source CHECK (source IN ('bhl','loc'));
```

If the existing constraint name differs, the migration must first discover the actual check constraint name in implementation and drop that specific BHL-only check. The replay test must assert behavior, not the historical constraint name.

#### `commerce_policy_status_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_policy_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
draft
pending_approval
active
paused
superseded
retired
```

#### `commerce_tier_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_tier_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
tier_1
tier_2
tier_3
blocked
```

#### `commerce_csm_tier_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_csm_tier_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
strong
moderate
weak
blocked
```

CSM tier is advisory only. It must not drive product eligibility routing.

#### `commerce_hard_gate_status_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_hard_gate_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
passed
blocked_rights
blocked_resolution
blocked_quality
blocked_legal
not_evaluated
```

#### `commerce_computation_trigger_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_computation_trigger_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
initial
policy_version_change
signal_correction
manual_recompute
rights_update
```

#### `commerce_curator_decision_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_curator_decision_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
approved
rejected
pending
escalated
```

#### `commerce_curator_review_reason_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_curator_review_reason_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
priority_illustrator
boundary_case
manual_flag
rights_anomaly
none
```

#### `commerce_recommendation_status_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_recommendation_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
pending_curator_review
curator_approved
curator_rejected
assigned
retired
```

This vocabulary is seeded in Migration 19 but consumed by Migration 23.

#### `commerce_collection_gap_type_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_collection_gap_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
fills_gap
reinforces_strength
expands_coverage
flagship_anchor
none
```

This vocabulary is seeded in Migration 19 but consumed by Migration 23.

#### `commerce_audit_event_type_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_audit_event_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
score_computed
signal_updated
hard_gate_blocked
hard_gate_passed
curator_reviewed
tier_assigned
policy_applied
eligibility_updated
score_archived
replay_verified
replay_failure
```

This vocabulary is seeded in Migration 19 but consumed by Migration 22.

#### `commerce_actor_type_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_actor_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
system_worker
curator
policy_approver
administrator
```

This vocabulary is seeded in Migration 19 but consumed by Migration 22.

#### `taxon_commercial_tier_vocabulary`

Governed table with independent lifecycle.

```sql
CREATE TABLE IF NOT EXISTS taxon_commercial_tier_vocabulary (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    value          TEXT NOT NULL UNIQUE,
    description    TEXT NOT NULL,
    score          NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    status         TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by    TEXT NOT NULL,
    approved_by    TEXT,
    approved_at    TIMESTAMPTZ,
    provenance     JSONB NOT NULL DEFAULT '{}',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_taxon_commercial_tier_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);
```

Seed proposed values:

```text
high
moderate
low
none
```

#### `priority_illustrators_vocabulary`

Governed table with independent lifecycle.

```sql
CREATE TABLE IF NOT EXISTS priority_illustrators_vocabulary (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_name TEXT NOT NULL UNIQUE,
    display_name   TEXT NOT NULL,
    prestige_score NUMERIC(4,3) NOT NULL CHECK (prestige_score BETWEEN 0 AND 1),
    status         TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by    TEXT NOT NULL,
    approved_by    TEXT,
    approved_at    TIMESTAMPTZ,
    provenance     JSONB NOT NULL DEFAULT '{}',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_priority_illustrator_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);
```

Seed proposed names:

```text
Audubon
Gould
Merian
Redoute
Lear
Nodder
Haeckel
Wolf
```

#### `commerce_place_tier_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_place_tier_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    score       NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
unesco_flagship
national_park
regional
local
none
```

#### `place_iconic_taxa_vocabulary`

Governed table with independent lifecycle. This replaces the earlier non-governed `place_iconic_taxa` table name.

```sql
CREATE TABLE IF NOT EXISTS place_iconic_taxa_vocabulary (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id        UUID NOT NULL REFERENCES places(id),
    concept_id      UUID REFERENCES concepts(id),
    scientific_name TEXT NOT NULL,
    common_name     TEXT,
    iconic_score    NUMERIC(4,3) NOT NULL CHECK (iconic_score BETWEEN 0 AND 1),
    status          TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by     TEXT NOT NULL,
    approved_by     TEXT,
    approved_at     TIMESTAMPTZ,
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_place_iconic_taxa_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    ),
    UNIQUE (place_id, scientific_name)
);
```

Yellowstone must have at least five proposed entries before scoring activation, but activation is a governed event after migration.

#### `commerce_color_profile_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_color_profile_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    score       NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
hand_colored
chromolithograph
bw_engraving
photographic
unknown
```

#### `commerce_resolution_tier_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_resolution_tier_vocabulary (
    value        TEXT PRIMARY KEY,
    description  TEXT NOT NULL,
    min_width_px INT,
    score        NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    sort_order   INT NOT NULL UNIQUE
);
```

Seed values:

```text
premium
standard
marginal
blocked
```

#### `commerce_anchor_type_vocabulary`

```sql
CREATE TABLE IF NOT EXISTS commerce_anchor_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);
```

Seed values:

```text
biological
geographic
cultural
```

### Indexes

```sql
CREATE INDEX IF NOT EXISTS idx_taxon_commercial_tier_status
    ON taxon_commercial_tier_vocabulary(status, value);

CREATE INDEX IF NOT EXISTS idx_priority_illustrators_status
    ON priority_illustrators_vocabulary(status, canonical_name);

CREATE INDEX IF NOT EXISTS idx_place_iconic_taxa_place_status
    ON place_iconic_taxa_vocabulary(place_id, status, iconic_score DESC);

CREATE INDEX IF NOT EXISTS idx_place_iconic_taxa_concept
    ON place_iconic_taxa_vocabulary(concept_id)
    WHERE concept_id IS NOT NULL;
```

### Constraints

- `illustration_opportunities.source` must accept `bhl` and `loc` and reject any other value.
- Governed rows with `status = 'active'` require `approved_by`, `approved_at`, and a second human distinct from `authored_by`.
- Vocabulary values are stable primary keys or unique keys.
- Scores are bounded to `0..1`.
- `place_iconic_taxa_vocabulary` enforces uniqueness by `(place_id, scientific_name)`.

### Triggers

```sql
CREATE TRIGGER trg_taxon_commercial_tier_updated_at
    BEFORE UPDATE ON taxon_commercial_tier_vocabulary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_priority_illustrators_updated_at
    BEFORE UPDATE ON priority_illustrators_vocabulary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_place_iconic_taxa_updated_at
    BEFORE UPDATE ON place_iconic_taxa_vocabulary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

### Replay Requirements

Replay file:

```text
tests/replay/test_migration_019_commerce_governed_vocabulary.py
```

Assertions:

1. `illustration_opportunities.source` accepts `bhl`.
2. `illustration_opportunities.source` accepts `loc`.
3. `illustration_opportunities.source` rejects any other value.
4. All required vocabulary tables exist.
5. All required seed values exist.
6. `commerce_policy_status_vocabulary` contains exactly the six approved policy states.
7. `taxon_commercial_tier_vocabulary` active rows require second-human approval.
8. `priority_illustrators_vocabulary` active rows require second-human approval.
9. `place_iconic_taxa_vocabulary` active rows require second-human approval.
10. Duplicate `(place_id, scientific_name)` iconic taxa rows are rejected.
11. Score fields in governed tables reject values outside `0..1`.

## Migration 20: Commerce Policy

### Purpose

Create the PostgreSQL-authoritative scoring policy table. Policy governs workers and API behavior. Policy activation is not part of this migration.

### Tables

#### `commerce_policy`

```sql
CREATE TABLE IF NOT EXISTS commerce_policy (
    id                           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version                      TEXT NOT NULL UNIQUE,
    status                       TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value),
    effective_from               TIMESTAMPTZ,
    effective_until              TIMESTAMPTZ,
    authored_by                  TEXT NOT NULL,
    approved_by                  TEXT,
    approved_at                  TIMESTAMPTZ,
    changelog                    TEXT NOT NULL,
    previous_version_id          UUID REFERENCES commerce_policy(id),
    max_score_age_days           INT NOT NULL DEFAULT 90 CHECK (max_score_age_days > 0),

    formula_spec                 JSONB NOT NULL,
    composite_weights            JSONB NOT NULL,
    tier_thresholds              JSONB NOT NULL,
    hard_gate_values             JSONB NOT NULL,
    model_activation_thresholds  JSONB NOT NULL,
    product_surface_requirements JSONB NOT NULL,

    provenance                   JSONB NOT NULL DEFAULT '{}',
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_commerce_policy_approval_identity CHECK (
        approved_by IS NULL OR approved_by IS DISTINCT FROM authored_by
    ),
    CONSTRAINT chk_commerce_policy_approved_status CHECK (
        status NOT IN ('active','paused','superseded')
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)
    ),
    CONSTRAINT chk_commerce_policy_effective_window CHECK (
        effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from
    )
);
```

Seed one draft row:

```text
version = '1.0.0'
status = 'draft'
max_score_age_days = 90
changelog = 'Initial Commerce Intelligence policy.'
```

`formula_spec` must explicitly define:

- Pass 1 COS computation using five model subscores.
- Pass 2 CSM advisory computation using six commercial success dimensions.
- Input hash canonicalization: SHA-256, lowercase hex, alpha-sorted JSON keys, JSON nulls retained.
- Staleness config with `poll_interval_hours`, default 24.

### Indexes

```sql
CREATE UNIQUE INDEX IF NOT EXISTS uniq_commerce_policy_one_active
    ON commerce_policy((status))
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_commerce_policy_status
    ON commerce_policy(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_policy_previous_version
    ON commerce_policy(previous_version_id)
    WHERE previous_version_id IS NOT NULL;
```

### Constraints

- `version` is unique.
- `status` references six-state vocabulary.
- At most one policy can be `active`.
- `active`, `paused`, and `superseded` policies require approval metadata.
- `approved_by` must differ from `authored_by`.
- `max_score_age_days` must be positive.
- Effective date windows must be valid.

### Triggers

#### Updated At

```sql
CREATE TRIGGER trg_commerce_policy_updated_at
    BEFORE UPDATE ON commerce_policy
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

#### Immutability Trigger

Specification:

```text
Function: enforce_commerce_policy_immutability()
Table: commerce_policy
Timing: BEFORE UPDATE
When OLD.status IN ('active','paused','superseded')
Reject changes to:
  version
  authored_by
  formula_spec
  composite_weights
  tier_thresholds
  hard_gate_values
  model_activation_thresholds
  product_surface_requirements
  max_score_age_days
Effect: RAISE EXCEPTION
```

#### Activation Trigger

Specification:

```text
Function: enforce_commerce_policy_activation()
Table: commerce_policy
Timing: BEFORE INSERT OR UPDATE
Rules when NEW.status = 'active':
  approved_by IS NOT NULL
  approved_at IS NOT NULL
  approved_by IS DISTINCT FROM authored_by
  effective_from IS NOT NULL
  no other row has status = 'active'
Effect: RAISE EXCEPTION on violation
```

### Replay Requirements

Replay file:

```text
tests/replay/test_migration_020_commerce_policy.py
```

Assertions:

1. `commerce_policy` exists.
2. Draft v1.0.0 policy exists.
3. Invalid status is rejected.
4. Two active policies cannot coexist.
5. Active policy without approver is rejected.
6. Active policy with same author and approver is rejected.
7. `paused` and `superseded` policies require approval metadata.
8. `max_score_age_days <= 0` is rejected.
9. Active policy formula and threshold fields are immutable.
10. Draft policy formula fields remain editable.
11. `formula_spec` contains both COS and CSM pass definitions.
12. `formula_spec` contains the D-1 input hash canonicalization specification.

## Migration 21: Commerce Opportunities

### Purpose

Create the runtime scoring state table for Commerce Intelligence. This migration stores both Pass 1 COS and Pass 2 CSM outputs, but workers remain disabled until Migration 22 audit logging exists.

### Tables

#### `commerce_opportunities`

```sql
CREATE TABLE IF NOT EXISTS commerce_opportunities (
    id                                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id                      UUID NOT NULL UNIQUE REFERENCES illustration_opportunities(id),
    policy_version_id                   UUID NOT NULL REFERENCES commerce_policy(id),
    computed_at                         TIMESTAMPTZ NOT NULL,
    computed_by                         TEXT NOT NULL,
    computation_trigger                 TEXT NOT NULL REFERENCES commerce_computation_trigger_vocabulary(value),
    policy_stale                        BOOLEAN NOT NULL DEFAULT FALSE,
    last_scored_at                      TIMESTAMPTZ,

    hard_gate_status                    TEXT NOT NULL REFERENCES commerce_hard_gate_status_vocabulary(value),

    rights_confidence                   NUMERIC(4,3) CHECK (rights_confidence BETWEEN 0 AND 1),
    golden_age_factor                   NUMERIC(4,3) CHECK (golden_age_factor BETWEEN 0 AND 1),
    institutional_credit                NUMERIC(4,3) CHECK (institutional_credit BETWEEN 0 AND 1),
    provenance_completeness             NUMERIC(4,3) CHECK (provenance_completeness BETWEEN 0 AND 1),
    resolution_tier_score               NUMERIC(4,3) CHECK (resolution_tier_score BETWEEN 0 AND 1),
    place_relevance_score               NUMERIC(4,3) CHECK (place_relevance_score BETWEEN 0 AND 1),
    place_tier_score                    NUMERIC(4,3) CHECK (place_tier_score BETWEEN 0 AND 1),

    illustrator_prestige                NUMERIC(4,3) CHECK (illustrator_prestige BETWEEN 0 AND 1),
    taxon_commercial_tier               TEXT,
    taxon_commercial_tier_score         NUMERIC(4,3) CHECK (taxon_commercial_tier_score BETWEEN 0 AND 1),
    taxon_place_iconic                  NUMERIC(4,3) CHECK (taxon_place_iconic BETWEEN 0 AND 1),

    image_quality_score                 NUMERIC(4,3) CHECK (image_quality_score BETWEEN 0 AND 1),
    image_quality_reviewed_by           TEXT,
    image_quality_reviewed_at           TIMESTAMPTZ,
    composition_fit                     NUMERIC(4,3) CHECK (composition_fit BETWEEN 0 AND 1),
    identification_confidence           NUMERIC(4,3) CHECK (identification_confidence BETWEEN 0 AND 1),
    color_profile                       TEXT REFERENCES commerce_color_profile_vocabulary(value),
    color_score                         NUMERIC(4,3) CHECK (color_score BETWEEN 0 AND 1),

    image_width_px                      INT CHECK (image_width_px IS NULL OR image_width_px >= 0),
    resolution_tier                     TEXT REFERENCES commerce_resolution_tier_vocabulary(value),

    museum_score                        NUMERIC(4,3) CHECK (museum_score BETWEEN 0 AND 1),
    retail_score                        NUMERIC(4,3) CHECK (retail_score BETWEEN 0 AND 1),
    publishing_score                    NUMERIC(4,3) CHECK (publishing_score BETWEEN 0 AND 1),
    tourism_score                       NUMERIC(4,3) CHECK (tourism_score BETWEEN 0 AND 1),
    reference_score                     NUMERIC(4,3) CHECK (reference_score BETWEEN 0 AND 1),

    commerce_opportunity_score          NUMERIC(4,3) CHECK (commerce_opportunity_score BETWEEN 0 AND 1),
    commerce_tier                       TEXT REFERENCES commerce_tier_vocabulary(value),

    csm_score                           NUMERIC(4,3) CHECK (csm_score BETWEEN 0 AND 1),
    csm_tier                            TEXT REFERENCES commerce_csm_tier_vocabulary(value),

    eligible_wall_art_premium           BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_wall_art_standard          BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_calendar                   BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_puzzle                     BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_card                       BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_book_illustration          BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_educational                BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_museum_print               BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_institutional_license      BOOLEAN NOT NULL DEFAULT FALSE,

    requires_curator_review             BOOLEAN NOT NULL DEFAULT FALSE,
    curator_review_reason               TEXT REFERENCES commerce_curator_review_reason_vocabulary(value),
    curator_decision                    TEXT NOT NULL DEFAULT 'pending' REFERENCES commerce_curator_decision_vocabulary(value),
    curator_reviewed_by                 TEXT,
    curator_reviewed_at                 TIMESTAMPTZ,
    curator_notes                       TEXT,

    score_inputs                        JSONB NOT NULL DEFAULT '{}',
    input_hash_sha256                   TEXT NOT NULL,

    status                              TEXT NOT NULL DEFAULT 'pending_review',
    provenance                          JSONB NOT NULL DEFAULT '{}',
    created_at                          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_commerce_opportunities_input_hash CHECK (input_hash_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_commerce_opportunities_computed_by CHECK (length(computed_by) > 0),
    CONSTRAINT chk_commerce_opportunities_review_identity CHECK (
        curator_decision = 'pending'
        OR curator_reviewed_by IS NOT NULL
    ),
    CONSTRAINT chk_commerce_opportunities_status CHECK (
        status IN ('pending_review','active','blocked','stale','superseded','retired','archived','integrity_suspect')
    )
);
```


No `collection_fit_score` or `commercial_value_score` columns are permitted.

### Indexes

```sql
CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_policy_score
    ON commerce_opportunities(policy_version_id, commerce_opportunity_score DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_tier_score
    ON commerce_opportunities(commerce_tier, commerce_opportunity_score DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_csm_tier
    ON commerce_opportunities(csm_tier, csm_score DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_gate
    ON commerce_opportunities(hard_gate_status, computed_at DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_curator
    ON commerce_opportunities(curator_decision, requires_curator_review, computed_at DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_stale
    ON commerce_opportunities(policy_stale, last_scored_at DESC)
    WHERE policy_stale = TRUE;

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_last_scored
    ON commerce_opportunities(last_scored_at)
    WHERE status NOT IN ('blocked','archived');
```

### Constraints

- One `commerce_opportunities` row per `illustration_opportunities.id`.
- `policy_version_id` references `commerce_policy`.
- All scoring values are `0..1` or null.
- `input_hash_sha256` is exactly 64 lowercase hex characters.
- `hard_gate_status` references governed vocabulary.
- `commerce_tier` references governed vocabulary.
- `csm_tier` references governed vocabulary and is advisory only.
- `curator_decision` references governed vocabulary.
- Curator decision other than `pending` requires reviewer identity.
- `taxon_commercial_tier` must reference an active governed row via trigger.
- Failed hard gate must prevent product eligibility flags.

### Triggers

#### Updated At

```sql
CREATE TRIGGER trg_commerce_opportunities_updated_at
    BEFORE UPDATE ON commerce_opportunities
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

#### Active Taxon Tier Trigger

Specification:

```text
Function: enforce_active_taxon_commercial_tier()
Table: commerce_opportunities
Timing: BEFORE INSERT OR UPDATE
Rule:
  if NEW.taxon_commercial_tier IS NOT NULL:
    matching taxon_commercial_tier_vocabulary.value must exist with status = 'active'
Effect:
  RAISE EXCEPTION on missing or inactive tier
```

#### Eligibility Hard Gate Trigger

Specification:

```text
Function: enforce_commerce_opportunity_gate_eligibility()
Table: commerce_opportunities
Timing: BEFORE INSERT OR UPDATE
Rule:
  if NEW.hard_gate_status != 'passed':
    all eligible_* fields must be FALSE
Effect:
  RAISE EXCEPTION if caller attempts TRUE eligibility under failed gate
```

#### COS Audit Deferred Trigger

Specification for Migration 21:

```text
Function: enforce_commerce_opportunity_audit_exists()
Table: commerce_opportunities
Timing: CONSTRAINT TRIGGER AFTER INSERT OR UPDATE
Deferrable: YES, INITIALLY DEFERRED
Status in Migration 21:
  NOT CREATED YET, because score_audit_log is Migration 22.
Required in Migration 22:
  once score_audit_log exists, add deferred trigger requiring score audit for any row with commerce_opportunity_score IS NOT NULL.
```

### Replay Requirements

Replay file:

```text
tests/replay/test_migration_021_commerce_opportunities.py
```

Assertions:

1. `commerce_opportunities` exists.
2. `commerce_opportunities` references `illustration_opportunities`.
3. Only one commerce opportunity row can exist per illustration opportunity.
4. No `collection_fit_score` column exists.
5. No `commercial_value_score` column exists.
6. Five model subscore columns exist: `museum_score`, `retail_score`, `publishing_score`, `tourism_score`, `reference_score`.
7. `csm_score` and `csm_tier` exist.
8. `last_scored_at` exists.
9. `input_hash_sha256` rejects non-lowercase or non-64-hex input.
10. All numeric scores reject values outside `0..1`.
11. Invalid `hard_gate_status` is rejected.
12. Invalid `commerce_tier` is rejected.
13. Invalid `csm_tier` is rejected.
14. Invalid `curator_decision` is rejected.
15. Inactive `taxon_commercial_tier_vocabulary` rows cannot be referenced by a scored opportunity.
16. Failed hard gate with any `eligible_* = TRUE` is rejected.
17. `last_scored_at` index supports staleness polling query.
18. Migration 21 does not create `score_audit_log`.
19. Worker activation remains blocked until Migration 22 audit requirements exist.

## Cross-Migration Replay Requirements

Replay file:

```text
tests/replay/test_migration_019_021_commerce_director_decisions.py
```

Assertions:

1. Migrations 19, 20, and 21 run after Migration 18 on a fresh database.
2. LOC source expansion is applied before Commerce Intelligence scoring tables are used.
3. Governed vocabularies are seeded before `commerce_policy` creation.
4. `commerce_policy` v1.0.0 draft exists before `commerce_opportunities` creation.
5. M19-21 do not create `score_audit_log`.
6. M19-21 do not create `product_recommendations`.
7. M19-21 do not create `collection_recommendations`.
8. CSM fields are present on `commerce_opportunities` and do not affect product eligibility checks.
9. Staleness fields are present: `max_score_age_days`, `last_scored_at`, `policy_stale`.
10. All Director Decision B-1 through D-3/D-5 schema impacts are reflected.

## Ready-for-Implementation Checklist

- Migration 19 includes mandatory source constraint amendment.
- Migration 19 creates governed vocabulary tables with second-human activation constraints.
- Migration 20 creates six-state `commerce_policy` with `max_score_age_days`.
- Migration 20 seeds only draft policy; activation is a governed event, not migration behavior.
- Migration 21 creates `commerce_opportunities` with five COS model subscores.
- Migration 21 includes CSM advisory fields.
- Migration 21 includes `last_scored_at` for polling staleness.
- Migration 21 excludes `score_audit_log`, product recommendations, and collection recommendations.
- Replay tests are defined for each migration.
- Worker activation is explicitly blocked until Migration 22 and replay worker implementation.

## Non-Goals

Migrations 19-21 do not:

- create `score_audit_log`
- create `product_recommendations`
- create `collection_recommendations`
- create worker roles or RLS policies
- activate scoring workers
- activate replay workers
- create API routes
- create Mission Control views
- generate products
- publish to Shopify or Etsy
