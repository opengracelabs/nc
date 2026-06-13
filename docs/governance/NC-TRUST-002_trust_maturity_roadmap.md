# NC-TRUST-002: Trust Maturity Roadmap

| Field | Value |
|---|---|
| Document | NC-TRUST-002 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-TRUST-001 · NC-INSTITUTION-001 · NC-SIGNATURE-002 |
| Scope | Reviews NC trust architecture against 4 reference models. Defines maturity levels for 6 trust domains. Issues sequenced roadmap to world-class status. |

---

## Reference Models

Four institutions. Each teaches NC something the others cannot.

| Institution | Trust model | What it teaches NC |
|---|---|---|
| **Smithsonian** | Scholar authority | Named humans, published methodology, peer citation |
| **Rijksmuseum** | Collection authority | Certificate standard, edition architecture, print shop quality |
| **National Geographic** | Editorial authority | Byline accountability, fact-checking visibility, editorial chain |
| **Getty** | Provenance authority | Ownership chain, open content communication, ULAN/AAT metadata, institutional charter |

Getty is the new reference in this document. Its specific contribution: the Getty
Provenance Index sets the professional standard for provenance documentation;
the Getty Open Content Program is the model for communicating PD rights to the public;
the J. Paul Getty Trust is the model for institutional charter and accountability.
Getty reveals two gaps not addressed in NC-TRUST-001: the ownership history link in
provenance chains, and the institutional legal/accountability layer.

---

## The Maturity Model

Five levels across six trust domains.

```
Level 0 — Absent        No system, no signal, no person
Level 1 — Declared      Exists but not systematised; name without process
Level 2 — Documented    Policy published, process visible, publicly accessible
Level 3 — Institutionalised  Consistent, auditable, reproducible, peer-legible
Level 4 — Authoritative  Independently recognised, sector-leading, cited by peers
```

**World-class floor = Level 3 in all 6 domains.**
Level 4 is what Smithsonian, Rijksmuseum, Getty, and NatGeo have after 50–200 years.
NC targets Level 3 everywhere and Level 4 where structural advantage exists.

**NC's structural advantage for Level 4:**
- Provenance transparency: NC's PD chain (creator → institution → CC0 → NC) is *shorter
  and cleaner* than the ownership chains traditional museums must document. A museum
  tracing a 17th-century Dutch painting must account for 400 years of sales, seizures,
  and restitution claims. NC's chain is typically creator (1750–1900) → institution
  (held continuously) → CC0 (2010s). This advantage can be exploited at Level 4.
- Digital-native edition registry: Traditional print publishers use paper registries.
  NC's is born digital — verifiable, permanent, publicly queryable. Level 4 in editions
  is structurally easier for NC than for any analogue predecessor.

---

## Current State Assessment

Where NC stands today (before NC-TRUST-001 implementation) and after each sprint.

### Domain 1: Curator Identity

*Measures: named humans accountable for collection decisions, visible credentials,
published selection methodology.*

| Level | Standard | Reference |
|---|---|---|
| **0** | No named curator, no accountability for selection | NC today |
| **1** | One named person, a title, a bio page | NC after TRUST-001 Phase 0 |
| **2** | Named curator per collection, curatorial statement, credentials publicly verifiable | NC after Sprint 1 |
| **3** | ORCID IDs, published methodology, named peer reviewer for each collection, editorial board | NC target |
| **4** | PhD-credentialed senior curators, published catalogue raisonnés, cited in peer literature | Smithsonian / Getty |

**Current state: Level 0**

**World-class requirement (Level 3):**
- Named curator per collection with verifiable credentials (ORCID or equivalent)
- Public curatorial methodology: how illustrations are selected, how PD status is
  confirmed, how source institution is verified
- Named authority reviewer per collection (distinct from the curator — a second named
  person who confirmed the GeoNames, Wikidata, and rights checks)
- Curator record version history: who made what decision when

**Getty gap (new):**
Getty curators are named in published acquisition announcements. When the Getty acquires
a work, a named curator's statement is published. When the Getty releases works as open
content, a named program director is responsible. NC needs the equivalent: a named
"Open Content Lead" who is publicly accountable for every PD determination.

