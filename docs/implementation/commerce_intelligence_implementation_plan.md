# Commerce Intelligence Implementation Plan

| Field | Value |
|---|---|
| Version | v0.5.0 |
| Status | Approved — sequencing only. No redesign. No schema changes beyond what is specified. |
| Repository | opengracelabs/nc |
| Date | 2026-06-06 |
| Role | Principal Architect |

---

## Frozen References

This plan treats the following documents as frozen inputs. This plan sequences their
implementation. It does not redesign them.

| Document | Location | Governs |
|---|---|---|
| Commerce Intelligence Constitution v1 | `docs/governance/commerce_intelligence_constitution_v1.md` | Governance rules, article-level constraints, audit requirements, policy lifecycle |
| Commerce Intelligence Runtime v1 | `docs/architecture/commerce_intelligence_runtime_v1.md` | SQL schema, scoring formulas, worker contracts, API surface, staleness rules |
| Commercial Success Model v1 | `docs/commerce/commercial_success_model_v1.md` | Scoring dimensions, classification labels, channel routing strategy |

When a provision of the Constitution conflicts with the Runtime document on a schema field,
the Runtime document governs the field definition. The Constitution governs the rules applied
to that field. They do not conflict — they operate at different layers.

---

## Part I — Reconciliation Notes

These notes resolve the three surface-level differences between the frozen documents before
sequencing begins. They are not redesigns. They are binding interpretations for this plan.

### R1 — Schema Authority

The Runtime document (`commerce_intelligence_runtime_v1.md`) is the SQL authority for all five
tables. Its `CREATE TABLE` statements are the implementation target. The Constitution's
pseudo-schema definitions (Articles 22–26) describe governance constraints that are applied as
additional `CHECK` constraints, triggers, and PostgreSQL `RULE` objects on top of the Runtime
schema. They are additive, not alternative.

### R2 — Scoring Dimension Mapping

The CSM (`commercial_success_model_v1.md`) defines seven dimensions (VAS, PIS, SSS, TAS, IPS,
PVS, RCS). The Runtime defines six score columns in `commerce_opportunities`. The mapping is
resolved in the `score_weights` JSONB of each `commerce_policy` record — not in the schema. The
schema carries the six numeric columns. The policy JSON stores how CSM dimensions contribute to
each column. This is a configuration decision, seeded in Migration 19.

| CSM Dimension | Weight | Runtime Column | Notes |
|---|---|---|---|
| VAS — Visual Authority | 30% | `visual_quality_score` | Composition, era, illustrator prestige, color process |
| PIS — Place Identity | 20% | `place_relevance_score` | From `illustration_opportunity_places.relevance_score` |
| SSS — Story Strength | 15% | `provenance_score` | Illustrator attribution, expedition lineage, publication rarity |
| TAS — Tourism Appeal | 15% | `place_relevance_score` (policy-weighted sub-component) | Iconic place status; weighted inside `place_relevance_score` via policy |
| IPS — Institutional Prestige | 10% | `provenance_score` (sub-component) | `source_id` institutional weight embedded in provenance scoring |
| PVS — Product Versatility | 10% | `visual_quality_score` (sub-component) | Resolution, format, derivative presence |
| RCS — Rights Clarity | Hard Gate | `rights_status` + `rights_readiness_score` | Must be `Public Domain` or `CC0`; `rights_readiness_score` = 1.000 required |

The `commercial_value_score` and `collection_fit_score` columns in the Runtime schema have no
direct CSM counterpart. They are computed by the worker from collection membership, product
profile availability, and place tier signals. They are not redundant — they capture commercial
context that the CSM dimensions do not.

### R3 — Classification Tier Mapping

The CSM defines five named tiers by CSP (0–100). The Constitution defines four tiers by COS
(0.0–1.0). The Runtime uses `commerce_score` (0.0–1.0) with no named tiers in the schema. The
`commerce_policy.rules` JSONB stores both the tier names and thresholds. No schema change is
needed. The runtime `status` field lifecycle is separate from CSM classification.

| CSM Label | CSP Range | commerce_score Equivalent | Constitution Tier | Channel Deployment |
|---|---|---|---|---|
| MASTERWORK | 90–100 | ≥ 0.90 | tier_1 (upper) | Archival prints, folios, museum licensing |
| FLAGSHIP | 75–89 | 0.75 – 0.89 | tier_1 (lower) / tier_2 (upper) | Wall art, calendars, puzzles, apparel |
| STANDARD | 60–74 | 0.60 – 0.74 | tier_2 (lower) | Etsy, postcards, stationery |
| REFERENCE | 40–59 | 0.40 – 0.59 | tier_3 | Field guides, educational use only |
| BLOCKED | < 40 | < 0.40 | blocked | No commercial routing |

The CSM classification label is stored in `commerce_policy.rules` as a named threshold map. The
scoring worker reads this map and writes the label to `commerce_opportunities.score_components`
at compute time. The label is derived output — not a schema column.

---

## Part II — FK Dependency Graph

This graph determines the mandatory migration order. No migration may be executed before all
tables it references exist.

