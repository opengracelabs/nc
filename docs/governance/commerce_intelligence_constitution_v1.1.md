# Commerce Intelligence Constitution v1.1

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Ratified — implementation authorized for Migrations 19–23. |
| Supersedes | `commerce_intelligence_constitution_v1.md` (v1.0.0) |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Ratified | 2026-06-06 |
| Role | Principal Architect |

---

## Amendment Log — v1.0.0 → v1.1.0

The following Director Decisions were applied to resolve all implementation blockers
identified in the Implementation Readiness Audit (2026-06-06). No articles were deleted.
Affected articles are annotated `[Amended v1.1]`. Articles not listed are unchanged.

| Decision | Finding | Resolution | Articles Affected |
|---|---|---|---|
| B-1 | `score_audit_log` schema conflict | Hybrid: runtime fields + Constitution chain fields coexist | 24, 27, 28 |
| B-2 | Policy status vocabulary conflict | Unified 6-state: add `paused`, retain `pending_approval` + `superseded` | 5, 16, 22, 33 |
| B-3 | LOC source constraint blocks scoring | Migration 19a is mandatory; `CHECK (source IN ('bhl', 'loc'))` before M-22 | 35, 36, 37 |
| B-4 | `scoring_worker_role` unimplemented | RLS descoped for v0.5.0; workers connect as application user | 28, 36 |
| H-1 | CSM and COS reconciliation | Two-pass scorer: Pass 1 = COS (5 model subscores), Pass 2 = CSM (6 dimensions) | 8, 12, 13, 14, 23 |
| H-2 | `collection_fit_score` / `commercial_value_score` undefined | Columns renamed to match formula_spec: 5 model subscores are the authority | 8, 23 |
| D-1 | `input_hash` algorithm unspecified | SHA-256, lowercase hex, keys alpha-sorted, null values retained as JSON null | 15 |
| D-2 | Staleness detection unspecified | Polling: `last_scored_at` + `max_score_age_days` policy parameter | 38 (new) |
| D-3/D-5 | `place_iconic_taxa` / `taxon_commercial_tier` JSONB vs. table | Separate governed tables with independent lifecycle; policy JSONB references tables | 7, 22, 36 |

---

## Preamble

This Constitution establishes the governance model for the Commerce Intelligence layer of Nature &
Culture. It defines five governed entities and the rules that govern their creation, mutation,
replayability, and audit. It answers ten questions:

1. Final governance model
2. Final vocabularies
3. Final hard gates
4. Replayability requirements
5. Audit requirements
6. NIST alignment
7. Human approval boundaries
8. Policy version governance
9. Scoring policy lifecycle
10. Constitutional migration order

This Constitution is subordinate to the Strategic Directive and the Illustration Opportunity
Doctrine. Any provision of this Constitution that conflicts with those documents is void. This
Constitution governs the five entities below. It does not govern `illustration_opportunities`,
`assets`, `collections`, or any upstream entity. Those are governed by their own existing
constitutional rules, which this Constitution must not weaken.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration discovery and commerce
platform. It is not a biodiversity inventory.

**1.2** The commercial object is an Illustration Opportunity — not a species, not a taxon, not an
occurrence record. Taxa are metadata anchors. Places are commercial anchors. Illustrations are
commercial products.

**1.3** The Commerce Intelligence layer scores Illustration Opportunities for commercial routing. It
does not create opportunities. It does not approve rights. It does not generate products. It
classifies, scores, recommends, and records.

### Article 2 — Scope

This Constitution governs exactly five entities:

| Entity | Role |
|---|---|
| `commerce_policy` | Authoritative scoring parameters at runtime |
| `commerce_opportunities` | Scored commercial state of one Illustration Opportunity |
| `score_audit_log` | Append-only tamper-detected event record |
| `product_recommendations` | Derived product surface routing for curator review |
| `collection_recommendations` | Derived collection placement for curator review |

### Article 3 — Constitutional Authority Order

```
Strategic Directive
        ↓
Illustration Opportunity Doctrine
        ↓
Commerce Intelligence Constitution (this document)
        ↓
commerce_policy (active version)
        ↓
Workers / FastAPI
```

Workers and API endpoints derive their authority from the active `commerce_policy`. They do not
derive authority from this Constitution directly. This Constitution governs policy. Policy governs
execution.

### Article 4 — Doctrine of PostgreSQL Authority

**4.1** PostgreSQL is the sole authority for all commerce intelligence state. No scoring result,
routing decision, or governance event exists unless recorded in PostgreSQL.

**4.2** MinIO holds asset evidence files. Workers compute scores. FastAPI governs routing. Humans
approve decisions. AI provides advisory estimates. None of these are authoritative. The PostgreSQL
record is.

**4.3** The existing `asset_rights` constraint — `rights_status IN ('Public Domain', 'CC0')` — is a
constitutional floor. This Constitution adds gates above that floor. It does not lower it.

---

## Part II — Governed Vocabularies

### Article 5 — Commerce State Vocabularies `[Amended v1.1]`

These vocabularies govern status fields on the five governed entities. A field value outside its
governed vocabulary is invalid. The FastAPI boundary must reject it. Workers must not produce it.

| Vocabulary | Values |
|---|---|
| `policy_status` | `draft` \| `pending_approval` \| `active` \| `paused` \| `superseded` \| `retired` |
| `commerce_tier` | `tier_1` \| `tier_2` \| `tier_3` \| `blocked` |
| `csm_tier` | `MASTERWORK` \| `FLAGSHIP` \| `STANDARD` \| `REFERENCE` \| `BLOCKED` |
| `hard_gate_status` | `passed` \| `blocked_rights` \| `blocked_resolution` \| `blocked_quality` \| `blocked_legal` \| `not_evaluated` |
| `computation_trigger` | `initial` \| `policy_version_change` \| `signal_correction` \| `manual_recompute` \| `rights_update` |
| `curator_decision` | `approved` \| `rejected` \| `pending` \| `escalated` |
| `curator_review_reason` | `priority_illustrator` \| `boundary_case` \| `manual_flag` \| `rights_anomaly` \| `none` |
| `recommendation_status` | `pending_curator_review` \| `curator_approved` \| `curator_rejected` \| `assigned` \| `retired` |
| `collection_gap_type` | `fills_gap` \| `reinforces_strength` \| `expands_coverage` \| `flagship_anchor` \| `none` |
| `audit_event_type` | see Article 24 |
| `actor_type` | `system_worker` \| `curator` \| `policy_approver` \| `administrator` |

**B-2 Amendment note:** `paused` has been added to `policy_status`. The unified 6-state lifecycle is:
`draft → pending_approval → active ⇄ paused → superseded → retired`. `paused` allows a policy to
be suspended without immediate supersession — e.g., during an active investigation. A `paused` policy
does not score new opportunities. Existing scored records retain their tier assignments. A `paused`
policy may return to `active` (requires second-human approval) or transition to `superseded`.

**H-1 Amendment note:** `csm_tier` vocabulary has been added. It is a computed output of the
two-pass scorer (Article 13). It is distinct from `commerce_tier` (COS-derived) and is not used for
routing decisions. It is an advisory classification used by curators for product pricing and
collection strategy.

### Article 6 — Signal Vocabularies

Signal vocabularies govern the value space of scoring inputs. A scoring worker that produces a
value outside these constraints must fail, log a `score_error` event, and not advance.

| Signal Vocabulary | Values | Default if Missing |
|---|---|---|
| `taxon_commercial_tier` | `high` \| `moderate` \| `low` \| `none` | No default — must be seeded; absence blocks scoring |
| `color_profile` | `hand_colored` \| `chromolithograph` \| `bw_engraving` \| `photographic` \| `unknown` | `unknown` → `color_score = 0.30` |
| `resolution_tier` | `premium` \| `standard` \| `marginal` \| `blocked` | Derived from `image_width_px` at compute time |
| `place_tier` | `unesco_flagship` \| `national_park` \| `regional` \| `local` \| `none` | Sourced from concepts graph; `none` → `place_tier_score = 0.0` |
| `anchor_type` | `biological` \| `geographic` \| `cultural` | `biological` |

### Article 7 — Vocabulary Seeding Requirements `[Amended v1.1]`

The following reference vocabularies must be seeded and governed in PostgreSQL before the scoring
worker may activate. Absence does not block ingestion. It blocks scoring. An opportunity missing a
required vocabulary receives `hard_gate_status = 'not_evaluated'` until the vocabulary is seeded.

**D-3/D-5 Amendment:** `taxon_commercial_tier` and `place_iconic_taxa` are governed tables with
independent lifecycles. They are not embedded in `commerce_policy` JSONB. Changes to individual
entries do not require a policy version bump. Each entry in these tables has its own `authored_by`,
`approved_by`, `approved_at` fields and is subject to the second-human rule at the row level.

