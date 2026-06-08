# DD-GALLICA-002 — Ratification Package

| Field | Value |
|---|---|
| **Decision ID** | DD-GALLICA-002 |
| **Package Version** | 1.0 — Initial |
| **Status** | Awaiting Ratification |
| **Governing Decision** | DD-GALLICA-002_gallica_production_activation.md |
| **Prepared** | 2026-06-08 |

---

## Section 1 — Pre-Ratification Confirmation

The Director must confirm all of the following before signing. No box may be left
blank. If any confirmation cannot be made, ratification is blocked until the
underlying issue is resolved.

| # | Confirmation | Status |
|---|---|---|
| 1.1 | DD-GALLICA-001 has been reviewed in full and is ready for ratification or has already been ratified | ☐ |
| 1.2 | DD-GALLICA-002 has been reviewed in full and is correct as written | ☐ |
| 1.3 | I understand that `source_id = 'bnf_gallica'` is NOT currently in the sources table; the ratification package authorizes a new INSERT | ☐ |
| 1.4 | I understand that the INSERT sets `governance_state = 'active'` and this is intentional — no `proposed`/`approved` transitional states apply to a governed INSERT | ☐ |
| 1.5 | I understand that the Gallica Rights Addendum v1 (DD-GALLICA-001 Article 2) is hereby ratified as a governing document and is immutable without a new version | ☐ |
| 1.6 | I understand that EU Directive 2019/790 Article 14 and the Bridgeman doctrine are constitutional doctrine — they may not be suspended by Director Decision | ☐ |
| 1.7 | I understand that SC-3 (BLOCKED filter accuracy) and SC-5 (FM exclusion) are constitutional success criteria: failure on either requires immediate pilot suspension | ☐ |
| 1.8 | I understand that audio and film ingestion from Gallica is formally excluded and may not be activated by Director Decision — it requires a Phase 3 constitutional gate amendment | ☐ |
| 1.9 | I understand that `governance_state = 'active'` does not mean the pilot may begin — Gate 3 (infrastructure) and Gate 4 (Asset Zero) must be closed first | ☐ |
| 1.10 | I understand that exceeding the 50-asset pilot cap requires DD-GALLICA-003 and is not authorized by this Decision | ☐ |

---

## Section 2 — Director Approval Statement

By signing below, I, the Director (opengracelabs), formally ratify Director Decision
DD-GALLICA-002 and the complete Gallica Production Activation Package. I confirm:

1. I have read and understood DD-GALLICA-001 (Source Audit and Activation Framework)
   and DD-GALLICA-002 (Production Activation) in their entirety.

2. I formally designate BnF Gallica as **Institution #6** in NC's active content
   institution portfolio, effective today.

3. I formally ratify the **Gallica Rights Addendum v1** (DD-GALLICA-001 Article 2,
   Tables GA-1A, GA-1B, GA-2, and the three-layer priority sequence in Article 2.3)
   as a governing document alongside the Europeana Rights Matrix v1.0. The Addendum
   may not be modified except by a new version ratification process.

4. I authorize the source registry INSERT for `source_id = 'bnf_gallica'` as specified
   in Section 4 of this Ratification Package, to be executed after Gate 1 is closed
   (Standards Constitution Amendments SA-3 and SA-6 ratified).

5. I authorize the Madagascar pilot (geonames 1062947) at a 50-asset cap over a 90-day
   window, to begin only after Gates 0 through 4 have been closed in sequence.

6. I authorize the Asset Zero requirement: a pre-1800 Madagascar endemic species
   illustration from Buffon's "Histoire Naturelle" or Sonnerat's "Voyage aux Indes
   orientales et à la Chine" (1782) as the first preference, per DD-GALLICA-002 Article 7.

7. I commit to the governance gate sequence in DD-GALLICA-002 Article 6. No gate may
   be bypassed, skipped, or partially closed.

| Field | Value |
|---|---|
| **Director** | opengracelabs |
| **Signature** | _________________________________ |
| **Date** | _________________________________ |

---

## Section 3 — Second-Human Approval

By signing below, the Second Human Approver independently confirms that:

1. DD-GALLICA-001 and DD-GALLICA-002 have each been reviewed and the governance
   framework is sound.

2. The Gallica Rights Addendum v1 is a correct and coherent supplement to the
   Europeana Rights Matrix v1.0. The text-path classifications in Tables GA-1A and GA-1B
   are consistent with NC's PD-only commercial mandate.

