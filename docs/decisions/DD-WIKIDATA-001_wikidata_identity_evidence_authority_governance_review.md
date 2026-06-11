# DD-WIKIDATA-001: Wikidata — Identity and Evidence Authority Governance Review

| Field | Value |
|---|---|
| Document | DD-WIKIDATA-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Institution Number | **Not Assigned** — Identity and Evidence Authority; not a content institution |
| Decision | APPROVED — FORMALIZE AS IDENTITY AND EVIDENCE AUTHORITY |
| Prior Rulings | Institution Coverage Audit v1 OQ-2 (2026-06-10) · IFC v1 Article 1.2 · DD-GBIF-001 Article 5 (2026-06-11) · Standards Constitution v1.0 Article 16 |

---

## I. Institution Overview

**Wikidata**
- Operator: Wikimedia Foundation (San Francisco, CA / Berlin, DE)
- URL: https://www.wikidata.org
- Governance: Free and open collaborative knowledge base; governed by Wikimedia Foundation policies and community consensus
- Core product: Structured linked-data knowledge base — entity identifiers (QIDs), property-value statements, multilingual labels, external identifier crosswalks, and interwiki links across all Wikimedia projects

Wikidata is the Wikimedia Foundation's universal entity database. It assigns stable Q-item identifiers (QIDs) to real-world entities — people, places, taxa, institutions, concepts, events — and stores structured property-value claims about each. It is the primary global crosswalk hub, holding external identifier mappings to GeoNames, Getty TGN, Getty ULAN, VIAF, LCNAF, GBIF taxon keys, museum collection IDs, ORCID, and hundreds of other authority systems.

Wikidata does not hold illustrations, photographs, artworks, or PD heritage media. Media associated with Wikidata entities is hosted on Wikimedia Commons, a separate system not governed by this document.

---

## II. Governance Classification — Ruling

### II.1 The Four Options

**Option 1 — Identity Authority:** Wikidata governs entity identity resolution. NC reads Wikidata as a reference service — QID lookup, entity disambiguation, alternate names, administrative hierarchy, crosswalk to other identifier systems. Governed by Standards Constitution v1.0. No Institution Factory stages. No content adapter.

**Option 2 — Evidence Authority:** Wikidata as a factual evidence source for structured claims about NC's governed entity domains — creator biographical data, place geographic metadata, institution metadata, taxon crosswalk QIDs. Governed evidence metadata only; no content pipeline involvement.

**Option 3 — Content Institution:** Wikidata as a source of images and media for the illustration commerce pipeline. Requires Institution Factory stages, adapter module, rights matrix, M36 content writes.

**Option 4 — Hybrid (Identity + Evidence Authority):** Wikidata serves simultaneously as the entity identity anchor system and as a structured evidence source across NC's four governed entity domains. This is the dual role GBIF holds in the biological domain, generalized to Wikidata's universal scope.

### II.2 Option 3 (Content Institution): REJECTED

Four independent disqualifiers:

**Disqualifier 1 — No content.** Wikidata holds structured data about entities, not creative works. It holds no illustrations, engravings, lithographs, watercolors, or scientific plates. Wikidata `P18` (image) properties are filename references to Wikimedia Commons — they are metadata pointers, not hosted images. Wikidata cannot be a content institution because it contains no content in the NC commercial sense.

**Disqualifier 2 — Wrong domain.** The NC commercial object is a Golden Age illustration (1750–1900) by a priority illustrator. Wikidata produces no such object. Its structured data claims are factual, not creative. This is a categorical distinction, not a licensing question.

**Disqualifier 3 — Doctrine.** The Illustration Opportunity Doctrine defines the commercial object as an illustration rooted in a place and a taxon. Wikidata entity records are identity metadata, not illustrations. Institution Factory stages govern the path from raw institutional content to a governed illustration opportunity. That path does not apply to a structured-data knowledge base.

**Disqualifier 4 — Media provenance.** Any image reachable via a Wikidata `P18` reference is hosted on Wikimedia Commons. Its rights and provenance are governed by Commons, not Wikidata. Wikidata cannot grant or represent commercial rights for Commons-hosted media. A Wikidata-entry adapter that followed `P18` links would create provenance laundering — assigning a Wikidata source to a Commons-hosted file.

### II.3 Option 1 (Identity Authority alone): INSUFFICIENT

Standards Constitution v1.0 Article 16 already establishes Wikidata under the "Map" posture for entity identity resolution. That posture is correct and is confirmed here. However, Identity Authority alone understates Wikidata's active role in NC's pipeline.

Wikidata does not merely resolve entity identities on demand. It supplies structured evidence that NC stores in canonical entity records: biographical data for `creator_authority_registry`, geographic supplemental data for `places`, institutional data for `sources`, and crosswalk identifiers that enable multi-system entity federation. This evidence role requires its own governed policy — the GBIF Evidence Authority standard (SA-GBIF-001) provides the precedent.

