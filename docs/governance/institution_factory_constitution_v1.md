# Institution Factory Constitution v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — effective immediately |
| Supersedes | `institution_factory_v1.md` (process document — remains as implementation reference) |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |
| Authority | Strategic Direction v1 · MSC v1.2 · Foundation Model Constitution v1.0 · Standards Constitution v1.0 · CI Constitution v1.2 · Wireframe Constitution v1 · Europeana Rights Matrix v1.0 · Institution Coverage Audit v1.0 |

---

## Preamble

This Constitution governs the activation of every future content institution in Nature & Culture.
It answers five questions:

1. Which stages of institution activation are mandatory?
2. What must be true before each stage is considered complete?
3. What constitutes a failure condition at each stage?
4. What human approvals are required, from whom, and for what?
5. Which invariants are permanent and cannot be overridden?

This Constitution is subordinate to the Strategic Directive and the Illustration Opportunity
Doctrine. Any provision that conflicts with those documents is void. This Constitution governs
institution activation. It does not govern scoring, routing, catalog, or publication. Those
are governed by their own constitutions.

The governing principle of this Constitution: **every future content institution follows the same
constitutional path without exception.** Deviation requires a constitutional amendment, not a
governance workaround, an exception, or a Director Decision alone.

---

## Part I — Foundations

### Article 1 — Scope and Identity

**1.1** This Constitution governs the complete lifecycle from the discovery of a candidate
institution to the authorization of full-collection ingestion. It governs every institution
classified as a **Content Institution** under Article 3.

**1.2** This Constitution does not govern:
- Identity and Reference Authorities (GeoNames, OSM, Wikidata, GBIF) — governed by Standards Constitution v1.0
- Aggregator References (Europeana, DPLA, Trove) — governed by their individual Director Decisions; member institutions follow this Constitution for direct integration
- Post-activation scoring, routing, catalog, or publication — governed by their respective constitutions
- Media type phase ordering — governed by MSC v1.2 Article 5.8

**1.3** The output of this Constitution is a content institution in `operational_status = 'ingesting'`
with a ratified Director Decision, a human-verified Asset Zero record, and a completed pilot.
An institution cannot reach `operational_status = 'ingesting'` by any other path.

### Article 2 — Authority Chain

**2.1** The authority hierarchy for institution activation decisions:

```
Strategic Directive
        ↓
Illustration Opportunity Doctrine
        ↓
Institution Factory Constitution (this document)
        ↓
Individual Director Decisions (DD-[INST]-001 and amendments)
        ↓
Institution-specific workers / adapters
```

A Director Decision that conflicts with this Constitution is void in the conflicting provision.
A worker that violates an invariant of this Constitution is in constitutional violation regardless
of what its DD authorizes.

**2.2** This Constitution is senior to all institution-specific governance documents. A DD may
narrow the requirements of this Constitution for a specific institution. It may not widen them
(i.e., it may set a stricter asset cap than the constitutional maximum; it may not raise the cap
above the constitutional maximum without a constitutional amendment).

### Article 3 — Institutional Classification Vocabulary

**3.1** Every candidate institution is classified into exactly one of three constitutional classes
before Stage 1 proceeds.

| Class | Definition | Path |
|---|---|---|
| **Content Institution** | Holds, curates, and digitises its own collection. First-party API publisher. | This Constitution in full. |
| **Aggregator Reference** | Aggregates content from member institutions. Does not hold the collection. | Governed by aggregator-specific DD. Member institutions follow this Constitution for direct integration. |
| **Identity and Reference Authority** | Provides entity identity, geographic data, or classification frameworks. Does not hold media assets. | Standards Constitution v1.0 only. |

**3.2** Classification is made at Stage 1. It cannot be changed retroactively. If a classification
error is discovered after Stage 1, a new Stage 1 Discovery Report supersedes the prior one and
resets the lifecycle. Any engineering work completed under the incorrect classification is void
for governance purposes until the corrected classification is ratified.

**3.3** An Aggregator Reference is not a substitute for direct institutional integration. When
content from a member institution is present in the NC pipeline via an aggregator route, and NC
subsequently onboards that member institution directly, this Constitution applies to the direct
integration. The direct route supersedes the aggregator route for the same physical object per
the deduplication protocol in Invariant IFC-9.

### Article 4 — The Sequencing Principle

**4.1** The nine stages of institution activation are mandatory and sequential. No stage may
begin before its predecessor's exit gate is cleared.

**4.2** An institution that has not cleared the exit gate of Stage N may not perform any action
that is constitutionally reserved for Stage N+1 or later. Performing such an action is a
constitutional violation regardless of business urgency.

**4.3** No engineering work (adapter development, schema changes, worker deployment) may begin
before Stage 2 (Governance) is complete. Code written before a DD is ratified exists outside the
governance framework. It may not be deployed to production until the relevant DD is ratified.

**4.4** Stages may not be retroactively declared complete after violations are discovered in a later
stage. If a Stage N violation is discovered during Stage N+2 work, Stage N must be remediated and
its exit gate re-cleared before Stage N+2 proceeds. All work performed in stages after the violated
stage is suspended until remediation is complete.

---

## Part II — Stage Framework

### Article 5 — The Nine Mandatory Stages

**5.1** The nine stages of institution activation are:

| Stage | Name | Governing article |
|---|---|---|
| 1 | Discovery | Article 7 |
| 2 | Governance | Article 8 |
| 3 | Connectivity | Article 9 |
| 4 | Rights | Article 10 |
| 5 | Adapter | Article 11 |
| 6 | M36 | Article 12 |
| 7 | Asset Zero | Article 13 |
| 8 | Pilot | Article 14 |
| 9 | Operational | Article 15 |