3. The Institution #6 designation and Madagascar pilot scope are appropriate given NC's
   current institutional portfolio and commercial objectives.

4. The Asset Zero specification in DD-GALLICA-002 Article 7 is achievable against
   Gallica's known collection and rights profile.

5. SC-3 and SC-5 as constitutional suspension criteria are understood and appropriate.

| Field | Value |
|---|---|
| **Second Human Approver** | _________________________________ |
| **Role** | _________________________________ |
| **Signature** | _________________________________ |
| **Date** | _________________________________ |

---

## Section 4 — Source Registry Amendment

### 4.1 Pre-INSERT Verification

Execute this query before running the INSERT. Expected result: `0`.
If the result is not `0`, halt — `bnf_gallica` already exists and this INSERT
must not proceed.

```sql
SELECT COUNT(*) AS existing_count
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 0
-- If result != 0: HALT. Do not proceed with INSERT.
```

### 4.2 Source Registry INSERT

Execute as a single transaction:

```sql
BEGIN;

INSERT INTO sources (
  source_id,
  display_name,
  description,
  source_type,
  governance_state,
  governance_version,
  rights_strategy,
  auth_type,
  phase_restriction,
  config,
  provenance,
  created_at,
  updated_at
) VALUES (
  'bnf_gallica',
  'BnF Gallica',
  'Bibliothèque nationale de France digital library. Direct Tier 1 Core content institution. 5+ million digitized documents: illustrations, maps, manuscripts, photographs, livres anciens. NC Phase 1 only (image, map, illustration). Audio/video excluded. Gallica Rights Addendum v1 governs rights classification for French-language rights fields.',
  'direct_institution',
  'active',
  'DD-GALLICA-002',
  'gallica_rights_addendum_v1',
  'none',
  'phase_1',
  '{
    "sru_endpoint": "https://gallica.bnf.fr/SRU",
    "oai_endpoint": "https://gallica.bnf.fr/services/OAIRecord",
    "iiif_image_base": "https://gallica.bnf.fr/iiif",
    "iiif_presentation_base": "https://gallica.bnf.fr/iiif",
    "iiif_version": "2.1",
    "iiif_bridging_required": true,
    "iiif_image_url_template": "https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/f1/full/full/0/native.jpg",
    "iiif_manifest_url_template": "https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/manifest.json",
    "oai_record_url_template": "https://gallica.bnf.fr/services/OAIRecord?identifier=oai:bnf.fr:gallica/{ark_id}",
    "auth_type": "none",
    "identifier_scheme": "ark",
    "identifier_prefix": "ark:/12148/",
    "rate_limit": {
      "requests_per_second": 2,
      "burst": 5,
      "timeout_seconds": 45,
      "max_retries": 3,
      "backoff_base_seconds": 2
    },
    "rights_strategy": "gallica_rights_addendum_v1",
    "rights_field_iiif": "manifest.license",
    "rights_field_oai": "dc:rights",
    "rights_determination_priority": [
      "iiif_license_uri",
      "dc_rights_uri",
      "dc_rights_text"
    ],
    "eu_article_14_reliance": true,
    "bridgeman_doctrine_reliance": true,
    "bnf_pd_authority_tier": 1,
    "source_role": "direct_institution",
    "aggregation_tier": "one_tier",
    "metadata_standard": "dc_via_oai_pmh",
    "phase_1_only": true,
    "audio_video_excluded": true,
    "sru_query_language": "SRU/CQL",
    "rights_filter": {
      "mode": "pre_ingestion",
      "authority": "gallica_rights_addendum_v1",
      "uri_path": {
        "allowed_uris": [
          "http://creativecommons.org/publicdomain/zero/1.0/",
          "https://creativecommons.org/publicdomain/zero/1.0/",
          "http://creativecommons.org/publicdomain/mark/1.0/",
          "https://creativecommons.org/publicdomain/mark/1.0/",
          "http://rightsstatements.org/vocab/NoC-US/1.0/",
          "https://rightsstatements.org/vocab/NoC-US/1.0/"
        ],
        "review_required_uris": [
          "http://rightsstatements.org/vocab/NoC-CR/1.0/",
          "https://rightsstatements.org/vocab/NoC-CR/1.0/",
          "http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
          "https://rightsstatements.org/vocab/NoC-OKLR/1.0/",
          "http://rightsstatements.org/vocab/NKC/1.0/",
          "https://rightsstatements.org/vocab/NKC/1.0/"
        ],
        "filter_mode": "strict"
      },
      "text_path": {
        "allowed_patterns": [
          "domaine public",
          "public domain",
          "libre de réutilisation",
          "usage commercial autorisé"
        ],
        "review_required_patterns": [
          "domaine public revisité"
        ],
        "blocked_patterns": [
          "usage non-commercial uniquement",
          "usage non commercial",
          "droits réservés",
          "tous droits réservés",
          "under copyright",
          "all rights reserved"
        ],
        "absent_rights_treatment": "blocked",
        "unrecognized_french_pd_treatment": "review_required"
      }
    },
    "iiif_bridging_spec": "docs/standards/gallica_iiif_bridge_v1.md",
    "metadata_cc_by_separation": true,
    "pilot_active": true,
    "pilot_place_geonames_id": 1062947,
    "pilot_place_wikidata": "Q1019",
    "pilot_asset_cap": 50,
    "pilot_governing_decision": "DD-GALLICA-002"
  }',
  '{
    "governing_decisions": ["DD-GALLICA-001", "DD-GALLICA-002"],
    "activation_date": null,
    "institution_number": 6,
    "wave": 3,
    "ratification_date": null,
    "ratified_by": "opengracelabs",
    "second_human_approver": null
  }',
  NOW(),
  NOW()
);

COMMIT;
```

