# Commerce Execution Constitution v1.0

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

This Constitution governs the execution layer of Nature & Culture. It answers one question:

> How does an approved provider route become an executable commerce action?

The answer is: through a machine-readable execution policy, mandatory human authorization of each
candidate, an idempotency-keyed execution record, and a governed cascade that propagates confirmed
outcomes back to all upstream layers. Execution is the first and only layer in the constitutional
chain that authorizes real state change. Every prior layer produces governed records. This layer
produces governed action.

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity Doctrine,
the Commerce Intelligence Constitution v1.1, the Product Routing Constitution v1.1, the Catalog
Constitution v1.1, the Publication Constitution v1.1, and the Provider Routing Constitution v1.0.
Any provision that conflicts with those documents is void.

Prior layers answer: "is this item constitutionally ready?" This layer answers: "is this platform
authorized to act, and what exactly will it do?" These questions have different governance
requirements. Constitutional readiness and execution authorization are distinct. An item can be
constitutionally ready (provider route approved) without being execution-authorized. The execution
policy and human approval of each candidate are the additional authorizations required.

Three properties are non-negotiable at this layer:

**Idempotency.** No external state change may be attempted more than once for the same governed
intent. The execution system must be able to detect and suppress duplicate attempts regardless of
whether the first attempt succeeded or failed.

**Immutability of intent.** The payload that will be submitted — or that was submitted — must be
recorded before the action is taken and must be immutable thereafter. What was authorized to be
submitted and what was submitted must be the same record.

**Rollback governance.** Every action that can be taken must have a governed rollback path. The
rollback conditions, the rollback payload, and the rollback outcome are all governed records.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration commerce platform.

**1.2** An `execution_candidate` is the governed declaration that a specific
`provider_route_candidate` has been human-authorized for execution. It holds the complete
accumulated provenance chain from illustration to provider route as an immutable snapshot, a
derived and immutable execution payload, and a derived idempotency key.

**1.3** An `execution_record` is the governed record of a single execution attempt — original or
retry. It is distinct from the `execution_candidate`: the candidate is the authorization; the
record is the action. One candidate may have multiple records (one per attempt). Each record's
prepared payload is immutable after creation.

**1.4** An `execution_replay` is the governed record of a determinism audit: given the same
immutable snapshot and the same execution policy, does the system re-derive the same payload as
was originally prepared? Replay does not execute. It compares. Its outcome is itself an
immutable, integrity-verified record.

**1.5** The `execution_audit_log` is the append-only, hash-chained event record for all state
transitions across `execution_candidate`, `execution_record`, and `execution_replay`.

**1.6** No external system is contacted by any definition, schema, constraint, trigger, or worker
protocol in this Constitution. Provider API calls, HTTP requests, and external submissions are
downstream of this Constitution. The execution worker's governed output is an authorized,
immutable, idempotency-keyed `execution_record`. What happens with that record is out of scope
for v1.0.

### Article 2 — Scope

This Constitution governs exactly five entities:

| Entity | Role |
|---|---|
| `execution_policy` | Machine-readable authority for all execution decisions |
| `execution_candidate` | Human-authorized intent to execute for one provider route |
| `execution_record` | Governed record of a single execution attempt (original or retry) |
| `execution_audit_log` | Append-only, hash-chained event record for all execution transitions |
| `execution_replay` | Governed determinism audit record |

### Article 3 — Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Commerce Intelligence Constitution v1.1
            └─ Product Routing Constitution v1.1
                 └─ Catalog Constitution v1.1
                      └─ Publication Constitution v1.1
                           └─ Provider Routing Constitution v1.0
                                └─ Commerce Execution Constitution v1.0  ← this document
                                     └─ execution_policy (active record)
                                          └─ execution_worker
```

---

## Part II — Vocabulary

### Article 4 — Execution Policy Status Vocabulary

`execution_policy_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `draft` | Being authored. No execution work permitted. |
| `pending_approval` | Awaiting second-human approval. No execution work permitted. |
| `active` | Authoritative. Execution worker operates under this policy. Only one `active` at any time. |
| `paused` | All new executions suspended. Existing approved candidates may not proceed. |
| `superseded` | Replaced by a newer version. Existing records remain valid. |
| `retired` | Permanently withdrawn. No new records may reference this policy. |

Transitions: `draft → pending_approval → active ⇄ paused → superseded → retired`.
Only `active ⇄ paused` is reversible.

A `paused` policy blocks new execution_record creation, even for already-approved candidates.
This is the emergency stop mechanism. A candidate approved under an `active` policy does not
inherit execution authorization if that policy is subsequently paused.

### Article 5 — Execution Candidate Status Vocabulary

`execution_candidate_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `pending` | Created from an approved provider_route_candidate. Awaiting human authorization. |
| `approved` | Human-authorized. Ready for execution worker. |
| `executing` | Execution worker has begun. At least one execution_record exists. |
| `succeeded` | An execution_record was confirmed. Terminal cascade applied. |
| `failed` | All retry attempts exhausted. No confirmed execution_record. |
| `rolled_back` | Rollback execution completed. Terminal state. |
| `rejected` | Human rejected before execution. Terminal state. |
| `withdrawn` | Withdrawn before execution. Terminal state. |

Valid transitions:

```
pending → approved → executing → succeeded → retired
                              → failed → rolled_back
       → rejected
       → withdrawn (from pending or approved only)
