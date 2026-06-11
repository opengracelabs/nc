# DD-GBIF-001: Global Biodiversity Information Facility — Source Audit

| Field | Value |
|---|---|
| Document | DD-GBIF-001 |
| Version | 1.0 |
| Status | **RATIFIED** — DD-GBIF-001-FGD 2026-06-11 |
| Date | 2026-06-11 |
| Institution Number | **Not Assigned** — Identity and Evidence Authority; not a content institution |
| Decision | FORMALIZE AS IDENTITY AND EVIDENCE AUTHORITY |
| Prior Rulings | Institution Coverage Audit v1 OQ-3 (2026-06-10) · DD-ALA-001 Article 6 (2026-06-10) |

---

## I. Institution Overview

**Global Biodiversity Information Facility (GBIF)**
- Headquarters: Copenhagen, Denmark
- URL: https://www.gbif.org
- Governance: Intergovernmental organization (109 member countries)
- Core product: Aggregated biodiversity occurrence data — 2.5B+ occurrence records from 100K+ datasets

GBIF is the world's foremost biodiversity data aggregator. It does not produce primary data; it republishes data contributed by member institutions (natural history museums, herbaria, research universities, citizen science platforms, government agencies). GBIF maintains its own **Backbone Taxonomy** — a synthetic species name authority used to resolve occurrence records to scientific names.

---

## II. Governance Classification — Ruling

### II.1 The Three Options

**Option 1 — Identity Authority:** GBIF governs taxon identity resolution and occurrence evidence. NC reads GBIF as a reference service — taxon key → scientific name, occurrence count, place relevance. No M36 writes. Governed by Standards Constitution v1.0.

**Option 2 — Content Institution:** GBIF as a source of images and media for the illustration commerce pipeline. Requires Institution Factory stages, adapter module, rights matrix, M36 writes.

**Option 3 — Hybrid:** Identity Authority for occurrence data, limited Content Institution for CC0 media contributed by member institutions.

### II.2 Option 2 (Content Institution): REJECTED

Five independent disqualifiers:

**Disqualifier 1 — Wrong content type.** GBIF's image corpus is dominated by contemporary scientific photography from iNaturalist, Wikimedia, and natural history museum collections. The NC commercial object is a Golden Age illustration (1750–1900): an engraving, lithograph, watercolor, or scientific plate by a priority illustrator (Audubon, Gould, Merian, Redouté, Haeckel, Nodder, et al.). GBIF does not hold this content in any significant quantity. GBIF surfaces BHL illustrations on species pages, but BHL is already NC's primary discovery source; dual-sourcing from GBIF creates provenance complexity with no content gain.

**Disqualifier 2 — Wrong license distribution.** iNaturalist contributes the majority of GBIF's multimedia. iNaturalist images are licensed by individual users, with CC BY-NC 4.0 the most common choice. CC BY-NC prohibits commercial use; IFC-1 is unsatisfiable at scale for GBIF's image corpus. DD-ALA-001 Article 6 established that GBIF does not homogenize per-record licenses — it is a passthrough aggregator. A CC BY-NC iNaturalist photograph remains CC BY-NC whether accessed via iNaturalist directly or via GBIF.

**Disqualifier 3 — Aggregator architecture.** GBIF is a secondary aggregator for media, not a primary rights holder. For any GBIF-hosted image, the rights status, rights statement, and licensing terms originate with the contributing institution or citizen scientist. NC has no direct relationship with GBIF that grants commercial rights; commercial rights must be traced to the primary source. The Institution Factory cannot govern a source whose rights are opaque at the aggregator layer.

**Disqualifier 4 — Provenance duplication.** GBIF's highest-quality CC0 images come from the same natural history museum institutions already in NC's target pipeline (NHM London, Smithsonian, NARA, etc.). Ingesting the same records from both the primary institution and GBIF creates duplicate source_records with divergent provenance, complicating rights tracing and audit.

