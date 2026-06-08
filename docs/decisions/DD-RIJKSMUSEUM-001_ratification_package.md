# DD-RIJKSMUSEUM-001 Ratification Package

| Field | Value |
|---|---|
| **Decision ID** | DD-RIJKSMUSEUM-001 + Amendment A1 |
| **Package Version** | 1.0 |
| **Status** | Ready for Signature |
| **Repository** | opengracelabs/nc |
| **Drafted** | 2026-06-07 |
| **Ratification Date** | — (to be recorded at signing) |
| **Decision Document** | `docs/decisions/DD-RIJKSMUSEUM-001_rijksmuseum_production_activation.md` |
| **Amendment Document** | `docs/decisions/DD-RIJKSMUSEUM-001-A1_data_services_platform_amendment.md` |

This package contains every item required to ratify DD-RIJKSMUSEUM-001 and its
concurrent Amendment A1. Both documents are ratified together as a single act.
Nothing in this package requires further design. All governance has been completed.
Sign and apply.

---

## Section 1 — Pre-Ratification Confirmation

The Director must confirm all items below before signing. Check each item.

```
GOVERNING DOCUMENTS
[ ] Europeana Rights Matrix v1.0 — ratified 2026-06-07
    File: docs/governance/europeana_rights_matrix_v1.md
    Note: This document governs Rijksmuseum edm:rights classification.
          It was drafted for Europeana and applies identically to
          Rijksmuseum OAI-PMH EDM records. No separate rights matrix
          is required for Rijksmuseum.

[ ] Institution Coverage Audit v1.0 — ratified 2026-06-07
    File: docs/governance/institution_coverage_audit_v1.md
    Note: Rijksmuseum rated Grade A (CC0), Wave 3, high priority.
          This audit is the source of the Wave 3 designation.

[ ] MSC v1.2 — ratified 2026-06-07 (IIIF Tier 1 Reference Institution)
    File: docs/governance/media_substrate_constitution_v1.2.md

[ ] Standards Constitution v1.0 — ratified 2026-06-07
    File: docs/governance/standards_constitution_v1.0.md
    Note: EDM is recognized as a mapped standard (via Europeana).
          IIIF is authorized in sources.standards by DD-RIJKSMUSEUM-001
          Article 4. SA-4 (formal IIIF Presentation manifest standard)
          is NOT required for pilot activation — deferred.

[ ] CI Constitution v1.2 — ratified (signal_substitutions available)
    File: docs/governance/commerce_intelligence_constitution_v1.2.md

PLATFORM PREREQUISITES
[ ] OAI-PMH endpoint confirmed live and accessible — no API key required
    Test: curl -s "https://data.rijksmuseum.nl/oai?verb=Identify"
    Expected: <repositoryName>Rijksmuseum OAI-PMH API</repositoryName>
    Confirmed: 2026-06-07

[ ] OAI-PMH EDM format confirmed available
    Test: curl -s "https://data.rijksmuseum.nl/oai?verb=ListMetadataFormats"
    Expected: metadataPrefix 'edm' listed
    Confirmed: 2026-06-07

[ ] OAI-PMH set 261222 (papier collectie) confirmed accessible
    Test: curl -s "https://data.rijksmuseum.nl/oai?verb=ListIdentifiers&metadataPrefix=edm&set=261222"
    Expected: ≥ 1 identifier returned
    Confirmed: 2026-06-07 (identifiers returned)

[ ] OAI-PMH EDM record contains edm:rights URI
    Test: GetRecord on any identifier from set 261222 with metadataPrefix=edm
    Expected: ore:Aggregation/edm:rights element present
    Confirmed: 2026-06-07 (edm:rights = PDM on record 200105955)

[ ] IIIF delivery on iiif.micr.io confirmed
    Test: Inspect edm:object WebResource svcs:has_service in any EDM record
    Expected: https://iiif.micr.io/{id} URI pattern
    Confirmed: 2026-06-07

DATABASE PREREQUISITES
[ ] Rijksmuseum not yet in sources table
    Test: SELECT COUNT(*) FROM sources WHERE source_id = 'rijksmuseum';
    Expected: 0 rows

[ ] Migration 17 applied — governance columns present on sources table
    Test: SELECT governance_state FROM sources LIMIT 1;
    Expected: query succeeds (column exists)
    Note: If this query fails, apply 17_source_governance.sql before ratification.
          Do NOT remove governance_state from RU-SR-1 SQL as a workaround.

[ ] M36 substrate tables confirmed live
    Test: SELECT COUNT(*) FROM media_type_registry;
    Expected: 11 rows (deployed 2026-06-07 — commit 7288b59)

[ ] No prior DD-RIJKSMUSEUM-001 has been ratified (this is the first)

DECISION DOCUMENTS
[ ] DD-RIJKSMUSEUM-001 reviewed in full — all eleven articles read and understood
[ ] DD-RIJKSMUSEUM-001-A1 reviewed in full — all amended articles read and understood
[ ] Article 9 gates understood — 7 items must be complete before first ingestion run
[ ] Article 10 exclusions understood — pilot is natural history prints only, 100-asset cap
[ ] Amendment A1 co-ratification understood — both documents ratified simultaneously
```