**5.2** All nine stages are mandatory for every Content Institution. No stage may be designated
as optional, waived, or combined with an adjacent stage without a constitutional amendment.

**5.3** A stage is complete when and only when its exit gate, as defined in the governing article,
is cleared. A stage is not complete because the implementing team believes its work is done. The
exit gate is the constitutional test.

**5.4** The Stage ordering is total. The following concurrent operations are the only authorized
exceptions to strict sequencing:

| Concurrent operations | Authorization |
|---|---|
| Stage 4 (Rights) fixture development may begin once Stage 3 connectivity smoke tests are green, without waiting for the full Stage 3 exit gate | This article (5.4) |
| Stage 5 Sprint 1 may begin once Stage 4 rights.py is drafted and rights fixtures exist, without waiting for Sprint 2 compliance audit | This article (5.4) |

All other concurrency requires a constitutional amendment.

### Article 6 — Exit Gate Definition

**6.1** An **exit gate** is a set of one or more conditions that must be true for a stage to be
considered complete. Exit gates are defined per stage in Articles 7–15.

**6.2** Exit gate conditions are constitutional tests, not process milestones. An exit gate may
not be declared cleared by the implementing team alone. The following clearance authority applies:

| Stage | Clearance authority |
|---|---|
| 1 | Director |
| 2 | Director + Second-Human (independent) |
| 3 | Principal Architect |
| 4 | Principal Architect (compliance audit) |
| 5 | Principal Architect (sprint compliance audit, each sprint) |
| 6 | Principal Architect |
| 7 | Director + designated Human Reviewer |
| 8 | Director (after SC-N queries all pass) |
| 9 | Director |

**6.3** A compliance audit may not be self-certified by the implementer. The Principal Architect
function is constitutionally independent of the implementing team for audit purposes. A sprint
compliance audit signed by the same person who wrote the code being audited is not a valid audit.

---

## Part III — Stage Definitions

### Article 7 — Stage 1: Discovery

**7.1** Stage 1 determines whether a candidate institution is worth the governance and engineering
investment of full activation. It produces a Discovery Report and a Director decision.

**7.2** The Discovery Report must address:
- (a) Constitutional class (Content Institution / Aggregator / Identity Authority per Article 3)
- (b) MSC v1.2 Reference Institution tier (Tier 1 / Tier 2)
- (c) PD candidacy estimate: minimum 1,000 commercially viable PD illustration opportunities required to proceed
- (d) API surface inventory: bulk enumeration method, rights field type, image delivery protocol
- (e) Aggregator overlap: whether the institution's holdings are already partially present via aggregator route
- (f) Geographic coverage: mapping to NC canonical places
- (g) Commercial priority: Illustration Opportunity density estimate per CI Constitution v1.2

**7.3** An institution with no machine-readable rights attestation may not be classified as Proceed
without a custom rights determination protocol documented in the Discovery Report and escalated to
the Director before Stage 2 begins. Absence of machine-readable rights is a Stage 1 escalation
condition, not a Stage 1 blocker, but the custom protocol must be ratified as part of Stage 2.

**7.4 — Exit gate:**
Director decision recorded: **Proceed**, **Defer**, or **Reject**.

**7.5 — Failure conditions:**
- (a) Stage 2 begins without a Director **Proceed** decision. Constitutional violation. Stage 2 work is void and must be halted until the decision is made.
- (b) The PD candidacy estimate is absent from the Discovery Report. The exit gate may not be cleared.
- (c) Stage 1 is bypassed entirely and Stage 2 begins without any Discovery Report. Constitutional violation. All Stage 2–9 work is void until Stage 1 is completed retroactively and a Director Proceed decision is recorded.

---

### Article 8 — Stage 2: Governance

**8.1** Stage 2 produces the authoritative governance document (Director Decision) for every
aspect of the institution's integration. Stage 2 is the constitutional blocker for all
engineering work.

**8.2** The Director Decision document must address all of the following. A DD that omits any
topic is incomplete and may not be ratified:

| Article | Topic | Minimum content required |
|---|---|---|
| 1 | Source classification | Content institution vs. aggregator; deduplication protocol if aggregator overlap identified at Stage 1 |
| 2 | Rights strategy | Rights authority; `block_if_absent` value; ALLOWED, REVIEW_REQUIRED, and BLOCKED vocabulary; FM-4 confirmation |
| 3 | API governance | All endpoints, auth mechanism, enumeration strategy |
| 4 | IIIF governance | IIIF endpoint, IIIF ID derivation method |
| 5 | Metadata mapping | Field-by-field mapping from institution schema to NC substrate contract |
| 6 | Pilot scope | Specific collection/set, asset cap (≤ 500), pilot window (≤ 90 days), place association deferral policy |
| 7 | Success criteria | SC-1 through SC-N, each with SQL verification query |
| 8 | Source registry amendments | RU-SR-1 INSERT SQL with all required `sources` table fields |

**8.3** The Rights strategy article must explicitly confirm: "FM-4 is permanent for this
institution. No foundation model output may directly or indirectly influence any
`media_rights` record for any asset sourced from [institution name]." This confirmation
must appear verbatim or in equivalent constitutional language. A DD without this confirmation
may not be ratified.

**8.4** All DD articles must be validated against live API responses before ratification.
If live testing invalidates any article, a numbered amendment is required. An amendment
document must specify the triggering findings with live API evidence, the affected articles,
and the amended text. Amendments are ratified concurrently with the DD or as a subsequent
ratified document.

