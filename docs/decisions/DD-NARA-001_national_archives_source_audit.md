# DD-NARA-001: National Archives and Records Administration — Source Audit and Activation Decision

**Type:** Decision Document — Institution Source Audit  
**Status:** DRAFT — Pending Ratification  
**Authority:** Institution Factory Constitution v1 (IFC-1–IFC-12), 17 U.S.C. § 105, 36 CFR § 1254.62  
**Institution Number:** #18  
**Date Drafted:** 2026-06-10  
**Drafted By:** NC Principal Architect  

---

## DECISION

**APPROVED**

The National Archives and Records Administration (NARA) is APPROVED as a production source for the NC commercial illustration pipeline. US federal government works are in the public domain by operation of law (17 U.S.C. § 105). NARA holds no equivalent ToS commercial restriction to the BnF/Gallica disqualifier (DD-GALLICA-003). The Catalog API is documented, public, and API-key-authenticated. NARA fills NC's Historic Maps Tier 1 (unlocked by CI v1.2) and US federal expedition cartographic content. Standard conditions apply.

---

## I. INSTITUTION PROFILE

**Institution:** National Archives and Records Administration  
**Catalog URL:** https://catalog.archives.gov/  
**Developer portal:** https://www.archives.gov/developer  
**Data portal:** https://www.archives.gov/data  
**Type:** Independent US federal agency; national repository for permanently valuable federal records  
**Scale:** 500M+ digitized pages; 148M+ digital objects with URLs in bulk dataset; 41M photographs; 10M maps, charts, and architectural drawings  
**Geographic scope:** United States federal records from 1774 to present; global scope for expedition and military cartography  

NARA is the US federal government's official archives. Its Catalog (catalog.archives.gov) provides API access to archival descriptions and digital objects across all record groups. NARA holds the original administrative records of major US scientific expeditions — Lewis and Clark, the Pacific Railroad Surveys (1853–1860), the Wilkes Expedition (1838–1842), and the post-Civil War Western surveys (Hayden, King, Wheeler, Powell). NARA also holds 10M+ maps and charts from the USGS, War Department, Hydrographic Office, Bureau of Land Management, and Forest Service.

NARA's digitized catalog is also available as a biannual bulk snapshot on AWS S3 (`s3://nara-national-archives-catalog/`, no auth required), providing an alternative high-volume harvest path independent of the API rate limit.

---

## II. RIGHTS AND COMMERCIAL USE AUDIT (IFC-1 GATE)

### II.1 Legal Basis for Public Domain Status

**Statute:** 17 U.S.C. § 105 — "Copyright protection under this title is not available for any work of the United States Government."

**Regulation:** 36 CFR § 1254.62 — "Many of our holdings are in the public domain as products of employees or agents of the Federal Government."

**NARA policy:** "Works of the U.S. Government that have been produced by the National Archives and Records Administration are in the public domain and may be copied and distributed without permission."

This is a statutory basis, not an institutional licensing policy. It is categorically stronger than CC0 (which requires a legal act by the rights holder) — there is no copyright to license because none attaches. Unlike Gallica (DD-GALLICA-003), where BnF asserted a ToS commercial fee unrelated to copyright, NARA has no equivalent ToS commercial restriction on federally produced records.

### II.2 IFC-1 Gate Analysis

**For records with `useRestriction.status == "Unrestricted"`:** IFC-1 PASSED. These records are US government works in the public domain. No copyright, no license fee, no ToS commercial restriction.

**For records with any other `useRestriction.status`:** These records carry third-party copyright (donated materials, materials obtained from private commercial sources, Presidential records) or have unresolved status. NARA explicitly places responsibility on users. The NARA adapter MUST block any record not carrying `Unrestricted` status.

**36 CFR § 1254.62 exceptions confirmed:**
- Federal agency records obtained from private commercial sources may carry publication restrictions
- Donated historical materials may carry copyright
- Presidential records may contain copyrighted third-party materials