**Disqualifier 5 — Doctrine.** NC is not a biodiversity system (Platform Identity doctrine). GBIF's core inventory — occurrence records, species observations, specimen catalogues — is biodiversity data, not illustration commerce inventory. The Illustration Opportunity Doctrine defines the commercial object as an illustration rooted in a place and a taxon, not a biodiversity observation. Ingesting GBIF as a content institution would import a biodiversity paradigm into a commerce platform.

### II.3 Option 3 (Hybrid): REJECTED

The Hybrid option is a subset of the Content Institution option and inherits all five disqualifiers. A "CC0 filter" against GBIF's image corpus does not resolve Disqualifiers 1, 3, 4, or 5. The CC0 image subset of GBIF is small, dominated by Wikimedia Commons (already accessible directly), and not concentrated in Golden Age illustration. The Hybrid model adds institutional complexity with no meaningful content gain.

### II.4 Option 1 (Identity Authority): RATIFIED — with formal extension to Evidence Authority

**GBIF is ratified as an Identity and Evidence Authority.**

The existing governance designation in Standards Constitution v1.0 ("Identity and Reference Authority") is confirmed, and formally extended to "Identity and Evidence Authority" to capture GBIF's active role in place-relevance scoring and illustration opportunity evidence records. The addition of "Evidence" does not constitute a new governance tier — it clarifies that GBIF data stored in NC is evidence metadata, not content inventory.

This ruling supersedes any future proposal to classify GBIF as a content institution or hybrid. Such a reclassification requires a new DD (DD-GBIF-002) that affirmatively reverses this ruling and addresses all five disqualifiers above. Institution Coverage Audit v1 OQ-3 and DD-ALA-001 Article 6 are ratified as permanent references.

---

## III. Licensing Model

### III.1 GBIF Data Products

| Data type | License | NC use permitted? |
|---|---|---|
| GBIF Backbone Taxonomy | CC0 | Yes — taxon key resolution, name authority |
| GBIF occurrence records (CC0 datasets) | CC0 | Yes — place relevance evidence |
| GBIF occurrence records (CC BY datasets) | CC BY | Yes — evidence metadata (attribution recorded) |
| GBIF occurrence records (CC BY-NC datasets) | CC BY-NC | Conditional — evidence use only; prohibited for commercial inventory |
| GBIF media (iNaturalist majority) | CC BY-NC dominant | No — commercially unusable per IFC-1 |
| GBIF media (Wikimedia-sourced) | CC BY-SA / CC0 mix | Available at source directly; no GBIF mediation needed |
| GBIF media (museum collections) | Per source institution | Available from primary institution directly |

### III.2 Key Licensing Ruling

NC's use of GBIF occurrence data for place-relevance scoring and taxon key resolution is a factual data use, not a copyrightable content use. Factual data (species X was observed at location Y in year Z) is not subject to copyright under the copyright statutes of GBIF member nations. The CC0/CC BY licensing of GBIF occurrence datasets is therefore belt-and-suspenders governance: even without any formal license, factual occurrence data would not create copyright exposure.

GBIF's CC0 Backbone Taxonomy, covering scientific names, ranks, synonyms, and taxon keys, is unambiguously available for any use.

**No GBIF Rights Matrix is required.** Rights matrices govern content records written to the M36 store as commercial inventory. GBIF evidence records are not commercial inventory. A **GBIF Evidence Policy** (Section V) governs what GBIF data may be stored, in what form, and for what purpose.

---

## IV. GBIF Media Ingestion Ruling

**GBIF media is not ingested. No adapter. No M36 source_item writes.**

This is a permanent ruling, not a pilot exclusion. The five disqualifiers in Section II.2 are all permanent: the content type mismatch is structural, the license distribution problem is structural (GBIF does not change contributor licenses), the aggregator provenance problem is structural, the provenance duplication risk is structural, and the doctrine prohibition is constitutional.

SA documents for a GBIF media ingestion path will not be drafted unless DD-GBIF-001 is reversed by DD-GBIF-002.

---

## V. GBIF Occurrence Record Governance

### V.1 Ruling: Conditional Storage — Evidence Records Only