### II.4 Option 2 (Evidence Authority alone): INSUFFICIENT

Evidence Authority describes what Wikidata contributes to NC's pipeline but does not capture the primary role: Wikidata QIDs are the identity anchors for NC's canonical entity records. The `wikidata_qid` field on `places`, `creator_authority_registry`, and `sources` is an identity field, not an evidence field. Evidence fields carry scored inputs; identity fields carry stable external identifiers that link NC's internal records to the global linked-data ecosystem. Both functions are active; neither alone describes the full role.

### II.5 Option 4 (Identity and Evidence Authority): RATIFIED

**Wikidata is ratified as an Identity and Evidence Authority.**

Standards Constitution v1.0 Article 16 governs Wikidata's "Map" posture — this ruling does not amend that posture. It formally extends Article 16's scope from "Identity and Reference Authority" to "Identity and Evidence Authority," adding the governed evidence role for each of the four NC entity domains.

Institution Factory Constitution v1 Article 1.2 already lists Wikidata explicitly as an entity governed by Standards Constitution v1.0, not the Institution Factory. This DD confirms and formalizes that exclusion.

This ruling supersedes any future proposal to classify Wikidata as a content institution. Such a reclassification requires DD-WIKIDATA-002 that affirmatively reverses this ruling and addresses all four disqualifiers above.

---

## III. Licensing Model

### III.1 Wikidata Data Licensing

All Wikidata structured data is published under **Creative Commons Zero (CC0 1.0 Universal)**. This is Wikimedia Foundation policy, not per-entity licensing. CC0 applies unconditionally to all Wikidata data used by NC:

| Data type | License | NC use permitted? |
|---|---|---|
| Wikidata entity labels (all languages) | CC0 | Yes — unconditional |
| Wikidata statements / property-value pairs | CC0 | Yes — unconditional |
| Wikidata Q-item identifiers | CC0 | Yes — unconditional |
| Wikidata external identifier crosswalks | CC0 | Yes — unconditional |
| Wikidata geographic coordinates (`P625`) | CC0 | Yes — unconditional |
| Wikidata biographical data (birth/death dates, nationality) | CC0 | Yes — unconditional |
| Wikidata taxon identifiers (GBIF key, ITIS ID, etc.) | CC0 | Yes — unconditional |
| Wikidata text descriptions | CC0 | Yes — descriptions are CC0; Wikipedia text is CC BY-SA and is out of scope |
| Wikimedia Commons media files (`P18` referents) | Per Commons file | **Not governed here** — Commons is a separate system |
| Wikidata website UI content | Wikimedia TOU | Not stored by NC |

### III.2 Key Licensing Ruling

NC's use of Wikidata for entity identity resolution, crosswalk lookups, and structured evidence is a factual data use. QIDs, property values, and crosswalk identifiers are structured facts — they are not copyrightable under any NC member-jurisdiction copyright statute. The CC0 licensing of all Wikidata data is therefore belt-and-suspenders governance: even without any formal license, factual entity data would not create copyright exposure.

**No Wikidata Rights Matrix is required.** Rights matrices govern content records written to the M36 store as commercial inventory. Wikidata identity and evidence records are not commercial inventory. A **Wikidata Evidence Policy** (Section VI) governs what Wikidata data may be stored, in what form, and for what purpose.

### III.3 The Commons Boundary

Wikidata's CC0 license does not extend to media files referenced via Wikidata `P18` (image), `P154` (logo), `P94` (coat of arms), or any other Wikidata property that links to a Commons filename. Each such file has its own license on Wikimedia Commons. NC may not treat a Wikidata CC0 statement as license clearance for the media file it references. This boundary is unconditional (see Section VIII, Media Ingestion Ruling).

---

## IV. Commercial Reuse Policy

### IV.1 Wikimedia Foundation Commercial Reuse Position

The Wikimedia Foundation explicitly authorizes commercial reuse of all Wikidata data under CC0. There is no:
- Fee for commercial use
- Registration requirement
- Terms of Service restriction on commercial applications
- Endorsement restriction that prohibits commercial product branding

This distinguishes Wikidata from Gallica (BnF requires a license fee for commercial reuse — DD-GALLICA-003) and from NOAA (which carries a nonendorsement policy for branding). Wikidata's commercial reuse policy is clean and unconditional for structured data.

### IV.2 API Terms

Wikidata's public APIs (Wikidata Query Service SPARQL endpoint; MediaWiki Action API) impose:
- Rate limits for unauthenticated callers (SPARQL: 60-second timeout per query; Action API: standard MediaWiki limits)
- Bot user-agent policy: NC API access must use a descriptive `User-Agent` header identifying the NC application
- No commercial restriction

