# SA-NOAA-002: NOAA Image Delivery Protocol v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | DRAFT — Pending Ratification |
| SA Number | SA-NOAA-002 |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-11 |
| Authority | DD-NOAA-001 · SA-NOAA-001 · NOAA Governance Review v1 · Institution Factory Constitution v1 |
| Delivery Protocol | Path A: Flickr API (Sprint 1 pilot) · Path B: NOAA Photo Library (Sprint 1 evaluation) |
| IIIF Status | Not available — neither path provides IIIF |
| Blocks | NOAA Sprint 1 (required before adapter implementation) |

---

## Governing Principle

This amendment specifies how the NOAA adapter extracts image URLs and constructs the `media_file` records for assets that have passed the SA-NOAA-001 rights gate. It covers two delivery paths:

- **Path A — Flickr API** (active for Sprint 1 pilot): Programmatic image URL extraction from the Flickr API JSON response.
- **Path B — NOAA Photo Library** (Sprint 1 evaluation target; production candidate): Direct file URL extraction from Photo Library metadata, if a programmatic access path is confirmed in Sprint 1.

This amendment also governs the third-party platform dependency introduced by Path A (Flickr) — the first such dependency in the NC adapter portfolio. The Platform Dependency Statement in Part IV is a constitutional-level acknowledgment required by the NOAA Governance Review v1.

**No IIIF:** Neither Flickr nor the NOAA Photo Library provides IIIF Image API or Presentation API endpoints. NOAA is not a IIIF Consortium member. All image delivery is via direct JPEG/PNG URLs.

---

## Part I — Path A: Flickr API Delivery (Sprint 1 Pilot)

### I.1 Sprint 1 Scope Limitation

**CRITICAL: Path A is authorized for Sprint 1 only.** The Flickr API is the confirmed programmatic access path for the 50-asset, 90-day pilot specified in DD-NOAA-001. Path A does not constitute production authorization for a full catalog harvest.

Sprint 2 and beyond require one of two gates to be met before further Flickr ingestion:
- **Gate 2A:** Photo Library direct path confirmed viable (Sprint 1 evaluation deliverable) → Photo Library becomes the production standard (Path B). Flickr demoted to fallback.
- **Gate 2B:** Photo Library confirmed non-viable AND a Platform Dependency Governance Review formally authorizes Flickr as the production path (Section IV.4).

No Sprint 2 Flickr harvest may begin until Gate 2A or Gate 2B is met. The adapter codebase must include a `SPRINT_1_ONLY` flag or equivalent mechanism to prevent inadvertent Sprint 2 Flickr harvest before the gate decision.

### I.2 Flickr API Endpoint

**Base URL:** `https://api.flickr.com/services/rest/`  
**Method:** `flickr.people.getPhotos`  
**Authentication:** Flickr API key required. Key passed as parameter `api_key`. Key stored in environment variable `FLICKR_API_KEY` only — never hardcoded. No OAuth required for read-only access to public photos.  
**Format:** JSON (`format=json&nojsoncallback=1`)

### I.3 Required API Parameters

```
method=flickr.people.getPhotos
user_id=<NOAA account NSID>
extras=url_o,url_l,url_c,url_z,license,description,title,tags,owner_name,date_taken
license=7,8,9,10
per_page=100
page=<page number>
format=json
nojsoncallback=1
api_key=<FLICKR_API_KEY>
```

**`extras` field explanation:**
- `url_o`: Original image URL (full resolution) — preferred
- `url_l`: Large image URL (~1024px on longest side) — first fallback
- `url_c`: Medium 800px URL — second fallback
- `url_z`: Medium 640px URL — third fallback
- `license`: License integer (required for SA-NOAA-001 primary gate)
- `description`: Description text (required for secondary validation in SA-NOAA-001 Part III)
- `title`: Title text (secondary validation)
- `tags`: Tags (subject-matter scope filtering)
- `owner_name`: Account name confirmation
- `date_taken`: Timestamp for provenance evidence

