# NC-WEB-004: Experience Blueprint

| Field | Value |
|---|---|
| Document | NC-WEB-004 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | NC-EXPERIENCE-001 · NC-WEB-001 · NC-PRODUCT-001 · Wireframe Constitution v1 |
| Governs | Visitor-facing design, copy, and interaction for all five Phase 0/1 public pages |
| Scope | Homepage v2 · Earthrise Story v2 · Earthrise Product v2 · Collection Page v1 · Places Index v2 |
| NC-COLLECTIONS-001 | **DOES NOT EXIST** — this document creates the collection page template; NC-COLLECTIONS-001 must be drafted as a governance document before Phase 1 collection activation |

---

## I. Purpose

NC-WEB-004 translates the strategic intent of NC-EXPERIENCE-001 into concrete, page-by-page design specifications. It defines what appears above the fold on every page, what gets removed, what gets hidden from customers, and what specific elements should create wonder, trust, and desire.

This document does not produce code. It produces design decisions. Every decision is constrained by NC-WEB-001 (attribution invariants), NC-PRODUCT-001 (product governance), and NC-EXPERIENCE-001 (experience principles XP-1 through XP-5).

**The core problem this document solves:** The current site is a governance skeleton rendered as a visitor experience. It communicates in the language of internal operations — phase labels, manual purchase forms, status codes, and compliance copy — while delivering no emotional experience. A visitor who arrives at the current homepage learns that NC has completed its attribution verification procedures. They do not feel anything about it.

**The solution:** Make the governance invisible and make the illustration central.

---

## II. Current Site Audit

### Overall Verdict: Functional skeleton. Zero emotional register.

The current site correctly implements every governance requirement. Every attribution string is present. Every rights badge appears. Every prohibited phrase is absent. The governance architecture works.

The visitor experience does not. The site reads as an internal tool that forgot to put on clothes before going public.

### Page-by-Page Findings

#### Homepage (`/`) — CRITICAL

| Element | Problem | Classification |
|---|---|---|
| Eyebrow: "Phase 0 public launch" | Internal governance label rendered as a marketing headline | **Remove** |
| Headline: "Earthrise, with provenance visible." | Technically accurate, emotionally inert | **Rewrite** |
| Lead: "Nature & Culture publishes public-domain heritage stories and products only after rights, source, and attribution checks are visible on the page." | Compliance language as a value proposition | **Replace** |
| Hero media: CSS gradient `<div>` | Placeholder where the most significant photograph of the 20th century should be | **Replace with real image** |
| Product grid: shows `NC-PROD-001`, `NC-PROD-008` | Internal product codes as visitor-facing headings | **Remove codes, keep titles** |
| Place cards: "Coming soon" / "Live Phase 0" status | Internal governance state exposed to visitors | **Remove status labels** |
| Attribution block: `EarthriseAttributionBlock` inline in body | Compliance text in the main content flow, styled as body copy | **Redesign and reposition** |
| Products section heading: "Phase 0 products" | Internal phase language | **Rewrite or remove section** |

#### Earthrise Story Page (`/stories/earthrise`) — MODERATE

| Element | Problem | Classification |
|---|---|---|
| Hero media: CSS gradient `<div>` | Same placeholder problem as homepage | **Replace with real image** |
| `heroText` fallback: just "Earthrise" | Fallback is a single word — not a headline | **Write curated fallback** |
| `storyText` fallback: 1 sentence | Inadequate for a story page — reads as a stub | **Write 800-word curated copy** |
| `educationText` fallback | Generic, no specific information value | **Replace with editorial voice** |
| Section: "Own Earthrise" | Section title is commerce framing but could be richer | **Revise to narrative** |
| CTA: "Shop the Phase 0 Earthrise product family through manual purchase." | Dual violation: "Phase 0" and "manual purchase" | **Rewrite** |

#### Earthrise Product Page (`/products/earthrise`) — CRITICAL

| Element | Problem | Classification |
|---|---|---|
| Eyebrow: "NC-PROD-001 / NC-PROD-008" | Internal product codes as the first words a visitor reads | **Remove entirely** |
| Hero media: CSS gradient `<div>` | No actual illustration on a product page | **Replace with real image** |
| Badge: "Certificate of Authenticity" | Present but not explained or designed — reads as a bullet point | **Build as a feature** |
| `ManualPurchaseCTA` eyebrow: "Manual purchase" | The word "manual" is internal operations language | **Remove "manual"** |
| `ManualPurchaseCTA` headline: "Request purchase" | Weak commerce framing — implies uncertainty | **Replace with "Enquire" or "Reserve"** |
| Rights details: full paragraph + "Source: NASA. Asset ID: AS08-14-2383. Human verified: yes." | Valuable information rendered as raw data | **Redesign as provenance panel** |
| Attribution block: inline after rights details | Two separate attribution treatments on one page | **Consolidate into provenance panel** |
| Variant display: two cards in a grid | No clear variant hierarchy — Gicléé and Digital look identical | **Build as a selector** |

#### Places Page (`/places`) — MODERATE

| Element | Problem | Classification |
|---|---|---|
| Lead: "Phase 0 keeps place pages as governed previews while source authority gates complete." | Full governance explanation as visitor copy | **Remove entirely** |
| Place cards: "Coming soon" / "Live Phase 0" | Status labels in the visitor layer | **Remove status, add visual richness** |
| No visual content | Place cards are text-only — no illustration, no atmosphere | **Add illustration thumbnails** |

#### Products Page (`/products`) — CRITICAL

