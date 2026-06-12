# NC-AI-001: AI Governance Architecture Blueprint

| Field | Value |
|---|---|
| Document | NC-AI-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | Foundation Model Constitution v1.0 · Strategic Direction v1 · Wireframe Constitution v1 · NC-PILOT-001 · NC-PRODUCT-001 · NC-WEB-001 · DD-GBIF-001 · DD-WIKIDATA-001 · DD-GEONAMES-001 · DD-OSM-001 · DD-NOAA-001 |
| External alignment | UNESCO Recommendation on the Ethics of AI (2021) · UN Global Digital Compact (2024) · OECD AI Principles (2019, updated 2024) |
| **Decision** | **APPROVE WITH CONDITIONS** |

---

## Core Doctrine

```
Graph = truth.
Models = interpretation, generation, summarization, personalization.
Models may not create source truth, rights truth, or provenance truth.
```

This doctrine is the NC formulation of Foundation Model Constitution v1.0 Article 1.3:
*"The constitutional role of every FM in NC is identical: synthesis instrument producing advisory candidates."*

It is not a default. It is not graduated by model capability or confidence score. It is permanent.

---

## Preamble

NC-AI-001 is a governing extension document. It does not supersede or amend the Foundation Model Constitution v1.0 (FMC). It extends FMC with:
- A task-to-model routing classification for the 15 NC task categories
- A model family governance classification for the 9 model families NC considers
- An open model strategy governing local vs. API model selection
- Cost control architecture
- A resolution of the constitutional conflict between FMC v1.0 and the Strategic Direction v1 frozen stack ruling

NC-AI-001 is subordinate to: Strategic Directive, Foundation Model Constitution v1.0, Illustration Opportunity Doctrine, Media Substrate Constitution v1.2, Commerce Intelligence Constitution v1.2, Wireframe Constitution v1.

---

## I. Constitutional Conflict Resolution

### I.1 The Conflict

The Foundation Model Constitution v1.0 (ratified 2026-06-07) defines the intelligence fabric as:

```
PostgreSQL → PostGIS → Neo4j → pgvector → Foundation Models → PostgreSQL
```

The Strategic Direction v1 (ratified 2026-06-07, same day) and Wireframe Constitution v1 (same day) freeze the NC stack at:

```
PostgreSQL + PostGIS + pg_trgm — no Neo4j, no pgvector
```

This is confirmed by inspection of `infrastructure/postgres/init/00_extensions.sql`: neither `vector` nor any Neo4j extension is present. The frozen stack is the actual deployed stack. The FMC intelligence fabric diagram describes aspirational architecture that does not match the running system.

### I.2 Resolution

**Ruling:** The frozen stack (Strategic Direction v1, Wireframe Constitution v1) governs the actual NC system. FMC v1.0 references to Neo4j and pgvector describe architecture that is not authorized for implementation without a Director Decision amending the Strategic Direction v1 frozen stack clause and passing second-human approval.

**Operative remapping for NC-AI-001:**

| FMC v1.0 reference | NC-AI-001 operative equivalent |
|---|---|
| Neo4j (relationship traversal) | PostgreSQL recursive CTEs over canonical tables |
| pgvector (semantic retrieval) | pg_trgm trigram search + score-vector proximity in `score_inputs JSONB` |
| `context_layers_required: ["neo4j"]` | `context_layers_required: ["postgresql_cte"]` |
| `context_layers_required: ["pgvector"]` | `context_layers_required: ["postgresql_trgm"]` |

FMC v1.0 Articles that reference Neo4j or pgvector (Articles 1.4, 3.3, 11.10, 21.2, 21.4, 23.2, 27.1) are operative as written except where they reference Neo4j or pgvector specifically — those references are replaced by the operative remapping above. No constitutional amendment to FMC is required for this remapping; this document governs the interpretation.

**Condition NC-AI-001-C-1:** A formal amendment to FMC v1.0 must be drafted to update the intelligence fabric diagram and all Neo4j/pgvector field references to the operative remapping. This amendment is non-blocking for Phase 0 AI use cases but must be completed before any AI use case with `context_layers_required` is activated for production.

---

## II. The Intelligence Fabric (Operative Architecture)

```
┌─────────────────────────────────────────────────────────┐
│                   CANONICAL AUTHORITY                   │
│  PostgreSQL (facts · rights · provenance · activation)  │
│  PostGIS (spatial predicates — extension of PostgreSQL) │
└──────────────────────────┬──────────────────────────────┘
                           │ read-only context retrieval
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   RETRIEVAL LAYER                       │
│  pg_trgm (text search · trigram similarity)             │
│  PostgreSQL CTEs (relationship traversal)               │
│  GeoNames (place identity lookup)                       │
│  GBIF (taxon / occurrence lookup)                       │
│  Wikidata (entity crosswalk)                            │
│  Governed constants (attribution strings, rights codes) │
└──────────────────────────┬──────────────────────────────┘
                           │ grounded context
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   GROUNDING LAYER                       │
│  Injects: attribution constants · rights records        │
│  Blocks: hallucination paths to rights/provenance       │
│  Validates: retrieval performed before FM call          │
└──────────────────────────┬──────────────────────────────┘
                           │ governed prompt
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   MODEL ROUTER                          │
│  Task classification · Model selection · Cost gating   │
│  Uses: foundation_model_registry (FMC Article 6)       │
└──────────────────────────┬──────────────────────────────┘
                           │ authorized model call
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   MODEL EXECUTION                       │
│  Local models (classification · extraction · bulk)      │
│  API models (reasoning · generation · complex tasks)    │
│  All calls: fm_inference_record written first           │
└──────────────────────────┬──────────────────────────────┘
                           │ candidate output
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   OUTPUT VALIDATION                     │
│  Pattern block: NARA · endorsement · rights claims      │
│  Attribution check: governed constants only             │
│  fm_candidate_record written                            │
└──────────────────────────┬──────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
      Human Gate     Auto-apply      PROHIBITED
      (Medium/High)  (Low stakes,    (rights · provenance ·
                     confidence≥t)   activation · commerce)
            │              │
            ▼              ▼
┌─────────────────────────────────────────────────────────┐
│              CANONICAL WRITE (PostgreSQL only)          │
│  Human-approved or auto-applied candidates only         │
│  fm_candidate_record.promoted_record_id recorded        │
└─────────────────────────────────────────────────────────┘
```

---

## III. Model Router

### III.1 Routing Inputs

The model router receives a task request containing:

| Field | Values | Governance source |
|---|---|---|
| `task_category` | 15 categories (§VIII) | NC-AI-001 vocabulary |
| `stakes_level` | Low / Medium / High / Critical | FMC Article 10.2 |
| `quality_tier` | DRAFT / REVIEW / PUBLISH | NC-AI-001 quality tier |
| `cost_tier` | LOCAL / API_ECONOMY / API_STANDARD / API_PREMIUM | NC-AI-001 cost tier |
| `language` | ISO 639-1 code | Multilingual routing |
| `content_type` | text / code / structured / multimodal | FMC Article 7 capability type |

### III.2 Routing Logic

```
1. task_category → use_case_id (FMC Article 10 vocabulary)
2. stakes_level → human_gate_required (FMC Article 10.2)
3. language == CJK → prefer Qwen (local) or Gemini (API)
   language == European → prefer Mistral (local) or Gemini (API)
   language == EN → prefer Claude (API) or local small model
4. cost_tier == LOCAL → filter to local_inference = TRUE models only
5. content_type == code → prefer Claude or DeepSeek Coder
6. content_type == multimodal → prefer Gemini (vision)
7. Select highest-ranked eligible model from foundation_model_registry
```

