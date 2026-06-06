# Publication Constitution v1.0

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

This Constitution governs the publication layer of Nature & Culture. It answers one question:

> How does a catalog object become a publication candidate?

The answer is: through a machine-readable publication policy, a governed publication worker, and
a channel-specific profile that captures what the item looks like in that channel. No provider is
contacted. No listing is created. No storefront is integrated. The output is a
`publication_candidate` with a `publication_channel_profile` — the governed declaration that a
specific catalog variant is ready for a specific distribution channel. Publication is governance.

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity Doctrine,
the Commerce Intelligence Constitution v1.1, the Product Routing Constitution v1.1, and the Catalog
Constitution v1.1. Any provision that conflicts with those documents is void. This Constitution
governs four entities and the worker that supports them.

The catalog layer answers: "what should exist, in what configuration, at what governed price."
The publication layer answers: "for which channels is this item ready, and what does it look like
in each?" These are distinct governance questions governed by distinct policies.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration commerce platform.

**1.2** A `publication_candidate` is the governed declaration that a specific `catalog_variant` is
ready for a specific distribution channel. A `publication_channel_profile` is the channel-specific
governance record capturing metadata, image specification, rights statement, and pricing export for
that channel. Neither record is a listing, a storefront entry, or a provider payload.

**1.3** The catalog worker produces governed catalog variants with approved pricing. The publication
worker reads those variants and routes them to channels via the publication policy. These are
distinct responsibilities governed by distinct policies.

**1.4** A channel is a governed distribution context — a named, policy-defined category of how an
illustration product reaches an audience. Channels are not provider names. Provider integration is
explicitly out of scope for v1.0 and must not be embedded in any column, constraint, or vocabulary
value governed by this Constitution.

**1.5** The `publication_channel_profile` is the terminal governance record in the constitutional
chain. It captures the governed answer to: "if this item were submitted to this channel, what
would that submission contain?" The submission itself is downstream of this Constitution.

### Article 2 — Scope

This Constitution governs exactly four entities:

| Entity | Role |
|---|---|
| `publication_policy` | Machine-readable authority for all publication decisions |
| `publication_candidate` | Governed intent to publish a catalog variant to a channel |
| `publication_channel_profile` | Channel-specific governance record for a publication candidate |
| `publication_audit_log` | Append-only, hash-chained event record for all publication transitions |

### Article 3 — Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Commerce Intelligence Constitution v1.1
            └─ Product Routing Constitution v1.1
                 └─ Catalog Constitution v1.1
                      └─ Publication Constitution v1.0  ← this document
                           └─ publication_policy (active record)
                                └─ publication_worker
```

No lower authority may override a higher authority. A publication policy provision that contradicts
any higher authority is void.

---

## Part II — Vocabulary

### Article 4 — Publication Policy Status Vocabulary

`publication_policy_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Being authored. No publication work permitted. |
| `pending_approval` | Awaiting second-human approval. No publication work permitted. |
| `active` | Authoritative. Publication worker uses this policy. Only one `active` at any time. |
| `paused` | Publication suspended. Existing records remain valid. |
| `superseded` | Replaced by a newer version. Existing records remain valid. |
| `retired` | Permanently withdrawn. No new records may reference this policy. |

Transitions: `draft → pending_approval → active ⇄ paused → superseded → retired`.
Only `active ⇄ paused` is reversible.

### Article 5 — Publication Candidate Status Vocabulary

`publication_candidate_status_vocabulary` contains exactly these values:

| Value | Transition Rule |
|---|---|
| `nominated` | Initial state. Set by publication worker. |
| `under_review` | Curator has claimed for review. |
| `ready` | Governance requirements satisfied. Item is constitutionally cleared for the channel. |
| `published` | External publication confirmed. Set by channel worker or curator after actual submission. |
| `rejected` | Curator rejected. Terminal state. |
| `retired` | Removed from publication. Terminal state. |
| `withdrawn` | Withdrawn before publication. Terminal state. |

Valid transitions:

```
nominated → under_review → ready → published → retired
                        → rejected
nominated → ready   [system_worker only — when curator review not required]
nominated → withdrawn
under_review → withdrawn
ready → withdrawn (before publication)
published → retired
```

The `nominated → ready` direct transition is reserved for `actor_type = 'system_worker'`. Curator
approvals must proceed through `under_review`. The `ready → published` transition is set by a
channel worker (future implementation) or by a curator who confirms external submission. In v1.0,
the `ready` state is the terminal governance output.

