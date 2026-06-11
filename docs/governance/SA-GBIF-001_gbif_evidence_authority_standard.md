# SA-GBIF-001: GBIF Evidence Authority Standard

| Field | Value |
|---|---|
| Document | SA-GBIF-001 |
| Version | 1.0 |
| Status | **RATIFIED** — DD-GBIF-001-FGD 2026-06-11 |
| Type | Standards Constitution Amendment |
| Amends | Standards Constitution v1.0 — adds Article 18 (GBIF) |
| Authority | DD-GBIF-001 |
| Date | 2026-06-11 |

---

## Purpose

This standard formalizes GBIF's governed role in the NC platform. DD-GBIF-001 classified GBIF as an Identity and Evidence Authority. This document operationalizes that classification across four policies: what GBIF evidence is, how taxon data is governed, how occurrence data is governed, and how GBIF licensing is handled.

No Institution Factory stages. No adapter. No M36 content writes.

---

## Article 18 — Global Biodiversity Information Facility (GBIF)

**Ruling: Evidence Authority — Consume and Map**

GBIF is the world's primary aggregator of biodiversity occurrence data. NC consumes GBIF data for two governed purposes: taxon identity anchoring and place-relevance evidence. GBIF is not a content institution. GBIF data is never written to the M36 content pipeline.

The four policies below are constitutional amendments to Standards Constitution v1.0 and govern all NC components that interact with GBIF.

---

### Policy 1 — GBIF Evidence Policy

#### 1.1 Governed Role

GBIF's governed source role in NC is `"validation_only"`. This role designation applies to all GBIF data in all NC workers. No future code or governance change may promote GBIF to `"primary_discovery"` or `"content"` without a DD-GBIF-002 governance document that reverses DD-GBIF-001.

GBIF evidence records are **evidence metadata**. They are not content inventory. They never acquire a `source_item` identifier, a `media_rights` record, or any M36 content record. They are stored exclusively to support taxon anchoring, place-relevance scoring, and illustration opportunity provenance.

#### 1.2 Permitted Evidence Uses

| Use | Governed purpose | Where stored |
|---|---|---|
| Taxon key resolution | Biological anchor identity confirmation | `illustration_opportunities.gbif_taxon_key` |
| Occurrence count scoring | Place-relevance signal (capped input) | Evidence payload in illustration opportunity record |
| Dataset count scoring | Evidence breadth indicator | Evidence payload |
| Place relevance score | `place_relevance_score` field on place_link | `illustration_opportunities.place_relevance_score` |
| Backbone taxonomy lookup | Name authority resolution | In-memory / cached; not stored as a table |
| Evidence provenance URL | Source attribution in illustration opportunity evidence array | `evidence[].source_url` |

#### 1.3 Prohibited Evidence Uses

The following are unconditional prohibitions. They apply at all scales, in all sprints, in all pipeline stages:

| Prohibited use | Authority |
|---|---|
| Writing GBIF-sourced images to `source_item` | DD-GBIF-001 Article 3 |
| Writing GBIF-sourced images to `media_file` | DD-GBIF-001 Article 3 |
| Writing GBIF-sourced images to `media_rights` | DD-GBIF-001 Article 3 |
| Assigning GBIF an M36 source slug | DD-GBIF-001 Article 8 |
| Using GBIF as an occurrence publisher (NC writes to GBIF) | Doctrine: NC is not a biodiversity system |
| Storing raw occurrence payloads | Section 1.4 below |
| Storing observer names from occurrence records | PII; no NC purpose |
| Storing individual occurrence record IDs | Ephemeral; not load-bearing |
| Assigning GBIF an institution number | DD-GBIF-001, institution classification |

#### 1.4 Evidence Record Schema

The following fields constitute the complete GBIF evidence record schema. No additional GBIF fields may be added to NC schemas without a Standards Constitution amendment.

**Taxon identity fields:**

