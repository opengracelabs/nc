# Catalog Constitution v1.0

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Draft — awaiting ratification. |
| Repository | opengracelabs/nc |
| Branch | v0.5.1-product-routing |
| Drafted | 2026-06-06 |
| Role | Principal Architect |

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
Any provision that conflicts with those documents is void. This Constitution governs four entities
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
                 └─ Catalog Constitution v1.0  ← this document
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

### Article 5 — Catalog Candidate Status Vocabulary

`catalog_candidate_status_vocabulary` contains exactly these values:

| Value | Transition Rule |
|---|---|
| `nominated` | Initial state. Set by catalog worker at nomination time. |
| `under_review` | Curator has claimed the candidate for review. |
| `approved` | Curator approved. Variants and pricing profiles may now be finalized. |
| `rejected` | Curator rejected. No catalog entry. Candidate is terminal. |
| `published` | All required variants are `active` and all required pricing profiles are `approved`. Candidate is live in the governed catalog. |
| `retired` | Candidate removed from active catalog. Variants and pricing profiles are retired. |
| `withdrawn` | Withdrawn by curator before review is complete. Terminal state. |

Valid transitions:
```
nominated → under_review → approved → published → retired
                        → rejected
nominated → withdrawn
under_review → withdrawn
approved → withdrawn (before publication)
```

### Article 6 — Catalog Variant Status Vocabulary

`catalog_variant_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `proposed` | Variant generated by catalog worker from `variant_spec`. Awaiting approval if required. |
| `approved` | Variant approved by curator (required for premium families; see Article 22). |
| `active` | Variant is live. A `catalog_pricing_profile` with `status = 'approved'` must exist. |
| `retired` | Variant removed from catalog. Terminal state. |
| `rejected` | Variant rejected by curator. Terminal state. |

### Article 7 — Catalog Pricing Profile Status Vocabulary

`catalog_pricing_profile_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Pricing profile generated by catalog worker. Awaiting approval if required. |
| `approved` | Pricing approved. Required before a variant may transition to `active`. |
| `superseded` | Replaced by a revised pricing profile for the same variant. |
| `retired` | Pricing profile retired. Terminal state. |

### Article 8 — Catalog Audit Event Type Vocabulary

`catalog_audit_event_type_vocabulary` contains exactly these values:

| Value | Level | Meaning |
|---|---|---|
| `candidate_nominated` | Candidate | Catalog worker created a candidate |
| `candidate_under_review` | Candidate | Curator claimed for review |
| `candidate_approved` | Candidate | Curator approved |
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
| `policy_validated` | Policy | Catalog worker validated policy at load time |

---

## Part III — Nomination Gates

### Article 9 — Pre-Nomination Gates

Before creating a `catalog_candidate`, the catalog worker must evaluate five nomination gates.
Gates NG-0 through NG-3 are opportunity-level: failure skips the entire nomination. Gate NG-4
is an idempotency gate evaluated per `(opportunity_id, product_family)` pair.

| Gate | Level | Condition | Failure Behavior |
|---|---|---|---|
| **NG-0** | Opportunity | `product_recommendations.status = 'assigned'` | Skip nomination — recommendation not ready |
| **NG-1** | Opportunity | `product_recommendations.recommendation_confidence >= catalog_policy.entry_spec.min_confidence` | Skip nomination — confidence below policy threshold |
| **NG-2** | Opportunity | `commerce_opportunities.curator_decision = 'approved'` | Skip nomination — opportunity not curator-approved |
| **NG-3** | Opportunity | `commerce_opportunities.hard_gate_status = 'passed'` | Skip nomination — opportunity constitutionally blocked |
| **NG-4** | Family | No existing `catalog_candidate` for `(opportunity_id, product_family)` with `status NOT IN ('rejected', 'retired', 'withdrawn')` | Skip that family — idempotency; do not duplicate active candidates |

NG-4 allows re-nomination after rejection or withdrawal. It prevents duplicate active candidates
for the same opportunity-family pair.

### Article 10 — Variant and Pricing Gates

After a `catalog_candidate` is created, the catalog worker proposes variants from
`catalog_policy.variant_spec`. Before proposing a variant, the worker must verify:

| Gate | Condition | Failure Behavior |
|---|---|---|
| **VG-0** | `catalog_candidate.status = 'nominated'` | Do not propose variants — candidate not in valid state |
| **VG-1** | No existing `catalog_variant` for `(catalog_candidate_id, variant_key)` | Skip variant — idempotency |
| **VG-2** | The variant's `product_type` is listed in `routing_rules[family].product_types` (from the active `product_routing_policy`) | Skip variant — product_type not authorized by routing |