```

`approved → withdrawn` is permitted before the execution worker begins. Once `executing`, the
candidate may not be withdrawn — the execution_record is the governing record of in-flight state.

The `executing → succeeded` transition requires a confirmed `execution_record` with
`status = 'confirmed'`. It is enforced by `trg_exc_candidate_success_gate`. The `executing →
failed` transition requires that `execution_records` for this candidate have exhausted the
`max_retries` limit defined in `execution_policy.execution_rules[action_type]`.

### Article 6 — Execution Record Status Vocabulary

`execution_record_status_vocabulary` contains exactly these values:

| Value | Meaning |
|---|---|
| `prepared` | Payload derived and recorded. Not yet submitted. |
| `submitted` | Submitted to external system. Awaiting confirmation. |
| `confirmed` | External system confirmed receipt. Triggers candidate success cascade. |
| `failed` | Attempt failed. Candidate may retry if within `max_retries`. |
| `rolled_back` | Rollback of this record completed. |

Valid transitions:

```
prepared → submitted → confirmed
                    → failed → rolled_back
prepared → failed   [payload preparation completed but pre-submission check failed]
```

In v1.0, the `submitted → confirmed` transition is set by a curator who confirms external
submission, or by a future submission worker. `prepared` is the terminal governance output for
the execution layer in v1.0.

### Article 7 — Execution Action Type Vocabulary

`execution_action_type_vocabulary` contains exactly these values:

| Value | Description | Reversible |
|---|---|---|
| `create_listing` | Create a new product listing with a provider | Yes — via `retire_listing` |
| `update_listing` | Update metadata or pricing of an existing listing | Yes — via `update_listing` with prior state |
| `retire_listing` | Remove a listing from a provider | No — terminal action |

`retire_listing` is a terminal action. A `rolled_back` record for a `retire_listing` execution
requires a new `create_listing` execution candidate — it cannot be restored in place. This
constraint is enforced by Article 24 (rollback gate RBG-2).

In v1.0, only `create_listing` is covered by the seed execution_policy. `update_listing` and
`retire_listing` require explicit `execution_rules` entries before the execution worker may
process them.

### Article 8 — Execution Audit Event Type Vocabulary

`execution_audit_event_type_vocabulary` contains exactly these values:

| Value | Level | Meaning |
|---|---|---|
| `candidate_pending` | Candidate | Execution candidate created |
| `candidate_approved` | Candidate | Human authorized execution |
| `candidate_rejected` | Candidate | Human rejected execution |
| `candidate_withdrawn` | Candidate | Candidate withdrawn |
| `candidate_executing` | Candidate | Execution worker began |
| `candidate_succeeded` | Candidate | Execution confirmed; cascade applied |
| `candidate_failed` | Candidate | All retries exhausted |
| `candidate_rolled_back` | Candidate | Rollback completed |
| `record_prepared` | Record | Execution record created with immutable payload |
| `record_submitted` | Record | Record submitted to external system |
| `record_confirmed` | Record | External system confirmed |
| `record_failed` | Record | Attempt failed |
| `record_rolled_back` | Record | Record rollback completed |
| `replay_verified` | Replay | Replay produced identical payload |
| `replay_failure` | Replay | Replay diverged — payload or state inconsistency |
| `cascade_applied` | Candidate | Upstream status updates applied on success |
| `idempotency_collision` | Candidate | Duplicate idempotency key detected — execution suppressed |
| `retry_authorized` | Candidate | Retry within policy limit; new execution_record prepared |
| `rollback_triggered` | Candidate | Rollback conditions met; rollback record prepared |

---

## Part III — Execution Gates

### Article 9 — Pre-Execution Gates (XG)

Before preparing an `execution_record`, the execution worker must evaluate seven gates. All gates
are candidate-level. Gate failure suppresses the execution attempt and is recorded in
`execution_audit_log`.

| Gate | Condition | Failure Behavior |
|---|---|---|
| **XG-0** | `provider_route_candidate.status = 'approved'` | Do not create execution_candidate |
| **XG-1** | `execution_candidate.status = 'approved'` | Do not create execution_record |
| **XG-2** | Active `execution_policy` exists and `status = 'active'` (not `paused`) | Do not create record; log `policy_validated` |
| **XG-3** | `execution_policy.execution_rules` contains an entry for `action_type` | Do not create record; log `policy_validated` |
| **XG-4** | No existing `execution_record` for this `execution_candidate_id` with `status = 'confirmed'` | Suppress; log `idempotency_collision`; mark candidate `succeeded` if not already |
| **XG-5** | `idempotency_key` not present in any other `execution_record` with `status = 'confirmed'` | Suppress; log `idempotency_collision` — another candidate has already executed this intent |
| **XG-6** | `attempt_count(execution_candidate_id) < execution_policy.execution_rules[action_type].max_retries` | Do not create record; transition candidate to `failed` |

XG-0 is evaluated before creating `execution_candidate`. XG-1 through XG-6 are evaluated before
creating each `execution_record`.

**9.1** XG-4 and XG-5 are the idempotency gates. They are evaluated in order. XG-4 detects
intra-candidate duplicates (the same candidate was already confirmed). XG-5 detects
inter-candidate duplicates (a different candidate for the same real-world intent was already
confirmed). Both are constitutionally blocking.

**9.2** XG-5 cross-candidate idempotency collision requires human review before any action is
taken. The execution worker must log `idempotency_collision`, halt processing for this candidate,
and set the candidate status to `pending` (escalation hold) until a curator resolves the
collision. This is not a failure — it is an integrity checkpoint.

### Article 10 — Rollback Gates (RBG)

Before preparing a rollback `execution_record`, the execution worker must evaluate three gates.

| Gate | Condition | Failure Behavior |
|---|---|---|
| **RBG-0** | `execution_candidate.status = 'failed'` | Do not initiate rollback |
| **RBG-1** | `execution_policy.execution_rules[action_type].rollback_on_failure = true` | Do not initiate rollback; candidate remains `failed` |
| **RBG-2** | `action_type != 'retire_listing'` | Do not initiate rollback; log error — `retire_listing` has no constitutional rollback path in v1.0 |

If all three gates pass, the execution worker prepares a rollback `execution_record` with
`action_type = 'rollback_<original_action_type>'`. Rollback records are governed by the same
immutability and idempotency rules as original records.

---

## Part IV — Policy Schema

### Article 11 — `execution_policy` Schema

```
execution_policy
├── id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── version                 TEXT NOT NULL UNIQUE
├── status                  TEXT NOT NULL DEFAULT 'draft'
│                               FK → execution_policy_status_vocabulary
├── effective_from          TIMESTAMPTZ
├── effective_until         TIMESTAMPTZ
├── authored_by             TEXT NOT NULL
├── approved_by             TEXT
├── approved_at             TIMESTAMPTZ
├── changelog               TEXT NOT NULL
├── previous_version_id     UUID FK → execution_policy(id)
│
├── execution_rules         JSONB NOT NULL     -- Article 12
│
├── provenance              JSONB NOT NULL DEFAULT '{}'
├── created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Constraints:**
- `approved_by IS DISTINCT FROM authored_by`
- `status NOT IN ('active','paused','superseded') OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)`
- `UNIQUE partial index WHERE status = 'active'`
- `execution_rules` immutable once `status IN ('active','paused','superseded')`
- `version` and `authored_by` immutable once `status IN ('active','paused','superseded')`
- Activation trigger sets previously active policy to `superseded` within the same transaction

