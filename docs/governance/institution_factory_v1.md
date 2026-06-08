# Institution Factory v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |
| Authority | Strategic Direction v1 · MSC v1.2 · Standards Constitution v1.0 · CI Constitution v1.2 · Wireframe Constitution v1 · Europeana Rights Matrix v1.0 · Institution Coverage Audit v1.0 |

---

## Purpose

Every future institution onboarded to Nature & Culture must follow the same
constitutional path. This document defines that path. It is derived from the
completed onboarding patterns of BHL, LOC, Smithsonian, Europeana, and Rijksmuseum,
and from every ratified NC constitution.

This document governs all new content institutions. It does not govern identity
authorities (Wikidata, GeoNames, OSM, GBIF) or aggregator references (Europeana, DPLA),
which have their own governance contracts. The distinction is constitutional: a
content institution holds, curates, and digitises its own collection. An aggregator
does not hold the collection. An identity authority provides entity identity, not media.

**The nine stages are sequential. No stage may begin before its predecessor's exit gate
is cleared. No exception is authorized without a constitutional amendment.**

---

## Stage Overview

| # | Stage | Purpose | Key output | Exit gate |
|---|---|---|---|---|
| 1 | Discovery | Determine if the institution is worth onboarding | Discovery Report | Proceed/Defer/Reject decision |
| 2 | Governance | Ratify the decision document and ratification package | DD-[INST]-001 + Ratification Package | Two-human ratification |
| 3 | Connectivity | Prove APIs respond and insert source record | Source record in DB | SC-1 verified |
| 4 | Rights | Map institution rights vocabulary to NC policy | rights.py + rights fixtures | Sprint 2 Compliance COMPLIANT |
| 5 | Adapter | Build the ingest worker to sprint compliance | Sprint N Compliance Verdict | All sprints COMPLIANT |
| 6 | M36 | Integrate with the universal media substrate | INGESTION READY verdict | All six tables wired |
| 7 | Asset Zero | Prove a single real record end-to-end | One human-verified activated record | Place association + terminal rights |
| 8 | Pilot | Capped harvest under human oversight | Pilot report | All SC-N met |
| 9 | Operational | Full collection ingestion authorized | Ongoing harvest | Director Decision |

---

## Stage 1 — Discovery

### Purpose

Determine whether the institution has sufficient PD holdings, API quality, commercial
priority, and geographic fit to justify the governance and engineering investment of
onboarding.

### Entry criteria

None. Discovery may be initiated at any time. It requires no prior governance document.

### Process

**1.1 — Institution classification**

Classify the institution using Institution Coverage Audit v1.0 Article 1:

| Class | Definition | Treatment |
|---|---|---|
| Content Institution | Holds, curates, digitises its own collection | Full onboarding path (this document) |
| Aggregator Reference | Aggregates from member institutions | Governed by aggregator DD; direct institution path for members |
| Identity/Reference Authority | Provides entity identity or geographic data | Standards Constitution v1.0 only |

Aggregator-covered institutions must still follow this path for direct integration.
The aggregator route is supplementary, not a substitute, per Institution Coverage Audit v1.0 Article 3.

**1.2 — Reference Institution Tier**

Assign an MSC v1.2 Article 28 tier:

| Tier | Definition |
|---|---|
| Tier 1 | Governance pattern adopted as NC constitutional doctrine |
| Tier 2 | Production data source; governance pattern documented |
| Tier 3 | Discovery or reference use only; not a production pipeline source |

**1.3 — PD Candidacy Assessment**

Estimate the volume of PD/CC0 assets in the collection. The assessment must determine:
- What proportion of holdings pre-date the PD cutoff (US: published before 1928; international: life+70 years)
- Whether the institution has a published open access programme with machine-readable rights attestation
- Whether `edm:rights` URIs or equivalent vocabulary is present in API responses

An institution with fewer than an estimated 1,000 commercially viable PD illustration
opportunities is a Defer candidate regardless of other factors.

**1.4 — API Surface Inventory**

Document every API surface the institution exposes:

| Surface | Preferred | Acceptable | Not supported |
|---|---|---|---|
| Bulk enumeration | OAI-PMH (edm/oai_dc) | REST cursor-based | Manual download only |
| Rights field | `edm:rights` URI vocabulary | `permitDownload` bool | None |
| Image delivery | IIIF Image API 2+/3 | Direct URL | None |
| Metadata format | EDM, MARC, Dublin Core | Custom JSON | Undocumented |

