# Product Routing Constitution v1.1

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Ratified — implementation authorized for Migrations 24–25. |
| Supersedes | `product_routing_constitution_v1.0.md` (v1.0.0) |
| Repository | opengracelabs/nc |
| Branch | v0.5.1-product-routing |
| Drafted | 2026-06-06 |
| Ratified | 2026-06-06 |
| Role | Principal Architect |

---

## Director Review — v1.0.0 → v1.1.0

Thirteen findings applied. No articles deleted. Affected articles annotated `[Amended v1.1]`.

| Decision | Finding | Resolution | Articles Affected |
|---|---|---|---|
| DR-1 | Article 10.5 ambiguous — "every product family in `product_routing_policy`" implies all vocabulary entries must be present, but reserved families (e.g., `fashion`) are intentionally absent | Clarified: 10.5 governs only entries present in `routing_rules`; reserved families may be absent | 10 |
| DR-2 | Article 8.1 flag gate incorrectly applied to `flag_mode: "derived"` — no flags to check | Amended: 8.1 applies only when `flag_mode IN ('any','all')`; derivation formula governs eligibility when `flag_mode = 'derived'` | 8 |
| DR-3 | Article 12.4 claims `chk_product_recommendations_review_identity` enforces self-approval prevention — constraint actually checks only `curator_reviewed_by IS NOT NULL`, not identity distinctness | Corrected: self-approval prevention at curator review is an application-layer control; no DB constraint enforces it in v1.0; false claim removed | 12 |
| DR-4 | Article 15 claims `product_recommendations.policy_version_id` is the routing replayability anchor — confirmed FK points to `commerce_policy(id)`, not `product_routing_policy` | Corrected: routing replayability anchor is `recommendation_basis.routing_policy_id`; `policy_version_id` FK records the scoring policy | 15, 17 |
| DR-5 | Article 16 step 3 refers to "scoring loop" — incorrect term in routing context | Fixed: "routing loop" | 16 |
| DR-6 | Article 17 `tier_gate` template hardcodes `true` for gate pass fields | Fixed: shown as `<bool>` | 17 |
| DR-7 | PA-12 prohibits all UPDATEs on `product_recommendations`, conflicting with Commerce Intelligence Constitution which explicitly permits curator status transitions | Corrected: PA-12 scoped to routing worker only; curator status transitions governed by CI Constitution remain permitted | 19 |
| DR-8 | `derivation` field schema undefined — Article 10.3 requires it for `flag_mode: "derived"` but structure is never specified | Added Article 10.6 defining the `derivation` object schema | 10 |
| DR-9 | Article 15 supersession mechanism unspecified — who transitions old policy to `superseded`? | Clarified: activation trigger must set previously active policy to `superseded` within the same transaction | 13, 15 |
| DR-10 | Paused policy behavior undefined — routing worker behavior when no active policy exists not specified | Added: worker exits cleanly with no-op when no active policy found | 16 |
| DR-11 | Weight sum tolerance unspecified — floating point arithmetic may produce sums not exactly equal to 1.0 | Added: weights must sum to 1.0 within ±0.001 | 11 |
| DR-12 | M-24 dependency description described M-23 as "for pattern reference" — actual dependency is runtime validation, not schema FK | Clarified: M-23 dependency is runtime; routing worker validates routing_rules keys against `product_family_vocabulary` at policy load time | 20 |
| DR-13 | home_decor `derivation` field missing from Article 21 seed spec | Added machine-readable `derivation` object for `home_decor` in seed spec | 21 |

---

## Preamble

This Constitution governs the routing of scored, curator-approved Illustration Opportunities into
product recommendation records. It answers one question:

> How does a commerce opportunity become a product recommendation?

The answer is: through a machine-readable routing policy, a governed routing worker, and a curator
approval step. No external provider is involved. No product is generated. No inventory is created.
The output of routing is a `product_recommendation` record — a governed intent, not a product.

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity Doctrine,
and the Commerce Intelligence Constitution v1.1. Any provision that conflicts with those documents
is void. This Constitution governs the `product_routing_policy` entity and the routing worker that
consumes it. It does not govern `illustration_opportunities`, `commerce_opportunities`, or
`product_recommendations` schema — those are governed by the Commerce Intelligence Constitution.
This Constitution governs the *process* by which `product_recommendations` records are created.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration commerce platform.