### Article 12 — `execution_rules` Canonical Structure

`execution_rules` is a JSONB object keyed by `action_type`. Each entry governs one class of
execution action.

```json
{
  "<action_type>": {
    "requires_human_approval":  true,
    "max_retries":              <int>,
    "retry_delay_seconds":      <int>,
    "rollback_on_failure":      <bool>,
    "idempotency_key_fields":   [<snapshot_path>, ...],
    "payload_spec":             { "<payload_field>": "<snapshot_path>" }
  }
}
```

**12.1** `requires_human_approval` must be `true` for all action types in v1.0. The execution
layer governs state-changing actions; no `system_worker` may approve an execution_candidate.
A future policy version may relax this for specific, well-bounded action types, but that requires
a constitution amendment.

**12.2** `max_retries` is the total number of `execution_record` entries permitted for one
`execution_candidate`. It includes the original attempt. A `max_retries` of 1 means exactly one
attempt with no retries. Minimum value is 1. Maximum value is 5.

**12.3** `idempotency_key_fields` is an ordered list of dot-separated paths into
`execution_candidate.route_snapshot`. The idempotency key is derived by concatenating the values
at these paths, separated by `|`, and taking the SHA-256 hash of the result using D-1 canonical
JSON encoding. The key is deterministic: the same snapshot fields produce the same key. The key
is recorded on `execution_candidate` and on every `execution_record` for that candidate.

**12.4** `payload_spec` maps output payload field names to dot-separated paths into
`execution_candidate.route_snapshot`. Every field in `payload_spec` must be resolvable from the
snapshot schema defined in Article 17. The activation trigger validates this. Fields that are
not resolvable block policy activation.

**12.5** All `action_type` keys in `execution_rules` must exist in
`execution_action_type_vocabulary`. The activation trigger validates this.

---

## Part V — Entity Schemas

### Article 13 — `execution_candidate` Schema

