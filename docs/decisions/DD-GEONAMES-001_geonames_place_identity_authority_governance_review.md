# DD-GEONAMES-001: GeoNames — Place Identity Authority Governance Review

| Field | Value |
|---|---|
| Document | DD-GEONAMES-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Institution Number | **Not Assigned** — Place Identity Authority; not a content institution |
| Decision | APPROVED WITH CONDITIONS |
| Conditions | SA-GEONAMES-001 (CC BY 4.0 attribution standard) required before place pages are published at scale |
| Prior Rulings | Standards Constitution v1.0 Article 17 · Invariant S-3 · IFC v1 Article 1.2 · DD-WIKIDATA-001 Article 11 (2026-06-11) |

---

## I. Institution Overview

**GeoNames**
- Operator: GeoNames.org (Marc Wick; registered Switzerland)
- URL: https://www.geonames.org
- Governance: Open-data geographic names database, community-contributed with editorial curation
- Core product: Global gazetteer — 12M+ geographic features with names, coordinates, feature classification, administrative hierarchy, alternate names in 300+ languages

GeoNames is the world's foremost open geographic names database. It assigns stable integer identifiers to geographic features and provides: canonical feature code (fcode), feature class (fclass), country code, administrative hierarchy (admin1–admin4), authoritative coordinates (WGS 84), population figures for populated places, and multilingual alternate names.

GeoNames does not hold illustrations, photographs, artworks, maps, or any media in the NC commercial sense. GeoNames is a geographic metadata database.

---

## II. Governance Classification — Ruling

### II.1 Prior Classification (Standards Constitution v1.0)

Standards Constitution v1.0 Article 17 already classifies GeoNames under the **"Adopt"** posture:

> "GeoNames is the authoritative geographic names database. NC adopts GeoNames as the place identity authority. Every NC place maps to a GeoNames ID."

Invariant **S-3** makes this constitutional:

> "No NC place entity exists without a GeoNames ID. A place without a GeoNames ID is a candidate, not a canonical place record. NC does not invent geographic identifiers."

This DD does not alter the "Adopt" posture. It formalizes GeoNames' classification beyond a posture ruling into a full governance designation, addresses the CC BY 4.0 licensing obligations that Article 17 does not fully analyze, and defines the evidence role that GeoNames plays in NC's scoring layer.

### II.2 The Three Options

**Option 1 — Place Identity Authority only.** GeoNames as a pure identity system — stable integer identifiers that anchor NC place entities to a global canonical reference. S-3 is the operative rule. GeoNames data is consumed but not treated as evidence; it simply anchors. Governed by Standards Constitution v1.0 Article 17.

**Option 2 — Place Identity and Evidence Authority.** GeoNames as both the identity anchor system and an active evidence source. Population figures feed the Tourism Attraction Score; feature codes determine place type routing in the CI Constitution; alternate names power multilingual search. These are scored and routed inputs — they constitute evidence in the governance sense, even though they live in the `places` table directly rather than in advisory evidence payloads.

**Option 3 — Content Institution.** GeoNames as a source of maps, satellite imagery, or geographic media for the illustration commerce pipeline.

### II.3 Option 3 (Content Institution): REJECTED

Two disqualifiers:

**Disqualifier 1 — No content.** GeoNames is a gazetteer. It holds geographic names, coordinates, administrative hierarchy, and feature codes. It does not hold illustrations, photographs, cartographic images, or any media in the NC commercial sense. There is nothing to ingest as illustration commerce inventory.

**Disqualifier 2 — IFC v1 Article 1.2.** Institution Factory Constitution v1 Article 1.2 explicitly enumerates GeoNames alongside Wikidata, Europeana, and DPLA as systems **not governed by the Institution Factory**:

> "Identity and Reference Authorities (GeoNames, OSM, Wikidata, GBIF) — governed by Standards Constitution v1.0"

This exclusion is constitutional. Reclassifying GeoNames as a content institution requires a constitutional amendment to IFC v1, not a Director Decision alone.

### II.4 Option 1 (Identity Authority only): INSUFFICIENT

Standards Constitution v1.0 Article 17 establishes GeoNames as identity authority. But GeoNames contributes more than stable identifiers:

- `places.population` (GeoNames source) is an input to the Tourism Attraction Score — a governing CI Constitution scoring signal
- `places.feature_code` and `places.feature_class` (GeoNames source) determine which anchor-type routing formula applies in the CI Constitution
- `places.alternate_names` (GeoNames source) governs multilingual place search and discovery — a scored discoverability signal

These are active commercial intelligence inputs, not passive identity fixtures. An "Identity Authority only" classification would leave their governance unaddressed. The CC BY 4.0 attribution obligation also applies to this data whether it is characterized as identity or evidence — a licensing analysis is required either way.

