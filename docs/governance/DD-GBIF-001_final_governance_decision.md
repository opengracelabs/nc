# DD-GBIF-001: Final Governance Decision

| Field | Value |
|---|---|
| Document | DD-GBIF-001-FGD |
| Version | 1.0 |
| Status | **RATIFIED** |
| Closes | DD-GBIF-001 v1.0 (DRAFT) · SA-GBIF-001 v1.0 (DRAFT) |
| Authority | Standards Constitution v1.0 · SA-GBIF-001 · Institution Coverage Audit v1 · DD-ALA-001 |
| Date | 2026-06-11 |

---

## DECISION

**APPROVED**

GBIF is ratified as an **Identity and Evidence Authority**. Both DD-GBIF-001 and SA-GBIF-001 are ratified in full. All five ratification tasks pass with no conditions and no open items that block ratification. Three operational open questions survive (Section VI) but none affect the governing framework or require amendments before production use.

---

## I. Ratification Task 1 — Identity and Evidence Authority Classification

**Ruling: CONFIRMED**

GBIF is classified as an Identity and Evidence Authority. It is not a Content Institution. This classification is permanent.

**Basis for confirmation:**

DD-GBIF-001 Section II.4 ratified this classification after evaluating three options (Identity Authority, Content Institution, Hybrid) and finding five independent disqualifiers against Content Institution status:

1. Wrong content type — GBIF's image corpus is contemporary scientific photography, not Golden Age illustration (1750–1900)
2. Wrong license distribution — iNaturalist CC BY-NC dominance; IFC-1 unsatisfiable at scale
3. Aggregator architecture — GBIF holds no primary commercial rights; all rights trace to contributing institutions
4. Provenance duplication — GBIF's CC0 images originate from the same institutions already in NC's pipeline
5. Doctrine prohibition — NC is not a biodiversity system (Platform Identity doctrine)

The Hybrid option is rejected as a subset of the Content Institution option, inheriting all five disqualifiers.

DD-GBIF-001 Article 1 is ratified: the Identity and Evidence Authority classification is **permanent**. Reinstatement as Content Institution requires a new DD (DD-GBIF-002) that affirmatively reverses each of the five disqualifiers above. No such document may be initiated without Principal Architect sign-off.

**SA-GBIF-001 Article 18 opening ruling — "Evidence Authority: Consume and Map" — is ratified.** GBIF data is consumed for two governed purposes: taxon identity anchoring and place-relevance evidence. It is never written to the M36 content pipeline in any form.

**Formal extension confirmed:** The Standards Constitution v1.0 designation "Identity and Reference Authority" is extended to "Identity and Evidence Authority" to reflect GBIF's active role in place-relevance scoring. This extension does not create a new governance tier; it clarifies the governed scope of GBIF data stored in NC.

---

## II. Ratification Task 2 — Permanent Prohibitions

**Ruling: CONFIRMED — all four prohibitions unconditional and permanent**

| Prohibition | Authority | Status |
|---|---|---|
| No media ingestion | DD-GBIF-001 Article 3; SA-GBIF-001 I-1, I-5 | PERMANENT — no special-case exception exists for CC0 GBIF images |
| No M36 writes (any type) | DD-GBIF-001 Article 1; SA-GBIF-001 I-1, I-2 | PERMANENT — GBIF data never enters M36 content pipeline |
| No `source_item` creation | SA-GBIF-001 I-1 (enumerated) | PERMANENT — `source_item` is a content inventory record; GBIF is evidence metadata |
| No `media_rights` creation | SA-GBIF-001 I-1 (enumerated) | PERMANENT — GBIF is not a rights-bearing content source |

**IFC-1 applicability note:** IFC-1 (the PD hard gate) does not apply to GBIF. IFC-1 governs M36 content records. GBIF evidence records are not M36 content records. The prohibition on GBIF M36 writes predates and supersedes IFC-1's scope — it is a doctrine ruling, not an IFC enforcement matter. A future IFC-1 review may not relax the GBIF prohibition; the prohibition derives from DD-GBIF-001 Article 3 independently of IFC-1.

**SA-9 note:** GBIF is not assigned an M36 source slug. `build_rights_evidence(source_slug="gbif")` is explicitly prohibited (SA-GBIF-001 I-2). SA-9 does not apply to GBIF. No extension to SA-9 for GBIF is required.

---

## III. Ratification Task 3 — License Policy

**Ruling: CONFIRMED — with CC BY-NC precision ruling below**

The license policy table from SA-GBIF-001 Policy 4 is ratified:

| Data product | License | NC use classification |
|---|---|---|
| GBIF Backbone Taxonomy | CC0 | **ALLOWED** — unrestricted; full taxon anchoring use |
| GBIF occurrence records (CC0 datasets) | CC0 | **ALLOWED** — evidence use; factual data, no copyright risk |
| GBIF occurrence records (CC BY datasets) | CC BY | **ALLOWED** — evidence use; citation required in provenance payload |
| GBIF occurrence records (CC BY-NC datasets) | CC BY-NC | **BLOCKED for commercial scoring** — see precision ruling below |
| GBIF media (any source) | Any | **BLOCKED** — media ingestion permanently prohibited |