**Getty also uses ULAN (Union List of Artist Names) IDs for every creator.**
NC's illustrator records should carry ULAN IDs where available. Owen Jones (ULAN
500010851), Edward Wilson (if listed), David Roberts (ULAN 500028453). This is
the Level 3 → Level 4 transition for curator identity. ULAN is not a blocker at
Level 3 but it signals peer-legibility.

---

### Domain 2: Provenance

*Measures: depth of documented chain, stability of source links, ownership history
between creator and current holder, legal basis for rights status.*

| Level | Standard | Reference |
|---|---|---|
| **0** | "Public domain" attribution text. No chain. | NC today |
| **1** | Creator + institution named on product page | After TRUST-001 Phase 0 |
| **2** | 4-link chain: creation → institution → rights → NC curation. Stable URL to source record. | After TRUST-001 Phase 1 |
| **3** | 5-link chain adds ownership/custody history. Legal basis cited by statute. All chains version-controlled. | NC target |
| **4** | Scholarly annotation, literature citations, auction records, conservation history, Getty Provenance Index level | Getty |

**Current state: Level 0**

**World-class requirement (Level 3):**

NC-TRUST-001 defines a 4-link chain: Creation → Institutional holding → Rights status
→ NC acquisition. Level 3 requires a fifth link: **custody history** — the chain of
custody between the creator and the current holding institution.

For most NC works, this link is short and verifiable:
- Wilson's watercolours: "Bequeathed to the Natural History Museum, London by Edward
  Wilson's estate, 1912." One documented transfer.
- Owen Jones plates: "Produced for Plans of the Alhambra, published 1836–45. Plates
  held in the V&A collection since the institution's founding collection, 1852."
- NGA Cole paintings: "Purchased by the National Gallery of Art from [auction/dealer],
  [year]. NGA accession [number]."

These custody notes are short for NC's material because the institutional chains are
clean. This is NC's provenance advantage. A museum with a Vermeer must document four
centuries. NC's Wilson has one documented transfer. Level 3 provenance for NC is
lower-effort than for any traditional museum.

**Legal basis standard (Level 3):**

`pd_basis` must cite the specific statute, not just the concept. Examples:

| Rights basis | Display text |
|---|---|
| UK copyright expiry | "Copyright expired under UK Copyright Act 1988 (life + 70 years). Edward Wilson died 1912; copyright expired 1982." |
| US government work | "Work of the US federal government. Not subject to copyright under 17 U.S.C. § 105." |
| CC0 release | "Released as Creative Commons Zero (CC0) by the Natural History Museum, London, 2014. CC0 waives all copyright and related rights worldwide." |
| Pre-1928 published US | "Published in the United States before January 1, 1928. Now in the public domain under US copyright law." |

The specific statute or act is the Level 3 requirement. "Public domain" alone is Level 1.

**Stable URL requirement (Level 3):**

Source institution links must resolve permanently. NC should:
- Prefer permalink/accession-number-based URLs over search result URLs
- Archive the institutional record snapshot at the time of curation (Wayback Machine or
  equivalent)
- Flag broken source links within 30 days of detection

---

### Domain 3: Editions

*Measures: edition architecture clarity, registry completeness, physical authentication
on the print itself, public verifiability, retirement procedure.*

| Level | Standard | Reference |
|---|---|---|
| **0** | "Limited edition" label. No registry. No system. | NC today |
| **1** | Registry exists. Public verify page. Edition size defined before sale. | After TRUST-001 Phase 1 |
| **2** | Edition stamp/mark on physical print. Policy published. Closure procedure documented. | After Sprint 2 |
| **3** | Two-factor authentication (certificate + physical mark). Edition archive permanent. Retirement documented. | NC target |
| **4** | Independent third-party registration. Notarised closure records. Recognised by specialist auction houses. | Fine art print market standard |

**Current state: Level 0**

**World-class requirement (Level 3):**

