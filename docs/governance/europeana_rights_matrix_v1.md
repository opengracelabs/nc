# Europeana Rights Matrix v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |
| Authority | Strategic Directive · MSC v1.2 · Standards Constitution v1.0 · Commerce Intelligence Constitution v1.2 |

---

## Governing Principle

NC's Illustration Opportunity Doctrine imposes a single hard gate: **Public Domain or CC0 only. No exceptions.**

This gate applies to all four NC use contexts. NC is not an educational exemption platform, a
research library, or a tourism bureau. NC is a commerce platform. Every image NC publishes
— whether on a place page, in a story, or as an activated product — reflects NC's
commercial identity. No use context relaxes the PD gate until the Illustration Opportunity
Doctrine is amended by constitutional process.

All four use cases (Commerce, Education, Tourism, Research) share the same rights floor.
The classification column in the tables below applies uniformly across all four.

---

## Part I — Allowed Rights Table

Assets bearing any of the following rights statements may proceed through the NC
ingestion pipeline. Human review is required before any terminal `media_rights.rights_status`
value is set. Commerce is permitted after activation approval.

---

### Table 1A — ALLOWED (Unconditional After Human Review)

| # | Rights Statement | URI | `rights_status` Target | Use Contexts |
|---|---|---|---|---|
| 1 | **CC0 1.0 Universal** | `http://creativecommons.org/publicdomain/zero/1.0/` | `verified_cc0` | Commerce · Education · Tourism · Research |
| 2 | **Public Domain Mark 1.0** | `http://creativecommons.org/publicdomain/mark/1.0/` | `verified_pd` | Commerce · Education · Tourism · Research |
| 3 | **No Copyright — United States** | `http://rightsstatements.org/vocab/NoC-US/1.0/` | `verified_pd` | Commerce · Education · Tourism · Research |

**Notes:**

- **CC0** — Creator has permanently waived all copyright and neighboring rights worldwide.
  Governed under MSC v1.2 Article 29.3(b) (Smithsonian CC0 verification protocol).
  Equivalent to PD for NC commerce.

- **PDM** — Institutional declaration that the work is free of known copyright restrictions.
  Not a rights waiver by the creator — an institutional determination by the applying institution.
  Eligibility depends on the applying institution's authority. The Rijksmuseum is a recognized
  PDM authority (confirmed in NC Europeana API validation). Trust registry open question: see OQ-3.

- **NoC-US** — Work is in the public domain under US copyright law. Co-governed by LOC and the
  Rights Statements Working Group. Governing rights statement for US-published pre-1928 works
  and life+70 determinations. Constitutionally mandated under MSC v1.2 Article 29.1(b).

---

### Table 1B — CONDITIONALLY ALLOWED (REVIEW REQUIRED → May Resolve ALLOWED)

These statements are not blocked. They are held pending human investigation. If the human
reviewer determines that no restriction bars NC commerce, the asset advances to ALLOWED.
If the investigation cannot confirm PD status or cannot dismiss the restriction, the asset
is rejected.

