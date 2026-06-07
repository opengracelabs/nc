# Europeana Activation Checklist v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |
| Goal | Europeana → activated NC production source |
| Authority | MSC v1.2 · Standards Constitution v1.0 · CI Constitution v1.2 · Europeana Rights Matrix v1.0 |

---

## Current State Assessment

Before the governance path begins, the existing Europeana source record must be
understood accurately. Several fields are already in place; several are missing or
ungoverned.

### What exists (Migration 17 backfill)

| Field | Current value | Assessment |
|---|---|---|
| `source_id` | `'europeana'` | Correct |
| `governance_state` | `'active'` | Set by blanket backfill — no formal Director Decision |
| `operational_status` | `'healthy'` | Correct — API key validated 2026-06-07 |
| `auth_type` | `'api_key'` | Correct |
| `entity_types` | `['cultural_object']` | Incomplete — missing `'image'`, `'map'`, `'photography'` |
| `standards` | `['cidoc_crm', 'skos', 'prov_o', 'premis']` | **Gap: `'edm'` missing** |
| `config.api_endpoint` | `https://api.europeana.eu/record/v2` | Correct |
| `config.rate_limit` | `{requests_per_second: 2, burst: 10}` | Present |
| `config.rights_strategy` | **ABSENT** | **Critical gap** |
| `config.source_role` | **ABSENT** | Gap — aggregator distinction not recorded |
| `config.completeness_minimum` | **ABSENT** | Gap — no quality floor defined |
| `config.rights_filter` | **ABSENT** | **Critical gap** — Rights Matrix cannot be applied without config |

### What the blanket backfill did not constitute

Migration 17's `governance_state = 'active'` backfill treated Europeana identically to
infrastructure sources (GeoNames, OSM, Wikidata). For those sources, blanket activation
is appropriate — they are identity and reference services, not content acquisition pipelines.

Europeana is a content acquisition source. Its `'active'` status from the backfill means the
record is valid and the API is reachable. It does not mean:

- Production ingestion has been formally authorized by Director Decision
- The Rights Matrix has been applied to the source config
- An aggregator-versus-content-institution provenance model has been defined
- Any ingestion worker has been authorized to create `source_record` rows from Europeana data

The governance path below formalizes what the backfill could not provide.

---

## Part I — Required Director Decisions

### DD-EUR-001 — Europeana Production Activation

**Status:** Required. Not yet issued.

**What this decision must authorize:**

1. Formal designation of Europeana as an active production source for NC content acquisition,
   superseding the Migration 17 blanket backfill as the authoritative activation event.

2. Classification of Europeana as an **aggregator-source** — distinct from direct institution
   sources (LOC, Smithsonian, Rijksmuseum). In NC's taxonomy, Europeana routes to content
   held by contributing institutions; it is not itself a holding institution.
   (Ref: Institution Coverage Audit v1 — Europeana reclassified as aggregator reference.)

3. Designation of the **Europeana Rights Matrix v1.0** as the governing document for all
   rights determinations on Europeana-sourced assets. The Rights Matrix is a constitutional
   prerequisite for production ingestion. No Europeana asset may be ingested without a
   Rights Matrix classification on its `edm:rights` value.

4. Designation of the **EDM tripartite provenance model** as the governing mapping for all
   Europeana-sourced assets:
   - `ore:Aggregation` → `source_record`
   - `edm:ProvidedCHO` → `source_item`
   - `edm:WebResource` → `media_file`
   (Ref: MSC v1.2 Article 29.2(a))

5. Authorization of the **aggregator provenance rule**: for any asset ingested via the
   Europeana API, `source_record.source` = `'europeana'`. The contributing institution
   (`edm:dataProvider`) is credited in the provenance record but does not require a
   separate NC source record. This rule governs until a direct institutional API
   relationship is established with the holding institution.

6. Definition of the **initial ingestion scope**: whether DD-EUR-001 authorizes open-ended
   Europeana ingestion or is scoped to a specific pilot (e.g., Yellowstone prototype only).
   Recommended: scope to Yellowstone pilot for first ingestion run; broaden by subsequent DD.

