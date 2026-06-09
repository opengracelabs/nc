# DD-GALLICA-003 — Gallica Commercial Reuse Disqualification

| Field | Value |
|---|---|
| **Decision ID** | DD-GALLICA-003 |
| **Type** | Source Disqualification |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | DD-GALLICA-002 (production authorization withdrawn) |
| **Governing Documents** | DD-GALLICA-001 · DD-GALLICA-002 · Strategic Directive v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · MSC v1.2 |
| **Effective date** | Date of ratification |

---

## Background

DD-GALLICA-001 classified BnF Gallica as a Tier 1 Core direct content institution and
established the Gallica Rights Addendum v1 as the governing rights instrument.
DD-GALLICA-002 authorized Gallica as Institution #6 and authorized the Madagascar pilot.
Both decisions remain in Draft — Pending Ratification status.

Following a review of BnF's published Conditions of Use, the following clause was
identified as directly incompatible with NC's commercial production model:

> **"Commercial re-use of digitized documents is subject to a license fee."**
> — BnF Conditions générales d'utilisation (Gallica)

This clause applies at the platform level, governing the terms under which BnF's
digitizations may be commercially reused, regardless of the public domain status of
the underlying work or the presence of a CC0 or PDM designation on individual records.
It was not addressed in DD-GALLICA-001 or DD-GALLICA-002, which focused on copyright
and reproduction rights doctrine (EU Article 14, Bridgeman) rather than contractual
platform terms of service.

This Decision resolves the conflict and withdraws the production authorization issued
in DD-GALLICA-002 before any production ingestion has occurred.

---

## Findings

### F-1 — BnF Platform Terms Impose a Commercial License Fee

BnF's Conditions of Use state, without qualification, that commercial re-use of
digitized documents hosted on Gallica is subject to a license fee. This is a
contractual term governing access to BnF's digital platform, not an assertion of
copyright in the underlying works. It operates independently of:

- The public domain status of the underlying work
- The presence of a CC0 or PDM designation on individual records
- EU Directive 2019/790 Article 14 (which removes reproduction rights claims over
  faithful PD reproductions but does not override platform contractual terms)
- The Bridgeman doctrine (which addresses copyright, not ToS obligations)

The license fee requirement is a platform access condition that persists even where
BnF has no enforceable copyright in the underlying or digitized work.

### F-2 — NC Is a Commercial Operator

NC is a commercial platform. Its primary product is commerce-enabling access to
public domain illustrations for use in physical and digital products. Every asset
NC ingests from Gallica and surfaces in its product pipeline constitutes "commercial
re-use of digitized documents" within the meaning of BnF's platform terms.

The commercial pipeline is not incidental to NC's operation — it is NC's purpose.
NC cannot operate in a "research-only" posture toward Gallica while simultaneously
surfacing Gallica-sourced assets in commercial product flows.

### F-3 — EU Article 14 and Bridgeman Do Not Resolve This Conflict

DD-GALLICA-001 Article 3 and DD-GALLICA-002 Article 3 established EU Directive
2019/790 Article 14 and *Bridgeman Art Library v. Corel Corp* as negative rights
clearance instruments — i.e., instruments establishing that BnF cannot assert
copyright in faithful 2D PD reproductions.

These instruments address IPR: they defeat copyright claims. They do not address
contractual ToS obligations. A platform may impose fee requirements on commercial
reuse of its content through contractual terms that are entirely separate from
copyright law. BnF's license fee requirement is such a term. Article 14 and
Bridgeman clear the IPR dimension; they leave the contractual dimension intact.

The rights governance framework in DD-GALLICA-001 is therefore incomplete as a
basis for commercial production sourcing. It correctly analyzed the copyright
landscape but did not reach the ToS layer.

### F-4 — CC0 Items Do Not Escape the Conflict

A CC0 designation is a copyright waiver. It is issued under Creative Commons CC0 1.0
Universal and operates in the domain of intellectual property rights. It waives all
copyright and related rights to the fullest extent permitted by law.

BnF's license fee condition is a contractual platform term, not a rights assertion.
When BnF designates a digitization CC0, it waives its reproduction rights; it does
not thereby waive its ability to impose contractual access conditions on its platform.
The license fee requirement may therefore apply to CC0-designated items as a platform
term that coexists with the CC0 copyright waiver.

