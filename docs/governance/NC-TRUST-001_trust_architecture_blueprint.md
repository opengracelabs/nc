# NC-TRUST-001: Trust Architecture Blueprint

| Field | Value |
|---|---|
| Document | NC-TRUST-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-INSTITUTION-001 · NC-WEB-001 · NC-SIGNATURE-002 |
| Scope | Designs 7 trust layer systems: Curator, Editor, Certificate, Edition Registry, Provenance Display, Institution Display, Educational Licensing Display. |

---

## Purpose

NC-INSTITUTION-001 found that every trust gap at NC is a disclosure gap. The work is
sound. The governance is rigorous. None of it is visible. This blueprint designs the
seven systems that make the institutional work legible — to collectors, scholars,
teachers, journalists, and first-time visitors simultaneously.

Each system is designed at the level of a buildable specification: data model, display
rules, operational requirements, and the specific NC-INSTITUTION-001 gaps it closes.

---

## Trust Layer Architecture

Seven systems. Three audiences. One product page.

```
                    ┌──────────────────────────────────────────┐
                    │              PRODUCT PAGE                │
                    │                                          │
CURATOR SYSTEM ─────┤  [Provenance Block]  [Institution Block] ├──── GENERAL PUBLIC
EDITOR SYSTEM ──────┤  [Curator Credit]    [Editorial Byline]  ├──── JOURNALISTS
CERTIFICATE ────────┤  [Certificate CTA]   [Edition Status]    ├──── COLLECTORS
EDITION REGISTRY ───┤  [Edition Number]    [Verify Link]       ├──── COLLECTORS
PROVENANCE DISPLAY ─┤  [Rights Chain]      [Source Record]     ├──── ALL
INSTITUTION DISPLAY ┤  [Partner Logo]      [Collection Link]   ├──── ALL
EDUCATIONAL ────────┤  [Educator Badge]    [Free Download]     ├──── TEACHERS
                    └──────────────────────────────────────────┘
```

**Audience → trust question → system that answers it:**

| Audience | Question | System |
|---|---|---|
| Scholar / journalist | Who selected this and why? | Curator |
| Journalist / general public | Who wrote this and is it accurate? | Editor |
| Collector | What exactly did I buy? | Certificate |
| Collector / reseller | Is the limited edition claim real? | Edition Registry |
| All | Where did this come from? Why can NC sell it? | Provenance Display |
| All | Who are NC's institutional partners? | Institution Display |
| Teacher / institution | Can I use this in my classroom? | Educational Licensing |

---

## System 1: Curator

**Closes:** IR-001 (no named staff), IR-007 (no visible selection methodology), IR-008
(no bylines)

**Reference model:** Smithsonian (named curators per department, public credentials,
published research record)

### Purpose

A curator at NC is the named human accountable for a collection. They decided which
illustrations belong, why they belong, and what the collection says. They are not a
brand voice — they are the institutional authority whose name stands behind the work.

### Data Model

```
curator {
  curator_id:       string         // NC-CUR-NNN
  name:             string
  title:            string         // e.g., "Collection Curator, Islamic Architecture"
  credentials:      string         // 2–3 lines: background, not CV
  bio:              text           // 150–200 words. First person.
  collections:      string[]       // array of collection slugs
  content_types:    enum[]         // illustration_selection | place_editorial |
                                   // institution_profile | taxon_note
  orcid:            string|null    // optional ORCID identifier
  contact:          string         // institutional email address
  active:           boolean
  since:            date
}
```

### Display Specification

**Curator profile page** (`/curators/[name]`):
- Name, title, bio
- "Collections curated" — linked list of collection cards
- No personal social media, no external links unrelated to NC work
- Photo optional; institutional rather than personal framing

**On collection page:**
```
Curated by [Name], [Title]
[2-sentence curatorial statement — not the same as the bio, written
specifically for this collection]
→ About the curator
```

**On product page:**
```
Curated by [Name]  ·  [Collection Name]
```

**In certificate of authenticity:**
Full curator name, title, and curator_id.

### Operational Requirements

- Every collection must have an assigned curator before Gate CP.
- Curator credentials must be verifiable independently (ORCID preferred; publicly
  available professional record minimum).
- When a curator leaves or changes role, collections are reassigned — not left without
  attribution. The previous curator is noted in collection version history.