```
[Existing — not created by this plan]
  illustration_opportunities   (Migration 16)
  illustration_opportunity_places
  illustration_opportunity_assets
  assets                       (Migration 01)
  asset_rights                 (Migration 15)
  collections                  (Migration 16)
  collection_assets            (Migration 16)
  collection_places            (Migration 16)

Migration 19: commerce_policy
  No FKs to new tables.
  Referenced by: all four subsequent tables.

Migration 20: commerce_opportunities
  FK → commerce_policy(id)          [requires Migration 19]
  FK → illustration_opportunities   [exists]
  FK → concepts(id)                 [exists]
  FK → places(id)                   [exists]
  Self-FK: superseded_by → commerce_opportunities(id)

Migration 21: score_audit_log
  FK → commerce_policy(id)          [requires Migration 19]
  entity_id: UUID — no FK by design (polymorphic: references commerce_opportunities,
    product_recommendations, or collection_recommendations by entity_type)

Migration 22: product_recommendations
  FK → commerce_opportunities(id)   [requires Migration 20]
  FK → commerce_policy(id)          [requires Migration 19]
  FK → collections(id)              [exists — nullable]
  FK → assets(id)                   [exists — nullable]
  FK → illustration_opportunities   [exists — nullable]
  Self-FK: superseded_by → product_recommendations(id)

Migration 22: collection_recommendations
  FK → commerce_policy(id)          [requires Migration 19]
  FK → collections(id)              [exists — nullable]
  FK → places(id)                   [exists — nullable]
  FK → concepts(id)                 [exists — nullable]
  Self-FK: superseded_by → collection_recommendations(id)

Migration 23: vocabulary seed + pre-activation
  No new tables.
  Writes to: commerce_policy (status transition draft → approved)
```

**Strict ordering: 19 → 20 → 21 → 22 → 23**

Migrations 21 and 22 are independent of each other. Migration 21 may be executed before or
after Migration 22. It must precede scoring worker activation regardless of position relative
to Migration 22.

---

## Part III — Migration Definitions

### Migration 19 — Commerce Policy

**File:** `infrastructure/postgres/init/19_commerce_policy.sql`

**Purpose:** Create the versioned scoring and gating contract. Seed the three draft policies
that all subsequent workers will reference. Embed the CSM scoring dimension mappings, priority
illustrators list, and classification thresholds in policy JSONB. Nothing else may be scored
until this migration completes and at least one policy reaches `active`.

**Creates:**

```
TABLE: commerce_policy
  id              UUID PRIMARY KEY
  policy_key      TEXT NOT NULL                    -- e.g. 'commerce-opportunity'
  policy_version  TEXT NOT NULL                    -- e.g. 'v1'
  status          TEXT NOT NULL DEFAULT 'draft'
  applies_to      TEXT NOT NULL                    -- 'commerce_opportunity' | 'product_recommendation'
                                                   --   | 'collection_recommendation' | 'global'
  rules           JSONB NOT NULL DEFAULT '{}'      -- classification thresholds, stale reasons
  score_weights   JSONB NOT NULL DEFAULT '{}'      -- dimension weights and CSM tier map
  gates           JSONB NOT NULL DEFAULT '{}'      -- hard gate values and gate evaluation order
  reviewer_policy JSONB NOT NULL DEFAULT '{}'      -- second-human rule, approval requirements
  provenance      JSONB NOT NULL DEFAULT '{}'
  created_by      TEXT NOT NULL
  approved_by     TEXT                             -- must differ from created_by
  approved_at     TIMESTAMPTZ
  effective_from  TIMESTAMPTZ
  effective_until TIMESTAMPTZ
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()

CONSTRAINT chk_commerce_policy_status:
  status IN ('draft','approved','active','paused','retired')

CONSTRAINT chk_commerce_policy_applies_to:
  applies_to IN ('commerce_opportunity','product_recommendation',
                 'collection_recommendation','global')

CONSTRAINT chk_commerce_policy_second_human:
  approved_by IS DISTINCT FROM created_by   -- self-approval prohibited

UNIQUE (policy_key, policy_version)

TRIGGER: set_updated_at
TRIGGER (constraint): one status = 'active' per applies_to at a time
TRIGGER (constraint): approved_by IS NOT NULL when status IN ('active','paused','retired')
```

**Seeds (status = 'draft'):**

Three draft policy records. Each embeds its complete scoring contract in JSONB so historical
scores remain explainable without checking code history.

