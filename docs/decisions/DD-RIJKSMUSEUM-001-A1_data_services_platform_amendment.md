# DD-RIJKSMUSEUM-001-A1 — Rijksmuseum Data Services Platform Amendment

| Field | Value |
|---|---|
| **Amendment ID** | DD-RIJKSMUSEUM-001-A1 |
| **Amends** | DD-RIJKSMUSEUM-001 — Rijksmuseum Production Activation |
| **Type** | Platform Change — API Governance Rewrite |
| **Status** | Draft — Pending Ratification (with DD-RIJKSMUSEUM-001) |
| **Repository** | opengracelabs/nc |
| **Drafted** | 2026-06-07 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Trigger** | Rijksmuseum Data Services launch — keyless APIs at data.rijksmuseum.nl |
| **Governing Documents** | DD-RIJKSMUSEUM-001 · Europeana Rights Matrix v1.0 · M36 Engineering Spec v2 |

---

## Scope

This amendment replaces Articles 3, 4, 5, 6 (RU-SR-1), 7(b), 9.3, and 10(b) of
DD-RIJKSMUSEUM-001 in their entirety. All other articles remain in force unchanged.

This amendment must be ratified concurrently with DD-RIJKSMUSEUM-001. Neither
document is ratifiable without the other.

---

## Triggering Findings

**A1-F-1 — Data Services is a new platform.**
Rijksmuseum operates a new public platform at `https://data.rijksmuseum.nl` with
two services: a Search API and an OAI-PMH endpoint. Both are accessible without an
API key. TLS certificate issued 2026-02-27; OAI-PMH earliest datestamp 2026-01-13.
This is a distinct platform from the old `www.rijksmuseum.nl/api` infrastructure.

**A1-F-2 — The Search API is a Linked Art collection enumeration, not a search API.**
`GET https://data.rijksmuseum.nl/search/collection` returns an ActivityStreams
`OrderedCollectionPage` conforming to `https://linked.art/ns/v1/search.json`.
It contains 836,132 items. Each item is a bare `{"id": "https://id.rijksmuseum.nl/{id}", "type": "HumanMadeObject"}` — no metadata, no rights, no image fields.
Only `pageToken` is a supported parameter; `q`, `search`, `text`, and all
legacy filter parameters return `{"detail": "Unsupported query parameter: ..."}`.
This API is a **cursor-based full collection enumerator**, not a queryable search
surface. All pilot query strategies based on `q=` parameters are invalid.

**A1-F-3 — `permitDownload` does not exist in the new platform.**
The `permitDownload` field was specific to the old Rijksmuseum Collection API v4
(`www.rijksmuseum.nl/api/{lang}/collection`). It does not appear in the Linked Art
collection API, in OAI-PMH EDM records, or in OAI-PMH DC records from the new
platform. The `permitDownload` rights gate defined in DD-RIJKSMUSEUM-001 Article 3
cannot be implemented against any currently available Rijksmuseum Data Services
surface. DD-RIJKSMUSEUM-001 Article 3 must be replaced.

**A1-F-4 — OAI-PMH EDM exposes `edm:rights`. The Europeana Rights Matrix is directly applicable.**
The new OAI-PMH endpoint at `https://data.rijksmuseum.nl/oai` supports two
metadata formats: `edm` (Europeana Data Model) and `oai_dc` (Dublin Core).
The `ese` format named in DD-RIJKSMUSEUM-001 Article 4.2 is not supported.
EDM records expose `edm:rights` URI. Confirmed on record
`https://id.rijksmuseum.nl/200105955`:
`edm:rights = http://creativecommons.org/publicdomain/mark/1.0/` (PDM).
The Europeana Rights Matrix v1.0 (NC governed document) directly classifies
Rijksmuseum `edm:rights` URIs. OAI-PMH EDM is now the **primary ingest surface**:
it exposes rights natively without any Search API cross-reference.
The constraint in DD-RIJKSMUSEUM-001 Article 10(b) — prohibiting OAI-PMH without
Search API cross-reference — is lifted. OAI-PMH EDM may be used as the pilot
ingest surface.

