# Foundation Model Constitution v1.0

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — governance effective immediately. No implementation authorization required. |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |

---

## Preamble

This Constitution governs how Foundation Models participate in Nature & Culture's
intelligence fabric. It answers eight questions: which models are authorized, how are
they registered, how are version changes managed, where is the candidate-to-canonical
boundary, what are the replay requirements, when do humans approve, which outputs may
influence commerce, and which outputs are permanently advisory.

The governing doctrine of this Constitution is stated in the Strategic Directive and
repeated here without modification: **AI = Advisory.** This is not a default. It is
not a starting position that can be graduated away from with sufficient Director Decisions.
It is the permanent identity of Foundation Models within NC's architecture.

Foundation Models in NC are synthesis instruments. They read context from PostgreSQL,
PostGIS, Neo4j, and pgvector. They generate candidates. They do not decide. Every
decision — canonical record creation, rights determination, activation, scoring, collection
curation — is made by a human or a constitutionally authorized automated worker operating
on governed formula. Foundation Models advise those decisions; they do not make them.

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity
Doctrine, the Universal Media Substrate Constitution, and the Relationship & Semantic
Intelligence Constitution. All five Constitutional Invariants of the Relationship &
Semantic Intelligence Constitution apply here. This Constitution adds five additional
invariants specific to Foundation Model governance.

---

## Part I — Foundations

### Article 1 — Identity and Constitutional Role

**1.1** A Foundation Model (FM) in NC is any large-scale machine learning model accessed
via API or local inference that accepts natural language or multimodal input and produces
natural language, structured, or classification output. This definition includes but is
not limited to: large language models, vision-language models, and classification models
built on foundation model architectures.

**1.2** Embedding models are governed by the Relationship & Semantic Intelligence
Constitution (Articles 9–11). An embedding model that generates dense vector
representations is not a Foundation Model under this Constitution. A model that generates
both embeddings and natural language outputs falls under both constitutions.

**1.3** The constitutional role of every FM in NC is identical regardless of capability,
provider, or output quality: **synthesis instrument producing advisory candidates**.
No FM has a different constitutional role. No FM is an authority. No FM governs.

**1.4** The Intelligence Fabric positioning:

```
PostgreSQL   (authority — facts, rights, scores, activations)
PostGIS      (spatial intelligence — projection of PostgreSQL spatial data)
pgvector     (semantic intelligence — projection of PostgreSQL content)
Neo4j        (relationship intelligence — projection of PostgreSQL relationships)
     ↓ all layers feed context to ↓
Foundation Models  (synthesis — generates advisory candidates from all context)
     ↓ outputs flow back to ↓
PostgreSQL   (candidate records — workflow_items, agent_notes, provenance)
     ↓ human approves or rejects ↓
PostgreSQL   (canonical records — governed entities)
```

The cycle is closed. FMs consume from PostgreSQL and return to PostgreSQL. They do not
break the cycle. They do not short-circuit the human approval step.

### Article 2 — Scope

This Constitution governs:

| Entity | Purpose |
|---|---|
| `foundation_model_registry` | Authorized models, providers, capability types, activation status |
| `fm_prompt_template_registry` | Versioned prompt templates governing FM calls |
| `fm_inference_record` | Append-only provenance record for every governed FM call |
| `fm_candidate_record` | Structured output of a governed FM call, pending human review |
| Authorized use case vocabulary | Which tasks FMs may perform |
| Permanently advisory output vocabulary | Which outputs may never become canonical |
| Commerce boundary rules | How FM outputs relate to the scoring pipeline |

This Constitution does not govern: PostgreSQL schema (Media Substrate Constitution),
embedding models (R&SI Constitution), product pricing, collection curation decisions
(human authority), or rights determination (Media Substrate Constitution, Article 1.5).

### Article 3 — Authority Hierarchy and Precedence

**3.1** The Strategic Directive doctrine "AI = Advisory" is the superseding principle.
No article in this Constitution may be interpreted to grant FM outputs canonical authority.
Where this Constitution is silent, the Advisory doctrine governs.

**3.2** This Constitution is senior to all worker configurations, API contracts, and
application logic that calls Foundation Models. A worker that calls an FM outside the
governed use case vocabulary is in violation of this Constitution regardless of the
quality of the output.

**3.3** The five invariants of the Relationship & Semantic Intelligence Constitution
(P-1 through P-5) are incorporated by reference and apply to FM outputs as follows:
P-1 (Projection Invariant) governs any FM output that becomes a Neo4j node or pgvector
embedding. P-2 (Availability Invariant) requires that FM unavailability not cause platform
failure. P-3 (Rebuild Invariant) requires that FM-derived content be rebuildable from
canonical PostgreSQL state. P-4 and P-5 (Score Gate and Rights Gate) are extended and
deepened by this Constitution.

### Article 4 — The Central Governance Principle

**4.1** All FM outputs are candidates until promoted by human approval. This is the
unconditional governing rule.

