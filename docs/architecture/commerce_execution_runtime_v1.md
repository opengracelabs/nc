# Commerce Execution Runtime v1

## Mission

Design the Commerce Execution Runtime for Nature & Culture using the Commerce
Execution Constitution v1.0.

This document is architecture only. It does not implement migrations, workers,
routers, tests, external integrations, or provider execution.

## Scope Boundary

Commerce Execution is downstream of Provider Routing.

```text
commerce_opportunities
  -> product_recommendations
  -> catalog_candidates
  -> catalog_variants
  -> publication_candidates
  -> provider_route_candidates
  -> execution_candidates
  -> execution_records
```

This runtime answers:

> Is this approved provider route human-authorized for a governed commerce action,
> and what exact immutable payload would be used?

This phase does not answer:

> Did we submit the payload to an external system?

Not allowed in this design:

- No APIs.
- No Shopify.
- No fulfillment execution.
- No external submission.
- No order creation.
- No product creation in a provider system.
- No webhook handling.
- No confirmation cascade from external state.

The runtime may prepare governed execution records. It may not execute them.

The terminal output of this design is:

```text
execution_records.status = 'prepared'
submitted_at IS NULL
confirmed_at IS NULL
```

Any handoff from a prepared record to an external submission system is a future
runtime and is not part of Commerce Execution Runtime v1.

## Constitutional Basis

The Commerce Execution Constitution defines five governed entities:

- `execution_policy`
- `execution_candidate`
- `execution_record`
- `execution_audit_log`
- `execution_replay`

This runtime design uses the requested public names:

- `execution_policy`
- `execution_candidates`
- `execution_records`
- `execution_worker`
- `execution_replay_worker`

Implementation should either use plural table names consistently or preserve the
Constitution's singular entity names through views/aliases. The authority and
semantics are constitutional regardless of table naming.

Although the Constitution describes later `submitted`, `confirmed`, rollback,
and success cascade states, this design intentionally implements only the
constitutionally governed preparation boundary. Those later states remain
reserved vocabulary; no worker in this design may enter them.

## Design Principles

1. PostgreSQL is authoritative for all execution state.
2. Replay is required before execution readiness can be trusted.
3. Every candidate has immutable route snapshot, execution payload, and
   idempotency key.
4. No system worker may approve an execution candidate.
5. No execution record can be prepared without a human-approved candidate.
6. No external API is called by the governed worker.
7. No fulfillment execution occurs in v1.
8. Append-only audit is mandatory.
9. Replay must load the candidate's pinned policy, not the active policy.
10. Prepared payload construction must be policy-driven, not hardcoded.

## Runtime Tables

### execution_policy

`execution_policy` is the machine-readable authority for deriving execution
payloads, idempotency keys, retry limits, and rollback policy.

Recommended schema:

