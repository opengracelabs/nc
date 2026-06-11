# NOAA Sprint 3 Governance Review v1

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | DRAFT — Pending Ratification |
| Review Authority | NC Governance |
| Sprint | Sprint 3 design gate |
| Governing Documents | DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · IFC-1 · NOAA Sprint 2 Remediation Review v1 |
| M36 Write Path Reference | `workers/shared_media_adapter/store.py` · `workers/aic_adapter/store.py` |
| Date | 2026-06-11 |

---

## DECISION

**APPROVE — Sprint 3 governance ratified.**

The write-path decision matrix, workflow_item routing, hard-block rules, evidence field requirements, SA-9 compatibility specification, and replay test requirements defined below constitute the governing design for NOAA Sprint 3. No Sprint 3 M36 implementation may begin until the three Sprint 3 entry gates (Section X) are cleared.

---

## I. Architectural Foundation

Sprint 3 integrates the NOAA adapter into the shared M36 write path (`write_normalized_record` in `workers/shared_media_adapter/store.py`). The key facts of that path that govern NOAA's design are:

**Write-path gate:** `write_normalized_record` calls the shared URI-based `classify_rights(normalized.get("rights_uri"))`. It does not call NOAA's record-based `classify_rights`. NOAA's `store.py` must pre-gate on the NOAA decision before passing records to the shared path.

**Write counts:** 7 substrate writes for ALLOWED records (source_item, source_record, media_file, media_rights, preservation_event, media_technical_metadata, pin). 8 writes for REVIEW_REQUIRED records (same 7 plus workflow_item in `workflow_items` table with `capability: 'rights_review'`). 0 writes for records blocked or rejected before the shared path.

**FM-4 compliance:** `insert_media_rights` hardcodes `rights_status = 'pending_verification'` in SQL. No adapter worker can write `'verified_pd'` or `'classified_pd'` to the `media_rights` table. The `worker_classified_status` field in the rights evidence JSON may say `"classified_pd"` (after `WORKER_STATUS_REMAP`), but the database row always reads `'pending_verification'` until human promotion. FM-4 is structurally enforced.

**Rights URI as shared-path signal:** The shared write path routes ALLOWED/REVIEW_REQUIRED/BLOCKED based solely on `normalized["rights_uri"]`. NOAA's `store.py` must map NOAA decisions to the correct shared-path URI before calling `write_normalized_record`. The mapping is defined in Section IV.

**Pre-gate pattern:** Following the AIC pattern (`write_record` in `workers/aic_adapter/store.py`), NOAA's `write_record` performs a pre-gate check against the NOAA rights decision before calling `write_normalized_record`. Records that fail the NOAA pre-gate are returned with `status: "rejected"` and a specific NOAA reason code. The shared path is never called for pre-gate rejections.

---

## II. Write-Path Decision Matrix

| NOAA Rights Decision | Rights Basis | Store Writes | Workflow Item | Shared Path URI |
|---|---|---|---|---|
| ALLOWED | `flickr_us_government_work` | 7 | No | `NoC-US/1.0/` |
| ALLOWED | `noaa_federal_credit` | 7 | No | `NoC-US/1.0/` |
| REVIEW_REQUIRED | `partner_or_contributor_marker` (foreign agency) | 7 + 1 | Yes | `NKC/1.0/` |
| REVIEW_REQUIRED | `partner_or_contributor_marker` (partner institution) | 7 + 1 | Yes | `NKC/1.0/` |
| REVIEW_REQUIRED | `public_domain_license_without_federal_credit` | 7 + 1 | Yes | `NKC/1.0/` |
| REVIEW_REQUIRED | `personal_name_noaa_credit` | **0** | **No** | pre-gate rejected |
| BLOCKED | `blocked_partner_marker` (Getty/Reuters/AP/satellite) | 0 | No | pre-gate rejected |
| BLOCKED | `flickr_all_rights_reserved` | 0 | No | pre-gate rejected |
| BLOCKED | `unsupported_flickr_license` | 0 | No | pre-gate rejected |
| BLOCKED | `missing_rights_evidence` | 0 | No | pre-gate rejected |
| BLOCKED | `missing_object` | 0 | No | pre-gate rejected |
| Any | missing `record_id`, `title`, or `source_url` | 0 | No | pre-gate rejected |

---

## III. ALLOWED → M36 Write Path

**7 substrate writes. No workflow_item.**