| Field | Source | Type | Rule |
|---|---|---|---|
| `gbif_taxon_key` | GBIF Backbone API | integer | Primary biological anchor. Stored in `illustration_opportunities`. |
| `gbif_canonical_name` | GBIF Backbone API | string | Scientific name at resolution time. |
| `gbif_taxon_rank` | GBIF Backbone API | string | kingdom / phylum / class / order / family / genus / species |
| `gbif_kingdom` | GBIF Backbone API | string | Top-level classification. |
| `gbif_backbone_version` | GBIF Backbone metadata | string | Backbone version at resolution time (e.g., "2023-06-28"). |
| `gbif_resolution_date` | NC-generated | ISO 8601 date | Date the taxon key was resolved. Required for backbone sync audit. |
| `wikidata_qid` | GBIF → Wikidata link | string | Wikidata Q-item inherited via GBIF DwC mapping. May be null. |

**Occurrence evidence fields:**

| Field | Source | Type | Cap | Rule |
|---|---|---|---|---|
| `gbif_occurrence_count` | GBIF species occurrence API | integer | 100 (hard cap per Invariant I-3) | Place-relevance scoring input. |
| `gbif_dataset_count` | GBIF species occurrence API | integer | None | Evidence breadth indicator. |
| `gbif_source_url` | GBIF species page | string | — | Provenance URL for evidence record. |
| `place_relevance_score` | Derived | float 0.0–1.0 | — | Scoring output, not stored as raw GBIF data. |

#### 1.5 Source Provenance Format

Every illustration opportunity record that includes GBIF evidence must carry the following provenance structure:

```json
{
  "source_roles": {
    "bhl": "primary_discovery",
    "gbif": "validation_only",
    "wikidata": "context_only"
  }
}
```

The `"gbif": "validation_only"` assignment is mandatory. Its omission is a governance violation detectable in replay tests.

#### 1.6 Invariants

**I-1 — No content writes.** No GBIF-sourced record may be written to `source_item`, `source_record`, `media_file`, `media_rights`, `media_technical_metadata`, or `preservation_event`. Violation is an IFC-1 breach regardless of rights status.

**I-2 — No source slug.** GBIF has no M36 source slug. `build_rights_evidence(source_slug="gbif")` is not valid and must never be called.

**I-3 — Occurrence count cap.** `gbif_occurrence_count` must be capped at 100 in any scoring context. Uncapped occurrence count may not influence any NC score. Violation is a Commerce Intelligence Constitution breach (CI Constitution v1.2 bias mitigation clause).

**I-4 — Source role immutability.** `"gbif": "validation_only"` in provenance is immutable without DD-GBIF-002.

---

### Policy 2 — GBIF Taxon Policy

#### 2.1 GBIF Backbone Taxonomy

The GBIF Backbone Taxonomy is NC's authoritative taxon name resolution service for biological anchors. It is published under CC0 and is available for unrestricted use.

**Ruling: Adopt as biological anchor authority.**

The GBIF Backbone is the synthetic name authority that resolves scientific name strings to stable integer taxon keys. NC uses the backbone for:
- Resolving illustration subject names (from BHL metadata) to canonical `gbif_taxon_key` identifiers
- Inheriting the DwC mapping (`dwc:taxonID = gbif_taxon_key`) per Standards Constitution v1.0 Article 11
- Inheriting the GBIF → Wikidata Q-item mapping for biological anchor identity

#### 2.2 Taxon Key Resolution

`gbif_taxon_key` is the canonical biological anchor identifier. It is an integer corresponding to the GBIF Backbone `speciesKey` or `taxonKey` for the accepted usage of a scientific name.

**Resolution process:**
1. Scientific name string from source metadata (BHL, illustration record)
2. GBIF Species Match API: `GET /v1/species/match?name={name}&strict=false`
3. Accept if `matchType` ∈ {`EXACT`, `FUZZY`} and `confidence ≥ 90`
4. Reject if `matchType == NONE` or `confidence < 90`
5. Prefer `speciesKey` over `taxonKey` for species-level resolution
6. Record `gbif_backbone_version` and `gbif_resolution_date` at time of resolution