### 4.3 Post-INSERT Verification

Execute all 13 checks. Every check must return the expected value. Any deviation is
a critical error — investigate before proceeding.

```sql
-- GAL-SR-1: Row exists
SELECT COUNT(*) AS row_count
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 1

-- GAL-SR-2: Governance state is active
SELECT governance_state
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 'active'

-- GAL-SR-3: Auth type is none
SELECT config->>'auth_type' AS auth_type
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 'none'

-- GAL-SR-4: IIIF bridging required flag
SELECT (config->>'iiif_bridging_required')::boolean AS bridging_required
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: true

-- GAL-SR-5: Phase restriction is phase_1
SELECT phase_restriction
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 'phase_1'

-- GAL-SR-6: EU Article 14 reliance
SELECT (config->>'eu_article_14_reliance')::boolean AS article_14
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: true

-- GAL-SR-7: Bridgeman doctrine reliance
SELECT (config->>'bridgeman_doctrine_reliance')::boolean AS bridgeman
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: true

-- GAL-SR-8: Audio/video excluded
SELECT (config->>'audio_video_excluded')::boolean AS audio_video_excluded
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: true

-- GAL-SR-9: Rights strategy
SELECT rights_strategy
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 'gallica_rights_addendum_v1'

-- GAL-SR-10: Pilot geonames ID
SELECT (config->>'pilot_place_geonames_id')::integer AS pilot_geonames
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 1062947

-- GAL-SR-11: Pilot asset cap
SELECT (config->>'pilot_asset_cap')::integer AS pilot_cap
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 50

-- GAL-SR-12: BnF Tier 1 PD authority
SELECT (config->>'bnf_pd_authority_tier')::integer AS tier
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 1

-- GAL-SR-13: Institution number
SELECT (provenance->>'institution_number')::integer AS institution_number
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: 6

-- Composite readiness check (all critical fields)
SELECT
  source_id,
  governance_state,
  rights_strategy,
  auth_type,
  phase_restriction,
  (config->>'iiif_bridging_required')::boolean AS bridging_required,
  (config->>'eu_article_14_reliance')::boolean AS article_14,
  (config->>'audio_video_excluded')::boolean AS audio_excluded,
  (config->>'pilot_asset_cap')::integer AS pilot_cap,
  (provenance->>'institution_number')::integer AS institution_number
FROM sources
WHERE source_id = 'bnf_gallica';
-- EXPECTED: bnf_gallica | active | gallica_rights_addendum_v1 | none | phase_1 | t | t | t | 50 | 6
```

---

## Section 5 — Pilot Scope Controls

### 5.1 Pilot Parameters

| Parameter | Value | Authority |
|---|---|---|
| Place | Madagascar | DD-GALLICA-001 Article 9(a) |
| Geonames ID | 1062947 | DD-GALLICA-001 Article 9(a) |
| Wikidata | Q1019 | DD-GALLICA-001 Article 9(a) |
| Asset cap | 50 | DD-GALLICA-001 Article 9(a); Article 8 |
| Pilot window | 90 days from first batch | DD-GALLICA-001 Article 9(a) |
| Media types | Phase 1 only (image, map, illustration) | DD-GALLICA-001 Article 5 |
| Rights paths | Both URI path and text path | DD-GALLICA-001 Article 2 |