An institution that cannot provide bulk enumeration via OAI-PMH or a cursor-based REST API
is a Defer or Reject candidate. An institution without machine-readable rights attestation
requires a custom rights determination protocol — record this in the Discovery Report and
flag it as a governance escalation.

**1.5 — Aggregator Deduplication Check**

Determine whether the institution's holdings are already partially present in the NC pipeline
via an aggregator (Europeana, DPLA, Trove). If yes, the deduplication protocol from
DD-RIJKSMUSEUM-001 Article 2(d) applies: direct institution records supersede aggregator
records for the same physical object. This is not a blocker but must be stated explicitly
in the DD.

**1.6 — Geographic Coverage Mapping**

Map the institution's holdings to NC place pages. An institution with no anchor to
any of NC's 70 canonical places (per the 70-place commerce matrix) is a Defer
candidate. Geographic coverage gap classifications from Institution Coverage Audit v1.0
apply:

| Gap | Description |
|---|---|
| Critical | Zero coverage for an entire continent or major biome |
| Moderate | Partial coverage; existing sources cover fewer than 50% of canonical places in region |
| Minor | Coverage exists but this institution adds significant depth |

**1.7 — Commercial Priority Assessment**

Assess Illustration Opportunity density per the CI Constitution v1.2. The primary
commercial object is the Illustration Opportunity, not the raw asset count. An institution
with 500,000 assets but 200 commercially usable illustration opportunities is lower
priority than an institution with 50,000 assets and 8,000 commercially usable ones.

Prioritise: biological illustration (Audubon, Gould, Haeckel, Merian, Nodder tier),
natural history photography, historic cartography, and cultural object photography
from canonical places.

### Deliverable

**Discovery Report** containing:
1. Institution classification (Content / Aggregator / Identity)
2. Reference Institution tier (Tier 1 / 2 / 3)
3. PD candidacy estimate (volume + basis)
4. API surface inventory (endpoints, formats, auth)
5. Aggregator overlap status
6. Geographic coverage map to NC canonical places
7. Commercial priority assessment (Illustration Opportunity density estimate)
8. Recommendation: Proceed / Defer / Reject with rationale

### Exit gate

Director decision: **Proceed**, **Defer**, or **Reject**.

A Defer decision must state the condition under which the institution may re-enter the
path. A Reject decision is final unless a constitutional amendment creates a new
eligibility class.

---

## Stage 2 — Governance

### Purpose

Produce and ratify the authoritative decision document governing every aspect of the
institution's integration with NC. No engineering work may begin before Stage 2 is complete.

### Entry criteria

Stage 1 Discovery Report with Director **Proceed** decision.

### Process

**2.1 — Assign Decision Document identifier**

Format: `DD-[INSTITUTION]-001` where `[INSTITUTION]` is the institution's canonical
slug (uppercase). Example: `DD-RIJKSMUSEUM-001`, `DD-NHM-001`, `DD-BNFGALLICA-001`.

**2.2 — Write the Decision Document**

The DD must address all eight topics:

| Article | Topic | Minimum content |
|---|---|---|
| 1 | Source classification | Content institution vs. aggregator; MSC tier; deduplication protocol if needed |
| 2 | Rights strategy | Rights authority, `block_if_absent` policy, REVIEW_REQUIRED vocabulary, BLOCKED vocabulary, FM-4 confirmation |
| 3 | API governance | All endpoints, auth mechanism, enumeration strategy, bulk harvest approach |
| 4 | IIIF governance | IIIF endpoint, IIIF ID derivation, fallback if no IIIF |
| 5 | Metadata mapping | Field-by-field mapping from institution schema to NC substrate contract |
| 6 | Pilot scope | Specific collection/set, asset cap, 90-day window, place association deferral policy |
| 7 | Success criteria | SC-1 through SC-N, each with SQL verification query |
| 8 | Source registry amendments | `RU-SR-1` (or equivalent) INSERT SQL with all required `sources` table fields |

Rights strategy must explicitly state:
- Whether the Europeana Rights Matrix v1.0 governs this institution or an institution-specific matrix is required
- The `block_if_absent` value (`true` for all content institutions unless a constitutional amendment specifies otherwise)
- That FM-4 is permanent: no foundation model output may influence any `media_rights` record sourced from this institution

**2.3 — Live API testing**

All DD articles must be validated against live API responses before ratification. If live
testing invalidates any DD article, a numbered amendment is required before the ratification
package is written. Amendments follow the DD-RIJKSMUSEUM-001-A1 pattern: document the
triggering findings with live API evidence, rewrite only the affected articles, maintain
full traceability.

**2.4 — Write the Ratification Package**