- A single person may hold the curator role for all initial collections. Institutional
  personhood requires a named individual, not a team.

### Minimum viable state (pre-launch)

One named curator. One curatorial statement per collection. One curator page. This
closes IR-001 entirely. The founder is the curator until there are others.

---

## System 2: Editor

**Closes:** IR-008 (no bylines), IR-012 (no corrections policy)

**Reference model:** National Geographic (full masthead, bylined journalism, named
editors accountable for every claim, corrections policy with stated turnaround)

### Purpose

Every editorial word on NC was written by a named person who stands behind it. An
editor is not the same as a curator: the curator selects the illustration; the editor
writes the story around it. They may be the same person at launch, but the role is
distinct.

### Data Model

```
editor {
  editor_id:        string         // NC-EDT-NNN
  name:             string
  title:            string         // e.g., "Editorial Director" or "Contributing Editor"
  bio:              text           // 100 words. Credentials relevant to NC editorial.
  content_authored: string[]       // array of content IDs
  active:           boolean
}

editorial_content {
  content_id:       string
  content_type:     enum           // collection_intro | place_description |
                                   // illustrator_bio | expedition_note |
                                   // institution_profile
  author_id:        string         // ref: editor.editor_id
  reviewer_id:      string|null    // ref: curator.curator_id — fact reviewer
  published_date:   date
  version:          integer        // increments on revision
  version_history:  {date, change_summary}[]
  corrections:      {date, description, reporter}[]
}
```

### Display Specification

**On collection introduction:**
```
Written by [Name], [Title]
Reviewed by [Curator Name], [Curator Title]
Published [date]  ·  [Version N]  ·  Corrections policy →
```

**On place description:**
```
[Name], [Title]  ·  Published [date]
```

**Corrections policy page** (`/editorial/corrections`):
- "If you believe any NC editorial content contains a factual error, contact
  [email]. We acknowledge all corrections within 5 business days. Verified
  corrections are applied to the live content and noted in the version history
  with the reporter's name (if consented)."

**Editorial masthead** (`/about/editorial`):
- Named editors, roles, content areas
- Editorial process in 3 steps: draft → curator review → publish
- Corrections policy link

### Operational Requirements

- No editorial content goes live without an author attribution.
- Fact claims that cannot be verified by the assigned editor must be marked for
  curator review before publication.
- If the author and curator are the same person, the content is labeled
  "Written and curated by [Name]" — this is acceptable for a small team.
- Version history is append-only. Previous versions are retained, not deleted.

---

## System 3: Certificate of Authenticity

**Closes:** IR-003 (no certificate), IR-006 (no print specs), IR-011 (no conservation
guidance)

**Reference model:** Rijksmuseum print shop (8-field certificate with every print,
institutional stamp, edition number, conservation note)

### Purpose

The certificate is the physical and digital proof of what a collector bought. It is
the bridge between the NC platform and a collector's archive, insurance record, or
estate inventory. Without it, a print is a poster. With it, a print is a collectible.

### Certificate Fields (12 required)

```
certificate {
  certificate_id:     string    // NC-[COL]-[PROD]-[NNN]-[YYYY]
                                // NC-COL001-PROD001-042-2026

  // Work identity
  work_title:         string    // Exact title of the illustrated work
  creator_name:       string    // Full name of the original illustrator
  creator_dates:      string    // "(1772–1838)" format
  creation_date:      string    // Year or range: "1842" or "c. 1901–1904"
  creation_context:   string    // "From Plans of the Alhambra, Plate 12"

  // Institutional provenance
  source_institution: string    // "Natural History Museum, London"
  source_record_url:  string    // Direct URL to institutional record
  rights_status:      string    // "Public domain. CC0 release by NHM, 2014."

  // Edition
  edition_type:       enum      // collector | open | digital
  edition_number:     integer|null  // null for open/digital
  edition_size:       integer|null  // null for open/digital

  // Production (physical prints only)
  paper_brand:        string    // e.g., "Hahnemühle Photo Rag"
  paper_gsm:          integer   // e.g., 308
  paper_archival:     string    // "Acid-free, OBA-free, 100% cotton rag"
  print_process:      string    // "Giclée (inkjet, archival pigment inks)"
  uv_resistance:      string    // "100+ years (ISO 11798 standard)"
  print_studio:       string    // Name and location of print studio

  // Curation
  curator_name:       string
  curator_id:         string    // ref: curator.curator_id
  collection_name:    string

  // Document metadata
  produced_date:      date
  issuing_institution: string   // "Nature & Culture"
}
```

