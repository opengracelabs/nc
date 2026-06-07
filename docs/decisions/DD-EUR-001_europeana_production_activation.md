# DD-EUR-001 — Europeana Production Activation

| Field | Value |
|---|---|
| **Decision ID** | DD-EUR-001 |
| **Type** | Source Activation |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-07 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Migration 17 blanket backfill (informal) |
| **Governing Documents** | Europeana Activation Checklist v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · CI Constitution v1.2 |

---

## Background

Europeana has been registered in the NC `sources` table since the initial seed
(`03_seed.sql`) and was set to `governance_state = 'active'` by Migration 17's blanket
backfill on 2026-06-07. That backfill treated Europeana identically to infrastructure
sources (GeoNames, OSM, Wikidata). It was technically correct — the API relationship
existed and the key was valid — but it did not constitute a formal production authorization.

Before this Decision, no formal governance document:
- Authorized the Europeana ingestion pipeline to create `source_record`, `media_file`,
  or `media_rights` rows from Europeana API data
- Declared Europeana's role as an aggregator-source (distinct from direct institution sources)
- Designated a governing rights document for Europeana-sourced assets
- Defined the scope, quality floor, or success criteria for production ingestion

This Decision supplies all of the above. It does not change `governance_state` (which
is already `'active'`) — it retroactively provides the Director authority that the
backfill could not.

Additionally, on 2026-06-07 the following prerequisites were completed:

| Prerequisite | Status |
|---|---|
| Europeana API key validated (`creptionce`) | Complete |
| Europeana Rights Matrix v1.0 ratified | Complete |
| MSC v1.2 ratified — Europeana as Tier 1 Reference Institution | Complete |
| Standards Constitution v1.0 — EDM as Mapped standard | Complete |
| CI Constitution v1.2 — geographic signal substitution available | Complete |
| Europeana Activation Checklist v1.0 ratified | Complete |
| `sources.governance_state = 'active'` | Complete (Migration 17) |

All prerequisites are satisfied. No implementation gate blocks this Decision.

---

## Findings

The Director finds:

**F-1.** Europeana is a Tier 1 Reference Institution under MSC v1.2 Article 28.3 for
two governance domains: the EDM tripartite aggregation model and the Rights Statements
Working Group vocabulary. These adoptions are constitutional and do not require further
Director authorization.

**F-2.** Europeana functions as an aggregator, not a holding institution. It routes assets
from thousands of contributing institutions under a unified API and rights vocabulary.
NC's institutional taxonomy must reflect this: Europeana is an aggregator-source, not
a content institution, for NC's internal source classification.

**F-3.** The Europeana Rights Matrix v1.0, ratified 2026-06-07, provides a complete and
enforceable rights classification for every rights statement used in the Europeana ecosystem.
The Matrix is the precondition for production ingestion. It is operative.

**F-4.** The NC `sources` table record for Europeana (`source_id = 'europeana'`) is
incomplete as a content acquisition source. It lacks `rights_strategy`, `source_role`,
`completeness_minimum`, `rights_filter`, `edm_tripartite`, and `'edm'` in its standards
array. These gaps would permit an ingestion worker to operate without rights governance.
They must be closed before the first production ingestion run.

**F-5.** The Yellowstone Prototype Specification v1.0 (ratified 2026-06-07) requires
Europeana-sourced assets (photography, maps) to populate the Yellowstone pilot experience.
Europeana is the only currently-validated source with sufficient PD-eligible Yellowstone
material. The API validation run returned 757 PD-eligible results for the Yellowstone
query — sufficient for a meaningful pilot.

**F-6.** No FM system may participate in any rights determination at any stage. This is
not a policy preference — it is a permanent constitutional invariant (FM-4) that predates
this Decision and cannot be modified by this Decision or any subsequent DD.

---

## Decision

### Article 1 — Production Authorization

Europeana is formally authorized as an active NC production source for content acquisition.
This authorization supersedes the Migration 17 blanket backfill as the authoritative
activation event for Europeana.

