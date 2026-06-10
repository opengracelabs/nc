# DD-YALE-001 — Yale Collections Open Access Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-YALE-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-10 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first Yale governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 |

---

## Background

This Decision covers two Yale University art institutions accessed through a single unified
platform: the **Yale Center for British Art (YCBA)** and the **Yale University Art Gallery
(YUAG)**. Both institutions contribute records to **LUX** (`lux.collections.yale.edu`),
Yale's federated Linked Art platform, which serves as the authorised primary ingestion path.

YCBA holds the largest collection of British art outside the United Kingdom: approximately
70,000 open-access images spanning 15th–20th century British painting, prints, drawings,
and watercolors. YUAG is an encyclopedic global collection of 180,000+ digitized objects,
with confirmed open-access images across European Old Masters, American art, and global
material culture. Both institutions are founding members of the IIIF Consortium and deliver
IIIF Presentation API v3 manifests — a new first for NC's pipeline.

Yale presents four governance characteristics that materially differentiate it from all prior
institutions in NC's pipeline:

1. **Dual-institution single-adapter — new institution pattern.** YCBA and YUAG are distinct
   institutions with distinct source slugs, rights statements, commercial-use language, and
   data policies. However, both are accessed via the same LUX API endpoint using the same
   Linked Art 1.0 protocol. DD-YALE-001 is NC's first multi-institution single-adapter
   governance document. A shared LUX adapter must route records to institution-specific
   rights matrices and evidence fields based on the record's source institution.

2. **Linked Art 1.0 / JSON-LD — new protocol class (7th adapter class).** LUX is not a
   REST cursor API, not a CSV bulk download, and not GraphQL. It is a Linked Art 1.0
   JSON-LD platform built on MarkLogic. All records are serialized using the CIDOC-CRM
   ontology via the Linked Art application profile. NC has never processed JSON-LD records.
   **SA-16 (Linked Art Adapter Profile) is required** and blocks Sprint 1.

3. **Linked Art `subject_to` rights — new rights class (7th rights class).** Rights
   information in LUX records is carried in the `subject_to` array using Linked Art's
   rights statement vocabulary. YCBA records carry CC0 1.0; YUAG records carry
   "No Copyright - United States" (RightsStatements.org). Both are NC-allowed but require
   a Yale-specific parsing rule. Neither boolean-object-form, string-equality-form,
   integer-flag-form, nor institution-wide-CC0 patterns apply. **Yale Rights Matrix v1 is
   required.**

4. **IIIF Presentation API v3 — first v3 instance in NC's pipeline.** Prior institutions
   either have no Presentation manifests (NGA) or use v2 (Rijksmuseum, Gallica). YCBA and
   YUAG default to v3 manifests. v2 is available via URL substitution. NC's IIIF handling
   layer must accommodate v3 manifest structures.

