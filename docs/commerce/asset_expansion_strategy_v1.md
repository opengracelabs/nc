# Asset Expansion Strategy v1

| Field | Value |
|---|---|
| Version | 1.0.1 |
| Status | Ratified — amended by erratum 2026-06-06 |
| Repository | opengracelabs/nc |
| Date | 2026-06-06 |
| Role | Principal Architect |
| Constitutional Basis | Commerce Intelligence v1.2, Product Routing v1.1, Catalog v1.1, Publication v1.1, Asset Intelligence v1.1 |

---

## Erratum — 2026-06-06

**Historic Maps row corrected.** Original version stated "Constitutional fit: Full, New governance
required: No." This was incorrect. The `historic_maps_activation_plan_v1.md` analysis found that
CI Constitution v1.1 was insufficient for full Tier 1 Historic Maps support: `taxon_commercial_tier_score`
occupies intra-subscore weight slots (retail: 0.25, publishing: 0.15, reference: 0.20) that are
unconditionally zero for geographic-anchored assets. `anchor_weight_spec` corrects composite
weights but cannot modify intra-subscore signal values. The 0.088 suppressed COS weight prevented
Tier 1 access.

CI Constitution v1.2 (Director Decision G-3) resolved this gap by adding `signal_substitutions`
to `anchor_weight_spec.geographic`. With CI v1.2 ratified, Historic Maps has full constitutional
fit. The Summary Matrix and Historic Maps section below have been corrected.

---

## Strategic Context

The current pipeline is commercially optimized for Natural History Illustration and
Prints/Engravings. This document evaluates seven additional asset classes against three
expansion criteria:

1. **Constitutional fit** — can the asset class be governed by the ratified constitutional
   framework without amendment?
2. **Governance requirement** — does expansion require a new or amended constitution?
3. **Pipeline reuse** — can the asset class enter commercial scoring without code changes
   beyond Migrations M-32–M-35?

The seven classes are ranked by estimated near-term commercial return to the platform.

---

## Summary Matrix

| Rank | Asset Class | Constitutional Fit | New Governance | Pipeline Unchanged |
|---|---|---|---|---|
| 1 | Historic Maps | **Full** (requires CI v1.2 — now ratified) | Yes — CI v1.2 signal_substitutions | Yes |
| 2 | Historic Photography | **Full** | No | Yes |
| 3 | Botanical Art | **Full** | No | Yes |
| 4 | Architectural Drawings | **Partial** | Yes | No |
| 5 | Posters | **Full** | No | Yes |
| 6 | Books | **Partial** | Yes | No |
| 7 | Manuscripts | **Partial** | Yes | No |

**Tier 1 — Expand now (after M-32–M-35 activation):** Historic Maps, Historic Photography,
Botanical Art, Posters.

**Tier 2 — Expand after targeted governance amendment:** Architectural Drawings, Books,
Manuscripts.

---

## Detailed Analysis

---

### 1. Historic Maps

**Constitutional fit: Full — requires CI Constitution v1.2 (now ratified).**

Asset Intelligence v1.1 resolves the anchor-type governance gaps. CI Constitution v1.2
(Director Decision G-3) resolves the intra-subscore scoring gap:

- `anchor_type = 'geographic'` is a ratified vocabulary value (Asset Intelligence v1.1 Article 4).
- `creator_prestige_registry` includes the `cartography` domain (Asset Intelligence v1.1 Article 7.2).
- `anchor_weight_spec.geographic` applies place-dominant composite weighting (AI v1.1 Article 25.2).
- `anchor_weight_spec.geographic.signal_substitutions` substitutes `place_relevance_score` for
  `taxon_commercial_tier_score` in retail, publishing, and reference intra-subscore computation
  (CI v1.2 Article 13, Director Decision G-3). This resolves the 0.088 suppressed COS weight.
- `cross_anchor_discount_rate` governs biological iconicity cross-anchor cases (AI v1.1 Article 14.2).
- Product surfaces `museum_print`, `tourism`, `institutional_license`, `reference` are applicable.
  With signal_substitutions active, strong maps can reach COS ≈ 0.844 — full Tier 1 access.