NC-TRUST-001 defines the registry and the certificate. The Level 3 gap is the
**physical authentication mark on the print itself.** A certificate can be lost,
separated from its print, or disputed. The physical mark on the print is the
second authentication factor.

**Two physical mark options (NC should choose one):**

*Option A — Blind emboss stamp:*
A custom embossing die pressed into the paper margin of every Collector's Edition print.
The stamp is NC's institutional mark + edition number (e.g., "NC 042/100"). This is the
Rijksmuseum print shop standard. The emboss is permanent, invisible until angled light,
and cannot be added after printing. It authenticates the print, not the paper.

*Option B — Edition numbering in pencil in the margin:*
"42/100" hand-written in the lower-left margin, curator-initialled in the lower-right.
This is the conventional fine art print standard (Senefelder convention for lithographs).
It is lower cost than a die and is recognisable to any print collector.

**Recommendation: Option B for launch.** Pencil edition numbering is the accepted
convention, requires no equipment investment, and is immediately recognisable to print
collectors. Add blind emboss die at Level 4 when print volume justifies the tooling cost.

**Retirement procedure (Level 3):**

When a Collector's Edition closes:
1. Edition status updated to "closed" in registry
2. Edition closure notice published on the product page (date + final count)
3. The original high-resolution production file is archived with a closure record
   (cannot be reused for the same edition; a Second Edition requires a new edition_id)
4. The last print issued receives a note on its certificate: "Final print of this edition"

This procedure is the difference between a registered limited edition and an
unverifiable claim.

---

### Domain 4: Certificates

*Measures: field completeness, physical quality, independent verifiability, conservation
standard, insurance-grade language.*

| Level | Standard | Reference |
|---|---|---|
| **0** | No certificate | NC today |
| **1** | 12-field certificate exists, ships with print, PDF downloadable | After TRUST-001 Phase 0 |
| **2** | Permanent verify URL, conservation language reviewed, print studio named | After Sprint 1 |
| **3** | Insurance-grade language, conservator-reviewed conservation note, institutional seal, two-factor with physical mark | NC target |
| **4** | Embossed seal, notarised on request, accepted by major auction houses and insurers | Christie's / Sotheby's prints standard |

**Current state: Level 0**

**World-class requirement (Level 3):**

NC-TRUST-001 defines the 12 certificate fields. Three additional requirements for Level 3:

**Insurance-grade language:**
A collector's insurance policy for fine art requires provenance documentation written
in language an underwriter can act on. The certificate's rights block must read:

*"This work is in the public domain. The copyright in the original work by [Creator]
(died [year]) expired under [statute] on [date]. The Natural History Museum, London
additionally released the digital reproduction under Creative Commons Zero (CC0) in
[year], waiving all copyright and related rights. Nature & Culture produces and sells
this print under both bases. No licence fee or royalty is owed to any party."*

This language is more explicit than "Public domain. CC0 release by NHM, 2014." It is
the language a lawyer and an insurer can read without further inquiry.

**Conservator-reviewed conservation note:**
The standard conservation note in NC-TRUST-001 is correct but generic. Level 3 requires
the conservation note to be reviewed by a named conservator (or cite a published
conservation standard such as ISO 9706 or ANSI/NISO Z39.48). The certification of the
paper's archival quality should cite a specific standard, not a marketing claim.

Example: *"Paper: Hahnemühle Photo Rag 308gsm. Acid-free, OBA-free, 100% cotton rag.
Meets ISO 9706 standard for permanent paper. UV-resistant inks rated 100+ years per
ISO 11798 accelerated ageing test. Frame with UV-protective glazing. Avoid relative
humidity above 60% and temperatures above 21°C."*

**Institutional seal:**
A printed (not embossed at Level 3) NC institutional seal on the certificate — the NC
mark used consistently across all printed materials. This is distinct from the print's
physical mark (Domain 3). The certificate seal authenticates the certificate document
itself.

---

### Domain 5: Institutions

*Measures: visibility of partner institutions at product level, depth of institutional
relationship, partnership formalisation, co-created content.*

