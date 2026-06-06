# Asset Intelligence Constitution v1.1

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Ratified — implementation authorized for Migrations M-32 through M-35 |
| Supersedes | `asset_intelligence_constitution_v1.md` (v1.0.0) |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-06 |
| Ratified | 2026-06-06 |
| Role | Principal Architect |

---

## Director Review — v1.0.0 → v1.1.0

Seven blocking findings applied. No articles deleted. Affected articles annotated `[Amended v1.1]`.

| Finding | Description | Resolution | Articles Affected |
|---|---|---|---|
| BF-1 | Article 9.4 restricts Principal Architect review to `natural_history` domain for Tier 1; PA-8 requires PA review for all domains — direct contradiction | Amended: 9.4 now applies to all creator_domains for Tier 1; natural_history context retained as rationale note only | 9 |
| BF-2 | No PostgreSQL RULE preventing hard DELETE on `creator_prestige_registry`, `place_iconic_taxa_registry`, or `creator_authority_registry`; CI Constitution PA-9 equivalent absent | Added no-DELETE RULE requirement to all three registry tables in M-33 and M-34; added PA-17 | 7, 11, 15, 26, 27 |
| BF-3 | `anchor_weight_spec.mixed` uses `blend_strategy` as an opaque string; no policy-activation invariant requires it to match a registered algorithm; workers cannot fail-fast at policy load | Renamed to `blend_algorithm_version`; activation invariant added: must match a registered algorithm in the scoring worker | 25, 28 |
| BF-4 | `cross_anchor_discount_rate` declared as a governed policy parameter (Article 14.3) but absent from the canonical `anchor_weight_spec` structure; workers forced to hardcode, violating PA-16 | Added `cross_anchor_discount_rate` as a top-level field in `anchor_weight_spec`; Article 14.3 references it by field name | 14, 25, 27 |
| BF-5 | `alternate_names TEXT[]` on `creator_authority_registry` has no immutability rule after `active`; post-activation modifications are unapproved changes to governed data; historical alternate-name resolutions become suspect | Declared `alternate_names` immutable after `active`; additions or removals require a new versioned record; BEFORE UPDATE trigger added to M-33 DDL | 15, 16, 17, 27 |
| BF-6 | Article 28 prerequisite 6 implies replay worker re-queries the registry by row ID; CI Constitution replay protocol uses stored signal values from `score_inputs`, not live re-queries; re-query is fragile against row retirement and version changes | Amended Article 10.1 and Article 28 prerequisite 6: `illustrator_prestige` is a stored numeric value in `score_inputs`; registry row ID is audit metadata only; replay verifies formula arithmetic from stored values | 10, 28 |
| BF-7 | `anchor_type = 'mixed'` has no pre-scoring hard block; workers can proceed with unconfirmed provisional blend weights; `curator_review_reason = 'manual_flag'` is a review flag, not a scoring stop | Amended Article 6: unconfirmed mixed anchor sets `hard_gate_status = 'not_evaluated'` with `reason = 'mixed_anchor_blend_unconfirmed'`; uses existing CI Constitution gate infrastructure; no schema change | 6, 22 |

---

## Preamble

This Constitution establishes the governance model for four asset intelligence registries in Nature &
Culture. It resolves Open Question Q2 from the Commerce Intelligence Constitution v1.1
(`anchor_type` on `illustration_opportunities`), formalizes the creator prestige and authority
models identified as gaps in the 2026-06-06 Asset-Class Capability Audit, and extends
place-iconic taxa governance to support multi-anchor asset classes.

This Constitution answers five questions:

1. How should biological, geographic, cultural, and mixed assets be governed?
2. How should creator prestige be versioned and approved?
3. How should place-iconic relationships be governed?
4. How should creator authorities be modeled?
5. Which registries require second-human approval?

This Constitution is subordinate to the Strategic Directive, the Illustration Opportunity
Doctrine, and the Commerce Intelligence Constitution v1.1. Any provision that conflicts with those
documents is void. This Constitution governs four registries:

| Registry | Purpose |
|---|---|
| `anchor_type` on `illustration_opportunities` | Classifies the primary value anchor of an asset |
| `creator_prestige_registry` | Governs creator prestige scores and their lifecycle |
| `place_iconic_taxa_registry` | Governs place-taxon iconic relationships |
| `creator_authority_registry` | Models authoritative creator identity with external authority links |

These registries are scoring support infrastructure. They do not create opportunities. They do not
approve rights. They supply governed reference values that scoring workers use to compute Class B
signals. Their governance failure degrades scoring fidelity; it does not break the pipeline.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain illustration commerce platform. It is
not a biodiversity inventory.

**1.2** The commercial object is an Illustration Opportunity. An Illustration Opportunity may be
anchored in biology, geography, culture, or a mixture of these. The anchor type determines which
scoring dimensions are most informative for that asset.

**1.3** Every registry governed by this Constitution is subject to the second-human rule: a human
may not approve their own submission. This rule is enforced at the database level for all
registries.

**1.4** Workers resolve prestige and iconicity from registries. Workers do not write to registries.
Workers do not approve registry entries. These are hard boundaries enforced by schema and
convention.

### Article 2 — Scope

This Constitution governs exactly four entities:

| Entity | Role |
|---|---|
| `anchor_type` field on `illustration_opportunities` | Classifies the primary value anchor of each opportunity |
| `creator_prestige_registry` | Governed table: creator → prestige tier and domain |
| `place_iconic_taxa_registry` | Governed table: place × taxon → iconicity strength and anchor context |
| `creator_authority_registry` | Governed table: canonical creator identity with authority file links |

### Article 3 — Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Commerce Intelligence Constitution v1.1
            └─ Asset Intelligence Constitution v1.1  ← this document
                 └─ creator_prestige_registry (active entries)
                 └─ place_iconic_taxa_registry (active entries)
                 └─ creator_authority_registry (active entries)
                      └─ Scoring workers (Class B signal resolution)