### Physical Certificate Design

**Format:** A5 (148 × 210mm), 300gsm uncoated stock, single-sided or folded.

**Layout (top to bottom):**
1. NC institutional mark (top left) · Source institution name (top right)
2. Rule line
3. Work title (large, 16pt) / Creator name and dates (14pt)
4. Creation date and context (12pt)
5. Rule line
6. Provenance block (institution, record URL, rights status)
7. Edition block (type, number, size)
8. Production block (paper, process, UV rating, studio) — physical prints only
9. Rule line
10. Curation credit (curator name, title, collection)
11. Certificate ID (bottom left) · Produced date (bottom right)
12. Conservation note (below rule)

**Conservation note (standard text):**
*"To preserve this print: store flat or rolled in acid-free tissue. Frame with
UV-protective glass or acrylic. Keep away from direct sunlight and humidity above
65%. For framing guidance, contact [email]."*

### Digital Certificate

For digital downloads and physical prints sold online: a PDF certificate is generated
at time of purchase and available permanently at:
`nc.art/certificates/[certificate_id]`

The certificate page also shows verification status (see System 4).

### Operational Requirements

- Certificate ID is generated at moment of sale, not at moment of printing.
- Physical certificates ship inside the tube, rolled separately from the print.
- Digital certificates are emailed at time of purchase and permanently linked from
  the order record.
- If an edition closes, the certificate page updates to show "Edition closed: [date]."
- Lost certificates can be re-issued. A record of re-issue is appended to the
  edition registry (but does not change the edition number).

---

## System 4: Edition Registry

**Closes:** IR-005 (edition claim is unverifiable), IR-003 (partial — certificate is
incomplete without registry backing)

**Reference model:** Rijksmuseum print editions; fine art print market conventions
(limited editions have sequential numbers, public registries, verifiable status)

### Purpose

"Limited edition" is a claim. The edition registry is the system that makes the claim
true and verifiable. It tracks every print issued, every certificate assigned, and the
open/closed status of every edition.

### Data Model

```
edition {
  edition_id:       string    // NC-EDN-[COL]-[PROD]-[TYPE]
                              // NC-EDN-COL001-PROD001-CE (Collector's Edition)
  product_id:       string
  collection_id:    string
  edition_type:     enum      // collector | open | digital
  edition_size:     integer|null  // null for open editions
  edition_current:  integer   // auto-increments. Starts at 1.
  edition_status:   enum      // open | closed | retired
  opened_date:      date
  closed_date:      date|null
  retired_date:     date|null
  retirement_reason: string|null  // "Edition limit reached" | "Product retired" | etc.
}

certificate_record {
  certificate_id:   string    // NC-[COL]-[PROD]-[NNN]-[YYYY]
  edition_id:       string    // ref: edition.edition_id
  edition_number:   integer   // sequential within edition
  buyer_hash:       string    // one-way hash of buyer ID (not reversible — privacy)
  purchase_date:    date
  produced_date:    date
  reissued:         boolean
  reissue_date:     date|null
}
```

### Edition Types and Rules

**Collector's Edition:**
- Fixed size: 50, 100, or 250 prints (defined at product creation, cannot be changed)
- Sequential edition numbers (1/50, 2/50 … 50/50)
- Edition closes automatically when limit is reached
- Once closed: product page shows "Edition closed — [N] prints in circulation"
- File or plate is retired (not reused for same edition type)
- Can open a second edition (e.g., "Second Collector's Edition") — new edition_id,
  new sequential numbers, new certificates. First edition certificates remain valid.

**Open Edition:**
- No edition limit
- No edition number on certificate
- Certificate still issued for every print (provenance, production specs)
- Clearly labeled "Open Edition" on product page and certificate
- Lower price point than Collector's Edition of the same work

**Digital Download:**
- No edition concept
- License-based (PD content, educational/personal use)
- Confirmation receipt issued (not a certificate)
- No certificate ID system applies

### Public Verification

A certificate verification page at `/verify`:

Input: Certificate ID (e.g., NC-COL001-PROD001-042-2026)