`commerce-opportunity:v1` — governs `commerce_opportunities` scoring:
```json
{
  "policy_key": "commerce-opportunity",
  "policy_version": "v1",
  "applies_to": "commerce_opportunity",
  "score_weights": {
    "rights_readiness_score":  0.24,
    "visual_quality_score":    0.20,
    "place_relevance_score":   0.16,
    "provenance_score":        0.14,
    "collection_fit_score":    0.14,
    "commercial_value_score":  0.12,
    "weights_sum_check":       1.00,
    "csm_dimension_map": {
      "VAS": { "column": "visual_quality_score",  "share": 0.30 },
      "PIS": { "column": "place_relevance_score", "share": 0.20 },
      "SSS": { "column": "provenance_score",      "share": 0.15 },
      "TAS": { "column": "place_relevance_score", "share": 0.15, "sub_weight": true },
      "IPS": { "column": "provenance_score",      "share": 0.10, "sub_weight": true },
      "PVS": { "column": "visual_quality_score",  "share": 0.10, "sub_weight": true }
    },
    "priority_illustrators": [
      "Audubon", "Gould", "Merian", "Redouté",
      "Lear", "Nodder", "Haeckel", "Wolf"
    ]
  },
  "gates": {
    "gate_order": [0, 1, 2, 3, 4],
    "gate_0_rights_record_required": true,
    "gate_1_min_rights_confidence":  0.70,
    "gate_2_min_image_width_px":     2000,
    "gate_3_legal_hold_blocks":      true,
    "gate_4_min_quality_score":      0.40
  },
  "rules": {
    "classification_thresholds": {
      "MASTERWORK": 0.90,
      "FLAGSHIP":   0.75,
      "STANDARD":   0.60,
      "REFERENCE":  0.40,
      "BLOCKED":    0.00
    },
    "stale_reasons": [
      "rights_changed", "asset_changed", "asset_status_changed",
      "asset_derivative_changed", "opportunity_changed",
      "place_relevance_changed", "collection_changed",
      "collection_status_changed", "product_profile_changed",
      "provider_policy_changed", "pricing_policy_changed",
      "qa_policy_changed", "policy_changed", "worker_version_changed",
      "manual_review_required"
    ]
  },
  "reviewer_policy": {
    "second_human_required_for_active": true,
    "priority_illustrator_escalates":   true,
    "boundary_case_delta":              0.05
  }
}
```

`product-recommendation:v1` — governs `product_recommendations` scoring. `collection-recommendation:v1` — governs `collection_recommendations` scoring. Both seeded as `draft` with their dimension weights from the Runtime document.

**Mandatory before:** Migration 20, 21, 22, 23, and all workers.

---

### Migration 20 — Commerce Opportunities

**File:** `infrastructure/postgres/init/20_commerce_opportunities.sql`

**Purpose:** Create the primary scoring entity. One record per evaluated subject (asset,
illustration opportunity, or collection). Carries the full scored commercial state, input
snapshot for replayability, and stale/superseded chain for version management.

**Creates:**

```
TABLE: commerce_opportunities
  id                       UUID PRIMARY KEY
  subject_type             TEXT NOT NULL         -- 'asset' | 'illustration_opportunity' | 'collection'
  subject_id               UUID NOT NULL         -- ID in the subject table
  place_id                 UUID FK → places(id)  -- nullable
  concept_id               UUID FK → concepts(id)-- nullable
  source                   TEXT NOT NULL         -- references sources(source_id)
  opportunity_type         TEXT NOT NULL

  rights_status            TEXT NOT NULL         -- 'Public Domain' | 'CC0' (hard gate, non-null)
  rights_readiness_score   NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  visual_quality_score     NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  place_relevance_score    NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  provenance_score         NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  collection_fit_score     NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  commercial_value_score   NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  commerce_score           NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)

  status                   TEXT NOT NULL DEFAULT 'candidate'
  policy_id                UUID NOT NULL FK → commerce_policy(id)
  worker_version           TEXT NOT NULL         -- e.g. 'commerce_opportunity_worker:v0.5.0'
  input_hash               TEXT NOT NULL         -- deterministic hash of normalized input_snapshot
  score_components         JSONB NOT NULL DEFAULT '{}'  -- per-dimension breakdown + CSM label
  input_snapshot           JSONB NOT NULL DEFAULT '{}'  -- full signal values at compute time
  stale_reason             TEXT                  -- from policy rules.stale_reasons vocabulary
  superseded_by            UUID FK → commerce_opportunities(id)
  provenance               JSONB NOT NULL DEFAULT '{}'

  reviewed_by              TEXT
  reviewed_at              TIMESTAMPTZ
  rejection_reason         TEXT
  override_reason          TEXT

  created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()

CONSTRAINT chk_commerce_opportunity_subject:
  subject_type IN ('asset','illustration_opportunity','collection')

CONSTRAINT chk_commerce_opportunity_status:
  status IN ('candidate','recommended','approved','rejected','stale','superseded')

CONSTRAINT chk_commerce_opportunity_rights:
  rights_status IN ('Public Domain','CC0')

TRIGGER: set_updated_at
```

**Indexes (from Runtime document):**

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

The unique partial index on active records is the replayability guard. The same subject, same
policy, and same input hash cannot produce two active records. A changed input hash means the
old record must be marked stale before the new record is inserted.

**Mandatory before:** Migration 22, scoring worker activation.

---

### Migration 21 — Score Audit Log

**File:** `infrastructure/postgres/init/21_score_audit_log.sql`

**Purpose:** Create the append-only NIST audit record. Install PostgreSQL-level no-UPDATE and
no-DELETE rules. Revoke UPDATE and DELETE from the scoring worker database role. This migration
must complete before any worker is permitted to write to `commerce_opportunities`. The audit log
is a precondition of scoring — not a consequence.