```
execution_candidate
├── id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── provider_route_candidate_id     UUID NOT NULL REFERENCES provider_route_candidate(id)
├── publication_candidate_id        UUID NOT NULL REFERENCES publication_candidate(id)
├── execution_policy_id             UUID NOT NULL REFERENCES execution_policy(id)
├── action_type                     TEXT NOT NULL
│                                       REFERENCES execution_action_type_vocabulary(value)
├── status                          TEXT NOT NULL DEFAULT 'pending'
│                                       REFERENCES execution_candidate_status_vocabulary(value)
│
├── idempotency_key                 TEXT NOT NULL              -- Article 13.1; immutable
├── route_snapshot                  JSONB NOT NULL             -- Article 17; immutable
├── execution_payload               JSONB NOT NULL             -- Article 13.2; immutable
│
├── pending_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── approved_at                     TIMESTAMPTZ
├── approved_by                     TEXT
├── approved_notes                  TEXT
├── curator_reviewed_by             TEXT
├── curator_reviewed_at             TIMESTAMPTZ
│
├── UNIQUE (provider_route_candidate_id, action_type)
│       WHERE status NOT IN ('rejected','withdrawn','rolled_back')
├── CONSTRAINT chk_exc_candidate_snapshot   CHECK (route_snapshot <> '{}'::jsonb)
├── CONSTRAINT chk_exc_candidate_payload    CHECK (execution_payload <> '{}'::jsonb)
├── CONSTRAINT chk_exc_candidate_ikey       CHECK (
│       idempotency_key ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_exc_candidate_approval   CHECK (
│       status IN ('pending','rejected','withdrawn') OR
│       (approved_by IS NOT NULL AND approved_at IS NOT NULL)
│   )
├── CONSTRAINT chk_exc_candidate_self_approval CHECK (
│       approved_by IS NULL OR approved_by IS DISTINCT FROM
│       (route_snapshot->>'matched_by')
│   )
│
├── provenance                      JSONB NOT NULL DEFAULT '{}'
├── created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Triggers on `execution_candidate`:**

1. **`trg_exc_candidate_snapshot_immutable`** — BEFORE UPDATE: if `OLD.route_snapshot`,
   `OLD.execution_payload`, or `OLD.idempotency_key` differs from the corresponding NEW value,
   raise an exception. These three fields are written once and never updated.

2. **`trg_exc_candidate_status_transitions`** — BEFORE UPDATE OF status: enforces valid
   transition table from Article 5. Rejects any transition not listed.

3. **`trg_exc_candidate_success_gate`** — BEFORE UPDATE OF status: when `NEW.status =
   'succeeded'`, verify that at least one `execution_record` with `status = 'confirmed'` exists
   for this candidate. If not, raise an exception.

4. **`trg_exc_candidate_paused_policy_gate`** — BEFORE UPDATE OF status: when `NEW.status =
   'executing'`, verify that `execution_policy.status = 'active'` for the policy identified by
   `execution_candidate.execution_policy_id`. A paused policy blocks new execution attempts even
   for already-approved candidates.

**13.1 Idempotency key derivation.** The idempotency key is computed at candidate creation time:
1. Collect the values at each path listed in
   `execution_policy.execution_rules[action_type].idempotency_key_fields`
   from `route_snapshot`
2. Serialize each value using D-1 canonical JSON (keys alpha-sorted, null retained, floats to 6
   decimal places)
3. Concatenate with `|` as separator
4. Compute SHA-256 of the concatenated string
5. Encode as 64-character lowercase hexadecimal

The key is stored as `execution_candidate.idempotency_key` and is immutable. Every
`execution_record` for this candidate carries the same key.

**13.2 Execution payload derivation.** The execution payload is computed at candidate creation
time from `execution_policy.execution_rules[action_type].payload_spec` applied to `route_snapshot`.
Each field in `payload_spec` is resolved from the snapshot path and written to
`execution_payload`. The payload is immutable after creation — it is the constitutional record
of what the platform is authorized to submit. No runtime mutation is permitted.

### Article 14 — `execution_record` Schema

```
execution_record
├── id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── execution_candidate_id      UUID NOT NULL REFERENCES execution_candidate(id)
├── execution_policy_id         UUID NOT NULL REFERENCES execution_policy(id)
├── action_type                 TEXT NOT NULL REFERENCES execution_action_type_vocabulary(value)
├── attempt_number              INT NOT NULL
├── status                      TEXT NOT NULL DEFAULT 'prepared'
│                                   REFERENCES execution_record_status_vocabulary(value)
│
├── idempotency_key             TEXT NOT NULL              -- copied from execution_candidate
├── prepared_payload            JSONB NOT NULL             -- Article 14.1; immutable
├── rollback_payload            JSONB                      -- Article 14.2; null if not a rollback
├── is_rollback                 BOOLEAN NOT NULL DEFAULT FALSE
│
├── prepared_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── submitted_at                TIMESTAMPTZ
├── confirmed_at                TIMESTAMPTZ
├── failed_at                   TIMESTAMPTZ
├── failure_reason              TEXT
├── external_reference          TEXT                       -- provider confirmation reference (future)
├── outcome_detail              JSONB NOT NULL DEFAULT '{}'
│
├── UNIQUE (execution_candidate_id, attempt_number)
├── CONSTRAINT chk_exc_record_payload   CHECK (prepared_payload <> '{}'::jsonb)
├── CONSTRAINT chk_exc_record_ikey      CHECK (idempotency_key ~ '^[0-9a-f]{64}$')
├── CONSTRAINT chk_exc_record_attempt   CHECK (attempt_number >= 1)
│
├── provenance                  JSONB NOT NULL DEFAULT '{}'
├── created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
└── updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Triggers on `execution_record`:**

1. **`trg_exc_record_payload_immutable`** — BEFORE UPDATE: if `OLD.prepared_payload` or
   `OLD.idempotency_key` differs from the corresponding NEW value, raise an exception.

2. **`trg_exc_record_status_transitions`** — BEFORE UPDATE OF status: enforces valid transition
   table from Article 6.

**14.1 `prepared_payload` is the exact payload the platform is authorized to submit.** It is
copied verbatim from `execution_candidate.execution_payload`. A rollback record's
`prepared_payload` is the payload that would reverse the original action. `prepared_payload`
is immutable after creation.

**14.2 `rollback_payload`** is non-null only when `is_rollback = TRUE`. It records the state
that existed before the original action (captured from `route_snapshot` or from the external
confirmation detail of the original record). The rollback payload is the governed record of
what the rollback will submit.

### Article 15 — `execution_audit_log` Schema

`execution_audit_log` is append-only. No UPDATE or DELETE is permitted. Enforcement follows the
PostgreSQL RULE pattern established in the Commerce Intelligence Constitution.

```
execution_audit_log
├── id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── execution_candidate_id      UUID NOT NULL REFERENCES execution_candidate(id)
├── execution_policy_id         UUID NOT NULL REFERENCES execution_policy(id)
├── execution_record_id         UUID REFERENCES execution_record(id)   -- NULL for candidate-level events
├── event_type                  TEXT NOT NULL
│                                   REFERENCES execution_audit_event_type_vocabulary(value)
├── event_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── actor_type                  TEXT NOT NULL              -- "system_worker" | "curator"
├── actor_id                    TEXT NOT NULL
├── actor_notes                 TEXT                       -- required when actor_type = 'curator'
├── previous_state              JSONB NOT NULL DEFAULT '{}'
├── new_state                   JSONB NOT NULL DEFAULT '{}'
├── entry_checksum_sha256       TEXT NOT NULL
├── previous_entry_checksum     TEXT
├── reason                      TEXT NOT NULL
├── generated_by                TEXT NOT NULL
├── created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
│
├── CONSTRAINT chk_exc_audit_entry_checksum    CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$')
├── CONSTRAINT chk_exc_audit_previous_checksum CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_exc_audit_distinct_checksum CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
│   )
├── CONSTRAINT chk_exc_audit_actor_id          CHECK (length(actor_id) > 0)
├── CONSTRAINT chk_exc_audit_reason            CHECK (length(reason) > 0)
├── CONSTRAINT chk_exc_audit_generated_by      CHECK (length(generated_by) > 0)
├── CONSTRAINT chk_exc_audit_curator_notes     CHECK (
│       actor_type <> 'curator' OR actor_notes IS NOT NULL
│   )
│
└── UNIQUE (execution_candidate_id, entry_checksum_sha256)
```