**8.5** The Ratification Package is a mandatory companion to every DD. It must contain:
- (a) Pre-ratification checklist (all governing documents present; platform prerequisites met; DB prerequisites met)
- (b) Director Approval Statement (10-point minimum confirmation)
- (c) Second-Human Approval Statement (8-point minimum confirmation, independent of Director)
- (d) Source registry SQL: RU-SR-1 INSERT with 10-point post-INSERT verification query
- (e) Pilot scope controls
- (f) Suspension triggers (minimum: Trigger A — rights gate breach; Trigger B — FM exclusion breach)
- (g) Success criteria SC-1 through SC-N with SQL verification queries
- (h) Post-ratification action register with ordered gate sequence

**8.6 — Exit gate:**
Both Director and Second-Human approval statements signed in the Ratification Package.
DD status field updated to `Ratified`. Date recorded. Both human identities recorded.

**8.7 — Failure conditions:**
- (a) A worker creates any `source_record` row for this institution before the DD is ratified. Constitutional violation. Those `source_record` rows are void and must be deleted before the legitimate pilot begins.
- (b) The DD is ratified by only one human. The DD is not ratified. Any engineering work begun on the basis of a single-human approval is not constitutionally authorized.
- (c) The Second-Human approver is the same person as the Director. The two-human gate is not satisfied by one person signing twice. The DD is not ratified.
- (d) The Rights strategy article omits the FM-4 confirmation (Article 8.3). The DD may not be ratified until this is added.
- (e) An amendment is required by live API testing (Article 8.4) but is not produced. The DD may not be ratified until the amendment is written and validated.

---

### Article 9 — Stage 3: Connectivity

**9.1** Stage 3 proves that the institution's APIs respond correctly, applies required DB
migrations, and inserts the source record into the `sources` table.

**9.2** Required DB migrations must be applied before the RU-SR-1 INSERT. The INSERT
may not be modified to omit columns added by a pending migration. Omitting required
columns is a constitutional violation.

**9.3** The RU-SR-1 INSERT must be executed exactly as written in the Ratification Package.
Post-INSERT verification: all 10 rows of the 10-point verification query must return `true`.
A single row returning `false` means the INSERT did not execute correctly. The row must be
corrected or deleted and re-inserted before the exit gate can be cleared.

**9.4** The following API smoke tests are mandatory:

| Test | Required result |
|---|---|
| OAI-PMH `Identify` | HTTP 200; `deletedRecord` policy present |
| OAI-PMH `ListMetadataFormats` | Preferred format (e.g., `edm`) confirmed present |
| OAI-PMH `ListRecords` (pilot set, first page) | ≥ 1 record; rights field present in ≥ 1 record |
| IIIF URL resolution | HTTP 200; image data returned |
| Rights URI sample | ≥ 1 ALLOWED-class rights URI present in live records |
| Auth verification | If `auth_type != 'none'`: auth token validates without error |

All six smoke tests must pass. A smoke test may not be skipped.

**9.5 — Exit gate:**
SC-1 verified: `SELECT source_id FROM sources WHERE source_id = '[slug]'` returns exactly one row.
All six API smoke tests pass. Results recorded.

**9.6 — Failure conditions:**
- (a) RU-SR-1 executed with `source_id` value that differs from the ratified Ratification Package. Constitutional violation. The row must be deleted and re-inserted with the correct value.
- (b) Any API smoke test fails but Stage 4 begins anyway. Constitutional violation. Stage 4 must be halted until all smoke tests pass.
- (c) A required DB migration is bypassed by removing columns from the RU-SR-1 INSERT. Constitutional violation. The migration must be applied and the INSERT re-executed.

---

### Article 10 — Stage 4: Rights

**10.1** Stage 4 produces a compliant rights classification module and rights test fixtures.
It must be complete before Sprint 2 of Stage 5 may begin.

**10.2** Every rights classification module must implement the following three decisions with
no gaps:

| Decision | Definition | Required worker action |
|---|---|---|
| ALLOWED | Rights URI maps to CC0, PDM, or equivalent ALLOWED-class URI | Write `rights_status = 'pending_verification'`; no workflow_item |
| REVIEW_REQUIRED | Rights URI maps to a review-required class | Write `rights_status = 'pending_verification'`; create `workflow_item` with `capability = 'rights_review'` |
| BLOCKED | Rights URI maps to a blocked class, OR rights field is absent | Reject before any DB write; return `{"status": "rejected", "writes": 0}` |

**10.3** The `block_if_absent` rule is constitutional for all Content Institutions. An absent
rights field is classified BLOCKED, not REVIEW_REQUIRED. The null check must fire before the
blocked token check and before any DB write. This is not configurable per institution.

**10.4** The rights classification module must be audited by the Principal Architect before
Sprint 2 of Stage 5 may proceed. The audit verdict must be one of:
- `[INSTITUTION] SPRINT 2 COMPLIANT` — Stage 5 Sprint 2 may proceed
- `NOT COMPLIANT — [violations listed]` — violations must be remediated; no Sprint 2 until compliant

**10.5** Institutions that use `edm:rights` URI vocabulary may re-export `workers/europeana_adapter/rights.py`
as a thin wrapper. The wrapper re-export is subject to the same Sprint 2 compliance audit
as a new module.

**10.6** Three rights test fixtures are required at minimum:

| Fixture | Class | File naming |
|---|---|---|
| Real record with ALLOWED rights URI | ALLOWED | `tests/fixtures/[slug]/[slug]_allowed_[label].[ext]` |
| Real record with REVIEW_REQUIRED rights URI | REVIEW_REQUIRED | `tests/fixtures/[slug]/[slug]_review_required.[ext]` |
| Real or modified record with absent rights field | BLOCKED (absent) | `tests/fixtures/[slug]/[slug]_no_rights.[ext]` |