**1.2** The commercial object is an Illustration Opportunity. A product recommendation is a
governed routing decision: this opportunity should be considered for this product family.

**1.3** Product routing classifies scored opportunities into product families. It does not generate
products, create inventory, contact providers, or trigger fulfillment. Routing is governance.

**1.4** The scoring worker computes eligibility flags on `commerce_opportunities`. The routing
worker reads those flags and applies routing rules to determine which product families apply. These
are distinct responsibilities governed by distinct policies.

**1.5** The `commerce_policy` governs scoring. The `product_routing_policy` governs routing. They
are independently versioned and independently activated.

### Article 2 — Scope

This Constitution governs exactly two entities:

| Entity | Role |
|---|---|
| `product_routing_policy` | The machine-readable authority for routing decisions |
| `product_routing_policy_status_vocabulary` | Governed lifecycle states for the policy |

This Constitution specifies the *process* by which the routing worker creates records in
`product_recommendations`. It does not define the schema of `product_recommendations` — that is
fixed by the Commerce Intelligence Constitution.

### Article 3 — Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Commerce Intelligence Constitution v1.1
            └─ Product Routing Constitution v1.1  ← this document
                 └─ product_routing_policy (active record)
                      └─ product_routing_worker
```

No lower authority may override a higher authority. A routing policy provision that contradicts
the Commerce Intelligence Constitution is void.

---

## Part II — Vocabulary

### Article 4 — Product Routing Policy Status Vocabulary

The `product_routing_policy_status_vocabulary` table contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Policy is being authored. No routing permitted under this policy. |
| `pending_approval` | Policy is awaiting second-human approval. No routing permitted. |
| `active` | Policy is authoritative. Routing worker uses this policy. Only one `active` record may exist at any time. |
| `paused` | Routing is suspended. Active records already created under this policy remain valid. |
| `superseded` | Policy was replaced by a newer version. Records created under this policy remain valid. |
| `retired` | Policy is permanently withdrawn. No new records may reference this policy. |

Transitions: `draft → pending_approval → active ⇄ paused → superseded → retired`.

Only `active → paused` and `paused → active` are reversible. All other transitions are terminal.

### Article 5 — Product Family Routing Eligibility

Each product family in `product_family_vocabulary` maps to one or more `eligible_*` flag columns
on `commerce_opportunities`. These flags are computed by the scoring worker from
`commerce_policy.product_surface_requirements`. The routing worker reads them — it does not
recompute them.

| Product Family | Primary Eligible Flag(s) | Notes |
|---|---|---|
| `wall_art` | `eligible_wall_art_premium`, `eligible_wall_art_standard` | Either flag routes to this family; premium flag selects premium product_types |
| `museum_print` | `eligible_museum_print` | Requires curator review always |
| `calendar` | `eligible_calendar` | |
| `book` | `eligible_book_illustration` | |
| `puzzle` | `eligible_puzzle` | |
| `card` | `eligible_card` | |
| `educational` | `eligible_educational` | |
| `institutional_license` | `eligible_institutional_license` | Requires curator review always |
| `home_decor` | *(derived — see Article 5.1)* | No dedicated flag; derived from wall_art eligibility |
| `fashion` | *(reserved — not routed in v1.0)* | Routing deferred to a future policy version |

**5.1 Derived eligibility for `home_decor`**: An opportunity is eligible for `home_decor` if
`eligible_wall_art_standard = TRUE AND csm_tier IN ('MASTERWORK', 'FLAGSHIP', 'STANDARD') AND
commerce_tier IN ('tier_1', 'tier_2')`. No dedicated flag exists. The routing worker evaluates
this derivation from the `derivation` object in `routing_rules["home_decor"]` (see Article 10.6).
This derivation must be recorded in `recommendation_basis.derivation_note`.

**5.2 Reserved families**: Any product family in `product_family_vocabulary` with no routing rule
in the active routing policy must not receive routing decisions. Routing to an unmapped family is a
constitutional violation (PA-11). Reserved families (e.g., `fashion`) are intentionally absent
from `routing_rules` and are not violations.

### Article 6 — Commerce Tier Ordering

For routing threshold evaluation, commerce tiers are ordered:

```
tier_1 > tier_2 > tier_3 > blocked
```

An opportunity satisfies `min_commerce_tier: "tier_2"` if its `commerce_tier` is `tier_1` or
`tier_2`. `blocked` never satisfies any routing threshold.

CSM tiers are ordered:

```
MASTERWORK > FLAGSHIP > STANDARD > REFERENCE > BLOCKED
```

An opportunity satisfies `min_csm_tier: "STANDARD"` if its `csm_tier` is `MASTERWORK`,
`FLAGSHIP`, or `STANDARD`. `BLOCKED` never satisfies any routing threshold.

---

## Part III — Routing Eligibility Gates

### Article 7 — Pre-Routing Gates

Before any family-level routing evaluation, an opportunity must clear four opportunity-level
pre-routing gates (PRG-0 through PRG-3). A gate failure at this level prevents routing entirely —
no `product_recommendation` records are created for that opportunity.

PRG-4 is a family-level idempotency gate evaluated independently per product family after
PRG-0 through PRG-3 pass.

| Gate | Level | Condition | Failure Behavior |
|---|---|---|---|
| **PRG-0** | Opportunity | `commerce_opportunities.curator_decision = 'approved'` | Skip opportunity — not eligible |
| **PRG-1** | Opportunity | `commerce_opportunities.hard_gate_status = 'passed'` | Skip opportunity — constitutionally blocked |
| **PRG-2** | Opportunity | `commerce_opportunities.policy_stale = FALSE` | Skip opportunity — re-score required before routing |
| **PRG-3** | Opportunity | `commerce_opportunities.commerce_tier NOT IN ('blocked')` | Skip opportunity — blocked by scoring |
| **PRG-4** | Family | No existing `product_recommendation` for this `(opportunity_id, recommended_product_family)` with `status NOT IN ('curator_rejected', 'retired')` | Skip that family only — do not create duplicate active routing decisions |

An opportunity that passes PRG-0 through PRG-3 but already has an active recommendation for
`wall_art` may still receive a new recommendation for `museum_print`.

These gates are applied only at the moment the routing worker claims an opportunity for
processing. They are not re-evaluated at curator review time.

### Article 8 — Family-Level Routing Gate `[Amended v1.1]`

After the pre-routing gates pass, the routing worker evaluates each product family independently.
A family is included in the routing output if and only if all of the following hold:

**8.1 Flag gate**: Evaluated according to `routing_rules[family].flag_mode`:

- When `flag_mode = "any"`: at least one column named in `routing_rules[family].eligible_flags`
  must be `TRUE` on `commerce_opportunities`.
- When `flag_mode = "all"`: every column named in `routing_rules[family].eligible_flags` must be
  `TRUE` on `commerce_opportunities`.
- When `flag_mode = "derived"`: the `routing_rules[family].derivation` object is evaluated
  instead (see Article 10.6). The `eligible_flags` array is ignored.

**8.2 Commerce tier gate**: `commerce_opportunities.commerce_tier` satisfies
`routing_rules[family].min_commerce_tier` per the ordering in Article 6.

**8.3 CSM tier gate**: `commerce_opportunities.csm_tier` satisfies
`routing_rules[family].min_csm_tier` per the ordering in Article 6.

**8.4 Score gates** (both must pass):
- `commerce_opportunities.commerce_opportunity_score >= routing_rules[family].min_commerce_score`
- `commerce_opportunities.csm_score >= routing_rules[family].min_csm_score`

A family that fails any gate is silently excluded for that opportunity. No error record is written.
The exclusion is implicit in the absence of a `product_recommendation` record for that family.

---

## Part IV — Policy Schema

### Article 9 — `product_routing_policy` Schema

The `product_routing_policy` table is the machine-readable authority for all routing decisions.

```
product_routing_policy
├── id                    UUID PRIMARY KEY
├── version               TEXT NOT NULL UNIQUE         -- e.g. "1.0.0"
├── status                TEXT NOT NULL FK → product_routing_policy_status_vocabulary
├── effective_from        TIMESTAMPTZ                  -- NULL until activation
├── effective_until       TIMESTAMPTZ                  -- NULL unless superseded
├── authored_by           TEXT NOT NULL
├── approved_by           TEXT                         -- NULL until approval
├── approved_at           TIMESTAMPTZ                  -- NULL until approval
├── changelog             TEXT NOT NULL
├── previous_version_id   UUID FK → product_routing_policy(id)
│
├── routing_rules         JSONB NOT NULL               -- Article 10
├── confidence_spec       JSONB NOT NULL               -- Article 11
│
├── provenance            JSONB NOT NULL DEFAULT '{}'
├── created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Constraints:**
- `approved_by IS DISTINCT FROM authored_by` (second-human approval)
- `status NOT IN ('active','paused','superseded') OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active'` — only one active policy at any time
- `routing_rules` and `confidence_spec` are immutable once `status IN ('active','paused','superseded')`