All items must be checked before proceeding to Section 2.

---

## Section 2 — Director Approval Statement

**Instructions:** The Director reads this statement, confirms it is accurate, and records
approval by entering the ratification date and signing.

---

> I, acting as Director of Nature & Culture (repository: opengracelabs/nc), hereby
> ratify **Director Decision DD-RIJKSMUSEUM-001 — Rijksmuseum Production Activation**
> and its concurrent **Amendment A1 — Data Services Platform Amendment**.
> I ratify both documents as a single act. Neither document takes effect independently.
>
> I confirm:
>
> 1. I have read DD-RIJKSMUSEUM-001 in its entirety, including all eleven articles,
>    the Background, Findings, and Explicit Exclusions. I have read Amendment A1 in
>    its entirety, including all triggering findings and all amended articles.
>
> 2. All prerequisites listed in Section 1 of this ratification package are satisfied,
>    including the live confirmation of the Rijksmuseum Data Services OAI-PMH endpoint
>    and the presence of the `edm:rights` field in EDM records.
>
> 3. The Europeana Rights Matrix v1.0 is the governing document for all rights
>    determinations on assets ingested via the Rijksmuseum OAI-PMH EDM surface.
>    I understand that no Rijksmuseum-sourced asset may enter the pipeline without
>    an `edm:rights` URI that classifies as ALLOWED or REVIEW REQUIRED under
>    that Matrix. There is no `permitDownload` field in the new platform.
>
> 4. The FM exclusion (FM Constitution v1.0 Invariant FM-4) is permanent for all
>    Rijksmuseum-sourced assets. No FM output may influence any `media_rights` record
>    for any Rijksmuseum-sourced asset. I understand this cannot be changed by
>    subsequent Director Decision.
>
> 5. This Decision authorises the natural history illustration pilot only, using
>    OAI-PMH set 261222 as the primary harvest source. Production ingestion beyond
>    the pilot query scope, the 100-asset cap, or the 90-day window requires
>    DD-RIJKSMUSEUM-002. I do not authorise open-ended Rijksmuseum ingestion
>    by signing here.
>
> 6. Source registry amendment RU-SR-1 (Revised per A1) is authorised and must be
>    applied as a single INSERT transaction before the first ingestion run begins.
>    It is an INSERT, not an UPDATE — the Rijksmuseum is not yet in the sources table.
>
> 7. OAI-PMH EDM is the primary pilot ingest surface. The old
>    `www.rijksmuseum.nl/api/{lang}/collection` endpoint is superseded and not
>    authorised for NC use.
>
> 8. Place association for Rijksmuseum assets is not required at ingestion time.
>    It is required before `activation_eligible`. The human activation reviewer
>    is responsible for assigning at least one `places` record before any Rijksmuseum
>    asset may advance.
>
> 9. The pilot success criteria (SC-1 through SC-8) are the governing evaluation
>    framework. If SC-3 (BLOCKED filter accuracy) or SC-5 (FM exclusion) fail,
>    the pilot is immediately suspended. No production expansion proceeds until
>    the pilot is formally reviewed.
>
> 10. I understand that the existing `europeana_adapter/rights.py` `classify_rights()`
>     function is directly reusable for Rijksmuseum `edm:rights` classification, and
>     that this reuse is authorised by this Decision.
>
> **Ratification date:** ___________________________
>
> **Director:** opengracelabs ___________________________

---

## Section 3 — Second-Human Approval Statement

**Instructions:** The second approver reads this statement independently — without
deference to the Director's view — and records approval.

---