NC must not use Wikidata APIs in a manner that violates fair use policy (e.g., high-frequency polling that mimics a full database extraction). Governed caching policy (Section VI, §6.5) is the compliance mechanism.

### IV.3 Nonendorsement

Wikidata and the Wikimedia Foundation marks may not be used to imply institutional endorsement of the NC platform. NC may reference Wikidata as a data source in provenance metadata and attribution statements without implying endorsement. This is operational guidance, not a commercial restriction.

---

## V. Governance Role Definition

### V.1 Entity Resolution (Primary Role)

Wikidata QIDs are stable global entity identifiers. NC uses QIDs as the universal external anchor for its four canonical entity types:

| NC entity | Wikidata QID role | Storage location |
|---|---|---|
| `creator_authority_registry` | Identity anchor for illustrators, artists, naturalists | `creator_authority_registry.wikidata_qid` |
| `places` | Identity anchor for geographic places | `places.wikidata_qid` |
| `sources` (institutions) | Identity anchor for content institutions | `sources.wikidata_qid` |
| Biological taxa | Taxon identity anchor (inherited via GBIF backbone) | `illustration_opportunities` biological anchor |

QIDs are load-bearing identifiers, not advisory metadata. They link NC's internal records to the global linked-data graph and enable future federation with Wikidata-connected systems (peer museum APIs, cultural heritage aggregators).

### V.2 Crosswalk Authority (Primary Role)

Wikidata is NC's primary crosswalk hub — the system that maps between identifier namespaces. For any NC entity with a Wikidata QID, Wikidata provides mappings to:

| External system | Wikidata property | NC use |
|---|---|---|
| GeoNames | P1566 | Place identity cross-validation, GeoNames ID confirmation |
| Getty TGN | P1667 | Geographic name authority crosswalk |
| Getty ULAN | P245 | Creator authority crosswalk (OQ-1 of Standards Constitution v1.0) |
| VIAF | P214 | Creator authority federation |
| LCNAF | P244 | Library of Congress Name Authority crosswalk |
| GBIF taxon key | P846 | Biological anchor crosswalk (authoritative) |
| ITIS taxon ID | P815 | Secondary taxon crosswalk |
| Museum collection IDs | Various | Institution-specific collection identifier mappings |

Crosswalk data enables NC to link its canonical records to peer authority systems without adopting those systems as primary stores. The crosswalk is directional: NC reads crosswalk data from Wikidata; NC does not maintain its own crosswalk database.

### V.3 Place Identity (Active Role)

Wikidata supplements GeoNames as a place data source for NC's `places` table. GeoNames is the authoritative NC place identity system (Standards Constitution v1.0 Article 17, Invariant S-3). Wikidata is supplementary — it provides:

- Alternate names in additional languages beyond GeoNames coverage
- Historical place names (P571 inception, P576 dissolution, P1566 crosswalk)
- Administrative hierarchy verification
- Cultural and heritage significance metadata (instance-of class, notable for, etc.)

Wikidata does not override GeoNames for place identity. Where Wikidata and GeoNames conflict on coordinates, names, or hierarchy, GeoNames is authoritative.

### V.4 Cultural Identity (Active Role)

Wikidata is the primary biographical evidence source for `creator_authority_registry` enrichment. For illustrators and naturalists in the NC priority list and extended creator registry, Wikidata provides:

- Birth and death dates (P569, P570)
- Nationality and citizenship (P27)
- Occupational classification (P106)
- Alternative name forms (P1559, P742, aliases)
- Notable works links (P800) — for provenance cross-referencing
- External authority IDs (VIAF, ULAN, LCNAF — see §V.2)

Wikidata cultural identity data is used for display enrichment and authority resolution, not for scoring. Creator prestige scoring (COS component) is governed by the Priority Illustrator Registry, not by Wikidata claims.

### V.5 Taxonomic Linkage (Inherited Role)

Wikidata maps biological taxa to multiple identifier systems via properties including `P846` (GBIF taxon key), `P815` (ITIS TSN), `P685` (NCBI taxon ID), and `P105` (taxon rank). NC inherits Wikidata taxon QIDs through the GBIF backbone mapping established in SA-GBIF-001 (Policy 2, §2.5). Direct Wikidata taxon resolution supplements GBIF when a GBIF backbone entry does not carry a `wikidata_qid`.

Wikidata's taxonomic role is supplementary to GBIF's biological anchor authority. GBIF's `gbif_taxon_key` is NC's canonical biological anchor (SA-GBIF-001 Invariant I-3). `wikidata_qid` on a biological anchor is a crosswalk identifier, not a competing authority.

### V.6 Source Role in the Illustration Opportunity Pipeline

Wikidata's governed source role in the illustration opportunity pipeline is `"context_only"`. This designation is codified in SA-GBIF-001 §1.5 (Provenance Format) and is the only permitted designation for Wikidata in provenance output:

```json
{
  "source_roles": {
    "bhl": "primary_discovery",
    "gbif": "validation_only",
    "wikidata": "context_only"
  }
}
```

`"context_only"` means Wikidata data enriches the illustration opportunity record with entity context (creator biography, place alternate names, taxon crosswalk) but does not contribute discovery signals, rights evidence, or commercial scoring inputs. No future code change may promote Wikidata to `"primary_discovery"` or `"content"` without a DD-WIKIDATA-002 governance document.

---

## VI. Wikidata Evidence Policy

### VI.1 Governing Principle

Wikidata evidence records are **identity and context metadata**, not content inventory. They never acquire a `source_item` identifier, a `media_rights` record, or any M36 content record. They are stored to support four governed purposes: entity identity anchoring, crosswalk federation, place enrichment, and creator/institution authority resolution.

This evidence policy is the Wikidata equivalent of the GBIF Evidence Policy (SA-GBIF-001 Policy 1). It governs all NC components that interact with Wikidata.

### VI.2 Evidence Schema — Creator Domain

Fields governed for storage in `creator_authority_registry`:

| Field | Wikidata source | Type | Rule |
|---|---|---|---|
| `wikidata_qid` | Item QID | string (`Q{integer}`) | Primary identity anchor. Required for all canonical creator records. |
| `wikidata_birth_date` | P569 | ISO 8601 date | Advisory; human-verified before canonical promotion. |
| `wikidata_death_date` | P570 | ISO 8601 date | Advisory; confirms public domain status window. |
| `wikidata_nationality` | P27 (citizenship) | string | Country name / Q-item label; display only. |
| `wikidata_viaf_id` | P214 | string | VIAF crosswalk. Supplementary to primary VIAF resolution. |
| `wikidata_ulan_id` | P245 | string | Getty ULAN crosswalk. Load-bearing when OQ-1 (Standards Constitution v1.0) is resolved. |
| `wikidata_lcnaf_id` | P244 | string | LCNAF crosswalk. Supplementary. |
| `wikidata_resolution_date` | NC-generated | ISO 8601 date | Date QID was resolved for this entity. Required. |

**Fields explicitly not stored in creator domain:**
- Individual statement GUIDs (ephemeral Wikidata provenance; not load-bearing for NC)
- Wikipedia article text (CC BY-SA, not CC0; out of scope)
- Commons media filenames from `P18` (image) or equivalent (media ingestion prohibited, §VIII)
- Social media identifiers (P2002, P2003, etc.) — no NC commercial purpose
- Any Wikidata field not enumerated above

### VI.3 Evidence Schema — Place Domain

Fields governed for storage in `places`:

| Field | Wikidata source | Type | Rule |
|---|---|---|---|
| `wikidata_qid` | Item QID | string (`Q{integer}`) | Primary identity anchor. Required for all canonical place records. |
| `wikidata_geonames_id` | P1566 | string | Cross-validation of `places.geonames_id`. Must match GeoNames canonical. |
| `wikidata_tgn_id` | P1667 | string | Getty TGN crosswalk. Supplementary. |
| `wikidata_alternate_names` | P1559, aliases | JSONB array | Multilingual alternate names supplement to GeoNames alternateNames. |
| `wikidata_instance_of` | P31 | string (Q-label) | Place type classification (e.g., "national park", "island", "reef"). Display only. |
| `wikidata_resolution_date` | NC-generated | ISO 8601 date | Date QID was resolved for this entity. Required. |

**Conflict resolution rule:** Where `wikidata_geonames_id` (Wikidata's P1566 claim) differs from `places.geonames_id` (NC's GeoNames-resolved canonical ID), GeoNames is authoritative. Flag the conflict in a `wikidata_conflict` metadata field; do not overwrite the GeoNames-canonical value.

**Fields explicitly not stored in place domain:**
- Wikidata geographic coordinates (`P625`) — GeoNames is the canonical coordinate source (Standards Constitution Invariant S-3)
- Administrative hierarchy (GeoNames is authoritative for `admin1_code`, `admin2_code`)
- Commons images referenced via Wikidata place items
- Tourist or heritage significance descriptors (not a scored NC input)

### VI.4 Evidence Schema — Institution Domain

Fields governed for storage in `sources`:

| Field | Wikidata source | Type | Rule |
|---|---|---|---|
| `wikidata_qid` | Item QID | string (`Q{integer}`) | Primary identity anchor. Required for all canonical institution records. |
| `wikidata_official_website` | P856 | URI | Cross-validation of `sources.base_url`. Not canonical — institution's direct confirmation is authoritative. |
| `wikidata_resolution_date` | NC-generated | ISO 8601 date | Date QID was resolved. Required. |