| Level | Standard | Reference |
|---|---|---|
| **0** | Attribution text only. No institution visible on product. | NC today |
| **1** | Institution name + source record link on every product page | After TRUST-001 Phase 0 |
| **2** | Institution pages on NC, institution block above fold, logo where permitted | After TRUST-001 Phase 2 |
| **3** | Formal partnership acknowledgment, co-announced products, named institutional contact | NC target |
| **4** | Published MoUs, joint content creation, mutual link exchange, institutional endorsement of NC quality standard | Google A&C / Smithsonian partner standard |

**Current state: Level 0**

**World-class requirement (Level 3):**

NC-TRUST-001 takes institutions to Level 2: institution pages, logo display, source links.
Level 3 requires formalisation of the relationship — not a legal contract necessarily,
but a documented acknowledgment from the institution that NC uses their content.

**Level 3 for each Tier 1 institution:**

| Institution | Level 3 action | Outcome |
|---|---|---|
| NHM London | Email to NHM Digital to notify of CC0 use, request logo permission | Named NHM contact; permission on file; NHM aware of NC |
| NGA Washington | NGA has a formal CC0 re-use notification process | NGA record of NC as commercial CC0 user |
| Walters Art Museum | Walters CC0 is institution-wide; email notification | Walters contact on file |
| CMA Cleveland | CMA open access; email notification | CMA contact on file |
| Met Museum | Met CC0; email notification | Met contact on file |

None of these require a legal instrument. They require an email to the right person.
The outcome is: NC has named contacts at every Tier 1 institution, those contacts know
NC exists, and NC can say "in communication with [institution]" in any press context.

**The Getty model for Open Content communication:**
Getty's Open Content page is not a legal notice — it is a public statement of intent
that builds trust through transparency. NC should publish an equivalent:
`/about/open-content` that names every source institution, the basis for using their
content, and the NC commitment to attribution and provenance. This is Level 3 in
public communication about institutional relationships.

---

### Domain 6: Educational Reuse

*Measures: free access clarity, resource depth, institutional adoption pathway, curriculum
credibility, accessibility compliance.*

| Level | Standard | Reference |
|---|---|---|
| **0** | No educational affordance visible. Commerce only. | NC today |
| **1** | "For educators" badge, free download path exists, educators page | After TRUST-001 Phase 2 |
| **2** | Context guides for 5 collections, WCAG statement published, educational license | After Sprint 2 |
| **3** | Formal curriculum materials, named educational partnerships, school adoption documented | NC target |
| **4** | Accredited curriculum packages, professional development, named school system partnerships | NatGeo Education standard |

**Current state: Level 0**

**World-class requirement (Level 3):**

NC-TRUST-001 takes educational reuse to Level 1 (free downloads, educators page).
Level 2 adds context guides and the WCAG statement. Level 3 requires that a school
can formally adopt NC as a curriculum resource — which requires:

**WCAG 2.1 AA compliance (not just a statement):**
Level 2 is publishing the accessibility statement. Level 3 is completing the audit and
remediating the findings. An institution cannot formally adopt a platform with known
unresolved accessibility failures. The audit is the gate.

**Curriculum alignment documentation (more than context guides):**
Context guides (NC-TRUST-001) are teacher-facing entry points. Level 3 requires
curriculum alignment at the subject and year-group level, aligned to at least one
national curriculum standard (UK National Curriculum, US Common Core, Australian
Curriculum, or IB). The specific alignment signals to curriculum coordinators — not
just classroom teachers — that NC has done the mapping work.

**Named educational partnership:**
Before Level 3 is reached, NC should have at least one named educational organisation
(a school, a library, a museum education department, a heritage body) that has used
NC materials and is willing to say so publicly. This is the educational equivalent of
the press coverage gap in NC-INSTITUTION-001 — it must be earned, and the earlier work
in Level 1 and 2 creates the conditions for it.

---

## Maturity Assessment Matrix

Current state, after NC-TRUST-001 full implementation, and world-class target.

