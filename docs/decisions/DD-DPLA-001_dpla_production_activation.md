# DD-DPLA-001 — DPLA Production Activation

| Field | Value |
|---|---|
| **Decision ID** | DD-DPLA-001 |
| **Type** | Source Activation (Aggregator-Source) |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-08 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first DPLA governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 |

---

## Background

The Digital Public Library of America (DPLA) is a US-focused discovery aggregator that
surfaces digitized collections from approximately 3,000 contributing institutions via
roughly 30 regional Service Hub intermediaries. DPLA does not hold or digitize its own
content — it aggregates metadata and image references from hubs (state digital libraries,
universities, regional consortia), which in turn aggregate from local contributing
institutions (historical societies, local libraries, archives, museums).

DPLA was explicitly classified as an **Aggregator Reference** in the Institution Coverage
Audit v1.0 (Article 3), placing it in the same governance category as Europeana but
scoped to the US regional institutional landscape. The Audit recommended treating DPLA
as a discovery routing tool rather than a direct content source. This Decision formally
activates DPLA as a production aggregator-source in the NC pipeline — a more limited
role than a direct content institution, but a production-authorized path.

DPLA is not registered in the NC `sources` table as of the date of this Decision.
This Decision authorizes an INSERT (not an UPDATE). No prior governance document has
authorized DPLA ingestion into the NC pipeline.

The DPLA API key has been acquired (stored at `DPLA_API_KEY`). The Bulk Download API
(`https://api.dp.la/v2/items`) has been validated as accessible. No ingestion has
occurred prior to this Decision.

---

## Comparison with Europeana (DD-EUR-001)

DPLA and Europeana share the same governance category (aggregator-source) but differ
across five dimensions that drive materially different governance requirements:

| Dimension | Europeana (DD-EUR-001) | DPLA (this Decision) |
|---|---|---|
| Geographic scope | European institutions | US regional institutions |
| Rights field type | `edm:rights` — URI only | `edm:rights` (URI) and `sourceResource.rights` (URI or free text) |
| Image delivery | IIIF API via contributing institution | External `object` URL (thumbnail) + `isShownAt` (institution page) |
| Quality filter | `completeness` score 1–10 | No completeness equivalent — quality proxy required |
| Aggregation tiers | One (Europeana ← institution) | Two (DPLA ← hub ← institution) |
| Rights assertion reliability | High — Europeana data quality rules | Variable — small institutions apply standards inconsistently |
| API standard | EDM (RDF vocabulary, established) | DPLA MAP v5 (JSON, partially EDM-aligned) |

Each of these differences is addressed in the governing articles below. Unique risks
relative to Europeana are identified in the Unique Risk Register (Part VIII).

---

## Findings

**F-1. DPLA as two-tier aggregator.** DPLA does not aggregate directly from contributing
institutions. It aggregates from Service Hubs (Digital Commonwealth, Mountain West
Digital Library, California Digital Library, SADIN, etc.), which in turn aggregate from
local institutions. This two-tier structure means NC is three steps from the original
rights holder: institution → hub → DPLA → NC. Rights metadata may have been modified or
lost at either aggregation step. This Decision imposes explicit hub provenance capture
requirements to address this risk.

**F-2. Rights field heterogeneity.** The DPLA Metadata Application Profile v5 exposes
rights data via two fields:

- `edm:rights` — a URI from the RightsStatements.org or Creative Commons vocabulary
  (present in many but not all records)
- `sourceResource.rights` — free text, URI, or an array combining both

The Europeana Rights Matrix v1.0 governs URI-form rights statements and applies fully
when `edm:rights` is present as a classified URI. For records where only free-text rights
claims are present in `sourceResource.rights`, the Matrix cannot be applied
deterministically. A separate free-text rights handling rule is required (Article 3).