ALLOWED records are confirmed NOAA federal works under 17 U.S.C. § 105. They pass directly through to the shared write path with `rights_uri = "https://rightsstatements.org/vocab/NoC-US/1.0/"`. The shared `classify_rights` sees `NoC-US/1.0/` → ALLOWED → no workflow_item created.

**Pre-gate conditions for ALLOWED to proceed:**

1. `rights["decision"] == "ALLOWED"` from NOAA `classify_rights(record)`
2. `normalized["record_id"]` is present and non-empty
3. `normalized["title"]` is present and non-empty
4. `normalized["source_url"]` is present and non-empty
5. `normalized["representative_media_url"]` is present and non-empty (url_m must not be this value — SPC-3-2 must be cleared before Sprint 3 implementation)
6. `validation_status(build_technical_metadata(normalized)) == "valid"`

If any condition fails → `status: "rejected"`, `writes: 0`, specific reason code.

**Evidence status after write:**
- `media_rights.rights_status = 'pending_verification'` (hardcoded in shared SQL)
- `media_rights.rights_evidence.worker_classified_status = "classified_pd"` (after WORKER_STATUS_REMAP)
- `media_rights.rights_evidence.evidence_status = "pending_human_review"`
- `media_rights.rights_evidence.applying_policy = "noaa_rights_matrix_v1"`
- NOAA-specific evidence extension fields present (Section VI)

**Pilot cap:** Maximum 50 ALLOWED writes total per pilot run (DD-NOAA-001 Article 10). Sprint 3 must enforce this cap in the harvest coordinator. The cap covers the full pilot period; it does not reset per execution.

---

## IV. REVIEW_REQUIRED → Workflow Item Path

**7 + 1 substrate writes. Workflow item created.**

Three NOAA rights bases route to this path: `partner_or_contributor_marker` (foreign agencies and partner institutions), and `public_domain_license_without_federal_credit` (Flickr license 7/9/10 without federal credit confirmation).

**URI mapping:** NOAA's `write_record` sets `normalized["rights_uri"] = "https://rightsstatements.org/vocab/NKC/1.0/"` (No Known Copyright) before calling `write_normalized_record`. The shared `classify_rights` sees NKC → REVIEW_REQUIRED → writes all 7 substrate records, then creates a workflow_item.

**Why NKC/1.0/:** NKC is the correct semantic URI for "we have not been able to confirm the copyright status." A NOAA Flickr image credited to NASA/ESA or a state university is genuinely in this state — potential § 105 but unconfirmed. The actual NOAA rights classification and original rights_statement_uri are preserved in the evidence extension (Section VI), so no information is lost.

**Workflow item payload (`context.item_payload`):**
```json
{
  "noaa_record_id": "<source_record_id>",
  "noaa_rights_basis": "<partner_or_contributor_marker | public_domain_license_without_federal_credit>",
  "noaa_partner_markers": ["NASA/ESA", "..."],
  "noaa_contributor_markers": [],
  "noaa_license_id": "<7|9|10 or null>",
  "noaa_original_rights_uri": "<NoC-US/1.0/ or PDM>",
  "noaa_rights_policy_id": "noaa_rights_matrix_v1",
  "matrix_classification": "review_required",
  "matrix_rule": "<rights_basis>",
  "source_record_id": "<source_record_id>",
  "edm_rights_uri": "https://rightsstatements.org/vocab/NKC/1.0/"
}
```

These fields must be populated by `build_evidence_extension` in the NOAA `StoreRuntime`.

**Workflow item routing:**

| Partner Markers | Workflow Type (in `status_reason`) |
|---|---|
| ESA, JAXA, CSA, European Space Agency, etc. | `foreign_agency_rights_review` |
| NASA/ESA, NASA/JAXA (joint-mission) | `foreign_agency_rights_review` |
| University, College, Institute, NGO, Foundation | `partner_institution_rights_review` |
| MBARI, Schmidt Ocean Institute, AURA, STScI | `partner_institution_rights_review` |
| contractor, contract | `partner_institution_rights_review` |
| license 7/9/10 only (no partner markers) | `public_domain_unverified_rights_review` |

The `status_reason` field in the workflow_item row carries the workflow type. This is the standard NC `workflow_items` pattern.

**Evidence status after write:**
- `media_rights.rights_status = 'pending_verification'` (hardcoded in SQL)
- `media_rights.rights_evidence.worker_classified_status = "pending_verification"` (NKC does not remap)
- `media_rights.rights_evidence.evidence_status = "pending_human_review"`
- workflow_item `status = 'pending'`, `capability = 'rights_review'`, `priority = 40`