GBIF occurrence data **is stored in NC**, subject to the following conditions:

1. GBIF data is stored as **evidence metadata**, not as content inventory. It is never assigned a `source_item`, `media_file`, or `media_rights` record. It never enters the M36 content pipeline.
2. Storage is limited to the fields defined in the GBIF Evidence Record Schema (Section V.2).
3. GBIF evidence records serve exactly three governed purposes: taxon key anchoring, place-relevance scoring, and illustration opportunity provenance.
4. No additional GBIF fields may be stored without a Standards Constitution amendment.

### V.2 GBIF Evidence Record Schema

The following GBIF-sourced fields are governed for storage in NC:

**Taxon identity fields (stored in `illustration_opportunities.concept_id` anchor):**
| Field | GBIF source | Purpose |
|---|---|---|
| `gbif_taxon_key` | GBIF Backbone taxon ID | Primary biological anchor; stable identifier |
| `scientific_name` | GBIF Backbone | Human-readable taxon label |
| `taxon_rank` | GBIF Backbone | kingdom / phylum / class / order / family / genus / species |
| `kingdom` | GBIF Backbone | Top-level taxonomic classification |
| `wikidata_qid` | GBIF → Wikidata link | Wikidata reconciliation (GBIF inherits DwC→Wikidata mapping) |

**Occurrence evidence fields (stored as evidence payload in illustration opportunity records):**
| Field | GBIF source | Purpose | Cap |
|---|---|---|---|
| `gbif_occurrence_count` | GBIF species occurrence API | Place-relevance scoring input | 100 (enforced in rank.py) |
| `gbif_dataset_count` | GBIF species occurrence API | Evidence breadth indicator | No cap |
| `place_relevance_score` | Derived from occurrence evidence | Place-commercial-relevance signal | 0.0–1.0 |
| `gbif_source_url` | GBIF species page URL | Evidence provenance link | — |

**Fields explicitly not stored:**
- Individual occurrence record IDs (ephemeral; not load-bearing for NC)
- Observer names (PII; no NC purpose)
- Raw occurrence payloads (unbounded; not needed)
- Taxon image URLs (media ingestion is prohibited per Section IV)
- Any GBIF field not enumerated above

### V.3 API Governance

GBIF API: `https://api.gbif.org/v1`

GBIF provides a public, unauthenticated API with a published rate limit of approximately 1 request/second for unauthenticated callers. Authenticated callers (registered application) receive higher limits. For NC at pilot scale, unauthenticated access is sufficient.

**Caching requirement:** GBIF occurrence counts for a given taxon key are stable on a monthly timescale (GBIF runs bulk ingestion jobs, not real-time). NC must not issue GBIF occurrence API calls on every scoring run. The scoring worker must cache GBIF evidence per `gbif_taxon_key` with a minimum TTL of 24 hours. This is a Standards Constitution v1.0 conformance requirement (§ "GBIF consumption rule").

**Live vs. cached:** The taxon discovery worker currently issues live GBIF API calls during scoring (`gbif_api_base_url` in config). A caching policy must be defined before full catalog harvest scale. At 50K+ taxon candidates, live GBIF calls per scoring run would exhaust rate limits.

### V.4 Commerce Intelligence Constitution Constraint

The Commerce Intelligence Constitution v1.2 contains a hard prohibition:

> "COS must not correlate with GBIF occurrence frequency, species popularity, or taxonomic inventory completeness. Any such correlation in a replay analysis indicates a contaminated signal and is a constitutional breach."

GBIF occurrence counts are governed scoring inputs, but the cap at 100 (`gbif_occurrence_count_capped`) is the CI Constitution compliance mechanism — it prevents high-occurrence species (rats, pigeons, common sparrows) from receiving disproportionate COS simply because they are well-documented in GBIF. The cap is load-bearing governance, not an implementation convenience. Removing it requires a CI Constitution amendment.