**Governing answer to "Can Yale be approved as a production source?":** **Yes — with
qualification.** YCBA is approved unconditionally: the institution states "download and use
for any purpose" with no commercial restriction at any layer. YUAG is approved with a
governance note: the institution's rights-and-reproductions form separates commercial from
scholarly requests, but this process applies only to works not available as open-access
downloads. No commercial prohibition on already-digitized, open-access PD works has been
identified at YUAG. The YCBA Open Data ToS requires attribution ("Data Source: Yale Center
for British Art") — this is a data citation obligation, not a commercial use restriction.
NC's pipeline must store and surface YCBA attribution in rights evidence.

---

## Part I — Source Classification Audit

### I.1 — Yale Center for British Art (YCBA)

**Institution name:** Yale Center for British Art

**Location:** New Haven, Connecticut, United States

**Institution type:** University art museum (Yale University)

**Open access programme:** YCBA Open Access — launched 2016 with initial release of
22,000+ public-domain images; current corpus ~70,000 images. Formal policy: "believed to
be in the public domain and free of other restrictions, you may download and use for any
purpose." Source: `britishart.yale.edu/using-images-works-public-domain`.

**Rights model:** Per-record. Each record carries a rights statement. Confirmed open-access
records carry CC0 1.0 in the Linked Art `subject_to` field.

**Commercial reuse status:** PERMITTED WITHOUT FEE — explicitly. "Any purpose" language
confirmed.

**Attribution requirement:** Yes — data ToS requires "Data Source: Yale Center for British
Art" with link to `britishart.yale.edu`. This is a data citation obligation, not a rights
restriction. NC must store attribution metadata; it does not block commercial image use.

**IIIF support:** Full. Founding IIIF Consortium member. Presentation API v3 (default),
v2 available. Manifests at `https://manifests.collections.yale.edu/ycba/obj/<ID>`.
OAI-PMH endpoint also available (`harvester-bl.britishart.yale.edu/oaicatmuseum/`,
LIDO XML) — secondary path only.

**Collection size:**
- Open-access images: ~70,000
- Prints and drawings: ~55,000 (35,000 prints, 20,000+ drawings/watercolors)
- Primary commercial strength: British topographical prints, natural history illustration,
  18th–19th century British painting

**Proposed institution number:** #14

**Proposed source ID:** `ycba`

**Proposed source priority:** 15

---

### I.2 — Yale University Art Gallery (YUAG)

**Institution name:** Yale University Art Gallery

**Location:** New Haven, Connecticut, United States

**Institution type:** University art museum (Yale University)

**Open access programme:** YUAG Open Access. Formal policy: "no permission required" for
open-access PD works. Per `artgallery.yale.edu/open-access-images`. Rights-and-reproductions
workflow applies only to works requiring custom photography; it does not govern already-
digitized open-access images.

**Rights model:** Per-record. Confirmed open-access records carry "No Copyright - United
States" (`http://rightsstatements.org/vocab/NoC-US/1.0/`) in the Linked Art `subject_to`
field. This is the RightsStatements.org NoC-US statement, not CC0 — an institutional
declaration that a work has no copyright in the United States context.

**Commercial reuse status:** PERMITTED — no prohibition identified for open-access
downloads. Governance note: YUAG's commercial use language is less explicit than YCBA's
"any purpose" statement. Commercial photography orders for non-digitized works go through a
separate paid process; this does not affect open-access digital downloads. The distinction
must be noted in the pilot report and revisited at DD-YALE-002.

**IIIF support:** Full. Founding IIIF Consortium member. Presentation API v3 (default),
v2 available. Manifests at `https://manifests.collections.yale.edu/yuag/obj/<ID>`.

**Collection size:**
- Total online objects: 180,000+
- Prints and drawings: 29,000 prints, 11,000+ drawings
- Open-access image count: not confirmed (no published PD-only count; 154,000 IIIF-
  compliant works includes total digitized objects, not open-access only — Gate 3 item)
- Primary commercial strength: European Old Masters, Dutch/Flemish prints, American art,
  Byzantine / medieval manuscripts

**Proposed institution number:** #15

**Proposed source ID:** `yuag`

**Proposed source priority:** 16

---

### I.3 — LUX Platform

**Platform:** LUX (`lux.collections.yale.edu`) — Yale's unified Linked Art platform

**Backend:** MarkLogic

**Protocol:** Linked Art 1.0 / JSON-LD (CIDOC-CRM application profile). Not REST cursor,
not GraphQL, not CSV bulk download.

**Authentication:** None required for public search and data endpoints.

**Total LUX records:** 41+ million (aggregates across all Yale collections — libraries,
museums, special collections). YCBA and YUAG records are a subset; filtering by
institutional provenance is required.

**NC institution tier (both):** Tier 1 Core — CC0 / NoC-US, direct, no aggregator
intermediary.

---

## Part II — Rights Strategy Audit

### II.1 — Commercial Reuse Qualification

| Layer | YCBA Position | YUAG Position | Compatible? |
|---|---|---|---|
| Copyright | CC0 1.0 per record | NoC-US per record | YES |
| Platform ToS | No commercial fee; "any purpose" | No prohibition for open-access downloads | YES |
| Attribution requirement | "Data Source: Yale Center for British Art" (data ToS) | None identified | YES — metadata obligation, not use restriction |
| Per-asset fee | None | None | YES |
| License agreement | None required | None required | YES |
| Commercial form | N/A | Applies to custom photography orders only, not digital open-access | YES |

**YCBA is approved as a production source unconditionally.** "Any purpose" language
eliminates any ambiguity at the commercial reuse layer.

**YUAG is approved as a production source** — no prohibition on commercial use of
open-access digital images identified. The rights-and-reproductions commercial process
is scoped to works requiring new photography, not to works already available for download.
Governance note: YUAG commercial language is less explicit than YCBA's; this must be
revisited and confirmed at Gate 3 before DD-YALE-002 is drafted.

The conflict that disqualified Gallica (DD-GALLICA-003) — a platform-level license fee for
commercial reuse imposed by BnF's ToS — does not exist at Yale. Neither YCBA nor YUAG
imposes a commercial license fee on PD open-access images.

### II.2 — Can Yale Inherit Prior Rights Matrix Architecture?

**Answer: No.**

Yale's rights determination is structurally distinct from all prior institutions in NC's
pipeline:

1. The rights field is in the Linked Art `subject_to` array — a JSON-LD node, not a flat
   string, boolean, or integer field. Extracting the rights statement requires traversing
   a nested JSON-LD structure.
2. YCBA and YUAG use different rights statement URIs: CC0 1.0 (YCBA) and NoC-US (YUAG).
   A single-value equality check is insufficient; the rights parser must handle both.
3. The record format is JSON-LD with CIDOC-CRM predicates (`subject_to`, `classified_as`,
   `produced_by`, `identified_by`) — alien to all prior adapter architectures.

**Yale Rights Matrix v1 is the seventh distinct rights class in NC's pipeline:**
- URI-form (Europeana, Rijksmuseum): compare `rights` URI to allowlist
- Boolean-object-form (Met, AIC, SMK): `field is True` on object record
- String-equality-form (CMA): `field == "CC0"` on object record
- API-tier-guarantee (Paris Musées): removed/inactive
- Image-record integer-flag-form (NGA): `image_record["openaccess"] == 1`, join required
- Institution-wide CC0 (Walters): no per-record flag; institution-level grant
- **Linked Art `subject_to` form (Yale):** traverse `subject_to` array, extract rights
  statement URI or id, compare to ALLOWED set

### II.3 — Yale Rights Matrix v1 Classification Rules

Rights classification operates on a single Linked Art record (JSON-LD object). The
`subject_to` field is an array of rights assertions; each entry may carry an `id`
(rights statement URI) or `classified_as` (rights type). The authorised extraction
path is `record["subject_to"][N]["id"]` for N in range(len(subject_to)).

**ALLOWED rights statement URIs:**

| Source | Statement | URI |
|---|---|---|
| YCBA | CC0 1.0 Universal | `https://creativecommons.org/publicdomain/zero/1.0/` |
| YUAG | No Copyright — United States | `http://rightsstatements.org/vocab/NoC-US/1.0/` |

**Classification rules (ordered, first match wins):**

| Rule ID | Condition | Outcome | rights_basis |
|---|---|---|---|
| YL-R-1 | `record` is not a dict or is missing `subject_to` | BLOCKED | `missing_subject_to` |
| YL-R-2 | `subject_to` is an empty list | BLOCKED | `no_rights_statement` |
| YL-R-3 | No entry in `subject_to` has an `id` matching the ALLOWED URI set | BLOCKED | `rights_not_allowed` |
| YL-R-4 | `representation` array is empty or absent | BLOCKED | `no_image` |
| YL-R-5 | IIIF manifest URI not derivable from record `id` | BLOCKED | `no_iiif_manifest` |
| YL-R-6 | All prior rules pass; matched URI is CC0 1.0 | ALLOWED | `ycba_cc0` |
| YL-R-7 | All prior rules pass; matched URI is NoC-US | ALLOWED | `yuag_noc_us` |

**ALLOWED outcome:**
- `decision`: ALLOWED
- `rights_statement_uri`: matched URI (CC0 or NoC-US)
- `rights_status`: `"pending_verification"` (CI-4 ceiling)
- `rights_policy_id`: `"yale_rights_matrix_v1"`

**REVIEW_REQUIRED class:** Not applicable in Sprint 1–2. The Linked Art `subject_to`
field either maps to an allowed URI or it does not. A REVIEW_REQUIRED tier may be added
at Gate 3 if records are found carrying CC BY or other REVIEW_REQUIRED statements per
the Europeana Rights Matrix; this requires a standards amendment at that time.

**"Copyright Undetermined" records:** The research identified at least one YCBA record
(George Edwards natural history volume, orbis:11697891) carrying a "Copyright Undetermined"
or similar non-cleared status. These records are BLOCKED by YL-R-3. IFC-1 (PD hard gate)
is unconditionally permanent — no record with unresolved rights may be written.

### II.4 — Rights Evidence Requirements (SC-7)

Additional fields in `media_rights.rights_evidence` for all Yale records:

**YCBA records:**
- `ycba_subject_to_uri` (str) — extracted rights statement URI from `subject_to`
- `ycba_record_id` (str) — verbatim `record["id"]` (LUX URI)
- `ycba_object_id` (str) — numeric object ID extracted from `record["id"]`
- `ycba_iiif_manifest` (str) — derived IIIF manifest URL
- `ycba_attribution` (str) — "Yale Center for British Art" (ToS obligation)

**YUAG records:**
- `yuag_subject_to_uri` (str) — extracted rights statement URI from `subject_to`
- `yuag_record_id` (str) — verbatim `record["id"]` (LUX URI)
- `yuag_object_id` (str) — numeric object ID extracted from `record["id"]`
- `yuag_iiif_manifest` (str) — derived IIIF manifest URL

### II.5 — YCBA Attribution Compliance

The YCBA Open Data ToS (`britishart.yale.edu/open-data-and-data-services-terms-use`)
requires:
> Attribution: "Data Source: Yale Center for British Art" with a link to britishart.yale.edu

This is a data citation obligation, not a restriction on commercial image use. NC's
pipeline must:
- Store `ycba_attribution` in rights evidence for all YCBA records (per II.4)
- Surface attribution in any downstream product pages that display YCBA-origin images
- The ToS does not specify attribution for image use (only data use) — but conservative
  compliance treats image pages as within scope

This obligation does not apply to YUAG records.

### II.6 — Shared Store Extension (Sprint 3 Prerequisite)

`build_rights_evidence` in `shared_media_adapter/store.py` must extend to
`source_slug in {"met", "aic", "cma", "smk", "nga", "walters", "ycba", "yuag"}` before
Yale Sprint 3. SA-9 must be drafted and ratified before Sprint 3. Eight institutions in
this branch without SA-9 is a critical constitutional maintenance liability.

---

## Part III — Data Access Audit

### III.1 — LUX Architecture Overview

LUX serves all Yale collection records through a unified Linked Art 1.0 endpoint. The
ingestion path for YCBA and YUAG is:

```
1. Search LUX for records with institutional provenance in {ycba, yuag}
   — via /api/search/item with institution filter
2. For each result page: fetch full record via /data/object/<uuid>
3. Extract: subject_to (rights), produced_by (creator), identified_by (title/accession),
   timespan (dates), representation (images), subject_of (IIIF manifest link)
4. Classify rights via Yale Rights Matrix v1
5. Derive IIIF manifest URL from numeric object ID
6. Normalize fields to NC substrate
7. Write to M36
```

Alternatively: bulk harvest via IIIF Change Discovery API 1.0 (Yale publishes change
feeds at `lux.collections.yale.edu`). This harvest mechanism is preferred for production
volume — it avoids repeated search pagination and returns Linked Art records directly.
Gate 3 must confirm whether the Change Discovery feed filters by institution or aggregates
all 41M records.

### III.2 — LUX API Endpoints

**Search API base:** `https://lux.collections.yale.edu/api/search/`

**Entity-type endpoint for physical objects:**
```
https://lux.collections.yale.edu/api/search/item
  ?q={"AND":[{"responsibleUnits":{"name":"Yale Center for British Art"}}]}
  &page=1
  &pageLength=20
```

**Individual record:**
```
https://lux.collections.yale.edu/data/object/<uuid>
```

**Pagination:** Page-number (offset-based). Parameters: `page` (1-indexed), `pageLength`
(max confirmed: 20; Gate 3 must confirm max pageLength). No cursor token. Response
includes total count; `num_pages()` derivable from `total / pageLength`.

**Authentication:** None required.

**Python client library:** `luxy` (`github.com/project-lux/luxy`, Apache 2.0) — an
official Yale wrapper for the LUX search API. NC may use this as a reference implementation
but must write its own adapter conforming to NC's adapter interface.

### III.3 — Linked Art 1.0 Field Mapping

Standard Linked Art 1.0 field names as used in LUX records:

| Linked Art Field | Path | NC Field | Transformation |
|---|---|---|---|
| Record URI | `record["id"]` | `source_url` | Raw URI |
| Numeric object ID | Extract from `record["id"]` tail | `record_id` | `str(uuid_tail)` |
| Title | `identified_by[type=Name]["content"]` | `title` | First Name entry |
| Accession number | `identified_by[type=Identifier]["content"]` | `accession_num` | First Identifier |
| Creator | `produced_by.carried_out_by[0]._label` | `creator` | First agent label |
| Creator URI | `produced_by.carried_out_by[0].id` | `creator_lux_uri` | Raw LUX URI |
| Date begin | `produced_by.timespan.begin_of_the_begin` | `date_start` | Integer year |
| Date end | `produced_by.timespan.end_of_the_end` | `date_end` | Integer year |
| Rights URI | `subject_to[N].id` | `rights_statement_uri` | First matched ALLOWED |
| Classification | `classified_as[N].id` (Getty AAT) | `edm_type` | Extract preferred label |
| Geographic subject | `about[type=Place]._label` | `geographic_subjects` | Collect all |
| Image reference | `representation[0].id` | `representative_media_url` | IIIF derivation |
| IIIF manifest | `subject_of[type=LinguisticObject, service=IIIF]` | `iiif_manifest_url` | Derived |
| Institution | `member_of._label` | `source_slug` | Map to ycba or yuag |

**Date fields:** Machine-readable integers (`begin_of_the_begin`, `end_of_the_end`) in
ISO 8601 / integer-year form. Not freetext. Directly usable as `date_start` / `date_end`.

**Geographic subjects:** Encoded under `about` as Place-type objects with `classified_as`
using Getty TGN or GeoNames URIs. Label extraction from `._label` is sufficient for pilot;
URI-based place matching is a Phase 2 enhancement.

**Institution disambiguation:** The `member_of` field or record URI prefix (`/ycba/` vs
`/yuag/`) distinguishes YCBA from YUAG records within a joint LUX search. The adapter
must route each record to the correct rights matrix and evidence schema.

### III.4 — IIIF Manifest URL Derivation

Manifest URLs are directly derivable from the record's numeric object ID without an
additional API call:

```
YCBA:  https://manifests.collections.yale.edu/ycba/obj/<NUMERIC_ID>
YUAG:  https://manifests.collections.yale.edu/yuag/obj/<NUMERIC_ID>
```

The numeric ID is extracted from the record's `id` URI tail (e.g.,
`https://lux.collections.yale.edu/data/object/abc123-...` → numeric ID extracted from
the YCBA/YUAG collections URL or from the `identified_by` accession number pattern).

