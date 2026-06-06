# Provider Routing Constitution v1.0

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

This Constitution governs the provider routing layer of Nature & Culture. It answers one question:

> How does a publication candidate become a provider route?

The answer is: through a machine-readable provider routing policy, a versioned provider capability
profile, and a governed routing worker that matches each ready publication candidate to the
providers capable of fulfilling it. No provider API is called. No submission is made. No external
system is contacted. The output is a `provider_route_candidate` — the governed declaration that a
specific publication candidate can be fulfilled by a specific provider.

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity Doctrine,
the Commerce Intelligence Constitution v1.1, the Product Routing Constitution v1.1, the Catalog
Constitution v1.1, and the Publication Constitution v1.1. Any provision that conflicts with those
documents is void.

The publication layer answers: "for which channels is this item ready, and what does it look like
in each?" The provider routing layer answers: "within that channel, which providers can fulfill
this specific item, given their current capabilities?" These are distinct governance questions.
A channel is an abstract distribution context. A provider is a concrete fulfillment partner
operating within that channel. Conflating the two is a constitutional violation.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration commerce platform.

**1.2** A `provider_route_candidate` is the governed record that a specific
`publication_candidate` has been evaluated for fulfillment by a specific provider, and the
outcome of that evaluation — including whether the provider's capabilities match the item's
requirements. A route candidate is not a submission, not an order, and not a listing.

**1.3** A `provider_capability_profile` is the versioned, immutable-after-activation record of
what a provider can fulfill: which channels they serve, which product types they support, and what
technical requirements they impose. Capability profiles are facts about providers, not platform
decisions. They require human verification to activate.

**1.4** A `provider_routing_policy` is the platform's machine-readable decision about which
providers are eligible candidates for each `(channel, product_family, product_type)` combination.
It is a platform decision — distinct from provider capability facts — and requires second-human
approval to activate.

**1.5** The separation between routing policy (platform decision) and capability profile (provider
fact) is constitutional. The policy answers "which providers should we consider?" The capability
profile answers "can this provider actually do this?" Both must pass for a route to be created.

**1.6** Provider selection — choosing among multiple approved routes for a single publication
candidate — is downstream of this Constitution and is explicitly out of scope for v1.0.

### Article 2 — Scope

This Constitution governs exactly four entities:

| Entity | Role |
|---|---|
| `provider_routing_policy` | Platform authority for which providers are eligible per channel and product type |
| `provider_capability_profile` | Versioned record of a provider's fulfillment capabilities |
| `provider_route_candidate` | Governed evaluation record for one (publication_candidate, provider) pair |
| `provider_routing_audit_log` | Append-only, hash-chained event record for all routing transitions |

### Article 3 — Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Commerce Intelligence Constitution v1.1
            └─ Product Routing Constitution v1.1
                 └─ Catalog Constitution v1.1
                      └─ Publication Constitution v1.1
                           └─ Provider Routing Constitution v1.0  ← this document
                                └─ provider_routing_policy (active record)
                                     └─ provider_capability_profile (active per provider)
                                          └─ provider_routing_worker
```

No lower authority may override a higher authority. A provider routing policy provision that
contradicts any higher authority is void.

---

## Part II — Vocabulary

### Article 4 — Provider Routing Policy Status Vocabulary

`provider_routing_policy_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Being authored. No routing work permitted. |
| `pending_approval` | Awaiting second-human approval. No routing work permitted. |
| `active` | Authoritative. Routing worker uses this policy. Only one `active` at any time. |
| `paused` | Routing suspended. Existing records remain valid. |
| `superseded` | Replaced by a newer version. Existing records remain valid. |
| `retired` | Permanently withdrawn. No new records may reference this policy. |

Transitions: `draft → pending_approval → active ⇄ paused → superseded → retired`.
Only `active ⇄ paused` is reversible.

### Article 5 — Provider Capability Profile Status Vocabulary

`provider_capability_profile_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Being authored. Not usable by routing worker. |
| `pending_verification` | Awaiting human verification of capabilities against provider documentation. |
| `active` | Verified. Routing worker may use this profile. Only one `active` per `provider_name`. |
| `superseded` | Replaced by a newer version for this provider. Existing routes remain valid. |
| `retired` | Withdrawn. Provider no longer available. Existing routes remain valid. |

Transitions: `draft → pending_verification → active → superseded → retired`.
No transition is reversible. `active → superseded` is triggered by activation of a new profile
for the same `provider_name` within the same transaction.

### Article 6 — Provider Route Candidate Status Vocabulary

`provider_route_candidate_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `matched` | Routing policy lists this provider as eligible for this (channel, product_type). |
| `validated` | Provider capability gates passed. Provider can fulfill this item. |
| `under_review` | Curator review required before approval. |
| `approved` | Approved for submission. Route is constitutionally cleared. |
| `submitted` | Submission to provider confirmed. Set by submission worker (future). |
| `rejected` | Capability gate failed or curator rejected. Terminal state. |
| `retired` | Retired after approval. Terminal state. |
| `withdrawn` | Withdrawn before approval. Terminal state. |

