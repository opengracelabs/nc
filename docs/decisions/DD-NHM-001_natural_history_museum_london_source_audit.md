# DD-NHM-001: Natural History Museum London — Source Audit and Activation Decision

**Type:** Decision Document — Institution Source Audit  
**Status:** DRAFT — Pending Ratification  
**Authority:** Institution Factory Constitution v1 (IFC-1–IFC-12), DD-GALLICA-003 (ToS disqualification precedent), DD-GETTY-001 (IIIF + Linked Art precedent)  
**Institution Number:** #17  
**Date Drafted:** 2026-06-10  
**Drafted By:** NC Principal Architect  

---

## DECISION

**CONDITIONAL**

The Natural History Museum London (NHM) is CONDITIONALLY APPROVED as a production source for the NC commercial illustration pipeline, subject to the conditions in this document. NHM holds direct NC Priority Illustrator content (Nodder, Parkinson, Haeckel), confirmed IIIF v3, and a publicly accessible API. The conditional status arises from a two-tier rights structure that requires NHM-specific rights gate logic and Sprint 1 confirmation before ingestion may begin.

---

## I. INSTITUTION PROFILE

**Institution:** Natural History Museum, London  
**URL:** https://www.nhm.ac.uk/  
**Data Portal:** https://data.nhm.ac.uk/  
**Type:** National natural history museum; independent charity  
**Established:** 1881 (founded on collections from the British Museum, 1753)  
**Scale:** 80 million+ specimens; 6+ million digitized records on Data Portal; 350,000 artworks in Library and Archives; 100+ datasets on the Data Portal  
**Geographic scope:** Global — specimens and illustrations from virtually every bioregion, with colonial-era depth for Africa, Asia-Pacific, South America, and the Pacific  

NHM London is one of the world's leading natural history institutions and the direct institutional successor to Hans Sloane's 18th-century collection. Its Library and Archives hold approximately 350,000 artworks including the original Sydney Parkinson botanical field sketches from Cook's First Voyage (1768–1771), the Frederick Nodder finished watercolours derived from Parkinson's drawings, and Haeckel's *Kunstformen der Natur* lithographs. These constitute NC Priority Tier 1 illustration content by named Priority Illustrators.

NHM has operated a Digital Collections Programme since 2014 and published a formal Open Information and Exceptions Policy in 2024 (DOI: 10.3897/rio.10.e120629), adopting an open-by-default stance under the Science International Open Data Accord.

---

## II. RIGHTS AND COMMERCIAL USE AUDIT (IFC-1 GATE)

### II.1 Two-Tier Rights Structure

NHM's rights framework splits on the institutional tier of access. This split is the governing architectural fact of this DD.

**Tier A — Data Portal (data.nhm.ac.uk):**

Collection specimens, natural history records, and associated datasets: **CC0** (dataset-level metadata) and **CC BY** (digital media/images). The Data Portal Terms state: *"You may use the data contained in this site for any purpose, providing it does not infringe the licence and terms & conditions."* CC BY 4.0 explicitly permits commercial use. No license fee is mentioned for Data Portal images.

- Source: https://data.nhm.ac.uk/terms-conditions
- Policy: https://riojournal.com/article/120629/ (Open Information and Exceptions Policy, 2024)

**Tier B — Library and Archives (nhmimages.com picture library):**