Gate 3 must confirm the exact extraction rule for numeric ID from LUX record UUID.
Alternative: retrieve manifest URI directly from `subject_of` array in the LUX record
if a IIIF service node is present.

**IIIF version:** v3 by default. v2 available at:
```
https://manifests.collections.yale.edu/v2/ycba/obj/<ID>
https://manifests.collections.yale.edu/v2/yuag/obj/<ID>
```

NC's adapter must request v3 by default. If v3 parsing fails, fall back to v2 with a
logged warning. SA-16 must specify v3-first handling.

### III.5 — Enumeration and Replay Determinism

Enumeration order: sort by numeric object ID ASC within each institution (YCBA then YUAG).
CI-8 requires deterministic enumeration across replay runs. LUX page-number pagination
must be traversed in ascending page order; records within each page must be sorted by
object ID before processing.

The IIIF Change Discovery API bulk harvest path (if confirmed at Gate 3) provides a
chronologically ordered stream of record changes — this must be supplemented with an
initial full-collection seed run sorted by ID ASC before incremental Change Discovery
harvesting begins.

### III.6 — Rate Limits

No numeric rate limit published for LUX API. The YCBA Open Data ToS warns: "excessive
requests may be throttled or blocked." NC convention: 5 req/s, burst 10, with exponential
backoff on 429/503. Gate 3 must confirm whether production-volume LUX requests require
registration or a user-agent agreement with Yale. User-Agent header must identify NC
and include contact email per YCBA ToS.