Valid transitions:

```
matched → validated → under_review → approved → submitted → retired
                   → approved  [system_worker only — when curator review not required]
                   → rejected  [capability gate failure]
matched → rejected  [capability evaluation failed before validation]
matched → withdrawn
validated → withdrawn
under_review → withdrawn
approved → withdrawn (before submission)
submitted → retired
```

The `validated → approved` direct transition is reserved for `actor_type = 'system_worker'`.
Curator approvals must proceed through `under_review`. A route in `matched` state that fails
capability gates transitions to `rejected` within the same transaction. All transitions are
enforced by `trg_pvr_candidate_status_transitions`.

### Article 7 — Provider Vocabulary

`provider_vocabulary` is a governed table, not a fixed constitutional list. New providers may
be added by inserting into `provider_vocabulary` as part of creating their first
`provider_capability_profile`. Removing a provider from `provider_vocabulary` requires all
`provider_route_candidate` records with `provider_name = <provider>` to be in terminal status
(`rejected`, `retired`, `withdrawn`). No provider may be hard-deleted while active routes exist.

The seed vocabulary for M-34 is:

| Value | Channel Type | Notes |
|---|---|---|
| `pod_primary` | print_on_demand | Primary print-on-demand fulfillment partner |
| `pod_secondary` | print_on_demand | Secondary print-on-demand fulfillment partner |
| `digital_primary` | digital_download | Primary digital file delivery partner |
| `museum_primary` | museum_retail | Primary museum retail fulfillment partner |
| `educational_primary` | educational | Primary educational distribution partner |
| `institutional_primary` | institutional | Primary institutional licensing partner |

Provider names are immutable once in use by any `provider_route_candidate`.

### Article 8 — Provider Routing Audit Event Type Vocabulary

`provider_routing_audit_event_type_vocabulary` contains exactly these values:

| Value | Level | Meaning |
|---|---|---|
| `route_matched` | Candidate | Routing policy matched this provider as eligible |
| `route_validated` | Candidate | Provider capability gates passed |
| `route_under_review` | Candidate | Curator review initiated |
| `route_approved` | Candidate | Route approved for submission |
| `route_submitted` | Candidate | Submission to provider confirmed |
| `route_rejected` | Candidate | Capability gate failed or curator rejected |
| `route_retired` | Candidate | Route retired |
| `route_withdrawn` | Candidate | Route withdrawn |
| `capability_gate_failed` | Candidate | Named capability gate check failed |
| `policy_validated` | Policy | Routing worker validated policy at load time |
| `capability_profile_superseded` | Profile | Capability profile superseded by newer version |
| `replay_verified` | Replay | Replay produced identical routing outcome |
| `replay_failure` | Replay | Replay diverged — routing outcome changed |

---

## Part III — Provider Routing Gates

### Article 9 — Vendor Route Gates (VRG)

Before evaluating any provider for a given `publication_candidate`, the routing worker must
evaluate five gates. VRG-0 through VRG-3 are candidate-level: failure skips all providers for
this candidate. VRG-4 is a candidate-level policy gate.

| Gate | Condition | Failure Behavior |
|---|---|---|
| **VRG-0** | `publication_candidate.status = 'ready'` | Skip all providers for this candidate |
| **VRG-1** | `publication_channel_profile.status = 'ready'` for this candidate | Skip all providers |
| **VRG-2** | `catalog_snapshot.commerce_opportunity.hard_gate_status = 'passed'` (from snapshot) | Skip all providers — rights re-asserted from snapshot |
| **VRG-3** | Active `provider_routing_policy` exists | Halt — log `policy_validated` event; no routing possible |
| **VRG-4** | `provider_routing` in active policy contains at least one entry for `"<channel>.<family>.<product_type>"` matching this candidate | Skip this candidate — no policy-eligible providers for this combination |

VRG-2 reads `hard_gate_status` from `publication_candidate.catalog_snapshot` — not from a live
read. The publication worker (PPG-3) already performed the live rights re-assertion. The provider
routing worker does not repeat a live read; it reads the snapshot value captured at publication
nomination time.

### Article 10 — Vendor Capability Gates (VCG)

After VRG gates pass, the routing worker evaluates each policy-eligible provider individually.
VCG gates are evaluated per `(publication_candidate, provider)` pair.