Output:
```
Certificate NC-COL001-PROD001-042-2026

Work:         Edward Wilson, King Penguin and Chick, c. 1903
Collection:   South Georgia — "The Far Shore"
Edition:      Collector's Edition · Copy 42 of 100
Status:       ✓ Valid certificate
Edition:      Open (57 of 100 issued as of [date])
Curated by:   [Name], Nature & Culture
Produced:     [Date]

View this certificate →
Report a concern →
```

This page is publicly accessible without a login. A collector, reseller, or insurer
can verify any NC certificate in under 30 seconds.

### Operational Requirements

- Edition size is set at product creation and locked before Gate E.
- Edition size changes require a governance amendment (cannot be undone after first
  certificate is issued).
- Edition status is updated in real time as certificates are issued.
- Edition registry is backed up daily and archived permanently — edition records must
  outlast the platform.
- If NC ever ceases to operate, edition records must be transferred to an archival
  repository (this is a constitutional commitment, to be added at ratification).

---

## System 5: Provenance Display

**Closes:** IR-002 (PD value chain invisible), IR-017 (no source institution link),
IR-004 (partial — institution not surfaced)

**Reference model:** Rijksmuseum object pages (provenance history, acquisition,
conservation, bibliography visible); Smithsonian collections (accession records,
rights statements, exhibition history)

### Purpose

The provenance display answers, on every product page: who made this, where is the
original, how did it get to NC, and why can NC sell it. In that order.

### Provenance Chain Model

Every NC illustration has a provenance chain. The chain has four required links:

```
provenance_chain {
  // Link 1: Creation
  creator_name:         string
  creator_dates:        string      // "(1842–1903)"
  creator_role:         string      // "Physician and naturalist, Discovery Expedition"
  creation_date:        string
  creation_context:     string      // "Painted during the British National
                                    //  Antarctic Expedition, 1901–04"

  // Link 2: Institutional holding
  institution_name:     string      // "Natural History Museum, London"
  institution_record:   string      // URL to source record
  accession_notes:      string|null // optional: when acquired, from whom

  // Link 3: Rights status
  pd_basis:             string      // "Copyright expired [year] under [jurisdiction] law"
  pd_release:           string|null // "Released as CC0 by NHM, 2014" if applicable
  pd_release_url:       string|null // URL to rights statement
  rights_display:       string      // Human-readable single sentence

  // Link 4: NC acquisition
  nc_curator:           string      // curator name
  nc_selected_date:     string      // year
  nc_authority_note:    string|null // e.g., "GeoNames 4030001 / Wikidata Q35637 confirmed"
}
```

### Display Specification

**Product page — provenance block (collapsed by default, expanded on click):**

```
PROVENANCE

Created by
  Edward Wilson  (1872–1912)
  British physician, naturalist, and artist
  Painted during the Discovery Expedition, 1901–04

Held by
  Natural History Museum, London
  [View original record at NHM →]

Rights
  Public domain · Copyright expired 1982 (UK: life + 70 years)
  Released as CC0 by NHM, 2014
  [About public domain →]

Curated by
  [Name] · Nature & Culture · Selected 2026
```

**Collapsed state (always visible):**
```
  From the collection of Natural History Museum, London  ·  Public domain  ·  Provenance ↓
```

This collapsed state ensures the institution and rights claim are visible without any
user action. The expanded detail rewards engaged visitors.

**Standalone provenance page** (`/works/[slug]/provenance`):
Full provenance chain with all fields, plus: the illustrator's biography (from Editor
System), the expedition or commission context, and a timeline of key events
(creation → institutional acquisition → rights release → NC curation).

### Operational Requirements

- Provenance chain must be complete (all 4 links populated) before a product can pass
  Gate E.
- `institution_record` URL must be a stable, direct URL to the object record at the
  source institution (not a search result, not a general collection page).
- `pd_basis` must cite the specific legal basis (expired copyright, CC0 release,
  government work, etc.) — not simply "public domain."
- Provenance chains are version-controlled. If an institution's rights status changes,
  the chain is updated and the change is logged.

---

## System 6: Institution Display

**Closes:** IR-004 (partner institutions invisible), IR-017 (no source link at product
level)