> I provide second-human approval for **Director Decision DD-RIJKSMUSEUM-001 —
> Rijksmuseum Production Activation** and its Amendment A1.
>
> My approval is independent. I have reviewed DD-RIJKSMUSEUM-001 and Amendment A1
> on their own merits.
>
> I confirm:
>
> 1. The rights governance framework — Europeana Rights Matrix v1.0 applied to
>    Rijksmuseum `edm:rights` — is appropriate and complete. The three ALLOWED
>    statements (CC0, PDM, NoC-US) correctly identify the commerce-eligible rights
>    statements under NC's PD hard gate. PDM is the expected primary value for
>    Dutch Golden Age works; CC0 applies where the Rijksmuseum has explicitly waived
>    rights to its digitisation.
>
> 2. Amendment A1's replacement of the `permitDownload` gate with `edm:rights`
>    classification is appropriate. The `edm:rights` URI provides equivalent or
>    superior authoritative rights attestation from the Rijksmuseum for OAI-PMH EDM
>    records. No rights information is lost in this change.
>
> 3. The pilot scope — OAI-PMH set 261222 (papier collectie), natural history
>    subject filter, 100-asset cap, 90-day window — is reasonable and appropriately
>    constrained for a first production Rijksmuseum ingestion run.
>
> 4. The two-human activation gate is present: one human for rights verification,
>    one for activation approval. I confirm that no Rijksmuseum-sourced asset may
>    reach `activation_target` status without both approvals.
>
> 5. I have reviewed Article 10 (Explicit Exclusions) and confirm the scope
>    boundaries are clear and enforceable: `permitDownload: false`-equivalent
>    objects (BLOCKED-class `edm:rights`), OAI-PMH without EDM format, IIIF
>    Presentation manifests as schema_standard, and all Phase 2–4 media types
>    are excluded from this Decision.
>
> 6. I confirm that the seven items in Article 9 (Required Actions Before First
>    Ingestion Run) must all be complete before any production ingestion begins.
>    My approval does not authorise the ingestion run — it authorises the Decision.
>
> 7. If pilot criterion SC-3 (BLOCKED filter accuracy) or SC-5 (FM exclusion) fails,
>    the pilot must be immediately suspended. I confirm this understanding.
>
> 8. I note that the `activation_target` table (M36-014) was deferred in the current
>    M36 deployment. Success criteria SC-1 and SC-4 are contingent on M36-014 being
>    implemented before the pilot concludes. This does not block pilot activation —
>    it is recorded as a known dependency.
>
> **Approval date:** ___________________________
>
> **Name:** ___________________________ **Role:** ___________________________

---

## Section 4 — Source Registry Amendment

**Authority:** DD-RIJKSMUSEUM-001 Article 6 + Amendment A1
**Applies to:** `sources` table — new row INSERT
**Must be applied:** As a single INSERT transaction, after both signatures are recorded,
and after Migration 17 is confirmed applied (Section 1 prerequisite).

**Pre-INSERT verification — confirm no existing row:**

```sql
SELECT COUNT(*) FROM sources WHERE source_id = 'rijksmuseum';
-- Expected: 0 rows.
-- If 1 row returned: do not INSERT. Investigate.
```

**Migration 17 verification — confirm governance columns exist:**

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'sources'
  AND column_name IN ('governance_state', 'operational_status');
-- Expected: 2 rows.
-- If 0 rows: apply 17_source_governance.sql before proceeding.
```

---

**Amendment SQL — RU-SR-1 (Revised per A1):**

```sql
-- DD-RIJKSMUSEUM-001 Article 6 + A1 — Source Registry Amendment RU-SR-1
-- Authorised by: DD-RIJKSMUSEUM-001 + A1
-- Ratification date: <insert date>
-- Applied by: <insert name>
-- Applied at: <insert timestamp>