**`license` pre-filter:** The `license=7,8,9,10` parameter pre-filters API results to PD-asserted images. This is a performance optimization, not a rights gate. The SA-NOAA-001 gate still applies to all returned records regardless of this filter.

### I.4 Pagination

Flickr pagination is page-number based:
- `page` parameter: 1-indexed page number
- `per_page`: up to 500 per request (use 100 for Sprint 1)
- Total count: `photos.total` in response
- Total pages: `photos.pages` in response

**Termination condition:** Stop when `page > photos.pages` OR when no records pass SA-NOAA-001 gate in a full page (empty harvest signal).

### I.5 Account NSID Resolution

NOAA Flickr accounts must be resolved to Flickr NSIDs (numeric user IDs) before ingestion. Sprint 1 must confirm:

| Account | Username | NSID (Sprint 1 to confirm) |
|---|---|---|
| Primary | @usoceangov | TBD Sprint 1 |
| Fisheries | @noaafisheries | TBD Sprint 1 |

If additional NOAA division accounts exist and are confirmed federal, they must be added to this table before ingestion. NSIDs are stable identifiers; usernames can change.

### I.6 Image URL Hierarchy

The adapter MUST attempt image URL extraction in the following priority order:

| Priority | Field | Resolution | Use Condition |
|---|---|---|---|
| 1 | `url_o` | Original (full resolution) | Preferred; use if present and accessible |
| 2 | `url_l` | Large (~1024px) | If `url_o` absent or access-restricted |
| 3 | `url_c` | Medium 800px | If `url_l` absent |
| 4 | `url_z` | Medium 640px | If `url_c` absent |
| — | None available | — | BLOCK with `reason: "missing_image_evidence"` |

**`url_o` availability note:** Flickr restricts original-size URL delivery to accounts where the uploader has enabled original-size sharing. For NOAA government accounts, original sharing is expected to be enabled, but Sprint 1 must confirm `url_o` field presence in the API response. If `url_o` is absent from NOAA account photos, `url_l` becomes the effective primary.

**Minimum acceptable resolution:** Records with no URL at `url_c` or higher (≥640px) MUST be blocked with `reason: "insufficient_resolution"`. Sub-640px images are not acceptable for NC product generation.

### I.7 Photo Record Identifier

**Primary identifier:** Flickr `photo.id` (string integer, e.g., `"12345678901"`)  
**Canonical URL:** `https://www.flickr.com/photos/<owner-nsid>/<photo-id>/`  
**Stored as:** `source_record.external_id` = `"flickr:<photo-id>"`

### I.8 Subject-Matter Scope Filter

DD-NOAA-001 Article 9 restricts the NOAA adapter to natural history content. The adapter MUST apply a subject-matter filter before writing records. For Sprint 1, scope restriction is implemented via:

**Allowed tag patterns (any of the following must be present):**
- Tags: `coral`, `reef`, `fish`, `marine`, `ocean`, `sea`, `coastal`, `fisheries`, `mammal`, `whale`, `dolphin`, `turtle`, `seabird`, `shark`, `salmon`, `tuna`, `manatee`, `sealion`, `walrus`, `seal`, `polarbear`
- Tag containing any species common name in NOAA's documented taxa
- Collection/album name indicating marine life, fisheries, or natural history subject

**Excluded collection/album names (BLOCK with `reason: "out_of_scope_subject"`):**
- "Weather", "Forecast", "Hurricane", "Satellite Imagery", "NWS", "Climate Data", "Ships and Facilities", "Personnel"

Sprint 1 must expand and refine this list based on actual Flickr collection/album naming observed in @usoceangov and @noaafisheries.

---

## Part II — Path B: NOAA Photo Library (Sprint 1 Evaluation)

### II.1 Evaluation Status

Path B is not active for Sprint 1 ingestion. Sprint 1 must complete an evaluation of the NOAA Photo Library (photolib.noaa.gov) to determine whether a programmatic access path exists.

**Sprint 1 evaluation deliverable (due before Sprint 1 close):**

A documented finding covering:

1. **Hidden API endpoint:** Inspect browser network requests during Photo Library gallery browsing. Document any XHR/fetch calls to API endpoints (JSON responses). If an undocumented API is found, document: base URL, endpoint structure, response schema, rights field name, image URL fields, pagination mechanism.

2. **RSS/OAI-PMH/Sitemap:** Check for `/rss`, `/oai`, `/sitemap.xml` feeds at photolib.noaa.gov. Document if present.

3. **Bulk download package:** Investigate whether NOAA provides a bulk metadata export of the Photo Library via institutional request, data.gov, or direct download. Document if available.

4. **Static index files:** Check for CSV, JSON, or XML index files linked from the Photo Library developer or data pages.

**Evaluation outcome:**

| Outcome | Path B Status | Sprint 2 Action |
|---|---|---|
| API/bulk path confirmed | CLEARED | Path B becomes production standard; Path A demoted to fallback |
| No programmatic path found | BLOCKED | Platform Dependency Governance Review required before Sprint 2 Flickr harvest |
| Partial path (scraping only) | CONDITIONAL | DD-NOAA-002 defines scraping architecture if appropriate |

### II.2 Path B Delivery Specification (Pending Confirmation)

The following specification is provisional. It will be finalized in SA-NOAA-002 v1.1 based on the Sprint 1 evaluation finding.

**Expected delivery mechanism:** Direct JPEG/PNG file URL embedded in Photo Library metadata response.  
**Expected URL pattern:** `https://photolib.noaa.gov/[collection]/[media-id].[ext]` (pattern TBD Sprint 1)  
**Expected rights field:** `credit` (text string — see SA-NOAA-001 Part II)  
**Identifier:** Photo Library media ID (format TBD Sprint 1)

---

## Part III — Cross-Path Rules

These rules apply to all records regardless of which delivery path produced them.

### III.1 No IIIF

NOAA provides no IIIF endpoints. The NOAA adapter MUST NOT attempt IIIF manifest construction or IIIF Image API tile requests. Direct URL delivery is the sole image delivery mechanism. Any code path that checks for or uses IIIF for NOAA records is a bug.

### III.2 Missing Image Evidence

Any record that passes SA-NOAA-001 rights gate but has no valid image URL MUST be blocked with `reason: "missing_image_evidence"`. No `media_file` record may be created without a valid image URL. This applies to both paths.

### III.3 FM-4 Invariant

FM-4 applies without exception. The NOAA adapter worker MUST write `"pending_verification"` to `media_rights.rights_status`, never `"verified_pd"` or `"classified_pd"`. Reclassification occurs in `build_rights_evidence` via the SA-9 slug remap.

### III.4 M36 Write Order

M36 write order (canonical store write sequencing) MUST be preserved for all NOAA records. No writes to `media_rights` or `media_file` may precede the `source_record` write. No Sprint 1 code may include store writes — Sprint 1 is client-and-extraction only.

### III.5 Attribution Field

Every NOAA `source_record` MUST include:

```json
{
  "institution_credit": "NOAA",
  "credit_line": <exact credit string from source>,
  "attribution_format": "Image: NOAA | Credit: NOAA/[Division]",
  "attribution_required": false,
  "attribution_requested": true
}
```

Attribution is not legally required for § 105 works, but NOAA requests it. NC records the request and includes it in output metadata. The `attribution_required: false` field signals that products may omit attribution without rights violation, though including it is preferred.

---

## Part IV — Platform Dependency Statement

**Required by NOAA Governance Review v1, Condition 4.**

This statement is a formal governance record of the architectural decision to use a third-party platform (Flickr/SmugMug) as the Sprint 1 access path. No comparable dependency exists in the current NC adapter portfolio.

### IV.1 Platform Classification

| Field | Value |
|---|---|
| Platform | Flickr |
| Platform Operator | SmugMug Inc. |
| Platform Type | `third_party_social_media` |
| Platform Ownership | Private company (acquired from Verizon Media by SmugMug, 2018) |
| NOAA Account Type | Official federal government account |
| API Stability | Documented since 2004; has had breaking changes historically |
| Images Hosted | 25,000+ from @usoceangov; additional from @noaafisheries |
| Relationship to NOAA's Canonical Archive | Subset — Flickr is a distribution channel, not NOAA's primary archive |