**F-3. No IIIF delivery.** DPLA does not provide IIIF image delivery. The `object` field
in a DPLA item record contains a URL to a preview or thumbnail image, typically at the
contributing institution's server. Full-resolution images — the minimum NC requires for
print product creation — must be retrieved from the `isShownAt` URL, which links to the
item's page at the contributing institution. That institution may or may not provide
direct image download, and the resolution available varies by institution. An asset
cannot advance to `activation_eligible` until full-resolution access has been confirmed
at the contributing institution. This is a structural difference from Europeana and
Rijksmuseum and creates a non-trivial image resolution verification step in the pipeline.

**F-4. No completeness filter.** Europeana's `completeness` field (1–10) provides a
machine-readable metadata quality floor. DPLA has no equivalent. NC must use proxy
quality signals to filter low-quality records: minimum required fields (`title`,
`dataProvider`, `object`, `sourceResource.date`), image accessibility check, and
contributing institution tier assessment. These proxies are defined in Article 5.

**F-5. DPLA MAP v5 as governing metadata standard.** The DPLA Metadata Application
Profile v5 is the JSON-LD vocabulary governing all DPLA item records. MAP v5 uses EDM
vocabulary partially (`ore:Aggregation`, `edm:WebResource`, `edm:rights`) but wraps
the described object in a non-standard `sourceResource` object rather than `edm:ProvidedCHO`.
The DPLA MAP is not registered in the NC Standards Constitution v1.0. This Decision
calls for Standards Constitution Amendment SA-5 to register `dpla_map_v5` as a Mapped
standard before the first production ingestion run.

**F-6. Potential overlap with Europeana.** Some US institutions that contribute to DPLA
also contribute to Europeana. An asset ingested via Europeana may also be discoverable
via DPLA. Deduplication must be handled at the `source_item.provider_item_id` level.
The DPLA `@id` field is the canonical item identifier for deduplication. When a DPLA item
and a Europeana item share the same contributing institution and object, the source with
the higher-quality image delivery (Europeana/IIIF, when available) is preferred.

**F-7. Commercial positioning for US regional content.** DPLA's primary commercial value
to NC is access to content from US regional institutions that do not have independent API
relationships with NC. State historical societies, local library collections, and regional
archives hold significant pre-1928 photography, illustration, and cartographic material
relevant to US national parks, regional natural heritage, and cultural history. This is
material NC cannot access through LOC, Smithsonian, or Europeana alone.

**F-8. FM exclusion permanent.** No Foundation Model output may influence any rights
determination for any DPLA-sourced asset at any stage. This is FM Constitution v1.0
Invariant FM-4. It cannot be modified by this Decision or any subsequent DD.

---

## Decision

### Article 1 — Production Authorization

DPLA is formally authorized as an active NC production aggregator-source for content
acquisition. This is the first and authoritative governance event for DPLA as a NC
source. No prior authorization exists.

This Decision authorizes an INSERT into the `sources` table creating a new record for
`source_id = 'dpla'` with `governance_state = 'active'`.

The authorization is scoped to the pilot defined in Article 6. Broad DPLA harvest
beyond the pilot scope requires DD-DPLA-002.

---

### Article 2 — Aggregator Designation and Two-Tier Provenance Rule

DPLA is designated as an **aggregator-source** in NC's source taxonomy, specifically
as a **two-tier aggregator**. This designation means:

**(a)** DPLA routes content from Service Hubs, which route from contributing institutions.
DPLA is not a holding institution. NC's classification as an aggregator-source reflects
DPLA's structural role, not a diminishment of its operational importance.

**(b) Hub provenance rule.** For every asset ingested via the DPLA API, `source_record.source
= 'dpla'`. Both the contributing institution (`dataProvider`) and the Service Hub
(`provider`) must be captured in the provenance record. The hub identity is material
to rights reliability assessment — hub-level rights enrichment practices vary by hub.

**(c) Provenance hierarchy.** The canonical provenance chain for a DPLA asset is:

```
Contributing Institution (dataProvider)
  → Service Hub (provider)
    → DPLA (source_id = 'dpla')
      → NC (source_record)
```

This chain must be preserved in `source_record.provenance_chain` (JSON field) for
every ingested DPLA asset. Hub identity is not optional metadata — it is required for
rights reliability assessment.

