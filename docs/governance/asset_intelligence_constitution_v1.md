# Asset Intelligence Constitution v1.0

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Draft — awaiting Principal Architect ratification |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-06 |
| Role | Principal Architect |

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
            └─ Asset Intelligence Constitution v1.0  ← this document
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
| `mixed` | Asset holds significant commercial value from two or more anchors simultaneously. An Audubon plate in Yellowstone: biological (the bird) and geographic (the place). Requires explicit `anchor_blend` record. |

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

### Article 6 — Mixed-Anchor Governance

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

**6.2** Curator approval is required for every `anchor_type = 'mixed'` assignment. Workers may
propose `mixed` provisionally but must set `curator_review_reason = 'manual_flag'` on
`commerce_opportunities`. The blend weights require human review before scoring proceeds. The
default blend when a curator confirms `mixed` without specifying weights is
`primary_weight = 0.60, secondary_weight = 0.40`.

**6.3** A worker may not self-confirm an `anchor_type = 'mixed'` assignment. Proposal is
permitted; confirmation requires a curator governance event.

---

## Part III — Creator Prestige Registry

### Article 7 — Registry Definition

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
                            -- canonical name; resolved via creator_authority_registry when available
  creator_authority_id  UUID REFERENCES creator_authority_registry(id)
                            -- optional link; NULL permitted while authority record is proposed
  creator_domain        TEXT NOT NULL
  prestige_tier         TEXT NOT NULL          -- 'tier_1' | 'tier_2' | 'tier_3'
  prestige_score        NUMERIC(4,3) NOT NULL  -- tier_1=1.000, tier_2=0.750, tier_3=0.500
  tier_rationale        TEXT NOT NULL          -- why this creator holds this tier
  active_years          TEXT                   -- e.g. "1820–1880" or "c. 1750"
  primary_works         TEXT                   -- flagship publication(s); e.g. "Birds of America"
  status                TEXT NOT NULL DEFAULT 'proposed'
  authored_by           TEXT NOT NULL
  approved_by           TEXT                   -- required before status = 'active'
  approved_at           TIMESTAMPTZ
  version               INT NOT NULL DEFAULT 1 -- incremented on each update
  previous_version_id   UUID REFERENCES creator_prestige_registry(id)
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  retired_at            TIMESTAMPTZ

  CONSTRAINT chk_cpr_domain      CHECK (creator_domain IN (
                                    'natural_history','cartography','fine_art',
                                    'photography','printmaking','other'))
  CONSTRAINT chk_cpr_tier        CHECK (prestige_tier IN ('tier_1','tier_2','tier_3'))
  CONSTRAINT chk_cpr_score       CHECK (prestige_score BETWEEN 0.0 AND 1.0)
  CONSTRAINT chk_cpr_status      CHECK (status IN ('proposed','active','retired'))
  CONSTRAINT chk_cpr_second_human CHECK (
    status != 'active' OR approved_by IS DISTINCT FROM authored_by
  )
  CONSTRAINT chk_cpr_score_tier  CHECK (
    (prestige_tier = 'tier_1' AND prestige_score = 1.000) OR
    (prestige_tier = 'tier_2' AND prestige_score = 0.750) OR
    (prestige_tier = 'tier_3' AND prestige_score = 0.500)
  )
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

### Article 9 — Prestige Registry Lifecycle

**9.1** Lifecycle states:

```
proposed
  ↓ authored by one human, with rationale in tier_rationale
  ↓ approved by a second human (not the author)
active
  ↓ update proposed: new record with previous_version_id → old record
  ↓ new record approved (second human) → new record active, old record retired (same transaction)
retired
```

**9.2** An active entry may be updated only by creating a new record with `previous_version_id`
pointing to the active entry. On approval, the new record becomes `active` and the previous record
becomes `retired` in the same transaction.

**9.3** A `prestige_tier` downgrade (Tier 1 → Tier 2 or lower) is a Principal Architect decision.
It may not be made by a curator alone. Downgrades require written rationale in `tier_rationale`
and must be logged as a governance event in `registry_audit_log`.

**9.4** Any addition to `creator_domain = 'natural_history'` at `prestige_tier = 'tier_1'`
requires Principal Architect review. Tier 1 natural history additions directly affect the
`museum_print` and `institutional_license` product surfaces, which require
`illustrator_prestige = 1.0`. A Tier 1 addition is a commercial decision, not solely a historical one.

### Article 10 — Worker Resolution Protocol for Prestige

**10.1** The scoring worker resolves `illustrator_prestige` as follows:

```
1. Normalize the opportunity's creator name: lowercase, strip honorifics and parenthetical dates.
2. Query creator_prestige_registry WHERE status = 'active'
   AND creator_name ILIKE normalized_name.
3. If match: illustrator_prestige = prestige_score from the matched row.
   Record matched creator_name and registry row id in score_inputs snapshot.
4. If no exact match: illustrator_prestige = 0.0.
   Flag requires_curator_review = TRUE with curator_review_reason = 'manual_flag' if the
   raw creator name is non-empty and contains a recognizable personal name token.
```

**10.2** Fuzzy matching is not permitted for prestige resolution. The match must be exact
(case-insensitive). Near-misses must be flagged and escalated to curator review. No Tier 1 or
Tier 2 prestige signal may be applied without an exact match in the registry.

**10.3** Workers must not infer prestige from external sources, AI training data, or hardcoded
lookup tables. The `creator_prestige_registry` is the sole authority. Any implementation that
applies prestige from any other source is unconstitutional.

---

## Part IV — Place-Iconic Taxa Registry

### Article 11 — Registry Definition

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
                            -- taxon identifier from BHL or LOC subject vocabulary
  taxon_display_name    TEXT NOT NULL
                            -- human-readable name for audit display
  anchor_type           TEXT NOT NULL
                            -- 'biological' | 'geographic' | 'cultural'
                            -- governs which anchor_type opportunities this entry boosts
  iconicity_tier        TEXT NOT NULL     -- 'canonical' | 'strong' | 'moderate'
  iconicity_score       NUMERIC(4,3) NOT NULL
                            -- canonical=1.000, strong=0.750, moderate=0.500
  iconicity_rationale   TEXT NOT NULL
                            -- why this taxon is iconic for this place in this anchor context
  status                TEXT NOT NULL DEFAULT 'proposed'
  authored_by           TEXT NOT NULL
  approved_by           TEXT
  approved_at           TIMESTAMPTZ
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
  retired_at            TIMESTAMPTZ

  UNIQUE (place_id, taxon_key, anchor_type)
  -- same taxon may be iconic for same place in different anchor contexts independently

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

### Article 14 — Worker Resolution Protocol for Iconicity

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
          taxon_place_iconic_for_place = MAX(iconicity_score) × 0.50.
          Log 'cross_anchor_discount_applied: true' in score_inputs.
   d. If no match at all: taxon_place_iconic_for_place = 0.0.
4. taxon_place_iconic = MAX(taxon_place_iconic_for_place) across all linked places.
```

**14.2** Cross-anchor discount: An opportunity whose `anchor_type` does not match the registry
entry's `anchor_type` receives 50% of the iconicity score. The discount is a deliberate governance
choice: a geographic asset benefits from biological iconic taxa entries, but less directly than
a biological asset. The discount is automatic and does not require human approval.

**14.3** The cross-anchor discount rate (50%) is a parameter that may be changed by a minor policy
version bump on `commerce_policy`. It must not be hardcoded in worker code.

---

## Part V — Creator Authority Registry

### Article 15 — Registry Definition

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
  canonical_name        TEXT NOT NULL UNIQUE
                            -- the one canonical name used in all NC records; immutable after active
  alternate_names       TEXT[]
                            -- historical spellings, maiden names, pen names, transliterations
  birth_year            INT               -- null if unknown
  death_year            INT               -- null if unknown or living
  nationality           TEXT              -- ISO 3166-1 alpha-2 at peak active period; null if unknown
  dominant_domain       TEXT NOT NULL     -- creator_domain vocabulary (Article 7.2)
  active_period_start   INT               -- earliest known active year; null if unknown
  active_period_end     INT               -- latest known active year; null if ongoing or unknown

  -- External authority links
  -- At least one is required for active records in non-'other' domains (Article 16.3)
  viaf_uri              TEXT              -- Virtual International Authority File
  loc_authority_uri     TEXT              -- Library of Congress Name Authority File
  ulan_uri              TEXT              -- Union List of Artist Names (Getty)
  orcid_uri             TEXT              -- ORCID (for modern creators)

  -- Internal link
  prestige_registry_id  UUID REFERENCES creator_prestige_registry(id)
                            -- null if no prestige entry exists yet

  -- Governance
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
```

### Article 16 — Authority Resolution Hierarchy

**16.1** When the scoring worker or ingestion worker encounters a creator name, resolution proceeds
in order:

```
1. Exact match against creator_authority_registry.canonical_name (case-insensitive).
2. Exact match against any element of creator_authority_registry.alternate_names (case-insensitive).
3. If match via alternate_name:
     Resolve to canonical_name for all downstream scoring.
     Log 'alternate_name_resolved: true' in score_inputs with the matched alternate and
     the resolved canonical_name.
4. If no match: creator remains unresolved.
     illustrator_prestige = 0.0.
     Unresolved creators are eligible for curator-initiated authority record proposals.
```

**16.2** Alternate name resolution is automatic and does not require human approval per use. The
canonical resolution is governed at registry activation time — the list of alternate names was
approved when the record became `active`.

**16.3** At least one external authority URI (`viaf_uri`, `loc_authority_uri`, or `ulan_uri`) must
be present for any `status = 'active'` entry where `dominant_domain IN ('natural_history',
'cartography', 'photography', 'fine_art')`. For `printmaking` and `other` domains, authority
URIs are recommended but not required.

**16.4** `canonical_name` is immutable after the record reaches `active`. Name corrections require
a new record with the corrected canonical, followed by retirement of the incorrect record and
update of all `creator_prestige_registry` entries referencing the retired record.

### Article 17 — Authority Record Lifecycle

**17.1** Lifecycle states follow the pattern established in Article 9 for prestige: `proposed →
active → retired`. Second-human approval is required for all transitions to `active`.

**17.2** `canonical_name` is immutable after `active`. Any proposed name correction is a new record,
not an update.

**17.3** A `creator_authority_registry` record may not be retired while any
`creator_prestige_registry` entry references it with `status = 'active'`. The prestige entry must
be retired first, or its `creator_authority_id` must be updated to the replacement record within
the same transaction.