**Promotion path:** A human reviewer who confirms the record is a § 105 federal work (or a CC-licensed work permitting commercial reuse) updates the workflow_item to `status: 'completed'` and updates `media_rights.rights_status` to the appropriate terminal state. This is standard M36 review workflow and requires no NOAA-specific implementation.

---

## V. Hard Blocks

**0 writes. No workflow item.**

The following cases are rejected in NOAA's `write_record` pre-gate. The shared path is never reached.

### V.1 Commercial Operators — Getty, Reuters, AP, Maxar, DigitalGlobe, Planet, GeoEye

`rights_basis = "blocked_partner_marker"` with one or more `blocked_markers`.

These are definitive commercial licensing situations. There is no scenario where a Getty-credited image in NOAA's Flickr stream is a § 105 federal work. A workflow_item would waste reviewer time on a certain rejection. Hard-block at store layer.

Return: `status: "rejected"`, `reason: "blocked_partner_marker"`, `blocked_markers: [...]`, `writes: 0`.

### V.2 Personal Name Credits — SPC-3-3 Resolution

`rights_basis = "personal_name_noaa_credit"` with one or more `contributor_markers`.

**Sprint 3 resolves SPC-3-3 with Option A.** Personal name/NOAA credits are hard-blocked at the store layer. NOAA's `write_record` checks `rights_basis == "personal_name_noaa_credit"` and rejects before calling the shared path, regardless of the ALLOWED/REVIEW_REQUIRED decision from rights.py.

Rationale: NC cannot verify federal employment status from a credit line at scale. "Photo by John Smith/NOAA" covers federal employees, contractors, visiting scientists, and interns. A human review queue for this class would be populated almost entirely by records that must be rejected anyway. The IFC-1-safe path is to hard-block. Records that are genuinely federal employee photographs will have NOAA division credits (not personal names) and will be ALLOWED via the federal credit gate.

SA-NOAA-001 v1.1 must document the store-layer hard block as the definitive enforcement mechanism for personal name credits. The `rights.py` decision (REVIEW_REQUIRED vs BLOCKED) is rendered moot by the store-layer gate.

Return: `status: "rejected"`, `reason: "contributed_image_exception"`, `contributor_markers: [...]`, `writes: 0`.

### V.3 All Other BLOCKED Decisions

`rights_basis` ∈ {`flickr_all_rights_reserved`, `unsupported_flickr_license`, `missing_rights_evidence`, `missing_object`}

Return: `status: "rejected"`, `reason: <rights_basis>`, `writes: 0`.

### V.4 Missing Required Fields

Records that pass the NOAA rights gate but fail the M36 contract field check (missing `record_id`, `title`, `source_url`, or `representative_media_url`) are rejected at the pre-gate with `reason: "invalid_normalized_record"`. These are adapter errors, not rights failures.

---

## VI. Required Evidence Fields

### VI.1 M36 Contract Fields

All NOAA records written to the store must include the following fields in the normalized payload (per `workers/shared_media_adapter/contracts.py`). These are new requirements for Sprint 3 — the current `normalize_record` output is missing several:

| Field | Source | Sprint 3 Addition? |
|---|---|---|
| `record_id` | `source_record_id` (Flickr `id`) | Already present |
| `title` | Flickr `title` | Already present |
| `description` | Flickr `description._content` | Already present |
| `date` | Flickr `date_taken` or `date_upload` | **Add in Sprint 3** |
| `creator` | `credit` or `owner_name` | Already present |
| `subject_terms` | Flickr `tags` → list | **Add in Sprint 3** |
| `rights_uri` | Mapped in `write_record` per Section IV | Must be set in store.py |
| `provider` | `"NOAA"` (static) | **Add in Sprint 3** |
| `dataProvider` | Flickr `owner_name` or `"NOAA Photo Library"` | **Add in Sprint 3** |
| `edm_type` | `"IMAGE"` (static) | **Add in Sprint 3** |
| `source_url` | Flickr photo page URL | Already present |
| `representative_media_url` | `image_url` (url_z minimum) | Already present (url_m removed by SPC-3-2) |
| `preview_urls` | `[url_z, url_c]` (lower-res) | **Add in Sprint 3** |
| `width_px` | Flickr `o_width` | Already present |
| `height_px` | Flickr `o_height` | Already present |
| `raw_payload_hash` | SHA-256 of raw JSON | Already present |
| `rights_decision` | From NOAA `classify_rights` | Already present |
| `rights_allowed` | `True` for ALLOWED records only | Already present |

