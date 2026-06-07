# DD-EUR-001 Ratification Package

| Field | Value |
|---|---|
| **Decision ID** | DD-EUR-001 |
| **Package Version** | 1.0 |
| **Status** | Ready for Signature |
| **Repository** | opengracelabs/nc |
| **Drafted** | 2026-06-07 |
| **Ratification Date** | — (to be recorded at signing) |
| **Decision Document** | `docs/decisions/DD-EUR-001_europeana_production_activation.md` |

This package contains every item required to ratify DD-EUR-001. Nothing in this package
requires further design. All governance has been completed. Sign and apply.

---

## Section 1 — Pre-Ratification Confirmation

The Director must confirm all items below before signing. Check each item.

```
GOVERNING DOCUMENTS
[ ] Europeana Rights Matrix v1.0 — ratified 2026-06-07
    File: docs/governance/europeana_rights_matrix_v1.md

[ ] Europeana Activation Checklist v1.0 — ratified 2026-06-07
    File: docs/governance/europeana_activation_checklist_v1.md

[ ] MSC v1.2 — ratified 2026-06-07 (Europeana Tier 1 Reference Institution)
    File: docs/governance/media_substrate_constitution_v1.2.md

[ ] Standards Constitution v1.0 — ratified 2026-06-07 (EDM as Mapped)
    File: docs/governance/standards_constitution_v1.0.md

[ ] CI Constitution v1.2 — ratified (geographic signal substitution available)
    File: docs/governance/commerce_intelligence_constitution_v1.2.md

PREREQUISITES
[ ] Europeana API key validated and functional (creptionce — confirmed 2026-06-07)
[ ] Yellowstone place query returns ≥ 757 PD-eligible results in Europeana API
[ ] docs/decisions/ directory exists for DD record storage
[ ] No prior DD-EUR-001 has been issued (this is the first)

DECISION DOCUMENT
[ ] DD-EUR-001 reviewed in full — all ten articles read and understood
[ ] Article 8 exclusions understood — scope is Yellowstone pilot only, 100-asset cap
[ ] Article 9 gates understood — 6 items must be complete before first ingestion run
```

All items must be checked before proceeding to Section 2.

---

## Section 2 — Director Approval Statement

**Instructions:** The Director reads this statement, confirms it is accurate, and records
approval by entering the ratification date and signing.

---

> I, acting as Director of Nature & Culture (repository: opengracelabs/nc), hereby
> ratify **Director Decision DD-EUR-001 — Europeana Production Activation**.
>
> I confirm:
>
> 1. I have read DD-EUR-001 in its entirety, including all ten articles, the
>    Background, Findings, and Explicit Exclusions.
>
> 2. All prerequisites listed in Section 1 of this ratification package are satisfied.
>
> 3. The Europeana Rights Matrix v1.0 is the governing document for all rights
>    determinations on assets ingested via the Europeana API. I understand that no
>    Europeana-sourced asset may be ingested without a Rights Matrix classification
>    on its `edm:rights` value.
>
> 4. The FM exclusion (FM Constitution v1.0 Invariant FM-4) is permanent. No FM
>    output may influence any `media_rights` record for any Europeana-sourced asset.
>    I understand this cannot be changed by subsequent Director Decision.
>
> 5. This Decision authorizes the Yellowstone pilot only. Production ingestion beyond
>    the Yellowstone pilot query scope, or beyond the 100-asset cap, requires
>    DD-EUR-002. I do not authorize open-ended Europeana ingestion by signing here.
>
> 6. Source registry amendments EU-SR-1 through EU-SR-7 are authorized and must be
>    applied as a single UPDATE before the first ingestion run begins.
>
> 7. The pilot success criteria (SC-1 through SC-8) are the governing evaluation
>    framework. If SC-3 or SC-5 fail, the pilot is immediately suspended.
>    No production expansion proceeds until the pilot is formally reviewed.
>
> **Ratification date:** ___________________________
>
> **Director:** opengracelabs ___________________________

---

