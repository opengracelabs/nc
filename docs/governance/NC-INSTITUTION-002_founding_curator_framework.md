# NC-INSTITUTION-002: Founding Curator Framework

| Field | Value |
|---|---|
| Document | NC-INSTITUTION-002 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-STANDARDS-001 · NC-INSTITUTION-001 · NC-TRUST-001 |
| Scope | Designs the curator, editor, governance, disclosure, and accountability model for NC. Establishes the Founding Curator designation. Resolves the anonymous desk blocker identified in NC-STANDARDS-001. |

---

## Why This Document Exists

NC-STANDARDS-001 identified one non-technical action that blocks more than any other:

> *"Name a curator. It unblocks NC-COAS, NC-PDPS Link 6, and the editorial credibility
> layer across all standards. It is not a development task. It is a decision."*

The current `trustCurators` array has three entries — Institutional Editorial Board,
Heritage Places Desk, Expedition & Ecology Desk — none of which are people. The
infrastructure for curators exists. The pages are live. The data model is defined.
What is absent is a named individual whose professional identity is publicly staked
on the collection decisions.

This document defines the model that resolves that absence — for one person at
founding, and for the team that grows from that one person.

---

## Reference Model Principles

Four institutions. One governing principle from each.

**Smithsonian: The curator's reputation is the institution's reputation.**
Smithsonian curators are publicly identified by name. When the Smithsonian acquires
a work, a named curator's statement appears in the announcement. When the collection
is criticised, that curator answers. The institutional authority of a Smithsonian
collection is inseparable from the professional identity of the person who built it.
A collection without a named curator is an inventory, not an institution.

**Rijksmuseum: Named decisions are trusted decisions.**
When Wim Pijbes made the Rijksmuseum's CC0 release in 2011, he said so in his own
name. Not "the Rijksmuseum has decided" — but "I have decided, and here is why." That
personal act of accountability is what made the decision credible and quotable. The
Rijksmuseum's authority on collection questions flows through its named directors and
curators. Anonymous institutional pronouncements are less trusted than named ones.

**Getty: The program director is accountable for the program.**
Getty's Open Content Program has a named program director. Getty's provenance research
has named researchers. The ULAN is maintained by a named team. When Getty makes a
provenance determination or rights classification, there is a named professional whose
peer reputation is attached to that determination. This is the mechanism by which
Getty's standards are taken seriously by the scholarly community.

**National Geographic: The named expert makes the claim credible.**
NatGeo consults named scientists and names them in stories. "According to Dr. Jane
Smith, biologist at the University of X" carries weight that "according to experts"
does not. The named expert is a trust transfer mechanism — their institutional
credibility flows into NatGeo's editorial credibility. NC's named illustrator
authority (Owen Jones, David Roberts, Edward Wilson) serves the same function on the
content side, but the curatorial claim — *we verified this illustration, we confirmed
this provenance, we made this selection* — needs a named human to carry it.

---

## Role Definitions

NC's trust architecture requires four distinct roles. At founding, one person may hold
all four. The roles are defined separately because the accountability structures are
different, the public disclosures are different, and the succession requirements are
different.

---

### Role 1: Founding Curator

**What it is:**
A permanent designation, not a job title. The Founding Curator is the named individual
who established NC's collection standards, selected the founding collections, and is
publicly accountable for the institutional decisions made during the founding period.
This designation persists in NC's public record regardless of whether the person later
delegates day-to-day curatorial responsibilities.

The Getty comparison: the name J. Paul Getty is on the institution permanently because
Getty built it. The NC Founding Curator's name is on the institution's founding
narrative permanently because they built it.

**Public accountability:**
- Named on NC's institutional history page
- Named as the signatory on the founding governance documents (PD Provenance Standard,
  Certificate Standard, Edition Standard)
- Named in the first annual institutional disclosure report
- Named in the founding curatorial statement on the collections page

**What the Founding Curator signs:**
- The first institutional disclosure: *"I, [Name], as Founding Curator of Nature &
  Culture, confirm that the following collections have been selected according to the
  NC Public Domain Provenance Standard..."*