### Article 6 — Publication Channel Profile Status Vocabulary

`publication_channel_profile_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Generated by publication worker. Awaiting review if required. |
| `reviewed` | Curator has reviewed metadata and channel configuration. |
| `ready` | Profile is complete and constitutionally cleared. Parent candidate may transition to `ready`. |
| `published` | Profile has been submitted externally. Set in concert with candidate `published`. |
| `retired` | Profile retired. Terminal state. |

### Article 7 — Publication Channel Vocabulary

`publication_channel_vocabulary` contains exactly these values:

| Value | Audience | Curator Review |
|---|---|---|
| `print_on_demand` | General retail — print products | false |
| `digital_download` | General retail — digital files | false |
| `museum_retail` | Museum shop retail | **true** |
| `educational` | Educational institutions | false |
| `institutional` | Institutional licensing | **true** |

`curator_always_required` is a constitutional property of the channel, not a policy parameter. The
values above are fixed. A new channel requires a constitution amendment, not a policy update.

### Article 8 — Publication Audit Event Type Vocabulary

`publication_audit_event_type_vocabulary` contains exactly these values:

| Value | Level | Meaning |
|---|---|---|
| `candidate_nominated` | Candidate | Publication worker created a candidate |
| `candidate_under_review` | Candidate | Curator claimed for review |
| `candidate_ready` | Candidate | Governance requirements satisfied |
| `candidate_published` | Candidate | External publication confirmed |
| `candidate_rejected` | Candidate | Curator rejected |
| `candidate_retired` | Candidate | Candidate retired |
| `candidate_withdrawn` | Candidate | Candidate withdrawn |
| `channel_profile_drafted` | Profile | Publication worker drafted a channel profile |
| `channel_profile_reviewed` | Profile | Curator reviewed channel profile |
| `channel_profile_ready` | Profile | Channel profile cleared for publication |
| `channel_profile_published` | Profile | Channel profile submitted externally |
| `channel_profile_retired` | Profile | Channel profile retired |
| `policy_validated` | Policy | Worker validated policy at load time |
| `replay_verified` | Replay | Replay produced identical channel profiles |
| `replay_failure` | Replay | Replay diverged — integrity suspect |

---

## Part III — Publication Gates

### Article 9 — Pre-Nomination Gates

Before creating a `publication_candidate`, the publication worker must evaluate five gates. Gates
PPG-0 through PPG-3 are opportunity-level: failure skips all channels for that variant. PPG-4 is
an idempotency gate per `(catalog_variant_id, channel)` pair.

| Gate | Level | Condition | Failure Behavior |
|---|---|---|---|
| **PPG-0** | Variant | `catalog_candidate.status = 'published'` | Skip all channels for this variant |
| **PPG-1** | Variant | `catalog_variant.status = 'active'` | Skip all channels |
| **PPG-2** | Variant | `catalog_pricing_profile.status = 'approved'` for this variant | Skip all channels |
| **PPG-3** | Variant | `commerce_opportunities.hard_gate_status = 'passed'` (re-verified) | Skip all channels — rights gate is re-asserted at publication time |
| **PPG-4** | Channel | No existing `publication_candidate` for `(catalog_variant_id, channel)` with `status NOT IN ('rejected','retired','withdrawn')` | Skip that channel — idempotency |

PPG-3 re-asserts the constitutional rights gate. Even though hard gates were checked at scoring
time, a legal hold or rights revocation may have occurred since scoring. The publication layer is
the last constitutional checkpoint before external distribution.

### Article 10 — Channel Profile Gate

After a `publication_candidate` is created, the publication worker generates a
`publication_channel_profile`. Before generating the profile, the worker must verify:

| Gate | Condition | Failure Behavior |
|---|---|---|
| **CPG-0** | `publication_candidate.status = 'nominated'` | Do not generate profile |
| **CPG-1** | No existing `publication_channel_profile` for this `publication_candidate_id` with `status NOT IN ('retired')` | Skip — idempotency |
| **CPG-2** | `channel_spec[channel]` exists in the active publication_policy | Log `policy_validated` event; skip candidate |
| **CPG-3** | `catalog_snapshot.opportunity_snapshot.image_width_px >= channel_spec[channel].min_image_width_px` | Log `policy_validated` event; skip candidate — image does not meet channel resolution requirement |

CPG-3 is the only gate that varies per channel. An illustration that meets PPG-3 (scoring gate:
≥ 2000px) may still fail CPG-3 for a channel with a higher resolution requirement (e.g.,
`museum_retail` at 4000px). This is not a constitutional violation — it is correct behavior.

---

## Part IV — Policy Schema

### Article 11 — `publication_policy` Schema

```
publication_policy
├── id                      UUID PRIMARY KEY
├── version                 TEXT NOT NULL UNIQUE           -- e.g. "1.0.0"
├── status                  TEXT NOT NULL FK → publication_policy_status_vocabulary
├── effective_from          TIMESTAMPTZ                    -- NULL until activation
├── effective_until         TIMESTAMPTZ                    -- NULL unless superseded
├── authored_by             TEXT NOT NULL
├── approved_by             TEXT                           -- NULL until approval
├── approved_at             TIMESTAMPTZ                    -- NULL until approval
├── changelog               TEXT NOT NULL
├── previous_version_id     UUID FK → publication_policy(id)
│
├── channel_routing         JSONB NOT NULL                 -- Article 12
├── channel_spec            JSONB NOT NULL                 -- Article 13
│
├── provenance              JSONB NOT NULL DEFAULT '{}'
├── created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Constraints:**
- `approved_by IS DISTINCT FROM authored_by`
- `status NOT IN ('active','paused','superseded') OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active'`
- `channel_routing` and `channel_spec` immutable once `status IN ('active','paused','superseded')`
- `version` and `authored_by` immutable once `status IN ('active','paused','superseded')`
- Activation trigger sets previously active policy to `superseded` within the same transaction
- Activation trigger validates all channel values in `channel_routing` and `channel_spec` exist in
  `publication_channel_vocabulary`

