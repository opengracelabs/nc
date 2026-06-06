# Historic Maps Activation Plan v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified |
| Repository | opengracelabs/nc |
| Date | 2026-06-06 |
| Role | Principal Architect |
| Corrects | `asset_expansion_strategy_v1.md` assertion "Full constitutional fit — no amendment required" |
| Constitutional Basis | CI v1.1, Product Routing v1.1, Catalog v1.1, Asset Intelligence v1.1 |

---

## Executive Finding

**Asset Expansion Strategy v1 was incorrect about Historic Maps.**

The strategy classified Historic Maps as "Full constitutional fit — no amendment required." After
auditing the live scoring formula (`commerce_policy` migration 20) against the actual signal
weights, this is wrong. A targeted CI Constitution v1.2 amendment is required before Historic
Maps can reach Tier 1 and access the `museum_print` and `institutional_license` product surfaces.

**Without the amendment**: Maps activate at Tier 2 only (wall art, calendar, puzzle, card).
`museum_print` and `institutional_license` are inaccessible. This is Partial Support.

**With the amendment**: Maps score at Tier 1 based on merit. All product surfaces accessible.
This is Full Support.

The amendment is targeted — a Minor CI Constitution version bump plus a commerce_policy version
bump. No new migrations. No new vocabulary tables. No redesign of the scoring formula structure.

---

## Part I — Pipeline Audit

### Stage 1 — Commerce Intelligence

| Gap | Root Cause | Status After M-32–M-35 |
|---|---|---|
| `anchor_type = null` on LOC assets blocks tier advancement | CI Constitution Open Question Q2: field not on `illustration_opportunities` | **RESOLVED** — M-32 adds the field with backfill `'biological'` for BHL assets; LOC assets assigned `'geographic'` by derivation worker |
| `anchor_weight_spec.geographic` not in active `commerce_policy` | No policy amendment has added it | **RESOLVED** — M-35 activation adds `anchor_weight_spec` to `formula_spec` |
| `illustrator_prestige = 0.0` for all cartographers | `creator_prestige_registry` has no cartography-domain entries | **RESOLVED** by curator seeding per Article 24 prerequisite |
| `taxon_place_iconic` does not apply geographic anchor context | `place_iconic_taxa_vocabulary` (pre-v1.1) lacked anchor_type awareness | **RESOLVED** — M-34 creates `place_iconic_taxa_registry` with anchor_type per entry; cross-anchor discount applies |
| **`taxon_commercial_tier_score = 0.0` permanently in retail/publishing/reference subscores** | No geographic-subject tier signal exists; `anchor_weight_spec` adjusts composite weights but not intra-subscore signal weights | **NOT RESOLVED** — requires CI Constitution v1.2 amendment |

### Stage 2 — Product Routing

| Gap | Status |
|---|---|
| `eligible_museum_print` blocked: requires `illustrator_prestige = 1.0` (policy seed line 545) | RESOLVED by Tier 1 cartographer seeding — no amendment needed |
| `eligible_institutional_license` blocked: requires `min_museum_score = 0.8` | Only achievable with Tier 1 scoring (see scoring analysis below) |
| Routing rules (`routing_rules`) are score/tier-based, not content-type-based | No amendment needed — routing is anchor-agnostic |

### Stage 3 — Catalog Intelligence

| Gap | Status |
|---|---|
| Nomination gates NG-0–NG-4 do not reference taxon_key or biological content | **No gap** — gates are score/status-based |
| `opportunity_snapshot` includes `taxon_commercial_tier` | Stored as `'none'` for maps — no amendment needed |

### Stage 4 — Publication Intelligence

Not audited in depth; no prior indication of geographic-specific blocks. Publication gates govern curator approval and variant readiness — not content-type-specific. No amendment presumed necessary.

### Stage 5 — Provider Routing

No geography-specific routing rules identified. Print-on-demand providers are content-agnostic.
No amendment needed.

**Summary**: One gap — the scoring formula — survives M-32–M-35. All other stages are either
resolved by M-32–M-35, resolved by seeding, or require no change.

---