| Element | Problem | Classification |
|---|---|---|
| Headline: "Phase 0 products" | Phase label as page title | **Rewrite** |
| Lead: "Earthrise is the only public product family in Phase 0. Manual purchase is enabled after governed verification." | Two violations in two sentences | **Replace** |
| Badge: "Manual purchase" on every card | Internal operations label on a commerce page | **Remove** |
| Phase eyebrow on every card: "Phase 0" | Internal label | **Remove** |

#### About Page (`/about`) — MODERATE

| Element | Problem | Classification |
|---|---|---|
| Headline: "Public-domain commerce with visible provenance." | Technically correct, not compelling | **Rewrite as editorial narrative** |
| Three cards: "Public domain first" / "Rights verification" / "Attribution visible" | Compliance bullets, not a story | **Rebuild as "How We Work" section** |

---

## III. The Three Registers

Every design decision in this document should serve one or more of three emotional registers. These are not marketing categories — they are visitor states that drive behavior.

### Wonder

**What creates wonder at NC:**
- An 1878 illustration of a coral formation so detailed you can count the polyps
- The Earthrise photograph at full screen — the whole Earth from 240,000 miles away
- A timeline that reveals: "This is what the world knew about Yellowstone in 1872 — before photographs"
- Deep zoom into a Haeckel plate, watching brushstrokes from 150 years ago appear
- The contrast between a satellite image and the illustration made at the same place 200 years earlier
- The unexpected: a commerce platform that shows all its verification work

**Wonder must appear:** Above the fold on every page. The visitor must feel something before they read anything.

### Trust

**What creates trust at NC:**
- A rights badge on every asset, always visible — not a disclaimer, a mark of quality
- MASTERWORK / FLAGSHIP / STANDARD as curatorial tiers, displayed as designed badges
- The source institution name and mark — "NASA" with the NASA insignia, not just text
- A Human Verified checkmark — not a checkbox, a designed iconographic mark
- Progressive provenance: one click reveals the full chain from photograph to product
- Design quality itself — a well-made page signals a well-made institution
- The Certificate of Authenticity shown as a designed object, not a PDF afterthought

**Trust must appear:** On every asset surface, at Level 0 (always visible) and Level 2 (click to expand).

### Desire

**What creates desire at NC:**
- The illustration at wall scale — showing how a 24×20 inch Earthrise print occupies a room
- Edition framing: "Museum Gicléé — a limited archival edition"
- Quality tier as scarcity: MASTERWORK is not an internal threshold, it is a mark of distinction
- Provenance as value: "This is the verified, source-traced, human-authenticated edition"
- Cross-discovery: the visitor who reads the Earthrise story arrives at the product page already wanting it
- The unavailability of certain things (deferred place pages) makes the available things more precious

**Desire must appear:** On product pages above the fold, in the commerce module of every place and story page, in the quality tier badge system.

---

## IV. Design System Foundations

The current CSS (`styles.css`) has a solid foundation. These additions are required before the five page designs can be built.

### Typography

**Current state:** Inter only (geometric sans-serif). Adequate for UI. Insufficient for editorial.

**Required addition:** A serif companion for headlines, story bodies, and illustration titles.

Recommended candidates (in order of preference):
1. **Cormorant Garamond** — free, Google Fonts, historically resonant, high elegance ceiling
2. **Tiempos Headline** — commercial, used by NatGeo, excellent large size
3. **Playfair Display** — free, widely used, good fallback

CSS addition:
```css
--font-serif: "Cormorant Garamond", Georgia, "Times New Roman", serif;
--font-sans: Inter, ui-sans-serif, system-ui, sans-serif;   /* already present */
```

**Rule:** All editorial headlines (h1 on story/collection pages), illustration titles, place names, and pull quotes use `--font-serif`. All UI, navigation, badges, prices, and metadata use `--font-sans`.

### Color System Extension

**Current tokens (keep):** `--ink`, `--muted`, `--line`, `--paper`, `--panel`, `--accent`, `--accent-dark`, `--gold`

**Required additions:**

```css
/* Quality tier badge colors */
--tier-masterwork: #b37a2b;       /* = --gold, re-use */
--tier-masterwork-bg: #fdf6e9;
--tier-flagship: #6b7280;         /* silver-slate */
--tier-flagship-bg: #f3f4f6;
--tier-standard: #374151;
--tier-standard-bg: #f9fafb;
--tier-reference: #9ca3af;
--tier-reference-bg: #f9fafb;

/* Rights badge colors */
--rights-pd: #1e3a5f;             /* navy for §105 */
--rights-pd-bg: #eef2f7;
--rights-cc0: #14532d;            /* deep green for CC0 */
--rights-cc0-bg: #f0fdf4;

/* Hero overlay */
--hero-overlay: rgb(0 0 0 / 0.28);

/* Translucent header */
--header-glass: rgb(251 250 246 / 0.88);
```

### Spacing and Layout

**Add to CSS:**
```css
:root {
  --content-max: 1280px;
  --prose-max: 780px;
  --hero-height: 100svh;
}
```

**Translucent sticky header pattern:**
```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
  background: var(--header-glass);
  border-bottom: 1px solid var(--line);
}

/* On hero pages: header overlays the image */
.page--has-hero .site-header {
  position: absolute;
  width: 100%;
  background: transparent;
  backdrop-filter: none;
  border-bottom: none;
}
/* becomes sticky after hero scrolls out of view — requires IntersectionObserver */
```

### Badge Component System

Four badge variants replace the current single `.badge` class:

```css
.badge--masterwork { background: var(--tier-masterwork-bg); color: var(--tier-masterwork); border-color: var(--tier-masterwork); }
.badge--flagship   { background: var(--tier-flagship-bg);   color: var(--tier-flagship);   border-color: var(--tier-flagship); }
.badge--standard   { background: var(--tier-standard-bg);   color: var(--tier-standard);   border-color: var(--tier-standard); }
.badge--pd         { background: var(--rights-pd-bg);       color: var(--rights-pd);       border-color: var(--rights-pd); }
.badge--cc0        { background: var(--rights-cc0-bg);      color: var(--rights-cc0);      border-color: var(--rights-cc0); }
.badge--verified   { background: #f0fdf4; color: #15803d; border-color: #15803d; }  /* Human Verified */
```

---

## V. Page Designs

### V.1 Homepage v2

#### Above the Fold

```
┌──────────────────────────────────────────────────────────────────┐
│  Nature & Culture       Places · Stories · Collections · Shop    │  ← translucent header over hero
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│                                                                  │
│         ┌────────────────────────────────────────┐              │
│         │                                        │              │
│         │   EARTHRISE PHOTOGRAPH                 │              │
│         │   (actual image, full bleed,           │              │
│         │    width: 100vw, height: 100svh)        │              │
│         │                                        │              │
│         │                                        │              │
│         │                                        │              │
│         └────────────────────────────────────────┘              │
│  ┌ editorial overlay, bottom-left, max-width 560px ───────────┐ │
│  │ The illustrated record                                      │ │
│  │ of Earth's great places.         [Explore Earthrise →]     │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  NASA · Apollo 8 · December 24, 1968 · Public Domain             │  ← single credit line
└──────────────────────────────────────────────────────────────────┘
```

**Headline rule:** Maximum 8 words. No governance language. No phase references. Serif typeface at `clamp(3.2rem, 7vw, 6rem)`, white, on dark portion of image.

**CTA:** Ghost button (white outline, white text). Not filled green — does not compete with the photograph.

**Credit line:** Single line, bottom-left, `--font-sans`, 0.72rem, white at 70% opacity. This is the Level 0 attribution (always visible, non-intrusive). The full `EarthriseAttributionBlock` content moves to the provenance panel on the product page.

#### Below the Fold

**Section 2 — Editorial Lead** (`--paper` background, `padding: clamp(56px, 8vw, 96px)`)

```
For two hundred and fifty years, the world's greatest naturalists
documented Earth's wild places in painstaking detail — plates,
maps, and field illustrations that captured what science knew
before photography existed.

Those works are now public domain. Nature & Culture has verified,
placed, and made them available for the first time in one
collection.
```

Two paragraphs. Maximum 100 words combined. No governance language. No phase references. `--prose-max` width. Serif typeface for body.

**Section 3 — Featured Story** (full-width editorial card)

```
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────┐  Stories                      │
│  │                              │                               │
│  │   EARTHRISE PHOTOGRAPH       │  Earthrise                    │
│  │   (300–400px height)         │                               │
│  │                              │  On December 24, 1968,        │
│  │                              │  William Anders looked        │
│  │                              │  out the window of           │
│  │                              │  Apollo 8 and took          │
│  │                              │  the most reproduced         │
│  │                              │  photograph in history.      │
│  └──────────────────────────────┘                               │
│                                  [Read the story →]             │
│                                  [Shop Earthrise →]             │
└─────────────────────────────────────────────────────────────────┘
```

**Section 4 — Discovery Entry Points** (3 equal columns)

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  By Place        │  │  By Illustrator  │  │  By Era          │
│                  │  │                  │  │                  │
│  Yellowstone     │  │  Haeckel         │  │  1750 – 1900     │
│  Grand Canyon    │  │  Gould           │  │  Golden Age of   │
│  Great Barrier   │  │  Audubon         │  │  Natural History │
│  Reef            │  │  Nodder          │  │  Illustration    │
│  Galápagos       │  │  Merian          │  │                  │
│                  │  │  Redouté         │  │  [Explore →]     │
│  [All places →]  │  │  [All →]         │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

Phase 1 only: illustrator pages and era pages are real links. Phase 0: "All places →" links to `/places`, others are visual only.

**Section 5 — Places Coming to NC** (editorial teaser, no status labels)