- The permanence commitment: *"I, [Name], commit that..."*
- The founding narrative on `/about/founding`

**Criteria for the designation:**
The Founding Curator is the person who:
1. Made the collection selection decisions for the founding collections
2. Verified the rights basis for each founding product
3. Established the institutional standards (the governance documents)
4. Is publicly contactable as an accountable individual

This is not a qualification bar — it is a description of who did the work. The
founder is the Founding Curator. If the work was done by one person, that person
holds the designation regardless of formal credentials. The credential is the work,
made visible.

---

### Role 2: Collection Curator

**What it is:**
The ongoing operational role. The Collection Curator is responsible for a defined set
of collections: selecting which illustrations belong, verifying provenance, confirming
rights basis, writing or approving curatorial statements, and signing certificates.

**One curator per collection cluster.** At founding, one person holds all clusters.
As NC grows, collections are delegated: Islamic sphere to one curator, natural history
to another, East Asia to a third. The model scales without restructuring.

**What a Collection Curator does:**
- Selects illustrations for the collection (applies NC-PDPS selection criteria)
- Verifies provenance chain (all 6 NC-PDPS links) before Gate CP
- Confirms rights basis at statutory level (not just "public domain")
- Writes or approves the curatorial statement on the collection page
- Signs the curator field on every certificate issued for their collections
- Is listed as the authority reviewer on collections they did not personally curate
  (second-person verification requirement from NC-TRUST-002)
- Holds the published curator profile at `/curators/[slug]`

**Public disclosures:**
- Curator profile page: name, title, credentials (2–3 sentences), collections curated
- Curatorial statement per collection (signed, dated)
- ORCID ID where available
- A professional contact route (institutional email)