**Reference model:** Google Arts & Culture (institution logo on every object page,
explicit partner acknowledgment, "explore this institution" pathway); Rijksmuseum
(strong own-brand, but collections sourced from other institutions are clearly
attributed)

### Purpose

NC's institutional partners — NHM, NGA, Walters, Europeana, Met, CMA — collectively
represent more trust than NC can generate independently for years. The institution
display routes that trust onto every NC product page. NC does not stand alone; it
stands in front of world-class institutions.

### Institution Record

```
institution {
  institution_id:     string      // NC-INS-NNN
  slug:               string      // "nhm" | "nga" | "walters" | etc.
  name:               string      // "Natural History Museum, London"
  short_name:         string      // "NHM London" — for compact display
  location:           string      // "London, UK"
  founded:            integer     // year
  description:        text        // 2–3 sentences: what the institution is
  relationship_type:  enum        // cc0_partner | pd_source | aggregator
  rights_basis:       string      // "CC0, 2014" | "Public domain only"
  nc_collection_count: integer    // updated dynamically
  institution_url:    string      // homepage
  collection_url:     string|null // their digital collection URL
  nc_collection_slug: string      // "/institutions/nhm"
  logo_url:           string|null // institution logo (with permission)
  logo_permitted:     boolean     // explicit permission to display logo
  active:             boolean
}
```

### Institution Tiers

**Tier 1 — CC0 Partner:**
Institution has made explicit CC0 or public domain release for a body of work that NC
uses commercially. NC has verified the release directly. Examples: NHM, NGA, CMA, Met.

Display treatment: Full logo (if permitted), partnership statement, institution page
link, "Explore [N] works from NHM →" link.

**Tier 2 — Public Domain Source:**
Institution holds works NC uses; works are PD by copyright expiry, not by explicit CC0
release. No formal partnership. Examples: Works accessed via Europeana from smaller
European institutions.