The Ratification Package follows the DD-RIJKSMUSEUM-001 ratification package structure:

| Section | Content |
|---|---|
| Pre-ratification checklist | All governing documents present; platform prerequisites met; DB prerequisites met |
| Director Approval Statement | 10-point confirmation covering all DD articles |
| Second-Human Approval Statement | 8-point independent confirmation |
| Source Registry SQL | RU-SR-1 INSERT with 10-point post-INSERT verification query |
| Pilot scope controls | OAI-PMH parameters, asset cap, timing controls |
| Suspension triggers | Trigger A (rights gate breach), Trigger B (FM exclusion breach) |
| Success criteria queries | SC-1 through SC-N with SQL |
| Post-ratification action register | Ordered gate sequence from M-series migration to pilot activation |

**2.5 — Ratification**

Two humans must independently review and approve both the DD and the Ratification Package.
Both approvals must be recorded by name, date, and role in the Ratification Package.

A DD with only one human approval is not ratified. A worker may not create any
`source_record` rows for an institution whose DD is not ratified.

### Deliverables

1. `docs/decisions/DD-[INST]-001_[institution]_production_activation.md`
2. `docs/decisions/DD-[INST]-001-A1_[amendment_title].md` (if live API testing required amendments)
3. `docs/decisions/DD-[INST]-001_ratification_package.md`

### Exit gate

Both Director and Second-Human approval statements signed in the Ratification Package.
Status field of DD updated to `Ratified`. Date recorded.

---

## Stage 3 — Connectivity

### Purpose

Prove that the institution's APIs respond correctly, apply any required DB migrations,
and insert the institution's source record into the `sources` table.

### Entry criteria

DD and Ratification Package both ratified (Stage 2 exit gate cleared).

### Process

**3.1 — Apply required DB migrations**

If the DD's source registry INSERT references `sources` table columns added by a
pending migration (e.g., `governance_state`, `operational_status`), apply that
migration before executing the INSERT. The INSERT must never be modified to omit
required columns as a workaround for a missing migration.

**3.2 — Execute source registry INSERT**

Execute the `RU-SR-1` (or equivalent) INSERT SQL from the Ratification Package.
Run the 10-point post-INSERT verification query. All 10 rows must return `true`.

**3.3 — API smoke tests**

| Test | Pass condition |
|---|---|
| OAI-PMH `Identify` | HTTP 200, `deletedRecord` policy present |
| OAI-PMH `ListMetadataFormats` | Preferred format (e.g., `edm`) confirmed present |
| OAI-PMH `ListRecords` (first page, pilot set) | At least 1 record returned, `<edm:rights>` or equivalent field present in at least one record |
| IIIF URL resolution | First IIIF URL from a live record returns HTTP 200 and image data |
| Rights URI sample | At least one ALLOWED-class URI present in live records |
| Auth verification | If `auth_type != 'none'`: API key / OAuth token validates without error |

**3.4 — Deduplication check**

If the Discovery Report identified aggregator overlap, execute the deduplication
check query from the DD Article 2(d) equivalent. Record the count of existing
aggregator-routed `source_item` rows that will require supersession flagging.

### Deliverable

Stage 3 Connectivity Report (inline or as a ratification package addendum):
- Migration applied: yes/no (migration number)
- RU-SR-1 INSERT: executed, 10-point verification all true
- API smoke test results: all 6 tests pass/fail
- Deduplication count: N existing aggregator rows identified

### Exit gate

SC-1 verified: `SELECT source_id FROM sources WHERE source_id = '[slug]'` returns one row.
All API smoke tests green. Deduplication count recorded.

---

## Stage 4 — Rights

### Purpose

Classify the institution's rights vocabulary against NC policy and produce a compliant
`rights.py` module (or verify the existing one covers this institution) and rights
test fixtures covering all three decision classes.

### Entry criteria

Stage 3 exit gate cleared (source record in DB, API smoke tests green).

### Constitutional constraints — non-negotiable

| Constraint | Source |
|---|---|
| PD hard gate: only PD/CC0 assets enter the production pipeline | Strategic Direction v1 |
| FM-4 permanent: no foundation model output influences any `media_rights` record | MSC v1.2 + DD-RIJKSMUSEUM-001 |
| `block_if_absent = true` for all content institutions | DD-RIJKSMUSEUM-001 A1; default unless amended |
| Rights terminal values (`verified_cc0`, `verified_pd`) are set by human only | MSC v1.2 |
| Worker writes `rights_status = 'pending_verification'` only | MSC v1.2 |

### Process

**4.1 — Rights vocabulary mapping**