**Fields explicitly not stored in institution domain:**
- Wikidata collection IDs (institution-specific, governed by individual institution DDs)
- Wikidata infrastructure properties (ISNI, ROR, etc.) — not required for NC commercial pipeline
- Commons logos (`P154`) — not ingested (see §VIII)

### VI.5 Evidence Schema — Taxon Domain

Fields governed for taxon QID storage (biological anchor, inherited via GBIF):

| Field | Wikidata source | Type | Rule |
|---|---|---|---|
| `wikidata_qid` | Item QID (taxon item) | string (`Q{integer}`) | Crosswalk anchor. Inherited from GBIF backbone mapping (SA-GBIF-001 §2.5). May be resolved directly when GBIF does not supply a QID. |
| `wikidata_gbif_taxon_key` | P846 | integer | Cross-validation of `gbif_taxon_key`. Must match NC's GBIF-resolved canonical key. |
| `wikidata_resolution_date` | NC-generated | ISO 8601 date | Date QID was resolved. Required. |

**Authority hierarchy:** GBIF `gbif_taxon_key` is the canonical biological anchor (SA-GBIF-001 Invariant I-3). Wikidata `wikidata_qid` for a taxon is a crosswalk identifier. Where Wikidata `P846` and NC's resolved GBIF key differ, flag for human review — do not silently overwrite.

### VI.6 Invariants

**W-1 — No content writes.** No Wikidata-sourced record may be written to `source_item`, `source_record` (as content), `media_file`, `media_rights`, `media_technical_metadata`, or `preservation_event`. Violation is an IFC-1 breach regardless of the CC0 status of any Wikidata data.

**W-2 — No source slug.** Wikidata has no M36 source slug. `build_rights_evidence(source_slug="wikidata")` is not valid and must never be called.

**W-3 — Source role immutability.** `"wikidata": "context_only"` in illustration opportunity provenance is immutable without DD-WIKIDATA-002.

**W-4 — Rights exclusion.** Wikidata `P6216` (copyright status) and `P275` (copyright license) claims are advisory FM context only. They may never set `media_rights.rights_status`. This is Standards Constitution v1.0 Article 16.3 and Foundation Model Constitution Invariant FM-4.

**W-5 — Read-only.** NC reads from Wikidata; NC does not write entity data to Wikidata. Standards Constitution v1.0 Article 16.1.

**W-6 — Commons boundary.** Wikidata CC0 does not extend to Commons-hosted media. No Wikidata `P18` (or equivalent) reference may be followed as an image ingestion pathway. The media file at the Commons filename has its own license; Wikidata does not govern it.

**W-7 — QID resolution date required.** Every `wikidata_qid` stored in any NC canonical table must carry a companion `wikidata_resolution_date`. A QID without a resolution date is a governance violation detectable in schema audit.

**W-8 — GeoNames authority over place identity.** Wikidata-sourced place data supplements GeoNames; it does not override it. No NC place record may have its `geonames_id`, coordinates, or administrative hierarchy modified based on Wikidata data alone. GeoNames is the authoritative source per Standards Constitution Invariant S-3.

### VI.7 API Governance

Wikidata provides two governed API surfaces:

**MediaWiki Action API** — `https://www.wikidata.org/w/api.php`
- Entity lookup by QID: `?action=wbgetentities&ids=Q{id}&format=json`
- Property lookup: `?action=wbgetentities&ids=Q{id}&props=claims&format=json`
- Rate limit: standard MediaWiki limits; no formal published cap for reasonable use
- Required: descriptive `User-Agent` header

**Wikidata Query Service (SPARQL)** — `https://query.wikidata.org/sparql`
- Complex entity resolution and crosswalk queries
- Timeout: 60 seconds per query (hard limit)
- Required: descriptive `User-Agent` header
- Not for high-frequency per-entity lookups — use Action API for those

**Caching requirement:** Wikidata entity data changes infrequently for the entity types NC uses (biographical dates, place QIDs, institution QIDs). NC must cache Wikidata API responses with a minimum TTL of 30 days. Live Wikidata API calls must not be issued on every scoring run or on every place/creator record retrieval.

| Data type | Minimum TTL | Rationale |
|---|---|---|
| Entity QID lookup (creator, place, institution) | 30 days | QIDs are stable; entity merges/redirects are rare |
| Biographical data (birth/death dates, nationality) | 30 days | Historical facts; not updated frequently |
| External identifier crosswalks | 30 days | Mapping additions are infrequent |
| Taxon QIDs | 30 days | Taxonomy is stable between GBIF backbone releases |
| Place alternate names | 7 days | Community-contributed; more volatile |

---

## VII. M36 Write Scope Ruling

### VII.1 Identity Field Writes — PERMITTED

The following M36 writes are governed and permitted. They are the core purpose of Wikidata's Identity Authority role:

| Table | Column | Permitted write | Condition |
|---|---|---|---|
| `places` | `wikidata_qid` | Yes | GeoNames-verified place, human-reviewed QID assignment |
| `creator_authority_registry` | `wikidata_qid` | Yes | Canonical creator record, human-reviewed QID assignment |
| `sources` | `wikidata_qid` | Yes | Active governed institution, QID confirmed from Wikidata item |
| `illustration_opportunities` | `wikidata_qid` (biological anchor) | Yes | Inherited from GBIF backbone mapping, SA-GBIF-001 §2.5 |

These writes record the resolved Wikidata QID at a point in time. They are subject to Invariant W-7 (resolution date required) and Invariant W-5 (read-only — NC reads from Wikidata, does not write back).

### VII.2 Evidence Field Writes — PERMITTED (Schema-Bounded)

Supplementary evidence fields (biographical data, crosswalk IDs, alternate names per §VI.2–VI.5) may be written to their governed canonical tables. All such writes must:
- Conform to the evidence schema in §VI.2–VI.5
- Not exceed the governed field list without a Standards Constitution amendment
- Record `wikidata_resolution_date` alongside any QID-anchored write

### VII.3 Content Pipeline Writes — PROHIBITED

The following M36 write categories are unconditionally prohibited:

| Prohibited write | Authority |
|---|---|
| `source_item` records from Wikidata data | Invariant W-1 |
| `source_record` records with Wikidata as content source | Invariant W-1 |
| `media_file` records from Wikidata-referenced images | Invariant W-1 + W-6 |
| `media_rights` records based on Wikidata `P6216`/`P275` | Invariant W-4 |
| M36 source slug assignment to Wikidata | Invariant W-2 |

### VII.4 Distinction from GBIF

GBIF's M36 write prohibition is broader: GBIF data does not appear in canonical entity tables at all — it appears only in illustration opportunity evidence payloads. Wikidata's QIDs ARE stored in canonical entity tables (`places`, `creator_authority_registry`, `sources`). This difference is governed:

- GBIF's evidence role is domain-specific (biological occurrences) and does not anchor canonical entity records
- Wikidata's identity role anchors canonical entity records via QID — that is the core purpose of Article 16 of Standards Constitution v1.0
- Neither GBIF nor Wikidata enters the content pipeline (source_item / media_file / media_rights)

The distinction is: **entity-table identity writes** (Wikidata, permitted) vs. **content-pipeline writes** (both Wikidata and GBIF, prohibited).

---

## VIII. Media Ingestion Ruling

**Wikidata media is not ingested. No adapter. No M36 source_item writes.**

This is a permanent ruling, not a pilot exclusion. Four independent disqualifiers in §II.2 are all permanent. Additionally:

**The Commons boundary (Invariant W-6):** Wikidata `P18` (image), `P154` (logo), `P94` (coat of arms), `P1801` (commemorative plaque), and all other Wikidata properties that reference Wikimedia Commons filenames are **not ingestion pathways**. These properties are metadata pointers. The target files are hosted on Wikimedia Commons, a separate system with its own governance. NC may not follow a Wikidata property reference as if Wikidata had granted the file's license.

Wikimedia Commons itself is a potential future content institution (it holds a large corpus of PD heritage images). If NC ever evaluates Wikimedia Commons as a content institution, it does so through a separate DD for Commons. That evaluation is independent of and does not conflict with Wikidata's Identity and Evidence Authority classification.

SA documents for a Wikidata media ingestion path will not be drafted unless DD-WIKIDATA-001 is reversed by DD-WIKIDATA-002.

---

## IX. Relationship to Standards Constitution v1.0 Article 16

### IX.1 What Article 16 Establishes (Confirmed)

DD-WIKIDATA-001 confirms the following Article 16 provisions without modification:

- **"Map" posture** — NC maps its internal model to Wikidata; it does not adopt Wikidata's RDF model internally
- **16.1 Read-only rule** — NC reads from Wikidata; NC does not write to Wikidata
- **16.2 QID versioning** — QIDs stored with resolution date; NC's local record is the canonical mapping
- **16.3 Rights exclusion** — Wikidata is not a rights evidence source; `P6216`/`P275` may never set `media_rights.rights_status`

### IX.2 What This DD Adds

| Addition | Location |
|---|---|
| Formal classification: Identity and Evidence Authority | §II.5 |
| Evidence Policy across four domains (creator, place, institution, taxon) | §VI |
| Eight governance invariants (W-1 through W-8) | §VI.6 |
| M36 write scope ruling (identity writes permitted; content writes prohibited) | §VII |
| Media ingestion ruling (permanent prohibition) | §VIII |
| Commons boundary doctrine | §VIII, Invariant W-6 |
| Source role designation: `"context_only"` | §V.6 |
| API governance and caching policy | §VI.7 |
| SA-WIKIDATA-001 commissioning | §X |