**Creates:**

```
TABLE: score_audit_log
  id               UUID PRIMARY KEY
  entity_type      TEXT NOT NULL        -- 'commerce_opportunity' | 'product_recommendation'
                                        --   | 'collection_recommendation'
  entity_id        UUID NOT NULL        -- ID in the entity table (no FK by design — polymorphic)
  policy_id        UUID FK → commerce_policy(id)
  worker_version   TEXT
  score_name       TEXT NOT NULL        -- e.g. 'commerce_score', 'recommendation_score'
  previous_score   NUMERIC(4,3)
  new_score        NUMERIC(4,3)
  previous_status  TEXT
  new_status       TEXT
  input_hash       TEXT
  score_components JSONB NOT NULL DEFAULT '{}'
  input_snapshot   JSONB NOT NULL DEFAULT '{}'  -- full signal values at event time
  reason           TEXT NOT NULL               -- from stale_reasons vocabulary or event reason
  generated_by     TEXT NOT NULL               -- worker_id or curator_id; never anonymous
  generated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()

CONSTRAINT chk_score_audit_entity_type:
  entity_type IN ('commerce_opportunity','product_recommendation','collection_recommendation')
```

**Append-only protection (Constitution Article 28):**

```sql
-- No UPDATE on any row, ever.
CREATE RULE no_update_score_audit_log AS
    ON UPDATE TO score_audit_log DO INSTEAD NOTHING;

-- No DELETE on any row, ever.
CREATE RULE no_delete_score_audit_log AS
    ON DELETE TO score_audit_log DO INSTEAD NOTHING;

-- Revoke from the scoring worker role.
-- Replace :scoring_worker_role with the actual role name.
REVOKE UPDATE, DELETE ON score_audit_log FROM :scoring_worker_role;
```

**Indexes:**

```sql
CREATE INDEX idx_score_audit_log_entity
    ON score_audit_log(entity_type, entity_id, generated_at DESC);
CREATE INDEX idx_score_audit_log_policy
    ON score_audit_log(policy_id, generated_at DESC);
CREATE INDEX idx_score_audit_log_reason
    ON score_audit_log(reason, generated_at DESC);
```

**Mandatory before:** All scoring worker activation. No exceptions. A scoring worker must not
write to `commerce_opportunities` unless it can also write to `score_audit_log` in the same
transaction.

**Audit event write order within a transaction:**

```
1. BEGIN
2. INSERT score_audit_log (previous_state captured)
3. INSERT or UPDATE commerce_opportunities
4. COMMIT
```

If step 3 fails, step 2 is rolled back. The audit log never contains an orphaned event.
If step 2 fails, step 3 must not proceed.

---

### Migration 22 — Product and Collection Recommendations

**File:** `infrastructure/postgres/init/22_recommendations.sql`

**Purpose:** Create the two derived recommendation tables. These are downstream of
`commerce_opportunities`. They cannot be populated until at least one `commerce_opportunity`
record is approved. This migration creates the schema; it does not activate recommendation
workers.

**Creates:**

```
TABLE: product_recommendations
  id                            UUID PRIMARY KEY
  commerce_opportunity_id       UUID NOT NULL FK → commerce_opportunities(id)
  collection_id                 UUID FK → collections(id)         -- nullable
  asset_id                      UUID FK → assets(id)              -- nullable
  opportunity_id                UUID FK → illustration_opportunities(id) -- nullable

  product_family                TEXT NOT NULL
  product_type                  TEXT NOT NULL
  provider_route                TEXT
  channel_policy                JSONB NOT NULL DEFAULT '{}'

  product_family_fit_score      NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  asset_product_fit_score       NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  expected_margin_score         NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  provider_readiness_score      NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  channel_fit_score             NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  demand_signal_score           NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  operational_complexity_score  NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  recommendation_score          NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)

  generation_policy             JSONB NOT NULL DEFAULT '{}'
  variant_plan                  JSONB NOT NULL DEFAULT '{}'
  qa_gates                      JSONB NOT NULL DEFAULT '{}'

  status                        TEXT NOT NULL DEFAULT 'candidate'
  policy_id                     UUID NOT NULL FK → commerce_policy(id)
  worker_version                TEXT NOT NULL
  input_hash                    TEXT NOT NULL
  score_components              JSONB NOT NULL DEFAULT '{}'
  input_snapshot                JSONB NOT NULL DEFAULT '{}'
  stale_reason                  TEXT
  superseded_by                 UUID FK → product_recommendations(id)
  provenance                    JSONB NOT NULL DEFAULT '{}'

  reviewed_by                   TEXT
  reviewed_at                   TIMESTAMPTZ
  rejection_reason              TEXT
  override_reason               TEXT

  created_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()

CONSTRAINT chk_product_recommendation_status:
  status IN ('candidate','plan_ready','sample_required','approved',
             'rejected','generated','stale','superseded','retired')

TRIGGER: set_updated_at
```