```
┌─────────────────────────────────────────────────────────────────┐
│  More places arriving                                           │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ [illus.] │  │ [illus.] │  │ [illus.] │  │ [illus.] │       │
│  │          │  │          │  │          │  │          │       │
│  │Yellowstone│  │Grand     │  │Great     │  │Galápagos │       │
│  │          │  │Canyon    │  │Barrier   │  │          │       │
│  │          │  │          │  │Reef      │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

Each card shows the best available illustration for that place (governed, from existing assets). No "Coming soon" label. No status. No phase. Cards are not clickable in Phase 0 — or link to a non-existent page with a simple "This place is arriving soon" one-liner.

#### What Is Removed from Homepage

| Removed element | Current location | Reason |
|---|---|---|
| "Phase 0 public launch" eyebrow | Hero | Internal governance label |
| Governance lead copy | Hero | Compliance language as value proposition |
| CSS gradient hero-media | Hero | Placeholder — not a visitor-facing design element |
| "Phase 0 products" section heading | Body | Internal label |
| Product grid (two product cards) | Body | Commerce belongs on product/story pages, not homepage |
| Place cards with status labels | Body | Status labels exposed to visitors |
| `EarthriseAttributionBlock` | Body | Full attribution block redesigned as Level 0 credit line |

---

### V.2 Earthrise Story Page v2

#### Above the Fold

```
┌──────────────────────────────────────────────────────────────────┐
│  Nature & Culture       ← Stories    (translucent header)       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   EARTHRISE PHOTOGRAPH — FULL BLEED, 100svh                      │
│   (slightly darker overlay than homepage — this is a story,     │
│    not an index. The image is the opening chapter.)              │
│                                                                  │
│                                                                  │
│  ┌ pull quote overlay, bottom third ─────────────────────────┐  │
│  │                                                            │  │
│  │  "We came all this way to explore the Moon, and the most  │  │
│  │   important thing is that we discovered the Earth."        │  │
│  │                               — William Anders, 1968       │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  NASA · William Anders · Apollo 8 · December 24, 1968 · §105    │  ← credit line
└──────────────────────────────────────────────────────────────────┘
```

**Pull quote:** The Anders quote is the single most powerful piece of copy available for this page. It is historically documented, not AI-generated, and it does more editorial work than any headline NC could write. It should be in the large serif typeface.

#### Story Body (below fold)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Earthrise                                                     │
│   ─────────────────────────────────────────────────────         │
│   (serif h1, left-aligned, max-width: --prose-max)             │
│                                                                 │
│   [800–1200 words of editorial narrative]                       │
│                                                                 │
│   Phase 0: Curated copy (see §VI below)                         │
│   Phase 1+: AI-generated, graph-grounded, human-reviewed        │
│             via getReviewedPageGeneration("story", "earthrise") │
│                                                                 │
│   Content arc:                                                  │
│   · The mission context — what Apollo 8 was for                 │
│   · The moment — December 24, 1968, orbital mechanics           │
│   · Anders' decision — 70mm Hasselblad, color film, impulsive  │
│   · The image — why it looked different from everything before  │
│   · The cultural impact — Sierra Club, Earth Day, the shift     │
│   · The public domain status — §105, what it means for access   │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  [EARTHRISE — inline image, narrower, 600px max-width]   │  │
│   │  NASA · Apollo 8 · December 24, 1968 · Public Domain     │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│   (story continues...)                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Commerce Module (end of story)

```
┌─────────────────────────────────────────────────────────────────┐
│  Own Earthrise                                                  │
│  ─────────────────────────────────────────────────────          │
│  A museum-grade edition of the most significant photograph      │
│  taken by any human being. Verified source, public domain,      │
│  archival quality.                                              │
│                                                                 │
│  ┌────────────────────────────┐  ┌────────────────────────────┐ │
│  │  [EARTHRISE thumbnail]     │  │  [EARTHRISE thumbnail]     │ │
│  │                            │  │                            │ │
│  │  Earthrise                 │  │  Earthrise                 │ │
│  │  Museum Gicléé             │  │  Digital Download          │ │
│  │  24 × 20 in · Archival     │  │  High resolution · Instant │ │
│  │  ◆ MASTERWORK              │  │  ◆ MASTERWORK              │ │
│  │  [View product →]          │  │  [View product →]          │ │
│  └────────────────────────────┘  └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### Attribution (end of page)

```
┌─────────────────────────────────────────────────────────────────┐
│  ─────────────────────────────────────────────────────          │
│  NASA: Photograph by William Anders, Apollo 8,                  │
│  December 24, 1968. 17 U.S.C. § 105 — public domain.           │
│  Image credit: NASA. NASA does not endorse this product.        │
└─────────────────────────────────────────────────────────────────┘
```

This is the `EarthriseAttributionBlock` — but rendered as a designed museum-label element (thin top border, muted background, small type) rather than a `<section>` with default paragraph styling.

#### What Is Removed from Story Page

| Removed | Reason |
|---|---|
| "Story" eyebrow (acceptable to keep, but lower priority) | Replace with breadcrumb `Stories / Earthrise` |
| CSS gradient hero-media | Replace with real image |
| Generic `storyText` fallback | Replace with curated Phase 0 copy |
| "Shop the Phase 0 Earthrise product family through manual purchase." | Both "Phase 0" and "manual purchase" — rewrite as above |
| Section title "Own Earthrise" (plain) | Keep title, redesign section |

#### Phase 0 Curated Copy (hardcoded fallback)

Until `getReviewedPageGeneration("story", "earthrise")` returns `publication_allowed: true`, the page must render something other than a one-word title and a single generic sentence. The following is the governed Phase 0 copy (permanent fallback, human-authored, no AI involvement):

> On December 24, 1968, astronaut William Anders looked out the window of Apollo 8 as the spacecraft emerged from behind the Moon and saw Earth rising above the lunar horizon. He grabbed a 70mm Hasselblad camera loaded with color film and took the photograph that would become known as Earthrise.
>
> It was an accident. The crew had not planned to photograph the Earth. The mission was to photograph potential Apollo landing sites on the lunar surface. But the image Anders captured in that moment — the whole Earth, small and bright and fragile against the blackness of space — became one of the most reproduced photographs in history and a defining image of the environmental movement.
>
> The photograph is a work of the United States federal government, created by a government employee in the course of official duties. Under 17 U.S.C. § 105, it entered the public domain at the moment of creation. It has never been subject to copyright. Nature & Culture has verified this status, traced the image to its source record at NASA (AS08-14-2383), and presents it here with full attribution visible.

This copy belongs in `governed-content.ts` as `EARTHRISE_STORY_FALLBACK`, not hardcoded in the component.

---

### V.3 Earthrise Product Page v2

#### Above the Fold (split screen)

```
┌─────────────────────────────────────────────┬─────────────────┐
│                                             │                 │
│                                             │  Earthrise      │
│                                             │                 │
│   EARTHRISE PHOTOGRAPH                      │  ◆ MASTERWORK   │
│   (full height of viewport,                 │                 │
│    60% width)                               │  Museum Gicléé  │
│                                             │  24 × 20 in     │
│   Zoomable — cursor:zoom-in,               │  Archival paper  │
│   on click: lightbox/deep zoom             │                 │
│                                             │  ● PD  §105     │
│                                             │  ✓ Human Verified│
│                                             │  NASA · 1968    │
│                                             │                 │
│                                             │  [Enquire →]    │
│                                             │                 │
│                                             │  Also available:│
│                                             │  [Digital Download]│
│                                             │                 │
└─────────────────────────────────────────────┴─────────────────┘
```

