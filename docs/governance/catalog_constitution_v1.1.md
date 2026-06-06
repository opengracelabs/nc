# Catalog Constitution v1.1

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Ratified — implementation authorized for Migrations 26–28. |
| Supersedes | `catalog_constitution_v1.0.md` (v1.0.0) |
| Repository | opengracelabs/nc |
| Branch | v0.5.1-product-routing |
| Drafted | 2026-06-06 |
| Ratified | 2026-06-06 |
| Role | Principal Architect |

---

## Director Review — v1.0.0 → v1.1.0

Nine blocking findings applied. No articles deleted. Affected articles annotated `[Amended v1.1]`.

| Finding | Description | Resolution | Articles Affected |
|---|---|---|---|
| BF-1 | `nominated → approved` direct transition absent from Article 5 but required by Article 22.1 auto-advance | Added `nominated → approved` as a valid direct transition; constrained to `actor_type = 'system_worker'` only | 5, 22 |
| BF-2 | VG-2 loads active `product_routing_policy` at runtime — ungoverned cross-policy dependency | Removed VG-2 from runtime gates; validation of `variant_spec` product_types moved to catalog_policy activation trigger | 10, 13, 21 |
| BF-3 | `replay_verified` and `replay_failure` absent from `catalog_audit_event_type_vocabulary` | Added both event types to Article 8 vocabulary | 8 |
| BF-4 | Article 20 `replay_nomination()` policy load method unspecified | Made explicit: replay always loads policy by exact `catalog_candidate.catalog_policy_id` | 20 |
| BF-5 | `opportunity_snapshot` immutability declared but no DB enforcement mechanism specified | Added BEFORE UPDATE trigger spec on `catalog_candidate` that prevents mutation of `opportunity_snapshot` | 15, 19 |
| BF-6 | `chk_catalog_pricing_floor_ceiling` uses strict `<`; rejects `book_interior` seed where floor=ceiling=$0 | Changed constraint to `<=`; added note that floor=ceiling is a price-lock | 17, 25 |
| BF-7 | PA-12 lacks enforcement mechanism — no trigger specified on `catalog_variant.status` | Added BEFORE UPDATE trigger spec on `catalog_variant.status` checking approved pricing before `active` transition | 16, 23 |
| BF-8 | Colon separator in `variant_key`; dimension values not prohibited from containing `:` | Added constraint: dimension values must not contain `:`; catalog worker validates at policy load time | 13, 23 |
| BF-9 | Catalog worker transaction scope unspecified; candidate INSERT and audit INSERT could split across transactions | Added Article 26 (Catalog Worker Protocol) specifying nomination as a single atomic transaction | 26 (new) |

---

## Preamble

This Constitution governs the catalog layer of Nature & Culture. It answers two questions:

> How does a product recommendation become a catalog candidate?
> How does a catalog candidate become a governed product with variants and pricing?

The catalog is not a storefront. It is the governed intent layer between routing decisions and
eventual commerce. Its output is a set of governed records — `catalog_candidate`,
`catalog_variant`, `catalog_pricing_profile` — that describe what should exist in commerce, how
it should be configured, and at what governed price. No product is generated. No inventory is
created. No provider is contacted. The catalog is governance.

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity
Doctrine, the Commerce Intelligence Constitution v1.1, and the Product Routing Constitution v1.1.
Any provision that conflicts with those documents is void. This Constitution governs five entities
and the worker and audit log that support them.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration commerce platform.

**1.2** The catalog records governed intent. A `catalog_candidate` is the decision to bring an
Illustration Opportunity into the product catalog. A `catalog_variant` is a specific product
configuration. A `catalog_pricing_profile` is the pricing governance for that configuration. None
of these is a product. None triggers fulfillment.

**1.3** The routing worker routes scored opportunities into product recommendations. The catalog
worker nominates assigned recommendations into catalog candidates and generates their variants and
pricing profiles. These are distinct responsibilities governed by distinct policies.

**1.4** `catalog_policy` governs the catalog worker. It is independently versioned and
independently activated from `commerce_policy` and `product_routing_policy`.

**1.5** `catalog_pricing_profile` is pricing governance, not a price list. It captures a governed
target price derived from policy-defined markup formulas. Provider integration is not in scope for
v1.0. The computed price is the constitutional answer to: "what should this variant cost?"

### Article 2 — Scope

This Constitution governs exactly five entities:

| Entity | Role |
|---|---|
| `catalog_policy` | Machine-readable authority for all catalog decisions |
| `catalog_candidate` | A nominated Illustration Opportunity ready for catalog entry |
| `catalog_variant` | A specific product configuration within a catalog candidate |
| `catalog_pricing_profile` | Pricing governance for a specific catalog variant |
| `catalog_audit_log` | Append-only, hash-chained event record for all catalog state transitions |

This Constitution also specifies the process by which the catalog worker creates these records and
the curator approval rules that govern their lifecycle. It does not govern upstream entities.

### Article 3 — Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Commerce Intelligence Constitution v1.1
            └─ Product Routing Constitution v1.1
                 └─ Catalog Constitution v1.1  ← this document
                      └─ catalog_policy (active record)
                           └─ catalog_worker