**A1-F-5 — IIIF delivery is provided by `iiif.micr.io`, not `www.rijksmuseum.nl/api/iiif/`.**
The EDM `edm:object` `WebResource` and `edm:isShownBy` fields in OAI-PMH EDM
records point to `https://iiif.micr.io/{id}/...` — a Rijksmuseum-contracted
third-party IIIF Image API provider. The `svcs:has_service` triple links to the
IIIF Image API service base at `https://iiif.micr.io/{id}`. The IIIF Image API
pattern documented in DD-RIJKSMUSEUM-001 Articles 4.3, 5.2, and RU-SR-1 is
incorrect. No API key is required for `iiif.micr.io`.

**A1-F-6 — OAI-PMH identifier format changed.**
OAI-PMH identifiers are now URI-form: `https://id.rijksmuseum.nl/{numeric_id}`.
The old format `oai:rijksmuseum.nl:SK-A-1505` does not resolve. The `dc:identifier`
field within the EDM record contains the legacy object number (e.g. `NG-888-4`).
`source_identifier` must use the URI form. The legacy object number is stored as
a supplementary field.

---

## Amended Articles

### Amended Article 3 — Rights Authority

*Replaces DD-RIJKSMUSEUM-001 Article 3 in its entirety.*

The Rijksmuseum `edm:rights` URI is the governing rights field for all NC
Rijksmuseum ingestion via OAI-PMH EDM.

**(a)** Rights classification follows the **Europeana Rights Matrix v1.0**
(NC governed document, `docs/governance/europeana_rights_matrix_v1.md`).
That document's ALLOWED, REVIEW REQUIRED, and BLOCKED categories apply verbatim.

**(b) ALLOWED:** `edm:rights` normalises to one of:
- `https://creativecommons.org/publicdomain/zero/1.0/` (CC0) → `rights_status = 'verified_cc0'`
- `https://creativecommons.org/publicdomain/mark/1.0/` (PDM) → `rights_status = 'verified_pd'`
- `https://rightsstatements.org/vocab/NoC-US/1.0/` (NoC-US) → `rights_status = 'verified_pd'`

ALLOWED objects enter the pipeline with `rights_status = 'pending_verification'`.
After human verification: `rights_status` is set to the terminal value above.

**(c) REVIEW REQUIRED:** `edm:rights` normalises to one of:
- `https://rightsstatements.org/vocab/NoC-CR/1.0/` (NoC-CR)
- `https://rightsstatements.org/vocab/NoC-OKLR/1.0/` (NoC-OKLR)
- `https://rightsstatements.org/vocab/NKC/1.0/` (NKC)

REVIEW REQUIRED objects enter the pipeline with `rights_status = 'pending_verification'`
and a `workflow_item` of `capability = 'rights_review'`.

**(d) BLOCKED:** `edm:rights` contains any InC token, CC license (`/licenses/`),
NoC-NC, CNE, or any unknown/absent value that is not ALLOWED or REVIEW REQUIRED.
Pre-ingestion rejection is mandatory. Every rejection must be logged.

**(e)** The FM exclusion (FM Constitution v1.0 Invariant FM-4) applies permanently
to all Rijksmuseum-sourced assets. No FM output may influence any `media_rights`
record for any Rijksmuseum-sourced asset. This invariant is identical to
DD-EUR-001 Article 3(c) and DD-RIJKSMUSEUM-001 Article 3(e).

**(f) Required evidence for ALLOWED objects.**
`media_rights.rights_evidence` must include:

```json
{
  "source": "rijksmuseum",
  "source_record_id": "<uuid>",
  "edm_rights_uri": "<normalized uri>",
  "rights_matrix_classification": "allowed",
  "applying_policy": "europeana_rights_matrix_v1.0",
  "oai_pmh_identifier": "<https://id.rijksmuseum.nl/{id}>",
  "raw_payload_hash": "<hash>",
  "worker_classified_status": "<verified_cc0 or verified_pd>",
  "evidence_status": "pending_human_review"
}
```