**Homonym handling:** Where a name resolves to multiple backbone entries (homonym), prefer the entry with higher `confidence` score. Do not attempt to disambiguate via FM reasoning. Flag unresolved homonyms as `gbif_match_status: "ambiguous"` in the evidence record.

#### 2.3 Resolution Date Recording

`gbif_resolution_date` is mandatory on every stored `gbif_taxon_key`. It records the date NC resolved the name to the key. It does not imply the key is permanently correct — backbone updates may change assignments.

**Read-only rule:** NC reads from GBIF backbone; NC does not write taxon data to GBIF. This mirrors Standards Constitution v1.0 Article 16.1 (Wikidata read-only rule).

#### 2.4 Backbone Synchronization Policy

The GBIF Backbone is updated approximately annually (periodic major releases plus monthly incremental updates). When a backbone update changes an existing taxon key (taxon split, merge, synonym promotion, or rank change), stored `gbif_taxon_key` values may become stale.

**Sync policy:**
- NC conducts a **backbone sync audit** annually, not more frequently
- The audit compares stored `gbif_taxon_key` values against the current backbone using the `/v1/species/{key}` status endpoint
- Taxon keys that have been merged into another key are updated in bulk
- Taxon keys that have been split require human review — automated reassignment is prohibited
- The backbone sync audit is a governance event, not an automated process. It requires a Principal Architect decision before any bulk remapping occurs
- `gbif_backbone_version` on each stored record enables retroactive audit without live API calls

**Backbone sync is not a continuous process.** NC's `gbif_taxon_key` values are stable identifiers at their resolution date. The annual audit corrects drift, not continuous staleness.

#### 2.5 Wikidata Relationship

GBIF backbone entries map to Wikidata Q-items via the DwC → Wikidata link (GBIF publishes `wikidata_qid` for most backbone entries). NC inherits this mapping. When a GBIF backbone entry has a `wikidata_qid`, NC stores it alongside `gbif_taxon_key` in the biological anchor record.

Where GBIF provides a `wikidata_qid` and NC's own Wikidata resolution (Standards Constitution v1.0 Article 16) produces a different Q-item, NC's resolution takes precedence. GBIF's Q-item mapping is advisory; NC's is authoritative.

#### 2.6 Common Names

GBIF provides vernacular (common) names per taxon key (`/v1/species/{key}/vernacularNames`). NC may use GBIF vernacular names for display and search purposes. GBIF vernacular names are factual data (not copyrightable). They are stored as supplementary metadata, not as governed evidence records.

---

### Policy 3 — GBIF Occurrence Policy

#### 3.1 Governed Purpose

GBIF occurrence data has one governed purpose in NC: providing evidence that a taxon was historically present at or near a specific place. This evidence supports the `place_relevance_score` assigned to illustration opportunities. A high occurrence count for taxon X in the GBIF datasets associated with location Y indicates strong place-relevance for an illustration of taxon X sold at location Y.

Occurrence data does not govern rights. Occurrence data does not govern commercial value. Occurrence data is one of several scoring inputs and is subject to the cap and anti-correlation rules defined in the Commerce Intelligence Constitution v1.2.

#### 3.2 Occurrence Fields Governed for Storage

See Policy 1, Section 1.4, Occurrence evidence fields. The complete set is:
- `gbif_occurrence_count` (capped at 100)
- `gbif_dataset_count`
- `gbif_source_url`
- `place_relevance_score` (derived output)

No other occurrence fields may be stored.

#### 3.3 Occurrence Count Cap — CI Constitution Compliance

`gbif_occurrence_count` must be capped at 100 before use in any scoring formula. This is Invariant I-3 of the Evidence Policy and is required by Commerce Intelligence Constitution v1.2 bias mitigation.

