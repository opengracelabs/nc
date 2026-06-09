# DD-MET-001 — Metropolitan Museum of Art Open Access Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-MET-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first Metropolitan Museum governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 |

---

## Background

The Metropolitan Museum of Art (The Met) is one of the world's largest art museums,
holding a permanent collection of over two million objects spanning five thousand years
of art from every culture and geography. The Met's Open Access programme, launched in
February 2017, placed approximately 375,000 images — now exceeding 492,000 as of 2024 —
in the public domain under CC0 (Creative Commons Zero). This is one of the most
consequential open access decisions made by any major cultural institution globally,
and it creates a direct pipeline to NC's commerce mission.

The Institution Coverage Audit v1.0 (Article 2) rated The Met as a **Tier 1 Core**
content institution with: Rights A (CC0), Volume Very High, API Good, IIIF Yes,
Geographic Reach: Global (acquisitions). The Coverage Audit placed The Met in Wave 4
onboarding ("Met, Getty, British Library, Kew — enrich existing North America +
botanical pipeline — Medium complexity"). This Decision constitutes the formal Stage 1
Discovery Report and initiates Stage 2 Governance for The Met.

This Decision presents four governance complexities absent from or different in prior DDs:

1. **No OAI-PMH.** The Met's Open Access API is a custom REST JSON API — not OAI-PMH.
   Bulk enumeration follows the REST cursor pattern (retrieve all object IDs via a
   single endpoint, then iterate per-record). This is the first NC institution to use
   this enumeration pattern at scale.

2. **Boolean rights architecture.** The Met uses `isPublicDomain: true/false` (a
   boolean flag) rather than URI-form rights statements (`edm:rights` vocabulary).
   The Europeana Rights Matrix v1.0 does not govern boolean-form rights attestation.
   A Met-specific rights matrix is required. It is simpler than prior institution
   matrices — but it is institution-specific, not URI-general.

3. **Direct image delivery — IIIF confirmation required.** The Met's API returns
   direct image URLs (`primaryImage` field) pointing to JPEG files at
   `https://images.metmuseum.org/CRDImages/`. IIIF Presentation API manifest
   availability requires live verification before the IIIF governance article can be
   finalized. This DD establishes the governance framework pending that confirmation;
   a DD-MET-001-A1 amendment is authorized if live testing reveals material differences
   from findings stated here.

4. **Bulk CSV export path.** The Met publishes a complete metadata export
   (`MetObjects.csv`) via its GitHub repository (`github.com/metmuseum/openaccess`),
   updated periodically. This export contains all metadata fields including the
   `Is Public Domain` column. It is a supplemental enumeration path — faster than
   iterating all object IDs via API — but it is a static snapshot. The governance
   relationship between the CSV export and the live API requires explicit definition.

The Met is not registered in the NC `sources` table as of the date of this Decision.
This Decision, if ratified, authorizes an INSERT. No prior governance document has
authorized Metropolitan Museum ingestion into the NC pipeline.

---

## Part I — Source Classification Audit

**F-1. Direct content institution.** The Metropolitan Museum of Art holds, acquires,
curates, and serves its own permanent collection through first-party infrastructure.
The Open Access API (`collectionapi.metmuseum.org`) is a first-party API operated
entirely by The Met. All provenance chains terminate at The Met's acquisition records.
This is a one-tier provenance model: The Met → NC. The aggregator-source designation
applied to Europeana (DD-EUR-001) and DPLA (DD-DPLA-001) does not apply. The Met is
a **direct content institution**, the same category as Rijksmuseum and BnF Gallica.

**F-2. Open Access programme scope.** The Met's CC0 designation covers 492,000+ objects
as of 2024. These are objects determined by The Met's curators to be in the public
domain in the United States. The determination is institutional — not an automated
date calculation alone. The Met employs dedicated rights staff who review PD status.
NC treats The Met's `isPublicDomain: true` designation as an institutional rights
determination equivalent to the Rijksmuseum's CC0 designation.

**F-3. Collection scope for NC's mission.** The Met's collection spans all geographies
and periods. The NC-relevant subset (pre-1900 PD material with strong illustration,
cartographic, or natural history content) is commercially substantial:

| Department | NC relevance | Content type | Commercial priority |
|---|---|---|---|
| Asian Art | High | Japanese woodblock prints (ukiyo-e), Chinese botanical art, Korean nature painting | Very High — Japan, China, Korea geographic gap |
| Drawings and Prints | Very High | European natural history illustration, botanical prints, zoological engravings | Very High — Priority Illustrator tier |
| Egyptian Art | High | Place-anchored cultural objects; naturalistic animal and plant motifs | High — Egypt/Nile Valley place pages |
| Photographs | High | Pre-1928 natural history and landscape photography | High — multiple geographic regions |
| European Paintings | Medium | Pre-1900 botanical and nature paintings | Medium — supplemental to illustration tier |
| Greek and Roman Art | Medium | Mediterranean cultural objects; place-anchored (Athens, Crete, Sicily) | Medium |
| Islamic Art | Medium | Islamic geometric and naturalistic art; geographic reach to Middle East, Central Asia | Medium |
| Arts of Africa, Oceania, and the Americas | Medium | Pre-colonial cultural objects; geographic relevance to regions NC lacks | Medium |
| Ancient Near East | Lower | Archaeological objects; limited illustration commercial appeal | Lower |

**F-4. Priority illustrator coverage.** The Met holds material directly relevant to
NC's Priority Illustrator Registry and Golden Age (1750–1900) commercial mandate:

| Illustrator / Category | Met holding | Coverage quality |
|---|---|---|
| Katsushika Hokusai | Significant woodblock print collection including nature subjects ("Thirty-Six Views of Mount Fuji", fish and shell series) | Strong — multiple prints confirmed CC0 |
| Utagawa Hiroshige | Large collection of landscape and nature woodblock prints | Strong — "One Hundred Famous Views of Edo" series |
| European botanical engravers | Drawings and Prints department holds pre-1900 botanical, zoological, and cartographic prints from multiple European traditions | Good — requires subject-level filtering |
| Edward Lear | Lear material in Drawings and Prints department | Requires enumeration verification |
| John James Audubon | Audubon prints held at institutional scale (Smithsonian primary; Met supplemental) | Supplemental — verify via search |

**F-5. Classification ruling.** The Metropolitan Museum of Art is classified as a
**Tier 1 Core direct content institution** (Institution Coverage Audit v1.0 Article 2,
Article 14). Its institutional category is identical to Rijksmuseum and BnF Gallica.
Wave 4 onboarding per Coverage Audit Article 17. This Decision, if ratified, initiates
Wave 4 formal onboarding.

---

## Part II — Rights Strategy Audit

**F-6. The Met rights architecture — boolean, not URI.** Unlike all prior NC institutions
(Europeana, Rijksmuseum, BnF Gallica), The Met's API does not use URI-form rights
statements. The governing rights field is:

```json
"isPublicDomain": true
```

This is a boolean field present in every API response for every object. The secondary
field is:

```json
"rightsAndReproduction": ""
```

This is a free-text string. For CC0 objects, `rightsAndReproduction` is an empty string.
For non-PD objects, it contains copyright notice text (e.g., "© Artist Name" or
"© [Estate/Gallery]"). The `rightsAndReproduction` field is not a reliable primary
rights authority — it is a secondary cross-check only.

**F-7. Europeana Rights Matrix inapplicability.** The Europeana Rights Matrix v1.0
governs URI-form rights statements (`edm:rights` vocabulary). The Met does not use
URI-form rights statements. The Matrix does not govern `isPublicDomain: true/false`.
A **Met Rights Matrix v1** is required as an institution-specific rights instrument.

The Met Rights Matrix v1 is simpler than all prior matrices:
there are exactly two classification outcomes — ALLOWED and BLOCKED. No REVIEW_REQUIRED
class exists at the pre-ingestion filter stage, because `isPublicDomain` is always
present in API responses and its meaning is not ambiguous.

**F-8. Met Rights Matrix v1.**

**Table MR-1A — ALLOWED**

| Condition | NC classification | Worker action | Human review rule |
|---|---|---|---|
| `isPublicDomain: true` | ALLOWED → CC0 | Set `rights_status = 'pending_verification'` | HR-MET-1: confirm CC0 against Met Open Access policy; confirm image URL resolves |
| `isPublicDomain: true` AND `primaryImage` non-empty | ALLOWED → CC0 | Set `rights_status = 'pending_verification'`; capture image URL | HR-MET-1 |

**Table MR-2 — BLOCKED**

| Condition | Block reason | Worker action |
|---|---|---|
| `isPublicDomain: false` | Non-PD work; copyright retained or licensed | Reject before any DB write; log `blocked_reason = 'not_public_domain'` |
| `isPublicDomain: true` AND `primaryImage` empty string | PD object but no image delivered | Reject as ineligible for Phase 1 pipeline; log `blocked_reason = 'no_image_url'` |
| `isPublicDomain` field absent from API response | Cannot classify; treat as absent per CI-5 | Reject; log `blocked_reason = 'missing_rights_field'` |

**Table MR-3 — No REVIEW_REQUIRED class**

The Met Rights Matrix v1 does not include a REVIEW_REQUIRED class at the pre-ingestion
filter stage. The `isPublicDomain` boolean is binary and does not admit of an intermediate
classification. Records that fail the ALLOWED criteria are BLOCKED.

The NC constitutional REVIEW_REQUIRED pathway (MSC v1.2; `workflow_item` with
`capability = 'rights_review'`) remains available for post-ingest human escalation
on specific records, but it is not triggered by the Met Rights Matrix automatically.

**F-9. `block_if_absent` implementation.** Constitutional invariant CI-5 requires that
absent rights field routes to BLOCKED, not REVIEW_REQUIRED. For The Met, the `isPublicDomain`
field is structurally always present in API responses. Nonetheless, the `block_if_absent`
guard must be implemented as a defensive check before any DB write:

```python
is_pd = normalized.get("is_public_domain")
if is_pd is None:                          # BLOCKED — field absent
    return {"status": "rejected", "reason": "missing_rights_field", "writes": 0}
if is_pd is False:                         # BLOCKED — not public domain
    return {"status": "rejected", "reason": "not_public_domain", "writes": 0}
if not normalized.get("primary_image"):    # BLOCKED — no image URL
    return {"status": "rejected", "reason": "no_image_url", "writes": 0}
# ALLOWED — proceed
```

**F-10. The Met as public domain authority.** The Met's `isPublicDomain: true` designation
is the product of institutional rights review by The Met's curators. The Met has published
and maintained an explicit Open Access policy since February 2017. NC treats The Met as a
**Tier 1 NC public domain authority** for its CC0-designated collection, with the following
conditions:

- (a) The `isPublicDomain: true` designation is treated as equivalent to a PDM
  (Public Domain Mark) designation for NC pipeline classification purposes.
- (b) The human reviewer's confirmation burden (HR-MET-1) is: confirm that the
  `isPublicDomain` flag is `true` in the API response, confirm the image URL resolves,
  and confirm the object date is consistent with a PD determination. Full independent
  copyright analysis is not required for objects with unambiguous pre-1928 dates.
- (c) For objects where `objectEndDate` (the latest possible creation date) is after 1927,
  the reviewer must apply independent PD analysis — The Met's `isPublicDomain: true`
  on a post-1927 creation date requires verification of the specific rights basis
  (e.g., author died before 1956, US formality failure, or other PD route).
- (d) The Met's authority status may be suspended by Director Decision if evidence
  emerges that The Met is systematically misclassifying non-PD objects as `isPublicDomain: true`.

**F-11. FM-4 permanent.** FM-4 applies permanently to all Met rights determinations.
No FM output may influence any `media_rights` record for any Met-sourced asset. The
simplicity of the Met Rights Matrix (boolean) does not change this constitutional
requirement.

---

## Part III — API Surface Audit

**F-12. Met Open Access API endpoints.** The Met exposes a custom REST JSON API at:

```
Base URL: https://collectionapi.metmuseum.org/public/collection/v1/
```

| Endpoint | Method | Response | NC use |
|---|---|---|---|
| `/objects` | GET | `{ "total": N, "objectIDs": [id, id, ...] }` | Bulk enumeration — returns ALL object IDs |
| `/objects?departmentIds=N` | GET | `{ "total": N, "objectIDs": [...] }` | Department-scoped enumeration |
| `/objects/{objectID}` | GET | Full object JSON | Per-record metadata fetch |
| `/departments` | GET | Array of `{ departmentId, displayName }` | Department discovery and scoping |
| `/search?q=...` | GET | `{ "total": N, "objectIDs": [...] }` | Subject / keyword search |
| `/search?q=*&isPublicDomain=true` | GET | PD-filtered object ID list | PD-filtered enumeration |
| `/search?q=*&isPublicDomain=true&departmentId=N` | GET | Department + PD filtered | Pilot scoping path |

**Authentication:** None. The API is fully open — no API key, no OAuth, no registration
required.

**F-13. Enumeration strategy — REST cursor pattern.** The Met's `/objects` endpoint returns
ALL object IDs in a single JSON response (no pagination). As of 2024, this response contains
~490,000 integer IDs in a single array. This is the Met-specific enumeration pattern:

```
Step 1: GET /objects?departmentIds={id}  →  list of objectIDs for the department
Step 2: For each objectID: GET /objects/{objectID}  →  full record JSON
Step 3: At worker layer: if isPublicDomain is True and primaryImage is non-empty → ALLOWED; else BLOCKED
```

For production (full collection), the full-enumeration path is:
```
Step 1: GET /objects  →  all ~490K object IDs
Step 2: Filter by isPublicDomain: true at record level (reduces to ~492K PD records)
Step 3: Iterate per-record with rate limiting
```

This enumeration pattern differs from all prior NC institutions (OAI-PMH at Europeana,
Rijksmuseum, DPLA, BnF Gallica). It requires a dedicated adapter — the OAI-PMH adapter
pattern does not apply.

**F-14. Bulk CSV export — supplemental path.** The Met maintains a bulk metadata export:

```
Repository:  github.com/metmuseum/openaccess
File:        MetObjects.csv
Contents:    All collection objects; all metadata fields; "Is Public Domain" column (TRUE/FALSE)
Size:        ~250 MB
Update cadence:  Periodic (not real-time)
```

The CSV export provides a static snapshot of all metadata. Its primary value for NC is:

- Pre-filtering: extract all rows where `Is Public Domain = True` without iterating the API
- Batch planning: estimate department-level PD volumes for pilot scoping
- Deduplication seed: cross-reference against NC's `source_item` table during bulk import

The CSV is **not** a substitute for live API fetches in the production pipeline:
- It may lag the live API by days or weeks
- Image URLs in the CSV may be stale if The Met's CDN structure changes
- Rights status in the CSV may not reflect recent changes to `isPublicDomain`

The NC adapter must use the live API for all production record creation. The CSV is
authorized as a planning and batch-scoping instrument only.

**F-15. Rate limiting.** The Met's Open Access API has no published rate limit. The
institution requests "reasonable use." NC policy for a public, unauthenticated API without
published limits is: ≤ 5 requests per second, with exponential backoff on any HTTP 429.
This is conservative relative to observed API behavior but appropriate for a production
pipeline that must not create access degradation for other API users.

**F-16. API response completeness.** The Met's per-object response is structurally complete
for NC's pipeline needs. Fields of particular importance:

| Field | NC pipeline use | Notes |
|---|---|---|
| `isPublicDomain` | Primary rights gate | Always present; boolean |
| `primaryImage` | `media_file.source_url` | Empty string if no image (not null) |
| `additionalImages` | Secondary image array | May be large; policy required (see Article 3) |
| `objectID` | `source_item.provider_item_id` | Integer; stable identifier |
| `objectURL` | `source_record.object_page_url` | Canonical Met page for provenance |
| `objectWikidata_URL` | Entity linking → Wikidata QID | Enables NC place/creator entity linking |
| `tags[].Wikidata_URL` | Subject entity linking | Enables NC subject → canonical entity links |
| `tags[].AAT_URL` | AAT subject classification | Art & Architecture Thesaurus IDs |
| `country`, `region`, `subregion`, `city` | Geographic metadata → place association | Rich geographic provenance; key for NC place pages |
| `geographyType` | Place association qualifier | "From", "Found in", "Probably from", etc. |
| `department` | `anchor_type` derivation + pilot scoping | Governs department-based pilot queries |
| `objectDate`, `objectBeginDate`, `objectEndDate` | PD date analysis | Integer begin/end dates enable date-based PD range checks |
| `artistWikidata_URL` | Creator entity linking → Priority Illustrator match | Enables direct Priority Illustrator Registry lookup |
| `artistULAN_URL` | ULAN creator identifier | Cross-reference for creator deduplication |
| `constituents` | Full creator array | Multiple creator records with roles |

**F-17. `additionalImages` policy requirement.** The Met's API returns an `additionalImages`
array that can contain zero to dozens of additional image URLs per object. For NC's Phase 1
pipeline:

- `primaryImage` is the authoritative Phase 1 delivery target
- `additionalImages` are not ingested in the pilot; they are not production-blocked
- Future Phase 1+ policy may authorize ingestion of `additionalImages` as secondary
  `media_file` rows per object. This requires a Director Decision before implementation.
- For Asset Zero and the pilot, `additionalImages` is logged but not written to `media_file`.

---

## Part IV — IIIF and Image Delivery Audit

**F-18. Image delivery via direct URL.** The Met's API delivers images via direct JPEG URLs:

```
primaryImage: "https://images.metmuseum.org/CRDImages/{department}/{size}/{filename}.jpg"
```

The URL pattern uses a Met CDN (`images.metmuseum.org`). The size component may vary:
`original` is the preferred full-resolution path. This is a direct JPEG delivery — not
a IIIF Image API tile URL in the standard IIIF form (`/iiif/2/{identifier}/full/full/0/default.jpg`).

**F-19. IIIF Presentation API manifest availability — requires live verification.**
The Met has announced IIIF support and provides IIIF manifests for public domain objects.
The expected manifest URL pattern is:

```
https://collectionapi.metmuseum.org/public/collection/v1/iiif/{objectID}/manifest.json
```

This endpoint is not explicitly documented in the current Met Open Access API documentation.
Live verification against this URL pattern is a Gate 3 prerequisite. Two outcomes are possible:

| Outcome | Governance response |
|---|---|
| Manifests are available and valid for PD objects | IIIF Presentation API authorized; `media_file.iiif_manifest_url` populated |
| Manifests are absent or return 404/403 | DD-MET-001-A1 required; image delivery via `primaryImage` URL only; `iiif_manifest_url = null` |

If manifests are available, they are expected to be IIIF Presentation API 3.0 (consistent
with The Met's stated standards compliance). If they are IIIF Presentation API 2.x, the
Gallica bridging specification pattern (DD-GALLICA-001 Article 4) applies.

**F-20. Minimum dimension compliance.** MSC v1.2 Article 29.2(d) requires a minimum
400px on the shortest side. The Met's open access images are routinely 3000–7000px on
the longest side for high-quality works. Dimension compliance is expected to be
straightforward. Asset Zero must confirm via HTTP HEAD or `media_technical_metadata`.

**F-21. No watermark on open access images.** The Met's CC0 open access images are
served without watermarks. The `images.metmuseum.org` CDN serves full-resolution
watermark-free images for all `isPublicDomain: true` objects with a non-empty
`primaryImage` URL. Watermark-free delivery does not require a specific Asset Zero
validation gate (unlike BnF Gallica), but it must be confirmed during Asset Zero
as a procedural check.

**F-22. Image delivery governance — `primaryImage` as primary source_url.** Pending
IIIF Presentation API manifest confirmation, the `primaryImage` URL is the authoritative
`media_file.source_url` for all Met objects in the pipeline. This constitutes a
deviation from the IIIF-primary delivery standard (Standards Constitution v1.0 Article
10). This deviation is authorized by this Decision for the pilot period, subject to the
following conditions:

- (a) IIIF manifest availability is confirmed or ruled out at Gate 3 via live testing
- (b) If IIIF manifests are not available: `media_file.source_url = primaryImage URL`,
  `media_file.iiif_manifest_url = null`, `source_record.schema_standard = 'met_openaccess_v1'`
- (c) If IIIF manifests are available: `media_file.iiif_manifest_url` populated from
  manifest endpoint, `media_file.source_url = primaryImage URL` (retained as direct URL),
  `source_record.schema_standard = 'met_openaccess_iiif_v1'`
- (d) A Standards Constitution amendment (SA-7) is required to formally register either
  the IIIF path or the direct URL path for the Met adapter. SA-7 may not be bypassed
  by treating the primaryImage URL as a IIIF URL.

---

## Part V — Commercial Opportunity Assessment

**F-23. Illustration Opportunity density.** The Met's CC0 collection of 492,000+
objects is large, but NC's commercial mission requires Illustration Opportunities (IOs) —
not raw object counts. IOs are objects with strong natural history, geographic, or cultural
illustration content that can be activated as NC products. The Met's IO density is:

| Department | Est. PD objects | Est. IOs for NC | IO density | Priority |
|---|---|---|---|---|
| Asian Art | ~60,000 | ~8,000–15,000 | High | Very High |
| Drawings and Prints | ~80,000 | ~20,000–35,000 | Very High | Very High |
| Photographs | ~25,000 | ~5,000–10,000 | High | High |
| Egyptian Art | ~35,000 | ~3,000–6,000 | Medium-High | High |
| European Paintings | ~2,500 | ~400–800 | Medium | Medium |
| Islamic Art | ~12,000 | ~2,000–4,000 | Medium | Medium |
| Greek and Roman Art | ~17,000 | ~1,500–3,000 | Medium | Medium |

The Drawings and Prints and Asian Art departments together represent the core NC
commercial opportunity: tens of thousands of pre-1900 illustrations spanning natural
history, botanical art, cartography, and cultural illustration at outstanding quality.

**F-24. Japan geographic gap activation.** The Coverage Audit (OQ-4) identified Japan
as a top-5 global tourism destination with zero NC source coverage. The Met's Asian Art
department is the single richest institutional source for pre-1900 Japanese woodblock
prints (ukiyo-e) accessible to NC under CC0. The Hokusai and Hiroshige collections alone
represent hundreds of prints depicting:

- Mount Fuji and the Tōkaidō landscape (geographic → Japan place pages)
- Fish, shellfish, and marine life (biological → coastal Japan)
- Birds and flowers (biological → Japanese endemic species)
- Rain, snow, and seasonal landscapes (geographic + atmospheric)

This is the highest-priority NC commercial use case for The Met's collection.

**F-25. Deduplication with prior sources.** The Met's objects are not currently in NC's
pipeline via any aggregator route. The Europeana and DPLA aggregators do not include Met
objects (The Met does not contribute to Europeana or DPLA). No deduplication
protocol is required at activation. This is a clean first-ingestion scenario.

---

## Decision

### Article 1 — Source Classification Authorization

The Metropolitan Museum of Art is classified as a **Tier 1 Core direct content
institution** in NC's institutional taxonomy. This is the first and authoritative
governance classification for The Met as an NC source.

**(a)** The Met is not an aggregator. The aggregator-source designation of Europeana
(DD-EUR-001) and DPLA (DD-DPLA-001) does not apply. The provenance model is one-tier:
The Met → NC.

**(b)** This Decision authorizes an INSERT into the `sources` table creating a new record
for `source_id = 'met'`. The `governance_state = 'active'` designation is authorized.

**(c)** The Met is a Wave 4 institution per Institution Coverage Audit v1.0 Article 17.
This DD initiates Wave 4 onboarding for The Met.

**(d)** The Met's institution number context:

| # | Institution | Source Role | DD Status |
|---|---|---|---|
| 1 | BHL | Direct | Active (seeded) |
| 2 | Europeana | Aggregator | DD-EUR-001 pending ratification |
| 3 | Library of Congress | Direct | Pending |
| 4 | Rijksmuseum | Direct | DD-RIJKSMUSEUM-001 pending ratification |
| 5 | DPLA | Aggregator | DD-DPLA-001 pending ratification |
| 6 | BnF Gallica | Direct | DD-GALLICA-002 pending ratification |
| **7** | **Metropolitan Museum of Art** | **Direct** | **DD-MET-001 (this Decision)** |

---

### Article 2 — Met Rights Matrix v1

The **Europeana Rights Matrix v1.0** does not govern Metropolitan Museum assets. The Met
does not use `edm:rights` URI vocabulary. This Decision defines and ratifies the **Met
Rights Matrix v1** as the governing rights instrument for all Met-sourced assets.

#### 2.1 Rights Determination Authority

The Met's `isPublicDomain` field is the sole and authoritative rights classification
signal. It is set by The Met's curatorial and rights staff under The Met's CC0 Open
Access Policy (effective February 2017). NC treats this designation as a Tier 1
institutional PD authority determination (F-10).

#### 2.2 Classification Table

**Table MR-1A — ALLOWED**

| `isPublicDomain` | `primaryImage` | NC classification | Worker action |
|---|---|---|---|
| `true` | Non-empty URL | ALLOWED → CC0 | Proceed to record creation; `rights_status = 'pending_verification'` |

No partial-ALLOWED class exists. Both conditions must be met.

**Table MR-2 — BLOCKED**

| Condition | Block code | Pre-DB rejection |
|---|---|---|
| `isPublicDomain: false` | `not_public_domain` | Yes — reject before any DB write |
| `isPublicDomain: true` AND `primaryImage = ""` (empty) | `no_image_url` | Yes — reject before any DB write |
| `isPublicDomain` field absent | `missing_rights_field` | Yes — reject before any DB write (CI-5) |
| Any other unanticipated state | `unclassifiable` | Yes — reject; escalate to Director |

**No REVIEW_REQUIRED class exists for the Met Rights Matrix v1.**

#### 2.3 Human Review Rule HR-MET-1

For all ALLOWED records (Table MR-1A), the human reviewer must confirm:

1. `isPublicDomain = true` confirmed in live API response for the specific `objectID`
2. `primaryImage` URL resolves (HTTP 200) at full resolution
3. `objectEndDate ≤ 1927` — if true, PD confirmation is complete
4. `objectEndDate > 1927` — reviewer must document the specific PD basis (death date,
   formality failure, or other instrument) before setting terminal rights status
5. Image is watermark-free at the resolved URL

No independent copyright analysis is required for items where conditions 1–3 are all
satisfied. Conditions 1–5 together constitute the complete HR-MET-1 review.

#### 2.4 Rights Evidence Fields

For every Met `media_rights` row, the evidence dict must contain all CI-8 required fields:

```python
{
    "source": "met",
    "source_record_id": "<source_record.id>",
    "met_is_public_domain": true,
    "rights_matrix_classification": "ALLOWED",
    "applying_policy": "met_rights_matrix_v1",
    "met_object_id": "<objectID>",
    "raw_payload_hash": "<SHA256 of raw API response>",
    "worker_classified_status": "pending_verification",
    "evidence_status": "worker_classified"
}
```

The field `met_is_public_domain` is the Met-specific equivalent of `edm_rights_uri` in
prior institutions' evidence dicts. It satisfies CI-8's requirement for a rights
statement field.

#### 2.5 FM Exclusion (Permanent)

FM-4 applies permanently to all Met rights determinations. No FM output may influence
any `media_rights` record for any Met-sourced asset. The boolean simplicity of the Met
Rights Matrix does not modify or relax this requirement.

---

### Article 3 — API Governance

#### 3.1 Authorized API Surfaces

The following Met API surfaces are authorized for pilot ingestion:

| Surface | Endpoint | Use | Status |
|---|---|---|---|
| Object enumeration (department) | `GET /public/collection/v1/objects?departmentIds={id}` | Pilot scoping by department | Authorized |
| Object enumeration (PD-filtered search) | `GET /public/collection/v1/search?q=*&isPublicDomain=true&departmentId={id}` | PD-filtered enumeration | Authorized |
| Per-record fetch | `GET /public/collection/v1/objects/{objectID}` | Metadata + rights + image URL | Authorized |
| Department discovery | `GET /public/collection/v1/departments` | Department ID enumeration | Authorized |
| Bulk CSV export | `github.com/metmuseum/openaccess MetObjects.csv` | Pilot planning and batch scoping only | Authorized (planning only) |

The following surfaces are **not authorized** under this Decision:

| Surface | Reason |
|---|---|
| Full `/objects` (all 490K IDs) | Pilot scope only; full enumeration requires DD-MET-002 |
| Met TheMet API (3D model data) | Phase 4; not in scope |
| Met digital labels or curatorial text APIs | Not evaluated; separate decision required |
| `additionalImages` for DB write | Policy deferred (F-17); requires Director Decision |

#### 3.2 Enumeration Protocol

For the pilot, the authorized enumeration protocol is:

```python
# Step 1: Get department-scoped PD object IDs
resp = GET /search?q=*&isPublicDomain=true&departmentId={PILOT_DEPT_ID}
object_ids = resp["objectIDs"]  # may be empty if department has no search results

# Step 2: Fetch per-record detail with rate limiting
for obj_id in object_ids[:PILOT_CAP]:
    record = GET /objects/{obj_id}
    # Step 3: Apply Met Rights Matrix v1
    if classify_met_rights(record) == "ALLOWED":
        write_record(record)  # M36 write path
    else:
        log_blocked(record)
```

The `isPublicDomain=true` filter in the search step is a pre-filter only — the per-record
Met Rights Matrix check (Article 2.2) must still be applied at the worker layer. A record
returned by the search filter must not be assumed to be ALLOWED without the worker check.

#### 3.3 Rate Limiting

| Parameter | Value | Authority |
|---|---|---|
| `requests_per_second` | ≤ 5 | This Article |
| `burst` | 10 | This Article |
| `timeout_seconds` | 30 | This Article |
| Backoff on HTTP 429 | Exponential, 2× per retry, max 5 retries | Standard NC policy |
| User-Agent header | `NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)` | Required for good API citizenship |

#### 3.4 Authentication

None. No API key, OAuth, or registration is required. The API is fully open.

#### 3.5 `additionalImages` Policy

`additionalImages` must be logged in `source_record.raw_payload` (as part of the
raw JSON hash) but must not generate additional `media_file` rows during the pilot.
The primary `media_file` row uses `primaryImage` only. This policy is encoded in the
adapter and requires a Director Decision to change.

---

### Article 4 — Image Delivery Governance

#### 4.1 Primary Image Delivery

`media_file.source_url` is set to the `primaryImage` URL from the Met API response:

```
https://images.metmuseum.org/CRDImages/{department}/{path}/{filename}
```

This is a direct JPEG delivery URL. It is not a IIIF Image API URL. NC's image
retrieval pipeline (preservation_event: `preservation_retrieval`) fetches from this URL.

#### 4.2 IIIF Presentation API Manifest — Conditional

Live verification of the IIIF manifest endpoint is a Gate 3 prerequisite:

```
GET https://collectionapi.metmuseum.org/public/collection/v1/iiif/{objectID}/manifest.json
```

**If manifests are available (HTTP 200):**
- `media_file.iiif_manifest_url` is populated with the manifest URL
- `source_record.schema_standard = 'met_openaccess_iiif_v1'`
- Standards Amendment SA-7 must specify the met_openaccess_iiif_v1 schema standard

**If manifests are unavailable (HTTP 404 / absent from all tested objects):**
- `media_file.iiif_manifest_url = null`
- `source_record.schema_standard = 'met_openaccess_v1'`
- A DD-MET-001-A1 amendment is required to record this finding and specify the
  direct-URL delivery governance
- Standards Amendment SA-7 must specify the met_openaccess_v1 schema standard (no IIIF)

The Principal Architect must produce DD-MET-001-A1 before Gate 3 is closed if IIIF
manifest confirmation contradicts findings in this Decision.

#### 4.3 Minimum Dimension Requirement

MSC v1.2 Article 29.2(d) minimum (400px on shortest side) applies. The Met's CC0
images are routinely well above this threshold. Objects where `primaryImage` resolves
to an image below the minimum dimension must be rejected and logged. The expected
rejection rate on this criterion is near-zero but must be implemented.

---

### Article 5 — Metadata Field Mapping

The Met adapter maps API JSON fields to NC's `source_record` layer:

| Met API field | NC field | Notes |
|---|---|---|
| `objectID` | `source_item.provider_item_id` | Integer; cast to string for storage |
| `objectURL` | `source_record.object_page_url` | Canonical provenance URL |
| `title` | `source_record.title` | First / primary title |
| `objectName` | `source_record.object_name` | Object type descriptor |
| `artistDisplayName` | `source_record.creator` | Primary creator display string |
| `constituents` | `source_record.creator_array` | Full creator array with roles |
| `artistWikidata_URL` | `source_record.creator_wikidata_url` | Enables Priority Illustrator lookup |
| `artistULAN_URL` | `source_record.creator_ulan_url` | ULAN cross-reference |
| `objectDate` | `source_record.date_display` | Raw date string |
| `objectBeginDate` | `source_record.date_begin` | Integer year |
| `objectEndDate` | `source_record.date_end` | Integer year — key for PD date analysis |
| `medium` | `source_record.medium` | Material description |
| `dimensions` | `source_record.dimensions` | Physical dimensions text |
| `department` | `source_record.department` | Met department name |
| `culture` | `source_record.culture` | Cultural attribution |
| `period` | `source_record.period` | Chronological period |
| `classification` | `source_record.classification` | Object type classification |
| `creditLine` | `source_record.credit_line` | Acquisition provenance |
| `country` | `source_record.country` | Geographic provenance — country |
| `region` | `source_record.geographic_region` | Geographic provenance — region |
| `subregion` | `source_record.geographic_subregion` | Geographic provenance — subregion |
| `city` | `source_record.geographic_city` | Geographic provenance — city |
| `geographyType` | `source_record.geography_type` | "From", "Found in", "Probably from", etc. |
| `river`, `locale`, `locus`, `excavation` | `source_record.geographic_detail` | Additional geographic specificity |
| `isPublicDomain` | `source_record.rights_raw` + rights classification | Primary rights field |
| `rightsAndReproduction` | `source_record.rights_text` | Secondary rights text |
| `primaryImage` | `media_file.source_url` | Image delivery URL |
| `additionalImages` | Logged; not written to media_file (pilot policy) | See Article 3.5 |
| `tags[].term` | `source_record.subjects` | Subject terms array |
| `tags[].Wikidata_URL` | `source_record.subject_wikidata_urls` | Wikidata entity links for subjects |
| `tags[].AAT_URL` | `source_record.subject_aat_urls` | AAT classification URLs |
| `objectWikidata_URL` | `source_record.object_wikidata_url` | Object-level Wikidata entity link |
| `isHighlight` | `source_record.is_highlight` | Met editorial highlight designation |
| `accessionNumber` | `source_record.accession_number` | Institutional accession ID |
| `metadataDate` | `source_record.metadata_date` | Last metadata update timestamp |
| `repository` | `source_record.repository` | Always "Metropolitan Museum of Art, New York, NY" |

#### 5.1 `anchor_type` Derivation

`source_item.anchor_type` must be derived from department and tags — not hardcoded.
The derivation logic:

```python
BIOLOGICAL_DEPARTMENTS = {"Drawings and Prints"}  # when subject tags include biological taxa
GEOGRAPHIC_DEPARTMENTS = {"Photographs", "Egyptian Art", "Greek and Roman Art", "Islamic Art",
                           "Arts of Africa, Oceania, and the Americas", "Ancient Near East"}
CULTURAL_DEPARTMENTS = {"The Costume Institute", "European Sculpture and Decorative Arts",
                         "Medieval Art", "Arms and Armor", "Musical Instruments"}

def derive_anchor_type(record):
    dept = record.get("department", "")
    tags = [t.get("Wikidata_URL", "") for t in record.get("tags", [])]
    # If any tag Wikidata URL is a biological taxon (Q16521 subclass): biological
    if any_tag_is_biological_taxon(tags):
        return "biological"
    # If country/region field is non-empty: geographic
    if record.get("country") or record.get("region"):
        return "geographic"
    # Department-based fallback
    if dept in BIOLOGICAL_DEPARTMENTS:
        return "biological"
    if dept in GEOGRAPHIC_DEPARTMENTS:
        return "geographic"
    if dept in CULTURAL_DEPARTMENTS:
        return "cultural"
    return "cultural"  # safe default — cultural for unclassified art objects
```

Wikidata taxon detection (`any_tag_is_biological_taxon`) must use the Wikidata QID class
hierarchy lookup, not a string match on the term. This lookup may be cached per session.

#### 5.2 Place Association Protocol

The Met's `country`, `region`, `subregion`, `city`, and `geographyType` fields provide
geographic provenance for the object's origin (not The Met's location). This geographic
provenance is the primary place association signal:

```
country = "Japan" → associate with NC place page for Japan
country = "Egypt" → associate with NC place page for Egypt
geographyType = "Probably from" → use as associated place but flag confidence as "probable"
geographyType = "Made in" → geographic place of manufacture — may differ from cultural origin
```

Geographic provenance is not always present. For objects with no geographic provenance
fields, place association requires subject-tag analysis (`tags[].Wikidata_URL` for
place entities). For objects with neither geographic fields nor place-entity tags, place
association must be deferred — not manufactured from department name.

---

### Article 6 — Pilot Scope

This Decision authorizes a **scoped pilot** for the Asian Art department, focused on
Japan place pages.

**(a) Rationale — Japan geographic gap.** The Coverage Audit (OQ-4) identified Japan
as a top-5 global tourism destination with zero NC source coverage. The Met's Asian Art
department holds the most commercially valuable pre-1900 Japanese woodblock print
collection (ukiyo-e) accessible to NC under CC0. This pilot simultaneously:

1. Opens NC's first Japan place content (Mount Fuji, Edo/Tokyo, coastal Japan)
2. Validates the Met Rights Matrix v1 against real objects in production
3. Exercises the REST cursor enumeration pattern with department scoping
4. Tests the geographic provenance → place association logic with clean `country = "Japan"` data
5. Activates Hokusai and Hiroshige as NC Priority Illustrator candidates — both top-tier
   commercial creators not yet represented in any NC pipeline

**(b) Pilot query scope.** The pilot enumeration query:

```
Primary (Japanese Art — PD):
  GET /search?q=Japan&isPublicDomain=true&departmentId={ASIAN_ART_DEPT_ID}

  Where {ASIAN_ART_DEPT_ID} is confirmed via GET /departments before pilot start.

Supplemental (Drawings and Prints — natural history illustrations):
  GET /search?q=natural+history&isPublicDomain=true&departmentId={DRAWINGS_PRINTS_DEPT_ID}
  maximumRecords: 25 (sub-cap within pilot cap)
```

**(c) Place association target.** All assets ingested under this Decision must be
associated with Japan (`places.geonames_id = 1861060`, Wikidata Q17) or a specific
Japanese place page (Fuji, Edo, Kyoto, etc.) via either:
- `country = "Japan"` in the API response, or
- A subject tag with a Japanese place Wikidata URL

Assets returned by the query that cannot be associated with a Japan place page must
be discarded, not queued for a different place. Place expansion requires DD-MET-002.

**(d) Pilot batch size.** The first ingestion batch is capped at **100 assets**. This
cap is set higher than the Gallica pilot (50 assets) because:
- Rights classification is binary (no bilingual text path, no REVIEW_REQUIRED class)
- The Met's rights architecture is significantly simpler than Gallica's
- No IIIF bridging adapter uncertainty (pending live verification per Article 4.2)
- The ukiyo-e collection is commercially homogeneous — 100 assets provides meaningful
  commercial coverage assessment

**(e) Sub-caps within pilot cap:**

| Source query | Sub-cap | Purpose |
|---|---|---|
| Asian Art, Japan query | 75 assets | Primary pilot |
| Drawings and Prints, natural history query | 25 assets | Supplement; validates non-Japan anchor_type derivation |
| BLOCKED rejections | Not counted | Logged; do not consume cap |

**(f) Drawings and Prints sub-pilot place association.** For the Drawings and Prints
sub-cap (25 assets), place association follows subject-tag analysis since natural history
prints may have European geographic provenance (Netherlands, France, UK) rather than
Japan. The 25-asset sub-cap tests the geographic provenance derivation for European
illustration material. Place association for this sub-cap is not restricted to Japan.
These assets are logged separately from the primary Japan pilot.

---

### Article 7 — Asset Zero Requirements

Asset Zero for The Met must satisfy all of the following requirements.

**(a) Subject requirement.** Asset Zero must be a pre-1900 Japanese woodblock print
depicting a natural history subject from the Asian Art department. Priority subjects:

| Priority | Subject | Commercial rationale |
|---|---|---|
| 1 | Mount Fuji landscape (with birds, waves, or vegetation) | NC's highest-value Japan place association; Hokusai / Hiroshige tier |
| 2 | Bird or fish woodblock print (ukiyo-e) | Natural history + Japan place; biologically annotatable |
| 3 | Flower or botanical woodblock (Four Seasons series, etc.) | Botanical illustration; strong seasonal commerce appeal |
| 4 | Pre-1900 European natural history print (Drawings and Prints dept) | Supplemental; validates alternate department and anchor_type |

**(b) Rights requirement.** Asset Zero must:
- Have `isPublicDomain: true` in the live API response for its specific `objectID`
- Have a non-empty `primaryImage` URL that resolves to a full-resolution image
- Have `objectEndDate ≤ 1900` (pre-1900 creation date, preferably pre-1868 for Edo period)
- Pass HR-MET-1 human review

**(c) Candidate objects.** The following specific Hokusai and Hiroshige works are the
preferred Asset Zero candidates. Exact `objectID` values must be confirmed via live
API query before Gate 4:

| Creator | Work | Expected department | NC commercial tier |
|---|---|---|---|
| Katsushika Hokusai | "The Great Wave off Kanagawa" (*Fugaku Sanjūrokkei*, ca. 1831) | Asian Art | MASTERWORK candidate |
| Katsushika Hokusai | "Fine Wind, Clear Morning" (Red Fuji, *Fugaku Sanjūrokkei*, ca. 1831) | Asian Art | MASTERWORK candidate |
| Utagawa Hiroshige | Any print from "Tōkaidō Gojūsan-tsugi" (Fifty-three Stations of the Tōkaidō, 1833–34) | Asian Art | FLAGSHIP to MASTERWORK |
| Katsushika Hokusai | Fish or bird print from "A Picture Book of Realistic Paintings" or similar | Asian Art | FLAGSHIP |

The "Great Wave" or "Red Fuji" are the ideal Asset Zero candidates. If The Met holds
an example under CC0 (`isPublicDomain: true`), it should be the Asset Zero record.
Multiple Met impressions of these works may exist — select the highest-quality impression
with the best image resolution.

**(d) IIIF and image delivery requirement.** Asset Zero must confirm:
- `primaryImage` URL resolves (HTTP 200) with full-resolution image ≥ 400px shortest side
- If IIIF manifest endpoint is live: IIIF manifest resolves and is valid
- If IIIF manifest endpoint is absent: documented in Asset Zero Report as DD-MET-001-A1
  trigger; `media_file.iiif_manifest_url = null` recorded

**(e) Place association requirement.** Asset Zero must be associated with Japan
(`places.geonames_id = 1861060`) or a specific Japanese place page. Mount Fuji
(`places.geonames_id = 2640981`) is the preferred place for any Hokusai Fuji print.

**(f) Commerce tier expectation.** A Hokusai "Great Wave" or "Red Fuji" impression held
at The Metropolitan Museum under CC0 is NC's highest-value single Asset Zero candidate
across all institutions. It should score at the **MASTERWORK** CSM tier. A FLAGSHIP score
is acceptable for less iconic subjects. If the score falls to PREMIUM or below, the
scoring formula must be reviewed before the pilot proceeds — the expected commercial
tier is a calibration reference.

**(g) Asset Zero is not production.** Asset Zero is a governance validation exercise.
The 100-asset pilot cap begins with the first production ingestion batch, not with
Asset Zero validation.

---

### Article 8 — Success Criteria

The pilot is evaluated at conclusion of the 90-day window or when 100 assets have
been processed — whichever comes first. All nine criteria must be evaluated.

| # | Criterion | Threshold | Constitutional? |
|---|---|---|---|
| SC-1 | Activated assets | ≥ 15 reach `activation_target` with second-human approval | No |
| SC-2 | Rights verification completeness | 100% of `activation_eligible` assets have documented `media_rights.rights_evidence` including `met_is_public_domain: true` | No |
| SC-3 | BLOCKED filter accuracy | Zero non-PD assets in `source_record` for source `'met'` | **Yes — suspend** |
| SC-4 | Place association | ≥ 90% of Asian Art pilot assets associated with a Japan place page | No |
| SC-5 | FM exclusion | Zero FM output connected to any rights determination | **Yes — suspend** |
| SC-6 | Commerce coverage | 100% activated assets have COS + CSM tier in `asset_opportunities` | No |
| SC-7 | Image URL integrity | 100% of `media_file.source_url` values resolve (HTTP 200) with dimension ≥ 400px | No |
| SC-8 | Constitutional integrity | Zero `preservation_event.event_outcome = 'violation'` for `'met'` assets | No |
| SC-9 | Pipeline completion rate | ≥ 85% of ingested assets complete all pre-activation gates without worker error | No |

**SC-3 and SC-5 are constitutional.** Failure on either suspends the pilot immediately
before any other criteria are evaluated.

**SC-3 note.** This criterion has a tighter formulation than the equivalent Gallica
criterion (SC-3 for Gallica was "zero BLOCKED assets in source_record"). For The Met,
the criterion is specifically "zero non-PD assets in source_record" — meaning the
worker's `isPublicDomain` check must function as a perfect filter. Any `source_record`
row for a Met object where `isPublicDomain: false` in the live API response constitutes
SC-3 failure.

**SC-4 note (90% threshold).** A 10% tolerance is provided because some Japanese art
objects may have `country` metadata pointing to a specific Japanese province or city
that does not yet have an NC place page. These objects are not incorrectly classified —
they are correctly associated with Japan but require a new place page that may not
exist. They should not be discarded; they should be queued for place page creation.
The 90% threshold requires that most objects have a live place association at the
pilot's end.

**SC-7 note (image URL integrity).** This criterion is Met-specific. The Met's CDN
(`images.metmuseum.org`) is generally stable, but the `primaryImage` URL in the API
response must be confirmed to be persistent and not a temporary signed URL. If any URLs
resolve at fetch but return 403 at a later verification check, SC-7 must be investigated
before the pilot is declared successful.

---

### Article 9 — Source Registry Authorization

The Metropolitan Museum of Art is not currently registered in the `sources` table.
This Decision authorizes a single **INSERT** creating `source_id = 'met'`. The INSERT
must be executed as a single authorized statement after DD-MET-001 is ratified.

| Amendment | Field | Value |
|---|---|---|
| MET-SR-1 | `source_id` | `'met'` |
| MET-SR-2 | `name` | `'Metropolitan Museum of Art Open Access'` |
| MET-SR-3 | `institution` | `'Metropolitan Museum of Art'` |
| MET-SR-4 | `base_url` | `'https://collectionapi.metmuseum.org'` |
| MET-SR-5 | `fetch_strategy` | `'api'` |
| MET-SR-6 | `auth_type` | `'none'` |
| MET-SR-7 | `priority` | `8` |
| MET-SR-8 | `entity_types` | `ARRAY['image', 'photography', 'illustration', 'map']` |
| MET-SR-9 | `standards` | `ARRAY['met_openaccess_v1']` |
| MET-SR-10 | `governance_state` | `'active'` |
| MET-SR-11 | `operational_status` | `'unavailable'` |
| MET-SR-12 | `status` | `'active'` |
| MET-SR-13 | `config` | See target JSON below |

The `sources.config` target state at INSERT:

```json
{
  "api_base": "https://collectionapi.metmuseum.org/public/collection/v1",
  "objects_endpoint": "/objects",
  "search_endpoint": "/search",
  "departments_endpoint": "/departments",
  "iiif_manifest_base": "https://collectionapi.metmuseum.org/public/collection/v1/iiif",
  "iiif_manifest_pattern": "/iiif/{objectID}/manifest.json",
  "iiif_version": "pending_verification",
  "iiif_manifest_available": null,
  "image_base": "https://images.metmuseum.org/CRDImages",
  "auth_type": "none",
  "enumeration_pattern": "rest_all_ids_then_per_record",
  "identifier_scheme": "met_object_id",
  "rate_limit": {
    "requests_per_second": 5,
    "burst": 10,
    "timeout_seconds": 30
  },
  "rights_strategy": "met_rights_matrix_v1",
  "rights_field": "isPublicDomain",
  "rights_field_type": "boolean",
  "rights_field_secondary": "rightsAndReproduction",
  "block_if_absent": true,
  "source_role": "direct_institution",
  "aggregation_tier": "one_tier",
  "metadata_standard": "met_openaccess_json",
  "phase_1_only": true,
  "pd_authority_tier": 1,
  "completeness_required_fields": [
    "objectID", "isPublicDomain", "primaryImage", "title", "objectDate"
  ],
  "rights_filter": {
    "mode": "pre_ingestion",
    "primary_authority": "met_rights_matrix_v1",
    "allowed_condition": "isPublicDomain == true AND primaryImage != ''",
    "blocked_conditions": [
      "isPublicDomain == false",
      "isPublicDomain == null",
      "primaryImage == ''"
    ],
    "filter_mode": "strict"
  },
  "pilot_config": {
    "departments": ["Asian Art", "Drawings and Prints"],
    "pilot_cap": 100,
    "primary_sub_cap": 75,
    "supplemental_sub_cap": 25,
    "pilot_place_geonames_id": 1861060,
    "pilot_place_name": "Japan"
  },
  "image_policy": {
    "primary_image_field": "primaryImage",
    "additional_images_policy": "log_only",
    "min_dimension_px": 400
  },
  "bulk_export": {
    "repo": "github.com/metmuseum/openaccess",
    "file": "MetObjects.csv",
    "authorized_use": "planning_and_batch_scoping_only",
    "not_authorized_use": "production_record_creation"
  }
}
```

The `iiif_manifest_available` field is set to `null` at INSERT pending live verification
at Gate 3. After IIIF live testing, a Director-authorized UPDATE sets it to `true` or
`false` and updates `iiif_version` and `standards` accordingly.

---

### Article 10 — Standards Constitution Amendments Required

The following amendments are required before or concurrent with the first production
ingestion run:

**SA-7: Metropolitan Museum Open Access Adapter Profile**

This amendment must formally register:
- `met_openaccess_v1` as a governed `source_record.schema_standard` value for the
  direct-URL delivery path (if IIIF manifests are unavailable)
- `met_openaccess_iiif_v1` as a governed schema standard for the IIIF manifest path
  (if IIIF manifests are confirmed available)
- The `isPublicDomain` boolean field as a governed rights attestation instrument for
  The Met (not a URI but equivalent in governance standing to `edm:rights` for
  institutions governed by the Europeana Rights Matrix)
- The Met Rights Matrix v1 as a governed institution-specific rights matrix
- The REST all-IDs enumeration pattern as a governed bulk enumeration approach
  (complementing OAI-PMH already in the Standards Constitution)
- The `met_object_id` identifier scheme as a governed `provider_item_id` format
- The `images.metmuseum.org/CRDImages/` CDN URL pattern as a governed image
  delivery URL format

SA-7 is the Met-specific standards amendment. It does not cover any other institution.

---

### Article 11 — Activation Prerequisites

The following must be complete before the first production ingestion run begins.
No gate may be skipped.

| # | Action | Gate |
|---|---|---|
| 11.1 | DD-MET-001 ratified (Director signature + second-human approval) | Gate 1 |
| 11.2 | Source registry INSERT (MET-SR-1 through MET-SR-13) executed as single authorized statement | Gate 2 |
| 11.3 | Standards Amendment SA-7 ratified | Gate 2 |
| 11.4 | Met API smoke test: `GET /departments` returns valid department list including Asian Art and Drawings and Prints with confirmed `departmentId` values | Gate 3 |
| 11.5 | IIIF manifest live verification: `GET /iiif/{objectID}/manifest.json` tested against ≥ 5 known CC0 objects; result recorded (available / unavailable) | Gate 3 |
| 11.6 | If IIIF manifests unavailable: DD-MET-001-A1 drafted and ratified | Gate 3 |
| 11.7 | Met Rights Matrix v1 worker implementation: `block_if_absent` guard, `isPublicDomain` boolean check, `primaryImage` empty-string check — all present in adapter code | Gate 3 |
| 11.8 | Rate limiting confirmed at ≤ 5 req/s against production Met API endpoints | Gate 3 |
| 11.9 | Human reviewer designated for Met rights review (HR-MET-1 protocol) | Gate 3 |
| 11.10 | FM exclusion confirmed in writing for Met pipeline — no FM system has access to rights workflow | Gate 3 |
| 11.11 | Asset Zero candidate `objectID` confirmed via live API for Hokusai / Hiroshige preferred subject | Gate 4 |
| 11.12 | Asset Zero: `isPublicDomain: true` confirmed in live API response for specific `objectID` | Gate 4 |
| 11.13 | Asset Zero: `primaryImage` URL resolves HTTP 200, image ≥ 400px shortest side | Gate 4 |
| 11.14 | Asset Zero: IIIF manifest result recorded (available or null) | Gate 4 |
| 11.15 | Asset Zero: Japan place association confirmed (`places.geonames_id = 1861060` or Mount Fuji) | Gate 4 |
| 11.16 | Asset Zero: second-human approval of `verified_cc0` terminal rights status | Gate 4 |
| 11.17 | Pilot formally authorized by Director (start date + end date recorded) | Gate 5 |

---

## Part VI — Unique Risk Register

Risks specific to The Met relative to prior activated sources.

| Risk ID | Risk | Severity | Prior DD equivalent | Mitigation |
|---|---|---|---|---|
| **R-1** | No OAI-PMH — REST all-IDs enumeration pattern is unproven in NC pipeline | High | No equivalent (all prior institutions use OAI-PMH) | SA-7 registers the REST pattern; adapter built to this pattern before Gate 3 |
| **R-2** | IIIF manifest availability unconfirmed — `primaryImage` delivery path may be the only option | Medium | Gallica IIIF 2.1 (different version gap; same "bridging required" pattern) | Article 4.2 conditional governance; DD-MET-001-A1 if manifests absent |
| **R-3** | Boolean rights flag creates false confidence — `isPublicDomain: true` on post-1927 objects requires independent PD analysis | Medium | No exact equivalent | HR-MET-1 Rule 4: reviewer must document PD basis for post-1927 `objectEndDate` objects |
| **R-4** | `additionalImages` array inadvertently written to `media_file` in adapter | Medium | No equivalent | Article 3.5 explicit policy; adapter code review at Gate 3 |
| **R-5** | CDN URL (`images.metmuseum.org`) impermanence — URLs may break if Met CDN is restructured | Medium | No equivalent | SC-7 monitors URL integrity; `preservation_event` records CDN URL at ingest time |
| **R-6** | Japan place pages may not exist for all relevant geographic subdivisions (Tokyo, Kyoto, Fuji) | Low-Medium | Europeana pilot place association | SC-4 90% threshold; new place pages created for prominent Japan destinations pre-pilot |
| **R-7** | Full-collection scale (492K PD objects) creates future enumeration cost | Low | No equivalent | Pilot cap (100 assets); full collection enumeration authorized only via DD-MET-002 |
| **R-8** | `anchor_type` derivation complexity — biological taxon detection via Wikidata QID class hierarchy lookup may have performance cost | Low | No equivalent | Cache Wikidata lookups per session; fallback to geographic for objects with country metadata |
| **R-9** | `constituents` array for multi-creator objects requires a first-creator selection policy | Low | No equivalent | Article 5: `artistDisplayName` is the primary; full `constituents` stored in `source_record.creator_array` |
| **R-10** | Metadata currency — CSV export may be used inadvertently for production (not just planning) despite policy | Low | No equivalent | Article 3.1 explicit exclusion; adapter configuration encodes `authorized_use: planning_only` |

---

### Article 12 — Subsequent Decisions

| ID | Trigger | Scope |
|---|---|---|
| **DD-MET-001-A1** | If live IIIF manifest testing at Gate 3 returns unavailable | Amend Article 4 to govern direct-URL delivery without IIIF manifests; update SA-7 scope accordingly |
| **Standards Constitution v1.x** | Gate 2 prerequisite | SA-7: Met Open Access Adapter Profile |
| **DD-MET-002** | Pilot success (SC-1 through SC-9 met) | Met scope expansion: full Asian Art department; Drawings and Prints department at scale; Egypt and Greece place pages; full REST enumeration beyond Japan pilot |
| **DD-MET-003** | When DD-MET-002 is operational | Drawings and Prints full collection; European Paintings natural history subset; Photographs pre-1928 harvest |
| **DD-MET-004** | When Met additionalImages policy is reviewed | Authorize secondary `media_file` rows from `additionalImages`; requires Director Decision per Article 3.5 |

DD-MET-002 is not automatically triggered by pilot success. It requires Director review
of pilot results, Principal Architect recommendation, and a new Decision. Key inputs to
DD-MET-002: SC-4 Japan place association results (how many new place pages were needed);
SC-7 CDN URL integrity at 90 days (stability indicator for at-scale CDN dependency);
and the commercial quality distribution of activated assets (COS scores for ukiyo-e
vs. Drawings and Prints comparison).

DD-MET-002 is expected to be the highest-volume single DD in NC's history. The Met's
Drawings and Prints department alone may yield 20,000–35,000 commercially viable
illustration opportunities. The governance framework for that volume — harvest scheduling,
human review queue management, place association at scale — requires dedicated treatment.

---

## Ratification

This Decision requires:

1. **Director signature** — opengracelabs (the Director)
2. **Second-human approval** — a second person with authority over NC governance decisions

Neither the Director's signature nor the second-human approval has been recorded.
This document is a Draft until both signatures are present.

| Role | Name | Date |
|---|---|---|
| Director | — | — |
| Second Human Approver | — | — |

---

*DD-MET-001 Draft — 2026-06-09*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