Synthetic modification of a real fixture is authorized for the absent-rights fixture only.

**10.7 — Exit gate:**
Sprint 2 Compliance Audit verdict: `[INSTITUTION] SPRINT 2 COMPLIANT`.

**10.8 — Failure conditions:**
- (a) Sprint 2 of Stage 5 begins without a Sprint 2 compliance audit verdict. Constitutional violation. Sprint 2 is suspended until the audit is completed.
- (b) The absent-rights null check fires AFTER the BLOCKED token check. Constitutional violation (Invariant IFC-5). The module must be remediated before Sprint 2 is marked compliant.
- (c) FM output is used to classify rights for a record. Constitutional violation (Invariant IFC-3). The classification must be discarded, the `media_rights` row deleted, and the rights module corrected.

---

### Article 11 — Stage 5: Adapter

**11.1** Stage 5 builds the institution's ingest worker through a mandatory sprint sequence.
Each sprint has a defined scope and a required compliance audit before the next sprint begins.

**11.2** The mandatory sprint sequence:

| Sprint | Scope | Minimum test coverage | Required verdict before proceeding |
|---|---|---|---|
| 1 | Source classification, API client, raw fetch, normalization structure | `test_[slug]_adapter_sprint1.py` | `[INST] SPRINT 1 COMPLIANT` |
| 2 | Rights adapter, EDM/metadata normalization | `test_[slug]_adapter_sprint2.py` | `[INST] SPRINT 2 COMPLIANT` |
| 3 | M36 store, technical metadata, complete write path | `test_[slug]_store.py` + `test_[slug]_adapter_sprint3.py` | `[INST] INGESTION READY` or violations listed |
| 4 | Remediation of Sprint 3 violations (if any) | `test_[slug]_adapter_sprint4.py` | `[INST] INGESTION READY` |

Sprint 4 is mandatory if and only if Sprint 3 returns violations. A Sprint 3 verdict of
`[INST] INGESTION READY` advances directly to Stage 6.

**11.3** The standard violations to check at Sprint 3 are:

| Code | Description | Constitutional authority |
|---|---|---|
| V1 | Absent `rights_uri` routes to REVIEW_REQUIRED instead of BLOCKED | Invariant IFC-5 |
| V2 | `anchor_type` hardcoded; not derived from set membership or accepted as parameter | Invariant IFC-6 |
| V3 | `media_rights.rights_evidence` missing required fields from A1 Article 3(f) equivalent | Invariant IFC-8 |
| V4 | Worker sets `rights_status` to a terminal value | Invariant IFC-2 |
| V5 | Worker advances `source_item.status` beyond `'proposed'` | Invariant IFC-4 |
| V6 | M36 table writes not wrapped in a single transaction | Invariant IFC-7 |
| V7 | FM output influences any `media_rights` column | Invariant IFC-3 |

**11.4** Every adapter must contain four modules with these responsibilities:

| Module | Responsibility | May not be combined with |
|---|---|---|
| `rights.py` | Rights classification only | Any other module |
| `edm.py` / `normalize.py` | Metadata normalization only | `store.py` |
| `technical.py` | Technical metadata extraction and validation only | `store.py` |
| `store.py` | M36 write path only — all six table writes | Any other module |

Module responsibilities may not be merged. A `store.py` that also classifies rights is a
constitutional violation.

**11.5** A compliance audit is the Principal Architect function. The Sprint N compliance
audit verdict is the controlling document for whether Sprint N+1 may begin. The
implementing team may not self-certify a compliance verdict.

**11.6** When Sprint 3 returns violations, a Remediation Specification must be produced
before Sprint 4 begins. The Remediation Specification must state for each violation:
exact required behavior, exact prohibited behavior, minimum compliant fix (code-level),
required unit tests, and required replay tests.

**11.7 — Exit gate:**
Sprint N (final) Compliance Audit verdict: `[INSTITUTION] INGESTION READY`.

**11.8 — Failure conditions:**
- (a) Sprint N+1 begins without Sprint N compliance audit cleared. Constitutional violation. Sprint N+1 is suspended.
- (b) Compliance audit is self-certified by the implementer. Audit is void. A new audit by the Principal Architect is required.
- (c) Any V1–V7 violation present in the deployed adapter. Constitutional violation. The adapter may not be used in production until the violation is remediated and a new compliance audit returns `INGESTION READY`.
- (d) Module responsibilities are merged (e.g., `store.py` contains rights classification logic). Constitutional violation. The merged code must be separated before the Sprint 3 audit can clear.

---

### Article 12 — Stage 6: M36

**12.1** Stage 6 verifies that all six M36 substrate tables are correctly wired for this
institution and that all M36-layer constitutional invariants are satisfied. It does not
introduce new engineering; it verifies what Stage 5 built.

**12.2** All six M36 tables must be wired per the following requirements:

| Table | Required content | Constitutional constraint |
|---|---|---|
| `source_item` | One row per unique institution record | `status = 'proposed'`; `anchor_type` from governed vocabulary |
| `source_record` | One row per ingest event | `schema_standard` matches institution; `raw_payload_hash` present |
| `media_rights` | One row per `source_item` | `rights_status = 'pending_verification'`; evidence dict per IFC-8; `commercial_reuse_permitted = FALSE`; `modification_permitted = FALSE`; `verified_by = NULL`; `verified_at = NULL` |
| `media_file` | One row per primary deliverable | `preservation_status = 'pending_retrieval'`; `source_url` present |
| `preservation_event` | One row per rights classification event | `agent_type = 'worker'`; `event_outcome = 'pending_human_review'` |
| `media_technical_metadata` | One row per `source_item` | `validation_status` from `validation_status()` function; `content_hash` present |