## Section 3 — Second-Human Approval Statement

**Instructions:** The second approver reads this statement independently — without
deference to the Director's view — and records approval.

---

> I provide second-human approval for **Director Decision DD-EUR-001 — Europeana
> Production Activation**.
>
> My approval is independent. I have reviewed DD-EUR-001 on its own merits.
>
> I confirm:
>
> 1. The rights governance framework — Europeana Rights Matrix v1.0 — is appropriate
>    and complete for the described use case. The three ALLOWED statements (CC0, PDM,
>    NoC-US) are correctly identified as the commerce-eligible statements under
>    NC's PD hard gate.
>
> 2. The pilot scope (Yellowstone query, 100-asset cap, 90-day window) is reasonable
>    and appropriately constrained for a first production ingestion run.
>
> 3. The two-human activation gate (one for rights verification, one for activation
>    approval) is present in the pipeline design. I confirm that no Europeana-sourced
>    asset may reach `activation_target` status without both approvals.
>
> 4. I have reviewed Article 8 (Explicit Exclusions) and confirm that the scope
>    boundaries are clear and enforceable.
>
> 5. I confirm that the six items in Article 9 (Required Actions Before First
>    Ingestion Run) must all be complete before any production ingestion begins.
>    My approval does not authorize the ingestion run — it authorizes the Decision.
>    The ingestion run requires Article 9 completion.
>
> 6. If pilot criterion SC-3 (BLOCKED filter accuracy) or SC-5 (FM exclusion) fails,
>    the pilot must be immediately suspended. I confirm this understanding.
>
> **Approval date:** ___________________________
>
> **Name:** ___________________________ **Role:** ___________________________

---

## Section 4 — Source Registry Amendments

**Authority:** DD-EUR-001 Article 5
**Applies to:** `sources WHERE source_id = 'europeana'`
**Must be applied:** As a single transaction before the first production ingestion run.

**Verification of current state before applying:**

```sql
-- Run first. Confirm output matches before applying amendment.
SELECT
    source_id,
    entity_types,
    standards,
    config,
    governance_state,
    operational_status
FROM sources
WHERE source_id = 'europeana';
```

Expected current output:

```
source_id    : europeana
entity_types : {cultural_object}
standards    : {cidoc_crm,skos,prov_o,premis}
config       : {"api_endpoint": "https://api.europeana.eu/record/v2",
                "rate_limit": {"requests_per_second": 2, "burst": 10}}
governance_state   : active
operational_status : healthy
```

If the output does not match, do not apply the amendment. Investigate the discrepancy first.

---

**Amendment SQL — EU-SR-1 through EU-SR-7:**

```sql
-- DD-EUR-001 Article 5 — Source Registry Amendments EU-SR-1 through EU-SR-7
-- Authorized by: DD-EUR-001
-- Ratification date: <insert date>
-- Applied by: <insert name>
-- Applied at: <insert timestamp>

BEGIN;

UPDATE sources
SET
    -- EU-SR-5: Add 'edm' to standards array
    standards    = ARRAY['cidoc_crm', 'skos', 'prov_o', 'premis', 'edm'],

    -- EU-SR-6: Expand entity_types to Phase 1 media types
    entity_types = ARRAY['cultural_object', 'image', 'photography', 'map', 'illustration'],

    -- EU-SR-1 through EU-SR-4, EU-SR-7: Config amendments (merged onto existing config)
    config       = '{
        "api_endpoint":      "https://api.europeana.eu/record/v2",
        "auth_key_env":      "EUROPEANA_API_KEY",
        "rate_limit":        {"requests_per_second": 2, "burst": 10},
        "rights_strategy":   "rights_matrix_filtered",
        "source_role":       "aggregator",
        "completeness_minimum": 4,
        "edm_tripartite":    true,
        "rights_filter": {
            "mode":      "pre_ingestion",
            "authority": "europeana_rights_matrix_v1",
            "allowed_uris": [
                "http://creativecommons.org/publicdomain/zero/1.0/",
                "http://creativecommons.org/publicdomain/mark/1.0/",
                "http://rightsstatements.org/vocab/NoC-US/1.0/"
            ],
            "review_required_uris": [
                "http://rightsstatements.org/vocab/NoC-CR/1.0/",
                "http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
                "http://rightsstatements.org/vocab/NKC/1.0/"
            ],
            "filter_mode": "strict"
        }
    }'::jsonb,

    updated_at   = NOW()

WHERE source_id = 'europeana';

COMMIT;
```