Before creating a `catalog_pricing_profile`, the worker must verify:

| Gate | Condition | Failure Behavior |
|---|---|---|
| **PG-0** | `catalog_variant.status = 'proposed'` | Do not apply pricing — variant not in valid state |
| **PG-1** | No existing `catalog_pricing_profile` with `status NOT IN ('superseded','retired')` for this `catalog_variant_id` | Skip — idempotency; one active pricing profile per variant at any time |
| **PG-2** | `pricing_spec[family][product_type]` exists in the active catalog_policy | Skip — no pricing rule for this variant type |

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
- `approved_by IS DISTINCT FROM authored_by` (second-human approval required)
- `status NOT IN ('active','paused','superseded') OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active'` — only one active policy at any time
- `entry_spec`, `variant_spec`, `pricing_spec` are immutable once `status IN ('active','paused','superseded')`
- `version`, `authored_by` are immutable once `status IN ('active','paused','superseded')`
- Activation trigger must set the previously active policy to `superseded` within the same
  transaction (same pattern as `product_routing_policy`, Article 13 of the Routing Constitution)

### Article 12 — `entry_spec` Canonical Structure

`entry_spec` governs which assigned recommendations are eligible for nomination as catalog
candidates.

```json
{
  "min_confidence":                   <float [0,1]>,
  "min_commerce_score":               <float [0,1]>,
  "min_csm_score":                    <float [0,1]>,
  "families_requiring_variant_approval":  [<family_value>, ...],
  "families_requiring_pricing_approval":  [<family_value>, ...]
}
```

**12.1** `min_confidence` — minimum `recommendation_confidence` required on the
`product_recommendation` before nomination. Evaluated at NG-1.

**12.2** `min_commerce_score` and `min_csm_score` — minimum score thresholds read from the
linked `commerce_opportunity`. These are advisory gates evaluated by the catalog worker at
nomination time and recorded in `nomination_basis`. They do not replace the hard gates (NG-2
through NG-3), which are constitutional.

**12.3** `families_requiring_variant_approval` — list of product families for which every proposed
variant must receive explicit curator approval before becoming `active`. If empty, no family
requires variant-level curator approval.

**12.4** `families_requiring_pricing_approval` — list of product families for which every pricing
profile requires explicit curator approval before becoming `approved`. If empty, pricing profiles
generated mechanically from `pricing_spec` may be auto-approved by the catalog worker.

### Article 13 — `variant_spec` Canonical Structure

`variant_spec` defines which variants to generate per product family and product type. The catalog
worker uses this spec to deterministically generate `catalog_variant` records.

```json
{
  "<family_value>": {
    "<product_type>": {
      "sizes":     [<string>, ...],    -- dimension labels, e.g. "8x10", "11x14"
      "finishes":  [<string>, ...],    -- e.g. "matte", "glossy"
      "materials": [<string>, ...]     -- e.g. "fine_art_paper", "canvas"
    }
  }
}
```

**13.1** The catalog worker generates one `catalog_variant` for each combination of
`(size × finish × material)` for each `product_type` present in the spec. Each variant is
assigned a `variant_key` of the form:
```
{family}:{product_type}:{size}:{finish}:{material}
```

**13.2** `variant_spec` must contain entries only for product families present in
`product_family_vocabulary`. Product types within each family must match values declared in the
active `product_routing_policy`'s `routing_rules[family].product_types`. The catalog worker
validates this at policy load time.

**13.3** The set of variants produced for a given `(catalog_candidate, catalog_policy)` pair must
be deterministic. Given the same `opportunity_snapshot` and the same `catalog_policy.variant_spec`,
the catalog worker must always produce the same set of variant_key values. This is the variant
replayability invariant.

### Article 14 — `pricing_spec` Canonical Structure

`pricing_spec` defines the pricing governance formula for each product type and size combination.
The catalog worker uses this spec to generate `catalog_pricing_profile` records.

```json
{
  "<family_value>": {
    "<product_type>": {
      "price_tier":              string,          -- "PREMIUM" | "STANDARD" | "VALUE"
      "markup_multiplier":       <float>,         -- applied to base_unit
      "floor_price":             <float>,         -- minimum computed_price in USD
      "ceiling_price":           <float>,         -- maximum computed_price in USD
      "requires_curator_approval": boolean,
      "base_unit_by_size": {
        "<size>": <float>                         -- base unit cost in USD for this size
      }
    }
  }
}
```