### Article 10 — `routing_rules` Canonical Structure `[Amended v1.1]`

`routing_rules` is a JSONB object keyed by product family value from `product_family_vocabulary`.
Each family entry is an object with the following required fields:

```json
{
  "<family_value>": {
    "eligible_flags":          [string],    // column names from commerce_opportunities; ignored when flag_mode = "derived"
    "flag_mode":               string,      // "any" | "all" | "derived"
    "min_commerce_tier":       string,      // "tier_1" | "tier_2" | "tier_3"
    "min_csm_tier":            string,      // "MASTERWORK" | "FLAGSHIP" | "STANDARD" | "REFERENCE"
    "min_commerce_score":      number,      // float [0, 1]
    "min_csm_score":           number,      // float [0, 1]
    "curator_always_required": boolean,
    "product_types":           [string]     // governed product type labels for this family
  }
}
```

**10.1** `flag_mode: "any"` — at least one flag in `eligible_flags` must be TRUE.

**10.2** `flag_mode: "all"` — all flags in `eligible_flags` must be TRUE.

**10.3** `flag_mode: "derived"` — eligibility is computed from the `derivation` object (Article
10.6). The `derivation` field must be present when `flag_mode` is `"derived"`. The `eligible_flags`
array is ignored.

**10.4** `product_types` must contain at least one entry. It is the machine-readable list of
specific product types within this family. These are written into
`product_recommendations.recommended_product_types` as JSONB.