Map every rights URI or field value the institution uses to one of three NC classes:

| Class | Action | Terminal status |
|---|---|---|
| ALLOWED | Ingest; worker sets `pending_verification` | Human sets `verified_cc0` or `verified_pd` |
| REVIEW_REQUIRED | Ingest; open `workflow_item` with `capability = 'rights_review'` | Human reviews and sets terminal value |
| BLOCKED | Reject before any DB write; zero records created | — |

The mapping is governed by:
- **Europeana Rights Matrix v1.0** if the institution uses Europeana EDM `edm:rights` URIs
- **An institution-specific matrix** (documented as a new governance file) if the institution uses a different vocabulary

Institutions that use `edm:rights` URIs can re-export `workers/europeana_adapter/rights.py`
as a thin wrapper (the Rijksmuseum pattern). Institutions with a custom vocabulary require
a new rights module.

**4.2 — `block_if_absent` enforcement**

Absent rights field must be classified as BLOCKED in `write_record()`. The check must
fire before the BLOCKED token check and before any DB write. This is the V1 pattern
from the Rijksmuseum Sprint 4 remediation spec and is now the constitutional standard.

```python
if not normalized.get("rights_uri"):          # BLOCKED — no rights field
    return {
        "status": "rejected",
        "reason": "missing_rights_uri",
        "record_id": normalized.get("record_id"),
        "writes": 0,
    }
```

**4.3 — Rights test fixtures**

Produce at minimum three XML/JSON fixture files:

| Fixture | Rights class | Filename pattern |
|---|---|---|
| A real record with an ALLOWED rights URI | ALLOWED | `[slug]_allowed_[label].xml` |
| A real record with a REVIEW_REQUIRED rights URI | REVIEW_REQUIRED | `[slug]_review_required.xml` |
| A real or synthetic record with absent rights | BLOCKED (absent) | `[slug]_no_rights.xml` |

Fixtures must be real API responses from live endpoints where possible. Synthetic
fixtures are acceptable only for the absent-rights case (modify a real fixture).

### Deliverable

1. `workers/[slug]_adapter/rights.py` — rights classification module, or confirmation that `europeana_adapter/rights.py` covers this institution via re-export
2. `tests/fixtures/[slug]/[slug]_allowed_*.xml` — ALLOWED fixture
3. `tests/fixtures/[slug]/[slug]_review_required.xml` — REVIEW_REQUIRED fixture
4. `tests/fixtures/[slug]/[slug]_no_rights.xml` — BLOCKED (absent) fixture

### Exit gate

Sprint 2 Compliance Audit returns **[INSTITUTION] SPRINT 2 COMPLIANT**. No V-class violations in rights.py or edm.py / normalization module.

---

## Stage 5 — Adapter

### Purpose

Build the institution's ingest worker to constitutional compliance through a structured
sprint sequence with a compliance audit gate between each sprint.

### Entry criteria

Stage 4 exit gate cleared (rights.py compliant, fixtures in place).

### Sprint structure

Each sprint has a defined scope and a mandatory compliance audit before the next sprint may begin.

| Sprint | Scope | Audit file | Audit verdict |
|---|---|---|---|
| Sprint 1 | Source classification, API client, raw OAI/REST fetch, record normalization structure | `test_[slug]_adapter_sprint1.py` | [INST] SPRINT 1 COMPLIANT |
| Sprint 2 | Rights adapter, EDM/metadata normalization, `normalize_oai_edm_record()` equivalent | `test_[slug]_adapter_sprint2.py` | [INST] SPRINT 2 COMPLIANT |
| Sprint 3 | M36 store (`store.py`), technical metadata, M36 write path | `test_[slug]_store.py` + `test_[slug]_adapter_sprint3.py` | [INST] INGESTION READY |
| Sprint 4 | Remediation of violations found in Sprint 3 audit (if any) | `test_[slug]_adapter_sprint4.py` | [INST] INGESTION READY |

A Sprint 3 audit that finds no violations advances directly to Stage 6.
A Sprint 3 audit that finds violations requires Sprint 4 remediation before Stage 6.

### Compliance audit format

For each sprint, the compliance audit must:

1. List every violation found (V1, V2, ... Vn) with the exact file and line number
2. State the constitutional authority violated
3. If clean: state `[INSTITUTION] SPRINT N COMPLIANT`
4. If violations: state `NOT INGESTION READY` and list violations

No sprint may be marked compliant by the implementer alone. The compliance audit is a
Principal Architect function.

### Standard violations to check at each sprint

