# NC-WEB-010 Launch Readiness Review
**Date:** 2026-06-12  
**Branch:** v0.4.0-collection-000001  
**Pages:** `/` · `/stories/earthrise` · `/products/earthrise` · `/collections` · `/collections/earthrise`

---

## What's Resolved Since NC-WEB-009

The collection platform has materially advanced. Before cataloguing what remains:

| Item | Status |
|------|--------|
| `Breadcrumbs` component on collection page (Home / Collections / Earthrise) | ✅ |
| `ProvenanceGlance` component — 5-item grid (Source, Mission, Date, Frame, Rights) | ✅ |
| `FeaturedWorksGrid` — differentiated crops via `imageTreatment` + CSS `object-position` | ✅ |
| `NextJourneys` section — dark background, 3 journey cards with hover states | ✅ |
| OG meta tags on collection page (`openGraph: title, description, type, images`) | ✅ |
| `alternates.canonical` on collection page | ✅ |
| `metadataBase` in layout.tsx | ✅ |
| Collection index grid: `repeat(auto-fit, minmax(260px, 1fr))` (Phase 1 ready) | ✅ |
| `CollectionExperience.tsx` component file | ✅ |

What follows is what remains. Each item is described with its page, the user-facing effect, and a precise fix.

---

## 1. What Still Looks Amateur

**A — Collections index: three planned cards show the Earthrise photograph.**  
`/collections` renders four cards. All four use `collection.imageSrc`. The `plannedCollection()` factory spreads `...earthriseCollection` without overriding `imageSrc`, so Yellowstone, Grand Canyon, and Great Barrier Reef all display Earth rising above the lunar surface. A visitor who shares `/collections` or navigates to it directly sees four identical photographs with three wrong labels. This is the most visible quality failure on the platform.

**B — "PLANNED COLLECTION" badge.**  
The three planned collection cards carry `badge: "PLANNED COLLECTION"`. This is governance language. A public visitor reading "PLANNED COLLECTION" encounters internal project management vocabulary. Replace with nothing, or omit the badge entirely on `status: "planned"` entries.

**C — ManualPurchaseCTA: "Contact for availability" / "Contact us."**  
The purchase panel on the product page has h2 "Contact for availability" (implies stock uncertainty) and button "Contact us" (names the channel, not the action). This has persisted through every audit since NC-WEB-004. Compare: Apple "Add to Bag", MoMA "Buy print", Rijksmuseum "Download". The specific action toward the specific object is the standard. Required: "Enquire about this edition" / "Send enquiry."

**D — Product image: letterboxed landscape in a square frame.**  
`.premium-product-image` has `aspect-ratio: 1/1` with `object-fit: contain` (`styles.css` line 475). The Earthrise photograph is landscape (~3:2). It renders with black bars above and below inside a square container. This is the wrong product presentation for a print sold at 24 × 20 inches.

**E — Naming inconsistency: "Overview" vs "Oasis."**  
The homepage `#collections` section is headed "Earthrise: The Overview Collection" (line 55 of `page.tsx`). The story page feature-section is headed "Earthrise: The Overview Collection" (line 75 of `stories/earthrise/page.tsx`). The canonical collection name is "Earthrise: The Oasis Collection" — used on `/collections`, on `/collections/earthrise`, and in `collections.ts`. Two surfaces say one name, two surfaces say another. A visitor who reads the homepage and then visits the collection page sees different titles for the same thing.

**F — Hero lead: "A source-traceable edition of Earthrise."**  
The homepage hero — the first copy a visitor reads below the headline — says "A source-traceable edition of Earthrise, the photograph that turned lunar exploration into a portrait of home." "Source-traceable edition" is internal governance vocabulary. It describes the record-keeping system, not the photograph or the experience. It has persisted across five audits.

**G — ProvenanceGlance before curator statement: data before drama.**  
The collection page renders in this order: Hero → `<ProvenanceGlance>` (light green data grid) → `curator-statement-section` (dark blockquote). A visitor descends from the full-bleed hero into a grid of data labels (Source / Mission / Date / Frame / Rights) before they reach the page's best content. The curator statement — "We went to the Moon to discover the Moon. Instead, we found ourselves." — should follow the hero immediately. Provenance belongs after the narrative, where it functions as authority confirmation rather than an interruption.

---

## 2. What Still Feels Unfinished