**10.5** Every entry present in `routing_rules` must be a valid product family value from
`product_family_vocabulary`. Reserved families (e.g., `fashion`) are intentionally absent from
`routing_rules` and are not violations. The routing worker must validate all `eligible_flags`
column names exist on `commerce_opportunities` at policy load time.

**10.6 `derivation` Object Schema**: When `flag_mode = "derived"`, the routing rule must include
a `derivation` object with the following structure:

```json
"derivation": {
  "logic": "all",           // "all" | "any" — how conditions are combined
  "conditions": [
    {
      "column":   "<column_name>",   // column on commerce_opportunities
      "operator": "<op>",            // "eq" | "in" | "gte" | "lte" | "gt" | "lt"
      "value":    <value>            // scalar or array (for "in")
    }
  ]
}
```

`logic: "all"` requires every condition to be TRUE. `logic: "any"` requires at least one
condition to be TRUE. The routing worker evaluates conditions against the opportunity row at
routing time.

### Article 11 — `confidence_spec` Canonical Structure `[Amended v1.1]`

`confidence_spec` is a JSONB object keyed by product family value. Each family entry defines the
weighted formula used to compute `recommendation_confidence`:

```json
{
  "<family_value>": {
    "signals": {
      "<column_name>": <weight>,    // float; all weights must sum to 1.0 within ±0.001
      ...
    }
  }
}
```

**11.1** All signal names must be columns that exist on `commerce_opportunities`.

**11.2** All weights within a family's `signals` object must sum to 1.0 within ±0.001. This is
enforced by the routing worker at policy load time, not by a DB constraint. A policy that fails
weight validation must not activate — the routing worker must raise an error and halt.

**11.3** The computed confidence is:

```
recommendation_confidence = sum(weight_i * signal_i)
```

where each `signal_i` is read from `commerce_opportunities` as a float. `NULL` signal values are
treated as `0.0` for confidence computation.

**11.4** `confidence_spec` must contain an entry for every family present in `routing_rules`.

### Article 12 — Curator Review Rules `[Amended v1.1]`

**12.1** A routing decision requires curator review if any of the following hold:
- `routing_rules[family].curator_always_required = true`
- `commerce_opportunities.requires_curator_review = TRUE`
- `commerce_opportunities.csm_tier = 'MASTERWORK'`

**12.2** When curator review is required, the routing worker writes
`product_recommendations.status = 'pending_curator_review'`. The `curator_reviewed_by` and
`curator_reviewed_at` columns are left NULL.

