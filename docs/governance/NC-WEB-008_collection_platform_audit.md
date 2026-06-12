# NC-WEB-008 Collection Platform Audit
**Date:** 2026-06-12  
**Branch:** v0.4.0-collection-000001  
**Pages reviewed:** `/` · `/collections` · `/collections/earthrise` · `/products/earthrise` · `/stories/earthrise`  
**Reference models:** Rijksmuseum · National Geographic · Google Arts & Culture · MoMA · Smithsonian  
**Dimensions:** Collection · Discovery · Collection Desirability

---

## I. Platform State

Since NC-WEB-007, four structural changes were made:

| Change | Status |
|--------|--------|
| `/collections` index page created | ✅ |
| `/collections/earthrise` page created | ✅ |
| Nav "Collections" → `/collections` (not `/#collections`) | ✅ |
| ManualPurchaseCTA: "Request purchase" → "Contact for availability" / "Contact us" | ✅ partial |
| Product page: "Back to Earthrise Collection" back-link | ✅ |
| Story page: "View the Earthrise Collection" cross-link | ✅ |
| Product image aspect-ratio: 1/1 → landscape | ❌ persists |
| Story page: attribution block position | ❌ persists |
| Story page: collection-teaser visual module | ❌ persists |
| Homepage hero lead: "source-traceable" copy | ❌ persists |
| Place card specific copy | ❌ persists |

The collection platform now has the correct URL structure, an editorial hero, a curator statement, discovery pathways, a featured works grid, and a collection CTA. The CSS for all major collection components is properly defined. This is a significant advance from NC-WEB-007's 3.75/10 baseline.

---

## II. Page-by-Page Assessment

### `/collections` — Collections Index

**Architecture:** `collections-index-page` with `collection-index-grid` (single column, max-width 760px). One `collection-card image-card` with MASTERWORK badge, "Earthrise: The Oasis Collection" heading, editorial description, and link to `/collections/earthrise`.

**What works:** The single-card layout is Phase 0 appropriate. The description is editorial: "The moment humanity found home: a focused archival collection around Apollo 8, planetary awareness, and the photograph that changed the meaning of exploration." MASTERWORK badge correctly placed.

**Gaps:**
- h1 is generic: "Source-led collections." — not an editorial headline
- `collection-index-grid` is `grid-template-columns: minmax(0, 760px)` — this is a single-column constraint that won't auto-expand when a second collection is added. Must become `repeat(auto-fill, minmax(480px, 760px))` or similar before Phase 1
- No "coming soon" teasers for Yellowstone, Grand Canyon, Great Barrier Reef — the index feels like an ending, not a beginning
- Page is structurally a dead-end after Phase 0 without additional collection cards

---

### `/collections/earthrise` — Earthrise: The Oasis Collection

**Architecture:** `collection-detail-page` with:
- `collection-hero` (92svh, full-bleed image, overlay copy, gold eyebrow, MASTERWORK COLLECTION badge, large h1)
- `curator-statement-section` (dark full-width blockquote)
- `collection-narrative-section` (two-column editorial)
- `collection-pathway-grid` (3-column pathway cards)
- `collection-card-grid` / "Featured works" (3 collection cards)
- `collection-cta-section` (light green background, headline, two CTAs)
- `EarthriseAttributionBlock` at footer

**What works:**