```

No lower authority may override a higher authority. A registry entry that contradicts the Commerce
Intelligence Constitution or higher documents is void.

---

## Part II — Anchor Type Governance

### Article 4 — Resolution of Open Question Q2

**4.1** This article resolves Open Question Q2 from Commerce Intelligence Constitution v1.1
(Article 37). The `anchor_type` field is added to `illustration_opportunities` as a first-class
governed field — not derived, not advisory.

**4.2** The `anchor_type` vocabulary:

| Value | Definition |
|---|---|
| `biological` | Primary commercial value derives from a biological subject: taxon, organism, natural history specimen. The golden-age illustration canon. |
| `geographic` | Primary commercial value derives from a place or landscape: cartographic record, survey illustration, topographic view, expedition document. |
| `cultural` | Primary commercial value derives from a cultural or human-made subject: architectural record, poster, ethnographic document, decorative art. |
| `mixed` | Asset holds significant commercial value from two or more anchors simultaneously. An Audubon plate in Yellowstone: biological (the bird) and geographic (the place). Requires explicit `anchor_blend` record and curator confirmation before scoring proceeds. |

**4.3** `anchor_type` is not a direct scoring input. It is an anchor-class classifier that selects
which subscore weight set is applied to the composite formula. The `commerce_policy.formula_spec`
must include an `anchor_weight_spec` block (Article 25) governing this selection.

**4.4** `anchor_type` defaults to `biological` for all BHL-sourced opportunities where no explicit
value has been set. It defaults to `geographic` for LOC-sourced opportunities where the catalog
record contains cartographic subject terms. It defaults to `cultural` for LOC-sourced
opportunities classified as photographic or poster material. Workers derive a provisional value at
ingestion time. Curators may override.

### Article 5 — anchor_type Assignment Protocol

**5.1 Worker-derived assignment**. Derivation rules by source:

| Source | Derivation Rule |
|---|---|
| BHL | Default `biological`. Propose `mixed` if `place_relevance_score > 0.70` at scoring time and the linked place has active iconic taxa entries. |
| LOC — cartographic subject terms | Default `geographic`. Propose `mixed` if biological taxa are named in the item record. |
| LOC — photograph | Default `cultural`. Propose `geographic` if the item record identifies a natural landscape or protected area. |
| LOC — poster | Default `cultural`. |

Workers write provisional values only. All provisional values are eligible for curator override
before scoring proceeds.

**5.2 Curator override**. A curator may override a worker-derived `anchor_type`. Override requires:

1. Score audit log entry: `event_type = 'signal_updated'`, `actor_type = 'curator'`, `actor_id` present.
2. `actor_notes` documenting the rationale.
3. `signal_correction` recompute enqueued.

**5.3 Immutability after publication**. Once a `catalog_candidate` linked to an opportunity
reaches `status = 'published'`, `anchor_type` on the linked `illustration_opportunities` record
may not be changed without a curator governance event and full recompute of all downstream scoring
records. A `replay_failure` is expected and constitutionally required after any post-publication
`anchor_type` change.

### Article 6 — Mixed-Anchor Governance `[Amended v1.1]`

**6.1** The `mixed` anchor type requires an `anchor_blend` record on `illustration_opportunities`
specifying which two anchor types contribute and at what relative weight.

`anchor_blend` is stored as JSONB on `illustration_opportunities`:

```json
{
  "primary":           "<anchor_type>",
  "secondary":         "<anchor_type>",
  "primary_weight":    <float [0.5, 1.0]>,
  "secondary_weight":  <float [0.0, 0.5]>
}
```

Constraints:

- `primary_weight + secondary_weight = 1.0` (±0.001)
- `primary_weight >= 0.5` (primary anchor is always dominant)
- `primary != secondary`
- `anchor_type = 'mixed' → anchor_blend IS NOT NULL`
- `anchor_type != 'mixed' → anchor_blend IS NULL`

**6.2** Curator approval is required for every `anchor_type = 'mixed'` assignment before scoring
proceeds. Workers may propose `mixed` provisionally and must set `curator_review_reason =
'manual_flag'` on `commerce_opportunities`. The blend weights require human review before scoring
proceeds. The default blend when a curator confirms `mixed` without specifying weights is
`primary_weight = 0.60, secondary_weight = 0.40`.

**6.3** A worker may not self-confirm an `anchor_type = 'mixed'` assignment. Proposal is permitted;
confirmation requires a curator governance event: `event_type = 'signal_updated'`,
`actor_type = 'curator'`, with `actor_notes` documenting the confirmed blend values.

**6.4 Mixed-anchor confirmation gate** `[New — v1.1]`: When the scoring worker evaluates an
opportunity with `anchor_type = 'mixed'`, it must verify that a curator governance event
confirming the `anchor_blend` exists in `score_audit_log` for that opportunity
(`event_type = 'signal_updated'`, `actor_type = 'curator'`). If no such event exists, the scoring
worker must set `hard_gate_status = 'not_evaluated'` with
`reason = 'mixed_anchor_blend_unconfirmed'` and halt. This uses the existing
`hard_gate_status = 'not_evaluated'` mechanism established in CI Constitution Article 7 for
ungoverned vocabulary. Scoring of a mixed-anchor opportunity without curator confirmation of the
blend is unconstitutional.

---

## Part III — Creator Prestige Registry

### Article 7 — Registry Definition `[Amended v1.1]`

**7.1** The `creator_prestige_registry` supersedes `priority_illustrators_vocabulary` as the
governed source for `illustrator_prestige` computation. The eight priority illustrators in Commerce
Intelligence Constitution Article 7 — Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel,
Wolf — are re-seeded in this registry as `prestige_tier = 'tier_1'` with `creator_domain =
'natural_history'`.

**7.2** The registry extends prestige governance to additional creator domains:

| Domain | Definition |
|---|---|
| `natural_history` | Illustrators whose primary body of work depicts biological subjects in the golden-age tradition (1750–1900). |
| `cartography` | Cartographers and survey illustrators whose maps or geographic illustrations are recognized primary historical records. |
| `fine_art` | Fine art illustrators and printmakers with documented museum acquisition and commercial auction presence. |
| `photography` | Photographers represented in major institutional collections with recognized historical significance. |
| `printmaking` | Printmakers working in relief, intaglio, or planographic traditions with established commercial presence. |
| `other` | Creators whose domain does not fit existing categories. Requires Principal Architect review at every proposal. |

**7.3** `creator_prestige_registry` schema:

```
creator_prestige_registry
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  creator_name          TEXT NOT NULL
  creator_authority_id  UUID REFERENCES creator_authority_registry(id)
  creator_domain        TEXT NOT NULL
  prestige_tier         TEXT NOT NULL
  prestige_score        NUMERIC(4,3) NOT NULL
  tier_rationale        TEXT NOT NULL
  active_years          TEXT
  primary_works         TEXT
  status                TEXT NOT NULL DEFAULT 'proposed'
  authored_by           TEXT NOT NULL
  approved_by           TEXT
  approved_at           TIMESTAMPTZ
  version               INT NOT NULL DEFAULT 1
  previous_version_id   UUID REFERENCES creator_prestige_registry(id)
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  retired_at            TIMESTAMPTZ

  CONSTRAINT chk_cpr_domain       CHECK (creator_domain IN (
                                     'natural_history','cartography','fine_art',
                                     'photography','printmaking','other'))
  CONSTRAINT chk_cpr_tier         CHECK (prestige_tier IN ('tier_1','tier_2','tier_3'))
  CONSTRAINT chk_cpr_score        CHECK (prestige_score BETWEEN 0.0 AND 1.0)
  CONSTRAINT chk_cpr_status       CHECK (status IN ('proposed','active','retired'))
  CONSTRAINT chk_cpr_second_human CHECK (
    status != 'active' OR approved_by IS DISTINCT FROM authored_by
  )
  CONSTRAINT chk_cpr_score_tier   CHECK (
    (prestige_tier = 'tier_1' AND prestige_score = 1.000) OR
    (prestige_tier = 'tier_2' AND prestige_score = 0.750) OR
    (prestige_tier = 'tier_3' AND prestige_score = 0.500)
  )