```

No lower authority may override a higher authority. A catalog policy provision that contradicts
any higher authority is void.

---

## Part II — Vocabulary

### Article 4 — Catalog Policy Status Vocabulary

`catalog_policy_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Policy is being authored. No catalog work permitted under this policy. |
| `pending_approval` | Awaiting second-human approval. No catalog work permitted. |
| `active` | Authoritative. Catalog worker uses this policy. Only one `active` record at any time. |
| `paused` | Catalog work is suspended. Existing records remain valid. |
| `superseded` | Replaced by a newer version. Existing records remain valid. |
| `retired` | Permanently withdrawn. No new records may reference this policy. |

Transitions: `draft → pending_approval → active ⇄ paused → superseded → retired`.
Only `active ⇄ paused` is reversible.

### Article 5 — Catalog Candidate Status Vocabulary `[Amended v1.1]`

`catalog_candidate_status_vocabulary` contains exactly these values:

| Value | Transition Rule |
|---|---|
| `nominated` | Initial state. Set by catalog worker at nomination time. |
| `under_review` | Curator has claimed the candidate for review. |
| `approved` | Candidate approved. Variants and pricing profiles may now be finalized. |
| `rejected` | Curator rejected. No catalog entry. Terminal state. |
| `published` | All required variants are `active` and all required pricing profiles are `approved`. Candidate is live in the governed catalog. |
| `retired` | Candidate removed from active catalog. Variants and pricing profiles are retired. |
| `withdrawn` | Withdrawn by curator before review is complete. Terminal state. |

Valid transitions:

```
nominated → under_review → approved → published → retired
                        → rejected
nominated → approved  [system_worker only — auto-advance when curator review not required]
nominated → withdrawn
under_review → withdrawn
approved → withdrawn (before publication)
```

The `nominated → approved` direct transition is reserved for `actor_type = 'system_worker'`. A
curator may not use this path; curator approvals must proceed through `under_review`. This
constraint is enforced by a BEFORE UPDATE trigger on `catalog_candidate` that, when
`OLD.status = 'nominated' AND NEW.status = 'approved'`, requires the transition to have been
initiated by the catalog worker (application-layer enforcement; `nominated_by` and
`curator_reviewed_by` provide the audit trail).

### Article 6 — Catalog Variant Status Vocabulary

`catalog_variant_status_vocabulary` contains exactly these values:

| Value | Transition Rule |
|---|---|
| `proposed` | Initial state. Generated by catalog worker from `variant_spec`. |
| `approved` | Variant approved. Required before `active` for families in `families_requiring_variant_approval`; set by system_worker for all other families. |
| `active` | Variant is live. A `catalog_pricing_profile` with `status = 'approved'` must exist. Enforced by BEFORE UPDATE trigger (Article 16). |
| `retired` | Variant removed from catalog. Terminal state. |
| `rejected` | Variant rejected by curator. Terminal state. |

Valid transitions:

```
proposed → approved → active → retired
         → rejected
```

For families not requiring variant-level curator approval, the catalog worker transitions variants
from `proposed → approved` immediately, with `actor_type = 'system_worker'`. All variants must
pass through `approved` before becoming `active` — there is no `proposed → active` direct path.

### Article 7 — Catalog Pricing Profile Status Vocabulary