**Verification of post-amendment state:**

```sql
-- Run after applying. Confirm all seven amendments are present.
SELECT
    'EU-SR-1' AS amendment,
    config->>'rights_strategy' = 'rights_matrix_filtered' AS applied
FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-2', config->>'source_role' = 'aggregator'
FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-3', (config->>'completeness_minimum')::int = 4
FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-4', config->'rights_filter' IS NOT NULL
FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-5', 'edm' = ANY(standards)
FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-6', 'photography' = ANY(entity_types)
FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-7', (config->>'edm_tripartite')::boolean = true
FROM sources WHERE source_id = 'europeana';
```

All seven rows must return `applied = true`. If any returns `false`, the amendment
is incomplete. Do not begin ingestion until all seven return `true`.

**Applied by:** ___________________________ **Date/time:** ___________________________

---

## Section 5 — Pilot Scope Controls

These are the operational parameters that govern the pilot ingestion run.
They derive directly from DD-EUR-001 Article 6. No modification is permitted.

### 5.1 — Query Parameters

```
Europeana Record API v2
Endpoint:   https://api.europeana.eu/record/v2/search.json
API key:    $EUROPEANA_API_KEY  (from .env — never committed to git)

Required parameters:
  query    = yellowstone
  qf       = TYPE:IMAGE
  rows     = 100  (maximum per request; paginate if needed)
  profile  = rich

Rights filter (applied server-side):
  rights   = http://creativecommons.org/publicdomain/zero/1.0/
           OR http://creativecommons.org/publicdomain/mark/1.0/
           OR http://rightsstatements.org/vocab/NoC-US/1.0/
           OR http://rightsstatements.org/vocab/NoC-CR/1.0/
           OR http://rightsstatements.org/vocab/NoC-OKLR/1.0/
           OR http://rightsstatements.org/vocab/NKC/1.0/

Completeness:
  f.COMPLETENESS.min = 4

Note: The server-side rights filter includes REVIEW REQUIRED statements
(NoC-CR, NoC-OKLR, NKC) to allow them into the pipeline for workflow_item creation.
The pre-ingestion worker filter then separates ALLOWED from REVIEW REQUIRED.
BLOCKED statements are excluded server-side by omission from the rights parameter.
```

### 5.2 — Asset Cap Enforcement

The pilot is capped at **100 assets that pass the pre-ingestion gate**. BLOCKED
assets rejected at the pre-ingestion filter do not count toward the cap.

Cap enforcement rule:
```
ingested_count = COUNT(source_record) WHERE source = 'europeana'
                 AND created_at >= <pilot_start_date>

If ingested_count >= 100:
  STOP ingestion.
  Log: "DD-EUR-001 pilot cap reached. Awaiting DD-EUR-002 for continuation."
  Do not ingest further assets under DD-EUR-001.
```

### 5.3 — Pilot Window

```
Pilot start:  Date of first production ingestion run after Article 9 gates are complete
Pilot end:    90 calendar days after pilot start, OR when 100-asset cap is reached,
              whichever comes first.
Pilot review: Within 14 calendar days of pilot end.
```

Pilot start date (record here): ___________________________

Pilot end date (90 days from start): ___________________________

### 5.4 — Place Association Control

Every asset ingested under DD-EUR-001 must be associated with Yellowstone National Park
before it may advance to `activation_eligible`.