1. **`taxon_commercial_tier_vocabulary`** (governed table) — required for Retail and Reference
   subscores. Schema:

   ```
   taxon_commercial_tier_vocabulary
     id              UUID PRIMARY KEY
     taxon_key       TEXT NOT NULL UNIQUE    -- BHL or LOC taxon identifier
     tier            TEXT NOT NULL           -- 'high' | 'moderate' | 'low' | 'none'
     tier_rationale  TEXT
     status          TEXT NOT NULL DEFAULT 'proposed'
     authored_by     TEXT NOT NULL
     approved_by     TEXT                    -- required before status = 'active'
     approved_at     TIMESTAMPTZ
     created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
     updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
     CONSTRAINT chk_tier   CHECK (tier IN ('high','moderate','low','none'))
     CONSTRAINT chk_status CHECK (status IN ('proposed','active','retired'))
     CONSTRAINT chk_second_human CHECK (
       status != 'active' OR approved_by IS DISTINCT FROM authored_by
     )
   ```

   Tier guidance: `high` (birds, butterflies, orchids, marine life), `moderate` (large mammals,
   reptiles, trees, ferns), `low` (plain invertebrates, grasses, fungi), `none` (geographic or
   cultural anchor only).

2. **`priority_illustrators_vocabulary`** (governed table) — required for `illustrator_prestige`
   computation. Current governed list: Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel,
   Wolf. Additions require Principal Architect approval (second-human rule applies).

3. **`place_iconic_taxa_vocabulary`** (governed table) — required for `taxon_place_iconic` in the
   Tourism subscore. Schema:

   ```
   place_iconic_taxa_vocabulary
     id               UUID PRIMARY KEY
     place_id         UUID NOT NULL REFERENCES places(id)
     taxon_key        TEXT NOT NULL
     iconic_rationale TEXT
     status           TEXT NOT NULL DEFAULT 'proposed'
     authored_by      TEXT NOT NULL
     approved_by      TEXT
     approved_at      TIMESTAMPTZ
     created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
     UNIQUE (place_id, taxon_key)
     CONSTRAINT chk_status CHECK (status IN ('proposed','active','retired'))
     CONSTRAINT chk_second_human CHECK (
       status != 'active' OR approved_by IS DISTINCT FROM authored_by
     )
   ```

   Yellowstone is the first target. A minimum of five active entries per place is required before
   the Tourism subscore is considered meaningful for that place.

4. **`place_tier_vocabulary`** — sourced from the concepts graph. Requires `places` and concept
   vocabulary records to be complete for each place under scoring.

---

## Part III — Signal Classification

### Article 8 — The Four Signal Classes `[Amended v1.1]`

Signals are classified by their source and governance requirements. Classification determines when
a signal is readable, what happens when it is absent, and who can modify it.

#### Class A — Auto-Computable

Produced by workers from existing PostgreSQL records or asset metadata. No human input required.
Audit log entry required on write.

| Signal | Derived From | Absent Value |
|---|---|---|
| `rights_confidence` | Rights extractor + `asset_rights.rights_status` | `0.0` — hardest default, blocks scoring |
| `golden_age_factor` | `illustration_opportunities.publication_year` (1750–1900 → 1.0, outside → linear decay) | `0.0` |
| `institutional_credit` | `sources.source_id` vocabulary (LOC, BHL, Smithsonian = 1.0) | `0.5` |
| `provenance_completeness` | PREMIS and PROV-O field coverage ratio on the asset record | Computed |
| `resolution_tier_score` | `image_width_px` → tier map → numeric (see Article 12) | `0.0` if absent |
| `place_relevance_score` | `illustration_opportunity_places.relevance_score` (max over all linked places) | `0.0` |
| `place_tier_score` | Concepts graph via `place_tier` vocabulary | `0.0` |
| **Five model subscores** | Weighted sums from Class A and Class B signals per `formula_spec.subscores` | Computed (Pass 1) |
| `commerce_opportunity_score` | Weighted sum of five model subscores per `formula_spec.composite` | Computed (Pass 1) |
| `commerce_tier` | COS against `tier_thresholds`; hard gate checks override | Derived (Pass 1) |
| **Six CSM dimension scores** | Weighted sums from raw signals per `formula_spec.csm_dimension_map` | Computed (Pass 2) |
| `csm_score` | Weighted sum of six CSM dimensions per `csm_dimension_map.composite` | Computed (Pass 2) |
| `csm_tier` | CSM score against `csm_dimension_map.tier_thresholds` | Derived (Pass 2) |
| All product eligibility flags | Tier + subscore + image signal thresholds per `product_surface_requirements` | Derived |
| `hard_gate_status` | Hard gate evaluation (pre-scoring) | Derived |

**H-1/H-2 Amendment:** The five model subscores (`museum_score`, `retail_score`, `publishing_score`,
`tourism_score`, `reference_score`) are the authoritative runtime columns. The previous
`collection_fit_score` and `commercial_value_score` columns do not exist in this version. The
`csm_tier` is computed in Pass 2 from the same `score_inputs` snapshot. It is an advisory output
for curatorial use — it does not affect `commerce_tier` or product eligibility routing.

#### Class B — Governed-List Lookup

Value is computed by a worker against a governed vocabulary table seeded in PostgreSQL. The worker
computes; the governance table supplies the reference values. Conservative defaults apply when the
table is absent or the entry is missing.

| Signal | Governed Table | Absent Default |
|---|---|---|
| `illustrator_prestige` | `priority_illustrators_vocabulary` | `0.0` |
| `taxon_commercial_tier_score` | `taxon_commercial_tier_vocabulary` | `0.0` — not `none` |
| `taxon_place_iconic` | `place_iconic_taxa_vocabulary` per-place | `0.0` |

#### Class C — Human-Reviewed

Cannot advance past advisory estimate without human confirmation. AI may produce a pre-screen
estimate. The human value supersedes the AI estimate. Updates require actor and timestamp.

| Signal | Nature | AI Advisory Permitted? | Blocks Tier 1 and 2? |
|---|---|---|---|
| `image_quality_score` | Print-readiness assessment (0.0–1.0) | Yes | Yes — both blocked without confirmed value |
| `composition_fit` | Visual composition assessment (0.0–1.0) | Yes | Blocks premium wall art and puzzle |
| `identification_confidence` | Taxon clarity under ambiguity (0.0–1.0) | Yes | Blocks Publishing subscore above 0.5 |
| `color_profile` | Color process identification when EXIF absent | Yes | No — defaults to `unknown` |

When a Class C signal is corrected by a human:

1. Write `score_audit_log` entry: `event_type = 'signal_updated'`, `previous_state` = old value,
   `new_state` = new value, `actor_type = 'curator'`, `actor_id` = curator identifier.
2. Enqueue `signal_correction` recompute in `workflow_items`.
3. Recompute produces a new `score_audit_log` entry: `event_type = 'score_computed'`,
   `trigger = 'signal_correction'`, full `score_inputs` snapshot.
4. The old COS is superseded in `commerce_opportunities`. It is not deleted. It is retained in
   `score_audit_log`.

#### Class D — Boundary-Escalated Conditions

These are not signals. They are conditions that trigger mandatory curator review regardless of COS.
The review must complete before tier routing proceeds.

| Condition | Reason | Required Action |
|---|---|---|
| `illustrator_prestige = 1.0` | Priority illustrator — high misattribution risk | Curator verifies attribution before routing |
| COS within ±0.05 of any tier threshold | Boundary ambiguity | Curator reviews tier assignment |
| `rights_confidence` between 0.70 and 0.80 | Marginal rights confidence | Rights review before Tier 1 or Tier 2 |
| Any hard gate status changed by a worker | Possible system error | Curator acknowledges gate change |

---

## Part IV — Hard Gate Architecture

### Article 9 — Gate Definitions

Hard gates are sequential blocking conditions evaluated before COS computation proceeds. A gate
failure produces a specific `hard_gate_status` value and a `score_audit_log` entry. Gates are not
overridable by workers. Gates 0–4 are overridable only by a curator governance event. Gate 5 is
publication-stage only and lives outside `commerce_opportunities`.

**Gate 0 — Rights Record Existence**

```
Condition:   No asset_rights record exists for the linked asset.
Action:      hard_gate_status = 'blocked_rights'
             COS computation does not proceed.
             Audit log: event_type = 'hard_gate_blocked'
Cure:        asset_rights record created and approved.
Note:        This gate enforces the existing check_collection_asset_commercial_ready()
             constraint at the commerce intelligence layer, one stage earlier.
```

**Gate 1 — Rights Confidence**

```
Condition:   rights_confidence < 0.70
Action:      hard_gate_status = 'blocked_rights'
             COS computation does not proceed.
Cure:        Rights extractor updated; signal_correction recompute triggered.
```

**Gate 2 — Resolution**

```
Condition:   image_width_px < 2000
Action:      hard_gate_status = 'blocked_resolution'
             COS computation does not proceed.
Cure:        Higher-resolution source image acquired.
```