**H — Story page: attribution block between image and story body.**  
`<EarthriseAttributionBlock />` renders at story page line 40 — after the `<figure>` and before the `<div className="story-body">`. A bordered, padded card interrupts between the photograph and the first paragraph. This was identified as the #1 story-page issue in NC-WEB-004, NC-WEB-005, NC-WEB-007, NC-WEB-008, and NC-WEB-009. Five audits. The fix is 5 minutes: delete line 40, add a `<section className="section attribution-section">` at the bottom of the page.

**I — Story page: collection-teaser renders as four text spans.**  
The story page ends its narrative with a feature-section containing four `<span>` elements: "NASA source / Story / Print / Digital." These are category labels, not a commerce module. A visitor who has read the entire story is the highest-intent visitor on the platform — they want to know what to do next. They receive a list of things that exist.

**J — Story page: educationText fallback.**  
`educationText` fallback is: "Nature & Culture presents the image as a verified public-domain work with source, rights, and attribution visible beside the experience." This renders in the "Why Earthrise matters" section's two-column copy, as one of two editorial paragraphs. It is internal operations language placed in editorial body copy.

**K — Pathway cards: no links.**  
The three discovery pathway cards (The Thin Blue Line / The Lunar Cradle / The Movement Icon) have hover states but no destinations. They have 280px min-height, `transform: translateY(-2px)` on hover, a subtle box-shadow — all the visual affordance of a clickable element, with none of the function.

**L — Featured works cards: no links.**  
The three featured works (Earthrise Heritage Edition / The Lunar Horizon / The Overview Folio) have differentiated image treatments and editorial copy but no link to anywhere. A visitor drawn to "The Lunar Horizon" has no action available.

**M — NextJourneys: all three links say "Continue."**  
The three journey cards at the bottom of the collection page all use "Continue" as link text. "Continue" is a navigation label for the same sequence. These are three different destinations (story, editions, collections) — the link text should name the destination or the action: "Read the story," "View editions," "Browse all collections."

**N — No price signal.**  
No page on the platform shows a price, a price range, or a "price on enquiry" indicator. An enquiring visitor has no anchor for expectation. This is the single largest gap between NC and every commercial reference model (Apple, MoMA, Rijksmuseum). The floor for Phase 0 is "Price on enquiry" in the edition panels.

**O — No OG meta tags on story page or product page.**  
`/stories/earthrise` and `/products/earthrise` have `<Metadata>` objects with `title` and `description` but no `openGraph` property. When these pages are shared on social media or via messaging apps, the preview renders with text only — no image, no styled title, no description card. The collection page has OG tags. The two pages most likely to be shared commercially do not.

---

## 3. What Blocks Public Sharing

Three issues make the platform embarrassing to share before they are fixed:

1. **Item A** — Collections index: four cards, all showing the Earthrise photograph, three labeled as places that are not space. This is the first thing a visitor sees when clicking "Collections" in the nav.

2. **Item O** — No OG tags on story and product pages. Social shares of `/stories/earthrise` (the most linked page) and `/products/earthrise` (the most commercially relevant page) render as text-only links.

3. **Item E** — "Overview Collection" vs "Oasis Collection" naming conflict. A visitor who screenshots the homepage and the collection page for a newsletter or post will see two different titles for the same collection. This reads as either a mistake or a rebrand in progress.

---

## 4. What Blocks First Sale

Four issues are directly on the purchase path:

1. **Item C** — ManualPurchaseCTA: "Contact us." The last action a visitor takes before potentially enquiring is clicking a button that says "Contact us." This is the lowest-specificity, lowest-conviction CTA in commerce.

2. **Item N** — No price signal. A visitor ready to buy has no idea whether this is a $50 print or a $500 print. "Price on enquiry" is a legitimate answer that still sets an expectation.

3. **Item D** — Product image 1:1 with black bars. A visitor on the product page evaluating a 24 × 20 inch print sees the photograph letterboxed in a square. The product is misrepresented by its own page.

4. **Item I** — Story page collection-teaser. The visitor who has read the full story — the highest-intent visitor — encounters four text spans where an edition comparison module should be.

---

## 5. What Blocks 8/10 Experience

Eight items prevent 8/10:

**Item A** (collections index images), **Item C** (CTA copy), **Item D** (product image), **Item E** (naming), **Item F** (hero lead), **Item G** (provenance placement), **Item H** (attribution block), **Item I** (collection-teaser).

These eight together represent the gap between the current 6.5/10 and 8/10. Items A–I combined take under 2 hours.

---

## Top 15 Fixes, Ranked by Impact

Fixes 1–8 reach 8/10. Fixes 9–15 extend toward 9/10.

---

### Fix 1 — Collections index: remove Earthrise image from planned cards

