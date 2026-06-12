# NC-WEB-007 Collection Experience Audit
**Date:** 2026-06-12  
**Branch:** v0.4.0-collection-000001  
**Baseline:** NC-WEB-005 Visual Audit (6.2/10 overall)  
**Focus:** Collections · Storytelling · Product desirability · Discovery  
**Reference models:** Rijksmuseum · National Geographic · Apple · MoMA · Smithsonian

---

## I. NC-WEB-006 Implementation State

### What exists

The current implementation contains:

| Element | Status |
|---------|--------|
| Full-bleed hero on homepage (`min-height: 100svh`) | ✅ |
| Cormorant Garamond serif for h1/h2 (imported, applied) | ✅ |
| MASTERWORK badge (dark gold, correctly styled) | ✅ |
| Progressive provenance panel (`<details>`/`<summary>`) | ✅ |
| Collection section on homepage (`id="collections"`, image cards) | ✅ |
| Card hover states (translateY, shadow, image zoom) | ✅ |
| Dedicated `/collections/earthrise` page | ❌ |
| Nav "Collections" → collection destination | ❌ (→ `/#collections` anchor) |
| Differentiated collection gallery items | ❌ (3 identical crops) |
| Story page improvements | ❌ (largely unchanged) |
| ManualPurchaseCTA copy | ❌ ("Request purchase" persists) |
| Place card specific copy | ❌ (identical generic copy) |

### Critical finding: the collection has no URL

The `Collections` nav link routes to `/#collections` — an in-page anchor that scrolls the homepage to a three-card section. This means:

- There is no `/collections/earthrise` page
- A visitor who navigates to "Collections" lands on the homepage and scrolls to a section
- The collection cannot be linked, bookmarked, or shared as a first-class destination
- Every reference model in this audit maintains dedicated collection URLs

The branch name `v0.4.0-collection-000001` signals that collection pages are the intended Sprint 2 deliverable. The homepage section is a placeholder for a page that does not yet exist.

### Cormorant Garamond: confirmed active

The NC-WEB-005 Visual Audit noted "serif typeface status unknown." Confirmed: `@import url("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&display=swap")` is present in `styles.css`. All h1 and h2 elements use `font-family: var(--serif)` = Cormorant Garamond. The full-bleed hero headline "The world seen whole." renders in Cormorant Garamond at `clamp(4rem, 10vw, 9.6rem)`. This is a significant quality signal that was not captured in the prior visual audit.

---

## II. Reference Model Analysis

### Rijksmuseum — collection as object destination

The Rijksmuseum's collection model treats each artwork as a first-class destination with its own URL (`/en/collection/{object-number}`). The individual object page IS the collection page: full-bleed image, museum label, provenance and acquisition history, related works, high-res download, and a link to the print shop. The collection index (`/en/collection`) is a discovery tool — filters by artist, era, medium, theme — that routes to individual object pages. Commerce is integrated at the object level: the "Download" button (free, high-res) appears alongside the "Buy print" link. Revenue comes from prints, licenses, and high-res commercial downloads.

**NC implication:** Every PD source image NC holds should eventually have its own collection page at `/collections/{slug}`. For Phase 0, Earthrise is the first.

### National Geographic — editorial gallery as collection

NatGeo photo collections are galleries: each has a cover image, editorial intro (150–300 words), photographer credit, location, and an image-by-image progression. The gallery intro tells you why these images exist as a group. Related stories appear in a sidebar. The gallery is the storytelling engine — it doesn't just show images, it argues for their significance. Commerce is light (print licensing through a partner) but present.

**NC implication:** A collection page needs an editorial intro that argues for the collection's existence, not just lists its contents.

### Apple — product family as collection

Apple's product family pages (`/shop/buy-iphone`) group items at different price and capability points. The family page answers: what's in this family, how do they differ, which one is right for me? Each item has a thumbnail, one-line differentiator, and a price. A "Compare" table is available. The commerce path is clear: family page → individual product → buy. The design principle: make the decision easy, not overwhelming.

**NC implication:** The Earthrise collection has two products (Museum Print, Digital Edition). The collection page should answer "which is right for me" before routing to the product page. The edition comparison belongs here as well as on the product page.

### MoMA — collection-to-shop continuity