**Gate 3 — Legal Hold**

```
Condition:   rights_confidence = 0.0
             (rights extractor returned 'blocked' advisory)
Action:      hard_gate_status = 'blocked_legal'
             COS computation does not proceed.
Cure:        None at curator level. Requires source-level rights resolution.
             Curator authority does not extend to legal holds.
```

**Gate 4 — Quality**

```
Condition:   image_quality_score < 0.40 (human-reviewed value)
             OR image_quality_score IS NULL (not yet reviewed)
Action:      hard_gate_status = 'blocked_quality'
             COS is computed and stored but commerce_tier is forced to 'blocked'.
             All product eligibility flags set to FALSE.
Cure:        Human reviews image_quality_score.
             If score >= 0.40: trigger 'signal_correction' recompute; gate lifts.
             If score < 0.40:  hard_gate_status = 'blocked_quality' permanent.
Note:        Gate 4 is post-scoring. COS is computed to prioritize the human
             review queue. Gate 4 blocks routing, not scoring.
```

**Gate 5 — Curator Approval (Publication Stage)**

```
Condition:   curator_decision != 'approved'
             OR curator_reviewed_at IS NULL
Action:      No product_recommendations or collection_recommendations
             may advance to status = 'assigned'.
Location:    This gate lives in product_recommendations and
             collection_recommendations, not in commerce_opportunities.
```

### Article 10 — Gate Evaluation Order

Gates are evaluated in order 0 → 4 before COS computation. The first failing gate sets
`hard_gate_status` and stops evaluation. Gates do not stack. When Gate 3 fires, Gates 1 and 2
do not also fire.

### Article 11 — Gate Override Protocol

Gates 0–2 and Gate 4 may be resolved by a valid cure condition (signal correction or rights
update). The resolution is automatic when the cure condition is met. No manual override is needed.

A curator may manually escalate a gate result only when the automated cure path is unavailable.
Manual escalation requires:
1. A curator governance event in `score_audit_log`: `actor_type = 'curator'`, `actor_id` present.
2. A written `actor_notes` entry explaining the override reason.
3. The resulting COS computation flagged `requires_curator_review = TRUE`.

Gate 3 (`blocked_legal`) cannot be manually overridden at any level. It requires source-level
rights resolution and a new rights extractor run.

---

## Part V — Replayability

### Article 12 — The Replayability Guarantee

Replayability means: given only the data stored in PostgreSQL, any historical COS and CSM score
can be reproduced by any worker, at any time, without access to the original external source system.

This guarantee has three components:

**12.1 — Signal Snapshot.** At every scoring event, the full resolved value of every signal is
captured in `score_audit_log.score_inputs` (JSONB). Values are stored directly, not as references.
Example:

```json
{
  "illustrator_prestige": 1.0,
  "rights_confidence": 0.95,
  "golden_age_factor": 1.0,
  "institutional_credit": 1.0,
  "provenance_completeness": 0.88,
  "image_quality_score": 0.81,
  "composition_fit": 0.75,
  "taxon_commercial_tier": "high",
  "taxon_commercial_tier_score": 1.0,
  "identification_confidence": 0.92,
  "place_relevance_score": 0.87,
  "taxon_place_iconic": 1.0,
  "place_tier": "national_park",
  "place_tier_score": 0.75,
  "color_profile": "hand_colored",
  "color_score": 1.0,
  "image_width_px": 4800,
  "resolution_tier": "premium",
  "resolution_tier_score": 1.0
}
```

**12.2 — Policy Anchor.** `policy_version_id` is recorded on every `score_audit_log` entry. It
points to the exact `commerce_policy` record — including its `formula_spec` — in effect at compute
time. Superseded policies are retained permanently.

**12.3 — Output Snapshot.** `score_audit_log.score_outputs` records every subscore, the composite
COS, the commerce tier, the CSM score, and the CSM tier at compute time: `[Amended v1.1]`

```json
{
  "museum_score": 0.952,
  "retail_score": 0.884,
  "publishing_score": 0.887,
  "tourism_score": 0.867,
  "reference_score": 0.832,
  "commerce_opportunity_score": 0.886,
  "commerce_tier": "tier_1",
  "csm_score": 0.931,
  "csm_tier": "MASTERWORK"
}
```

The replay guarantee extends to both passes. The same `score_inputs` snapshot is used for Pass 1
(COS) and Pass 2 (CSM). A replay that confirms COS but produces a different `csm_tier` is a
`replay_failure`.

### Article 13 — The formula_spec Contract `[Amended v1.1]`

`commerce_policy.formula_spec` is a machine-readable JSON document that fully describes the
scoring algorithm for both passes. Workers derive all computation logic from this document. No
scoring weights, thresholds, or formula structure may be hardcoded in worker code.

**Constitutional minimum `formula_spec` structure (Pass 1 — COS):**

```json
{
  "scorer_version": "weighted_sum_v1",
  "subscores": {
    "museum_score": {
      "inputs": [
        { "signal": "illustrator_prestige",    "weight": 0.35 },
        { "signal": "rights_confidence",       "weight": 0.25 },
        { "signal": "golden_age_factor",       "weight": 0.20 },
        { "signal": "institutional_credit",    "weight": 0.10 },
        { "signal": "provenance_completeness", "weight": 0.10 }
      ]
    },
    "retail_score": {
      "inputs": [
        { "signal": "image_quality_score",         "weight": 0.30 },
        { "signal": "taxon_commercial_tier_score", "weight": 0.25 },
        { "signal": "resolution_tier_score",       "weight": 0.20 },
        { "signal": "composition_fit",             "weight": 0.15 },
        { "signal": "color_score",                 "weight": 0.10 }
      ]
    },
    "publishing_score": {
      "inputs": [
        { "signal": "identification_confidence",   "weight": 0.30 },
        { "signal": "image_quality_score",         "weight": 0.25 },
        { "signal": "golden_age_factor",           "weight": 0.20 },
        { "signal": "taxon_commercial_tier_score", "weight": 0.15 },
        { "signal": "rights_confidence",           "weight": 0.10 }
      ]
    },
    "tourism_score": {
      "inputs": [
        { "signal": "place_relevance_score", "weight": 0.35 },
        { "signal": "taxon_place_iconic",    "weight": 0.25 },
        { "signal": "place_tier_score",      "weight": 0.20 },
        { "signal": "image_quality_score",   "weight": 0.20 }
      ]
    },
    "reference_score": {
      "inputs": [
        { "signal": "identification_confidence",   "weight": 0.35 },
        { "signal": "taxon_commercial_tier_score", "weight": 0.20 },
        { "signal": "golden_age_factor",           "weight": 0.20 },
        { "signal": "image_quality_score",         "weight": 0.15 },
        { "signal": "provenance_completeness",     "weight": 0.10 }
      ]
    }
  },
  "composite": {
    "inputs": [
      { "signal": "retail_score",    "weight": 0.30 },
      { "signal": "tourism_score",   "weight": 0.25 },
      { "signal": "museum_score",    "weight": 0.20 },
      { "signal": "publishing_score","weight": 0.15 },
      { "signal": "reference_score", "weight": 0.10 }
    ]
  },
  "signal_defaults": {
    "image_quality_score":       null,
    "composition_fit":           null,
    "identification_confidence": 0.0,
    "taxon_place_iconic":        0.0,
    "color_profile":             "unknown",
    "color_score":               0.30
  },
  "null_signal_policy": "null_blocks_tier_12_advancement",
  "resolution_tier_map": {
    "premium":  { "min_width_px": 4000, "score": 1.00 },
    "standard": { "min_width_px": 2000, "score": 0.75 },
    "marginal": { "min_width_px": 1200, "score": 0.40 },
    "blocked":  { "min_width_px": 0,    "score": 0.00 }
  }
}
```

**Constitutional minimum `csm_dimension_map` block (Pass 2 — CSM): `[Amended v1.1]`**

The `csm_dimension_map` is a top-level sibling of `subscores` in `formula_spec`. It is evaluated
after Pass 1. It uses the same `score_inputs` snapshot. No new signals are required.