| # | Rights Statement | URI | `rights_status` if Resolved | Trigger |
|---|---|---|---|---|
| 4 | **No Copyright — Contractual Restrictions** | `http://rightsstatements.org/vocab/NoC-CR/1.0/` | `verified_pd` (if restriction does not cover NC commerce) | Contractual restriction on PD work |
| 5 | **No Copyright — Other Known Legal Restriction** | `http://rightsstatements.org/vocab/NoC-OKLR/1.0/` | `verified_pd` (if restriction not applicable in NC's jurisdiction) | Non-copyright legal restriction on PD work |
| 6 | **No Known Copyright** | `http://rightsstatements.org/vocab/NKC/1.0/` | `verified_pd` (if independent PD analysis confirms) | No rights holder identified; PD not formally declared |

These three are REVIEW REQUIRED — not ALLOWED. They may never be treated as ALLOWED
without a completed human review that independently confirms eligibility. See Part III.

---

## Part II — Blocked Rights Table

Assets bearing any of the following rights statements are blocked from NC ingestion
for commerce purposes. The pre-ingestion filter (Rule RM-1) must reject them before
any `source_record` is created. No human review, Director Decision, or constitutional
amendment to this matrix alone can lift a BLOCKED classification. Lifting a BLOCKED
classification requires both a doctrine amendment (permitting non-PD works) AND a new
version of this matrix.

---

### Table 2A — In Copyright (InC) — All Variants BLOCKED

These statements assert active copyright. The NC hard gate is absolute.

| Rights Statement | URI | Block Reason |
|---|---|---|
| **In Copyright** | `http://rightsstatements.org/vocab/InC/1.0/` | Active copyright. No PD determination possible. |
| **In Copyright — EU Orphan Works** | `http://rightsstatements.org/vocab/InC-OW-EU/1.0/` | In copyright under EU Orphan Works Directive. Rights owner unknown ≠ no rights. |
| **In Copyright — Educational Use Permitted** | `http://rightsstatements.org/vocab/InC-EDU/1.0/` | Educational exception does not grant commercial rights. NC is a commerce platform. |
| **In Copyright — Non-Commercial Use Permitted** | `http://rightsstatements.org/vocab/InC-NC/1.0/` | Explicit commercial use restriction. Hard gate. |
| **In Copyright — Rights-Holder(s) Unlocatable or Unidentifiable** | `http://rightsstatements.org/vocab/InC-RUU/1.0/` | In copyright; rights holder unlocatable, not absent. Cannot use commercially. |

---

### Table 2B — No Copyright with Non-Commercial Restriction — BLOCKED

| Rights Statement | URI | Block Reason |
|---|---|---|
| **No Copyright — Non-Commercial Use Only** | `http://rightsstatements.org/vocab/NoC-NC/1.0/` | Institution has imposed non-commercial restriction on PD work. NC is explicitly excluded regardless of underlying PD status. |

---

### Table 2C — Rights Status Unknown — BLOCKED

These statements indicate the provider either did not evaluate rights or was unable to
determine them. NC cannot proceed to commerce without a rights determination.

| Rights Statement | URI | Block Reason |
|---|---|---|
| **Copyright Not Evaluated** | `http://rightsstatements.org/vocab/CNE/1.0/` | No rights evaluation performed by provider. NC cannot ingest without evaluation. |
| **Copyright Undetermined** | `http://rightsstatements.org/vocab/UND/1.0/` | Provider investigated; rights status inconclusive. NC cannot proceed commercially on an undetermined status. |

---

### Table 2D — Creative Commons — NoDerivatives Variants — BLOCKED

NC's print product workflow requires derivative transformations: image sizing, cropping,
margin adjustment, product composition. NoDerivatives prohibits these transformations.
BLOCKED unconditionally.

| Rights Statement | URI | Block Reason |
|---|---|---|
| **CC BY-ND 4.0** | `http://creativecommons.org/licenses/by-nd/4.0/` | No-derivatives clause. NC product workflow requires derivative transformations. |
| **CC BY-ND 3.0** | `http://creativecommons.org/licenses/by-nd/3.0/` | Same. |
| **CC BY-ND 2.0** | `http://creativecommons.org/licenses/by-nd/2.0/` | Same. |
| **CC BY-ND 1.0** | `http://creativecommons.org/licenses/by-nd/1.0/` | Same. |

---

### Table 2E — Creative Commons — All NonCommercial Variants — BLOCKED

NonCommercial restrictions are directly incompatible with NC's commerce mission. No
doctrine amendment, Director Decision, or per-item review can lift NC blocks. The NC
in the rights statement and the NC in Nature & Culture describe the same incompatibility.

| Rights Statement | URI |
|---|---|
| **CC BY-NC 4.0** | `http://creativecommons.org/licenses/by-nc/4.0/` |
| **CC BY-NC 3.0** | `http://creativecommons.org/licenses/by-nc/3.0/` |
| **CC BY-NC 2.0** | `http://creativecommons.org/licenses/by-nc/2.0/` |
| **CC BY-NC 1.0** | `http://creativecommons.org/licenses/by-nc/1.0/` |
| **CC BY-NC-SA 4.0** | `http://creativecommons.org/licenses/by-nc-sa/4.0/` |
| **CC BY-NC-SA 3.0** | `http://creativecommons.org/licenses/by-nc-sa/3.0/` |
| **CC BY-NC-SA 2.0** | `http://creativecommons.org/licenses/by-nc-sa/2.0/` |
| **CC BY-NC-SA 1.0** | `http://creativecommons.org/licenses/by-nc-sa/1.0/` |
| **CC BY-NC-ND 4.0** | `http://creativecommons.org/licenses/by-nc-nd/4.0/` |
| **CC BY-NC-ND 3.0** | `http://creativecommons.org/licenses/by-nc-nd/3.0/` |
| **CC BY-NC-ND 2.0** | `http://creativecommons.org/licenses/by-nc-nd/2.0/` |
| **CC BY-NC-ND 1.0** | `http://creativecommons.org/licenses/by-nc-nd/1.0/` |

---

### Table 2F — Creative Commons — Attribution and ShareAlike — BLOCKED (Pending Doctrine Amendment)

CC BY and CC BY-SA licenses retain copyright. NC's Illustration Opportunity Doctrine
requires PD or CC0. CC BY works are commercially usable under the license terms, but
they are not public domain. NC's hard gate is not "commercially usable" — it is "public
domain or CC0."

These statements are classified BLOCKED until the Illustration Opportunity Doctrine is
amended to permit licensed (non-PD) content in NC commerce. A doctrine amendment would
require: (1) Illustration Opportunity Doctrine revision, (2) new version of this matrix,
(3) Director Decision.

Per-item human review does not resolve this block. See Rule HR-3 (Part III).

| Rights Statement | URI | Block Reason |
|---|---|---|
| **CC BY 4.0** | `http://creativecommons.org/licenses/by/4.0/` | Copyright reserved. Not PD. Doctrine amendment required. |
| **CC BY 3.0** | `http://creativecommons.org/licenses/by/3.0/` | Same. |
| **CC BY 2.0** | `http://creativecommons.org/licenses/by/2.0/` | Same. |
| **CC BY 1.0** | `http://creativecommons.org/licenses/by/1.0/` | Same. |
| **CC BY-SA 4.0** | `http://creativecommons.org/licenses/by-sa/4.0/` | Copyright reserved. ShareAlike clause would bind NC products. Doctrine amendment required. |
| **CC BY-SA 3.0** | `http://creativecommons.org/licenses/by-sa/3.0/` | Same. |
| **CC BY-SA 2.0** | `http://creativecommons.org/licenses/by-sa/2.0/` | Same. |
| **CC BY-SA 1.0** | `http://creativecommons.org/licenses/by-sa/1.0/` | Same. |

---

### Table 2G — Legacy Europeana Statements — BLOCKED

| Rights Statement | URI | Block Reason |
|---|---|---|
| **Europeana Out of Copyright — Non-Commercial** | `http://www.europeana.eu/rights/out-of-copyright-non-commercial/` | Deprecated. Non-commercial restriction. Equivalent to modern NoC-NC. |
| **Europeana Orphan Work (EU)** | `http://www.europeana.eu/rights/orphan-work-eu/` | Deprecated. Equivalent to modern InC-OW-EU. In copyright. |

---

### Table 2H — Missing, Malformed, or Unrecognized URI — BLOCKED

| Condition | Block Reason |
|---|---|
| `edm:rights` absent from EDM payload | No rights determination possible. Warning preservation event required (MSC v1.2 Article 29.2c). |
| URI present but not from `rightsstatements.org` or `creativecommons.org` | Standards Constitution v1.0 Invariant S-4: only governed vocabulary URIs permitted. |
| URI present but malformed (not a valid URI) | Treat as absent. |

---

## Part III — Human Review Rules

These rules govern the REVIEW REQUIRED workflow (Table 1B). They do not apply to ALLOWED
statements (which require only human confirmation, not investigation) or to BLOCKED
statements (which require no human review).

---

### Rule HR-1 — Workflow Item Creation

A `workflow_item` must be created before any investigation begins. The item must contain:

```
item_type:        'rights_review'
item_payload:
  europeana_record_id:   <Europeana object identifier>
  edm_rights_uri:        <exact URI from edm:rights field>
  matrix_classification: 'review_required'
  matrix_rule:           <HR-2a | HR-2b | HR-2c>
  raw_edm_payload:       <full EDM object as received from API>
status:           'pending'
assigned_to:      NULL
```

The asset's `media_rights.rights_status` must remain `'pending_verification'` until
the `workflow_item` is resolved. No downstream processing — activation, scoring, or
product creation — may begin while the item is open.

---

### Rule HR-2 — Investigation Requirements by Statement

**HR-2a — NoC-CR (Contractual Restrictions)**

The human reviewer must:

1. Identify the specific contractual restriction. This requires contacting the Europeana
   data provider directly or reviewing the provider's stated terms.
2. Determine whether the restriction covers NC's commerce use case (print-on-demand,
   digital download, framed prints for resale).