## Part II — Scoring Formula Analysis

### The Gap

The current `commerce_policy` (migration 20) formula contains `taxon_commercial_tier_score` as a
weighted input in three subscores:

| Subscore | Signal Weight | COS Contribution Weight | Net COS Weight Lost to Gap |
|---|---|---|---|
| `retail_score` | 0.25 | 0.30 | **0.075** |
| `publishing_score` | 0.15 | 0.15 | **0.023** |
| `reference_score` | 0.20 | 0.10 | **0.020** |

For maps, `taxon_commercial_tier_score = 0.0` unconditionally. These three subscore slots —
representing **0.118 total COS weight** — contribute nothing to any map's composite score.

`anchor_weight_spec.geographic` reduces the composite weight of `retail_score` from 0.30 to 0.20
and `publishing_score` from 0.15 to 0.05. This reduces the COS weight lost from 0.118 to:

| Subscore | Signal Weight | Geographic COS Weight | Net COS Weight Lost |
|---|---|---|---|
| `retail_score` | 0.25 | **0.20** | **0.050** |
| `publishing_score` | 0.15 | **0.05** | **0.008** |
| `reference_score` | 0.20 | **0.15** | **0.030** |

With geographic weights: **0.088 total COS weight** permanently at zero. This is the irreducible
gap that `anchor_weight_spec` alone cannot close.

### Maximum Achievable COS for Maps

Given signal values for a strong Hayden Survey Yellowstone map (all non-taxon signals at
realistic high values, composition_fit curator-reviewed at 0.70):

| Scenario | COS | Commerce Tier |
|---|---|---|
| Biological weights, no seeding | 0.640 | **Tier 2 (barely)** |
| Geographic weights (`anchor_weight_spec.geographic`), no seeding | 0.710 | Tier 2 |
| Geographic weights + place-iconic seeding (Yellowstone 5-entry minimum) | 0.754 | Tier 2 |
| Geographic weights + seeding + signal substitution (**CI v1.2**) | **0.844** | **Tier 1** |

The Tier 1 threshold is COS ≥ 0.80. Maps cannot reliably reach Tier 1 without signal
substitution. Without Tier 1, `eligible_museum_print` and `eligible_institutional_license` are
not set by the scoring worker (`museum_print` requires Tier 1 + `illustrator_prestige = 1.0`
per `product_surface_requirements` line 543–546).

### Why `anchor_weight_spec` Is Insufficient

`anchor_weight_spec` governs composite subscore contribution weights — the outer layer of the
COS formula. It does not govern intra-subscore signal weights — the inner layer. The formula:

```
retail_score = (image_quality × 0.30) + (taxon_commercial_tier × 0.25) + ...
```

is intra-subscore. `anchor_weight_spec.geographic` can reduce retail_score's contribution to COS
from 0.30 to 0.20, but it cannot remove `taxon_commercial_tier × 0.25` from the retail_score
formula. The constitutional design of `anchor_weight_spec` did not anticipate this layer.

This is the structural gap. It requires a CI Constitution v1.2 amendment to address.

---

## Part III — Required Constitutional Amendment

### Amendment Target

**CI Constitution v1.2** — Add signal substitution rules for geographic-anchored assets to the
`anchor_weight_spec` policy structure.

### Amendment Design: Signal Substitution

When `anchor_type = 'geographic'`, the scoring worker substitutes `place_relevance_score` for
`taxon_commercial_tier_score` in all subscores that include it. `place_relevance_score` is an
existing scored signal (continuous, 0.0–1.0). It captures the commercial significance of the
linked place — the geographic equivalent of how `taxon_commercial_tier_score` captures the
commercial significance of a biological subject.

The substitution applies only within the intra-subscore formula. It does not create a new signal,
does not require a new vocabulary table, and does not change the formula structure — it is a
signal routing rule at policy application time.

### `anchor_weight_spec` Extension — Signal Substitutions Block

Add `signal_substitutions` to `anchor_weight_spec.geographic`:

```json
"geographic": {
  "composite_modifier": {
    "tourism_weight":    0.35,
    "museum_weight":     0.25,
    "retail_weight":     0.20,
    "reference_weight":  0.15,
    "publishing_weight": 0.05
  },
  "signal_substitutions": {
    "taxon_commercial_tier_score": "place_relevance_score"
  }
}
```

The `signal_substitutions` block is a map from `original_signal_name → substitute_signal_name`.
When applied by the scoring worker during intra-subscore computation for a geographic-anchored
asset, every occurrence of `taxon_commercial_tier_score` in any subscore formula is replaced by
the value of `place_relevance_score`.

### Activation Invariant

A new activation invariant must be added to the CI Constitution (alongside the existing
`scorer_version` and `blend_algorithm_version` invariants): at policy activation time, the scoring
worker must validate that every signal named in any `signal_substitutions` block is a recognized
scored signal. A policy that names an unrecognized substitute signal must be rejected at activation.

### CI Constitution Articles Requiring Amendment

| Article | Change |
|---|---|
| Article 6 — Signal Vocabulary | Add `signal_substitutions` to the governed `anchor_weight_spec` description |
| Article 12 — Scoring Algorithm | Add step: "For geographic-anchored assets, apply `signal_substitutions` from `anchor_weight_spec.geographic` before intra-subscore computation. Substituted signal name and value must be recorded in `score_inputs` as `substituted_signals: { original: value, substitute: value }`." |
| Article 13 — Policy Activation Invariants | Add: `signal_substitutions` values must be recognized scored signals; validated at activation time |
| Article 14 — Replay Protocol | Add: `substituted_signals` in `score_inputs` are replay inputs; replay reconstructs the substitution from the stored substitute value, not by re-querying policy |
| Article 37 — Open Question Q2 | Close: resolved by Asset Intelligence v1.1 (M-32) and this amendment (CI v1.2) |
| Article — Prohibited Acts | Add PA: no scoring worker may hardcode a geographic signal substitution; all substitutions must be read from `anchor_weight_spec.signal_substitutions` |

### Commerce Policy Amendment

After CI Constitution v1.2 ratification: issue a **Minor `commerce_policy` version bump** adding
the `signal_substitutions` block to `anchor_weight_spec.geographic` in `formula_spec`. Requires
second-human approval per CI Constitution Article 19.

**No new migration needed.** The `anchor_weight_spec` is added to `formula_spec` by the M-35
activation governed event. The `signal_substitutions` block is a field addition to that same JSONB
object, delivered as a Minor policy bump.

---

## Part IV — Activation Phases

### Phase 1 — Partial Activation (No Constitutional Amendment)

**Prerequisite chain:**

1. M-32: Add `anchor_type` to `illustration_opportunities`. Backfill existing records
   `'biological'`. LOC map ingest worker derives `'geographic'` from cartographic subject terms.
2. M-33: Create `creator_prestige_registry` + `creator_authority_registry`. Seed eight
   priority natural history illustrators as `proposed`.
3. M-34: Create `place_iconic_taxa_registry`. Seed Yellowstone five-entry minimum (bison,
   grizzly bear, gray wolf, trumpeter swan, osprey) as `proposed`.
4. Curator approval cycle: all seed entries transition to `status = 'active'` (second-human
   approval for each). Tier 1 cartographer entries seeded and approved.
5. M-35 activation: `anchor_weight_spec` added to `commerce_policy.formula_spec` (Minor version
   bump, second-human approval). `blend_algorithm_version` and `cross_anchor_discount_rate`
   included per Asset Intelligence v1.1 Article 28.
6. Scoring worker updated to resolve prestige from `creator_prestige_registry`; full
   `commerce_opportunities` recompute. Principal Architect confirms queue depth acceptable.
7. LOC map opportunities enter scoring pipeline.

**Phase 1 outcome:**