**Key decisions on this section:**

- **No internal product codes** (`NC-PROD-001`) in the visitor layer. These are system identifiers, not product names. The product name is "Earthrise Museum Gicléé."
- **"Enquire"** replaces "Request purchase" and "Manual purchase." Enquire is used in museum shops, gallery contexts, and high-value art commerce. It implies seriousness without exposing operational detail.
- **MASTERWORK badge** is the first quality signal — it appears at the top of the commerce panel, above the price. It communicates curatorial judgment before any copy is read.
- **PD badge** (`● PD  §105`) replaces the full "Public domain" badge text. The circle and the legal citation are the visual language of the rights system.
- **Human Verified mark** (✓) is a distinct iconographic element — not a checkbox, not a green badge — that communicates curator approval.
- **Image zoom** is essential. The visitor should be able to examine the photograph at high resolution. This is the Google Arts & Culture model: resolution is a form of reverence.

#### Below the Fold

**Section 1 — The Illustration Story** (`--prose-max` width, serif body)

```
On Christmas Eve, 1968, from 240,000 miles above the lunar
surface, William Anders photographed something no human
being had ever seen with their own eyes: the entire Earth
from the outside.

The image is not technically complex. It is formally
beautiful — a crescent of blue and white against black,
hovering above a grey lunar horizon. But what makes it
significant is what it is of, and when.

[200–400 words. Phase 0: curated. Phase 1+: AI-generated.]
```

**Section 2 — Variants** (selector, not a grid of identical cards)

```
┌─────────────────────────────────────────────────────────────────┐
│  Choose your edition                                            │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  ● Museum Gicléé             Digital Download                   │
│    24 × 20 inches            High-resolution file               │
│    Archival pigment inks     300 DPI · TIFF format              │
│    Hahnemühle Photo Rag      Instant delivery                   │
│    Certificate of Authenticity                                  │
│                                                                 │
│  [Enquire about Museum Gicléé →]                                │
└─────────────────────────────────────────────────────────────────┘
```

**Section 3 — Provenance Panel** (progressive disclosure)

```
┌─────────────────────────────────────────────────────────────────┐
│  Provenance                                                     │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  NASA · Photograph by William Anders · Apollo 8                 │
│  December 24, 1968 · AS08-14-2383 · §105 · Human Verified       │
│                                                                 │
│  [+ See full record]  ← click expands the panel below          │
│                                                                 │
│  ┌ expanded (hidden by default) ──────────────────────────────┐ │
│  │  Rights basis: 17 U.S.C. § 105 — United States Government  │ │
│  │  Work. Created by a federal employee in official duties.    │ │
│  │  Not subject to copyright. Public domain at creation.       │ │
│  │                                                             │ │
│  │  Source institution: NASA                                   │ │
│  │  Original record: NASA Image and Video Library              │ │
│  │  Asset ID: AS08-14-2383                                     │ │
│  │  Human verification: Completed · Gate 8                     │ │
│  │                                                             │ │
│  │  Image credit: NASA. NASA does not endorse this product.    │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Section 4 — Certificate of Authenticity**

```
┌─────────────────────────────────────────────────────────────────┐
│  Certificate of Authenticity                                    │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  Every Museum Gicléé edition ships with a Certificate of        │
│  Authenticity that records the source institution, asset ID,    │
│  rights status, edition number, and verification date.          │
│                                                                 │
│  [Preview certificate →]  ← opens a designed CoA mockup        │
└─────────────────────────────────────────────────────────────────┘
```

**Section 5 — From the Story**

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Read the Earthrise story                                     │
└─────────────────────────────────────────────────────────────────┘
```

#### What Is Removed from Product Page

| Removed | Replaced with |
|---|---|
| Eyebrow "NC-PROD-001 / NC-PROD-008" | Nothing — the product name is the headline |
| CSS gradient hero-media | Actual Earthrise photograph, zoomable |
| Badge "Certificate of Authenticity" (bullet in a badge row) | Section with description (Section 4 above) |
| `ManualPurchaseCTA` eyebrow "Manual purchase" | Removed entirely |
| `ManualPurchaseCTA` headline "Request purchase" | "Enquire about Museum Gicléé" |
| "A manual invoice and fulfillment details will follow after review." | Hidden from visitor layer. Operational detail. |
| Full `EarthriseAttributionBlock` inline | Consolidated into Provenance Panel (Section 3) |
| Two-card grid for variants | Selector (Section 2) |

---

### V.4 Collection Page v1

**Governance note:** NC-COLLECTIONS-001 does not exist. This page design creates the template pattern. NC-COLLECTIONS-001 must be drafted as a governance document defining: collection eligibility criteria, collection naming convention, minimum illustration count per collection, curator approval requirements, and permitted commerce surfaces.

**Phase 0 collection:** "Earthrise" — one illustration. The proof of concept. This is intentional: a collection of one MASTERWORK illustration is a stronger statement than a grid of assets. It establishes the format.

**URL:** `/collections/earthrise`

**Navigation:** `Collections` → `Earthrise`

#### Above the Fold