**12.3** The write path test counts are constitutional:
- An ALLOWED record must produce exactly 7 DB writes (source_item, source_record, media_file, media_rights, preservation_event, media_technical_metadata, source_item UPDATE).
- A REVIEW_REQUIRED record must produce exactly 8 DB writes (the 7 above plus workflow_item INSERT).
- A BLOCKED or absent-rights record must produce exactly 0 DB writes.

A write count that deviates from these values indicates a constitutional violation in the
M36 write path. The deviation must be identified and remediated before the exit gate clears.

**12.4 — Exit gate:**
All six tables wired. Write count invariant verified (7 / 8 / 0). All IFC-1 through IFC-12
invariants confirmed for this institution's write path.

**12.5 — Failure conditions:**
- (a) Any of the six M36 tables is missing from the write path. Constitutional violation. Stage 7 may not begin.
- (b) ALLOWED record write count ≠ 7. Constitutional violation — a write is missing or an extra write is present.
- (c) BLOCKED record write count ≠ 0. Constitutional violation — a record that should be rejected is writing to the DB.
- (d) Any M36 invariant (IFC-2 through IFC-8) violated in the write path. Constitutional violation. Remediation required before Stage 7.

---

### Article 13 — Stage 7: Asset Zero

**13.1** Stage 7 proves that a single real record — not a fixture — flows from API fetch
through the complete M36 write path to human-verified, place-associated, activated state.
Stage 7 may not be skipped or replaced by fixture-based validation.

**13.2** The Asset Zero record must meet all of the following:
- (a) Fetched from the production API endpoint, not a test fixture or synthetic record
- (b) Carries an ALLOWED-class rights URI
- (c) Has a resolvable IIIF URL
- (d) Has a title, a date, and at least one subject term
- (e) Is associable with one NC canonical place

**13.3** The Asset Zero rights verification sequence is mandatory and immutable:

1. `write_record()` executed against the production DB. `source_item.status = 'proposed'`; `media_rights.rights_status = 'pending_verification'`.
2. The designated Human Reviewer retrieves the record and independently verifies PD status against the institution's open access policy.
3. The Human Reviewer sets `media_rights.rights_status` to `verified_cc0` or `verified_pd`.
4. The Human Reviewer sets `media_rights.verified_by` and `media_rights.verified_at`.
5. A `preservation_event` of type `rights_verified` with `agent_type = 'human'` is recorded.
6. Place association is recorded.
7. The Director advances `source_item.status` to `'activated'`.

Steps 2–7 may not be automated. No script, worker, or FM output may perform any action
in steps 2–7.

**13.4** The IIIF URL of the Asset Zero record must be resolved and confirmed returning a
full-resolution image before the exit gate is cleared. A `media_file.source_url` that
returns an error is a Stage 7 failure.

**13.5 — Exit gate:**
One `source_item` with:
- `status = 'activated'`
- `media_rights.rights_status` in `('verified_cc0', 'verified_pd')`
- `media_rights.verified_by` non-null
- `media_rights.verified_at` non-null
- `media_rights.commercial_reuse_permitted = TRUE` (set by Human Reviewer)
- Place association present
- IIIF URL confirmed returning HTTP 200 and image data

**13.6 — Failure conditions:**
- (a) The Asset Zero record is a fixture, not a real API response. Stage 7 exit gate may not be cleared on a fixture record.
- (b) Any of steps 2–7 of Article 13.3 is performed by a script, worker, or automated process. Constitutional violation (Invariants IFC-1, IFC-2, IFC-4). The record's `media_rights` values set by automation are void. A human must redo the verification.
- (c) `source_item.status = 'activated'` is set by a worker. Constitutional violation (Invariant IFC-4). The status must be reset to `'proposed'` and set to `'activated'` by a human.
- (d) IIIF URL does not resolve. Stage 7 exit gate may not be cleared. The IIIF issue must be diagnosed and resolved.
- (e) The Human Reviewer who verifies the Asset Zero record is the same person who wrote the ingest worker. This does not constitute a violation of the two-human gate (Stage 2 applies; Stage 7 requires one human). However, it is recorded for the Pilot Report.

---

### Article 14 — Stage 8: Pilot

**14.1** Stage 8 runs a capped, scoped, time-limited harvest under active human oversight.
It validates the success criteria from the DD before full collection ingestion is authorized.

**14.2** The pilot parameters must fall within these constitutional bounds:

| Parameter | Minimum | Maximum | Notes |
|---|---|---|---|
| Asset cap | 50 | 500 | Set in DD; may not be exceeded without Director Decision |
| Duration | 30 days | 90 days | Set in DD |
| Collection scope | 1 set/collection | 3 sets/collections | Set in DD |
| Human reviews | 10% of cap | — | Minimum; Director may require more |

The pilot asset cap may not be exceeded without a Director Decision. Exceeding the cap
without a Director Decision is a constitutional violation. Ingestion must halt until
the Director grants an extension or terminates the pilot.

**14.3** Two suspension triggers must be armed before any pilot harvest begins:

| Trigger | Condition |
|---|---|
| Trigger A | Count of `source_item` rows with `status = 'proposed'` and no `workflow_item` cleared exceeds the human review backlog threshold defined in the DD |
| Trigger B | Any `media_rights` row where `worker_classified_status` is not one of the three expected values (ALLOWED / REVIEW_REQUIRED / BLOCKED) |