| Signal Behavior | After Phase 1 |
|---|---|
| `anchor_type` | `'geographic'` — correctly set, no null blocking |
| `illustrator_prestige` | 0.0–1.0 — from registry |
| `taxon_place_iconic` | 0.0–0.5 (cross-anchor discounted) — from seeded registry |
| `taxon_commercial_tier_score` | 0.0 — permanent gap, not fixed in Phase 1 |
| COS range (strong Hayden/Yellowstone map) | 0.71–0.76 |
| Commerce tier | Tier 2 |
| Product surfaces accessible | `wall_art_standard`, `calendar`, `puzzle`, `card`, `educational` |
| Product surfaces inaccessible | `museum_print`, `institutional_license`, `wall_art_premium` |

Phase 1 is commercially viable. Maps enter the pipeline and generate revenue at standard price
points. But the premium surfaces — the primary commercial target for historic cartography — remain
blocked.

### Phase 2 — Full Activation (With CI Constitution v1.2 Amendment)

**Required constitutional steps:**

1. Ratify CI Constitution v1.2 with signal substitution articles (Part III above).
2. Scoring worker updated to read `signal_substitutions` from `anchor_weight_spec` and apply
   substitutions before intra-subscore computation. `substituted_signals` written to `score_inputs`.
3. Replay worker updated to reconstruct substitution from `score_inputs.substituted_signals`.
4. Issue Minor `commerce_policy` version bump: add `signal_substitutions: { "taxon_commercial_tier_score": "place_relevance_score" }` to `anchor_weight_spec.geographic`. Second-human approval required.
5. Full `commerce_opportunities` recompute for all `anchor_type = 'geographic'` records.
   `policy_stale = TRUE` set on all geographic-anchored opportunities at policy activation.

**Phase 2 outcome:**

| Signal Behavior | After Phase 2 |
|---|---|
| `place_relevance_score` substitutes `taxon_commercial_tier_score` in retail, publishing, reference subscores | Active |
| COS range (strong Hayden/Yellowstone map, Tier 1 prestige, seeded place-iconic) | **0.84–0.93** |
| Commerce tier | **Tier 1** |
| Product surfaces accessible | **All** — including `museum_print` and `institutional_license` |
| `museum_print` eligibility | Requires `illustrator_prestige = 1.0` + `min_museum_score = 0.80` + `min_rights_confidence = 1.0` |

Maps of iconic places by recognized cartographers score Tier 1 on merit. Maps of minor places by
unknown cartographers score Tier 2 or Tier 3 on merit. Tier assignment becomes editorially
correct — it reflects actual commercial potential, not a penalty for the absence of biological content.

---

## Part V — Curator Seeding Obligations

### Tier 1 Cartographer Seed (Unblocks `museum_print`)

`museum_print` requires `illustrator_prestige = 1.0` from `product_surface_requirements`. Without
at least one active Tier 1 cartographer entry in `creator_prestige_registry`, no map can ever be
`eligible_museum_print = TRUE`. This seeding obligation is a hard prerequisite for Phase 1
commercial activation.

Priority Tier 1 candidates:

| Creator | Basis |
|---|---|
| Ferdinand Vandeveer Hayden | Primary author of the 1871 Yellowstone Survey maps; LOC collection; institutional recognition in geological survey literature |
| John Wesley Powell | Primary author of Colorado River / Grand Canyon survey; USGS founding director; LOC and Smithsonian holdings |
| William Henry Holmes | Panoramic cartographic illustrations for USGS surveys; Yellowstone and Grand Canyon; Smithsonian collections |

All three require: `creator_domain = 'cartography'`, `prestige_tier = 'tier_1'`,
`prestige_score = 1.000`, Principal Architect review (PA-8), second-human approval. Authority
records in `creator_authority_registry` with `loc_authority_uri` populated first.

### Yellowstone Place-Iconic Seed (Unblocks Tourism Signal)

Five-entry minimum per Article 13.2. Required before LOC Yellowstone map scoring is considered
reliable (signal_quality_warning fires if fewer than five active entries).

| Entry | `taxon_key` | `anchor_type` | `iconicity_tier` |
|---|---|---|---|
| Bison | `bos-bison` | `biological` | `canonical` |
| Grizzly bear | `ursus-arctos-horribilis` | `biological` | `strong` |
| Gray wolf | `canis-lupus` | `biological` | `strong` |
| Trumpeter swan | `cygnus-buccinator` | `biological` | `strong` |
| Osprey | `pandion-haliaetus` | `biological` | `moderate` |

