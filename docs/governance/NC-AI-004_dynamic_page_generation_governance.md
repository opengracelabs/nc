# NC-AI-004: Dynamic Page Generation Governance

| Field | Value |
|---|---|
| Document | NC-AI-004 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | NC-AI-001 · NC-AI-002 · NC-WEB-001 · NC-PRODUCT-001 · NC-FIRST-SALE · SA-GEONAMES-001 · SA-OSM-001 |
| Reference note | DD-NASA-001 does not exist as a formal decision document. NASA governance for dynamic copy is drawn from NC-FIRST-SALE (FS-001/FS-002), NC-WEB-001 §IV.1/IV.5, NC-PRODUCT-001 §IV, and `apps/web/lib/governed-content.ts`. A formal DD-NASA-001 is a condition of this document (§XVI.C-1). |
| Governs | All AI-generated copy for NC web pages (Homepage, Story, Product, Educational, Tourism/Place) |
| **Decision** | **APPROVE WITH CONDITIONS** |

---

## Core Rule

> The model may write the words on the page, but the graph and source evidence remain the truth.

No model output may assert, establish, or influence: rights status, provenance, asset source, attribution strings, entity identifiers (GeoNames ID, GBIF taxon key, Wikidata QID), or product activation state. These are canonical facts resident in PostgreSQL. The model receives them as read-only context and may reference them in generated text. It may never produce them.

This rule is an extension of NC-AI-001 core doctrine, which is itself an extension of Foundation Model Constitution v1.0 Article 1.3 and Invariants FM-1 through FM-4.

---

## I. Scope

NC-AI-004 governs the generation, validation, review, publication, and rollback of AI-assisted copy for five web page families:

1. **Homepage copy** — hero copy, value proposition, featured place/asset editorial
2. **Story page copy** — editorial narrative for asset stories (Earthrise story, place stories)
3. **Product page copy** — product descriptions, variant copy, CTA copy, COA copy
4. **Educational copy** — educational summaries, discovery guides, lesson pack content
5. **Tourism/place copy** — place introductions, contextual guides, species/heritage copy

For each family this document defines: source grounding requirements, attribution preservation protocol, prohibited phrase validation requirements, human review gates, publication snapshot requirements, and rollback path.

**Out of scope:** Map tile generation (SA-OSM-001), media rights determination (FM-4, NC-AI-002), product activation (FM-5), collection publication state, pricing, and any content for deferred assets (§II.5).

---

## II. Pre-Generation Invariants

Before any model call is authorized for any page family, the following invariants must hold. Failure of any invariant is a grounding layer block — the model call is rejected, logged, and queued for PA review.

### II.1 Rights Invariant (IFC-1 + FM-4)

Every asset referenced in the generation request must have:
- `media_rights.rights_status = 'verified_pd'`
- `media_rights.human_verified = TRUE`

The model receives the rights record as read-only context. It does not determine rights status. It does not mention rights status in generated text except by referencing the injected governed string. Any reference to rights in generated text must use the exact formula from the governed constants layer — no paraphrase permitted.

### II.2 Attribution Invariant (AI-ATT-1)

Attribution strings are **retrieved from the governed constants layer, never generated**. For every asset type:

| Asset type | Governed constant | Source |
|---|---|---|
| NASA (Earthrise) | `NASA_EARTHRISE_CREDIT` · `NASA_NONENDORSEMENT` | `governed-content.ts` + Python `earthrise_demo.py` |
| NASA (other) | `"Image credit: NASA. NASA does not endorse this product."` | Injected from source record |
| NOAA | `"Credit: NOAA/[Division]"` | Injected from source record `division` field |
| GeoNames | `"Geographic data © GeoNames (geonames.org) — CC BY 4.0"` | SA-GEONAMES-001 §II.1 |
| OSM (Mapbox) | `"© OpenStreetMap contributors   |   Map data provided by Mapbox"` | SA-OSM-001 §III.1 |
| BHL | `"Source: Biodiversity Heritage Library"` | Injected from source record |
| Institution (general) | Per institution DD attribution field | Injected from `source_items.attribution_required` |

These strings are injected as `attribution_requirements` on the `GroundingSource` and must appear in the output's `attribution_requirements` field intact. The model does not write them in the generated text body — they appear in the attribution block rendered by the template layer, separate from the generated text body.

### II.3 Grounding Invariant (NC-AI-001 §V.1)

Retrieval is unconditional for all five page families. The generation request must include:

| Page family | Required retrieval |
|---|---|
| Homepage | Featured asset records · Governed constants for any featured federal asset |
| Story page | Asset record(s) with rights status · Creator record · Governed attribution constants · Place record if applicable |
| Product page | Product spec · Asset record · Rights record (read-only) · Activation target status · NC-WEB-001 §IV copy rules · Prohibited phrases register |
| Educational copy | Asset record(s) · GBIF biological evidence (text only, no media) · Place record if geo-anchored · Educational standard alignment (if applicable) |
| Tourism/place copy | Place record (GeoNames ID, feature code, coordinates) · Asset record(s) · Heritage designation data (text, not FM-generated) · GBIF evidence (text counts) · Co-attribution order requirements (SA-GEONAMES-001 §III.1) |

A model call that does not include required retrieval is rejected by the grounding layer before execution.

### II.4 Entity ID Invariant (NC-AI-001 §XV.3)

Any FM output that contains a numeric string matching known entity ID patterns (GeoNames ID, GBIF taxon key, Wikidata Q-number, source record ID) must be validated against canonical sources before acceptance. An FM-invented entity ID that does not resolve in `places.geonames_id`, `source_items.source_record_id`, or `gbif_evidence.gbif_taxon_key` is rejected. The output validation layer performs this check.

### II.5 Deferred Asset Invariant (FS-002 + NC-WEB-001 §IV.3)

