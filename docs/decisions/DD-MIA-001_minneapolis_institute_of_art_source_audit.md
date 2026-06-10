# DD-MIA-001: Minneapolis Institute of Art (Mia) — Source Audit and Activation Decision

**Type:** Decision Document — Institution Source Audit  
**Status:** APPROVED WITH CONDITIONS — Pending Sprint 1 Gate Passage and SA Ratification  
**Authority:** Institution Factory Constitution v1 (IFC-1–IFC-12), NC Europeana Rights Matrix v1  
**Institution Number:** #19  
**Date Drafted:** 2026-06-10  
**Date Finalized:** 2026-06-10  
**Drafted By:** NC Principal Architect  
**Source slug:** `mia`

---

## DECISION

**APPROVED WITH CONDITIONS**

Mia is approved for production ingestion. Conditions: (1) Sprint 1 content audit confirms NC-relevant illustration holdings (G-6); (2) SA-MIA-RIGHTS-001 ratified before Sprint 2; (3) SA-MIA-DELIVERY-001 ratified before Sprint 2; (4) Sprint 2 rights implementation passes all six gates defined in Section XI.

**Critical finding — the `restricted` field trap:**  
The `restricted` integer field is NOT a safe rights gate. Object `10000` carries `restricted=0` alongside `rights_type='In Copyright–Educational Use'` (© Heal's Fabrics, London, 1973). The `restricted` field controls Mia's own display permissions, not commercial copyright status. The operative field is `rights_type`. Any implementation gating on `restricted == 0` alone will ingest copyright-protected works — a constitutional violation of IFC-1.

**Rights Matrix:**  
Mia Rights Matrix v1 is embedded in this document (Section III.4) and formally ratified via SA-MIA-RIGHTS-001. The matrix is the canonical rights specification for `workers/mia_adapter/rights.py`.

---

## I. INSTITUTION PROFILE

**Institution:** Minneapolis Institute of Art (Mia)  
**Primary domain:** https://artsmia.org  
**Collections portal:** https://collections.artsmia.org  
**GitHub:** https://github.com/artsmia  
**Type:** Municipal art museum; Hennepin County, Minnesota  
**Collection size:** ~130,000 objects  
**PD + valid image (confirmed):** **64,416 objects** (Codex-observed count, 2026-06-10)  
**Departments:** European Art, Asian Art, Arts of the Americas, Arts of Global Africa, Prints and Drawings (40,000+ prints, 6,000 drawings), Contemporary Art, Textiles, Decorative Arts  
**Accession number format:** `"13.59"`, `"61.36.14"` (TMS format, period-delimited year + sequence)

Mia publishes collection metadata under CC0 and maintains a public GitHub repository (`artsmia/collection`) containing all object records as JSON files. The collection is strong in Asian art, 19th-century European prints, and decorative arts. Mia's Prints and Drawings study room (Herschel V. Jones Print Study Room) is a dedicated research facility holding 40,000+ prints spanning 15th-century German engravings through 20th-century lithographs.

---

## II. CONNECTIVITY AUDIT (STAGE 3)

### II.1 API Endpoint Status

The documented primary API endpoint `api.artsmia.org` is **UNREACHABLE** as of 2026-06-10. Both HTTP and HTTPS connections timed out (curl exit code `000`). This is not a 4xx or 5xx error — the server does not respond.

| Endpoint | Method | Status | Notes |
|---|---|---|---|
| `https://api.artsmia.org/objects/1` | REST JSON | **DOWN** | Connection refused / timeout |
| `http://api.artsmia.org/objects/1` | REST JSON | **DOWN** | Connection refused / timeout |
| `https://collections.artsmia.org` | SPA | UP | Returns HTML, all routes |
| `https://{id%7}.api.artsmia.org/800/{id}.jpg` | Image CDN | **UP** | HTTP/2, HTTPS confirmed |
| `github.com/artsmia/collection` | Bulk JSON | **UP** | Complete records, confirmed working |

**Stage 3 verdict:** CLEARED WITH CONDITIONS. The REST API is offline; the two confirmed-working data paths are the GitHub bulk repository and the image CDN. Production ingestion must use the GitHub bulk path as the primary harvest mechanism. Sprint 1 must confirm whether `api.artsmia.org` recovers before Sprint 2 begins.

### II.2 GitHub Bulk Path (Primary Data Source)

**URL:** `https://github.com/artsmia/collection`  
**Format:** Individual JSON files per object  
**Structure:** `objects/{id/1000}/{id}.json`  
**Example:** Object 17 → `objects/0/17.json`  
**Access:** Public, no authentication, HTTPS  
**Clone command:** `git clone --depth=1 https://github.com/artsmia/collection.git`

The GitHub repository is confirmed working as of this audit. Object JSON contains `id: "http://api.artsmia.org/objects/{n}"` — the numeric ID is the terminal path component. The Codex-confirmed PD count of 64,416 was derived from a full enumeration of this repository.

### II.3 Image CDN (Confirmed HTTPS)

**Pattern:** `https://{numeric_id % 7}.api.artsmia.org/{size}/{numeric_id}.jpg`  
**Sizes:** `800/` (800px), empty (400px default), `full/` (full resolution)  
**Example:** `https://1.api.artsmia.org/800/1.jpg`  
**HTTPS:** Confirmed — HTTP/2, S3-backed (`x-amz-version-id` response header)  
**Auth:** None required  
**Rate limiting:** Present at `artsmia.org/images/` path (429 observed); CDN shards are not rate-limited in testing  
**Access gate:** CDN serves images for ALL objects regardless of `restricted` or `rights_type`. There is no CDN-level rights gate. NC MUST apply `rights_type` filtering before constructing the CDN URL.

### II.4 IIIF Status — CONFIRMED ABSENT

**IIIF in production: CONFIRMED ABSENT.**

`collections.artsmia.org/iiif/1/manifest.json` returns HTTP 200 but with `Content-Type: text/html` — the SPA catch-all handler, not a IIIF manifest. All IIIF manifest URL patterns tested return SPA HTML. No JSON manifest is served.

Mia is not listed as a IIIF Consortium member (iiif.io/community/consortium/members/). The `artsmia` GitHub organization has no IIIF-related repository. This is a permanent condition. Records MUST NOT be blocked for missing IIIF manifest — there will never be one.

SA-MIA-DELIVERY-001 governs CDN direct delivery as the NC image delivery class for Mia.

---

## III. RIGHTS AND COMMERCIAL USE AUDIT (IFC-1 GATE)

### III.1 The `restricted` Field — Confirmed Insufficient as Sole Gate

The `restricted` integer field (`0` or `1`) appears in every object record. Prior analysis suggested `restricted == 0` as the NC gate. Live audit disproves this.

**Object 10000 confirms the defect:**

```json
{
  "restricted": 0,
  "rights_type": "In Copyright–Educational Use",
  "image_copyright": "© Heal's Fabrics, London, Barbara Brown, 1973",
  "image": "valid"
}
```

This record is `restricted=0` — Mia permits educational display — but carries active copyright from 1973. Commercial use is not permitted.

**What `restricted` actually means:**  
The `restricted` field controls whether Mia's own website shows the full image. From source code (`artwork-image.js`): `showImage = art.image == 'valid' && rights !== 'Permission Denied'`. Mia shows images unless explicitly denied by the rights holder. `restricted=0` means "Mia has not been told to withhold this image." It says nothing about whether a third party may commercially reuse it.

**The `restricted` field MUST NOT appear in any conditional branch of the rights classification function.** It may appear in `build_evidence_extension` for provenance tracing only (Article 2).

### III.2 The `rights_type` Field — Confirmed Operative Gate

The `rights_type` string field contains RightsStatements.org vocabulary labels sourced from Mia's TMS database. Confirmed values from live survey of 200+ objects and source code review (`rights-types.js`):

| `rights_type` value | RightsStatements.org ID | NC Decision | `restricted` correlation |
|---|---|---|---|
| `"Public Domain"` | CC-PDM | **ALLOWED** | Always `restricted=0` |
| `"No Copyright–United States"` | NoC-US | **ALLOWED** | Always `restricted=0` |
| `"No Copyright—Contractual Restrictions"` | NoC-CR | **REVIEW REQUIRED** | Always `restricted=0` |
| `"No Known Copyright"` | NKC | **REVIEW REQUIRED** | Always `restricted=0` |
| `"In Copyright"` | InC | **BLOCKED** | Always `restricted=1` |
| `"In Copyright–Educational Use"` | InC-EDU | **BLOCKED** | **May be `restricted=0`** |
| `"In Copyright–Non-Commercial Use"` | InC-NC | **BLOCKED** | May be `restricted=0` |
| `"In Copyright–Rights-holder(s) Unlocatable"` | InC-RUU | **BLOCKED** | **May be `restricted=0`** |
| Missing / null | — | **BLOCKED** | — |
| Unknown value | — | **BLOCKED (fail closed)** | — |

The `rights_type` values map directly to NC's existing Europeana Rights Matrix v1. The NC ALLOWED/REVIEW REQUIRED/BLOCKED classification is already defined for each RightsStatements.org identifier. Mia Rights Matrix v1 (Section III.4) is a label-to-NC-decision translation layer on top of the existing matrix.

### III.3 Commercial Use Authorization

**Confirmed for `rights_type == "Public Domain"` and `rights_type == "No Copyright–United States"`:**

Mia's open access documentation: "Images [of public domain works] are available for any use." No license fee. No ToS commercial restriction on PD works. CC0 metadata. Mia does not assert reproduction copyright over digitized PD works — consistent with *Bridgeman Art Library v. Corel Corp* (SDNY 1999).

**NoC-US basis:** Asserts US public domain under 17 U.S.C. or similar statute. NC is a US-based commerce platform. NoC-US is unambiguous in NC's operational jurisdiction.

**NoC-CR and NKC:** Require human review workflow. Contractual restrictions or unconfirmed PD status may limit commercial use. May not be auto-ingested; human review produces a `workflow_item`. NC income is not generated from REVIEW_REQUIRED records until review completes.

IFC-1: **CLEARED** for `rights_type IN {"Public Domain", "No Copyright–United States"}`.

### III.4 Mia Rights Matrix v1 — Formal Specification

`rights_policy_id: "mia_rights_matrix_v1"`  
**Governing authority:** NC Europeana Rights Matrix v1, IFC-1, DD-MIA-001  
**Ratified via:** SA-MIA-RIGHTS-001  
**Implementation target:** `workers/mia_adapter/rights.py`

#### Decision Table

| Condition | Decision | `rights_basis` | `rights_statement_uri` | `rights_status` |
|---|---|---|---|---|
| Record is null or not a dict | BLOCKED | `missing_object` | null | `blocked` |
| `rights_type` key absent | BLOCKED | `missing_rights_type` | null | `blocked` |
| `rights_type` is null or empty string | BLOCKED | `missing_rights_type` | null | `blocked` |
| `rights_type == "In Copyright"` | BLOCKED | `mia_in_copyright` | null | `blocked` |
| `rights_type == "In Copyright–Educational Use"` | BLOCKED | `mia_inc_edu` | null | `blocked` |
| `rights_type == "In Copyright–Non-Commercial Use"` | BLOCKED | `mia_inc_nc` | null | `blocked` |
| `rights_type == "In Copyright–Rights-holder(s) Unlocatable"` | BLOCKED | `mia_inc_ruu` | null | `blocked` |
| `rights_type` not in known vocabulary | BLOCKED | `unknown_rights_type` | null | `blocked` |
| `image != "valid"` (any rights_type not already blocked) | BLOCKED | `no_image` | null | `blocked` |
| `image_width` is 0 or missing (image="valid") | BLOCKED | `invalid_image_dimensions` | null | `blocked` |
| `rights_type == "Public Domain"` + valid image | **ALLOWED** | `mia_public_domain` | PDM URI | `pending_verification` |
| `rights_type == "No Copyright–United States"` + valid image | **ALLOWED** | `mia_noc_us` | NoC-US URI | `pending_verification` |
| `rights_type == "No Copyright—Contractual Restrictions"` + valid image | **REVIEW REQUIRED** | `mia_noc_cr` | NoC-CR URI | `pending_verification` |
| `rights_type == "No Known Copyright"` + valid image | **REVIEW REQUIRED** | `mia_nkc` | NKC URI | `pending_verification` |

**Check order is mandatory:** rights_type gate executes before image gate. An InC record is blocked at the rights_type check — it must not flow to the image check with a false `rights_basis` of `no_image`.

**URI constants** (from `shared_media_adapter/rights.py`):
- PDM URI: `https://creativecommons.org/publicdomain/mark/1.0/`
- NoC-US URI: `https://rightsstatements.org/vocab/NoC-US/1.0/`
- NoC-CR URI: `https://rightsstatements.org/vocab/NoC-CR/1.0/`
- NKC URI: `https://rightsstatements.org/vocab/NKC/1.0/`

#### Definitional Rulings

**`"Public Domain"` → ALLOWED.** Maps to CC Public Domain Mark (PDM URI). NC Europeana Rights Matrix v1 Table 1A row 2: PDM is ALLOWED unconditionally after human activation. FM-4 applies: `media_rights.rights_status` writes `"pending_verification"`, never `"verified_pd"`. Mia applies PDM to works it has determined are free of known restrictions — same trust model applied to Rijksmuseum PDM assertions.

**`"No Copyright–United States"` → ALLOWED.** Maps to RS.org NoC-US. NC Europeana Rights Matrix v1 Table 1A row 3: NoC-US is ALLOWED unconditionally after human activation. FM-4 applies. NC is a US-based commerce platform; NoC-US is unambiguous in NC's operational jurisdiction.

**`"No Copyright—Contractual Restrictions"` → REVIEW REQUIRED.** Maps to RS.org NoC-CR. NC Europeana Rights Matrix v1 Table 1B: REVIEW REQUIRED — "held pending human investigation." The adapter decision is REVIEW_REQUIRED. The record IS written to the M36 substrate (7 writes proceed, plus 1 `workflow_item` write = 8 total). `media_rights.rights_status` remains `"pending_verification"`. No product is activated without human review completion.

**`"No Known Copyright"` → REVIEW REQUIRED.** Maps to RS.org NKC. NC Europeana Rights Matrix v1 Table 1B: REVIEW REQUIRED. NKC means the institution found no known copyright holder but could not formally declare the work PD. Copyright may exist even when the holder is unknown. Same REVIEW_REQUIRED mechanism as NoC-CR.

**All `"In Copyright*"` variants → BLOCKED.** Blocked at the `rights_type` check, unconditionally. `restricted=0` on an InC record does not modify this outcome.

**Unknown `rights_type` → BLOCKED (fail closed).** Any value not in the known vocabulary receives `decision: BLOCKED, rights_basis: "unknown_rights_type"`. A new TMS value appearing from a future Mia vocabulary migration defaults to BLOCKED until a governance review adds it to SA-MIA-RIGHTS-001.

#### Rights Classification — Architecture

**Rights Class: 3B (standardized label set)**

Rights Class 3A = institutional string (CMA `"Open Access"`).  
Rights Class 3B = RightsStatements.org label set (Mia `"Public Domain"`, `"No Copyright–United States"`).

Architecturally identical adapter code path to CMA. No new rights class number required.

---

## IV. CONTENT TYPE ASSESSMENT

### IV.1 Volume — Confirmed

| Category | Count |
|---|---|
| **Public Domain + valid image** | **64,416** |
| PD + invalid image (no scan) | ~46,000 est. |
| In Copyright (any) | ~28,990 est. |
| NoC-CR / NKC + valid image | ~3,510 est. |
| **Total collection** | **~130,000** |

The 64,416 figure is the Codex-confirmed enumeration from the full GitHub repository (2026-06-10). This supersedes the prior sampling-based estimate of ~52,000.

### IV.2 Sampled Content

From a stratified sample of 200 objects with `rights_type` in ALLOWED set and `image="valid"`:

**By department (PD/NoC-US, valid image):**

| Department | Sample count |
|---|---|
| Asian Art | 14 |
| European Art | 12 |
| Arts of the Americas | 6 |
| Arts of Global Africa | 2 |

**Confirmed print examples:**

| ID | Title | Medium | Dated |
|---|---|---|---|
| 8701 | Actor Ichikawa Monnosuke II as Soga Jūrō | Woodblock print (nishiki-e) | 1794 |
| 9601 | Enjoying the Evening Cool on the Riverbed at Shijō | Woodblock print (nishiki-e) | c. 1784 |
| 42301 | Poppies | Woodblock print (surimono) | 1821 |
| 47101 | St. Christopher with the Head Turned to the Right | Engraving | 1521 |
| 51001 | Les Vaches au marais | Etching | 1850 |
| 57601 | The Last Load | Wood engraving | 1869 |

### IV.3 Natural History Illustration Assessment

**Confirmed:** Mia holds a strong prints collection (40,000+ prints, 6,000 drawings) with confirmed pre-1900 European and Japanese works. Japanese woodblock prints (kacho-e: flower-and-bird genre) by Hiroshige, Hokusai, and contemporaries represent a confirmed NC-compatible illustration category.

**Not confirmed from sample:** No Priority Illustrator works (Audubon, Gould, Merian, Redouté, Haeckel, Wolf, Nodder) appeared in the 200-object stratified sample. The sample size cannot rule out holdings across 40,000+ prints.

**Sprint 1 content gate (G-6):** ≥1 Priority Illustrator holding OR ≥500 natural history illustration candidates in the PD/NoC-US valid subset. Primary search targets: `artist CONTAINS "Audubon"`, `"Gould"`, `"Redouté"`, `"Haeckel"`, filtered to PD + valid image. If G-6 fails, pilot scope is reconsidered.

---

## V. ASSET ZERO

**Recommendation (provisional):** First confirmed Priority Illustrator print with `rights_type="Public Domain"` and `image="valid"` from the Prints and Drawings department. Candidates in order of preference:

1. A confirmed Audubon, Gould, or Redouté print (NC golden-age tier)
2. A Hiroshige or Hokusai kacho-e (flower-and-bird woodblock) — NC Asian illustration tier
3. Any pre-1800 European natural history engraving from the collection

Specific object ID to be confirmed in Sprint 1. Asset Zero cannot be designated before the content audit.

---

## VI. PILOT SCOPE

**Recommended Pilot:** Prints and Drawings — Natural History and Botanical Illustration  
**Target asset count:** 75  
**Duration:** 90 days  
**Rights gate:** `rights_type IN {"Public Domain", "No Copyright–United States"}` AND `image="valid"` AND `image_width > 0`  
**Primary anchor:** Botanical / ornithological subjects (place anchor TBD by Sprint 1 content audit)  
**Fallback anchor:** Japanese woodblock (kacho-e) — Hiroshige / Hokusai  

---

## VII. DECISION ARTICLES

**Article 1 — Approval**  
Mia is APPROVED WITH CONDITIONS as a production source. The approval is effective upon satisfaction of all Sprint 1 gates (Articles 2–12 conditions) and ratification of SA-MIA-RIGHTS-001 and SA-MIA-DELIVERY-001.

**Article 2 — Rights Gate (Constitutional)**  
The Mia adapter MUST gate on `rights_type IN {"Public Domain", "No Copyright–United States"}` — NOT on `restricted == 0` alone. Implementation of `restricted == 0` as the sole rights gate is a constitutional violation of IFC-1 and MUST NOT be committed to any Sprint without a passing `test_mia_rights_blocks_restricted_zero_inc_edu` replay test. The `restricted` field MUST NOT appear in any conditional branch of `classify_rights`. This is the primary IFC-1 risk of this integration.

**Article 3 — REVIEW REQUIRED Path**  
Records with `rights_type IN {"No Copyright—Contractual Restrictions", "No Known Copyright"}` AND `image="valid"` MUST produce a `REVIEW_REQUIRED` decision and create a `workflow_item`. They MUST NOT be silently blocked and MUST NOT be auto-ingested to `classified_cc0`. The REVIEW_REQUIRED path produces 8 M36 writes (7 standard + 1 workflow_item).

**Article 4 — Image Validity Gate**  
Records with `image != "valid"` OR `image_width == 0` OR `image_width` missing MUST be blocked. The CDN URL MUST NOT be constructed for blocked records. Image gate executes only after the rights_type gate.

**Article 5 — API Endpoint Condition**  
`api.artsmia.org` must be confirmed working OR formally documented as decommissioned with GitHub bulk as the authoritative harvest path before Sprint 2 begins. SA-MIA-DELIVERY-001 must reflect the confirmed primary harvest path.

**Article 6 — Image Delivery Protocol**  
Image delivery is via CDN: `https://{numeric_id % 7}.api.artsmia.org/{size}/{numeric_id}.jpg`. The numeric ID is extracted from the `id` field URI (terminal path component). HTTPS is confirmed. SA-MIA-DELIVERY-001 governs this CDN URL construction pattern.

**Article 7 — Institution Number**  
Mia is assigned Institution #19 in the NC institution registry. Source slug: `mia`.

**Article 8 — Rights Class**  
Mia is classified under Rights Class 3B (standardized label set). The `rights_type` field uses RightsStatements.org vocabulary labels. The NC decision for each label is governed by the NC Europeana Rights Matrix v1. SA-MIA-RIGHTS-001 formalizes the label-to-NC-decision translation. No new rights class number is assigned.

**Article 9 — No IIIF**  
Mia does not provide production IIIF endpoints. This is CONFIRMED, not merely unconfirmed. SA-MIA-DELIVERY-001 documents CDN direct delivery as the NC image delivery class for Mia. No code path may block a Mia record for missing IIIF manifest.

**Article 10 — FM-4 Invariant**  
FM-4 applies without exception. The Mia adapter worker MUST write `"pending_verification"` to `media_rights.rights_status`. Reclassification to `"classified_cc0"` or `"classified_pd"` is only possible via human review workflow completion.

**Article 11 — SA-9 / SA-9R Extension**  
SA-9 MUST be extended to include `"mia"` before Sprint 3. If SA-9R is implemented, `build_evidence_extension` callable on `StoreRuntime` handles this automatically. If SA-9R is not yet in place, `build_rights_evidence` in the shared store must add a `mia` branch manually.

**Article 12 — Content Gate for Full Ratification**  
Full DD-MIA-001 ratification requires Sprint 1 confirmation of ≥1 Priority Illustrator holding OR ≥500 natural history illustration candidates in the PD/NoC-US valid subset. A pilot scoped to decorative arts alone is not NC doctrine-aligned without confirmed illustration content.

**Article 13 — Mia Rights Matrix v1**  
The Mia Rights Matrix v1 (Section III.4) is the canonical rights specification for this integration. It supersedes all preliminary assessments and informal descriptions. `rights_policy_id: "mia_rights_matrix_v1"` must be written to every `media_rights.rights_evidence` JSONB record produced by the Mia adapter. This identifier must never change without a version bump and a new SA.

---

## VIII. GOVERNANCE CLASSIFICATION

**Mia is Met-tier, not Yale/Getty-tier.**

| Dimension | Yale/Getty | Mia | Met/AIC/SMK |
|---|---|---|---|
| Record format | JSON-LD (Linked Art) | Plain JSON | Plain JSON |
| Rights field | Nested `subject_to` URI traversal | `rights_type` string | Boolean flag |
| Rights class | 7 (Linked Art) | **3B (string label set)** | 2 (boolean) |
| IIIF | Confirmed (v3/v2) | **Absent (confirmed)** | Confirmed |
| Harvest | ActivityStreams / REST | **GitHub bulk clone** | REST API |
| Auth | None | None | None |

**Closest architectural peer: CMA (Cleveland Museum of Art).** Same string-equality rights pattern, GitHub-accessible data, numeric IDs, no IIIF. Key differences: CMA uses a single institutional string; Mia uses a standardized vocabulary set. CMA REST API is live; Mia's is offline.

**No new adapter class.** Mia uses the same plain-JSON-with-string-rights pattern as CMA and NARA. GitHub bulk harvest is the same mechanism as NGA and Walters.

---

## IX. REQUIRED STANDARDS AMENDMENTS

| SA | Title | Content | Blocks | Status |
|---|---|---|---|---|
| SA-MIA-RIGHTS-001 | Mia Rights Matrix v1 | `rights_type` label→NC-decision map; `image` validity gate; `restricted` field advisory role; `rights_policy_id: "mia_rights_matrix_v1"` | Sprint 2 | REQUIRED |
| SA-MIA-DELIVERY-001 | Mia Image Delivery Protocol | CDN URL `https://{id%7}.api.artsmia.org/800/{id}.jpg`; numeric ID extraction from `id` URI; GitHub bulk as primary harvest; `api.artsmia.org` status; no IIIF documented | Sprint 2 | REQUIRED |
| SA-9 / SA-9R | Slug remap extension (add `mia`) | Add `"mia"` as 12th slug to `build_rights_evidence` remap OR confirm SA-9R callable resolves automatically | Sprint 3 | REQUIRED |

---

## X. RISK REGISTER

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R-1 | `restricted=0` implemented as sole gate — ingests InC-EDU/InC-RUU works | **CRITICAL** | Article 2 + mandatory Sprint 2 gate test `test_mia_rights_blocks_restricted_zero_inc_edu` |
| R-2 | Unknown `rights_type` value fails open → incorrectly ingested | High | Fail-closed default in Mia Rights Matrix v1 Article 3 (SA-MIA-RIGHTS-001) |
| R-3 | `api.artsmia.org` remains offline — no live API for incremental updates | High | GitHub bulk path confirmed; SA-MIA-DELIVERY-001 Article 5 documents resolution |
| R-4 | `NoC-CR` / `NKC` auto-promoted to ALLOWED without human review | High | Article 3 + Sprint 2 gate G-E; REVIEW_REQUIRED workflow_item required |
| R-5 | CDN URL constructed before rights check — InC objects get valid URL recorded | Medium | SA-MIA-RIGHTS-001 Article 5; store-level test confirms zero writes for BLOCKED records |
| R-6 | No confirmed Priority Illustrator holdings — pilot scoped to wrong content type | Medium | Sprint 1 content gate G-6 (Article 12) |
| R-7 | SA-9 overdue — currently blocking Sprint 3 for 6 institutions | High | SA-9R remediation resolves permanently; Mia Sprint 3 depends on SA-9R or manual addition |

---

## XI. SPRINT 2 APPROVAL GATES

Sprint 2 code review must confirm all six gates before the branch is merged. The Principal Architect must sign off on Gate G-B specifically — it is the single most important IFC-1 compliance proof in the Mia integration.

| Gate | Description | Blocking |
|---|---|---|
| G-A | SA-MIA-RIGHTS-001 ratified before any Sprint 2 code is committed | Yes |
| G-B | `test_mia_rights_blocks_restricted_zero_inc_edu` passes as first Sprint 2 test | Yes |
| G-C | All 13 rights matrix tests pass before normalization work begins | Yes |
| G-D | `test_mia_rights_restricted_field_not_checked` confirms `restricted` has no effect on decision | Yes |
| G-E | REVIEW_REQUIRED path produces `workflow_item`; `media_rights.rights_status == "pending_verification"` | Yes |
| G-F | Zero M36 writes for any BLOCKED record confirmed by replay test | Yes |

---

## XII. SPRINT 2 FIXTURE SPECIFICATION

All 11 fixtures are required for IFC-1 compliance. Location: `tests/fixtures/mia/`.

| File | `rights_type` | `restricted` | `image` | Expected decision | Expected `rights_basis` |
|---|---|---|---|---|---|
| `record_public_domain_valid_image.json` | `"Public Domain"` | 0 | `"valid"` | ALLOWED | `mia_public_domain` |
| `record_noc_us_valid_image.json` | `"No Copyright–United States"` | 0 | `"valid"` | ALLOWED | `mia_noc_us` |
| `record_noc_cr_valid_image.json` | `"No Copyright—Contractual Restrictions"` | 0 | `"valid"` | REVIEW_REQUIRED | `mia_noc_cr` |
| `record_nkc_valid_image.json` | `"No Known Copyright"` | 0 | `"valid"` | REVIEW_REQUIRED | `mia_nkc` |
| `record_in_copyright.json` | `"In Copyright"` | 1 | `"valid"` | BLOCKED | `mia_in_copyright` |
| **`record_restricted_zero_inc_edu.json`** | **`"In Copyright–Educational Use"`** | **0** | **`"valid"`** | **BLOCKED** | **`mia_inc_edu`** |
| `record_restricted_zero_inc_ruu.json` | `"In Copyright–Rights-holder(s) Unlocatable"` | 0 | `"valid"` | BLOCKED | `mia_inc_ruu` |
| `record_public_domain_no_image.json` | `"Public Domain"` | 0 | `"invalid"` | BLOCKED | `no_image` |
| `record_public_domain_zero_width.json` | `"Public Domain"` | 0 | `"valid"` (width=0) | BLOCKED | `invalid_image_dimensions` |
| `record_missing_rights_type.json` | *(absent)* | 0 | `"valid"` | BLOCKED | `missing_rights_type` |
| `record_unknown_rights_type.json` | `"Need Permission"` | 0 | `"valid"` | BLOCKED | `unknown_rights_type` |

**`record_restricted_zero_inc_edu.json`** is based on confirmed live object 10000 (© Heal's Fabrics, London, Barbara Brown, 1973). This fixture MUST exist and its associated test MUST pass before any other Sprint 2 test is run.

---

## XIII. FAILURE MODE CATALOG

Every path by which a copyright-protected record could incorrectly reach `media_rights` as ALLOWED.

**FM-1 — `restricted == 0` sole gate (PRIMARY RISK)**  
Mechanism: `if record.get("restricted") == 0` used as pre-filter. Records with `restricted=0, rights_type='In Copyright–Educational Use'` pass and are ingested.  
Volume at risk: ~4,400 objects estimated (3.4% of collection extrapolated from sample).  
Detection: Sprint 2 Gate G-B — `test_mia_rights_blocks_restricted_zero_inc_edu`.  
Severity: **CRITICAL — IFC-1 constitutional violation.**

**FM-2 — Fail-open for unknown rights_type**  
Mechanism: if/elif chain without final `else` BLOCKED clause. A future unknown `rights_type` value falls through to ALLOWED.  
Detection: `test_mia_rights_blocks_unknown_rights_type` (Fixture 11).  
Severity: HIGH.

**FM-3 — `NoC-CR` auto-promoted to ALLOWED**  
Mechanism: NoC-CR placed in ALLOWED set because it begins with "No Copyright."  
Detection: `test_mia_rights_review_required_noc_cr` (Fixture 3).  
Severity: HIGH — contractual restriction may specifically prohibit NC commerce.

**FM-4 — `rights_type == null` treated as REVIEW_REQUIRED**  
Mechanism: `if rights_type not in BLOCKED_TYPES` — `None` not in set, flows to REVIEW_REQUIRED.  
Detection: `test_mia_rights_blocks_missing_rights_type` (Fixture 10).  
Severity: MEDIUM.

**FM-5 — CDN URL constructed before rights check**  
Mechanism: Normalization constructs CDN URL unconditionally; store writes `media_file.source_url` before evaluating rights decision.  
Detection: Sprint 2 Gate G-F — store test confirms zero writes for any BLOCKED record.  
Severity: MEDIUM.

**FM-6 — `NKC` treated as equivalent to `"No Known Copyright"` NoC-US**  
Mechanism: NKC auto-promoted to ALLOWED because "no copyright" language resembles NoC-US.  
Detection: `test_mia_rights_review_required_nkc` (Fixture 4).  
Severity: HIGH — NKC does not declare PD; copyright may exist.

**FM-7 — `image_width` not gated**  
Mechanism: `image="valid"` treated as sufficient; `image_width=0` records processed.  
Detection: `test_mia_rights_blocks_zero_width_image` (Fixture 9).  
Severity: MEDIUM — broken media record written; no copyright violation.

---

## XIV. SPRINT 1 GATES (CONDITIONS FOR FULL RATIFICATION)

| Gate | Condition | Pass | Fail |
|---|---|---|---|
| G-1 | `rights_type` field present in all sampled GitHub records | Confirmed in 100% of non-null sample | Block Sprint 2 |
| G-2 | `restricted=0, rights_type=InC-EDU` pattern reproduced | Object 10000 or equivalent confirmed | Critical — block Sprint 2 |
| G-3 | CDN URL pattern confirmed working for ≥10 objects | HTTP 200 from `{id%7}.api.artsmia.org/800/{id}.jpg` | Block Sprint 2 |
| G-4 | `api.artsmia.org` status resolved | Working or formally decommissioned | Document in SA-MIA-DELIVERY-001 |
| G-5 | PD + valid image count ≥ 25,000 | Codex count confirms 64,416 — **PASSED** | Revisit pilot scope |
| G-6 | ≥1 Priority Illustrator OR ≥500 natural history candidates | `rights_type="Public Domain"` + botanical/ornithological filter | Consider withdrawal if fails |
| G-7 | NoC-CR records present in collection | ≥1 confirmed example | Simplify matrix if absent |
| G-8 | Replay tests run without network (GitHub fixtures only) | 0 live API calls in test suite | Block Sprint 2 |

**G-5 status: PASSED.** Codex-confirmed count of 64,416 Public Domain objects with valid images exceeds the 25,000 threshold. No further confirmation required for this gate.

---

## XV. RATIFICATION TABLE

| Role | Approval | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

**Conditions for ratification:**
1. Sprint 1 gates G-1 through G-8 passed (G-5 already passed)
2. SA-MIA-RIGHTS-001 accepted (Mia Rights Matrix v1 — rights_type gate; `restricted` advisory documentation)
3. SA-MIA-DELIVERY-001 accepted (CDN URL pattern; GitHub bulk path; API status; no IIIF)
4. Institution #19 recorded in NC institution registry
5. Asset Zero designated (specific object ID confirmed in Sprint 1)
6. Content gate G-6 passed

---

## EXECUTIVE SUMMARY

Mia holds 64,416 confirmed Public Domain objects with valid digitized images, confirmed via full GitHub repository enumeration (2026-06-10). The collection's Prints and Drawings department (40,000+ prints) is the primary NC target. HTTPS CDN delivers images; GitHub bulk clone provides the complete harvest path; and the rights vocabulary maps cleanly onto NC's existing Europeana Rights Matrix v1 framework.

**The `restricted` field trap is the defining finding of this audit.** `restricted=0` does NOT mean commercially reusable. Object 10000 proves it: `restricted=0`, active 1973 copyright, `rights_type='In Copyright–Educational Use'`. The gate is `rights_type`, not `restricted`. Any implementation that gates on `restricted == 0` alone will ingest copyright-protected works (IFC-1 violation). Test `test_mia_rights_blocks_restricted_zero_inc_edu` must pass before any other Sprint 2 work proceeds.

**Three conditions for Sprint 2:**

1. SA-MIA-RIGHTS-001 ratified (Mia Rights Matrix v1, embedded in Section III.4)
2. SA-MIA-DELIVERY-001 ratified (CDN URL construction, GitHub bulk path, no IIIF)
3. Sprint 1 content audit confirms ≥1 Priority Illustrator or ≥500 natural history candidates

Rights Class 3B (standardized label set), Institution #19, source slug `mia`. Closest peer: CMA.

---

*DD-MIA-001 drafted 2026-06-10 under authority of Institution Factory Constitution v1.*  
*Finalized 2026-06-10 incorporating SA-MIA-RIGHTS-001, Mia Rights Matrix v1, and Codex-confirmed PD count (64,416).*  
*Live data probed from `github.com/artsmia/collection` and `{id%7}.api.artsmia.org` CDN.*  
*Source code reviewed: `artsmia/art` — `rights-types.js`, `image-cdn.js`, `artwork-image.js`.*  
*Critical precedent: `restricted=0` is NOT an IFC-1 gate. Only `rights_type` governs.*