This creates an irresolvable conflict for NC: even CC0 items from Gallica may carry
a contractual commercial reuse fee requirement that NC cannot simply override by
reference to the CC0 license.

### F-5 — No Production Ingestion Has Yet Occurred

DD-GALLICA-001 and DD-GALLICA-002 are both in Draft — Pending Ratification status.
No production ingestion of Gallica content has occurred. No Gallica records appear
in the M36 substrate. The Gallica adapter code exists (`workers/gallica_adapter/`)
but has not been run against the production database in an activated state.

This Decision therefore operates as a pre-activation withdrawal, not a retroactive
remediation. No records need to be purged. No `governance_state` transition has
taken effect in the sources table.

### F-6 — Research and Internal Discovery Remain Permissible

BnF's license fee condition applies to "commercial re-use." Internal research,
source evaluation, pipeline testing, and non-commercial discovery workflows do not
constitute commercial re-use and are not subject to the fee. The Gallica adapter
code, fixture files, and test suite may be retained for these purposes.

---

## Source Policy Analysis

The governing NC production-source requirement, per the Strategic Directive and
Commercial Directive, is:

> **Production sources must permit commercial reuse without licence fees.**

This requirement is not waivable by Director Decision alone. It is foundational to
NC's commercial model: every asset in the commerce pipeline must be licensable to
end customers without an upstream fee obligation that would make NC's margin
calculations undefined or negative.

BnF's condition — "commercial re-use of digitized documents is subject to a license
fee" — directly and completely fails this requirement. There is no reading of BnF's
platform terms under which commercial reuse of Gallica digitizations is fee-free.

The conflict is:

| Requirement | BnF Position | Compatible? |
|---|---|---|
| Commercial reuse permitted | Subject to license fee | **NO** |
| No upstream licence fees | Fee required for commercial use | **NO** |
| No per-asset licensing obligation | Platform-level commercial fee | **NO** |
| Rights certainty for commerce | ToS creates open-ended obligation | **NO** |

There is no partial compliance path. BnF's condition does not distinguish between
asset classes, rights status, or volume. Every commercial reuse is subject to the
fee. NC cannot ingest Gallica content into its commerce pipeline under these terms
without either (a) entering a commercial licence agreement with BnF, or (b)
operating in breach of BnF's platform terms.

Option (a) is outside the scope of NC's current operational model and would require
a separate commercial negotiation, legal review, and governance instrument. Option
(b) is not permissible under NC's governance framework.

---

## Decision

### Article 1 — Withdrawal of Production Authorization

**1.1** The production authorization issued in DD-GALLICA-002 Article 1 is hereby
withdrawn in its entirety. BnF Gallica is removed from NC's approved production
source list.

**1.2** The Institution #6 designation issued in DD-GALLICA-002 Article 1(a) is
hereby rescinded. Institution #6 is unassigned pending a qualified replacement.

**1.3** The authorization to INSERT `source_id = 'bnf_gallica'` with
`governance_state = 'active'` issued in DD-GALLICA-002 Article 1(d) is withdrawn.
If any such INSERT has been executed, it must be reversed: `governance_state` must be
set to `'deprecated'` and the record flagged with `deprecation_reason = 'DD-GALLICA-003'`.

**1.4** DD-GALLICA-002 is superseded by this Decision in full. DD-GALLICA-001 is
superseded in part: its source classification, rights addendum, and technical
findings are retained as research instruments; its activation framework conclusions
and source registry authorization are withdrawn.

### Article 2 — Source Status: Deprecated — Research Only

**2.1** BnF Gallica is reclassified from `governance_state = 'active'` (authorized
in DD-GALLICA-002) to `governance_state = 'deprecated'`.

**2.2** Permitted uses under deprecated status:
- Internal research and source evaluation
- Pipeline testing with dry-run enabled (`gallica_dry_run = True`)
- Academic or non-commercial discovery workflows
- Adapter code maintenance for research purposes

**2.3** Prohibited uses under deprecated status:
- Production ingestion into the M36 substrate
- Surfacing Gallica-sourced assets in NC commerce product flows
- Deactivating `gallica_dry_run = True` in any environment connected to production
- Issuing a DD-GALLICA-004 that reinstates production authorization without a
  resolved commercial licence agreement with BnF (see Article 4)

**2.4** The prohibition on production ingestion is permanent unless reversed by a
ratified DD-GALLICA-004 that satisfies the conditions in Article 4. It may not be
suspended by Director Decision alone.