```
Required association:
  places.geonames_id = 5843591   (Yellowstone National Park)
  places.wikidata_qid = 'Q351'

If an asset cannot be associated with Yellowstone (e.g., a Europeana result that
appeared in the query but depicts an unrelated subject):
  → Discard at ingestion. Do not create source_record.
  → Log: reason for discard, Europeana record ID.
  → Do not count toward pilot cap.
```

---

## Section 6 — Pilot Suspension Criteria

Two criteria are constitutional. Failure on either suspends the pilot immediately.
Four criteria are operational. Failure on operational criteria triggers remediation
without suspension.

### 6.1 — Constitutional Suspension Triggers (immediate)

These are not performance failures. They are constitutional violations.

**Trigger A — SC-3 failure: BLOCKED asset entered the pipeline**

```
Condition: Any source_record row exists WHERE source = 'europeana'
           AND the edm:rights value from the raw_payload
           maps to a BLOCKED classification in the Rights Matrix.

Response:
  1. Immediately halt all Europeana ingestion worker processes.
  2. Record preservation_event: event_type='rights_verification',
     event_outcome='violation', event_detail='BLOCKED asset in pipeline — pilot suspended'.
  3. Open a governance incident workflow_item: item_type='governance_incident'.
  4. Do not resume ingestion until the incident is resolved and the pre-ingestion
     filter is verified to be operating correctly.
  5. Notify the Director.
```

**Trigger B — SC-5 failure: FM output connected to rights determination**

```
Condition: Any fm_candidate_record row exists WHERE use_case_id = 'rights_analysis_advisory'
           AND (
             the candidate_record is referenced in any workflow_item.item_payload
             for item_type = 'rights_review',
             OR any media_rights row for a Europeana-sourced source_item has
             a preservation_event that references an fm_candidate_record
           ).

Response:
  1. Immediately halt all Europeana ingestion and rights review processes.
  2. Record preservation_event: event_type='rights_verification',
     event_outcome='violation', event_detail='FM output connected to rights — FM-4 violated'.
  3. Open a governance incident workflow_item: item_type='governance_incident'.
  4. The incident must be reviewed by the Director before any rights review resumes.
  5. Notify the Director.
```

### 6.2 — Operational Remediation Triggers (no suspension)

Failure on any of the following triggers a remediation process. Ingestion may continue
during remediation unless the Principal Architect determines suspension is warranted.

| Trigger | Condition | Response |
|---|---|---|
| SC-1 below threshold | Fewer than 10 activation_targets at pilot end | Review pipeline for bottlenecks in rights review or activation approval queue |
| SC-2 gap | Any verified_pd/verified_cc0 record lacking required evidence | Rights reviewer must supply missing evidence; cannot proceed to activation without it |
| SC-4 gap | Any activation_target lacking place_id for Europeana assets | Halt activation approval for ungeolocated assets; do not count toward SC-1 |
| SC-6 gap | Any activation_target without asset_opportunities record | Commerce scoring worker has failed; investigate before further activation approval |
| SC-7 violation log | Any preservation_event with event_outcome='violation' (non-constitutional) | Investigate cause; remediate and re-run affected step |
| SC-8 error rate | > 20% of ingested assets fail pipeline completion | Pause ingestion; debug worker errors before continuing |

---

## Section 7 — Success Criteria Sign-Off Checklist

**Purpose:** This checklist is completed by the Principal Architect after the pilot
window closes, then reviewed by the Director for DD-EUR-002 decision.

**Pilot end date:** ___________________________

**Completed by (Principal Architect):** ___________________________

---

### SC-1 — Activated Assets

**Threshold:** ≥ 10 assets reach `activation_target` status with second-human approval.

```sql
-- Measurement query
SELECT COUNT(*)
FROM activation_targets at
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'europeana'
  AND at.status IN ('active', 'activated');
```

Result: _____ assets

Pass threshold (≥ 10)? [ ] Yes  [ ] No

If No — remediation action taken: ___________________________

---

### SC-2 — Rights Verification Completeness

**Threshold:** 100% of `activation_eligible` assets have documented rights evidence
in `media_rights.rights_evidence` with required fields per Rights Matrix HR-4.