PostgreSQL RULE: no DELETE permitted on creator_prestige_registry.  [BF-2 — v1.1]
  -- status = 'retired' is the terminal state. Hard deletion is unconstitutional.
  -- Enforced by: CREATE RULE no_delete_creator_prestige AS ON DELETE TO creator_prestige_registry DO INSTEAD NOTHING;
  -- (or: DO INSTEAD RAISE EXCEPTION 'creator_prestige_registry rows may not be deleted')
```

### Article 8 — Prestige Tier Definitions

| Tier | Score | Criteria |
|---|---|---|
| `tier_1` | 1.000 | Monographic work recognized as a primary historical and commercial reference. Institutional collection presence at five or more major museums or archives. Commercially established at auction or print-on-demand at premium price points. Tier 1 is not awarded on historical fame alone — commercial viability is a required criterion. |
| `tier_2` | 0.750 | Documented institutional collection presence at two or more major institutions. Commercially active in the secondary market. Recognized in the scholarly literature of their domain. |
| `tier_3` | 0.500 | Single institutional collection presence or documented publication history. Recognized in domain-specific reference works. Commercially present at standard price points. |

**8.1** The `creator_domain = 'other'` requires Principal Architect review at every proposal,
regardless of tier. No worker may auto-derive a prestige score for a creator in the `other` domain.
All `other` domain entries require curator-initiated proposals.

### Article 9 — Prestige Registry Lifecycle `[Amended v1.1]`

**9.1** Lifecycle states:

```
proposed
  ↓ authored by one human, with rationale in tier_rationale
  ↓ approved by a second human (not the author)
active
  ↓ update proposed: new record with previous_version_id → old record
  ↓ new record approved (second human) → new record active, old record retired (same transaction)
retired  (terminal — no hard DELETE permitted; see Article 7.3)
```

**9.2** An active entry may be updated only by creating a new record with `previous_version_id`
pointing to the active entry. On approval, the new record becomes `active` and the previous record
becomes `retired` in the same transaction.

**9.3** A `prestige_tier` downgrade (Tier 1 → Tier 2 or lower) is a Principal Architect decision.
It may not be made by a curator alone. Downgrades require written rationale in `tier_rationale`
and must be logged as a governance event in `registry_audit_log`.

**9.4** Any new entry or tier upgrade to `prestige_tier = 'tier_1'`, regardless of
`creator_domain`, requires Principal Architect review. `[Amended v1.1 — BF-1: scope corrected
from natural_history only to all domains]` Tier 1 additions directly affect the `museum_print`
and `institutional_license` product surfaces, which require `illustrator_prestige = 1.0`. A Tier 1
addition in any domain is a commercial decision, not solely a historical one. The natural_history
domain is noted here because it was the original governed list, but the commercial governance
rationale applies equally to cartography, photography, fine art, and all other domains.

### Article 10 — Worker Resolution Protocol for Prestige `[Amended v1.1]`

**10.1** The scoring worker resolves `illustrator_prestige` as follows:

```
1. Normalize the opportunity's creator name: lowercase, strip honorifics and parenthetical dates.
2. Query creator_prestige_registry WHERE status = 'active'
   AND creator_name ILIKE normalized_name.
3. If match:
     illustrator_prestige = prestige_score from the matched row.  ← stored as concrete numeric
     Record in score_inputs:
       "illustrator_prestige":   <numeric value, e.g. 1.000>
       "prestige_creator_name":  "<matched canonical name>"
       "prestige_registry_row":  "<registry row UUID>"   ← audit metadata only (see 10.4)
4. If no exact match: illustrator_prestige = 0.0.
   Flag requires_curator_review = TRUE with curator_review_reason = 'manual_flag' if the
   raw creator name is non-empty and contains a recognizable personal name token.
