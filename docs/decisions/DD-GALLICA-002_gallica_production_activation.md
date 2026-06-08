# DD-GALLICA-002 — Gallica Production Activation (Institution #6)

| Field | Value |
|---|---|
| **Decision ID** | DD-GALLICA-002 |
| **Type** | Production Activation |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-08 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — production authorization for framework defined in DD-GALLICA-001 |
| **Governing Audit** | DD-GALLICA-001 — BnF Gallica Source Audit and Activation Framework |
| **Governing Documents** | DD-GALLICA-001 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 |

---

## Background

DD-GALLICA-001 completed the source audit and activation framework for BnF Gallica,
establishing: source classification as a Tier 1 Core direct content institution; the
Gallica Rights Addendum v1 as the governing rights instrument; the IIIF 2.1 bridging
specification requirement; the audio/video Phase 3 exclusion; and the Madagascar pilot
scope with a 50-asset cap.

This Decision converts that framework into a production authorization. It designates
Gallica as **Institution #6** in NC's active content portfolio, formally ratifies the
Gallica Rights Addendum v1, authorizes the source registry INSERT, specifies the
governance gate sequence, formalizes the Asset Zero requirements with specific candidates,
and defines the ten pilot success criteria that govern the path to DD-GALLICA-003
(scope expansion).

Nothing in this Decision modifies DD-GALLICA-001's governance framework. This Decision
is the operational companion to that audit.

---

## Findings

**F-1.** All governance instruments required by DD-GALLICA-001 are either ratified or
ready for ratification as part of this Decision. The Gallica Rights Addendum v1 (embedded
in DD-GALLICA-001 Article 2) is hereby formally ratified as a governing document.
Standards Constitution Amendments SA-3 and SA-6 are required before Gate 2 of this
Decision's gate sequence — they are activation conditions, not ratification conditions.

**F-2.** BnF Gallica is the sixth content institution to enter active NC pipeline
authorization, after BHL, Europeana, Library of Congress, Rijksmuseum, and DPLA.
Gallica's activation closes NC's most significant priority illustrator gap (Redouté,
Buffon primary institutional holdings) and initiates the Africa geographic coverage
track (Madagascar pilot).

**F-3.** The Madagascar pilot is the correct scope for initial activation. Madagascar
simultaneously tests: the Gallica Rights Addendum v1 text-path classification
(French "domaine public" declarations on Buffon-era material); the IIIF 2.1 → 3.0
bridging adapter in production; OAI-PMH bulk metadata harvest; and the commercial
viability of Francophone colonial-era natural history illustration as an NC product
category. No other single query scope exercises all four simultaneously.

**F-4.** Asset Zero candidates are identifiable from three source publications with
strong Gallica coverage and confirmed pre-1800 publication dates: Buffon's "Histoire
Naturelle" (1749–1804), Sonnerat's "Voyage aux Indes orientales et à la Chine" (1782),
and Audebert and Vieillot's "Oiseaux Dorés" (1802, marginally inside the pre-1800
preference but acceptable given exceptional quality). The Buffon lemur plates are
preferred as they are the most commercially compelling and the most clearly governed
by the BnF Tier 1 PD authority designation.

**F-5.** No blocking technical prerequisites exist that preclude ratification. The
source registry INSERT may be executed immediately after ratification. The IIIF bridging
adapter and OAI-PMH worker implementation are Gate 3 items — they must be complete
before the first ingestion run, not before ratification.

---

## Decision

### Article 1 — Institution #6 Designation and Production Authorization

**(a)** BnF Gallica is formally designated as **Institution #6** in NC's active content
institution portfolio. This designation is effective upon ratification of this Decision.

**(b)** BnF Gallica is authorized as a production source for Phase 1 content acquisition
(image, map, photography, illustration). This authorization is scoped to the Madagascar
pilot defined in Article 8. Production ingestion beyond the Madagascar pilot requires
DD-GALLICA-003.

**(c)** The Institution #6 designation places Gallica in the following portfolio context:

| # | Institution | Source Role | Activation Status |
|---|---|---|---|
| 1 | BHL | Direct | Active (seeded) |
| 2 | Europeana | Aggregator | DD-EUR-001 pending ratification |
| 3 | Library of Congress | Direct | DD-LOC-001 pending |
| 4 | Rijksmuseum | Direct | DD-RIJKSMUSEUM-001 pending ratification |
| 5 | DPLA | Aggregator | DD-DPLA-001 pending ratification |
| **6** | **BnF Gallica** | **Direct** | **DD-GALLICA-002 (this Decision)** |