MoMA's collection pages maintain visual and tonal continuity with the shop. An artwork page at `/collection/works/{id}` shows the full image, curatorial text, medium/date/dimensions, exhibition history, and a "Shop MoMA" link that routes to products using that artwork. The shop page shows prints, bags, cards, and licensed products. The handoff is seamless — the visitor moves from artwork to shop without a change in register.

**NC implication:** The collection page must have a clear, unbroken path to the enquiry/purchase. "Shop This Collection" as a CTA at the bottom of the collection page, before the next-journeys teaser.

### Smithsonian — provenance as authority signal

The Smithsonian's collection pages are provenance-first: every object page leads with source institution, accession number, date acquired, exhibition history. This depth of record creates institutional trust. Visitors read the provenance and believe the Smithsonian knows what it's talking about. The commerce path is weak (primarily educational), but the authority model is exemplary.

**NC implication:** Provenance on a collection page is not just a compliance requirement — it's the authority signal that earns the visitor's trust before they reach the commerce CTA. The progressive provenance panel should appear on the collection page.

---

## III. Current Score vs. Reference Models

| Dimension | NC Current | Rijksmuseum | NatGeo | Apple | MoMA | Smithsonian |
|-----------|-----------|-------------|--------|-------|------|-------------|
| Collections | **2** | 10 | 9 | 7 | 9 | 8 |
| Storytelling | **5** | 9 | 10 | 6 | 8 | 9 |
| Product desirability | **4** | 8 | 5 | 10 | 7 | 3 |
| Discovery | **4** | 9 | 9 | 7 | 8 | 8 |
| **Average** | **3.75** | **9.0** | **8.25** | **7.5** | **8.0** | **7.0** |

### Collections: 2/10

There is no `/collections/earthrise` page. The collection exists as a homepage section. The three collection cards (`#collections`) show identical 4:3 crops of the same image. The MASTERWORK badge appears on all three cards with no differentiation. The section heading "Earthrise: The Overview Collection" has a lead paragraph, but there is no editorial intro that argues for the collection's significance. The collection cannot be directly linked.

The reference gap is almost entirely architectural: every reference model has dedicated collection URLs. This is a one-sprint fix.

### Storytelling: 5/10

The story page contains genuinely good editorial content: the lead paragraph, the story body, "Why Earthrise matters," and the "The mission looked outward. The image asked us to look back." heading are all well-written. The storytelling score is limited by three structural failures:

1. `EarthriseAttributionBlock` appears between the photograph and the story body — a card-styled section that interrupts narrative flow at the highest-impact moment
2. The `collection-teaser` section at the bottom of the story page renders four text spans (`NASA source · Story · Print · Digital`) instead of a visual collection module — the story ends and then shows a list
3. The `educationText` fallback ("Nature & Culture presents the image as a verified public-domain work with source, rights, and attribution visible beside the experience.") is internal governance language placed in the story body

### Product desirability: 4/10

The MASTERWORK badge (well-styled: dark background, gold text, gold border) and the progressive provenance panel (`<details>`) are genuine improvements. The edition comparison with `<dl>` structure is semantically correct. The score is limited by:

1. `ManualPurchaseCTA`: h2 = "Request purchase," button = "Request purchase" — at the moment of decision, the copy announces a bureaucratic process instead of an action
2. Product image: `aspect-ratio: 1/1` still in `.premium-product-image` CSS (line 475) — the Earthrise landscape photograph is letterboxed in a square container even with `object-fit: contain`, wasting vertical space with black bars at top and bottom
3. No edition thumbnails — the visitor is asked to choose between Museum Print and Digital Edition without seeing either

### Discovery: 4/10

The nav now has Collections + Discover, which is an improvement. The collection image grid on the homepage creates visual discovery. Discovery is limited by: no differentiation between place cards (identical generic copy); the "Collections" nav goes to `/#collections` instead of a dedicated page; the story → collection → product path has gaps at every handoff.

---

## IV. Earthrise Collection Page Design

### URL

```
/collections/earthrise
```

Nav "Collections" link: change from `/#collections` → `/collections/earthrise` (Phase 0 single collection).

### Page architecture

