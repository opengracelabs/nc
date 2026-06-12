# NC-WEB-005 Visual Audit
**Date:** 2026-06-12  
**Baseline:** NC-WEB-004 Final Audit (4.0/10)  
**Scope:** Live rendered pages after Codex implementation — /, /products/earthrise, /stories/earthrise  
**Method:** Browser render via Playwright + `curl` fetch of rendered HTML. No code review. Scores based on what a visitor experiences, not what the code implements.

---

## I. Score Summary

| Dimension     | NC-WEB-004 | NC-WEB-005 | Delta | Sprint 1 Target |
|---------------|-----------|-----------|-------|-----------------|
| Wonder        | 4         | **7**     | +3    | 7               |
| Trust         | 5         | **7**     | +2    | 7               |
| Beauty        | 4         | **6**     | +2    | 6               |
| Storytelling  | 5         | **6**     | +1    | 6               |
| Commerce      | 3         | **5**     | +2    | 5               |
| Discovery     | 3         | **6**     | +3    | 6               |
| **Overall**   | **4.0**   | **6.2**   | **+2.2** | **6.2**      |

Sprint 1 target from NC-WEB-005 was 6.2. Actual post-Codex score: **6.2.** Projection was accurate.

Reference model targets for orientation:
- Apple: 8.2 · NatGeo: 8.5 · Patagonia: 8.5 · Google Arts & Culture: 6.8 · Rijksmuseum: 8.5

---

## II. What Changed: Page-by-Page Observations

### Homepage (`/`)

**RESOLVED:**

**W-01 — Full-bleed hero.** The hero is now `<section class="full-bleed-hero">` containing `<img class="full-bleed-hero-image">`. The old `hero-image-frame` border-radius framing is gone. The photograph fills the section. Overlay copy sits inside `<div class="full-bleed-hero-copy">`. A single `<p class="hero-credit">NASA · Apollo 8 · William Anders · Public Domain</p>` anchors attribution at the bottom of the hero. This is the single most impactful change across all pages.

**W-05 — MASTERWORK badge.** `<span class="masterwork-badge">MASTERWORK</span>` appears on both the collection cards in the featured collection section and on the product card in the discovery section. The badge exists as a designed element.

**W-04 — Collection section with images.** The homepage now has `<section id="collections" class="collection-section">` containing a `<ul class="collection-card-grid">` with 3 `<li class="collection-card image-card">` items, each with an `<img>` tag. The previous version had no visual collection grid.

**W-09 — Navigation labels.** Navigation updated: `Collections → /#collections` / `Discover → /places` / `Editions → /products` / `About → /about`. The missing "Collections" and "Discover" L1 items from the prior audit are now present.

**W-08 — Footer.** Changed from "Verified public-domain sources, visible attribution, manual commerce only." to "Public-domain sources, visible attribution, source-traceable editions." Governance qualifier removed. "Manual commerce only" removed from visitor-facing surface.

**PERSISTING:**

**W-14 — "source-traceable" in hero lead.** The primary pitch inside the full-bleed hero reads: "A source-traceable edition of Earthrise." "Source-traceable" is internal governance language. Visitors read: "a thing whose sources can be traced." The intended message is desire for a specific artifact. Suggested copy: "The first photograph of the whole Earth. Now available as a museum-quality giclée print."

**W-10 — Identical place card copy.** All 5 place cards still render identical body text: "Source-led stories, collections, and editions connected to this place." Discovery fails at the discovery section. Zero differentiation between Yellowstone, Grand Canyon, Great Barrier Reef, Earthrise, and the Moon.

**W-17 — Two equal-weight CTAs.** The hero still renders two buttons (`light-button` and `ghost-button`). Visual hierarchy slightly improved — the light button (primary) is marginally more prominent than the ghost button — but both are buttons. The secondary CTA should be a text link to reduce decision paralysis.

---

### Product Page (`/products/earthrise`)

**RESOLVED:**

**W-07 — Progressive provenance.** The product page now implements `<details class="provenance-panel"><summary>View full provenance</summary>` with a `<div class="provenance-detail-grid">` containing full provenance records (Attribution, Rights basis, Source identifier, Nonendorsement). Above the details element, `<div class="provenance-glance">` renders token-level data: NASA · Apollo 8 · December 24, 1968 · Public Domain. This is a clean, correct implementation of the three-level progressive provenance architecture specified in NC-WEB-005.