**(d)** The `sources.governance_state = 'active'` designation for `source_id = 'bnf_gallica'`
is hereby authorized. It is first applied by the INSERT in Article 5.

---

### Article 2 — Gallica Rights Addendum v1 Ratification

The Gallica Rights Addendum v1, defined in DD-GALLICA-001 Article 2 (Tables GA-1A,
GA-1B, GA-2, and Article 2.3 priority rules), is hereby formally ratified as a governing
document. It supplements the Europeana Rights Matrix v1.0 for all Gallica-sourced assets
and covers the following governance territory not addressed by the Matrix:

- French and English text-form rights declarations ("domaine public", "libre de
  réutilisation", "usage non-commercial uniquement", and all variants)
- "Domaine public revisité" as a REVIEW REQUIRED designation requiring Article 14 /
  Bridgeman assessment (HR-GA-3)
- BnF metadata CC-BY rights separation from image rights
- The three-layer rights determination priority sequence (IIIF `license` URI →
  `dc:rights` URI → `dc:rights` text)
- BnF Tier 1 PD Authority designation conditions (DD-GALLICA-001 Article 3.3)

The Gallica Rights Addendum v1 is immutable by Director Decision alone. Amending it
requires: (i) a new version of the Addendum, (ii) a constitutional amendment process,
(iii) Director Decision ratifying the new version.

---

### Article 3 — EU Directive 2019/790 Article 14 and Bridgeman Doctrine Confirmation

NC's reliance on EU Directive 2019/790 Article 14 (France transposed 2023) and on
*Bridgeman Art Library v. Corel Corp* (SDNY 1999) as negative rights clearance
instruments for Gallica reproductions of 2D PD works, as defined in DD-GALLICA-001
Articles 3.1 and 3.2, is hereby confirmed operative. These instruments are not
Director-level instruments — they are constitutional doctrine governing NC's commerce
rights framework for all Gallica ingestion. They may not be modified or suspended by
Director Decision.

---

### Article 4 — IIIF Bridging Specification

The IIIF 2.1 → 3.0 bridging adapter for Gallica must implement the following field
transformations before any IIIF 3.0 manifest may be generated from a Gallica source:

| IIIF 2.1 source | IIIF 3.0 target | Transformation |
|---|---|---|
| `@context: ".../presentation/2/context.json"` | `@context: ".../presentation/3/context.json"` | Replace URL |
| `license` (manifest-level string) | `rights` (string URI) | Rename field |
| `@id` (all objects) | `id` | Remove `@` prefix |
| `@type: "sc:Manifest"` | `type: "Manifest"` | Strip `sc:`, remove `@` |
| `@type: "sc:Canvas"` | `type: "Canvas"` | Strip `sc:`, remove `@` |
| `sequences[0].canvases` (array) | `items` (array of Canvas) | Structural lift |
| `resources[].resource` | `items[].items[].body` | Annotation body restructure |
| `thumbnail` (single object) | `thumbnail` (array of objects) | Wrap in array |
| `service[@id]` | `service[id]` | Rename in service object |
| `metadata` (key-value array) | `metadata` (label-value array) | Preserve; re-key |

The adapter must additionally inject NC IIIF Commerce Extension v1.0 properties
(`nc:activation_target_id`, `nc:csm_tier`, `nc:shop_url`, `nc:product_count`) per
Standards Constitution v1.0 Article 19.

The adapter specification must be documented as a governed artifact at
`docs/standards/gallica_iiif_bridge_v1.md` before Gate 3 is closed.

---

### Article 5 — Source Registry Authorization

BnF Gallica is not currently registered in the `sources` table. This Decision authorizes
a single **INSERT** creating `source_id = 'bnf_gallica'`. The exact INSERT statement is
specified in the Ratification Package Section 4. The governing parameters are:

| Parameter | Value | Authority |
|---|---|---|
| `source_id` | `'bnf_gallica'` | This Article |
| `governance_state` | `'active'` | Article 1(d) |
| `auth_type` | `'none'` | DD-GALLICA-001 Article 6 — no API key required |
| `rights_strategy` | `'gallica_rights_addendum_v1'` | Article 2 |
| `source_role` | `'direct_institution'` | DD-GALLICA-001 Article 1 |
| `phase_1_only` | `true` | DD-GALLICA-001 Article 5(a) |
| `rate_limit` | `≤ 2 req/s` | DD-GALLICA-001 Article 12.10 |
| `iiif_version` | `'2.1'` | DD-GALLICA-001 F-13 |
| `iiif_bridging_required` | `true` | Article 4 |
| `eu_article_14_reliance` | `true` | Article 3 |
| `bridgeman_doctrine_reliance` | `true` | Article 3 |

No changes to this record may be made after INSERT without a new Director Decision.

---

### Article 6 — Governance Gate Sequence

Production ingestion is gated by the following sequence. No gate may be skipped.
Proceeding past a gate without completing all gate requirements is a constitutional
violation.

```
GATE 0 — RATIFICATION
  [ ] DD-GALLICA-001 ratified (Director + second-human approval)
  [ ] DD-GALLICA-002 ratified (Director + second-human approval)
  → Opens: Gate 1

GATE 1 — STANDARDS CONSTITUTION AMENDMENTS
  [ ] SA-3 ratified: BnF Gallica API Profile registered in Standards Constitution v1.1
      (OAI-PMH DC mapping, IIIF 2.1 bridging spec, ARK scheme, Gallica Rights Addendum v1)
  [ ] SA-6 ratified: UNIMARC registered as Acknowledged Standard in Standards Constitution v1.1
  [ ] SA-4 confirmed: IIIF Presentation API amendment — either ratified as SA-4 independently
      or incorporated into SA-3
  → Opens: Gate 2

GATE 2 — SOURCE REGISTRY
  [ ] Pre-INSERT verification: SELECT COUNT(*) FROM sources WHERE source_id = 'bnf_gallica' = 0
  [ ] INSERT executed (Ratification Package Section 4 SQL) as single transaction
  [ ] Post-INSERT 13-point verification: all checks return true
  [ ] governance_state = 'active' confirmed
  → Opens: Gate 3

GATE 3 — INFRASTRUCTURE
  [ ] IIIF 2.1 → 3.0 bridging adapter implemented and documented
      (docs/standards/gallica_iiif_bridge_v1.md)
  [ ] OAI-PMH ingestion worker deployed: Gallica Rights Addendum v1 text-path logic
      (Tables GA-1A, GA-1B, GA-2 from DD-GALLICA-001 Article 2.2)
  [ ] Rights determination priority sequence implemented
      (IIIF license URI → dc:rights URI → dc:rights text)
  [ ] Rate limiting confirmed: ≤ 2 req/s against Gallica production endpoints
  [ ] Human reviewer designated for Gallica rights review
      (must be French-language capable for text-path review)
  [ ] FM exclusion confirmed in writing for Gallica pipeline
  → Opens: Gate 4

GATE 4 — ASSET ZERO
  [ ] Asset Zero candidate identified (Buffon / Sonnerat preferred per Article 7)
  [ ] ARK identifier captured and documented
  [ ] Rights classified via text-path: "domaine public" + pub date ≤ 1800 confirmed
  [ ] IIIF full-resolution delivery confirmed (watermark-free, ≥ 400px)
  [ ] IIIF 2.1 → 3.0 bridge produces valid IIIF 3.0 manifest
  [ ] Asset Zero reaches activation_target status with second-human approval
  [ ] Asset Zero ARK recorded in activation log
  → Opens: Gate 5

GATE 5 — PILOT AUTHORIZATION
  [ ] Gates 0–4 all closed
  [ ] Director formally authorizes pilot start
  [ ] Pilot start date recorded
  [ ] Pilot end date computed (90 days from start) and recorded
  → Pilot batch initiated (Madagascar SRU query, 50-asset cap)

GATE 6 — PILOT COMPLETION
  [ ] 50-asset cap reached OR 90-day window expired
  [ ] SC-1 through SC-10 evaluated (Ratification Package Section 7)
  [ ] Principal Architect recommendation for DD-GALLICA-003 (or remediation)
  [ ] Director pilot review sign-off
  → Opens: DD-GALLICA-003 decision process (or remediation + re-evaluation)

GATE 7 — FULL PRODUCTION (requires DD-GALLICA-003)
  Not within scope of this Decision.
```

---

### Article 7 — Asset Zero Specification

The Asset Zero candidate must satisfy all of the following requirements. The operational
checklist for Asset Zero validation is in
`docs/implementation/gallica_asset_zero_checklist_v1.md`.

**(a) Source publications (in priority order):**

| Priority | Publication | Author | Date | Madagascar relevance |
|---|---|---|---|---|
| 1 | *Histoire Naturelle, générale et particulière* | Buffon (Georges-Louis Leclerc) | 1749–1804 | Lemurs, fossas, Madagascar mammals — Volumes 12–13 Suppléments |
| 2 | *Voyage aux Indes orientales et à la Chine* | Pierre Sonnerat | 1782 | Madagascar birds, mammals, landscapes |
| 3 | *Histoire Naturelle des Mammifères* | Saint-Hilaire & Cuvier | 1819–1842 | Later; acceptable if pre-1828 volume confirmed |
| 4 | *Oiseaux Dorés ou à Reflets Métalliques* | Audebert & Vieillot | 1802 | Madagascar endemic birds; marginally post-1800 but commercially exceptional |

**(b) Subject requirement:** An endemic Madagascar species — ring-tailed lemur
(*Lemur catta*, "maki"), ruffed lemur (*Varecia variegata*, "maki vari"), aye-aye
(*Daubentonia madagascariensis*), fossa (*Cryptoprocta ferox*), or equivalent
unambiguously Madagascar-endemic subject. Generic animals with non-Madagascar range
do not qualify as Asset Zero for the Madagascar pilot.

**(c) Rights profile requirement:**
- `dc:rights` text must match "domaine public" pattern (Table GA-1A, row 1 or 2) OR
  IIIF `license` field must contain PDM URI
- No "domaine public revisité" designation (that would require HR-GA-3 review — not
  suitable for Asset Zero which must produce a clean pipeline validation)
- Publication date must be ≤ 1804 (Buffon) or ≤ 1782 (Sonnerat), confirmed from
  `dc:date` or work description

**(d) IIIF delivery requirement:**
- IIIF Image API `/full/full/0/native.jpg` returns HTTP 200
- Image dimensions: shortest side ≥ 400px (recommended: ≥ 2000px for MASTERWORK tier)
- Image is watermark-free at full resolution
- IIIF 2.1 → 3.0 bridging adapter produces valid manifest

**(e) Commerce tier expectation:** A pre-1800 hand-colored Buffon plate of an endemic
Madagascar lemur species, from the primary institutional collection of one of the world's
great national libraries, should score at the **MASTERWORK** CSM tier. If the Asset Zero
candidate scores FLAGSHIP or lower, the scoring formula must be reviewed before the
pilot proceeds — this is a calibration check, not a blocking criterion.

---

### Article 8 — Pilot Authorization

**(a)** The pilot is authorized for **Madagascar** (`places.geonames_id = 1062947`,
Wikidata Q1019) at a **50-asset cap** over a **90-day pilot window**, as specified in
DD-GALLICA-001 Article 9.

**(b)** The pilot is authorized to begin after Gate 4 (Asset Zero) is closed and
Gate 5 (Pilot Authorization) is opened. It is not authorized to begin before Gate 4.

**(c)** The specific SRU queries, sub-cap rules, place association requirements,
rights path breakdown, and BLOCKED rejection logging requirements are as defined in
DD-GALLICA-001 Article 9(a) through 9(e). Those provisions are operative.

**(d)** Pilot window record:

| Event | Date |
|---|---|
| Gate 5 opened (pilot authorized) | — |
| Pilot start (first batch) | — |
| Pilot end (90 days from start, or cap reached) | — |
| Pilot review due (14 days after pilot end) | — |

---

### Article 9 — Pilot Success Criteria

The pilot is evaluated at the conclusion of the 90-day window or when 50 assets have
been processed — whichever comes first. All ten criteria must be evaluated.
Success on SC-1 through SC-10 triggers the DD-GALLICA-003 decision process.

| # | Criterion | Threshold | Constitutional? |
|---|---|---|---|
| SC-1 | Activated assets | ≥ 7 reach `activation_target` with second-human approval | No |
| SC-2 | Rights verification completeness | 100% of `activation_eligible` assets have documented `media_rights.rights_evidence` | No |
| SC-3 | BLOCKED filter accuracy | Zero BLOCKED assets in `source_record` for `bnf_gallica` | **Yes — suspend** |
| SC-4 | Place association | 100% activated assets associated with Madagascar (geonames 1062947) | No |
| SC-5 | FM exclusion | Zero FM output connected to any rights determination | **Yes — suspend** |
| SC-6 | Commerce coverage | 100% activated assets have COS + CSM tier in `asset_opportunities` | No |
| SC-7 | Rights Addendum text-path accuracy | Zero text-path misclassifications (no wrong ALLOWED/BLOCKED determinations) | No |
| SC-8 | IIIF 3.0 manifest validity | 100% of ingested assets produce valid IIIF 3.0 manifests via bridging adapter | No |
| SC-9 | Constitutional integrity | Zero `preservation_event.event_outcome = 'violation'` for `bnf_gallica` assets | No |
| SC-10 | Pipeline completion rate | ≥ 75% of ingested assets complete all pre-activation gates without worker error | No |

**SC-3 and SC-5 are constitutional.** Failure on either suspends the pilot immediately,
before any other criteria are evaluated. All other criteria are performance criteria.

**SC-7 note (text-path accuracy).** This criterion is Gallica-specific. The Gallica
Rights Addendum v1 text-path classification must produce zero misclassifications. A
"misclassification" is defined as: (i) a BLOCKED asset reaching `source_record` via
incorrect text-path ALLOWED classification, or (ii) an ALLOWED asset being incorrectly
BLOCKED by the text-path filter. Human reviewer override of an automatic classification
is not a misclassification — it is the review process working correctly.

**SC-8 note (IIIF bridging).** Every asset with a Gallica IIIF manifest must produce
a bridged IIIF 3.0 manifest that validates against the IIIF Presentation API 3.0
specification. Assets without a IIIF manifest (single-image items using Image API only)
do not count against SC-8 — they are exempt from the manifest validity check.

---

### Article 10 — Explicit Exclusions

This Decision does not authorize:

**(a)** Any ingestion of assets with BLOCKED rights classifications (all InC variants,
NoC-NC, CC BY-ND, all NC variants, CNE, UND, "usage non-commercial", "droits réservés",
"tous droits réservés").

**(b)** Ingestion from SRU queries outside the Madagascar scope. Non-Madagascar
assets returned by the query must be discarded at ingestion.

**(c)** Audio or film ingestion. Phase 3 media types remain excluded per DD-GALLICA-001
Article 5. This exclusion cannot be lifted by Director Decision.

**(d)** Use of Gallica Bulk Export, BnF catalogue JSON API, BnF UNIMARC direct, or any
API surface other than OAI-PMH, SRU, and IIIF (Image + Presentation APIs).

**(e)** Ingestion of any Gallica asset bearing "domaine public revisité" text designation
without completion of the HR-GA-3 Article 14 / Bridgeman assessment. "Domaine public
revisité" assets may not be automatically classified as ALLOWED — they must enter the
REVIEW REQUIRED queue per Table GA-1B.

**(f)** Generating IIIF 3.0 manifests from assets that have not passed the IIIF 2.1 →
3.0 bridging adapter. Manifests produced directly from the raw 2.1 manifest structure
without bridging are not valid under NC's IIIF governance.

**(g)** Any increase to the 50-asset pilot cap without DD-GALLICA-003.

---

### Article 11 — Standards Constitution Amendments Confirmation

The following amendments are required as Gate 1 conditions. They do not require
ratification before this Decision is ratified — they are activation conditions, not
ratification conditions.

| Amendment | Content | Gate |
|---|---|---|
| SA-3 | BnF Gallica API Profile: OAI-PMH DC mapping, IIIF 2.1 bridging spec, ARK identifier scheme, Gallica Rights Addendum v1 registration | Gate 1 |
| SA-6 | UNIMARC as Acknowledged Standard (Map via OAI-PMH DC export; not adopted internally) | Gate 1 |
| SA-4 | IIIF Presentation API amendment — may be incorporated into SA-3 | Gate 1 |

Both SA-3 and SA-6 must be ratified as a Standards Constitution v1.1 before Gate 2
(source registry INSERT) proceeds. SA-3 without SA-6 does not close Gate 1.

---

### Article 12 — Subsequent Decisions

| ID | Trigger | Scope |
|---|---|---|
| **Standards Constitution v1.1** | Gate 1 prerequisite | SA-3 + SA-6 (+ SA-4 if applicable) |
| **DD-GALLICA-003** | Pilot success (SC-1 through SC-10 met) | Scope expansion beyond Madagascar; pilot cap removal; Buffon full collection harvest; Redouté botanical pilot |
| **DD-GALLICA-004** | Phase 3 constitutional gate satisfied (distant) | Phonorecord rights framework under MMA; early film assessment |
| **DD-GALLICA-005** | BnF UNIMARC direct path evaluation | Richer metadata via UNIMARC rather than OAI-PMH DC export |

DD-GALLICA-003 is not automatically triggered by pilot success. It requires Director
review, Principal Architect recommendation, and a new Decision document. Key inputs to
DD-GALLICA-003 will be: SC-7 text-path accuracy results (calibrating the Gallica Rights
Addendum v1 in production), SC-8 IIIF bridging performance (determining whether the
adapter is reliable at scale), and the commercial quality distribution of activated assets
(COS scores and CSM tier breakdown).

---

## Ratification

This Decision requires:

1. **Director signature** — opengracelabs (the Director)
2. **Second-human approval** — a second person with authority over NC governance decisions

| Role | Name | Date |
|---|---|---|
| Director | — | — |
| Second Human Approver | — | — |

---

*DD-GALLICA-002 Draft — 2026-06-08*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