`execution_record_id` is nullable. Events that operate at the candidate level
(`candidate_pending`, `candidate_approved`, `cascade_applied`, `idempotency_collision`) have
`execution_record_id = NULL`. Events that operate at the record level (`record_prepared`,
`record_submitted`, `record_confirmed`, `record_failed`) must have a non-null
`execution_record_id`.

Hash chain is per `execution_candidate_id`. D-1 canonical JSON throughout.

### Article 16 — `execution_replay` Schema

`execution_replay` is a first-class governance entity, not merely an audit artifact. A replay
run is a determinism audit: it verifies that the same snapshot and policy produce the same
payload. Each replay run is an immutable, integrity-verified record.

```
execution_replay
├── id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4()
├── execution_candidate_id      UUID NOT NULL REFERENCES execution_candidate(id)
├── execution_record_id         UUID REFERENCES execution_record(id)   -- NULL if pre-execution
├── execution_policy_id         UUID NOT NULL REFERENCES execution_policy(id)
├── replayed_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
├── replayed_by                 TEXT NOT NULL
│
├── outcome                     TEXT NOT NULL              -- Article 16.1
│
├── snapshot_used               JSONB NOT NULL             -- execution_candidate.route_snapshot
│                                                          -- captured at replay time
├── payload_derived             JSONB NOT NULL             -- payload re-derived from snapshot+policy
├── payload_recorded            JSONB NOT NULL             -- execution_candidate.execution_payload
├── idempotency_key_derived     TEXT NOT NULL              -- re-derived key
├── idempotency_key_recorded    TEXT NOT NULL              -- execution_candidate.idempotency_key
│
├── divergence_details          TEXT                       -- non-null when outcome != 'payload_match'
│
├── entry_checksum_sha256       TEXT NOT NULL
├── previous_entry_checksum     TEXT
│
├── CONSTRAINT chk_exc_replay_outcome         CHECK (outcome IN (
│       'payload_match', 'payload_diverge',
│       'idempotency_key_match', 'idempotency_key_diverge',
│       'snapshot_integrity_failure'
│   ))
├── CONSTRAINT chk_exc_replay_checksum        CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$')
├── CONSTRAINT chk_exc_replay_prev_checksum   CHECK (
│       previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
│   )
├── CONSTRAINT chk_exc_replay_key_format      CHECK (
│       idempotency_key_derived ~ '^[0-9a-f]{64}$' AND
│       idempotency_key_recorded ~ '^[0-9a-f]{64}$'
│   )
│
└── UNIQUE (execution_candidate_id, entry_checksum_sha256)
```

The hash chain on `execution_replay` is per `execution_candidate_id` — the same logical chain
as `execution_audit_log`. Replay records and audit log records share no hash chain; they maintain
separate chains for the same candidate. This allows either chain to be verified independently.

**16.1 Replay outcomes:**

| Outcome | Meaning |
|---|---|
| `payload_match` | Re-derived payload is bit-identical to recorded payload. Idempotency key matches. Integrity confirmed. |
| `payload_diverge` | Re-derived payload differs from recorded payload. Policy, snapshot, or payload resolution logic may have changed. |
| `idempotency_key_diverge` | Payload matches but idempotency key differs. Key derivation logic may have changed. |
| `snapshot_integrity_failure` | `route_snapshot` could not be fully parsed. Snapshot corruption suspected. |

When outcome is not `payload_match`, the `divergence_details` field must contain a
human-readable explanation of what diverged and a hypothesis for why.

After a replay run, the worker writes both:
1. An `execution_replay` row (this entity)
2. A `replay_verified` or `replay_failure` event to `execution_audit_log` with
   `new_state = {"execution_replay_id": "<UUID>", "outcome": "<outcome>"}`

This dual write makes replay events queryable both via the audit chain and via the replay table.
Both writes are within the same transaction.

---

## Part VI — Replayability

### Article 17 — Route Snapshot

**17.1** At execution_candidate creation time, the execution worker captures a full snapshot of
all upstream governed state and writes it to `execution_candidate.route_snapshot`. The snapshot
is immutable after creation, enforced by `trg_exc_candidate_snapshot_immutable`.

**17.2** The snapshot must include, at minimum:

```json
{
  "provider_route_candidate": {
    "id":                              "<UUID>",
    "provider_name":                   "<provider_name>",
    "channel":                         "<channel_name>",
    "status":                          "approved",
    "provider_routing_policy_id":      "<UUID>",
    "provider_capability_profile_id":  "<UUID>",
    "matched_by":                      "<actor_id>"
  },
  "publication_snapshot": {
    "publication_candidate": {
      "id":                    "<UUID>",
      "channel":               "<channel_name>",
      "publication_policy_id": "<UUID>"
    },
    "publication_channel_profile": {
      "id":               "<UUID>",
      "metadata":         { "<field>": "<value>", "...": "..." },
      "image_spec":       { "accepted_formats": [...], "min_width_px": <int>, "source_image_width": <int>, "color_profiles": [...] },
      "rights_statement": "<string>",
      "pricing_export":   { "computed_price": <float>, "currency": "USD", "price_tier": "<tier>", "floor_price": <float or null>, "ceiling_price": <float or null> }
    },
    "catalog_snapshot": {
      "catalog_variant":          { "id": "<UUID>", "variant_key": "<key>", "product_type": "<type>", "product_family": "<family>", "dimensions": { "...": "..." } },
      "catalog_pricing_profile":  { "id": "<UUID>", "computed_price": <float>, "price_tier": "<tier>", "floor_price": <float or null>, "ceiling_price": <float or null>, "markup_multiplier": <float> },
      "catalog_candidate":        { "id": "<UUID>", "product_family": "<family>", "catalog_policy_id": "<UUID>" },
      "illustration":             { "title": "<string>", "taxon_name": "<string>", "illustrator": "<string or null>", "publication_year": <int or null>, "publication_title": "<string or null>", "rights_status": "<Public Domain|CC0>", "source": "<bhl|loc>", "source_record_id": "<string>" },
      "commerce_opportunity":     { "csm_tier": "<tier>", "commerce_tier": "<tier>", "hard_gate_status": "passed", "image_width_px": <int>, "illustrator_prestige": <float>, "place_relevance_score": <float>, "requires_curator_review": <bool>, "computed_at": "<ISO 8601 UTC>" }
    }
  }
}
```