`gbif_taxon_key` presence (0.30 weight in discovery scoring) is governed as an identity confirmation signal, not a biodiversity abundance signal. Its purpose is to confirm that the taxon in question exists in the authoritative backbone, not to prefer well-studied taxa over poorly-studied ones.

---

## VI. Recommended Architecture

### VI.1 Current Architecture (Production, v0.3.0)

```
place_id + concept_id
    ↓
taxon_discovery_worker
    ├── GBIF API → gbif_taxon_key, occurrence_count, dataset_count (validation)
    ├── Wikidata → wikidata_qid, common_names (context)
    └── ranked candidates → illustration_opportunity_worker
            ↓
        BHL → illustration discovery (primary)
        GBIF evidence → place_relevance_score (validation_only)
        Wikidata context → taxonomic_context (context_only)
            ↓
        illustration_opportunity record
            source_roles: {bhl: primary_discovery, gbif: validation_only, wikidata: context_only}
```

The `source_roles` provenance field in `discover.py` formally documents GBIF's governed role: `"gbif": "validation_only"`. This is the correct architectural designation and is already in production.

### VI.2 Recommended Governance Additions (Not Code)

**Addition 1 — Formal GBIF Evidence Policy document.** A short governance document (analogous to a Rights Matrix, but for evidence metadata) that codifies Section V.2 above. This is a Standards Constitution amendment (SA to Standards Constitution v1.0). It prevents future scope creep where GBIF fields are added to NC schemas without governance review.

**Addition 2 — GBIF caching policy.** A defined TTL for GBIF occurrence count caching (minimum 24h recommended, 7 days for production scale). This must be governed before full catalog harvest. Not a content governance question — a platform performance and API-citizenship question.

**Addition 3 — GBIF Backbone Taxonomy synchronization policy.** GBIF releases new backbone taxonomy versions periodically (annually). When a backbone update changes a `gbif_taxon_key` (taxon split, merge, synonym promotion), NC's `concept_id` anchors may become stale. A Backbone Sync policy defines how NC handles backbone version updates. Recommended: annual review, no automatic updates, human-supervised remapping.

**Addition 4 — GBIF Evidence Record audit.** A periodic check that `gbif_occurrence_count` caps and `gbif_taxon_key` presence signals continue to satisfy the CI Constitution bias mitigation requirement. This is a governance audit, not a code change.

### VI.3 What Stays the Same

No changes to:
- `workers/taxon_discovery_worker/` (no adapter to add)
- `workers/illustration_opportunity_worker/` (no content writes to add)
- `workers/shared_media_adapter/` (GBIF never enters this path)
- Institution Factory sequence (GBIF is not assigned an institution number)

GBIF remains governed solely by Standards Constitution v1.0 and the CI Constitution bias mitigation clause. It does not acquire Rights Matrix governance, Institution Factory governance, or M36 write-path governance.

---

## VII. Governance Implications Summary

| Question | Ruling |
|---|---|
| Governance class | Identity and Evidence Authority (not Content Institution) |
| Institution Factory stages | None — not applicable |
| Institution number | Not assigned |
| Adapter module | None — not created |
| Rights matrix | None — replaced by GBIF Evidence Policy (Standards Amendment) |
| M36 source_item writes | Prohibited |
| M36 media_rights writes | Prohibited |
| Occurrence data storage | Permitted — evidence fields only, schema enumerated in Section V.2 |
| Media ingestion | Prohibited — permanent ruling |
| Backbone taxonomy use | Permitted — CC0, full use |
| CI Constitution constraint | Active — occurrence count cap at 100, anti-correlation rule |
| IFC-1 applicability | Not applicable — GBIF is not subject to IFC-1 |
| SA-9 applicability | Not applicable — GBIF is not an M36 source slug |
| Caching policy | Required before full catalog harvest scale |
| Backbone sync policy | Required — annual review cycle |

---

## VIII. Open Questions

**OQ-1 — GBIF authenticated API access.** NC currently uses the unauthenticated GBIF API. At catalog harvest scale, authenticated access (higher rate limits) may be required. A GBIF Data User Agreement acceptance and registered application ID are prerequisites for authenticated access. This is an operational question, not a governance question, but should be tracked.