### IX.3 Standards Constitution Amendment Required

The additions above must be formalized as a Standards Constitution v1.0 amendment (SA-WIKIDATA-001) that adds an Article 19 (Wikidata Evidence Authority) to the constitution. Until SA-WIKIDATA-001 is ratified, this DD governs. SA-WIKIDATA-001 does not alter the "Map" posture in Article 16 — it adds the evidence layer governance that Article 16 does not address.

---

## X. Recommended Standards Amendment

### X.1 SA-WIKIDATA-001 — Wikidata Identity and Evidence Authority Standard

**Type:** Standards Constitution Amendment
**Amends:** Standards Constitution v1.0 — adds Article 19 (Wikidata)
**Scope:**
- Formalizes the evidence schema for each of the four governed entity domains
- Codifies the eight invariants (W-1 through W-8)
- Adds API governance and caching TTLs
- Clarifies the Commons boundary doctrine
- Extends Article 16's `wikidata_qid` mapping to include the governed evidence fields

SA-WIKIDATA-001 should be drafted immediately following DD-WIKIDATA-001 ratification. It is not a prerequisite for pilot operations — the current implementation already conforms to the identity field governance in Article 16. It is a prerequisite for full catalog harvest scale, where uncontrolled Wikidata API access would violate caching policy.

### X.2 No Additional SAs Required at This Time

Wikidata does not require:
- A Rights Matrix (CC0 is unconditional; Invariant W-4 prohibits rights derivation from Wikidata claims)
- An Institution Factory stage document (IFC v1 Article 1.2 explicitly excludes Wikidata)
- An SA-9 extension (Wikidata has no M36 source slug; Invariant W-2)
- A pilot plan (Wikidata is already in production as the `"context_only"` source)

---

## XI. Governance Implications Summary

| Question | Ruling |
|---|---|
| Governance class | Identity and Evidence Authority (not Content Institution) |
| Classification basis | Standards Constitution v1.0 Article 16 + IFC v1 Article 1.2 |
| Institution Factory stages | None — not applicable |
| Institution number | Not assigned |
| Adapter module | None — not created |
| Rights matrix | None — Invariant W-4 prohibits rights derivation from Wikidata |
| M36 identity field writes | Permitted — `wikidata_qid` on places, creators, institutions, taxa |
| M36 evidence field writes | Permitted — schema-bounded per §VI.2–VI.5 |
| M36 content pipeline writes | Prohibited — Invariants W-1 through W-2 |
| Media ingestion | Prohibited — permanent ruling |
| Commons media (via P18 references) | Prohibited — Invariant W-6 |
| SA-9 applicability | Not applicable — no M36 source slug |
| IFC-1 applicability | Not applicable — Wikidata is not a content institution |
| Commercial reuse | Permitted — CC0, no ToS restriction, no fee |
| API caching | Required — 30-day TTL for entity data before catalog scale |
| Source role | `"context_only"` — immutable without DD-WIKIDATA-002 |
| Standards Constitution posture | Map (Article 16) — confirmed; Evidence layer added by this DD |
| SA-WIKIDATA-001 | Required before full catalog harvest scale |
| Rights exclusion (FM-4) | Active — Wikidata P6216/P275 never canonical for rights_status |
| GeoNames authority | Active — Wikidata supplements; never overrides |
| Read-only rule | Active — Standards Constitution Article 16.1 |

---

## XII. Open Questions

**OQ-1 — Getty ULAN adoption (Standards Constitution OQ-1).** Standards Constitution v1.0 OQ-1 recommends adding `ulan_id` to `creator_authority_registry` alongside `wikidata_qid`. Wikidata `P245` provides the ULAN crosswalk. If OQ-1 is resolved, SA-WIKIDATA-001 should include ULAN crosswalk governance (what to do when Wikidata `P245` and direct ULAN resolution produce different IDs). This OQ is inherited, not created by this DD.

**OQ-2 — Wikidata QID merge and redirect handling.** Wikidata entities are occasionally merged (two Q-items representing the same entity are merged into one, with the old QID redirected). NC's stored `wikidata_qid` values may reference redirected QIDs. A QID redirect resolution check — analogous to the GBIF backbone sync audit (SA-GBIF-001 §2.4) — should be part of the annual entity audit cycle. Frequency: annual, not continuous.

**OQ-3 — Wikidata reconciliation service (Standards Constitution OQ-5).** Standards Constitution v1.0 OQ-5 defers the question of NC publishing a Wikidata reconciliation endpoint until the activated catalog exceeds 10,000 assets. This DD does not resolve OQ-5. The precondition (10K activated assets) and the security/governance review remain as specified in OQ-5.