### 5.2 SRU Query Parameters

The pilot is authorized to use the following SRU query scope against Gallica:

```
Primary query (natural history illustrations):
  dc.type = "image" AND dc.subject any "Madagascar" 
  AND dc.date < "1850" AND dc.type not "sonore"

Secondary query (maps):
  dc.type = "carte" AND dc.subject any "Madagascar"
  AND dc.date < "1850"
```

These queries must be pre-filtered by the rights filter before creating `source_record`
entries. Assets outside Madagascar must be discarded at ingestion regardless of rights
classification.

### 5.3 Sub-Cap Controls

Within the 50-asset cap, the following sub-caps apply per DD-GALLICA-001 Article 9(d):

| Rights path | Sub-cap | Reason |
|---|---|---|
| REVIEW REQUIRED (URI path) | 10 assets | IIIF license URI REVIEW REQUIRED cases |
| "Domaine public revisité" text | 5 assets | HR-GA-3 review; limited reviewer bandwidth |
| ALLOWED (combined, all text/URI) | 35 assets minimum | Core pilot workload |

### 5.4 Asset Scope Verification Query

Use to check the live pilot asset count before authorizing additional batch runs:

```sql
SELECT
  mr.rights_status,
  COUNT(*) AS asset_count,
  MIN(si.created_at) AS first_ingested,
  MAX(si.created_at) AS last_ingested
FROM source_items si
JOIN source_records sr ON sr.id = si.source_record_id
JOIN media_rights mr ON mr.source_item_id = si.id
WHERE sr.source = 'bnf_gallica'
GROUP BY mr.rights_status
ORDER BY asset_count DESC;
```

```sql
-- Total assets in pilot
SELECT COUNT(*) AS total_pilot_assets
FROM source_items si
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica';
-- ENFORCED CAP: Must not exceed 50 without DD-GALLICA-003.
```

---

## Section 6 — Pilot Suspension Criteria

### 6.1 Constitutional Suspension (Automatic — no Director Decision required)

The pilot must be suspended immediately and the source `governance_state` set to
`'suspended'` if either of the following is detected:

| Code | Trigger | Required action |
|---|---|---|
| **SC-3** | Any `source_record` for `source = 'bnf_gallica'` has `rights_status = 'blocked'` AND has been created in the pipeline (i.e., did not fail pre-ingestion filter) | Suspend pilot. Audit all Gallica assets. Do not resume without Director Decision identifying root cause. |
| **SC-5** | Any FM-originated output is connected to a rights determination or media_rights record for any Gallica asset | Suspend immediately. Escalate as constitutional violation. |

SC-3 detection query:
```sql
SELECT COUNT(*) AS blocked_in_pipeline
FROM source_records sr
JOIN media_rights mr ON mr.source_item_id IN (
  SELECT si.id FROM source_items si WHERE si.source_record_id = sr.id
)
WHERE sr.source = 'bnf_gallica'
  AND mr.rights_status = 'blocked';
-- EXPECTED: 0 at all times during pilot
-- If > 0: SUSPEND PILOT NOW
```

SC-5 detection query:
```sql
SELECT COUNT(*) AS fm_rights_violation
FROM preservation_events pe
JOIN source_items si ON si.id = pe.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND pe.event_type = 'rights_determination'
  AND pe.event_metadata->>'rights_source_type' = 'fm_output';
-- EXPECTED: 0 at all times during pilot
-- If > 0: SUSPEND PILOT NOW — constitutional violation
```

### 6.2 Suspension Execution

If SC-3 or SC-5 triggers, execute:

```sql
BEGIN;

UPDATE sources
SET
  governance_state = 'suspended',
  updated_at = NOW()
WHERE source_id = 'bnf_gallica';

-- Verify
SELECT governance_state FROM sources WHERE source_id = 'bnf_gallica';
-- EXPECTED: 'suspended'

COMMIT;
```

After suspension, record the suspension event in `preservation_events` or
equivalent governance log with: `event_type = 'source_suspension'`,
`event_metadata = { "trigger": "SC-3" | "SC-5", "dd_gallica_002_article": "9" }`.