INSERT INTO sources (
    source_id,
    name,
    description,
    institution,
    base_url,
    fetch_strategy,
    auth_type,
    priority,
    entity_types,
    standards,
    governance_state,
    operational_status,
    status,
    config,
    provenance,
    created_at,
    updated_at
) VALUES (
    'rijksmuseum',
    'Rijksmuseum',
    'Royal Museum of the Netherlands. Dutch Golden Age art, natural history illustration, cartography, and decorative arts. CC0/PDM Open Access via Rijksmuseum Data Services.',
    'Rijksmuseum Amsterdam',
    'https://data.rijksmuseum.nl',
    'api',
    'none',
    3,
    ARRAY['image', 'photography', 'map'],
    ARRAY['cidoc_crm', 'skos', 'prov_o', 'premis', 'dc', 'edm', 'iiif'],
    'active',
    'unavailable',
    'active',
    '{
        "collection_api_endpoint":  "https://data.rijksmuseum.nl/search/collection",
        "collection_api_format":    "linked_art_ordered_collection",
        "oai_pmh_endpoint":         "https://data.rijksmuseum.nl/oai",
        "oai_pmh_primary_format":   "edm",
        "oai_pmh_formats":          ["edm", "oai_dc"],
        "iiif_service_host":        "https://iiif.micr.io",
        "iiif_id_source":           "edm_svcs_has_service",
        "auth_type":                "none",
        "auth_key_env":             null,
        "rate_limit":               {"requests_per_second": 5, "burst": 20},
        "rights_strategy":          "edm_rights_matrix",
        "source_role":              "institution",
        "schema_standard":          "edm",
        "identifier_format":        "uri",
        "identifier_pattern":       "https://id.rijksmuseum.nl/{id}",
        "legacy_identifier_field":  "dc:identifier",
        "oai_pmh_deleted_policy":   "persistent",
        "completeness_minimum":     6,
        "rights_filter": {
            "mode":                 "pre_ingestion",
            "authority":            "europeana_rights_matrix_v1.0",
            "rights_field":         "edm:rights",
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
            "filter_mode":          "strict",
            "block_if_absent":      true
        }
    }'::jsonb,
    '{"nc:authority": "DD-RIJKSMUSEUM-001+A1", "nc:activation_date": "<insert date>"}'::jsonb,
    NOW(),
    NOW()
);
```

**Post-INSERT verification:**

```sql
SELECT
    'RU-SR-1' AS amendment,
    source_id = 'rijksmuseum'                                   AS row_inserted
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-2 auth_type=none',
    config->>'auth_type' = 'none'
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-3 rights_strategy=edm_rights_matrix',
    config->>'rights_strategy' = 'edm_rights_matrix'
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-4 oai_pmh_endpoint',
    config->>'oai_pmh_endpoint' = 'https://data.rijksmuseum.nl/oai'
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-5 rights_field=edm:rights',
    config->'rights_filter'->>'rights_field' = 'edm:rights'
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-6 edm in standards',
    'edm' = ANY(standards)
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-7 iiif in standards',
    'iiif' = ANY(standards)
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-8 no api key',
    config->>'auth_key_env' = 'null' OR config->>'auth_key_env' IS NULL
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-9 governance_state=active',
    governance_state = 'active'
FROM sources WHERE source_id = 'rijksmuseum'
UNION ALL
SELECT 'RU-SR-10 source_role=institution',
    config->>'source_role' = 'institution'
FROM sources WHERE source_id = 'rijksmuseum';
-- All 10 rows must return true.
```

All ten rows must return `true`. If any returns `false`, the amendment is
incomplete. Do not begin ingestion until all ten return `true`.

**Applied by:** ___________________________ **Date/time:** ___________________________

---

## Section 5 — Pilot Scope Controls

These are the operational parameters that govern the pilot ingestion run.
They derive directly from DD-RIJKSMUSEUM-001 Articles 7 and 8 (as amended by A1).
No modification is permitted without DD-RIJKSMUSEUM-002.

### 5.1 — Harvest Parameters

```
Rijksmuseum OAI-PMH
Endpoint:       https://data.rijksmuseum.nl/oai
Auth:           None (no API key required)
Verb:           ListRecords
metadataPrefix: edm
set:            261222   (papier collectie — primary)

Expansion set (if 100-asset cap not reached from 261222 alone):
set:            26112    (Dutch Drawings of the Seventeenth Century)

Pre-ingestion filter (applied by worker before source_record creation):
  edm:rights present                     → BLOCK if absent
  edm:rights classifies ALLOWED or       → BLOCK if BLOCKED-class
    REVIEW_REQUIRED per Rights Matrix v1.0
  edm:type = IMAGE                        → BLOCK if absent or non-IMAGE
  svcs:has_service URI present            → BLOCK if absent (no IIIF delivery)
  dcterms:extent present                  → BLOCK if absent (no dimensions)
  dc:title present                        → BLOCK if absent (mandatory field)

Assets failing any pre-ingestion filter: logged, do not count toward 100-asset cap.
```

### 5.2 — Asset Cap Enforcement

The pilot is capped at **100 assets that pass the pre-ingestion gate**.

```sql
-- Cap enforcement check (run before each ingestion batch)
SELECT COUNT(*) AS ingested_count
FROM source_item si
WHERE si.source_id = 'rijksmuseum'
  AND si.created_at >= '<pilot_start_date>';