**(d) Direct institution future path.** When NC later establishes a direct API
relationship with a DPLA contributing institution (e.g., California Digital Library,
Boston Public Library), assets previously ingested via DPLA may be re-evaluated under
the direct source relationship. Deduplication is handled by `source_item.provider_item_id`
matching against the DPLA `@id` field. This Decision does not define the deduplication
resolution rule — it records the future scenario and defers its governance to the
relevant institution's onboarding DD.

---

### Article 3 — Rights Authority and DPLA Rights Strategy

The **Europeana Rights Matrix v1.0** is the governing document for all rights
determinations where a URI-form rights statement is present in a DPLA record.
For records without a classifiable URI, a DPLA-specific freetext handling rule applies.

#### 3.1 URI Path (Primary)

When a DPLA record contains `edm:rights` as a RightsStatements.org or Creative Commons
URI, the Europeana Rights Matrix v1.0 applies without modification:

- **ALLOWED** (CC0, PDM, NoC-US): proceed per Matrix Rules RM-1 through RM-5
- **REVIEW REQUIRED** (NoC-CR, NoC-OKLR, NKC): open workflow item per Matrix Rules HR-1 through HR-2
- **BLOCKED** (all others): reject at pre-ingestion filter; do not create `source_record`

When `edm:rights` is absent but `sourceResource.rights` contains a classifiable URI
as the sole rights value, that URI is treated as equivalent to `edm:rights` for Rights
Matrix application.

#### 3.2 Free-Text Path (Secondary)

When a DPLA record has no `edm:rights` URI and `sourceResource.rights` contains only
free text (no classifiable URI), the following rule applies:

**(a) PD-claim text patterns.** The following free-text patterns are recognized as
**NKC-equivalent** claims and must be handled via the human review workflow (Rule HR-2c
of the Europeana Rights Matrix):

| Free-text pattern (case-insensitive) | NC classification | Review rule |
|---|---|---|
| "public domain" | NKC-equivalent | HR-2c |
| "no known copyright" | NKC-equivalent | HR-2c |
| "no copyright restrictions" | NKC-equivalent | HR-2c |
| "copyright not evaluated" | CNE-equivalent | BLOCKED |
| No rights text present | Absent | BLOCKED |
| Any text not matching above | Unknown | BLOCKED |

**(b)** Free-text PD claims do NOT constitute rights assertions recognized under the
Europeana Rights Matrix. They are treated as unclassified PD claims requiring independent
NC analysis. The asset receives `rights_status = 'pending_verification'` and a
`workflow_item` opened under the NKC review rules.

**(c)** Free-text BLOCKED cases (CNE-equivalent, absent, unknown) are rejected at the
pre-ingestion filter. No `source_record` is created.

**(d)** Free-text PD claims ingested under this rule must carry an additional flag in
`media_rights.rights_evidence`:
```json
{
  "rights_source": "dpla_freetext",
  "original_text": "<exact text from sourceResource.rights>",
  "classification": "nkc_equivalent",
  "review_rule": "HR-2c"
}
```

#### 3.3 DPLA-Specific NoC-US Verification Standard

DPLA contributing institutions — particularly small historical societies and local
libraries — frequently apply the NoC-US rights statement (`http://rightsstatements.org/
vocab/NoC-US/1.0/`) without the rigorous copyright analysis the statement implies.
NC cannot rely on a DPLA contributing institution's NoC-US assertion at the same
confidence level as a major national library's assertion.

For DPLA-sourced assets with NoC-US in the URI path, the human confirmation checklist
(Rights Matrix Rule HR-4) must additionally include:

```json
{
  "dpla_nocus_enhanced_check": true,
  "contributing_institution": "<dataProvider value>",
  "hub": "<provider value>",
  "publication_year_verified": true,
  "publication_year": <year>,
  "pd_basis": "us_publication_before_1928",
  "hub_rights_enrichment_level": "<'curator_reviewed' | 'auto_applied' | 'unknown'>"
}
```

The `hub_rights_enrichment_level` field must be populated based on the contributing hub's
published rights application practices. Hubs known to apply rights via automated
metadata analysis (without curator review) increase verification burden. If this
information cannot be determined for a specific hub, it must be recorded as `'unknown'`
and the review standard applied accordingly.