`catalog_pricing_profile_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Generated by catalog worker. Awaiting curator approval if required; auto-approved otherwise. |
| `approved` | Pricing approved. Required before a variant may transition to `active`. |
| `superseded` | Replaced by a revised pricing profile for the same variant. |
| `retired` | Pricing profile retired. Terminal state. |

### Article 8 — Catalog Audit Event Type Vocabulary `[Amended v1.1]`

`catalog_audit_event_type_vocabulary` contains exactly these values:

| Value | Level | Meaning |
|---|---|---|
| `candidate_nominated` | Candidate | Catalog worker created a candidate |
| `candidate_under_review` | Candidate | Curator claimed for review |
| `candidate_approved` | Candidate | Curator or system_worker approved |
| `candidate_rejected` | Candidate | Curator rejected |
| `candidate_published` | Candidate | All active variants and approved pricing — candidate is live |
| `candidate_retired` | Candidate | Candidate retired from catalog |
| `candidate_withdrawn` | Candidate | Candidate withdrawn before review complete |
| `variant_proposed` | Variant | Catalog worker proposed a variant from variant_spec |
| `variant_approved` | Variant | Variant approved |
| `variant_active` | Variant | Variant is live |
| `variant_retired` | Variant | Variant retired |
| `variant_rejected` | Variant | Variant rejected by curator |
| `pricing_applied` | Pricing | Catalog worker generated a pricing profile from pricing_spec |
| `pricing_approved` | Pricing | Pricing profile approved |
| `pricing_superseded` | Pricing | Pricing profile superseded |
| `pricing_retired` | Pricing | Pricing profile retired |
| `policy_validated` | Policy | Catalog worker validated policy at load time; used to log skipped variants |
| `replay_verified` | Replay | Replay of nomination produced identical variants and pricing |
| `replay_failure` | Replay | Replay of nomination produced divergent output — integrity suspect |

---

## Part III — Nomination Gates

### Article 9 — Pre-Nomination Gates

Before creating a `catalog_candidate`, the catalog worker must evaluate five nomination gates.
Gates NG-0 through NG-3 are opportunity-level: failure skips the entire nomination for that
recommendation. Gate NG-4 is an idempotency gate evaluated per `(opportunity_id, product_family)`.

| Gate | Level | Condition | Failure Behavior |
|---|---|---|---|
| **NG-0** | Opportunity | `product_recommendations.status = 'assigned'` | Skip nomination |
| **NG-1** | Opportunity | `product_recommendations.recommendation_confidence >= catalog_policy.entry_spec.min_confidence` | Skip nomination |
| **NG-2** | Opportunity | `commerce_opportunities.curator_decision = 'approved'` | Skip nomination |
| **NG-3** | Opportunity | `commerce_opportunities.hard_gate_status = 'passed'` | Skip nomination |
| **NG-4** | Family | No existing `catalog_candidate` for `(opportunity_id, product_family)` with `status NOT IN ('rejected', 'retired', 'withdrawn')` | Skip that family only |

NG-4 allows re-nomination after rejection or withdrawal.

### Article 10 — Variant and Pricing Gates `[Amended v1.1]`

After a `catalog_candidate` is created, the catalog worker proposes variants from
`catalog_policy.variant_spec`. Before proposing a variant, the worker must verify:

| Gate | Condition | Failure Behavior |
|---|---|---|
| **VG-0** | `catalog_candidate.status = 'nominated'` | Do not propose variants |
| **VG-1** | No existing `catalog_variant` for `(catalog_candidate_id, variant_key)` | Skip variant — idempotency |

VG-2 (cross-policy routing policy check) is removed. Validation that `variant_spec` product_types
are authorized by the governing routing policy occurs at `catalog_policy` activation time, not at
worker runtime (see Article 21).

Before creating a `catalog_pricing_profile`, the worker must verify:

| Gate | Condition | Failure Behavior |
|---|---|---|
| **PG-0** | `catalog_variant.status = 'proposed'` | Do not apply pricing |
| **PG-1** | No existing `catalog_pricing_profile` with `status NOT IN ('superseded','retired')` for this `catalog_variant_id` | Skip — idempotency |
| **PG-2** | `pricing_spec[family][product_type]` exists in the active catalog_policy | Log `policy_validated` event noting the gap; skip variant entirely |

---

## Part IV — Policy Schema

### Article 11 — `catalog_policy` Schema

```
catalog_policy
├── id                      UUID PRIMARY KEY
├── version                 TEXT NOT NULL UNIQUE           -- e.g. "1.0.0"
├── status                  TEXT NOT NULL FK → catalog_policy_status_vocabulary
├── effective_from          TIMESTAMPTZ                    -- NULL until activation
├── effective_until         TIMESTAMPTZ                    -- NULL unless superseded
├── authored_by             TEXT NOT NULL
├── approved_by             TEXT                           -- NULL until approval
├── approved_at             TIMESTAMPTZ                    -- NULL until approval
├── changelog               TEXT NOT NULL
├── previous_version_id     UUID FK → catalog_policy(id)
│
├── entry_spec              JSONB NOT NULL                 -- Article 12
├── variant_spec            JSONB NOT NULL                 -- Article 13
├── pricing_spec            JSONB NOT NULL                 -- Article 14
│
├── provenance              JSONB NOT NULL DEFAULT '{}'
├── created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Constraints:**
- `approved_by IS DISTINCT FROM authored_by`
- `status NOT IN ('active','paused','superseded') OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active'`
- `entry_spec`, `variant_spec`, `pricing_spec`, `version`, `authored_by` are immutable once
  `status IN ('active','paused','superseded')`
- Activation trigger sets the previously active policy to `superseded` within the same transaction

### Article 12 — `entry_spec` Canonical Structure

```json
{
  "min_confidence":                      <float [0,1]>,
  "min_commerce_score":                  <float [0,1]>,
  "min_csm_score":                       <float [0,1]>,
  "families_requiring_variant_approval": [<family_value>, ...],
  "families_requiring_pricing_approval": [<family_value>, ...]
}
```

**12.1** `min_confidence` — minimum `recommendation_confidence` required. Evaluated at NG-1.

**12.2** `min_commerce_score` and `min_csm_score` — advisory gates evaluated at nomination time
and recorded in `nomination_basis`. They do not replace the constitutional hard gates NG-2
through NG-3.

**12.3** `families_requiring_variant_approval` — product families for which every proposed variant
must receive explicit curator approval before becoming `active`.

**12.4** `families_requiring_pricing_approval` — product families for which every pricing profile
requires explicit curator approval before becoming `approved`.

### Article 13 — `variant_spec` Canonical Structure `[Amended v1.1]`

```json
{
  "<family_value>": {
    "<product_type>": {
      "sizes":     [<string>, ...],
      "finishes":  [<string>, ...],
      "materials": [<string>, ...]
    }
  }
}
```

**13.1** The catalog worker generates one `catalog_variant` for each combination of
`(size × finish × material)` per `product_type`. Each variant is assigned a `variant_key`:

```
{family}:{product_type}:{size}:{finish}:{material}
```

The colon (`:`) is the reserved separator for the `variant_key` format. **Dimension values
(family, product_type, size, finish, material) must not contain the colon character.** The catalog
worker must validate this at policy load time and halt if any dimension value contains `:`.