-- If ingested_count >= 100:
--   STOP ingestion.
--   Log: "DD-RIJKSMUSEUM-001 pilot cap reached. Awaiting DD-RIJKSMUSEUM-002."
--   Do not ingest further assets under DD-RIJKSMUSEUM-001.
```

### 5.3 — Pilot Window

```
Pilot start:   Date of first production ingestion run after Article 9 gates complete
Pilot end:     90 calendar days after pilot start, OR when 100-asset cap is reached,
               whichever comes first.
Pilot review:  Within 14 calendar days of pilot end.
```

Pilot start date (record here): ___________________________

Pilot end date (90 days from start): ___________________________

### 5.4 — Place Association Control

Rijksmuseum place association is **not required at ingestion time**. It is required
before `activation_eligible`. The human activation reviewer is responsible.

```
At activation review, the reviewer must:
  1. Identify at least one NC places record relevant to the object's subject matter.
  2. Assign the place association before advancing the asset.
  3. If no relevant place can be identified:
     → Return asset to 'rights_verified' status.
     → Log reason in the workflow_item.
     → Do not advance to activation_eligible.
     → Asset does not count toward SC-1.
```

### 5.5 — IIIF Image URL Resolution

IIIF delivery is via `iiif.micr.io`. The IIIF ID must be read from the EDM record.

```
For each OAI-PMH EDM record:
  1. Parse edm:object → edm:WebResource → svcs:has_service
     → extract: https://iiif.micr.io/{iiif_id}
  2. Retrieve: https://iiif.micr.io/{iiif_id}/info.json
  3. Verify longest edge ≥ 400px (MSC v1.2 Article 29.2(d))
  4. If info.json unreachable or dimensions < 400px → BLOCK at pre-ingestion

media_file.source_url = https://iiif.micr.io/{iiif_id}/full/max/0/default.jpg
```

---

## Section 6 — Pilot Suspension Criteria

Two criteria are constitutional. Failure on either suspends the pilot immediately.
Six criteria are operational. Failure on operational criteria triggers remediation
without suspension.

### 6.1 — Constitutional Suspension Triggers (immediate)

**Trigger A — SC-3 failure: BLOCKED-class asset entered the pipeline**

```
Condition: Any source_item row with source_id = 'rijksmuseum' has a corresponding
           source_record whose raw_payload contains an edm:rights URI that
           classifies as BLOCKED under the Rights Matrix.

Response:
  1. Immediately halt all Rijksmuseum ingestion worker processes.
  2. Record preservation_event: event_type='rights_verification',
     event_outcome='violation',
     event_detail='BLOCKED edm:rights asset in pipeline — DD-RIJKSMUSEUM-001 pilot suspended'.
  3. Open a governance incident workflow_item: capability='governance_incident',
     entity_type='source_item'.
  4. Do not resume ingestion until the incident is resolved and the pre-ingestion
     rights filter is verified to be operating correctly.
  5. Notify the Director.
```

**Trigger B — SC-5 failure: FM output connected to rights determination**

```
Condition: Any FM output (fm_candidate_record or equivalent) is referenced in
           any workflow_item.context for capability='rights_review'
           where entity_type='source_item' and the source_item has
           source_id = 'rijksmuseum'.
           OR any preservation_event for a Rijksmuseum source_item references
           FM analysis in its event_detail.

Response:
  1. Immediately halt all Rijksmuseum ingestion and rights review processes.
  2. Record preservation_event: event_type='rights_verification',
     event_outcome='violation',
     event_detail='FM output connected to rights review — FM-4 violated — pilot suspended'.
  3. Open a governance incident workflow_item: capability='governance_incident'.
  4. The incident must be reviewed by the Director before any rights review resumes.
  5. Notify the Director.