### VI.2 NOAA-Specific Evidence Extension (via `build_evidence_extension`)

The `StoreRuntime.build_evidence_extension` callback must add the following fields to the `media_rights` evidence JSON for every NOAA record written:

| Field | Value | Note |
|---|---|---|
| `noaa_access_path` | `"flickr"` or `"noaa_photolib"` | Per SA-NOAA-001 Part VII |
| `noaa_primary_gate_field` | `"license_id"` (Flickr) or `"credit"` (Photo Library) | Per SA-NOAA-001 Part VII |
| `noaa_legal_basis` | `"17 U.S.C. § 105"` | Always — statutory basis for Rights Class 9 |
| `noaa_rights_class` | `9` | Always |
| `noaa_rights_policy_id` | `"noaa_rights_matrix_v1"` | Always |
| `endorsement_restrictions` | `"noaa_nonendorsement_policy"` | Always — NOAA name/logo may not imply federal endorsement per 5 U.S.C. § 3110 |
| `noaa_license_id` | Flickr `license` value | Evidence of primary gate field |
| `noaa_credit` | Extracted credit string | Evidence of credit gate field |
| `noaa_partner_markers` | From `classify_rights` result | REVIEW_REQUIRED records only |
| `noaa_contributor_markers` | From `classify_rights` result | Present but empty for ALLOWED records |
| `noaa_blocked_markers` | From `classify_rights` result | Empty for writes; populated in rejected pre-gate returns |
| `noaa_original_rights_uri` | `rights_statement_uri` from NOAA `classify_rights` | Preserved when NKC/1.0/ override is applied for REVIEW_REQUIRED |

`endorsement_restrictions: "noaa_nonendorsement_policy"` is mandatory on every NOAA write. It must be present and non-null in the evidence JSON. The shared store does not enforce this; the NOAA `build_evidence_extension` callback must add it unconditionally.

### VI.3 Mandatory Field Warnings Gate

`mandatory_evidence_warnings(normalized)` must return an empty list for all written records. Any record with mandatory field warnings must be rejected at the pre-gate with `reason: "invalid_normalized_record"`. The warning check runs on the full evidence envelope including the extension fields.

---

## VII. Anchor Type

NOAA records must have `anchor_type` assigned in `StoreRuntime`. NOAA content is predominantly biological (marine organisms, fisheries, coral reef species) with secondary geographic content (coastal surveys, ocean maps).

**Derivation rules:**

| Condition | Anchor Type |
|---|---|
| `subject_terms` contains one or more biological tokens | `"biological"` |
| `edm_type == "map"` or title contains geographic tokens | `"geographic"` |
| Default | `"biological"` |

Biological tokens: `fish`, `coral`, `whale`, `shark`, `sea`, `ocean`, `marine`, `bird`, `mollusk`, `crustacean`, `cephalopod`, `algae`, `kelp`, `species`, `specimen`, `plankton`.

Geographic tokens: `map`, `chart`, `survey`, `bathymetry`, `coastline`, `boundary`, `nautical`.

`"biological"` is the correct default for NOAA, unlike AIC where `"cultural"` is the default.

---

## VIII. SA-9 Compatibility

SA-9 adds `"noaa"` as the 13th source slug in the M36 write path. SA-9 must be completed before Sprint 3 implementation begins. The compatibility requirements:

### VIII.1 StoreRuntime Configuration

NOAA's `_runtime()` function must instantiate `StoreRuntime` with:

```
worker_id             = "noaa_adapter:sprint3"
source_slug           = "noaa"
schema_standard       = "noaa_discovery_v1"
technical_schema_version = "noaa-discovery-technical-v1"
validator_name        = "noaa_adapter.technical"
validator_version     = "v1"
rights_policy_id      = "noaa_rights_matrix_v1"
workflow_record_id_key = "source_record_id"
anchor_type           = (derived per Section VII)
build_technical_metadata = (NOAA technical.py callable)
validation_status     = (NOAA technical.py callable)
build_evidence_extension = (NOAA extension callable per Section VI.2)
```