| Gate | Condition | Failure Behavior |
|---|---|---|
| **VCG-0** | Active `provider_capability_profile` exists for this `provider_name` | Transition route_candidate to `rejected`; reason: `vcg0_no_active_capability_profile` |
| **VCG-1** | `capability_spec.product_types` contains the key `"<family>.<product_type>"` | Transition to `rejected`; reason: `vcg1_product_type_not_supported` |
| **VCG-2** | `catalog_snapshot.commerce_opportunity.image_width_px >= capability_spec.product_types["<family>.<product_type>"].min_image_width_px` | Transition to `rejected`; reason: `vcg2_image_width_insufficient` |
| **VCG-3** | `publication_snapshot.publication_channel_profile.image_spec.accepted_formats` and `capability_spec.product_types["<family>.<product_type>"].accepted_formats` share at least one common format | Transition to `rejected`; reason: `vcg3_format_incompatible` |
| **VCG-4** | No existing `provider_route_candidate` for `(publication_candidate_id, provider_name)` with `status NOT IN ('rejected','retired','withdrawn')` | Skip — idempotency |

VCG-4 is the idempotency gate. It is evaluated after VCG-0 through VCG-3 to avoid creating
duplicate records for the same `(candidate, provider)` pair.

**10.1** A `provider_route_candidate` is created with `status = 'matched'` before VCG gates are
evaluated. If any VCG-0 through VCG-3 gate fails, the candidate is transitioned to `rejected`
within the same transaction and a `capability_gate_failed` audit event records which gate and why.

---

## Part IV — Policy Schema

### Article 11 — `provider_routing_policy` Schema

```
provider_routing_policy
├── id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── version                 TEXT NOT NULL UNIQUE           -- e.g. "1.0.0"
├── status                  TEXT NOT NULL DEFAULT 'draft'
│                               FK → provider_routing_policy_status_vocabulary
├── effective_from          TIMESTAMPTZ                    -- NULL until activation
├── effective_until         TIMESTAMPTZ                    -- NULL unless superseded
├── authored_by             TEXT NOT NULL
├── approved_by             TEXT                           -- NULL until approval
├── approved_at             TIMESTAMPTZ                    -- NULL until approval
├── changelog               TEXT NOT NULL
├── previous_version_id     UUID FK → provider_routing_policy(id)
│
├── provider_routing        JSONB NOT NULL                 -- Article 12
│
├── provenance              JSONB NOT NULL DEFAULT '{}'
├── created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Constraints:**
- `approved_by IS DISTINCT FROM authored_by`
- `status NOT IN ('active','paused','superseded') OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active'`
- `provider_routing` immutable once `status IN ('active','paused','superseded')`
- `version` and `authored_by` immutable once `status IN ('active','paused','superseded')`
- Activation trigger runs all Article 19 validations within the same transaction

### Article 12 — `provider_routing` Canonical Structure

`provider_routing` is a JSONB object keyed by `"<channel>.<family>.<product_type>"`. Each entry
is an ordered list of provider names from `provider_vocabulary`. Order represents platform
preference when multiple providers are eligible — earlier entries are preferred. Preference order
is informational in v1.0; selection logic is out of scope.

```json
{
  "<channel>.<family>.<product_type>": [<provider_name>, ...]
}
```

**12.1** All provider names in `provider_routing` values must exist in `provider_vocabulary`. The
activation trigger validates this.

**12.2** All channel names in `provider_routing` keys must exist in
`publication_channel_vocabulary`. The activation trigger validates this.

**12.3** All `<family>.<product_type>` portions of keys must match entries in
`catalog_policy.variant_spec` of the `catalog_policy` that is active at the time this
`provider_routing_policy` is activated. This validation is performed once by the activation
trigger, not at worker load time.

**12.4** Each provider named in `provider_routing` values must have an active
`provider_capability_profile` at the time this policy is activated. The activation trigger
validates this. A `provider_routing_policy` cannot activate against a provider with no active
capability profile.

**12.5** A `(channel, family, product_type)` combination absent from `provider_routing` produces
no route candidates. The routing worker silently skips publication candidates with unmapped
routing.

---

## Part V — Provider Capability Profile

### Article 13 — `provider_capability_profile` Schema