```

### 6.2 — Operational Remediation Triggers (no suspension)

| Trigger | Condition | Response |
|---|---|---|
| SC-1 below threshold | Fewer than 10 activation_targets at pilot end | Review activation review queue backlog; confirm place association is not blocking unnecessarily |
| SC-2 gap | Any verified_pd/verified_cc0 record lacking required evidence per A1 Article 3(f) | Rights reviewer must supply missing evidence; cannot advance to activation without it |
| SC-4 gap | Any activation_eligible asset lacking a places assignment | Halt activation for ungeolocated assets; assign place before advancing |
| SC-6 gap | Any media_technical_metadata with longest edge < 400px | Log IIIF source; check if info.json pre-ingestion check was applied; block future assets from same IIIF pattern |
| SC-7 below threshold | anchor_type = 'mixed' on > 10% of pilot assets | Review derivation logic; apply manual corrections via workflow_item; enhance derivation for Phase 2 |
| SC-8 error rate | > 20% of ingested assets fail pipeline completion | Pause ingestion; debug worker errors before continuing |

---

## Section 7 — Success Criteria Sign-Off Checklist

**Purpose:** Completed by the Principal Architect after the pilot window closes.
Reviewed by the Director for DD-RIJKSMUSEUM-002 decision.

**Note on M36-014 (activation_target table):** This table was deferred in the current
M36 deployment (commit 7288b59). SC-1 and SC-4 queries reference activation state.
If M36-014 is not deployed by pilot end, SC-1 and SC-4 must be measured via
workflow_item completion records. Adapt queries accordingly.

**Pilot end date:** ___________________________

**Completed by (Principal Architect):** ___________________________

---

### SC-1 — Activated Assets

**Threshold:** ≥ 10 assets reach activation target with second-human approval.

```sql
-- Measurement (adapt if activation_target table not yet deployed)
SELECT COUNT(*) AS activated_count
FROM source_item si
WHERE si.source_id = 'rijksmuseum'
  AND si.status = 'activated';
```

Result: _____ assets

Pass threshold (≥ 10)? [ ] Yes  [ ] No

If No — remediation action taken: ___________________________

---

### SC-2 — Rights Verification Completeness

**Threshold:** 100% of rights-verified assets have complete evidence per A1 Article 3(f).

```sql
SELECT
    COUNT(*) FILTER (
        WHERE mr.rights_evidence ? 'permit_download_attested'
           OR mr.rights_evidence ? 'edm_rights_uri'
    ) AS with_evidence,
    COUNT(*) AS total_verified,
    COUNT(*) FILTER (
        WHERE mr.rights_evidence IS NULL
           OR mr.rights_evidence = '{}'::jsonb
    ) AS missing_evidence
FROM media_rights mr
JOIN source_item si ON si.id = mr.source_item_id
WHERE si.source_id = 'rijksmuseum'
  AND mr.rights_status IN ('verified_pd', 'verified_cc0');
```

Total verified: _____ With evidence: _____ Missing evidence: _____

Pass threshold (missing = 0)? [ ] Yes  [ ] No

If No — missing evidence supplied: [ ] Yes  [ ] No
(cannot complete sign-off if No)

---

### SC-3 — BLOCKED Filter Accuracy

**Threshold:** Zero BLOCKED-class `edm:rights` assets in `source_record` table.

```sql
-- Check source_records for Rijksmuseum assets
-- Worker must log all pre-ingestion rejections for this query to be meaningful
SELECT COUNT(*) AS blocked_rejections_logged
FROM preservation_event pe
JOIN source_item si ON si.id = pe.subject_id
  AND pe.subject_type = 'source_item'
WHERE si.source_id = 'rijksmuseum'
  AND pe.event_type = 'rights_verification'
  AND pe.event_outcome = 'blocked_pre_ingestion'
  AND pe.event_datetime >= '<pilot_start_date>';
```

Blocked assets rejected at pre-ingestion gate: _____

Any BLOCKED assets found in source_record? [ ] None found  [ ] Violations found

Pass threshold (no violations)? [ ] Yes  [ ] No

If No — **PILOT SUSPENDED** — do not complete this checklist until
constitutional incident (Trigger A, Section 6.1) is resolved.

---

### SC-4 — Place Association

**Threshold:** 100% of activated assets have at least one `places` record assigned.

```sql
-- Measurement requires place association mechanism (workflow_item or M36-014)
-- Adapt to actual implementation at pilot end.
SELECT
    COUNT(*) AS total_activation_eligible,
    COUNT(*) FILTER (WHERE si.status = 'activated') AS activated,
    COUNT(*) FILTER (
        WHERE si.status = 'activated'
          AND NOT EXISTS (
            SELECT 1 FROM workflow_items wi
            WHERE wi.entity_id = si.id
              AND wi.capability = 'place_association'
              AND wi.status = 'complete'
          )
    ) AS activated_without_place
FROM source_item si
WHERE si.source_id = 'rijksmuseum';
```

Total activated: _____ With place: _____ Without place: _____

Pass threshold (without place = 0)? [ ] Yes  [ ] No

---

### SC-5 — FM Exclusion

**Threshold:** Zero FM output connected to any rights determination for
Rijksmuseum-sourced assets.

```sql
SELECT COUNT(*) AS potential_violations
FROM preservation_event pe
JOIN source_item si ON si.id = pe.subject_id
  AND pe.subject_type = 'source_item'