#### 3.4 FM Exclusion (Permanent)

FM-4 applies permanently to all DPLA rights determinations. No FM output may influence
any `media_rights` record for any DPLA-sourced asset. This is unconditional and cannot
be modified by this Decision or any amendment to it.

---

### Article 4 — DPLA MAP v5 Mapping

The DPLA Metadata Application Profile v5 is adopted as the canonical mapping for all
DPLA `source_record` payloads, pending Standards Constitution Amendment SA-5.

The DPLA MAP three-layer mapping for NC is:

```
ore:Aggregation    →   source_record
sourceResource     →   source_item
object (media URL) →   media_file (stage 1: preview/thumbnail)
isShownAt          →   media_file (stage 2: full-resolution target)
```

Every DPLA ingestion worker must implement this mapping. The `object` field may contain
only a thumbnail — it populates `media_file` at stage 1 with `delivery_tier = 'preview'`.
The full-resolution image, when available at the contributing institution, is required
before any asset can advance to `activation_eligible`.

The field mapping from DPLA MAP v5 to NC `source_record` is:

| DPLA MAP v5 field | NC field | Notes |
|---|---|---|
| `@id` | `source_item.provider_item_id` | Canonical DPLA identifier for deduplication |
| `sourceResource.title` | `source_record.title` | First value if array |
| `sourceResource.creator` | `source_record.creator` | Array; join with "; " |
| `sourceResource.date.displayDate` | `source_record.date_display` | Display string |
| `sourceResource.date.begin` / `.end` | `source_record.date_start` / `date_end` | Parsed year if available |
| `sourceResource.description` | `source_record.description` | First value if array |
| `sourceResource.subject[].name` | `source_record.subjects` | Array |
| `sourceResource.type` | `source_record.media_type_raw` | Normalize to NC media type |
| `sourceResource.format` | `source_record.format_raw` | Store as-is |
| `sourceResource.rights` | `source_record.rights_raw` | Full raw value before classification |
| `edm:rights` | `media_rights.rights_statement_uri` | URI path primary |
| `object` | `media_file.source_url` (preview) | Preview URL; delivery_tier = 'preview' |
| `isShownAt` | `source_record.source_url` | Item page at contributing institution |
| `dataProvider` | `source_record.provenance_chain[0]` | Contributing institution |
| `provider.name` | `source_record.provenance_chain[1]` | Service Hub |
| `hasView[].@id` | `media_file.source_url` (if better resolution) | Alternative image URL |

The `dpla_map_v5` flag in source config (DPLA-SR-6) records this requirement for
worker introspection.

---

### Article 5 — Quality Floor (Completeness Proxy)

DPLA has no `completeness` score. The following minimum fields must be present in a
DPLA item record before a `source_record` may be created. An item record missing any
required field must be rejected at the pre-ingestion stage, not queued for review.

| Field | Required? | Rejection if absent |
|---|---|---|
| `sourceResource.title` (non-empty) | Yes | Reject — no title |
| `dataProvider` (non-empty) | Yes | Reject — no contributing institution |
| `object` (non-null URL) | Yes | Reject — no image reference |
| `edm:rights` OR `sourceResource.rights` (non-null) | Yes | Reject as BLOCKED (absent rights) |
| `sourceResource.date` (any sub-field) | No | Accept with `date_confidence = 'absent'` |

These four required fields are the DPLA quality floor proxy. They do not guarantee
quality — they eliminate the most egregious incomplete records. The completeness floor
may be raised by configuration update without a new DD; it may not be lowered below
the four required fields without a new DD.

---

### Article 6 — Image Resolution Protocol

Because DPLA does not provide IIIF delivery, image resolution must be verified before
any asset can advance to `activation_eligible`.

**(a)** The `object` URL in a DPLA record is treated as a **preview delivery** only.
Its presence satisfies the quality floor (Article 5) but does not satisfy the
MSC v1.2 Article 29.2(d) 400px minimum dimension requirement for activation.

