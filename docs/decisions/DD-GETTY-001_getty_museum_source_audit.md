# DD-GETTY-001: J. Paul Getty Museum — Source Audit and Activation Decision

**Type:** Decision Document — Institution Source Audit  
**Status:** DRAFT — Pending Ratification  
**Authority:** Institution Factory Constitution v1 (IFC-1–IFC-12), DD-YALE-001 (Linked Art precedent)  
**Institution Number:** #16  
**Date Drafted:** 2026-06-10  
**Drafted By:** NC Principal Architect  

---

## I. BACKGROUND AND INSTITUTION PROFILE

### I.1 Institution Identity

The J. Paul Getty Museum is a world-class encyclopedic art museum operating two campuses in Los Angeles, California: the Getty Center (1997) and the Getty Villa (1974). The museum is a department of the J. Paul Getty Trust, a private foundation. The museum holds approximately 250,000 objects spanning antiquity through the present, with particular strength in pre-1900 European paintings, illuminated manuscripts, decorative arts, drawings, photographs, and Greek and Roman antiquities.

The Getty Museum launched the **Getty Open Content Program** (hereinafter "Open Content Program") in 2013 and has expanded it incrementally. As of March 2024, the museum has released approximately 88,000 high-resolution digital images under CC0 1.0 Universal — unconditional dedication to the public domain. A companion collection at the Getty Research Institute (GRI) contributes a further ~78,000 open content images (prints, maps, study images, botanical books), bringing the total across both Getty entities to approximately 160,000+ open content images. This audit covers the Getty Museum collection only; the GRI is a Tier 2 expansion target documented separately.

### I.2 NC Strategic Relevance

The Getty Museum fills four high-priority gaps in NC's current institution set:

1. **Natural history illustration (NC Priority Tier 1):** Confirmed holdings of Maria Sibylla Merian and Jan van Huysum works — two of NC's seven named Priority Illustrators (Merian as the definitive entomological/botanical illustrator of the Golden Age; Van Huysum as the canonical Dutch flower painter).
2. **Illuminated manuscripts:** Manuscript collection spanning 9th–16th centuries across Christian Europe, Byzantium, Armenia, North Africa, Ethiopia, Judaism, and Islam — rivaling the Walters Art Museum (Institution #13) while adding IIIF delivery that Walters currently lacks.
3. **Mediterranean antiquity:** Greek and Roman antiquities collection fills the ancient world gap absent from the current NC institution set.
4. **French and Dutch decorative arts (17th–18th century):** Furniture, ceramics, tapestries, and silver from NC's Golden Age illustration window (1750–1900 and its immediate precursors).

No current NC institution covers the Netherlands / Dutch Golden Age botanical axis at this depth.

### I.3 Institution Factory Onboarding Stage

Per Institution Factory Constitution v1, this DD covers Stages 1–7 (Discovery through Asset Zero). Stage 8 (Pilot) is recommended upon ratification.

| Stage | Name | Status |
|---|---|---|
| 1 | Discovery | Complete (this DD) |
| 2 | Governance | CLEARED — IFC-1 satisfied |
| 3 | Connectivity | CLEARED — public API, no auth gate confirmed |
| 4 | Rights | CLEARED with conditions — SA-18 required |
| 5 | Adapter | PENDING — new Getty adapter, SA-19 required |
| 6 | M36 | PENDING — standard write order, no new schema |
| 7 | Asset Zero | RECOMMENDED — Van Huysum "Vase of Flowers" (82.PB.70) |
| 8 | Pilot | RECOMMENDED — Netherlands / Dutch Golden Age, 75 assets |
| 9 | Operational | NOT YET |

---

## II. RIGHTS AND COMMERCIAL REUSE AUDIT (IFC-1 GATE)

### II.1 Open Content Program Policy

**Policy Name:** Getty Open Content Program  
**Policy URL:** https://www.getty.edu/projects/open-content-program/  
**FAQs URL:** https://www.getty.edu/projects/open-content-program/faqs/  
**License:** CC0 1.0 Universal  

The Open Content Program is a curated subset of the full museum collection. Each record individually carries or does not carry the CC0 designation; new works are added on a rolling basis as rights review is completed. The program is **per-record**, not institution-wide — this is documented below under the rights model classification.

Getty's own statement: *"The works depicted in the images are not protected by copyright, but Getty may have a copyright interest in the digital image of the work. To the extent that Getty owns copyright in the digital images, we have chosen to make the images freely available under CC0."*

### II.2 Commercial Reuse Determination

**Commercial use permitted:** YES — unconditional.

Getty explicitly states open content images may be used *"without restriction or fees for commercial and noncommercial purposes."* Getty's own examples of permitted commercial use include academic and commercial publications, products and merchandise, and movies and TV. Commercial print resale is explicitly in scope.

**License fee:** NONE. Zero.  
**Attribution requirement:** VOLUNTARY ONLY. Getty requests (does not require): *"Digital image courtesy of Getty's Open Content Program."* CC0 carries no legal attribution obligation.  
**Watermark or branding requirement:** NONE.  
**No-endorsement clause:** Not confirmed in sources reviewed. No open-content-specific restriction found.  
**Third-party rights caveat:** Standard disclaimer that some images may include persons or objects for which a third party claims rights (trademark, privacy). For pre-1900 natural history/botanical works, this is practically irrelevant.

### II.3 Terms of Service Analysis

**ToS URL:** https://www.getty.edu/legal/terms-of-use/  

The general ToS governs the Getty website broadly and asserts proprietary rights over website text, images, and marks. However, the ToS explicitly carves out open content images:

*"Other than the open content images identified on the website for unrestricted downloading and the portions of the website expressly made available under a Creative Commons license, all of the text, images, marks, and other content of the Getty websites are proprietary to Getty."*

Open content images therefore fall **outside** the ToS's intellectual property restrictions. This is structurally analogous to the NGA Open Access Policy. It is categorically distinct from BnF/Gallica (DD-GALLICA-003), where the ToS imposed a **license fee for commercial reuse** that was unresolved by copyright doctrine alone. No such commercial-use ToS restriction exists at Getty.

### II.4 IFC-1 Gate Ruling

**IFC-1 PASSED.** Every record entering the Getty adapter must carry a confirmed CC0 rights URI in its Linked Art `subject_to` field before proceeding. The Getty adapter MUST enforce this gate at the record level — institution-wide permissibility does not eliminate per-record verification because the Open Content Program is a curated subset.

The Getty adapter MUST NOT write any record where `subject_to` does not contain a confirmed CC0 URI. Non-open-content records MUST be blocked with `rights_basis: "not_open_content"` or the applicable rejection basis from Getty Rights Matrix v1.

---

## III. CONNECTIVITY AND API AUDIT

### III.1 Primary Data Access Mechanism

The Getty Museum does not publish a flat CSV or JSON bulk download equivalent to Met, NGA, or Walters. There is no `thegetty/collection` GitHub repository. The data access model is exclusively API-based.

**Two primary access paths:**

**Path A — Linked Art REST API (individual record fetch):**  
Base: `https://data.getty.edu/museum/collection/`  
Entity types: `object`, `person`, `group`, `place`, `document`, `exhibition`, `activity`  
Example (object): `https://data.getty.edu/museum/collection/object/<UUID>`  
Response: JSON-LD per the Linked Art 1.0 specification.  

**Path B — ActivityStreams Change Feed (bulk harvest):**  
Base: `https://data.getty.edu/museum/collection/activity-stream`  
First page: `https://data.getty.edu/museum/collection/activity-stream/page/1`  
Protocol: W3C ActivityStreams 2.0 ordered collection. Each page lists created/modified/deleted record events with links to the full record URIs. Sequential page traversal constitutes a complete collection harvest.  

**SPARQL Endpoint:**  
`https://data.getty.edu/museum/collection/sparql`  
Available for complex graph queries. Not the primary harvest path but available for pilot and curation work.

**Developer documentation:**  
`https://data.getty.edu/museum/collection/docs/`  
`https://www.getty.edu/projects/open-data-apis/`

### III.2 Stage 3 Connectivity Assessment

| Criterion | Status |
|---|---|
| Public API (no private-only gate) | CONFIRMED |
| Authentication required | NOT CONFIRMED REQUIRED (likely none; verify in Sprint 1) |
| Rate limits published | NOT CONFIRMED (verify in Sprint 1) |
| HTTPS | CONFIRMED (data.getty.edu) |
| Stable endpoint / documented | CONFIRMED |

**Stage 3 verdict: CLEARED.** Unlike Paris Musées (DD-PARISMUSEES-001, Stage 3 BLOCKED due to private API returning thumbnails-only on public endpoints), Getty's API is published open data with documented endpoints and no confirmed authentication gate. The ActivityStreams harvest path is a recognized W3C standard. Sprint 1 must confirm: (a) no API key required, (b) rate limits if any, (c) User-Agent policy.

### III.3 ActivityStreams Harvest Protocol (New Ingestion Class)

The ActivityStreams change feed is a **new ingestion protocol class** for NC. Prior protocols in use:

| Protocol | Used By |
|---|---|
| REST cursor pagination | Met, AIC, SMK |
| OAI-PMH | (not used) |
| CSV bulk download (GitHub) | NGA, Walters |
| ActivityStreams + REST | **Getty (new)** |
| Linked Art page-number pagination | Yale |

The ActivityStreams protocol provides incremental update capability — the change feed allows NC to harvest new and modified records without re-fetching the entire collection. This is architecturally superior to full CSV re-downloads and to pagination-based crawls for long-term operations. SA-19 is required to ratify this protocol.

### III.4 ID Space Complexity

Getty assigns three distinct identifiers to each object:

1. **Linked Art UUID** (primary API key): e.g., `c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb`  
   URL: `https://data.getty.edu/museum/collection/object/<UUID>`  
2. **Collection page short ID**: e.g., `103JNH`  
   URL: `https://www.getty.edu/art/collection/object/103JNH`  
3. **Accession number**: e.g., `90.PA.20` (Irises), `82.PB.70` (Van Huysum)  

The NC Getty adapter MUST treat the Linked Art UUID as the `record_id` / primary identifier. Accession numbers MUST be preserved as a secondary identifier field (`getty_accession_number`). The collection page short ID is for human reference only and need not be stored.

---

## IV. IIIF AUDIT

### IV.1 IIIF Image API

**Confirmed.** Endpoint pattern: `https://media.getty.edu/iiif/image/<IMAGE_UUID>`  
All Open Content Program images are IIIF-enabled. Coverage is aligned to the ~88,000 open content museum images (all open content images are IIIF accessible).

### IV.2 IIIF Presentation API

**Confirmed.** Endpoint pattern: `https://media.getty.edu/iiif/manifest/<MANIFEST_UUID>`  
Example (Van Gogh Irises): `https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b`

**IIIF Version:** Presentation API v2 (context: `http://iiif.io/api/presentation/2/context.json`). This is the same version as Europeana and Rijksmuseum. No confirmed v3 implementation.

**Getty is a IIIF Consortium member.** Confirmed at iiif.io/community/consortium/members/.

### IV.3 Critical: Manifest UUID Is Not Derivable from Object UUID

**This is a significant adapter constraint.**

The manifest UUID (`53be857e-41e8-4198-b45d-2e0f52d3051b`) is distinct from and not arithmetically derivable from the Linked Art object UUID (`c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb`). The manifest link must be extracted from the object record itself.

The Linked Art object record is expected to contain the manifest reference via a `subject_of` or `representation` predicate (per Linked Art spec). The exact field path must be confirmed in Sprint 1. The adapter MUST extract the manifest URI from the record rather than constructing it from the object UUID.

This contrasts with Yale (where manifest URLs are constructible as `https://manifests.collections.yale.edu/<slug>/obj/<id>`). It introduces a dependency: the manifest cannot be requested without first fetching the full object record.

### IV.4 IIIF Audit Verdict

| Criterion | Status |
|---|---|
| Image API | CONFIRMED |
| Presentation API | CONFIRMED (v2) |
| Coverage (open content) | CONFIRMED (100% of open content set) |
| Manifest URL derivable from object ID | NO — must extract from record |
| IIIF Consortium member | YES |

---

## V. ARCHITECTURAL CLASSIFICATION

### V.1 Rights Model Classification

**Class:** Per-record, Linked Art `subject_to` URI form — **Rights Class 7 variant**.

The Getty Linked Art API encodes rights via the `subject_to` predicate in a Linked Art / CIDOC-CRM JSON-LD structure. The allowed CC0 URI is `https://creativecommons.org/publicdomain/zero/1.0/`.

**Critical field path difference from Yale:**

Yale's `subject_to` appears at the top level of the record object. Getty's rights assertion is expected at a different traversal depth — preliminary research indicates the path `referred_to_by[N].subject_to[M].classified_as[K].id`. This must be confirmed in Sprint 1.

This traversal variant does not constitute a new rights class (the semantic pattern is identical — scan a `subject_to` array for allowed URI). It does require a Getty-specific rights extraction function in the Getty adapter rather than direct reuse of Yale's `extract_subject_to_uris`. Getty Rights Matrix v1 (SA-18) governs this.

**Rights URI inventory for Getty adapter:**

| URI | NC Decision | Notes |
|---|---|---|
| `https://creativecommons.org/publicdomain/zero/1.0/` | ALLOWED | Open Content Program designation |
| All other URIs | BLOCKED | Not in Open Content Program |

No PDM or NoC-US is anticipated for the Getty Museum's primary open content designation. The Open Content Program uses CC0 exclusively.

### V.2 Ingestion Protocol Classification

**New protocol class: ActivityStreams 2.0 change feed + REST record fetch.**

This is the first ActivityStreams-based institution in NC's pipeline. The harvest loop is: paginate the activity-stream feed → extract record URIs for created/modified events → fetch each record from the Linked Art REST API → process through rights gate → store.

SA-19 must ratify this protocol including:
- Feed traversal termination condition
- Handling of `Delete` events (tombstone management)
- Page ordering guarantees
- Incremental vs full-harvest modes

### V.3 Getty Rights Matrix v1 (SA-18 Scope)

SA-18 must specify:

1. The exact field traversal path for `subject_to` within Getty Linked Art records (to be confirmed Sprint 1)
2. The single allowed URI (`CC0_URI`) and all blocked outcomes
3. Basis names: `"getty_cc0"` (allowed), `"missing_subject_to"`, `"no_rights_statement"`, `"not_open_content"` (blocked)
4. `rights_policy_id`: `"getty_rights_matrix_v1"`
5. Source slug: `"getty"` (single institution, no dual-institution routing)

### V.4 Comparison with Prior Institutions

| Dimension | Getty | Yale (YCBA/YUAG) | NGA | Walters |
|---|---|---|---|---|
| Rights class | 7 (variant) | 7 | 5 | 6 |
| Institution-wide? | No (per-record subset) | No (per-record) | No (per-record flag) | Yes |
| Bulk harvest path | ActivityStreams (new) | Page-number pagination | CSV/GitHub | CSV/GitHub |
| IIIF v | v2 | v3 | v2 only | None |
| Manifest derivable? | No — extract from record | Yes — constructible | N/A | N/A |
| Auth required | Likely none | None | None | None |
| Dual institution? | No | Yes | No | No |

---

## VI. ASSET ZERO

### VI.1 Selection Criteria (per Institution Factory v1)

Asset Zero must be: (a) confirmed open content / CC0, (b) pre-1900, (c) highest illustration tier alignment for NC, (d) IIIF accessible, (e) representative of institution's unique contribution to NC's collection.

### VI.2 Recommended Asset Zero

**Jan van Huysum — "Vase of Flowers" (1722)**  
Accession: 82.PB.70  
Collection page: https://www.getty.edu/art/collection/object/103REY  
Estimated Linked Art UUID: confirm in Sprint 1  
IIIF: confirmed accessible (manifest UUID to be extracted in Sprint 1)

**Rationale:**

1. **Priority Illustrator alignment.** Jan van Huysum is not one of NC's named seven Priority Illustrators, but the Dutch Golden Age flower painters are within NC's canonical Golden Age window (1700–1900). Van Huysum (1682–1749) is the supreme exemplar of Dutch botanical still life — "the god of flowers" — and his works have sold as fine art prints since the 18th century.

2. **Illustration tier.** "Vase of Flowers" is unambiguously ILLUSTRATION TIER for NC: highly detailed botanical composition, individual species identifiable, no figures, pure natural history subject matter. Direct commercial print product alignment.

3. **Pre-1800 (1722).** Well within NC's Golden Age priority window.

4. **Geographic anchor.** Fills Netherlands / Dutch Golden Age as a new NC place anchor. No current NC institution owns this geographic + subject combination at this depth.

5. **No overlap with Yale Asset Zero candidates.** Yale's primary axis is British art (YCBA) and American/New Haven collections (YUAG). Van Huysum does not compete with Yale's collection identity.

**Alternative Asset Zero (MASTERWORK tier):**  
Vincent van Gogh — "Irises" (1889)  
Accession: 90.PA.20  
Linked Art UUID: `c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb`  
IIIF Manifest: `https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b`

Irises provides maximum brand recognition and is also a botanical subject (irises as natural history subject). However, it is 1889 — late in the Golden Age window — and its commercial print market is already saturated. Recommended as SECONDARY asset zero only. Van Huysum is preferred for NC Asset Zero.

---

## VII. PILOT SCOPE

**Recommended Pilot:** Netherlands / Dutch Golden Age Natural History  
**Target asset count:** 75  
**Duration:** 90 days  
**Rights gate:** CC0 only (Open Content Program)  
**Primary anchor place:** Netherlands (Holland)

**Rationale:** The Netherlands anchor encompasses NC's most commercially valuable Getty assets — botanical still lifes, entomological illustrations (Merian's Amsterdam period), and Golden Age natural history subjects. This pilot directly fills NC's most significant unserved illustration niche.