**OQ-4 — Wikimedia Commons as a future content institution.** Wikimedia Commons holds a large corpus of PD heritage images, including illustrations from the Golden Age (1750–1900) that are currently inaccessible via NC's institution pipeline. Commons is a separate system from Wikidata and would require its own DD (DD-COMMONS-001), rights matrix, and pilot plan. This DD does not authorize or block a future Commons evaluation. It establishes only that accessing Commons via Wikidata `P18` references is prohibited (Invariant W-6); direct Commons evaluation is a separate governance track.

**OQ-5 — Wikidata as a crosswalk resolution service for institutional onboarding.** When new content institutions are onboarded via the Institution Factory, Wikidata QID resolution for the institution's collection items (works, creators) is a recurring step. A governed "Wikidata resolution sprint" pattern — analogous to Asset Zero for content institutions — could standardize this step across all institution onboardings. Deferred to SA-WIKIDATA-001.

---

## XIII. Decision Articles

**Article 1 — Governance Classification.** Wikidata is classified as an Identity and Evidence Authority under Standards Constitution v1.0. This classification is permanent. Wikidata is not a content institution and is not subject to the Institution Factory pipeline (IFC v1 Article 1.2 confirmed).

**Article 2 — Content Institution Disqualification.** Wikidata is permanently disqualified as a content institution on four independent grounds: no content in the NC commercial sense, wrong domain, doctrine prohibition, and media provenance laundering risk. Reinstatement requires DD-WIKIDATA-002 that affirmatively reverses each ground.

**Article 3 — Media Ingestion Prohibition.** No Wikidata-referenced image, video, or audio file may be ingested as NC commercial inventory. No Wikidata `P18` or equivalent property may be treated as an image ingestion pathway. This prohibition is permanent and unconditional.

**Article 4 — Commons Boundary Doctrine.** Wikidata CC0 does not extend to Wikimedia Commons-hosted media. Accessing a Commons file via a Wikidata property reference is governed as a Commons access, not a Wikidata access. Commons files retain their own licenses, independent of any Wikidata statement about them.

**Article 5 — Identity Field Write Authorization.** `wikidata_qid` fields in `places`, `creator_authority_registry`, `sources`, and the biological anchor component of `illustration_opportunities` are governed M36 writes. They are the core operational output of Wikidata's Identity Authority role. Human review is required before any bulk QID assignment operation.

**Article 6 — Evidence Policy Governance.** Wikidata evidence data may be stored in NC entity records subject to the schemas in §VI.2–VI.5. No additional Wikidata fields may be added to any NC schema without a Standards Constitution amendment. The field lists in §VI.2–VI.5 are exhaustive.

**Article 7 — Rights Exclusion (Invariant W-4).** Wikidata copyright properties (`P6216`, `P275`) are advisory FM context only. They may never set `media_rights.rights_status`. This invariant is co-equivalent with Foundation Model Constitution Invariant FM-4 and is unconditional.

**Article 8 — Source Role Designation.** Wikidata's governed source role in the illustration opportunity pipeline is `"context_only"`. This designation is codified in SA-GBIF-001 §1.5 and is confirmed here as the authoritative designation for Wikidata. No future code change may promote Wikidata to `"primary_discovery"` or `"content"` without DD-WIKIDATA-002.

**Article 9 — Standards Amendment Required.** SA-WIKIDATA-001 must be drafted and ratified before full catalog harvest scale. Pilot-scale operations under the current implementation conform to this DD. Production-scale operations require the formal Standards Constitution amendment.

**Article 10 — No SA-9 Applicability.** Wikidata does not receive an M36 source slug. It is not added to the `build_rights_evidence` source slug registry. SA-9 does not apply to Wikidata.

**Article 11 — GeoNames Supremacy.** Wikidata place data supplements GeoNames; it does not replace it. No NC place record's `geonames_id`, coordinates, or administrative hierarchy may be overwritten by Wikidata data. Wikidata `P1566` crosswalk is a validation input, not a canonical source.

**Article 12 — Caching Policy Prerequisite.** A Wikidata API caching policy (minimum TTL of 30 days for entity data) is required before full catalog harvest scale. At pilot scale (current operations), caching is recommended but not constitutionally mandatory.

---

## XIV. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☑ APPROVED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*DD-WIKIDATA-001 — drafted 2026-06-11*  
*Prior rulings: Institution Coverage Audit v1 OQ-2 · IFC v1 Article 1.2 · DD-GBIF-001 Article 5 · Standards Constitution v1.0 Article 16*  
*Governing standards: Standards Constitution v1.0 Article 16 · Foundation Model Constitution Invariant FM-4 · Commerce Intelligence Constitution v1.2 · Institution Factory Constitution v1 Article 1.2*  
*Decision: APPROVED — FORMALIZE AS IDENTITY AND EVIDENCE AUTHORITY — not a content institution*