### III.3 Fallback Hierarchy

If the primary model is unavailable:
1. Fall back to the next-ranked model for the same use case
2. If all API models unavailable: local model fallback where task permits
3. If local model unavailable or insufficient quality: task queued, not failed silently
4. FM unavailability must not cause platform failure (FMC Article 3.3, R&SI Invariant P-2 by incorporation)

---

## IV. Grounding Layer

### IV.1 Purpose

The grounding layer is the constitutional enforcement point between retrieval and model execution. It:
1. Injects governed attribution constants (never generated — always retrieved)
2. Injects the canonical rights record for any asset under discussion
3. Injects the governed entity IDs (GeoNames ID, GBIF taxon key, Wikidata QID) for any place, taxon, or institution under discussion
4. Blocks model calls that request rights determinations, provenance assertions, or source-truth generation
5. Validates that required retrieval was performed before the model call is authorized

### IV.2 Governed Constants (never generated, always injected)

The following strings are governed constants in `lib/governed-content.ts` (and their equivalents in the Python/API layer). They must never be generated by a model:

```
NASA_EARTHRISE_CREDIT     =  "NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain."
NASA_NONENDORSEMENT       =  "Image credit: NASA. NASA does not endorse this product."
EARTHRISE_RIGHTS          =  "Public domain — United States Government Work, 17 U.S.C. § 105"
GEONAMES_ATTRIBUTION      =  "Geographic data © GeoNames (geonames.org) — CC BY 4.0"
OSM_ATTRIBUTION           =  "© OpenStreetMap contributors"
NOAA_NONENDORSEMENT       =  "Credit: NOAA/[Division]"
```

Any model output that contains these strings must have retrieved them — not generated them. Output validation checks for generation-vs-retrieval provenance.

### IV.3 Grounding Layer Blocks

The grounding layer must reject the following prompt patterns before model execution:

| Blocked pattern | Reason | FMC reference |
|---|---|---|
| "Determine the rights status of…" | FM-4 — rights hardening invariant | FMC Article 12.1 |
| "Write an attribution line for…" | Attribution is retrieved, not generated | NC-AI-001 §IV.2 |
| "Is this image public domain?" | Rights determination — permanently human | FMC Article 16.1 |
| "Generate provenance for…" | FM-4 — provenance fabrication prohibition | FMC Article 12.6 |
| "Confirm NARA as source for Earthrise" | False provenance — FS-001 ruling | NC-FIRST-SALE |
| Any prompt containing `rights_status = 'verified_pd'` as an assertion | Cannot be asserted by model | FMC FM-4 |
| Any prompt with user behavioral/purchase data | Prohibited per FMC Article 12.5 | Wireframe Constitution |

---

## V. Retrieval Layer

### V.1 Retrieval is Mandatory for Rights-Adjacent Tasks

For all task categories involving assets, products, places, or provenance, retrieval is not optional. The model must receive canonical context before generating output. A model call without retrieval for these task types is a grounding layer block.

**Tasks requiring retrieval (unconditional):**
- rights/governance review
- source onboarding
- product copy
- place story
- educational module
- tourism guide
- website copy
- metadata extraction
- entity reconciliation
- image prompt generation (subject matter context)
- multilingual translation (of governed strings)

**Tasks where retrieval is conditional:**
- product recommendation (catalog retrieval required; user behavioral data prohibited)
- user-facing assistant (retrieval required for factual claims; general greetings exempt)
- product title generation (product spec retrieval required)
- code generation (codebase context retrieval recommended, not required for greenfield)

### V.2 Retrieval Sources by Task

| Retrieval source | Task relevance | NC governance |
|---|---|---|
| PostgreSQL `source_items` (pg_trgm) | All asset tasks | Frozen stack primary search |
| PostgreSQL `places` table (GeoNames data) | All place tasks | SA-GEONAMES-001; S-3 invariant |
| PostgreSQL `media_rights` (human_verified=TRUE only) | Rights context | FM-4 invariant — read-only |
| PostgreSQL `activation_targets` | Product tasks | Governed activation pipeline |
| PostgreSQL `commerce_opportunities` (read-only) | Scoring context | FM-5 invariant — read-only |
| GBIF API (occurrence/taxon, via SA-GBIF-001) | Biological evidence | Media ingestion prohibited |
| Wikidata (entity crosswalk, via DD-WIKIDATA-001) | Creator/place/institution identity | Content pipeline prohibited |
| GeoNames API (place identity, via SA-GEONAMES-001) | Place metadata | GN-7 read-only invariant |
| Governed constants (`lib/governed-content.ts`) | Attribution strings | Always injected, never generated |

**Retrieval sources that are permanently prohibited:**
- OSM canonical data (OS-1 invariant — no OSM data in NC tables, ever)
- GBIF media files (SA-GBIF-001 — media ingestion permanently prohibited)
- Wikidata Commons images (W-6 Commons boundary doctrine)
- User behavioral data (FMC Article 12.5, Wireframe Constitution)

---

## VI. Knowledge Graph Integration

### VI.1 Stack Reality

NC's knowledge graph operates over PostgreSQL using:
- **Recursive CTEs** for multi-hop relationship traversal (creator → works → places → collections)
- **PostGIS** for spatial predicates (places within bounds, place-asset proximity)
- **pg_trgm** for text similarity (creator name matching, title matching, subject term matching)
- **JSONB operators** for score signal proximity (`score_inputs->>'anchor_type'`)

There is no Neo4j instance. There is no pgvector extension. This is the frozen stack.

### VI.2 Graph Traversal Patterns

For FM context retrieval, the following PostgreSQL CTE patterns serve as the knowledge graph queries:

```sql
-- Creator network (replaces Neo4j multi-hop)
WITH RECURSIVE creator_works AS (
  SELECT io.id, io.illustrator, io.title, 0 AS depth
  FROM illustration_opportunities io
  WHERE io.illustrator_id = $creator_id
  UNION ALL
  SELECT io.id, io.illustrator, io.title, cw.depth + 1
  FROM illustration_opportunities io
  JOIN illustration_opportunity_places iop ON io.id = iop.illustration_opportunity_id
  JOIN creator_works cw ON iop.place_id IN (
    SELECT place_id FROM illustration_opportunity_places
    WHERE illustration_opportunity_id = cw.id
  )
  WHERE cw.depth < 3
)
SELECT * FROM creator_works;

-- Place-asset relevance context (replaces pgvector similarity)
SELECT io.id, io.title, iop.relevance_score,
       p.geonames_id, p.feature_code
FROM illustration_opportunities io
JOIN illustration_opportunity_places iop ON io.id = iop.illustration_opportunity_id
JOIN places p ON iop.place_id = p.id
WHERE p.geonames_id = $geonames_id
ORDER BY iop.relevance_score DESC
LIMIT 20;
```

### VI.3 Authority Hierarchy in FM Context

When the model receives context from multiple retrieval sources, the authority hierarchy governs:

1. **PostgreSQL canonical record** — authoritative (rights, provenance, entity IDs)
2. **GeoNames** — authoritative for coordinates, feature codes, place identity (GN-3, GN-1)
3. **GBIF** — authoritative for taxon identity and biological evidence (SA-GBIF-001)
4. **Wikidata** — advisory for crosswalk and cultural metadata (W-8: GeoNames > Wikidata for coordinates)
5. **FM output** — advisory only; cannot override any of the above

A model output that contradicts a canonical PostgreSQL record, a GeoNames coordinate, or a GBIF taxon key is never canonically authoritative. The model is wrong; the governed record is right.

---

## VII. Open Model Strategy

### VII.1 Classification: Local vs. API

| Criterion | Local preferred | API preferred |
|---|---|---|
| Data sensitivity | High (user data, unpublished content) | Low (public content, governed corpus) |
| Volume | High (batch processing, metadata extraction) | Low-medium (single-request quality tasks) |
| Latency requirement | Background (acceptable minutes) | Foreground (user-facing, seconds) |
| Quality bar | Draft / structured output | Final / published output |
| Cost | Compute-constrained | Revenue-generating context (justify API cost) |
| Language | CJK, specialized | English primary |

**Governing principle:** Local models for bulk, draft, and classified tasks. API models for final, published, and nuanced tasks. API models should not be called for tasks that a local model can perform adequately.

### VII.2 License Classification

| Model family | License | Commercial use | Local deployment |
|---|---|---|---|
| Claude (Anthropic) | API terms | Yes (per ToS) | No (API only) |
| Gemini (Google) | API terms | Yes (per ToS) | Via Gemma only |
| GPT/OpenAI | API terms | Yes (per ToS) | No (API only) |
| Qwen 2.5 | Apache 2.0 | Yes | Yes |
| DeepSeek Coder V2 | MIT | Yes | Yes |
| Mistral 7B / 8x7B | Apache 2.0 | Yes | Yes |
| Gemma 2B / 7B | Google Gemma license | Yes (commercial) | Yes |
| Llama 3 (70B and below) | Meta Llama 3 Community | Yes (< 700M MAU) | Yes |
| Phi-4 (Microsoft) | MIT | Yes | Yes |

### VII.3 Data Residency Classification

| Provider | API jurisdiction | Training exclusion | NC ruling |
|---|---|---|---|
| Anthropic | US | Confirmed opt-out available | PERMITTED for API tasks, confirm before activation (FMC Article 9.3) |
| Google (Gemini) | US / EU | Enterprise tier excludes training | PERMITTED for API tasks with enterprise agreement |
| OpenAI | US | Enterprise zero data retention available | PERMITTED for API tasks with ZDR agreement |
| Qwen API (Alibaba) | China | Unknown / not confirmed | **API PROHIBITED** — use local weights only |
| DeepSeek API | China | Unknown / not confirmed | **API PROHIBITED** — use local weights only |
| Mistral API | France / EU | EU data residency, GDPR | PERMITTED for EU language tasks |
| Local (all) | NC infrastructure | N/A — no data leaves NC | PERMITTED unconditionally |

**Ruling:** Qwen and DeepSeek must be deployed as local model weights only. Their API endpoints route through Chinese jurisdiction — data residency is incompatible with NC's governance posture and the FMC Article 9.2 provider assessment requirement. This ruling is not political; it is data governance.

---

## VIII. Task Classification Matrix

For each of the 15 NC task categories, this section defines:
- Primary model(s)
- Retrieval requirement
- Human review gate
- Auto-publish eligibility
- Prohibited outputs

### VIII.1 Rights / Governance Review

| Field | Value |
|---|---|
| **Primary model** | Claude (advisory analysis, draft only) |
| **Secondary model** | Local small model (pattern matching on raw text) |
| **use_case_id** | `rights_analysis_advisory` |
| **Stakes** | Critical |
| **Retrieval** | Unconditional — `media_rights` (read-only), institution DD, source record |
| **Human gate** | Always. Per-record. FM output is advisory context labeled "Advisory — human determination required." |
| **Auto-publish** | PROHIBITED — Invariant FM-4 |
| **Prohibited outputs** | Any `rights_status` assertion · Any provenance claim · Any NARA attribution for Earthrise · Any endorsement language |
| **Notes** | FM output is stored in `fm_candidate_record` permanently advisory state. It can never be promoted. The human makes an independent determination. |

### VIII.2 Source Onboarding

| Field | Value |
|---|---|
| **Primary model** | Claude (structural analysis, field mapping, DD draft assistance) |
| **Secondary model** | DeepSeek Coder (schema mapping, API response parsing) |
| **use_case_id** | `editorial_content_assistance` (for DD draft) + `structured_classification` (for field mapping) |
| **Stakes** | High (DD output) / Medium (field mapping) |
| **Retrieval** | Unconditional — existing institution DDs, institution factory stages, rights matrix |
| **Human gate** | Always. IFC exit gates are constitutionally required. No automation authorized. |
| **Auto-publish** | PROHIBITED |
| **Prohibited outputs** | Any rights determination · Any institution authorization without human sign-off · Any SA/DD ratification claim |

### VIII.3 Product Copy

| Field | Value |
|---|---|
| **Primary model** | Claude (final copy, product page descriptions, variant descriptions) |
| **Secondary model** | Mistral (draft variants, cost-reduction for bulk) |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Unconditional — product spec, asset metadata, rights record, NC-WEB-001 copy rules, prohibited phrases list |
| **Human gate** | Curator review required before any product copy is published. MASTERWORK tier: curator + PA. |
| **Auto-publish** | PROHIBITED. All product copy is draft until curator-approved. |
| **Prohibited outputs** | "NASA-endorsed" · "NASA-certified" · "NARA: Verified archival source" for Earthrise · "Verified by NASA" · "Official [Agency] product" · Any rights claim · Any Collector Edition copy until NARA Sprint 1 · Any deferred asset copy |
| **Output validation** | Every model output passes through the prohibited phrases validator before it reaches the human review queue |

### VIII.4 Place Story

| Field | Value |
|---|---|
| **Primary model** | Claude (English editorial) |
| **Secondary model** | Gemini (multilingual, vision-language for satellite imagery context) |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Unconditional — place data (GeoNames, PostGIS), approved assets, GBIF evidence (text only), historical context, attribution matrix per NC-WEB-001 §III |
| **Human gate** | Curator review + editorial approval before publication |
| **Auto-publish** | PROHIBITED |
| **Prohibited outputs** | Any rights claim · Unsourced provenance assertions · Smithsonian/partner endorsement claims · Deferred asset references as available · GBIF species images |
| **Notes** | FM may propose which assets to feature in a story; the curator approves the final selection. Asset selection has indirect commerce influence (Article 19 of FMC). |

### VIII.5 Educational Module

| Field | Value |
|---|---|
| **Primary model** | Claude |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Unconditional — place data, assets (PD only), GBIF biological data (text), scientific context |
| **Human gate** | Curator + educational review |
| **Auto-publish** | PROHIBITED |
| **Prohibited outputs** | Fabricated scientific claims · Species information not grounded in GBIF evidence · Endorsement language |

### VIII.6 Tourism Guide

| Field | Value |
|---|---|
| **Primary model** | Claude (English) / Gemini (multilingual) |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Unconditional — place data, heritage designations (UNESCO labels read from governed data, not asserted by model), assets, GBIF evidence |
| **Human gate** | Curator review |
| **Auto-publish** | PROHIBITED |
| **Prohibited outputs** | Any UNESCO endorsement assertion · Any government agency recommendation claim |