**Pilot success criteria:**
1. ≥75 records ingested with rights_decision=ALLOWED
2. Zero IFC-1 violations (no non-CC0 records written)
3. M36 write order preserved for 100% of records
4. IIIF manifest extraction confirmed functional (manifest UUID from record)
5. ActivityStreams harvest loop stable across ≥2 full feed traversals
6. Van Huysum Asset Zero record at MASTERWORK quality tier

---

## VIII. DECISION ARTICLES

**Article 1 — Production Authorization**  
The J. Paul Getty Museum is APPROVED as a production source candidate under NC's commercial-use requirements. The Open Content Program satisfies IFC-1: CC0 license, no fees, no ToS commercial restriction, no attribution obligation. No disqualifying condition equivalent to DD-GALLICA-003 (license fee) or DD-PARISMUSEES-001 (private API) exists.

**Article 2 — Institution Number**  
The Getty Museum is assigned Institution #16 in the NC institution registry.

**Article 3 — Source Slug**  
Source slug: `getty`. Single-institution adapter (no dual-institution routing required). No `member_of` disambiguation needed.

**Article 4 — Rights Class Assignment**  
Getty is classified under Rights Class 7 (Linked Art `subject_to` URI form), variant B (nested traversal path). This variant requires a Getty-specific rights extraction function. SA-18 (Getty Rights Matrix v1) governs this classification and must be ratified before Sprint 1.