**14.1** `computed_price = CLAMP(base_unit_by_size[size] × markup_multiplier, floor_price,
ceiling_price)`. The catalog worker computes this at pricing profile creation time and stores it
on `catalog_pricing_profile.computed_price`.

**14.2** `requires_curator_approval` in `pricing_spec` overrides `families_requiring_pricing_approval`
in `entry_spec`. If `pricing_spec[family][product_type].requires_curator_approval = true`, every
pricing profile for that product type requires explicit curator approval regardless of the entry_spec
setting.

**14.3** `pricing_spec` must contain entries for every `(family, product_type)` pair present in
`variant_spec`. A variant with no pricing rule in `pricing_spec` must not be created (VG-2
equivalent — the catalog worker skips it and logs a `policy_validated` event noting the gap).

**14.4** All price values are in USD. Multi-currency support is deferred to a future version.

---

## Part V — Entity Schemas

### Article 15 — `catalog_candidate` Schema

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
├── nominated_by              TEXT NOT NULL              -- catalog_worker identity
├── curator_reviewed_by       TEXT                       -- NULL until reviewed
├── curator_reviewed_at       TIMESTAMPTZ                -- NULL until reviewed
├── curator_notes             TEXT
├── opportunity_snapshot      JSONB NOT NULL             -- see Article 19
├── nomination_basis          JSONB NOT NULL             -- see Article 15.1
│
├── UNIQUE (opportunity_id, product_family)  WHERE status NOT IN ('rejected','retired','withdrawn')
├── CONSTRAINT chk_catalog_candidate_snapshot   CHECK (opportunity_snapshot <> '{}'::jsonb)
├── CONSTRAINT chk_catalog_candidate_basis      CHECK (nomination_basis <> '{}'::jsonb)
├── CONSTRAINT chk_catalog_candidate_review     CHECK (
│       status = 'nominated' OR status = 'under_review'
│       OR curator_reviewed_by IS NOT NULL
│   )
│
├── provenance                JSONB NOT NULL DEFAULT '{}'
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**15.1 `nomination_basis` canonical structure:**

```json
{
  "catalog_policy_id":          "<UUID>",
  "catalog_policy_version":     "<semver>",
  "nominated_at":               "<ISO 8601 UTC>",
  "product_recommendation_id":  "<UUID>",
  "recommendation_confidence":  <float>,
  "entry_spec_checks": {
    "min_confidence":           <float>,
    "min_confidence_passed":    <bool>,
    "min_commerce_score":       <float>,
    "min_commerce_score_passed": <bool>,
    "min_csm_score":            <float>,
    "min_csm_score_passed":     <bool>
  },
  "gate_checks": {
    "ng0_status_assigned":      <bool>,
    "ng1_confidence_met":       <bool>,
    "ng2_curator_approved":     <bool>,
    "ng3_hard_gate_passed":     <bool>,
    "ng4_no_duplicate":         <bool>
  },
  "requires_curator_review":    <bool>,
  "curator_review_reason":      "<string or null>"
}
```

### Article 16 — `catalog_variant` Schema