`verified_by` and `verified_at` on `media_rights` remain NULL until a human
reviewer sets them. `commercial_reuse_permitted` and `modification_permitted`
remain FALSE until human verification. The worker may not set terminal rights
status.

---

### Amended Article 4 — API Governance

*Replaces DD-RIJKSMUSEUM-001 Article 4 in its entirety.*

Four API surfaces remain authorised. Roles and postures are revised per A1-F-1
through A1-F-5.

#### 4.1 — Linked Art Collection API (Full Collection Enumeration)

```
Endpoint:    https://data.rijksmuseum.nl/search/collection
Auth:        None
Format:      Linked Art JSON-LD (ActivityStreams OrderedCollection)
Context:     https://linked.art/ns/v1/search.json
Pagination:  cursor-based via pageToken parameter only
Total items: 836,132 (as of 2026-06-07)
```

**Authorised use:**
- Full collection enumeration for bulk URI harvest
- Cursor-based pagination through the complete Rijksmuseum collection
- Seed list generation for OAI-PMH record fetch pipeline

**Prohibited:**
- Use as a standalone ingest surface — items contain no metadata, no rights,
  no image fields; each URI must be resolved via OAI-PMH or direct dereference
- Expectation that text search or subject filtering is possible — no query
  parameters are supported other than `pageToken`
- Ingestion of any object whose URI cannot be resolved to an OAI-PMH EDM record

**Renamed from:** "Search API v4" in DD-RIJKSMUSEUM-001 Article 4.1.
The old v4 endpoint `https://www.rijksmuseum.nl/api/{lang}/collection` is
superseded by this service and is no longer authorised for NC use.

#### 4.2 — OAI-PMH with EDM (Pilot: Primary Ingest Surface)

```
Endpoint:    https://data.rijksmuseum.nl/oai
Auth:        None
Formats:     edm  (Europeana Data Model — PRIMARY)
             oai_dc  (Dublin Core — secondary)
Protocol:    OAI-PMH 2.0
Deleted:     persistent (server tracks deleted records)
Harvest:     Full (ListRecords) + incremental (from/until)
```

**Authorised use:**
- Primary ingest surface for the pilot
- Rights determination via `edm:rights` URI (no Search API cross-reference needed)
- Image URL and IIIF service URL discovery via `edm:isShownBy` / `edm:object` / `svcs:has_service`
- Set-based subject filtering for pilot content selection
- Incremental harvest for changed-record detection via `from`/`until` parameters
- `deletedRecord: persistent` — deleted OAI-PMH records must be propagated to
  `source_item.status` via a `preservation_event`

**Metadata format for pilot:** `edm` is mandatory for the pilot. `oai_dc` is
supplementary only.

**Governance rules:**
- `edm:rights` must be present. Records where `edm:rights` is absent are BLOCKED
  per Amended Article 3(d).
- The worker must parse `edm:rights` and apply the Rights Matrix classification
  before creating `source_record`.
- The `svcs:has_service` triple in `edm:object` WebResource is the authoritative
  IIIF Image API service URL.

**Schema standard:** `source_record.schema_standard = 'edm'` for OAI-PMH EDM
records. This is the same value used for Europeana records; provenance is
distinguished by `source_record.institution_id = 'rijksmuseum'`.

**Not supported:** `ese` format. DD-RIJKSMUSEUM-001 Article 4.2 named `ese`
(Europeana Semantic Elements) — this format is not offered by the new endpoint.

**Constraint lifted:** DD-RIJKSMUSEUM-001 Article 10(b) prohibited OAI-PMH
without Search API cross-reference for `permitDownload`. That constraint is
permanently lifted by this amendment. OAI-PMH EDM exposes `edm:rights` natively.

#### 4.3 — IIIF Image API via `iiif.micr.io` (Pilot: Media File Delivery)