Additional institution-specific triggers defined in the DD are also mandatory. If any
trigger fires, ingestion must halt immediately. Ingestion may not resume without a
Director Decision. A suspension trigger that fires and is manually overridden without
a Director Decision is a constitutional violation.

**14.4** Success criteria evaluation: the SC-1 through SC-N SQL queries from the DD
must be run and recorded at minimum once per week during the pilot window. A SC that fails
must be investigated before the following week's evaluation. If a SC fails in the final
week and is not resolved, the pilot may not advance to Stage 9.

**14.5** The deduplication protocol (Invariant IFC-9) must be active during the pilot
if the Discovery Report identified aggregator overlap. Deduplication events must be counted
and reported in the Pilot Report.

**14.6 — Exit gate:**
All SC-1 through SC-N: **pass** in the final evaluation. No active suspension trigger.
Pilot duration has run its full course or Director Decision authorizes early conclusion.
Director Decision to proceed to Stage 9.

**14.7 — Failure conditions:**
- (a) Pilot asset cap exceeded without Director Decision. Constitutional violation. Ingestion halts until Director Decision is recorded.
- (b) Suspension trigger fires and ingestion continues. Constitutional violation. All records ingested after trigger fire without Director Decision are of questionable provenance and must be flagged for review.
- (c) Any SC fails in the final evaluation and Stage 9 is begun. Constitutional violation. Stage 9 must be halted and the SC failure remediated.
- (d) Pilot begins before the designated Human Reviewer is confirmed. Constitutional violation. Pilot is suspended until a Human Reviewer is designated and confirmed.
- (e) SC-N SQL queries are not run during the pilot window. The pilot is void. SC-N queries must be run retrospectively; if they cannot be run due to data state, the pilot window must be extended.

---

### Article 15 — Stage 9: Operational

**15.1** Stage 9 authorizes full-collection ingestion and transitions the institution to
`operational_status = 'ingesting'`. It has no exit gate — it is the terminal state of
the activation lifecycle. Future governance actions are governed by DD amendments, not
a new factory run.

**15.2** The `operational_status` transition to `'ingesting'` requires Director Decision.
It may not be set by a worker or by migration backfill. The UPDATE SQL must be recorded
in the operational action log with the Director identity and timestamp.

**15.3** The Trigger A and Trigger B suspension triggers from Stage 8 are permanent. They
do not expire at the end of the pilot. They govern the institution in production indefinitely.
Disabling a suspension trigger without a Director Decision and a constitutional amendment
is a constitutional violation.

**15.4** The FM-4 permanent confirmation must be recorded in the institution's operational
record. If it was not explicitly recorded in the DD, it must be recorded now. FM-4 is not
retroactively waivable by any future action.

**15.5** The institution coverage matrix must be updated with:
- Institution name and slug
- Activation date
- Media types active
- Geographic coverage (canonical places)
- Aggregator overlap status

**15.6 — Exit gate:**
None. Stage 9 has no exit. The institution is permanently operational.

**15.7 — Failure conditions:**
- (a) `operational_status = 'ingesting'` set without Director Decision. Constitutional violation. The status must be reset and a Director Decision recorded.
- (b) Full-collection harvest begins before Stage 8 exit gate is cleared. Constitutional violation. The harvest must halt until Stage 8 is complete.
- (c) Suspension trigger is disabled without a Director Decision. Constitutional violation. The trigger must be re-armed.

---

## Part IV — Constitutional Invariants

### Article 16 — The Twelve Invariants

The twelve invariants of this Constitution apply to every institution at every stage.
They may not be waived by institution-specific Director Decisions. Waiving any invariant
requires a constitutional amendment to this Constitution and to the authority document
listed in the `Source` column.

---

**Invariant IFC-1 — The PD Hard Gate.**
Only assets with rights status classifiable as ALLOWED under the Europeana Rights Matrix v1.0
or an institution-specific ratified equivalent may enter the NC production pipeline. No
CC-licensed, InC-licensed, or commercially restricted asset may enter the pipeline under any
circumstances. This invariant applies regardless of institutional agreement, editorial priority,
or commercial opportunity.

*Source: Strategic Direction v1. Cannot be lifted by Director Decision.*

---

**Invariant IFC-2 — The Two-Human Gate.**
Rights terminal values (`verified_cc0`, `verified_pd`) may be set only by a human. Stage 2
ratification requires two independent human approvals. The two humans must be different people.
One person approving twice does not satisfy the two-human gate.

*Source: MSC v1.2.*

---

**Invariant IFC-3 — FM-4 Permanent.**
No foundation model output may directly or indirectly write to, suggest, or influence any
`media_rights` column for any asset sourced from a governed institution. This invariant
is permanent. It survives any future amendment to this Constitution or to any other NC
constitution. It cannot be lifted by Director Decision, constitutional amendment, business
agreement, or any other mechanism.

*Source: MSC v1.2, Foundation Model Constitution v1.0 Invariant FM-4.*

---

**Invariant IFC-4 — Worker Status Ceiling.**
A worker process may not advance `source_item.status` beyond `'proposed'`. Status advancement
beyond `'proposed'` — to `'activated'` or any future status — is a human action only. A
worker that sets `source_item.status = 'activated'` is in constitutional violation regardless
of the record's rights state.

*Source: MSC v1.2.*

---

**Invariant IFC-5 — Block-If-Absent.**
An absent rights field is classified BLOCKED for all Content Institutions. It is not classified
REVIEW_REQUIRED, not silently passed through, and not treated as a missing field in a
validation warning. The null check must fire before the BLOCKED token check and before any DB
write. This is not configurable per institution or per collection.