**17.3** The `candidate_pending` audit event must write the route_snapshot to `new_state`. The
audit log is the primary record; the snapshot on `execution_candidate` is a query convenience.

### Article 18 — Execution Replayability Invariant

An execution candidate is replayable if, given:
- `execution_candidate.route_snapshot`
- The execution policy loaded by exact `execution_candidate.execution_policy_id`

...the execution worker can re-derive:
1. The exact `execution_payload` (deterministic from `payload_spec` applied to snapshot)
2. The exact `idempotency_key` (deterministic from `idempotency_key_fields` applied to snapshot)
3. The gate evaluation outcomes (deterministic from snapshot state)

**18.1 Replayability is a payload guarantee, not an outcome guarantee.** An execution that
succeeded by creating a listing cannot be replayed in the sense of re-creating the listing —
that would be a duplicate. Replay answers: "would we have prepared the same payload?" not "would
we get the same external outcome?"

**18.2 Replay must always load by exact ID.** The replay function must load
`execution_candidate.execution_policy_id` — not the currently active policy. If the active policy
has changed since the candidate was created, replay still uses the original policy. PA-13 prohibits
loading the active policy for replay.

**18.3 Replay frequency.** The execution worker must expose a `replay_candidate(candidate_id)`
function. Replay may be triggered by any curator or authorized system at any time. Each replay
run produces one `execution_replay` row and one `execution_audit_log` event.

---

## Part VII — Human Approval

### Article 19 — Execution Policy Approval

A `execution_policy` may only become `active` if all five conditions hold:

1. `status = 'pending_approval'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM authored_by`
4. `effective_from IS NOT NULL`
5. No other `execution_policy` has `status = 'active'`

The activation trigger must also perform the following validations within the same transaction.
If any validation fails, the activation is rejected:

- Set the previously active policy to `superseded`
- Validate all `action_type` keys in `execution_rules` exist in `execution_action_type_vocabulary`
- Validate `requires_human_approval = true` for all action types in v1.0 (future versions may
  relax this with a constitution amendment; for v1.0 the trigger must enforce it)
- Validate `max_retries` is between 1 and 5 inclusive for all action types
- Validate all `idempotency_key_fields` paths are resolvable from the snapshot schema in
  Article 17.2
- Validate all `payload_spec` paths are resolvable from the snapshot schema in Article 17.2

### Article 20 — Execution Candidate Approval

**20.1** An `execution_candidate` may transition to `approved` only if:
1. `status = 'pending'`
2. `approved_by IS NOT NULL AND approved_at IS NOT NULL`
3. `approved_by IS DISTINCT FROM matched_by` (the actor who matched the provider route)
4. The execution policy referenced by `execution_candidate.execution_policy_id` has
   `status = 'active'` at the time of approval

**20.2 No system_worker may approve an execution_candidate.** Execution authorization is always
a human act in v1.0. The `approved_by` field must identify a human curator. The DB constraint
`chk_exc_candidate_self_approval` enforces that the approver is not the same actor as the one
who initiated the route match.

**20.3** An `execution_candidate` that was approved under a policy that has since been superseded
may still be executed — the policy is loaded by the exact `execution_candidate.execution_policy_id`,
not the active policy. However, XG-2 requires the active policy to not be `paused`. If the
successor policy is paused, execution is blocked even for candidates approved under the prior
active policy. This prevents execution during a governance hold.

**20.4** Curator approval of an execution_candidate is the terminal human authorization in the
constitutional chain. Every upstream layer has been governed and validated. The approver is
confirming that the accumulated governance is complete and that the platform is authorized to act.

### Article 21 — Retry Authorization

**21.1** A retry does not require a new human approval. The original approval of the
`execution_candidate` pre-authorizes all retries within the `max_retries` limit defined in the
execution policy. Each retry creates a new `execution_record` with `attempt_number` incremented.

**21.2** Between retry attempts, the execution worker must wait at least
`execution_policy.execution_rules[action_type].retry_delay_seconds` seconds. This delay is
enforced at the application layer.

**21.3** If a retry succeeds (`execution_record.status = 'confirmed'`), the candidate transitions
to `succeeded` and the terminal cascade is applied (Article 25). If all retries are exhausted
without a confirmed record, the candidate transitions to `failed`.

**21.4** Retry records are governed by the same immutability rules as original records.
`prepared_payload` is identical to the original record — the payload authorized by the human
approver does not change between attempts. `idempotency_key` is identical. The only difference
between an original record and a retry record is `attempt_number` and `is_rollback = false`.

---

## Part VIII — Rollback Governance

### Article 22 — Rollback Conditions and Authorization

**22.1** A rollback is initiated when:
1. `execution_candidate.status = 'failed'`
2. `execution_policy.execution_rules[action_type].rollback_on_failure = true`
3. `action_type != 'retire_listing'` (RBG-2)

**22.2** The rollback is executed by the execution worker using a rollback `execution_record`
with `is_rollback = TRUE`. The rollback record's `prepared_payload` is derived from
`rollback_payload` — a snapshot of the state that existed before the original action. The
rollback payload is immutable after the rollback record is created.

**22.3** A rollback does not require a new human approval in v1.0. The original approval of the
`execution_candidate` implicitly pre-authorizes rollback if the policy specifies
`rollback_on_failure = true`. The approver is presumed to have accepted this consequence.

**22.4** If the rollback itself fails, no automatic re-rollback is attempted. The candidate
remains in `executing` status with a `rolled_back = false` execution_record at `failed` status.
A curator must intervene. This state is an escalation hold, not a terminal failure.