```
Service pattern:  https://iiif.micr.io/{iiif_id}
Image pattern:    https://iiif.micr.io/{iiif_id}/full/max/0/default.jpg
Info:             https://iiif.micr.io/{iiif_id}/info.json
Auth:             None
IIIF version:     2.x (Level 2 compliance)
```

**IIIF ID resolution:** The `iiif_id` component is read from the OAI-PMH EDM
record via the `svcs:has_service` triple attached to the `edm:object` WebResource:
```
edm:object → edm:WebResource → svcs:has_service → <https://iiif.micr.io/{iiif_id}>
```
The IIIF ID may not be constructed or guessed from `objectNumber` or any other
field. It must be read from the EDM record.

**Authorised use:**
- `media_file.source_url` = IIIF Image API full-resolution image URL
- `media_file` dimensions via `info.json`
- Full-resolution retrieval for MinIO ingestion

**Governance rules:**
- Only full-resolution delivery is authorised: `/full/max/0/default.jpg`
- `info.json` must be retrieved to populate `width_px` / `height_px` and verify
  the MSC v1.2 Article 29.2(d) 400px minimum on the longest edge
- Objects where the EDM record contains no `svcs:has_service` triple and no
  `edm:isShownBy` field are BLOCKED at pre-ingestion (no image URL)

**Replaces:** DD-RIJKSMUSEUM-001 Article 4.3, which incorrectly documented
`https://www.rijksmuseum.nl/api/iiif/{objectNumber}/...` as the IIIF pattern.

**Note on Standards Constitution:** Article 4.3 posture is unchanged. `iiif` is
authorised in `sources.standards` for the Rijksmuseum source row. SA-4 remains
required for IIIF Presentation API manifests as `schema_standard`.

#### 4.4 — IIIF Content State API (Phase 3: Deferred)

Unchanged from DD-RIJKSMUSEUM-001 Article 4.4.

---

### Amended Article 5 — Metadata Standards Mapping

*Replaces DD-RIJKSMUSEUM-001 Article 5 in its entirety.*

**`source_record.schema_standard`:** `edm` for OAI-PMH EDM records.

The following mapping defines how Rijksmuseum OAI-PMH EDM fields map to NC M36
substrate fields. The mapping is normative. Workers must implement it exactly.
All XML namespaces follow the OAI-PMH EDM RDF record structure confirmed via
live inspection.

#### 5.1 — Mandatory Fields

All 6 fields must be present. A record missing any mandatory field is **BLOCKED**
at pre-ingestion and logged.

| NC field | OAI-PMH EDM source | Notes |
|---|---|---|
| `source_identifier` | OAI-PMH header `<identifier>` | Full URI: `https://id.rijksmuseum.nl/{id}`. Verbatim. |
| `title` | `edm:ProvidedCHO / dc:title` | Use `xml:lang="nl"` if `en` absent |
| `canonical_source_url` | `ore:Aggregation / edm:isShownAt` | Rijksmuseum website URL for the object |
| `representative_media_url` | `ore:Aggregation / edm:isShownBy` | Full image URL on `iiif.micr.io`. BLOCKED if absent. |
| `rights_gate` | `ore:Aggregation / edm:rights` | BLOCKED if absent or BLOCKED-class URI |
| `raw_payload_hash` | SHA-256 of canonical XML | Computed by worker over raw EDM XML |

#### 5.2 — Standard Fields

Populated when present; NULL if absent.