```
┌──────────────────────────────────────────────────────────────────┐
│  Nature & Culture       Collections    (translucent header)     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   EARTHRISE PHOTOGRAPH — FULL BLEED                              │
│   (same image, distinct treatment from story page:              │
│    overlay is slightly lighter, more "gallery" than "cinema")   │
│                                                                  │
│                                                                  │
│  ┌ overlay, lower third ──────────────────────────────────────┐ │
│  │  Collections                                               │ │
│  │                                                            │ │
│  │  Earthrise                                                 │ │  ← serif, large
│  │  ─────────────────────────────────                         │ │
│  │  A single image. The whole world.                          │ │  ← editorial thesis
│  │                                                            │ │
│  │  1 work  ·  ◆ MASTERWORK  ·  NASA  ·  1968  ·  PD         │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

#### Collection Body

**Section 1 — Collection Editorial** (300–500 words, `--prose-max`)

```
This is the first collection published by Nature & Culture.
It contains one work.

That is not a limitation — it is the statement. Earthrise is
the most widely reproduced photograph in history, a work
of the United States federal government, public domain
at the moment of creation, and the starting point for
everything NC will publish.

Every collection that follows this one — the Golden Age of
Natural History Illustration, the North American Survey
expeditions, the Pacific voyages — begins here. A single
image that made the whole Earth visible as a place.

[Phase 0: curated copy · Phase 1+: AI-generated via NC-AI-001]
```

**Section 2 — Collection Gallery**

```
┌─────────────────────────────────────────────────────────────────┐
│  Works in this collection                      1 work           │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  [EARTHRISE — large, full-width card]                     │  │
│  │                                                           │  │
│  │  Earthrise                              ◆ MASTERWORK      │  │
│  │  William Anders · NASA · 1968           ● PD  §105        │  │
│  │                                         ✓ Human Verified  │  │
│  │  [View illustration →]   [Available as Museum Gicléé →]   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Section 3 — Shop This Collection**

```
┌─────────────────────────────────────────────────────────────────┐
│  Shop this collection                                           │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  ┌────────────────────────────┐  ┌────────────────────────────┐ │
│  │  [EARTHRISE thumbnail]     │  │  [EARTHRISE thumbnail]     │ │
│  │  Earthrise                 │  │  Earthrise                 │ │
│  │  Museum Gicléé             │  │  Digital Download          │ │
│  │  24 × 20 in · Archival     │  │  High resolution           │ │
│  │  ◆ MASTERWORK              │  │  ◆ MASTERWORK              │ │
│  │  [Enquire →]               │  │  [Enquire →]               │ │
│  └────────────────────────────┘  └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Section 4 — Coming collections** (editorial teaser, Phase 1 ready)

```
┌─────────────────────────────────────────────────────────────────┐
│  More collections arriving                                      │
│  ─────────────────────────────────────────────────────          │
│                                                                 │
│  The Golden Age of Natural History Illustration                 │
│  Audubon · Haeckel · Gould · Merian · Nodder · Redouté          │
│                                                                 │
│  North American Surveys                                         │
│  Hayden, Powell, and the expeditions that first documented     │
│  Yellowstone and the Grand Canyon                               │
│                                                                 │
│  Expedition Pacific                                             │
│  Cook voyages through Apollo — the Pacific documented          │
│  across 200 years of science and exploration                   │
└─────────────────────────────────────────────────────────────────┘
```

These are editorial cards, not links. Phase 0: no links. Phase 1: each becomes a real collection page.

---

### V.5 Places Index v2

#### Above the Fold

```
┌──────────────────────────────────────────────────────────────────┐
│  Nature & Culture       Places    (translucent header)          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Great places leave records.                                     │
│  We found them.                                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────          │
│                                                                  │
│  [Search places...]                                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Headline:** Two short sentences, serif, editorial register. No governance language. No phase reference. Above the fold but not full-bleed — this is an index, not a landing page. The visual richness comes from the place cards below.

**Search:** A visible search input, even at Phase 0 when it has only one live result. The search input communicates a platform, not a stub.

#### Below the Fold

**Featured Place — Earthrise** (full width, hero card)

```
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  [EARTHRISE PHOTOGRAPH — 480px height, full card width]  │   │
│  │                                                          │   │
│  │  Earthrise                                               │   │
│  │  ─────────────────────────                               │   │
│  │  The Apollo 8 photograph of Earth rising above           │   │
│  │  the Moon. The most reproduced image in history.         │   │
│  │                                                          │   │
│  │  ◆ MASTERWORK  ·  NASA  ·  1968  ·  PD                   │   │
│  │                                                          │   │
│  │  [Explore Earthrise →]    [Shop →]                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Upcoming Places Grid** (2 × 2, or 4-column on wide screens)

Each card:
- Best available illustration for that place (governed assets — e.g., NASA satellite for Yellowstone, Powell Survey for Grand Canyon)
- Place name in serif
- One-sentence editorial description
- No "Coming soon" label — the absence of a CTA communicates the state without exposing it
- No phase label
- No status field

```
┌────────────────────────┐  ┌────────────────────────┐
│  [SATELLITE IMAGE]     │  │  [POWELL SURVEY PLATE] │
│                        │  │                        │
│  Yellowstone           │  │  Grand Canyon          │
│                        │  │                        │
│  The world's first     │  │  Carved by the         │
│  national park,        │  │  Colorado River over   │
│  documented from       │  │  six million years,    │
│  1869 to the present.  │  │  first surveyed 1869.  │
│                        │  │                        │
└────────────────────────┘  └────────────────────────┘