**W-05 — MASTERWORK badge on product page.** The badge row on the product page now leads with `<span class="masterwork-badge">MASTERWORK</span>`. It appears before the rights badge and verified-pd badge. This is the correct order (quality signal before rights signal).

**W-11 (partial) — Edition comparison structure.** Edition panels are now `<article class="edition-panel museum-edition">` and `<article class="edition-panel digital-edition">` with structured `<dl>` description lists. The previous bullet-list implementation is replaced with a semantic definition list format.

**PERSISTING — CRITICAL:**

**W-03 — "Request purchase."** `ManualPurchaseCTA` still renders with:
- `<h2>Request purchase</h2>` — at the decision moment, the h2 announces that what follows is a bureaucratic request process
- `<a class="button" ...>Request purchase</a>` — the CTA label reinforces it
- The eyebrow was updated to "Purchase inquiry" but that makes it worse: eyebrow + h2 + button all signal "form" not "action"

Suggested fix: h2 → "Enquire about this edition" · button → "Send enquiry" · body → "Reply within 24 hours with availability, payment, and shipping." This is a four-string change.

**W-13 — Product image aspect ratio (status unknown).** The product image uses classes `earthrise-frame product-image-frame premium-product-image`. The new `premium-product-image` class may have fixed the `aspect-ratio: 1/1` crop identified in NC-WEB-005. Status cannot be confirmed without CSS inspection. If still 1:1, the landscape Earthrise photograph is cropped to a square — the most critical composition error on the site.

---

### Story Page (`/stories/earthrise`)

The story page received no material changes in the Codex implementation pass. All NC-WEB-005 findings persist without change.

**PERSISTING — all unchanged:**

**W-11 — Story page h1 fallback.** The h1 still renders "Earthrise" (single word). This is the full-page headline on the primary story surface. Every reference model — NatGeo, Patagonia, Rijksmuseum — writes editorial headlines for their flagship stories. "Earthrise" is a label, not an opening.

**W-12 — Attribution block position.** `EarthriseAttributionBlock` renders as a card-styled section immediately after the `<figure>` and before the story body. A visitor reads: photograph → attribution card → story. Attribution should be in the figcaption or rendered as a small muted line below the figure. The current position interrupts the moment of first emotional contact with the story.

**W-04 (story page) — Collection teaser.** The `collection-teaser` below the story body still renders as four `<span>` elements: "NASA source" / "Story" / "Print" / "Digital". This is not a visual commerce module; it is a text list of things that exist.

**W-06 (story page) — Governance language in body.** The `educationText` fallback still reads: "Nature & Culture presents the image as a verified public-domain work with source, rights, and attribution visible beside the experience." This is internal operations language in the body of a story page. Visitors encounter it at the end of a story they came to read.

**Not applied to story page — Full-bleed hero.** The homepage hero was changed to full-bleed. The story page still uses `<figure class="earthrise-frame story-image-frame">` — a framed image, not a full-width hero. The story page is the highest-engagement surface on the site. The homepage visitor converts to a story reader. That reader still encounters the pre-Codex framed image treatment.

---

## III. Dimension Analysis: NC-WEB-005 vs NC-WEB-004

### Wonder: 4 → 7 (+3)

The full-bleed hero is the one change that moves Wonder. The Earthrise photograph now fills the section. The frame is gone. The credit line is at the bottom. This is a correct implementation. The score does not reach 8 because: (a) the hero lead copy still says "source-traceable"; (b) the story page — where wonder compounds — is still framed; (c) no serif typeface was added, so the editorial headline ("The world seen whole.") renders in Inter rather than a typeface that signals cultural weight.

Reference gap: NatGeo Wonder = 10. Gap remains in editorial voice, story page treatment, and typeface.

### Trust: 5 → 7 (+2)

Two changes move Trust: MASTERWORK badge (quality signal exists) and progressive provenance panel (confidence path exists). Both are correctly implemented. The "Request purchase" h2 offsets trust gains — when a visitor has been convinced by MASTERWORK and provenance, the CTA headline "Request purchase" undermines the institutional register built on every screen that preceded it. No "Human Verified" mark present. No structured data (JSON-LD).

### Beauty: 4 → 6 (+2)