### Article 12 — `channel_routing` Canonical Structure

`channel_routing` is a JSONB object keyed by `"<family>.<product_type>"`. Each entry is a list of
channel names from `publication_channel_vocabulary`.

```json
{
  "<family>.<product_type>": [<channel_name>, ...]
}
```

**12.1** Every `(family, product_type)` pair present in `channel_routing` must match an entry in
the active `catalog_policy.variant_spec`. The publication worker validates this at policy load time.

**12.2** A `(family, product_type)` pair absent from `channel_routing` produces no publication
candidates. The publication worker silently skips variants with unmapped routing.

**12.3** All channel names in `channel_routing` values must be valid entries in
`publication_channel_vocabulary`. The activation trigger validates this — not the worker at runtime.

**12.4** The same channel may appear in multiple routing entries. A `museum_print.museum_giclée`
variant may route to both `museum_retail` and `print_on_demand`.

### Article 13 — `channel_spec` Canonical Structure

`channel_spec` is a JSONB object keyed by channel name. Each entry defines the governance
requirements for generating a `publication_channel_profile` for that channel.

```json
{
  "<channel_name>": {
    "min_image_width_px":     <int>,
    "accepted_image_formats": [<string>, ...],   -- "TIFF" | "JPEG" | "PNG"
    "color_profiles":         [<string>, ...],   -- "sRGB" | "AdobeRGB" | "CMYK"
    "rights_statement_template": "<string with {{placeholders}}>",
    "requires_attribution":   boolean,
    "metadata_fields": {
      "required": [<field_name>, ...],
      "optional": [<field_name>, ...]
    }
  }
}
```

**13.1** `rights_statement_template` is a string that may contain the following placeholders,
resolved at channel profile generation time from `catalog_snapshot`:
- `{{illustrator}}` — from `catalog_snapshot.illustration.illustrator`
- `{{publication_year}}` — from `catalog_snapshot.illustration.publication_year`
- `{{publication_title}}` — from `catalog_snapshot.illustration.publication_title`
- `{{taxon_name}}` — from `catalog_snapshot.illustration.taxon_name`
- `{{rights_status}}` — from `catalog_snapshot.illustration.rights_status`
- `{{source}}` — from `catalog_snapshot.illustration.source`

**13.2** Permitted `metadata_fields.required` values are drawn from the canonical metadata field
vocabulary: `title`, `description`, `tags`, `alt_text`, `attribution`, `provenance_note`,
`educational_level`, `license_terms`. The publication worker must validate that all required fields
can be resolved from `catalog_snapshot` at policy load time. If a required field has no resolvable
source in the snapshot, the activation trigger must block the policy.

**13.3** `channel_spec` must contain an entry for every channel name that appears in any
`channel_routing` value. The activation trigger validates this.

---