**Rationale for the cap:** Without a cap, charismatic megafauna and well-documented common species (Homo sapiens, Bos taurus, Passer domesticus) would produce artificially high place-relevance scores. The cap equalizes well-documented and poorly-documented species once the count exceeds 100. The cap is not arbitrary — it represents the point at which occurrence evidence is "confirmed abundant" and additional records carry no incremental commercial relevance signal.

**Anti-contamination rule:** NC's Commercial Opportunity Score (COS) must not correlate with raw GBIF occurrence frequency. Periodic replay analysis that reveals such correlation indicates a cap bypass or a contaminated scoring signal, and is a CI Constitution breach regardless of how it was introduced.

#### 3.4 API Access and Caching

**Endpoints governed:**
| Purpose | GBIF endpoint | Method |
|---|---|---|
| Taxon key resolution | `/v1/species/match` | GET |
| Backbone taxon lookup | `/v1/species/{key}` | GET |
| Occurrence count | `/v1/occurrence/count?taxonKey={key}` | GET |
| Dataset count | `/v1/occurrence/count?taxonKey={key}&isGeoreferenced=true` | GET |
| Vernacular names | `/v1/species/{key}/vernacularNames` | GET |

**API base URL:** `https://api.gbif.org/v1` (configured in `workers/taxon_discovery_worker/config.py`)

**Rate limits:**
- Unauthenticated: approximately 1 request/second; 10K requests/day
- Authenticated (registered app): higher limits, specific to application tier
- NC must not exceed unauthenticated limits without registering an application

**Caching requirement — mandatory before catalog scale:**

| Data type | Minimum TTL | Rationale |
|---|---|---|
| Taxon key resolution (`/species/match`) | 30 days | Names do not change monthly |
| Backbone taxon metadata (`/species/{key}`) | 30 days | Backbone updates are infrequent |
| Occurrence count | 24 hours | GBIF ingestion runs daily; counts are stable intraday |
| Dataset count | 24 hours | Same |
| Vernacular names | 30 days | Rarely updated |

NC must implement a caching layer for GBIF API responses before full catalog harvest (50K+ taxon candidates). Live GBIF API calls on every scoring run at catalog scale will exhaust unauthenticated rate limits within hours. At pilot scale (≤500 taxon candidates per run), caching is recommended but not mandatory. This transition is a **catalog scale prerequisite**, not a Sprint 3 prerequisite.

**Bulk download alternative:** For catalog-scale backbone resolution, GBIF provides bulk DwC dataset downloads. These may be used in place of per-taxon API calls for backbone resolution and vernacular name lookup. Bulk downloads are governed by the GBIF Data User Agreement. CC0 dataset bulk downloads require citation; NC must include a GBIF citation in its data provenance records when bulk data is used.

#### 3.5 Occurrence Evidence Record Format

When GBIF occurrence evidence is stored in an illustration opportunity record, it must follow this structure:

```json
{
  "source": "gbif",
  "evidence_type": "place_relevance",
  "source_url": "https://www.gbif.org/species/{gbif_taxon_key}",
  "payload": {
    "gbif_taxon_key": 12345,
    "gbif_occurrence_count": 847,
    "gbif_occurrence_count_capped": 100,
    "gbif_dataset_count": 23,
    "place_relevance_score": 0.87,
    "gbif_backbone_version": "2023-06-28",
    "gbif_resolution_date": "2026-06-11"
  }
}
```

`gbif_occurrence_count_capped` must always be present alongside `gbif_occurrence_count`. The raw count is preserved for audit; the capped count is the governed scoring input.

#### 3.6 Place Relevance Score Derivation

`place_relevance_score` is a derived field. It is not a raw GBIF field. It is computed from GBIF occurrence evidence (and optionally from geographic occurrence analysis) and normalized to the range 0.0–1.0.