```
TABLE: collection_recommendations
  id                            UUID PRIMARY KEY
  place_id                      UUID FK → places(id)               -- nullable
  concept_id                    UUID FK → concepts(id)             -- nullable
  existing_collection_id        UUID FK → collections(id)          -- nullable
  recommendation_type           TEXT NOT NULL

  title                         JSONB NOT NULL DEFAULT '{}'
  rationale                     TEXT NOT NULL
  candidate_asset_ids           UUID[] NOT NULL DEFAULT '{}'
  candidate_opportunity_ids     UUID[] NOT NULL DEFAULT '{}'

  thematic_coherence_score      NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  asset_depth_score             NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  rights_readiness_score        NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  product_breadth_score         NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  editorial_value_score         NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  commerce_potential_score      NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  provenance_score              NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)
  collection_score              NUMERIC(4,3) NOT NULL CHECK (BETWEEN 0 AND 1)

  recommended_product_families  JSONB NOT NULL DEFAULT '{}'

  status                        TEXT NOT NULL DEFAULT 'candidate'
  policy_id                     UUID NOT NULL FK → commerce_policy(id)
  worker_version                TEXT NOT NULL
  input_hash                    TEXT NOT NULL
  score_components              JSONB NOT NULL DEFAULT '{}'
  input_snapshot                JSONB NOT NULL DEFAULT '{}'
  stale_reason                  TEXT
  superseded_by                 UUID FK → collection_recommendations(id)
  provenance                    JSONB NOT NULL DEFAULT '{}'

  reviewed_by                   TEXT
  reviewed_at                   TIMESTAMPTZ
  rejection_reason              TEXT
  override_reason               TEXT

  created_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()

CONSTRAINT chk_collection_recommendation_type:
  recommendation_type IN ('new_collection','extend_collection','seasonal_drop',
                          'product_bundle','editorial_campaign')

CONSTRAINT chk_collection_recommendation_status:
  status IN ('candidate','recommended','approved','rejected',
             'converted_to_collection','stale','superseded')

TRIGGER: set_updated_at
```

**Indexes (from Runtime document):**

```sql
-- product_recommendations
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

-- collection_recommendations
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

**Mandatory before:** Recommendation workers. Not mandatory before commerce opportunity scoring
activates.

---

### Migration 23 — Vocabulary Seed and Pre-Activation Preparation

**File:** `infrastructure/postgres/init/23_commerce_vocabulary_seed.sql`

**Purpose:** Update the three draft policies with complete vocabulary data: priority
illustrators list, taxon commercial tier mappings, Yellowstone place_iconic_taxa seed, and
place tier thresholds. Transition policies from `draft` to `approved` — pending the second-human
`approved → active` governance event that happens outside migrations. This migration is the
last schema gate before the activation protocol begins.

**No new tables.** All writes are to existing `commerce_policy` records.

**Updates to `commerce-opportunity:v1` policy JSONB:**

Adds to `score_weights.priority_illustrators` the complete list with normalized name variants
for matching against `illustration_opportunities.illustrator`:
```
Audubon, J.J. Audubon, John James Audubon
Gould, John Gould, J. Gould
Merian, M.S. Merian, Maria Sibylla Merian
Redouté, P.J. Redouté, Pierre-Joseph Redouté
Lear, Edward Lear, E. Lear
Nodder, F.P. Nodder, Frederick Polydore Nodder
Haeckel, Ernst Haeckel, E. Haeckel
Wolf, Joseph Wolf, J. Wolf
```

Adds to `score_weights.taxon_commercial_tier_map`:
```
high:     Aves, Lepidoptera, Orchidaceae, Coleoptera (charismatic), marine megafauna
moderate: Mammalia, Reptilia, Amphibia, Arboreal flora, large ferns, succulents
low:      plain Invertebrata, non-charismatic Fungi, grasses, lichens
none:     geographic anchor only (maps, posters, architectural drawings)
```

Adds to `score_weights.place_iconic_taxa_seed` for Yellowstone National Park:
```
Bison bison (American Bison)
Ursus arctos horribilis (Grizzly Bear)
Oncorhynchus clarkii bouvieri (Yellowstone Cutthroat Trout)
Cervus canadensis (American Elk / Wapiti)
Haliaeetus leucocephalus (Bald Eagle)
Cygnus buccinator (Trumpeter Swan)
Canis lupus (Gray Wolf)
Pronghorn (Antilocapra americana)
```

Adds to `rules.classification_thresholds` validated against Yellowstone proof assets:
- 1871 Hayden Survey Map → expected MASTERWORK (CSP ≥ 0.90)
- Jackson *Old Faithful* photograph → expected FLAGSHIP (CSP 0.75–0.89)

**Policy status transition (in-migration UPDATE):**

```sql
UPDATE commerce_policy
SET status = 'approved',
    approved_by = NULL,   -- set to NULL; requires out-of-migration human approval
    updated_at = NOW()
WHERE policy_key IN ('commerce-opportunity','product-recommendation','collection-recommendation')
  AND policy_version = 'v1'
  AND status = 'draft';