Resumption requires a new Director Decision. The suspended source may not be
re-activated by rolling back the governance_state without a formal DD.

### 6.3 Operational Criteria (Remediation without Suspension)

These are performance failures, not constitutional violations. They require remediation
and may require extending the pilot window (with Director approval) but do not trigger
automatic suspension:

| Code | Trigger | Remediation |
|---|---|---|
| SC-1 | Fewer than 7 assets reach `activation_target` | Review rights classification for blockers; extend pilot window if needed |
| SC-7 | Text-path misclassification detected | Audit all text-path records; correct before proceeding; calibrate text-path filter |
| SC-8 | IIIF 3.0 manifest validation failure | Debug bridging adapter; re-bridge affected assets |
| SC-9 | `preservation_event.event_outcome = 'violation'` detected | Review each violation; escalate if constitutional |
| SC-10 | Pipeline completion rate < 75% | Debug worker errors; identify highest-frequency failure modes |

---

## Section 7 — Success Criteria Sign-Off Checklist

Complete all ten evaluations at pilot conclusion. Results must be documented by both
the Director and the Second Human Approver before DD-GALLICA-003 may be initiated.

### SC-1 — Activated Assets

```sql
SELECT COUNT(*) AS activation_target_count
FROM activation_targets at
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND at.status = 'activation_target';
```
**Threshold:** ≥ 7  
**Result:** _____ / Pass / Fail

### SC-2 — Rights Verification Completeness

```sql
SELECT
  COUNT(*) FILTER (WHERE mr.rights_evidence IS NOT NULL AND mr.rights_evidence != '{}')
    AS with_evidence,
  COUNT(*) FILTER (WHERE mr.rights_evidence IS NULL OR mr.rights_evidence = '{}')
    AS without_evidence,
  COUNT(*) AS total_activation_eligible
FROM media_rights mr
JOIN source_items si ON si.id = mr.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND mr.rights_status = 'activation_eligible';
```
**Threshold:** `without_evidence = 0`  
**Result:** _____ / Pass / Fail

### SC-3 — BLOCKED Filter Accuracy (Constitutional)

```sql
SELECT COUNT(*) AS blocked_in_pipeline
FROM source_records sr
JOIN media_rights mr ON mr.source_item_id IN (
  SELECT si.id FROM source_items si WHERE si.source_record_id = sr.id
)
WHERE sr.source = 'bnf_gallica'
  AND mr.rights_status = 'blocked';
```
**Threshold:** = 0  
**CONSTITUTIONAL: Failure requires suspension (recorded in Section 6.1)**  
**Result:** _____ / Pass / Fail

### SC-4 — Place Association

```sql
SELECT
  COUNT(*) FILTER (WHERE pa.geonames_id = 1062947) AS madagascar_associated,
  COUNT(*) FILTER (WHERE pa.geonames_id != 1062947 OR pa.geonames_id IS NULL) AS other_place,
  COUNT(*) AS total_activated
FROM activation_targets at
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
LEFT JOIN place_associations pa ON pa.source_item_id = si.id
WHERE sr.source = 'bnf_gallica'
  AND at.status = 'activation_target';
```
**Threshold:** `other_place = 0` and `total_activated > 0`  
**Result:** _____ / Pass / Fail

### SC-5 — FM Exclusion (Constitutional)

```sql
SELECT COUNT(*) AS fm_rights_violations
FROM preservation_events pe
JOIN source_items si ON si.id = pe.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND pe.event_type = 'rights_determination'
  AND pe.event_metadata->>'rights_source_type' = 'fm_output';
```
**Threshold:** = 0  
**CONSTITUTIONAL: Failure requires suspension (recorded in Section 6.1)**  
**Result:** _____ / Pass / Fail

### SC-6 — Commerce Coverage

```sql
SELECT
  COUNT(*) FILTER (
    WHERE ao.cos_score IS NOT NULL AND ao.csm_tier IS NOT NULL
  ) AS with_commerce,
  COUNT(*) FILTER (
    WHERE ao.cos_score IS NULL OR ao.csm_tier IS NULL
  ) AS without_commerce,
  COUNT(*) AS total_activated
FROM activation_targets at
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
LEFT JOIN asset_opportunities ao ON ao.source_item_id = si.id
WHERE sr.source = 'bnf_gallica'
  AND at.status = 'activation_target';
```
**Threshold:** `without_commerce = 0`  
**Result:** _____ / Pass / Fail