**13.2** `variant_spec` must contain entries only for families present in
`product_family_vocabulary`. The `catalog_policy` activation trigger must validate that every
`product_type` listed in `variant_spec[family]` appears in `routing_rules[family].product_types`
of the `product_routing_policy` that is `active` at the moment the catalog_policy is activated.
If validation fails, the activation trigger must raise an exception and block the transition.
This validation is not repeated at catalog worker runtime.

**13.3** The set of variants produced for a given `(catalog_candidate, catalog_policy)` pair must
be deterministic. Given the same `opportunity_snapshot` and the same `catalog_policy.variant_spec`,
the catalog worker must always produce the same set of `variant_key` values.

### Article 14 — `pricing_spec` Canonical Structure

```json
{
  "<family_value>": {
    "<product_type>": {
      "price_tier":                string,      -- "PREMIUM" | "STANDARD" | "VALUE"
      "markup_multiplier":         <float>,
      "floor_price":               <float>,     -- minimum computed_price in USD; may equal ceiling
      "ceiling_price":             <float>,     -- maximum computed_price in USD; may equal floor
      "requires_curator_approval": boolean,
      "base_unit_by_size": {
        "<size>": <float>                       -- base unit cost in USD
      }
    }
  }
}
```

**14.1** `computed_price = CLAMP(base_unit_by_size[size] × markup_multiplier, floor_price,
ceiling_price)`. When `floor_price = ceiling_price`, `computed_price` is exactly that value
regardless of `base_unit` and `markup_multiplier`. This is the price-lock pattern.

**14.2** `requires_curator_approval` in `pricing_spec` overrides `families_requiring_pricing_approval`
in `entry_spec` at the product_type level.

**14.3** `pricing_spec` must contain entries for every `(family, product_type)` pair present in
`variant_spec`. A variant with no pricing rule in `pricing_spec` is skipped; a `policy_validated`
event is written to `catalog_audit_log` noting the gap.

**14.4** All price values are in USD. Multi-currency support is deferred to a future version.

---

## Part V — Entity Schemas

### Article 15 — `catalog_candidate` Schema `[Amended v1.1]`

```
catalog_candidate
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── opportunity_id            UUID NOT NULL REFERENCES illustration_opportunities(id)
├── commerce_opportunity_id   UUID NOT NULL REFERENCES commerce_opportunities(id)
├── product_recommendation_id UUID NOT NULL REFERENCES product_recommendations(id)
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── product_family            TEXT NOT NULL REFERENCES product_family_vocabulary(value)
├── status                    TEXT NOT NULL DEFAULT 'nominated'
│                                 REFERENCES catalog_candidate_status_vocabulary(value)
├── nominated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── nominated_by              TEXT NOT NULL
├── curator_reviewed_by       TEXT
├── curator_reviewed_at       TIMESTAMPTZ
├── curator_notes             TEXT
├── opportunity_snapshot      JSONB NOT NULL
├── nomination_basis          JSONB NOT NULL
│
├── UNIQUE (opportunity_id, product_family)
│       WHERE status NOT IN ('rejected','retired','withdrawn')
├── CONSTRAINT chk_catalog_candidate_snapshot  CHECK (opportunity_snapshot <> '{}'::jsonb)
├── CONSTRAINT chk_catalog_candidate_basis     CHECK (nomination_basis <> '{}'::jsonb)
├── CONSTRAINT chk_catalog_candidate_review    CHECK (
│       status IN ('nominated','under_review') OR curator_reviewed_by IS NOT NULL
│   )
│
├── provenance                JSONB NOT NULL DEFAULT '{}'
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Triggers on `catalog_candidate`:**

1. **`trg_catalog_candidate_snapshot_immutable`** — BEFORE UPDATE: if `OLD.opportunity_snapshot` is
   not equal to `NEW.opportunity_snapshot`, raise an exception. The snapshot is written once at
   nomination time and must never be modified.

2. **`trg_catalog_candidate_publication_gate`** — BEFORE UPDATE OF status: when
   `NEW.status = 'published'`, verify:
   - `OLD.status = 'approved'`
   - At least one `catalog_variant` with `status = 'active'` exists for this candidate
   - Every `active` variant has exactly one `catalog_pricing_profile` with `status = 'approved'`
   If any condition fails, raise an exception.

**15.1 `nomination_basis` canonical structure:**

```json
{
  "catalog_policy_id":          "<UUID>",
  "catalog_policy_version":     "<semver>",
  "nominated_at":               "<ISO 8601 UTC>",
  "product_recommendation_id":  "<UUID>",
  "recommendation_confidence":  <float>,
  "entry_spec_checks": {
    "min_confidence":            <float>,
    "min_confidence_passed":     <bool>,
    "min_commerce_score":        <float>,
    "min_commerce_score_passed": <bool>,
    "min_csm_score":             <float>,
    "min_csm_score_passed":      <bool>
  },
  "gate_checks": {
    "ng0_status_assigned":  <bool>,
    "ng1_confidence_met":   <bool>,
    "ng2_curator_approved": <bool>,
    "ng3_hard_gate_passed": <bool>,
    "ng4_no_duplicate":     <bool>
  },
  "requires_curator_review": <bool>,
  "curator_review_reason":   "<string or null>"
}
```

### Article 16 — `catalog_variant` Schema `[Amended v1.1]`

```
catalog_variant
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_candidate_id      UUID NOT NULL REFERENCES catalog_candidate(id)
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── product_family            TEXT NOT NULL REFERENCES product_family_vocabulary(value)
├── product_type              TEXT NOT NULL
├── variant_key               TEXT NOT NULL
├── dimensions                JSONB NOT NULL
├── status                    TEXT NOT NULL DEFAULT 'proposed'
│                                 REFERENCES catalog_variant_status_vocabulary(value)
├── variant_basis             JSONB NOT NULL
│
├── UNIQUE (catalog_candidate_id, variant_key)
├── CONSTRAINT chk_catalog_variant_dimensions CHECK (dimensions <> '{}'::jsonb)
├── CONSTRAINT chk_catalog_variant_basis      CHECK (variant_basis <> '{}'::jsonb)
│
├── provenance                JSONB NOT NULL DEFAULT '{}'
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Trigger on `catalog_variant`:**