**(b)** Before any asset advances to `activation_eligible`, the ingestion worker must:
1. Retrieve the `isShownAt` URL (item page at contributing institution)
2. Identify and resolve the full-resolution image URL from that page
3. Confirm image dimensions ≥ 400px on the shortest side
4. Record the full-resolution URL in `media_file.source_url` with `delivery_tier = 'full_resolution'`

**(c)** If full-resolution access cannot be confirmed (institution server unreachable,
no direct image URL available, image locked behind registration), the asset must receive
`media_file.delivery_tier = 'preview_only'` and may **not** advance to `activation_eligible`.
It may remain in the pipeline as a `pending_resolution` candidate for 30 days. After
30 days without resolution, the asset must be marked `delivery_status = 'unresolvable'`
and excluded from future activation attempts for that source record.

**(d)** This resolution protocol is not required for quality floor checking — only for
advancement past `rights_verified` to `activation_eligible`.

---

### Article 7 — Source Registry Amendments

DPLA is not currently registered in the `sources` table. This Decision authorizes an
**INSERT** to create a new `sources` record for `source_id = 'dpla'`. The INSERT must
be executed as a single authorized statement.

| Amendment | Field | Value |
|---|---|---|
| DPLA-SR-1 | `source_id` | `'dpla'` |
| DPLA-SR-2 | `name` | `'Digital Public Library of America'` |
| DPLA-SR-3 | `institution` | `'DPLA'` |
| DPLA-SR-4 | `base_url` | `'https://dp.la'` |
| DPLA-SR-5 | `fetch_strategy` | `'api'` |
| DPLA-SR-6 | `auth_type` | `'api_key'` |
| DPLA-SR-7 | `priority` | `6` |
| DPLA-SR-8 | `entity_types` | `ARRAY['image', 'photography', 'map', 'illustration']` |
| DPLA-SR-9 | `standards` | `ARRAY['dc', 'dpla_map_v5']` |
| DPLA-SR-10 | `governance_state` | `'active'` |
| DPLA-SR-11 | `operational_status` | `'unavailable'` |
| DPLA-SR-12 | `status` | `'active'` |
| DPLA-SR-13 | `config` | See target JSON below |

The `sources.config` target state at INSERT:

```json
{
  "api_endpoint": "https://api.dp.la/v2",
  "auth_key_env": "DPLA_API_KEY",
  "rate_limit": {
    "requests_per_second": 2,
    "burst": 5,
    "timeout_seconds": 30
  },
  "rights_strategy": "dpla_rights_matrix_filtered",
  "source_role": "aggregator",
  "aggregation_tier": "two_tier",
  "map_standard": "dpla_map_v5",
  "rights_field_uri": "edm:rights",
  "rights_field_text": "sourceResource.rights",
  "image_delivery": "external_object_url",
  "iiif_available": false,
  "freetext_rights_handling": "nkc_equivalent_review",
  "hub_provenance_capture": true,
  "completeness_proxy_fields": ["sourceResource.title", "dataProvider", "object", "sourceResource.rights"],
  "rights_filter": {
    "mode": "pre_ingestion",
    "authority": "europeana_rights_matrix_v1",
    "uri_path": {
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
      "filter_mode": "strict"
    },
    "freetext_path": {
      "allowed_patterns": ["public domain", "no known copyright", "no copyright restrictions"],
      "treatment": "nkc_equivalent",
      "blocked_patterns": ["copyright not evaluated"],
      "unknown_treatment": "blocked"
    }
  }
}
```

---

### Article 8 — Pilot Scope

This Decision authorizes a **scoped pilot** only. Production ingestion under this Decision
is limited to the following parameters:

**(a) Query scope.** The pilot ingestion query is:

```
endpoint:  https://api.dp.la/v2/items
q:         yosemite
api_key:   $DPLA_API_KEY
rights_uri_filter: CC0 | PDM | NoC-US | NoC-CR | NoC-OKLR | NKC
sort_by:   score
page_size: 100
```