WHERE si.source_id = 'rijksmuseum'
  AND pe.event_outcome = 'violation'
  AND pe.event_detail::text ILIKE '%fm%'
  AND pe.event_datetime >= '<pilot_start_date>';
```

Potential FM-rights connections found: _____

Any FM output connected to rights determination? [ ] None found  [ ] Violations found

Pass threshold (no violations)? [ ] Yes  [ ] No

If No — **PILOT SUSPENDED** — do not complete this checklist until
constitutional incident (Trigger B, Section 6.1) is resolved.

---

### SC-6 — IIIF Image Quality

**Threshold:** 100% of ingested assets meet the 400px minimum on longest edge.

```sql
SELECT
    COUNT(*) FILTER (
        WHERE (mtm.content->>'width')::int >= 400
           OR (mtm.content->>'height')::int >= 400
    ) AS meets_minimum,
    COUNT(*) FILTER (
        WHERE (mtm.content->>'width')::int < 400
          AND (mtm.content->>'height')::int < 400
    ) AS below_minimum,
    COUNT(*) AS total
FROM media_technical_metadata mtm
JOIN source_item si ON si.id = mtm.source_item_id
WHERE si.source_id = 'rijksmuseum';
```

Total: _____ Meets 400px minimum: _____ Below minimum: _____

Pass threshold (below minimum = 0)? [ ] Yes  [ ] No

---

### SC-7 — anchor_type Derivation Accuracy

**Threshold:** ≥ 90% of pilot assets have `anchor_type != 'mixed'`.

```sql
SELECT
    anchor_type,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM source_item
WHERE source_id = 'rijksmuseum'
GROUP BY anchor_type
ORDER BY count DESC;
```

anchor_type distribution:

| anchor_type | count | % |
|---|---|---|
| biological | ___ | ___% |
| geographic | ___ | ___% |
| cultural | ___ | ___% |
| mixed | ___ | ___% |

% with `anchor_type != 'mixed'`: _____%

Pass threshold (≥ 90% non-mixed)? [ ] Yes  [ ] No

Operator review notes: ___________________________

---

### SC-8 — Pipeline Completion Rate

**Threshold:** ≥ 80% of ingested assets complete all pre-activation gates without
worker error.

```sql
SELECT
    COUNT(*) AS total_ingested,
    COUNT(*) FILTER (
        WHERE si.status IN ('rights_verified', 'activation_eligible', 'activated')
    ) AS completed_pipeline,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE si.status IN ('rights_verified', 'activation_eligible', 'activated')
        ) / NULLIF(COUNT(*), 0), 1
    ) AS completion_rate_pct
FROM source_item si
WHERE si.source_id = 'rijksmuseum'
  AND si.created_at >= '<pilot_start_date>';
```

Total ingested: _____ Completed pipeline: _____ Completion rate: _____%

Pass threshold (≥ 80%)? [ ] Yes  [ ] No

---

### Overall Pilot Assessment

SC criteria passed: _____ / 8

Constitutional criteria (SC-3, SC-5): [ ] Both passed  [ ] Suspension event occurred

Recommendation:

[ ] **PROCEED to DD-RIJKSMUSEUM-002** — All 8 criteria met. Pilot successful.
    Recommend scope expansion to broader collection and OAI-PMH bulk harvest.

[ ] **REMEDIATE and EXTEND** — Operational criteria failures (not SC-3/SC-5).
    Address remediation items. Extend pilot window. Re-evaluate before DD-RIJKSMUSEUM-002.

[ ] **INVESTIGATE** — Constitutional criteria failure. Pilot suspended.
    Do not recommend DD-RIJKSMUSEUM-002 until constitutional incident resolved.

**Principal Architect signature:** ___________________________ **Date:** ___________

**Director sign-off on pilot review:** ___________________________ **Date:** ___________

---

## Section 8 — Post-Ratification Action Register

Complete these steps in order after DD-RIJKSMUSEUM-001 + A1 are ratified
(both signatures recorded in Sections 2 and 3).

```
IMMEDIATELY AFTER RATIFICATION (before any implementation begins)
[ ] Record ratification date in DD-RIJKSMUSEUM-001 document header (line 11)
[ ] Record ratification date in DD-RIJKSMUSEUM-001-A1 document header
[ ] Update DD-RIJKSMUSEUM-001 header: "Governing Amendments: DD-RIJKSMUSEUM-001-A1"
    to include ratification date
[ ] Confirm docs/decisions/ commit includes both DD documents and this package