**4.2** A **candidate** is an FM-generated output stored in `fm_candidate_record` or
`workflow_items.agent_suggestions`, awaiting human review. A candidate has no canonical
authority. A candidate cannot trigger a pipeline action. A candidate cannot modify a
governed entity. A candidate is a structured advisory input to a human decision.

**4.3** A **canonical record** is a PostgreSQL row in a governed table, created through
a constitutionally authorized path (human approval or constitutionally authorized
automated worker action). The existence of a high-confidence FM output does not authorize
the creation of a canonical record without the governed path.

**4.4** The promotion of a candidate to a canonical record always requires:
- A human review decision (approve/reject) recorded in PostgreSQL, OR
- A constitutionally authorized automated promotion (Article 15) with configured confidence
  threshold and a human audit trail

**4.5** The boundary is not a technical one. It does not depend on confidence scores,
model capability, or output quality. An FM producing 100% accurate outputs is still
subject to this Constitution. The boundary is a governance principle, not an accuracy
threshold.

### Article 5 — The Ten Constitutional Invariants

Five invariants from the R&SI Constitution are incorporated by reference (P-1 through P-5).
Five additional invariants govern Foundation Models specifically.

**Invariant FM-1: The Candidate Invariant.**
All FM outputs are candidates. An FM output that directly modifies a canonical PostgreSQL
record without human review or constitutionally authorized automated promotion is a
constitutional violation. This applies regardless of the FM's confidence score or accuracy.

**Invariant FM-2: The Inference Record Invariant.**
Every FM call that produces a candidate influencing a canonical decision must produce an
`fm_inference_record` in PostgreSQL before the candidate is acted upon. An FM call without
a traceable inference record does not exist for governance purposes.

**Invariant FM-3: The Weaker Replay Guarantee Doctrine.**
FM replay cannot guarantee identical output reproduction due to the stochastic nature of
FM inference. NC acknowledges this as an accepted and permanent property of FM governance.
The replay guarantee covers: (a) input context reconstruction from `fm_inference_record`
fields; (b) decision traceability from candidate to canonical record; (c) model and prompt
version attribution. It does not cover exact output reproduction. This weakness must be
recorded as a replay caveat in any audit that relies on FM-influenced decisions.

**Invariant FM-4: The Rights Hardening Invariant.**
No FM output may directly or indirectly set, suggest, or influence
`media_rights.rights_status` as a canonical record. No FM output may be presented to a
human rights verifier as a rights determination rather than as advisory context. Rights
determinations are permanently and unconditionally human-verified. This invariant cannot
be lifted by Director Decision, constitutional amendment, or any other mechanism.

**Invariant FM-5: The Commerce Score Gate.**
No FM output may enter the commerce scoring pipeline (`commerce_opportunities.score_inputs`,
`csm_score`, `commerce_opportunity_score`) without a ratified amendment to the Commerce
Intelligence Constitution naming the specific FM output type and its weight. This invariant
cannot be lifted by Director Decision alone. It extends and deepens R&SI Constitution
Invariant P-4.

---

## Part II — Model Registry

### Article 6 — Foundation Model Registry

**6.1** Every FM that NC calls must be registered in `foundation_model_registry` before
its first call. An unregistered FM call is a constitutional violation. The registry is
the sole authority for which models NC uses.

**6.2** Required fields per registry entry:

| Field | Governance requirement |
|---|---|
| `model_id` | Canonical identifier. Immutable. Format: `{provider}:{family}:{version}` (e.g., `anthropic:claude-3-7-sonnet:20250219`). |
| `provider` | The model provider organization. |
| `model_family` | The model family name (e.g., `claude-3`, `gpt-4o`, `gemini-1.5`). |
| `model_version` | The exact pinned version string as provided by the vendor. Immutable on INSERT. |
| `capability_types` | Array. Values from the Article 7 vocabulary. |
| `authorized_use_cases` | Array. Values from the Article 10 vocabulary. Set at activation. |
| `context_window_tokens` | Maximum context window in tokens. For planning. |
| `output_format_constraint` | `json_schema` / `structured_text` / `free_text`. |
| `status` | `proposed` → `approved` → `active` → `suspended` → `retired`. |
| `activation_director_decision` | DD-X reference. Required before `status = 'active'`. |
| `activated_by` | Second-human approval identity. |
| `activated_at` | Timestamp of activation. |
| `retired_at` | Timestamp of retirement. NULL if not retired. |
| `retirement_reason` | Plain-language reason. Required on retirement. |

**6.3** The `foundation_model_registry` is governed by a no-DELETE rule. Retired entries
are marked `status = 'retired'`. The row is never removed. Retired `model_id` values are
permanently reserved and may not be reused for a different model.

**6.4** At most one model per `{provider}:{family}` combination may have
`status = 'active'` for a given use case category at any time. Activating a new version
of an existing model family requires retiring the prior version (Article 8).

### Article 7 — Model Capability Type Vocabulary

The capability type vocabulary is constitutional. New types require a constitutional
amendment.