```
catalog_variant
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_candidate_id      UUID NOT NULL REFERENCES catalog_candidate(id)
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── product_family            TEXT NOT NULL REFERENCES product_family_vocabulary(value)
├── product_type              TEXT NOT NULL
├── variant_key               TEXT NOT NULL
│                                 -- {family}:{product_type}:{size}:{finish}:{material}
├── dimensions                JSONB NOT NULL             -- see Article 16.1
├── status                    TEXT NOT NULL DEFAULT 'proposed'
│                                 REFERENCES catalog_variant_status_vocabulary(value)
├── variant_basis             JSONB NOT NULL             -- see Article 16.2
│
├── UNIQUE (catalog_candidate_id, variant_key)
├── CONSTRAINT chk_catalog_variant_dimensions CHECK (dimensions <> '{}'::jsonb)
├── CONSTRAINT chk_catalog_variant_basis      CHECK (variant_basis <> '{}'::jsonb)
│
├── provenance                JSONB NOT NULL DEFAULT '{}'
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**16.1 `dimensions` structure:**
```json
{
  "size":     "<value>",    -- e.g. "11x14"
  "finish":   "<value>",    -- e.g. "matte"
  "material": "<value>"     -- e.g. "fine_art_paper"
}
```

**16.2 `variant_basis` structure:**
```json
{
  "catalog_policy_id":     "<UUID>",
  "catalog_policy_version": "<semver>",
  "proposed_at":            "<ISO 8601 UTC>",
  "variant_spec_path":      "<family>.<product_type>",
  "variant_key":            "<key>",
  "requires_approval":      <bool>
}
```

### Article 17 — `catalog_pricing_profile` Schema

```
catalog_pricing_profile
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_variant_id        UUID NOT NULL REFERENCES catalog_variant(id)
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── price_tier                TEXT NOT NULL              -- "PREMIUM" | "STANDARD" | "VALUE"
├── base_unit                 NUMERIC(10,4) NOT NULL     -- from pricing_spec.base_unit_by_size
├── markup_multiplier         NUMERIC(6,4) NOT NULL      -- from pricing_spec
├── floor_price               NUMERIC(10,2)
├── ceiling_price             NUMERIC(10,2)
├── computed_price            NUMERIC(10,2) NOT NULL     -- CLAMP(base_unit * markup, floor, ceiling)
├── currency                  TEXT NOT NULL DEFAULT 'USD'
├── status                    TEXT NOT NULL DEFAULT 'draft'
│                                 REFERENCES catalog_pricing_profile_status_vocabulary(value)
├── authored_by               TEXT NOT NULL              -- catalog_worker identity
├── approved_by               TEXT                       -- NULL until approved
├── approved_at               TIMESTAMPTZ                -- NULL until approved
├── pricing_basis             JSONB NOT NULL             -- see Article 17.1
│
├── CONSTRAINT chk_catalog_pricing_floor_ceiling CHECK (
│       floor_price IS NULL OR ceiling_price IS NULL OR floor_price < ceiling_price
│   )
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
follows the same PostgreSQL RULE pattern used for `score_audit_log` in the Commerce Intelligence
Constitution.

```
catalog_audit_log
├── id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_candidate_id      UUID NOT NULL REFERENCES catalog_candidate(id)
├── catalog_variant_id        UUID REFERENCES catalog_variant(id)        -- NULL for candidate events
├── catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id)
├── event_type                TEXT NOT NULL REFERENCES catalog_audit_event_type_vocabulary(value)
├── event_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── actor_type                TEXT NOT NULL               -- "system_worker" | "curator"
├── actor_id                  TEXT NOT NULL               -- worker version or curator identity
├── actor_notes               TEXT                        -- required when actor_type = 'curator'
├── previous_state            JSONB NOT NULL DEFAULT '{}'
├── new_state                 JSONB NOT NULL DEFAULT '{}'
├── entry_checksum_sha256     TEXT NOT NULL               -- SHA-256, lowercase hex, 64 chars
├── previous_entry_checksum   TEXT                        -- NULL for first candidate event
├── reason                    TEXT NOT NULL
├── generated_by              TEXT NOT NULL               -- worker version string
├── created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
│
├── CONSTRAINT chk_catalog_audit_entry_checksum  CHECK (
│       entry_checksum_sha256 ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_catalog_audit_previous_checksum CHECK (
│       previous_entry_checksum IS NULL
│       OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_catalog_audit_distinct_checksum CHECK (
│       previous_entry_checksum IS NULL
│       OR previous_entry_checksum <> entry_checksum_sha256
│   )
├── CONSTRAINT chk_catalog_audit_actor_id        CHECK (length(actor_id) > 0)
├── CONSTRAINT chk_catalog_audit_reason          CHECK (length(reason) > 0)
├── CONSTRAINT chk_catalog_audit_generated_by    CHECK (length(generated_by) > 0)
├── CONSTRAINT chk_catalog_audit_curator_notes   CHECK (
│       actor_type <> 'curator' OR actor_notes IS NOT NULL
│   )
│
└── UNIQUE (catalog_candidate_id, entry_checksum_sha256)
```

The hash chain is per `catalog_candidate_id`. The `previous_entry_checksum` links each event to
the prior event for the same candidate. Hash computation follows D-1 canonical JSON (keys
alpha-sorted, null retained, floats to 6 decimal places), same as `score_audit_log`.

---

## Part VI — Replayability

### Article 19 — Opportunity Snapshot

**19.1** At nomination time, the catalog worker must capture a full snapshot of the linked
`commerce_opportunity` row and write it to `catalog_candidate.opportunity_snapshot`. This snapshot
is written once and is immutable thereafter.