The default `place_relevance_score` for records where GBIF validation is absent is 0.72. This default represents "assumed relevant" — when a taxon appears in a BHL illustration associated with a place (e.g., an Audubon plate of a North American bird), the place relevance is presumed high even without occurrence confirmation.

**Governing constraint:** `place_relevance_score` is a place-commercial-significance signal. It must not embed GBIF occurrence frequency as a proxy for species scientific importance or biodiversity significance. The signal must capture "was this taxon commercially relevant at this place" — not "is this taxon well-documented in GBIF databases."

---

### Policy 4 — GBIF License Policy

#### 4.1 Ruling: GBIF Does Not Grant NC Commercial Rights

GBIF is a passthrough aggregator for licensing purposes. GBIF does not hold primary copyright or grant commercial reuse rights for content contributed by member institutions. The license applicable to any GBIF-hosted record is the license assigned by the contributing institution or citizen scientist.

**This ruling extends DD-ALA-001 Article 6 to all GBIF media.** DD-ALA-001 established that ALA records remain CC BY-NC when accessed via GBIF — GBIF access does not convert licenses. This principle applies universally: no GBIF-accessed record has a different license than the same record accessed from its primary source.

#### 4.2 GBIF Data Products by License

| Data product | License | NC use |
|---|---|---|
| **GBIF Backbone Taxonomy** | CC0 1.0 Universal | Unrestricted. Full use for taxon anchoring, name resolution, vernacular names. |
| **GBIF occurrence records (CC0 datasets)** | CC0 | Evidence use permitted. Factual data; no copyright risk. |
| **GBIF occurrence records (CC BY datasets)** | CC BY | Evidence use permitted. Citation required in provenance. |
| **GBIF occurrence records (CC BY-NC datasets)** | CC BY-NC | Evidence use permitted (non-commercial data use). May not be used as a scoring input for commercial prioritization without legal review. |
| **GBIF GBIF.org website content** | GBIF terms of use | Not stored by NC. |
| **GBIF media — iNaturalist-contributed** | CC BY-NC dominant | **Prohibited.** Not ingested. |
| **GBIF media — Wikimedia-sourced** | CC BY-SA / CC0 mix | **Not ingested via GBIF.** Access Wikimedia directly if needed. |
| **GBIF media — museum collections** | Per source institution | **Not ingested via GBIF.** Access primary institution via Institution Factory. |
| **GBIF API response payloads** | GBIF terms of use | Cached and used per API terms. Not redistributed. |

#### 4.3 Occurrence Data Licensing — Factual Data Rule

GBIF occurrence records are factual biodiversity data: species X was observed at location Y on date Z by observer W. Factual data is not copyrightable under the applicable laws of GBIF's member nations (including the EU Database Directive's "substantial investment" threshold, which GBIF does not assert against non-commercial users, and which does not apply to NC's evidence use of individual occurrence counts rather than bulk database extraction).

NC's use of GBIF occurrence counts and dataset counts for place-relevance scoring does not constitute reproduction or extraction of a substantial part of the GBIF database. It constitutes factual reference to aggregated statistics about a species.

**This analysis does not authorize media ingestion.** The factual data rule applies to occurrence records (counts, keys, metadata). It does not apply to photographs, illustrations, or other creative works hosted in GBIF multimedia.

#### 4.4 CC BY Dataset Citation Requirement

When GBIF bulk downloads are used for backbone resolution or occurrence evidence (per Policy 3, Section 3.4), and those downloads contain CC BY datasets, NC must record a dataset citation in provenance:

```json
{
  "gbif_citation": {
    "doi": "10.15468/dl.{gbif_download_key}",
    "accessed": "2026-06-11",
    "license": "CC BY 4.0"
  }
}
```

This citation is recorded in the illustration opportunity evidence record's provenance field. It is not a rights gate — it is attribution governance.

#### 4.5 Media Prohibition — Permanent