```json
{
  "csm_dimension_map": {
    "scorer_version": "csm_pass2_v1",
    "dimensions": {
      "VAS": {
        "label": "Visual Authority Score",
        "csm_weight": 0.30,
        "inputs": [
          { "signal": "image_quality_score",     "weight": 0.50 },
          { "signal": "composition_fit",         "weight": 0.30 },
          { "signal": "color_score",             "weight": 0.20 }
        ]
      },
      "PIS": {
        "label": "Place Identity Score",
        "csm_weight": 0.20,
        "inputs": [
          { "signal": "place_relevance_score",   "weight": 0.60 },
          { "signal": "taxon_place_iconic",      "weight": 0.40 }
        ]
      },
      "SSS": {
        "label": "Story Strength Score",
        "csm_weight": 0.15,
        "inputs": [
          { "signal": "provenance_completeness", "weight": 0.40 },
          { "signal": "golden_age_factor",       "weight": 0.35 },
          { "signal": "illustrator_prestige",    "weight": 0.25 }
        ]
      },
      "TAS": {
        "label": "Tourism Appeal Score",
        "csm_weight": 0.15,
        "inputs": [
          { "signal": "taxon_place_iconic",      "weight": 0.40 },
          { "signal": "place_tier_score",        "weight": 0.35 },
          { "signal": "place_relevance_score",   "weight": 0.25 }
        ]
      },
      "IPS": {
        "label": "Institutional Prestige Score",
        "csm_weight": 0.10,
        "inputs": [
          { "signal": "institutional_credit",    "weight": 0.70 },
          { "signal": "provenance_completeness", "weight": 0.30 }
        ]
      },
      "PVS": {
        "label": "Product Versatility Score",
        "csm_weight": 0.10,
        "inputs": [
          { "signal": "resolution_tier_score",        "weight": 0.70 },
          { "signal": "identification_confidence",    "weight": 0.30 }
        ]
      }
    },
    "composite": {
      "inputs": [
        { "signal": "VAS", "weight": 0.30 },
        { "signal": "PIS", "weight": 0.20 },
        { "signal": "SSS", "weight": 0.15 },
        { "signal": "TAS", "weight": 0.15 },
        { "signal": "IPS", "weight": 0.10 },
        { "signal": "PVS", "weight": 0.10 }
      ]
    },
    "tier_thresholds": {
      "MASTERWORK": 0.90,
      "FLAGSHIP":   0.75,
      "STANDARD":   0.60,
      "REFERENCE":  0.40,
      "BLOCKED":    0.00
    },
    "null_signal_policy": "null_blocks_MASTERWORK_FLAGSHIP",
    "rcs_gate": "rights_confidence >= 0.70 required for any csm_tier above BLOCKED"
  }
}
```

**Two-pass scoring algorithm:**

```
Pass 1 — COS:
  1. Evaluate hard gates 0–4. Abort if any gate fails.
  2. Resolve all Class A and B signals from PostgreSQL.
  3. Apply formula_spec.subscores to compute museum_score, retail_score,
     publishing_score, tourism_score, reference_score.
  4. Apply formula_spec.composite to compute commerce_opportunity_score (COS).
  5. Derive commerce_tier from COS and tier_thresholds.
  6. Evaluate product eligibility flags.
  7. Write score_inputs and score_outputs (Pass 1 portion) to score_audit_log.

Pass 2 — CSM:
  8. Using the same score_inputs from step 2 (no re-fetch):
  9. Apply csm_dimension_map.dimensions to compute VAS, PIS, SSS, TAS, IPS, PVS.
  10. Apply csm_dimension_map.composite to compute csm_score.
  11. Derive csm_tier from csm_score and csm_dimension_map.tier_thresholds.
  12. Append csm_score and csm_tier to score_outputs in the same score_audit_log entry.

Passes 1 and 2 are written in one atomic score_audit_log INSERT.
csm_tier does not affect commerce_tier. It does not affect product eligibility routing.
csm_tier is advisory for curatorial use only.
```

**Invariants enforced at policy approval:**

- The weights within each subscore input array must sum to exactly `1.00`.
- The composite input weights must sum to exactly `1.00`.
- The CSM dimension input weights within each dimension must sum to exactly `1.00`.
- The `csm_dimension_map.composite` weights must sum to exactly `1.00`.
- `scorer_version` must match a registered algorithm in the scoring worker.
- `csm_dimension_map.scorer_version` must match a registered algorithm in the scoring worker.
- A policy is rejected at the `pending_approval → active` gate if any invariant fails.

### Article 14 — The Replay Protocol `[Amended v1.1]`

The replay worker operates as follows for any `score_audit_log` entry:

```
1. Load score_audit_log entry N for opportunity X.
2. Load commerce_policy where id = entry_N.policy_version_id.
3a. Apply formula_spec.scorer_version algorithm (Pass 1) to entry_N.score_inputs.
    Assert computed Pass 1 result == entry_N.score_outputs (COS, commerce_tier, subscores).
3b. Apply csm_dimension_map.scorer_version algorithm (Pass 2) to entry_N.score_inputs.
    Assert computed Pass 2 result == entry_N.score_outputs (csm_score, csm_tier).
4a. If both passes pass: write audit event_type = 'replay_verified'.
4b. If either pass fails: write audit event_type = 'replay_failure'.
    Flag commerce_opportunity for opportunity X as integrity_suspect.
    Remove from active product routing pending investigation.
```

A `replay_failure` is a constitutional breach. It must be investigated before any further scoring
of the affected opportunity proceeds.

### Article 15 — Hash Chain Integrity `[Amended v1.1]`

Each `score_audit_log` entry includes:

- **`entry_checksum_sha256`** — SHA-256 over `(opportunity_id || event_type || event_at || actor_id || score_inputs_canonical || score_outputs_canonical)`. Canonical form: JSON keys sorted alphabetically, no surplus whitespace, **null values retained as JSON null** (not omitted), floating-point values serialized to 6 decimal places. Output: lowercase hex string.
- **`previous_entry_checksum`** — the `entry_checksum_sha256` of the preceding entry for the same `opportunity_id`. Null for the first entry per opportunity. Forms a per-opportunity hash chain.

**D-1 Amendment:** Canonical JSON form explicitly includes null-valued fields as `null` (they are
not omitted). This ensures the checksum surface is deterministic across all workers regardless of
implementation language. Two workers computing `entry_checksum_sha256` from the same
`score_audit_log` record must produce identical output.

A broken chain (checksum mismatch, unexpected null, or missing chain link) is treated as a
`replay_failure`.

---

## Part VI — Policy Version Governance

### Article 16 — Policy Lifecycle `[Amended v1.1]`

```
draft
  ↓ authored by one human
pending_approval
  ↓ approved by a second human (not the author)
active  ─────────────────────────── (one active record at all times)
  ↓ suspended without supersession   ↑ reinstated (second-human approval required)
paused  ────────────────────────────
  ↓ when a new policy is activated (from active or paused)
superseded  ─────────────────────── (immutable; retained for replayability)
  ↓ when all references migrate
retired
```

**B-2 Amendment:** `paused` has been added between `active` and `superseded`. A `paused` policy
does not score new opportunities but is not immediately superseded. Reinstatement from `paused`
to `active` requires second-human approval. A `paused` policy does not count toward the
"one active at a time" constraint. If no policy is `active` (because the only active policy was
paused), the scoring worker halts and no new scores are produced until a policy is reinstated or
a new policy is activated.

Exactly one `commerce_policy` record may hold `status = 'active'` at any time. This is enforced
by a constraint trigger, not by application logic.

### Article 17 — The Second-Human Rule

A `commerce_policy` record may not transition from `pending_approval` to `active` unless
`approved_by` is set to a human identifier that is different from `authored_by`. Self-approval is
constitutionally prohibited.

### Article 18 — Immutability After Activation

Once a `commerce_policy` record reaches `active`, the following fields are immutable:

- `formula_spec`
- `composite_weights`
- `tier_thresholds`
- `hard_gate_values`
- `model_activation_thresholds`
- `product_surface_requirements`
- `scorer_version`

Mutation of any immutable field after activation is a constitutional violation. The only path to
change any scoring parameter is a new policy version. This is enforced by a constraint trigger
that raises an exception on any UPDATE to these fields when
`status IN ('active', 'paused', 'superseded')`.

### Article 19 — Version Semantics

Policy versions follow semantic versioning with governed meaning:

| Change Type | Version Increment | Reapproval Required |
|---|---|---|
| Vocabulary addition, signal default correction, documentation | Patch (1.0.0 → 1.0.1) | Author review; no second approver required |
| Composite weight change, model weight change | Minor (1.0.0 → 1.1.0) | Second-human approval required |
| Tier threshold change, hard gate value change | Minor (1.0.0 → 1.1.0) | Second-human approval + Principal Architect flag |
| Scorer algorithm change (`formula_spec` structure) | Major (1.0.0 → 2.0.0) | Full governance review |
| New model subscore added or removed | Major | Full governance review; all active `product_recommendations` expire |

A major version change sets all active `product_recommendations` and `collection_recommendations`
to `status = 'retired'`. They are not deleted. The recompute queue rescores all active
opportunities under the new policy.

### Article 20 — Recompute Queue on Policy Activation

When a new policy transitions to `active`:

1. The previous `active` policy transitions to `superseded`.
2. A recompute queue entry is created in `workflow_items` for every `commerce_opportunities`
   record where `status NOT IN ('blocked', 'archived')`.
3. Recompute is asynchronous. During transition, stale records are flagged
   `policy_stale = TRUE` on `commerce_opportunities`.
4. A stale record retains its existing tier and routing eligibility until recomputed. It does not
   lose commercial status during transition.