```

Note: `approved_by = NULL` here is intentional. The in-migration step sets `status = 'approved'`
to signal readiness. The second-human approval (`approved_by` set to a real curator identity,
`approved → active`) happens outside migrations as the activation protocol. The constraint
requiring `approved_by IS NOT NULL` for `active` and `retired` statuses enforces this at the
database level.

**Mandatory before:** Activation protocol. Not mandatory before Migration 22.

---

## Part IV — Implementation Order

Implementation proceeds in six phases. Each phase must be complete before the next begins.

### Phase 1 — Schema (Migrations 19–23)

Execute migrations in strict order. Each migration is additive and idempotent using
`CREATE TABLE IF NOT EXISTS` and `ON CONFLICT DO NOTHING` patterns consistent with the existing
codebase.

```
Migration 19: commerce_policy table + draft policy seed
Migration 20: commerce_opportunities table + indexes
Migration 21: score_audit_log table + no-update rule + no-delete rule + role revocation
Migration 22: product_recommendations + collection_recommendations tables + indexes
Migration 23: vocabulary seed + policy status → approved
```

No worker code may be written against the production schema until Migration 22 is complete.
Migration 21 (audit log) must be complete before the scoring worker emits any test writes.

### Phase 2 — Replay Worker

Build `commerce_replay_worker:v0.5.0` before building the scoring worker. The replay worker
is not a test helper — it is a production component that verifies scoring determinism.

Replay worker responsibilities (from Runtime document):
- Load frozen replay fixtures from `tests/replay/`
- Load pinned `commerce_policy` by key and version
- Execute the scoring formula against fixture inputs
- Assert `commerce_score` matches expected value to three decimal places
- Assert `input_hash` matches expected hash
- Assert `score_components` structure matches expected shape
- Assert correct `status` transitions for stale and superseded cases
- Assert `score_audit_log` write occurs in the same transaction as the opportunity write
- Write `replay_verified` or `replay_failure` result to `score_audit_log`

The replay worker must pass all twelve required replay cases from the Runtime document before
the scoring worker is activated. These cases are not unit tests — they are constitutional
preconditions of activation.

### Phase 3 — Commerce Opportunity Worker

Build `commerce_opportunity_worker:v0.5.0` after replay worker passes all twelve cases.

Worker input sources (from Runtime document):
- `illustration_opportunities` (primary)
- `illustration_opportunity_places`
- `illustration_opportunity_assets`
- `assets`
- `asset_rights`
- `collections`
- `collection_assets`

Worker responsibilities:
1. Load active `commerce-opportunity:v1` policy.
2. Load authoritative inputs for the subject.
3. Build normalized `input_snapshot` (values, not references).
4. Compute `input_hash` (deterministic — same inputs always same hash).
5. Check for existing active record with same `subject_type + subject_id + policy_id + input_hash`.
   - If found: no-op (idempotent).
   - If same subject and policy but different hash: mark old record stale, proceed.
6. Apply hard gates in order (0 → 4). On failure: write audit log, do not proceed.
7. Compute six dimension scores and `commerce_score`.
8. Determine CSM classification label from `policy.rules.classification_thresholds`.
9. Build `score_components` with per-dimension breakdown and label.
10. Within one transaction: INSERT audit log first, then INSERT commerce_opportunities.
11. If stale replacement: set `superseded_by` on old record.

The worker must not write to `commerce_opportunities` outside a transaction that also writes
to `score_audit_log`.

### Phase 4 — Staleness Worker

Build `commerce_staleness_worker:v0.5.0` alongside or immediately after the scoring worker.

Staleness worker responsibilities:
- Poll or receive events from upstream tables (rights changes, asset status, collection changes).
- For each change event, identify affected `commerce_opportunities` records.
- Mark affected records `status = 'stale'` with the appropriate `stale_reason` from policy vocabulary.
- Write `score_audit_log` event for every staleness transition.
- Queue recomputation in `workflow_items`.

Stale records that have an active replacement are set to `superseded` after the replacement is
confirmed. Stale records with no valid replacement remain stale with a clear `stale_reason`.

### Phase 5 — Recommendation Workers and FastAPI

Build in this sub-order:

1. **FastAPI read endpoints** (safe, no write) — list and detail for all five entities.
2. **FastAPI governance endpoints** (approve, reject, mark-stale) for `commerce_opportunities`.
3. **`product_recommendation_worker:v0.5.0`** — activates only after at least one
   `commerce_opportunity` record reaches `approved` status.
4. **`collection_recommendation_worker:v0.5.0`** — activates after at least one approved
   commerce opportunity exists.
5. **FastAPI governance endpoints** for `product_recommendations` and
   `collection_recommendations`.
6. **FastAPI worker trigger endpoints** — evaluate, regenerate.

Recommendation workers must not activate in `advisory` mode until the commerce opportunity
worker has produced at least five approved records. Do not activate against a single proof
record.

### Phase 6 — Activation Protocol (Governed Event)

See Part VII. This is not a code phase — it is a governance event. No development work occurs
here. The Principal Architect and a second human execute the activation protocol against the
approved (not yet active) policies.

---

## Part V — Replay Order

Replay must be executed at four points. Each gate must pass before proceeding.

### Replay Gate 1 — Pre-Activation (before scoring worker writes to production)

Execute all twelve required replay cases from the Runtime document against the draft policy.
All twelve must pass. Any failure blocks activation.

| Case | Description |
|---|---|
| RC-01 | Valid PD asset → commerce_opportunity created |
| RC-02 | CC0 asset → commerce_opportunity created |
| RC-03 | Missing rights record → blocked, no opportunity created |
| RC-04 | "No known copyright restrictions" without upstream normalization → blocked |
| RC-05 | Same inputs + same policy → same score + same input_hash |
| RC-06 | Policy change → existing recommendations marked stale |
| RC-07 | Asset checksum or derivative change → dependent recommendations marked stale |
| RC-08 | Collection membership change → dependent collection recommendations marked stale |
| RC-09 | Regeneration → new candidate created, old audit history preserved |
| RC-10 | Stale product recommendation → cannot be approved |
| RC-11 | Manual override → requires reviewer identity and reason |
| RC-12 | Every score creation, status transition, stale mark, and override → audit log written |

Fixture sources (from Runtime document): one verified BHL illustration opportunity, one PD
asset, one CC0 asset, one invalid-rights asset, one eligible collection, one ineligible
collection, one policy update fixture, one manual override fixture.

### Replay Gate 2 — Policy Activation (at activation protocol)

Run RC-05 again against the policy after vocabulary seed (Migration 23). Assert that the
Yellowstone Hayden Map proof scores ≥ 0.90 (MASTERWORK) and the Jackson photograph proof
scores between 0.75 and 0.89 (FLAGSHIP). If either assertion fails, the vocabulary seed is
incorrect and Migration 23 must be corrected before activation proceeds.

### Replay Gate 3 — Post-Activation (after first ten production scoring runs)

Run the replay worker against the first ten production `score_audit_log` entries. Assert that
`input_snapshot + policy_id → computed_score == stored score`. Any mismatch is a
`replay_failure` event and triggers constitution Article 14 investigation protocol.

### Replay Gate 4 — Policy Version Change (before any future policy update)

Before activating a new policy version, execute RC-05 and RC-06 against the new policy.
Assert determinism. Assert that affected recommendations are correctly marked stale.

---

## Part VI — Testing Order

Tests are organized in six layers. Each layer builds on the previous. Do not write layer N+1
tests until layer N tests pass.

### Layer 1 — Migration Tests

**Target:** Each migration executes cleanly against the existing schema.

Tests:
- Migration 19 is idempotent on repeat execution (`ON CONFLICT DO NOTHING`).
- Migration 20 is idempotent. FK integrity passes against Migration 19 output.
- Migration 21 is idempotent. No-update rule fires on test UPDATE attempt. No-delete rule
  fires on test DELETE attempt.
- Migration 22 is idempotent. FK integrity passes against Migrations 19 and 20.
- Migration 23 policy UPDATE executes cleanly. `status = 'approved'` on all three policies.
- Full stack replay: apply migrations 19–23 to a clean schema, assert all five tables exist
  with expected constraints.

Existing pattern: `tests/replay/test_migration_18_loc_maps_activation.py`.

### Layer 2 — Hard Gate Tests

**Target:** The scoring worker correctly evaluates all five gates in order.

Tests:
- Gate 0: No `asset_rights` record → `hard_gate_status = 'blocked_rights'`, no score.
- Gate 1: `rights_confidence < 0.70` → `hard_gate_status = 'blocked_rights'`, no score.
- Gate 2: `image_width_px < 2000` → `hard_gate_status = 'blocked_resolution'`, no score.
- Gate 3: `rights_confidence = 0.0` → `hard_gate_status = 'blocked_legal'`, no cure path.
- Gate 4: `image_quality_score < 0.40` → score computed, `status` forced to `blocked`, all
  eligibility flags `FALSE`.
- Gate 4 null: `image_quality_score IS NULL` → same behavior as Gate 4 failure.
- Gate 4 cure: `image_quality_score` updated to ≥ 0.40 → `signal_correction` recompute fires,
  gate lifts.
- Gate order: Gate 3 does not also fire Gate 1 when Gate 3 fires first.

### Layer 3 — Deterministic Scoring Tests

**Target:** Same inputs always produce same score and same input_hash.

Tests:
- RC-05 (from replay cases).
- Score rounded to exactly three decimal places for all six dimension scores and `commerce_score`.
- Weights in active policy sum to exactly 1.000 (validated at policy approval, not at score time).
- `input_hash` is stable across worker restarts (same normalized snapshot → same hash).
- `score_components` JSONB contains all six dimension scores, per-dimension weights, and CSM
  classification label.

### Layer 4 — Audit Log Integrity Tests

**Target:** Every scoring event writes a correct, tamper-evident audit log entry.

Tests:
- Audit log INSERT precedes `commerce_opportunities` INSERT or UPDATE in every transaction.
- Audit log has no gaps: count of audit log entries for an entity equals count of state
  transitions.
- `generated_by` is never null or empty string.
- No-update rule: attempt to UPDATE any audit log row raises exception.
- No-delete rule: attempt to DELETE any audit log row raises exception.
- `reason` field always populated from policy stale_reasons vocabulary or named event type.

### Layer 5 — Staleness Propagation Tests

**Target:** Upstream changes correctly cascade to stale recommendations.

Tests:
- RC-06, RC-07, RC-08 (from replay cases).
- Stale record cannot be approved: attempt to set `status = 'approved'` on stale record raises
  exception.
- Stale → superseded transition requires a replacement record to exist first.
- `stale_reason` is always a value from `policy.rules.stale_reasons`.
- Stale audit log entry written for every staleness transition.

### Layer 6 — End-to-End Governance Tests

**Target:** Full pipeline from illustration opportunity to approved recommendation.

Tests:
- Approved `illustration_opportunity` → scoring worker produces `commerce_opportunity` in
  `candidate` status.
- Curator approves → `status = 'recommended'` or `'approved'`.
- Approved `commerce_opportunity` → `product_recommendation_worker` produces recommendation.
- Approved `commerce_opportunity` → `collection_recommendation_worker` produces recommendation.
- Recommendation approval requires non-stale parent `commerce_opportunity`.
- Priority illustrator attribution triggers escalation flag on `commerce_opportunity`.
- Second-human rule enforced at policy `approved → active` transition (test that self-approval
  raises exception at constraint level).

---

## Part VII — Mandatory Gates Before Scoring Activates

Scoring activates means: the first worker write to `commerce_opportunities` in the production
database.

| Gate | Migration or Step | Mandatory? | Consequence if Skipped |
|---|---|---|---|
| M-19 | `commerce_policy` table exists and draft policies are seeded | **Yes** | Worker has no policy to reference; cannot compute input_hash or load weights |
| M-20 | `commerce_opportunities` table exists | **Yes** | Nowhere to write scores |
| M-21 | `score_audit_log` exists with no-update and no-delete rules | **Yes** | Constitutional precondition violated; scoring without audit is prohibited |
| M-22 | `product_recommendations` and `collection_recommendations` exist | No | Recommendation workers cannot activate; opportunity scoring proceeds without them |
| M-23 | Vocabulary seed and policies in `approved` status | Conditional | Scores are valid but vocabulary defaults to 0.0 for most signals; CSM classification labels will be wrong; activation without vocabulary is not recommended |
| Replay Gate 1 | All 12 replay cases pass | **Yes** | Scoring determinism not verified; constitution Article 14 precondition not met |
| Policy Activation | Second human sets policy `approved → active` | **Yes** | No active policy exists; scoring worker has nothing to read |

**Minimum mandatory set:** M-19, M-20, M-21, Replay Gate 1, Policy Activation.

M-22 and M-23 are strongly recommended before activation but are not hard blocks to opportunity
scoring. They are hard blocks to recommendation scoring.

---

## Part VIII — Activation Protocol

The activation protocol is a governed event. It is not a migration. It is not code. It
produces a governance record in `commerce_policy`.

```
Step 1: Principal Architect confirms Migration 23 is applied and Replay Gate 2 passes.