The `sources.governance_state = 'active'` designation is hereby formally governed by this
Decision. The Director confirms this designation is correct and appropriate.

---

### Article 2 — Aggregator Designation

Europeana is designated as an **aggregator-source** in NC's source taxonomy. This
designation means:

**(a)** Europeana routes content from contributing institutions. It is not itself a
holding institution. NC's classification as an aggregator reflects Europeana's role
in the content supply chain, not a diminishment of its status as a Tier 1 Reference
Institution for governance standards.

**(b)** For every asset ingested via the Europeana API, `source_record.source = 'europeana'`.
The contributing institution identified in `edm:dataProvider` is credited in the provenance
record but does not require a separate NC `sources` record. This is the
**aggregator provenance rule** and it governs until NC establishes a direct API
relationship with the contributing institution.

**(c)** When NC later onboards a contributing institution as a direct source (e.g.,
Rijksmuseum per Institution Coverage Audit Wave 3), assets previously ingested via
Europeana may be re-evaluated for re-ingestion under the direct source relationship.
Deduplication will be handled by `source_item.provider_item_id` matching. This Decision
does not define the deduplication rule — it acknowledges the future scenario and defers
its governance to the relevant institution's onboarding DD.

---

### Article 3 — Rights Authority

The **Europeana Rights Matrix v1.0** is the governing document for all rights
determinations on assets ingested via the Europeana API.

**(a)** The Rights Matrix pre-ingestion filter (Rule RM-1) is **mandatory** and must
execute before any `source_record` creation. An ingestion run that creates `source_record`
rows without first classifying `edm:rights` against the Rights Matrix is a constitutional
violation.

**(b)** The three ALLOWED statements that yield terminal `verified_pd` or `verified_cc0`
status after human review are: CC0 1.0, Public Domain Mark 1.0 (PDM), NoC-US 1.0.
No other rights statement may yield a terminal verified status without a new version
of the Rights Matrix issued after a doctrine amendment.

**(c)** The FM exclusion (Rights Matrix Rule RM-5, FM Constitution v1.0 Invariant FM-4)
applies permanently. This Decision does not modify it. No FM output may influence any
`media_rights` record for any Europeana-sourced asset, ever.

---

### Article 4 — EDM Tripartite Mapping

The EDM tripartite aggregation model is adopted as the canonical mapping for all
Europeana `source_record` payloads, per MSC v1.2 Article 29.2(a):

```
ore:Aggregation   →   source_record
edm:ProvidedCHO   →   source_item
edm:WebResource   →   media_file
```

Every Europeana ingestion worker must implement this mapping. A flat `source_record`
that does not decompose the EDM tripartite structure into the three NC layers is a
constitutional violation. The `edm_tripartite` flag in source config (EU-SR-7) records
this requirement for worker introspection.

---

### Article 5 — Source Registry Amendments

The following amendments to the `sources` table record for `source_id = 'europeana'`
are authorized and **must be applied before the first production ingestion run:**

| Amendment | Change | Field |
|---|---|---|
| EU-SR-1 | Add `rights_strategy: 'rights_matrix_filtered'` | `sources.config` |
| EU-SR-2 | Add `source_role: 'aggregator'` | `sources.config` |
| EU-SR-3 | Add `completeness_minimum: 4` | `sources.config` |
| EU-SR-4 | Add `rights_filter` object with ALLOWED and REVIEW REQUIRED URI lists | `sources.config` |
| EU-SR-5 | Add `'edm'` to standards array | `sources.standards` |
| EU-SR-6 | Expand entity_types to include `image`, `photography`, `map`, `illustration` | `sources.entity_types` |
| EU-SR-7 | Add `edm_tripartite: true` | `sources.config` |

These are data changes only. No new migration is required. All seven amendments
must be applied in a single authorized `UPDATE` statement, not piecemeal.

The `sources.config` post-amendment target state:

```json
{
  "api_endpoint": "https://api.europeana.eu/record/v2",
  "auth_key_env": "EUROPEANA_API_KEY",
  "rate_limit": {
    "requests_per_second": 2,
    "burst": 10
  },
  "rights_strategy": "rights_matrix_filtered",
  "source_role": "aggregator",
  "completeness_minimum": 4,
  "edm_tripartite": true,
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
}
```

---

### Article 6 — Pilot Scope

This Decision authorizes a **scoped pilot** only. Production ingestion under this Decision
is limited to the following parameters:

**(a) Query scope.** The pilot ingestion query is:
```
query=yellowstone
rights=http://creativecommons.org/publicdomain/zero/1.0/
       OR http://creativecommons.org/publicdomain/mark/1.0/
       OR http://rightsstatements.org/vocab/NoC-US/1.0/
       OR http://rightsstatements.org/vocab/NoC-CR/1.0/
       OR http://rightsstatements.org/vocab/NoC-OKLR/1.0/
       OR http://rightsstatements.org/vocab/NKC/1.0/
completeness_minimum=4
api=Europeana Record API v2
```

The server-side rights filter includes all three ALLOWED statements (CC0, PDM, NoC-US)
and all three REVIEW REQUIRED statements (NoC-CR, NoC-OKLR, NKC). BLOCKED statements
are excluded by omission. The pre-ingestion worker then classifies each returned asset
against the Rights Matrix: ALLOWED assets proceed to pipeline creation; REVIEW REQUIRED
assets receive a `workflow_item`; no BLOCKED asset may reach `source_record` creation.

Only assets matching this query scope may be ingested under DD-EUR-001. Assets from
queries outside this scope — different place, different subject, broader rights filter —
require DD-EUR-002.

**(b) Pilot batch size.** The first ingestion batch is capped at **100 assets**. This
ceiling provides sufficient volume to validate the full pipeline (ingestion → rights review →
scoring → activation) while keeping human review workload manageable for pilot assessment.
The cap may be raised only by DD-EUR-002.

**(c) Place association required.** All assets ingested under this Decision must be
associated with Yellowstone National Park (`places.geonames_id = 5843591`,
Wikidata Q351). Assets that cannot be associated with Yellowstone — because they are
unrelated to Yellowstone despite appearing in the query results — must be discarded at
ingestion, not queued for a different place. Place expansion requires DD-EUR-002.

**(d) REVIEW REQUIRED assets.** Assets classified REVIEW REQUIRED (NoC-CR, NoC-OKLR,
NKC) may be ingested into the pipeline with `rights_status = 'pending_verification'`
and `workflow_item` opened. They may not advance to `activation_eligible` until human
review completes. REVIEW REQUIRED assets count against the 100-asset pilot cap only if
they were successfully ingested (i.e., passed the pre-ingestion gate and received a
`source_record`).

**(e) BLOCKED assets.** BLOCKED assets must be rejected at the pre-ingestion filter.
They do not count against the pilot cap. Every rejection must be logged.

---

### Article 7 — Pilot Success Criteria

The pilot is evaluated at the conclusion of the 90-day pilot window or when the first
100 assets have been processed — whichever comes first. Success on all criteria
triggers the DD-EUR-002 decision process for scope expansion.

| # | Criterion | Threshold | Metric |
|---|---|---|---|
| SC-1 | Activated assets | ≥ 10 assets reach `activation_target` status with second-human approval | `COUNT(activation_targets) WHERE source = 'europeana'` |
| SC-2 | Rights verification completeness | 100% of `activation_eligible` assets have documented rights evidence in `media_rights.rights_evidence` | No `verified_pd` / `verified_cc0` record missing required evidence fields |
| SC-3 | BLOCKED filter accuracy | 100% of BLOCKED-classified assets rejected at pre-ingestion gate | Zero BLOCKED-statement assets in `source_record` table |
| SC-4 | Place association | 100% of activated assets associated with Yellowstone (`geonames_id = 5843591`) | No `activation_target` missing `place_id` for Europeana-sourced assets |
| SC-5 | FM exclusion | Zero FM output connected to any rights determination | No `fm_candidate_record` referenced in any `media_rights` or `workflow_item` for Europeana assets |
| SC-6 | Commerce coverage | 100% of activated assets have COS calculated and CSM tier assigned | No `activation_target` without corresponding `asset_opportunities` record |
| SC-7 | Constitutional integrity | Zero constitutional violations logged in preservation events | No `preservation_event.event_outcome = 'violation'` for Europeana-sourced assets |
| SC-8 | Pipeline completion rate | ≥ 80% of ingested assets complete gates 4–7 without worker error | Ingestion error rate ≤ 20% |