GBIF-hosted images, videos, and audio are permanently excluded from NC ingestion. This prohibition applies regardless of the per-record license of any specific GBIF media asset. The disqualifiers are structural (content type mismatch, aggregator architecture, provenance duplication) and do not depend on the license of any individual record.

No special-case exception exists for "CC0 GBIF images." CC0 GBIF images are available at their primary sources (natural history museums, Wikimedia). Sourcing them via GBIF creates avoidable provenance complexity and would require a GBIF content adapter that duplicates existing institution adapters.

**Authority:** DD-GBIF-001 Article 3.

#### 4.6 GBIF Data User Agreement

GBIF requires API users to accept the GBIF Data User Agreement for bulk data access. Key terms relevant to NC:
- NC may use GBIF data for any purpose consistent with the CC0/CC BY/CC BY-NC licenses of individual datasets
- NC must not misrepresent GBIF as the rights holder for any media
- NC must not imply GBIF endorsement of NC products

The endorsement restriction mirrors the NOAA nonendorsement policy. GBIF's name and logo may not be used to imply institutional endorsement of NC's commercial platform.

---

## Governance Summary

| Dimension | Ruling |
|---|---|
| Governance class | Identity and Evidence Authority |
| Standards Constitution amendment | Article 18 (this document) |
| Rights matrix | None — replaced by this Evidence Authority Standard |
| Institution Factory | Not applicable |
| M36 source writes | Permanently prohibited |
| Backbone taxonomy | CC0 — full use |
| Occurrence evidence | Permitted — schema-bounded, capped, cached |
| Media ingestion | Permanently prohibited |
| License model | Passthrough — GBIF does not grant commercial rights |
| CI Constitution constraint | Active — occurrence count cap at 100, anti-correlation rule |
| Caching policy | Required at catalog scale (24h occurrence TTL, 30d backbone TTL) |
| Backbone sync | Annual review cycle — not continuous |
| Source role | `"validation_only"` — immutable without DD-GBIF-002 |

---

## Invariant Registry

| ID | Invariant | Scope |
|---|---|---|
| I-1 | No content writes — GBIF data never enters M36 content pipeline | All components |
| I-2 | No source slug — GBIF is not an M36 source | store.py / rights workers |
| I-3 | Occurrence count capped at 100 | rank.py / all scoring workers |
| I-4 | Source role `"validation_only"` immutable | discover.py / all provenance output |
| I-5 | Media prohibition permanent — no GBIF image ingestion pathway | All adapters |
| I-6 | License passthrough — GBIF does not change contributing institution licenses | Rights governance |
| I-7 | Read-only — NC never writes taxon data to GBIF | All workers |
| I-8 | Backbone sync by annual audit only — no continuous automated remapping | taxon_discovery_worker |

---

## Standards Constitution Scope

This amendment adds to and refines the following Standards Constitution v1.0 sections:

| Section | Amendment |
|---|---|
| Article 11 (Darwin Core) | GBIF Evidence Policy formalizes the "consumption rule" reference |
| Article 16 (Wikidata) | GBIF Taxon Policy formalizes the inherited `wikidata_qid` mapping |
| Article 18 (new) | This document in its entirety |
| SS-02 (biological anchor) | `gbif_taxon_key` field governance formalized |
| SS-08 (biological anchor evidence) | Occurrence evidence record schema added |
| SS-11 (biological subject terms) | Vernacular name governance added |

---

## Ratification Table

| Role | Ratified | Date |
|---|---|---|
| Governance Review | ☑ APPROVED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*SA-GBIF-001 — drafted 2026-06-11*  
*Amends: Standards Constitution v1.0 (adds Article 18)*  
*Authority: DD-GBIF-001 · DD-ALA-001 Article 6 · Institution Coverage Audit v1 OQ-3*  
*Standards: GBIF Data User Agreement · CC0 1.0 · DwC TDWG 2021 · Commerce Intelligence Constitution v1.2*