### II.5 Option 2 (Place Identity and Evidence Authority): RATIFIED

**GeoNames is ratified as a Place Identity and Evidence Authority.**

This dual classification acknowledges:
1. **Identity role** — GeoNames IDs are the constitutional anchor for NC place entities (S-3); they are not advisory
2. **Evidence role** — GeoNames geographic metadata (population, feature_code, alternate_names, coordinates) feeds NC's commercial scoring and routing layer

The classification parallels DD-GBIF-001 (biological domain) and DD-WIKIDATA-001 (universal entity domain). GeoNames occupies the place domain with equivalent authority depth.

---

## III. Licensing Model

### III.1 The GeoNames License: CC BY 4.0

GeoNames publishes its database under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. This is the sole governing license for all GeoNames data products used by NC.

CC BY 4.0 is materially different from CC0:
- **CC0**: No conditions. No attribution required. No commercial restrictions.
- **CC BY 4.0**: Attribution required. Commercial use permitted. Share-alike not required. No NonCommercial restriction.

GeoNames CC BY 4.0 is the **only attribution-requiring license** among NC's three Identity and Evidence Authorities. GBIF Backbone Taxonomy is CC0; Wikidata is CC0. GeoNames is CC BY 4.0.

### III.2 GeoNames Data Products by License

| Data product | License | NC use permitted? | Attribution required? |
|---|---|---|---|
| GeoNames main database (geonames dump) | CC BY 4.0 | Yes | Yes |
| GeoNames alternate names | CC BY 4.0 | Yes | Yes |
| GeoNames feature codes / country info | CC BY 4.0 | Yes | Yes |
| GeoNames admin hierarchy tables | CC BY 4.0 | Yes | Yes |
| GeoNames time zone table | CC BY 4.0 | Yes | Yes |
| GeoNames webservice API responses | CC BY 4.0 (same data) | Yes | Yes |
| GeoNames website UI content | GeoNames TOU | Not stored by NC |

### III.3 Copyright Analysis — Facts vs. Database

A GeoNames record asserts facts about the real world: feature X has name Y, is located at coordinates Z, and belongs to administrative division W. Geographic facts are not copyrightable under the applicable copyright statutes of NC's operating jurisdictions (US, EU).

However, GeoNames' **compiled database** — the selection, arrangement, and coordination of 12M+ geographic records — may attract database protection under EU Directive 96/9/EC (sui generis database rights) and equivalent protections in other jurisdictions. The CC BY 4.0 license governs NC's access to the database as a whole.

**Practical consequence:** NC's use of individual GeoNames records (one geonames_id, one set of fields) is unlikely to constitute extraction of a substantial part of the database under EU law. But NC's bulk download of GeoNames for initial place catalog seeding (thousands of records) likely does constitute extraction of a substantial part — triggering CC BY 4.0 attribution obligation.

**Conservative position:** NC treats all GeoNames data — including individual record lookups via API — as subject to CC BY 4.0 attribution. This is the safer and correct compliance posture. It is also the posture most consistent with NC's provenance doctrine, which requires provenance on every row regardless of copyright exposure.

### III.4 No Rights Matrix Required

GeoNames is not a content source. No Rights Matrix governs commercial inventory decisions based on GeoNames data. The CC BY 4.0 obligation is an attribution governance matter, not a per-record rights clearance matter. A **GeoNames Attribution Standard** (part of SA-GEONAMES-001) governs the attribution obligation.

---

## IV. Attribution Requirements

### IV.1 What GeoNames Requires

CC BY 4.0 requires attribution when NC distributes or publicly performs the licensed material. For NC's uses:

| NC surface | GeoNames data present | Attribution required? |
|---|---|---|
| Internal pipeline (workers, M36 store) | geonames_id, feature_code, coordinates | No — internal processing, not distribution |
| API responses (`GET /api/v1/places/{id}`) | place data including geonames_id | Yes |
| Public place pages (web UI) | place name, coordinates, alternate names | Yes |
| IIIF manifests | place metadata | Yes |
| JSON-LD structured data | place geographic data | Yes |
| Exported CSV / bulk data products | place records | Yes |
| Partner API responses | place data | Yes |

### IV.2 Attribution Format

CC BY 4.0 requires "reasonable" attribution — sufficient to allow recipients to identify GeoNames as the source. NC's governed attribution format:

**Short form (UI, page footers, metadata fields):**
```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
```

**JSON-LD / API attribution (in place entity responses):**
```json
{
  "nc:geonames_attribution": {
    "name": "GeoNames",
    "url": "https://www.geonames.org",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "geonames_id": 12345
  }
}
```

**IIIF manifest `requiredStatement`:**
```json
{
  "requiredStatement": {
    "label": { "en": ["Data Source"] },
    "value": { "en": ["Geographic data © GeoNames (geonames.org) — CC BY 4.0"] }
  }
}
```