**CC BY-NC precision ruling:**

CC BY-NC occurrence records occupy a governed boundary position. They are not blocked absolutely — the factual data rule (SA-GBIF-001 Policy 4 Section 4.3) establishes that occurrence counts are factual, not copyrightable, and that NC's evidence use is not reproduction of a substantial portion of the GBIF database. However:

- CC BY-NC occurrence data **may not be used as a scoring input** for commercial inventory prioritization, COS construction, or any NC output that results in a commercial transaction
- CC BY-NC occurrence data **may be used** for identity confirmation (taxon key validation) where the output is not a commercial score
- At current NC scale, the majority of GBIF occurrence evidence is CC0 or CC BY. CC BY-NC datasets are a minority. NC does not presently track per-dataset license in occurrence evidence records
- **Prerequisite before catalog scale:** Before full catalog harvest, NC must implement per-dataset license tracking in GBIF evidence records to enforce the CC BY-NC commercial scoring block. At pilot scale (≤500 taxon candidates), the CC0/CC BY majority renders this a low-risk open question rather than a blocking condition

This precision ruling is added as the governing interpretation of DD-GBIF-001 Section III.1's "Conditional — evidence use only; prohibited for commercial inventory" ruling. It supersedes any looser reading.

**License passthrough rule — confirmed:** GBIF does not grant NC commercial rights for any contributed content. DD-ALA-001 Article 6 (GBIF access does not convert iNaturalist licenses) is extended to all GBIF data. This is Invariant I-6 in SA-GBIF-001.

---

## IV. Ratification Task 4 — Occurrence Count Cap Governance

**Ruling: CONFIRMED — load-bearing CI Constitution constraint; removal requires amendment**

The `gbif_occurrence_count` cap at 100 (`gbif_occurrence_count_capped = min(count, 100)`) is ratified as:

1. **SA-GBIF-001 Invariant I-3** — unconditional enforcement in all scoring contexts
2. **CI Constitution v1.2 compliance mechanism** — prevents high-occurrence species (common sparrows, pigeons, domestic cattle) from receiving disproportionate COS purely from GBIF documentation abundance
3. **Load-bearing governance** — the cap is not an implementation convenience. Removing it without a CI Constitution amendment is a constitutional breach regardless of stated intent

**Dual-field requirement confirmed:** Evidence records must store both:
- `gbif_occurrence_count` — raw count, preserved for audit
- `gbif_occurrence_count_capped` — capped count (≤100), the governed scoring input

The raw count must never be passed to a scoring function. A scoring function that receives the raw count rather than the capped count is a governance violation detectable in replay tests.

**Anti-contamination rule confirmed:** NC's Commercial Opportunity Score (COS) must not correlate with raw GBIF occurrence frequency. Periodic replay analysis revealing such correlation indicates either a cap bypass or a contaminated scoring signal, and is a CI Constitution v1.2 breach.

**`gbif_taxon_key` presence weight (0.30):** The 0.30 weight in discovery scoring is governed as an identity confirmation signal — confirming the taxon exists in the authoritative backbone — not as a biodiversity abundance signal. Its purpose is identity, not prevalence. This weight does not conflict with the anti-contamination rule; taxon key presence is binary (present/absent), not a frequency measure.

---

## V. Ratification Task 5 — Darwin Core Mapping Standard

**Ruling: CONFIRMED — Standards Constitution v1.0 Article 11 "Map" ruling applies**

Standards Constitution v1.0 Article 11 (Darwin Core) applies to GBIF data consumed by NC. Its ruling of "Map" — NC maps DwC terms for the biological intelligence layer only — is confirmed and extended by SA-GBIF-001.

**Field mapping confirmation:**

| NC field | DwC term | SA-GBIF-001 field | Ruling |
|---|---|---|---|
| `illustration_opportunities.concept_id` (biological) | `dwc:taxonID` | `gbif_taxon_key` | CONFIRMED — stable integer; GBIF is DwC-compliant |
| Taxon name | `dwc:scientificName` | `gbif_canonical_name` | CONFIRMED — stored at resolution time |
| Taxon rank | `dwc:taxonRank` | `gbif_taxon_rank` | CONFIRMED — kingdom → species |
| Kingdom | `dwc:kingdom` | `gbif_kingdom` | CONFIRMED |
| Wikidata QID | GBIF → Wikidata mapping | `wikidata_qid` | CONFIRMED — advisory; NC resolution takes precedence |
| Occurrence evidence source | `dwc:occurrenceID` (FK reference) | `gbif_source_url` | CONFIRMED — provenance reference, not stored occurrence ID |
| BHL publication | `dwc:bibliographicCitation` | (unchanged) | CONFIRMED |