## Part V — Entity Schemas

### Article 14 — `publication_candidate` Schema

```
publication_candidate
├── id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── catalog_variant_id         UUID NOT NULL REFERENCES catalog_variant(id)
├── catalog_candidate_id       UUID NOT NULL REFERENCES catalog_candidate(id)
├── publication_policy_id      UUID NOT NULL REFERENCES publication_policy(id)
├── channel                    TEXT NOT NULL REFERENCES publication_channel_vocabulary(value)
├── status                     TEXT NOT NULL DEFAULT 'nominated'
│                                  REFERENCES publication_candidate_status_vocabulary(value)
├── nominated_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── nominated_by               TEXT NOT NULL
├── curator_reviewed_by        TEXT
├── curator_reviewed_at        TIMESTAMPTZ
├── curator_notes              TEXT
├── catalog_snapshot           JSONB NOT NULL             -- Article 18; immutable after write
├── nomination_basis           JSONB NOT NULL             -- Article 14.1
│
├── UNIQUE (catalog_variant_id, channel)
│       WHERE status NOT IN ('rejected','retired','withdrawn')
├── CONSTRAINT chk_pub_candidate_snapshot  CHECK (catalog_snapshot <> '{}'::jsonb)
├── CONSTRAINT chk_pub_candidate_basis     CHECK (nomination_basis <> '{}'::jsonb)
├── CONSTRAINT chk_pub_candidate_review    CHECK (
│       status IN ('nominated','under_review') OR curator_reviewed_by IS NOT NULL
│   )
│
├── provenance                 JSONB NOT NULL DEFAULT '{}'
├── created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Triggers on `publication_candidate`:**

1. **`trg_pub_candidate_snapshot_immutable`** — BEFORE UPDATE: if `OLD.catalog_snapshot` differs
   from `NEW.catalog_snapshot`, raise an exception. The snapshot is written once at nomination.

2. **`trg_pub_candidate_ready_gate`** — BEFORE UPDATE OF status: when `NEW.status = 'ready'`,
   verify that a `publication_channel_profile` with `status = 'ready'` exists for this candidate.
   If not, raise an exception.

**14.1 `nomination_basis` canonical structure:**

```json
{
  "publication_policy_id":      "<UUID>",
  "publication_policy_version": "<semver>",
  "nominated_at":               "<ISO 8601 UTC>",
  "catalog_variant_id":         "<UUID>",
  "channel":                    "<channel_name>",
  "routing_rule_path":          "<family>.<product_type>",
  "gate_checks": {
    "ppg0_catalog_published":   <bool>,
    "ppg1_variant_active":      <bool>,
    "ppg2_pricing_approved":    <bool>,
    "ppg3_hard_gate_passed":    <bool>,
    "ppg4_no_duplicate":        <bool>
  },
  "requires_curator_review":    <bool>,
  "curator_review_reason":      "<string or null>"
}
```

### Article 15 — `publication_channel_profile` Schema

```
publication_channel_profile
├── id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── publication_candidate_id   UUID NOT NULL REFERENCES publication_candidate(id)
├── publication_policy_id      UUID NOT NULL REFERENCES publication_policy(id)
├── channel                    TEXT NOT NULL REFERENCES publication_channel_vocabulary(value)
├── status                     TEXT NOT NULL DEFAULT 'draft'
│                                  REFERENCES publication_channel_profile_status_vocabulary(value)
│
├── metadata                   JSONB NOT NULL             -- Article 15.1
├── image_spec                 JSONB NOT NULL             -- Article 15.2
├── rights_statement           TEXT NOT NULL
├── pricing_export             JSONB NOT NULL             -- Article 15.3
├── channel_basis              JSONB NOT NULL             -- Article 15.4
│
├── authored_by                TEXT NOT NULL
├── reviewed_by                TEXT
├── reviewed_at                TIMESTAMPTZ
│
├── CONSTRAINT chk_pub_channel_profile_metadata    CHECK (metadata <> '{}'::jsonb)
├── CONSTRAINT chk_pub_channel_profile_image_spec  CHECK (image_spec <> '{}'::jsonb)
├── CONSTRAINT chk_pub_channel_profile_rights      CHECK (length(rights_statement) > 0)
├── CONSTRAINT chk_pub_channel_profile_pricing     CHECK (pricing_export <> '{}'::jsonb)
├── CONSTRAINT chk_pub_channel_profile_basis       CHECK (channel_basis <> '{}'::jsonb)
├── CONSTRAINT chk_pub_channel_profile_review      CHECK (
│       reviewed_by IS NULL OR reviewed_by IS DISTINCT FROM authored_by
│   )
│
├── provenance                 JSONB NOT NULL DEFAULT '{}'
├── created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**15.1 `metadata` structure** — all required fields from `channel_spec[channel].metadata_fields.required`
must be present; optional fields may be included if resolved from `catalog_snapshot`:

```json
{
  "title":             "<string>",
  "description":       "<string>",
  "tags":              [<string>, ...],
  "alt_text":          "<string>",
  "attribution":       "<string or null>",
  "provenance_note":   "<string or null>",
  "educational_level": "<string or null>",
  "license_terms":     "<string or null>"
}
```

Fields not required by the channel's `channel_spec` and not resolvable from `catalog_snapshot`
must be omitted. Fields must not be fabricated — all values must derive from `catalog_snapshot`
or the `channel_spec` template. This is the metadata determinism invariant.

**15.2 `image_spec` structure:**

```json
{
  "accepted_formats":    [<string>, ...],
  "min_width_px":        <int>,
  "color_profiles":      [<string>, ...],
  "source_image_width":  <int>,
  "source_meets_spec":   <bool>
}
```

`source_image_width` is read from `catalog_snapshot.image_width_px` at profile generation time.
`source_meets_spec = (source_image_width >= min_width_px)` and must be `true` for the profile to
transition to `ready` (enforced by CPG-3 before profile creation — if CPG-3 fails, no profile
is created at all).

**15.3 `pricing_export` structure:**

```json
{
  "computed_price":    <float>,
  "currency":          "USD",
  "price_tier":        "<PREMIUM|STANDARD|VALUE>",
  "floor_price":       <float or null>,
  "ceiling_price":     <float or null>,
  "source":            "catalog_pricing_profile:<UUID>"
}
```

`computed_price`, `price_tier`, `floor_price`, and `ceiling_price` are read from the linked
`catalog_pricing_profile` at profile generation time and recorded here verbatim. This is the
pricing provenance chain — the publication channel profile records what pricing governed this
nomination, not what the eventual retail price will be.

**15.4 `channel_basis` structure:**

```json
{
  "publication_policy_id":      "<UUID>",
  "publication_policy_version": "<semver>",
  "channel":                    "<channel_name>",
  "drafted_at":                 "<ISO 8601 UTC>",
  "channel_spec_path":          "<channel_name>",
  "rights_template_applied":    "<template string>",
  "metadata_fields_required":   [<field_name>, ...],
  "metadata_fields_resolved":   [<field_name>, ...],
  "image_spec_applied":         { "min_width_px": <int>, "accepted_formats": [...] },
  "pricing_source":             "catalog_pricing_profile:<UUID>"
}
```

### Article 16 — `publication_audit_log` Schema

`publication_audit_log` is append-only. No UPDATE or DELETE is permitted. Enforcement follows the
PostgreSQL RULE pattern established in the Commerce Intelligence Constitution for `score_audit_log`.

```
publication_audit_log
├── id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── publication_candidate_id   UUID NOT NULL REFERENCES publication_candidate(id)
├── publication_policy_id      UUID NOT NULL REFERENCES publication_policy(id)
├── event_type                 TEXT NOT NULL REFERENCES publication_audit_event_type_vocabulary(value)
├── event_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── actor_type                 TEXT NOT NULL              -- "system_worker" | "curator"
├── actor_id                   TEXT NOT NULL
├── actor_notes                TEXT                       -- required when actor_type = 'curator'
├── previous_state             JSONB NOT NULL DEFAULT '{}'
├── new_state                  JSONB NOT NULL DEFAULT '{}'
├── entry_checksum_sha256      TEXT NOT NULL
├── previous_entry_checksum    TEXT
├── reason                     TEXT NOT NULL
├── generated_by               TEXT NOT NULL
├── created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
│
├── CONSTRAINT chk_pub_audit_entry_checksum    CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$')
├── CONSTRAINT chk_pub_audit_previous_checksum CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_pub_audit_distinct_checksum CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
│   )
├── CONSTRAINT chk_pub_audit_actor_id          CHECK (length(actor_id) > 0)
├── CONSTRAINT chk_pub_audit_reason            CHECK (length(reason) > 0)
├── CONSTRAINT chk_pub_audit_generated_by      CHECK (length(generated_by) > 0)
├── CONSTRAINT chk_pub_audit_curator_notes     CHECK (
│       actor_type <> 'curator' OR actor_notes IS NOT NULL
│   )
│
└── UNIQUE (publication_candidate_id, entry_checksum_sha256)
```