### IV.2 Known Platform Risks

| Risk | Severity | Probability | NC Impact |
|---|---|---|---|
| API terms change materially (rate limits, access restrictions) | HIGH | MEDIUM | NOAA ingestion halts pending mitigation |
| SmugMug/Flickr acquired again or restructured | HIGH | LOW | NOAA ingestion continuity at risk |
| NOAA account suspended or removed | MEDIUM | VERY LOW | Full NOAA ingestion halt until alternative path found |
| License tag self-reporting error (mislabeled image) | LOW | VERY LOW | SA-NOAA-001 secondary validation provides backstop |
| `url_o` access restricted (downgrade to `url_l`) | MEDIUM | LOW | Resolution quality reduced; acceptable short-term |
| Flickr content completeness gap (not all Photo Library images on Flickr) | CERTAIN | — | Production scope permanently limited to Flickr subset |

### IV.3 Sprint 1 Authorization

The Flickr path is authorized for Sprint 1 only:
- Asset target: 50 (per DD-NOAA-001 pilot specification)
- Duration: 90 days
- Purpose: path confirmation + pilot content harvest

Sprint 1 Flickr authorization expires at Sprint 1 close. No Sprint 2 Flickr harvest proceeds without Gate 2A or Gate 2B (Section I.1).

### IV.4 Sprint 2 Path-Promotion Decision Gate

At Sprint 1 close, the path-promotion decision must be recorded as a sprint closeout finding:

**Option A — Path B (Photo Library) confirmed viable:**
- Sprint 2 implements Photo Library direct adapter (SA-NOAA-002 v1.1 updates Path B specification)
- Flickr path demoted to fallback (used only if Photo Library path fails)
- No additional governance review required

**Option B — Path B (Photo Library) confirmed non-viable:**
- A Platform Dependency Governance Review must be opened before Sprint 2 Flickr harvest begins
- The review must address: permanent platform risk acceptance, contingency plan for platform failure, whether an alternative direct access path (NOAA Open Data Dissemination, Data.gov, institutional request) should be pursued before committing to Flickr as production
- Platform Dependency Governance Review must produce a decision document (DD-NOAA-002 or equivalent) authorizing the Flickr path as production
- Without that document, Sprint 2 NOAA ingestion is halted

### IV.5 Halt Conditions

NOAA ingestion via the Flickr path MUST halt immediately under any of the following conditions:
- Flickr API returns authentication errors for the `FLICKR_API_KEY` for more than 24 hours
- Flickr changes license field semantics such that License 8 no longer maps to "United States Government Work"
- NOAA's official Flickr accounts (@usoceangov, @noaafisheries) become inaccessible
- SmugMug/Flickr announces terms-of-service changes materially affecting API access or commercial downstream use of accessed content

On halt, NC must document the halt condition, notify the Principal Architect, and await a remediation decision (alternative path or amended SA).

---

## Part V — Sprint 1 Acceptance Criteria

Sprint 1 files authorized:

```
workers/noaa_adapter/__init__.py
workers/noaa_adapter/config.py
workers/noaa_adapter/flickr_client.py
tests/unit/test_noaa_flickr_client.py
tests/replay/test_noaa_adapter_sprint1.py
tests/fixtures/noaa/
```

Sprint 1 acceptance criteria:

1. Flickr API key read only from `FLICKR_API_KEY` environment variable; never hardcoded
2. API key passed as `api_key` parameter; never appears in source code, fixtures, or logs
3. `flickr.people.getPhotos` method used with NOAA NSID(s) confirmed in Sprint 1
4. `license=7,8,9,10` pre-filter applied to API request
5. Image URL extracted using the hierarchy: `url_o` → `url_l` → `url_c` → `url_z` → block
6. SA-NOAA-001 Path A primary gate (`license` integer) applied to every record
7. SA-NOAA-001 secondary validation (credit line, personal name, commercial operator) applied
8. `rights_status: "pending_verification"` written (not `"verified_pd"`)
9. Subject-matter scope filter applied (Article 9 enforcement)
10. `FLICKR_API_KEY` → `NSID` resolution for @usoceangov and @noaafisheries confirmed and documented
11. `url_o` availability confirmed or `url_l` designated as primary per Sprint 1 finding
12. Photo Library evaluation finding documented (Part II Sprint 1 deliverable)
13. Replay tests run without network access via mock transport
14. No store writes exist in Sprint 1 adapter code