Display treatment: Institution name (no logo), rights statement ("Public domain,
copyright expired [year]"), external link.

**Tier 3 — Aggregator:**
NC accesses works through an aggregator (Europeana, DPLA) that is not itself the
holding institution. Display treatment: "Via [Aggregator], from [Holding Institution]"
with links to both.

### Display Specification

**Product page — institution block (always visible, above fold):**

For Tier 1:
```
[NHM LOGO]
From the collection of Natural History Museum, London

Released as CC0 for worldwide use.

→ Explore the NHM Collection at NC (N works)
→ View this work at NHM Digital Collections
```

For Tier 2:
```
From the collection of [Institution Name], [Location]
Public domain · Copyright expired [year]

→ View this work at [Institution]
```

For Tier 3:
```
From [Holding Institution] via Europeana
Public domain · [Rights basis]

→ View this work on Europeana
```

**Institution page** (`/institutions/nhm`):
```
[NHM LOGO]  Natural History Museum, London
            London, UK · Founded 1881

[2-sentence description]

At Nature & Culture
[N] works · CC0 · [Types: natural history illustrations, botanical plates]

Rights relationship
"In 2014, the Natural History Museum released its digitised collection
under Creative Commons Zero (CC0), making it freely available for any
use worldwide, including commercial use. Nature & Culture uses NHM's
CC0 release to bring their natural history illustrations to collectors
and educators."
[NHM CC0 policy →]

Works from NHM at Nature & Culture
[Collection cards: South Georgia, Pacific / Cook Voyages, ...]
```

**Institutions index page** (`/institutions`):
Grid of all Tier 1 institutions with logo, name, collection count, and type. Tier 2
and 3 institutions listed below in text form. Accompanied by the NC institutional
philosophy:

*"Nature & Culture does not own the works it sells — no one does. They belong to the
public domain. The institutions listed here have done the work of preserving,
digitising, and releasing these works for humanity's use. We are a commercial layer
on top of their generosity."*

### Operational Requirements

- Institution display must appear above the fold on every product page, before the
  product description and price.
- Logo display requires explicit written permission from the institution. If permission
  is not confirmed, institution name is displayed as text only.
- `nc_collection_count` is updated dynamically from the product database. It is never
  hardcoded.
- If an institution changes its rights position (e.g., revokes CC0 for new works), the
  institution record is updated immediately and affected product pages are reviewed
  within 24 hours.

---

## System 7: Educational Licensing Display

**Closes:** IR-009 (no accessibility statement), IR-010 (no free download path), IR-013
(no teacher resources), IR-019 (no educational pricing tier)

**Reference model:** National Geographic Education (formal school licensing, teacher
resources, curriculum guides, free classroom use); Google A&C classroom mode (free
institutional access, explicit educational framing)

### Purpose

Every illustration on NC is in the public domain and freely usable for educational
purposes without permission, payment, or attribution requirement. NC's educational
licensing display makes this explicit — and builds a relationship with teachers that
the platform currently ignores entirely.

### Educational Use Tiers

**Tier 0 — Public Domain (applies to all NC content, no action required):**

Every NC illustration is PD. No license from NC is needed for educational use. This
tier is not a product — it is a statement of fact about copyright law that NC makes
visible on every page.

Display: "For educators" badge on every product page, linking to the educators page.

**Tier 1 — NC Educational Download (free, no account required):**

For every product that has passed Gate E, NC provides a free educational resolution
version: 1920px long edge, 150dpi, suitable for classroom projection and printed
handouts up to A3.

File format: JPEG with embedded XMP metadata (work title, creator, institution, rights
status, NC attribution).
Filename: `nc-[collection-slug]-[work-slug]-educational.jpg`

Download path: One click from the product page or the educators page. No login. No
payment. No friction.

**Tier 2 — NC Educational License (free, for institutional materials):**

Schools and universities wishing to use NC illustrations in published educational
materials (textbooks, curriculum packs, institutional websites, printed course readers)
may apply for a formal NC Educational License.

License terms:
- Free for public educational institutions
- Attribution required: "Image: [Work Title], [Creator]. From the collection of
  [Institution]. Via Nature & Culture (nc.art). Public domain."
- Limited to non-commercial educational materials
- Issued per institution, renewable annually
- No restriction on number of works or materials per license
- NC reserves the right to list the institution as an educational partner (opt-out
  available)

Application: A 3-field form on the educators page (institution name, contact email,
intended use). 5 business day response.

### Educational Licensing Data Model

```
educational_license {
  license_id:         string    // NC-EDU-NNN
  institution_name:   string
  institution_type:   enum      // primary | secondary | tertiary | nonprofit
  contact_email:      string
  contact_name:       string
  intended_use:       text
  issued_date:        date
  expiry_date:        date      // issued_date + 1 year
  status:             enum      // pending | active | expired | revoked
  listed_as_partner:  boolean
}
```

### Display Specification

**Product page — educational badge (always visible):**
```
[FOR EDUCATORS]
Public domain · Free to use in your classroom.
→ Download educational resolution (free)
→ Educator resources for this collection
```

**Educators page** (`/educators`):

```
Nature & Culture for Educators

Every illustration on this platform is in the public domain.
No permission. No payment. No licensing required for educational use.

[Three columns:]

FREE DOWNLOADS          EDUCATOR RESOURCES       INSTITUTIONAL LICENSE
──────────────          ──────────────────       ────────────────────
Download any NC         Context guides for       For schools using NC
illustration at         5 signature              images in published
educational             collections. Discussion  materials: free annual
resolution.             questions. Curriculum    license with attribution.
No account needed.      alignment notes.
→ Browse all           → Download resources     → Apply (3 fields)
  downloads
```

**Curriculum context guide format (one per signature collection):**

```
Nature & Culture Educator Resource: [Collection Name]

THE PLACE           [3 sentences: where, why significant, today]
THE ILLUSTRATOR     [3 sentences: who, when, what they were doing]
THE WORKS           [3 sentences: what the images show, why significant]
THE HISTORICAL      [3 sentences: what was happening in the world
MOMENT              when these were made]

DISCUSSION QUESTIONS
1. [For secondary: close-looking question about the illustration]
2. [For secondary: contextual question connecting art to history/science]
3. [For tertiary: interpretive question about the PD value chain]

CURRICULUM CONNECTIONS
History:    [Subject area + year group suggestion]
Biology:    [Subject area + year group suggestion, where relevant]
Art/Design: [Subject area + year group suggestion]
Geography:  [Subject area + year group suggestion]

FURTHER READING
[2–3 verifiable external sources: institution pages, not Wikipedia]

Rights note: All images are in the public domain. Download freely for
classroom use at nc.art/educators.
```

### Accessibility Statement

NC is required to publish an accessibility statement before any institutional
educational adoption can occur. The statement must be published at `/accessibility`
and must include:
- WCAG standard targeted (2.1 AA)
- Current conformance level (partial / full)
- Known limitations and remediation timeline
- Contact for accessibility concerns

If the WCAG audit has not been completed, the statement should read:
*"Nature & Culture is committed to WCAG 2.1 AA conformance. A formal accessibility
audit is [scheduled / in progress]. This statement will be updated with findings and
remediation timeline by [date]. To report an accessibility concern, contact [email]."*

A placeholder accessibility statement that acknowledges the gap is better than no
statement. It is required before any formal educational outreach.

### Operational Requirements

- Educational download must be available for every product at Gate E.
- Educational downloads must be served from a non-commerce URL path (i.e., not behind
  a paywall, not requiring cart interaction).
- Educational license applications must be reviewed within 5 business days.
- Context guides for the 5 signature collections must be complete before the first
  educational outreach or press coverage.
- Accessibility statement must be published before any educational institution
  partnership is announced.

---

## Implementation Sequence

**Phase 0 — Minimum institutional personhood (pre-Gate E):**
1. Name a curator (IR-001). Publish one curator profile page.
2. Write and publish PD explainer (`/about/public-domain`) (IR-002).
3. Add institution block to all product pages with institution name + source link (IR-004).
4. Define certificate fields. Issue first certificate for NC-PROD-001. (IR-003)

**Phase 1 — Collector-grade documentation (pre-public launch):**
5. Build edition registry (database + public verification page) (IR-005).
6. Add provenance block to all product pages (collapsed) (IR-002, IR-017).
7. Add bylines to all collection editorial content (IR-008).
8. Add print specification section to all physical product pages (IR-006, IR-011).
9. Publish editorial corrections policy (IR-012).

**Phase 2 — Educational and scholarly layer (post-launch):**
10. Build educators page with free download path (IR-010).
11. Commission WCAG audit. Publish accessibility statement with timeline (IR-009).
12. Write context guides for 5 signature collections (IR-013).
13. Launch educational license program (IR-019).
14. Build institution pages for all Tier 1 partners (IR-004 deep).

**Phase 3 — Full institutional architecture (ongoing):**
15. Publish public-facing governance standards summary (IR-007).
16. Build institutional history and founding narrative page (IR-016).
17. Establish NC Founding Collectors program (IR-014).
18. Request logo permissions from all Tier 1 institutions.
19. Build `works/[slug]/provenance` deep provenance pages for signature collections.

---

## Open Actions

| # | Action | System | Phase | Priority |
|---|---|---|---|---|
| OA-1 | Name and publish a curator. One page, one bio, one curatorial statement per collection. | Curator | Phase 0 | **Critical** |
| OA-2 | Write PD explainer page (`/about/public-domain`). 3 paragraphs. Plain language. | Provenance | Phase 0 | **Critical** |
| OA-3 | Add institution block (name + source record URL) to every product page | Institution | Phase 0 | **Critical** |
| OA-4 | Design and issue first certificate of authenticity for NC-PROD-001 | Certificate | Phase 0 | **Critical** |
| OA-5 | Build edition registry (DB schema + `/verify` page) | Edition Registry | Phase 1 | **Critical** |
| OA-6 | Add provenance block (collapsed) to all product pages | Provenance | Phase 1 | **High** |
| OA-7 | Add bylines to all collection and place editorial copy | Editor | Phase 1 | **High** |
| OA-8 | Add print specification section to physical product pages | Certificate | Phase 1 | **High** |
| OA-9 | Publish editorial corrections policy | Editor | Phase 1 | **High** |
| OA-10 | Build `/educators` page with free educational resolution download | Educational | Phase 2 | **High** |
| OA-11 | Publish WCAG accessibility statement (audit result or interim placeholder) | Educational | Phase 2 | **High** |
| OA-12 | Write context guides for 5 signature collections | Educational | Phase 2 | Medium |
| OA-13 | Request logo permissions from NHM, NGA, CMA, Walters, Met | Institution | Phase 2 | Medium |
| OA-14 | Build institution pages for all Tier 1 partners | Institution | Phase 2 | Medium |
| OA-15 | Publish founding narrative and governance summary | Curator / Editor | Phase 3 | Medium |

---

*NC-TRUST-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