Hash chain is per `publication_candidate_id`. D-1 canonical JSON: keys alpha-sorted, null
retained, floats to 6 decimal places. Same algorithm as `score_audit_log` and `catalog_audit_log`.

---

## Part VI — Replayability

### Article 17 — Catalog Snapshot

**17.1** At nomination time, the publication worker captures a snapshot of the governing catalog
entities and writes it to `publication_candidate.catalog_snapshot`. The snapshot is written once
and is immutable thereafter, enforced by `trg_pub_candidate_snapshot_immutable`.

**17.2** The snapshot must include, at minimum:

```json
{
  "catalog_variant": {
    "id":           "<UUID>",
    "variant_key":  "<key>",
    "product_type": "<type>",
    "product_family": "<family>",
    "dimensions":   { "size": "...", "finish": "...", "material": "..." }
  },
  "catalog_pricing_profile": {
    "id":              "<UUID>",
    "computed_price":  <float>,
    "price_tier":      "<tier>",
    "floor_price":     <float or null>,
    "ceiling_price":   <float or null>,
    "markup_multiplier": <float>
  },
  "catalog_candidate": {
    "id":             "<UUID>",
    "product_family": "<family>",
    "catalog_policy_id": "<UUID>"
  },
  "illustration": {
    "title":            "<string>",
    "taxon_name":       "<string>",
    "illustrator":      "<string or null>",
    "publication_year": <int or null>,
    "publication_title": "<string or null>",
    "rights_status":    "<Public Domain|CC0>",
    "source":           "<bhl|loc>",
    "source_record_id": "<string>"
  },
  "commerce_opportunity": {
    "csm_tier":            "<tier>",
    "commerce_tier":       "<tier>",
    "hard_gate_status":    "passed",
    "image_width_px":      <int>,
    "illustrator_prestige": <float>,
    "place_relevance_score": <float>,
    "computed_at":         "<ISO 8601 UTC>"
  }
}
```

**17.3** The `candidate_nominated` audit event must write the same snapshot to `new_state`. The
audit log is the primary record; the snapshot on `publication_candidate` is a query convenience.

### Article 18 — Publication Replayability Invariant

A publication nomination is replayable if, given:
- `publication_candidate.catalog_snapshot`
- The policy loaded by exact `publication_candidate.publication_policy_id`

...the publication worker can re-derive:
1. Which channels the variant routes to (deterministic from `channel_routing`)
2. What `publication_channel_profile` metadata would be generated (deterministic from `channel_spec` applied to snapshot)
3. What rights statement would be produced (deterministic from `rights_statement_template` + snapshot illustration fields)
4. What pricing export would be recorded (deterministic from snapshot `catalog_pricing_profile`)

The publication worker must expose a `replay_nomination(candidate_id)` function that:
1. Loads the candidate by `candidate_id`
2. Loads the policy by exact `publication_candidate.publication_policy_id` — not the active policy
3. Re-derives the expected channel profiles
4. Compares against persisted channel profiles
5. Writes `replay_verified` or `replay_failure` to `publication_audit_log`

Metadata determinism is the key invariant: given the same snapshot and policy, the same metadata
field values must be produced. If the `rights_statement_template` or `metadata_fields` changed
between the original nomination and the replay, the replay will produce different output and must
write `replay_failure`.

---

## Part VII — Human Approval

### Article 19 — Publication Policy Approval

A `publication_policy` may only become `active` if all five conditions hold:

1. `status = 'pending_approval'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM authored_by`
4. `effective_from IS NOT NULL`
5. No other `publication_policy` has `status = 'active'`

The activation trigger must also:
- Set the previously active policy to `superseded` within the same transaction
- Validate all channel names in `channel_routing` values exist in `publication_channel_vocabulary`
- Validate all channel names in `channel_spec` exist in `publication_channel_vocabulary`
- Validate every channel in `channel_routing` has a corresponding entry in `channel_spec`

### Article 20 — Curator Review Rules

**20.1** A publication candidate requires curator review if any of the following hold:
- The channel is listed as `curator_always_required` in Article 7 (`museum_retail`, `institutional`)
- `commerce_opportunities.requires_curator_review = TRUE` (from snapshot)
- `commerce_opportunities.csm_tier = 'MASTERWORK'` (from snapshot)