```

**10.2** Fuzzy matching is not permitted for prestige resolution. The match must be exact
(case-insensitive). Near-misses must be flagged and escalated to curator review. No Tier 1 or
Tier 2 prestige signal may be applied without an exact match in the registry.

**10.3** Workers must not infer prestige from external sources, AI training data, or hardcoded
lookup tables. The `creator_prestige_registry` is the sole authority.

**10.4 Replayability clarification** `[New — v1.1, BF-6]`: `illustrator_prestige` is stored as a
concrete resolved numeric value in `score_inputs`. `prestige_creator_name` and
`prestige_registry_row` are audit metadata recorded for traceability — they are not replay inputs.
The replay worker verifies formula arithmetic from the stored `illustrator_prestige` value
consistent with the CI Constitution Article 14 replay protocol. The replay worker does not
re-query `creator_prestige_registry` to re-derive the prestige score. If the registry row has been
retired and versioned since the original scoring event, the stored numeric value in `score_inputs`
remains the authoritative input for replay. A discrepancy between the stored value and the current
registry entry is not a `replay_failure` — it is expected and governs the recompute queue.

---

## Part IV — Place-Iconic Taxa Registry

### Article 11 — Registry Definition `[Amended v1.1]`

**11.1** The `place_iconic_taxa_registry` supersedes `place_iconic_taxa_vocabulary` as the
governed source for the `taxon_place_iconic` Class B signal. The schema is extended to support
anchor-type-aware iconicity: the same taxon may be iconic for the same place in different anchor
contexts, and each context has an independent iconicity strength.

**11.2** `place_iconic_taxa_registry` schema:

```
place_iconic_taxa_registry
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  place_id              UUID NOT NULL REFERENCES places(id)
  taxon_key             TEXT NOT NULL
  taxon_display_name    TEXT NOT NULL
  anchor_type           TEXT NOT NULL
  iconicity_tier        TEXT NOT NULL
  iconicity_score       NUMERIC(4,3) NOT NULL
  iconicity_rationale   TEXT NOT NULL
  status                TEXT NOT NULL DEFAULT 'proposed'
  authored_by           TEXT NOT NULL
  approved_by           TEXT
  approved_at           TIMESTAMPTZ
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  retired_at            TIMESTAMPTZ

  UNIQUE (place_id, taxon_key, anchor_type)

  CONSTRAINT chk_pitr_anchor       CHECK (anchor_type IN ('biological','geographic','cultural'))
  CONSTRAINT chk_pitr_tier         CHECK (iconicity_tier IN ('canonical','strong','moderate'))
  CONSTRAINT chk_pitr_score        CHECK (iconicity_score BETWEEN 0.0 AND 1.0)
  CONSTRAINT chk_pitr_status       CHECK (status IN ('proposed','active','retired'))
  CONSTRAINT chk_pitr_second_human CHECK (
    status != 'active' OR approved_by IS DISTINCT FROM authored_by
  )
  CONSTRAINT chk_pitr_score_tier   CHECK (
    (iconicity_tier = 'canonical' AND iconicity_score = 1.000) OR
    (iconicity_tier = 'strong'    AND iconicity_score = 0.750) OR
    (iconicity_tier = 'moderate'  AND iconicity_score = 0.500)
  )

PostgreSQL RULE: no DELETE permitted on place_iconic_taxa_registry.  [BF-2 — v1.1]
  -- status = 'retired' is the terminal state. Hard deletion is unconstitutional.
```

### Article 12 — Iconicity Tier Definitions

| Tier | Score | Definition |
|---|---|---|
| `canonical` | 1.000 | The taxon is the defining biological or cultural identity of the place. Its absence from the place's commercial identity is unimaginable. The bison for Yellowstone. The bald eagle for the United States. Requires curator review in addition to second-human approval. |
| `strong` | 0.750 | The taxon is strongly associated with the place in popular and scholarly reference. Present in primary commercial imagery of the place. The gray wolf for Yellowstone. The sequoia for Yosemite. |
| `moderate` | 0.500 | The taxon is documented at the place and referenced in naturalist literature but is not a primary identity marker. Present in secondary commercial imagery. |

### Article 13 — Minimum Entry Requirements Per Place

**13.1** A place requires a minimum of five `status = 'active'` entries in
`place_iconic_taxa_registry` before the `taxon_place_iconic` signal is considered reliable for
that place. Fewer than five active entries produces a degraded signal. The scoring worker must log
a `signal_quality_warning` in `score_inputs` when fewer than five active entries exist for any
matched place.

**13.2** Priority places for initial seeding, in constitutional order:

1. **Yellowstone National Park** — first LOC integration target. Minimum seed: bison (canonical,
   biological), grizzly bear (strong, biological), gray wolf (strong, biological), trumpeter swan
   (strong, biological), osprey (moderate, biological). Minimum five entries required before the
   LOC photography pipeline may activate for Yellowstone-linked assets.

2. **Grand Canyon National Park** — second LOC target. Minimum seed: California condor (canonical,
   biological), canyon wren (strong, biological), bighorn sheep (strong, biological), prickly pear
   cactus (moderate, biological), river otter (moderate, biological).

3. **Yosemite National Park** — sequoia (canonical, biological), black bear (strong, biological),
   mule deer (strong, biological), Steller's jay (moderate, biological), mountain lion (moderate,
   biological).

**13.3** These five-entry minimums are constitutional seeding obligations, not recommendations. A
migration that activates LOC photography scoring for a place must include the minimum seed entries
or a curator acknowledgement that the degraded-signal mode is acceptable for initial activation.

### Article 14 — Worker Resolution Protocol for Iconicity `[Amended v1.1]`

**14.1** The scoring worker resolves `taxon_place_iconic` as follows:

```
1. Identify all place_ids linked to the opportunity via illustration_opportunity_places.
2. Identify the opportunity's anchor_type from illustration_opportunities.anchor_type.
3. For each place_id:
   a. Query place_iconic_taxa_registry WHERE place_id = $place_id
      AND taxon_key = opportunity.taxon_key
      AND status = 'active'
      AND anchor_type = opportunity.anchor_type.
   b. If anchor-matching entry found:
        taxon_place_iconic_for_place = MAX(iconicity_score) over matched rows.
   c. If no anchor-matching entry found:
        Attempt match without anchor_type filter.
        If cross-anchor match found:
          taxon_place_iconic_for_place = MAX(iconicity_score)
            × anchor_weight_spec.cross_anchor_discount_rate.
          Log 'cross_anchor_discount_applied: true' in score_inputs.
   d. If no match at all: taxon_place_iconic_for_place = 0.0.