**Article 5 — IFC-1 Hard Gate**  
The Getty adapter MUST enforce per-record CC0 verification. Institution-wide Open Content Program membership does not substitute for per-record `subject_to` URI confirmation. Any record without a confirmed CC0 URI in `subject_to` MUST be blocked. This gate is unconditionally permanent per IFC-1.

**Article 6 — Ingestion Protocol**  
Primary harvest path is ActivityStreams change feed + Linked Art REST API. SA-19 (ActivityStreams Harvest Protocol) must be ratified before Sprint 1 and must specify feed traversal, Delete event handling, and incremental harvest mode.

**Article 7 — IIIF Manifest Extraction**  
The Getty adapter MUST extract the IIIF manifest URI from the Linked Art record (via `subject_of` or `representation` predicate — confirm Sprint 1). The adapter MUST NOT attempt to construct or derive the manifest UUID from the object UUID. A record with no resolvable manifest link MUST be stored with `yale_iiif_manifest: null` and flagged for review rather than rejected.

**Article 8 — SA-9 Extension**  
SA-9 (`build_rights_evidence` source slug remap) MUST be extended to include `"getty"` before Sprint 3. Current required slugs: met, aic, cma, smk, nga, walters, ycba, yuag, **getty** (9 slugs). SA-9 is now overdue across four institutions.