### SC-7 — Gallica Rights Addendum Text-Path Accuracy

```sql
-- Identify any assets that entered the pipeline via text-path classification
SELECT
  mr.rights_status,
  mr.rights_evidence->>'text_path_match' AS match_pattern,
  mr.rights_evidence->>'text_path_input' AS input_text,
  COUNT(*) AS count
FROM media_rights mr
JOIN source_items si ON si.id = mr.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND mr.rights_evidence->>'rights_source' = 'gallica_text_path'
GROUP BY mr.rights_status, match_pattern, input_text
ORDER BY count DESC;

-- Misclassification check: text-path assets with unexpected rights_status
SELECT COUNT(*) AS potential_misclassifications
FROM media_rights mr
JOIN source_items si ON si.id = mr.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND mr.rights_evidence->>'rights_source' = 'gallica_text_path'
  AND mr.rights_status NOT IN (
    'verified_pd', 'verified_cc0', 'activation_eligible', 'activation_target',
    'pending_verification', 'ineligible', 'review_required'
  );
```
**Threshold:** `potential_misclassifications = 0`; review first query for any implausible
pattern/status combinations  
**Result:** _____ / Pass / Fail

### SC-8 — IIIF 3.0 Manifest Validity

```sql
-- Check for manifests missing IIIF 3.0 context
SELECT COUNT(*) AS invalid_manifests
FROM asset_delivery_manifests adm
JOIN activation_targets at ON at.id = adm.activation_target_id
JOIN source_items si ON si.id = at.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND (
    adm.manifest_payload->>'@context' LIKE '%presentation/2%'
    OR adm.manifest_payload->>'type' IS NULL
    OR adm.manifest_payload->>'type' != 'Manifest'
    OR adm.manifest_payload->'items' IS NULL
  );
```
**Threshold:** = 0  
**Note:** Assets without a IIIF manifest (image-only items) are excluded from this
check — count only assets where `adm.manifest_payload IS NOT NULL`.  
**Result:** _____ / Pass / Fail

### SC-9 — Constitutional Integrity

```sql
SELECT COUNT(*) AS constitutional_violations
FROM preservation_events pe
JOIN source_items si ON si.id = pe.source_item_id
JOIN source_records sr ON sr.id = si.source_record_id
WHERE sr.source = 'bnf_gallica'
  AND pe.event_outcome = 'violation';
```
**Threshold:** = 0  
**Result:** _____ / Pass / Fail

### SC-10 — Pipeline Completion Rate

```sql
SELECT
  COUNT(*) FILTER (WHERE pe_complete.event_type IS NOT NULL) AS completed,
  COUNT(*) FILTER (WHERE pe_error.event_type IS NOT NULL) AS worker_errors,
  COUNT(*) AS total_ingested,
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE pe_complete.event_type IS NOT NULL) / NULLIF(COUNT(*), 0),
    1
  ) AS completion_pct
FROM source_items si
JOIN source_records sr ON sr.id = si.source_record_id
LEFT JOIN preservation_events pe_complete
  ON pe_complete.source_item_id = si.id
  AND pe_complete.event_type = 'ingestion_complete'
LEFT JOIN preservation_events pe_error
  ON pe_error.source_item_id = si.id
  AND pe_error.event_outcome = 'worker_error'
WHERE sr.source = 'bnf_gallica';
```
**Threshold:** `completion_pct >= 75.0`  
**Result:** _____% / Pass / Fail

### 7.1 Pilot Evaluation Sign-Off

| Criterion | Result | Pass/Fail | Evaluator |
|---|---|---|---|
| SC-1 (Activated assets ≥ 7) | | | |
| SC-2 (Rights evidence completeness) | | | |
| SC-3 (BLOCKED filter — Constitutional) | | | |
| SC-4 (Place association 100%) | | | |
| SC-5 (FM exclusion — Constitutional) | | | |
| SC-6 (Commerce coverage 100%) | | | |
| SC-7 (Text-path accuracy 0 misclassifications) | | | |
| SC-8 (IIIF 3.0 validity 100%) | | | |
| SC-9 (Constitutional integrity 0 violations) | | | |
| SC-10 (Pipeline completion ≥ 75%) | | | |

**Pilot outcome:**
☐ All criteria met or exceeded — proceed to DD-GALLICA-003  
☐ One or more operational criteria not met — remediation required before DD-GALLICA-003  
☐ SC-3 or SC-5 failed — pilot suspended (see Section 6.2)

