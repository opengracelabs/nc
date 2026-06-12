# NC-WEB-009 Premium Collection Audit
**Date:** 2026-06-12  
**Pages:** `/collections` · `/collections/earthrise` · `/` · `/stories/earthrise` · `/products/earthrise`  
**Reference:** Rijksmuseum · National Geographic · Apple · MoMA  
**Output:** Top 10 improvements ranked by impact

---

## What Prevents 8/10

Five barriers. All are single-component or single-file fixes.

**Barrier 1 — Collections index: three planned cards show the Earthrise photograph.**  
The collections index renders four cards. Earthrise is live with the correct image. Yellowstone, Grand Canyon, and Great Barrier Reef are planned — and all three currently inherit `imageSrc: earthriseImage` from the spread in `collections.ts` (lines 122–169). A visitor navigating to `/collections` sees four identical photographs of Earth from the Moon, three labeled with places that are not Earthrise. This is the most visible structural failure on the platform. It makes the collection inventory look broken rather than growing.

**Barrier 2 — Story page: attribution block between photograph and story body.**  
`<EarthriseAttributionBlock />` renders at line 40 of the story page — immediately after the `<figure>` and before `<div className="story-body">`. National Geographic flows: image → caption → paragraph one. No card interrupts. The Earthrise story page inserts a bordered attribution card at the most critical moment in the narrative — after the visitor has seen the photograph and before they read the first sentence. This has appeared as a priority fix in every audit since NC-WEB-004.

**Barrier 3 — ManualPurchaseCTA: "Contact for availability" / "Contact us."**  
The purchase panel says: h2 "Contact for availability," button "Contact us." "Contact for availability" sounds like the item may be out of stock. "Contact us" names the channel, not the action. Apple's product pages name the specific action ("Add to Bag"), which signals that the object is available now. The NC CTA should name the specific action toward the specific object: "Enquire about this edition" and "Send enquiry."

**Barrier 4 — Product image: `aspect-ratio: 1/1` at CSS line 475.**  
`.premium-product-image` has `aspect-ratio: 1 / 1`. With `object-fit: contain`, the landscape Earthrise photograph letterboxes in a square container — black above and below. This is the wrong product presentation for a print sold at museum-print scale. Five-minute CSS fix: `aspect-ratio: 4 / 3`.

**Barrier 5 — Story page: collection-teaser renders as four text spans.**  
The story page ends its narrative, provides a "View the Earthrise Collection" text link, then shows a `feature-section` with four `<span>` elements: "NASA source · Story · Print · Digital." This is a list of things that exist, not a path to owning one. MoMA's "Available in the Shop" section at the bottom of an artwork page shows product thumbnails with prices. The Earthrise story page shows text pills. A visitor who has read the entire story and is ready to act needs a visual object with a clear CTA, not a summary of categories.

---

## What Prevents 9/10

Four additional barriers after the above five are resolved. These require more than string changes.

**Barrier 6 — Story page: no full-bleed hero.**  
The homepage and collection page both have full-bleed heroes (`min-height: 100svh` and `92svh` respectively). The story page still uses a framed `<figure class="earthrise-frame story-image-frame">` — the same bordered, shadow-treated container that was the pre-Codex treatment for all pages. The story page is the highest-engagement surface: it's where visitors spend the most time. It deserves the same visual scale that the homepage applies to the same photograph.

**Barrier 7 — Collection page: no provenance section.**  
The product page has a full provenance architecture: `provenance-glance` tokens (NASA · Apollo 8 · December 24, 1968 · Public Domain) and a `<details>` panel with the complete source record. The collection page has no provenance. The Rijksmuseum places provenance on every object page — acquisition date, source institution, prior exhibition. The collection page is the canonical record holder for the Earthrise Oasis Collection; it should carry the same authority signal as the product page.

**Barrier 8 — Homepage hero lead: "A source-traceable edition of Earthrise."**  
"Source-traceable" is governance language. It describes the record-keeping system, not the experience. The lead should place the visitor in the moment: "The photograph that changed how humanity sees itself. Available as a museum-quality print and digital edition." This is the primary copy every visitor reads before making a decision about whether to explore further.