**Article 9 — Asset Zero**  
Jan van Huysum "Vase of Flowers" (1722, accession 82.PB.70) is designated Asset Zero for the Getty Museum pilot. The Van Gogh "Irises" (1889, accession 90.PA.20, Linked Art UUID `c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb`) is designated SECONDARY Asset Zero for brand signaling purposes only.

**Article 10 — Getty Research Institute Deferral**  
The Getty Research Institute (GRI, ~78,000 open content images) is deferred to a separate audit (DD-GRI-001). GRI images use the same data.getty.edu Linked Art API but may have different field paths, subject matter (prints, maps, historical photographs), and institutional provenance requirements. GRI SHALL NOT be merged into the Getty Museum adapter without a separate governance decision.

**Article 11 — Sprint 1 Confirmation Requirements**  
Before Sprint 1 adapter implementation begins, the following must be confirmed via direct API inspection:
1. Authentication: confirm no API key or OAuth required
2. Rate limits: confirm published limits or absence thereof
3. `subject_to` field path: confirm exact nested traversal in live records
4. Manifest reference field: confirm whether `subject_of` or `representation` carries the IIIF manifest URI
5. User-Agent policy: confirm required or recommended User-Agent header

**Article 12 — FM-4 Invariant**  
FM-4 applies without exception: the Getty adapter worker MUST write `"pending_verification"` (not `"verified_cc0"`) to `media_rights.rights_status`. Reclassification to `"classified_cc0"` occurs in `build_rights_evidence` via the shared store, not in the adapter worker.