The NC NARA adapter MUST treat `Unrestricted` as the sole allowed value. All other statuses MUST be blocked at the adapter level. This is a hard gate equivalent to IFC-1 — no non-`Unrestricted` record may be written.

### II.3 Commercial Use

**Permitted:** Yes, unrestricted for `Unrestricted` records. NARA states: "no written permission is required to use them" (vast majority of catalog images). No license fee for digital reproductions of PD government works. NARA does not assert reproduction copyright over digital scans — consistent with US law and *Bridgeman Art Library v. Corel Corp* (SDNY 1999).

**Attribution:** Not legally required. NARA's preferred credit format: "National Archives photo no. [photo_number]" or equivalent. NC will include NARA attribution in rights evidence; not mandatory.

**ToS commercial restriction:** None confirmed. Unlike BnF (DD-GALLICA-003), NARA does not charge a license fee for commercial use of government records. NARA explicitly states it "does not license content or grant exclusive publication privileges."

### II.4 Rights Model Classification

**Rights class:** Per-record enum string — `useRestriction.status == "Unrestricted"` — **Rights Class 9 (new)**.

This is structurally related to Rights Class 3 (CMA string-equality), but is semantically distinct: CMA's `share_license_status: "Open Access"` denotes an applied license; NARA's `useRestriction.status: "Unrestricted"` denotes absence of restriction under federal law. The source of truth differs (institutional license vs. federal statute), the vocabulary differs (multi-value authority list), and the governing standard (17 U.S.C. § 105) is unique. Rights Class 9 is formally new.

**NARA Use Restriction Status authority list:**

| Value | NC Decision | Basis |
|---|---|---|
| `Unrestricted` | ALLOWED | US government work, 17 U.S.C. § 105 |
| `Restricted - Fully` | BLOCKED | Third-party copyright or donor restriction |
| `Restricted - Partly` | BLOCKED | Partial restrictions require review |
| `Restricted - Possibly Copyright` | BLOCKED | Unresolved restriction |
| `Undetermined` | BLOCKED | Status unknown |
| Any other value | BLOCKED | `unknown_restriction_status` |

`rights_policy_id`: `"nara_rights_matrix_v1"`  
Source slug: `"nara"` (single institution)

---

## III. CONNECTIVITY AND API AUDIT

### III.1 NARA Catalog API v2

**Base URL:** `https://catalog.archives.gov/api/v2`  
**Search endpoint:** `GET /records/search`  
**OpenAPI:** `https://catalog.archives.gov/api/v2/api-docs/`  
**Documentation:** https://www.archives.gov/research/catalog/help/api  
**GitHub:** https://github.com/usnationalarchives/Catalog-API  

**Authentication:** API key required. Passed as HTTP header: `x-api-key: {NARA_API_KEY}`. Key stored in environment variable `NARA_API_KEY` only — never hardcoded.

**Pagination:** Offset-based. Parameters: `limit` (results per page) and `page` (page number). Deep pagination via `searchAfter` (sort token from last hit). Total count available at `body.hits.total.value`.

**Response format:** JSON. Elasticsearch-style envelope: `body.hits.total.value` (total), `body.hits.hits[]` (records). Record payload at `_source.record`.

**Primary identifier:** `naId` (National Archives Identifier) — numeric integer. Web URL: `https://catalog.archives.gov/id/{naId}`.

**Rights fields:**
- `useRestriction.status` — use/copyright restriction status (NC gate field)
- `accessRestriction.status` — physical/digital access level (secondary gate)

**Image delivery fields:** `digitalObjects[]` array → `objectUrl` (direct JPEG/file URL), `objectType`, `objectId`, `objectFileSize`, `objectFilename`. No IIIF in production.

**Rate limits:**

| Tier | Queries/month | Notes |
|---|---|---|
| Default (API key) | 10,000 | ~333/day — insufficient for production harvest |
| Standard higher tier | 150,000 | Request via Catalog_API@nara.gov — required before Sprint 2 |
| Partner tier | 1,500,000 | For formal NARA partners |