**Barrier 9 — No price signal anywhere.**  
No page on the site — not the homepage, not the collection page, not the product page — shows a price or a price-on-enquiry signal. Apple shows `$799` on every product family page. MoMA shows print prices on the shop page. Rijksmuseum shows prices in the download and shop sections. A visitor who has read the story, explored the collection, and arrived at the ManualPurchaseCTA has no idea what enquiring will cost them. "Price on enquiry" is a legitimate Phase 0 stance, but the absence of any signal creates uncertainty that suppresses action.

---

## Top 10 Improvements, Ranked by Impact

Each item is immediately actionable. Items 1–5 together cross the 8/10 threshold. Items 6–10 extend toward 9/10.

---

### 1. Fix collections index: remove or replace planned card images

**Impact:** Collection platform integrity. The three planned collection cards inherit the Earthrise photograph. Until each collection has its own source image, these cards should not show the Earthrise photograph.

**Options, in order of preference:**
- **Remove planned cards from the index entirely.** The `/collections` page shows only the Earthrise collection. "Coming soon" state belongs on the homepage "Next journeys" section, not in the authoritative collections index. This is the cleanest solution.
- **Use a styled CSS placeholder.** Give planned collections a dark gradient card with the place name as large text instead of an image. Add a `status: "planned"` CSS class that replaces `<img>` with a styled `<div>`.

**File:** `apps/web/lib/collections.ts` — move planned collections to a separate `plannedCollections` export; remove from `collections` array.  
**Also fix:** The "PLANNED COLLECTION" badge is internal governance language — replace with nothing, or omit the badge entirely on planned entries.  
**Effort:** 20 minutes.

---

### 2. Story page: move EarthriseAttributionBlock out of the narrative flow

**Impact:** Storytelling. The attribution card between the photograph and the story body has appeared as a priority fix in every audit since NC-WEB-004. It interrupts the highest-value moment in the reading experience.

**Fix:** Remove `<EarthriseAttributionBlock />` from between the figure and story body. It already exists in the figcaption (`NASA · Apollo 8 · William Anders · Public Domain`). Move the attribution block to the page's attribution section at the bottom (the same pattern as the homepage, where it is already in a dedicated `attribution-section`).

```tsx
// Remove from line 40 of stories/earthrise/page.tsx:
<EarthriseAttributionBlock />

// Add a dedicated section at the bottom of the article, before </article>:
<section className="section attribution-section">
  <EarthriseAttributionBlock />
</section>
```

**File:** `apps/web/app/stories/earthrise/page.tsx`  
**Effort:** 5 minutes.

---

### 3. ManualPurchaseCTA: name the action, not the channel

**Impact:** Desirability. "Contact us" is generic. "Send enquiry" names the specific action toward the specific object.

```tsx
// Current:
<p className="eyebrow">Availability</p>
<h2>Contact for availability</h2>
<p>Ask about {productName}. We will reply with availability, payment, and fulfillment details.</p>
<a className="button" href="...">Contact us</a>

// Replace with:
<p className="eyebrow">Own this edition</p>
<h2>Enquire about this edition</h2>
<p>{productName} is available as a Museum Print and Digital Edition. We reply within 24 hours with availability, payment, and shipping.</p>
<a className="button" href="...">Send enquiry</a>
```

**File:** `apps/web/components/ManualPurchaseCTA.tsx`  
**Effort:** 10 minutes.

---

### 4. Product image: restore landscape ratio

**Impact:** Desirability. One CSS property eliminates the letterboxed square frame.

```css
/* styles.css line 475 — change: */
.premium-product-image {
  aspect-ratio: 4 / 3;   /* was: 1 / 1 */
}

/* Also update the object-fit since letterboxing is no longer needed: */
.premium-product-image .earthrise-image {
  object-fit: cover;   /* was: contain */
}
```

**File:** `apps/web/app/styles.css`  
**Effort:** 5 minutes.

---

### 5. Story page: replace collection-teaser with edition cards

**Impact:** Desirability. The four text spans ("NASA source / Story / Print / Digital") are labels. Replace with two visual edition cards — Museum Print and Digital Edition — each with a one-line differentiator and an enquiry link.