5. The curator is notified of queue depth before activation is confirmed.

### Article 21 — Policy Retirement

A `superseded` policy may transition to `retired` only when all three conditions hold:

1. Zero `commerce_opportunities` records reference it as `policy_version_id`.
2. Zero `product_recommendations` or `collection_recommendations` records reference it.
3. The `score_audit_log` hash chain for all entries under that policy has passed replay
   verification.

`score_audit_log` entries and the policy record itself are retained permanently after retirement.
Retirement means no new references — not deletion.

---

## Part VII — Entity Specifications

### Article 22 — `commerce_policy` `[Amended v1.1]`

One record is `active` at all times. All others are `draft`, `pending_approval`, `paused`,
`superseded`, or `retired`.

```
commerce_policy
  id                            UUID PRIMARY KEY
  version                       TEXT NOT NULL UNIQUE          -- semver: "1.0.0"
  status                        TEXT NOT NULL                 -- policy_status: 6-state vocabulary
  effective_from                TIMESTAMPTZ                   -- when active
  effective_until               TIMESTAMPTZ                   -- null = still active or paused
  authored_by                   TEXT NOT NULL
  approved_by                   TEXT                          -- required for active; != authored_by
  approved_at                   TIMESTAMPTZ
  changelog                     TEXT NOT NULL                 -- what changed from previous version
  previous_version_id           UUID REFERENCES commerce_policy(id)
  max_score_age_days            INT NOT NULL DEFAULT 90       -- staleness threshold (Article 38)

  formula_spec                  JSONB NOT NULL                -- machine-readable scoring algorithm
  composite_weights             JSONB NOT NULL                -- subscore weights (must sum to 1.00)
  tier_thresholds               JSONB NOT NULL                -- tier_1, tier_2, tier_3 cutoffs
  hard_gate_values              JSONB NOT NULL                -- min_rights_confidence, min_image_width_px, min_quality_score
  model_activation_thresholds   JSONB NOT NULL                -- museum_unlock, tourism_unlock, etc.
  product_surface_requirements  JSONB NOT NULL                -- per-surface minimum requirements

  provenance                    JSONB NOT NULL DEFAULT '{}'
  created_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()

Constraints:
  CHECK (status IN ('draft','pending_approval','active','paused','superseded','retired'))
  UNIQUE partial index: one status = 'active' at a time
  CHECK (approved_by IS NOT NULL) WHERE status IN ('active','paused','superseded')
  CHECK (approved_by IS DISTINCT FROM authored_by)
  Immutability trigger on formula_spec and threshold fields when
    status IN ('active','paused','superseded')
```

`product_surface_requirements` governs which COS, subscore, and image signal minimums must be met
for each product surface. Initial v1.0.0 values:

```json
{
  "wall_art_premium":       { "min_cos": 0.80, "min_image_width_px": 4000, "min_quality_score": 0.75 },
  "wall_art_standard":      { "min_cos": 0.65, "min_image_width_px": 2000, "min_quality_score": 0.55 },
  "calendar":               { "min_cos": 0.65, "min_composition_fit": 0.60 },
  "puzzle":                 { "min_cos": 0.60, "min_composition_fit": 0.65 },
  "card":                   { "min_cos": 0.55, "min_image_width_px": 1200, "min_quality_score": 0.50 },
  "book_illustration":      { "min_publishing_score": 0.70, "min_identification_confidence": 0.85 },
  "educational":            { "min_reference_score": 0.65 },
  "museum_print":           { "min_museum_score": 0.80, "illustrator_prestige": 1.0, "min_rights_confidence": 1.0 },
  "institutional_license":  { "min_museum_score": 0.80, "min_rights_confidence": 1.0 }
}
```

### Article 23 — `commerce_opportunities` `[Amended v1.1]`

One record per Illustration Opportunity. Updated on recompute. Full history in `score_audit_log`.

```
commerce_opportunities
  id                          UUID PRIMARY KEY
  opportunity_id              UUID NOT NULL UNIQUE FK → illustration_opportunities
  policy_version_id           UUID NOT NULL FK → commerce_policy
  computed_at                 TIMESTAMPTZ NOT NULL
  computed_by                 TEXT NOT NULL             -- worker_id or curator_id
  computation_trigger         TEXT NOT NULL             -- computation_trigger vocabulary
  policy_stale                BOOLEAN NOT NULL DEFAULT FALSE
  last_scored_at              TIMESTAMPTZ               -- used by staleness worker (Article 38)

  -- Hard gate
  hard_gate_status            TEXT NOT NULL             -- hard_gate_status vocabulary

  -- Class A signals (values at compute time — not live references)
  rights_confidence           NUMERIC(4,3)
  golden_age_factor           NUMERIC(4,3)
  institutional_credit        NUMERIC(4,3)
  provenance_completeness     NUMERIC(4,3)
  resolution_tier_score       NUMERIC(4,3)
  place_relevance_score       NUMERIC(4,3)
  place_tier_score            NUMERIC(4,3)

  -- Class B signals
  illustrator_prestige        NUMERIC(4,3)
  taxon_commercial_tier       TEXT                      -- taxon_commercial_tier vocabulary
  taxon_commercial_tier_score NUMERIC(4,3)
  taxon_place_iconic          NUMERIC(4,3)

  -- Class C signals (human-reviewed)
  image_quality_score         NUMERIC(4,3)              -- null until reviewed
  image_quality_reviewed_by   TEXT
  image_quality_reviewed_at   TIMESTAMPTZ
  composition_fit             NUMERIC(4,3)              -- null until reviewed
  identification_confidence   NUMERIC(4,3)
  color_profile               TEXT                      -- color_profile vocabulary
  color_score                 NUMERIC(4,3)

  -- Derived image signals
  image_width_px              INT
  resolution_tier             TEXT                      -- resolution_tier vocabulary

  -- Five model subscores (Pass 1)
  museum_score                NUMERIC(4,3)
  retail_score                NUMERIC(4,3)
  publishing_score            NUMERIC(4,3)
  tourism_score               NUMERIC(4,3)
  reference_score             NUMERIC(4,3)

  -- Composite (Pass 1)
  commerce_opportunity_score  NUMERIC(4,3)
  commerce_tier               TEXT                      -- commerce_tier vocabulary

  -- CSM (Pass 2)
  csm_score                   NUMERIC(4,3)
  csm_tier                    TEXT                      -- csm_tier vocabulary (advisory only)

  -- Product surface eligibility
  eligible_wall_art_premium           BOOLEAN NOT NULL DEFAULT FALSE
  eligible_wall_art_standard          BOOLEAN NOT NULL DEFAULT FALSE
  eligible_calendar                   BOOLEAN NOT NULL DEFAULT FALSE
  eligible_puzzle                     BOOLEAN NOT NULL DEFAULT FALSE
  eligible_card                       BOOLEAN NOT NULL DEFAULT FALSE
  eligible_book_illustration          BOOLEAN NOT NULL DEFAULT FALSE
  eligible_educational                BOOLEAN NOT NULL DEFAULT FALSE
  eligible_museum_print               BOOLEAN NOT NULL DEFAULT FALSE
  eligible_institutional_license      BOOLEAN NOT NULL DEFAULT FALSE

  -- Curator review
  requires_curator_review     BOOLEAN NOT NULL DEFAULT FALSE
  curator_review_reason       TEXT                      -- curator_review_reason vocabulary
  curator_decision            TEXT NOT NULL DEFAULT 'pending'  -- curator_decision vocabulary
  curator_reviewed_by         TEXT
  curator_reviewed_at         TIMESTAMPTZ
  curator_notes               TEXT

  -- Full input snapshot (replayability — values, not references)
  score_inputs                JSONB NOT NULL DEFAULT '{}'

  status                      TEXT NOT NULL DEFAULT 'pending_review'
  provenance                  JSONB NOT NULL DEFAULT '{}'
  created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()

Constraints:
  UNIQUE (opportunity_id)
  CHECK (commerce_tier IN commerce_tier vocabulary)
  CHECK (csm_tier IN csm_tier vocabulary OR csm_tier IS NULL)
  CHECK (hard_gate_status IN hard_gate_status vocabulary)
  CHECK (curator_decision IN curator_decision vocabulary)
  CHECK (all NUMERIC scores BETWEEN 0 AND 1 OR NULL)
  Constraint trigger: hard_gate_status != 'passed' → all eligible_* = FALSE
  Constraint trigger: commerce_opportunity_score IS NOT NULL → score_audit_log entry must exist
```

**H-2 Amendment:** `collection_fit_score` and `commercial_value_score` do not exist in this
schema. The five model subscores (`museum_score`, `retail_score`, `publishing_score`,
`tourism_score`, `reference_score`) are the authoritative runtime columns. The runtime document
must be amended to match this schema before Migration 21 DDL is written.

**Tier boundaries (v1.0.0):**