**Bulk download:** AWS S3 biannual snapshot at `s3://nara-national-archives-catalog/` (no auth). Biannual JSON export covering all archival descriptions and digital object URLs. This is the recommended production-scale harvest path.

Stage 3: **CLEARED WITH CONDITIONS** — rate limit tier upgrade request and AWS S3 bulk path evaluation required before Sprint 2.

### III.2 IIIF Status

**IIIF in production: NOT AVAILABLE.**

NARA uses IIIF technology internally for the catalog image viewer but has no public IIIF API production endpoints. A GitHub prototype (`github.com/usnationalarchives/nara-iiif`) exists but is explicitly experimental (Heroku prototype, not production). NARA is not a IIIF Consortium member.

**Image delivery for NC:** Direct URL from `digitalObjects[].objectUrl`. Pattern: `https://catalog.archives.gov/OpaAPI/media/{naId}/content/{path}` or `https://catalog.archives.gov/medialive/{path}`. This mirrors Walters' direct JPEG delivery (DD-WALTERS-001, Rights Class 6) but sourced from API response rather than CSV. SA-23 governs this delivery class.

---

## IV. CONTENT TYPE ASSESSMENT

NARA passes the NC content type gate. Primary NC-relevant collections:

### IV.1 Historic Maps Tier 1 (CI v1.2 Unlocked)

CI v1.2 (ratified 2026-06-06) enables `signal_substitutions` for geographic assets, unlocking Historic Maps Tier 1. NARA is the primary US federal source for this tier.

| Collection | Volume | Period |
|---|---|---|
| USGS topographic and geological maps | Millions | 1879–present |
| War Department expedition maps | Thousands | 1800s |
| Hydrographic Office coastal charts | Thousands | 1840s–present |
| Bureau of Land Management survey plats | 15M+ acres documented | 1785–present |
| Forest Service maps | Thousands | 1881–present |
| Indian Affairs maps | 16,000+ | 1800–1939 |

### IV.2 Scientific Expedition Records

| Expedition | NARA Record Group | NC-Relevant Content |
|---|---|---|
| Lewis and Clark (1804–1806) | RG 77, RG 37 | Maps, correspondence, natural history notes |
| Wilkes Expedition (1838–1842) | RG 78 | Hydrographic/cartographic records |
| Pacific Railroad Surveys (1853–1860) | War Department records | Administrative and cartographic records |
| Hayden/King/Wheeler/Powell Western Surveys | RG 57, RG 77 | USGS geological and topographic illustration manuscripts |

**Note:** The published natural history illustration *volumes* from expeditions (Pacific Railroad Survey zoology/botany plates, Wilkes Expedition plates) are held at BHL, Smithsonian, and libraries — not NARA. NARA holds the *administrative and cartographic* records. NC's primary NARA value is maps and scientific photographs, not narrative illustration plates.

### IV.3 Still Picture Branch (RG 306 and others)

14M analog + 3M digital photographs including scientific expedition photography, government survey images, and federal agency documentary photography pre-1900.

---

## V. ASSET ZERO

**Recommended:** Pre-1900 USGS topographic map of Yellowstone National Park or Grand Canyon  
**Record Group:** RG 57 (U.S. Geological Survey), established 1879  
**Rights:** Unrestricted (US government work, 17 U.S.C. § 105)  
**Delivery:** `objectUrl` from `digitalObjects[]`  

Rationale: A pre-1900 USGS survey map provides NC Historic Maps Tier 1 alignment (CI v1.2 mandate), US federal public domain with no ambiguity, place anchor for NC's geographic product tier, and a proven illustration commerce category (vintage USGS maps). Specific `naId` to be confirmed in Sprint 1 via API search: `q=yellowstone&availableOnline=true&objectType=Image (JPG)`.

**Alternative Asset Zero:** William Henry Jackson or Timothy O'Sullivan western survey photographs (Wheeler/Hayden surveys, 1870s) from NARA Still Picture Branch — pre-1900, unrestricted, direct US federal photography.

---

## VI. PILOT SCOPE