The `curator-statement-section` is the highest-quality piece of content on the entire site. Dark background (#111714), full-width, Cormorant Garamond at `clamp(2rem, 5vw, 4.4rem)`, weight 600:

> *"We went to the Moon to discover the Moon. Instead, we found ourselves. Earthrise is the moment our species gained a planetary mirror, transforming a cold race for orbit into a profound awareness of our shared isolation and beauty."*

This is editorial authority. Rijksmuseum-tier curatorial voice. The blockquote renders as a full-width typographic statement that interrupts the scroll with something worth pausing for.

The collection narrative ("The oasis in the desert" / two-column copy) follows naturally from the blockquote and provides the factual record: what Apollo 8 saw, what the collection is, what it offers.

Discovery pathways are correctly architected: three thematic entry points (Atmospheric Science / Orbital Mechanics / Cultural Heritage) in a 3-column grid with 280px min-height cards and hover states. The eyebrow/h3/body structure gives each pathway visual hierarchy.

The `collection-hero-copy h1` renders at `clamp(3.4rem, 8vw, 8.2rem)` — slightly smaller than the homepage hero (`clamp(4rem, 10vw, 9.6rem)`) but still editorial scale. Cormorant Garamond at 8.2rem max for "Earthrise: The Oasis Collection" is correctly large.

**Active errors:**

**E-01 — All three featured works use identical images.** "Earthrise Heritage Edition," "The Lunar Horizon," and "The Overview Folio" all render `src="/images/earthrise-as08-14-2383.jpg"`. The collection has three conceptually distinct works — a heritage presentation, a detail study, and an intellectual record — but all three cards show the same full-frame image at 4:3 crop. A visitor sees three identical thumbnails. This collapses the impression that these are distinct things.

**E-02 — Naming inconsistency: "Oasis" vs "Overview."** The collection is named "Earthrise: The Oasis Collection" on `/collections`, `/collections/earthrise` (title + h1), and the `<Metadata>` description. But the homepage `#collections` section is headed "Earthrise: The Overview Collection," and the story page's feature-section also says "Earthrise: The Overview Collection." Four surfaces: two say Oasis, two say Overview. Canonical name must be chosen and applied everywhere.

**E-03 — Discovery pathways have no links.** The three pathway cards (The Thin Blue Line / The Lunar Cradle / The Movement Icon) have no `<a>` or `<Link>` elements. A visitor reads the pathway description and has no action to take. They are not dead-end cards in the sense of routing to an error — they simply don't go anywhere. At minimum, each should link to the story page (the closest content destination) with the pathway as context.

**E-04 — No provenance on the collection page.** The product page has a full provenance section (`provenance-glance` + `<details>` panel). The collection page — which is the canonical record holder — has no provenance. Visitors who arrive at the collection page directly (via the nav or a shared link) have no authority signal from the source record until they navigate to the product page.

**E-05 — No breadcrumb.** The collection page has no navigation context. The product page has "Back to Earthrise Collection" — a back-link added since NC-WEB-007. But the collection page itself has no "Collections > Earthrise" trail. A visitor who lands on `/collections/earthrise` from a search or external link has no visible path back to `/collections`.

**E-06 — Featured works have no links.** The three works cards on the collection page link to nothing. "Earthrise Heritage Edition" / "The Lunar Horizon" / "The Overview Folio" exist as descriptive cards but do not route anywhere. At minimum, each should link to `/products/earthrise`.

---

### `/products/earthrise` — Earthrise Product Page

**Improvements since NC-WEB-007:**
- "Back to Earthrise Collection" back-link above the product title ✅
- ManualPurchaseCTA updated: "Contact for availability" / "Contact us" ✅ (partial)

**Persisting issues:**

`ManualPurchaseCTA` now renders:
- eyebrow: "Availability"
- h2: "Contact for availability"
- body: "Ask about Earthrise. We will reply with availability, payment, and fulfillment details."
- button: "Contact us"

"Contact for availability" sounds like a product that may be out of stock. "Contact us" is the most generic CTA in commerce. The emotional register at the purchase moment should be: *I want this specific thing, and I am taking a step to get it.* "Send enquiry" achieves this. "Contact us" does not.

`aspect-ratio: 1/1` on `.premium-product-image` (CSS line 475) persists. The Earthrise photograph is landscape (4:3 approximately). With `object-fit: contain`, the image is letterboxed in a square frame: the photograph appears with black space above and below. This is the correct conservation treatment for a frame shop but the wrong product presentation for a web page.

---

### `/stories/earthrise` — Earthrise Story Page

**Improvements since NC-WEB-007:**
- "View the Earthrise Collection →" link added to the "Why Earthrise matters" section ✅
- h1 fallback: "The image that made Earth the subject" ✅ (editorial headline)
- Story body: three substantive paragraphs ✅
- Back-link connects story to collection ✅

**Persisting issues:**

`EarthriseAttributionBlock` still renders between the `<figure>` and the `story-body` (line 40 of story page). A visitor's reading path: header → lead → photograph → [attribution card] → story body. The attribution card is a bordered, padded section with two lines of governance text. It interrupts at the moment the photograph should lead directly into the story.

`collection-teaser` still renders as four `<span>` elements: "NASA source" / "Story" / "Print" / "Digital." This section is labeled "Earthrise: The Overview Collection" (naming conflict with the collection pages' "Oasis Collection") and describes the collection as connecting "AS08-14-2383 and connects the photograph, its mission context, source record, and launch editions in one focused experience." — but the visual element that follows this description is four pill-style spans in a grid. This is a list, not an experience.

`educationText` fallback still renders: "Nature & Culture presents the image as a verified public-domain work with source, rights, and attribution visible beside the experience." — governance documentation in the editorial body of a story page.

---

### `/` — Homepage

Largely unchanged from NC-WEB-005 post-Codex. Key persisting issue: the homepage `#collections` section still says "Earthrise: The Overview Collection" and routes its three cards to `/collections/earthrise` with labels "Enter collection" / "View in collection" / "View in collection." These now correctly link to the collection page. But the section heading creates the naming conflict noted in E-02.

---

## III. Scores vs Reference Models

### Collection Score

| Platform | Score | Notes |
|----------|-------|-------|
| Google Arts & Culture | 10 | Discovery-first; millions of works; thematic collections; editorial voice |
| Rijksmuseum | 10 | Object-level collection pages; provenance depth; exhibition history; download + print |
| MoMA | 9 | Curatorial voice; art-to-shop continuity; related works |
| National Geographic | 8 | Gallery-as-collection; editorial intro; photographer credit; related stories |
| Smithsonian | 8 | Topic collections; provenance authority; context depth |
| **NC current** | **7** | Dedicated URLs ✅; curator statement ✅; editorial narrative ✅; pathways ✅; identical works images ❌; no provenance ❌; no breadcrumb ❌; dead-end pathway cards ❌ |

The jump from 2 (NC-WEB-007) to 7 is real. The collection page has genuinely good editorial content — the curator statement is the site's strongest piece of copy. The score reaches 7 rather than 8 because the featured works section has a critical visual failure (identical images) and the provenance architecture that defines NC's authority is absent from the collection page itself.

**Gap to 8:** Three fixes — (1) differentiate featured works visually, (2) add provenance glance to collection page, (3) fix naming to Oasis Collection everywhere.

**Gap to 9:** Two more — (4) pathway cards become linkable navigation, (5) story page gets visual collection module (replacing teaser spans).

**Gap to 10 (Phase 1):** Multiple collections in the index, full-bleed story page heroes, illustrated place cards.

---

### Discovery Score

| Platform | Score | Notes |
|----------|-------|-------|
| Google Arts & Culture | 10 | Discovery is the product; tag cloud; related works at every turn |
| Rijksmuseum | 9 | Filters; related objects; similar technique; same maker |
| National Geographic | 9 | Related stories; related galleries; related places |
| MoMA | 8 | Related exhibitions; related artworks; "More from this artist" |
| Smithsonian | 8 | Topic links; artifact relationships; institutional cross-links |
| **NC current** | **6** | Dedicated collection URL ✅; story↔collection cross-links ✅; product back-link ✅; pathway cards ✅ (dead ends); identical place copy ❌; no next-journey section on collection page ❌ |

Cross-page navigation exists in both directions: story → collection, product → collection, nav → /collections. Discovery pathways give thematic framing. The score reaches 6 and not 7 because the pathway cards don't go anywhere (E-03), and the place cards section on the homepage still renders identical generic copy with no differentiation between five distinct places.

**Gap to 8:** Four fixes — (1) pathway cards → link to story/collection at minimum, (2) place cards → specific per-place descriptions, (3) collection page → next-journeys section with place cards at bottom, (4) collections index → grid-template-columns ready for Phase 1 expansion.

**Gap to 9:** Two more — (5) place pages as full discovery destinations (Phase 1), (6) related works when the collection grows.

---

### Collection Desirability Score

| Platform | Score | Notes |
|----------|-------|-------|
| Apple | 10 | Price visible; instant purchase; comparison built-in; zero friction |
| MoMA | 8 | Shop integrated with artwork; prints visible at art page |
| Rijksmuseum | 7 | High-res download + print shop prominent; price visible |
| National Geographic | 5 | Print licensing available but not foregrounded |
| Smithsonian | 3 | Primarily educational; commerce minimal |
| **NC current** | **5** | MASTERWORK badge ✅; progressive provenance ✅; collection CTA ✅; "Contact us" ❌; no price ❌; identical works no CTAs ❌; product image 1:1 ❌ |

Desirability at 5 reflects the genuine tension in the current implementation: the collection page builds atmosphere and authority (curator statement, editorial narrative, pathways) but the purchase action at the end says "Contact us." The featured works cards have no CTAs. The product image is letterboxed. No price is anywhere on any page.

**Gap to 8:** Five fixes — (1) ManualPurchaseCTA copy → "Enquire about this edition" / "Send enquiry," (2) product image aspect-ratio 1/1 → 4/3, (3) featured works → each card has a CTA ("Enquire") or routes to /products/earthrise, (4) story page collection-teaser → visual edition cards, (5) "Contact us" → "Send enquiry" on CTA section of collection page.

**Gap to 9:** Three more — (6) edition thumbnails/mockups visible on collection CTA section, (7) price or "from" price visible, (8) story page attribution block moved to figcaption so the story flows to the commerce CTA without interruption.

---

## IV. Summary Score Table

| Dimension | NC-WEB-007 | NC-WEB-008 | Delta | Gap to 8 | Gap to 9 |
|-----------|-----------|-----------|-------|-----------|----------|
| Collection | 2 | **7** | +5 | 1 pt | 2 pts |
| Discovery | 4 | **6** | +2 | 2 pts | 3 pts |
| Desirability | 4 | **5** | +1 | 3 pts | 4 pts |
| **Average** | **3.3** | **6.0** | **+2.7** | | |

---

## V. Gaps to 8/10 — Ranked by Impact

All 8/10 gaps are code-level fixes. No new pages required. Estimated total: 4–6 hours.

| # | Fix | Dimension(s) | Effort |
|---|-----|-------------|--------|
| G8-01 | **Featured works: differentiate images.** Story card → `object-position: center top` crop (lunar limb detail). Print card → add print-frame overlay CSS. Digital card → metadata overlay. One image, three presentations. | Collection | 1.5 hrs |
| G8-02 | **Naming: "Oasis Collection" everywhere.** Homepage `#collections` h2: "Earthrise: The Overview Collection" → "Earthrise: The Oasis Collection". Story page feature-section h2: same change. Two string changes. | Collection | 10 min |
| G8-03 | **Provenance on collection page.** Add `provenance-glance` tokens (NASA · Apollo 8 · December 24, 1968 · Public Domain) + `<details>` provenance panel between collection narrative and pathways. Reuse existing CSS — zero new styles needed. | Collection | 30 min |
| G8-04 | **ManualPurchaseCTA copy.** h2 → "Enquire about this edition." button → "Send enquiry." body → "We reply within 24 hours with availability, payment, and shipping." One component, four string changes. | Desirability | 15 min |
| G8-05 | **Pathway cards → links.** Each of the three pathway cards should route somewhere. For Phase 0: all three → `/stories/earthrise`. This makes the pathways feel like navigation, not decoration. Five minutes. | Discovery | 5 min |
| G8-06 | **Place cards: specific copy.** Five unique one-line descriptions in `governed-content.ts`. Earthrise: "The photograph that made Earth the subject." Yellowstone: "America's first national park, illustrated in its golden age." Grand Canyon: "A geological portrait of deep time." Great Barrier Reef: "The largest living structure on Earth, documented at its peak." Galapagos: "The islands that changed the theory of life." | Discovery | 30 min |
| G8-07 | **Featured works: add CTA links.** Each of the three works cards on the collection page should link to `/products/earthrise`. Currently no links. Five-minute edit. | Desirability | 5 min |
| G8-08 | **Product image: fix aspect ratio.** `.premium-product-image { aspect-ratio: 4 / 3; }` in styles.css. The Earthrise photograph is landscape. The square container creates black bars with `object-fit: contain`. | Desirability | 5 min |
| G8-09 | **Collection page: next-journeys section.** Add a `discover-section` at the bottom of the collection page (above attribution) with 3–4 place cards. Same component and CSS as homepage. | Discovery | 45 min |
| G8-10 | **Breadcrumb on collection page.** Small muted `<nav aria-label="breadcrumb">` above the hero: `Collections > Earthrise: The Oasis Collection`. One component, 20 minutes. | Collection + Discovery | 20 min |

---

## VI. Gaps to 9/10 — Ranked by Impact

9/10 gaps require new content, visual design, or Phase 1 infrastructure.

| # | Fix | Dimension(s) | Effort | Gate |
|---|-----|-------------|--------|------|
| G9-01 | **Story page: attribution block.** Move `<EarthriseAttributionBlock />` from between figure and story body to the figcaption or a dedicated section below the story body. The photograph should flow directly into the story. | Collection + Desirability | 30 min | — |
| G9-02 | **Story page: collection-teaser → edition cards.** Replace the four text spans ("NASA source / Story / Print / Digital") with two image cards — Museum Print card and Digital Edition card — each with a one-line differentiator and a "Enquire" link to `/products/earthrise`. | Desirability | 1.5 hrs | — |
| G9-03 | **Story page: educationText fallback.** Replace governance language with a curatorial note: "Earthrise is held by NASA under 17 U.S.C. § 105. Every edition is printed from the same verified source file, AS08-14-2383." | Collection | 10 min | — |
| G9-04 | **Homepage hero lead.** Replace "A source-traceable edition of Earthrise, the photograph that turned lunar exploration into a portrait of home." → "The photograph that changed how humanity sees itself. Available as a museum-quality print and digital edition." Removes governance language from the primary pitch. | Desirability | 10 min | — |
| G9-05 | **Story page: full-bleed hero.** Replace `<figure class="earthrise-frame story-image-frame">` with a full-bleed section (same pattern as homepage). The story page is the highest-engagement surface. The framed image is a Phase 0 holdover. | Collection | 2 hrs | — |
| G9-06 | **Collections index: Phase 1 layout.** Change `collection-index-grid` from `grid-template-columns: minmax(0, 760px)` to `repeat(auto-fill, minmax(480px, 760px))`. Otherwise the index stays single-column when Yellowstone and Grand Canyon arrive. | Discovery | 5 min | Phase 1 |
| G9-07 | **Collection page: edition preview on CTA.** The `collection-cta-section` CTA ("Begin with the image that made Earth visible as home") routes to two buttons. Add a small edition-comparison row above the buttons: two items — Museum Print (24 × 20 in · Archival) / Digital Edition (High-resolution · For study) — each with a price or price-on-inquiry note. | Desirability | 1.5 hrs | — |
| G9-08 | **Place pages as discovery destinations.** `/places/yellowstone`, `/places/grand-canyon`, etc. with illustration teasers and links to incoming collections. Phase 1 gate. Without these, the "Discover" nav is a dead-end page of text cards. | Discovery | Phase 1 | Phase 1 |
| G9-09 | **Second collection.** The collections index, homepage `#collections` section, and story page all point to a single collection. The discovery architecture is correct but the discovery inventory is one item. Yellowstone is the natural second collection (highest governance readiness, MASTERWORK source candidates). | Collection + Discovery | Phase 1 | Phase 1 |
| G9-10 | **Provenance depth on collection page.** The collection page currently has no provenance (G8-03 adds the glance). To reach 9, add the full `<details>` provenance panel to the collection page — the same level of detail as the product page. The collection page is where institutional authority is established; the provenance record should be accessible here. | Collection | 30 min | after G8-03 |

---

## VII. Recommended Implementation Order

### Immediate (15–30 min total — fix before any promotion or sharing)

1. **G8-02** — naming fix. Two string changes. Pick "Oasis Collection" as canonical. Done.
2. **G8-04** — ManualPurchaseCTA copy. "Enquire about this edition" / "Send enquiry."
3. **G8-05** — pathway cards → links. All three → `/stories/earthrise` for now.
4. **G8-07** — featured works → links. All three → `/products/earthrise`.
5. **G8-08** — product image aspect ratio. One CSS property.

These five changes take under an hour and close the most visible gaps.

### Sprint 2-B (2–3 hrs — complete the 8/10 threshold)

6. **G8-01** — differentiate featured works visually
7. **G8-03** — provenance section on collection page
8. **G8-06** — specific place card copy
9. **G8-09** — next-journeys section on collection page
10. **G8-10** — breadcrumb on collection page

### Sprint 3 (3–4 hrs — story page + 9/10 threshold)

11. **G9-01** — story attribution block position
12. **G9-02** — story collection-teaser → edition cards
13. **G9-03** — story educationText fallback
14. **G9-04** — homepage hero lead
15. **G9-05** — story page full-bleed hero
16. **G9-07** — collection CTA edition preview
17. **G9-10** — full provenance panel on collection page

---

## VIII. What Makes This Collection Different From Its References

The curator statement on the collection page achieves something most reference models do not have for their Phase 0 state: a declarative voice that explains *why* the collection exists, not just *what* it contains. Rijksmuseum has this for Vermeer and Rembrandt. MoMA has it for its permanent collection. NatGeo has it for its photo archives. NC has it for Earthrise on day one.

The gap between 6.0 and 9.0 is not content. The content is there. The gap is execution details: link destinations, image differentiation, copy precision, and the story page's resistance to the improvements that have already been applied to every other page.

Once the 10 items in §VII Immediate + Sprint 2-B are complete, the collection platform will be at 8/10 across all three dimensions. That is competitive with MoMA and within one sprint of Rijksmuseum-tier quality.

---

*NC-WEB-008 Collection Platform Audit. Produced: 2026-06-12.*