**12.3** When curator review is not required, the routing worker may write
`product_recommendations.status = 'assigned'` directly. Gate 5 (enforced by DB trigger in M-23)
still applies — `commerce_opportunities.curator_decision = 'approved'` is re-checked at INSERT.

**12.4** Prevention of curator self-approval is an application-layer control in v1.0. No DB
constraint enforces identity distinctness between the routing decision creator and the curator
reviewer on `product_recommendations`. Implementations must enforce this in the curator workflow
layer. A future version of this constitution may add a `routed_by` column and a corresponding
DB constraint.

---

## Part V — Policy Lifecycle

### Article 13 — Activation Protocol `[Amended v1.1]`

A `product_routing_policy` may only become `active` if all five conditions hold:

1. `status = 'pending_approval'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM authored_by`
4. `effective_from IS NOT NULL`
5. No other `product_routing_policy` has `status = 'active'`

These five conditions must be enforced by a BEFORE UPDATE trigger on `product_routing_policy`.

When a new policy transitions to `active`, the activation trigger must — within the same
transaction — set the previously active policy's `status` to `'superseded'` and its
`effective_until` to `NOW()`. The UNIQUE partial index on `status = 'active'` enforces that no
two active policies coexist; the trigger enforces the correct supersession cascade.

### Article 14 — Immutability

Once `status IN ('active', 'paused', 'superseded')`, the following columns are immutable:

- `version`
- `authored_by`
- `routing_rules`
- `confidence_spec`

Attempts to mutate these columns after the policy enters any of these states must raise an
exception. This is enforced by a BEFORE UPDATE trigger on `product_routing_policy`.

The following columns may be updated after activation (for lifecycle management only):

- `status` (lifecycle transitions only)
- `effective_until` (set when superseded)
- `provenance`, `updated_at`

`approved_by` and `approved_at` are set once during the `pending_approval → active` transition
and are thereafter immutable.

### Article 15 — Version Supersession `[Amended v1.1]`

When a new `product_routing_policy` version is activated:

1. The previously active policy's `status` is set to `superseded` by the activation trigger
2. The previously active policy's `effective_until` is set to `NOW()` by the activation trigger
3. The new policy's `previous_version_id` references the superseded policy

Existing `product_recommendations` records created under the superseded policy remain valid. The
routing worker will use the new active policy for all new routing decisions.

**Replayability anchor**: `product_recommendations.policy_version_id` is a FK to
`commerce_policy(id)` — it records the scoring policy that was active when the opportunity was
scored. It is not the routing replayability anchor. The routing replayability anchor is
`recommendation_basis.routing_policy_id`, which records the `product_routing_policy.id` that
governed the routing decision. Both anchors are required to replay a routing decision.

---

## Part VI — Routing Worker Protocol

### Article 16 — Routing Worker Responsibilities `[Amended v1.1]`

The `product_routing_worker` is the sole process authorized to create `product_recommendation`
records. Its protocol is:

1. **Load policy**: Query for `product_routing_policy WHERE status = 'active'`. If no active
   policy exists (policy is paused, all policies are superseded, or no policy has been seeded),
   the worker exits cleanly with no records written. No error is raised. No routing occurs.

2. **Validate policy**: Validate `confidence_spec` weights sum to 1.0 (within ±0.001) per family.
   Validate all `eligible_flags` column names exist on `commerce_opportunities`. Validate all
   `routing_rules` keys are valid values in `product_family_vocabulary`. Fail fast — if any
   validation fails, halt immediately and process no opportunities.

3. **Claim opportunities**: Query `commerce_opportunities` for records satisfying PRG-0 through
   PRG-3. Apply PRG-4 per family within the routing loop.

4. **Evaluate families**: For each opportunity, evaluate all product families from `routing_rules`
   against the family-level gates (Article 8). For each family that passes all gates:
   a. Compute `recommendation_confidence` from `confidence_spec`
   b. Build `recommendation_basis` (Article 17)
   c. Determine curator review requirement (Article 12)
   d. Write one `product_recommendation` INSERT

5. **Transaction scope**: Each `product_recommendation` INSERT is wrapped in its own transaction.
   A failure on one family does not block other families for the same opportunity.

6. **No re-scoring**: The routing worker reads scores from `commerce_opportunities`. It does not
   call the scoring worker, recompute COS, recompute CSM, or re-evaluate hard gates. Scoring
   output is fixed at routing time.