**17.4** `canonical_name` corrections require Principal Architect review. They are not curator
decisions.

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
retired
```

`pending_curator_review` is optional. It is used when the author requests curator input before
second-human approval proceeds.

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
| `anchor_type` on `illustration_opportunities` | Assignment (any value) | Curator | Only for `mixed` (Article 6.2) |
| `creator_prestige_registry` | New entry, any tier | Curator or Principal Architect | Yes — for Tier 1 entries and `other` domain |
| `creator_prestige_registry` | Tier downgrade | Principal Architect only | Yes — always |
| `creator_prestige_registry` | Tier upgrade | Curator | Yes — if upgrading to Tier 1 |
| `place_iconic_taxa_registry` | New entry, any tier | Curator | Yes — for `canonical` tier |
| `creator_authority_registry` | New entry | Curator or Principal Architect | No — unless correcting a canonical_name |
| `creator_authority_registry` | canonical_name correction | Principal Architect only | Yes — always |

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

### Article 22 — What Workers May Do

Workers may:

1. Derive a provisional `anchor_type` from source metadata using the rules in Article 5.1.
2. Query all four registries for signal resolution (read-only).
3. Flag an unresolved creator or unmatched place as `curator_review_reason = 'manual_flag'`.
4. Apply the cross-anchor iconicity discount (Article 14.2) automatically without human approval.
5. Log `signal_quality_warning` in `score_inputs` when fewer than five active place-iconic entries exist.

Workers must not:

1. Write new entries to any registry governed by this Constitution.
2. Approve, retire, or reject any registry entry.
3. Confirm `anchor_type = 'mixed'` without a curator governance event.
4. Apply `illustrator_prestige > 0.0` from any source other than `creator_prestige_registry`.
5. Hardcode prestige scores, creator lists, iconic taxa, or authority identifiers.

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
| Historic Maps | Minimum three `creator_prestige_registry` entries, `creator_domain = 'cartography'`, any tier, `status = 'active'`. Minimum five `place_iconic_taxa_registry` entries per target place, `status = 'active'`. `anchor_type = 'geographic'` confirmed for all map opportunities. |
| Historic Photography | Minimum three `creator_prestige_registry` entries, `creator_domain = 'photography'`, any tier, `status = 'active'`. Minimum five `place_iconic_taxa_registry` entries per target place, `status = 'active'`. `anchor_type = 'geographic'` or `'cultural'` confirmed for all photography opportunities. |
| Fine Art | Minimum three `creator_prestige_registry` entries, `creator_domain = 'fine_art'`, any tier, `status = 'active'`. |
| Posters | `anchor_type = 'cultural'` confirmed for all poster opportunities. No additional prestige prerequisite. |
| Educational Documents | No additional registry prerequisite. `eligible_educational` flag gates scoring. |

A scoring worker that encounters an opportunity in a class that has not met its registry
prerequisites must flag the opportunity as `hard_gate_status = 'not_evaluated'` with
`reason = 'registry_prerequisites_not_met'` and skip scoring. This is a hard stop, not a
degraded-signal continuation.

---

## Part VIII — Scoring Integration

### Article 25 — Integration with Commerce Intelligence Constitution

**25.1** This Constitution extends CI Constitution Article 6 signal vocabularies with the following
signals:

| Signal | Source | Default If Missing |
|---|---|---|
| `anchor_type` | `illustration_opportunities.anchor_type` | `'biological'` |
| `anchor_blend` | `illustration_opportunities.anchor_blend` (JSONB) | `null` — only present for `mixed` |
| `iconicity_score` | `place_iconic_taxa_registry` (supersedes `taxon_place_iconic` label) | `0.0` |
| `cross_anchor_discount_applied` | Boolean; logged in `score_inputs` when cross-anchor resolution occurs | `false` |
| `signal_quality_warning` | Boolean; logged when fewer than 5 active place-iconic entries exist for matched place | `false` |

**25.2** The `commerce_policy.formula_spec` must be extended to include an `anchor_weight_spec`
block that governs subscore weight selection by `anchor_type`. This block is a modifier on the
existing composite formula structure — it selects which weight set to apply, not a replacement of
the formula itself.

Canonical `anchor_weight_spec` structure:

```json
{
  "anchor_weight_spec": {
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
      "blend_strategy": "weighted_blend_from_anchor_blend_spec",
      "blend_from":     ["primary", "secondary"]
    }
  }
}
```

**25.3** For `anchor_type = 'mixed'`: the scoring worker blends the composite modifiers for the
two named anchors using `anchor_blend.primary_weight` and `anchor_blend.secondary_weight`. The
blended composite modifier replaces the single-anchor modifier for that scoring pass.

**25.4** `anchor_weight_spec` is part of `commerce_policy.formula_spec`. Adding `anchor_weight_spec`
for the first time is a Minor version bump and requires second-human approval per CI Constitution
Article 19. Changes to individual anchor weight sets thereafter are also Minor bumps.

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

### Article 26 — Prohibited Acts

| Act | Prohibition |
|---|---|
| **PA-1** | No hardcoded prestige scores or creator lists in worker code. `illustrator_prestige` must be resolved exclusively from `creator_prestige_registry`. |
| **PA-2** | No `illustrator_prestige > 0.0` applied without a matching `status = 'active'` entry in `creator_prestige_registry`. |
| **PA-3** | No worker may write entries to any registry governed by this Constitution. |
| **PA-4** | No registry entry may become `active` without second-human approval enforced by DB constraint. |
| **PA-5** | No `anchor_type = 'mixed'` confirmed without a curator governance event and a populated `anchor_blend` JSONB on `illustration_opportunities`. |
| **PA-6** | No LOC opportunity may enter commercial scoring in a class that has not met the registry prerequisites in Article 24. Workers must set `hard_gate_status = 'not_evaluated'`. |
| **PA-7** | No `canonical_name` on `creator_authority_registry` may be changed after `active`. Name corrections require a new record and retirement of the prior record. |
| **PA-8** | No Tier 1 entry in `creator_prestige_registry` without Principal Architect review. |
| **PA-9** | No `canonical` tier entry in `place_iconic_taxa_registry` without curator review in addition to second-human approval. |
| **PA-10** | No place-iconic signal computed from fewer than five active entries without logging `signal_quality_warning = true` in `score_inputs`. |
| **PA-11** | No prestige derived from AI training data, external APIs, or any source other than `creator_prestige_registry`. |
| **PA-12** | No registry audit event omitting `actor_notes` when `actor_type IN ('curator', 'principal_architect')`. |
| **PA-13** | No `prestige_tier` downgrade without Principal Architect approval. |
| **PA-14** | No UPDATE or DELETE on `registry_audit_log`. Append-only enforced by PostgreSQL RULE. |
| **PA-15** | No scoring worker may proceed past hard gate evaluation for an asset class whose registry prerequisites (Article 24) are not met. |
| **PA-16** | No `anchor_weight_spec` may be hardcoded in worker code. All anchor weight sets must live in `commerce_policy.formula_spec.anchor_weight_spec`. |

---

## Part X — Migration Sequence

### Article 27 — Required Migrations

These migrations depend on Migrations 19–31 (the commerce intelligence pipeline) having been
applied. They are independent of each other except where noted.

| Migration | Contents | Depends On |
|---|---|---|
| M-32 | Add `anchor_type TEXT NOT NULL DEFAULT 'biological'` to `illustration_opportunities`. Add `anchor_blend JSONB` to `illustration_opportunities`. Add CHECK: `anchor_type IN ('biological','geographic','cultural','mixed')`. Add CHECK: `anchor_type = 'mixed' → anchor_blend IS NOT NULL`. Add CHECK: `anchor_type != 'mixed' → anchor_blend IS NULL`. Backfill: all existing records set `anchor_type = 'biological'`. | M-19 (`illustration_opportunities` exists with LOC source constraint already unlocked) |
| M-33 | Create `creator_authority_registry` table + constraints + second-human CHECK. Create `creator_prestige_registry` table + constraints + second-human CHECK. Create `registry_audit_log` table + append-only RULEs. Seed: eight priority natural history illustrators in `creator_prestige_registry` as `prestige_tier = 'tier_1'`, `creator_domain = 'natural_history'`, `status = 'proposed'`. | M-32 |
| M-34 | Create `place_iconic_taxa_registry` table + constraints (extends `place_iconic_taxa_vocabulary` from M-19). Seed: Yellowstone five-entry minimum in `proposed` state. Seed: Grand Canyon five-entry minimum in `proposed` state. | M-33 |
| M-35 | Activation migration (governed event, not structural DDL): Transition all proposed seed entries to `active` (requires curator second-human approval events before this migration runs). Update scoring worker configuration to resolve prestige from `creator_prestige_registry` instead of `priority_illustrators_vocabulary`. Retire superseded `priority_illustrators_vocabulary` entries. Retire superseded `place_iconic_taxa_vocabulary` entries. Flag all `commerce_opportunities` as `policy_stale = TRUE` (full recompute required). Add `anchor_weight_spec` to `commerce_policy.formula_spec` (Minor version bump; second-human approval required). | M-34; curator approval of all proposed seed entries; commerce_policy Minor version bump ratified |

**M-32 backfill note**: Backfilling all existing records to `anchor_type = 'biological'` is safe
— all existing records are BHL-sourced natural history illustrations. LOC-sourced records ingested
after M-32 receive a provisional `anchor_type` from the ingestion worker per Article 5.1, subject
to curator review.

**M-33 seed note**: Eight priority illustrators are seeded as `proposed`. Workers continue to use
the existing hardcoded list from `priority_illustrators_vocabulary` until M-35 activation. This
overlap is intentional — it prevents a scoring gap during the registry transition.

**M-35 activation note**: Switching to `creator_prestige_registry` as the sole prestige source
affects all existing `commerce_opportunities` scores. The curator must be notified of recompute
queue depth before M-35 proceeds. The Principal Architect must confirm the recompute is
acceptable.

### Article 28 — Activation Prerequisites for M-35

The following conditions must be satisfied before M-35 proceeds:

1. All eight priority natural history illustrator seed entries in `creator_prestige_registry` are
   `status = 'active'` (second-human approved).
2. Minimum five Yellowstone entries in `place_iconic_taxa_registry` are `status = 'active'`.
3. `anchor_type` has been set (worker-derived or curator-confirmed) on all existing
   `illustration_opportunities` records.
4. `commerce_policy.formula_spec` has been updated to include `anchor_weight_spec` (Minor version
   bump; second-human approval required before M-35).
5. Scoring worker has been updated to resolve prestige from `creator_prestige_registry`.
6. Replay worker has been updated to replay prestige resolution from the `creator_name` and
   `registry_row_id` snapshot in `score_inputs`.

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

This Constitution v1.0.0 is submitted for Principal Architect ratification.

Implementation of Migrations M-32 through M-35 is authorized upon ratification, subject to:

1. The Principal Architect confirms this document is complete and correct.
2. Open Questions Q1 through Q4 in Article 29 do not block M-32 through M-34. They are tracked
   as future-work obligations.
3. M-35 requires curator completion of all seed approvals specified in Article 28. M-35 may not
   proceed until every prerequisite in Article 28 is confirmed.
4. The `commerce_policy.formula_spec` amendment (Article 25.2 — `anchor_weight_spec`) requires a
   Minor version bump and second-human approval before M-35 proceeds. This is independent of the
   migration sequence and may be authored and approved in parallel with M-32 through M-34.
5. The scoring worker change from hardcoded prestige list to registry-based resolution is a
   breaking change that triggers full `commerce_opportunities` recompute. The Principal Architect
   must confirm the recompute queue is acceptable before M-35 activates.