**19.2** The snapshot must include, at minimum, the following fields from `commerce_opportunities`:
`commerce_opportunity_score`, `commerce_tier`, `csm_score`, `csm_tier`, `hard_gate_status`,
`policy_version_id`, `illustrator_prestige`, `place_relevance_score`, `taxon_commercial_tier`,
`taxon_commercial_tier_score`, `image_width_px`, `image_quality_score`, `computed_at`.

**19.3** The `candidate_nominated` event in `catalog_audit_log` must write the same snapshot to
`new_state`. The audit log is the primary record. The snapshot on `catalog_candidate` is a
convenience copy for query performance.

### Article 20 — Catalog Replayability Invariant

A catalog routing decision is replayable if, given:
- `catalog_candidate.opportunity_snapshot` (opportunity state at nomination time)
- `catalog_candidate.catalog_policy_id` → `catalog_policy.entry_spec`, `variant_spec`,
  `pricing_spec`

...the catalog worker can re-derive:
1. Whether the nomination was eligible (NG-0 through NG-4)
2. Which variant_keys would be generated (deterministic from `variant_spec`)
3. What `computed_price` each variant would receive (deterministic from `pricing_spec`)

The catalog worker must expose a `replay_nomination()` function that accepts a candidate_id, loads
its snapshot and policy, and returns the expected set of variants and pricing profiles. A
`replay_verified` or `replay_failure` audit event is written as the outcome.

The `catalog_audit_log` hash chain provides integrity verification: if any event in the chain has
been tampered with, the checksum chain breaks, and the replay is flagged as unreliable.

---

## Part VII — Human Approval

### Article 21 — Catalog Policy Approval

A `catalog_policy` may only become `active` if:

1. `status = 'pending_approval'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM authored_by`
4. `effective_from IS NOT NULL`
5. No other `catalog_policy` has `status = 'active'`

These conditions are enforced by a BEFORE UPDATE trigger. The trigger must also set the previously
active policy to `superseded` within the same transaction.

### Article 22 — Catalog Candidate and Variant Approval

**22.1 Candidate curator review** is required when any of the following hold:
- `entry_spec.families_requiring_variant_approval` includes this candidate's `product_family`
- `entry_spec.families_requiring_pricing_approval` includes this candidate's `product_family`
- `commerce_opportunities.requires_curator_review = TRUE`
- `commerce_opportunities.csm_tier = 'MASTERWORK'`

When required, the catalog worker sets `catalog_candidate.status = 'nominated'` and writes
`candidate_nominated` to the audit log. The curator must explicitly transition to `under_review`
and then `approved` or `rejected`.

When not required, the catalog worker may auto-advance the candidate to `approved` immediately
after writing all variants and pricing profiles. The auto-advance must still write the
`candidate_approved` audit event with `actor_type = 'system_worker'`.

**22.2 Variant approval** is required per variant when `product_family` is listed in
`entry_spec.families_requiring_variant_approval`. When required, variants remain `proposed` until
a curator transitions them to `approved` or `rejected`.

**22.3 Pricing approval** is required per pricing profile when `pricing_spec[family][product_type].requires_curator_approval = true`
or when `product_family` is listed in `entry_spec.families_requiring_pricing_approval`. When
required, pricing profiles remain `draft` until a curator transitions them to `approved`. A
curator may not approve a pricing profile they authored.

**22.4 Publication gate**: A `catalog_candidate` may only transition to `published` when:
- `catalog_candidate.status = 'approved'`
- At least one `catalog_variant` with `status = 'active'` exists for this candidate
- Every `active` variant has exactly one `catalog_pricing_profile` with `status = 'approved'`

This gate is enforced by a BEFORE UPDATE trigger on `catalog_candidate` that fires on
`UPDATE OF status`.

---

## Part VIII — Prohibited Acts

### Article 23 — Prohibited Acts