### VIII.7 Product Recommendation

| Field | Value |
|---|---|
| **Primary model** | Local small model (classification, relevance scoring) |
| **Secondary model** | Claude (explanation generation, if shown to user) |
| **use_case_id** | `discovery_enrichment_synthesis` |
| **Stakes** | Low |
| **Retrieval** | Unconditional — governed product catalog (activation_targets with status='active' only) · place context · **User behavioral data: PROHIBITED** |
| **Human gate** | Not required for automated recommendations. Monthly batch audit required. |
| **Auto-publish** | **PERMITTED** — recommendations from the governed product catalog only. Model cannot surface unactivated, deferred, or prohibited products. The governed catalog is the constraint. |
| **Guardrail** | Before any recommendation is surfaced: verify `activation_target.status = 'active'` in PostgreSQL. Model output never bypasses this check. |

### VIII.8 Website Copy

| Field | Value |
|---|---|
| **Primary model** | Claude |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Unconditional — NC-WEB-001 copy rules, prohibited phrases, brand guidelines, attribution constants |
| **Human gate** | PA review for product pages, metadata. Curator for editorial sections. |
| **Auto-publish** | PROHIBITED |
| **Prohibited outputs** | Any phrase from NC-WEB-001 §IV prohibited copy register · "Phase 0" as customer-facing copy (internal term) · "NC-PROD-XXX" as customer-facing label · "governed" as a selling word · "Giclee" without accent |

### VIII.9 Metadata Extraction

| Field | Value |
|---|---|
| **Primary model** | Local small model (Phi-4, Gemma 7B) — structured output, field extraction from API responses |
| **Secondary model** | Claude (complex disambiguation, unstructured sources) |
| **use_case_id** | `subject_term_classification` / `creator_identity_resolution` |
| **Stakes** | Low (bulk extraction) / Medium (creator identity) |
| **Retrieval** | Required — schema definitions, existing entity records, institution source schema |
| **Human gate** | Required before any M36 (PostgreSQL canonical) write. Auto-apply eligible for `subject_term_classification` at confidence ≥ 0.92 (FMC Article 10). |
| **Auto-publish** | N/A (internal pipeline) |

### VIII.10 Entity Reconciliation

| Field | Value |
|---|---|
| **Primary model** | Local small model (fuzzy name matching, GeoNames/GBIF/Wikidata ID candidates) |
| **Secondary model** | Claude (disambiguation of ambiguous creators, compound names, historical variants) |
| **use_case_id** | `creator_identity_resolution` / `anchor_type_classification` |
| **Stakes** | Medium |
| **Retrieval** | Required — GeoNames API, GBIF taxon API, Wikidata crosswalk, canonical authority registry |
| **Human gate** | Required for new entity writes. Auto-apply eligible at confidence ≥ 0.96 (FMC Article 10). |
| **Auto-publish** | N/A (internal) |
| **Notes** | Entity reconciliation has indirect commerce influence (FMC Article 19.1) — creator identity affects creator prestige score. Director Decision required acknowledging this pathway. |

### VIII.11 Code Generation

| Field | Value |
|---|---|
| **Primary model** | Claude (architecture, complex logic, TypeScript/Python) |
| **Secondary model** | DeepSeek Coder V2 (local, bulk code generation, SQL queries) |
| **use_case_id** | `editorial_content_assistance` (code is advisory text output — same constitutional class) |
| **Stakes** | Medium (application code) / High (governance-adjacent code — migrations, rights workers) |
| **Retrieval** | Recommended — existing codebase context, architecture docs, frozen stack constraints |
| **Human gate** | PA review required before merge. Code that touches `media_rights`, `activation_targets`, or `commerce_opportunities` tables requires second-human review. |
| **Auto-publish** | PROHIBITED — no code merges without human review |
| **Critical rule** | Generated code must never bypass the second-human rule, the IFC-1 hard gate, or the `human_verified` flag path. Any generated code that touches these must be explicitly flagged for PA review. |

### VIII.12 User-Facing Assistant

| Field | Value |
|---|---|
| **Primary model** | Claude (API, primary; retrieval-grounded) |
| **use_case_id** | `discovery_enrichment_synthesis` (for factual queries) / `editorial_content_assistance` (for explanations) |
| **Stakes** | Medium (factual queries) / Low (general greetings) |
| **Retrieval** | Required for any factual claim about assets, places, rights, or provenance |
| **Human gate** | Not required for individual responses. Weekly audit of 10% sample required. |
| **Auto-publish** | N/A (conversational) |
| **Hard rules** | Model must not assert rights status · Must cite retrieval source for factual claims ("Based on our catalog…") · Must not answer rights questions definitively ("This image is public domain" → redirect to attribution page) · Must never generate attribution strings — always retrieve and display governed constants |

### VIII.13 Multilingual Translation

| Field | Value |
|---|---|
| **Primary model** | Qwen 2.5 (local, CJK) · Mistral (local, European) · Gemini (API, broad coverage) |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Low (UI strings) / Medium (editorial copy) / High (product pages, COA, legal copy) |
| **Retrieval** | Required — source strings, governed translation glossary, prohibited phrases in target language |
| **Human gate** | Required for product pages, legal copy, COA text, and any surface carrying attribution strings. UI string translation: batch review permitted. |
| **Auto-publish** | PROHIBITED for product/legal copy. Conditional for UI strings with batch human review. |
| **Special rule** | Attribution strings (NASA nonendorsement, GeoNames credit, OSM credit) must be translated only with explicit curator approval. The translated form must preserve the legal substance. The governed English form is always the authoritative version. |

### VIII.14 Image Prompt Generation

| Field | Value |
|---|---|
| **Primary model** | Claude |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Required — subject matter context, asset inventory, rights-safe reference |
| **Human gate** | Required |
| **Auto-publish** | PROHIBITED |
| **Prohibited prompts** | Any prompt designed to recreate a specific PD artwork for use as a product substitute · Any prompt designed to mimic the style of a living artist · Any prompt generating imagery intended to replace verified PD assets in the product catalog |
| **Permitted** | Editorial illustration (story pages, educational content) · Placeholder imagery during development · Atmospheric visual direction that does not substitute for a governed asset |
| **Note** | Image prompts are editorial tools only. Generated images are not products and may not enter the product pipeline without a new governed asset acquisition path (which does not currently exist). |

### VIII.15 Product Title Generation

| Field | Value |
|---|---|
| **Primary model** | Claude (final title candidates) |
| **Secondary model** | Local small model (bulk variant generation for A/B testing) |
| **use_case_id** | `editorial_content_assistance` |
| **Stakes** | Medium |
| **Retrieval** | Required — product spec, asset metadata, brand guidelines, NC-WEB-001 §IV copy rules |
| **Human gate** | Curator approval required before any title is used on a live product page |
| **Auto-publish** | PROHIBITED without curator sign-off |
| **Prohibited titles** | Any title containing prohibited phrases (§IV of NC-WEB-001) · "Collector's Edition" until NARA Sprint 1 · Any title attributing Earthrise to NARA · "Giclee" without accent |

---

## IX. Model Registry Classification

This section classifies the 9 model families against NC governance requirements. Each model that NC activates must complete the FMC Article 24 activation gate sequence.

### IX.1 Claude (Anthropic)