```sql
-- Measurement query
SELECT
    COUNT(*) FILTER (WHERE rights_evidence IS NOT NULL
                      AND rights_evidence != '{}'::jsonb) AS with_evidence,
    COUNT(*) AS total_verified,
    COUNT(*) FILTER (WHERE rights_evidence IS NULL
                      OR rights_evidence = '{}'::jsonb) AS missing_evidence
FROM media_rights mr
JOIN source_items si ON si.id = mr.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'europeana'
  AND mr.rights_status IN ('verified_pd', 'verified_cc0');
```

Total verified: _____ With evidence: _____ Missing evidence: _____

Pass threshold (missing = 0)? [ ] Yes  [ ] No

If No — missing evidence supplied: [ ] Yes  [ ] No (cannot proceed to sign-off if No)

---

### SC-3 — BLOCKED Filter Accuracy

**Threshold:** 100% of BLOCKED-classified assets rejected at pre-ingestion gate.
Zero BLOCKED-statement assets in `source_record` table.

```sql
-- Measurement query: check for any source_records where the raw_payload
-- edm:rights value maps to a BLOCKED classification.
-- Requires worker-level logging of rejected assets.
SELECT COUNT(*) AS blocked_rejections_logged
FROM worker_logs  -- or equivalent audit table
WHERE source = 'europeana'
  AND log_type = 'pre_ingestion_blocked'
  AND created_at >= '<pilot_start_date>';
```

Blocked assets rejected at pre-ingestion gate: _____

Any BLOCKED assets found in source_record? [ ] None found  [ ] Violations found

Pass threshold (no violations)? [ ] Yes  [ ] No

If No — **PILOT SUSPENDED** — do not complete this checklist until constitutional
incident (Trigger A, Section 6.1) is resolved.

---

### SC-4 — Place Association

**Threshold:** 100% of activated assets associated with Yellowstone
(`places.geonames_id = 5843591`).

```sql
-- Measurement query
SELECT
    COUNT(*) FILTER (WHERE p.geonames_id = '5843591') AS with_yellowstone,
    COUNT(*) FILTER (WHERE p.geonames_id != '5843591'
                      OR p.id IS NULL) AS missing_association,
    COUNT(*) AS total_activated
FROM activation_targets at
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
LEFT JOIN places p ON p.id = at.place_id
WHERE sr.source = 'europeana';
```

Total activated: _____ With Yellowstone: _____ Missing: _____

Pass threshold (missing = 0)? [ ] Yes  [ ] No

---

### SC-5 — FM Exclusion

**Threshold:** Zero FM output connected to any rights determination.

```sql
-- Measurement query
SELECT COUNT(*) AS potential_violations
FROM fm_candidate_records fcr
WHERE fcr.use_case_id = 'rights_analysis_advisory'
  AND EXISTS (
    SELECT 1 FROM workflow_items wi
    WHERE wi.item_type = 'rights_review'
      AND wi.item_payload::text LIKE '%' || fcr.candidate_id::text || '%'
  );
```

Potential FM-rights connections found: _____

Any FM output connected to rights determination? [ ] None found  [ ] Violations found

Pass threshold (no violations)? [ ] Yes  [ ] No

If No — **PILOT SUSPENDED** — do not complete this checklist until constitutional
incident (Trigger B, Section 6.1) is resolved.

---

### SC-6 — Commerce Coverage

**Threshold:** 100% of activated assets have COS calculated and CSM tier assigned.

```sql
-- Measurement query
SELECT
    COUNT(*) FILTER (WHERE ao.id IS NOT NULL) AS with_score,
    COUNT(*) FILTER (WHERE ao.id IS NULL) AS missing_score,
    COUNT(*) AS total_activated
FROM activation_targets at
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
LEFT JOIN asset_opportunities ao ON ao.source_item_id = si.id
WHERE sr.source = 'europeana';
```

Total activated: _____ With COS: _____ Missing: _____

Pass threshold (missing = 0)? [ ] Yes  [ ] No

---