*Source: DD-RIJKSMUSEUM-001 A1 Article 3(d) + 4.2. Elevated to constitutional invariant 2026-06-07.*

---

**Invariant IFC-6 — Anchor Type Vocabulary.**
`source_item.anchor_type` must be one of exactly four values: `biological`, `geographic`,
`cultural`, `mixed`. The value must be derived from OAI-PMH set membership or accepted as
an explicit parameter from the caller. It may not be hardcoded as a literal in the SQL or in
the function body. The default value when no set membership matches is `'cultural'`, not `'mixed'`.

*Source: DD-RIJKSMUSEUM-001 A1 Article 5.4. Elevated to constitutional invariant 2026-06-07.*

---

**Invariant IFC-7 — Transaction Boundary.**
All six M36 table writes for a single record must be wrapped in a single DB transaction.
A partial write — where some tables are written and others are not due to an exception —
is a constitutional violation. The transaction must roll back completely on any error.

*Source: MSC v1.2.*

---

**Invariant IFC-8 — Evidence Completeness.**
`media_rights.rights_evidence` must contain at minimum the following nine fields:

| Field | Description |
|---|---|
| `source` | Institution slug |
| `source_record_id` | UUID of the `source_record` row |
| Rights URI key (e.g., `edm_rights_uri`) | The normalized rights URI from the source record |
| `rights_matrix_classification` | Lowercase decision class: `allowed`, `review_required`, or `blocked` |
| `applying_policy` | The rights matrix document version governing this classification |
| Record identifier key (e.g., `oai_pmh_identifier`) | The institution's record identifier |
| `raw_payload_hash` | SHA-256 of the raw fetched payload |
| `worker_classified_status` | The worker's preliminary classification |
| `evidence_status` | `'pending_human_review'` (worker-set; immutable until human review) |

A `media_rights` row whose evidence dict is missing any of these nine fields is a
constitutional violation.

*Source: DD-RIJKSMUSEUM-001 A1 Article 3(f). Elevated to constitutional invariant 2026-06-07.*

---

**Invariant IFC-9 — Deduplication Protocol.**
When a direct-institution `source_item` is created for an object already present in the NC
pipeline via an aggregator route, the aggregator-sourced `source_item` must be flagged as
superseded via a `workflow_item` with `capability = 'deduplication_review'`. The aggregator
row must not be deleted. The deduplication flag must be set before the direct-institution
`source_item` is activated.

*Source: DD-RIJKSMUSEUM-001 Article 2(d).*

---

**Invariant IFC-10 — No Governance Shortcut.**
A worker may not create `source_record` rows for a Content Institution whose DD is not
ratified. `governance_state = 'active'` set by a DB migration backfill does not constitute
ratification. Stage 2 ratification is the sole basis for worker authorization to create
`source_record` rows.

*Source: Europeana Activation Checklist v1. Elevated to constitutional invariant 2026-06-07.*

---

**Invariant IFC-11 — Review Required Workflow.**
Records classified REVIEW_REQUIRED must produce a `workflow_item` with
`capability = 'rights_review'` in the same transaction as the `media_rights` row. A
REVIEW_REQUIRED record that does not produce a `workflow_item` has silently entered the
pipeline without queuing a human review. This is a constitutional violation.

*Source: MSC v1.2.*

---

**Invariant IFC-12 — Media Type Phase Ordering.**
New media types for a governed institution may only be activated in the sequence
defined by MSC v1.2 Article 5.8. Activating a Phase 2 media type before Phase 1 is
complete in production is a constitutional violation regardless of the institution's
collection composition.

*Source: MSC v1.2 Article 5.8.*

---

## Part V — Approval Requirements

### Article 17 — The Two-Human Gate

**17.1** The two-human gate requires two human approvals that are:
- (a) Independent: each approver reviews the document without knowledge of the other's decision
- (b) Distinct: both approvers are different people; one person approving twice does not satisfy the gate
- (c) Recorded: both identities, roles, and approval timestamps are in the Ratification Package
- (d) Scoped: approval covers the specific document version; approval of a prior version does not satisfy the gate for an amended version

**17.2** The two-human gate applies at:

| Gate | Timing |
|---|---|
| Stage 2 ratification | Before any engineering begins |
| Rights terminal value setting (Stage 7+) | Each individual rights decision |

**17.3** The two-human gate for Stage 2 is satisfied by: Director Approval Statement + Second-Human
Approval Statement, both in the Ratification Package. The Second-Human must be independent of the
engineering team that wrote the DD where possible.

**17.4** A document that passes a two-human gate retains its ratified status until explicitly
superseded or revoked by a new two-human approval. Amendments to a ratified DD require a new
two-human approval for the amendment specifically.

### Article 18 — Director Decision Requirements

**18.1** A Director Decision (DD) is a formal governance document authorizing a specific action.
The following actions require a Director Decision:

| Action | Required DD |
|---|---|
| Stage 1 Proceed decision | Recorded in Stage 1 Discovery Report |
| Stage 2 ratification | DD-[INST]-001 + Ratification Package |
| Pilot asset cap extension (Stage 8) | Recorded in the pilot operational log |
| Suspension trigger resume (Stage 8+) | Recorded before resuming ingestion |
| Stage 9 authorization | Recorded in Stage 9 operational log |
| Suspension trigger disable (permanent) | Requires constitutional amendment |

**18.2** A Director Decision is recorded by name, role, and timestamp in the relevant
governance document. A verbal or informal decision does not constitute a Director Decision.