| Property | Value |
|---|---|
| Registry ID format | `anthropic:claude-sonnet-4-6:{dated-version}` |
| Capability types | `text_generation` · `structured_classification` · `multimodal_synthesis` (with vision) |
| Authorized use cases | All 10 FMC use cases + NC-AI-001 task categories (§VIII) |
| API or local | API only |
| Data residency | US — confirm training exclusion before activation (FMC Article 9.3) |
| Version pinning | Required — use dated version IDs (e.g., `claude-sonnet-4-6`) not aliases |
| Cost tier | API_STANDARD to API_PREMIUM |
| DD required | DD-AI-001 (pending) — this document is the precursor; DD-AI-001 must formally activate Claude |
| Priority | **Primary model for all high-quality generation, reasoning, and advisory tasks** |
| Special rules | FM-4 non-negotiable (rights hardening) · FM-5 non-negotiable (commerce score gate) |

### IX.2 Gemini (Google)

| Property | Value |
|---|---|
| Registry ID format | `google:gemini-2.0-flash:{dated-version}` |
| Capability types | `text_generation` · `vision_analysis` · `multimodal_synthesis` |
| Authorized use cases | `editorial_content_assistance` (multilingual) · `discovery_enrichment_synthesis` (vision) |
| API or local | API only (Gemma for local) |
| Data residency | US — enterprise agreement required before activation (training exclusion) |
| Cost tier | API_ECONOMY to API_STANDARD |
| DD required | DD-AI-002 (Gemini provider activation) |
| Priority | Secondary API model; primary for CJK/European multilingual and vision tasks |
| Restriction | Not authorized for rights analysis advisory, product copy final, or governance review |

### IX.3 GPT / OpenAI (GPT-4o series)

| Property | Value |
|---|---|
| Registry ID format | `openai:gpt-4o:{dated-version}` |
| Capability types | `text_generation` · `structured_classification` |
| Authorized use cases | `editorial_content_assistance` · `structured_classification` tasks |
| API or local | API only |
| Data residency | US — Zero Data Retention agreement required before activation |
| Cost tier | API_STANDARD to API_PREMIUM |
| DD required | DD-AI-003 (OpenAI provider activation) |
| Priority | Tertiary; use only when Claude and Gemini are insufficient for specific tasks |
| Note | Codex (legacy standalone product) is deprecated by OpenAI. Code generation routes to Claude or DeepSeek Coder. "Codex" as a task category maps to Claude + DeepSeek Coder, not to a separate Codex endpoint. |

### IX.4 Qwen 2.5 (Alibaba / Open Weights)

| Property | Value |
|---|---|
| Registry ID format | `alibaba:qwen-2.5:{size}-instruct:{local}` |
| Capability types | `text_generation` · `structured_classification` |
| Authorized use cases | Multilingual translation (CJK) · `subject_term_classification` |
| API or local | **LOCAL ONLY** — Qwen API prohibited (China jurisdiction, data residency §VII.3) |
| Data residency | Local NC infrastructure — no data leaves platform |
| License | Apache 2.0 — commercial use permitted |
| Cost tier | LOCAL (compute only) |
| DD required | DD-AI-004 (Qwen local model activation) |
| Priority | Primary model for Chinese, Japanese, Korean language tasks |
| Recommended sizes | Qwen2.5-7B-Instruct (fast, metadata tasks) · Qwen2.5-14B-Instruct (higher quality translation) |

### IX.5 DeepSeek (Open Weights)

| Property | Value |
|---|---|
| Registry ID format | `deepseek:deepseek-coder-v2:{variant}:{local}` |
| Capability types | `text_generation` (code-focused) · `structured_classification` |
| Authorized use cases | Code generation · SQL query generation · schema mapping |
| API or local | **LOCAL ONLY** — DeepSeek API prohibited (China jurisdiction) |
| Data residency | Local NC infrastructure |
| License | MIT — commercial use permitted |
| Cost tier | LOCAL (compute only) |
| DD required | DD-AI-005 (DeepSeek local model activation) |
| Priority | Primary local model for code generation; secondary to Claude for complex architecture |
| Recommended variant | DeepSeek-Coder-V2-Lite-Instruct (16B, fast) · DeepSeek-Coder-V2-Instruct (236B, high quality, requires significant compute) |

### IX.6 Mistral (Mistral AI / Open Weights)

| Property | Value |
|---|---|
| Registry ID format | `mistral:mistral-7b-instruct:{version}:{local}` |
| Capability types | `text_generation` · `structured_classification` |
| Authorized use cases | Multilingual translation (French, Spanish, Italian, German, Portuguese) · Draft text generation |
| API or local | LOCAL preferred (Mistral API permitted as secondary — EU jurisdiction, best data residency among API options) |
| Data residency | Local preferred; Mistral API (France) as fallback — GDPR-compliant |
| License | Apache 2.0 — commercial use permitted |
| Cost tier | LOCAL (primary) · API_ECONOMY (Mistral API fallback) |
| DD required | DD-AI-006 (Mistral model activation) |
| Priority | Primary local model for European language tasks; secondary to Claude for English |
| Recommended variant | Mistral-7B-Instruct-v0.3 (local) · Mistral-8x7B-Instruct (higher quality, more compute) |

### IX.7 Gemma (Google / Open Weights)

| Property | Value |
|---|---|
| Registry ID format | `google:gemma-2:{size}-it:{local}` |
| Capability types | `structured_classification` · `text_generation` (lightweight) |
| Authorized use cases | `subject_term_classification` · `anchor_type_classification` · lightweight metadata extraction |
| API or local | LOCAL only in NC governance |
| Data residency | Local NC infrastructure |
| License | Google Gemma Terms of Service — commercial use permitted |
| Cost tier | LOCAL (compute only, lowest cost in catalog) |
| DD required | DD-AI-007 (Gemma local model activation) |
| Priority | Preferred for high-volume, low-stakes classification tasks — cheapest per-inference cost |
| Recommended sizes | Gemma-2-2B-IT (fastest, cheapest) · Gemma-2-9B-IT (higher quality classification) |

### IX.8 Local Small Models (Llama 3, Phi-4, etc.)

| Property | Value |
|---|---|
| Registry ID format | `meta:llama-3:{size}:{local}` / `microsoft:phi-4:{local}` |
| Capability types | `structured_classification` · `text_generation` (limited) |
| Authorized use cases | Metadata extraction · entity classification · subject term batch processing |
| API or local | LOCAL only |
| Data residency | Local NC infrastructure |
| License | Llama 3: Meta License (commercial < 700M MAU) · Phi-4: MIT |
| Cost tier | LOCAL (cheapest class) |
| DD required | DD per model family at activation |
| Priority | For bulk, high-volume, structured-output tasks where quality tier is DRAFT |
| Notes | Each distinct model variant requires its own `foundation_model_registry` entry per FMC Article 6 |

---

## X. Output Classification Register

### X.1 Auto-Publishable Outputs (no human gate required)

| Output | Condition | Guardrail |
|---|---|---|
| Product recommendations | Catalog-constrained: only `activation_targets` with `status='active'` | PostgreSQL verification before surfacing; user behavioral data prohibited |
| Subject term classifications (auto-apply) | Confidence ≥ 0.92; use case `subject_term_classification` | Monthly human batch audit required (FMC Article 15.3) |
| Anchor type classifications (auto-apply) | Confidence ≥ 0.96; use case `anchor_type_classification` | Monthly human batch audit required |
| Creator identity resolution (auto-apply) | Confidence ≥ 0.96; use case `creator_identity_resolution` | Monthly human batch audit required |