New CSS classes suggest visual improvement: `premium-product-layout`, `image-card`, `masterwork-badge`, `edition-panel`, `provenance-section`. The collection grid with images on the homepage is a genuine visual improvement over the previous text-only card list. Beauty does not reach 7 because: no serif typeface; story page unchanged; product image aspect ratio status unknown.

### Storytelling: 5 → 6 (+1)

Homepage and product page improved. Collection section on homepage has real images. Product page has a narrative arc: MASTERWORK → image → editions → provenance → why it matters. The story page — the only page explicitly designed to tell a story — is unchanged. h1 "Earthrise" is not a story headline. The attribution block interrupts. The collection teaser is a text list. Storytelling scores one point higher because the supporting pages (homepage, product) improved, but the primary storytelling surface did not.

### Commerce: 3 → 5 (+2)

MASTERWORK badge and progressive provenance create the conditions for desire. The visitor now encounters quality and authenticity signals before encountering the CTA. The Commerce score does not improve past 5 because the CTA still says "Request purchase" — the provenance pipeline was built and then the last ten feet to a sale remain broken.

Rijksmuseum Commerce = 7. Gap is in the CTA and in the absence of edition card images. The visitor can read that a Museum Edition exists at $480 + framing, but cannot see the product variant they are being asked to buy.

### Discovery: 3 → 6 (+3)

The largest score gain. "Collections" and "Discover" are now in the top navigation. The collection grid on the homepage creates visual discovery — three image cards instead of zero. The jump from 3 to 6 reflects that discovery was completely absent and is now partially present. Place cards still have identical copy, which means the discovery destination (/places) does not differentiate.

---

## IV. Top 20 Remaining Weaknesses

Ranked by estimated visitor impact.

| # | Weakness | Page(s) | Category | Effort |
|---|----------|---------|----------|--------|
| R-01 | ManualPurchaseCTA: h2 "Request purchase" + button "Request purchase" — commerce kill at decision moment | /products/earthrise | Commerce | 15 min |
| R-02 | Story page: no full-bleed hero — primary story surface still framed | /stories/earthrise | Wonder | 2 hrs |
| R-03 | Story page h1 = "Earthrise" — label not headline | /stories/earthrise | Storytelling | 30 min |
| R-04 | EarthriseAttributionBlock between photograph and story body — interrupts narrative flow | /stories/earthrise | Storytelling | 1 hr |
| R-05 | No serif typeface — all editorial headlines render in Inter, no cultural weight | All | Beauty | 30 min |
| R-06 | Identical place card copy for all 5 places — discovery fails at discovery section | / | Discovery | 1 hr |
| R-07 | Hero lead "A source-traceable edition of Earthrise" — governance language in primary pitch | / | Wonder | 15 min |
| R-08 | Collection teaser on story page = 4 text spans — not a visual commerce module | /stories/earthrise | Storytelling | 2 hrs |
| R-09 | educationText fallback = governance language in story body | /stories/earthrise | Storytelling | 30 min |
| R-10 | Product image aspect ratio status unknown — may still be 1:1 cropping landscape Earthrise | /products/earthrise | Beauty | 15 min |
| R-11 | Two equal-weight CTAs in homepage hero — decision paralysis (secondary should be text link) | / | Commerce | 15 min |
| R-12 | No edition card thumbnails — visitor asked to buy a product they cannot see | /products/earthrise | Commerce | 2 hrs |
| R-13 | About page = three compliance cards — not a story about who made this | /about | Trust | 3 hrs |
| R-14 | No Open Graph tags or JSON-LD structured data — link previews are unbranded | All | Trust | 1 hr |
| R-15 | No card hover states — place cards, collection cards, product cards have no visual affordance | All | Beauty | 1 hr |
| R-16 | Meta descriptions are functional, not editorial — no clickthrough signal | All | Discovery | 30 min |
| R-17 | Place cards: no illustrations — discovery destination shows text only | / /places | Beauty | 3 hrs (Phase 1 gate) |
| R-18 | Product page: "MASTERWORK" in all-caps mid-sentence in lead — typographically awkward | /products/earthrise | Beauty | 15 min |
| R-19 | Story page: no commerce module integration — the story ends, then there is a teaser, then nothing visible pulls to product | /stories/earthrise | Commerce | 2 hrs |
| R-20 | No `:focus-visible` styles — keyboard navigation has no visual affordance beyond browser defaults | All | Trust | 30 min |

---

## V. Path to 8.0/10