Items where NHM holds copyright: licensed under the **Non-Commercial Government Licence**. Commercial use requires a **paid license through NHM Images** (https://nhmimages.com), a commercial picture library. Items where copyright belongs to third parties (not NHM): restricted to non-commercial research or private study.

**Public Domain exception:** Items where no copyright subsists under UK law — primarily pre-1900 works by named creators who died before 1954 — are explicitly described by NHM as *"free of restrictions under UK copyright law allowing commercial use without permission."* NHM asks that these be used in accordance with Europeana Foundation guidelines (requested, not legally binding).

- Source: https://www.nhm.ac.uk/our-science/services/library/collections.html

### II.2 IFC-1 Gate Analysis

**Tier A (Data Portal) IFC-1 status:** PASSED. CC BY 4.0 permits commercial use; no license fee; no ToS commercial restriction. The NC Getty adapter provides a directly applicable precedent (CC BY is more permissive than Getty's CC0 for purposes of NC's IFC-1 gate — both permit commercial use).

**Tier B Library/Archives NHM-copyright IFC-1 status:** BLOCKED. The Non-Commercial Government Licence and commercial fee through NHM Images is structurally identical to the BnF/Gallica disqualifier (DD-GALLICA-003). Commercial reuse requires a paid licensing agreement with NHM that has not been secured.

**Public domain illustration IFC-1 status:** PASSED. Pre-copyright works (Parkinson, Nodder, Haeckel) carry no NC blocker. Attribution is requested but not legally required under UK copyright law.

**NC decision:** NC MUST restrict ingestion to Tier A (Data Portal) and confirmed public domain items. Tier B NHM-copyright Library/Archives content is outside NC's production scope unless a commercial licence is secured with NHM Images.

### II.3 Commercial License Fee Assessment

Tier A: **None confirmed.** Data Portal CC BY images are commercially usable without fee.  
Tier B: **Fee required.** NHM Images operates as a commercial picture library for NHM-copyright artwork. No fee schedule reviewed; not pursued.  
Public domain: **None.** Copyright expired.  

**Attribution requirement (Tier A):** Standard CC BY attribution — *"© The Trustees of the Natural History Museum, London."* Machine-readable in dataset metadata.  
**Attribution requirement (public domain):** NHM requests *"Library and Archives, Natural History Museum, London"* — voluntary, not legally binding.

### II.4 ToS Commercial Restriction Analysis

No confirmed ToS commercial restriction on Data Portal CC BY content. The "no misleading association with NHM" clause was not confirmed in research. The no-endorsement language applying to Library/Archives items does not extend to Data Portal CC BY content under the available documentation.

---

## III. CONTENT TYPE ASSESSMENT

NHM London passes the content type gate. Unlike ALA (DD-ALA-001, DISQUALIFIED for wrong content type), NHM holds confirmed golden-age natural history illustration content by NC named Priority Illustrators.

### III.1 Confirmed NC Priority Illustrator Content

| Illustrator | NHM Holdings | Status | Period |
|---|---|---|---|
| **Frederick Nodder** | Cook Voyages finished watercolours (derived from Parkinson) | Confirmed in Library; online gallery | fl. 1700–1801 |
| **Sydney Parkinson** | Original botanical field sketches, HMS Endeavour 1768–1771 | Confirmed; publicly accessible | 1745–1771 |
| **Ernst Haeckel** | *Kunstformen der Natur* coloured lithographs | Confirmed in Library holdings | 1899–1904 |
| John Gould | ~10,800 bird skin specimens (post-mortem acquisition) | Specimen collection only; illustration plates NOT confirmed | — |
| Audubon, Merian, Redouté, Lear, Wolf | Likely present in Library | **Not confirmed digitized** | — |

**Cook Voyages / Endeavour collection** (primary NC target):
- ~900+ botanical drawings from HMS Endeavour (1768–1771), HMS Resolution, HMS Discovery
- Artists: Sydney Parkinson (original field sketches), Frederick Nodder (finished watercolours)
- Online gallery: https://www.nhm.ac.uk/our-science/departments-and-staff/library-and-archives/collections/cook-voyages-collection/endeavour-botanical-illustrations/
- Digitized and publicly accessible
- All pre-1800, public domain, Pacific/Australia/New Zealand geographic scope

**NC strategic value:** Nodder is NC Priority Illustrator #6 (named in Illustration Opportunity Doctrine). Parkinson's original field drawings are the source material for Nodder's finished plates. This is the only confirmed institutional holding of Nodder originals at scale. NHM's Cook Voyages content fills NC's Pacific and Australia/New Zealand geographic gap, for which current NC institutions have zero coverage (ALA was disqualified; no Pacific institution currently in pipeline).

### III.2 Specimen Collection Content (Tier A mainstream)

The Data Portal's primary resource is 6+ million digitized natural history specimen records covering:
- Entomology (~33 million specimens total; world's largest insect collection, digitization ongoing)
- Ornithology (bird skins, eggs, nests)
- Botany (algae, bryophytes, ferns, seed plants)
- Paleontology (invertebrate and vertebrate fossils)
- Mineralogy and petrology

Specimen images are primarily close-up scientific photographs (not golden-age illustration plates), but high-quality natural history subject matter for NC's specimen-photograph tier. Commercial use under CC BY.

---

## IV. CONNECTIVITY AND API AUDIT

### IV.1 Data Portal API

**Base URL:** `https://data.nhm.ac.uk/api/3`  
**Primary endpoint:** `POST/GET /action/datastore_search`  
**Required parameter:** `resource_id` (UUID)  
**Primary collection specimens resource:** `05ff2255-c38a-40c9-b657-4ccb55ab2feb`  
**Documentation:** https://naturalhistorymuseum.github.io/dataportal-docs/  
**GitHub:** https://github.com/NaturalHistoryMuseum  

**Pagination:** Offset-based (`offset`, `limit`). Default limit: 100 records per request. Total record count available in response.  
**Authentication:** Not required for read access.  
**Rate limits:** Not numerically published. "Multiple calls per second" will result in suspension. Caching required.  
**Data format:** JSON (primary). Darwin Core Archive (DwC-A), CSV, Excel for bulk downloads.  
**Bulk download:** Confirmed. DwC-A and CSV exports. Large downloads asynchronous (email notification).  
**Standards:** Darwin Core; RDF (Turtle, JSON-LD, N3, RDF/XML) via HTTP content negotiation; 5-star linked open data.  

**Adapter class:** CKAN Datastore API. This is a **new ingestion class** for NC — the first CKAN-based institution. Prior protocols: REST cursor pagination (Met/AIC/CMA/SMK), CSV bulk download (NGA/Walters), Linked Art page-number pagination (Yale), ActivityStreams + REST (Getty), Europeana EDM. SA-20 required.

### IV.2 Stage 3 Connectivity Assessment

| Criterion | Status |
|---|---|
| Public API (no private-only gate) | CONFIRMED |
| Authentication required | NOT REQUIRED for reads |
| HTTPS | CONFIRMED |
| Stable documented endpoints | CONFIRMED |
| Rate limits | UNPUBLISHED (soft limit; caching required) |
| Bulk download | CONFIRMED (DwC-A) |

Stage 3: CLEARED with condition — Sprint 1 must implement request rate control and caching layer.

### IV.3 IIIF Audit

**IIIF Image API:** CONFIRMED — v3.0, Level 3 compliance.  
**Implementation:** Custom FastAPI server: https://github.com/NaturalHistoryMuseum/iiif-image-server  
**Production endpoint:** `https://data.nhm.ac.uk/vfactor_iiif`  
**Identifier format:** `<profile>:<name>` two-part identifier. Default profile renders prefix optional.  
**Image sources:** Disk (local) and `mss` (NHM internal storage, cached on retrieval).  

**IIIF Presentation API:** CONFIRMED — via `ckanext-iiif` CKAN extension.  
**Implementation:** https://github.com/NaturalHistoryMuseum/ckanext-iiif  
**Manifest URL pattern:** `/iiif/resource/<resource_id>/record/<record_id>`  
**Manifest generation:** Auto-generated when images are present on the record via `_image_field` metadata.  
**Presentation API version:** Not explicitly stated in available documentation — must be confirmed in Sprint 1.  

**IIIF URL derivability:** YES — manifests are constructable from `resource_id` + `record_id`. The link between Data Portal record UUIDs and IIIF image identifiers is confirmed via the ckanext-iiif extension logic but exact field name for the image identifier in the API response is not confirmed and must be verified in Sprint 1.

**NHM is NOT a confirmed IIIF Consortium member** (NHM does not appear on the iiif.io/community/consortium/members/ list).

**IIIF Version note:** NHM uses IIIF Image API v3 (Level 3) — same version as Yale (first v3 in NC pipeline). The Presentation API version requires Sprint 1 confirmation before the NHM adapter's manifest parser is written. If v3: reuse Yale IIIF v3 manifest traversal pattern (`items[]` canvas structure). If v2: reuse the Getty `sequences[]` pattern.

---

## V. RIGHTS MODEL CLASSIFICATION

### V.1 Rights Class Assignment

**Rights class:** Dataset-level CC license — **Rights Class 8 (new)**.

NHM's rights are attached at the dataset/resource level, not the individual record level. The CKAN `license_id` metadata field on each dataset (e.g., `cc-by`, `cc-zero`, `CC-BY-4.0`) governs all records in that dataset. This differs from:

- Rights Class 1–7 (per-record URI, boolean field, string field, integer flag, institution-wide, Linked Art)
- Rights Class 8: Dataset-level CC license — license verified once per dataset, applied to all records fetched from that dataset resource

This architecture means the NHM adapter MUST:
1. Verify the `license_id` of the target dataset before any record is fetched
2. Reject any dataset that does not carry `cc-zero`, `cc-by`, or `CC-BY-4.0`
3. Treat any dataset with `cc-by-nc`, `cc-by-nc-sa`, or unrecognized license as BLOCKED
4. Apply this dataset-level gate as a proxy for IFC-1 per-record compliance

**Critical unconfirmed:** Whether individual records within a CC BY dataset can carry a different (more restrictive) license at the record level via the Darwin Core `dcterms:license` field. This MUST be confirmed in Sprint 1. If per-record overrides exist, the adapter must implement per-record fallback checking.

SA-21 (NHM Rights Matrix v1) governs this classification.

### V.2 NHM Rights Matrix v1 (SA-21 Scope)

| Condition | Decision | Basis |
|---|---|---|
| Dataset `license_id` missing or unrecognized | BLOCKED | `missing_dataset_license` |
| Dataset `license_id` is CC BY-NC or more restrictive | BLOCKED | `non_commercial_dataset` |
| Dataset `license_id` is CC BY or CC0 | ALLOWED | `nhm_cc_by` or `nhm_cc0` |
| Per-record `dcterms:license` override is more restrictive | BLOCKED | `record_license_override` (if confirmed) |

`rights_policy_id`: `"nhm_rights_matrix_v1"`  
Source slug: `"nhm"` (single institution, no dual-institution routing)

---

## VI. ASSET ZERO

### VI.1 Recommendation

**Sydney Parkinson — Botanical field sketch, HMS Endeavour (1768–1771)**  
Online gallery: https://www.nhm.ac.uk/our-science/departments-and-staff/library-and-archives/collections/cook-voyages-collection/endeavour-botanical-illustrations/  
Geographic anchor: Pacific / Australia / New Zealand  
Creator: Sydney Parkinson (1745–1771)  
Period: 1768–1771  
Rights: Public domain (Parkinson died 1771; over 250 years)  

**NC rationale:** The Endeavour botanical illustrations are NC's most strategically valuable unacquired content. They fill the Pacific geographic gap (no current NC institution covers Pacific/Australia), represent the origin moment of European natural history illustration for that bioregion, and are associated with the HMS Endeavour voyage — a world-recognized cultural and scientific event. Nodder (NC Priority Illustrator #6) created the finished watercolour versions of Parkinson's sketches; both series are held at NHM.

**Alternative Asset Zero (Haeckel):**  
Ernst Haeckel — *Kunstformen der Natur* plate (1899–1904)  
NHM Library holdings; public domain  
Haeckel is within NC's Golden Age window; *Kunstformen* plates are among the most commercially recognizable natural history illustrations of the 19th century.

### VI.2 Sprint 1 Asset Zero Confirmation Required

The Asset Zero path requires Sprint 1 to confirm whether:
1. The Endeavour botanical illustrations are accessible via the Data Portal API and IIIF endpoints
2. Or whether they exist only as a web gallery (nhm.ac.uk/endeavour-botanical-illustrations) without IIIF/API support

If the Endeavour illustrations are Library-only (not on the Data Portal), Asset Zero shifts to a Haeckel *Kunstformen* plate or a Tier A Data Portal specimen image until the illustration access question is resolved.

---

## VII. PILOT SCOPE

**Recommended Pilot:** Pacific / Cook Voyages Natural History  
**Target asset count:** 75  
**Duration:** 90 days  
**Rights gate:** CC BY or CC0 (Tier A) and confirmed public domain (Parkinson/Nodder/Haeckel)  
**Primary anchor place:** Pacific Ocean / Australia / New Zealand  

**Rationale:** The Cook Voyages anchor is NC's first Pacific content and fills the geographic gap most prominently flagged in the Institution Coverage Audit v1 (zero coverage for Asia-Pacific). The pilot scope is achievable entirely within confirmed NHM Data Portal content and confirmed public domain illustration holdings.

**Pilot success criteria:**
1. ≥75 records ingested with `rights_decision=ALLOWED` from CC BY or public domain datasets
2. Zero IFC-1 violations (no non-commercial dataset records written)
3. M36 write order preserved for 100% of records
4. IIIF Presentation API manifest extraction confirmed (v2 or v3 — per Sprint 1 finding)
5. Dataset-level rights gate verified before first record fetch
6. Asset Zero (Parkinson/Nodder or Haeckel) written at MASTERWORK quality tier

---

## VIII. DECISION ARTICLES

**Article 1 — Conditional Production Authorization**  
The Natural History Museum London is CONDITIONALLY APPROVED as a production source under NC's commercial-use requirements. The conditions are defined in Articles 5–11 and in the Sprint 1 confirmation requirements (Article 12). Conditional status converts to full APPROVED upon ratification of SA-20, SA-21, and Sprint 1 completion.

**Article 2 — Institution Number**  
NHM is assigned Institution #17 in the NC institution registry.

**Article 3 — Source Slug**  
Source slug: `nhm`. Single institution, no dual-institution routing.

**Article 4 — Rights Class Assignment**  
NHM is classified under Rights Class 8 (new): dataset-level CC license via CKAN `license_id`. SA-21 (NHM Rights Matrix v1) governs classification. SA-20 (CKAN Datastore Adapter Profile) governs the ingestion protocol.

**Article 5 — Tier Restriction (IFC-1 Condition)**  
NC MUST restrict ingestion to: (a) Data Portal (data.nhm.ac.uk) datasets with confirmed CC BY or CC0 `license_id`; and (b) confirmed public domain items (Parkinson, Nodder, Haeckel — pre-1900 artists with expired copyright). NC MUST NOT access Library and Archives NHM-copyright content via NHM Images or any route that requires a commercial license agreement with NHM. Any dataset with a non-commercial license designation MUST be blocked at the adapter level before any record is fetched.

**Article 6 — Dataset Rights Gate**  
The NHM adapter MUST verify the `license_id` of the target dataset resource before fetching any records. Datasets with `license_id` values of `cc-by-nc`, `cc-by-nc-sa`, `OGL-UK-2.0` (where confirmed non-commercial), or any unrecognized value MUST be blocked. The dataset rights gate is the NHM equivalent of IFC-1.

**Article 7 — Per-Record Override Check (Conditional)**  
If Sprint 1 confirms that individual records within CC BY datasets can carry a more restrictive `dcterms:license` value, the NHM adapter MUST implement per-record license checking as a secondary gate. If Sprint 1 confirms per-record override is not present in the API response, Article 7 conditions are vacated for Sprint 2.

**Article 8 — IIIF Presentation API Version**  
The NHM adapter MUST confirm in Sprint 1 whether the Presentation API at `/iiif/resource/<resource_id>/record/<record_id>` returns v2 or v3 manifests. If v2: implement the `sequences[]` canvas traversal pattern (Getty precedent). If v3: implement the `items[]` canvas traversal pattern (Yale precedent). Both patterns are already ratified in the NC adapter codebase.

**Article 9 — Endeavour Illustration Pathway**  
Sprint 1 MUST determine whether the Cook Voyages / Endeavour botanical illustrations (Parkinson, Nodder) are accessible via the Data Portal API and IIIF, or only via the web gallery at nhm.ac.uk. If accessible via Data Portal: these records enter the standard NHM adapter pipeline with public domain rights basis. If web-gallery-only without API/IIIF: Asset Zero shifts to Haeckel *Kunstformen* plates and the Endeavour pathway is deferred to DD-NHM-002 (Library partnership).

**Article 10 — FM-4 Invariant**  
FM-4 applies without exception: the NHM adapter worker MUST write `"pending_verification"` (not `"verified_cc0"` or `"verified_cc_by"`) to `media_rights.rights_status`. Reclassification occurs in `build_rights_evidence` via the shared store.

**Article 11 — SA-9 Extension**  
SA-9 (`build_rights_evidence` source slug remap) MUST be extended to include `"nhm"` before Sprint 3. Current required slugs: met, aic, cma, smk, nga, walters, ycba, yuag, getty, **nhm** (10 slugs). SA-9 is critically overdue across four institutions and must be resolved before any Sprint 3 work on NHM, NGA, Walters, Yale, or Getty.

**Article 12 — Sprint 1 Confirmation Requirements**  
Before Sprint 1 adapter implementation begins, the following must be confirmed via direct API inspection:
1. IIIF Presentation API version (v2 or v3) at `/iiif/resource/.../record/...`
2. Field name for image identifier in the CKAN datastore record response (required to construct IIIF image URL)
3. Whether `dcterms:license` or equivalent per-record rights override exists in API JSON
4. Whether Endeavour / Cook Voyages illustrations are present as a named dataset on data.nhm.ac.uk with IIIF delivery
5. Rate limit behaviour — confirm caching layer is sufficient to avoid suspension

**Article 13 — NHM Images Commercial Route (Deferred)**  
A future DD-NHM-002 may revisit the Library and Archives NHM-copyright content route if a commercial licensing agreement is negotiated with NHM Images. DD-NHM-002 is NOT a prerequisite for production activation of the Tier A Data Portal route. The Tier A route is independently viable without any Library/Archives commercial agreement.

---

## IX. ARCHITECTURAL CLASSIFICATION SUMMARY

| Dimension | NHM | Getty | Yale |
|---|---|---|---|
| Rights class | 8 (dataset-level CC BY, new) | 7 (Linked Art `subject_to`, per-record) | 7 (Linked Art `subject_to`, per-record) |
| Ingestion protocol | CKAN Datastore (new) | ActivityStreams + REST (new) | Page-number pagination |
| IIIF Image API | v3 (confirmed) | v2 | v3 |
| Presentation API | Confirmed (version TBD) | v2 (confirmed) | v3 (confirmed) |
| Manifest derivable? | YES (resource_id + record_id) | NO (extract from record) | YES (constructible) |
| Auth required | No | No | No |
| NC Priority Illustrators | Nodder (confirmed), Haeckel (confirmed) | None confirmed | None confirmed |
| Pacific gap coverage | YES — fills entirely | No | No |

---

## X. RISK REGISTER

| ID | Risk | Severity | Probability | Mitigation |
|---|---|---|---|---|
| R-1 | Endeavour illustrations are web-gallery-only (no Data Portal API/IIIF) | High | Medium | Article 9 fallback to Haeckel Asset Zero; Library partnership DD-NHM-002 |
| R-2 | IIIF Presentation API is v2 (contradicts `iiif-image-server` v3 implementation) | Low | Low | Sprint 1 confirms; either v2 or v3 path is already implemented in NC |
| R-3 | Per-record `dcterms:license` overrides exist in CC BY datasets | Medium | Low | Sprint 1 confirms; Article 7 activates if true |
| R-4 | CKAN rate limiting causes harvest timeouts | Medium | Medium | Sprint 1 implements caching layer; SA-20 specifies backoff |
| R-5 | SA-9 overdue — blocks Sprint 3 across NHM + 4 other institutions | High | High | SA-9 must be resolved immediately; blocks NHM + NGA + Walters + Yale + Getty Sprint 3 |
| R-6 | Tier B Library/Archives content inadvertently accessed | High | Low | Article 5 hard gate; adapter restricted to data.nhm.ac.uk domain only |
| R-7 | Haeckel *Kunstformen* dates (1899–1904) overlap with NHM-copyright claim | Low | Low | Haeckel died 1919; works are public domain in all relevant jurisdictions |

---

## XI. STANDARDS AMENDMENTS REQUIRED

| SA | Title | Blocks | Status |
|---|---|---|---|
| SA-9 | `build_rights_evidence` source slug remap (add `nhm`) | NHM Sprint 3 | OVERDUE — also blocks NGA, Walters, Yale, Getty Sprint 3 |
| SA-20 | CKAN Datastore Adapter Profile | NHM Sprint 1 | REQUIRED |
| SA-21 | NHM Rights Matrix v1 (dataset-level CC gate) | NHM Sprint 1 | REQUIRED |

---

## XII. RATIFICATION TABLE

| Role | Approval | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

**Conditions for ratification:**
1. SA-20 scope accepted (CKAN Datastore protocol defined)
2. SA-21 scope accepted (dataset-level CC rights matrix defined)
3. Institution #17 assignment recorded in NC institution registry
4. Asset Zero designation accepted (Parkinson/Nodder Endeavour or Haeckel *Kunstformen* — per Sprint 1 Article 9 outcome)
5. Article 5 Tier Restriction acknowledged by governance

---

*DD-NHM-001 drafted 2026-06-10 under authority of Institution Factory Constitution v1.*  
*Precedents: DD-GALLICA-003 (Tier B Library/Archives analysis), DD-GETTY-001 (IIIF v3 + ActivityStreams), DD-ALA-001 (content type doctrine).*