### X.2 Draft-Only Outputs (require human review gate before any public surface)

| Output | Required reviewer | Gate |
|---|---|---|
| Product copy (all tiers) | Curator | Curator approval before product page publish |
| Product copy (MASTERWORK) | Curator + PA | Two-human gate per NC-PRODUCT-001 §IV |
| Place story | Curator + editorial review | Curator approval before story publish |
| Educational module | Curator + educational review | Curator approval |
| Tourism guide | Curator | Curator approval |
| Website copy (product pages) | PA | PA review before staging |
| Website copy (editorial) | Curator | Curator review |
| Multilingual translation (product/legal) | Curator | Curator approval |
| Product title candidates | Curator | Curator selection |
| Image prompt | Curator | Curator approval (editorial use only) |
| Code (all) | PA | PA review before merge |
| Code (governance-adjacent) | PA + second human | Second-human rule |
| Place story (multilingual) | Curator + translator | Both approvals required |
| User assistant responses (sample) | Weekly 10% audit | Designated reviewer |

### X.3 Prohibited Outputs (no model may generate; no human may approve)

| Prohibited output | Reason | Constitutional basis |
|---|---|---|
| Rights status determination (`rights_status = 'verified_pd'`) | FM-4 invariant | FMC Article 12.1, Article 16.1 |
| NARA as source for Earthrise | False provenance — FS-001 | NC-FIRST-SALE, NC-WEB-001-LA |
| "NASA-endorsed" / "Verified by NASA" / "Official NASA product" | Federal endorsement zero-tolerance | NC-PRODUCT-001 §IV |
| Provenance assertion without governed source | FM-4, Article 12.6 | FMC Article 12.6 |
| Activation approval (`activation_target.status = 'approved'`) | Human-governed | FMC Article 12.2 |
| Commerce score computation | FM-5 invariant | FMC Article 12.3 |
| Collection publication (`collections.status = 'published'`) | Human-governed | FMC Article 12.4 |
| User behavioral profiling | Wireframe Constitution permanent prohibition | FMC Article 12.5 |
| OSM data in any NC table | OS-1 invariant | DD-OSM-001 |
| GBIF media ingestion | SA-GBIF-001 | DD-GBIF-001 |
| Wikidata Commons images in product pipeline | W-6 Commons doctrine | DD-WIKIDATA-001 |
| Generated images as product substitutes for PD assets | No governed asset acquisition path exists | NC-AI-001 §VIII.14 |
| Attribution strings generated by model (vs. retrieved) | Attribution is governed constant | NC-AI-001 §IV.2 |

---

## XI. Human Review Gates

### XI.1 Gate Classification

| Gate | Trigger | Reviewer | Stakes | FMC reference |
|---|---|---|---|---|
| Rights Gate | Any FM output touching `media_rights` | Human rights verifier | Critical | FM-4, Article 16 |
| Activation Gate | Any FM output recommending activation approval | Curator + PA | Critical | Article 12.2, Article 24 |
| Commerce Gate | Any FM output touching score inputs | PA + constitutional amendment | Critical | FM-5, Article 18 |
| Curator Gate | Editorial copy, product copy, stories | Curator | Medium/High | Article 26 |
| PA Gate | Code, architecture, governance-adjacent copy | PA | High | Article 26 |
| Two-Human Gate | MASTERWORK products, rights records, collection publication | Curator + PA (or designated second human) | Critical | Media Substrate Constitution Art. 25 |
| Auto-Apply Audit | Monthly review of all auto-applied candidates | Designated reviewer | Low/Medium | FMC Article 15.3 |
| Provider Audit | Annual review of all API provider training exclusion confirmations | PA | Medium | FMC Article 9.3 |

### XI.2 Gate Bypass is a Constitutional Violation

Any system, worker, or human that routes FM output to a public surface without passing the required gate for that task is in violation of FMC Article 4. This applies regardless of FM output quality, confidence score, or human judgment about the model's reliability. The gate is not a quality check; it is a governance requirement.

---

## XII. Cost Controls

### XII.1 Cost Tier Definitions

| Tier | Definition | Typical use | Monthly budget signal |
|---|---|---|---|
| LOCAL | Local model inference; NC compute only | Bulk extraction, classification, drafts | Variable (compute) |
| API_ECONOMY | Low-cost API models (Gemini Flash, Mistral API) | Multilingual, secondary tasks | < $0.01/1K tokens |
| API_STANDARD | Mid-tier API models (Claude Haiku, GPT-3.5 equivalent) | Product copy drafts, metadata | $0.01–0.05/1K tokens |
| API_PREMIUM | Top-tier API models (Claude Sonnet/Opus, GPT-4o) | Final published copy, governance advisory | > $0.05/1K tokens |

### XII.2 Cost Routing Rules

1. **Bulk tasks (>100 records):** Local model or API_ECONOMY only. API_PREMIUM is prohibited for bulk.
2. **Draft outputs:** Local model or API_STANDARD. API_PREMIUM for drafts requires PA approval.
3. **Published outputs:** API_STANDARD minimum. API_PREMIUM preferred for MASTERWORK tier.
4. **Governance advisory (rights, onboarding):** API_PREMIUM only — quality of advisory context must not be cost-constrained.
5. **User-facing assistant (conversational):** API_STANDARD minimum. Cache repeated retrieval contexts.

### XII.3 Token Budget Controls

| Task category | Max input tokens | Max output tokens | Caching |
|---|---|---|---|
| Rights/governance review | 16,000 | 4,000 | DD text: cache for session |
| Product copy | 4,000 | 1,000 | Attribution constants: always cached |
| Place story | 8,000 | 3,000 | Place context: cache for 24h |
| Metadata extraction | 2,000 | 500 | Schema: always cached |
| User-facing assistant | 8,000 | 2,000 | Place/product context: cache 1h |
| Multilingual translation | 4,000 | 4,000 | Source strings: cache for session |
| Code generation | 16,000 | 8,000 | Codebase context: cache for session |

### XII.4 Cost Monitoring

- `fm_inference_record.token_count_input` + `token_count_output` — per-inference tracking (FMC Article 21.2)
- Monthly cost report by: `use_case_id`, `model_id`, `task_category`
- Alert threshold: >$X/month per use case requires PA review of routing decisions
- Budget exceeded: escalate to PA; downgrade cost tier if quality still acceptable

---

## XIII. Audit Logging

### XIII.1 Governing Structure

All audit obligations are inherited from FMC Articles 21–22 (`fm_inference_record`). NC-AI-001 adds audit requirements specific to the 15 task categories.

### XIII.2 Additional Audit Fields (NC-AI-001 extension)

The following fields are added to `fm_inference_record` by NC-AI-001:

| Field | Type | Governance |
|---|---|---|
| `task_category` | VARCHAR | NC-AI-001 §VIII vocabulary |
| `quality_tier` | VARCHAR | DRAFT / REVIEW / PUBLISH |
| `cost_tier` | VARCHAR | LOCAL / API_ECONOMY / API_STANDARD / API_PREMIUM |
| `retrieval_sources_used` | JSONB | Which retrieval sources were actually queried |
| `grounding_constants_injected` | TEXT[] | Which governed constants were injected |
| `prohibited_pattern_check` | BOOLEAN | TRUE if output passed prohibited phrase validation |
| `prohibited_pattern_findings` | JSONB | NULL if clean; findings detail if violations found |
| `human_gate_required` | BOOLEAN | Derived from task_category + stakes_level |
| `human_gate_completed` | BOOLEAN | Set TRUE when human review is recorded |
| `published_at` | TIMESTAMP | NULL until content reaches a public surface |