| capability_type | Description | Governing standard |
|---|---|---|
| `text_generation` | Generates natural language output from text input | — |
| `vision_analysis` | Analyzes image content from visual input | IIIF Image API for image delivery to model |
| `structured_classification` | Returns a classification label from a governed vocabulary | Output must match a governed vocabulary |
| `multimodal_synthesis` | Generates output from combined text + image input | — |

Embedding generation (`embedding`) is governed by the R&SI Constitution, not this one.

### Article 8 — Model Version Governance

**8.1** Model version governance applies when an active model's pinned version changes.
FM providers may silently update models. NC must pin exact versions and be notified of
changes. A version change is not automatically authorized.

**8.2** Three types of version change, with different governance requirements:

| Change type | Definition | Governance required |
|---|---|---|
| **Patch** | Same provider + family + capability, minor update (e.g., safety adjustments, inference speed). Provider confirms behavioral equivalence. | Director notification. New registry entry with `status = 'active'`. Prior entry retired. |
| **Major** | Same provider + family, but new training data cutoff, significant capability change, or provider-declared breaking change. | Director Decision required. New registry entry. Prior entry retired. All `fm_inference_record` from prior version marked `model_version_change_pending`. |
| **Provider or family change** | Moving from one provider/family to another (e.g., replacing an OpenAI model with an Anthropic model for a use case). | Director Decision + second-human approval. New entry. Constitutional amendment if the change affects a use case that feeds commerce scoring. |

**8.3** When a model is retired, all `fm_inference_record` entries that reference it retain
their `model_id` FK as a permanent historical record. Retired model records cannot be
deleted (no-DELETE rule). Future replay must acknowledge the version caveat (Invariant FM-3).

**8.4** NC must not rely on implicit model versioning by providers (e.g., calling
`gpt-4` without pinning a dated version). All registry entries must pin an exact version
string. If a provider does not support version pinning, that provider may not be used in
a governed FM call. This rule may not be waived.

### Article 9 — Provider Governance

**9.1** An FM provider is an organization that hosts and serves FM inference via API or
provides model weights for local deployment.

**9.2** Before a provider's first model may be activated, the Director must record a
provider authorization decision in `foundation_model_registry.activation_director_decision`
that explicitly addresses:
- Data residency: does NC's query content leave a governed jurisdiction?
- Training data exclusion: is NC's query content excluded from provider training?
- Rate limiting: are rate limits sufficient for NC's operational requirements?
- Vendor lock-in risk: what is the rebuild path if this provider is unavailable?

**9.3** A provider that uses NC's query content for training without explicit opt-out
confirmation is not authorized. Provider authorization must be re-confirmed annually.

---

## Part III — Use Case Governance

### Article 10 — Authorized Use Case Vocabulary

The use case vocabulary is constitutional. New use cases require a constitutional
amendment naming the capability type, stakes level, auto-apply eligibility, and the
governing confidence threshold if auto-apply is permitted.

| use_case_id | Capability type | Stakes | Auto-apply eligible | Confidence threshold |
|---|---|---|---|---|
| `subject_term_classification` | structured_classification | Low | Yes | ≥ 0.92 |
| `anchor_type_classification` | structured_classification | Medium | Yes | ≥ 0.96 |
| `creator_identity_resolution` | structured_classification | Medium | Yes | ≥ 0.96 |
| `illustration_opportunity_scoring` | text_generation | Medium | No | — |
| `place_relevance_advisory` | text_generation | Medium | No | — |
| `image_quality_advisory` | vision_analysis | High | No | — |
| `rights_analysis_advisory` | text_generation | Critical | **Never** | Invariant FM-4 |
| `collection_theme_suggestion` | text_generation | Medium | No | — |
| `editorial_content_assistance` | text_generation | Low | No (always advisory) | — |
| `discovery_enrichment_synthesis` | multimodal_synthesis | Medium | No | — |

**10.1** "Auto-apply eligible" means a candidate may be promoted to canonical status
without per-record human review, subject to the confidence threshold and the conditions
of Article 15. Auto-apply is always subject to a human audit trail and a human-reviewable
queue of all auto-applied records.

**10.2** "Stakes" governs the human review requirement and the audit retention period:

| Stakes | Human review | Audit retention |
|---|---|---|
| Low | Periodic batch review | 12 months |
| Medium | Per-record review or auto-apply with confidence threshold | 24 months |
| High | Per-record human approval required | 36 months |
| Critical | Per-record human approval required; FM output advisory only | Permanent |

**10.3** Use cases with `Stakes = Critical` are permanently non-promotable by automated
means regardless of confidence score. The FM provides context. A human decides. This is
not a threshold; it is a category.

### Article 11 — Authorized Use Case Definitions

**11.1 — `subject_term_classification`**

Given: `source_item` metadata (title, publication_title, illustrator, anchor_type).
Output: Array of TGM subject term candidates, each with confidence score.
Canonical path: Auto-applied at confidence ≥ 0.92 per term. Terms below threshold go
to workflow_item for human review. Canonical record: update to
`media_technical_metadata.content.subject_terms` after auto-apply or human approval.