`source_slug = "noaa"` is the SA-9 requirement. The `build_provenance` function in the shared store writes `"nc:source": runtime.source_slug` into every provenance JSON blob. NOAA's `"noaa"` slug must appear in every write for the audit trail to be correct.

### VIII.2 Evidence Source Attribution

After SA-9 is applied, all provenance records for NOAA writes will contain:
```json
{
  "prov:wasGeneratedBy": "noaa_adapter:sprint3",
  "nc:source": "noaa",
  "nc:source_identifier": "<record_id>",
  "nc:raw_payload_hash": "<sha256>"
}
```

This is the canonical NC attribution chain for NOAA records. No manual slug remapping is needed if `StoreRuntime.source_slug = "noaa"` is set correctly.

### VIII.3 SA-9 Completion Gate

SA-9 is complete when:
1. NOAA `store.py` is created with `StoreRuntime(source_slug="noaa", ...)`
2. A Sprint 3 replay test confirms `"nc:source": "noaa"` in the provenance output of an ALLOWED write
3. No other adapter's slug is used in NOAA write paths

SA-9 requires no changes to other adapters or to the shared store module.

---

## IX. Required Replay Tests

Sprint 3 requires seven replay tests before M36 write path authorization. All tests must use the mock-transport pattern (no live database connection). Write counts and payload contents must be deterministic.

### T1 — ALLOWED record produces 7 substrate writes

Fixture: `flickr_photo_usgov_clean_noaa.json` (license 8, clean NOAA credit)

Assertions:
- `result["status"] == "written"`
- `result["writes"] == 7`
- `result["workflow_item_id"] is None`
- Provenance JSON contains `"nc:source": "noaa"`
- Evidence JSON contains `"endorsement_restrictions": "noaa_nonendorsement_policy"`
- Evidence JSON contains `"noaa_legal_basis": "17 U.S.C. § 105"`
- Evidence JSON does NOT contain `rights_status: "verified_pd"` (FM-4)

### T2 — REVIEW_REQUIRED record produces 8 writes and workflow_item

Fixture: `flickr_photo_nasa_esa_review.json` (credit: NASA/ESA, license 8)

Assertions:
- `result["status"] == "written"`
- `result["writes"] == 8`
- `result["workflow_item_id"] is not None`
- Workflow item `context.item_payload["noaa_rights_basis"] == "partner_or_contributor_marker"`
- Workflow item `context.item_payload["noaa_partner_markers"]` contains `"NASA/ESA"`
- Normalized `rights_uri == "https://rightsstatements.org/vocab/NKC/1.0/"` (mapped)
- Evidence JSON contains `"noaa_original_rights_uri": "https://rightsstatements.org/vocab/NoC-US/1.0/"` (preserved)

### T3 — Commercial operator produces 0 writes

Fixtures: `flickr_photo_getty_blocked.json`, `flickr_photo_reuters_blocked.json`, `flickr_photo_ap_blocked.json`

Assertions for each:
- `result["status"] == "rejected"`
- `result["writes"] == 0`
- `result["reason"] == "blocked_partner_marker"`

### T4 — Personal name produces 0 writes (SPC-3-3)

Fixture: `flickr_photo_personal_noaa_review.json`

Assertions:
- `result["status"] == "rejected"`
- `result["writes"] == 0`
- `result["reason"] == "contributed_image_exception"`

This test is the Sprint 3 enforcement of SPC-3-3 regardless of what rights.py returns. If rights.py returns REVIEW_REQUIRED, the store pre-gate still rejects.

### T5 — FM-4: rights_status never 'verified_pd' in any write path

Fixture: `flickr_photo_usgov_clean_noaa.json`

Assertions:
- `result["status"] == "written"`
- The SQL args passed to `insert_media_rights` do NOT contain `"verified_pd"` or `"classified_pd"` as the `rights_status` parameter
- `media_rights.rights_status` SQL parameter is always `'pending_verification'`

(Implementation note: the shared store hardcodes `'pending_verification'` in the SQL string. This test confirms the NOAA store does not override this with a custom `insert_media_rights` call.)

### T6 — SA-9: source_slug is "noaa" in provenance

Fixture: `flickr_photo_usgov_clean_noaa.json`

Assertions:
- `build_provenance(normalized, runtime)["nc:source"] == "noaa"`
- `result["status"] == "written"`
- No other source slug appears in any provenance JSON in the write path

### T7 — Evidence extension is complete on all ALLOWED writes