| Domain | Today | After TRUST-001 | Sprint 1 | Sprint 2 | Sprint 3 (World-class) |
|---|---|---|---|---|---|
| Curator Identity | 0 | 1 | 2 | 3 | 3 |
| Provenance | 0 | 2 | 2–3 | 3 | 3 |
| Editions | 0 | 1–2 | 2 | 3 | 3 |
| Certificates | 0 | 1–2 | 2 | 3 | 3 |
| Institutions | 0 | 1–2 | 2 | 3 | 3 |
| Educational Reuse | 0 | 1 | 1–2 | 2 | 3 |

World-class (Level 3 across all 6) is achievable at Sprint 3. The educational reuse
domain is the slowest to mature because Level 3 requires earned institutional adoption,
not just published content.

---

## Gap Analysis by Domain

What NC-TRUST-001 does not yet address, and what each reference model adds.

| Domain | TRUST-001 covers | Gap to Level 3 | Reference teaching it |
|---|---|---|---|
| Curator Identity | Named curator, bio, bylines | ORCID ID · ULAN IDs for illustrators · Named authority reviewer distinct from curator · Published selection methodology | Getty (ULAN, named program director) |
| Provenance | 4-link chain, stable URLs, pd_basis | 5th link: custody history between creator and institution · Legal statute cited by section and year · Source URL archiving (Wayback) | Getty Provenance Index |
| Editions | Registry, verify page, edition types | Physical mark on print (pencil edition number in margin) · Documented retirement procedure · Closure notice published | Rijksmuseum (blind emboss) · Fine art print convention |
| Certificates | 12 fields, certificate_id, PDF | Insurance-grade rights language (statute, year, dual basis) · Conservator-reviewed conservation note citing ISO standard · Institutional seal | Rijksmuseum · Christie's prints |
| Institutions | Institution pages, logo display, source links | Named contact at each Tier 1 institution (email notification) · `/about/open-content` page naming all partners · NC declaration that institutions know NC uses their content | Getty Open Content · Google A&C |
| Educational Reuse | Free downloads, educators page, context guides, WCAG statement | WCAG audit completed (not just stated) · Curriculum alignment to named national standard · One named educational partnership | NatGeo Education · Smithsonian Education |

---

## The Trust Maturity Roadmap

Four sprints. Each sprint produces verifiable deliverables against the maturity matrix.

---

### Sprint 0 — Minimum Institutional Personhood
*Before Gate E. Non-negotiable. These are the floor, not the goal.*

**Goal: Level 1 in Curator, Provenance, Certificates, Institutions**

| Action | Domain | Deliverable | Closes |
|---|---|---|---|
| Name a curator. One bio page. One curatorial statement per collection. | Curator | `/curators/[name]` page live | Curator → Level 1 |
| Write PD explainer page at `/about/public-domain`. 3 paragraphs, plain language, statute-level basis for each rights type. | Provenance | Page live | Provenance → Level 1 |
| Add institution name + source record URL to every product page, above fold. | Institution | Institution block on all products | Institution → Level 1 |
| Issue first certificate of authenticity (NC-PROD-001). 12 fields. PDF available at time of purchase. | Certificate | First certificate issued | Certificate → Level 1 |
| Add byline to all editorial copy. | Editor | Bylines live | Editor → Level 1 |

**Sprint 0 review gate:** All 5 deliverables confirmed live by two distinct reviewers before Gate E opens.

---

### Sprint 1 — Documentation Layer
*3 months after Gate E. Commerce is live; now the institutional layer catches up.*

**Goal: Level 2 in Curator, Provenance, Certificates, Institutions · Level 1→2 in Editions**