Three remaining sprints from the NC-WEB-005 projection. Sprint 1 is complete.

### Sprint 2 (current) — Components + copy → 7.2/10
Estimated: 4–6 hours.  
All items are copy edits, component edits, or CSS additions. No new pages required.

1. **R-01** — ManualPurchaseCTA: h2 → "Enquire about this edition" / button → "Send enquiry" / body → "Reply within 24 hours."  
2. **R-03** — Story page h1: "On Christmas Eve, 1968, humanity saw itself from the outside for the first time."  
3. **R-04** — EarthriseAttributionBlock: move to figcaption below the image. Remove card styling.  
4. **R-05** — Add Cormorant Garamond or Lora via Google Fonts for editorial headlines (h1, h2, `.editorial-lead`).  
5. **R-06** — Five unique one-line place card descriptions in `governed-content.ts`.  
6. **R-07** — Hero lead: remove "source-traceable edition" copy. Replace with desire-oriented line.  
7. **R-09** — Story educationText fallback: remove governance language. Replace with curatorial note.  
8. **R-10** — Confirm / fix product image aspect ratio (`premium-product-image` CSS check).  
9. **R-11** — Homepage hero: secondary CTA → plain text link, not a button.  
10. **R-14** — Add Open Graph tags and JSON-LD `ImageObject` to product and story pages.  
11. **R-15** — Add hover state CSS to `.collection-card`, `.place-card`, `.product-card`.  
12. **R-16** — Update `<meta name="description">` for homepage, story, and product pages.  

**Projected score after Sprint 2:** Wonder 7 · Trust 8 · Beauty 7 · Storytelling 8 · Commerce 7 · Discovery 6 = **7.2/10**

### Sprint 3 — New pages + content → 8.0/10
Estimated: 6–8 hours.

1. **R-02** — Story page: full-bleed hero with William Anders quote overlay.  
2. **R-08** — Collection teaser on story page → visual collection module with image cards.  
3. **R-12** — Edition card thumbnails: Earthrise print and digital mockup images.  
4. **R-13** — About page: narrative story (who, what, why — 400 words).  
5. **R-17** — Place card illustrations (Phase 1 gate — gated on NC-COLLECTIONS-001).  
6. **R-19** — Story page: commerce module before footer.  

**Projected score after Sprint 3:** Wonder 8 · Trust 9 · Beauty 8 · Storytelling 9 · Commerce 8 · Discovery 7 = **8.2/10**

---

## VI. Critical Path

**Highest-impact single action remaining: R-01 (ManualPurchaseCTA copy).**  
Fifteen minutes of work. Four string changes. The entire provenance pipeline, MASTERWORK badge, and progressive disclosure investment leads to a CTA headline that says "Request purchase." Fix it before Sprint 2 begins.

**Highest-impact page remaining: story page (`/stories/earthrise`).**  
The story page received zero changes in the Codex pass. It is the highest-engagement surface — a visitor who reads the story is the visitor closest to a purchase. R-02 through R-04 and R-08 through R-09 are all concentrated here. Sprint 2 and Sprint 3 should lead with story page work.

**Gap before NC-COLLECTIONS-001 can be drafted:**  
Collection page (/collections/earthrise) and R-17 (place card illustrations) require NC-COLLECTIONS-001. This governance document does not exist. The Earthrise collection page may be built as a Phase 0 proof of concept before NC-COLLECTIONS-001 is ratified, per NC-WEB-004 §V.4.

---

## VII. What Codex Got Right

Three architectural choices in the Codex implementation are worth preserving:

1. **`<details>` + `<summary>` for provenance.** A clean, accessible, no-JS implementation of progressive disclosure. Collapses by default, expands on click, has semantic meaning. This is the right component for provenance at all quality levels.

2. **`provenance-glance` above the details element.** Rendering the token-level attribution (NASA · Apollo 8 · December 24, 1968 · Public Domain) as always-visible inline tokens before the expandable panel is the correct Level 0 / Level 1 hierarchy. Visitors who only glance still receive attribution. Visitors who want depth can expand.

3. **`edition-comparison-grid` with `<dl>`.** Moving edition comparison from bullet lists to description lists (term/definition pairs) is semantically correct and communicates the same data with more visual and semantic structure. This architecture supports future edition types without modification.

---

*NC-WEB-005 Visual Audit. Produced: 2026-06-12.*