4. taxon_place_iconic = MAX(taxon_place_iconic_for_place) across all linked places.
```

**14.2** Cross-anchor discount: An opportunity whose `anchor_type` does not match the registry
entry's `anchor_type` receives a discounted iconicity score. The discount rate is governed by
`anchor_weight_spec.cross_anchor_discount_rate` in `commerce_policy.formula_spec`. The discount
is automatic and does not require human approval per application.

**14.3** `[Amended v1.1 — BF-4]` The cross-anchor discount rate must not be hardcoded in worker
code. Workers must read it from `commerce_policy.formula_spec.anchor_weight_spec
.cross_anchor_discount_rate`. The initial governed value is `0.50`. Changes require a minor
`commerce_policy` version bump and second-human approval per CI Constitution Article 19.

---

## Part V — Creator Authority Registry

### Article 15 — Registry Definition `[Amended v1.1]`

**15.1** The `creator_authority_registry` is a governed table of canonical creator identity
records. It is the authority source for resolving creator name variants, linking creators to
external authority files, and anchoring `creator_prestige_registry` entries to unambiguous
identities.

**15.2** The registry is not a biographical database. It contains the minimum identity fields
required for disambiguation and external authority resolution.

**15.3** `creator_authority_registry` schema:

```
creator_authority_registry
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  canonical_name        TEXT NOT NULL UNIQUE        -- immutable after active
  alternate_names       TEXT[]                      -- immutable after active (see Article 16.4)
  birth_year            INT
  death_year            INT
  nationality           TEXT
  dominant_domain       TEXT NOT NULL
  active_period_start   INT
  active_period_end     INT

  viaf_uri              TEXT
  loc_authority_uri     TEXT
  ulan_uri              TEXT
  orcid_uri             TEXT

  prestige_registry_id  UUID REFERENCES creator_prestige_registry(id)

  status                TEXT NOT NULL DEFAULT 'proposed'
  authored_by           TEXT NOT NULL
  approved_by           TEXT
  approved_at           TIMESTAMPTZ
  notes                 TEXT
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()

  CONSTRAINT chk_car_status       CHECK (status IN ('proposed','active','retired'))
  CONSTRAINT chk_car_domain       CHECK (dominant_domain IN (
                                    'natural_history','cartography','fine_art',
                                    'photography','printmaking','other'))
  CONSTRAINT chk_car_second_human CHECK (
    status != 'active' OR approved_by IS DISTINCT FROM authored_by
  )
  CONSTRAINT chk_car_period       CHECK (
    active_period_start IS NULL OR active_period_end IS NULL OR
    active_period_start <= active_period_end
  )

PostgreSQL RULE: no DELETE permitted on creator_authority_registry.  [BF-2 — v1.1]
  -- status = 'retired' is the terminal state. Hard deletion is unconstitutional.

BEFORE UPDATE trigger: trg_car_immutable_after_active  [BF-5 — v1.1]
  -- When OLD.status = 'active':
  --   Raise exception if NEW.canonical_name != OLD.canonical_name
  --   Raise exception if NEW.alternate_names IS DISTINCT FROM OLD.alternate_names
  -- This enforces immutability of both canonical_name and alternate_names after activation.
```

### Article 16 — Authority Resolution Hierarchy `[Amended v1.1]`

**16.1** When the scoring worker or ingestion worker encounters a creator name, resolution proceeds
in order:

```
1. Exact match against creator_authority_registry.canonical_name (case-insensitive).
2. Exact match against any element of creator_authority_registry.alternate_names (case-insensitive).
3. If match via alternate_name:
     Resolve to canonical_name for all downstream scoring.
     Record in score_inputs:
       "alternate_name_resolved":  true
       "matched_alternate":        "<the matched alternate name>"
       "resolved_canonical":       "<canonical_name>"
       "authority_registry_row":   "<authority record UUID>"   ← audit metadata only
4. If no match: creator remains unresolved. illustrator_prestige = 0.0.
```

**16.2** Alternate name resolution is automatic. The canonical resolution is governed at registry
activation time — the `alternate_names` array was approved as part of the record and is immutable
after `active` (Article 16.4).

**16.3** At least one external authority URI (`viaf_uri`, `loc_authority_uri`, or `ulan_uri`) must
be present for any `status = 'active'` entry where `dominant_domain IN ('natural_history',
'cartography', 'photography', 'fine_art')`. For `printmaking` and `other` domains, authority
URIs are recommended but not required.

**16.4** `[Amended v1.1 — BF-5]` Both `canonical_name` and `alternate_names` are immutable after
the record reaches `active`. This is enforced by `trg_car_immutable_after_active` (Article 15.3).
Corrections to either field require a new record with `previous_version_id` pointing to the
current active record. On approval of the new record, the old record transitions to `retired` in
the same transaction. This is identical to the versioning pattern for `creator_prestige_registry`
(Article 9.2). Alternate name additions, removals, or corrections are not minor edits — they are
governed identity changes that must follow the full version-record lifecycle.

### Article 17 — Authority Record Lifecycle

**17.1** Lifecycle states: `proposed → active → retired`. Second-human approval is required for all
transitions to `active`. `retired` is the terminal state. Hard deletion is unconstitutional.

**17.2** `canonical_name` and `alternate_names` are both immutable after `active`. Corrections
require a new versioned record (Article 16.4).

**17.3** A `creator_authority_registry` record may not be retired while any
`creator_prestige_registry` entry references it with `status = 'active'`. The prestige entry must
be retired first, or its `creator_authority_id` updated to the replacement record within the same
transaction.

**17.4** `canonical_name` corrections and `alternate_names` corrections both require Principal
Architect review. They are not curator decisions.

---

## Part VI — Registry Lifecycle Governance

### Article 18 — Unified Lifecycle for All Registries

All four registries governed by this Constitution share a common lifecycle:

```
proposed
  ↓ authored by one human, with written rationale
  ↓ (optional: pending_curator_review — author uncertain, requests curator input)
  ↓ approved by a second human (not the author)
active
  ↓ update proposed (new record + previous_version_id link to current active)
  ↓ new record approved → new active, old record retired (same transaction)
  ↓ OR: retirement proposed (author) + approved (second human)