**New governance required: Yes — CI Constitution v1.2.** Now ratified. Curator seeding satisfies
all remaining prerequisites.

**Pipeline unchanged: Yes.** After M-32–M-35 and CI v1.2 commerce_policy Minor version bump,
the scoring worker reads `anchor_weight_spec.geographic.signal_substitutions` without code
change beyond implementing the Article 13 scoring algorithm.

**Prerequisites before first map asset scores:**

- Article 24 minimum: 3 `creator_prestige_registry` entries, `creator_domain = 'cartography'`,
  `status = 'active'`.
- Article 13 minimum: 5 `place_iconic_taxa_registry` entries per target place, `status =
  'active'`.
- `anchor_type = 'geographic'` confirmed by curator on each map opportunity.

**Priority seed candidates:** John Mitchell (1755 Map of British and French dominions), William
Faden, Rand McNally survey maps. Yellowstone cartographers: Ferdinand Hayden survey maps (LOC
collection, already explored in this session as LOC proof of concept).

**Commercial case:** Historic maps have established auction presence and institutional licensing
demand. The Hayden Survey integration already identified at least one LOC map asset. This is the
highest-confidence near-term expansion.

---

### 2. Historic Photography

**Constitutional fit: Full.**

- `anchor_type = 'geographic'` or `'cultural'` — both constitutional (Article 4).
- `creator_prestige_registry` includes `photography` domain (Article 7.2).
- `anchor_weight_spec.geographic` or `.cultural` applies appropriate signal weighting.
- Article 24 minimum prerequisites for photography are defined.

**New governance required: No.**

**Pipeline unchanged: Yes.** One calibration note, not a governance gap:

`color_profile` signal in CI Constitution Article 6 is optimized for illustrated color plates —
it scores color print presence positively over monochrome. Historic photographs in albumen,
cyanotype, or sepia formats are technically monochrome but carry high commercial value.
`color_profile` will understate these assets' commercial potential. This is a scoring calibration
concern, not a constitutional violation. Resolution: a Minor `commerce_policy` version bump
adjusting `color_profile` weight for `anchor_type IN ('geographic', 'cultural')` assets. The
curator_override mechanism handles individual high-value exceptions until calibration is applied.

**Prerequisites before first photography asset scores:**

- 3 `creator_prestige_registry` entries, `creator_domain = 'photography'`, `status = 'active'`.
- 5 `place_iconic_taxa_registry` entries per target place.
- `anchor_type` confirmed by curator per opportunity.

**Priority seed candidates:** William Henry Jackson (Yellowstone photographs, LOC collection),
Timothy O'Sullivan (geological survey photographs), Carleton Watkins (Yosemite).

**Commercial case:** Yellowstone photography by Jackson — same LOC collection as the Hayden
Survey — positions historic photography as the natural second activation alongside maps. Same
source, same provenance, same place seeding.

---

### 3. Botanical Art

**Constitutional fit: Full.**

Botanical Art is a subclass of Natural History Illustration — the platform's canonical
first-class asset. It requires no extension:

- `anchor_type = 'biological'` (default for all BHL-sourced assets).
- `taxon_commercial_tier` fully applicable to plant taxa.
- `taxon_place_iconic` applicable for place-associated flora.
- `illustrator_prestige` fully applicable — Redouté is already in the priority seed.
- `color_profile` highly applicable — botanical art is the exemplar of the celebrated color
  plate format.
- `era_score` fully applicable — botanical golden age 1750–1850 aligns with platform doctrine.

**New governance required: No.**

**Pipeline unchanged: Yes.** Botanical Art is already scoreable with the current pipeline.
M-32–M-35 improve scoring fidelity; they are not prerequisites for basic botanical scoring.

**Action required:** Prestige registry seeding only. The eight priority illustrators include one
botanical specialist (Redouté). The field is underseeded. Priority additions:

| Creator | Tier | Rationale |
|---|---|---|
| Georg Dionysius Ehret | Tier 1 | The foundational botanical illustrator; Plantae et Papiliones Rariores; Chelsea Physic Garden record |
| Pierre-Joseph Turpin | Tier 2 | Duhamel botanical plates; Annales du Muséum d'Histoire Naturelle |
| James Sowerby | Tier 2 | English Botany; prolific, institutionally recognized |
| Ferdinand Bauer | Tier 1 | Illustrationes Florae Novae Hollandiae; Kew collections |
| Walter Hood Fitch | Tier 2 | 10,000+ Curtis's Botanical Magazine plates; Kew |

**Commercial case:** Botanical art is the safest expansion — it is already scoreable, has
established commercial precedent (Redouté prints are the platform's flagship example), and
prestige seeding immediately increases scoring fidelity for hundreds of existing BHL assets.

---

### 4. Architectural Drawings

**Constitutional fit: Partial.**

`anchor_type = 'cultural'` is constitutional. The `anchor_weight_spec.cultural` weight set
applies. But two structural scoring gaps exist:

**Gap 1 — No `architecture` prestige domain.** `creator_prestige_registry` defines six domains:
`natural_history`, `cartography`, `fine_art`, `photography`, `printmaking`, `other`. Architects
and architectural illustrators do not fit `fine_art` without editorial reasoning. Forced
classification into `other` is constitutional but requires Principal Architect review at every
proposal (Article 8.1 and PA-8) — operationally unsustainable at scale.

**Gap 2 — Taxon signals are unconditionally zero.** `taxon_commercial_tier` and
`taxon_place_iconic` will be `0.0` for all architectural subjects. The composite score formula
will systematically suppress architectural assets relative to natural history and geographic
assets, regardless of commercial merit. There is no `place_iconic_cultural_registry` equivalent
to provide place-signal lift for architectural subjects. A celebrated Piranesi view of the
Pantheon scores the same as an unidentified building sketch.

**New governance required: Yes.**

Minimum requirements for a constitutional expansion:

| Requirement | Amendment Target |
|---|---|
| Add `architecture` domain to `creator_prestige_registry` | Asset Intelligence Constitution v1.2, Article 7.2 |
| Define `place_iconic_cultural_registry` or declare explicit scoring behavior when taxon signals are absent for cultural-anchor assets | Asset Intelligence Constitution v1.2, new article |
| Specify scoring floor or signal substitution for cultural-only assets | CI Constitution v1.2 or Asset Intelligence v1.2 |

**Pipeline unchanged: No.** After Asset Intelligence v1.2 and new migrations, the scoring worker
requires changes to handle the absence of taxon signals without penalizing commercial quality.

**Commercial case:** Decorative architectural engravings (Piranesi, Palladio, Batty Langley,
Gibbs) have established print-on-demand and museum commercial presence. The commercial case is
real but the governance cost is non-trivial. Architectural expansion is Tier 2.

---

### 5. Posters

**Constitutional fit: Full.**

Article 24 of Asset Intelligence v1.1 explicitly names Posters as a covered asset class with
the lightest prerequisites of any non-default class:

- `anchor_type = 'cultural'` confirmed per opportunity. No prestige prerequisite.
- Product surfaces `retail`, `tourism`, `museum_print` are all applicable.

**New governance required: No.**

**Pipeline unchanged: Yes.** After M-32–M-35.

**Calibration note:** Poster scoring quality is heavily dependent on anchor_type assignment.
WPA National Park posters (Yellowstone, Grand Canyon, Yosemite) are effectively `mixed` or
`geographic` with strong place_iconic alignment — their commercial signals are strong. Generic
decorative retail posters are `cultural` with minimal place or creator lift. Curator anchor_type
assignment is the primary lever for scoring fidelity. This is not a governance gap; it is
expected curatorial work.

**Priority opportunities:** WPA Federal Art Project posters, Yellowstone and Yosemite National
Park promotional posters (LOC Prints & Photographs Division). These have both the place
association and era provenance to score well under the current formula.

**Commercial case:** WPA posters have exceptional retail commercial presence ($200–$2000 per
print at auction). Institutional licensing demand for National Park poster imagery is documented.
The LOC Prints & Photographs Division holds thousands of PD WPA poster originals. This is a
high-return, low-governance expansion.

---

### 6. Books

**Constitutional fit: Partial — depends on scope definition.**

There are two interpretations of "Books" as an asset class:

**Interpretation A — Books as illustration sources (the current model).** Illustrated books
are already the primary source object for Illustration Opportunity extraction. BHL digitizes
illustrated books; the platform extracts individual plate opportunities from them. Under this
interpretation, Books are fully supported and the pipeline is unchanged.

**Interpretation B — Books as commercial objects (facsimile editions, full-volume licensing).**
If the commercial object is the full illustrated book — a facsimile edition, a licensed reprint,
an institutional subscription to complete volumes — no product surface for this exists in the
Product Routing Constitution. No routing rule governs full-book commercial disposition.

**The expansion strategy must declare which interpretation is intended.** The two are not
mutually exclusive but require separate treatment.

**For Interpretation B:**

**New governance required: Yes.**

| Requirement | Amendment Target |
|---|---|
| Define `facsimile_edition` and `institutional_volume_license` product surfaces | Product Routing Constitution v1.2 |
| Define eligibility criteria: minimum quality, era, provenance standards for full-book commercial candidacy | Catalog Constitution v1.2 |
| Define provider routing for print-on-demand facsimile production | Provider Routing Constitution amendment |

**Pipeline unchanged: No.** New product surfaces require routing worker changes.

**Commercial case:** Facsimile editions of landmark illustrated works (Audubon's Birds of
America, Gould folios, Redouté Les Roses) have commercial precedent at institutional and
collector price points. This is a longer-horizon opportunity requiring governance investment.
Near-term, the current plate-extraction model is sufficient.

**Recommendation:** Declare Interpretation A as current scope. Defer Interpretation B governance
to a future milestone after Tier 1 expansion classes are commercially active.

---

### 7. Manuscripts

**Constitutional fit: Partial.**

The constitutional framework can accommodate manuscript content, but three structural issues
produce systematic scoring failure:

**Issue 1 — `image_quality_score` gate.** Manuscript folios — handwritten text, faded ink,
uneven illumination, non-print surface texture — will systematically score below the
`image_quality_score` threshold that currently gates scoring candidacy. The gate was calibrated
for printed plate imagery. A constitutionally compliant manuscript illumination may fail the
quality gate that a mediocre print passes.

**Issue 2 — `format_compliance` gate.** Manuscript folios are non-standard aspect ratios
(vellum dimensions, codex page formats). Format compliance thresholds set for printed book plates
may reject valid manuscript images.

**Issue 3 — `asset_rights` complexity.** Many high-value manuscripts are held by institutions
that assert digitization rights over PD content (the Bridgeman precedent in the US context —
though its applicability to faithful reproductions has been challenged). The `asset_rights`
signal classification (PD/CC0/rights_restricted) for manuscript digitizations may require
institution-specific rights review that the current rights worker cannot automate.

**New governance required: Yes.**

| Requirement | Amendment Target |
|---|---|
| Manuscript-specific `image_quality_score` calibration or override gate | CI Constitution v1.2 |
| `format_compliance` override for known manuscript formats | CI Constitution v1.2 |
| Rights classification guidance for institutionally digitized manuscripts | CI Constitution v1.2 or new Rights Governance Article |

**Pipeline unchanged: No.** Quality and format compliance gates require calibration changes.

**Commercial case:** Illuminated manuscript reproductions are a distinct market segment with
institutional and collector demand. However, the rights complexity and quality gate barriers make
manuscripts the highest-cost Tier 2 expansion. Defer until Tier 1 classes are generating revenue.

---

## Expansion Sequence

### Tier 1 — Activate after M-32–M-35 (no governance amendment required)

| Priority | Asset Class | Unblocked By |
|---|---|---|
| 1A | Botanical Art | Prestige registry seeding (Ehret, Bauer, Fitch, et al.). Scoreable today. |
| 1B | Posters | M-32–M-35 activation + curator anchor_type assignment per opportunity. |
| 1C | Historic Maps | M-32–M-35 activation + 3 cartography prestige entries + 5 place-iconic entries per target place. |
| 1D | Historic Photography | M-32–M-35 activation + 3 photography prestige entries + color_profile calibration review. |

**Recommended first activation order:** Botanical Art → Historic Maps → Historic Photography →
Posters. Botanical Art shares the existing natural history pipeline. Maps and Photography share
the Yellowstone/LOC source already explored. Posters follow with WPA/LOC source.

### Tier 2 — Activate after targeted governance amendments

| Priority | Asset Class | Governance Amendment Required | Estimated Effort |
|---|---|---|---|
| 2A | Architectural Drawings | Asset Intelligence v1.2 (prestige domain + cultural scoring policy) | Moderate — targeted amendment |
| 2B | Books (as product objects) | Product Routing v1.2 + Catalog v1.2 (new product surfaces) | High — new product surface governance |
| 2C | Manuscripts | CI Constitution v1.2 (quality gate calibration + rights guidance) | High — gate calibration + rights review |

---

## Governance Gap Register

| Gap ID | Description | Affects | Required In | Status |
|---|---|---|---|---|
| G-1 | No `architecture` prestige domain | Architectural Drawings | Asset Intelligence v1.2 | Open |
| G-2 | No `place_iconic_cultural_registry` or scoring floor for cultural-only assets without taxon signals | Architectural Drawings | Asset Intelligence v1.2 | Open |
| G-3 (CI) | `taxon_commercial_tier_score` unconditionally zero for geographic-anchor assets in retail(0.25), publishing(0.15), reference(0.20) subscores; 0.088 COS weight suppressed; blocks Tier 1 | Historic Maps | CI Constitution v1.2 — `signal_substitutions` | **Resolved — CI v1.2 ratified** |
| G-3 (Policy) | `color_profile` signal optimized for color plates; disadvantages historic monochrome photography | Historic Photography | Commerce Policy Minor version bump | Open |
| G-4 | No `facsimile_edition` or `institutional_volume_license` product surface | Books (as products) | Product Routing v1.2 | Open |
| G-5 | `image_quality_score` gate not calibrated for manuscript formats | Manuscripts | CI Constitution v1.2 | Open |
| G-6 | `format_compliance` gate not calibrated for manuscript folio dimensions | Manuscripts | CI Constitution v1.2 | Open |
| G-7 | No rights classification guidance for institutionally digitized PD manuscripts | Manuscripts | CI Constitution v1.2 or Rights Governance | Open |

G-3 (CI) — the intra-subscore gap for geographic assets — was identified in `historic_maps_activation_plan_v1.md`
and resolved by CI Constitution v1.2 (Director Decision G-3). With this gap resolved, Historic Maps
is unblocked for Tier 1 access.

G-3 (Policy) is the only remaining gap affecting a Tier 1 asset class. It is a policy version bump, not a
constitutional amendment, and does not block Historic Photography activation — curator_override
handles individual high-value assets until calibration is applied.

G-1 and G-2 are prerequisites for any Architectural Drawings expansion. Both require Asset
Intelligence v1.2.

G-4 through G-7 are prerequisites for Books-as-products and Manuscripts expansion. All are
Tier 2 and do not affect Tier 1.

---

## Next Governance Actions

1. **Immediate — Prestige registry seeding.** Botanical Art is scoreable today. Seed Ehret,
   Bauer, Fitch, Sowerby, Turpin, and two LOC-identified cartographers (Hayden Survey) as
   `proposed` entries in `creator_prestige_registry`. Begin second-human approval cycle.

2. **With M-32–M-35 — Yellowstone seed approval.** The five-entry minimum for Yellowstone in
   `place_iconic_taxa_registry` (Article 13) must be approved (`status = 'active'`) before
   Yellowstone maps and photographs can score with place signal lift.

3. **Asset Intelligence v1.2 scope.** Commission the `architecture` prestige domain amendment
   and cultural scoring policy as a single Article amendment pass. Do not begin Architectural
   Drawings commercial activation until v1.2 is ratified.

4. **Books scope declaration.** Declare in a Principal Architect record whether Books-as-products
   is a current or deferred commercial objective. This resolves the ambiguity before any
   Product Routing Constitution amendment work begins.