### III.7 — Campus-Restricted Records

Some IIIF items are restricted to Yale campus network access only. These records will
return a non-200 response for the image URL from outside campus. The adapter must treat
a non-200 IIIF image response as BLOCKED (`no_image_access`) and must not write records
where the representative image is inaccessible. This is Gate 3 item.

---

## Part IV — Image Delivery and IIIF Governance

### IV.1 — IIIF Status

| Component | YCBA | YUAG |
|---|---|---|
| IIIF Image API | Confirmed | Confirmed |
| IIIF Presentation API | v3 default, v2 available | v3 default, v2 available |
| Manifest URL | `manifests.collections.yale.edu/ycba/obj/<ID>` | `manifests.collections.yale.edu/yuag/obj/<ID>` |
| Manifest derivability | Direct from numeric object ID | Direct from numeric object ID |
| Image delivery host | `media.collections.yale.edu` | `media.collections.yale.edu` |
| IIIF Consortium founding member | Yes | Yes |

### IV.2 — IIIF Image URL Construction

Image delivery is via the IIIF Image API. The image service URI is embedded in the
IIIF Presentation manifest's canvas `items[].items[].items[].body.service` node.
Representative image URL standard size:

```
{image_service_base}/full/!1024,1024/0/default.jpg
```

Thumbnail:
```
{image_service_base}/full/!200,200/0/default.jpg
```

Full resolution:
```
{image_service_base}/full/max/0/default.jpg
```

The `image_service_base` is extracted from the manifest, not constructed from the record
ID directly. Gate 3 must confirm the image service URI pattern from live manifest fetches.

**Campus-restriction check:** A HEAD or GET request to the representative image URL must
return HTTP 200 from a non-Yale IP before the record is written. Records returning 401,
403, or 302-to-login are BLOCKED with `no_image_access`.

### IV.3 — IIIF Presentation v3 Structural Notes

IIIF Presentation API v3 differs from v2 in these ways relevant to NC's adapter:
- Canvases contain `items` arrays (not `sequences/canvases`)
- Annotation bodies use `body.type = "Image"` with a IIIF service link
- Metadata is in `metadata` (array of `{label, value}` objects) — same key names but
  values are language maps: `{"en": ["value"]}` not plain strings
- Rights statement is in `rights` (string URI) at the manifest level — may duplicate
  or complement the LUX `subject_to` field

SA-16 must specify v3 manifest parsing. v2 fallback parsing must remain available.

---

## Part V — Commercial Opportunity Assessment