7. **No provider calls**: The routing worker makes no HTTP calls, webhook calls, or queue
   publications to external systems. Routing is a DB-only operation.

### Article 17 — `recommendation_basis` Canonical Structure `[Amended v1.1]`

Every `product_recommendation` record must have a non-empty `recommendation_basis`. The routing
worker must construct it according to this canonical structure:

```json
{
  "routing_policy_id":         "<UUID>",
  "routing_policy_version":    "<semver>",
  "routed_at":                 "<ISO 8601 UTC>",
  "eligible_flags_evaluated":  ["<flag_name>", ...],
  "flags_satisfied":           ["<flag_name>", ...],
  "flag_mode":                 "<any|all|derived>",
  "derivation_note":           "<string or null>",
  "tier_gate": {
    "commerce_tier":           "<value>",
    "min_commerce_tier":       "<value>",
    "commerce_tier_passed":    <bool>,
    "csm_tier":                "<value>",
    "min_csm_tier":            "<value>",
    "csm_tier_passed":         <bool>,
    "commerce_score":          <float>,
    "min_commerce_score":      <float>,
    "commerce_score_passed":   <bool>,
    "csm_score":               <float>,
    "min_csm_score":           <float>,
    "csm_score_passed":        <bool>
  },
  "confidence_inputs":         { "<signal>": <float>, ... },
  "confidence_weights":        { "<signal>": <float>, ... },
  "confidence_computed":       <float>
}
```

`derivation_note` must be a non-null string describing the derivation logic when
`flag_mode = "derived"`. It must be `null` for `"any"` and `"all"` modes.

All `tier_gate` boolean fields will be `true` in a written record — a family with any `false`
gate is silently excluded and produces no record. The booleans are included for human readability
and future diagnostic tooling.

### Article 18 — Idempotency

The routing worker must be safe to run multiple times against the same set of opportunities.

**18.1** PRG-4 ensures no duplicate active recommendations are created.

**18.2** If a `product_recommendation` with `status IN ('curator_rejected', 'retired')` exists for
a given `(opportunity_id, recommended_product_family)`, a new recommendation may be created. The
old record is not deleted.

**18.3** A routing policy update that changes routing rules may cause new families to become
eligible for previously-routed opportunities. The routing worker will create new recommendations
for newly eligible families, subject to PRG-4.

---

## Part VII — Prohibited Acts

### Article 19 — Prohibited Acts `[Amended v1.1]`

The following acts are unconstitutional. Any implementation that performs any of these acts is
immediately non-compliant.

| Act | Prohibition |
|---|---|
| **PA-1** | No routing without loading an active `product_routing_policy` first |
| **PA-2** | No hardcoded routing thresholds — all thresholds must live in `routing_rules` |
| **PA-3** | No hardcoded confidence weights — all weights must live in `confidence_spec` |
| **PA-4** | No routing without clearing all pre-routing gates (PRG-0 through PRG-4) |
| **PA-5** | No `recommendation_basis = '{}'` — basis must be populated on every record |
| **PA-6** | No external provider calls during routing |
| **PA-7** | No re-scoring of opportunities during routing — scoring output is fixed at routing time |
| **PA-8** | No routing policy activation without second-human approval |
| **PA-9** | No mutation of `routing_rules` or `confidence_spec` after policy activation |
| **PA-10** | No self-approval of routing policy |
| **PA-11** | No routing to a product family absent from the active `routing_rules` |
| **PA-12** | The routing worker must not UPDATE or DELETE `product_recommendation` records. Status transitions (`pending_curator_review → curator_approved`, `assigned`, etc.) are curator operations governed by the Commerce Intelligence Constitution and remain permitted through that authority. |

---

## Part VIII — Migration Sequence

### Article 20 — Required Migrations `[Amended v1.1]`

| Migration | Contents | Depends On |
|---|---|---|
| M-24 | `product_routing_policy_status_vocabulary` table + seed values; `product_routing_policy` table; immutability trigger; activation trigger (including supersession cascade); UNIQUE partial index on `status = 'active'` | M-23 (runtime dependency — routing worker validates `routing_rules` keys against `product_family_vocabulary` at policy load time; no schema FK required) |
| M-25 | Seed `product_routing_policy` v1.0.0 in `draft` status with machine-readable `routing_rules` and `confidence_spec` for all nine routed product families (`fashion` reserved and absent) | M-24 |