**22.5** A successful rollback transitions the `execution_candidate` to `rolled_back`. No cascade
is applied on rollback — upstream statuses are not updated. The rollback record is evidence of
an attempted and reversed action; it does not constitute a confirmed submission.

### Article 23 — Partial Rollback Prohibition

No partial rollback is permitted. A rollback `execution_record` must reverse the entire original
`prepared_payload`. Partial reversals — updating some fields but not others — are constitutionally
prohibited. If a complete reversal is not possible (e.g., the external system has no atomic
reversal API), the execution_candidate must be escalated to curator review and held in the
`failed` state pending human resolution.

---

## Part IX — Terminal Cascade

### Article 24 — Success Cascade

When an `execution_record` transitions to `confirmed`:

1. `execution_candidate.status → 'succeeded'`
2. `provider_route_candidate.status → 'submitted'` (via the `provider_route_candidate_id` on the candidate)
3. `publication_candidate.status → 'published'` (via the `publication_candidate_id` on the candidate)
4. `publication_channel_profile.status → 'published'` (via the `publication_channel_profile_id` on the provider_route_candidate)

All four updates and the `cascade_applied` audit event are written within the same atomic
transaction as the `record_confirmed` transition. If any update fails, the entire transaction
rolls back. The execution_record remains in `submitted` status pending the next attempt.

**24.1** The `catalog_candidate.status` update is out of scope for v1.0. A catalog_candidate
may have multiple catalog_variants, each with potentially multiple publication_candidates across
different channels. A single execution confirmation does not represent full catalog-level
publication. A future constitution may govern aggregate catalog publication status.

**24.2** The cascade updates are direct DB writes by the execution worker. They bypass the normal
status transition triggers on the upstream entities. This is permitted as an explicit constitutional
exception — the cascade is the authorized downstream consequence of a confirmed execution. The
cascade updates must each produce an audit event in the respective entity's audit log:
- A `candidate_published` event in `publication_audit_log`
- A `route_submitted` event in `provider_routing_audit_log`

---

## Part X — Prohibited Acts

### Article 25 — Prohibited Acts

| Act | Prohibition |
|---|---|
| **PA-1** | No execution_candidate created without an approved provider_route_candidate |
| **PA-2** | No execution_record created without a human-approved execution_candidate |
| **PA-3** | No execution_record created when execution_policy.status = 'paused' |
| **PA-4** | No mutation of `route_snapshot`, `execution_payload`, or `idempotency_key` after initial write |
| **PA-5** | No mutation of `execution_record.prepared_payload` or `execution_record.idempotency_key` after initial write |
| **PA-6** | No `UPDATE` or `DELETE` on `execution_audit_log` rows |
| **PA-7** | No execution_policy activation without second-human approval |
| **PA-8** | No mutation of `execution_rules` after policy activation |
| **PA-9** | No `system_worker` approving an execution_candidate |
| **PA-10** | No execution attempt after XG-4 or XG-5 idempotency collision — curator resolution required |
| **PA-11** | No execution attempt after XG-6 retry limit exceeded |
| **PA-12** | No `retire_listing` rollback — terminal action has no constitutional rollback path in v1.0 |
| **PA-13** | No replay loading the currently active policy — replay must use `execution_candidate.execution_policy_id` |
| **PA-14** | No partial rollback — rollback must reverse the entire prepared_payload |
| **PA-15** | No cascade applied unless execution_record.status = 'confirmed' |
| **PA-16** | No hardcoded execution payload construction — all fields from `payload_spec` |
| **PA-17** | No hardcoded idempotency key computation — all fields from `idempotency_key_fields` |
| **PA-18** | No external API call inside the execution_worker's governed scope — the worker produces governed records; external submission is downstream |
| **PA-19** | No execution_candidate approved by the same actor who matched the provider route |
| **PA-20** | No self-approval of execution_policy |

---

## Part XI — Execution Worker Protocol

### Article 26 — Transaction Scope and Ordering

**26.1 Candidate creation transaction:**

```
BEGIN;
  Verify XG-0: provider_route_candidate.status = 'approved'
  Derive execution_payload from route_snapshot + execution_policy
  Derive idempotency_key from route_snapshot + execution_policy
  INSERT execution_candidate (status = 'pending', payload = derived, key = derived)
  INSERT execution_audit_log (candidate_pending, new_state = route_snapshot)
COMMIT;
```

**26.2 Record preparation transaction (after human approval, XG-1 through XG-6 pass):**

```
BEGIN;
  Verify XG-1: execution_candidate.status = 'approved'
  Verify XG-2: active policy is not paused
  Verify XG-3: action_type in execution_rules
  Verify XG-4: no confirmed execution_record for this candidate
  Verify XG-5: idempotency_key not in any other confirmed execution_record
  Verify XG-6: attempt_count < max_retries
  UPDATE execution_candidate SET status = 'executing'
  INSERT execution_audit_log (candidate_executing)
  INSERT execution_record (status = 'prepared', attempt_number = N, prepared_payload = execution_candidate.execution_payload)
  INSERT execution_audit_log (record_prepared, execution_record_id = record.id)
COMMIT;
```

**26.3 Confirmation transaction (external confirmation received):**

```
BEGIN;
  UPDATE execution_record SET status = 'confirmed', confirmed_at = NOW(), external_reference = '<ref>'
  INSERT execution_audit_log (record_confirmed, execution_record_id = record.id)
  UPDATE execution_candidate SET status = 'succeeded'
  INSERT execution_audit_log (candidate_succeeded)
  -- Terminal cascade:
  UPDATE provider_route_candidate SET status = 'submitted'
  INSERT provider_routing_audit_log (route_submitted, ...)
  UPDATE publication_candidate SET status = 'published'
  INSERT publication_audit_log (candidate_published, ...)
  UPDATE publication_channel_profile SET status = 'published'
  INSERT publication_audit_log (channel_profile_published, ...)
  INSERT execution_audit_log (cascade_applied, new_state = {"updated_entities": [...]})
COMMIT;
```