**Pilot failure definition:** If SC-3 or SC-5 fail (BLOCKED asset entered pipeline, or FM
touched rights), the pilot is **immediately suspended** pending investigation. These are
not performance failures — they are constitutional violations. The other six criteria
are performance criteria; failure below threshold triggers remediation without suspension.

---

### Article 8 — Explicit Exclusions

This Decision does not authorize:

**(a)** Ingestion of assets with any rights statement other than CC0, PDM, NoC-US,
NoC-CR, NoC-OKLR, or NKC — even with human approval. BLOCKED statements remain
BLOCKED. (Ref: Rights Matrix Invariant RM-I-1.)

**(b)** Ingestion of assets from Europeana queries outside the Yellowstone scope defined
in Article 6(a). Any non-Yellowstone asset returned by the query — even if PD-eligible —
must be discarded.

**(c)** Source registry changes beyond the seven amendments in Article 5. Any additional
config changes to the `europeana` source record require a separate Director Decision.

**(d)** Onboarding contributing institutions (Rijksmuseum, etc.) as separate NC sources.
Those institutions require their own institution onboarding DDs per Institution Coverage
Audit v1 wave sequencing.

**(e)** Increasing the completeness floor below 4. The floor may be raised by configuration
update without a new DD; it may not be lowered below 4 without a new DD.

**(f)** Use of Europeana's SPARQL endpoint, Entity API, or any API surface other than
the Record API v2 (`https://api.europeana.eu/record/v2`).

**(g)** Ingestion of book, audio, film, 3D, or dataset media types via Europeana. Phase 1
media types only: image, map, photography, illustration.

**(h)** Retroactive rights clearance for assets ingested before this Decision was issued.
No `source_record` rows exist from Europeana pre-this-Decision; this exclusion is a
prospective safeguard.

---

### Article 9 — Required Actions Before First Ingestion Run

The following must be complete before the first production ingestion run begins.
The Principal Architect is responsible for confirming completion of each item.

| # | Action | Gate |
|---|---|---|
| 9.1 | DD-EUR-001 ratified (Director signature + second-human approval) | Gate 1 |
| 9.2 | Source registry amendments EU-SR-1 through EU-SR-7 applied in a single UPDATE | Gate 2 |
| 9.3 | Europeana ingestion worker updated to implement pre-ingestion rights filter (RM-1) | Gate 3 |
| 9.4 | At least one human reviewer authorized for `item_type = 'rights_review'` workflow items | Gate 3 |
| 9.5 | FM exclusion confirmed in writing — no FM system has access to rights workflow | Gate 3 |
| 9.6 | 30-day NKC resolution deadline operationalized in workflow system | Gate 3 |

No partial completion is acceptable. If any item in 9.1–9.6 is incomplete, the ingestion
run must not begin.

---

### Article 10 — Subsequent Decisions

The following Director Decisions are anticipated as consequences of this Decision:

| ID | Trigger | Scope |
|---|---|---|
| **DD-EUR-002** | Pilot success (all SC-1 through SC-8 met) | Europeana scope expansion beyond Yellowstone; pilot cap removal |
| **DD-LOC-001** | Separate track | LOC `governance_state` → `'active'` for map ingestion |
| **DD-RIJKSMUSEUM-001** | Institution Coverage Audit Wave 3 | Rijksmuseum direct API relationship |

DD-EUR-002 is not automatically triggered by pilot success. It requires a Director review
of the pilot results, a Principal Architect recommendation, and a new Decision document.

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

*DD-EUR-001 Draft — 2026-06-07*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