```
provider_capability_profile
├── id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── provider_name           TEXT NOT NULL FK → provider_vocabulary(value)
├── version                 TEXT NOT NULL                  -- e.g. "1.0.0"
├── status                  TEXT NOT NULL DEFAULT 'draft'
│                               FK → provider_capability_profile_status_vocabulary
├── effective_from          TIMESTAMPTZ                    -- NULL until activation
├── effective_until         TIMESTAMPTZ                    -- NULL unless superseded
├── authored_by             TEXT NOT NULL
├── verified_by             TEXT                           -- NULL until verification
├── verified_at             TIMESTAMPTZ                    -- NULL until verification
├── verification_source     TEXT                           -- documentation or agreement reference
├── changelog               TEXT NOT NULL
├── previous_version_id     UUID FK → provider_capability_profile(id)
│
├── capability_spec         JSONB NOT NULL                 -- Article 14
│
├── UNIQUE (provider_name, version)
├── provenance              JSONB NOT NULL DEFAULT '{}'
├── created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Constraints:**
- `verified_by IS DISTINCT FROM authored_by`
- `status NOT IN ('active','superseded') OR (verified_by IS NOT NULL AND verified_at IS NOT NULL AND verification_source IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active' AND (provider_name, status)` — one active profile
  per provider_name at any time
- `capability_spec` immutable once `status IN ('active','superseded')`
- `version`, `provider_name`, and `authored_by` immutable once `status IN ('active','superseded')`
- Activation trigger sets previously active profile for this `provider_name` to `superseded`
  within the same transaction

**Triggers:**
1. **`trg_pcp_immutability`** — BEFORE UPDATE: prevents mutation of `capability_spec`,
   `version`, `provider_name`, `authored_by` once status is `active` or `superseded`.
2. **`trg_pcp_activation`** — BEFORE UPDATE OF status: when `NEW.status = 'active'`, sets the
   previously active profile for `NEW.provider_name` to `superseded` within the same transaction.

### Article 14 — `capability_spec` Canonical Structure

`capability_spec` is a JSONB object with the following top-level keys:

```json
{
  "channels":      [<channel_name>, ...],
  "product_types": {
    "<family>.<product_type>": {
      "min_image_width_px":     <int>,
      "accepted_formats":       [<string>, ...],
      "color_profiles":         [<string>, ...],
      "max_file_size_mb":       <int or null>,
      "notes":                  "<string or null>"
    }
  },
  "regions":       [<string>, ...],
  "constraints":   [<string>, ...]
}
```

**14.1** `channels` lists all channels this provider serves. Only values from
`publication_channel_vocabulary` are permitted. The activation trigger validates this.

**14.2** `product_types` is keyed by `"<family>.<product_type>"`. Each entry specifies the
provider's technical requirements for that product type. The routing worker evaluates VCG-1
through VCG-3 against these entries.

**14.3** `regions` is a list of geographic regions the provider serves. Values are ISO 3166-1
alpha-2 country codes or regional strings (e.g., `"US"`, `"EU"`, `"WORLDWIDE"`). In v1.0,
`regions` is informational — it does not gate routing.

**14.4** `constraints` is a list of free-text strings describing provider limitations not
expressible in `product_types`. These are informational in v1.0.

**14.5** A provider's `capability_spec.product_types` must be a subset of what is expressible
within their `capability_spec.channels`. That is: if a product type belongs to a channel not
listed in `capability_spec.channels`, the activation trigger must reject the profile.

---

## Part VI — Entity Schemas

### Article 15 — `provider_route_candidate` Schema

```
provider_route_candidate
├── id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── publication_candidate_id        UUID NOT NULL REFERENCES publication_candidate(id)
├── publication_channel_profile_id  UUID NOT NULL REFERENCES publication_channel_profile(id)
├── provider_routing_policy_id      UUID NOT NULL REFERENCES provider_routing_policy(id)
├── provider_capability_profile_id  UUID NOT NULL REFERENCES provider_capability_profile(id)
├── provider_name                   TEXT NOT NULL REFERENCES provider_vocabulary(value)
├── channel                         TEXT NOT NULL REFERENCES publication_channel_vocabulary(value)
├── status                          TEXT NOT NULL DEFAULT 'matched'
│                                       REFERENCES provider_route_candidate_status_vocabulary(value)
├── matched_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── matched_by                      TEXT NOT NULL
├── curator_reviewed_by             TEXT
├── curator_reviewed_at             TIMESTAMPTZ
├── curator_notes                   TEXT
│
├── publication_snapshot            JSONB NOT NULL             -- Article 17; immutable after write
├── route_basis                     JSONB NOT NULL             -- Article 15.1
│
├── UNIQUE (publication_candidate_id, provider_name)
│       WHERE status NOT IN ('rejected','retired','withdrawn')
├── CONSTRAINT chk_pvr_snapshot  CHECK (publication_snapshot <> '{}'::jsonb)
├── CONSTRAINT chk_pvr_basis     CHECK (route_basis <> '{}'::jsonb)
├── CONSTRAINT chk_pvr_review    CHECK (
│       status IN ('matched','validated','under_review') OR curator_reviewed_by IS NOT NULL
│   )
│
├── provenance                      JSONB NOT NULL DEFAULT '{}'
├── created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Triggers on `provider_route_candidate`:**

1. **`trg_pvr_snapshot_immutable`** — BEFORE UPDATE: if `OLD.publication_snapshot` differs from
   `NEW.publication_snapshot`, raise an exception. The snapshot is written once at matching.

2. **`trg_pvr_candidate_status_transitions`** — BEFORE UPDATE OF status: enforces valid
   transition table from Article 6. Rejects any transition not in the table. Rejects
   `validated → approved` when actor context indicates `actor_type = 'curator'`
   (application-layer control).

**15.1 `route_basis` canonical structure:**

```json
{
  "provider_routing_policy_id":      "<UUID>",
  "provider_routing_policy_version": "<semver>",
  "provider_capability_profile_id":  "<UUID>",
  "provider_capability_profile_version": "<semver>",
  "provider_name":                   "<provider_name>",
  "channel":                         "<channel_name>",
  "routing_rule_path":               "<channel>.<family>.<product_type>",
  "matched_at":                      "<ISO 8601 UTC>",
  "gate_checks": {
    "vrg0_publication_ready":        <bool>,
    "vrg1_profile_ready":            <bool>,
    "vrg2_hard_gate_passed":         <bool>,
    "vrg3_active_policy":            <bool>,
    "vrg4_routing_rule_exists":      <bool>,
    "vcg0_capability_profile_active": <bool>,
    "vcg1_product_type_supported":   <bool>,
    "vcg2_image_width_sufficient":   <bool>,
    "vcg3_format_compatible":        <bool>,
    "vcg4_no_duplicate":             <bool>
  },
  "requires_curator_review":         <bool>,
  "curator_review_reason":           "<string or null>",
  "capability_gate_failure_reason":  "<string or null>"
}
```

### Article 16 — `provider_routing_audit_log` Schema

`provider_routing_audit_log` is append-only. No UPDATE or DELETE is permitted. Enforcement
follows the PostgreSQL RULE pattern established in the Commerce Intelligence Constitution for
`score_audit_log`.

```
provider_routing_audit_log
├── id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── provider_route_candidate_id     UUID NOT NULL REFERENCES provider_route_candidate(id)
├── provider_routing_policy_id      UUID NOT NULL REFERENCES provider_routing_policy(id)
├── event_type                      TEXT NOT NULL
│                                       REFERENCES provider_routing_audit_event_type_vocabulary(value)
├── event_at                        TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── actor_type                      TEXT NOT NULL              -- "system_worker" | "curator"
├── actor_id                        TEXT NOT NULL
├── actor_notes                     TEXT                       -- required when actor_type = 'curator'
├── previous_state                  JSONB NOT NULL DEFAULT '{}'
├── new_state                       JSONB NOT NULL DEFAULT '{}'
├── entry_checksum_sha256           TEXT NOT NULL
├── previous_entry_checksum         TEXT
├── reason                          TEXT NOT NULL
├── generated_by                    TEXT NOT NULL
├── created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
│
├── CONSTRAINT chk_pvr_audit_entry_checksum    CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$')
├── CONSTRAINT chk_pvr_audit_previous_checksum CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_pvr_audit_distinct_checksum CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
│   )
├── CONSTRAINT chk_pvr_audit_actor_id          CHECK (length(actor_id) > 0)
├── CONSTRAINT chk_pvr_audit_reason            CHECK (length(reason) > 0)
├── CONSTRAINT chk_pvr_audit_generated_by      CHECK (length(generated_by) > 0)
├── CONSTRAINT chk_pvr_audit_curator_notes     CHECK (
│       actor_type <> 'curator' OR actor_notes IS NOT NULL
│   )
│
└── UNIQUE (provider_route_candidate_id, entry_checksum_sha256)
```

Hash chain is per `provider_route_candidate_id`. D-1 canonical JSON: keys alpha-sorted, null
retained, floats to 6 decimal places. Same algorithm as all prior constitutional audit logs.

---

## Part VII — Replayability

### Article 17 — Publication Snapshot

**17.1** At matching time, the provider routing worker captures a full snapshot of the publication
layer state and writes it to `provider_route_candidate.publication_snapshot`. The snapshot is
written once and is immutable thereafter, enforced by `trg_pvr_snapshot_immutable`.

**17.2** The snapshot must include, at minimum:

```json
{
  "publication_candidate": {
    "id":                     "<UUID>",
    "channel":                "<channel_name>",
    "status":                 "ready",
    "publication_policy_id":  "<UUID>",
    "nominated_at":           "<ISO 8601 UTC>"
  },
  "publication_channel_profile": {
    "id":               "<UUID>",
    "status":           "ready",
    "metadata":         { "<field>": "<value>", "...": "..." },
    "image_spec": {
      "accepted_formats":   [<string>, ...],
      "min_width_px":       <int>,
      "color_profiles":     [<string>, ...],
      "source_image_width": <int>,
      "source_meets_spec":  <bool>
    },
    "rights_statement":   "<string>",
    "pricing_export": {
      "computed_price": <float>,
      "currency":       "USD",
      "price_tier":     "<tier>",
      "floor_price":    <float or null>,
      "ceiling_price":  <float or null>
    }
  },
  "catalog_snapshot": { ... }
}
```

The `catalog_snapshot` key contains the complete `publication_candidate.catalog_snapshot` value
verbatim — including the `illustration`, `commerce_opportunity`, `catalog_variant`,
`catalog_pricing_profile`, and `catalog_candidate` blocks. This gives the full provenance chain
from illustration to provider route in a single immutable record.

**17.3** The `route_matched` audit event must write the same snapshot to `new_state`. The audit
log is the primary record; the snapshot on `provider_route_candidate` is a query convenience.

### Article 18 — Provider Routing Replayability Invariant

A provider routing decision is replayable if, given:
- `provider_route_candidate.publication_snapshot`
- The policy loaded by exact `provider_route_candidate.provider_routing_policy_id`
- The capability profile loaded by exact `provider_route_candidate.provider_capability_profile_id`

...the routing worker can re-derive:
1. Whether VRG-0 through VRG-4 would pass (deterministic from snapshot and policy)
2. Whether VCG-0 through VCG-4 would pass (deterministic from capability_spec applied to snapshot)
3. The resulting status (`approved` or `rejected`) and the reason if rejected

The routing worker must expose a `replay_route(candidate_id)` function that:
1. Loads the route candidate by `candidate_id`
2. Loads the routing policy by exact `provider_route_candidate.provider_routing_policy_id`
3. Loads the capability profile by exact `provider_route_candidate.provider_capability_profile_id`
4. Re-evaluates all gates against the snapshot
5. Compares the derived outcome against the persisted status
6. Writes `replay_verified` or `replay_failure` to `provider_routing_audit_log`

**18.1 Provider capability versioning and replayability.** A provider's capabilities may change.
When capabilities change, a new `provider_capability_profile` is created and activated, superseding
the old. Existing route candidates retain their `provider_capability_profile_id` — pointing to the
profile that was active when the route was created. Replay must always load the exact profile by ID,
not the currently active profile for that provider. The currently active profile may differ.

**18.2** If a replayed route outcome differs from the persisted outcome, this indicates one of:
(a) the snapshot was mutated (integrity failure), (b) the gate evaluation logic changed, or
(c) the capability profile or routing policy records were mutated after activation (integrity
failure). In all cases, `replay_failure` is the correct audit event.

---

## Part VIII — Human Approval

### Article 19 — Provider Routing Policy Approval

A `provider_routing_policy` may only become `active` if all five conditions hold:

1. `status = 'pending_approval'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM authored_by`
4. `effective_from IS NOT NULL`
5. No other `provider_routing_policy` has `status = 'active'`

The activation trigger must also perform the following validations within the same transaction.
If any validation fails, the activation is rejected:

- Set the previously active policy to `superseded`
- Validate all provider names in `provider_routing` values exist in `provider_vocabulary`
- Validate all channel names in `provider_routing` keys exist in `publication_channel_vocabulary`
- Validate all `<family>.<product_type>` portions of `provider_routing` keys exist in
  `catalog_policy.variant_spec` of the currently active `catalog_policy`
- Validate every provider named in `provider_routing` values has an active
  `provider_capability_profile`

### Article 20 — Provider Capability Profile Verification

A `provider_capability_profile` may only become `active` if all four conditions hold:

1. `status = 'pending_verification'`
2. `verified_by IS NOT NULL AND verified_at IS NOT NULL AND verification_source IS NOT NULL`
3. `verified_by IS DISTINCT FROM authored_by`
4. No other `provider_capability_profile` for this `provider_name` has `status = 'active'`

`verification_source` must reference the documentation or agreement used to confirm the
capability claims — a contract reference, a provider API documentation version, or a written
confirmation from the provider. This is a traceability requirement.

The activation trigger for capability profiles must:
- Set the previously active profile for this `provider_name` to `superseded`
- Validate all channel names in `capability_spec.channels` exist in `publication_channel_vocabulary`
- Validate all `<family>.<product_type>` keys in `capability_spec.product_types` are recognizable
  product types (must exist in the active `catalog_policy.variant_spec`)

### Article 21 — Curator Review Rules

**21.1** A provider route candidate requires curator review if any of the following hold:
- The channel is `museum_retail` or `institutional` (constitutional property per Publication
  Constitution Article 7)
- `publication_snapshot.catalog_snapshot.commerce_opportunity.csm_tier = 'MASTERWORK'`
- `publication_snapshot.catalog_snapshot.commerce_opportunity.requires_curator_review = TRUE`
- The provider's `provider_capability_profile` has `status = 'superseded'` at routing time
  (stale capability — this condition should not occur if VCG-0 is correctly evaluated, but if it
  does, curator review is mandatory)

**21.2** When curator review is required, the routing worker transitions the route candidate from
`validated` to `under_review` within the nomination transaction, after VCG gates pass.

**21.3** When curator review is not required, the routing worker auto-advances using the
`validated → approved` direct transition with `actor_type = 'system_worker'`.

**21.4** The curator approval check (`curator_reviewed_by IS DISTINCT FROM matched_by`) is an
application-layer control. No DB constraint enforces self-approval prevention on
`provider_route_candidate`. This is consistent with the pattern established in the Product
Routing Constitution.

---

## Part IX — Prohibited Acts

### Article 22 — Prohibited Acts

| Act | Prohibition |
|---|---|
| **PA-1** | No routing evaluation without an active `provider_routing_policy` |
| **PA-2** | No hardcoded provider eligibility — all provider lists from `provider_routing` |
| **PA-3** | No hardcoded capability requirements — all requirements from `capability_spec` |
| **PA-4** | No route created without first evaluating VRG-0 through VRG-4 |
| **PA-5** | No VCG evaluation skipped for any provider listed in `provider_routing` for this candidate |
| **PA-6** | No `publication_snapshot = '{}'` — snapshot must be fully populated at matching time |
| **PA-7** | No `route_basis = '{}'` |
| **PA-8** | No `UPDATE` or `DELETE` on `provider_routing_audit_log` rows |
| **PA-9** | No `provider_routing_policy` activation without second-human approval |
| **PA-10** | No `provider_capability_profile` activation without second-human verification |
| **PA-11** | No mutation of `provider_routing` after policy activation |
| **PA-12** | No mutation of `capability_spec` after capability profile activation |
| **PA-13** | No `publication_snapshot` mutation after initial write |
| **PA-14** | No replay that loads the currently active capability profile — replay must use `provider_route_candidate.provider_capability_profile_id` |
| **PA-15** | No replay that loads the currently active routing policy — replay must use `provider_route_candidate.provider_routing_policy_id` |
| **PA-16** | No provider name that embeds a URL, API endpoint, credential, or external system identifier |
| **PA-17** | No external API call in the routing worker — DB-only operation |
| **PA-18** | No provider added to `provider_routing` without a verified active `provider_capability_profile` |
| **PA-19** | No `provider_routing_policy` activation if any listed provider lacks an active `provider_capability_profile` |
| **PA-20** | No capability profile activated without `verification_source` — traceability is mandatory |

---

## Part X — Provider Routing Worker Protocol

### Article 23 — Transaction Scope and Ordering

**23.1 Per-candidate evaluation sequence**: The routing worker evaluates one `publication_candidate`
at a time. For each candidate, it evaluates VRG gates once, then iterates over all policy-eligible
providers, evaluating VCG gates for each. Each `(candidate, provider)` pair is processed in its
own atomic transaction.

**23.2 Nomination transaction — capability gates pass, curator review not required:**

```
BEGIN;
  INSERT provider_route_candidate (status = 'matched') → obtain route_candidate.id
  INSERT provider_routing_audit_log (route_matched, new_state = publication_snapshot)
  UPDATE provider_route_candidate SET status = 'validated'
  INSERT provider_routing_audit_log (route_validated, actor_type = 'system_worker')
  UPDATE provider_route_candidate SET status = 'approved'
  INSERT provider_routing_audit_log (route_approved, actor_type = 'system_worker')