**`trg_catalog_variant_active_pricing_gate`** — BEFORE UPDATE OF status: when
`NEW.status = 'active'`, verify that exactly one `catalog_pricing_profile` with
`status = 'approved'` exists for `NEW.id`. If the condition fails, raise an exception:
`'catalog_variant cannot be active without an approved catalog_pricing_profile'`. This enforces
PA-12 at the DB level.

**16.1 `dimensions` structure:**
```json
{ "size": "<value>", "finish": "<value>", "material": "<value>" }
```

**16.2 `variant_basis` structure:**
```json
{
  "catalog_policy_id":      "<UUID>",
  "catalog_policy_version": "<semver>",
  "proposed_at":            "<ISO 8601 UTC>",
  "variant_spec_path":      "<family>.<product_type>",
  "variant_key":            "<key>",
  "requires_approval":      <bool>
}
```

### Article 17 — `catalog_pricing_profile` Schema `[Amended v1.1]`

```
catalog_pricing_profile
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_variant_id        UUID NOT NULL REFERENCES catalog_variant(id)
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── price_tier                TEXT NOT NULL
├── base_unit                 NUMERIC(10,4) NOT NULL
├── markup_multiplier         NUMERIC(6,4) NOT NULL
├── floor_price               NUMERIC(10,2)
├── ceiling_price             NUMERIC(10,2)
├── computed_price            NUMERIC(10,2) NOT NULL
├── currency                  TEXT NOT NULL DEFAULT 'USD'
├── status                    TEXT NOT NULL DEFAULT 'draft'
│                                 REFERENCES catalog_pricing_profile_status_vocabulary(value)
├── authored_by               TEXT NOT NULL
├── approved_by               TEXT
├── approved_at               TIMESTAMPTZ
├── pricing_basis             JSONB NOT NULL
│
├── CONSTRAINT chk_catalog_pricing_floor_ceiling CHECK (
│       floor_price IS NULL OR ceiling_price IS NULL OR floor_price <= ceiling_price
│   )
│   -- floor = ceiling is the price-lock pattern (computed_price is exactly fixed)
├── CONSTRAINT chk_catalog_pricing_computed CHECK (
│       computed_price >= COALESCE(floor_price, computed_price)
│       AND computed_price <= COALESCE(ceiling_price, computed_price)
│   )
├── CONSTRAINT chk_catalog_pricing_approval_identity CHECK (
│       approved_by IS NULL OR approved_by IS DISTINCT FROM authored_by
│   )
├── CONSTRAINT chk_catalog_pricing_basis CHECK (pricing_basis <> '{}'::jsonb)
│
├── provenance                JSONB NOT NULL DEFAULT '{}'
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**17.1 `pricing_basis` structure:**
```json
{
  "catalog_policy_id":         "<UUID>",
  "catalog_policy_version":    "<semver>",
  "applied_at":                "<ISO 8601 UTC>",
  "pricing_spec_path":         "<family>.<product_type>",
  "size":                      "<value>",
  "base_unit_source":          "pricing_spec",
  "base_unit":                 <float>,
  "markup_multiplier":         <float>,
  "floor_price":               <float or null>,
  "ceiling_price":             <float or null>,
  "computed_price":            <float>,
  "requires_curator_approval": <bool>
}
```

### Article 18 — `catalog_audit_log` Schema

`catalog_audit_log` is append-only. No UPDATE or DELETE is permitted on any row. Enforcement
follows the PostgreSQL RULE pattern used for `score_audit_log` in the Commerce Intelligence
Constitution.

```
catalog_audit_log
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_candidate_id      UUID NOT NULL REFERENCES catalog_candidate(id)
├── catalog_variant_id        UUID REFERENCES catalog_variant(id)
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── event_type                TEXT NOT NULL REFERENCES catalog_audit_event_type_vocabulary(value)
├── event_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── actor_type                TEXT NOT NULL
├── actor_id                  TEXT NOT NULL
├── actor_notes               TEXT
├── previous_state            JSONB NOT NULL DEFAULT '{}'
├── new_state                 JSONB NOT NULL DEFAULT '{}'
├── entry_checksum_sha256     TEXT NOT NULL
├── previous_entry_checksum   TEXT
├── reason                    TEXT NOT NULL
├── generated_by              TEXT NOT NULL
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
│
├── CONSTRAINT chk_catalog_audit_entry_checksum     CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$')
├── CONSTRAINT chk_catalog_audit_previous_checksum  CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_catalog_audit_distinct_checksum  CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
│   )
├── CONSTRAINT chk_catalog_audit_actor_id           CHECK (length(actor_id) > 0)
├── CONSTRAINT chk_catalog_audit_reason             CHECK (length(reason) > 0)
├── CONSTRAINT chk_catalog_audit_generated_by       CHECK (length(generated_by) > 0)
├── CONSTRAINT chk_catalog_audit_curator_notes      CHECK (
│       actor_type <> 'curator' OR actor_notes IS NOT NULL
│   )
│
└── UNIQUE (catalog_candidate_id, entry_checksum_sha256)
```

Hash chain is per `catalog_candidate_id`. Hash computation follows D-1 canonical JSON (keys
alpha-sorted, null retained, floats to 6 decimal places), identical to `score_audit_log`.

---

## Part VI — Replayability

### Article 19 — Opportunity Snapshot `[Amended v1.1]`

**19.1** At nomination time, the catalog worker captures a full snapshot of the linked
`commerce_opportunity` row and writes it to `catalog_candidate.opportunity_snapshot`. This snapshot
is written once and is immutable. The `trg_catalog_candidate_snapshot_immutable` trigger (Article
15) enforces immutability at the DB level — any UPDATE that changes `opportunity_snapshot` raises
an exception.

**19.2** The snapshot must include, at minimum:
`commerce_opportunity_score`, `commerce_tier`, `csm_score`, `csm_tier`, `hard_gate_status`,
`policy_version_id`, `illustrator_prestige`, `place_relevance_score`, `taxon_commercial_tier`,
`taxon_commercial_tier_score`, `image_width_px`, `image_quality_score`, `computed_at`.

**19.3** The `candidate_nominated` event in `catalog_audit_log` must write the same snapshot to
`new_state`. The audit log is the primary record. The snapshot on `catalog_candidate` is a
query-performance convenience copy.

### Article 20 — Catalog Replayability Invariant `[Amended v1.1]`

A catalog nomination decision is replayable if, given:
- `catalog_candidate.opportunity_snapshot`
- The policy loaded by exact `catalog_candidate.catalog_policy_id`

...the catalog worker can re-derive:
1. Whether the nomination was eligible (NG-0 through NG-4)
2. Which `variant_key` values would be generated (deterministic from `variant_spec`)
3. What `computed_price` each variant would receive (deterministic from `pricing_spec`)

The catalog worker must expose a `replay_nomination(candidate_id)` function that:
1. Loads `catalog_candidate` by `candidate_id`
2. Loads `catalog_policy` by exact `catalog_candidate.catalog_policy_id` — **not** the currently
   active policy. If the policy has been retired, the replay function must still load it by its
   exact `id`. This is the same pattern as the Commerce Intelligence replay worker
   (`load_policy_for_audit` uses `WHERE id = $1`, not `WHERE status = 'active'`).
3. Re-derives the expected set of variants and pricing profiles
4. Compares against the persisted variants and pricing profiles for this candidate
5. Writes a `replay_verified` or `replay_failure` audit event to `catalog_audit_log`

If `replay_failure`, the candidate's `status` is not automatically changed, but the failure event
is visible in the audit chain for curator investigation.

The `catalog_audit_log` hash chain provides integrity verification: if any event in the chain has
been tampered with, the checksum chain breaks, and the replay is flagged as unreliable before
recomputation begins.

---

## Part VII — Human Approval

### Article 21 — Catalog Policy Approval `[Amended v1.1]`

A `catalog_policy` may only become `active` if all five conditions hold:

1. `status = 'pending_approval'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM authored_by`
4. `effective_from IS NOT NULL`
5. No other `catalog_policy` has `status = 'active'`

The activation trigger must also:
- Set the previously active policy to `superseded` within the same transaction
- Validate that every `product_type` in `variant_spec[family]` exists in
  `routing_rules[family].product_types` of the currently active `product_routing_policy`. If
  validation fails, raise an exception and block activation. This is the only point at which
  the catalog constitution references the routing policy — it is a one-time activation gate, not
  a runtime dependency.

### Article 22 — Catalog Candidate and Variant Approval `[Amended v1.1]`

**22.1 Candidate curator review** is required when any of the following hold:
- `entry_spec.families_requiring_variant_approval` includes this candidate's `product_family`
- `entry_spec.families_requiring_pricing_approval` includes this candidate's `product_family`
- `commerce_opportunities.requires_curator_review = TRUE`
- `commerce_opportunities.csm_tier = 'MASTERWORK'`

When required, the catalog worker sets `catalog_candidate.status = 'nominated'` and writes
`candidate_nominated` to the audit log. The curator must transition to `under_review`, then to
`approved` or `rejected`.

When not required, the catalog worker auto-advances the candidate using the `nominated → approved`
direct transition (Article 5). The worker writes both `candidate_nominated` and
`candidate_approved` audit events with `actor_type = 'system_worker'`, within the same
transaction as the candidate INSERT (see Article 26).

**22.2 Variant approval** is required per variant when `product_family` is listed in
`entry_spec.families_requiring_variant_approval`. When required, variants remain `proposed` until
a curator transitions them to `approved`. When not required, the catalog worker transitions
variants from `proposed → approved` with `actor_type = 'system_worker'`, then from
`approved → active` after the pricing profile is in `approved` state.

**22.3 Pricing approval** is required when `pricing_spec[family][product_type].requires_curator_approval = true`
or when `product_family` is listed in `entry_spec.families_requiring_pricing_approval`. When
required, pricing profiles remain `draft` until a curator approves them. When not required,
the catalog worker transitions pricing profiles from `draft → approved` with
`actor_type = 'system_worker'`. Self-approval is prevented by `chk_catalog_pricing_approval_identity`.

**22.4 Publication gate** is enforced by `trg_catalog_candidate_publication_gate` (Article 15).
A `catalog_candidate` may only transition to `published` when:
- `catalog_candidate.status = 'approved'`
- At least one `catalog_variant` with `status = 'active'` exists for this candidate
- Every `active` variant has exactly one `catalog_pricing_profile` with `status = 'approved'`

---

## Part VIII — Prohibited Acts

### Article 23 — Prohibited Acts `[Amended v1.1]`

| Act | Prohibition |
|---|---|
| **PA-1** | No catalog_candidate nomination without an active `catalog_policy` |
| **PA-2** | No hardcoded variant dimensions — all dimensions must come from `variant_spec` |
| **PA-3** | No hardcoded pricing — all pricing parameters must come from `pricing_spec` |
| **PA-4** | No nomination without clearing all nomination gates (NG-0 through NG-4) |
| **PA-5** | No `opportunity_snapshot = '{}'` — snapshot must be fully populated at nomination time |
| **PA-6** | No `nomination_basis = '{}'` or `variant_basis = '{}'` or `pricing_basis = '{}'` |
| **PA-7** | No `UPDATE` or `DELETE` on `catalog_audit_log` rows |
| **PA-8** | No catalog_policy activation without second-human approval |
| **PA-9** | No mutation of `entry_spec`, `variant_spec`, or `pricing_spec` after policy activation |
| **PA-10** | No self-approval of catalog_policy |
| **PA-11** | No catalog_pricing_profile self-approval — `approved_by IS DISTINCT FROM authored_by` |
| **PA-12** | No variant with `status = 'active'` without an `approved` pricing profile — DB-enforced by `trg_catalog_variant_active_pricing_gate` |
| **PA-13** | No `catalog_candidate` publication without satisfying the publication gate (Article 22.4) — DB-enforced by `trg_catalog_candidate_publication_gate` |
| **PA-14** | No variant generation for a `product_type` not in `pricing_spec` — log `policy_validated` event and skip |
| **PA-15** | No dimension value containing `:` in `variant_spec` — the colon is the reserved separator for `variant_key`; the catalog worker must validate and halt if any dimension value contains `:` |
| **PA-16** | No mutation of `opportunity_snapshot` after initial write — DB-enforced by `trg_catalog_candidate_snapshot_immutable` |
| **PA-17** | No replay that loads the currently active catalog_policy — replay must load by exact `catalog_candidate.catalog_policy_id` |

---

## Part IX — Migration Sequence

### Article 24 — Required Migrations

| Migration | Contents | Depends On |
|---|---|---|
| M-26 | Five vocabulary tables + seed values: `catalog_policy_status_vocabulary`, `catalog_candidate_status_vocabulary`, `catalog_variant_status_vocabulary`, `catalog_pricing_profile_status_vocabulary`, `catalog_audit_event_type_vocabulary`. `catalog_policy` table, immutability trigger, activation trigger (supersession cascade + routing policy validation at activation time), UNIQUE partial index on active status. | M-23 (`product_family_vocabulary` FK); `product_routing_policy` table must exist for activation-time validation (runtime dependency, not schema FK) |
| M-27 | `catalog_candidate` table + constraints + `trg_catalog_candidate_snapshot_immutable` + `trg_catalog_candidate_publication_gate`. `catalog_variant` table + constraints + `trg_catalog_variant_active_pricing_gate`. `catalog_pricing_profile` table + constraints. `catalog_audit_log` table + constraints + append-only RULE enforcement. All indexes. | M-26 |
| M-28 | Seed `catalog_policy` v1.0.0 in `draft` status with `entry_spec`, `variant_spec`, `pricing_spec`. | M-27 |

**M-27 additional dependencies**: `catalog_candidate` references `product_recommendations(id)`
(created in M-23) and `commerce_opportunities(id)` (created in M-21). These are schema
dependencies, not runtime-only. M-27 depends on M-21 and M-23 via FK.

### Article 25 — Seed Policy Specification `[Amended v1.1]`

The M-28 seed populates `catalog_policy` v1.0.0 with the following constitutional defaults.
These values are immutable once the policy is activated.

**entry_spec:**
```json
{
  "min_confidence":                      0.70,
  "min_commerce_score":                  0.65,
  "min_csm_score":                       0.60,
  "families_requiring_variant_approval": ["museum_print", "institutional_license"],
  "families_requiring_pricing_approval": ["museum_print", "institutional_license"]
}
```

**variant_spec:**

| Family | Product Type | Sizes | Finishes | Materials |
|---|---|---|---|---|
| `wall_art` | `print_premium` | 8x10, 11x14, 16x20, 24x36 | matte, glossy | fine_art_paper |
| `wall_art` | `print_standard` | 8x10, 11x14 | matte | standard_paper |
| `wall_art` | `canvas` | 12x16, 16x20, 24x36 | gallery_wrap | canvas |
| `museum_print` | `museum_giclée` | 11x14, 16x20, 24x36 | matte | archival_paper |
| `calendar` | `wall_calendar` | standard | standard | coated_paper |
| `book` | `book_interior` | standard | standard | uncoated_paper |
| `puzzle` | `puzzle_1000` | standard | standard | standard |
| `card` | `greeting_card` | standard | matte, glossy | coated_card |
| `educational` | `classroom_poster` | 18x24 | matte | standard_paper |
| `institutional_license` | `digital_license` | digital | digital | digital |
| `home_decor` | `decorative_print` | 8x10, 11x14 | matte | fine_art_paper |

Note: `institutional_license:digital_license` uses `"digital"` for all dimension values, producing
the variant_key `institutional_license:digital_license:digital:digital:digital`. No colon
violations exist in any seed dimension value.

**pricing_spec:**

| Family | Product Type | Price Tier | Markup | Floor | Ceiling | Curator Approval | Note |
|---|---|---|---|---|---|---|---|
| `wall_art` | `print_premium` | PREMIUM | 3.5× | $18 | $125 | false | |
| `wall_art` | `print_standard` | STANDARD | 3.0× | $12 | $60 | false | |
| `wall_art` | `canvas` | PREMIUM | 4.0× | $45 | $200 | false | |
| `museum_print` | `museum_giclée` | PREMIUM | 5.0× | $75 | $350 | **true** | |
| `calendar` | `wall_calendar` | STANDARD | 2.5× | $18 | $40 | false | |
| `book` | `book_interior` | STANDARD | 1.0× | $0 | $0 | false | price-lock at $0 |
| `puzzle` | `puzzle_1000` | STANDARD | 3.0× | $22 | $55 | false | |
| `card` | `greeting_card` | VALUE | 4.0× | $4 | $12 | false | |
| `educational` | `classroom_poster` | VALUE | 2.5× | $8 | $25 | false | |
| `institutional_license` | `digital_license` | PREMIUM | 1.0× | $250 | $2500 | **true** | |
| `home_decor` | `decorative_print` | STANDARD | 3.0× | $14 | $65 | false | |

`book_interior` uses floor=ceiling=$0 (price-lock pattern). This satisfies
`chk_catalog_pricing_floor_ceiling` (`0 <= 0 = TRUE`). The markup multiplier is set to 1.0×
(not 2.0× as in v1.0 draft) to avoid dead-code confusion — with floor=ceiling=$0, the formula
collapses to `CLAMP(anything, 0, 0) = 0` regardless of multiplier.

`base_unit_by_size` JSONB objects must be provided as complete objects in the M-28 SQL seed for
each product_type × size combination. They are director decisions set at seeding time.

---

## Part X — Catalog Worker Protocol `[New — v1.1]`

### Article 26 — Transaction Scope and Ordering

**26.1 Nomination transaction**: The following operations for a single `catalog_candidate` are
wrapped in a single atomic transaction. If any step fails, the entire transaction rolls back:

```
BEGIN;
  INSERT catalog_candidate (status = 'nominated') → obtain candidate.id
  INSERT catalog_audit_log (candidate_nominated, new_state = opportunity_snapshot)
  [if auto-advance]:
    INSERT catalog_audit_log (candidate_approved, actor_type = 'system_worker')
    UPDATE catalog_candidate SET status = 'approved'