**Pilot:** American West / 19th Century Federal Cartography  
**Target asset count:** 75  
**Duration:** 90 days  
**Rights gate:** `useRestriction.status == "Unrestricted"` only  
**Primary anchor place:** American West (Yellowstone, Yosemite, Rocky Mountains, Grand Canyon)  
**Content types:** Maps and Charts (primary); Photographs and Other Graphic Materials (secondary)  

The American West federal survey anchor activates NC's Historic Maps Tier 1 (CI v1.2) with content no current NC institution holds. This pilot fills the US geographic content gap while delivering the highest-commercial-value map tier.

---

## VII. DECISION ARTICLES

**Article 1 — Production Authorization**  
NARA is APPROVED as a production source. US government records with `useRestriction.status: "Unrestricted"` are in the public domain by operation of 17 U.S.C. § 105. No license fee, no ToS commercial restriction, no attribution obligation.

**Article 2 — Institution Number**  
NARA is assigned Institution #18 in the NC institution registry.

**Article 3 — Source Slug**  
Source slug: `nara`. Single institution, no dual-institution routing.

**Article 4 — Rights Class Assignment**  
NARA is classified under Rights Class 9 (new): per-record enum string `useRestriction.status == "Unrestricted"`. SA-22 (NARA Rights Matrix v1) governs this classification.

**Article 5 — IFC-1 Hard Gate**  
The NARA adapter MUST block any record where `useRestriction.status` is not exactly `"Unrestricted"`. All non-allowed statuses MUST produce zero writes. Unconditionally permanent per IFC-1.

**Article 6 — Access Restriction Secondary Gate**  
Records with `accessRestriction.status` set to any restricted value MUST also be blocked, even if `useRestriction.status` is `Unrestricted`. Both gates must pass before ingestion proceeds.

**Article 7 — No IIIF Condition**  
NARA does not provide production IIIF endpoints. Image delivery is via `digitalObjects[].objectUrl` (direct URL). Records with no `digitalObjects` array or no valid `objectUrl` MUST be blocked with `reason: "missing_image_evidence"`. SA-23 governs this delivery model.

**Article 8 — API Rate Limit Condition**  
NC MUST submit a rate limit tier upgrade request to Catalog_API@nara.gov before Sprint 2 implementation. The AWS S3 bulk snapshot (`s3://nara-national-archives-catalog/`) MUST be evaluated as the primary harvest path for initial full-catalog ingestion.

**Article 9 — FM-4 Invariant**  
FM-4 applies without exception. The NARA adapter worker MUST write `"pending_verification"` to `media_rights.rights_status`, never `"verified_pd"`. Reclassification to `"classified_pd"` (or `"classified_cc0"`) happens in shared store `build_rights_evidence` via slug remap.

**Article 10 — SA-9 Extension**  
SA-9 (`build_rights_evidence` source slug remap) MUST be extended to include `"nara"` before Sprint 3. Required slugs: met, aic, cma, smk, nga, walters, ycba, yuag, getty, nhm, **nara** (11 slugs). SA-9 is critically overdue.

**Article 11 — API Key Environment Variable**  
The NARA API key MUST be read from the environment variable `NARA_API_KEY` via `os.getenv()` or Pydantic Settings. It MUST NOT be hardcoded in any source file, fixture, or test. Tests MUST use a mock HTTP transport; they MUST NOT make live API calls.

**Article 12 — Sprint 1 Scope**  
Sprint 1 is limited to: API key loading, search endpoint, record lookup by `naId`, `useRestriction` + `accessRestriction` extraction, `digitalObjects` still-image extraction, and `searchAfter` deep pagination support. No M36 writes in Sprint 1.

---

## VIII. ARCHITECTURAL COMPARISON