**Director sign-off:**  
Signature: _________________________________ Date: _____________

**Second Human sign-off:**  
Signature: _________________________________ Date: _____________

---

## Section 8 — Post-Ratification Action Register

Complete in sequence. No gate may open until all items in the preceding gate are closed.

### Gate 0 — Ratification (this Package)
- [ ] DD-GALLICA-001 ratified (both signatures in its ratification package)
- [ ] DD-GALLICA-002 ratified (Sections 2 and 3 above signed)
- [ ] This ratification package filed in docs/decisions/

### Gate 1 — Standards Constitution Amendments
- [ ] Assign author for Standards Constitution v1.1 SA-3 (BnF Gallica API Profile)
- [ ] Assign author for Standards Constitution v1.1 SA-6 (UNIMARC Acknowledged Standard)
- [ ] Decide SA-4 disposition: include in SA-3 or separate amendment
- [ ] Draft SA-3 + SA-6 (+ SA-4) content
- [ ] Ratify Standards Constitution v1.1
- [ ] Update MEMORY.md: Standards Constitution version

### Gate 2 — Source Registry
- [ ] Run GAL-SR-1 pre-INSERT check (Section 4.1) — confirm result = 0
- [ ] Execute INSERT (Section 4.2) in a transaction
- [ ] Run all 13 post-INSERT verification checks (Section 4.3) — confirm all pass
- [ ] Document INSERT execution: timestamp, executor, verification results
- [ ] Update provenance JSON: set `ratification_date` and `second_human_approver`

### Gate 3 — Infrastructure
- [ ] Build IIIF 2.1 → 3.0 bridging adapter (DD-GALLICA-002 Article 4 field map)
- [ ] Document bridging adapter at docs/standards/gallica_iiif_bridge_v1.md
- [ ] Write unit tests for all 10 field transformations in the bridging table
- [ ] Deploy OAI-PMH ingestion worker with Gallica Rights Addendum v1 text-path logic
- [ ] Test text-path matching against Tables GA-1A, GA-1B, GA-2 in a non-production env
- [ ] Implement rate limiter: ≤ 2 req/s against all Gallica endpoints
- [ ] Designate and authorize French-language rights reviewer
- [ ] Confirm FM exclusion in Gallica pipeline (written confirmation from dev lead)
- [ ] Document Gate 3 closure: timestamp, all confirmations received

### Gate 4 — Asset Zero
- [ ] Execute Asset Zero validation per docs/implementation/gallica_asset_zero_checklist_v1.md
- [ ] Document Asset Zero: ARK identifier, publication details, rights classification result
- [ ] Confirm IIIF 3.0 manifest output from bridging adapter validates correctly
- [ ] Confirm watermark-free full-resolution delivery
- [ ] Get second-human approval for Asset Zero activation
- [ ] Record Asset Zero ARK in `provenance` JSON for `bnf_gallica` source record:
  ```sql
  UPDATE sources SET
    provenance = jsonb_set(provenance, '{asset_zero_ark}', '"ark:/12148/{verified_ark}"'),
    provenance = jsonb_set(provenance, '{asset_zero_date}', '"YYYY-MM-DD"'),
    updated_at = NOW()
  WHERE source_id = 'bnf_gallica';
  ```

### Gate 5 — Pilot Authorization
- [ ] Confirm Gates 0–4 all closed (written confirmation)
- [ ] Director formally authorizes pilot start in writing (date this document)
- [ ] Record pilot start date and compute pilot end date (+ 90 days)
- [ ] Run first SRU batch query (natural history, Madagascar, pre-1850, Phase 1 only)
- [ ] Confirm 50-asset cap enforced in worker configuration

### Gate 6 — Pilot Completion
- [ ] 50-asset cap reached OR 90-day window expired
- [ ] Run all SC-1 through SC-10 queries (Section 7)
- [ ] Complete sign-off table in Section 7.1
- [ ] Principal Architect recommendation memo: proceed to DD-GALLICA-003 or remediate
- [ ] Director pilot review sign-off

### Gate 7 — Full Production (requires DD-GALLICA-003)
- [ ] DD-GALLICA-003 drafted, ratified
- [ ] Pilot cap lifted
- [ ] Additional query scopes authorized (France, Francophone Africa, Réunion, etc.)
- [ ] Out of scope for this Decision

---

*DD-GALLICA-002 Ratification Package v1.0 — 2026-06-08*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