COMMIT;
```

**26.2 Variant and pricing transaction**: Each `catalog_variant` and its corresponding
`catalog_pricing_profile` are written in a single atomic transaction:

```
BEGIN;
  INSERT catalog_variant (status = 'proposed') → obtain variant.id
  INSERT catalog_audit_log (variant_proposed)
  INSERT catalog_pricing_profile (status = 'draft') → obtain pricing_profile.id
  INSERT catalog_audit_log (pricing_applied)
  [if auto-approve variant and pricing]:
    UPDATE catalog_variant SET status = 'approved'
    INSERT catalog_audit_log (variant_approved, actor_type = 'system_worker')
    UPDATE catalog_pricing_profile SET status = 'approved', approved_by = worker_id
    INSERT catalog_audit_log (pricing_approved, actor_type = 'system_worker')
    UPDATE catalog_variant SET status = 'active'
    INSERT catalog_audit_log (variant_active, actor_type = 'system_worker')
COMMIT;
```

**26.3 Policy load and validation**: At startup, the catalog worker must:
1. Load the active `catalog_policy`
2. Validate: no dimension value in `variant_spec` contains `:`
3. Validate: `pricing_spec` contains entries for every `(family, product_type)` in `variant_spec`
4. Validate: weights and thresholds are internally consistent
If any validation fails, the worker must halt immediately without processing any opportunities.

**26.4 No re-scoring**: The catalog worker reads scores from `commerce_opportunities` and
`product_recommendations`. It does not call the scoring worker, routing worker, or re-evaluate
any gate from a prior layer. All upstream decisions are fixed at nomination time.

**26.5 No provider calls**: The catalog worker is a DB-only operation. No HTTP calls, webhook
calls, or queue publications to external systems.

---

## Part XI — Ratification

This Constitution is ratified. Migrations M-26, M-27, and M-28 are authorized for implementation.

Implementation of the `catalog_worker` is authorized after M-26 through M-28 are applied and the
v1.0.0 seed policy transitions to `active` through the constitutional activation protocol
(second-human approval required).