**11.2 — `anchor_type_classification`**

Given: `source_item` metadata (title, taxon_name, concept linkage, institution,
place connections).
Output: `anchor_type` classification (biological / geographic / cultural / mixed)
with confidence.
Canonical path: Auto-applied at confidence ≥ 0.96. Below threshold: workflow_item.
Canonical record: `illustration_opportunities.anchor_type`.
Note: anchor_type directly affects which scoring formula is applied (CI Constitution).
This is an indirect commerce influence (Article 19).

**11.3 — `creator_identity_resolution`**

Given: Illustrator name string as found in source_record (e.g., "J.J. Audubon",
"Audubon", "John J. Audubon").
Output: Candidate `creator_authority_registry.creator_id` match with confidence.
Canonical path: Auto-applied at confidence ≥ 0.96. Below threshold: workflow_item.
Canonical record: `illustration_opportunities.illustrator` normalized to authority form.

**11.4 — `illustration_opportunity_scoring`**

Given: BHL search result metadata + place context + concept context + institution.
Output: Structured advisory score across quality dimensions (composition, era, provenance,
place relevance) with natural language rationale.
Canonical path: Always workflow_item. Human reviews and may use as context for their
own scoring judgment. FM output never directly sets `commerce_opportunities` fields.

**11.5 — `place_relevance_advisory`**

Given: `source_item` metadata + target `place` context + PostGIS spatial data.
Output: Advisory relevance score (0.0–1.0) with rationale for why this asset is or is
not relevant to this place.
Canonical path: Always workflow_item. FM output may inform the human-confirmed
`illustration_opportunity_places.relevance_score` but does not set it.

**11.6 — `image_quality_advisory`**

Given: Image file via IIIF Image API (vision model) + `media_technical_metadata.content`.
Output: Advisory quality assessment across governed dimensions: composition, artistic
quality, botanical/scientific accuracy, print suitability.
Canonical path: Human confirmation required. FM output goes to workflow_item. Human
curator reviews and records their judgment. FM output is explicitly labeled as advisory
in the workflow_item.
Note: image quality assessment directly informs `commerce_opportunities.image_quality_score`,
making this a high-stakes use case with direct commerce proximity (Article 18).

**11.7 — `rights_analysis_advisory`**

Given: `source_record.raw_payload` + institution rights strategy + publication year.
Output: Advisory PD analysis with reasoning chain.
Canonical path: **None.** Invariant FM-4. FM output is stored in `workflow_item.agent_suggestions`
as advisory context for the human rights verifier. The FM output is labeled "Advisory only —
human verification required" in the workflow_item. The FM output must never be shown
to the human verifier in a way that presents it as a determination rather than as context.
The human verifier makes an independent determination. See Article 16.

**11.8 — `collection_theme_suggestion`**

Given: Array of activated `source_item` IDs + place context.
Output: Candidate collection theme (title, summary, collection_type, suggested sequence).
Canonical path: workflow_item. Human curator reviews, may accept, modify, or reject.
If accepted, curator creates the canonical `collections` record.

**11.9 — `editorial_content_assistance`**

Given: Place context, asset selection, desired story angle.
Output: Draft editorial text for NC-authored stories.
Canonical path: NC-authored stories require human authorship. FM output is a draft
that a human editor must substantially review, revise, and approve. FM-generated text
that appears verbatim in a published story without human editorial review is a governance
violation. This use case is permanently advisory regardless of FM output quality.

**11.10 — `discovery_enrichment_synthesis`**

Given: Full intelligence fabric context for a `source_item` — PostgreSQL canonical data +
PostGIS spatial context + Neo4j relationship traversal results + pgvector semantic
similarity results.
Output: Structured synthesis of all context layers, generating: related item candidates,
place connection candidates, collection membership candidates, subject term candidates.
Canonical path: All outputs are candidates. Each candidate type follows its own governed
canonical path (Articles 11.1–11.8). The synthesis output is a batch of candidates of
multiple types; each candidate is governed by its own use case rules.

### Article 12 — Prohibited Use Cases

The following uses of Foundation Models are constitutionally prohibited. A constitutional
amendment is required to permit any of the following — Director Decision alone is
insufficient.

**12.1 — Rights determination.** FM may not produce a canonical rights status. FM may not
be the sole basis for advancing a `source_item` from `acquired` to `rights_verified`.
FM rights analysis is advisory context only (Invariant FM-4).

**12.2 — Activation approval.** FM may not approve an `activation_target`. The second-human
rule (Media Substrate Constitution, Article 25) applies. FM may generate a recommendation
in `workflow_item.agent_suggestions`; a human approves.

**12.3 — Commerce score computation.** FM may not directly compute `csm_score`,
`commerce_opportunity_score`, or any subscore in `commerce_opportunities`. Scoring is
governed by the CI Constitution. FM outputs may feed into scoring only after a CI
Constitution amendment (Invariant FM-5).

**12.4 — Collection publication.** FM may not set `collections.status = 'published'`.
Collection publication requires human approval and the governed `check_collection_publishable`
trigger.