### XIII.3 Audit Retention

| Stakes level | Retention | Rationale |
|---|---|---|
| Low | 12 months | FMC Article 10.2 |
| Medium | 24 months | FMC Article 10.2 |
| High | 36 months | FMC Article 10.2 |
| Critical | Permanent | FMC Article 10.2 |
| Rights-adjacent (any) | Permanent | FM-4 invariant — rights audit chain must never be deleted |

### XIII.4 Append-Only Guarantee

`fm_inference_record` is append-only: no UPDATE, no DELETE (FMC Article 21.3). The audit chain is constitutionally immutable.

---

## XIV. Attribution Preservation

### XIV.1 The Attribution Preservation Invariant

**AI-ATT-1:** Attribution strings for governed content sources (NASA, NOAA, GeoNames, OSM, BHL, NARA) may never be generated by a model. They must always be retrieved from the governed constants layer and injected into the prompt context as literals. A model that outputs an attribution string must have received it as input context, not synthesized it.

### XIV.2 Attribution Injection Protocol

Before any model call involving a NASA-sourced asset:
1. Retrieve `NASA_EARTHRISE_CREDIT` and `NASA_NONENDORSEMENT` from governed constants
2. Inject into prompt: `"The following attribution text must appear verbatim in your output, unrewritten: {NASA_NONENDORSEMENT}"`
3. Validate: output contains the exact attribution text without paraphrase
4. If output paraphrases the attribution: reject; re-run with stronger instruction

### XIV.3 Attribution Validation in Output

The output validation layer runs the following checks on every model output before it enters the human review queue:

1. **NASA check:** If output discusses Earthrise or any NASA asset, confirm `NASA_NONENDORSEMENT` appears verbatim
2. **NARA check:** If output mentions "National Archives", "NARA", or "archival records" in relation to Earthrise: BLOCK and flag as FS-001 violation
3. **GeoNames check:** If output includes place data on a place page context: confirm `GEONAMES_ATTRIBUTION` is present or will be injected by the template
4. **OSM check:** If output is for a page with map tiles: confirm `OSM_ATTRIBUTION` is present
5. **Endorsement check:** Scan for prohibited endorsement phrases (§X.3)

---

## XV. Hallucination Controls

### XV.1 The Hallucination Risk Hierarchy

NC's highest-risk hallucination domains, in order of severity:

1. **Rights claims** — model asserts PD status for a non-verified asset. Mitigated by: FM-4 invariant (rights never generated), retrieval-only rights context, output validation block.
2. **Provenance claims** — model asserts creator, date, or institution for an asset without verified source. Mitigated by: FM-4 provenance fabrication prohibition, retrieval-grounded context only.
3. **Attribution strings** — model paraphrases a governed attribution constant. Mitigated by: AI-ATT-1 invariant, attribution injection protocol.
4. **Entity IDs** — model invents a GeoNames ID, GBIF taxon key, or Wikidata QID. Mitigated by: all entity IDs must be retrieved from canonical sources, never generated; entity ID validation in output.
5. **Factual claims** — model states incorrect historical or scientific facts about a place or taxon. Mitigated by: retrieval-grounded context, human editorial review.
6. **Product availability** — model claims a deferred or unactivated product is available. Mitigated by: product recommendation guardrail (§VIII.7), prohibited phrases validator.

### XV.2 Structural Hallucination Mitigations

| Technique | Applied to | Implementation |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | All factual tasks | Context from PostgreSQL always injected before generation |
| Governed constant injection | All attribution tasks | Attribution strings injected as literals, not prompts to generate |
| Output validation (prohibited patterns) | All tasks | Post-generation regex + semantic check before human queue |
| Confidence-gated auto-apply | Classification tasks | Hallucinated classifications have low confidence; stay in review queue |
| Human review chain | All medium/high/critical tasks | Human catches factual errors before publish |
| Entity ID grounding | Place/taxon/creator tasks | Every entity reference must resolve to a PostgreSQL UUID |
| Short-circuit for rights | Rights tasks | Grounding layer blocks rights generation before model is called |
| Temperature control | Factual extraction | Lower temperature (0.0–0.2) for structured/factual tasks; higher (0.7) for creative copy |

### XV.3 Entity ID Hallucination Block

Any FM output that contains a numeric string matching GeoNames ID patterns, GBIF taxon key patterns, or Wikidata Q-number patterns must be validated against the canonical authority before the output is accepted. An FM-invented `geonames_id` that does not exist in `places.geonames_id` is rejected.

---

## XVI. Public-Domain / Rights-Safe Generation Policy

### XVI.1 Governing Principle

NC generates content *about* public-domain works. NC does not generate substitutes *for* public-domain works.

The distinction:
- **Permitted:** Editorial text describing Haeckel's Hexacoralla plate, its scientific significance, its provenance, and its cultural context — grounded in the governed asset record
- **Prohibited:** An AI-generated image "in the style of Haeckel" used as a product image in place of the actual governed PD asset

### XVI.2 Text Generation Policy

AI-generated text about PD works is permitted under the following conditions:
1. The text is grounded in retrieved canonical facts (asset metadata, creator records, place context)
2. The text does not assert rights status
3. The text does not assert provenance for unverified elements
4. The text carries a human editorial review gate before publication
5. The text is labeled in the internal audit trail as AI-assisted

AI-generated text that becomes published editorial content must be "substantially reviewed" by a human editor (FMC Article 11.9 standard). Verbatim FM output on a public-facing page without human editorial review is a governance violation.

### XVI.3 Image Generation Policy

AI-generated images:
- **Prohibited as product images** — the NC catalog is PD assets, not AI-generated art
- **Prohibited as substitutes** for PD artworks in the product pipeline
- **Permitted for editorial illustration** (story pages, educational content, atmospheric design) with curator approval and clear internal labeling
- **Permitted for development placeholders** — must be replaced with governed assets before production
- Must never be used to fill a product image slot for an asset whose rights are under review or unconfirmed

### XVI.4 The Training Data Consideration

NC's model outputs may describe, summarize, or contextualize PD works. NC makes no claim that the underlying models were trained on those works. The rights basis for NC's products is:
- The underlying asset (the PD photograph, the PD illustration) is governed by its rights record
- The editorial text generated by the FM is NC-authored content
- The editorial text cannot inherit the PD status of the asset it describes
- NC-authored editorial text is NC's intellectual property, not public domain, unless explicitly licensed

---

## XVII. UN/UNESCO/OECD Alignment

### XVII.1 UNESCO Recommendation on the Ethics of AI (2021)