**Category:** Blocks public sharing · Looks amateur  
**Effort:** 15 minutes

The `plannedCollection()` factory spreads `...earthriseCollection` without overriding `imageSrc`. Add a `placeholderSrc` field or use a CSS-only placeholder for planned entries. Simplest fix: add an optional `imageSrc` override to the factory call, passing a dark gradient data URL or a CSS class that substitutes the image with a styled placeholder:

```typescript
// Option 1 (simplest): exclude planned collections from the public array
export const collections: CollectionMetadata[] = [earthriseCollection];
// Move plannedCollections to a separate export used only in admin/future contexts

// Option 2: add placeholder imageSrc override in plannedCollection() factory
function plannedCollection(...): CollectionMetadata {
  return {
    ...earthriseCollection,
    imageSrc: "/images/collection-placeholder.jpg", // dark solid or gradient
    ...
  };
}
```

Also remove the "PLANNED COLLECTION" badge string or replace it with nothing on planned entries.

---

### Fix 2 — ManualPurchaseCTA: name the action

**Category:** Blocks first sale · Looks amateur  
**Effort:** 10 minutes

```tsx
// apps/web/components/ManualPurchaseCTA.tsx
<p className="eyebrow">Own this edition</p>
<h2>Enquire about this edition</h2>
<p>
  {productName} is available as a Museum Print and Digital Edition.
  We reply within 24 hours with availability, payment, and shipping.
</p>
<a className="button" href="mailto:natureandculture@protonmail.com?subject=Earthrise edition enquiry">
  Send enquiry
</a>
```

---

### Fix 3 — Product image: restore landscape ratio

**Category:** Blocks first sale · Looks amateur  
**Effort:** 5 minutes

```css
/* apps/web/app/styles.css line 474–480 */
.premium-product-image {
  aspect-ratio: 4 / 3;   /* was: 1 / 1 */
}

.premium-product-image .earthrise-image {
  object-fit: cover;     /* was: contain */
}
```

---

### Fix 4 — Story page: move attribution block to page bottom

**Category:** Feels unfinished · Blocks 8/10  
**Effort:** 5 minutes

```tsx
// apps/web/app/stories/earthrise/page.tsx
// Delete line 40: <EarthriseAttributionBlock />

// Add at bottom of <article>, before </article>:
<section className="section attribution-section">
  <EarthriseAttributionBlock />
</section>
```

The `figcaption` ("NASA · Apollo 8 · William Anders · Public Domain") already provides Level 0 attribution at the image. The full `EarthriseAttributionBlock` is redundant mid-narrative and appropriate at the page footer.

---

### Fix 5 — Naming: "Overview Collection" → "Oasis Collection" everywhere

**Category:** Looks amateur · Blocks 8/10  
**Effort:** 10 minutes  
**Two files, two changes:**

```tsx
// apps/web/app/page.tsx line 55:
<h2>Earthrise: The Oasis Collection</h2>   // was: "The Overview Collection"

// apps/web/app/stories/earthrise/page.tsx line 75:
<h2>Earthrise: The Oasis Collection</h2>   // was: "The Overview Collection"
```

---

### Fix 6 — Collection page: move ProvenanceGlance after narrative

**Category:** Looks amateur · Blocks 8/10  
**Effort:** 10 minutes

The current page order is: Hero → ProvenanceGlance → Curator Statement → Narrative. The correct arc is: Hero → Curator Statement → Narrative → ProvenanceGlance (as authority confirmation, not introduction).

```tsx
// apps/web/app/collections/earthrise/page.tsx
// Move <ProvenanceGlance items={collection.provenanceGlance} />
// from line 50 (between hero and curator-statement)
// to after the collection-narrative-section, before the pathways section.
```

Also update the `ProvenanceGlance` eyebrow from "Provenance glance" (lowercase, informal) to "Source record" to match the product page register.

---

### Fix 7 — Homepage hero lead: remove governance language

**Category:** Looks amateur · Blocks 8/10  
**Effort:** 5 minutes

```tsx
// apps/web/app/page.tsx line 19–22:
<p className="lead hero-lead">
  The photograph that changed how humanity sees itself.
  Available as a museum-quality print and digital edition.
</p>
```

---

### Fix 8 — Story page: replace collection-teaser with edition cards

**Category:** Blocks first sale · Feels unfinished  
**Effort:** 45 minutes

Replace the `feature-section` containing four text spans with a visual edition comparison using existing `edition-panel` CSS:

```tsx
// apps/web/app/stories/earthrise/page.tsx — replace feature-section:
<section className="section compact-section">
  <p className="eyebrow">Editions</p>
  <h2>Own Earthrise: The Oasis Collection.</h2>
  <div className="edition-comparison-grid">
    <article className="edition-panel museum-edition">
      <span className="edition-kicker">For display</span>
      <h3>Museum Print</h3>
      <p>24 × 20 inch archival giclée. Certificate of Authenticity and NASA attribution included.</p>
      <Link href="/products/earthrise" className="text-link">Enquire about this edition →</Link>
    </article>
    <article className="edition-panel digital-edition">
      <span className="edition-kicker">For study</span>
      <h3>Digital Edition</h3>
      <p>High-resolution file for close study, teaching, and archival use.</p>
      <Link href="/products/earthrise" className="text-link">Enquire about this edition →</Link>
    </article>
  </div>
</section>
```

Remove the existing "Own Earthrise" section below — the edition comparison replaces it.

---

### Fix 9 — Add OG meta tags to story and product pages

**Category:** Blocks public sharing  
**Effort:** 20 minutes

```tsx
// apps/web/app/stories/earthrise/page.tsx
export const metadata: Metadata = {
  title: "Earthrise Story",
  description: "On Christmas Eve 1968, Apollo 8 revealed Earth as a world seen whole.",
  openGraph: {
    title: "Earthrise — Nature & Culture",
    description: "On Christmas Eve 1968, Apollo 8 revealed Earth as a world seen whole.",
    type: "article",
    images: ["/images/earthrise-as08-14-2383.jpg"]
  }
};

// apps/web/app/products/earthrise/page.tsx
export const metadata: Metadata = {
  title: "Earthrise",
  description: "Museum Print and Digital Edition of NASA AS08-14-2383. Public domain.",
  openGraph: {
    title: "Earthrise — Museum Print & Digital Edition",
    description: "Museum-quality print of NASA AS08-14-2383. Verified public domain. 24 × 20 inch archival giclée.",
    type: "website",
    images: ["/images/earthrise-as08-14-2383.jpg"]
  }
};
```

---

### Fix 10 — Add price signal to edition panels

**Category:** Blocks first sale  
**Effort:** 15 minutes

A visitor on the product page has no price anchor. Add a `Price` row to each edition's `<dl>`:

```tsx
// apps/web/app/products/earthrise/page.tsx — museum-edition dl:
<div><dt>Price</dt><dd>Available on enquiry</dd></div>

// digital-edition dl:
<div><dt>Price</dt><dd>Available on enquiry</dd></div>
```

This tells the visitor: the item has a price, getting that price requires action. Preferable to silence.

---

### Fix 11 — Pathway cards and featured works: add links

**Category:** Feels unfinished  
**Effort:** 10 minutes

**Pathways** — each card should link to the story page (the only content destination Phase 0 can offer):

```tsx
// apps/web/app/collections/earthrise/page.tsx — in pathway map:
<article className="pathway-card" key={pathway.title}>
  <p className="eyebrow">{pathway.theme}</p>
  <h3>{pathway.title}</h3>
  <p>{pathway.copy}</p>
  <Link href="/stories/earthrise" className="text-link">Explore →</Link>
</article>
```

**Featured works** — each card should link to the product page:

```tsx
// apps/web/components/CollectionExperience.tsx — FeaturedWorksGrid:
// Add after <p>{work.copy}</p>:
<Link href="/products/earthrise" className="text-link">View editions →</Link>
```

---

### Fix 12 — NextJourneys: specific link text

**Category:** Feels unfinished  
**Effort:** 10 minutes

Update `collections.ts` `nextJourneys` data — replace "Continue" label with the action:

```typescript
nextJourneys: [
  { ..., label: "Read the story" },      // href: /stories/earthrise
  { ..., label: "View editions" },        // href: /products/earthrise
  { ..., label: "Browse collections" }    // href: /collections
]
```

Update `NextJourneys` component to use `journey.label` instead of the hardcoded "Continue":

```tsx
// apps/web/components/CollectionExperience.tsx line 76:
<Link href={journey.href}>{journey.label ?? "Continue"}</Link>
```

Add `label?: string` to the `NextJourney` type in `collections.ts`.

---

### Fix 13 — Story page: replace educationText fallback

**Category:** Feels unfinished · Amateur  
**Effort:** 10 minutes

The `educationText` fallback renders as editorial body copy in the "Why Earthrise matters" section:

```tsx
// Current fallback:
"Nature & Culture presents the image as a verified public-domain work with source,
rights, and attribution visible beside the experience."

// Replace with:
"Earthrise is held by NASA under 17 U.S.C. § 105. Every edition is printed from
the same verified source file, AS08-14-2383, with NASA attribution and a statement
of rights."
```

---

### Fix 14 — Place cards: one specific line per place

**Category:** Feels unfinished  
**Effort:** 30 minutes

Five place cards on the homepage, all saying "Source-led stories, collections, and editions connected to this place." Update `governed-content.ts`:

```typescript
export const placeTeasers = [
  { slug: "earthrise",         title: "Earthrise",           copy: "The photograph that made Earth the subject." },
  { slug: "yellowstone",       title: "Yellowstone",         copy: "America's first national park, painted in its golden age." },
  { slug: "grand-canyon",      title: "Grand Canyon",        copy: "A geological portrait of deep time." },
  { slug: "great-barrier-reef",title: "Great Barrier Reef",  copy: "The largest living structure on Earth, documented at its peak." },
  { slug: "galapagos",         title: "Galapagos",           copy: "The islands that changed the theory of life." }
];
```

Update `homepage/page.tsx` to use `place.copy` instead of the hardcoded string.

---

### Fix 15 — Footer: remove "source-traceable"

**Category:** Minor polish  
**Effort:** 2 minutes

```tsx
// apps/web/app/layout.tsx footer:
<p>Public-domain heritage, visible attribution, editions with provenance.</p>
// was: "Public-domain sources, visible attribution, source-traceable editions."
```

---

## Summary Table

| # | Fix | Category | File | Time |
|---|-----|----------|------|------|
| 1 | Collections index: planned cards with wrong images | Public sharing / Amateur | `lib/collections.ts` | 15 min |
| 2 | ManualPurchaseCTA: "Enquire about this edition" / "Send enquiry" | First sale | `ManualPurchaseCTA.tsx` | 10 min |
| 3 | Product image: `aspect-ratio: 4/3`, `object-fit: cover` | First sale / Amateur | `styles.css` | 5 min |
| 4 | Story page: attribution block → page bottom | Unfinished / 8/10 | `stories/earthrise/page.tsx` | 5 min |
| 5 | Naming: "Overview" → "Oasis" on homepage and story | Amateur | `page.tsx` + `stories/earthrise/page.tsx` | 10 min |
| 6 | ProvenanceGlance: move after narrative, fix eyebrow | Amateur / 8/10 | `collections/earthrise/page.tsx` | 10 min |
| 7 | Hero lead: remove "source-traceable" | Amateur / 8/10 | `page.tsx` | 5 min |
| 8 | Story page: edition cards replacing teaser spans | First sale / 8/10 | `stories/earthrise/page.tsx` | 45 min |
| 9 | OG meta tags on story and product pages | Public sharing | `stories/earthrise/page.tsx` + `products/earthrise/page.tsx` | 20 min |
| 10 | Price signal: "Available on enquiry" in edition panels | First sale | `products/earthrise/page.tsx` | 15 min |
| 11 | Pathway cards + featured works: add links | Unfinished | `collections/earthrise/page.tsx` + `CollectionExperience.tsx` | 10 min |
| 12 | NextJourneys: specific link labels | Unfinished | `lib/collections.ts` + `CollectionExperience.tsx` | 10 min |
| 13 | Story educationText fallback: curatorial copy | Amateur | `stories/earthrise/page.tsx` | 10 min |
| 14 | Place cards: specific per-place descriptions | Unfinished | `lib/governed-content.ts` + `page.tsx` | 30 min |
| 15 | Footer: remove "source-traceable" | Polish | `layout.tsx` | 2 min |

**Fixes 1–8: ~105 minutes combined. Platform reaches 8/10 and is ready for public sharing.**  
**Fixes 9–15: ~97 minutes combined. Platform reaches 9/10 threshold.**

---

## Platform State After All 15 Fixes

| Dimension | Now | After 1–8 | After 1–15 |
|-----------|-----|-----------|------------|
| Collection | 7 | 8 | 9 |
| Discovery | 6 | 7 | 8 |
| Desirability | 5 | 8 | 9 |
| Storytelling | 6 | 8 | 9 |
| **Average** | **6.0** | **7.75 → 8** | **8.75 → 9** |

The remaining gap between 9 and 10 is content volume: a second collection, place pages with illustrations, and a direct purchase flow (beyond mailto). All three are Phase 1 gates, not code fixes.

---

*NC-WEB-010 Launch Readiness Review. Produced: 2026-06-12.*