**12.5 — User behavior profiling.** FM may not be called with user behavioral data as
context. The Wireframe Constitution permanently prohibits behavioral personalization. FM
calls must not reference user purchase history, browsing history, or behavioral patterns.

**12.6 — Provenance fabrication.** FM may not generate provenance data (creator attribution,
date attribution, institution attribution, rights evidence) for presentation as factual
rather than advisory. All provenance data in NC is sourced from governed institutions.
FM may assist in resolving ambiguous provenance as a structured hypothesis; it may not
assert provenance as fact.

---

## Part IV — Candidate vs. Canonical Boundary

### Article 13 — Candidate Record Requirements

**13.1** An FM candidate is an FM output that has been recorded in PostgreSQL but has
not been promoted to a canonical governed record. Every governed FM call that produces
output intended to influence a canonical decision must produce a candidate record.

**13.2** Candidate records live in one of two places:
- `fm_candidate_record` — for structured, high-fidelity FM outputs that require dedicated
  tracking (medium and high stakes use cases)
- `workflow_items.agent_suggestions` — for lightweight advisory outputs embedded in an
  existing workflow (low stakes use cases, discovery enrichment)

**13.3** Required fields for `fm_candidate_record`:

| Field | Governance requirement |
|---|---|
| `candidate_id` | UUID. PostgreSQL authority. |
| `inference_record_id` | FK to `fm_inference_record`. Required. |
| `use_case_id` | FK to authorized use case vocabulary. |
| `source_entity_type` | The PostgreSQL table of the entity this candidate pertains to. |
| `source_entity_id` | The PostgreSQL UUID of the entity this candidate pertains to. |
| `candidate_payload` | JSONB. The structured FM output. |
| `confidence_score` | NUMERIC(4,3). NULL if FM does not produce a confidence score. |
| `status` | `pending_review` → `approved` / `rejected` / `auto_applied` / `expired`. |
| `reviewed_by` | Identity of the human reviewer. NULL until reviewed. |
| `reviewed_at` | Timestamp of review. |
| `review_notes` | Free text. |
| `promoted_record_id` | UUID. The canonical record created from this candidate, if approved. NULL otherwise. |
| `auto_applied` | Boolean. TRUE if promoted without per-record human review (Article 15). |
| `expires_at` | Timestamp. Unreviewed candidates expire after 90 days. |
| `created_at` | Timestamp. |

**13.4** A candidate record is append-only once `status IN ('approved', 'rejected',
'auto_applied')`. The review decision is immutable. The candidate payload is immutable
on INSERT.

**13.5** Expired candidates (`expires_at` reached without review) transition to
`status = 'expired'`. An expired candidate is not automatically regenerated. The
originating workflow_item remains in the queue and triggers a re-run if the source
entity is still in scope.

### Article 14 — Canonical Promotion Protocol

**14.1** The canonical promotion protocol is the governed sequence for converting an
FM candidate into a canonical PostgreSQL record.

For per-record human review:

```
1. FM call produces fm_inference_record + fm_candidate_record
        ↓
2. fm_candidate_record surfaced in human review queue (workflow_item or direct)
        ↓
3. Human reviews candidate payload and confidence
        ↓ approve ────────────────────────────────────────────────────────────┐
        ↓ reject                                                               │
4a. fm_candidate_record.status = 'rejected'                                   │
    rejection_reason recorded                                                  │
    workflow_item closed                                                       │
    No canonical record created.                                               │
                                                                               │
4b. Human creates or updates canonical PostgreSQL record ◄─────────────────────┘
    fm_candidate_record.status = 'approved'
    fm_candidate_record.promoted_record_id = new canonical record UUID
    provenance of canonical record includes fm_inference_record.inference_id
```

**14.2** The second-human rule applies to all canonical promotions that are governed
by the second-human rule in the Media Substrate Constitution. A human who generated
the FM call may not also approve the resulting candidate for those governed entities.

### Article 15 — Auto-Apply Protocol

**15.1** Auto-apply is the constitutionally authorized promotion of FM candidates to
canonical records without per-record human review. It is permitted only for use cases
designated `Auto-apply eligible: Yes` in the Article 10 vocabulary, and only when the
candidate's `confidence_score` meets or exceeds the governed threshold.

**15.2** Auto-apply requirements:

- `use_case_id` must be in the auto-apply eligible list (Article 10)
- `confidence_score ≥ governed threshold` for the use case
- A Director Decision authorizing auto-apply for this use case must be active
- A human-reviewable audit log of all auto-applied records must exist
- A human review batch covering the last 30 days of auto-applies must be completed
  monthly by a designated reviewer

**15.3** Auto-apply does not exempt a record from the human audit requirement. The
monthly batch review is constitutionally required. If a human reviewer finds systemic
errors in auto-applied records, they must flag the use case for suspension and record
the finding. The Director then decides whether to suspend auto-apply for the affected
use case.