| NC field | OAI-PMH EDM source | Notes |
|---|---|---|
| `legacy_identifier` | `edm:ProvidedCHO / dc:identifier` | Legacy objectNumber (e.g. `NG-888-4`). Store for deduplication. |
| `description` | `edm:ProvidedCHO / dc:description` | Prefer `xml:lang="en"`; fallback `nl` |
| `date` | `edm:ProvidedCHO / dcterms:created` | String; both language values accepted |
| `creator` | `edm:ProvidedCHO / dc:creator` | Text value or URI; extract label if URI |
| `extent` | `edm:ProvidedCHO / dcterms:extent` | Dimensions string (e.g. `height 366 mm x width 290 mm`) |
| `rights_statement_uri` | `ore:Aggregation / edm:rights` | Normalised URI of the rights statement |
| `dc_type` | `edm:ProvidedCHO / dc:type` | URI reference to type concept |
| `technique` | `edm:ProvidedCHO / edmfp:technique` | URI reference(s) to technique concept(s) |
| `medium` | `edm:ProvidedCHO / dcterms:medium` | URI reference to medium concept |
| `subject` | `edm:ProvidedCHO / dc:subject` | URI reference(s) to subject concept(s) |
| `iiif_service_url` | `edm:object → edm:WebResource → svcs:has_service` | `https://iiif.micr.io/{iiif_id}` |
| `data_provider` | Constant: `'Rijksmuseum Amsterdam'` | Not derived from EDM for this source |

#### 5.3 — Subject and Classification Fields

All subject fields in the new EDM schema are URI references into the Rijksmuseum
controlled vocabulary (e.g. `https://id.rijksmuseum.nl/22112539`). The
dereferencing of these URIs to human-readable labels is deferred to Phase 2
worker enhancement. For the pilot, store URIs verbatim in `normalized_payload`.

#### 5.4 — anchor_type Derivation

`anchor_type` derivation from `dc:type` and `edmfp:technique` URI references is
not possible without resolving those URIs to labels. The pilot must defer to the
following fallback rule:

1. If `dc:type` URI dereferences (or resolves via local cache) to a label
   containing: `kaart`, `atlas`, `map`, `globe`
   → `anchor_type = 'geographic'`
2. Else if `dc:type` or `edmfp:technique` URI resolves to a label containing:
   `etching`, `engraving`, `drawing`, `print`, `watercolor`
   AND the OAI-PMH set membership includes a known natural history set
   → `anchor_type = 'biological'`
3. Default: `anchor_type = 'cultural'`

For pilot purposes (OAI-PMH set-based filtering for natural history content —
see Amended Article 7(b)), the expected outcome is `anchor_type = 'biological'`
for all pilot assets. The derivation logic may be overridden by a configuration
parameter that seeds `anchor_type` based on harvest set.

**Replaces:** DD-RIJKSMUSEUM-001 Article 5.4 which referenced `objectTypes[]`
and `classification.iconClasses[]` fields. Those fields do not exist in EDM.

---

### Amended Article 6 — Source Registry Amendment (RU-SR-1 Revised)

*Replaces DD-RIJKSMUSEUM-001 Article 6 RU-SR-1 SQL in its entirety.*
Pre-INSERT verification and post-INSERT verification queries are unchanged.

**Amendment RU-SR-1 (Revised) — Insert Rijksmuseum source record:**

```sql
-- DD-RIJKSMUSEUM-001 Article 6 / A1 — Source Registry Amendment RU-SR-1 (Revised)
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

**Note on `governance_state` / `operational_status` columns:** unchanged from
DD-RIJKSMUSEUM-001 Article 6. Apply Migration 17 first if not already applied.

**Post-INSERT verification (updated):**
```sql
SELECT
    source_id,
    config->>'source_role'                              AS source_role,
    config->>'rights_strategy'                         AS rights_strategy,
    config->>'auth_type'                               AS auth_type,
    config->'rights_filter'->>'authority'              AS rights_authority,
    'edm' = ANY(standards)                             AS edm_in_standards,
    'iiif' = ANY(standards)                            AS iiif_in_standards,
    config->>'auth_key_env' IS NULL
        OR config->>'auth_key_env' = 'null'            AS no_api_key,
    'image' = ANY(entity_types)                        AS image_active