GATE 1 — SCHEMA PREREQUISITE (independent of ratification — apply first if needed)
[ ] Confirm governance_state column exists on sources:
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'sources' AND column_name = 'governance_state';
[ ] If column absent: apply 17_source_governance.sql
    docker exec nature-culture-postgres-1 psql -U nc -d nc \
      -f /docker-entrypoint-initdb.d/17_source_governance.sql
[ ] Re-run verification: 2 rows returned for governance columns
    (Closes blocker R-S-1)

GATE 2 — SOURCE REGISTRY (before first ingestion run; requires ratification + Gate 1)
[ ] Run pre-INSERT verification query (Section 4) — confirm 0 rows
[ ] Run Migration 17 column verification (Section 4) — confirm 2 columns
[ ] Apply RU-SR-1 (Revised) INSERT (SQL in Section 4)
[ ] Run post-INSERT 10-point verification query — confirm all 10 rows return true
[ ] Record applier name and timestamp in Section 4 of this document
    (Closes blocker R-G-2)

GATE 3 — RIGHTS GOVERNANCE (before first ingestion run)
[ ] FM exclusion confirmed in writing for Rijksmuseum pipeline.
    Confirmation recorded here: ___________________________
    (Closes blocker R-G-3)

[ ] At least one human reviewer designated for rights_review workflow items.
    Designated reviewer: ___________________________
    (May be same person as DD-EUR-001 rights reviewer — no restriction.)
    (Closes blocker R-G-4)

GATE 3 — IMPLEMENTATION (before first ingestion run)
[ ] Rijksmuseum ingestion worker implemented:
    - OAI-PMH EDM harvest from https://data.rijksmuseum.nl/oai
    - Pre-ingestion rights filter using europeana_adapter/rights.py classify_rights()
      applied to edm:rights URI from EDM records
    - All 6 mandatory fields checked (Section 5.1 pre-ingestion filter)
    - IIIF info.json retrieved for dimension verification (Section 5.5)
    - anchor_type seeded from OAI-PMH set membership (biological for set 261222)
    - Europeana deduplication query (DD-RIJKSMUSEUM-001 Article 2(d))
    (Closes blocker R-I-1)

[ ] anchor_type derivation implemented and unit-tested (A1 Article 5.4)
    (Closes blocker R-I-2)

[ ] Article 9.3 gate verified: OAI-PMH EDM endpoint accessible
    curl -s "https://data.rijksmuseum.nl/oai?verb=ListMetadataFormats"
    Expected: edm metadataPrefix in response

GATE 4 — INGESTION AND ACTIVATION
[ ] Record pilot start date in Section 5.3
[ ] Record pilot end date (90 days from start) in Section 5.3
[ ] First ingestion run executed within pilot scope (Section 5.1)
[ ] Monitor SC-3 and SC-5 continuously — suspend immediately if violated
[ ] At pilot end: complete Section 7 sign-off checklist
[ ] Submit pilot review to Director for DD-RIJKSMUSEUM-002 decision
```

---

## Remaining Blockers After A1

All 7 remaining blockers from the readiness audit, with closure path.

| ID | Blocker | Closure |
|---|---|---|
| **R-G-1** | DD-RIJKSMUSEUM-001 + A1 not ratified | Section 2 + 3 signatures in this package |
| **R-G-2** | RU-SR-1 not applied | Section 4 of this package — requires R-G-1 + R-S-1 first |
| **R-G-3** | FM exclusion not confirmed in writing | Section 8 Gate 3 recording |
| **R-G-4** | No human reviewer designated | Section 8 Gate 3 designation |
| **R-S-1** | Migration 17 not applied — `governance_state` column missing | Section 8 Gate 1 — independent of ratification, apply now |
| **R-I-1** | No Rijksmuseum ingestion worker | Section 8 Gate 3 implementation. Note: `rights.py` `classify_rights()` is directly reusable. |
| **R-I-2** | `anchor_type` derivation not implemented | Section 8 Gate 3 implementation. Pilot simplification: set 261222 seeds `biological`. |

**First unblocked action:** R-S-1 (apply Migration 17). Independent of ratification.
Apply it now if not already done.

**Last action before first ingestion run:** Section 8 Gate 2 (RU-SR-1 INSERT).
Requires R-G-1 (ratification), R-S-1 (M17), and all Gate 3 items complete.

---

*DD-RIJKSMUSEUM-001 Ratification Package v1.0 — drafted 2026-06-07*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs) + Second Human Approver*