```
┌──────────────────────────────────────────────────────────────────┐
│ NATURE & CULTURE    Collections · Discover · Editions · About    │
│                                 ↑ links to /collections/earthrise │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ╔══════════════════════════════════════════════════════════╗    │
│  ║                                                          ║    │
│  ║   [EARTHRISE PHOTOGRAPH — full bleed, 80svh]             ║    │
│  ║                                                          ║    │
│  ║  ┌──────────────────────────────────────────────────┐   ║    │
│  ║  │  eyebrow: COLLECTIONS                             │   ║    │
│  ║  │  h1: Earthrise: The Overview Collection   [serif] │   ║    │
│  ║  │  eyebrow: Apollo 8 · December 24, 1968            │   ║    │
│  ║  │  lead: One NASA source image. Verified public     │   ║    │
│  ║  │  domain. Two editions for display and study.      │   ║    │
│  ║  └──────────────────────────────────────────────────┘   ║    │
│  ║                     NASA · Apollo 8 · William Anders ·  ║    │
│  ╚══════════════════════════════════════════════════════════╝    │
│                                                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  About this collection                              [section]     │
│  ────────────────────────────────────────────────────────────    │
│  [MASTERWORK]  NASA  ·  Apollo 8  ·  Dec 24, 1968  ·  PD        │
│                                                                    │
│  On Christmas Eve 1968, William Anders looked away from the      │
│  lunar surface and photographed Earth rising above the grey      │
│  horizon. The image became the first portrait of the whole        │
│  world — not a map, not a diagram, but a photograph.             │
│                                                                    │
│  Nature & Culture holds AS08-14-2383 as a verified public-       │
│  domain work under 17 U.S.C. § 105 and offers it in two         │
│  editions: a museum-quality archival print for display and        │
│  a high-resolution digital edition for close study.              │
│                                                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  This collection                                    [section]     │
│  ────────────────────────────────────────────────────────────    │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │
│  │ [STORY CROP] │   │ [PRINT MOCK] │   │ [DIGITAL IMG]│         │
│  │ 16:9 ratio   │   │ framed print │   │ with metadata│         │
│  │              │   │ simulation   │   │ overlay      │         │
│  │ MASTERWORK   │   │ MASTERWORK   │   │ MASTERWORK   │         │
│  │ Story        │   │ Museum Print │   │ Digital Ed.  │         │
│  │ The context  │   │ 24 × 20 in   │   │ High res.    │         │
│  │ and record   │   │ Archival ink │   │ For study    │         │
│  │ [Read →]     │   │ [Enquire →]  │   │ [Enquire →]  │         │
│  └──────────────┘   └──────────────┘   └──────────────┘         │
│                                                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Source record                                      [section]     │
│  ────────────────────────────────────────────────────────────    │
│  [NASA]  [Apollo 8]  [December 24, 1968]  [Public Domain]        │
│  [View full provenance ▼]   ← details/summary (same as product)  │
│                                                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ╔══════════════════════════════════════════════════════════╗    │
│  ║  Own Earthrise                                           ║    │
│  ║  Museum Print · Digital Edition                          ║    │
│  ║  [Enquire about this edition]   ←  primary CTA [button] ║    │
│  ╚══════════════════════════════════════════════════════════╝    │
│                                                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Next journeys                                      [section]     │
│  ────────────────────────────────────────────────────────────    │
│  [Yellowstone card]   [Grand Canyon card]   [GBR card]           │
│  Each with one specific line of copy                              │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

### Component requirements

| Component | Exists? | Action |
|-----------|---------|--------|
| `full-bleed-hero` CSS class | ✅ | Reuse from homepage |
| `collection-card-grid` CSS class | ✅ | Reuse, adjust for 3-col |
| `masterwork-badge` CSS class | ✅ | Reuse |
| `provenance-glance` + `<details>` | ✅ | Reuse from product page |
| `ManualPurchaseCTA` | ✅ | Reuse, after copy fix |
| Collection editorial intro copy | ❌ | Write in `governed-content.ts` |
| Differentiated gallery card images | ❌ | Story crop, print mockup, digital overlay |
| "Shop This Collection" CTA section | ❌ | New section, ~10 lines JSX |
| `/collections/earthrise/page.tsx` | ❌ | New file |
| Breadcrumb (`Collections > Earthrise`) | ❌ | New component or inline |

### Governed content additions required

```typescript
// In governed-content.ts

export const EARTHRISE_COLLECTION_INTRO = `On Christmas Eve 1968, 
William Anders looked away from the lunar surface and photographed 
Earth rising above the grey horizon. The image became the first 
portrait of the whole world — not a map, not a diagram, but a 
photograph made during a mission that was aimed elsewhere.

Nature & Culture holds AS08-14-2383 as a verified public-domain 
work under 17 U.S.C. § 105 and offers it in two editions: a 
museum-quality archival print for display and a high-resolution 
digital edition for close study. Every edition includes the 
NASA source credit and a statement of rights.`;