### V.1 — YCBA: British Art and Topography

YCBA holds the world's largest collection of British art outside the UK. For NC's
commercial pipeline:

- **British natural history illustration (18th–19th century):** George Stubbs (animal
  paintings), natural history drawings, botanical works — highest Illustration Opportunity
  value. Note: rights must be confirmed per-record; "Copyright Undetermined" records exist.
- **Topographical prints:** William Daniell's "A Voyage Round Great Britain," William
  Hodges (India), Samuel Atkins (maritime) — anchors British Isles, India, and colonial
  geography place pages. NC has zero South Asia content.
- **British Impressionism and plein air:** Turner watercolors, Constable sketches — fills
  England / landscape place pages
- **Prints corpus:** 35,000 prints spanning 1500–1900 — densest pre-1900 British print
  concentration in NC's pipeline

**Geographic gap coverage:**

| Gap | YCBA Coverage |
|---|---|
| England / Great Britain | **Primary fill** — dedicated to British art |
| India / South Asia | **Partial** — British India topography (Hodges, Daniell) |
| Caribbean / West Africa | **Partial** — British Empire subject matter in prints |
| Natural history (post-Gallica) | **Partial** — British tradition; per-record rights caution |

### V.2 — YUAG: Global Old Masters and American Art

YUAG is encyclopedic in scope. For NC's pipeline:

- **Dutch/Flemish Old Masters:** Rembrandt prints confirmed CC0 (The Windmill 1641,
  Jan Uytenbogaert 1635) — MASTERWORK tier, IIIF confirmed, directly usable as Asset Zero
- **American art:** Titian Ramsay Peale sketchbooks (Long's Rocky Mountain expedition,
  ~1819–20, 200+ natural history sketches) — highest Illustration Opportunity value if
  confirmed open access. Fills Western United States natural history gap.
- **Byzantine / medieval manuscripts:** Byzantine Cross confirmed NoC-US — fills NC's
  illuminated manuscript gap (complementary to Walters)
- **Prints and drawings:** 29,000 prints — supplemental to Rijksmuseum, SMK, NGA

**Geographic gap coverage:**

| Gap | YUAG Coverage |
|---|---|
| Netherlands / Dutch Golden Age | **Supplemental** — distinct Rembrandt objects from Rijksmuseum |
| American West / natural history | **Partial** — Peale sketchbooks pending rights confirm |
| Byzantine / Eastern Mediterranean | **Supplemental** — medieval material culture |

### V.3 — Combined Yale Priority Tier

Yale (YCBA + YUAG) fills three gaps unaddressed by any current NC production source:

1. **British art anchor** — no other NC institution holds British-focused content
2. **South Asian topography** — British India prints (Hodges, Daniell) are unique to YCBA
3. **Dutch Old Masters supplement** — Rembrandt prints at YUAG are distinct objects from
   Rijksmuseum holdings; different physical works with different provenance chains

---

## Decision

### Article 1 — Source Classification and Production Approval

**1.1** The Yale Center for British Art and the Yale University Art Gallery are both
classified as **Tier 1 Core** content institutions for NC's commercial pipeline. Both
pass NC's production-source commercial reuse requirement. See Part II.1.

**1.2** YCBA is assigned institution number **#14**. YUAG is assigned institution number
**#15**. Both are governed by this single Decision document due to their shared LUX
ingestion architecture.

**1.3** YCBA's "any purpose" policy language constitutes the clearest commercial
authorization in NC's pipeline outside NGA's federal-copyright status. No further
rights analysis layer is required for YCBA CC0 records.

**1.4** YUAG's commercial authorization is confirmed for open-access digital images
with the governance note in Part II.1. The rights-and-reproductions commercial process
applies to non-digitized works only and does not restrict open-access downloads.

**1.5** Source identifiers: `ycba` and `yuag`. Permanent once written.

**1.6** Current Institution Factory stage: **Stage 1 (Discovery) complete; Stage 2
(Governance) initiated by this Decision.**

### Article 2 — Yale Rights Matrix v1

**2.1** A single institution-specific rights matrix governs both YCBA and YUAG:
**Yale Rights Matrix v1** (`policy_id: "yale_rights_matrix_v1"`).