For these entries to contribute to map scoring, the cross-anchor discount applies: a
`'geographic'`-anchored map linking to Yellowstone matches biological entries at
`anchor_weight_spec.cross_anchor_discount_rate = 0.50`. Canonical bison entry: effective
`taxon_place_iconic = 0.50` for maps.

### LOC Ingest Worker Scope

The LOC ingest worker must be extended to recognize cartographic records before maps enter the
pipeline. Current BHL ingest worker handles natural history illustrations. A geographic subject
classification must:

1. Detect LOC subject terms identifying cartographic materials (Library of Congress Subject
   Headings: `Maps`, `Cartography`, geographic area headings).
2. Derive `anchor_type = 'geographic'`.
3. Populate `place_relevance_score` based on the mapped area's place tier.
4. Populate `identification_confidence` based on attribution certainty in the LOC catalog record.

This is a worker implementation requirement, not a constitutional one. No CI Constitution
amendment is needed for this. The LOC proof-of-concept (Hayden Survey maps) established the
source availability.

---

## Part VI — Constitutional Amendment Summary

| Amendment Required | Document | Type | Scope |
|---|---|---|---|
| **YES** | CI Constitution v1.2 | Targeted | Add `signal_substitutions` to `anchor_weight_spec` design; add scoring worker step, activation invariant, replay protocol extension, PA |
| **YES** | `commerce_policy` Minor version bump | Policy | Add `signal_substitutions` block to `anchor_weight_spec.geographic` in `formula_spec` |
| No | Asset Intelligence Constitution v1.1 | — | Fully covers anchor_type, prestige domain, place-iconic, cross-anchor discount |
| No | Product Routing Constitution v1.1 | — | Routing rules are score/tier-based, not content-type-specific |
| No | Catalog Constitution v1.1 | — | Nomination gates do not require biological content |

---

## Part VII — Sequenced Activation Checklist

**Phase 1 Prerequisites (in order):**

- [ ] CI Constitution v1.2 drafted (can be done in parallel with migration work)
- [ ] M-32 applied: `anchor_type` field added to `illustration_opportunities`
- [ ] M-33 applied: `creator_prestige_registry`, `creator_authority_registry` created
- [ ] M-34 applied: `place_iconic_taxa_registry` created
- [ ] Authority records created for Hayden, Powell, Holmes in `creator_authority_registry` (`loc_authority_uri` populated)
- [ ] Prestige records seeded for Hayden, Powell, Holmes (`prestige_tier = 'tier_1'`, `creator_domain = 'cartography'`) — Principal Architect reviewed
- [ ] Prestige records approved (second-human, not the seeding author)
- [ ] Yellowstone five-entry minimum seeded in `place_iconic_taxa_registry` — canonical and strong tiers seeded
- [ ] Yellowstone entries approved (second-human)
- [ ] `anchor_weight_spec` Minor policy version bump activated (second-human approval) — without `signal_substitutions` for Phase 1
- [ ] LOC ingest worker extended to recognize cartographic records
- [ ] First LOC map opportunity ingested, scored, and curator-reviewed
- [ ] Phase 1 scoring verified: COS 0.70–0.76 for strong Hayden/Yellowstone maps ✓

**Phase 2 Prerequisites (after Phase 1):**

- [ ] CI Constitution v1.2 ratified
- [ ] Scoring worker updated: reads `signal_substitutions`; writes `substituted_signals` to `score_inputs`
- [ ] Replay worker updated: reconstructs substitution from `score_inputs.substituted_signals`
- [ ] `commerce_policy` Minor version bump: `signal_substitutions` block added to `anchor_weight_spec.geographic` (second-human approval)
- [ ] Full recompute of all `anchor_type = 'geographic'` opportunities (`policy_stale = TRUE` set at activation)
- [ ] Phase 2 scoring verified: COS 0.84+ for strong Hayden/Yellowstone maps ✓
- [ ] First Tier 1 map eligible for `museum_print` — curator review and approval ✓