retired  (terminal — no hard DELETE on any registry table governed by this Constitution)
```

### Article 19 — The Second-Human Rule Across All Registries

**19.1** The second-human rule applies to all four registries and is enforced at the database level
via CHECK constraints. Self-approval is constitutionally prohibited and technically prevented.

**19.2** The second-human rule applies to each entry individually, not to batches. A batch
submission of ten prestige entries requires ten individual second-human approvals.

**19.3** Registry entries approved in violation of the second-human rule are void. The scoring
worker must not use void entries. Void entries are flagged back to `proposed` pending re-approval.

### Article 20 — Second-Human Approval Authority by Registry and Action

| Registry | Action | Second Human | Principal Architect Required? |
|---|---|---|---|
| `anchor_type` on `illustration_opportunities` | Assignment (any non-mixed value) | Curator | No |
| `anchor_type` on `illustration_opportunities` | `mixed` confirmation (Article 6.3–6.4) | Curator | No — but PA review recommended for first mixed assignment per asset class |
| `creator_prestige_registry` | New entry, any tier | Curator or Principal Architect | Yes — for Tier 1 (all domains) and `other` domain (all tiers) |
| `creator_prestige_registry` | Tier downgrade | Principal Architect only | Yes — always |
| `creator_prestige_registry` | Tier upgrade to Tier 1 | Curator | Yes — always (all domains) |
| `creator_prestige_registry` | Tier upgrade to Tier 2 or Tier 3 | Curator | No |
| `place_iconic_taxa_registry` | New entry, any tier | Curator | Yes — for `canonical` tier |
| `creator_authority_registry` | New entry | Curator or Principal Architect | No |
| `creator_authority_registry` | `canonical_name` or `alternate_names` correction | Principal Architect only | Yes — always |

### Article 21 — Registry Audit Requirements

Every state transition on every registry must be recorded in `registry_audit_log`. The event
structure:

```json
{
  "registry":        "<registry_name>",
  "record_id":       "<UUID>",
  "event_type":      "<proposed | approved | retired | rejected | updated>",
  "event_at":        "<ISO 8601 UTC>",
  "actor_type":      "<curator | principal_architect | system_worker>",
  "actor_id":        "<identity>",
  "previous_status": "<status or null>",
  "new_status":      "<status>",
  "actor_notes":     "<rationale — required for all human events>"
}
```

Registry audit events are written to `registry_audit_log` (Article 25). They are separate from
`score_audit_log`. Registry governance is upstream of scoring; the two audit trails must not be
conflated.

---

## Part VII — Human Approval Boundaries

### Article 22 — What Workers May Do `[Amended v1.1]`

Workers may:

1. Derive a provisional `anchor_type` from source metadata using the rules in Article 5.1.
2. Query all four registries for signal resolution (read-only).
3. Flag an unresolved creator or unmatched place as `curator_review_reason = 'manual_flag'`.
4. Apply the cross-anchor iconicity discount automatically using the rate from
   `anchor_weight_spec.cross_anchor_discount_rate`.
5. Log `signal_quality_warning` in `score_inputs` when fewer than five active place-iconic entries
   exist for a matched place.
6. Set `hard_gate_status = 'not_evaluated'` with `reason = 'mixed_anchor_blend_unconfirmed'` when
   `anchor_type = 'mixed'` and no curator confirmation event exists (Article 6.4).

Workers must not:

1. Write new entries to any registry governed by this Constitution.
2. Approve, retire, or reject any registry entry.
3. Confirm `anchor_type = 'mixed'` without a curator governance event (Article 6.3).
4. Apply `illustrator_prestige > 0.0` from any source other than `creator_prestige_registry`.
5. Hardcode prestige scores, creator lists, iconic taxa, authority identifiers, or the
   cross-anchor discount rate.
6. Proceed with mixed-anchor scoring when the mixed-anchor confirmation gate (Article 6.4) has
   not been cleared.

### Article 23 — What AI May Do

AI may:

1. Suggest candidate entries for `creator_prestige_registry` based on bibliographic research.
   Suggestions are advisory. A human must create the `proposed` record.
2. Suggest `anchor_type` derivation rules for new source types not covered by Article 5.1.
3. Suggest canonical name and alternate name candidates for `creator_authority_registry`.
4. Cross-reference external authority files (VIAF, LOC, ULAN) and suggest `authority_uri` values.

AI must not:

1. Create entries in any registry directly.
2. Approve, retire, or reject any registry entry.
3. Apply prestige scores derived from its training data. The registry is the sole authority.

### Article 24 — Curator Workflow Obligations

Before any asset class beyond Natural History Illustration and Prints/Engravings may be
commercially scored, the following registry prerequisites must be met:

| Asset Class | Registry Prerequisites |
|---|---|
| Historic Maps | Minimum three `creator_prestige_registry` entries, `creator_domain = 'cartography'`, any tier, `status = 'active'`. Minimum five `place_iconic_taxa_registry` entries per target place. `anchor_type = 'geographic'` confirmed for all map opportunities. |
| Historic Photography | Minimum three `creator_prestige_registry` entries, `creator_domain = 'photography'`, any tier, `status = 'active'`. Minimum five `place_iconic_taxa_registry` entries per target place. `anchor_type = 'geographic'` or `'cultural'` confirmed for all photography opportunities. |
| Fine Art | Minimum three `creator_prestige_registry` entries, `creator_domain = 'fine_art'`, any tier, `status = 'active'`. |
| Posters | `anchor_type = 'cultural'` confirmed for all poster opportunities. No additional prestige prerequisite. |
| Educational Documents | No additional registry prerequisite. `eligible_educational` flag gates scoring. |

A scoring worker that encounters an opportunity in a class that has not met its registry
prerequisites must set `hard_gate_status = 'not_evaluated'` with
`reason = 'registry_prerequisites_not_met'` and skip scoring.

---

## Part VIII — Scoring Integration

### Article 25 — Integration with Commerce Intelligence Constitution `[Amended v1.1]`

**25.1** This Constitution extends CI Constitution Article 6 signal vocabularies with the following
signals:

| Signal | Source | Default If Missing |
|---|---|---|
| `anchor_type` | `illustration_opportunities.anchor_type` | `'biological'` |
| `anchor_blend` | `illustration_opportunities.anchor_blend` (JSONB) | `null` — present only for `mixed` |
| `iconicity_score` | `place_iconic_taxa_registry` (supersedes `taxon_place_iconic` label) | `0.0` |
| `cross_anchor_discount_applied` | Boolean; logged in `score_inputs` when discount applied | `false` |
| `signal_quality_warning` | Boolean; logged when fewer than 5 active place-iconic entries | `false` |

**25.2** The `commerce_policy.formula_spec` must be extended to include an `anchor_weight_spec`
block. `[Amended v1.1 — BF-3, BF-4]`

Canonical `anchor_weight_spec` structure:

```json
{
  "anchor_weight_spec": {
    "cross_anchor_discount_rate": 0.50,
    "biological": {
      "composite_modifier": {
        "retail_weight":     0.30,
        "tourism_weight":    0.25,
        "museum_weight":     0.20,
        "publishing_weight": 0.15,
        "reference_weight":  0.10
      }
    },
    "geographic": {
      "composite_modifier": {
        "tourism_weight":    0.35,
        "museum_weight":     0.25,
        "retail_weight":     0.20,
        "reference_weight":  0.15,
        "publishing_weight": 0.05
      }
    },
    "cultural": {
      "composite_modifier": {
        "retail_weight":     0.30,
        "museum_weight":     0.25,
        "tourism_weight":    0.20,
        "reference_weight":  0.15,
        "publishing_weight": 0.10
      }
    },
    "mixed": {
      "blend_algorithm_version": "weighted_anchor_blend_v1",
      "blend_from":              ["primary", "secondary"]
    }
  }
}
```

**BF-3 Amendment:** `blend_strategy` has been renamed to `blend_algorithm_version`. The value
`"weighted_anchor_blend_v1"` names a registered algorithm in the scoring worker. The following
activation invariant is added: `blend_algorithm_version` must match a registered algorithm in the
scoring worker. A `catalog_policy` record that fails this invariant at activation time must be
rejected — status must not advance from `pending_approval` to `active`.

**BF-4 Amendment:** `cross_anchor_discount_rate` is now a top-level field in `anchor_weight_spec`.
Its initial governed value is `0.50`. Workers read this value from policy; they must not hardcode
it. Changes require a Minor `commerce_policy` version bump and second-human approval.

**25.3** For `anchor_type = 'mixed'`: the scoring worker blends the `composite_modifier` weight
sets for the two anchors named in `anchor_blend.primary` and `anchor_blend.secondary`, weighted by
`anchor_blend.primary_weight` and `anchor_blend.secondary_weight`. The blended weight set replaces
the single-anchor modifier for that scoring pass.

**Blend algorithm `weighted_anchor_blend_v1`:**

```
For each subscore weight key (retail, tourism, museum, publishing, reference):
  blended_weight[key] =
    anchor_weight_spec[primary].composite_modifier[key] × primary_weight
    + anchor_weight_spec[secondary].composite_modifier[key] × secondary_weight