| Tier | COS Range | Commercial Treatment |
|---|---|---|
| `tier_1` | ≥ 0.80 | All surfaces eligible. Premium pricing. Museum and institutional licensing available. |
| `tier_2` | 0.65 – 0.79 | Wall art, calendar, puzzle, card eligible. Standard pricing. |
| `tier_3` | 0.50 – 0.64 | Educational and reference licensing only. No retail surfaces. |
| `blocked` | < 0.50 or gate failed | No commercial routing. Archived as provenance record only. |

### Article 24 — `score_audit_log` `[Amended v1.1]`

Append-only. No updates. No deletes. Enforced by PostgreSQL rules. The NIST audit record.

```
score_audit_log
  id                          UUID PRIMARY KEY
  opportunity_id              UUID NOT NULL FK → illustration_opportunities
                                              -- FK to illustration_opportunities, not to
                                              -- commerce_opportunities, so the audit record
                                              -- survives future opportunity restructuring.
  policy_version_id           UUID NOT NULL FK → commerce_policy
  event_type                  TEXT NOT NULL   -- audit_event_type vocabulary (see below)
  event_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
  actor_type                  TEXT NOT NULL   -- actor_type vocabulary
  actor_id                    TEXT NOT NULL   -- worker_id or human identifier; never anonymous
  actor_notes                 TEXT            -- required for curator events

  trigger                     TEXT NOT NULL   -- computation_trigger vocabulary

  score_inputs                JSONB NOT NULL DEFAULT '{}'   -- full signal snapshot (values, not refs)
  score_outputs               JSONB NOT NULL DEFAULT '{}'   -- all subscores + COS + tier + CSM
  previous_state              JSONB NOT NULL DEFAULT '{}'   -- commerce_opportunities before event
  new_state                   JSONB NOT NULL DEFAULT '{}'   -- commerce_opportunities after event

  -- Hash chain integrity (NIST AU-9)
  entry_checksum_sha256       TEXT NOT NULL                 -- tamper detection
  previous_entry_checksum     TEXT                          -- hash chain; null for first entry per opportunity

  -- Human-readable context (B-1 hybrid addition)
  reason                      TEXT NOT NULL                 -- human-readable event description
  generated_by                TEXT NOT NULL                 -- worker version tag or curator identifier

  created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()

audit_event_type vocabulary:
  'score_computed'        COS and CSM computed or recomputed (both passes)
  'signal_updated'        Class C signal corrected by human
  'hard_gate_blocked'     Hard gate evaluation blocked scoring
  'hard_gate_passed'      Hard gate status resolved
  'curator_reviewed'      Curator approved, rejected, or escalated
  'tier_assigned'         commerce_tier set or changed
  'policy_applied'        New policy version applied to existing record
  'eligibility_updated'   Product eligibility flags changed
  'score_archived'        Opportunity removed from active scoring
  'replay_verified'       Replay worker confirmed COS and CSM reproducibility
  'replay_failure'        Replay worker detected inconsistency in either pass

Constraints:
  PostgreSQL RULE: no UPDATE permitted on score_audit_log
  PostgreSQL RULE: no DELETE permitted on score_audit_log
  CHECK (actor_type IN actor_type vocabulary)
  CHECK (entry_checksum_sha256 IS NOT NULL)
  CHECK (event_type IN audit_event_type vocabulary)
```

**B-1 Amendment:** `reason` and `generated_by` are added from the runtime document as
human-readable context fields. They coexist with `actor_id`, `actor_type`, and `event_type` (the
governance fields). `actor_id` + `event_type` are the authoritative audit fields for NIST
compliance. `reason` + `generated_by` are readable summaries for operators. Neither field
supersedes the other. Both are NOT NULL — every audit event must have a human-readable reason.

### Article 25 — `product_recommendations`

Derived from `commerce_opportunities`. Recommends product families and types for curator review.
Does not generate products. Does not write to Shopify.

```
product_recommendations
  id                          UUID PRIMARY KEY
  opportunity_id              UUID NOT NULL FK → illustration_opportunities
  commerce_opportunity_id     UUID NOT NULL FK → commerce_opportunities
  policy_version_id           UUID NOT NULL FK → commerce_policy
  recommended_product_family  TEXT NOT NULL   -- product family vocabulary
  recommended_product_types   JSONB NOT NULL DEFAULT '{}'
  recommended_providers       JSONB NOT NULL DEFAULT '{}'
  recommendation_confidence   NUMERIC(4,3)
  recommendation_basis        JSONB NOT NULL DEFAULT '{}'   -- explainability record

  status                      TEXT NOT NULL DEFAULT 'pending_curator_review'
  curator_reviewed_by         TEXT
  curator_reviewed_at         TIMESTAMPTZ
  curator_decision_notes      TEXT

  provenance                  JSONB NOT NULL DEFAULT '{}'
  created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()

Constraints:
  UNIQUE (opportunity_id, recommended_product_family)
  CHECK (status IN recommendation_status vocabulary)
  CHECK (recommendation_confidence BETWEEN 0 AND 1)
  CHECK: may only be created when commerce_opportunities.curator_decision = 'approved'
```

`recommendation_basis` is the per-decision explainability record. Required fields:

```json
{
  "primary_model": "retail",
  "primary_model_score": 0.884,
  "threshold_applied": "wall_art_standard",
  "threshold_value": 0.65,
  "score_exceeded_by": 0.234,
  "signals_driving_recommendation": [
    { "signal": "image_quality_score", "value": 0.81, "weight": 0.30, "contribution": 0.243 },
    { "signal": "taxon_commercial_tier_score", "value": 1.0, "weight": 0.25, "contribution": 0.250 }
  ]
}
```

An auditor reading `recommendation_basis` must be able to understand why this product family was
recommended without access to any other system.

### Article 26 — `collection_recommendations`

Derived from `commerce_opportunities`. Recommends which collection an opportunity should join, or
proposes a new collection. Does not modify `collection_assets`.

```
collection_recommendations
  id                          UUID PRIMARY KEY
  opportunity_id              UUID NOT NULL FK → illustration_opportunities
  commerce_opportunity_id     UUID NOT NULL FK → commerce_opportunities
  policy_version_id           UUID NOT NULL FK → commerce_policy
  recommended_collection_id   UUID FK → collections          -- null if new collection proposed
  new_collection_proposal     JSONB DEFAULT '{}'              -- theme, place, title concept
  fit_score                   NUMERIC(4,3) NOT NULL
  fit_basis                   JSONB NOT NULL DEFAULT '{}'     -- explainability record
  collection_gap_type         TEXT NOT NULL DEFAULT 'none'    -- collection_gap_type vocabulary

  status                      TEXT NOT NULL DEFAULT 'pending_curator_review'
  curator_reviewed_by         TEXT
  curator_reviewed_at         TIMESTAMPTZ
  curator_decision_notes      TEXT

  provenance                  JSONB NOT NULL DEFAULT '{}'
  created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()

Constraints:
  CHECK (recommended_collection_id IS NOT NULL OR new_collection_proposal != '{}')
  CHECK (status IN recommendation_status vocabulary)
  CHECK (collection_gap_type IN collection_gap_type vocabulary)
  CHECK (fit_score BETWEEN 0 AND 1)
  CHECK: may only be created when commerce_opportunities.curator_decision = 'approved'
```

`collection_gap_type` values:

| Value | Meaning |
|---|---|
| `fills_gap` | Collection has a thematic gap this opportunity addresses |
| `reinforces_strength` | Deepens the collection's strongest existing theme |
| `expands_coverage` | Adds a new place or taxon within scope |
| `flagship_anchor` | Hero asset that anchors the collection's commercial identity |
| `none` | No fit identified; curator decides |

---

## Part VIII — Audit Architecture

### Article 27 — Audit Record Content (NIST AU-3) `[Amended v1.1]`

Every `score_audit_log` entry must contain:

| NIST Field | NC Field | Requirement |
|---|---|---|
| Who | `actor_type` + `actor_id` | Mandatory; no anonymous events permitted |
| What | `event_type` + `score_inputs` + `score_outputs` | Mandatory; full snapshot required; `score_outputs` includes both COS and CSM |
| When | `event_at` | Mandatory; server-side timestamp |
| Where | `opportunity_id` + `policy_version_id` | Mandatory; both anchors required |
| Why | `trigger` + `reason` + `actor_notes` | `trigger` and `reason` mandatory; `actor_notes` required for all curator events |

### Article 28 — Audit Record Protection (NIST AU-9) `[Amended v1.1]`

The `score_audit_log` table is protected by four independent mechanisms:

1. **PostgreSQL RULE (no UPDATE):** Any UPDATE statement on `score_audit_log` raises an
   exception at the database level.
2. **PostgreSQL RULE (no DELETE):** Any DELETE statement raises an exception at the database
   level.
3. **Entry checksum:** `entry_checksum_sha256` covers the full record content. Modification
   invalidates the checksum.