The server-side query uses `q=yosemite` as the full-text search term. Rights filtering
must be applied as a post-retrieval pre-ingestion step, not as a server-side parameter,
because DPLA's API does not support rights statement URI filtering in the same
declarative way as Europeana. The pre-ingestion worker must classify each returned
record against Article 3 of this Decision before any `source_record` is created.

**(b) Place association.** All assets ingested under this Decision must be associated
with Yosemite National Park (`places.geonames_id = 5404921`, Wikidata Q82757). Assets
returned by the Yosemite query that cannot be associated with Yosemite — because they
are unrelated to Yosemite despite appearing in query results — must be discarded at
ingestion, not queued for a different place. Place expansion requires DD-DPLA-002.

**(c) Pilot batch size.** The first ingestion batch is capped at **75 assets**. This
ceiling is lower than the Europeana pilot (100 assets) because of three additional risk
factors: free-text rights heterogeneity, external image resolution uncertainty, and
two-tier provenance ambiguity. The cap may be raised only by DD-DPLA-002.

**(d) Rights path breakdown.** Within the 75-asset cap:
- URI-ALLOWED assets (CC0, PDM, NoC-US): no sub-cap; proceed with standard confirmation
- URI-REVIEW REQUIRED assets (NoC-CR, NoC-OKLR, NKC): sub-capped at 20 of the 75
- Free-text NKC-equivalent assets: sub-capped at 10 of the 75 (exercises freetext path
  without overloading human review queue)

**(e) BLOCKED assets.** BLOCKED assets must be rejected at the pre-ingestion filter.
They do not count against the pilot cap. Every rejection must be logged with the
applicable rejection reason.

**(f) Image resolution verification.** All assets that pass the rights gate and reach
`pending_activation` must complete the image resolution protocol (Article 6) before
advancing. Assets that fail resolution verification are suspended, not discarded — they
remain in the pipeline at `delivery_status = 'pending_resolution'` for up to 30 days.
Suspended assets count against the 75-asset cap only if they reached `source_record`
creation.

---

### Article 9 — Pilot Success Criteria

The pilot is evaluated at the conclusion of the 90-day pilot window or when the first
75 assets have been processed — whichever comes first. Success on all criteria triggers
the DD-DPLA-002 decision process for scope expansion.

| # | Criterion | Threshold | Metric |
|---|---|---|---|
| SC-1 | Activated assets | ≥ 8 assets reach `activation_target` status with second-human approval | `COUNT(activation_targets) WHERE source = 'dpla'` |
| SC-2 | Rights verification completeness | 100% of `activation_eligible` assets have documented rights evidence in `media_rights.rights_evidence` | No `verified_pd` / `verified_cc0` record missing required evidence fields |
| SC-3 | BLOCKED filter accuracy | 100% of BLOCKED-classified assets rejected at pre-ingestion gate | Zero BLOCKED-statement assets in `source_record` table for DPLA source |
| SC-4 | Place association | 100% of activated assets associated with Yosemite (`geonames_id = 5404921`) | No `activation_target` missing `place_id` for DPLA-sourced assets |
| SC-5 | FM exclusion | Zero FM output connected to any rights determination | No `fm_candidate_record` referenced in any `media_rights` or `workflow_item` for DPLA assets |
| SC-6 | Commerce coverage | 100% of activated assets have COS calculated and CSM tier assigned | No `activation_target` without corresponding `asset_opportunities` record |
| SC-7 | Image resolution | ≥ 70% of ingested assets successfully resolve full-resolution image (Article 6) | `COUNT(media_file WHERE delivery_tier = 'full_resolution') / COUNT(source_record WHERE source = 'dpla') ≥ 0.70` |
| SC-8 | Hub provenance capture | 100% of `source_record` rows for DPLA assets have both `dataProvider` and `provider` captured in `provenance_chain` | No `source_record` with `source = 'dpla'` missing provenance_chain hub fields |
| SC-9 | Constitutional integrity | Zero constitutional violations logged | No `preservation_event.event_outcome = 'violation'` for DPLA-sourced assets |
| SC-10 | Pipeline completion rate | ≥ 75% of ingested assets complete rights gate without worker error | Ingestion error rate ≤ 25% (higher allowance than Europeana due to external image delivery risk) |