**15.4** Auto-apply is suspended automatically if: `confidence_score` drops below
threshold in three consecutive candidates for the same use case, or if a human reviewer
flags more than 5% of auto-applied records in a monthly batch as incorrect.

### Article 16 — Permanently Advisory Outputs

**16.1** The following use case outputs are permanently advisory. They may never be
promoted to canonical records by any mechanism — automated or human. They may only exist
as advisory context in `fm_candidate_record` or `workflow_items.agent_suggestions`.

This list is constitutional. Removing a use case from this list requires a constitutional
amendment. Director Decision is not sufficient.

| Use case | Reason permanently advisory |
|---|---|
| `rights_analysis_advisory` | Invariant FM-4. Rights determinations are permanently human-verified. |
| Any output asserting `media_rights.rights_status` | Invariant FM-4. Regardless of which use case generates it. |
| Any output asserting `activation_target.status = 'approved'` | Activation is human-governed. |
| Any output asserting `collections.status = 'published'` | Collection publication is human-governed. |
| Any FM output presented as provenance | Provenance is sourced from governed institutions, not generated. |
| Any FM output presented as a rights statement URI | Rights statement URIs are from the governed vocabulary (Article 24.1 of Media Substrate Constitution). FM does not select them. |

**16.2** A workflow_item that presents a permanently advisory FM output to a human must
clearly label the output as "Advisory — human determination required." The label is
constitutional; it may not be removed by UI configuration.

---

## Part V — Commerce Boundary

### Article 17 — The Commerce Boundary Defined

**17.1** The commerce boundary is the line between FM outputs that are entirely upstream
of commercial scoring and FM outputs that could affect the numbers that determine
`csm_tier` and product eligibility.

**17.2** Three categories:

| Category | Definition | Governance |
|---|---|---|
| **Direct commerce influence** | FM output directly appears in `commerce_opportunities.score_inputs` or modifies a score column. | Requires CI Constitution amendment (Invariant FM-5). |
| **Indirect commerce influence** | FM output modifies a field that is consumed by a scoring formula (e.g., `anchor_type`, `subject_terms`). | Requires Director Decision documenting the indirect path. |
| **Commerce-isolated** | FM output affects only discovery, editorial, or provenance — no path to a scoring formula. | No special approval beyond use case activation. |

### Article 18 — Direct Commerce Influence (Invariant FM-5)

**18.1** No FM output may appear in `commerce_opportunities.score_inputs` without a
ratified CI Constitution amendment. The amendment must:
- Name the specific `use_case_id` and FM output field
- Specify the weight or role of the FM output in the formula
- Specify the replay requirements for the specific signal
- Pass second-human approval
- Reference this article by number

**18.2** The Score Gate cannot be bypassed by routing FM output through an intermediate
worker that applies the output to a scoring field without recording the FM provenance.
Any field in `score_inputs` that is derived from FM output must be labeled with the
`fm_inference_record.inference_id` in the JSONB.

**18.3** The Score Gate applies to all FM capability types equally. A structured
classification model classifying anchor_type is subject to the same governance as a
generative model providing quality assessment, if that output enters scoring.

### Article 19 — Indirect Commerce Influence

**19.1** Indirect commerce influence occurs when an FM output modifies a non-scoring
field that a scoring formula subsequently reads. Current indirect influence pathways:

| FM output | Field modified | Scoring formula dependency |
|---|---|---|
| `anchor_type_classification` | `illustration_opportunities.anchor_type` | CI Constitution formula_spec uses anchor_type to select composite weights |
| `subject_term_classification` | `media_technical_metadata.content.subject_terms` | pgvector space content, potential future scoring signal |
| `creator_identity_resolution` | `illustration_opportunities.illustrator` (normalized) | `creator_prestige_registry` lookup in Asset Intelligence scoring |
| `place_relevance_advisory` (if human-promoted) | `illustration_opportunity_places.relevance_score` | `place_relevance_score` in CI scoring |

**19.2** For each indirect influence pathway, the Director must record a Director Decision
acknowledging the pathway and confirming that:
- The indirect influence is governed
- The FM output contributing to the field is recorded in the field's entity's `provenance`
- Human review is in the promotion chain
- The pathway is disclosed in `commerce_opportunities.score_inputs` where technically
  feasible

**19.3** A new indirect influence pathway discovered after this Constitution is ratified
must be reported to the Director within one week of discovery and a Director Decision
must address it within 30 days.

### Article 20 — Commerce-Isolated FM Use

**20.1** FM outputs that have no path to a scoring formula require no commerce-specific
governance beyond their use case activation. The following use cases are currently
commerce-isolated:

- `editorial_content_assistance` — affects story text only
- `collection_theme_suggestion` — affects collection framing; collection membership
  is governed separately; the suggestion does not set scoring signals

**20.2** A use case that is currently commerce-isolated may become an indirect influence
pathway if the scoring model is amended. The CI Constitution amendment that creates this
new dependency must identify the use case and add it to the Article 19.1 table.

---

## Part VI — Replay Requirements

### Article 21 — Inference Record Requirements