**Sprint 2 — rights.py / normalization module:**
- FM output influences rights classification (V-class, constitutional)
- `classify_rights(None)` not caught before ingest (V-class, per `block_if_absent` invariant)
- BLOCKED token check missing or incomplete
- REVIEW_REQUIRED records do not generate `workflow_item`

**Sprint 3 — store.py:**
- V1: Absent rights_uri not BLOCKED before DB writes
- V2: `anchor_type` hardcoded (not derived from set membership or accepted as parameter)
- V3: Evidence dict missing required A1 Article 3(f) fields (see §Constitutional Invariants)
- V4: Worker sets `rights_status` to a terminal value
- V5: Worker advances `source_item.status` beyond `'proposed'`
- V6: Any M36 table write not wrapped in a transaction

### Adapter module structure

Every institution adapter must contain these modules:

| Module | Responsibility |
|---|---|
| `rights.py` | Rights classification — re-export from europeana adapter or institution-specific |
| `edm.py` / `normalize.py` | Metadata normalization from institution schema to substrate contract |
| `technical.py` | Technical metadata extraction and validation |
| `store.py` | M36 write path — all six table writes |

Module names may vary but responsibilities may not be merged or re-ordered.

### Deliverable

All four modules present, all sprint compliance audits returned COMPLIANT.

### Exit gate

Sprint N (final) Compliance Audit returns **[INSTITUTION] INGESTION READY**.

---

## Stage 6 — M36

### Purpose

Verify that all six M36 substrate tables are correctly wired for this institution
and that all constitutional invariants governing the write path are satisfied.

### Entry criteria

Stage 5 exit gate cleared (INGESTION READY verdict).

### M36 write path verification

The following must be confirmed for every new institution:

| Table | Required | Verification |
|---|---|---|
| `source_item` | One row per unique institution record | `anchor_type` from governed vocabulary; `status = 'proposed'` |
| `source_record` | One row per ingest event | `schema_standard` matches institution (e.g., `'edm'`); `raw_payload_hash` present |
| `media_rights` | One row per `source_item` | `rights_status = 'pending_verification'`; evidence dict contains all 9 fields; `commercial_reuse_permitted = FALSE`; `modification_permitted = FALSE`; `verified_by = NULL`; `verified_at = NULL` |
| `media_file` | One row per primary deliverable | `preservation_status = 'pending_retrieval'`; `source_url` present |
| `preservation_event` | One row per rights classification event | `agent_type = 'worker'`; `event_outcome = 'pending_human_review'` |
| `media_technical_metadata` | One row per `source_item` | `validation_status` from `validation_status()` function; `content_hash` present |

### Constitutional invariants at the M36 layer

These invariants apply universally. Violation of any is a constitutional breach.

| Invariant | Rule |
|---|---|
| PD hard gate | `media_rights.commercial_reuse_permitted = FALSE` and `modification_permitted = FALSE` until human sets terminal value |
| Worker status ceiling | `source_item.status` never exceeds `'proposed'` from a worker write |
| FM-4 permanent | No foundation model inference result may write to or influence any `media_rights` column |
| Two-human gate | `rights_status` terminal values (`verified_cc0`, `verified_pd`) require human; worker may not set them |
| Transaction boundary | All six writes must be wrapped in a single DB transaction |
| Evidence completeness | `media_rights.rights_evidence` must contain: `source`, `source_record_id`, `edm_rights_uri` (or equivalent), `rights_matrix_classification`, `applying_policy`, `oai_pmh_identifier` (or equivalent), `raw_payload_hash`, `worker_classified_status`, `evidence_status` |
| REVIEW_REQUIRED workflow | Records classified REVIEW_REQUIRED must generate a `workflow_item` with `capability = 'rights_review'` |
| anchor_type vocabulary | Only `biological`, `geographic`, `cultural`, `mixed` — from set membership derivation or explicit parameter |

### Deliverable

M36 Substrate Verification Report confirming all six tables wired and all invariants satisfied.

### Exit gate

M36 write path: 7 DB writes (ALLOWED record) / 8 DB writes (REVIEW_REQUIRED record).
Zero DB writes on BLOCKED or absent rights. All constitutional invariants confirmed.

---

## Stage 7 — Asset Zero

### Purpose

Prove that a single real record — not a fixture — flows from API fetch through the complete
M36 write path to a human-verified, place-associated, activated state.

### Entry criteria

Stage 6 exit gate cleared. Designated human reviewer confirmed (name and role recorded).

### Process

**7.1 — Fetch a real record**