COMMIT;
```

**23.3 Nomination transaction — capability gates pass, curator review required:**

```
BEGIN;
  INSERT provider_route_candidate (status = 'matched') → obtain route_candidate.id
  INSERT provider_routing_audit_log (route_matched, new_state = publication_snapshot)
  UPDATE provider_route_candidate SET status = 'validated'
  INSERT provider_routing_audit_log (route_validated, actor_type = 'system_worker')
  UPDATE provider_route_candidate SET status = 'under_review'
  INSERT provider_routing_audit_log (route_under_review, actor_type = 'system_worker')
COMMIT;
```

**23.4 Nomination transaction — capability gate fails:**

```
BEGIN;
  INSERT provider_route_candidate (status = 'matched') → obtain route_candidate.id
  INSERT provider_routing_audit_log (route_matched, new_state = publication_snapshot)
  UPDATE provider_route_candidate SET status = 'rejected'
  INSERT provider_routing_audit_log (
    capability_gate_failed,
    reason = '<vcg_gate_id>: <failure_reason>',
    actor_type = 'system_worker'
  )
COMMIT;
```

**23.5 Policy load and validation**: At startup, the routing worker must:
1. Load the active `provider_routing_policy`
2. Validate all provider names in `provider_routing` values exist in `provider_vocabulary`
3. Validate all channel names in `provider_routing` keys exist in `publication_channel_vocabulary`
4. Halt immediately if validation fails — process no candidates

The routing worker does not re-validate `provider_routing` product types against `catalog_policy`
at load time. That cross-policy validation was performed once by the activation trigger at policy
activation (Article 19). It is not repeated at runtime.

**23.6 Capability profile loading**: For each provider evaluated during routing, the routing
worker loads the ACTIVE `provider_capability_profile` for that provider at runtime. The active
profile may differ from the profile that was active when the routing policy was last activated.
The worker records the `provider_capability_profile_id` of the profile it used in
`provider_route_candidate.provider_capability_profile_id` and `route_basis`. This is the
replayability anchor for the capability evaluation.

**23.7 No external calls**: The routing worker is a DB-only operation. It does not contact any
provider API, external service, or network resource.

**23.8 No scoring**: The routing worker does not call any upstream scorer or re-evaluate any
upstream gate beyond VRG-0 through VCG-4.

---

## Part XI — Migration Sequence

### Article 24 — Required Migrations

| Migration | Contents | Depends On |
|---|---|---|
| M-32 | Seven vocabulary tables + seed values: `provider_routing_policy_status_vocabulary`, `provider_capability_profile_status_vocabulary`, `provider_route_candidate_status_vocabulary`, `provider_vocabulary` (seed: 6 providers from Article 7), `provider_routing_audit_event_type_vocabulary`. `provider_capability_profile` table + constraints + `trg_pcp_immutability` + `trg_pcp_activation` (supersession cascade + channel validation). UNIQUE partial index WHERE status = 'active' AND provider_name. | M-30 (`publication_candidate`, `publication_channel_profile` must exist for FK from M-33) |
| M-33 | `provider_routing_policy` table + constraints + immutability trigger + activation trigger (all Article 19 validations). UNIQUE partial index WHERE status = 'active'. `provider_route_candidate` table + constraints + `trg_pvr_snapshot_immutable` + `trg_pvr_candidate_status_transitions`. `provider_routing_audit_log` table + constraints + append-only RULE. All indexes. | M-32 |
| M-34 | Seed `provider_capability_profile` records (draft) for all 6 seed providers. Seed `provider_routing_policy` v1.0.0 (draft) with `provider_routing` for all channel/product_type combinations. | M-33 |

### Article 25 — Seed Specification

**Seed capability profiles (M-34, draft status):**

| Provider | Channels | Supported Product Types | Min Width px | Formats |
|---|---|---|---|---|
| `pod_primary` | print_on_demand | wall_art.print_premium, wall_art.print_standard, wall_art.canvas, museum_print.museum_giclée, calendar.wall_calendar, puzzle.puzzle_1000, card.greeting_card, home_decor.decorative_print | 3000 | TIFF, JPEG |
| `pod_secondary` | print_on_demand | wall_art.print_premium, wall_art.print_standard, calendar.wall_calendar, card.greeting_card | 2400 | JPEG |
| `digital_primary` | digital_download | wall_art.print_premium, book.book_interior, educational.classroom_poster | 2000 | JPEG, PNG |
| `museum_primary` | museum_retail | museum_print.museum_giclée | 4000 | TIFF |
| `educational_primary` | educational | educational.classroom_poster | 2400 | JPEG, PNG |
| `institutional_primary` | institutional | institutional_license.digital_license | 3000 | TIFF |

**Seed provider_routing_policy v1.0.0 (M-34, draft status):**

| Channel.Family.Product Type | Providers (by preference) |
|---|---|
| `print_on_demand.wall_art.print_premium` | `pod_primary`, `pod_secondary` |
| `print_on_demand.wall_art.print_standard` | `pod_primary`, `pod_secondary` |
| `print_on_demand.wall_art.canvas` | `pod_primary` |
| `print_on_demand.museum_print.museum_giclée` | `pod_primary` |
| `print_on_demand.calendar.wall_calendar` | `pod_primary`, `pod_secondary` |
| `print_on_demand.puzzle.puzzle_1000` | `pod_primary` |
| `print_on_demand.card.greeting_card` | `pod_primary`, `pod_secondary` |
| `print_on_demand.home_decor.decorative_print` | `pod_primary` |
| `digital_download.wall_art.print_premium` | `digital_primary` |
| `digital_download.book.book_interior` | `digital_primary` |
| `digital_download.educational.classroom_poster` | `digital_primary` |
| `museum_retail.museum_print.museum_giclée` | `museum_primary` |
| `educational.educational.classroom_poster` | `educational_primary` |
| `institutional.institutional_license.digital_license` | `institutional_primary` |

---

## Part XII — Ratification

This Constitution is a draft. It becomes authoritative upon ratification by the Principal
Architect. Ratification is recorded by updating the status field at the top of this document to
`Ratified` and setting the ratification date.

Implementation of Migrations M-32, M-33, and M-34 is not authorized until ratification.

Implementation of the `provider_routing_worker` is not authorized until M-32 through M-34 are
applied, all seed capability profiles have been verified and activated (second-human verification
required per Article 20), and the v1.0.0 seed routing policy has been activated through the
constitutional activation protocol (second-human approval required per Article 19).