Fixture: `flickr_photo_usgov_clean_noaa.json`

Assertions:
- `evidence["endorsement_restrictions"] == "noaa_nonendorsement_policy"`
- `evidence["noaa_legal_basis"] == "17 U.S.C. § 105"`
- `evidence["noaa_rights_class"] == 9`
- `evidence["noaa_access_path"] == "flickr"`
- `evidence["noaa_primary_gate_field"] == "license_id"`
- `evidence["noaa_rights_policy_id"] == "noaa_rights_matrix_v1"`

---

## X. Sprint 3 Entry Gates

All gates must be cleared before Sprint 3 M36 write path implementation begins. Sprint 3 planning is already authorized (NOAA Sprint 2 Remediation Review v1).

### Entry Gate A — SPC-3-2: url_m Removed

`choose_image_url` in `client.py` must iterate only `("url_o", "url_l", "url_c", "url_z")`. A record with only `url_m` available returns `None` and is rejected at the pre-gate with `reason: "invalid_normalized_record"`.

Verification: `test_noaa_client_rejects_url_m_only_record` passing.

### Entry Gate B — SA-NOAA-001 v1.1 Ratified

SA-NOAA-001 v1.1 must be drafted and ratified, incorporating:
- SPC-3-3 resolution: personal name credits produce `rejected: "contributed_image_exception"` at store layer
- NKC/1.0/ as the shared-path URI for REVIEW_REQUIRED records entering the workflow_item path
- NOAA-specific evidence extension fields from Section VI.2
- Store-layer REVIEW_REQUIRED sub-types (foreign agency, partner institution, PD-no-credit)

### Entry Gate C — SA-9 Specification

SA-9 must be formally applied: the NOAA Sprint 3 store module must use `source_slug = "noaa"` in `StoreRuntime`. Verified by T6.

### Carry-Forward Gates (must close before full catalog harvest)

- **Gate 5:** NSIDs confirmed for @usoceangov and @noaafisheries
- **Gate 6:** Photo Library evaluation finding (Gate 2A or 2B)
- **SPC-3-1:** NOAA space-prefix added before Path B activation

---

## XI. Sprint 3 Scope

### Authorized

- M36 write path for Flickr Path A (ALLOWED records)
- Workflow item creation for REVIEW_REQUIRED records (foreign agency, partner institution, PD-no-credit)
- `store.py` module creation in `workers/noaa_adapter/`
- SA-9 application (source_slug = "noaa")
- SA-NOAA-001 v1.1 and SA-NOAA-002 v1.1 drafting and ratification
- Contract field completion in `normalize.py` (`date`, `subject_terms`, `provider`, `dataProvider`, `edm_type`, `preview_urls`)
- Anchor type derivation in `store.py`

### Pilot Constraints (binding)

- Maximum 50 ALLOWED writes per pilot run (DD-NOAA-001 Article 10)
- Pilot scope: Florida Keys + Hawaii marine ecosystems
- Pilot duration: 90 days from first write
- Full catalog harvest requires separate authorization after pilot completes

### Not Authorized Until Further Gates

- Path B (NOAA Photo Library) — requires Gate 6 (Gate 2A finding) and SPC-3-1
- Other Flickr accounts beyond @usoceangov — requires Gate 5 (NSIDs confirmed)
- Full catalog harvest — requires pilot completion finding
- `rights_status` promotion beyond `'pending_verification'` — requires human review workflow (M36 standard; no NOAA-specific work needed)

### Not In Scope (Sprint 3)

- Asset Zero selection — contingent on pilot run finding
- SPC-3-1 (NOAA space-prefix) — Path B prerequisite, not Sprint 3 unless Path B activates
- Any modification to the shared store module (`workers/shared_media_adapter/store.py`)
- Any SA-9 work that modifies other adapters

---

## XII. Ratification Table

| Role | Ratified | Date |
|---|---|---|
| Governance Review | ☐ PENDING | — |
| Principal Architect | ☐ PENDING | — |

---

*NOAA Sprint 3 Governance Review v1 — drafted 2026-06-11*  
*Architecture basis: `workers/shared_media_adapter/store.py` · `workers/aic_adapter/store.py` · `workers/shared_media_adapter/contracts.py`*  
*Authority: DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · IFC-1 · NOAA Sprint 2 Remediation Review v1*  
*Sprint 3 planning: previously authorized · Sprint 3 M36 implementation: conditional on Entry Gates A, B, C*