3. Determine whether the restriction has a jurisdiction scope that covers NC's primary
   market (United States).
4. Determine whether the restriction has an expiry date.

Resolution criteria:
- If the restriction does not cover NC commerce → resolve ALLOWED, set `verified_pd`
- If the restriction covers NC commerce → reject, set `rights_status = 'ineligible'`
- If the restriction cannot be identified → reject, set `rights_status = 'ineligible'`

Required evidence in `media_rights.rights_evidence`:
```json
{
  "contractual_restriction_assessed": true,
  "restriction_identified": true,
  "restriction_scope": "<description of restriction>",
  "covers_nc_commerce": false,
  "assessment_notes": "<reviewer rationale>",
  "reviewer_id": "<human identity>",
  "assessed_at": "<ISO 8601 timestamp>"
}
```

**HR-2b — NoC-OKLR (Other Known Legal Restriction)**

The human reviewer must:

1. Identify the specific legal restriction. Common types: cultural patrimony law,
   export control, indigenous cultural property protocol, data protection law, moral
   rights doctrine in a specific jurisdiction.
2. Determine whether the restriction applies in the US (NC's primary commerce jurisdiction).
3. Determine whether the restriction covers commercial reproduction as NC performs it.

Resolution criteria:
- If the restriction has no US applicability and no claim over NC commerce → resolve ALLOWED
- If the restriction applies or cannot be dismissed → reject

Required evidence in `media_rights.rights_evidence`:
```json
{
  "legal_restriction_assessed": true,
  "restriction_type": "<name of restriction, e.g. 'Maori cultural property protocol'>",
  "jurisdiction_applicability": "<assessment>",
  "covers_nc_commerce": false,
  "assessment_notes": "<reviewer rationale>",
  "reviewer_id": "<human identity>",
  "assessed_at": "<ISO 8601 timestamp>"
}
```

**HR-2c — NKC (No Known Copyright)**

The human reviewer must conduct an independent PD analysis. The provider's investigation
is noted but not relied upon — NC requires its own determination.

The independent analysis must address:
1. Publication date: when was the work first published?
2. US publication status: was the work published in the United States, or published abroad
   without compliance with US formalities (pre-Berne)?
3. Author life dates: if not a work-for-hire, when did the author die?
4. Jurisdiction rules: apply US copyright law for NC commerce eligibility.
5. Renewal records (for works published 1923–1963 in the US): did copyright registration lapse?

Standard PD determination rules:
- Published in the US before 1928 → PD under US law
- Published outside the US before 1909 → likely PD in US (Berne retroactivity limitations)
- Author died before 1956 and work published before death → likely PD under life+70

Resolution criteria:
- If PD analysis confirms public domain status → resolve ALLOWED, set `verified_pd`
- If analysis is inconclusive → reject, set `rights_status = 'ineligible'`
- The `pending_verification` status may not persist indefinitely. A NKC workflow item
  unresolved after 30 days must be closed as rejected, not left open.

Required evidence in `media_rights.rights_evidence`:
```json
{
  "pd_analysis_completed": true,
  "pd_basis": "<'us_publication_before_1928' | 'life_plus_70_confirmed' | 'foreign_pre_berne'>",
  "publication_year": <year or null>,
  "author_death_year": <year or null>,
  "jurisdiction": "us",
  "analysis_notes": "<methodology and sources consulted>",
  "reviewer_id": "<human identity>",
  "assessed_at": "<ISO 8601 timestamp>"
}
```

---

### Rule HR-3 — CC BY and CC BY-SA: No Per-Item Resolution

CC BY and CC BY-SA assets classified under Table 2F are BLOCKED at the ingestion filter
(Rule RM-1) and must not enter the `workflow_item` review queue. They are not REVIEW
REQUIRED — they are BLOCKED pending a doctrine amendment.

If a CC BY or CC BY-SA asset has been incorrectly placed in the review queue, the
workflow item must be closed with:

```
status: 'rejected'
rejection_reason: 'doctrine_amendment_required'
rejection_notes: 'CC BY assets are blocked under current Illustration Opportunity Doctrine.
                  Resolution requires doctrine amendment, not per-item review. See
                  Europeana Rights Matrix v1 OQ-1.'
```

The accumulation of CC BY and CC BY-SA rejections is the evidence base for the OQ-1
doctrine amendment decision. Do not resolve these per-item.

---

### Rule HR-4 — Evidence Requirements for ALLOWED Statements (Confirmation, Not Investigation)

ALLOWED statements do not require investigation — they require confirmation. The human
reviewer must confirm the following before setting any terminal `rights_status`:

| Statement | Confirmation Required | Evidence in `rights_evidence` |
|---|---|---|
| **CC0** | (i) CC0 waiver issued by rights holder or institutional program; (ii) specific asset within declared CC0 scope; (iii) institutional CC0 declaration URL available | `cc0_declaration_url`: URL of institutional CC0 statement |
| **PDM** | (i) Applying institution is a recognized NC source with documented PD determination process; (ii) specific item falls within institution's stated PD scope | `pd_determination_url`: URL of institution's PD scope documentation; `applying_institution`: institution name |
| **NoC-US** | (i) US publication confirmed; (ii) Publication date or author death dates confirm PD under US law | `pd_basis`: `"us_publication_before_1928"` or `"life_plus_70_confirmed"`; `publication_year` if determinable |

A `verified_pd` or `verified_cc0` record that lacks the required evidence field is a
constitutional violation under MSC v1.2 Article 29.2(b).

---

### Rule HR-5 — Audit Trail

Every rights determination — ALLOWED, rejected, or open — must produce an append-only
`preservation_event`:

```
event_type:    'rights_verification'
event_outcome: 'success'   -- for ALLOWED terminal status
               'warning'   -- for REVIEW REQUIRED items opened
               'failure'   -- for BLOCKED pre-ingestion rejections
event_detail:  <matrix rule applied, edm:rights URI evaluated, reviewer identity>
performed_by:  <human reviewer ID (ALLOWED/REVIEW) or ingestion worker ID (BLOCKED)>
```

If a rights determination is reversed on review, a new event must be written. The original
event must not be modified. The audit log is immutable.

---

### Rule HR-6 — FM Exclusion (Permanent)

Foundation Model output may not influence any rights determination at any stage. This rule
is inherited from FM Constitution v1.0 Invariant FM-4 and is permanent. It cannot be
relaxed by this matrix, by Director Decision, or by constitutional amendment.

The `rights_analysis_advisory` FM use case (FM Constitution v1.0, Article 14.5) produces
output stored in `fm_candidate_record` only. It does not connect to the `workflow_item`
rights review queue. It does not connect to `media_rights`. FM advisory rights analysis
is informational for human reference only — it is not a step in the rights determination
process.

---

## Part IV — Use-Case Eligibility Summary

NC's four use contexts (Commerce, Education, Tourism, Research) all operate under the
same PD hard gate. There is no educational exception, fair use exception, or research
exemption in NC's current constitutional framework. NC is a commerce platform. All
published assets — whether displayed in a story, on a place page, or as an activated
product — reflect NC's commercial identity and are governed by the same rights standard.

| Rights Statement | Commerce | Education | Tourism | Research | Notes |
|---|---|---|---|---|---|
| CC0 | Yes | Yes | Yes | Yes | All use contexts unrestricted |
| PDM | Yes | Yes | Yes | Yes | All use contexts unrestricted |
| NoC-US | Yes | Yes | Yes | Yes | All use contexts unrestricted |
| NoC-CR (resolved) | Yes | Yes | Yes | Yes | After human review dismisses restriction |
| NoC-OKLR (resolved) | Yes | Yes | Yes | Yes | After human review dismisses restriction |
| NKC (resolved) | Yes | Yes | Yes | Yes | After independent PD analysis confirms |
| CC BY | No | No | No | No | Blocked; doctrine amendment required |
| CC BY-SA | No | No | No | No | Blocked; doctrine amendment required |
| CC BY-ND | No | No | No | No | Derivative restriction — permanent block |
| All CC NC | No | No | No | No | Commercial restriction — permanent block |
| All InC | No | No | No | No | Active copyright — permanent block |
| CNE / UND | No | No | No | No | Rights not determined — permanent block |

**Open Question OQ-5 (new):** If NC develops a non-commerce editorial layer (free discovery
pages, educational institution partnerships, research APIs), should that layer have a
separate rights tier permitting CC BY display for informational use without product
activation? This question cannot be resolved within the Europeana Rights Matrix. It
requires a Strategic Directive amendment defining whether NC has a non-commerce publishing
mode.

---

## Part V — Pipeline Implementation Rules

### RM-1 — Pre-Ingestion Filter (Blocking)

Before creating any `source_record` for a Europeana asset, the ingestion worker must:
1. Extract `edm:rights` from the EDM payload.
2. Classify the URI against Parts I and II of this matrix.
3. If BLOCKED: log the rejection with the URI and applicable table; do not create
   `source_record`, `media_file`, or `media_rights`. Stop.
4. If REVIEW REQUIRED: create `source_record` and `media_rights` with
   `rights_status = 'pending_verification'`; open `workflow_item` per HR-1. Stop.
5. If ALLOWED: create `source_record` and `media_rights` with
   `rights_status = 'pending_verification'`; open confirmation checklist per HR-4.
   Do not set terminal status until human confirmation is recorded.

The pre-ingestion filter is not advisory. It is blocking. No other pipeline step may
begin before it completes.

### RM-2 — Terminal Status Values

| Determination | `media_rights.rights_status` | Permitted next state |
|---|---|---|
| ALLOWED (CC0, confirmed) | `verified_cc0` | Eligible for activation |
| ALLOWED (PD, confirmed) | `verified_pd` | Eligible for activation |
| BLOCKED (pre-ingestion) | Not set — no `media_rights` record created | None |
| REVIEW REQUIRED (open) | `pending_verification` | Blocked until workflow item resolved |
| REVIEW REQUIRED (rejected) | `ineligible` | No further processing |
| REVIEW REQUIRED (resolved ALLOWED) | `verified_pd` | Eligible for activation |

### RM-3 — Europeana EDM Minimum Fields Warning

Per MSC v1.2 Article 29.2(c): a `source_record` with `schema_standard = 'edm'` missing
any of `dc:title`, `dc:description`, `dc:date`, `edm:rights` must receive a
`preservation_event` of type `rights_verification` with outcome `warning` before rights
verification begins. This event must be visible to the human reviewer.

---

## Part VI — Invariants

**RM-I-1 — Hard Gate.** BLOCKED classifications (Tables 2A–2H) cannot be overridden
by human review, Director Decision, or this matrix's amendment alone. Lifting a BLOCKED
classification requires both an Illustration Opportunity Doctrine amendment and a new
version of this matrix issued after that amendment.

**RM-I-2 — FM Exclusion (Permanent).** FM Constitutional Invariant FM-4 applies to all
rights determinations without exception and cannot be relaxed by any version of this matrix.

**RM-I-3 — Pre-Ingestion Primacy.** The pre-ingestion filter (RM-1) runs before any
other pipeline step. It is not advisory.

**RM-I-4 — Audit Immutability.** Rights verification preservation events are append-only.
A reversal must produce a new event, not modify the original.

**RM-I-5 — URI Vocabulary Lock.** Only URIs from `http://rightsstatements.org/` and
`http://creativecommons.org/` are valid `media_rights.rights_statement_uri` values.
All other URIs are BLOCKED per Standards Constitution v1.0 Invariant S-4.

---

## Part VII — Open Questions

**OQ-1 — CC BY Doctrine Amendment.** Should NC amend the Illustration Opportunity
Doctrine to permit CC BY-licensed assets in commerce? CC BY is commercially usable,
derivative-compatible, and present in many high-quality institutional photography
collections. The counter-argument: NC's positioning as a pure public domain platform
is a trust signal. Resolution requires Director Decision + Illustration Opportunity
Doctrine amendment + new matrix version.

**OQ-2 — NoC-CR Volume.** If NoC-CR review volume exceeds operational capacity, a
blanket BLOCKED policy for NoC-CR may be preferable to an open queue. Revisit at
first production Europeana ingestion run.

**OQ-3 — PDM Institutional Trust Registry.** Should NC maintain a list of institutions
whose PDM determinations NC accepts without independent review? Candidate: Rijksmuseum
(confirmed in API validation). Without a registry, every PDM asset requires independent
human verification. Revisit at first production ingestion run.

**OQ-4 — Life+70 vs. Life+50 Jurisdiction Ambiguity.** NC's position: apply US copyright
law for commerce eligibility. This should be constitutionalized in a future MSC amendment
to prevent interpretive drift.

**OQ-5 — Non-Commerce Editorial Layer.** If NC develops editorial content without product
activation (free discovery, educational partnerships, research APIs), should that layer
have a separate rights tier permitting CC BY for informational display? Cannot be resolved
within this matrix. Requires Strategic Directive amendment.

---

*Europeana Rights Matrix v1.0.0 — ratified 2026-06-07*
*Authority: Strategic Directive · MSC v1.2 · Standards Constitution v1.0 · CI Constitution v1.2*
*Next version trigger: Illustration Opportunity Doctrine amendment permitting licensed content, or new rights vocabulary in Europeana ecosystem*