FROM sources
WHERE source_id = 'rijksmuseum';
-- All boolean columns must return true.
-- auth_type must be 'none'.
-- rights_strategy must be 'edm_rights_matrix'.
-- rights_authority must be 'europeana_rights_matrix_v1.0'.
```

---

### Amended Article 7(b) — Pilot Query Strategy

*Replaces DD-RIJKSMUSEUM-001 Article 7(b) only. All other Article 7 clauses unchanged.*

The q-parameter text search approach is not available on the new platform.
The pilot uses **OAI-PMH set-based harvest** targeting collections with high
natural history print and drawing density.

**Pilot harvest parameters:**
```
endpoint    = https://data.rijksmuseum.nl/oai
verb        = ListRecords
metadataPrefix = edm
set         = 261222          (papier/paper collection — prints, drawings)
```

Additional set for expanded coverage if the 100-asset cap is not reached
from `261222` alone:
```
set         = 26112           (Dutch Drawings of the Seventeenth Century)
```

**Pre-ingestion filter (mandatory, applied by worker before source_record creation):**
```
edm:rights present AND classifies as ALLOWED or REVIEW_REQUIRED per Rights Matrix
AND edm:type = IMAGE (edm:ProvidedCHO/edm:type = "IMAGE")
AND svcs:has_service URI present (IIIF service resolvable)
AND dcterms:extent present (physical dimensions available)
```

Objects failing any condition are BLOCKED and logged. They do not count toward
the 100-asset cap.

**Subject filtering for natural history content:**
The pilot relies on set `261222` (papier collectie) having sufficient natural
history content within Dutch Golden Age prints. Explicit subject filtering by
`dc:subject` URI vocabulary is deferred to Phase 2 — URI label resolution is
not available in the pilot worker. The operator reviews the first 20 harvested
records for subject relevance before enabling full harvest.

---

### Amended Article 9 — Gate 9.3 Only

*Replaces DD-RIJKSMUSEUM-001 Article 9, item 9.3 only.*

| # | Action | Gate |
|---|---|---|
| 9.3 | OAI-PMH EDM endpoint accessible and validated: `ListMetadataFormats` returns `edm` format, `GetRecord` returns a well-formed EDM record | Gate 3 |

`RIJKSMUSEUM_API_KEY` is no longer required. Gate 9.3 no longer involves
`.env` configuration.

---

### Amended Article 10(b)

*Replaces DD-RIJKSMUSEUM-001 Article 10(b) in its entirety.*

**(b) ~~OAI-PMH as a standalone ingest surface without Search API cross-reference~~**
**LIFTED by Amendment A1.** OAI-PMH EDM may be used as a standalone pilot
ingest surface. `edm:rights` in EDM records is the governing rights field.
No Search API cross-reference is required.

---

## Answers to Review Questions

**1. Does `RIJKSMUSEUM_API_KEY` remain required?**

No. Neither the new OAI-PMH endpoint nor the Linked Art collection endpoint
require an API key. IIIF delivery via `iiif.micr.io` is also keyless. R-C-1
is CLOSED.

**2. Which articles require amendment?**

| Article | Status |
|---|---|
| Article 3 — Rights Authority | REPLACED: `permitDownload` gate → `edm:rights` matrix |
| Article 4 — API Governance | REPLACED: endpoints, formats, roles, IIIF host |
| Article 5 — Metadata Mapping | REPLACED: v4 JSON fields → EDM OAI-PMH fields |
| Article 6 (RU-SR-1) — SQL | REPLACED: config fields, endpoints, auth_type, rights_strategy |
| Article 7(b) — Pilot query | REPLACED: `q=` query → OAI-PMH set harvest |
| Article 9.3 — Gate | REPLACED: API key gate → OAI-PMH validation gate |
| Article 10(b) — Exclusion | LIFTED: OAI-PMH cross-reference requirement removed |
| Articles 1, 2, 7(a,c-g), 8, 10(a,c-j), 11 | UNCHANGED |

**3. Does RU-SR-1 require amendment?**

Yes. The following fields change:

| Config field | Was | Now |
|---|---|---|
| `base_url` | `https://www.rijksmuseum.nl/api` | `https://data.rijksmuseum.nl` |
| `auth_type` | `'key'` | `'none'` |
| `search_api_endpoint` | old www.rijksmuseum.nl URL | `collection_api_endpoint` → new URL |
| `search_api_version` | `'v4'` | removed — replaced by `collection_api_format` |
| `oai_pmh_endpoint` | old URL with key in path | `https://data.rijksmuseum.nl/oai` |
| `iiif_image_api_pattern` | `www.rijksmuseum.nl/api/iiif/{object_number}` | derived from `svcs:has_service` on `iiif.micr.io` |
| `iiif_manifest_pattern` | old URL | removed — deferred to SA-4 |
| `auth_key_env` | `'RIJKSMUSEUM_API_KEY'` | `null` |
| `rights_strategy` | `'permit_download_gate'` | `'edm_rights_matrix'` |
| `schema_standard` | (absent) | `'edm'` |
| `oai_pmh_formats` | `['oai_dc', 'ese']` | `['edm', 'oai_dc']` |
| `rights_filter.authority` | `'dd_rijksmuseum_001'` | `'europeana_rights_matrix_v1.0'` |
| `rights_filter.rights_field` | (absent, was permitDownload) | `'edm:rights'` |