| UNESCO value | NC-AI-001 implementation |
|---|---|
| Proportionality and do no harm | FM-4 (rights hardening) + output validation prevent AI from causing rights harm. Prohibited output register (§X.3). |
| Safety and security | Grounding layer blocks, prohibited pattern checks, audit logging (§XIII) |
| Fairness and non-discrimination | Open model strategy includes CJK/European models for linguistic inclusion. No user behavioral profiling (FMC Article 12.5). |
| Sustainability | Local model preference (§VII.1) reduces API dependency and carbon cost. Cost controls (§XII). |
| Right to privacy | User behavioral data permanently excluded from all FM calls (FMC Article 12.5, Wireframe Constitution). No model training on NC user data. |
| Human oversight and determination | Human review gates (§XI) are constitutional — not optional or threshold-based. Rights gates are permanent. |
| Transparency and explainability | `fm_inference_record` (FMC Article 21) provides full audit trail. Retrieval sources recorded. Model and version pinned. Human decision recorded. |
| Responsibility and accountability | Clear ownership (PA + curator). Audit chain immutable. Human who approves a candidate is accountable for that decision (FMC Article 26.3). |
| Awareness and AI literacy | Public-domain transparency: all attribution visible on product pages. AI-assisted label in internal audit trail. |
| Multi-stakeholder governance | Open model strategy embraces non-US, non-API models. Local model deployment reduces single-provider dependency. |
| Promotion of responsible AI | This document is a publicly articulable governance architecture. NC commits to operating AI in a manner consistent with its public-domain mission. |

### XVII.2 UN Global Digital Compact (2024)

| GDC principle | NC-AI-001 implementation |
|---|---|
| Digital inclusion | Multilingual strategy (Qwen, Mistral, Gemini) enables CJK and European access to NC content |
| AI safety | Output validation, hallucination controls, human gates, prohibited output register |
| Data governance | Rights-safe generation policy (§XVI). No user data in FM calls. No training on NC user data. |
| Human rights | No profiling, no discrimination, no generation of content that misattributes or falsifies rights |
| Global cooperation | Open model strategy prefers open-weight, openly licensed models (Apache 2.0, MIT) |
| Trustworthy AI | Immutable audit log, full inference provenance, human accountability chain |

### XVII.3 OECD AI Principles (2019, updated 2024)

| OECD principle | NC-AI-001 implementation |
|---|---|
| Inclusive growth and sustainable development | Place-centered NC platform benefits global heritage access. Local model preference reduces cost barrier. |
| Human-centered values and fairness | Human review gates for all published content. No automation of rights, activation, or collection publication. |
| Transparency and explainability | `fm_inference_record` traces every FM-influenced decision. FMC Invariant FM-2 (inference record invariant). |
| Robustness, security and safety | Fallback hierarchy (§III.3). Model unavailability does not cause platform failure (R&SI P-2). Output validation before human queue. |
| Accountability | PA owns AI governance. Curator owns editorial AI outputs. Human who approves a candidate is accountable for that decision. Annual provider audit. |

---

## XVIII. Conditions

### Conditions for Approval

**C-1 (FMC Stack Conflict):** Draft and ratify FMC v1.0 Amendment 1 updating the intelligence fabric diagram and `context_layers_required` field vocabulary to reflect the frozen stack (PostgreSQL + PostGIS + pg_trgm, no Neo4j, no pgvector). Non-blocking for Phase 0 use cases. Required before any `context_layers_required` field is used in production.

**C-2 (DD-AI-001 — Claude Activation):** File DD-AI-001 to formally activate Claude as the primary FM. Must address: provider governance assessment (FMC Article 9.2), training exclusion confirmation, version pinning protocol, authorized use cases list. This document is the precursor; DD-AI-001 is the activation gate.

**C-3 (DD per API Provider):** Before any API provider other than Anthropic is activated: file the corresponding DD (DD-AI-002 for Google/Gemini, DD-AI-003 for OpenAI) addressing FMC Article 9.2 requirements. Zero Data Retention agreement required for OpenAI. Enterprise agreement required for Google.

**C-4 (DD per Local Model):** Before any local model is deployed: file the corresponding DD (DD-AI-004 through DD-AI-007+ for Qwen, DeepSeek, Mistral, Gemma, Llama, Phi). Include: license confirmation, compute requirements, version pinning, authorized use cases.

**C-5 (Prohibited Phrases Validator):** Before any model call produces output destined for a public surface, the prohibited pattern validator (§XIV.3) must be implemented and tested against the NC-WEB-001 §IV prohibited copy register and the NC-AI-001 §X.3 prohibited output register.

**C-6 (Entity ID Hallucination Block):** Before any entity-reconciliation or place-story use case goes to production, the entity ID validation (§XV.3) must be implemented: any FM-generated GeoNames ID, GBIF taxon key, or Wikidata QID must be validated against canonical sources before acceptance.

**C-7 (First Model Activation — Phase 0 Use Cases):** The first production use case (recommended: `subject_term_classification` or `editorial_content_assistance` for product copy drafts) must complete the full FMC Article 24–25 activation gate sequence: `foundation_model_registry` entry → DD-AI-001 → second-human approval → `status = 'active'` → prompt template approved → staging test inference record.

**C-8 (Cost Monitoring):** Before API models are called in production: implement `fm_inference_record.token_count_input` + `token_count_output` monitoring and the monthly cost report by use case (§XII.4).

---

## XIX. Decision

**APPROVE WITH CONDITIONS**

The NC-AI-001 AI Governance Architecture Blueprint is approved as the governing reference for all AI use in the Nature & Culture platform, subject to the 8 conditions in §XVIII.

The Foundation Model Constitution v1.0 remains the senior constitutional document. NC-AI-001 extends it with task routing, model classification, cost controls, and external alignment. No provision of NC-AI-001 may be interpreted to grant FM outputs canonical authority or to relax any FMC constitutional invariant.

**Priority sequence for condition resolution:**

1. **C-2 (DD-AI-001 — Claude):** First. Claude is already in use for governance work; this formalizes and governs that use.
2. **C-5 (Prohibited Phrases Validator):** Before any model output reaches a product page.
3. **C-1 (FMC Stack Conflict Amendment):** Before any production use case with `context_layers_required`.
4. **C-7 (First Model Activation):** Gates all production AI use.
5. **C-3 + C-4 (Provider DDs):** As each provider/model is onboarded.
6. **C-6 (Entity ID Hallucination Block):** Before place story or entity reconciliation use cases.
7. **C-8 (Cost Monitoring):** Before scale.

**Zero-tolerance rules that apply immediately, before any condition is resolved:**
- FM-4 (rights hardening) — no model may output a rights determination. Permanent. Unconditional.
- FM-5 (commerce score gate) — no model output enters commerce scoring. Permanent. Unconditional.
- AI-ATT-1 (attribution preservation) — attribution strings are retrieved, not generated. Permanent. Unconditional.
- FS-001 equivalence — no model may output NARA attribution for Earthrise or "Verified by NASA" language. Permanent. Unconditional.
- User behavioral data exclusion — no model call may include user behavioral, purchase, or browsing data as context. Permanent. Unconditional.

---

*NC-AI-001 v1.0 — drafted 2026-06-12. Pending ratification.*
*Reference models: Foundation Model Constitution v1.0 · Strategic Direction v1 · Wireframe Constitution v1 · NC-PILOT-001-FRR · NC-PRODUCT-001 · NC-WEB-001 · NC-WEB-001-LA · DD-GBIF-001 · DD-WIKIDATA-001 · DD-GEONAMES-001 · DD-OSM-001 · DD-NOAA-001*
*External alignment: UNESCO Recommendation on the Ethics of AI (2021) · UN Global Digital Compact (2024) · OECD AI Principles (2019, 2024)*
*Conditions: 8 (C-1 through C-8) — all non-blocking for Phase 0 except C-5 (prohibited phrases validator before product page model use)*