### Article 3 — Adapter Code and Test Fixtures

**3.1** `workers/gallica_adapter/` is retained in the repository. It is not deleted.
It serves as a research and dry-run tool.

**3.2** `gallica_dry_run = True` must be enforced as the permanent default in
`workers/gallica_adapter/config.py`. Any commit that sets `gallica_dry_run = False`
as default is a CI violation and must not be merged.

**3.3** Tests, fixtures, decision documents, and curated data related to Gallica
are retained unchanged. They represent validated research output and are not affected
by this disqualification.

**3.4** The Gallica Rights Addendum v1 (DD-GALLICA-001 Article 2) is retained as a
research instrument. It correctly describes the rights landscape for Gallica items.
It is no longer operative as a production classification instrument.

### Article 4 — Path to Reinstatement

Reinstatement of Gallica as a production source requires all of the following:

**4.1 Commercial licence agreement.** A formal written licence agreement with BnF
that explicitly permits NC's commercial reuse of Gallica digitizations without
per-asset or per-use fees. The agreement must be reviewed by qualified legal counsel
and ratified as a governance instrument.

**4.2 Revised source policy instrument.** A new DD-GALLICA-004 (Gallica Production
Reinstatement) that: references the executed licence agreement; amends the Gallica
Rights Addendum v1 to incorporate the licence terms; and re-establishes the
production activation gates from DD-GALLICA-002.

**4.3 Two-human ratification.** DD-GALLICA-004 requires Director sign-off and
second-human approval, both of whom must review the licence agreement before signing.

**4.4 Revised institution number.** Institution #6 has been unassigned. If Gallica
is reinstated, it receives the next available institution number at the time of
DD-GALLICA-004 ratification.

### Article 5 — Impact on Downstream Governance

**5.1** The Institution Coverage Audit v1.0 listed BnF/Gallica as a Must Add
institution. This classification remains factually correct — Gallica holds
irreplaceable natural history illustration content. The disqualification is a
commercial terms conflict, not a content quality or rights status finding. The
Must Add rating is retained pending resolution of the commercial terms conflict.

**5.2** NC's French and Francophone world geographic gaps identified in the
Institution Coverage Audit v1.0 are not resolved by this Decision. They require
an alternative sourcing strategy. Candidates to evaluate: Musée d'Orsay (already
partially covered via Paris Musées pipeline), other BnF-adjacent institutions with
cleaner commercial terms, or direct BnF licence negotiation.

**5.3** Priority illustrator coverage gaps created by this disqualification:
- Redouté (primary holdings at BnF) — no current NC source
- Buffon's Histoire Naturelle plates — no current NC source at this volume
- Audebert and Vieillot — no current NC source

These gaps must be tracked in the Institution Coverage Audit and addressed in
subsequent source discovery decisions.

**5.4** The Gallica adapter (Sprint 1–3, ratified as ingestion-ready in commit
`c225a2f`) is not deleted. Its Sprint compliance audit history is valid research
output. If DD-GALLICA-004 reinstates production authorization, the adapter may
be re-qualified without re-running full Sprint 1–3 compliance audits, subject to
review of any API or rights changes since original qualification.

---

## Consequences Summary

| Item | Before this Decision | After ratification |
|---|---|---|
| Production authorization | Pending (DD-GALLICA-002 draft) | **Withdrawn** |
| Institution #6 | Assigned to Gallica (draft) | **Unassigned** |
| `governance_state` | `'active'` (authorized, not yet inserted) | **`'deprecated'`** |
| `gallica_dry_run` | Default True | **Permanently True (production prohibition)** |
| Gallica Rights Addendum v1 | Production governing instrument | **Research instrument only** |
| Adapter code | Ingestion-ready | **Retained, research/dry-run only** |
| Path to reinstatement | N/A | **Requires BnF licence + DD-GALLICA-004** |
| Priority illustrator gap | Addressed (Redouté, Buffon) | **Gap reopened — unaddressed** |
| French geographic coverage | Partially addressed | **Gap reopened** |

---

## Ratification

This Decision is in Draft status. Both parties must review the Findings (specifically
F-1 through F-4) and Article 2 (prohibited uses) before signing. This Decision has
material consequences for NC's institution portfolio and geographic coverage strategy
and must not be ratified without explicit review of the commercial licence path
(Article 4).

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