**18.3** The Director and the Second-Human are not required to be different people for
Stage 1, Stage 8, and Stage 9 decisions. They are required to be different for Stage 2 ratification.

---

## Part VI — Failure Conditions and Remediation

### Article 19 — Failure Mode Classification

**19.1** Failure conditions are classified into two tiers:

| Tier | Name | Definition | Consequence |
|---|---|---|---|
| **Tier 1** | Constitutional Violation | An invariant (IFC-1 through IFC-12) is breached or a mandatory stage requirement is bypassed | Stage is suspended. Work produced under the violation is void for governance purposes until remediated. |
| **Tier 2** | Exit Gate Failure | Stage exit gate conditions are not met, but no invariant is breached | Stage is incomplete. Work may continue but stage may not advance. |

**19.2** A Tier 1 violation does not automatically void all downstream work. The scope of
voidness is limited to work that directly depends on the violated component. Work that is
independent of the violated component is not affected unless it also relies on something void.

**19.3** Remediation of a Tier 1 violation requires:
1. Identification of the violated invariant and the specific records or artifacts affected
2. Remediation Specification (per Article 11.6 format) naming the exact fix
3. Implementation of the fix
4. Compliance audit confirming the fix
5. Re-clearance of the affected stage's exit gate

**19.4** A Tier 1 violation discovered in Stage N+2 that originates in Stage N requires
remediation of Stage N before Stage N+2 may advance, even if Stage N+1 was clean.
Article 4.4 applies.

### Article 20 — Permanent Violations

**20.1** Some violations are permanent in consequence — they cannot be remediated by
fixing the code. They require explicit governance action to acknowledge and document.

| Violation | Permanent consequence | Required governance action |
|---|---|---|
| Worker sets terminal rights value on a record | That record's `media_rights.rights_status` is void; the terminal value was set without authorization | Human must redo rights verification; record must have new `preservation_event` documenting the void and re-verification |
| FM output influences `media_rights` (IFC-3) | The classification result is void regardless of whether it was correct | The record must be re-classified by human; a Director Decision must be recorded acknowledging the FM-4 breach |
| `source_record` created without ratified DD (IFC-10) | Those rows are void | Rows must be deleted; DD must be ratified; rows re-created under legitimate authorization |
| Two-human gate satisfied by one person twice | DD is not ratified | Second human must review and approve; all work since the false ratification is conditionally void pending legitimate ratification |

---

## Part VII — Reference Implementations and Amendment

### Article 21 — Reference Implementations

**21.1** The following implementations are the constitutional archetypes. When an article
of this Constitution is ambiguous in a specific implementation context, the archetype governs.

| Component | Archetype | Location |
|---|---|---|
| Decision Document | DD-RIJKSMUSEUM-001 | `docs/decisions/DD-RIJKSMUSEUM-001_rijksmuseum_production_activation.md` |
| Amendment format | DD-RIJKSMUSEUM-001-A1 | `docs/decisions/DD-RIJKSMUSEUM-001-A1_data_services_platform_amendment.md` |
| Ratification Package | DD-RIJKSMUSEUM-001 Ratification | `docs/decisions/DD-RIJKSMUSEUM-001_ratification_package.md` |
| rights.py (re-export) | Rijksmuseum rights module | `workers/rijksmuseum_adapter/rights.py` |
| rights.py (canonical) | Europeana rights module | `workers/europeana_adapter/rights.py` |
| M36 store | Rijksmuseum store | `workers/rijksmuseum_adapter/store.py` |
| Unit test pattern | Rijksmuseum store tests | `tests/unit/test_rijksmuseum_store.py` |
| Replay test pattern | Rijksmuseum Sprint 4 replay | `tests/replay/test_rijksmuseum_adapter_sprint4.py` |
| Remediation Specification | Rijksmuseum Sprint 4 spec | `docs/implementation/rijksmuseum_sprint4_remediation_spec.md` |

**21.2** A deviation from a reference implementation is not automatically a violation.
The reference implementation illustrates the constitutional requirements. An alternative
implementation that satisfies all constitutional requirements is valid.

### Article 22 — Amendment

**22.1** This Constitution may be amended by Director Decision only when:
- (a) A new institution class is discovered that the current classification vocabulary cannot accommodate
- (b) A new API protocol or rights vocabulary requires a new stage or a modification to an existing stage's requirements
- (c) An invariant is found to conflict with a superior constitution (Strategic Directive, Illustration Opportunity Doctrine)
- (d) Operational experience across multiple institution activations reveals a stage requirement that causes systematic harm without constitutional benefit

**22.2** An amendment may not weaken Invariants IFC-1, IFC-2, IFC-3, or IFC-4. Those invariants
are load-bearing structural commitments of NC's governance model. Weakening them would require
a rewrite of the Strategic Directive itself.

**22.3** An amendment may not eliminate the two-human gate for Stage 2 ratification. The two-human
gate is structural. It may be extended to additional stages by amendment; it may not be removed
from Stage 2.

**22.4** Invariant IFC-3 (FM-4 Permanent) may not be lifted by any amendment to this Constitution.
It may only be lifted by a Director Decision amending the Foundation Model Constitution v1.0
Invariant FM-4 — which itself states it cannot be lifted by Director Decision. IFC-3 is
unconditionally permanent.

**22.5** Amendments are numbered in sequence: this Constitution is v1.0. Amendments produce
v1.1, v1.2, etc. A major restructuring that changes more than three articles produces v2.0.
All versions are retained in the repository.

---

*Institution Factory Constitution v1 — 2026-06-07*
*Every future content institution follows this constitutional path without exception.*
*Deviation requires amendment, not workaround.*