4. **Hash chain:** `previous_entry_checksum` links entries per opportunity. A broken chain
   triggers `replay_failure`.
5. **Role privilege separation (deferred — v0.5.0):** Database-level INSERT-only privilege for
   the scoring worker role is deferred to a future migration. For v0.5.0, workers connect as the
   application database user. Mechanisms 1–4 provide tamper detection without database role
   separation. Role separation is scheduled for the migration following v0.5.0 activation.

**B-4 Amendment:** The scoring worker role and row-level security architecture are descoped for
v0.5.0. Migration 22 does not include `CREATE ROLE` or `REVOKE` statements. This is documented
as a known limitation, not a constitutional waiver. The append-only PostgreSQL RULE and hash
chain integrity remain in effect and provide the primary tamper-detection guarantees.

### Article 29 — Audit Record Generation (NIST AU-12)

Only the following components may write to `score_audit_log`:

| Component | Events Generated |
|---|---|
| Scoring worker | `score_computed`, `hard_gate_blocked`, `hard_gate_passed`, `tier_assigned`, `eligibility_updated` |
| FastAPI curator endpoint | `signal_updated`, `curator_reviewed` |
| Policy activation worker | `policy_applied` |
| Replay worker | `replay_verified`, `replay_failure` |
| Archival worker | `score_archived` |

No other component may write to `score_audit_log`. The FastAPI gateway validates `actor_type`
before accepting any log write.

### Article 30 — Non-Repudiation

Every audit entry includes a stable, non-reusable `actor_id`. For human actors: the curator's
governed identity from the FastAPI authentication system. For workers: the worker process
identifier including version tag. An audit entry with an unresolvable `actor_id` is flagged as
`integrity_suspect` and triggers curator review.

### Article 31 — NIST AI RMF Alignment

Because the scoring system uses AI-advisory signals (Class C pre-screening estimates), the
following AI RMF principles apply:

| Principle | NC Mechanism |
|---|---|
| Transparency | `commerce_policy.formula_spec` is the transparency artifact. Human-readable. Stored in PostgreSQL. Both Pass 1 (COS) and Pass 2 (CSM) algorithms are fully specified. |
| Explainability | `recommendation_basis` on `product_recommendations` is the per-decision explainability artifact. |
| Human Oversight | Class D escalation conditions and Gate 5 preserve human oversight at every routing decision. AI estimates are advisory only. |
| Accuracy and Reliability | The replay protocol (Article 14) is the accuracy verification mechanism. Both passes are verified. |
| Bias Mitigation | COS must not correlate with GBIF occurrence frequency, species popularity, or taxonomic inventory completeness. Any such correlation in a replay analysis indicates a contaminated signal and is a constitutional breach. |

---

## Part IX — Human Approval Boundaries

### Article 32 — The Approval Chain

```
illustration_opportunity (curator approved)
          ↓
commerce_opportunity (scoring worker computes COS + CSM)
          ↓
Curator reviews COS, commerce_tier, and csm_tier (curator_decision = 'approved')
          ↓
product_recommendations generated (status = 'pending_curator_review')
          ↓
Curator approves product recommendation (status = 'curator_approved')
          ↓
collection_recommendations generated (status = 'pending_curator_review')
          ↓
Curator assigns to collection (status = 'assigned')
          ↓
collection_assets (existing governance chain)
          ↓
Product publication (existing collection_product_profile chain)
```

No step in this chain may be skipped or delegated to a worker. Workers compute. Humans approve.

### Article 33 — Mandatory Human Events `[Amended v1.1]`

The following events require a human actor. Workers must not produce them.

| Event | Required Actor | Recorded In |
|---|---|---|
| `policy_status: pending_approval → active` | Second human (not author) | `commerce_policy.approved_by` |
| `policy_status: paused → active` | Second human (not original author) | `commerce_policy.approved_by` (updated) |
| `curator_decision: pending → approved` (opportunity) | Curator | `commerce_opportunities.curator_reviewed_by` |
| `curator_decision: pending → rejected` | Curator | `commerce_opportunities.curator_reviewed_by` |
| `curator_decision: pending → escalated` | Curator | `commerce_opportunities` + `score_audit_log` |
| Class C signal update | Curator | `score_audit_log` event_type = 'signal_updated' |
| Gate 3 legal hold escalation | Curator (acknowledgement only; cannot cure) | `score_audit_log` |
| `recommendation_status: → curator_approved` | Curator | `product_recommendations.curator_reviewed_by` |
| `recommendation_status: → assigned` | Curator | `collection_recommendations.curator_reviewed_by` |
| `image_quality_score` initial set | Curator | `commerce_opportunities.image_quality_reviewed_by` |
| `taxon_commercial_tier_vocabulary` entry: proposed → active | Second human (not author) | `taxon_commercial_tier_vocabulary.approved_by` |
| `place_iconic_taxa_vocabulary` entry: proposed → active | Second human (not author) | `place_iconic_taxa_vocabulary.approved_by` |

### Article 34 — AI Advisory Boundaries

AI may:
- Produce pre-screen estimates for Class C signals.
- Suggest `collection_gap_type` on `collection_recommendations`.
- Pre-compute `score_inputs` for curator review.
- Flag Class D escalation conditions.

AI must not:
- Set `curator_decision` to any value other than `pending`.
- Set `image_quality_score` as a confirmed value (only as advisory estimate in `agent_notes`).
- Create `product_recommendations` or `collection_recommendations` directly.
- Transition any entity status that requires a human event.
- Write entries to `taxon_commercial_tier_vocabulary` or `place_iconic_taxa_vocabulary` directly.

---

## Part X — Prohibited Acts

The following acts are unconstitutional. Any system component that attempts them must be rejected,
and an error event must be written before the attempt is rolled back.

1. **Computing COS without writing a `score_audit_log` entry first.** The audit entry is a
   precondition, not a consequence.

2. **Advancing a `product_recommendation` or `collection_recommendation` to `status = 'assigned'`
   when `commerce_opportunities.curator_decision != 'approved'`.** Recommendations derive from
   approved opportunities only.

3. **Writing any UPDATE or DELETE statement on `score_audit_log`.** The no-update and no-delete
   rules are enforced at the database level.

4. **Modifying any immutable field on a `commerce_policy` record after it reaches `active`,
   `paused`, or `superseded`.**

5. **Using GBIF occurrence counts, species popularity, taxonomic frequency, or any biodiversity
   inventory metric as a scoring input.** This is a direct violation of the Illustration
   Opportunity Doctrine and a constitutional breach.

6. **Overriding Gate 3 (`blocked_legal`) at any level below source-level rights resolution.**
   Curator authority does not extend to legal holds.

7. **Activating a `commerce_policy` without a second human approver whose identity differs from
   the policy author.**

8. **Hardcoding formula weights, tier thresholds, or hard gate values in worker code.** All
   scoring parameters are sourced exclusively from `commerce_policy.formula_spec`.

9. **Deleting a `commerce_opportunities` record.** Opportunities are archived, not deleted.
   Archival sets `status = 'archived'` and writes a `score_archived` audit event. The record and
   its audit chain are retained permanently.

10. **Creating a `product_recommendation` or `collection_recommendation` without a
    `recommendation_basis` JSONB record that satisfies the minimum required fields defined in
    Article 25.**

11. **Implementing the scoring worker without implementing the replay worker simultaneously.**
    Scoring without replay produces an unverified audit chain. This is unconstitutional.

---

## Part XI — Constitutional Migration Order

### Article 35 — Prerequisites Before Migration `[Amended v1.1]`

The following conditions must be satisfied before any migration in this series proceeds:

1. `illustration_opportunities.status = 'approved'` records exist for at least one BHL
   opportunity with confirmed `asset_rights`.
2. The governed vocabulary tables for `taxon_commercial_tier_vocabulary`,
   `priority_illustrators_vocabulary`, `place_tier_vocabulary`, and
   `place_iconic_taxa_vocabulary` schemas are designed and ready to seed.
3. The `place_iconic_taxa_vocabulary` seeding plan for Yellowstone (minimum five entries) is
   drafted and ready for curator review.
4. The replay worker design is complete. It must be implemented at the same time as the scoring
   worker, not after.
5. **[B-3 — Resolved]** The `illustration_opportunities` source constraint amendment
   (`CHECK (source IN ('bhl', 'loc'))`) is confirmed as Migration 19a and is mandatory before
   Migration 22. Open Question 1 from v1.0.0 is resolved.

### Article 36 — Migration Sequence `[Amended v1.1]`