┌────────────────────────┐  ┌────────────────────────┐
│  [HAECKEL PLATE]       │  │  [DARWIN/GOULD PLATE]  │
│                        │  │                        │
│  Great Barrier Reef    │  │  Galápagos             │
│                        │  │                        │
│  The world's largest   │  │  Darwin's archipelago  │
│  coral system,         │  │  — illustrated by      │
│  documented by         │  │  Gould and Wallace     │
│  Haeckel in 1899.      │  │  from 1845.            │
│                        │  │                        │
└────────────────────────┘  └────────────────────────┘
```

**Footer CTA (at bottom of places index)**

```
┌─────────────────────────────────────────────────────────────────┐
│  More places coming to NC                                       │
│                                                                 │
│  New places are published when source, rights, and             │
│  attribution verification is complete.                          │
│                                                                 │
│  [opengracelabs@protonmail.com]  ← "Get notified" email link   │
└─────────────────────────────────────────────────────────────────┘
```

#### What Is Removed from Places Index

| Removed | Replaced with |
|---|---|
| "Phase 0 keeps place pages as governed previews while source authority gates complete." | Nothing. Remove entirely. |
| "Coming soon" / "Live Phase 0" status labels | Editorial descriptions with no status labels |
| Text-only place cards | Illustrated place cards |

---

## VI. Complete Removal Registry

The following elements must be removed from all visitor-facing surfaces. They are internal governance labels, operational language, or compliance copy that belongs in internal systems, not the visitor experience.

| Element | Current locations | Disposition |
|---|---|---|
| `"Phase 0 public launch"` | Homepage eyebrow | Remove |
| `"Phase 0"` | Products page headline, product card eyebrows, places page lead | Remove from all visitor surfaces |
| `"Phase 0 products"` | Products page headline | Rewrite to "Products" or "Our collection" |
| `"Manual purchase"` | `ManualPurchaseCTA` eyebrow, Products page badge, Products page lead | Remove entirely — operational language |
| `"Manual purchase is enabled after governed verification."` | Products page lead | Remove |
| `"manual fulfillment path"` | Products page product description | Remove |
| `"NC-PROD-001"`, `"NC-PROD-008"` | Product page eyebrow, products page card eyebrows | Remove from all visitor surfaces — retain in `governed-content.ts` for internal reference |
| `"NC-PROD-001 / NC-PROD-008"` as combined eyebrow | Product page | Remove |
| `"Request purchase"` | `ManualPurchaseCTA` headline | Replace with "Enquire" |
| `"A manual invoice and fulfillment details will follow after review."` | `ManualPurchaseCTA` body | Remove |
| `"Coming soon"` status label | Place cards, `governed-content.ts` `placeTeasers` | Remove from visitor layer |
| `"Live Phase 0"` status label | Place cards | Remove from visitor layer |
| `status` field on place cards | Places page, homepage places section | Do not render in visitor layer |
| `"Phase 0 keeps place pages as governed previews while source authority gates complete."` | Places page lead | Remove entirely |
| `"only after rights, source, and attribution checks are visible on the page"` | Homepage lead | Remove — replace with editorial copy |
| `"Manual purchase is available"` | Any surface | Remove |
| `"governed verification"` | Products page | Remove |
| Product code as `<p className="eyebrow">` | All product cards | Remove |

**Internal references that must be preserved but hidden:**
- `NC-PROD-001`, `NC-PROD-008` codes: keep in `governed-content.ts`, API calls, and internal tooling — remove only from rendered visitor HTML
- `phase: "Phase 0"` on `ProductSummary` type: keep in the type, do not render in visitor UI
- `status` on `placeTeasers`: keep in data, do not render in visitor UI

---

## VII. Top 25 Improvements Ranked by Impact

Impact is measured across four dimensions: revenue impact (conversion), trust impact (credibility), discovery impact (engagement), and experience quality (return visits).

| Rank | Improvement | Impact | Phase | Effort | Blocks |
|---|---|---|---|---|---|
| 1 | **Replace CSS gradient hero-media with actual Earthrise photograph** on homepage, story page, product page | Revenue + Trust + Wonder | Phase 0 | Low | None — NC-NASA-002 is human_verified=TRUE |
| 2 | **Remove all governance copy from visitor surfaces** — phase labels, manual purchase language, status codes (see §VI) | Trust + Revenue | Phase 0 | Low | None |
| 3 | **Replace homepage headline** with editorial voice ("The illustrated record of Earth's great places.") | Wonder + Trust | Phase 0 | Low | None |
| 4 | **Replace "Request purchase" with "Enquire"** in `ManualPurchaseCTA` — reframe the commerce interaction | Revenue | Phase 0 | Low | None |
| 5 | **Add serif typeface** (Cormorant Garamond or Tiempos) for all editorial headlines and story body text | Wonder + Trust | Phase 0 | Low | None |
| 6 | **Implement MASTERWORK quality tier badge** (gold, designed) on Earthrise product page and collection page | Trust + Desire | Phase 0 | Low | None — tier is already known |
| 7 | **Implement progressive provenance disclosure** on product page: one-line credit → expandable panel → full record | Trust | Phase 0 | Medium | None |
| 8 | **Write Phase 0 curated story copy** for Earthrise (hardcoded in `governed-content.ts` as `EARTHRISE_STORY_FALLBACK`) | Wonder | Phase 0 | Low | None — human-authored, no AI gate |
| 9 | **Replace product page product-code eyebrow with no eyebrow** (product title is the headline) | Trust | Phase 0 | Low | None |
| 10 | **Implement translucent sticky header** on hero pages (homepage, story, collection) | Wonder | Phase 0 | Medium | None |
| 11 | **Build Collection Page v1** (`/collections/earthrise`) using template from §V.4 | Discovery + Commerce | Phase 0 | Medium | NC-COLLECTIONS-001 governance doc needed |
| 12 | **Redesign Places Index** to remove status labels and add editorial teaser cards with illustrations | Discovery + Wonder | Phase 0 | Medium | Available illustrations needed per place |
| 13 | **Redesign `EarthriseAttributionBlock`** from paragraph-styled section to museum-label element (thin top border, muted bg, small type) | Trust | Phase 0 | Low | None — content unchanged |
| 14 | **Add "Enquire" CTA above the fold** on product page — currently the purchase path requires scrolling to the `ManualPurchaseCTA` component | Revenue | Phase 0 | Low | None |
| 15 | **Implement product page split-screen layout** with illustration dominant (60%) and commerce panel (40%) | Wonder + Desire | Phase 0 | Medium | Requires real image |
| 16 | **Add variant selector** to product page (Museum Gicléé vs Digital Download as a UI selector, not two identical cards) | Revenue | Phase 0 | Low | None |
| 17 | **Add Human Verified mark** (✓ iconographic element) to product page commerce panel | Trust | Phase 0 | Low | None — IFC-1 already satisfied |
| 18 | **Add PD rights badge** (colored: navy bg, §105 text) to replace current plain "Public domain" badge | Trust | Phase 0 | Low | None |
| 19 | **Add "Collections" to L1 navigation** alongside existing links | Discovery | Phase 0/1 | Low | Phase 0: one collection (Earthrise). Phase 1: full. |
| 20 | **Rewrite homepage editorial lead** with two-paragraph historical context copy (see §V.1 Section 2) | Wonder | Phase 0 | Low | None — human-authored |
| 21 | **Build Certificate of Authenticity section** on product page with preview (even a text mockup in Phase 0) | Trust + Desire | Phase 0 | Medium | None |
| 22 | **Remove product grid from homepage** — move product discovery to story and collection pages | Experience quality | Phase 0 | Low | None |
| 23 | **Rewrite About page** as "How We Work" editorial narrative — 3 sections: The Illustrations / The Verification / The Products | Trust | Phase 0 | Low | None |
| 24 | **Add illustration thumbnails to upcoming place cards** (places index) — even as seeded static images in Phase 0 | Wonder | Phase 0 | Medium | Governed assets must exist per place |
| 25 | **Implement image zoom** on product page illustration — cursor: zoom-in, click to full-screen | Wonder + Desire | Phase 1 | Medium | Requires high-resolution image delivery (MASTERWORK: 6000px+) |

---

## VIII. NC-COLLECTIONS-001 Gap

NC-COLLECTIONS-001 was referenced in the scope of this document but does not exist. The collection page template defined in §V.4 is production-ready as a design pattern. However, before Collections can be activated as a governed commerce surface, NC-COLLECTIONS-001 must be drafted and ratified, defining:

1. **Collection eligibility:** What constitutes a collection (minimum illustration count, quality tier requirements, place/theme coherence criteria)
2. **Collection naming convention:** How collections are titled, slugged, and catalogued
3. **Curator requirements:** Which collections require PA sign-off, which require two-human activation
4. **Commerce surfaces:** Which product lines may be surfaced in a collection "Shop This Collection" module
5. **Attribution requirements:** Collection-level attribution vs per-illustration attribution
6. **Phase activation gates:** Phase 0 (Earthrise), Phase 1 (Golden Age, North American Surveys), Phase 2+ (Expedition Pacific, etc.)

**Recommended immediate action:** Draft NC-COLLECTIONS-001 as a governance document before Phase 1 collection activation. The Earthrise collection page (`/collections/earthrise`) may be built in Phase 0 as a single-illustration proof-of-concept; it does not require NC-COLLECTIONS-001 ratification since it uses only already-authorized assets and commerce surfaces.

---

## IX. What Should Be Above the Fold — Summary Table

| Page | Above fold: show | Above fold: hide |
|---|---|---|
| **Homepage** | Full-bleed Earthrise photograph · 8-word editorial headline · Ghost CTA · Level 0 credit line | All governance copy · Phase labels · Product grid · Status cards · Attribution block |
| **Story Page** | Full-bleed Earthrise photograph · William Anders pull quote · Translucent header with back-link · Level 0 credit line | Headline (scrolls below fold) · Story body · Commerce module · Attribution block |
| **Product Page** | Earthrise photograph (60% width, zoomable) · Product title · MASTERWORK badge · Rights badges · Enquire CTA · Variant toggle | Provenance panel (collapsed by default) · CoA section · Story section · Related products |
| **Collection Page** | Full-bleed Earthrise (gallery treatment) · "Collections" breadcrumb · Collection title · One-sentence thesis · Work count · Source/rights badges | Collection editorial · Gallery · Shop module · Coming collections |
| **Places Index** | Two-line editorial headline · Search input (visible even at Phase 0) | Place card grid (immediately below fold but requires minimal scroll) · Footer CTA |

---

## X. Ratification Conditions

**C-1:** All §VI removal items confirmed as safe to remove (no governance obligation requires their presence in the visitor layer; governance obligations are satisfied at the data layer).

**C-2:** NC-COLLECTIONS-001 drafted before `/collections/earthrise` is activated as a commerce surface. The page may be built in Phase 0; the commerce module activates after NC-COLLECTIONS-001 ratification.

**C-3:** Curated Phase 0 story copy (§V.2) reviewed by PA before publication. Copy is human-authored, not AI-generated — no NC-AI-001 gates apply. Attribution claims ("§105," "public domain at creation") are sourced from existing governance records, not generated.

**C-4:** "Enquire" CTA implementation reviewed to confirm fulfillment path (`mailto:opengracelabs@protonmail.com?subject=Earthrise purchase request`) is preserved — only the visitor-facing label changes, not the underlying mechanism.

**C-5:** Image delivery confirmed for Phase 0 before implementation begins. NC-NASA-002 (AS08-14-2383) must be accessible to the web app at an appropriate URL. If the image is served from MinIO, the delivery path must be confirmed before placeholder divs are replaced.

---

*NC-WEB-004 v1.0 · Drafted 2026-06-12 · Pending ratification · Principal Architect*