Use the production API endpoint (not a test fixture). The record must:
- Carry an ALLOWED-class rights URI
- Have a resolvable IIIF URL
- Have a title, date, and at least one subject term
- Be associable with one NC canonical place

**7.2 — Run the full write path**

Execute `write_record()` against the production DB (not a test DB). Confirm:
- `source_item` row created with `status = 'proposed'`
- `media_rights` row created with `rights_status = 'pending_verification'`
- `workflow_item` created only if REVIEW_REQUIRED; not created for ALLOWED
- All 7 writes confirmed in `preservation_event`

**7.3 — Human rights verification**

The designated human reviewer:
1. Retrieves the `source_item` by its `source_identifier`
2. Verifies PD status against the originating institution's open access policy
3. Sets `media_rights.rights_status` to `verified_cc0` or `verified_pd`
4. Sets `media_rights.verified_by` to their identifier
5. Sets `media_rights.verified_at` to the current timestamp
6. Records a `preservation_event` of type `rights_verified`, `agent_type = 'human'`

This step may not be automated. No script may set a terminal rights value.

**7.4 — Place association**

Associate the Asset Zero record with its canonical NC place. The place must be an
existing place page (or a new place page created for this asset). Record the
`place_id` → `source_item_id` link.

**7.5 — IIIF URL confirmation**

Resolve the `media_file.source_url` IIIF endpoint. Confirm it returns a full-resolution
image. Record the resolved URL and HTTP response code in the Asset Zero Report.

**7.6 — Activate the source_item**

After rights verification, advance `source_item.status` to `'activated'`. This is the
only point in the lifecycle where a human may advance status to `'activated'`. Workers
may never set this value.

### Deliverable

**Asset Zero Report** containing:
- Institution slug + source_identifier of the record
- DB row IDs: source_item, source_record, media_file, media_rights, media_technical_metadata
- Rights status at activation: `verified_cc0` or `verified_pd`
- Verified by: human name/identifier + timestamp
- Place association: place_id + place name
- IIIF URL confirmed resolving
- Status: `activated`

### Exit gate

One `source_item` with:
- `status = 'activated'`
- `media_rights.rights_status` in (`verified_cc0`, `verified_pd`)
- `media_rights.verified_by` non-null
- Place association present
- IIIF URL confirmed

---

## Stage 8 — Pilot

### Purpose

Run a capped, scoped, time-limited harvest under active human oversight to validate
success criteria before authorizing full-collection ingestion.

### Entry criteria

Stage 7 Asset Zero exit gate cleared. All success criteria queries from the DD
(SC-1 through SC-N) written and tested against the Asset Zero record.

### Pilot parameters

These parameters are set in the DD at Stage 2. They are institution-specific but must
fall within the following bounds:

| Parameter | Minimum | Maximum | Default |
|---|---|---|---|
| Asset cap | 50 | 500 | 100 |
| Duration | 30 days | 90 days | 90 days |
| Collection scope | 1 set/collection | 3 sets/collections | 1 set |
| Human reviews required | 10 | — | 10% of pilot cap |

### Suspension triggers

Two triggers must be armed before the pilot begins. Triggering either suspends ingestion
immediately and requires Director Decision to resume:

| Trigger | Condition |
|---|---|
| Trigger A | `SELECT COUNT(*) FROM source_item WHERE source_id = '[slug]' AND status = 'proposed'` exceeds pilot cap without human review queue clearing |
| Trigger B | Any `media_rights` row where `worker_classified_status` does not match one of the three expected classes (ALLOWED / REVIEW_REQUIRED / BLOCKED) |

Additional institution-specific triggers may be defined in the DD.

### Pilot execution

Weekly SC-N query evaluation. For each of SC-1 through SC-N:
- Run the SQL query from the DD
- Record pass/fail
- If any SC fails, investigate before continuing

The pilot is not a performance test. It is a governance test. Volume is secondary to
correctness of every row written.

### Deduplication enforcement

If the Discovery Report identified aggregator overlap, the deduplication protocol must
be active during the pilot:
1. For each new direct-institution `source_item` created, check for existing
   aggregator-routed `source_item` with matching `source_identifier` provenance
2. Flag the aggregator `source_item` as superseded via `workflow_item` with
   `capability = 'deduplication_review'`
3. Do not delete the aggregator row — flag only

### Deliverable

**Pilot Report** containing:
- Pilot window (start date → end date)
- Assets ingested: N (must be ≤ cap)
- Human reviews completed: N
- SC-1 through SC-N: each pass/fail with query output
- Suspension triggers: armed/fired/cleared
- Deduplication events: N flagged
- Recommendation: Proceed to Operational / Extend Pilot / Halt