**4. Does source configuration change?**

Yes. See RU-SR-1 Revised SQL above. Core changes: keyless auth, new endpoints,
EDM rights strategy, `iiif.micr.io` delivery host, `ese` removed, `edm` added.

**5. Does this remove any readiness blockers?**

Yes. R-C-1 is closed. See below.

---

## Blocker Status After A1

### Closed Blockers

| ID | Was | Resolution |
|---|---|---|
| **R-C-1** | `RIJKSMUSEUM_API_KEY` absent from `.env` | CLOSED. No API key required on new platform. Gate 9.3 amended. |

### Remaining Blockers (7 of 8)

| ID | Category | Status |
|---|---|---|
| **R-G-1** | Governance | DD-RIJKSMUSEUM-001 + A1 not ratified. Director + second-human signatures absent. Gate 1. |
| **R-G-2** | Governance | RU-SR-1 (Revised) not applied. Blocked on R-G-1 and R-S-1. |
| **R-G-3** | Governance | FM exclusion for Rijksmuseum pipeline not confirmed in writing. |
| **R-G-4** | Governance | No human reviewer designated for `rights_review` workflow items. |
| **R-S-1** | Schema | Migration 17 not applied — `governance_state` / `operational_status` columns absent from `sources` table. RU-SR-1 INSERT will fail without them. Independent of ratification. |
| **R-I-1** | Implementation | No Rijksmuseum ingestion worker exists. A1 changes the required implementation: OAI-PMH EDM harvest + `edm:rights` classification via Rights Matrix (not `permitDownload` gate). Note: the existing `europeana_adapter/rights.py` `classify_rights()` function is directly reusable for `edm:rights` classification. |
| **R-I-2** | Implementation | Article 5.4 `anchor_type` derivation not implemented. A1 changes the required logic: set-based seeding (not `objectTypes[]`/`iconClasses[]`). Simpler than original — pilot may use `anchor_type = 'biological'` as a set-seeded constant for the natural history sets. |

### Dependency Order (unchanged)

```
Unblocked now:   R-S-1  ·  R-G-1  ·  R-I-1  ·  R-I-2  ·  R-G-3  ·  R-G-4
Blocked on R-G-1 + R-S-1:  R-G-2 (apply RU-SR-1 Revised)
```

R-G-2 remains the last action before the first ingestion run.

---

## Ratification

This amendment must be ratified concurrently with DD-RIJKSMUSEUM-001.
A separate ratification signature block is not required — the DD-RIJKSMUSEUM-001
ratification table covers both documents when both are named.

DD-RIJKSMUSEUM-001 ratification header should be updated to read:

> **Governing Amendments:** DD-RIJKSMUSEUM-001-A1 (included in this ratification)

| Role | Name | Date |
|---|---|---|
| Director | — | — |
| Second Human Approver | — | — |

---

*DD-RIJKSMUSEUM-001-A1 Draft — 2026-06-07*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending concurrent ratification with DD-RIJKSMUSEUM-001*