---

## Part VI — Invariants

**SA002-I-1 — Sprint 1 Scope Cap.** The Flickr path is authorized for Sprint 1 (50 assets, 90 days) only. Sprint 2 Flickr harvest requires Gate 2A or Gate 2B from Section I.1.

**SA002-I-2 — No IIIF.** The NOAA adapter must not use IIIF protocols at any path. Direct URL delivery only.

**SA002-I-3 — URL Hierarchy Priority.** `url_o` takes priority over `url_l`. If `url_o` is available, the adapter must not fall back to `url_l`. Deliberate use of a lower-resolution URL when a higher-resolution URL is available is a bug.

**SA002-I-4 — Halt Conditions Binding.** The halt conditions in Section IV.5 are binding operational rules, not advisory. Any engineer detecting a halt condition must stop ingestion immediately and document the event.

**SA002-I-5 — Platform Dependency Statement Immutability.** This Platform Dependency Statement (Part IV) is a permanent governance record. It must not be removed in future SA versions. Amended versions may modify risk assessments and decision gates but must retain the historical record of the Sprint 1 platform dependency decision.

**SA002-I-6 — FM-4 (Permanent).** Foundation Model output may not influence delivery path selection, image URL extraction, resolution selection, or any field in `media_file` or `media_rights`. FM-4 from the Foundation Model Constitution v1.0 applies without exception.

---

## Part VII — Open Questions

**OQ-1 — `url_o` access for NOAA Flickr accounts.** Sprint 1 must confirm whether NOAA's government accounts have enabled full-resolution original sharing. If `url_o` is absent, this is confirmed behavior (not a bug), and `url_l` becomes the de facto primary. SA-NOAA-002 v1.1 will update the URL hierarchy accordingly.

**OQ-2 — Multiple NOAA Flickr accounts.** There may be additional NOAA division accounts beyond @usoceangov and @noaafisheries. Sprint 1 must audit NOAA's Flickr presence and document all confirmed federal accounts. Any additional accounts require explicit governance confirmation before ingestion.

**OQ-3 — Photo Library access path type.** If Sprint 1 finds an undocumented API endpoint in the Photo Library, SA-NOAA-002 v1.1 must define it formally. If only HTML scraping is available, a DD-NOAA-002 must govern whether NC accepts scraping as a delivery mechanism (not addressed in this version).

**OQ-4 — NOAA Open Data Dissemination (NODD) as S3 analog.** NOAA's Open Data Dissemination program provides AWS S3 access to NOAA datasets. Most NODD content is scientific/numerical data (weather model output, satellite L2 data). Sprint 2 should evaluate whether any NODD S3 buckets contain image-format content suitable for NC. If yes, an S3 delivery path would be a stronger production alternative than Flickr.

**OQ-5 — Scope filter refinement.** The Sprint 1 subject-matter scope filter (Section I.8) uses a tag-based heuristic. Sprint 1 must evaluate whether Flickr collection/album structure provides a more reliable scope filter than individual tags, and document findings for SA-NOAA-002 v1.1.

---

*SA-NOAA-002 v1.0.0 — drafted 2026-06-11*  
*Authority: DD-NOAA-001 · SA-NOAA-001 · NOAA Governance Review v1*  
*Precedent: SA-23 (NARA Direct Image Delivery) — same Rights Class 9, direct-URL delivery model*  
*Architectural novelty: First third-party platform delivery path (Flickr) in NC adapter portfolio — Platform Dependency Statement (Part IV) is a new governance artifact class*  
*Next version trigger: Sprint 1 Photo Library evaluation finding; `url_o` availability confirmation; additional NOAA account audit*