**2.2** Yale Rights Matrix v1 introduces a new rights class: **Linked Art `subject_to`
form** (seventh distinct rights class in NC's pipeline). The rights statement is carried
in the `subject_to` array of a Linked Art JSON-LD record. Neither boolean-object-form,
string-equality-form, integer-flag-form, nor institution-wide-CC0 patterns apply.

**2.3** Yale Rights Matrix v1 cannot inherit any prior rights matrix.

**2.4** ALLOWED URIs: CC0 1.0 (`https://creativecommons.org/publicdomain/zero/1.0/`)
for YCBA records; NoC-US (`http://rightsstatements.org/vocab/NoC-US/1.0/`) for YUAG
records. Both are in the ALLOWED set.

**2.5** Classification rules: per Part II.3 (YL-R-1 through YL-R-7).

**2.6** `rights_status` in ALLOWED outcome: `"pending_verification"` (CI-4 ceiling).
`"verified_cc0"` and `"verified_noc_us"` are never written by the worker (FM-4).

**2.7** No REVIEW_REQUIRED class in Sprint 1–2. Addition of a REVIEW_REQUIRED tier
for CC BY / CC BY-SA records requires a subsequent standards amendment.

**2.8** Rights evidence fields per Part II.4 (institution-specific prefixes: `ycba_*`
and `yuag_*`).

**2.9** YCBA attribution compliance: `ycba_attribution: "Yale Center for British Art"`
must be written to all YCBA rights evidence records. This is a constitutional
compliance obligation under the YCBA Open Data ToS.

**2.10** `shared_media_adapter/store.py` remap must extend to
`source_slug in {"met", "aic", "cma", "smk", "nga", "walters", "ycba", "yuag"}` before
Sprint 3. SA-9 must be drafted and ratified as a blocking condition. Eight institutions
in this branch is a critical maintenance liability.

### Article 3 — Ingestion Architecture

**3.1** The authorised primary ingestion path for both YCBA and YUAG is the **LUX Linked
Art API** at `https://lux.collections.yale.edu/api/`. The OAI-PMH endpoint at YCBA is
a confirmed secondary path but must not be used as primary ingestion.

**3.2** The LUX adapter must distinguish YCBA and YUAG records by institutional
provenance (from `member_of`, record URI prefix, or search filter) and route each record
to the correct rights matrix branch and evidence schema.

**3.3** IIIF Change Discovery API bulk harvest is the preferred production-volume path.
Gate 3 must confirm: (a) whether the Change Discovery feed is scoped to YCBA/YUAG or
aggregates all 41M LUX records; (b) the initial seed strategy for first full-collection
ingest. If the feed is not institution-scoped, the search API pagination path is used
for pilot; Change Discovery is deferred to Phase 2.

**3.4** Enumeration order: object ID ASC within institution (YCBA first, then YUAG).
Required for CI-8 replay determinism.

**3.5** User-Agent header: must identify NC software and contact email on all LUX
requests, per YCBA Open Data ToS.

**3.6** `yale_dry_run = True` is the mandatory default in `config.py`. Production
activation requires explicit override and two-human sign-off.

**3.7** Campus-restricted images must be detected via HTTP status check before writing.
Records returning non-200 on the representative image URL are BLOCKED with
`no_image_access`.

### Article 4 — IIIF and Image Delivery Governance

**4.1** IIIF Presentation API v3 at `manifests.collections.yale.edu` is the authorised
manifest source and primary image delivery path for both YCBA and YUAG.

**4.2** Manifest URL derivation: `https://manifests.collections.yale.edu/{source_slug}/obj/{numeric_id}`.
Gate 3 must confirm numeric ID extraction rule from LUX record UUID or `identified_by`.

**4.3** v3-first handling: the adapter requests v3 manifests by default. If a v3 fetch
fails or cannot be parsed, fall back to v2 (`/v2/{source_slug}/obj/{numeric_id}`) with
a logged warning. SA-16 specifies v3 manifest structure and v2 fallback.

**4.4** Image service base URL is extracted from the v3 manifest canvas body service
node. It is not constructed from the record ID. Gate 3 must confirm the image service
URI pattern from live manifest fetches.

**4.5** `representative_media_url`: `{image_service_base}/full/!1024,1024/0/default.jpg`.

**4.6** Campus-restriction check required before writing: HEAD or GET on the
representative image URL must return HTTP 200 from a non-Yale IP.

### Article 5 — Metadata Field Mapping

| Linked Art Path | NC Substrate Field | Transformation |
|---|---|---|
| `record["id"]` | `source_url` | Raw URI |
| Numeric tail of `record["id"]` | `record_id` | `str(numeric_id)` |
| `identified_by[type=Name][0]["content"]` | `title` | Strip |
| `identified_by[type=Identifier][0]["content"]` | `accession_num` | Strip |
| `produced_by.carried_out_by[0]._label` | `creator` | Strip |
| `produced_by.carried_out_by[0].id` | `creator_lux_uri` | Raw LUX URI |
| `produced_by.timespan.begin_of_the_begin` | `date_start` | Integer year |
| `produced_by.timespan.end_of_the_end` | `date_end` | Integer year |
| `subject_to[N].id` (matched ALLOWED) | `rights_statement_uri` | First match in ALLOWED set |
| `classified_as[N]._label` | `edm_type` | First non-AAT-metaType label |
| `about[type=Place][N]._label` | `geographic_subjects` | Collect all Place labels |
| `member_of._label` | `source_slug` | Map label → `ycba` or `yuag` |
| Constructed IIIF manifest URL | `iiif_manifest_url` | Per Article 4.2 |
| Extracted image service base | `representative_media_url` | Per Article 4.5 |
| SHA256(canonical JSON) | `raw_payload_hash` | Sort keys on raw Linked Art record |

**Anchor type derivation rules (ordered, first match wins):**
1. `about` contains a Place-type node with a TGN or GeoNames URI → `"geographic"`
2. Any `classified_as` label matching biological vocabulary (bird, botanical, flower,
   plant, animal, fish, insect, natural history) → `"biological"`
3. `classified_as` or `title` contains "map" → `"geographic"`
4. `about` contains a Place-type node (no URI, label only) → `"geographic"`
5. `creator_lux_uri` non-null (creator has a LUX agent record with place affiliation —
   verify at Gate 3) → `"geographic"`
6. Default → `"cultural"`

### Article 6 — Pilot Scope

**6.1** The Yale pilot is authorised for two concurrent batches: YCBA topographical
prints (British Isles or India) and YUAG Dutch/Flemish Old Masters.

**6.2** Pilot target: **75 assets** total: 40 YCBA + 35 YUAG.

**6.3** YCBA batch (40): British topographical prints, pre-1850. Filter: `classified_as`
= "prints" or "topographical prints"; `date_end < 1850`; rights `subject_to` URI = CC0.
Primary target: William Daniell or William Hodges India material; secondary: British
Isles coastal/landscape views.

**6.4** YUAG batch (35): Dutch/Flemish prints, pre-1700. Filter: `about` includes
Netherlands/Flanders place node or `produced_by.carried_out_by` nationality = Dutch;
`date_end < 1700`; rights `subject_to` URI = NoC-US.

**6.5** Pilot duration: 90 days. Two-human sign-off required for activation.

**6.6** Post-pilot expansion priority: YCBA natural history illustration (British
ornithology, botanical drawings) — requires per-record rights confirmation; "Copyright
Undetermined" records must be excluded until cleared.

### Article 7 — Asset Zero Requirements

**7.1** Asset Zero must satisfy:
- `subject_to` URI in ALLOWED set; Yale Rights Matrix v1 classifies as ALLOWED
- IIIF manifest URL resolves; `representative_media_url` returns HTTP 200 from non-Yale IP
- Pre-1900 subject matter
- MASTERWORK tier preferred (globally recognized work)
- Source confirmed as `ycba` or `yuag`

**7.2** Recommended Asset Zero: **Rembrandt van Rijn, "The Windmill" (1641)**
- YUAG object ID: 2579
- IIIF manifest: `https://manifests.collections.yale.edu/yuag/obj/2579`
- Rights: "No Copyright - United States" — confirmed on YUAG record page
- Date: 1641 — pre-1900, pre-1800
- Image URL: `https://media.collections.yale.edu/thumbnail/yuag/f8d82fbd-0a4e-413a-b992-f7a2d07cbf18`
- Assessment: Confirmed NoC-US, confirmed IIIF v3, confirmed open access. Globally
  recognized MASTERWORK. Strongest confirmed Asset Zero candidate in NC's pipeline.

**7.3** Alternative (YCBA): A confirmed-CC0 William Hodges or William Daniell topographical
print. Specific accession number must be identified at Gate 7 — no confirmed-CC0 natural
history record was identified in research. Thomas Bewick print (tms:51051) is confirmed
CC0 but is a portrait, not illustration-opportunity priority content.

**7.4** Asset Zero checklist:
- [ ] LUX record confirmed accessible via `lux.collections.yale.edu/data/object/<uuid>`
- [ ] `subject_to` URI = NoC-US (YUAG) or CC0 (YCBA) confirmed in LUX record
- [ ] IIIF manifest URL resolves HTTP 200 from non-Yale IP
- [ ] Representative image URL resolves HTTP 200 from non-Yale IP
- [ ] Yale Rights Matrix v1 classifies as ALLOWED (YL-R-1 through YL-R-7)
- [ ] `normalize_record()` produces no mandatory field warnings
- [ ] `write_record()` returns `status: "written"`, `writes: 7`
- [ ] `media_rights.rights_status = "pending_verification"` in DB
- [ ] Institution-specific evidence fields populated (`yuag_*` or `ycba_*`)
- [ ] Two-human sign-off

### Article 8 — Success Criteria

**SC-1 (Asset Zero):** Rembrandt "The Windmill" written with `rights_status =
"pending_verification"`. IIIF image resolves HTTP 200. Two-human sign-off.

**SC-2 (Rights matrix coverage):** Both YL-R-6 (CC0) and YL-R-7 (NoC-US) triggered
at least once across pilot. Zero records written with unresolved rights.

**SC-3 (Pilot volume):** 75 assets written (40 YCBA, 35 YUAG). BLOCKED rate ≤ 10%
(higher allowance than prior institutions due to possible campus-restriction rate).

**SC-4 (FM-4):** Zero violations. Non-waivable.

**SC-5 (No terminal attestation):** Zero `"verified_cc0"` or `"verified_noc_us"` in
`worker_classified_status`.

**SC-6 (Anchor type fidelity):** Correct for ≥ 90% of pilot assets. At least one
geographic (topographical print), one biological if natural history content present.

**SC-7 (Yale evidence completeness):** All YCBA records have `ycba_attribution` populated.
All YUAG records have `yuag_subject_to_uri` populated. Zero exceptions.

**SC-8 (Image access):** `representative_media_url` resolves HTTP 200 from non-Yale IP
for ≥ 90% of written records. Records failing campus-restriction check are BLOCKED, not
written — BLOCKED count logged separately.

**SC-9 (Dual-institution routing):** Zero YCBA records processed with YUAG rights matrix
and vice versa. Institution routing is deterministic and auditable via `source_slug`.

**SC-10 (IIIF v3 parsing):** v3 manifest path taken for ≥ 90% of records. v2 fallback
usage logged. Zero silent manifest parse failures.

**SC-11 (Human review gate):** Two-human sign-off on pilot completion report before
DD-YALE-002.

### Article 9 — Source Registry Authorization

**YCBA:**

| Parameter | Value |
|---|---|
| `source_id` | `ycba` |
| `source_name` | `Yale Center for British Art` |
| `source_type` | `university_museum_open_access` |
| `institution_number` | `14` |
| `priority` | `15` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `yale_rights_matrix_v1` |
| `api_base_url` | `https://lux.collections.yale.edu/api` |
| `manifest_base_url` | `https://manifests.collections.yale.edu/ycba/obj` |
| `schema_standard` | `yale_linked_art_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-YALE-001` |

**YUAG:**

| Parameter | Value |
|---|---|
| `source_id` | `yuag` |
| `source_name` | `Yale University Art Gallery` |
| `source_type` | `university_museum_open_access` |
| `institution_number` | `15` |
| `priority` | `16` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `yale_rights_matrix_v1` |
| `api_base_url` | `https://lux.collections.yale.edu/api` |
| `manifest_base_url` | `https://manifests.collections.yale.edu/yuag/obj` |
| `schema_standard` | `yale_linked_art_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-YALE-001` |

### Article 10 — Standards Amendments

**SA-16 (Required — new protocol class, blocks Sprint 1):** Linked Art Adapter Profile.
Codifies: Linked Art 1.0 JSON-LD parsing, LUX API endpoint patterns, page-number
pagination, field extraction rules for all CIDOC-CRM predicates used in LUX records
(`subject_to`, `identified_by`, `produced_by`, `classified_as`, `about`, `representation`,
`subject_of`, `member_of`), IIIF Presentation API v3 manifest parsing (v3-first with v2
fallback), image service base URL extraction, User-Agent header requirements, campus-
restriction detection, `yale_linked_art_v1` schema standard definition.

**SA-17 (Required — new rights class, blocks Sprint 1):** Yale Rights Matrix v1.
Codifies: Linked Art `subject_to` rights parsing, ALLOWED URI set (CC0 + NoC-US),
YL-R-1 through YL-R-7 classification rules, institution routing (ycba vs yuag),
evidence fields (`ycba_*`, `yuag_*`), YCBA attribution compliance obligation.

**SA-9 (Critical — blocking for Sprint 3):** CC0 Adapter Profile extension. The
`build_rights_evidence` remap must extend to eight source slugs. Eight institutions in
this branch without SA-9 is a constitutional maintenance liability.

### Article 11 — Activation Prerequisites

**Constitutional (CI-class, non-waivable):**
- [ ] SA-16 (Linked Art Adapter Profile) ratified before Sprint 1
- [ ] SA-17 (Yale Rights Matrix v1) ratified before Sprint 1
- [ ] SA-9 ratified before Sprint 3
- [ ] `yale_dry_run = True` default in `config.py`
- [ ] YCBA attribution field present in all YCBA rights evidence records (ToS obligation)

**Gate 3 (must resolve before DD-YALE-002):**
- [ ] YUAG commercial reuse language confirmed for open-access digital downloads
- [ ] Numeric object ID extraction rule from LUX record UUID confirmed
- [ ] Image service base URL pattern confirmed from live manifest fetches
- [ ] Campus-restriction baseline rate measured across pilot candidates
- [ ] LUX production rate limit policy confirmed (registration required or not)
- [ ] IIIF Change Discovery feed scope confirmed (institution-filtered or all-of-LUX)
- [ ] YUAG open-access image count confirmed (CSV/API filter result)
- [ ] `maxpixels` or resolution cap policy confirmed for both institutions

**Sprint prerequisites:**
- [ ] `workers/yale_adapter/config.py` — LUX API base URLs, manifest base URLs, ALLOWED
      rights URIs, rate limits, dry_run, User-Agent string with contact email
- [ ] `workers/yale_adapter/client.py` — Linked Art JSON-LD fetch, page-number pagination,
      institution routing (ycba/yuag disambiguation), campus-restriction check
- [ ] `workers/yale_adapter/rights.py` — Yale Rights Matrix v1 (YL-R-1 through YL-R-7),
      `subject_to` extraction, CC0/NoC-US ALLOWED set
- [ ] `workers/yale_adapter/manifest.py` — IIIF v3 manifest fetch and parsing,
      image service base URL extraction, v2 fallback
- [ ] `workers/yale_adapter/normalize.py` — Linked Art field mapping per Article 5,
      anchor type derivation, YCBA attribution injection
- [ ] `workers/yale_adapter/technical.py` — `yale_linked_art_v1` schema standard
- [ ] `workers/yale_adapter/store.py` — dual-institution routing, `StoreRuntime` with
      `source_slug` in {"ycba", "yuag"}, rights evidence schema selection

### Article 12 — Subsequent Decisions

**DD-YALE-002** (Yale Production Activation): Drafted upon Asset Zero completion, pilot
completion, Gate 3 items resolved, and SC-1 through SC-11 passing. Must address YUAG
commercial use confirmation finding from Gate 3.

---

## Risk Register

| ID | Risk | Probability | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | LUX rate limits not published; adapter hits throttle during pilot | Medium | Medium | 5 req/s default; exponential backoff; Gate 3 rate policy confirmation |
| R-2 | Campus-restricted records block image delivery for NC (non-Yale IP) | High | Medium | SC-8 allows 10% BLOCKED; campus-restriction check before write; Gate 3 baseline measurement |
| R-3 | Numeric object ID extraction from LUX UUID is non-trivial or changes | Medium | High | Gate 3 must confirm extraction rule; alternatively use `subject_of` manifest link directly |
| R-4 | YUAG commercial use prohibition discovered in deeper ToS review | Low | High | Gate 3 commercial use confirmation required before DD-YALE-002; YUAG-only moratorium until confirmed |
| R-5 | IIIF Change Discovery feed covers all 41M LUX records — unusable without institution filter | Medium | High | Gate 3 confirms; search API pagination fallback for pilot regardless |
| R-6 | SA-9 not ratified before Sprint 3 — eight-institution remap branch | High | High | SA-9 must be drafted immediately; treat as Sprint 3 blocking condition |
| R-7 | SA-16 not ratified before Sprint 1 — Linked Art protocol undefined | High | High | SA-16 is Sprint 1 blocker; draft immediately |
| R-8 | YCBA natural history records carry "Copyright Undetermined" at high rate | Medium | Medium | IFC-1 hard gate blocks all undetermined records; pilot uses confirmed-CC0 prints only |
| R-9 | Image service base URL not uniformly derivable from manifest for all records | Medium | Low | Extract from manifest `subject_of` service node; gate on HTTP 200 check |
| R-10 | IIIF v3 parsing fails for edge-case canvas structures | Low | Low | v2 fallback available; logged warning path in SA-16 |
| R-11 | LUX institution disambiguation fails for records with ambiguous `member_of` | Low | Medium | Gate 3: confirm disambiguation rule; reject records with ambiguous institution |
| R-12 | Priority natural history illustrators (Audubon, Gould) not in YCBA/YUAG holdings | Certain | Info | Yale fills British art gap; Audubon/Gould require separate institution (NHM London, Trove) |

---

## Ratification

This Decision is in Draft status. Requires Director sign-off (`opengracelabs`) and
second-human approval. Both parties must review:

- **Part II.1** (Commercial Reuse Qualification — the production approval finding,
  including the YUAG governance note)
- **II.5** (YCBA attribution compliance obligation)
- **Article 3.7** (campus-restriction detection as a blocking condition)
- **Article 10** (SA-16 and SA-17 as Sprint 1 blockers; SA-9 as Sprint 3 blocker)
- **Article 11** (Gate 3 items, especially YUAG commercial use confirmation)

Upon ratification: SA-16 must be drafted immediately (blocks Sprint 1); SA-17 may be
drafted concurrently; SA-9 must be drafted and ratified before Sprint 3 begins.

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