**What NC does not adopt from DwC — confirmed:**
- Occurrence records: NC does not publish sighting data
- Observation events: no field observations in NC pipeline
- Sampling framework: not applicable
- MeasurementOrFact: NC quality scores are commercial, not scientific

**Consumption rule confirmed (Article 11):** NC reads DwC-compliant records from GBIF as evidence for biological-anchored opportunities. DwC terms are consumed, not stored natively — they inform `concept_id` resolution and are preserved in `source_record.raw_payload`.

**SA-GBIF-001 addition to Article 11:** The addition of `gbif_backbone_version` and `gbif_resolution_date` to the evidence schema (Policy 2, Section 2.3) extends Article 11 by adding backbone version tracking. These fields are not DwC terms but are required for backbone sync governance. They do not conflict with the Article 11 ruling.

**Backbone sync integration with DwC:** When backbone updates change a `dwc:taxonID` (taxon split, merge, synonym promotion), NC's stored `concept_id` value may become stale. The SA-GBIF-001 annual backbone sync audit process (Policy 2, Section 2.4) is the governed response. The DwC `dwc:taxonID` mapping is stable at resolution time; the annual audit corrects accumulated drift.

---

## VI. Surviving Open Questions

Three open questions from DD-GBIF-001 Section VIII survive this ratification. None block the APPROVED decision. All are operational questions to be resolved before full catalog harvest.

**OQ-1 — GBIF authenticated API access.** At catalog scale (50K+ taxon candidates), unauthenticated API access (≈1 req/sec) will be insufficient. NC must register an application with GBIF before catalog harvest to obtain authenticated access and higher rate limits. This is an operational prerequisite, not a governance question. No SA is required.

**OQ-2 — GBIF DwC bulk download vs. live API.** For large-scale taxon key lookups, GBIF bulk DwC dataset downloads may be more efficient than per-taxon API calls. SA-GBIF-001 Policy 3 governs both paths (API and bulk). The architecture decision between them is deferred to the caching policy governance document. No new SA is required to authorize bulk downloads — the CC BY citation requirement in SA-GBIF-001 Policy 4 Section 4.4 governs that path.

**OQ-3 — GBIF multimedia license distribution monitoring.** The Content Institution disqualification (Disqualifier 2) rests in part on iNaturalist CC BY-NC dominance. NC should monitor GBIF multimedia license distribution annually to detect material shifts. If CC0 contributions increase to exceed CC BY-NC contributions, a monitoring report should be filed — not a new DD. The media prohibition remains until DD-GBIF-002 is issued regardless of license distribution changes.

---

## VII. Ratification Status

### DD-GBIF-001 v1.0

All ten articles are ratified without amendment. The only addition to the governing framework is the CC BY-NC precision ruling in Section III above, which governs implementation of DD-GBIF-001 Section III.1 and does not require a DD amendment.

### SA-GBIF-001 v1.0

All four policies and eight invariants are ratified without amendment. SA-GBIF-001 is added to the Standards Constitution v1.0 as Article 18. The article number is confirmed: the Standards Constitution's Darwin Core article (Article 11) and Wikidata article (Article 16) are prior art; Article 18 is the first GBIF-specific governance article.

---

## VIII. Governance Framework — Final State

| Dimension | Ratified Ruling |
|---|---|
| Governance class | Identity and Evidence Authority — permanent |
| Content Institution disqualification | Permanent — 5 independent grounds |
| Institution number | Not assigned — permanent |
| Institution Factory | Not applicable — permanent |
| M36 source writes | Prohibited — permanent |
| Media ingestion | Prohibited — permanent |
| Source slug (SA-9) | Not applicable — permanent |
| Backbone taxonomy | CC0 — full use — permanent |
| Occurrence data (CC0/CC BY) | ALLOWED for evidence use — permanent |
| Occurrence data (CC BY-NC) | BLOCKED for commercial scoring; ALLOWED for identity confirmation |
| Media data (any license) | BLOCKED — permanent |
| Occurrence count cap | 100 (hard) — CI Constitution load-bearing — requires amendment to change |
| Source role | `"validation_only"` — immutable without DD-GBIF-002 |
| Darwin Core mapping | Article 11 "Map" ruling — confirmed |
| `dwc:taxonID = gbif_taxon_key` | Confirmed |
| Backbone sync | Annual review cycle — no continuous automated remapping |
| Caching policy | Mandatory before catalog scale (24h occurrence, 30d backbone) |
| CC BY citation | Required when bulk downloads contain CC BY datasets |

---

## IX. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | **APPROVED** | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*DD-GBIF-001-FGD — 2026-06-11*  
*Closes: DD-GBIF-001 v1.0 · SA-GBIF-001 v1.0*  
*Authority: Standards Constitution v1.0 Article 11 and Article 18 · Commerce Intelligence Constitution v1.2 · DD-ALA-001 Article 6 · Institution Coverage Audit v1 OQ-3*