### SC-7 — Constitutional Integrity

**Threshold:** Zero constitutional violations logged in preservation events for
Europeana-sourced assets during the pilot window.

```sql
-- Measurement query
SELECT COUNT(*) AS violations
FROM preservation_events pe
JOIN source_items si ON si.id = pe.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'europeana'
  AND pe.event_outcome = 'violation'
  AND pe.created_at >= '<pilot_start_date>';
```

Constitutional violations logged: _____

Pass threshold (violations = 0)? [ ] Yes  [ ] No

---

### SC-8 — Pipeline Completion Rate

**Threshold:** ≥ 80% of ingested assets complete all pipeline gates without worker error.

```sql
-- Measurement query (approximate — depends on worker error logging)
SELECT
    COUNT(*) AS total_ingested,
    COUNT(*) FILTER (WHERE si.status = 'activation_eligible'
                      OR at.id IS NOT NULL) AS completed_pipeline,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE si.status = 'activation_eligible'
                                  OR at.id IS NOT NULL)
        / NULLIF(COUNT(*), 0), 1
    ) AS completion_rate_pct
FROM source_records sr
LEFT JOIN source_items si ON si.source_record_id = sr.id
LEFT JOIN activation_targets at ON at.source_item_id = si.id
WHERE sr.source = 'europeana'
  AND sr.created_at >= '<pilot_start_date>';
```

Total ingested: _____ Completed pipeline: _____ Completion rate: _____%

Pass threshold (≥ 80%)? [ ] Yes  [ ] No

---

### Overall Pilot Assessment

SC criteria passed: _____ / 8

Constitutional criteria (SC-3, SC-5): [ ] Both passed  [ ] Suspension event occurred

Recommendation:

[ ] **PROCEED to DD-EUR-002** — All 8 criteria met. Pilot successful.
    Recommend scope expansion to additional Europeana place categories.

[ ] **REMEDIATE and EXTEND** — Operational criteria failures (not SC-3/SC-5).
    Address remediation items. Extend pilot window. Re-evaluate before DD-EUR-002.

[ ] **INVESTIGATE** — Constitutional criteria failure. Pilot suspended.
    Do not recommend DD-EUR-002 until constitutional incident resolved.

**Principal Architect signature:** ___________________________ **Date:** ___________

**Director sign-off on pilot review:** ___________________________ **Date:** ___________

---

## Section 8 — Post-Ratification Action Register

Complete these steps in order after DD-EUR-001 is ratified (both signatures recorded).

```
IMMEDIATELY AFTER RATIFICATION (before any implementation begins)
[ ] Record ratification date in DD-EUR-001 document header
[ ] Record ratification date in memory: project_europeana_activation.md
[ ] Confirm docs/decisions/ commit includes both DD-EUR-001 and this package

GATE 2 — SOURCE REGISTRY (before first ingestion run)
[ ] Run pre-amendment verification query (Section 4) — confirm current state matches expected
[ ] Apply EU-SR-1 through EU-SR-7 in single transaction (SQL in Section 4)
[ ] Run post-amendment verification query (Section 4) — confirm all 7 rows return applied=true
[ ] Record applier name and timestamp in Section 4 of this document

GATE 3 — RIGHTS WORKFLOW (before first ingestion run)
[ ] Europeana ingestion worker updated — pre-ingestion rights filter implemented
[ ] At least one human reviewer authorized for rights_review workflow items
[ ] FM exclusion confirmed in writing — confirmation recorded here: ___________________________
[ ] 30-day NKC deadline operationalized

GATE 4+ — INGESTION AND ACTIVATION
[ ] Record pilot start date in Section 5.3
[ ] Record pilot end date (90 days from start) in Section 5.3
[ ] First ingestion run executed within pilot scope (Section 5.1)
[ ] At pilot end: complete Section 7 sign-off checklist
[ ] Submit pilot review to Director for DD-EUR-002 decision
```

---

*DD-EUR-001 Ratification Package v1.0 — drafted 2026-06-07*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs) + Second Human Approver*