---

## IX. RISK REGISTER

| ID | Risk | Severity | Probability | Mitigation |
|---|---|---|---|---|
| R-1 | Sprint 1 discovers API key required | Medium | Low | Add auth layer; no rights impact |
| R-2 | `subject_to` traversal path differs from preliminary research | Medium | Medium | Sprint 1 confirmation required (Article 11) before any Sprint 2 work |
| R-3 | Rate limiting causes harvest timeout | Low | Medium | Implement exponential backoff in ActivityStreams client |
| R-4 | Manifest UUID cannot be extracted from record (field absent) | Medium | Low | Article 7 directs storage of null manifest with review flag; does not block record |
| R-5 | Open Content Program coverage for Dutch Golden Age is sparser than expected | Low | Low | Pilot scope can shift to alternative geographic anchor (France, Mediterranean) |
| R-6 | GRI images intermixed with Museum images in activity feed | Medium | Medium | Source slug `getty` scoped to Museum collection path only; GRI deferral per Article 10 |
| R-7 | ActivityStreams `Delete` events reference previously ingested records | Medium | Medium | SA-19 must specify tombstone behavior before Sprint 1 |
| R-8 | SA-9 overdue across NGA, Walters, Yale; Getty addition compounds risk | High | High | SA-9 MUST be ratified before any of NGA/Walters/Yale/Getty reach Sprint 3 |
| R-9 | Van Huysum Asset Zero Linked Art UUID not yet confirmed | Low | Low | Confirm UUID in Sprint 1 via API lookup on accession 82.PB.70 |

---

## X. STANDARDS AMENDMENTS REQUIRED

| SA | Title | Blocks | Status |
|---|---|---|---|
| SA-9 | `build_rights_evidence` source slug remap (add `getty`) | Getty Sprint 3 | OVERDUE — also blocks NGA, Walters, Yale Sprint 3 |
| SA-18 | Getty Rights Matrix v1 | Getty Sprint 1 | REQUIRED |
| SA-19 | ActivityStreams Harvest Protocol | Getty Sprint 1 | REQUIRED |

Note: SA-16 (Linked Art Adapter Profile, drafted for Yale) may require an amendment to document the Getty nested traversal variant. SA-18 may reference SA-16 as its parent protocol profile.

---

## XI. RATIFICATION TABLE

| Role | Approval | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

**Conditions for ratification:**
1. SA-18 scope confirmed (field path verification deferred to Sprint 1 per Article 11)
2. SA-19 scope statement accepted
3. Institution #16 assignment recorded in NC institution registry
4. Asset Zero designation (Van Huysum 82.PB.70) accepted

---

*DD-GETTY-001 drafted 2026-06-10 under authority of Institution Factory Constitution v1.*  
*Prior precedent: DD-NGA-001 (CSV protocol), DD-YALE-001 (Linked Art JSON-LD), DD-GALLICA-003 (disqualification model).*