**Structure:**
```tsx
<section className="section feature-section compact-section">
  <div>
    <p className="eyebrow">Collection</p>
    <h2>Earthrise: The Oasis Collection</h2>
    <p>
      The collection begins with AS08-14-2383. Own it in two editions:
      a Museum Print for display or a Digital Edition for study.
    </p>
    <Link href="/collections/earthrise" className="text-link">
      Explore the full collection
    </Link>
  </div>
  <div className="edition-comparison-grid">
    <article className="edition-panel museum-edition">
      <span className="edition-kicker">For display</span>
      <h3>Museum Print</h3>
      <p>24 × 20 inch archival giclée. Certificate of Authenticity included.</p>
      <Link href="/products/earthrise" className="text-link">Enquire →</Link>
    </article>
    <article className="edition-panel digital-edition">
      <span className="edition-kicker">For study</span>
      <h3>Digital Edition</h3>
      <p>High-resolution file with source and attribution notes.</p>
      <Link href="/products/earthrise" className="text-link">Enquire →</Link>
    </article>
  </div>
</section>
```

Also update the h2: "Earthrise: The **Oasis** Collection" (naming consistency — both the homepage and story page still say "Overview Collection").

**File:** `apps/web/app/stories/earthrise/page.tsx`  
**Effort:** 45 minutes.

---

### 6. Story page: full-bleed hero

**Impact:** Wonder + Storytelling. The homepage and collection page both present Earthrise at full viewport height. The story page still presents the same photograph in a bordered, shadow-treated frame. Visitors who reach the story from the homepage have already seen the image at full scale; they encounter it here at reduced scale.

**Fix:** Replace the framed `<figure>` and header with a full-bleed story hero, using the same CSS pattern as the homepage (`full-bleed-hero` with `collection-hero-copy`-style overlay). The story body then begins at the section below.

```tsx
// Replace:
<header className="story-header">...</header>
<figure className="earthrise-frame story-image-frame">...</figure>

// With:
<section className="collection-hero" aria-label="Earthrise story hero">
  <img className="collection-hero-image" src="..." alt="..." />
  <div className="collection-hero-copy">
    <p className="eyebrow light-eyebrow">Story · Apollo 8 · December 24, 1968</p>
    <h1>{heroText}</h1>
    <p className="lead hero-lead">
      On Christmas Eve 1968, Apollo 8 rounded the Moon and revealed
      Earth as a blue world rising above a gray horizon.
    </p>
  </div>
  <p className="hero-credit">NASA · Apollo 8 · William Anders · Public Domain</p>
</section>
```

**File:** `apps/web/app/stories/earthrise/page.tsx`  
**Effort:** 1 hour.

---

### 7. Collection page: add provenance section

**Impact:** Collection authority. The product page has a complete provenance architecture. The collection page — the canonical record holder — has no provenance signal. Add the same `provenance-glance` + `<details>` pattern used on the product page, between the collection narrative and discovery pathways.

```tsx
<section className="section compact-section provenance-section">
  <p className="eyebrow">Source record</p>
  <h2>Verified public domain.</h2>
  <div className="provenance-glance">
    <span>NASA</span>
    <span>Apollo 8</span>
    <span>December 24, 1968</span>
    <span>Public Domain</span>
  </div>
  <details className="provenance-panel">
    <summary>View full provenance</summary>
    <div className="provenance-detail-grid">
      <div><strong>Attribution</strong><p>{NASA_EARTHRISE_CREDIT}</p></div>
      <div><strong>Rights basis</strong><p>{EARTHRISE_RIGHTS}</p></div>
      <div><strong>Source identifier</strong><p>AS08-14-2383</p></div>
      <div><strong>Nonendorsement</strong><p>{NASA_NONENDORSEMENT}</p></div>
    </div>
  </details>
</section>
```

Zero new CSS required — all classes already exist.

**File:** `apps/web/app/collections/earthrise/page.tsx`  
**Effort:** 20 minutes.

---

### 8. Homepage hero lead: remove governance language

**Impact:** Wonder. "A source-traceable edition of Earthrise" describes the record system. The lead should place the visitor in the experience.

```tsx
// Current:
"A source-traceable edition of Earthrise, the photograph that turned lunar
exploration into a portrait of home."

// Replace with:
"The photograph that changed how humanity sees itself. Available as a
museum-quality print and digital edition."
```

**File:** `apps/web/app/page.tsx` line 20  
**Effort:** 5 minutes.

---

### 9. Collection page: differentiate featured works

**Impact:** Collection. The three works ("Earthrise Heritage Edition," "The Lunar Horizon," "The Overview Folio") all render the same `collection.imageSrc`. The `CollectionWork` type currently has no `imageSrc` field — all works inherit the collection hero image.