7. Definition of the **quality floor**: minimum Europeana completeness score for ingested
   assets. Recommended: `completeness >= 4` (medium quality on Europeana's 0–10 scale).

8. Authorization of the **source config amendments** listed in Part II.

**What DD-EUR-001 does NOT need to address:**

- Migration or schema change — no new tables or columns required
- FM involvement in rights determination — permanently excluded per FM-4
- Media Substrate pipeline changes — existing pipeline handles EDM-schema assets

---

### DD-EUR-002 — Europeana Scope Expansion (Future)

**Status:** Not yet required. Reserved.

DD-EUR-001 is expected to authorize a scoped pilot (Yellowstone). When NC is ready to
expand Europeana ingestion to additional places or subject categories beyond the pilot scope,
DD-EUR-002 authorizes that expansion. DD-EUR-002 must reference DD-EUR-001 as its predecessor
and specify the new ingestion scope.

---

## Part II — Required Source Registry Updates

These are data-layer changes to the `sources` table. They require no migration — they are
`UPDATE` statements authorized by DD-EUR-001. They are governance-significant: the source
config is a constitutional document that governs worker behavior.

### Amendment EU-SR-1 — rights_strategy

**Field:** `sources.config` (JSONB — add key)

**Required addition:**
```json
"rights_strategy": "rights_matrix_filtered"
```

**Constitutional basis:** Every content acquisition source must declare its rights
strategy in config. The `rights_matrix_filtered` strategy instructs the Europeana
ingestion worker to apply Rights Matrix v1.0 pre-ingestion classification before
creating any `source_record`. A source without a declared rights strategy is constitutionally
incomplete for production ingestion.

LOC uses `"rights_strategy": "date_based_pre_1928"`. Europeana cannot use date-based
strategy because it surfaces assets from many jurisdictions and time periods; the Rights
Matrix provides the jurisdiction-aware classification that date alone cannot.

---

### Amendment EU-SR-2 — source_role

**Field:** `sources.config` (JSONB — add key)

**Required addition:**
```json
"source_role": "aggregator"
```

**Constitutional basis:** The Institution Coverage Audit v1 reclassified Europeana from
content institution to aggregator reference. This classification must be recorded in the
source config so that ingestion workers, provenance builders, and future auditors can
distinguish aggregator-sourced records from direct institution-sourced records. No existing
source uses this key; it is new.

---

### Amendment EU-SR-3 — completeness_minimum

**Field:** `sources.config` (JSONB — add key)

**Required addition:**
```json
"completeness_minimum": 4
```

**Constitutional basis:** Europeana's completeness score (0–10) is a quality signal for
the Asset Intelligence layer. A completeness floor prevents ingestion of asset stubs with
insufficient metadata for rights determination or commerce scoring. The floor of 4 admits
assets with adequate metadata while excluding the lowest-quality records. This value may be
raised by subsequent DD — it may not be lowered below 4 without a Director Decision.

---

### Amendment EU-SR-4 — rights_filter

**Field:** `sources.config` (JSONB — add key)

**Required addition:**
```json
"rights_filter": {
  "mode": "pre_ingestion",
  "authority": "europeana_rights_matrix_v1",
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
}
```

**Constitutional basis:** Rights Matrix v1.0 Rule RM-1 requires the pre-ingestion filter
to run before any `source_record` creation. The filter config embeds the Rights Matrix
classification directly in the source config so that the Europeana worker can implement it
without hardcoding rights URIs in worker logic. The `authority` field records which matrix
version governs. When this matrix is superseded, only the config key changes — worker
logic does not need updating.

The `filter_mode: strict` instructs the worker to treat any URI not in either list as
BLOCKED (not as REVIEW REQUIRED). This is consistent with Rights Matrix Part II Table 2H.

---

### Amendment EU-SR-5 — standards array

**Field:** `sources.standards` (TEXT[] — add element)

**Required addition:** Append `'edm'` to the standards array.

**From:** `['cidoc_crm', 'skos', 'prov_o', 'premis']`
**To:** `['cidoc_crm', 'skos', 'prov_o', 'premis', 'edm']`

**Constitutional basis:** Standards Constitution v1.0 classifies Europeana EDM as a
Mapped standard. The `sources.standards` array records which standards apply to assets
from this source. EDM is the governing schema for all Europeana `source_record` payloads.
Its absence from the array is a gap that must be closed before production ingestion begins.

---

### Amendment EU-SR-6 — entity_types

**Field:** `sources.entity_types` (TEXT[] — expand)

**From:** `['cultural_object']`
**To:** `['cultural_object', 'image', 'photography', 'map', 'illustration']`

**Constitutional basis:** The current `entity_types` value is too broad to guide
downstream routing workers. Europeana surfaces images, photographs, maps, and
illustrations — all Phase 1 media types under MSC v1.2. Specifying them explicitly
allows the media type routing worker to apply correct `media_type_id` values during
`source_item` creation.

---

### Amendment EU-SR-7 — edm_tripartite

**Field:** `sources.config` (JSONB — add key)

**Required addition:**
```json
"edm_tripartite": true
```

**Constitutional basis:** Records that this source uses the EDM tripartite aggregation
model (MSC v1.2 Article 29.2(a)). Workers reading this flag apply the three-layer mapping:
`ore:Aggregation` → `source_record`, `edm:ProvidedCHO` → `source_item`,
`edm:WebResource` → `media_file`. A Europeana ingestion worker that ignores `edm_tripartite`
and creates a flat `source_record` without the three-layer structure is a constitutional
violation.

---

## Part III — governance_state Transitions

### Current state

```
sources WHERE source_id = 'europeana':
  governance_state   = 'active'
  operational_status = 'healthy'
```

### Required transitions

**None.** Europeana's `governance_state = 'active'` is the correct terminal state
for an authorized production source. No state transition is required.

The vocabulary for `governance_state` is:
`proposed` → `approved` → `active` → [`suspended` | `deprecated` | `retired`]

Europeana entered `active` via Migration 17 backfill, not the standard `proposed →
approved → active` path. DD-EUR-001 formally documents the governance authority behind
the `active` designation, retroactively supplying the Director Decision that the backfill
did not include. After DD-EUR-001 is issued, Europeana's `active` status is formally
governed.

### Contrast with LOC

LOC entered at `governance_state = 'proposed'` because it was registered for the first
time in Migration 17 with an explicit note that ingestion was not yet permitted. DD-LOC-001
is required to advance it to `active`.

Europeana was already seeded before Migration 17 added the governance columns; the backfill
correctly set it to `active` because the API relationship existed. The governance gap is
not the state — it is the absence of formal authorization documentation and config completeness.

### Operational status transitions

`operational_status` is system-managed, not governance-managed. It will transition from
`'healthy'` to `'degraded'` or `'unavailable'` automatically based on API health checks.
No Director Decision governs operational status transitions.

---

## Part IV — Required Rights Review Workflow

The Rights Matrix establishes the framework. Before production ingestion begins, the
following workflow elements must be operational.

### RR-1 — Pre-Ingestion Filter (Required Before First Ingestion)

The Europeana ingestion worker must implement Rights Matrix Rule RM-1 before any
production `source_record` is created. This is a non-negotiable precondition. The
worker must:

1. Extract `edm:rights` from each EDM payload before creating any database record.
2. Classify the URI against the `rights_filter` config (EU-SR-4).
3. BLOCKED: log and discard — no records created.
4. REVIEW REQUIRED: create `source_record` + `media_rights` at `pending_verification`;
   open `workflow_item`.
5. ALLOWED: create `source_record` + `media_rights` at `pending_verification`; open
   confirmation checklist per Rights Matrix HR-4.

An ingestion run that skips step 1 is a constitutional violation regardless of the
asset's actual rights status.

### RR-2 — Human Reviewer Authorization

At least one human reviewer must be authorized for `item_type = 'rights_review'`
`workflow_item` records before production ingestion begins. The reviewer must:

- Understand the Rights Matrix v1.0 HR-2a, HR-2b, and HR-2c investigation requirements.
- Have authority to set terminal `media_rights.rights_status` values.
- Be capable of running independent PD analysis (publication date, author life dates,
  US copyright rules) for NKC cases.

The reviewer identity must be recorded in every `preservation_event` written for rights
determinations. An anonymous rights determination is a constitutional violation.

### RR-3 — 30-Day NKC Resolution Deadline

NKC `workflow_item` records must be resolved within 30 calendar days of creation.
An unresolved NKC item at day 31 must be closed as rejected (`rights_status = 'ineligible'`).
This prevents accumulation of stale pending items that block pipeline progress.

### RR-4 — FM Exclusion Confirmation

Before the first ingestion run, the implementation team must confirm in writing (as a
Director Decision attachment or operational note) that no FM system has access to the
rights determination workflow. FM output stored in `fm_candidate_record` under
`rights_analysis_advisory` is informational only and must not connect to the
`workflow_item` rights queue or the `media_rights` table. (Ref: Rights Matrix RM-5,
FM Constitution v1.0 Invariant FM-4.)

---

## Part V — Required Activation Target Workflow

Once rights are verified, the asset must pass through the NC activation pipeline
before it can enter commerce. The following steps are required.

### AT-1 — Media Substrate Pipeline Completion

Each Europeana-ingested asset must complete the full Media Substrate pipeline before
becoming `activation_eligible`. The canonical sequence per MSC v1.2:

```
source_record (ore:Aggregation — EDM schema)
  ↓
source_item (edm:ProvidedCHO — cultural object record)
  ↓
media_file (edm:WebResource — image/map file)
  ↓
media_technical_metadata (resolution, format, completeness score)
  ↓
media_rights (rights_statement_uri, rights_status = 'pending_verification')
  ↓ [human rights review]
media_rights.rights_status = 'verified_pd' | 'verified_cc0'
  ↓
preservation_event (rights_verification — outcome: success)
  ↓
source_item.status = 'activation_eligible'
```

An asset may not advance past `activation_eligible` until `media_rights.rights_status`
is a terminal verified value. An asset with `rights_status = 'pending_verification'`
is blocked from activation regardless of its completeness or quality scores.

### AT-2 — Commerce Opportunity Scoring

After `activation_eligible` is set, the Commerce Intelligence pipeline runs:

1. **Anchor type classification** — geographic assets (maps, photographs of places)
   use CI Constitution v1.2 `signal_substitutions` for geographic anchors.
2. **COS calculation** — using the anchor_weight_spec for the asset's anchor_type.
   - Maps sourced via Europeana with `anchor_type = 'geographic'` are eligible for
     CI v1.2 G-3 signal substitution (same as LOC Hayden Survey maps).
   - Photography with `anchor_type = 'geographic'` follows the same path.
3. **CSM tier assignment** — COS → tier (MASTERWORK / HERITAGE / DOCUMENT / FRAGMENT).
4. **Commerce opportunity record creation** — `asset_opportunities` row created.

### AT-3 — Human Activation Approval

NC's activation protocol requires second-human approval before any `activation_target`
record is created. For Europeana-sourced assets:

- The first human reviewed and confirmed rights (`verified_pd` or `verified_cc0`).
- The second human reviews the commerce opportunity record: COS score, CSM tier,
  anchor classification, and place association.
- Only after both humans have approved may the `activation_target` record be created
  and the asset made available for product creation.

This two-human gate applies to all Europeana assets without exception. The first
Europeana ingestion run should not attempt to automate either review step.

### AT-4 — Place Association Required

Every Europeana-sourced asset activated for commerce must be associated with at least
one `places` record. NC is a place-centered platform. An activated asset without a
place association is not discoverable through the primary NC navigation hierarchy.

For the Yellowstone pilot: all activated assets must be associated with
`places.geonames_id = 5843591` (Yellowstone National Park).

The place association is set in `activation_targets.place_id` and must be confirmed
during the second-human activation approval step.

---

## Part VI — Ordered Activation Checklist

The gates below are strictly ordered. Gate N may not begin before Gate N−1 is complete.
Parallelizable sub-steps within a gate are noted.

```
GATE 0 — PREREQUISITES (all complete as of 2026-06-07)
  [x] Europeana Rights Matrix v1.0 ratified
  [x] Europeana API key validated (creptionce — confirmed working)
  [x] MSC v1.2 ratified — Europeana Tier 1 governance rules
  [x] Standards Constitution v1.0 — EDM as Mapped standard
  [x] CI Constitution v1.2 — geographic signal substitution available
  [x] sources.governance_state = 'active' (Migration 17 backfill)
  [x] sources.operational_status = 'healthy'

GATE 1 — DIRECTOR DECISION (no implementation until complete)
  [ ] DD-EUR-001 issued — Europeana Production Activation
        Must contain: aggregator designation, Rights Matrix authority,
        EDM tripartite mapping, aggregator provenance rule,
        initial scope definition, quality floor, config amendment authorization

GATE 2 — SOURCE REGISTRY AMENDMENTS (data changes — no migration)
  [ ] EU-SR-1: rights_strategy = 'rights_matrix_filtered' added to config
  [ ] EU-SR-2: source_role = 'aggregator' added to config
  [ ] EU-SR-3: completeness_minimum = 4 added to config
  [ ] EU-SR-4: rights_filter object added to config
  [ ] EU-SR-5: 'edm' added to standards array
  [ ] EU-SR-6: entity_types expanded to include image, photography, map, illustration
  [ ] EU-SR-7: edm_tripartite = true added to config
  Note: EU-SR-1 through EU-SR-7 may be applied in a single UPDATE. No migration required.

GATE 3 — RIGHTS REVIEW WORKFLOW AUTHORIZATION
  [ ] RR-1: Europeana ingestion worker updated to implement pre-ingestion rights filter
  [ ] RR-2: At least one human reviewer authorized for rights_review workflow items
  [ ] RR-3: 30-day NKC resolution deadline operationalized
  [ ] RR-4: FM exclusion confirmed in writing — no FM access to rights workflow

GATE 4 — PILOT INGESTION RUN (scope per DD-EUR-001)
  [ ] Ingestion query defined:
        query=<pilot scope>, rights filter applied, completeness >= 4
  [ ] Pre-ingestion rights filter runs — BLOCKED assets discarded
  [ ] ALLOWED assets: source_record + source_item + media_file + media_rights created
  [ ] REVIEW REQUIRED assets: workflow_items opened
  [ ] Preservation events written for all rights outcomes

GATE 5 — RIGHTS REVIEW (all ALLOWED assets from pilot)
  [ ] Human reviewer confirms rights evidence for each ALLOWED asset (per HR-4)
  [ ] media_rights.rights_status set to 'verified_pd' or 'verified_cc0'
  [ ] Preservation event written: rights_verification, outcome: success
  [ ] source_item.status = 'activation_eligible' set for verified assets
  [ ] REVIEW REQUIRED workflow items investigated per HR-2a / HR-2b / HR-2c

GATE 6 — COMMERCE SCORING
  [ ] Anchor type classification run on activation-eligible assets
  [ ] COS calculated (CI v1.2 — geographic signal substitution applied where applicable)
  [ ] CSM tier assigned
  [ ] asset_opportunities records created

GATE 7 — ACTIVATION APPROVAL
  [ ] Second human reviews each commerce opportunity (COS, tier, place association)
  [ ] Place association confirmed (Yellowstone: geonames_id = 5843591)
  [ ] activation_target records created for approved assets
  [ ] Products available for commerce

GATE 8 — PILOT REVIEW
  [ ] Pilot ingestion results reviewed against Gates 4–7 metrics
  [ ] Rights review queue cleared or triaged
  [ ] DD-EUR-002 scope expansion decision initiated if pilot successful
```

---

## Part VII — Invariants

**AC-I-1 — DD-EUR-001 is Gate 1.** No source registry update, ingestion run, or worker
modification may precede DD-EUR-001. The Director Decision is not a formality — it is the
constitutional authorization event that separates the blanket backfill from formal
production activation.

**AC-I-2 — Rights Matrix is Non-Optional.** The pre-ingestion rights filter (Gate 3, RR-1)
must be in place before the first production ingestion run begins. An ingestion run without
the rights filter is a constitutional violation regardless of how it is scoped.

**AC-I-3 — Two-Human Gate.** The two-human activation approval (Gate 7, AT-3) applies to
every Europeana asset without exception. No automation may substitute for either review.

**AC-I-4 — FM Exclusion (Permanent).** FM output does not participate in any step of
this checklist. Gates 5, 6, and 7 are human-governed. (Ref: FM Constitution v1.0, FM-4.)

**AC-I-5 — No Scope Creep Beyond DD-EUR-001.** The pilot ingestion run may not exceed
the scope authorized by DD-EUR-001. If the ingestion worker encounters assets outside
the authorized scope, it must stop and queue them for DD-EUR-002 authorization.

---

## Part VIII — Open Questions

**OQ-1 — Pilot Scope.** DD-EUR-001 must define the initial ingestion scope. Recommended:
Yellowstone prototype pilot only (`query = yellowstone`), producing the ~757 PD-eligible
assets identified in API validation. Broader scope requires DD-EUR-002.

**OQ-2 — Aggregator Provenance vs. Direct Rijksmuseum Source.** Rijksmuseum assets
ingested via Europeana carry `source_id = 'europeana'`. When NC later onboards Rijksmuseum
as a direct source (per Institution Coverage Audit Wave 3), those assets could be
re-ingested with `source_id = 'rijksmuseum'` at higher metadata quality. The deduplication
rule (match on `source_item.provider_item_id`?) must be defined before Rijksmuseum is
onboarded to prevent duplicate `source_item` records.

**OQ-3 — Completeness Floor Calibration.** The recommended floor of `completeness >= 4`
is based on Europeana's documentation (4 = medium quality). The API validation run showed
top Yellowstone PD results at completeness 6–7 (Rijksmuseum). If the floor is set too low,
NC ingests assets with insufficient metadata for rights determination. If set too high, NC
misses legitimate PD assets with sparse metadata. Calibrate after first pilot ingestion.

**OQ-4 — REVIEW REQUIRED Volume.** NoC-CR and NoC-OKLR assets open human review queues.
If the pilot produces significant REVIEW REQUIRED volume, the 30-day NKC deadline may
need review. Define queue capacity before the pilot ingestion run begins.

---

*Europeana Activation Checklist v1.0.0 — ratified 2026-06-07*
*Authority: Strategic Directive · MSC v1.2 · Standards Constitution v1.0 · CI v1.2 · Europeana Rights Matrix v1.0*
*Next version trigger: DD-EUR-001 issued; post-pilot review*