### IV.3 Attribution Conditions

**GN-ATT-1 — Public-facing attribution required.** Any NC page, API response, or data product that includes GeoNames-sourced data must carry GeoNames attribution in the governed format above.

**GN-ATT-2 — Internal attribution not required.** Attribution is not required in internal pipeline records, worker logs, or M36 internal state. Attribution is a distribution-time obligation.

**GN-ATT-3 — Attribution must survive downstream.** If NC makes its place data available to partners or aggregators, the attribution requirement must be passed downstream in licensing terms or included directly in the data export.

**GN-ATT-4 — Attribution does not affect rights determination.** GeoNames CC BY 4.0 attribution is owed for geographic metadata. It is not rights clearance for NC commercial inventory. No GeoNames attribution statement constitutes evidence of commercial rights for an illustration asset.

---

## V. Commercial-Use Compatibility

### V.1 Ruling: Compatible with NC Commercial Operations

CC BY 4.0 explicitly permits commercial use. There is no NonCommercial restriction on GeoNames data. NC may use GeoNames data in:
- Commercial place pages (with attribution)
- Commercial API products (with attribution)
- Commercial partner licensing (with attribution passed downstream)
- Commercial print products that include place metadata (with attribution in materials)

**GeoNames is commercially compatible.** This distinguishes it from:
- Gallica/BnF: ToS prohibits commercial reuse without fee (DD-GALLICA-003 — DISQUALIFIED)
- GBIF CC BY-NC datasets: NonCommercial restriction prohibits commercial scoring use
- NHM Library/Archives: Non-Commercial Government Licence (DD-NHM-001 — CONDITIONAL, excluded from pilot)

### V.2 Attribution as the Only Condition

The single compliance requirement for commercial use is attribution (§IV). Attribution is a defined, governable obligation — not a structural blocker. SA-GEONAMES-001 codifies the attribution standard as NC's compliance mechanism.

### V.3 No Fee, No Registration, No Endorsement Restriction

GeoNames imposes:
- No license fee for commercial use
- No registration requirement for commercial products
- No endorsement restriction (GeoNames does not operate as a governmental or quasi-governmental body requiring nonendorsement language)

This is a cleaner commercial position than NOAA (nonendorsement policy) and cleaner than any content institution with a ToS. GeoNames is structurally compatible with NC's commercial pipeline.

---

## VI. Place Identity Role

### VI.1 Constitutional Foundation (S-3)

Standards Constitution v1.0 Invariant S-3 is the governing rule:

> "No NC place entity exists without a GeoNames ID. A place without a GeoNames ID is a candidate, not a canonical place record. NC does not invent geographic identifiers."

This is unconditional. It cannot be overridden by a Director Decision. Changing it requires a Standards Constitution amendment.

**Consequence:** GeoNames is not advisory for place identity. It is the identity system. A place's `geonames_id` is as load-bearing as a `source_item.uuid` — it is the stable, external anchor that links NC's internal record to a globally recognized geographic feature.

### VI.2 Canonical Place Data Fields

The following fields in `places` are GeoNames-sourced and governed as identity and evidence data:

| Field | GeoNames source | Type | Role |
|---|---|---|---|
| `geonames_id` | `geonameId` | integer | Primary identity anchor. Required. Invariant S-3. |
| `feature_code` | `fcode` | string | Place type classification. Routing and scoring input. |
| `feature_class` | `fclass` | string (A/H/L/P/R/S/T/U/V) | Broad feature class. Routing input. |
| `country_code` | `countryCode` | string (ISO 3166-1 alpha-2) | Country identity. Required. |
| `admin1_code` | `adminCode1` | string | Province / state. |
| `admin2_code` | `adminCode2` | string | County / district. |
| `geom` | `lat`, `lng` | PostGIS POINT (SRID 4326) | Authoritative coordinates. |
| `population` | `population` | integer | Populated-place population. TAS scoring input. |
| `alternate_names` | `alternateNames` | JSONB array | Multilingual names. Search and discovery input. |

**Fields explicitly not stored from GeoNames:**
- Raw hierarchy chains (resolved into admin1/admin2; hierarchy tables are not mirrored)
- Individual altname record IDs (ephemeral; not load-bearing)
- Timezone data (not a current NC use case)
- Wikipedia title crosslink (Wikidata is the crosswalk hub for this — DD-WIKIDATA-001 §V.2)
- Any GeoNames field not enumerated above without a Standards Constitution amendment

### VI.3 Feature Code Governance

GeoNames feature codes are the canonical vocabulary for NC place type classification. They govern two distinct functions:

**Function 1 — Place page routing.** The Wireframe Constitution identifies place types (national park, city, reef, island, mountain) that correspond to specific GeoNames fcodes. A place's fcode determines which Wireframe page template it receives. This is a constitutional dependency.