**OQ-2 — GBIF DwC dataset downloads for bulk backbone resolution.** For large-scale taxon key lookups, GBIF's bulk DwC dataset downloads (available via GBIF.org data download API) may be more efficient than per-taxon API calls. These downloads are governed by the GBIF Data User Agreement (CC0 datasets are free; CC BY requires citation). Whether NC should use bulk downloads versus live API calls is an architecture decision deferred to the caching policy governance document.

**OQ-3 — GBIF multimedia endpoint monitoring.** GBIF's multimedia content mix changes as contributing institutions update their licenses. iNaturalist's CC BY-NC dominance could shift if iNaturalist changes default license settings, or if CC0-contributing institutions increase their upload volume. NC should monitor GBIF multimedia license distribution annually to detect if the Content Institution disqualification ever materially weakens. This monitoring is passive; it does not authorize ingestion without a new DD.

---

## IX. Decision Articles

**Article 1 — Governance Classification.** GBIF is classified as an Identity and Evidence Authority under Standards Constitution v1.0. This classification is permanent. GBIF is not a content institution and is not subject to the Institution Factory pipeline.

**Article 2 — Content Institution Disqualification.** GBIF is permanently disqualified as a content institution on five independent grounds: wrong content type, wrong license distribution, aggregator architecture, provenance duplication risk, and doctrine prohibition. Reinstatement requires DD-GBIF-002 that affirmatively reverses each ground.

**Article 3 — Media Ingestion Prohibition.** No GBIF-hosted image, video, or audio record may be ingested as NC commercial inventory. This prohibition is permanent. No adapter, SA, or pilot is authorized for GBIF media ingestion.

**Article 4 — Occurrence Record Governance.** GBIF occurrence data may be stored in NC as evidence metadata, subject to the schema enumerated in Section V.2. The CI Constitution cap (`gbif_occurrence_count_capped = min(count, 100)`) is load-bearing governance. Modifications require a CI Constitution amendment.

**Article 5 — GBIF Backbone Taxonomy.** The GBIF Backbone Taxonomy (CC0) is available for full use in taxon identity anchoring. NC's `gbif_taxon_key` field is the canonical biological anchor identifier for the `illustration_opportunities.concept_id` relationship.

**Article 6 — Source Role Designation.** GBIF's governed source role in the illustration opportunity pipeline is `"validation_only"`. This designation is codified in `workers/illustration_opportunity_worker/discover.py` provenance output. No future code change may promote GBIF to `"primary_discovery"` or `"content"` without a DD-GBIF-002 governance document.

**Article 7 — Standards Amendment Required.** The GBIF Evidence Policy (Section V) must be formalized as a Standards Constitution amendment before full catalog harvest scale. At pilot scale, the existing implementation satisfies the evidence governance requirement informally. At production scale, the formal amendment is required.

**Article 8 — No SA-9 Applicability.** GBIF does not receive an M36 source slug. It is not added to the `build_rights_evidence` source slug registry. SA-9 does not apply to GBIF.

**Article 9 — Caching Policy Prerequisite.** A GBIF API caching policy (minimum TTL defined, cache layer specified) is required before full catalog harvest scale. This prerequisite does not apply to pilot operations at the current 50K taxon candidate ceiling.

**Article 10 — Prior Ruling Ratification.** Institution Coverage Audit v1 OQ-3 and DD-ALA-001 Article 6 are ratified as permanent precedents. Both documents established GBIF's identity-only governance role and confirmed that GBIF access does not alter per-record license designations of contributing institutions.

---

## X. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☑ APPROVED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*DD-GBIF-001 — drafted 2026-06-11*  
*Prior rulings: Institution Coverage Audit v1 OQ-3 · DD-ALA-001 Article 6*  
*Governing standards: Standards Constitution v1.0 · Commerce Intelligence Constitution v1.2*  
*Decision: FORMALIZE AS IDENTITY AND EVIDENCE AUTHORITY — not a content institution*