| Act | Prohibition |
|---|---|
| **PA-1** | No catalog_candidate nomination without an active `catalog_policy` |
| **PA-2** | No hardcoded variant dimensions — all dimensions must come from `variant_spec` |
| **PA-3** | No hardcoded pricing — all pricing parameters must come from `pricing_spec` |
| **PA-4** | No nomination without clearing all five nomination gates (NG-0 through NG-4) |
| **PA-5** | No `opportunity_snapshot = '{}'` — snapshot must be fully populated at nomination time |
| **PA-6** | No `nomination_basis = '{}'` or `variant_basis = '{}'` or `pricing_basis = '{}'` |
| **PA-7** | No `UPDATE` or `DELETE` on `catalog_audit_log` rows |
| **PA-8** | No catalog_policy activation without second-human approval |
| **PA-9** | No mutation of `entry_spec`, `variant_spec`, or `pricing_spec` after policy activation |
| **PA-10** | No self-approval of catalog_policy |
| **PA-11** | No catalog_pricing_profile self-approval — `approved_by IS DISTINCT FROM authored_by` |
| **PA-12** | No variant with `status = 'active'` without an `approved` pricing profile |
| **PA-13** | No `catalog_candidate` publication without satisfying the publication gate (Article 22.4) |
| **PA-14** | No variant generation for a product_type not present in `pricing_spec` — skip with audit event |
| **PA-15** | No variant_key that cannot be deterministically re-derived from the opportunity_snapshot and the catalog_policy — variant_key must encode only dimensions declared in variant_spec |

---

## Part IX — Migration Sequence

### Article 24 — Required Migrations

| Migration | Contents | Depends On |
|---|---|---|
| M-26 | All five vocabulary tables + seed values: `catalog_policy_status_vocabulary`, `catalog_candidate_status_vocabulary`, `catalog_variant_status_vocabulary`, `catalog_pricing_profile_status_vocabulary`, `catalog_audit_event_type_vocabulary`. `catalog_policy` table, immutability trigger, activation trigger (with supersession cascade), UNIQUE partial index on active status. | M-23 (product_family_vocabulary, which `catalog_candidate.product_family` FKs) |
| M-27 | `catalog_candidate` table + constraints + BEFORE UPDATE trigger (publication gate). `catalog_variant` table + constraints. `catalog_pricing_profile` table + constraints. `catalog_audit_log` table + constraints + append-only RULE enforcement. All indexes. | M-26 |
| M-28 | Seed `catalog_policy` v1.0.0 in `draft` status with `entry_spec`, `variant_spec`, `pricing_spec` for all governed product families. | M-27 |

### Article 25 — Seed Policy Specification

The M-28 seed must populate `catalog_policy` v1.0.0 with:

**entry_spec defaults:**

```json
{
  "min_confidence":                      0.70,
  "min_commerce_score":                  0.65,
  "min_csm_score":                       0.60,
  "families_requiring_variant_approval": ["museum_print", "institutional_license"],
  "families_requiring_pricing_approval": ["museum_print", "institutional_license"]
}
```

**variant_spec defaults (selected families):**

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
| `institutional_license` | `digital_license` | N/A | N/A | digital |
| `home_decor` | `decorative_print` | 8x10, 11x14 | matte | fine_art_paper |

**pricing_spec defaults:**

| Family | Product Type | Price Tier | Markup | Floor | Ceiling | Curator Approval |
|---|---|---|---|---|---|---|
| `wall_art` | `print_premium` | PREMIUM | 3.5× | $18 | $125 | false |
| `wall_art` | `print_standard` | STANDARD | 3.0× | $12 | $60 | false |
| `wall_art` | `canvas` | PREMIUM | 4.0× | $45 | $200 | false |
| `museum_print` | `museum_giclée` | PREMIUM | 5.0× | $75 | $350 | **true** |
| `calendar` | `wall_calendar` | STANDARD | 2.5× | $18 | $40 | false |
| `book` | `book_interior` | STANDARD | 2.0× | $0 | $0 | false |
| `puzzle` | `puzzle_1000` | STANDARD | 3.0× | $22 | $55 | false |
| `card` | `greeting_card` | VALUE | 4.0× | $4 | $12 | false |
| `educational` | `classroom_poster` | VALUE | 2.5× | $8 | $25 | false |
| `institutional_license` | `digital_license` | PREMIUM | 1.0× | $250 | $2500 | **true** |
| `home_decor` | `decorative_print` | STANDARD | 3.0× | $14 | $65 | false |

`base_unit_by_size` values are director decisions and must be provided as a complete JSONB object
in the M-28 seed SQL. The values above indicate the pricing tier and markup structure; exact base
unit costs are set at seeding time and are immutable once the policy is activated.

---

## Part X — Ratification

This Constitution is a draft. It becomes authoritative upon ratification by the Principal
Architect. Ratification is recorded by updating the status field at the top of this document to
`Ratified` and setting the ratification date.

Implementation of Migrations M-26, M-27, and M-28 is not authorized until ratification.

Implementation of the `catalog_worker` is not authorized until M-26 through M-28 are applied and
the v1.0.0 seed policy transitions to `active` through the constitutional activation protocol
(second-human approval required).