| Action | Domain | Deliverable | Level |
|---|---|---|---|
| Build edition registry (DB schema + `/verify` page). Define edition sizes for all Collector's Editions before close of Sprint 1. | Editions | Public `/verify` page live | Editions → Level 2 |
| Add provenance block (4 links, collapsed) to all product pages. Cite specific statute in pd_basis. | Provenance | Provenance block on all products | Provenance → Level 2 |
| Upgrade certificate to insurance-grade rights language. Publish conservation note citing ISO 9706 and ISO 11798. | Certificate | Updated certificate PDF + physical template | Certificate → Level 2 |
| Assign ORCID IDs to all NC curators. Add to curator profile pages. | Curator | ORCID visible on curator pages | Curator → partial Level 3 |
| Build institution pages for all Tier 1 partners (`/institutions/nhm`, `/institutions/nga`, etc.). | Institution | Institution pages live (5) | Institution → Level 2 |
| Send email notifications to Tier 1 institutions: NHM, NGA, Walters, CMA, Met. Request logo permission. Document receipt. | Institution | 5 sent notifications, responses tracked | Institution → Level 3 start |
| Publish editorial corrections policy at `/editorial/corrections`. | Editor | Corrections page live | Editor → Level 2 |
| Begin WCAG 2.1 AA audit (commission or self-audit). Publish interim accessibility statement at `/accessibility`. | Educational | Accessibility statement live | Educational → Level 1–2 |

**Sprint 1 review gate:** Edition registry live with at least one closed edition or one pending edition with defined size. Certificate upgrade confirmed on 3 physical prints. WCAG audit commissioned.

---

### Sprint 2 — Authentication Layer
*6 months after Gate E. Collector-grade trust is established.*

**Goal: Level 3 in Certificates, Editions · Level 2→3 in Provenance, Institutions · Level 2 in Educational Reuse**

| Action | Domain | Deliverable | Level |
|---|---|---|---|
| Implement physical edition mark on all Collector's Edition prints: pencil edition number and curator initials in lower margin. | Editions | Standard applied to all new CE prints | Editions → Level 3 |
| Document and publish edition retirement procedure. Apply to first closed edition. | Editions | Retirement procedure published; first retirement executed | Editions → Level 3 |
| Add institutional seal (NC mark) to certificate document template. | Certificate | Seal on all new certificates | Certificate → Level 3 |
| Add 5th provenance link (custody history) to all 5 signature collections. Cite specific transfer records. | Provenance | 5-link chain on signature collections | Provenance → Level 3 |
| Archive source institution URLs via Wayback Machine. Document in provenance record. | Provenance | All source URLs archived | Provenance → Level 3 |
| Publish `/about/open-content` page naming all source institutions, rights bases, and NC commitments. | Institution | Open content page live | Institution → Level 3 |
| Complete WCAG audit. Publish results + remediation timeline at `/accessibility`. | Educational | WCAG audit results published | Educational → Level 2 |
| Build educators page (`/educators`) with free download path (Tier 1) and license application (Tier 2). | Educational | Educators page live, downloads active | Educational → Level 2 |
| Publish context guides for 5 signature collections (6-section format from TRUST-001). | Educational | 5 context guides available | Educational → Level 2 |
| Add ULAN IDs for priority NC illustrators (Owen Jones, David Roberts, Edward Wilson, Thomas Cole). | Curator | ULAN IDs on illustrator records | Curator → Level 3 start |

**Sprint 2 review gate:** At least one Collector's Edition print has physical edition mark and is verified against the registry via `/verify`. Open content page live. WCAG results published with remediation dates.

---

### Sprint 3 — Institutional Authority
*12 months after Gate E. World-class floor reached.*

**Goal: Level 3 in all 6 domains**

| Action | Domain | Deliverable | Level |
|---|---|---|---|
| Publish named authority reviewer for each collection (the second person who confirmed GeoNames, Wikidata, and rights checks). | Curator | Authority reviewer visible on collection pages | Curator → Level 3 |
| Publish selection methodology document: how NC chooses illustrations, how PD is confirmed, how institutions are vetted. | Curator | Methodology page at `/about/methodology` | Curator → Level 3 |
| Extend 5-link provenance chain to all products (not just signature collections). | Provenance | All products have complete chains | Provenance → Level 3 |
| Implement URL health monitoring: broken source links flagged within 30 days. | Provenance | Monitoring active | Provenance → Level 3 |
| Confirm logo display permissions in writing from at least 3 Tier 1 institutions. Display logos. | Institution | Institutional logos on product pages (3+) | Institution → Level 3 |
| Publish curriculum alignment documentation for 5 signature collections against one named national curriculum. | Educational | Curriculum alignment live | Educational → Level 3 |
| Document first named educational use of NC content. Publish as case study or testimonial at `/educators/stories`. | Educational | First educational story published | Educational → Level 3 |
| Complete WCAG 2.1 AA remediation for all identified failures from Sprint 2 audit. Re-audit. | Educational | WCAG conformance confirmed | Educational → Level 3 |