```sql
CREATE TABLE execution_policy (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version               TEXT NOT NULL UNIQUE,
    status                TEXT NOT NULL REFERENCES execution_policy_status_vocabulary(value),
    effective_from        TIMESTAMPTZ,
    effective_until       TIMESTAMPTZ,
    authored_by           TEXT NOT NULL,
    approved_by           TEXT,
    approved_at           TIMESTAMPTZ,
    changelog             TEXT NOT NULL,
    previous_version_id   UUID REFERENCES execution_policy(id),

    execution_rules       JSONB NOT NULL,

    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Governance:

- Only one active policy.
- Active policy requires second-human approval.
- `execution_rules` immutable once status is `active`, `paused`, or
  `superseded`.
- `status = 'paused'` blocks creation of new `execution_records`.
- Activation validates every action type, every idempotency path, and every
  payload path.
- Activation must fail if `execution_rules` contains provider endpoint URLs,
  API credentials, webhook metadata, external provider IDs, or channel-specific
  submission directives.

Execution rule shape:

```json
{
  "create_listing": {
    "requires_human_approval": true,
    "max_retries": 1,
    "retry_delay_seconds": 0,
    "rollback_on_failure": false,
    "idempotency_key_fields": [
      "provider_route_candidate.id",
      "catalog_variant.id",
      "provider_capability_profile.provider_key",
      "action_type"
    ],
    "payload_spec": {
      "action_type": "action_type",
      "provider_key": "provider_capability_profile.provider_key",
      "publication_candidate_id": "publication_candidate.id",
      "catalog_candidate_id": "catalog_candidate.id",
      "catalog_variant_id": "catalog_variant.id",
      "product_family": "catalog_variant.product_family",
      "product_type": "catalog_variant.product_type",
      "variant_key": "catalog_variant.variant_key",
      "title": "catalog_candidate.catalog_title",
      "price_snapshot": "catalog_variant.price_snapshot",
      "rights_snapshot": "catalog_candidate.rights_snapshot"
    }
  }
}
```

In this phase, `create_listing` means "prepare an internal execution payload for
a future listing-like action." It does not create a Shopify listing, provider
product, or fulfillment order.

Allowed seed action coverage:

```text
create_listing: prepare-only
update_listing: vocabulary-reserved, no seed rule required
retire_listing: vocabulary-reserved, no seed rule required
```

### execution_candidates

`execution_candidates` are human-authorization records for one approved provider
route candidate.

Recommended schema:

```sql
CREATE TABLE execution_candidates (
    id                           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider_route_candidate_id  UUID NOT NULL REFERENCES provider_route_candidates(id),
    publication_candidate_id     UUID NOT NULL REFERENCES publication_candidates(id),
    execution_policy_id          UUID NOT NULL REFERENCES execution_policy(id),
    action_type                  TEXT NOT NULL REFERENCES execution_action_type_vocabulary(value),
    status                       TEXT NOT NULL DEFAULT 'pending'
                                    REFERENCES execution_candidate_status_vocabulary(value),

    idempotency_key              TEXT NOT NULL,
    route_snapshot               JSONB NOT NULL,
    execution_payload            JSONB NOT NULL,

    pending_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    approved_at                  TIMESTAMPTZ,
    approved_by                  TEXT,
    approved_notes               TEXT,
    curator_reviewed_by          TEXT,
    curator_reviewed_at          TIMESTAMPTZ,

    provenance                   JSONB NOT NULL DEFAULT '{}',
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (provider_route_candidate_id, action_type),
    CONSTRAINT chk_execution_candidate_snapshot CHECK (route_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_execution_candidate_payload CHECK (execution_payload <> '{}'::jsonb),
    CONSTRAINT chk_execution_candidate_idempotency CHECK (idempotency_key ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_execution_candidate_approval CHECK (
        status IN ('pending','rejected','withdrawn')
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)
    )
);
```

Immutable fields:

- `route_snapshot`
- `execution_payload`
- `idempotency_key`

Required parent gate:

```text
provider_route_candidates.route_status IN ('approved_for_execution', 'approved_for_planning')
provider_route_candidates.route_decision = 'recommend'
provider_route_candidates.curator_decision = 'approved'
provider_route_candidates.staleness_status = 'current'
publication_candidates.staleness_status = 'current'
```

If this gate fails, the worker must not create an execution candidate.

Compatibility note: the Execution Constitution uses the canonical phrase
`provider_route_candidate.status = 'approved'`. The current provider-routing
runtime uses route-specific fields. For v1, `approved_for_planning` is only
eligible when paired with explicit curator approval; a future migration may
normalize this as `approved_for_execution`.

### execution_records

`execution_records` represent governed preparation attempts. In this no-execution
phase, records stop at `prepared`.

Recommended schema:

```sql
CREATE TABLE execution_records (
    id                       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_candidate_id   UUID NOT NULL REFERENCES execution_candidates(id),
    execution_policy_id      UUID NOT NULL REFERENCES execution_policy(id),
    action_type              TEXT NOT NULL REFERENCES execution_action_type_vocabulary(value),
    attempt_number           INT NOT NULL,
    status                   TEXT NOT NULL DEFAULT 'prepared'
                               REFERENCES execution_record_status_vocabulary(value),

    idempotency_key          TEXT NOT NULL,
    prepared_payload         JSONB NOT NULL,
    rollback_payload         JSONB,
    is_rollback              BOOLEAN NOT NULL DEFAULT FALSE,

    prepared_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    submitted_at             TIMESTAMPTZ,
    confirmed_at             TIMESTAMPTZ,
    failed_at                TIMESTAMPTZ,
    failure_reason           TEXT,
    outcome_detail           JSONB NOT NULL DEFAULT '{}',

    provenance               JSONB NOT NULL DEFAULT '{}',
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (execution_candidate_id, attempt_number),
    CONSTRAINT chk_execution_record_payload CHECK (prepared_payload <> '{}'::jsonb),
    CONSTRAINT chk_execution_record_idempotency CHECK (idempotency_key ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_execution_record_attempt CHECK (attempt_number >= 1),
    CONSTRAINT chk_execution_record_no_submission CHECK (
        submitted_at IS NULL AND confirmed_at IS NULL
    )
);
```

For this design phase:

- Valid created status is `prepared` only.
- `submitted_at` remains null.
- `confirmed_at` remains null.
- No `external_reference` field is used.
- No fulfillment, listing, or provider state is written.
- No worker may mutate a prepared record into `submitted`, `confirmed`,
  `failed`, or `rolled_back`.

The Constitution includes later submitted/confirmed/cascade semantics. Those are
explicitly out of scope here.

### execution_audit_log

`execution_audit_log` is append-only and hash-chained per execution candidate.

Required events:

- `candidate_pending`
- `candidate_approved`
- `candidate_rejected`
- `candidate_withdrawn`
- `policy_validated`
- `record_prepared`
- `idempotency_collision`
- `replay_verified`
- `replay_failure`

Recommended schema:

```sql
CREATE TABLE execution_audit_log (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_candidate_id     UUID NOT NULL REFERENCES execution_candidates(id),
    execution_policy_id        UUID NOT NULL REFERENCES execution_policy(id),
    execution_record_id        UUID REFERENCES execution_records(id),
    event_type                 TEXT NOT NULL REFERENCES execution_audit_event_type_vocabulary(value),
    event_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_type                 TEXT NOT NULL REFERENCES commerce_actor_type_vocabulary(value),
    actor_id                   TEXT NOT NULL,
    actor_notes                TEXT,
    previous_state             JSONB NOT NULL DEFAULT '{}',
    new_state                  JSONB NOT NULL DEFAULT '{}',
    entry_checksum_sha256      TEXT NOT NULL,
    previous_entry_checksum    TEXT,
    reason                     TEXT NOT NULL,
    generated_by               TEXT NOT NULL,
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Rules:

- No UPDATE.
- No DELETE.
- Checksum is canonical JSON SHA-256.
- `previous_entry_checksum` must match latest audit entry for the candidate.
- Curator actor events require notes.

### execution_replay

`execution_replay` is a first-class deterministic verification record.

Recommended schema:

```sql
CREATE TABLE execution_replay (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_candidate_id     UUID NOT NULL REFERENCES execution_candidates(id),
    execution_record_id        UUID REFERENCES execution_records(id),
    execution_policy_id        UUID NOT NULL REFERENCES execution_policy(id),
    replayed_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    replayed_by                TEXT NOT NULL,

    outcome                    TEXT NOT NULL,
    snapshot_used              JSONB NOT NULL,
    payload_derived            JSONB NOT NULL,
    payload_recorded           JSONB NOT NULL,
    idempotency_key_derived    TEXT NOT NULL,
    idempotency_key_recorded   TEXT NOT NULL,
    divergence_details         TEXT,

    entry_checksum_sha256      TEXT NOT NULL,
    previous_entry_checksum    TEXT,
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Replay outcomes:

- `payload_match`
- `payload_diverge`
- `idempotency_key_match`
- `idempotency_key_diverge`
- `snapshot_integrity_failure`

A successful replay writes both:

1. `execution_replay` row
2. `execution_audit_log` event with `event_type = 'replay_verified'`

A failed replay writes:

1. `execution_replay` row
2. `execution_audit_log` event with `event_type = 'replay_failure'`

## Worker Design

### execution_worker

The execution worker has two responsibilities in this phase:

1. Create pending execution candidates from approved provider routes.
2. Prepare internal execution records for human-approved execution candidates.

It does not submit anything.

The worker must not import provider SDKs, instantiate HTTP clients, read provider
API credentials, or derive provider-specific transport envelopes. Its only
observable side effects are PostgreSQL writes.

#### Candidate Creation Flow

```text
load active execution_policy
claim approved provider_route_candidates
build full route_snapshot
resolve execution_payload from execution_policy.execution_rules[action_type].payload_spec
derive idempotency_key from execution_policy.execution_rules[action_type].idempotency_key_fields
insert execution_candidate with status = pending
insert execution_audit_log candidate_pending
```

The route snapshot must include:

- provider route candidate
- provider capability profile
- publication candidate
- catalog candidate
- catalog variant
- product recommendation
- commerce opportunity
- policy IDs and versions for each upstream layer
- worker version
- matched_by / approved_by fields needed for self-approval checks

#### Record Preparation Flow

```text
load active execution_policy
claim execution_candidates where status = approved
verify execution_policy.status = active
verify action_type has execution_rules entry
verify no confirmed execution_record exists for candidate
verify no other confirmed execution_record has same idempotency_key
verify attempt_count < max_retries
update execution_candidate.status = executing
insert execution_audit_log candidate_executing
insert execution_record with status = prepared
insert execution_audit_log record_prepared
```

Because this design forbids fulfillment execution, the worker stops here.

No `record_submitted` event is emitted.
No `record_confirmed` event is emitted.
No cascade is applied.
No external identifier is recorded.

### execution_replay_worker

The replay worker verifies deterministic payload derivation.

Replay flow:

```text
load execution_candidate by id
load execution_policy by execution_candidate.execution_policy_id
re-derive execution_payload from route_snapshot + payload_spec
re-derive idempotency_key from route_snapshot + idempotency_key_fields
compare derived payload to execution_candidate.execution_payload
compare derived key to execution_candidate.idempotency_key
insert execution_replay
insert execution_audit_log replay_verified or replay_failure
```

Replay must never load the current active policy unless it is the candidate's
pinned policy. This is a constitutional requirement.

## Gate Enforcement

### Candidate Gate

Before creating `execution_candidates`:

```text
XG-0: approved provider route candidate exists
XG-0a: route_decision = 'recommend'
XG-0b: curator_decision = 'approved'
XG-0c: route_status IN ('approved_for_execution', 'approved_for_planning')
XG-0d: provider_route_candidate.staleness_status = 'current'
XG-0e: publication_candidate.staleness_status = 'current'
```

`approved_for_planning` is accepted only as a compatibility status when
`curator_decision = 'approved'`. It must not be treated as execution
authorization by itself.

Failure behavior:

- Do not create execution candidate.
- Write audit only if a candidate already exists; otherwise log to worker metrics.

### Record Gate

Before creating `execution_records`:

```text
XG-1: execution_candidate.status = 'approved'
XG-2: execution_policy.status = 'active'
XG-3: execution_rules contains action_type
XG-4: no confirmed execution_record for this execution_candidate_id
XG-5: no other confirmed execution_record has same idempotency_key
XG-6: attempt_count < max_retries
```

In this no-execution design, XG-4 and XG-5 normally see no confirmed records,
because confirmation is out of scope. They must still exist for forward
compatibility and replay safety.

## Idempotency Design

The idempotency key is derived from policy-defined snapshot paths.

Example source values:

```text
provider_route_candidate.id
provider_capability_profile.provider_key
publication_candidate.id
catalog_variant.id
action_type
```

Algorithm:

1. Resolve each configured path from `route_snapshot`.
2. Serialize values with canonical JSON.
3. Join values with `|`.
4. SHA-256 hash.
5. Store lowercase 64-character hex string.

The key is stored on both `execution_candidates` and `execution_records`.

## Payload Design

The execution payload is derived entirely from `payload_spec`.

Example payload:

```json
{
  "action_type": "create_listing",
  "provider_key": "gelato_print_network",
  "publication_candidate_id": "...",
  "catalog_candidate_id": "...",
  "catalog_variant_id": "...",
  "product_family": "wall_art",
  "product_type": "standard_print",
  "variant_key": "standard_print_12x16",
  "title": "Moran Survey Plate - Wall Art",
  "price_snapshot": {"currency": "USD", "final_price_cents": 3699},
  "rights_snapshot": {"rights_confidence": 1.0, "hard_gate_status": "passed"}
}
```

This payload is an internal governed payload. It is not submitted.

## Staleness Handling

An execution candidate becomes stale or must be withdrawn when:

- provider route candidate becomes stale, blocked, retired, or superseded
- publication candidate becomes stale or blocked
- catalog variant changes price snapshot
- catalog candidate rights snapshot changes
- execution policy is paused before record preparation
- execution policy is superseded before candidate approval

Recommended handling:

```text
pending -> withdrawn, reason = upstream_stale
approved -> withdrawn if no execution_record exists
executing -> no automatic withdrawal; record state governs
```

No prepared record should be mutated. A new route requires a new execution
candidate and new idempotency key.

## API Design

No API surface is part of this design.

Do not implement:

```text
FastAPI routers
external submission APIs
provider API clients
POST /execution/records/{id}/submit
POST /execution/records/{id}/confirm
POST /execution/fulfillment/*
POST /execution/shopify/*
```

Governance actions such as approval, rejection, withdrawal, and replay may be
performed in future through internal tooling, direct administrative workflows, or
routers. This document does not design those APIs.

## Replay Tests

Required implementation tests:

1. Approved provider route creates pending execution candidate.
2. Non-approved provider route cannot create execution candidate.
3. Human-approved execution candidate creates prepared execution record.
4. No execution record can be created from pending candidate.
5. Prepared payload is immutable.
6. Route snapshot is immutable.
7. Idempotency key is deterministic.
8. Duplicate confirmed idempotency key suppresses record preparation.
9. Paused execution policy blocks record preparation.
10. Replay reproduces payload and idempotency key.
11. Replay uses pinned policy, not active policy.
12. Audit chain is append-only.
13. No APIs, Shopify, fulfillment, external IDs, submitted state, or confirmed
    execution state exists.

## Runtime Sequence

```text
provider_route_candidate approved_for_planning
  -> execution_worker builds route_snapshot
  -> execution_worker derives execution_payload
  -> execution_worker derives idempotency_key
  -> execution_candidate pending
  -> curator approves execution_candidate
  -> execution_worker verifies XG-1..XG-6
  -> execution_record prepared
  -> stop
```

The runtime stops at `execution_record.status = 'prepared'`.

## Open Boundary for Future Phases

Future execution phases may design external submission, confirmation, rollback,
and cascade behavior. Those phases must be separate from this runtime and must
not weaken the immutable candidate, payload, idempotency, replay, or audit
requirements defined here.

## Summary

Commerce Execution Runtime v1 converts an approved provider route into a
human-authorized, immutable, replayable execution candidate and then into an
idempotency-keyed prepared execution record.

It is PostgreSQL-authoritative and replay-first. It does not call APIs, does not
use Shopify, and does not execute fulfillment.