**M-24 dependency note**: `product_routing_policy` has no FK to `product_family_vocabulary`.
The M-23 dependency is runtime, not schema-level: the routing worker validates all `routing_rules`
keys against `product_family_vocabulary` at policy load time. M-23 must be applied before M-24
runs in production to ensure the vocabulary is populated before any routing policy is loaded.

### Article 21 — Seed Policy Specification `[Amended v1.1]`

The M-25 seed must populate `routing_rules` and `confidence_spec` for the following families.
Threshold values below are constitutional mandates for v1.0.0. A director decision is required
to change any threshold — that decision produces a new policy version, not a migration change.

**Routing Rules — v1.0.0 Seed:**

| Family | Eligible Flags | Flag Mode | Min Commerce Tier | Min CSM Tier | Min Commerce Score | Min CSM Score | Curator Always |
|---|---|---|---|---|---|---|---|
| `wall_art` | `eligible_wall_art_premium`, `eligible_wall_art_standard` | `any` | `tier_2` | `STANDARD` | 0.65 | 0.60 | false |
| `museum_print` | `eligible_museum_print` | `any` | `tier_1` | `MASTERWORK` | 0.80 | 0.90 | **true** |
| `calendar` | `eligible_calendar` | `any` | `tier_2` | `STANDARD` | 0.65 | 0.60 | false |
| `book` | `eligible_book_illustration` | `any` | `tier_2` | `STANDARD` | 0.65 | 0.60 | false |
| `puzzle` | `eligible_puzzle` | `any` | `tier_3` | `STANDARD` | 0.50 | 0.60 | false |
| `card` | `eligible_card` | `any` | `tier_3` | `STANDARD` | 0.50 | 0.60 | false |
| `educational` | `eligible_educational` | `any` | `tier_3` | `REFERENCE` | 0.50 | 0.40 | false |
| `institutional_license` | `eligible_institutional_license` | `any` | `tier_1` | `FLAGSHIP` | 0.80 | 0.75 | **true** |
| `home_decor` | *(none — derived)* | `derived` | `tier_2` | `STANDARD` | 0.65 | 0.60 | false |

**`home_decor` derivation object (required for `flag_mode: "derived"`):**

```json
"derivation": {
  "logic": "all",
  "conditions": [
    { "column": "eligible_wall_art_standard", "operator": "eq",  "value": true },
    { "column": "csm_tier",                   "operator": "in",  "value": ["MASTERWORK", "FLAGSHIP", "STANDARD"] },
    { "column": "commerce_tier",              "operator": "in",  "value": ["tier_1", "tier_2"] }
  ]
}
```

**product_types per family (v1.0.0 seed):**

| Family | product_types |
|---|---|
| `wall_art` | `["print_premium", "print_standard", "canvas", "framed", "poster"]` |
| `museum_print` | `["museum_giclée", "archival_print"]` |
| `calendar` | `["wall_calendar", "desk_calendar"]` |
| `book` | `["book_interior", "cover_art"]` |
| `puzzle` | `["puzzle_500", "puzzle_1000"]` |
| `card` | `["greeting_card", "notecard_set"]` |
| `educational` | `["classroom_poster", "reference_sheet"]` |
| `institutional_license` | `["digital_license", "print_license"]` |
| `home_decor` | `["decorative_print", "tile_art"]` |

**Confidence Spec — v1.0.0 Seed:**

Standard families (`wall_art`, `calendar`, `book`, `puzzle`, `card`, `educational`,
`home_decor`) use this formula:

| Signal | Weight |
|---|---|
| `commerce_opportunity_score` | 0.40 |
| `csm_score` | 0.35 |
| `illustrator_prestige` | 0.15 |
| `place_relevance_score` | 0.10 |

Premium families (`museum_print`, `institutional_license`) use this formula:

| Signal | Weight |
|---|---|
| `csm_score` | 0.45 |
| `commerce_opportunity_score` | 0.30 |
| `illustrator_prestige` | 0.15 |
| `place_relevance_score` | 0.10 |

All weight sets sum to 1.00.

---

## Part IX — Ratification

This Constitution is ratified. Migrations M-24 and M-25 are authorized for implementation.

Implementation of the `product_routing_worker` is authorized after M-24 and M-25 are applied
and the v1.0.0 seed policy transitions to `active` through the constitutional activation protocol
(second-human approval required).