Invariant: sum(blended_weight.values()) must equal 1.0 within ±0.001.
```

**25.4** `anchor_weight_spec` is part of `commerce_policy.formula_spec`. Adding
`anchor_weight_spec` for the first time is a Minor version bump and requires second-human approval
per CI Constitution Article 19. Changes to individual anchor weight sets thereafter are also Minor
bumps.

**25.5** `registry_audit_log` table schema:

```
registry_audit_log
  id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  registry                TEXT NOT NULL
  record_id               UUID NOT NULL
  event_type              TEXT NOT NULL
  event_at                TIMESTAMPTZ NOT NULL DEFAULT NOW()
  actor_type              TEXT NOT NULL
  actor_id                TEXT NOT NULL
  previous_status         TEXT
  new_status              TEXT
  actor_notes             TEXT
  previous_state          JSONB NOT NULL DEFAULT '{}'
  new_state               JSONB NOT NULL DEFAULT '{}'
  entry_checksum_sha256   TEXT NOT NULL
  previous_entry_checksum TEXT

  CONSTRAINT chk_ral_registry   CHECK (registry IN (
    'creator_prestige_registry',
    'place_iconic_taxa_registry',
    'creator_authority_registry',
    'anchor_type'
  ))
  CONSTRAINT chk_ral_event      CHECK (event_type IN (
    'proposed','approved','retired','rejected','updated'
  ))
  CONSTRAINT chk_ral_checksum   CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$')
  CONSTRAINT chk_ral_notes      CHECK (
    actor_type NOT IN ('curator','principal_architect') OR actor_notes IS NOT NULL
  )