No deferred asset may appear in generated copy in a way that implies availability, commercial access, or product rights. The deferred asset register is canonical:

| Asset / group | Governing block |
|---|---|
| Thomas Moran paintings | DD-SMITHSONIAN-001 required |
| Canaletto Venice paintings | No DD — not eligible |
| HMS Beagle chart | DD-TNA-001/UKHO-001 required |
| de' Barbari 1500 Venice map | Museo Correr — no DD |
| St. Mark's Basilica elevation | Unidentified institution |
| ESA/Copernicus imagery | DD-ESA-001 required |
| Darwin's sketch notebook | Cambridge UL — no DD |
| Cook's Pacific chart | DD-TNA-001 required |
| NARA Collector Edition / Apollo 8 Mission Plan | NARA Sprint 1 required |

**Pre-generation check:** The grounding layer checks the `activation_targets` table. Any asset in the generation request that does not have `activation_targets.status = 'active'` is rejected. A deferred asset check against the deferred asset register is run before the grounding validation step.

---

## III. The Generation Pipeline (all page families)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. GENERATION REQUEST                                          │
│     task_type · actor · quality_tier · page_family             │
│     page_url · page_version_target · inputs                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. PRE-GENERATION CHECKS (grounding layer — rejects here)      │
│     □ II.1 Rights invariant (all referenced assets)            │
│     □ II.2 Attribution constants retrieved (not to generate)   │
│     □ II.3 Required retrieval present                          │
│     □ II.4 No entity ID injection required from FM             │
│     □ II.5 No deferred assets in request                       │
│     □ Policy lookup: human_review_required=TRUE for page family │
│     □ No user behavioral data in inputs                        │
└────────────────────────┬────────────────────────────────────────┘
                         │ grounded request
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. PROMPT CONSTRUCTION                                         │
│     Governed constants injected as literals                     │
│     Prohibited phrases register injected as instruction         │
│     Co-attribution order injected (SA-GEONAMES-001 §III.1)     │
│     Source record IDs injected for citation grounding           │
│     Deferred asset list injected as hard constraints            │
└────────────────────────┬────────────────────────────────────────┘
                         │ governed prompt
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. MODEL EXECUTION                                             │
│     Provider selected per NC-AI-001 §VIII task routing          │
│     Sprint 1: DeterministicMockProvider (no external calls)     │
│     fm_inference_record written before execution                │
└────────────────────────┬────────────────────────────────────────┘
                         │ candidate output
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. OUTPUT VALIDATION (§IV — prohibited phrase validator)       │
│     □ Rights hallucination check                               │
│     □ NASA/NOAA endorsement phrase check                       │
│     □ NARA/Earthrise false attribution check                   │
│     □ Deferred asset availability implication check            │
│     □ Ungrounded claim detection (entity IDs, provenance)      │
│     □ Attribution string generation check                      │
│     □ Rollback trigger detection                               │
│     If any check FAILS → rejected, logged, NOT queued          │
└────────────────────────┬────────────────────────────────────────┘
                         │ validated candidate
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. HUMAN REVIEW QUEUE                                          │
│     fm_candidate_record written: status = 'pending'            │
│     publication_allowed = FALSE (hard)                         │
│     Reviewer assigned per page family gate (§VII)              │
└────────────────────────┬────────────────────────────────────────┘
                         │ approved candidate
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  7. PUBLICATION                                                 │
│     Human marks candidate: status = 'approved'                 │
│     Publication snapshot written (§VIII)                       │
│     page_copy_version record created                           │
│     Previous version archived (rollback path preserved, §IX)   │
│     Attribution blocks injected by template (not by model)     │
└────────────────────────┬────────────────────────────────────────┘
                         │ live page
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  8. POST-PUBLICATION AUDIT                                      │
│     Monthly sample audit (10% of published AI copy)            │
│     Rollback triggered on any verified prohibited phrase find   │
│     Rollback triggered on any rights error in source record     │
└─────────────────────────────────────────────────────────────────┘
```

---

## IV. Prohibited Phrase Validation (C-5 Implementation)

This section is the implementation specification for NC-AI-001 Condition C-5 and the NC-AI-002 Finding F-1. The prohibited phrase validator runs at Step 5 (output validation) on every generation output before it enters the human review queue.

### IV.1 Rights Hallucination Register

A rights hallucination is any model output that contains a novel rights determination — i.e., asserts that an asset has a particular rights status without receiving that status as retrieved input context. Rights language from the governed constants layer is permitted (it was injected, not generated).

**Patterns that trigger rejection:**

| Pattern | Reason |
|---|---|
| `"is public domain"` asserted by the model as original text | FM-4 — rights determination |
| `"rights cleared"` / `"rights verified"` / `"rights confirmed"` | FM-4 — rights assertion |
| `"legally free to use"` / `"free to reproduce"` | FM-4 — rights advice |
| `"PD confirmed"` / `"PD verified"` / `"confirmed public domain"` | FM-4 — rights assertion |
| `rights_status = 'verified_pd'` as asserted text | FM-4 — canonical field assertion |
| Any assertion about the rights status of a deferred asset | FM-4 + FS-002 |
| `"CC0"` asserted without retrieved CC0 record as context | FM-4 — rights assertion |

**Exception:** The phrase "public domain" used in an informational sentence that *cites* the injected rights basis string ("treated as a public domain work under 17 U.S.C. § 105") is permitted — the injected constant establishes the rights context; the generated text references it. The distinction is between `asserting` rights and `citing` retrieved rights basis.

**Implementation:** Rights language detection via regex + semantic pattern matching on all generated output text before Step 6. Any match triggers immediate rejection (not queued as a finding) and logs a `rights_hallucination_attempt` event in `ai_audit_event`.

### IV.2 Federal Agency Endorsement Register

Source: NC-WEB-001 §IV.1 · NC-PRODUCT-001 §IV · NC-FIRST-SALE FS-001

**Hard-block phrases (immediate rejection, cascade alert):**

| Phrase | Scope | Consequence |
|---|---|---|
| "NASA-endorsed" | Any | Cascade deactivation of ALL federal-source assets |
| "NASA-certified" | Any | Same |
| "NASA-approved" | Any | Same |
| "Official NASA product" / "Official NASA print" | Any | Same |
| "Verified by NASA" | Any | Same |
| "NASA archival quality" | Any | Same |
| "In partnership with NASA" | Any | Same |
| "NOAA-certified" | Any | Same |
| "NOAA-endorsed" | Any | Same |
| "In partnership with NOAA" | Any | Same |
| Any phrase suggesting federal agency review of NC product quality | Any | Same |
| "NASA has certified" / "NOAA has approved" | Any | Same |

**Consequence of any cascade trigger:** Immediate page takedown of ALL pages displaying federal-source assets. Review by PA before reinstatement. This consequence is not graduated — one endorsement phrase in any AI-generated output triggers the full cascade.

**Implementation:** Exact string match (case-insensitive) + proximity pattern match (e.g., "NASA" within 5 tokens of "partner\|certified\|approved\|official\|endorsed\|verified") on all generated output text.

### IV.3 NARA/Earthrise False Attribution Register

Source: NC-FIRST-SALE FS-001 · NC-WEB-001 §IV.5

**Hard-block patterns (rejection + FS-001 audit event):**

| Phrase / pattern | Reason |
|---|---|
| "National Archives" in context of Earthrise | FS-001 — NARA attribution for NASA asset |
| "NARA" adjacent to "Earthrise" | FS-001 |
| "NARA: Verified archival source" | FS-001 — exact prohibited construction |
| "Archives verified" in Earthrise context | FS-001 |
| "archival record" in Earthrise sourcing context | FS-001 |
| "Earthrise from the National Archives" | FS-001 |
| "AS08-14-2383" attributed to NARA | FS-001 |

**Implementation:** Earthrise context detection (source_record_id = "AS08-14-2383" or title contains "Earthrise") activates NARA phrase block. NARA phrases in any Earthrise-context output are hard-blocked regardless of surrounding text.

### IV.4 Deferred Asset Availability Register

Source: NC-FIRST-SALE FS-002 · NC-WEB-001 §IV.3

**Hard-block patterns:**

| Pattern | Example |
|---|---|
| Deferred asset name + availability implication | "Thomas Moran's Grand Canyon is available from NC" |
| Deferred asset name + product language | "purchase the Canaletto Venice print" |
| Deferred asset name + price or ordering language | "the HMS Beagle chart is $X" |
| "Collector's Edition" | Until NARA Sprint 1 complete |
| "30×30 Acrylic" or "Collector Acrylic" | Until NARA Sprint 1 complete |
| Venice institution claims (Canaletto, de' Barbari) | Until DD-MET-001/AIC-001/CMA-001 ratified |
| ESA/Copernicus imagery availability | Until DD-ESA-001 ratified |

**Implementation:** Deferred asset name list injected as a prohibited phrase list in the prompt (hard instruction). Output validation runs deferred asset regex after generation. Match → rejection + FS-002 audit event.

### IV.5 Ungrounded Claim Register

**Rejection patterns for claims that are not grounded in retrieved evidence:**

| Pattern | Test |
|---|---|
| Species name not in GBIF evidence context | Biological name that does not appear in retrieved GBIF evidence text |
| Place claim with no retrieved place record | Geographic assertion about a place with no `places` record in retrieval context |
| Creator claim with no retrieved creator record | "Painted by X" where X is not in retrieved `source_items.illustrator` context |
| Date claim with no retrieved date | "from the year X" where X is not in retrieved source record |
| Institution claim with no retrieved institution | "held at [institution]" where institution is not in retrieved source record |
| Heritage designation claim | "UNESCO World Heritage Site" — designation must come from governed place data, not FM assertion |

**Implementation:** Cross-reference validation between generated text named entities (NER pass) and the retrieval context provided. Entities in generated text that have no counterpart in the retrieval context trigger an `ungrounded_claim` warning (not immediate rejection — queued for reviewer attention as a finding, not a hard block, since NER is imperfect).

---

## V. Page Family Specifications

### V.1 Homepage Copy Generation

**Task type:** `public_website_copy`
**Policy:** `human_review_required = TRUE` · `grounding_required = TRUE` · `publication_allowed_by_default = FALSE`
**Primary model (live):** Claude (NC-AI-001 §VIII.8)
**Cost tier:** API_STANDARD

**Generation inputs (required):**

| Input | Source |
|---|---|
| Featured asset metadata (if asset appears in hero) | `source_items` PostgreSQL |
| Rights record (if federal asset in hero) | `media_rights` (read-only) |
| Governed attribution constants (if NASA/NOAA asset in hero) | `governed-content.ts` / governed constants layer |
| Activation targets (featured products) | `activation_targets` where `status = 'active'` only |
| Prohibited phrases register (§IV) | NC-AI-004 §IV |
| Brand voice guidelines | NC-AI-004 §VI |
| Phase gate status | Phase 0: Earthrise only; Phase 1+: per NC-WEB-001 §II |

**Permitted generated copy zones:**

| Zone | What the model may write |
|---|---|
| Hero headline | Value proposition, platform identity statement |
| Hero subheading | Editorial mission statement |
| Featured editorial module | 1–3 sentence description of featured place or asset |
| CTA copy | Button label, CTA subtext (must not promise availability of non-active products) |
| Section introductions | "Places", "Collections", "Stories" section editorial copy |

**Prohibited by generation:**

| What | Rule |
|---|---|
| Any homepage copy for deferred assets | FS-002 |
| Product availability claims for non-active products | IFC-1 + FM-5 |
| "Coming to NC" claims for unconfirmed institution partnerships | No speculative provenance |
| NASA/NOAA endorsement language | §IV.2 |
| Attribution strings | AI-ATT-1 — attribution is template-injected, not generated |
| Price, edition count, or stock claims | Not a model output domain |

**Human review gate:** PA review before any homepage copy is published. Homepage is the primary trust and conversion surface.

---

### V.2 Story Page Copy Generation

**Task type:** `place_story`
**Policy:** `human_review_required = TRUE` · `grounding_required = TRUE` · `publication_allowed_by_default = FALSE`
**Primary model (live):** Claude (English) / Gemini (multilingual) — NC-AI-001 §VIII.4
**Cost tier:** API_STANDARD

**Generation inputs (required):**

| Input | Source |
|---|---|
| Asset record (all assets featured in story) | `source_items` PostgreSQL |
| Rights record for each asset | `media_rights` (read-only) |
| Creator record | `source_items.illustrator`, `illustrators` table |
| Place record (if place-anchored story) | `places` table, GeoNames data |
| Governed attribution constants (all federal-source assets in story) | Governed constants layer |
| GeoNames attribution (if place data used) | SA-GEONAMES-001 §II.1 |
| GBIF evidence text (if biological content) | SA-GBIF-001 — text/counts only, no media |
| Historical context (from retrieved source record, not FM-generated) | `source_items.description`, institution metadata |
| Prohibited phrases register | NC-AI-004 §IV |
| NC-WEB-001 §III per-page attribution rules | Per story page |

**Permitted generated copy zones:**

| Zone | What the model may write |
|---|---|
| Story introduction (lede) | Editorial framing of the asset's cultural or historical significance |
| Historical context | Contextual narrative grounded in retrieved creator/date/mission data |
| Place context | Geographic and ecological narrative grounded in retrieved place data and GBIF evidence |
| Pull quotes / section headers | Evocative copy grounded in retrieved context |
| Story footer call-to-action | "Explore the collection" / "Own this piece" linking to active product only |

**Critical rule for Earthrise story page:**

The Earthrise story (URL: `/stories/earthrise`) is governed by FS-001. Generated copy must:
- Describe the photograph using retrieved creator (`William Anders`), mission (`Apollo 8`), and date (`December 24, 1968`) from the source record
- Not assert NASA endorsement or partnership with NC
- Not reference NARA in any Earthrise sourcing context
- Not reference deferred assets (Moran, ESA/Copernicus) as available
- Not generate the `NASA_NONENDORSEMENT` string — it is template-injected below the story body

**Attribution placement for story pages:**
1. Per-asset NASA credit: inline below each NASA image (template-injected, exact governed string)
2. NASA nonendorsement: article footer (template-injected)
3. GeoNames: page footer if place data used (template-injected, not in story body)
4. OSM: map overlay if map shown (not in story body)

The model must not place attribution strings in the story body text. Attribution is structurally separated.

**Human review gate:** Curator review + editorial approval before publication. PA review for story pages that include product recommendations.

---

### V.3 Product Page Copy Generation

**Task type:** `product_copy`
**Policy:** `human_review_required = TRUE` · `grounding_required = TRUE` · `publication_allowed_by_default = FALSE`
**Primary model (live):** Claude (NC-AI-001 §VIII.3)
**Cost tier:** API_STANDARD (MASTERWORK tier: API_PREMIUM)
**Human gate:** Curator (all tiers) · PA + curator (MASTERWORK tier — two-human gate)

**This is the highest-stakes copy generation category.** Product copy directly influences purchase decisions and carries legal attribution obligations. FM-4, AI-ATT-1, and FS-001 all apply simultaneously.

**Generation inputs (required — unconditional):**

| Input | Source |
|---|---|
| Product specification | `activation_targets` record + NC-COMMERCE-001 product record |
| Asset record (featured asset) | `source_items` PostgreSQL |
| Rights record | `media_rights` — `rights_status`, `rights_basis`, `human_verified` (read-only) |
| Activation status confirmation | `activation_targets.status = 'active'` — must be verified before generation is authorized |
| Governed attribution constants | Governed constants layer |
| NC-WEB-001 §IV copy rules | Prohibited formulations, allowed formulations |
| Prohibited phrases register (§IV of this document) | Full register |
| Product line eligibility | NC-PRODUCT-001 §II per-line conditions |
| Federal nonendorsement doctrine | NC-PRODUCT-001 §IV (zero-tolerance cascade) |

**Permitted generated copy zones:**

| Zone | What the model may write |
|---|---|
| Product title | Short title for the product variant (curator selects from candidates) |
| Product description (hero) | 2–4 sentence narrative description of the asset and its significance |
| Product description (detail) | Technical specifications (print dimensions, paper, ink) — using retrieved spec data |
| Variant description | Short description for each product variant (framed, unframed, digital) |
| "Why this piece" copy | Editorial explanation of the asset's cultural/historical relevance |
| SEO metadata | Title tag, meta description candidates |

**Prohibited generated copy (product pages):**

| Prohibited | Rule |
|---|---|
| Rights claim not from retrieved basis string | FM-4 |
| NASA/NOAA endorsement phrases (full register, §IV.2) | Federal nonendorsement doctrine — cascade |
| "NARA archival source" for Earthrise | FS-001 |
| "Collector's Edition" | NARA Sprint 1 required |
| "30×30 Acrylic" variant | NARA Sprint 1 required |
| Price, stock count, edition number | Not a model output domain (commerce system) |
| Deferred asset product copy | FS-002 |
| "Royalty-free" / "Rights-free" / "License-free" | NC-WEB-001 §IV.2 |
| Product copy for `activation_targets.status ≠ 'active'` | FM-5 + IFC-1 |
| Attribution strings (generated) | AI-ATT-1 — template-injected |
| "governed" as a selling word | NC-WEB-001 §I (internal term, not customer language) |
| "Giclee" without accent | Quality standard |

**MASTERWORK tier rules (NC-PROD-001 — Earthrise Giclée):**

NC-PROD-001 is a MASTERWORK tier product. In addition to the above:
- Two-human gate (Curator + PA) required before publication
- API_PREMIUM model required (quality of final copy must not be cost-constrained)
- COA copy is governed by `NC-FIRST-SALE_COA_template.md` — the model generates *candidates* for curator review; the COA template text is authoritative
- "Includes Certificate of Authenticity" appears on the product page — template literal, not generated

---

### V.4 Educational Copy Generation

**Task type:** `education_module`
**Policy:** `human_review_required = TRUE` · `grounding_required = TRUE` · `publication_allowed_by_default = FALSE`
**Primary model (live):** Claude (NC-AI-001 §VIII.5)
**Cost tier:** API_STANDARD

**Generation inputs (required):**

| Input | Source |
|---|---|
| Asset record(s) | `source_items` PostgreSQL |
| Rights record | `media_rights` (read-only) |
| Place record (if geo-anchored) | `places` table, GeoNames data |
| GBIF taxon evidence (biological content) | GBIF API via SA-GBIF-001 — text/counts/taxon names only |
| Taxon scientific name | `gbif_evidence.canonical_name` — retrieved, not generated |
| Creator record | `illustrators` table |
| Historical period context | Retrieved from `source_items` metadata |
| Educational level target | Input parameter (K-12 level, university, general public) |
| Prohibited phrases register | NC-AI-004 §IV |
| Governed attribution constants (federal assets) | Governed constants layer |

**Permitted generated copy zones:**

| Zone | What the model may write |
|---|---|
| Learning objectives | Outcome statements grounded in the retrieved asset/place/species context |
| Contextual narrative | Historical, ecological, or cultural educational text |
| Discussion questions | Questions grounded in retrieved evidence |
| Glossary definitions | Terms grounded in retrieved evidence |
| Caption text | Educational captions for assets (not attribution — attribution is template-injected) |
| Discovery guide copy | Place/species discovery guide text grounded in retrieved data |

**Critical biological content rule:**

GBIF is the sole authority for biological evidence in NC (SA-GBIF-001). For educational content involving species:
- Taxon names must come from `gbif_evidence.canonical_name` (retrieved), not FM-generated
- Occurrence counts must come from `gbif_evidence.occurrence_count` (retrieved, capped at 100 per CI Constitution)
- Biological claims not grounded in retrieved GBIF evidence are flagged as `ungrounded_claim` by the output validator
- GBIF media is permanently excluded (SA-GBIF-001) — no species images from GBIF in educational content

**Prohibited:**

| Prohibited | Rule |
|---|---|
| Unsourced biological claims | SA-GBIF-001 — GBIF evidence authority |
| "Endangered" / "Critically Endangered" IUCN status not retrieved | Ungrounded conservation claim |
| Rights claims for educational license reuse | FM-4 |
| Educational packs for deferred assets | FS-002 |
| NASA/NOAA endorsement in educational context | §IV.2 |

**Human review gate:** Curator review + educational quality review before publication. Curator selects final from candidate variants.

---

### V.5 Tourism / Place Copy Generation

**Task type:** `place_story` (tourism variant)
**Policy:** `human_review_required = TRUE` · `grounding_required = TRUE` · `publication_allowed_by_default = FALSE`
**Primary model (live):** Claude (English) / Gemini (multilingual) — NC-AI-001 §VIII.6
**Cost tier:** API_STANDARD

**This is the most attribution-complex category.** Place pages carry the fullest co-attribution stack (NASA/NOAA asset credit + GeoNames CC BY 4.0 + OSM ODbL + institutional credits). All attribution is template-injected; none is generated.

**Generation inputs (required — unconditional):**

| Input | Source |
|---|---|
| Place record | `places.geonames_id`, `places.name`, `places.feature_code`, `places.country_code`, coordinates |
| GeoNames canonical name and coordinates | `places` table (GeoNames-derived, §V.5 note) |
| GeoNames feature code | `places.feature_code` — governs CI Constitution routing; must not be overridden |
| Heritage designations | Retrieved from governed place data — not FM-asserted |
| Asset records (all assets displayed on place page) | `source_items` PostgreSQL |
| Rights records | `media_rights` (read-only) |
| GBIF biological evidence | SA-GBIF-001 — text/counts, species list from `gbif_evidence` table |
| OSM tile configuration (display only) | Tile service parameters for rendering; NOT OSM data ingestion |
| Co-attribution order | SA-GEONAMES-001 §III.1 — injected as instruction, not generated |
| Governed attribution constants | All federal-source assets on the page |
| NOAA write cap status | `noaa_sprint3_write_count` — checked before GBR page generation (cap: 7 ALLOWED) |
| Prohibited phrases register | NC-AI-004 §IV |
| Phase gate status | Phase 1+ required for all place pages except Earthrise |

**§V.5 note — GeoNames canonical IDs (confirmed, must not be overridden by FM):**

| Place | Canonical GeoNames ID | Source |
|---|---|---|
| Yellowstone | 5843591 | GeoNames direct API (fcode=PRKA) — NC-DATA-001 supersedes FRR §III |
| Grand Canyon | 5296401 | Confirmed via Wikidata P1566, 2026-06-11 |
| Great Barrier Reef | 2164628 | Confirmed via Wikidata P1566, 2026-06-11 |
| Galápagos | 3658931 | Confirmed |
| Venice | 3164603 | Confirmed |
| Earthrise | No GeoNames ID | S-3 cosmic anchor exception — no GN attribution required |
| Papahānaumokuākea | TBD | Not confirmed — place page blocked until confirmed |

These IDs are canonical records in `places.geonames_id`. They are injected as retrieval context. The model must never assert, correct, or generate a GeoNames ID.

**Permitted generated copy zones:**

| Zone | What the model may write |
|---|---|
| Place introduction (lede) | Geographic and ecological framing paragraph |
| Heritage significance | Cultural/scientific significance narrative (grounded in retrieved designations) |
| Featured asset contextual copy | 1–3 sentences contextualizing the asset within the place (grounded in asset record) |
| Species/ecology copy | Biological narrative grounded in GBIF evidence text |
| Historical context | Historical narrative grounded in retrieved asset/institution metadata |
| Commerce contextual copy | "Explore the [Place] collection" — linking to active products only |
| "Coming soon" stub copy | For Phase 1+ places before full activation (not claiming availability) |

**Attribution placement for tourism/place pages (all template-injected — not generated):**

Per SA-GEONAMES-001 §III.1 co-attribution order:
1. Per-asset federal agency credit (NASA/NOAA) — adjacent to each asset
2. `Geographic data © GeoNames (geonames.org) — CC BY 4.0` — page footer, always visible
3. `© OpenStreetMap contributors | Map data provided by Mapbox` — map overlay, bottom-right
4. Institutional credits (BHL, NOAA, institution name) — adjacent to each asset or footer

**Prohibited on place pages:**

| Prohibited | Rule |
|---|---|
| Heritage designation claims not from retrieved data | Ungrounded claim |
| "UNESCO World Heritage Site" not retrieved from governed data | UNESCO does not endorse NC |
| OSM data stored in NC tables | OS-1 through OS-5 |
| GBIF media | SA-GBIF-001 |
| GeoNames ID assertion by model | Entity ID invariant (§II.4) |
| NOAA content beyond ALLOWED write cap (7) | SA-NOAA-002 |
| Wikidata Commons images | W-6 Commons boundary doctrine |
| Place page copy for Phase 0 (SA not yet ratified) | NC-WEB-001 §II |
| Tourism recommendations implying federal agency endorsement | §IV.2 |

**NOAA write cap gate (GBR page):** Before the Great Barrier Reef place page generation is authorized, the system must check `noaa_sprint3_write_count`. If the count is at or approaching 7 ALLOWED writes, PA must review before the generation request is authorized. This check is pre-generation, not post.

---

## VI. Brand Voice and Generation Constraints

All NC-AI-004 generation operates within the following brand voice constraints. These are injected as instructions in all prompts.

### VI.1 Voice

| Constraint | Instruction |
|---|---|
| Tone | Clear, precise, understated. Not promotional. Not academic. Not breathless. |
| Authority register | Expert-curator voice. NC presents, it does not hype. |
| Factual claims | Only claims grounded in retrieved evidence. "Based on our catalog records..." is acceptable. |
| Rights language | Reference the injected rights basis. Do not assert. |
| Length | Product descriptions: 50–120 words. Story lede: 80–160 words. Place intro: 100–200 words. Educational copy: per educational level. |
| Format | Prose. No bullet lists in public copy. No markdown in rendered output. |

### VI.2 Prohibited Voice Patterns

| Pattern | Example | Rule |
|---|---|---|
| Promotional hyperbole | "The most breathtaking photograph ever taken" | Ungrounded superlative |
| Scarcity language | "Only X left" / "Limited time" | Not a model output domain |
| Urgency language | "Act now" / "Don't miss" | Not consistent with NC brand |
| Affiliation language | "NC partners with NASA" | Federal nonendorsement §IV.2 |
| Internal jargon | "governed", "Phase 0", "NC-PROD-001", "IFC-1" | Internal system terms, not customer language |
| Accusative rights language | "illegally reproduced" / "pirated" | Out of scope |

---

## VII. Human Review Gate Specifications

### VII.1 Gate Table by Page Family

| Page family | Task type | Required reviewer(s) | Stakes | Two-human? |
|---|---|---|---|---|
| Homepage copy | `public_website_copy` | PA | High | No (PA only) |
| Story page — editorial | `place_story` | Curator + editorial approval | Medium | No |
| Story page — with product recommendations | `place_story` | Curator + PA | Medium-High | No |
| Product page — STANDARD/FLAGSHIP | `product_copy` | Curator | High | No |
| Product page — MASTERWORK (NC-PROD-001) | `product_copy` | Curator + PA | Critical | **Yes** |
| Product page — COA text | `product_copy` | PA | Critical | **Yes** |
| Educational copy | `education_module` | Curator + educational review | Medium | No |
| Place copy (Phase 1+) | `place_story` | Curator | Medium | No |
| Place copy with NOAA assets | `place_story` | Curator + NOAA cap check | High | No |
| Multilingual copy (product/legal) | `editorial_content_assistance` | Curator + translator | High | No |
| SEO metadata | `public_website_copy` | PA | Low-Medium | No |

### VII.2 Review Record Requirements

When a human reviewer approves a candidate:
1. `fm_candidate_record.status` → `'approved'`
2. `fm_candidate_record.reviewed_by` → reviewer identifier
3. `fm_candidate_record.reviewed_at` → timestamp
4. `fm_candidate_record.review_notes` → optional notes
5. PA record (if two-human gate): second reviewer logged separately
6. `page_copy_version` record created (§VIII)

When a reviewer rejects:
1. `fm_candidate_record.status` → `'rejected'`
2. Rejection reason required
3. Candidate is logged but not published
4. Re-generation may be requested with amended inputs

---

## VIII. Publication Snapshot

Every published page-copy version creates a `page_copy_version` record:

| Field | Value |
|---|---|
| `page_url` | Canonical URL of the page |
| `page_family` | Homepage / Story / Product / Educational / Tourism |
| `copy_version_id` | UUID |
| `generation_request_id` | FK → `ai_generation_request` |
| `generation_result_id` | FK → `ai_generation_result` |
| `candidate_id` | FK → `fm_candidate_record` |
| `approved_by` | Reviewer identifier |
| `approved_at` | Timestamp |
| `pa_approved_by` | PA identifier (two-human gate only) |
| `pa_approved_at` | Timestamp (two-human gate only) |
| `copy_snapshot` | JSONB — full copy at time of publication (verbatim) |
| `attribution_snapshot` | JSONB — full attribution block at time of publication |
| `grounding_source_ids` | UUID[] — FK to `ai_grounding_source` records used |
| `status` | `active` / `archived` / `rolled_back` |
| `provenance` | `{"authority": "NC-AI-004", "sprint": "X"}` |

**Snapshot guarantee:** The `copy_snapshot` captures the verbatim published copy. If rights errors are discovered post-publication, the snapshot is the audit record of what was live at what time. This record is append-only and must not be deleted.

**Attribution snapshot:** The `attribution_snapshot` captures the exact attribution strings that appeared on the page at publication time. This is the compliance record for GeoNames CC BY 4.0, OSM ODbL, and federal nonendorsement.

---

## IX. Rollback Path

### IX.1 Rollback Triggers

The following events automatically trigger a rollback process (page must be taken down within 15 minutes of confirmation):

| Trigger | Initiator |
|---|---|
| Rights record corrected: `rights_status` changed from `verified_pd` | Automated monitor on `media_rights` table |
| Rights record corrected: `human_verified` set to FALSE | Automated monitor |
| Any prohibited phrase confirmed in published copy | PA manual review finding |
| Federal endorsement phrase confirmed in published copy | Automated monitor + PA (cascade deactivation) |
| NARA attribution confirmed for Earthrise | PA (FS-001 audit trigger) |
| Source record retracted by institution | PA manual action |
| Any deferred asset confirmed as appearing in published product context | FS-002 audit trigger |

### IX.2 Rollback Execution

1. `page_copy_version.status` → `'rolled_back'`
2. Previous `active` version identified in `page_copy_version` history
3. Previous version's `copy_snapshot` restored to live page
4. If no clean previous version exists: page reverts to a static placeholder ("This page is temporarily unavailable while we review content")
5. `ai_audit_event` written: `event_type = 'rollback_executed'` with full rollback context
6. PA notified immediately
7. If cascade trigger (endorsement phrase): cascade deactivation protocol (NC-PRODUCT-001 §IV) executed before page is re-published

### IX.3 Rollback for Federal Cascade

If the rollback was triggered by a federal endorsement phrase (§IV.2):
1. **All** pages displaying federal-source assets go to placeholder simultaneously
2. PA review is required for all pages before re-activation
3. The generation pipeline is suspended for `product_copy` and `public_website_copy` task types until PA clears the suspension
4. A full prohibited phrase validator audit is run against all `active` copy snapshots before any page is re-published
5. This process cannot be short-circuited by any single reviewer — PA + second-human approval required for cascade reinstatement

---

## X. Verification Summary

### X.1 No Rights Hallucination

**Structural controls:**
- Pre-generation: IFC-1 invariant (rights record must exist and be human_verified before generation authorized)
- Grounding: rights record injected as read-only context, not as a generation target
- Prompt rule: "Do not assert rights status"
- Output validation: rights hallucination pattern register (§IV.1)
- Post-publication: monthly audit of published AI copy

**Residual risk:** NER-based ungrounded claim detection is imperfect; a rights assertion in unusual phrasing may pass the validator but be caught by human reviewer. This is acceptable — the human gate is the backstop.

### X.2 No NASA/NOAA Endorsement Language

**Structural controls:**
- Prompt rule: federal nonendorsement doctrine injected as hard instruction in all prompts touching federal-source assets
- Output validation: full endorsement phrase register (§IV.2) — exact string match + proximity pattern match
- Rollback trigger: any confirmed endorsement phrase triggers full cascade
- Publication snapshot: `attribution_snapshot` records exact nonendorsement text that appeared on each page

**Zero-tolerance:** This control is not graduated. One phrase triggers cascade. The model is never in a "close enough" zone.

### X.3 No NARA Attribution for Earthrise

**Structural controls:**
- Pre-generation: Earthrise asset `source_record_id = 'AS08-14-2383'` activates NARA block in grounding layer
- Prompt rule: "AS08-14-2383 is a NASA photograph. NARA must not appear as a source or verifier for this asset."
- Output validation: NARA/Earthrise pattern register (§IV.3) — triggered by Earthrise context
- Rollback trigger: NARA attribution confirmed in Earthrise context

**FS-001 equivalence:** This control matches NC-AI-001 zero-tolerance rule for NARA/Earthrise.

### X.4 No Deferred Assets

**Structural controls:**
- Pre-generation: `activation_targets.status` check blocks generation for any non-active asset
- Deferred asset name list injected as hard constraints in prompt
- Output validation: deferred asset availability register (§IV.4)
- Rollback trigger: deferred asset appearing in published product context

### X.5 No Ungrounded Claims

**Structural controls:**
- Grounding invariant (§II.3): required retrieval defined per page family; grounding layer rejects requests without it
- Entity ID invariant (§II.4): FM-generated entity IDs validated against canonical sources
- GBIF evidence authority: biological claims grounded in retrieved GBIF evidence
- Output validation: ungrounded claim detection (§IV.5) — NER + retrieval cross-reference
- Human review: reviewer is final backstop for editorial accuracy

---

## XI. Required Standards Amendments and Decision Documents

### XI.1 New SA Required — SA-NC-AI-004-001 (Page Copy Governance Standard)

A Standards Amendment is required to:
1. Extend `ai_generation_request` schema with `page_url`, `page_family`, `quality_tier` fields
2. Create `page_copy_version` table in PostgreSQL (§VIII schema)
3. Extend `ai_grounding_source.allowed_use` to include `page_copy`
4. Register `public_website_copy` and `place_story` (tourism variant) in `ai_task_policy` with correct seeded values

### XI.2 DD-NASA-001 (Condition C-1)

**The reference model list for this document specifies DD-NASA-001. This document does not exist.** NASA governance for NC copy is currently distributed across:
- NC-FIRST-SALE (FS-001/FS-002)
- NC-WEB-001 §IV.1 and §IV.5
- NC-PRODUCT-001 §IV
- `apps/web/lib/governed-content.ts` governed constants

A formal DD-NASA-001 is required before Phase 1 to consolidate NASA governance into a single authoritative decision document, covering: source authority confirmation, rights class for 17 U.S.C. § 105, nonendorsement text canonical form, URL authority, and federal nonendorsement cascade protocol. This is Condition C-1 of this document.

### XI.3 Governed Constants Single Source (NC-AI-002 F-3)

NC-AI-002 Finding F-3 identified that `NASA_NONENDORSEMENT` has two independent definitions. Before any live model generates copy for any page that displays this string, a canonical resolution is required (PostgreSQL table or shared Python package). This is Condition C-2 of this document, inherited from NC-AI-002.

---

## XII. Conditions

**C-1 (DD-NASA-001 — high priority):** File and ratify DD-NASA-001 before Phase 1 place page launch. Non-blocking for Phase 0 Earthrise copy (existing FS-001/NC-WEB-001 coverage sufficient). Blocking for any Phase 1+ place page that displays NASA assets.

**C-2 (Governed constants single source — NC-AI-002 F-3):** Resolve dual definition of `NASA_NONENDORSEMENT` before any live model generates Earthrise copy. See NC-AI-002 §V.

**C-3 (Output validation implementation):** Implement the prohibited phrase validator (§IV) as a production service before any live model (Claude, Gemini, OpenAI, or any API provider) generates copy for any page family. Sprint 1 mitigates this with a deterministic mock. Blocks live API activation.

**C-4 (Page copy version schema):** Implement `page_copy_version` table and publication snapshot mechanism (§VIII) before the first live AI-generated copy is published. Publication snapshot is required for audit, attribution compliance (GeoNames CC BY 4.0 compliance audit), and rollback.

**C-5 (Rollback monitor):** Implement automated monitor on `media_rights` table changes and `ai_human_review` events that triggers rollback when rights records are corrected. Manual rollback via PA is sufficient for Sprint 1. Automated monitor required before catalog scale.

**C-6 (NOAA write cap pre-generation check):** Implement pre-generation check against NOAA write cap before any GBR page generation is authorized. Cap is 7 ALLOWED writes; GBR place page = write #1. This check must run before the generation request reaches the grounding layer.

**C-7 (SA ratification gates):** SA-GEONAMES-001 and SA-OSM-001 must be ratified before any Phase 1+ place page copy is generated for publication. Generation of draft candidates for internal review is permitted before SA ratification; publication is not.

**C-8 (Deferred asset list currency):** The deferred asset register in §II.5 must be reviewed and updated at each Director Decision ratification session. As DDs are ratified (DD-SMITHSONIAN-001, DD-TNA-001, etc.), the relevant assets must be removed from the deferred register and activated through the standard pipeline.

---

## XIII. Decision

**APPROVE WITH CONDITIONS**

The NC-AI-004 Dynamic Page Generation Governance is approved as the governing document for all AI-generated website copy at Nature & Culture, subject to the 8 conditions in §XII.

**Priority sequence for condition resolution:**

1. **C-3 (Output validation):** First. No live model may generate any page copy until the prohibited phrase validator is in production.
2. **C-2 (Governed constants single source):** Required before any live model generates Earthrise copy.
3. **C-4 (Page copy version schema):** Required before the first live AI-generated copy is published.
4. **C-1 (DD-NASA-001):** Required before Phase 1 place pages with NASA assets.
5. **C-7 (SA ratification):** Required before Phase 1 place copy is published.
6. **C-6 (NOAA write cap check):** Required before GBR page generation is authorized.
7. **C-5 (Rollback monitor):** Required before catalog scale.
8. **C-8 (Deferred asset list currency):** Ongoing — review at each DD ratification.

**What is authorized now (Sprint 1, deterministic mock):**

- All five page family generation flows may run against the deterministic mock
- Human review queue is operational
- Publication snapshot schema may be built and tested
- Output validation may be developed and tested against mock outputs

**What requires conditions to be met before activation:**

- Any live API model generating any page copy: C-3 required
- Any live Earthrise copy (product or story): C-2 + C-3 required
- Any Phase 1+ place page published with AI copy: C-1 + C-3 + C-4 + C-7 required
- GBR page copy: all of the above + C-6

**Permanent rules (no conditions, immediate):**

- FM-4: no model asserts rights status in any generated copy
- AI-ATT-1: attribution strings retrieved, never generated
- Federal nonendorsement zero-tolerance: one endorsement phrase → cascade deactivation
- FS-001: NARA attribution for Earthrise permanently prohibited
- FS-002: deferred assets never appear as available in AI-generated copy
- OS-1 through OS-5: OSM data never enters any NC canonical table

---

*NC-AI-004 v1.0 — drafted 2026-06-12. Pending ratification.*
*Reference models: NC-AI-001 · NC-AI-002 · NC-WEB-001 · NC-PRODUCT-001 · NC-FIRST-SALE · SA-GEONAMES-001 · SA-OSM-001*
*Note: DD-NASA-001 referenced but not yet filed — see §XI.2 and Condition C-1.*
*Conditions: 8 (C-1 through C-8). C-3 is the primary gate before live API activation.*