**Function 2 — CI Constitution scoring formula selection.** The CI Constitution governs different scoring formulas for different place types. Feature code is the input to formula selection for geographic-anchor illustration opportunities. Changing how feature codes are stored or sourced is a CI Constitution change, not just a data change.

Feature codes are not editable by NC staff without a Director Decision that justifies the override and documents the GeoNames departure.

### VI.4 Place Candidate Resolution Protocol

When a new place is required (from a new institution's pilot, from a taxon discovery result, from a collection), the resolution protocol is:

1. Identify the place by name / approximate coordinates
2. Query GeoNames API: `GET /searchJSON?q={name}&maxRows=5&style=full`
3. Select the GeoNames match with the correct feature code and administrative context
4. If no GeoNames match exists: the place remains a **candidate** and cannot enter the canonical `places` table
5. If GeoNames match exists: create `places` record with GeoNames fields, assign `geonames_id`, then resolve `wikidata_qid` via Wikidata (DD-WIKIDATA-001 §V.3)

The GeoNames resolution step is mandatory and prior to Wikidata resolution. GeoNames identity precedes Wikidata crosswalk.

---

## VII. Relationship to Wikidata

### VII.1 Authority Hierarchy

DD-WIKIDATA-001 establishes the authority hierarchy for place data (Article 11, Invariant W-8):

> "GeoNames is authoritative for place identity. Wikidata supplements with additional names, cultural metadata, crosswalks. Where they conflict: GeoNames wins."

This DD confirms and extends that hierarchy:

| Data dimension | Authority | Rule |
|---|---|---|
| Place identity (geonames_id) | GeoNames | Constitutional (S-3). Wikidata P1566 is crosswalk, not primary. |
| Feature classification (fcode) | GeoNames | CI Constitution routing dependency. Not overridable. |
| Coordinates (lat/lon) | GeoNames | Canonical WGS 84 source. Wikidata P625 is not stored. |
| Administrative hierarchy | GeoNames | admin1/admin2 codes from GeoNames. |
| Alternate names (primary set) | GeoNames | alternateNames from GeoNames. |
| Alternate names (supplement) | Wikidata | Additional languages not in GeoNames alternateNames. |
| Cultural / heritage metadata | Wikidata | P31 (instance of), historical names, notable for. |
| External identifier crosswalks | Wikidata | P1566 (GeoNames ID on Wikidata), P1667 (TGN), etc. |
| Entity QID | Wikidata | Stable Wikimedia entity identifier. |

### VII.2 Complementary Roles, No Overlap

GeoNames and Wikidata do not duplicate each other's functions in NC:
- GeoNames owns the geographic data layer (identity, coordinates, hierarchy, feature codes)
- Wikidata owns the entity crosswalk layer (QIDs, external ID mappings, cultural supplement)

The GeoNames → Wikidata pipeline is: resolve geonames_id first, then look up the Wikidata Q-item that carries P1566 = geonames_id. The GeoNames resolution is the prerequisite; the Wikidata resolution is the follow-on.

### VII.3 Conflict Resolution

Where Wikidata P1566 on a Q-item does not match NC's `places.geonames_id`:
- Investigate which is correct
- GeoNames is authoritative for the correct ID
- Do not silently accept Wikidata's P1566 claim as override of a GeoNames-resolved canonical ID
- If Wikidata's P1566 claim reveals a GeoNames resolution error, correct the GeoNames resolution (update `places.geonames_id` to the correct GeoNames ID) — do not substitute the Wikidata claim

### VII.4 Licensing Interaction

GeoNames is CC BY 4.0. Wikidata is CC0. When NC's `places` table combines GeoNames fields and Wikidata fields, the CC BY 4.0 attribution obligation governs the GeoNames-sourced fields. Wikidata-sourced supplement fields do not independently trigger attribution. However, place API responses and place pages that include any GeoNames-sourced field must carry GeoNames attribution (§IV).

---

## VIII. Relationship to OpenStreetMap

### VIII.1 OSM Classification Status

IFC v1 Article 1.2 lists OSM in the same category as GeoNames:

> "Identity and Reference Authorities (GeoNames, OSM, Wikidata, GBIF) — governed by Standards Constitution v1.0"

OSM is pre-classified as an Identity and Reference Authority but has no corresponding Standards Constitution article (unlike GeoNames, which has Article 17) and no Director Decision. This DD does not govern OSM. OSM governance requires its own DD (DD-OSM-001).

### VIII.2 OSM vs. GeoNames for NC

OSM and GeoNames serve different functions and have different licensing implications:

| Dimension | GeoNames | OpenStreetMap |
|---|---|---|
| License | CC BY 4.0 | ODbL 1.0 (Open Database License) |
| Share-alike | No | Yes — ODbL is share-alike |
| NC current use | Active — `places` table anchor (S-3) | Not active |
| Primary function | Name authority, admin hierarchy, feature codes | Geographic geometry, routing, tagging |
| Geometry detail | Centroid coordinates | Full polygon / multipolygon geometry |

**ODbL share-alike implications.** ODbL 1.0 requires that any derivative database produced from OSM data be released under ODbL. This creates a significant licensing complication for NC:
- If NC's `places` table incorporates OSM geometry data, it may constitute a derivative database under ODbL
- ODbL's share-alike would require NC to license its place database under ODbL if it contains OSM-derived geometry
- This is incompatible with NC's commercial doctrine (NC does not release its commercial intelligence layer under share-alike terms)

**Recommended posture:** OSM should be evaluated for geometry-only use cases (place boundary polygons where GeoNames provides only a centroid) under a clear ODbL derivative-database analysis before any OSM data enters the `places` table. DD-OSM-001 should conduct this analysis. Until DD-OSM-001 is ratified, OSM data does not enter the NC canonical data layer.

### VIII.3 GeoNames Sufficiency for Current NC Scope

At current NC scope (place pages for cities, national parks, reefs, islands, mountains — Wireframe Constitution), GeoNames centroid coordinates and feature codes are sufficient. The Wireframe Constitution does not require polygon boundary geometry for place pages. GeoNames covers NC's current place identity needs without OSM.

---

## IX. GeoNames Evidence Policy

### IX.1 Governing Principle

GeoNames evidence records are **place identity and geographic metadata**. They are stored directly in the `places` canonical table as first-class fields, not in advisory evidence payloads. This differs from GBIF (occurrence counts in evidence payloads) and Wikidata (QIDs and supplement data in entity tables).

GeoNames data is more deeply structural than either GBIF or Wikidata evidence: without GeoNames, there is no `places` record at all (Invariant S-3). The evidence policy therefore governs a set of fields that are simultaneously identity fixtures and scoring inputs.

### IX.2 Governed Evidence Schema

See §VI.2 for the complete field list. Summary:

**Identity fields (constitutional, non-negotiable):**
- `geonames_id` — primary anchor, Invariant S-3
- `feature_code`, `feature_class` — place type, routing dependency
- `country_code` — country identity
- `geom` — authoritative coordinates

**Evidence fields (scoring inputs):**
- `population` — TAS scoring input (CI Constitution)
- `admin1_code`, `admin2_code` — hierarchy for place relevance scoring
- `alternate_names` — search and discovery signal

No GeoNames field may be added to the `places` schema without a Standards Constitution amendment.

### IX.3 Source Provenance

GeoNames as a data source must be recorded in place record provenance. At minimum, every `places` record created from GeoNames data must carry:

```json
{
  "geonames_source": {
    "geonames_id": 12345,
    "resolution_date": "2026-06-11",
    "api_version": "geonames_api_v1",
    "feature_code": "PRK",
    "country_code": "US"
  }
}
```

`resolution_date` is required on all GeoNames-resolved place records. A record without `resolution_date` on its GeoNames fields is a governance violation.

### IX.4 Invariants

**GN-1 — Identity lock.** No NC place record exists without a `geonames_id`. Invariant S-3 of Standards Constitution v1.0. This invariant is permanent and unconditional.

**GN-2 — Feature code integrity.** `places.feature_code` and `places.feature_class` must reflect the GeoNames canonical values for the resolved `geonames_id`. Manual override requires a Director Decision documenting the GeoNames departure. A feature code override without a DD is a CI Constitution violation (routing formula selection is broken).

**GN-3 — Coordinate authority.** `places.geom` coordinates are sourced from GeoNames `lat`/`lng`. Wikidata `P625` coordinates may not overwrite GeoNames coordinates. Manual geometry correction requires a Director Decision and GeoNames deviation record.

**GN-4 — No content writes.** GeoNames data never enters the content pipeline (source_item, media_file, media_rights, preservation_event). GeoNames is a place identity system; it does not generate commercial inventory.

**GN-5 — No source slug.** GeoNames has no M36 source slug. `build_rights_evidence(source_slug="geonames")` is not valid and must never be called.

**GN-6 — Attribution obligation.** Any NC public-facing surface that includes GeoNames-sourced place data must carry GeoNames CC BY 4.0 attribution in the governed format (§IV.2). Attribution omission on a public-facing surface is a licensing compliance violation.

**GN-7 — Read-only.** NC reads from GeoNames; NC does not write to GeoNames. NC does not contribute corrections to the GeoNames open-edit database on behalf of the NC commercial pipeline.

**GN-8 — Resolution date required.** Every `places` record created from a GeoNames lookup must record `geonames_resolution_date`. Records without this field are audit-incomplete.

### IX.5 API Governance

GeoNames provides:
- **JSON API** — `http://api.geonames.org/` (authenticated; requires free account registration)
- **Search endpoint** — `/searchJSON?q={name}&maxRows=N&username={user}`
- **Lookup endpoint** — `/getJSON?geonameId={id}&username={user}`
- **Hierarchy endpoint** — `/hierarchyJSON?geonameId={id}&username={user}`
- **Bulk data dumps** — downloadable from geonames.org/export/

**Rate limits:** GeoNames API free tier provides 20,000 API credits per day per account. Authenticated access requires a registered username (free, no fee). NC must register a GeoNames application account.

**Caching requirement:** GeoNames data is stable. Feature codes, coordinates, and admin hierarchy do not change for established places. NC must cache GeoNames API responses:

| Data type | Minimum TTL | Rationale |
|---|---|---|
| Place lookup by name / coordinates | 90 days | Established places rarely change |
| geonames_id feature metadata | 90 days | Feature codes are very stable |
| alternate_names | 30 days | Community-contributed; more volatile |
| Admin hierarchy | 90 days | Administrative divisions change rarely |

**Bulk download preferred for initial catalog seeding.** For the initial NC place catalog (hundreds to thousands of places), GeoNames bulk data dumps are more efficient and API-friendly than per-place API calls. Bulk downloads are governed by CC BY 4.0; citation is required in NC's data provenance documentation.

---

## X. M36 Write Scope Ruling

### X.1 Place Table Writes — PERMITTED AND REQUIRED

GeoNames-sourced fields in the `places` table are not just permitted writes — they are **constitutionally required** by Invariant S-3. Without `geonames_id`, no place record is canonical. These writes are the core operational output of GeoNames' Place Identity Authority role:

| Table | Column(s) | Status | Condition |
|---|---|---|---|
| `places` | `geonames_id` | Required | Invariant S-3. No place without this. |
| `places` | `feature_code`, `feature_class` | Required | CI Constitution routing dependency. |
| `places` | `country_code`, `admin1_code`, `admin2_code` | Required | Place hierarchy. |
| `places` | `geom` (PostGIS POINT) | Required | Authoritative coordinates. |
| `places` | `population` | Permitted | TAS scoring input. |
| `places` | `alternate_names` | Permitted | Search/discovery input. |

All such writes must record `geonames_resolution_date` in the place record's provenance field (Invariant GN-8).

### X.2 Content Pipeline Writes — PROHIBITED

| Prohibited write | Authority |
|---|---|
| `source_item` from GeoNames | Invariant GN-4 + Disqualifier 1 |
| `media_file` from GeoNames | Invariant GN-4 |
| `media_rights` from GeoNames | Invariant GN-4 + GN-5 |
| M36 source slug for GeoNames | Invariant GN-5 |

### X.3 Distinction from GBIF and Wikidata

GeoNames M36 writes are deeper than either GBIF or Wikidata:
- **GBIF**: writes to illustration opportunity evidence payloads only; no canonical entity table writes
- **Wikidata**: writes `wikidata_qid` and supplementary fields to canonical entity tables (places, creators, sources)
- **GeoNames**: writes the foundational identity and geographic fields without which the `places` record cannot exist

This depth makes GeoNames the most structurally critical of the three Identity and Evidence Authorities. Its data is not advisory; it is constitutional infrastructure.

---

## XI. Media Ingestion Ruling

**GeoNames media is not ingested. There is no media to ingest.**

GeoNames holds no illustrations, photographs, engravings, lithographs, watercolors, maps, or scientific plates. The GeoNames database is a geographic names database. No media ingestion pathway exists or could exist for GeoNames — this prohibition is trivially true but is stated for completeness and to prevent any future mischaracterization of a GeoNames expansion as a media source.

GeoNames does not hold cartographic imagery. Historic maps are sourced from NARA (DD-NARA-001), which provides USGS topo series and survey maps as a govworks source. GeoNames feature codes and coordinate data are used to georeference and classify those maps, but GeoNames is not a map source.

---

## XII. Attribution Compliance Framework

### XII.1 The Condition

DD-GEONAMES-001 is **APPROVED WITH CONDITIONS**. The single condition is:

> **SA-GEONAMES-001 must be ratified before NC place pages are published to the public web at scale.**

SA-GEONAMES-001 formalizes the CC BY 4.0 attribution standard as a governed compliance artifact. It ensures that attribution is implemented consistently across all NC public surfaces that include GeoNames data.

This condition does not block:
- Internal pipeline operations (GeoNames ID resolution, place record creation)
- Pilot-scale operations (pilot place pages in a staging environment)
- API development (internal API testing)

This condition does block:
- Production launch of public place pages without confirmed attribution implementation
- API production launch with external partners without confirmed attribution pass-through
- Bulk data export products without confirmed attribution in data schema

### XII.2 Attribution Checklist (Pre-Scale Gate)

Before place pages are published at scale, the following must be confirmed:

| Surface | Attribution present? | Format verified? |
|---|---|---|
| Public place page footer / data credits | ☐ | ☐ |
| Place API response (`/api/v1/places/{id}`) | ☐ | ☐ |
| IIIF manifest `requiredStatement` (where place metadata present) | ☐ | ☐ |
| JSON-LD `<script>` on place pages | ☐ | ☐ |
| Data export schema (if bulk exports offered) | ☐ | ☐ |
| Partner API terms (attribution pass-through required) | ☐ | ☐ |

All six must be checked and confirmed before SA-GEONAMES-001 ratification.

### XII.3 Attribution Implementation Pattern

GeoNames attribution is a data source attribution, not a per-asset rights statement. It belongs in:
- A persistent "Data Sources" or "About" section on the NC website
- A `dc:source` or `nc:geonames_attribution` field in API responses
- The IIIF manifest `requiredStatement` on any manifest whose place metadata derives from GeoNames
- NC's published data governance documentation

Attribution is **not** required in:
- Individual print product packaging (NC's commercial products are not derived from GeoNames maps)
- NC's internal operational documentation
- Worker-level logs or database audit trails

---

## XIII. Governance Implications Summary

| Question | Ruling |
|---|---|
| Governance class | Place Identity and Evidence Authority (not Content Institution) |
| Standards Constitution posture | Adopt (Article 17) — confirmed; evidence layer and attribution added by this DD |
| Institution Factory applicable? | No — IFC v1 Article 1.2 explicit exclusion |
| Institution number | Not assigned |
| Adapter module | None — not created |
| Rights Matrix | None — CC BY 4.0 is not a per-record rights gate; Attribution Standard governs |
| M36 place table writes | Required — `geonames_id` and canonical fields are constitutional (S-3) |
| M36 content pipeline writes | Prohibited — Invariants GN-4 + GN-5 |
| Media ingestion | Prohibited — no media exists |
| SA-9 applicability | Not applicable — no M36 source slug |
| IFC-1 applicability | Not applicable — not a content institution |
| Licensing | CC BY 4.0 — attribution required; commercial use permitted |
| Commercial reuse | Compatible — CC BY 4.0 permits commercial use with attribution |
| Attribution obligation | Required on all public-facing surfaces (GN-ATT-1) |
| Attribution implementation gate | SA-GEONAMES-001 — required before scale |
| Relationship to Wikidata | GeoNames is authoritative for identity and coordinates; Wikidata supplements (DD-WIKIDATA-001 Article 11, Invariant W-8) |
| Relationship to OSM | OSM not active in NC; ODbL share-alike requires DD-OSM-001 analysis before any OSM data enters places table |
| API authentication | Required — free GeoNames account (username) |
| API caching | Required — 30–90 day TTL per data type |
| Invariants | GN-1 (identity lock, S-3) · GN-2 (feature code integrity) · GN-3 (coordinate authority) · GN-4 (no content writes) · GN-5 (no source slug) · GN-6 (attribution) · GN-7 (read-only) · GN-8 (resolution date required) |
| SA-GEONAMES-001 | Required before place pages published at scale |

---

## XIV. Open Questions

**OQ-1 — OSM polygon geometry for place boundary pages.** Wireframe Constitution v1 defines place pages for regions, parks, and natural areas that would benefit from polygon boundary display (not just centroid points). GeoNames provides only centroid coordinates. OSM provides polygon and multipolygon geometry. If NC's place page design requires boundary display, DD-OSM-001 must analyze ODbL share-alike implications before OSM geometry enters the `places` table. Resolution: commission DD-OSM-001 when place boundary display is added to the Wireframe Constitution scope.

**OQ-2 — GeoNames account registration.** NC currently uses the GeoNames API. The GeoNames free tier requires a registered username. Whether NC has a registered account, and whether that account is documented in the platform configuration, should be confirmed as part of SA-GEONAMES-001 ratification.

**OQ-3 — GeoNames data version pinning.** GeoNames releases weekly data dump updates. NC's `places` table is seeded from a GeoNames dump at a point in time. The `geonames_resolution_date` field records when each place was resolved, but does not record which GeoNames dump version was used. At catalog scale, a GeoNames dump version should be recorded in provenance to enable reproducible audits. Deferred to SA-GEONAMES-001.

**OQ-4 — Place candidates without GeoNames coverage.** Invariant S-3 means a place with no GeoNames entry cannot be a canonical NC place. GeoNames covers 12M+ features but has gaps — some culturally significant heritage sites, very small settlements, or recently renamed features may lack GeoNames records. The protocol for handling these gaps (submit to GeoNames, maintain candidate list, accept a GeoNames provisional record) should be defined in SA-GEONAMES-001.

**OQ-5 — GeoNames Premium API.** GeoNames offers a commercial premium API with higher rate limits and additional endpoints. At full catalog scale (10,000+ places, frequent place resolution), the free tier (20K credits/day) may be insufficient. Premium tier cost/benefit analysis is deferred to SA-GEONAMES-001.

---

## XV. Decision Articles

**Article 1 — Governance Classification.** GeoNames is classified as a Place Identity and Evidence Authority under Standards Constitution v1.0. This classification is permanent. GeoNames is not a content institution and is not subject to the Institution Factory pipeline (IFC v1 Article 1.2 confirmed).

**Article 2 — Constitutional Fixture Confirmation.** Invariant S-3 ("GeoNames Place Identity Lock") is confirmed as a permanent, unconditional constitutional requirement. No NC place entity may exist without a GeoNames ID. This requirement cannot be overridden by a Director Decision; only a Standards Constitution amendment may modify it.

**Article 3 — CC BY 4.0 Attribution Obligation.** GeoNames data is licensed under CC BY 4.0. All NC public-facing surfaces that include GeoNames-sourced place data must carry GeoNames attribution in the governed format (§IV.2). Attribution omission on a public-facing surface is a licensing compliance violation.

**Article 4 — Commercial Use Authorization.** CC BY 4.0 permits commercial use without restriction beyond attribution. GeoNames data is authorized for all NC commercial operations — place pages, API products, commercial print products, partner licensing — provided attribution is maintained per Article 3.

**Article 5 — Place Table Write Authorization.** GeoNames-sourced fields in the `places` table (geonames_id, feature_code, feature_class, country_code, admin1_code, admin2_code, geom, population, alternate_names) are governed and required M36 writes. They constitute the constitutional infrastructure of NC place entities.

**Article 6 — Content Pipeline Prohibition.** GeoNames data never enters the content pipeline (source_item, media_file, media_rights). GeoNames has no M36 source slug. `build_rights_evidence(source_slug="geonames")` is invalid. Invariants GN-4 and GN-5 are permanent.

**Article 7 — Media Ingestion Prohibition.** GeoNames holds no media. No media ingestion pathway for GeoNames exists or will be created. This is a permanent ruling by absence of subject matter.

**Article 8 — Feature Code Integrity.** `places.feature_code` and `places.feature_class` must reflect GeoNames canonical values. Manual override requires a Director Decision. An unconstrained feature code override is a CI Constitution violation because it breaks routing formula selection.

**Article 9 — GeoNames-Wikidata Authority Hierarchy.** GeoNames is authoritative for place identity, coordinates, feature classification, and administrative hierarchy. Wikidata supplements with cultural metadata and crosswalk identifiers. Where GeoNames and Wikidata conflict on any GeoNames-sourced field, GeoNames is authoritative. This hierarchy is confirmed by DD-WIKIDATA-001 Article 11 and Invariant W-8.

**Article 10 — OSM Exclusion Pending DD-OSM-001.** OpenStreetMap data does not enter the NC `places` table until DD-OSM-001 analyzes ODbL share-alike implications and issues a governing ruling. GeoNames is sufficient for current NC place identity scope.

**Article 11 — Attribution Compliance Gate.** SA-GEONAMES-001 must be ratified and the attribution checklist in §XII.2 must be fully confirmed before NC place pages are published at scale. This condition does not block internal pipeline operations or pilot-scale staging operations.

**Article 12 — Resolution Date Required.** Every `places` record created from a GeoNames lookup must record `geonames_resolution_date`. Records without this field fail provenance audit requirements (Invariant GN-8).

**Article 13 — Standards Amendment.** SA-GEONAMES-001 must formalize: CC BY 4.0 attribution standard, API governance and caching policy, feature code governance rules, GeoNames account registration requirement, and OQ-2 through OQ-4 resolution. SA-GEONAMES-001 extends Standards Constitution v1.0 Article 17 with the evidence and attribution layers not covered in the original article.

---

## XVI. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☑ APPROVED WITH CONDITIONS | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*DD-GEONAMES-001 — drafted 2026-06-11*  
*Prior rulings: Standards Constitution v1.0 Article 17 · Invariant S-3 · IFC v1 Article 1.2 · DD-WIKIDATA-001 Article 11 and Invariant W-8*  
*Governing standards: Standards Constitution v1.0 · Institution Factory Constitution v1.0 · Commerce Intelligence Constitution v1.2 · Wireframe Constitution v1*  
*Decision: APPROVED WITH CONDITIONS — Place Identity and Evidence Authority — CC BY 4.0 attribution standard (SA-GEONAMES-001) required before scale*