**21.1** An `fm_inference_record` is the provenance record for a governed FM call. It is
required for all calls under use cases with Stakes ≥ Medium, and for all calls that produce
a candidate influencing a canonical decision. Low-stakes, commerce-isolated use cases may
use batch inference records (one record per batch of N calls) if Director Decision authorizes.

**21.2** Required fields for `fm_inference_record`:

| Field | Governance requirement |
|---|---|
| `inference_id` | UUID. PostgreSQL authority. |
| `model_id` | FK to `foundation_model_registry.model_id`. |
| `model_version` | The exact version string at inference time. Immutable. |
| `prompt_template_id` | FK to `fm_prompt_template_registry.template_id`. |
| `prompt_version` | The exact prompt template version at inference time. |
| `use_case_id` | FK to the authorized use case vocabulary. |
| `context_sources` | JSONB. Records which layers were queried for context: `{"postgresql": ["table.id"], "neo4j": ["schema_version"], "pgvector": ["space_name", "model_id"]}` |
| `input_hash` | SHA-256 of the fully-constructed prompt sent to the model (after variable substitution). Enables detection of identical inputs. |
| `output_hash` | SHA-256 of the raw FM output before parsing. |
| `output_parsed` | JSONB. The structured, parsed output. |
| `latency_ms` | Inference latency in milliseconds. |
| `token_count_input` | Input tokens consumed. |
| `token_count_output` | Output tokens consumed. |
| `worker_id` | The worker that made the FM call. |
| `called_at` | Timestamp. |

**21.3** The `fm_inference_record` table is append-only. No UPDATE or DELETE is permitted.

**21.4** `context_sources` must be populated completely and honestly. A worker that calls
an FM with context from Neo4j but omits `neo4j` from `context_sources` is in violation
of Invariant FM-2.

### Article 22 — The Weaker Replay Guarantee (Invariant FM-3 Implementation)

**22.1** NC's replay guarantee for FM-influenced decisions covers three things and
explicitly does not cover a fourth:

**Covered:**
1. Input reconstruction: Given `fm_inference_record.prompt_template_id`,
   `prompt_version`, and `context_sources`, the input prompt can be reconstructed for
   any past inference, subject to the availability of the source PostgreSQL, Neo4j, and
   pgvector state at that historical moment.
2. Decision traceability: `fm_candidate_record.inference_record_id` + 
   `fm_candidate_record.promoted_record_id` creates a traceable chain from canonical
   record back to FM output back to inference input.
3. Model attribution: `fm_inference_record.model_id` + `model_version` identifies
   exactly which model produced which output.

**Not covered:**
4. Output reproduction: Running the same prompt against the same model version will not
   reliably produce the same output. This is an accepted property of FM inference.
   Replay audits must acknowledge this caveat explicitly.

**22.2** When a replay audit encounters a retired model (`foundation_model_registry.status
= 'retired'`), the auditor must record: "Exact output reproduction is not possible. The
model `{model_id}` at version `{model_version}` is retired. The decision traceability
chain is intact. The input reconstruction is available. The original output is preserved
in `fm_inference_record.output_parsed`."

**22.3** The caveat does not invalidate the original decision. A human reviewed and
approved the original candidate. That approval is the canonical decision. The FM output
was advisory input to that decision. The approval record is the authoritative fact;
the FM output is the advisory context.

### Article 23 — Prompt Template Governance

**23.1** A prompt template is the governing input specification for an FM call. It defines
what context variables are injected, what output format is required, and what instructions
constrain the FM's response. Prompt templates are versioned assets with constitutional status.

**23.2** Required fields for `fm_prompt_template_registry`:

| Field | Governance requirement |
|---|---|
| `template_id` | UUID. PostgreSQL authority. |
| `template_name` | Human-readable name. |
| `use_case_id` | FK to authorized use case vocabulary. |
| `template_version` | Semantic version (e.g., `1.0.0`). |
| `template_text` | The prompt template with variable placeholders. Immutable on INSERT. |
| `variable_schema` | JSONB. Defines what variables are injected and their source tables. |
| `output_schema` | JSONB. JSON Schema for the required structured output. |
| `context_layers_required` | Array. Which intelligence layers must be queried before this prompt is called (`postgresql` / `postgis` / `neo4j` / `pgvector`). |
| `stakes_level` | Inherited from use_case_id. Documented here for prompt-level visibility. |
| `status` | `draft` → `approved` → `active` → `retired`. |
| `approved_by` | Second-human approval required before `status = 'active'`. |
| `approved_at` | Timestamp. |

**23.3** A prompt template may not be modified after `status = 'active'`. Changes create
a new version entry. The prior version is retired. All ongoing FM calls transition to the
new version within one projection cycle. `fm_inference_record` entries always reference
the version active at call time.

**23.4** Prompt templates that include scoring signals (fields from `commerce_opportunities`
or `score_inputs`) require Director review before approval. Director Decision must
acknowledge that the prompt template creates an indirect commerce influence pathway
(Article 19).