export const EARTHRISE_COLLECTION_TITLE = 
  "Earthrise: The Overview Collection";

export const EARTHRISE_COLLECTION_LEAD = 
  "One NASA source image, verified public domain. " +
  "Two editions for display and study.";
```

---

## V. Top 20 Improvements

Ranked by estimated impact on the four focus dimensions.

| # | Improvement | Dimension(s) | Effort | Impact |
|---|-------------|-------------|--------|--------|
| C-01 | Create `/collections/earthrise/page.tsx` with full-bleed hero, editorial intro, gallery, provenance, shop CTA | Collections | 3 hrs | Critical |
| C-02 | Nav "Collections" → `/collections/earthrise` (not `/#collections`) | Collections · Discovery | 5 min | Critical |
| C-03 | ManualPurchaseCTA: h2 → "Enquire about this edition" · button → "Send enquiry" · body → "Reply within 24 hours." | Desirability | 15 min | Critical |
| C-04 | Story page: remove `<EarthriseAttributionBlock />` from between figure and story body — move to figcaption or page footer | Storytelling | 30 min | High |
| C-05 | Story page: replace `collection-teaser` (4 text spans) with visual collection card grid (image cards with links) | Storytelling · Discovery | 1 hr | High |
| C-06 | Story page h1 fallback: "The image that made Earth the subject" → "On Christmas Eve, 1968, humanity saw the whole world for the first time." | Storytelling | 15 min | High |
| C-07 | Product image: fix `aspect-ratio: 1/1` in `.premium-product-image` CSS → `aspect-ratio: 4/3` (the photograph's native ratio) | Desirability | 5 min | High |
| C-08 | Homepage collection cards: differentiate the three cards visually (story crop at 16:9, print at 3:4 portrait, digital at 16:9 with metadata overlay) | Collections · Discovery | 2 hrs | High |
| C-09 | Collection page: `provenance-glance` + `<details>` provenance panel (reuse product page pattern) | Collections · Storytelling | 30 min | Medium |
| C-10 | Story page: "Own Earthrise" section → replace `<button>View Earthrise editions</button>` with a two-card edition comparison module (Museum Print / Digital Edition, each with one-line differentiator and enquiry link) | Desirability | 1 hr | Medium |
| C-11 | Homepage hero lead: replace "A source-traceable edition of Earthrise, the photograph that turned lunar exploration into a portrait of home." → "The photograph that changed how humanity sees itself. Available as a museum-quality print and digital edition." | Storytelling | 10 min | Medium |
| C-12 | Place cards: specific one-line descriptions for all 5 places (Earthrise: "The photograph that made Earth the subject." · Yellowstone: "America's first national park, painted in its golden age." · etc.) | Discovery | 30 min | Medium |
| C-13 | Story page: `educationText` fallback → replace governance language with curatorial note: "Earthrise is held by NASA as a public-domain work under 17 U.S.C. § 105. Every edition is printed from the same verified source file." | Storytelling | 10 min | Medium |
| C-14 | Collection page: Open Graph meta tags (`og:image`, `og:title`, `og:description`) + `application/ld+json` `ImageObject` schema | Discovery | 45 min | Medium |
| C-15 | Breadcrumb on collection page: `Nature & Culture > Collections > Earthrise` as small muted line below the hero | Collections · Discovery | 20 min | Low-Medium |
| C-16 | Story page: in "Why Earthrise matters" section, add "View the Earthrise Collection →" link to `/collections/earthrise` | Discovery · Collections | 5 min | Low-Medium |
| C-17 | Product page: add "← Back to Earthrise Collection" link above the product title (creates a coherent navigation path) | Collections · Discovery | 10 min | Low-Medium |
| C-18 | Story page: full-bleed hero treatment (same as homepage) — replace `<figure class="story-image-frame">` with full-bleed section | Storytelling | 2 hrs | Low-Medium |
| C-19 | Collection page: "Next journeys" section using `placeTeasers` data with specific copy per place | Discovery | 30 min | Low |
| C-20 | Footer: update from "Public-domain sources, visible attribution, source-traceable editions." → "Public-domain heritage, editorial provenance, two editions of Earthrise." (Phase 0 specific, update at Phase 1 with live places) | Storytelling | 5 min | Low |

---

## VI. Path to 8/10

### Current scores (4 focus dimensions)

| Dimension | Score |
|-----------|-------|
| Collections | 2 |
| Storytelling | 5 |
| Product desirability | 4 |
| Discovery | 4 |
| **Average** | **3.75** |

### Sprint 2: Collection page + critical fixes → 7.0/10

**C-01 through C-07** (estimated 6–8 hours combined):

- **C-01** (collection page) lifts Collections from 2 → 7. This is the structural prerequisite for everything else.
- **C-02** (nav fix) is 5 minutes and completes C-01 — without it, the collection page is invisible.
- **C-03** (ManualPurchaseCTA copy) lifts Product desirability from 4 → 6. One component, four string changes.
- **C-04** (story attribution position) lifts Storytelling from 5 → 6. The attribution block has been interrupting the story since Phase 0.
- **C-05** (story collection teaser) lifts Storytelling further to 7 — replaces the text-span list with a visual module.
- **C-06** (story h1 fallback) is a copy change that costs 15 minutes.
- **C-07** (product image aspect ratio) is a 5-minute CSS fix that removes an active composition error.

| Dimension | After Sprint 2 |
|-----------|---------------|
| Collections | 7 |
| Storytelling | 7 |
| Product desirability | 6 |
| Discovery | 6 |
| **Average** | **6.5** |

### Sprint 3: Differentiation + commerce → 8.0/10

**C-08 through C-17** (estimated 4–5 hours):

- **C-08** (differentiated gallery cards) lifts Collections to 8 — the collection page is now visually compelling, not just architecturally correct.
- **C-10** (edition comparison on story page) lifts Product desirability to 7 — the visitor has a commerce decision point at the end of the story, not just a button to another page.
- **C-11** through **C-17** collectively lift Storytelling and Discovery to 8 — specific copy, provenance on collection page, breadcrumb, cross-links.

| Dimension | After Sprint 3 | Reference avg |
|-----------|---------------|---------------|
| Collections | 8 | 8.6 |
| Storytelling | 8 | 8.4 |
| Product desirability | 7 | 6.6 |
| Discovery | 8 | 8.2 |
| **Average** | **7.75 → rounds to 8.0** | **7.95** |

C-18 (story page full-bleed hero) is the single highest-effort remaining item and lifts Storytelling to 9. With it: **8.25/10**.

---

## VII. What Makes NC Different From Its References

Before executing Sprint 2, one principle from each reference model worth internalizing:

**Rijksmuseum:** The object URL is permanent. The Night Watch's URL doesn't change between exhibitions. For NC, `/collections/earthrise` is a permanent address — not a campaign page, not a section, not a hash anchor. It's where Earthrise lives.

**National Geographic:** The editorial intro earns the gallery. A visitor who reads "William Anders had 10 seconds to photograph what he saw before the spacecraft moved on" is primed to look differently at the photograph than a visitor who sees it cold.

**Apple:** The decision between Museum Print and Digital Edition should require the same cognitive load as choosing between iPhone 15 and iPhone 15 Pro. Clear differentiator, clear price (when applicable), clear use case. Not two panels of description list — two visual objects with one headline each.

**MoMA:** The shop is not separate from the collection. The print is available on the same page as the artwork. "Own this" is not a navigation decision — it's the next step on the same page.

**Smithsonian:** Provenance depth = trust depth. The visitor who reads AS08-14-2383 / 17 U.S.C. § 105 / NASA nonendorsement has a different level of confidence than the visitor who only reads "public domain." Show the record. It's the asset.

---

## VIII. Required Code Files

Sprint 2 produces three files:

1. `apps/web/app/collections/earthrise/page.tsx` — new
2. `apps/web/lib/governed-content.ts` — add `EARTHRISE_COLLECTION_INTRO`, `EARTHRISE_COLLECTION_TITLE`, `EARTHRISE_COLLECTION_LEAD`
3. `apps/web/app/layout.tsx` — change nav `href="/#collections"` → `href="/collections/earthrise"`

ManualPurchaseCTA fix (`apps/web/components/ManualPurchaseCTA.tsx`) is a dependency that should land before or simultaneously with the collection page, since the collection page routes to the product page.

---

*NC-WEB-007 Collection Experience Audit. Produced: 2026-06-12.*