```

Append-only. PostgreSQL RULE enforces no UPDATE, no DELETE. Hash chain follows the D-1 canonical
JSON specification from CI Constitution Article 15.

---

## Part IX — Prohibited Acts

### Article 26 — Prohibited Acts `[Amended v1.1]`

| Act | Prohibition |
|---|---|
| **PA-1** | No hardcoded prestige scores or creator lists in worker code. `illustrator_prestige` must be resolved exclusively from `creator_prestige_registry`. |
| **PA-2** | No `illustrator_prestige > 0.0` applied without a matching `status = 'active'` entry in `creator_prestige_registry`. |
| **PA-3** | No worker may write entries to any registry governed by this Constitution. |
| **PA-4** | No registry entry may become `active` without second-human approval enforced by DB constraint. |
| **PA-5** | No `anchor_type = 'mixed'` confirmed without a curator governance event and a populated `anchor_blend` JSONB on `illustration_opportunities`. |
| **PA-6** | No LOC opportunity may enter commercial scoring in a class that has not met the registry prerequisites in Article 24. Workers must set `hard_gate_status = 'not_evaluated'`. |
| **PA-7** | No `canonical_name` on `creator_authority_registry` may be changed after `active`. Name corrections require a new record. |
| **PA-8** | No Tier 1 entry in `creator_prestige_registry` in any domain without Principal Architect review. |
| **PA-9** | No `canonical` tier entry in `place_iconic_taxa_registry` without curator review in addition to second-human approval. |
| **PA-10** | No place-iconic signal computed from fewer than five active entries without logging `signal_quality_warning = true` in `score_inputs`. |
| **PA-11** | No prestige derived from AI training data, external APIs, or any source other than `creator_prestige_registry`. |
| **PA-12** | No registry audit event omitting `actor_notes` when `actor_type IN ('curator', 'principal_architect')`. |
| **PA-13** | No `prestige_tier` downgrade without Principal Architect approval. |
| **PA-14** | No UPDATE or DELETE on `registry_audit_log`. Append-only enforced by PostgreSQL RULE. |
| **PA-15** | No scoring worker may proceed past hard gate evaluation for an asset class whose registry prerequisites (Article 24) are not met. |
| **PA-16** | No `anchor_weight_spec` parameter — including `cross_anchor_discount_rate` — may be hardcoded in worker code. All parameters must live in `commerce_policy.formula_spec.anchor_weight_spec`. |
| **PA-17** | No hard DELETE on `creator_prestige_registry`, `place_iconic_taxa_registry`, or `creator_authority_registry`. `[New — v1.1, BF-2]` `status = 'retired'` is the terminal state. Deletion severs the audit chain for historical scoring events. Enforced by PostgreSQL RULE on each table. |
| **PA-18** | No scoring of an opportunity with `anchor_type = 'mixed'` without a curator confirmation event in `score_audit_log` (Article 6.4). `[New — v1.1, BF-7]` Unconfirmed mixed anchor is a hard pre-scoring block, not a review flag. |
| **PA-19** | No `alternate_names` modification on an `active` `creator_authority_registry` record. `[New — v1.1, BF-5]` Both `canonical_name` and `alternate_names` are immutable after `active`. Enforced by `trg_car_immutable_after_active`. |

---

## Part X — Migration Sequence

### Article 27 — Required Migrations `[Amended v1.1]`

These migrations depend on Migrations 19–31 (the commerce intelligence pipeline) having been
applied.

| Migration | Contents | Depends On |
|---|---|---|
| M-32 | Add `anchor_type TEXT NOT NULL DEFAULT 'biological'` to `illustration_opportunities`. Add `anchor_blend JSONB`. Add CHECK: `anchor_type IN ('biological','geographic','cultural','mixed')`. Add CHECK: `anchor_type = 'mixed' → anchor_blend IS NOT NULL`. Add CHECK: `anchor_type != 'mixed' → anchor_blend IS NULL`. Backfill: all existing records set `anchor_type = 'biological'`. | M-19 |
| M-33 | Create `creator_authority_registry` + constraints + second-human CHECK + no-DELETE RULE + `trg_car_immutable_after_active` trigger (enforces `canonical_name` and `alternate_names` immutability after `active`). Create `creator_prestige_registry` + constraints + second-human CHECK + no-DELETE RULE. Create `registry_audit_log` + append-only RULEs. Seed: eight priority natural history illustrators as `prestige_tier = 'tier_1'`, `creator_domain = 'natural_history'`, `status = 'proposed'`. `[Amended v1.1: no-DELETE RULE added to both tables; alternate_names immutability trigger added to creator_authority_registry]` | M-32 |
| M-34 | Create `place_iconic_taxa_registry` + constraints + second-human CHECK + no-DELETE RULE. Seed: Yellowstone five-entry minimum in `proposed` state. Seed: Grand Canyon five-entry minimum in `proposed` state. `[Amended v1.1: no-DELETE RULE added]` | M-33 |

**Activation (governed event, not a migration):**

All seed entries must transition from `proposed` to `active` through the constitutional approval
process before scoring workers use them. Activation of `anchor_weight_spec` in
`commerce_policy.formula_spec` (Article 25.2) is a Minor version bump requiring second-human
approval and must include `cross_anchor_discount_rate` and `blend_algorithm_version` in the seed
values. `[Amended v1.1 — BF-3, BF-4]`

**M-32 backfill note**: All existing records are BHL-sourced natural history illustrations.
Backfill to `anchor_type = 'biological'` is safe.

**M-33 seed note**: Eight priority illustrators seeded as `proposed`. Workers continue using
`priority_illustrators_vocabulary` until activation. This overlap is intentional.

**Activation note**: Switching to `creator_prestige_registry` as sole prestige source triggers
full `commerce_opportunities` recompute. The Principal Architect must confirm queue depth is
acceptable before activation proceeds.

### Article 28 — Activation Prerequisites `[Amended v1.1]`

The following conditions must be satisfied before activation proceeds:

1. All eight priority natural history illustrator entries in `creator_prestige_registry` are
   `status = 'active'` (second-human approved).
2. Minimum five Yellowstone entries in `place_iconic_taxa_registry` are `status = 'active'`.
3. `anchor_type` has been set on all existing `illustration_opportunities` records.
4. `commerce_policy.formula_spec` has been updated to include `anchor_weight_spec` with
   `cross_anchor_discount_rate` and `blend_algorithm_version` fields (Minor version bump;
   second-human approval required). `[Amended v1.1 — BF-3, BF-4]`
5. Scoring worker has been updated to resolve prestige from `creator_prestige_registry`.
6. `[Amended v1.1 — BF-6]` Replay worker has been updated to verify `illustrator_prestige` and
   `taxon_place_iconic` by re-computing formula arithmetic from stored `score_inputs` values.
   The replay worker does not re-query `creator_prestige_registry` or `place_iconic_taxa_registry`
   to re-derive these values. `prestige_registry_row` and `authority_registry_row` in `score_inputs`
   are audit metadata only — they are not replay inputs.

---

## Part XI — Open Questions

### Article 29 — Deferred Decisions

**Q1 — `creator_domain = 'other'` prestige application**. When a creator resolves to an authority
record with `dominant_domain = 'other'`, the scoring worker applies `illustrator_prestige = 0.0`
conservatively. A future version should define whether partial prestige is applicable for
confirmed Tier 3 `other`-domain creators.

**Q2 — Multi-place iconicity conflict resolution**. If an opportunity links to two places and
iconic taxa registries conflict for the same taxon (canonical for Place 1, moderate for Place 2),
the current protocol (Article 14.1 step 4) uses MAX. This may overstate the signal. A future
version should consider weighted average over `place_relevance_score` per place.

**Q3 — BHL cartographic and expedition asset reclassification**. BHL contains cartographic and
expedition survey materials currently defaulted to `anchor_type = 'biological'`. These should be
reclassified to `geographic`. The reclassification requires a bulk curator review event. Scope
and timeline are deferred.

**Q4 — Proactive prestige downgrade review cycle**. A creator who gains Tier 2 status through
auction activity may later lose commercial relevance. The versioning pattern (Article 9.2) handles
downgrade mechanics, but no staleness review cycle is defined. A future version should specify a
periodic review trigger — for example, annual review of all Tier 1 entries.

---

## Ratification

This Constitution v1.1.0 supersedes v1.0.0. All seven blocking findings identified in the
2026-06-06 governance audit are resolved. Implementation of Migrations M-32 through M-34 and the
Activation governed event is authorized, subject to:

1. The Principal Architect confirms this document is complete and correct.
2. Open Questions Q1 through Q4 in Article 29 do not block M-32 through M-34. They are tracked
   as future-work obligations.
3. Activation requires curator completion of all seed approvals in Article 28. Activation may not
   proceed until every prerequisite in Article 28 is confirmed.
4. The `commerce_policy.formula_spec` amendment (Article 25.2) requires a Minor version bump
   including `cross_anchor_discount_rate: 0.50` and `blend_algorithm_version:
   "weighted_anchor_blend_v1"` in the `anchor_weight_spec` seed, with second-human approval before
   activation proceeds.
5. The scoring worker change from hardcoded list to registry-based prestige resolution triggers
   full `commerce_opportunities` recompute. The Principal Architect must confirm queue depth before
   activation.