### Exit gate

All SC-1 through SC-N: **pass**. No active suspension trigger. Human reviewer confirms.
Director Decision to proceed.

---

## Stage 9 — Operational

### Purpose

Authorize full-collection ingestion. The institution transitions from pilot to
production. Ongoing monitoring replaces active oversight.

### Entry criteria

Stage 8 Pilot Report with all SC-N pass. Director Decision to proceed.

### Process

**9.1 — Update operational status**

```sql
UPDATE sources
SET operational_status = 'ingesting',
    updated_at = NOW()
WHERE source_id = '[slug]';
```

This is the only authorized `operational_status` transition made outside a ratification
package. It requires Director approval.

**9.2 — Arm full-collection harvest**

Authorize the worker to paginate the full collection. For OAI-PMH: remove the
`--set` scope restriction and enable full `ListRecords` harvest. Rate limits from
the DD source config (`config.rate_limit`) apply permanently.

**9.3 — Coverage matrix update**

Add the institution to the institution coverage matrix with:
- Institution name and slug
- Coverage tier (Tier 1 / 2 / 3)
- Activation date
- Media types active
- Geographic coverage (canonical places)
- Aggregator status (direct / aggregator-supplemented)

**9.4 — Standing suspension triggers**

The Trigger A and Trigger B from Stage 8 remain armed permanently. They are not
pilot-only controls. If either fires in production, the same suspension protocol
applies: halt ingestion, open investigation, Director Decision to resume.

**9.5 — FM-4 permanent confirmation**

Record in the institution's operational record that FM-4 is permanent for this
source. No future worker update, no future amendment, and no future automation
pipeline may write to `media_rights` columns based on model inference for this
institution's assets.

### Deliverable

Operational Record:
- `operational_status = 'ingesting'` confirmed in DB
- Coverage matrix updated
- Suspension triggers armed
- FM-4 confirmation recorded

### Exit gate

None. This stage has no exit — the institution is now permanently operational.
Future governance actions (new media types, new sets, API endpoint changes) are
governed by new DD amendments, not a new factory run.

---

## Constitutional Invariants

These rules apply to every institution at every stage. They may not be
waived by institution-specific governance. Amendment requires a constitutional change
to the authority listed.

| # | Invariant | Rule | Authority |
|---|---|---|---|
| CI-1 | PD hard gate | Only PD/CC0 assets enter the production pipeline. No exception for commercial, educational, or non-commercial licenses. | Strategic Direction v1 |
| CI-2 | Two-human gate | Rights terminal values (`verified_cc0`, `verified_pd`) and Stage 2 ratification each require two independent human approvals. | MSC v1.2 |
| CI-3 | FM-4 permanent | No foundation model inference output may write to or influence any `media_rights` column for any institution. | MSC v1.2 |
| CI-4 | Worker status ceiling | A worker process may not advance `source_item.status` beyond `'proposed'`. Status advancement is a human action. | MSC v1.2 |
| CI-5 | block_if_absent | Absent rights field is classified BLOCKED. It routes to REVIEW_REQUIRED for no institution. | DD-RIJKSMUSEUM-001 A1 |
| CI-6 | anchor_type vocabulary | `source_item.anchor_type` must be one of `biological`, `geographic`, `cultural`, `mixed`. Derivation must come from set membership or explicit parameter — never hardcoded. | DD-RIJKSMUSEUM-001 A1 |
| CI-7 | Transaction boundary | All six M36 table writes for a single record must be wrapped in a single DB transaction. Partial writes are a constitutional violation. | MSC v1.2 |
| CI-8 | Evidence completeness | `media_rights.rights_evidence` must contain all 9 fields: `source`, `source_record_id`, rights URI key, `rights_matrix_classification`, `applying_policy`, record identifier key, `raw_payload_hash`, `worker_classified_status`, `evidence_status`. | DD-RIJKSMUSEUM-001 A1 Art. 3(f) |
| CI-9 | Deduplication protocol | When a direct institution `source_item` is created for an object already present via an aggregator route, the aggregator row must be flagged as superseded via `workflow_item`. Not deleted — flagged. | DD-RIJKSMUSEUM-001 Art. 2(d) |
| CI-10 | No governance shortcut | No worker may create `source_record` rows for an institution whose DD is not ratified. `governance_state` backfills do not constitute ratification for content institutions. | Europeana Activation Checklist v1 |
| CI-11 | REVIEW_REQUIRED workflow | REVIEW_REQUIRED records must produce a `workflow_item` with `capability = 'rights_review'`. They may not silently enter the pipeline without human review queued. | MSC v1.2 |
| CI-12 | Media type phase ordering | New media types may only be activated in the MSC v1.2 Article 5.8 constitutional sequence. Activating a Phase 2 type before Phase 1 is complete is a constitutional violation. | MSC v1.2 Art. 5.8 |