**Sprint 3 review gate:** External review of NC trust layer against this maturity matrix. All 6 domains confirmed at Level 3 by a reviewer distinct from the person who implemented the work. This is the Gate E equivalent for institutional maturity.

---

### Sprint 4 — Structural Advantage (selective Level 4)
*18–24 months. World-class established; pursue Level 4 where NC has structural advantage.*

NC's two structural Level 4 opportunities:

**Provenance → Level 4:**
NC's PD chains are shorter and more documentable than traditional museum provenance. NC
should publish a formal provenance methodology document citing the Getty Provenance Index
as a standard reference, apply the methodology to all collections, and make the
methodology publicly available under Creative Commons. This positions NC as the provenance
standard-setter for PD illustration commerce — a domain that currently has no defined
professional standard. NC can *write* that standard.

**Edition Registry → Level 4:**
NC's edition registry is born digital, publicly queryable, and designed for permanent
archive. No traditional print publisher has a public, real-time verifiable edition
registry. NC can publish the registry API for third-party auction house integration.
When a collector wants to verify a print for resale, they query NC's API. This is Level 4
in a domain where the incumbent standard (paper certificate, phone call to gallery) is
still Level 2. NC can leapfrog to Level 4 without waiting 100 years.

---

## The Level 3 Test

A single-question test for each domain. When NC can answer yes to all six, it is at
world-class floor.

| Domain | Level 3 test question |
|---|---|
| Curator Identity | "Can a scholar identify, by name, who selected each illustration and why — and independently verify their credentials?" |
| Provenance | "Can a collector, lawyer, or insurer trace the complete chain from the creator's hands to NC's product page using only publicly available documents?" |
| Editions | "Can a buyer verify, in under 60 seconds without contacting NC, that the print in their hands is copy 42 of a genuine 100-print limited edition?" |
| Certificates | "Does the certificate, by itself, contain enough information for an insurance underwriter to assess and insure the print?" |
| Institutions | "Do NC's Tier 1 source institutions know that NC uses their content commercially, and is there a named contact at each institution who can confirm this?" |
| Educational Reuse | "Can a teacher, arriving at NC for the first time, immediately understand that every image is free to use in their classroom — and find the tools to do so?" |

---

## Summary Verdicts by Reference Model

| Model | What NC learns | What NC exceeds (at Level 3) |
|---|---|---|
| **Smithsonian** | Named humans, published methodology, peer-legible credentials | NC's provenance chain for PD illustration will be shorter, more complete, and more publicly accessible than the Smithsonian's for comparable works |
| **Rijksmuseum** | Certificate standard, physical print mark, edition closure procedure | NC's edition registry is public and queryable; Rijksmuseum's is internal. NC's `/verify` page has no Rijksmuseum equivalent. |
| **National Geographic** | Byline accountability, editorial fact-checking chain, corrections culture | NatGeo does not sell fine art prints. NC's certificate and provenance infrastructure exceeds anything NatGeo has in the commerce domain. |
| **Getty** | Custody history in provenance, Open Content communication model, institutional charter, ULAN metadata | NC's PD chains are cleaner than Getty's (NC holds no contested works). NC's edition registry is more transparent than Getty's. |

At Level 3, NC does not merely match these institutions — it exceeds them in the specific
domains that matter for PD illustration commerce. None of the four reference models has a
public edition registry, a publicly verifiable certificate system, or a PD value chain
communicated at the statutory level on every product page.

The Smithsonian, Rijksmuseum, NatGeo, and Getty built trust over decades because they had
no choice — there was no faster path. NC can reach Level 3 in 12 months and publish the
methodology that got it there. That publication is the trust signal that takes NC to Level 4.

---

*NC-TRUST-002 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