```
Migration 19a (MANDATORY — execute first):
  Amend illustration_opportunities source constraint.
  Remove: CHECK (source = 'bhl')
  Replace: CHECK (source IN ('bhl', 'loc'))
  Prerequisite: None beyond existing M-1–18 being applied.
  Note: Previously optional/deferred. Now mandatory per Director Decision B-3.
        Must precede Migration 22 (score_audit_log links to illustration_opportunities).

Migration 19b (was Migration 19):
  Create governed vocabulary tables:
    - taxon_commercial_tier_vocabulary
      (governed table with authored_by, approved_by, second-human constraint)
    - priority_illustrators_vocabulary
      (governed table with authored_by, approved_by, second-human constraint)
    - place_tier_vocabulary
      (from existing concepts graph — lightweight seed only)
    - place_iconic_taxa_vocabulary
      (governed table with place_id FK, authored_by, approved_by, second-human constraint)
  Seed initial rows for each table (status = 'proposed'; requires curator approval to activate).
  Note: These are governed tables, not JSONB in commerce_policy.
        Changes to individual entries do not require a policy version bump.

Migration 20:
  Create commerce_policy table with 6-state status vocabulary:
    CHECK (status IN ('draft','pending_approval','active','paused','superseded','retired'))
  Add max_score_age_days column (staleness threshold; default 90).
  Create constraint trigger: one status = 'active' at a time.
  Create immutability trigger: formula_spec and thresholds locked after active/paused/superseded.
  Seed initial commerce_policy v1.0.0 record (status = 'draft').

Migration 21:
  Create commerce_opportunities table.
  Columns: five model subscores (museum, retail, publishing, tourism, reference).
           NO collection_fit_score. NO commercial_value_score.
  Add csm_score and csm_tier columns (Pass 2 outputs).
  Add last_scored_at column (staleness worker).
  Create constraint trigger: hard_gate_status != 'passed' → eligibility flags = FALSE.
  Create constraint trigger: COS present → audit log entry required.

Migration 22:
  Create score_audit_log table with hybrid schema:
    - Governance fields: actor_type, actor_id, event_type, entry_checksum_sha256,
      previous_entry_checksum, previous_state, new_state
    - Runtime fields: reason, generated_by
    - All other runtime fields: score_inputs, score_outputs, trigger
  Add audit_event_type CHECK constraint (11 vocabulary values).
  Create PostgreSQL RULE: no UPDATE on score_audit_log.
  Create PostgreSQL RULE: no DELETE on score_audit_log.
  Note: Role-level privilege separation is DESCOPED for v0.5.0 (Decision B-4).
        No CREATE ROLE or REVOKE statements in this migration.
        Role separation is scheduled as a post-v0.5.0 migration.

Migration 23:
  Create product_recommendations table.
  Create collection_recommendations table.

Activation (governed event, not a migration):
  Step 1: Curator reviews and approves vocabulary table entries
          (taxon_commercial_tier_vocabulary, place_iconic_taxa_vocabulary — Yellowstone).
  Step 2: Principal Architect authors commerce_policy v1.0.0:
            authored_by = Principal Architect identity
            status → pending_approval
  Step 3: Second human approves: status → active
  Step 4: Scoring worker activated.
  Step 5: Replay worker activated simultaneously (constitutional requirement).
```

### Article 37 — Open Architectural Questions `[Amended v1.1]`

The following questions were open in v1.0.0. Resolved questions are removed from the open list.
Questions remaining open are carried forward.

**[RESOLVED — v1.1] Q1 — `illustration_opportunities` source constraint.**
Decision B-3 resolved this question. Migration 19a is mandatory and amends the constraint to
`CHECK (source IN ('bhl', 'loc'))` before Migration 22. LOC opportunities may be inserted into
`illustration_opportunities` after Migration 19a is applied.

**[RESOLVED — v1.1] Q3 — `place_iconic_taxa` governance process.**
Decision D-3/D-5 resolved this question. `place_iconic_taxa_vocabulary` is a governed table with
an independent lifecycle. Entries are proposed by curators, approved by a second human (not the
proposer), and governed by the second-human rule at the row level. The policy JSONB references
the table — it does not embed the list.

**[Remaining Open] Q2 — `anchor_type` on `illustration_opportunities`.**
The `anchor_type` vocabulary (`biological | geographic | cultural`) is referenced by the
`commerce_opportunities` signal schema but is not yet a field on `illustration_opportunities`.
LOC visual assets (posters, photographs, architectural drawings) require it for accurate Tourism
and Reference subscore computation. Before LOC opportunities enter scoring, `anchor_type` must be
added to `illustration_opportunities`. This is a pre-condition for LOC asset scoring via the
illustration opportunity pathway, not for LOC asset scoring via `subject_type = 'asset'`.

**[Remaining Open] Q5 — Worker authentication and role privilege separation.**
The RLS architecture (Decision B-4) is descoped for v0.5.0. A future migration must define:
(a) the scoring worker database role, (b) INSERT-only privilege on `score_audit_log`,
(c) Docker Compose connection string for the worker role. This must be resolved before v0.6.0
or before the platform handles more than 500 scored opportunities, whichever comes first.

**[Remaining Open] Q6 — Class C signal human review workflow.**
No API endpoint, admin workflow, or FastAPI route for Class C signal submission is defined. The
`null_signal_policy = "null_blocks_tier_12_advancement"` rule gates advancement without a review
workflow in place, but curators have no mechanism to submit `image_quality_score` or
`composition_fit` values. This must be resolved before the first tier_1 or tier_2 classification
is needed.

---

## Part XII — Staleness Detection

### Article 38 — Staleness Detection Mechanism `[New — v1.1]`

**D-2 Amendment:** The staleness detection mechanism for v0.5.0 is polling. The
`commerce_staleness_worker` operates on a configurable schedule and identifies stale records by
comparing `commerce_opportunities.last_scored_at` against the `max_score_age_days` parameter in
the active `commerce_policy`.

**Staleness detection algorithm:**

```
1. Load active commerce_policy. Read max_score_age_days (default: 90).
2. Query commerce_opportunities WHERE:
     last_scored_at < NOW() - INTERVAL '(max_score_age_days) days'
     AND status NOT IN ('blocked', 'archived')
3. For each stale record:
     a. Set policy_stale = TRUE.
     b. Write score_audit_log entry:
          event_type = 'score_computed'  (recompute triggered)
          trigger = 'policy_version_change'
          reason = 'staleness_detected: last_scored_at exceeded max_score_age_days'
          generated_by = 'commerce_staleness_worker:{version}'
          actor_type = 'system_worker'
          actor_id = 'commerce_staleness_worker:{version}'
     c. Enqueue recompute in workflow_items.
4. Stale records retain their existing tier and routing eligibility until recomputed.
```

**Governance parameters (in commerce_policy):**

| Parameter | Location | Default | Meaning |
|---|---|---|---|
| `max_score_age_days` | `commerce_policy.max_score_age_days` | 90 | Days before a scored opportunity is considered stale |
| `staleness_poll_interval_hours` | `formula_spec.staleness_config.poll_interval_hours` | 24 | How often the staleness worker runs |

**Future upgrade path:** The polling mechanism may be replaced by `pg_notify` + LISTEN/NOTIFY
triggers in a future migration. The trigger would fire on UPDATE to `illustration_opportunities`,
`assets`, or `asset_rights` and notify the staleness worker in near-real-time. The polling
mechanism is chosen for v0.5.0 because it requires no additional PostgreSQL configuration and
aligns with the Docker Compose infrastructure constraint.

---

## Ratification

This Constitution v1.1.0 supersedes v1.0.0 and is ratified as the governing design document for
the Commerce Intelligence layer of Nature & Culture v0.5.0.

All nine implementation blockers identified in the 2026-06-06 readiness audit are resolved in this
version. Implementation of Migrations 19a through 23 is authorized.

Implementation is authorized subject to:

1. The Principal Architect confirms this document is complete and correct.
2. Open Questions Q2, Q5, and Q6 in Article 37 do not block v0.5.0 Migrations 19a–23. They are
   tracked as future-work obligations.
3. The migration sequence in Article 36 is approved in the order specified. Migration 19a is
   mandatory and executes first.
4. The initial `commerce_policy v1.0.0` record is authored and approved by two humans before
   activation.
5. The scoring worker and replay worker are activated simultaneously (Article 38 / Prohibited
   Act 11).

The `commerce_intelligence_runtime_v1.md` document must be amended before Migration 21 DDL is
written to:
- Remove `collection_fit_score` and `commercial_value_score` columns
- Add `museum_score`, `retail_score`, `publishing_score`, `tourism_score`, `reference_score` as
  the five authoritative runtime columns (if not already present)
- Add `csm_score` and `csm_tier` columns
- Add `last_scored_at` column
- Update the composite scoring formula to the 5-subscore model specified in Article 13
- Add the hybrid `score_audit_log` fields (`reason`, `generated_by`, `actor_id`, `actor_type`,
  `event_type`, `entry_checksum_sha256`, `previous_entry_checksum`, `previous_state`, `new_state`)
- Update `commerce_policy` status CHECK constraint to 6-state vocabulary
- Add `max_score_age_days` column to `commerce_policy`