---

## Artifact Registry

This table records the minimum artifacts that must exist at each stage exit gate.
Nothing in the artifact registry may be omitted.

| Stage | Artifact | Location |
|---|---|---|
| 1 | Discovery Report | `docs/decisions/DD-[INST]-000_discovery_report.md` |
| 2 | Decision Document | `docs/decisions/DD-[INST]-001_[name]_production_activation.md` |
| 2 | Amendment(s) if needed | `docs/decisions/DD-[INST]-001-A[N]_[title].md` |
| 2 | Ratification Package | `docs/decisions/DD-[INST]-001_ratification_package.md` |
| 3 | Stage 3 Connectivity confirmation | In Ratification Package addendum or inline |
| 4 | rights.py or re-export | `workers/[slug]_adapter/rights.py` |
| 4 | Rights fixtures (×3 minimum) | `tests/fixtures/[slug]/` |
| 5 | Adapter modules (×4) | `workers/[slug]_adapter/{rights,normalize,technical,store}.py` |
| 5 | Sprint compliance audits | In conversation record or `docs/implementation/[slug]_sprint[N]_compliance.md` |
| 5 | Remediation spec if needed | `docs/implementation/[slug]_sprint[N]_remediation_spec.md` |
| 6 | M36 Substrate Verification | In conversation record or addendum |
| 7 | Asset Zero Report | `docs/architecture/[slug]_asset_zero_report.md` |
| 8 | Pilot Report | `docs/architecture/[slug]_pilot_report.md` |
| 9 | Operational Record | Institution coverage matrix updated |

---

## Naming Conventions

| Entity | Convention | Example |
|---|---|---|
| Institution slug | lowercase, no hyphens | `rijksmuseum`, `nhm`, `bnfgallica` |
| DD identifier | `DD-[SLUG_UPPER]-001` | `DD-NHM-001` |
| Amendment identifier | `DD-[SLUG_UPPER]-001-A[N]` | `DD-NHM-001-A1` |
| Adapter directory | `workers/[slug]_adapter/` | `workers/nhm_adapter/` |
| Fixture directory | `tests/fixtures/[slug]/` | `tests/fixtures/nhm/` |
| Sprint test file | `test_[slug]_adapter_sprint[N].py` | `test_nhm_adapter_sprint3.py` |
| Store test file | `test_[slug]_store.py` | `test_nhm_store.py` |

---

## Reference Implementations

The following implementations are the constitutional archetypes for each component.
When in doubt, follow the archetype.

| Component | Archetype | Location |
|---|---|---|
| Decision Document | DD-RIJKSMUSEUM-001 | `docs/decisions/DD-RIJKSMUSEUM-001_rijksmuseum_production_activation.md` |
| Rights strategy (EDM) | DD-RIJKSMUSEUM-001 A1 | `docs/decisions/DD-RIJKSMUSEUM-001-A1_data_services_platform_amendment.md` |
| Ratification Package | DD-RIJKSMUSEUM-001 Ratification | `docs/decisions/DD-RIJKSMUSEUM-001_ratification_package.md` |
| rights.py (re-export) | Rijksmuseum rights module | `workers/rijksmuseum_adapter/rights.py` |
| rights.py (canonical) | Europeana rights module | `workers/europeana_adapter/rights.py` |
| Metadata normalization | Rijksmuseum EDM module | `workers/rijksmuseum_adapter/edm.py` |
| M36 store | Rijksmuseum store | `workers/rijksmuseum_adapter/store.py` |
| Technical metadata | Rijksmuseum technical | `workers/rijksmuseum_adapter/technical.py` |
| Unit test pattern | Rijksmuseum store tests | `tests/unit/test_rijksmuseum_store.py` |
| Replay test pattern | Rijksmuseum Sprint 4 replay | `tests/replay/test_rijksmuseum_adapter_sprint4.py` |
| Remediation spec | Rijksmuseum Sprint 4 spec | `docs/implementation/rijksmuseum_sprint4_remediation_spec.md` |
| Activation checklist | Europeana Activation Checklist | `docs/governance/europeana_activation_checklist_v1.md` |

---

*Institution Factory v1 — 2026-06-07*
*Authority: All ratified NC constitutions*
*Every future institution follows this path without exception.*