| Dimension | NARA | Walters (Rights Class 6) | CMA (Rights Class 3) |
|---|---|---|---|
| Rights class | 9 (new — enum string) | 6 (institution-wide CC0) | 3 (string-equality) |
| Rights field | `useRestriction.status` | None (institution-wide) | `share_license_status` |
| Allowed value | `"Unrestricted"` | Implicit (all records) | `"Open Access"` |
| Legal basis | 17 U.S.C. § 105 | CC0 grant | CC0 grant |
| Ingestion protocol | REST API v2 + optional AWS S3 | CSV bulk download | REST API (offset cursor) |
| IIIF | No (direct objectUrl) | No (direct JPEG) | No (direct URL from API) |
| Auth required | Yes (API key, header) | No | No |
| Rate limits | 10K/month default | N/A (CSV) | None confirmed |
| Bulk path | AWS S3 (biannual) | GitHub CSV | N/A |

---

## IX. RISK REGISTER

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R-1 | Rate limit (10K/mo) blocks Sprint 2 API work | High | Request tier upgrade; use AWS S3 for bulk harvest |
| R-2 | AWS S3 JSON schema differs from API v2 schema | Medium | SA-23 must specify both paths; Sprint 1 confirms `_source.record` structure |
| R-3 | `objectUrl` pattern varies across media types | Low | Filter by `objectType` in `IMAGE_OBJECT_TYPES` at extraction time |
| R-4 | Third-party copyright records intermixed with `Unrestricted` | Low | 36 CFR § 1254.62 warning documented; IFC-1 gate at adapter level is sufficient |
| R-5 | SA-9 overdue — blocks Sprint 3 across NHM + NARA + 5 other institutions | High | SA-9 must be drafted immediately after SA-22 + SA-23 ratification |
| R-6 | Pacific Railroad Survey illustration plates not in NARA | None | Documented in Section IV.2; pilot scoped to maps and photos only |

---

## X. STANDARDS AMENDMENTS REQUIRED

| SA | Title | Blocks | Status |
|---|---|---|---|
| SA-9 | `build_rights_evidence` source slug remap (add `nara`) | NARA Sprint 3 | OVERDUE |
| SA-22 | NARA Rights Matrix v1 (`useRestriction.status` enum gate) | NARA Sprint 2 | REQUIRED |
| SA-23 | NARA Direct Image Delivery Protocol (`digitalObjects[].objectUrl` + S3 path) | NARA Sprint 2 | REQUIRED |

---

## XI. SPRINT 1 ACCEPTANCE CRITERIA

Sprint 1 files authorized:

```
workers/nara_adapter/__init__.py
workers/nara_adapter/config.py
workers/nara_adapter/client.py
tests/unit/test_nara_client.py
tests/replay/test_nara_adapter_sprint1.py
tests/fixtures/nara/
```

Acceptance criteria:

1. API key read only from `NARA_API_KEY` environment variable
2. Requests send `x-api-key` header; key never appears in source code or fixtures
3. Search URL and request parameters deterministic (canonical sort)
4. `naId` lookup uses records search endpoint with `naId_is` parameter
5. Still-image digital object extraction filters by `objectType`
6. `useRestriction.status` and `accessRestriction.status` extracted correctly
7. `searchAfter` deep pagination token preserved from `sort[]` values
8. Replay tests run without network access via mock transport
9. No store writes exist anywhere in the NARA adapter Sprint 1

---

## XII. RATIFICATION TABLE

| Role | Approval | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

**Conditions for ratification:**
1. SA-22 scope accepted (NARA Rights Matrix v1 enum gate defined)
2. SA-23 scope accepted (direct objectUrl delivery protocol + S3 path scoped)
3. Institution #18 recorded in NC institution registry
4. Rate limit tier upgrade request noted as pre-Sprint-2 action item
5. Asset Zero designation accepted (pre-1900 USGS map, American West, confirmed Sprint 1)

---

*DD-NARA-001 drafted 2026-06-10 under authority of Institution Factory Constitution v1.*  
*Legal basis: 17 U.S.C. § 105 (federal works PD); 36 CFR § 1254.62 (NARA policy).*  
*Precedents: DD-GALLICA-003 (no equivalent ToS restriction), DD-WALTERS-001 (direct image URL delivery pattern), DD-CMA-001 (string-equality rights class).*