**23.5** Prompt templates must never include: user behavioral data, personal information,
raw `media_rights.rights_evidence` (this would expose evidence to the FM provider without
governance justification), or unpublished NC collection strategy.

---

## Part VII — Human Governance

### Article 24 — Model Activation Gate

**24.1** Before any FM model may be called in production, its `foundation_model_registry`
entry must have `status = 'active'` with a valid Director Decision reference and
second-human approval.

**24.2** The activation gate sequence:

```
1. Engineer proposes model: INSERT into foundation_model_registry (status = 'proposed')
        ↓
2. Director Decision recorded (DD-X):
   - Provider governance assessment completed (Article 9.2)
   - Capability types declared
   - Authorized use cases declared
   - Version pinning confirmed
   - Replay path confirmed
        ↓
3. Second-human approves registry entry
        ↓
4. UPDATE foundation_model_registry SET status = 'active'
        ↓
5. Workers may begin calling this model for authorized use cases
```

**24.3** A model activated for specific use cases may not be used for other use cases
without a Director Decision amending `authorized_use_cases`. Using an active model for
an unauthorized use case is a constitutional violation.

### Article 25 — Use Case Activation Gate

**25.1** An authorized use case (Article 10) is not operational until:
- The model to be used has been activated for this use case (Article 24)
- A prompt template has been approved for this use case (Article 23)
- If auto-apply eligible: a Director Decision authorizing auto-apply for this use case
  is active (Article 15.2)
- At least one test inference record exists from a staging environment

**25.2** First production use of a new use case requires Director awareness. The Director
need not approve individual inferences, but must be notified of use case activation and
must have reviewed the prompt template before the template is approved.

### Article 26 — Candidate Promotion Gate

**26.1** For high-stakes and critical use cases, the candidate promotion gate is:

```
fm_candidate_record.status = 'pending_review'
        ↓ surfaced in human review queue
        ↓ human reviews candidate payload, confidence, and source inference
        ↓ human makes independent judgment (not just confirms FM output)
        ↓ approve / reject
        ↓
canonical record created (approve) OR candidate rejected (reject)
```

**26.2** The second-human rule applies to candidate promotions that govern entities
subject to the second-human rule in the Media Substrate Constitution. The same human
who initiated the FM call may not promote the resulting candidate for those entities.

**26.3** Human reviewers of FM candidates are responsible for their review judgment,
not for the FM output. A human who approves an FM candidate must be prepared to defend
their approval decision — not the FM's output. The FM provided context; the human decided.

### Article 27 — Worker Authority Boundaries

**27.1** FM workers are authorized to:
- Call FM APIs for authorized use cases with active models
- Write `fm_inference_record` records to PostgreSQL
- Write `fm_candidate_record` records to PostgreSQL
- Update `workflow_items.agent_suggestions` with FM candidates
- Auto-apply candidates meeting the auto-apply criteria (Article 15)
- Query all intelligence layers (PostgreSQL, PostGIS, Neo4j, pgvector) for context

**27.2** FM workers are not authorized to:
- Write to any governed entity table directly (rights, activation, scoring, collections)
- Call FM APIs for prohibited use cases (Article 12)
- Use unregistered models
- Use models for unauthorized use cases
- Modify `fm_inference_record` or `fm_candidate_record` after INSERT
- Suppress or omit `context_sources` from inference records
- Call FM APIs with user behavioral data as context
- Present FM rights analysis as a determination rather than advisory context

---

## Open Questions

| OQ | Question | Recommended resolution |
|---|---|---|
| OQ-1 | Should `fm_inference_record` be a separate table or stored as JSONB within `workflow_items.provenance`? | Separate table. Inference records are high-volume, require dedicated indexing on `model_id` and `called_at`, and serve a different governance purpose than workflow provenance. Merging them obscures the provenance chain. |
| OQ-2 | What is the batch inference record policy for `editorial_content_assistance`? | One inference record per story session (a session is one FM call per story draft). Not per token or per paragraph. Rationale: editorial assistance is low-stakes and batch; the cost of per-paragraph inference records exceeds their governance value. |
| OQ-3 | Should `rights_analysis_advisory` be in the authorized use case vocabulary at all, given that it is permanently advisory and cannot be promoted? | Yes. Explicitly governing it prevents workers from calling FMs for rights analysis under a different use case label to evade FM-4. The constitution must name the use case precisely so the prohibition is unambiguous. |
| OQ-4 | How should the monthly auto-apply audit (Article 15.3) be operationalized? | Director nominates a designated human reviewer for each auto-apply use case. The reviewer receives a monthly report of all auto-applied records. The report must be reviewed and signed off before the next month's auto-apply quota is renewed. Quota renewal is a Director Decision. |
| OQ-5 | Which FM should be the initial registered model? | This is Director Decision DD-AI-001 (to be recorded separately). The model must meet the version pinning requirement (Article 8.4) and pass provider governance assessment (Article 9.2). Both Anthropic Claude and OpenAI GPT families meet minimum requirements. The Director chooses based on commercial terms, data residency, and training exclusion confirmation. |