**20.2** When curator review is required, the publication worker sets
`publication_candidate.status = 'nominated'` and writes `candidate_nominated`. The curator must
explicitly transition through `under_review` before approving.

**20.3** When curator review is not required, the publication worker auto-advances the candidate
using the `nominated → ready` direct transition with `actor_type = 'system_worker'`. Both
`candidate_nominated` and `candidate_ready` audit events are written within the same transaction.

**20.4** The `publication_channel_profile.reviewed_by IS DISTINCT FROM authored_by` constraint
prevents self-review of channel profiles. This applies only when a curator transition sets
`reviewed_by` — the `system_worker` auto-advance path sets `reviewed_by = NULL` (no human
reviewer).

**20.5 Ready gate**: A `publication_candidate` may only transition to `ready` when a
`publication_channel_profile` with `status = 'ready'` exists for this candidate. This gate is
enforced by `trg_pub_candidate_ready_gate` (Article 14).

**20.6 Channel profile ready gate**: A `publication_channel_profile` may only transition to
`ready` when all required metadata fields are present in `metadata` (non-null, non-empty string).
This gate is enforced by a BEFORE UPDATE trigger on `publication_channel_profile.status` that
validates `metadata` against `channel_spec[channel].metadata_fields.required`.

---

## Part VIII — Prohibited Acts

### Article 21 — Prohibited Acts

| Act | Prohibition |
|---|---|
| **PA-1** | No publication nomination without an active `publication_policy` |
| **PA-2** | No hardcoded channel routing — all routing must come from `channel_routing` |
| **PA-3** | No hardcoded channel metadata requirements — all requirements from `channel_spec` |
| **PA-4** | No nomination without clearing all five pre-nomination gates (PPG-0 through PPG-4) |
| **PA-5** | No `catalog_snapshot = '{}'` — snapshot must be fully populated at nomination time |
| **PA-6** | No `nomination_basis = '{}'` or `channel_basis = '{}'` |
| **PA-7** | No `UPDATE` or `DELETE` on `publication_audit_log` rows |
| **PA-8** | No publication_policy activation without second-human approval |
| **PA-9** | No mutation of `channel_routing` or `channel_spec` after policy activation |
| **PA-10** | No self-approval of publication_policy |
| **PA-11** | No `catalog_snapshot` mutation after initial write |
| **PA-12** | No fabricated metadata — all metadata field values must derive from `catalog_snapshot` or `channel_spec` template resolution |
| **PA-13** | No channel profile marked `ready` without all required metadata fields populated |
| **PA-14** | No `publication_candidate` marked `ready` without a `ready` channel profile |
| **PA-15** | No replay that loads the currently active policy — replay must use `publication_candidate.publication_policy_id` |
| **PA-16** | No channel value that references a specific provider, storefront, or external system |
| **PA-17** | No pricing values fabricated in `pricing_export` — all values must be read verbatim from the linked `catalog_pricing_profile` at nomination time |

---

## Part IX — Publication Worker Protocol

### Article 22 — Transaction Scope and Ordering

**22.1 Nomination transaction**: The following operations for a single `publication_candidate` and
its channel profile are wrapped in a single atomic transaction. If any step fails, the transaction
rolls back:

```
BEGIN;
  INSERT publication_candidate (status = 'nominated') → obtain candidate.id
  INSERT publication_audit_log (candidate_nominated, new_state = catalog_snapshot)
  INSERT publication_channel_profile (status = 'draft') → obtain profile.id
  INSERT publication_audit_log (channel_profile_drafted)
  [if curator review not required]:
    UPDATE publication_channel_profile SET status = 'reviewed'
    INSERT publication_audit_log (channel_profile_reviewed, actor_type = 'system_worker')
    UPDATE publication_channel_profile SET status = 'ready'
    INSERT publication_audit_log (channel_profile_ready, actor_type = 'system_worker')
    UPDATE publication_candidate SET status = 'ready'
    INSERT publication_audit_log (candidate_ready, actor_type = 'system_worker')
COMMIT;
```

**22.2 Policy load and validation**: At startup, the publication worker must:
1. Load the active `publication_policy`
2. Validate all channels in `channel_routing` values exist in `publication_channel_vocabulary`
3. Validate all channels in `channel_spec` have corresponding `channel_routing` entries
4. Validate `rights_statement_template` contains only permitted `{{placeholders}}`
5. Validate all `metadata_fields.required` values can be resolved from the expected snapshot schema
6. Halt immediately if any validation fails — process no candidates