**SC-7 note (image resolution).** The 70% threshold acknowledges that some contributing
institutions will not provide full-resolution access. Assets below the threshold are not
failures — they indicate the structural resolution limit of DPLA as an aggregator source.
SC-7 failure at < 50% would indicate a systemic problem with the pilot query selection
or the resolution protocol implementation.

**Pilot failure definition (constitutional):** If SC-3 or SC-5 fail, the pilot is
**immediately suspended** pending investigation. BLOCKED asset entry and FM involvement
in rights are constitutional violations, not performance failures. All other criteria
are performance criteria; failure below threshold triggers remediation without suspension.

---

### Article 10 — Explicit Exclusions

This Decision does not authorize:

**(a)** Ingestion of assets with any rights statement classified as BLOCKED under
the Europeana Rights Matrix v1.0, even with human approval. BLOCKED statements remain
BLOCKED. (Ref: Rights Matrix Invariant RM-I-1.)

**(b)** Ingestion of assets from DPLA queries outside the Yosemite scope defined
in Article 8(a). Any non-Yosemite asset — even if PD-eligible — must be discarded
at ingestion. Place expansion requires DD-DPLA-002.

**(c)** Use of the `object` URL as the sole image for print product activation. The
preview/thumbnail image does not meet MSC v1.2 Article 29.2(d) minimum dimensions.
Full-resolution confirmation (Article 6) is mandatory before activation.

**(d)** Ingestion from DPLA's Bulk Download files (`.parquet` format). This Decision
authorizes only the DPLA Items API (`https://api.dp.la/v2/items`). Bulk download
ingestion requires a separate Director Decision.

**(e)** Source registry changes beyond the twelve amendments in Article 7. Any
additional config changes to the `dpla` source record require a separate Director
Decision.

**(f)** Onboarding DPLA contributing institutions or Service Hubs as separate NC
sources. Each hub or contributing institution requires its own institution onboarding
DD per the Institution Factory Constitution v1.0.

**(g)** Ingestion of book, audio, film, 3D, or dataset media types via DPLA.
Phase 1 media types only: image, map, photography, illustration.

**(h)** Retroactive rights clearance. No `source_record` rows exist from DPLA prior
to this Decision; this exclusion is a prospective safeguard.

**(i)** Lowering the completeness proxy floor below the four required fields defined
in Article 5 without a new Director Decision.

**(j)** Use of DPLA's V2 Collections API, DPLA Primary Source Sets API, or any
API surface other than the Items API (`/v2/items`).

---

### Article 11 — Standards Constitution Amendment Required

The DPLA Metadata Application Profile v5 is not registered in the NC Standards
Constitution v1.0. This Decision calls for:

**Standards Amendment SA-5: Add DPLA MAP v5 as Mapped Standard**

- Name: `dpla_map_v5`
- Posture: Map (NC does not adopt MAP v5 as internal model; maps to DC/JSON-LD
  for the governed `source_record` structure per Article 4 field mapping table)
- Required for: DPLA ingestion worker `schema_standard` field
- Governing specification: https://pro.dp.la/hubs/metadata-application-profile

This amendment must be incorporated into a Standards Constitution v1.1 before
`schema_standard = 'dpla_map_v5'` may be used in any `source_record` row.

The amendment does not need to precede the source registry INSERT (Article 7), but
must precede the first production ingestion run.

---

### Article 12 — Required Actions Before First Ingestion Run

The following must be complete before the first production ingestion run begins.