Step 2: Principal Architect (as policy author) sets status on all three policies:
        From:  approved
        To:    [no change yet — this step confirms readiness]

Step 3: Second human (not Principal Architect) reviews:
        - commerce_policy.score_weights for commerce-opportunity:v1
        - commerce_policy.gates for hard gate values
        - Replay Gate 2 results for Yellowstone proof assets

Step 4: Second human updates:
        UPDATE commerce_policy
        SET status = 'active',
            approved_by = '[second human identity]',
            approved_at = NOW(),
            effective_from = NOW()
        WHERE policy_key = 'commerce-opportunity'
          AND policy_version = 'v1'
          AND status = 'approved';
        -- Repeat for product-recommendation:v1 and collection-recommendation:v1
        -- in advisory mode per Runtime document launch recommendation.

Step 5: commerce_opportunity_worker:v0.5.0 is enabled.
        First scoring run: a single known illustration opportunity
        (recommended: the Hayden Survey Map or an approved BHL opportunity).
        Assert: score ≥ 0.90 for MASTERWORK, audit log written, replay_verified event fires.

Step 6: Replay Gate 3 executes after first ten production scoring runs.
        If any replay_failure: pause worker, investigate before proceeding.

Step 7: Staleness worker enabled.
Step 8: product_recommendation_worker enabled (advisory mode).
Step 9: collection_recommendation_worker enabled (advisory mode).
```

No step may be skipped. Steps 2–4 must be executed by two different humans. The database
constraint (`approved_by IS DISTINCT FROM created_by`) enforces this at the row level.

---

## Rollback Posture

If a migration must be rolled back before any production scoring data exists:

- Drop workers and API routes before dropping tables.
- Execute migrations in reverse order: 23 → 22 → 21 → 20 → 19.
- Existing tables (`illustration_opportunities`, `collections`, etc.) are not affected — these
  migrations are additive.

If a migration must be rolled back after `score_audit_log` contains production data:

- Do not drop `score_audit_log`. Retire the affected policies instead.
- Set all `commerce_opportunities` records to `status = 'stale'` with `stale_reason = 'policy_changed'`.
- Preserve the full audit chain.
- A rollback that destroys audit history is a constitutional violation.