**26.4 Retry transaction:**

```
BEGIN;
  INSERT execution_audit_log (retry_authorized, reason = 'attempt N of M')
  INSERT execution_record (status = 'prepared', attempt_number = N+1, prepared_payload = execution_candidate.execution_payload)
  INSERT execution_audit_log (record_prepared, execution_record_id = record.id)
COMMIT;
```

**26.5 Rollback transaction (RBG gates pass):**

```
BEGIN;
  INSERT execution_record (status = 'prepared', is_rollback = TRUE, rollback_payload = <prior_state>)
  INSERT execution_audit_log (rollback_triggered, execution_record_id = record.id)
COMMIT;
```

**26.6 Replay transaction:**

```
BEGIN;
  Load execution_candidate by candidate_id
  Load execution_policy by execution_candidate.execution_policy_id  -- NOT active policy
  Re-derive payload from route_snapshot + policy
  Re-derive idempotency_key from route_snapshot + policy
  Compare derived vs. recorded payload and key
  INSERT execution_replay (outcome = '<outcome>', payload_derived = ..., payload_recorded = ..., ...)
  INSERT execution_audit_log (replay_verified | replay_failure, new_state = {"execution_replay_id": "<UUID>"})
COMMIT;
```

**26.7 Policy load and validation:** At startup, the execution worker must:
1. Load the active `execution_policy`
2. Validate all `action_type` keys exist in `execution_action_type_vocabulary`
3. Validate all `idempotency_key_fields` paths are resolvable from the expected snapshot schema
4. Validate all `payload_spec` paths are resolvable from the expected snapshot schema
5. Halt immediately if any validation fails — process no candidates

---

## Part XII — Migration Sequence

### Article 27 — Required Migrations

| Migration | Contents | Depends On |
|---|---|---|
| M-35 | Eight vocabulary tables + seed values: `execution_policy_status_vocabulary`, `execution_candidate_status_vocabulary`, `execution_record_status_vocabulary`, `execution_action_type_vocabulary`, `execution_audit_event_type_vocabulary`. `execution_policy` table + constraints + immutability trigger + activation trigger (all Article 19 validations). UNIQUE partial index WHERE status = 'active'. | M-33 (`provider_route_candidate` must exist for FK from M-36) |
| M-36 | `execution_candidate` table + all constraints + `trg_exc_candidate_snapshot_immutable` + `trg_exc_candidate_status_transitions` + `trg_exc_candidate_success_gate` + `trg_exc_candidate_paused_policy_gate`. `execution_record` table + constraints + `trg_exc_record_payload_immutable` + `trg_exc_record_status_transitions`. `execution_audit_log` table + constraints + append-only RULE. `execution_replay` table + constraints. All indexes. | M-35 |
| M-37 | Seed `execution_policy` v1.0.0 in `draft` status with `execution_rules` for `create_listing` action type. | M-36 |

### Article 28 — Seed Policy Specification

The M-37 seed populates `execution_policy` v1.0.0 with:

**execution_rules for `create_listing`:**

```json
{
  "create_listing": {
    "requires_human_approval":  true,
    "max_retries":              3,
    "retry_delay_seconds":      300,
    "rollback_on_failure":      false,
    "idempotency_key_fields": [
      "provider_route_candidate.id",
      "provider_route_candidate.provider_name",
      "publication_snapshot.catalog_snapshot.catalog_variant.variant_key",
      "publication_snapshot.catalog_snapshot.catalog_candidate.catalog_policy_id"
    ],
    "payload_spec": {
      "provider_name":       "provider_route_candidate.provider_name",
      "channel":             "provider_route_candidate.channel",
      "variant_key":         "publication_snapshot.catalog_snapshot.catalog_variant.variant_key",
      "product_family":      "publication_snapshot.catalog_snapshot.catalog_variant.product_family",
      "product_type":        "publication_snapshot.catalog_snapshot.catalog_variant.product_type",
      "title":               "publication_snapshot.publication_channel_profile.metadata.title",
      "description":         "publication_snapshot.publication_channel_profile.metadata.description",
      "tags":                "publication_snapshot.publication_channel_profile.metadata.tags",
      "rights_statement":    "publication_snapshot.publication_channel_profile.rights_statement",
      "computed_price":      "publication_snapshot.publication_channel_profile.pricing_export.computed_price",
      "currency":            "publication_snapshot.publication_channel_profile.pricing_export.currency",
      "price_tier":          "publication_snapshot.publication_channel_profile.pricing_export.price_tier",
      "image_formats":       "publication_snapshot.publication_channel_profile.image_spec.accepted_formats",
      "source_image_width":  "publication_snapshot.publication_channel_profile.image_spec.source_image_width",
      "rights_status":       "publication_snapshot.catalog_snapshot.illustration.rights_status",
      "illustrator":         "publication_snapshot.catalog_snapshot.illustration.illustrator",
      "source_record_id":    "publication_snapshot.catalog_snapshot.illustration.source_record_id"
    }
  }
}
```

---

## Part XIII — Ratification

This Constitution is a draft. It becomes authoritative upon ratification by the Principal
Architect. Ratification is recorded by updating the status field at the top of this document to
`Ratified` and setting the ratification date.

Implementation of Migrations M-35, M-36, and M-37 is not authorized until ratification.

Implementation of the `execution_worker` is not authorized until M-35 through M-37 are applied
and the v1.0.0 seed policy transitions to `active` through the constitutional activation protocol
(second-human approval required, Article 19).

The complete constitutional chain is now specified. The pipeline from
`illustration_opportunity` to `execution_record` is fully governed.