**What Collection Curators do not do:**
They do not write the editorial copy (that is the Editor's role). They do not set
institutional policy (that is the Director's role). They do not handle commerce
operations. The role is: content authority for a defined collection cluster.

---

### Role 3: Collection Editor

**What it is:**
The person accountable for the words on NC's editorial pages. Not the curator's
assistant — a distinct professional role. The Editor writes collection introductions,
place descriptions, illustrator biographies, and expedition narratives. The Editor is
accountable for factual accuracy, register, and sourcing.

The NatGeo distinction: NatGeo separates the scientist (the named expert consulted)
from the journalist (the named writer). The scientist is not the journalist. The
Collection Curator is NC's named expert; the Collection Editor is NC's named journalist.

At founding, one person holds both roles. The distinction matters when the roles
separate: the editor who writes the Alhambra copy is accountable for the claim that
Owen Jones made 102 architectural drawings in 1834. The curator who selects those
drawings is accountable for the provenance determination. These are different claims
requiring different expertise.

**What a Collection Editor does:**
- Writes collection introduction copy (long-form editorial, 300–600 words)
- Writes place descriptions
- Writes illustrator biographies
- Writes expedition narratives
- Cites sources for all historical claims
- Routes factual questions to the Collection Curator for verification
- Signs bylines on all authored content
- Manages the corrections inbox for their authored content

**Public disclosures:**
- Byline on all editorial content: "[Author name], [Title] · Published [date]"
- Editor profile page: name, title, subject areas, bio (100 words)
- Corrections policy: personal accountability for corrections to their content

**What Collection Editors do not do:**
They do not make provenance decisions. They do not sign certificates. They do not
make institutional commitments. They report editorial claims; they do not certify
rights status.

---

### Role 4: Institutional Director

**What it is:**
The public face of NC as an institution. The Director is accountable for everything
the institution commits to: the permanence guarantee, the annual disclosure, the
institutional relationships with source institutions, and the governance standards.

The Rijksmuseum Director comparison: Wim Pijbes was accountable for the CC0 policy.
The NC Director is accountable for the NC Standards Suite, the institutional
notifications to source institutions, and the public-facing institutional commitments.

At founding, the Founding Curator is also the Director. These roles separate when the
institution grows: the Director becomes the institutional accountability role; the
Founding Curator becomes the permanent designation on the founding record.

**What the Institutional Director does:**
- Signs the annual institutional disclosure report
- Signs institutional notifications to source institutions
- Signs the permanence commitment
- Is the named contact for institutional-level challenges (rights disputes, scholarly
  corrections to the standards themselves)
- Publishes the founding narrative
- Is publicly named with a contact route

**Public disclosures:**
- Named on the About page as Institutional Director
- Named as signatory on the annual disclosure report
- Named as the institutional contact on the standards pages
- Contact email published (not personal email — institutional)

---

## The Minimum Viable Founding Configuration

**One person. Four roles. Fully compliant.**

At founding, one person holds all four roles simultaneously. This is not a
compromise — it is a legitimate founding configuration. What matters is that the
person is named, their roles are disclosed, and their accountability is specific.

**The minimum viable public presence for the founding configuration:**

```
About page — Founding statement:
  "Nature & Culture was founded by [Name] in [year]. [Name] serves as Founding
  Curator, Collection Curator, Collection Editor, and Institutional Director.
  This reflects the scale of the founding team. The role structure is designed
  to separate as the institution grows."

Curators page — One profile:
  Name: [Name]
  Title: Founding Curator
  Credentials: [2–3 sentences: relevant background — does not require a PhD.
               Relevant background means: knowledge of the subject material,
               familiarity with PD rights, commitment to the provenance standard]
  Collections: [all founding collections]
  ORCID: [if available]
  Contact: [institutional email]

Curatorial statement per collection:
  "Curated by [Name], Founding Curator, Nature & Culture. [2 sentences specific
  to this collection: why these illustrations, what makes them significant.
  Written in first person. Dated.]"
```

This is the minimum. It is not elaborate. One page, one profile, six sentences per
collection, one email address. It resolves the anonymous desk problem completely and
unblocks every standard simultaneously.

---

## Public Disclosure Requirements

What must be publicly visible, attributed to a named person, before NC can claim
institutional credibility.

### Tier 1 — Before any product goes on sale

| Disclosure | Page | Who signs it |
|---|---|---|
| Founding curator identity | `/about` or `/curators` | Founding Curator |
| Curator profile (name, title, credentials, collections) | `/curators/[slug]` | Self |
| Curatorial statement per collection | Collection page | Collection Curator |
| Certificate curator field | Every certificate | Collection Curator |
| Institutional contact email | `/about` | Institutional Director |

### Tier 2 — Before public launch

| Disclosure | Page | Who signs it |
|---|---|---|
| Founding narrative | `/about/founding` | Institutional Director |
| Editorial bylines on all copy | Collection pages | Collection Editor |
| Corrections policy | `/editorial/corrections` | Collection Editor |
| Permanence commitment | `/certificate`, `/registry` | Institutional Director |
| Institutional notification status | `/about/open-content` | Institutional Director |

### Tier 3 — Within 90 days of first public sale

| Disclosure | Page | Who signs it |
|---|---|---|
| First annual disclosure report | `/institutions/disclosure` | Institutional Director |
| WCAG accessibility statement | `/accessibility` | Institutional Director |
| PD explainer | `/about/public-domain` | Institutional Director or Editor |

### Permanent ongoing disclosures

| Disclosure | Frequency | Who signs it |
|---|---|---|
| Annual institutional disclosure report | Annual | Institutional Director |
| Version history on governance documents | On each change | Named editor of document |
| Corrections acknowledgment | Within 5 days of report | Collection Editor |
| Edition closure notices | When each CE closes | Collection Curator |

---

## Accountability Model

**Five accountability mechanisms. Each answers a different question.**

### 1. Provenance Accountability

*Question: Who verified that this work is what NC says it is?*

The Collection Curator is accountable for every provenance determination. Their name
is in the NC-PDPS Link 6 (`curator_name`) for every product. If a provenance
determination is challenged, the Collection Curator is the named respondent.

Challenge process:
- Challenge submitted to: [institutional email], subject line "Provenance challenge: [certificate_id]"
- Collection Curator acknowledges within 5 business days
- Resolution within 30 days (confirm, correct, or escalate to an independent reviewer)
- Correction published in provenance record version history with challenger acknowledged
  (if consented)

### 2. Editorial Accountability

*Question: Who made this claim about this work, this place, or this illustrator?*

The Collection Editor is accountable for every editorial claim. Their byline is on
every piece of content they authored. If a claim is challenged, the Editor is the
named respondent.

Corrections process:
- Correction submitted to: [institutional email], subject line "Correction: [page URL]"
- Collection Editor acknowledges within 5 business days
- Verified corrections applied within 10 days
- Correction noted in page version history with date and reporter (if consented)
- Material corrections noted visibly at top of content: "Correction [date]: [brief description]"

### 3. Commerce Accountability

*Question: Is this edition what NC says it is? Is the rights basis what NC claims?*

The Institutional Director is accountable for the edition architecture and rights
basis. The permanence commitment (edition records transferred to Internet Archive if
NC ceases operation) is signed by the Director.

Commerce challenges:
- Disputed edition claim: Director responds within 5 business days
- Rights dispute: Director acknowledges; if unresolved, external rights review
  commissioned within 30 days
- Product quality complaint: Director routes to print studio; resolution within 14 days

### 4. Institutional Accountability

*Question: Did NC actually notify these institutions? Are the rights bases real?*

The annual institutional disclosure report, signed by the Director, is the
accountability mechanism. It documents every institution, notification status, and
rights basis. It is publicly verifiable — anyone can check whether a notification was
sent by contacting the named institution.

External institutional challenges:
- If a source institution challenges NC's use of their content: Director responds
  within 5 business days; full review within 30 days; public update to disclosure
  report within 60 days

### 5. Standards Accountability

*Question: Does NC actually conform to its own published standards?*

NC-INSTITUTION-001 identified the gap between NC's internal governance (rigorous)
and its public disclosure (minimal). The founding curator framework closes this gap
by making conformance verifiable: anyone can check whether the named curator's ORCID
exists, whether the provenance chain is complete, whether the certificate verification
endpoint works, whether the annual disclosure has been published.

Self-audit commitment: NC publishes an annual conformance review against the NC
Trust Maturity Model (NC-TRUST-002) within 90 days of each anniversary. The review
is authored and signed by the Institutional Director. Findings — including
non-conformances — are disclosed.

---

## Succession and Scaling Model

**What happens when the team grows.**

### Adding a second curator

When a second Collection Curator joins:
1. The Founding Curator delegates specific collection clusters to the new curator
2. The new curator's profile is added to `/curators/[slug]`
3. Collections are reassigned in trust.ts: `collections[]` array updated
4. Certificate records for new products in those collections carry the new curator's
   name and ORCID
5. Existing products retain the original curator attribution (provenance records are
   permanent; curator attribution does not change retroactively)

The Founding Curator designation remains on all founding-period collections
permanently — it is a historical record, not a current assignment.

### Separating the Editor role

When the first dedicated editor joins:
1. The editor writes new collection copy; the founder's editorial work is versioned
   ("Updated [date] by [New Editor]")
2. Bylines on existing content are updated where the content is substantively revised;
   otherwise they remain attributed to the original author with version history
3. The new editor holds the corrections inbox for their own authored content

### Separating the Director role

When the founding curator delegates the Director role:
1. The annual disclosure is signed by the new Director
2. The institutional contact email is updated
3. The Founding Curator is named on the institutional history page as the founding
   Director and Founding Curator
4. New Director's name appears on all Tier 2 and Tier 3 disclosures going forward

---

## Implementation

What changes in the codebase and on the site to move from the current state to the
minimum viable founding configuration.

### Step 1: Update trust.ts — Replace desks with a named person

In `apps/web/lib/trust.ts`, the `trustCurators` array currently has three anonymous
desks. Replace with one or more named individuals.

**Minimum change (one person, all collections):**

```typescript
export const trustCurators: TrustCurator[] = [
  {
    slug: "[your-slug]",
    name: "[Your Name]",
    title: "Founding Curator",
    summary:
      "[2 sentences: relevant background and what you curate at NC]",
    profile:
      "[3–4 sentences: your approach to collection selection, provenance, and the
       public domain. First person. This is not a CV — it is a statement of
       curatorial approach.]",
    collections: [
      "earthrise", "alhambra", "south-georgia",
      "versailles", "chichen-itza", "petra"
    ],
    byline: "Curated by [Your Name], Founding Curator"
  }
];
```

Add `orcid: string | null` and `contact: string` to the `TrustCurator` type.

### Step 2: Update collection pages — Replace desk bylines

Each collection page currently shows a byline from the desk. Replace with the named
individual's byline. In `collectionTrustProfiles` in trust.ts, update the
`curatorSlug` values to reference the new named curator's slug.

### Step 3: Update certificate page — Named curator statement

In `trust.ts`, update `certificateRecord.curatorStatement` from:
> "This certificate links the edition to the public NASA source record and preserves
> the difference between source attribution, institutional custody, and product
> publication."

To a first-person statement by the named curator:
> "I curated this edition from the NASA public record. Earthrise was photographed by
> William Anders on Apollo 8 on December 24, 1968. It is a work of the United States
> government and is in the public domain under 17 U.S.C. § 105. The certificate
> records source, rights basis, and edition structure. — [Name], Founding Curator"

### Step 4: Add curator credit to about page

The current `/about` page should carry the founding curator's name as the named
institutional contact. At minimum: "Founded by [Name]" with the institutional email.
The full founding narrative can follow in Tier 2.

### Step 5: Publish curatorial statements per collection

Each collection currently has a `curatorStatement` field. If not already in first
person and attributed, update to:
```
"[2–3 sentences why these specific illustrations, in first person.] — [Name],
Founding Curator, [date]"
```

---

## The Founding Curator Designation in the Public Record

The Founding Curator's name will appear in:
- `/curators/[slug]` (permanent)
- `/about/founding` (permanent)
- Every certificate issued during their tenure as Collection Curator
- The first annual institutional disclosure report
- The version history of all governance documents ratified during their tenure
- NC-PDPS Link 6 (`curator_name`) for all founding-period products

This is the institutional permanence signal. The collections NC is building now will
carry this person's name as the curatorial authority. That name is the institution's
answer to the Smithsonian question: *who decided this?*

The answer — a specific person, with a specific statement, on a specific date —
is the difference between a credible institution and an anonymous content platform.

---

## Open Actions

| # | Action | File | Priority |
|---|---|---|---|
| OA-1 | **Add ORCID and contact fields to TrustCurator type** | `apps/web/lib/trust.ts` | Critical |
| OA-2 | **Replace desk entries with named founding curator** | `apps/web/lib/trust.ts` | Critical |
| OA-3 | **Update curatorStatement to first-person signed statement** | `apps/web/lib/trust.ts` | Critical |
| OA-4 | Update collectionTrustProfiles to reference new curator slug | `apps/web/lib/trust.ts` | Critical |
| OA-5 | Add founding curator credit to `/about` page | `apps/web/app/about/page.tsx` | Critical |
| OA-6 | Update collection page bylines to named individual | Collection pages | High |
| OA-7 | Add ORCID display to `/curators/[slug]` page template | `apps/web/app/curators/[slug]/page.tsx` | High |
| OA-8 | Draft founding narrative for `/about/founding` | New page | High |
| OA-9 | Publish corrections policy at `/editorial/corrections` | New page | High |
| OA-10 | Determine NC-PROD-001 edition size (100) — ratify this decision | Governance | Critical |

---

## Summary

The founding curator framework establishes four distinct roles — Founding Curator,
Collection Curator, Collection Editor, Institutional Director — which one person may
hold simultaneously at founding. The Founding Curator designation is permanent; it
records who built the institution and what decisions they made.

The minimum viable change is five lines in trust.ts: replace three anonymous desks
with one named person. That change — a decision, not development — unblocks every
trust standard simultaneously, makes every certificate credible, and gives NC the
institutional personhood that NC-INSTITUTION-001 identified as the primary barrier
to world-class trust.

An institution is not its design. It is the person who stands behind it.

---

*NC-INSTITUTION-002 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