**Fix:** Add `imageSrc` and `objectPosition` to `CollectionWork` type. Give each work a distinct crop:

```typescript
// In collections.ts, extend CollectionWork:
export type CollectionWork = {
  title: string;
  label: string;
  copy: string;
  imageAlt: string;
  imageSrc: string;
  objectPosition: string; // CSS object-position value
};

// Update earthrise works:
works: [
  {
    title: "Earthrise Heritage Edition",
    label: "The Masterwork",
    imageSrc: earthriseImage,
    objectPosition: "center center", // full frame
    ...
  },
  {
    title: "The Lunar Horizon",
    label: "Detail Study",
    imageSrc: earthriseImage,
    objectPosition: "center 80%", // focus on lunar foreground
    ...
  },
  {
    title: "The Overview Folio",
    label: "Intellectual Record",
    imageSrc: earthriseImage,
    objectPosition: "center 20%", // focus on Earth
    ...
  }
]
```

Then in the collection page, pass `objectPosition` as an inline style on the `<img>`.

**Files:** `apps/web/lib/collections.ts`, `apps/web/app/collections/earthrise/page.tsx`  
**Effort:** 30 minutes.

---

### 10. Add a price signal to the product page

**Impact:** Desirability. No page on the site shows a price. This creates uncertainty that suppresses enquiry. Phase 0 can use a non-commitment price signal without locking to a transactional price.

Add a `<p className="price-signal">` line to `ManualPurchaseCTA` above the enquiry button:

```tsx
// In ManualPurchaseCTA, add before the button:
<p className="price-signal">Museum Print · Price on enquiry</p>
<p className="price-signal">Digital Edition · Price on enquiry</p>
```

Or add to each `edition-panel` in the comparison section:

```tsx
<div><dt>Price</dt><dd>Available on enquiry</dd></div>
```

The Rijksmuseum shows download prices on its object pages before visitors click "Download." Apple shows prices on every family page before a visitor opens the buy flow. A visitor who sees "Price on enquiry" knows: (1) this item is real, (2) it has a price, (3) getting that price requires action. Without this signal, there is no way to know if this is a commerce platform or a display archive.

**File:** `apps/web/components/ManualPurchaseCTA.tsx` or `apps/web/app/products/earthrise/page.tsx`  
**Effort:** 15 minutes.

---

## Summary

| # | Fix | Threshold | Effort |
|---|-----|-----------|--------|
| 1 | Collections index: remove planned cards with wrong images | 8/10 | 20 min |
| 2 | Story page: move attribution block to bottom section | 8/10 | 5 min |
| 3 | ManualPurchaseCTA: "Enquire about this edition" / "Send enquiry" | 8/10 | 10 min |
| 4 | Product image: `aspect-ratio: 4/3`, `object-fit: cover` | 8/10 | 5 min |
| 5 | Story page: replace teaser spans with edition cards | 8/10 | 45 min |
| 6 | Story page: full-bleed hero | 9/10 | 1 hr |
| 7 | Collection page: add provenance section | 9/10 | 20 min |
| 8 | Homepage hero lead: remove "source-traceable" | 9/10 | 5 min |
| 9 | Collection works: differentiate with `objectPosition` | 9/10 | 30 min |
| 10 | Product page: price signal ("Price on enquiry") | 9/10 | 15 min |

Items 1–5: **≈ 85 minutes combined.** Cross the 8/10 threshold.  
Items 6–10: **≈ 2 hours combined.** Extend toward 9/10.

---

## What Each Reference Would Change Today

**Rijksmuseum** — adds provenance to the collection page (item 7) immediately. Every Rijksmuseum object page carries the accession record. The collection page without a source record is an exhibit without a label.

**National Geographic** — removes the attribution block from between the photograph and the story (item 2). NatGeo story pages flow: image → caption → first sentence. Always.

**Apple** — changes "Contact us" to "Send enquiry" (item 3) and adds the price signal (item 10). Apple never presents a product without a price. Even bespoke configurations show "from $X."

**MoMA** — replaces the collection-teaser spans with visual edition cards (item 5). MoMA's "Available in the Shop" section shows the product visually before asking for a commerce action.

---

*NC-WEB-009 Premium Collection Audit. Produced: 2026-06-12.*