| # | Action | Gate |
|---|---|---|
| 12.1 | DD-DPLA-001 ratified (Director signature + second-human approval) | Gate 1 |
| 12.2 | Source registry INSERT (DPLA-SR-1 through DPLA-SR-13) executed as a single authorized statement | Gate 2 |
| 12.3 | Standards Constitution Amendment SA-5 ratified (`dpla_map_v5` registered) | Gate 2 |
| 12.4 | DPLA ingestion worker implemented: pre-ingestion rights filter (URI path + freetext path per Article 3) | Gate 3 |
| 12.5 | DPLA ingestion worker implemented: image resolution protocol (Article 6) | Gate 3 |
| 12.6 | DPLA ingestion worker implemented: hub provenance capture (Article 2(c)) | Gate 3 |
| 12.7 | At least one human reviewer authorized for `item_type = 'rights_review'` workflow items (DPLA source) | Gate 3 |
| 12.8 | FM exclusion confirmed in writing — no FM system has access to rights workflow | Gate 3 |
| 12.9 | Hub rights enrichment level documented for California Digital Library (primary hub for Yosemite query) | Gate 3 |

No partial completion is acceptable. If any item in 12.1–12.9 is incomplete, the
ingestion run must not begin.

---

## Part VIII — Unique Risk Register

The following risks are specific to DPLA relative to Europeana. Each has a mitigation
defined in the governing articles above.

| Risk ID | Risk Description | Severity | Europeana equivalent? | Mitigation in this DD |
|---|---|---|---|---|
| **R-1** | Free-text rights claims cannot be classified by URI-based Rights Matrix | High | No — Europeana requires `edm:rights` URI | Article 3.2: NKC-equivalent freetext path |
| **R-2** | `object` URL may be thumbnail only; print resolution not available | High | No — Europeana uses IIIF | Article 6: image resolution protocol; SC-7 threshold |
| **R-3** | No completeness score — low-quality records not filtered at API level | Medium | No — Europeana `completeness` ≥ 4 filter | Article 5: four-field quality floor proxy |
| **R-4** | Two-tier aggregation — rights metadata may have been modified by hub | Medium | No — Europeana is one-tier aggregator | Article 2(c): hub provenance capture; SC-8 |
| **R-5** | Small institution NoC-US assertions may not reflect rigorous copyright analysis | High | Partial — Europeana member institutions generally have higher standards | Article 3.3: DPLA-specific NoC-US enhanced check |
| **R-6** | Contributing institution server may be unreliable; images may go 404 | Medium | No — IIIF infrastructure is stable | Article 6(c): 30-day resolution window; `unresolvable` terminal state |
| **R-7** | Hub identity unknown for some records; `provider` field absent or generic | Low-Medium | N/A | Article 2(c): hub provenance required; Article 5: `dataProvider` required field |
| **R-8** | DPLA Bulk Download files may be mistaken for API-authorized ingestion path | Low | N/A | Article 10(d): explicit exclusion of Bulk Download |
| **R-9** | Overlap with Europeana-sourced records from same institution | Low | DD-EUR-001 Article 2(c) handles this | Article 2(d): `@id`-based deduplication against `source_item.provider_item_id` |
| **R-10** | CC BY assets may surface in DPLA from non-PD-declaring institutions | Medium | Yes — Rights Matrix 2F covers this | Europeana Rights Matrix RM-I-1 applies; CC BY is BLOCKED per Table 2F |

---

### Article 13 — Subsequent Decisions

The following Director Decisions are anticipated as consequences of this Decision:

| ID | Trigger | Scope |
|---|---|---|
| **DD-DPLA-002** | Pilot success (all SC-1 through SC-10 met) | DPLA scope expansion beyond Yosemite; pilot cap removal; freetext path expansion |
| **Standards Amendment SA-5** | Required before Gate 2 | DPLA MAP v5 → Standards Constitution v1.1 |
| **DD-CAL-DL-001** | Wave 3+ institution onboarding | California Digital Library as direct content institution |
| **DD-DPLA-003** | If Bulk Download path is needed | Authorization of DPLA Bulk Download ingestion |

DD-DPLA-002 is not automatically triggered by pilot success. It requires a Director
review of pilot results, a Principal Architect recommendation, and a new Decision
document. Image resolution success rate (SC-7) will be a primary input to the DD-DPLA-002
scope decision — if resolution rates are low, bulk DPLA ingestion has limited commercial
value until the contributing institution direct-relationship path is opened.

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

*DD-DPLA-001 Draft — 2026-06-08*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