**22.3 Metadata resolution**: The publication worker resolves metadata fields from
`catalog_snapshot.illustration.*` at profile generation time. The resolution is deterministic:
the same snapshot plus the same `channel_spec` always produces the same metadata. No external
lookups. No API calls. No inference beyond what is in the snapshot and the policy.

**22.4 No re-scoring**: The publication worker reads all scores, tiers, and gate statuses from
`catalog_snapshot`. It does not call any upstream worker or re-evaluate any upstream gate.

**22.5 No provider calls**: The publication worker is a DB-only operation.

---

## Part X — Migration Sequence

### Article 23 — Required Migrations

| Migration | Contents | Depends On |
|---|---|---|
| M-29 | Five vocabulary tables + seed values: `publication_policy_status_vocabulary`, `publication_candidate_status_vocabulary`, `publication_channel_profile_status_vocabulary`, `publication_channel_vocabulary`, `publication_audit_event_type_vocabulary`. `publication_policy` table, immutability trigger, activation trigger (supersession cascade + channel validation). UNIQUE partial index on active status. | M-27 (`catalog_variant`, `catalog_candidate` tables must exist for FK from M-30) |
| M-30 | `publication_candidate` table + constraints + `trg_pub_candidate_snapshot_immutable` + `trg_pub_candidate_ready_gate`. `publication_channel_profile` table + constraints + `trg_pub_channel_profile_ready_gate`. `publication_audit_log` table + constraints + append-only RULE. All indexes. | M-29 |
| M-31 | Seed `publication_policy` v1.0.0 in `draft` status with `channel_routing` and `channel_spec` for all five governed channels. | M-30 |

### Article 24 — Seed Policy Specification

The M-31 seed populates `publication_policy` v1.0.0 with:

**channel_routing defaults:**

| Family.Product Type | Channels |
|---|---|
| `wall_art.print_premium` | `print_on_demand`, `digital_download` |
| `wall_art.print_standard` | `print_on_demand` |
| `wall_art.canvas` | `print_on_demand` |
| `museum_print.museum_giclée` | `museum_retail`, `print_on_demand` |
| `calendar.wall_calendar` | `print_on_demand` |
| `book.book_interior` | `digital_download` |
| `puzzle.puzzle_1000` | `print_on_demand` |
| `card.greeting_card` | `print_on_demand` |
| `educational.classroom_poster` | `educational`, `digital_download` |
| `institutional_license.digital_license` | `institutional` |
| `home_decor.decorative_print` | `print_on_demand` |

**channel_spec defaults:**

| Channel | Min Width px | Formats | Color | Curator | Required Metadata |
|---|---|---|---|---|---|
| `print_on_demand` | 3000 | TIFF, JPEG | sRGB | false | title, description, tags, alt_text |
| `digital_download` | 2400 | JPEG, PNG | sRGB | false | title, description, tags |
| `museum_retail` | 4000 | TIFF | AdobeRGB | **true** | title, description, attribution, provenance_note |
| `educational` | 2400 | JPEG, PNG | sRGB | false | title, description, educational_level |
| `institutional` | 3000 | TIFF | AdobeRGB | **true** | title, description, attribution, license_terms |

**rights_statement_template defaults:**

| Channel | Template |
|---|---|
| `print_on_demand` | `{{rights_status}} illustration by {{illustrator}} ({{publication_year}}). Source: {{source}}.` |
| `digital_download` | `{{rights_status}}. Original source: {{source}}, record {{source_record_id}}.` |
| `museum_retail` | `{{rights_status}}. {{illustrator}}, {{publication_year}}. From {{publication_title}}. {{source_record_id}}.` |
| `educational` | `Public domain illustration. Free for educational use. Source: {{source}}.` |
| `institutional` | `{{rights_status}} illustration. Institutional licensing. Source: {{source}}, record {{source_record_id}}.` |

---

## Part XI — Ratification

This Constitution is a draft. It becomes authoritative upon ratification by the Principal
Architect. Ratification is recorded by updating the status field at the top of this document to
`Ratified` and setting the ratification date.

Implementation of Migrations M-29, M-30, and M-31 is not authorized until ratification.

Implementation of the `publication_worker` is not authorized until M-29 through M-31 are applied
and the v1.0.0 seed policy transitions to `active` through the constitutional activation protocol
(second-human approval required).
