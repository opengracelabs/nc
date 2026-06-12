# NC-WEB-005: Premium Experience Audit

| Field | Value |
|---|---|
| Document | NC-WEB-005 |
| Version | 1.0 |
| Status | **DRAFT** |
| Date | 2026-06-12 |
| Basis | Live code review · branch `v0.4.0-collection-000001` |
| Predecessor | NC-WEB-004 Final Audit (same branch, same date) |
| Reference models | Apple · National Geographic · Patagonia · Google Arts & Culture · Rijksmuseum |

---

## I. Changes Since NC-WEB-004

Before scoring, the record must be exact about what changed.

**Internal / non-visible changes:**
- `ProductSummary` type: `phase` field removed — eliminates one vector for "Phase 0" leaking into rendered UI
- `phaseZeroProducts` renamed to `earthriseProducts` — cleaner internal naming
- `getPhaseZeroProducts` renamed to `getEarthriseProducts` — matches new naming
- About page headline: "Public-domain commerce with visible provenance." → "Public-domain works, source-traceable editions." — marginally less governance-flavoured, still not editorial

**Experience-facing changes:** None.

The hero is still split-screen. No serif typeface has been added. `ManualPurchaseCTA` still reads "Request purchase" in both the h2 and button. No MASTERWORK badge exists. The collection teaser is still three bordered spans. Place card copy is still identical across all five cards. The footer still says "manual commerce only." The navigation still shows Places / Stories / Products / About.

**Verdict on the update:** The internal type cleanup is correct. It does not move a single experience score. The NC-WEB-004 recommendations have not yet been implemented.

---

## II. Benchmark Scoring

Scale: 1–10. Scores are for the NC site as it exists today, compared against the same five reference model homepages.

### Dimension 1: Wonder

| Site | Score | NC-WEB-004 | Delta |
|---|---|---|---|
| National Geographic | 10 | 10 | — |
| Rijksmuseum | 9 | 9 | — |
| Apple | 9 | 9 | — |
| Patagonia | 8 | 8 | — |
| Google Arts & Culture | 8 | 8 | — |
| **NC Current** | **4** | **4** | **0** |

The Earthrise photograph is present. It remains inside a rounded `.earthrise-frame` in the right column of a split-screen grid, occupying approximately 40% of horizontal viewport. The `.hero-immersive` class sets `min-height: 82vh` but the layout is still `grid-template-columns: 1.1fr 0.9fr` — text left, image right, padded, bordered, shadowed. The image is presented as an exhibit, not as an experience. Nothing here has changed.

---

### Dimension 2: Trust

| Site | Score | NC-WEB-004 | Delta |
|---|---|---|---|
| Rijksmuseum | 10 | 10 | — |
| Patagonia | 10 | 10 | — |
| National Geographic | 9 | 9 | — |
| Apple | 8 | 8 | — |
| Google Arts & Culture | 8 | 8 | — |
| **NC Current** | **5** | **5** | **0** |

Attribution is accurate. `EarthriseAttributionBlock` renders the correct NASA credit and nonendorsement text. The `governed-content.ts` strings are correct. No MASTERWORK badge. No Human Verified mark. No provenance panel. The trust signals that exist are correct; the trust signals that would differentiate NC from a generic print shop do not yet exist.

---

### Dimension 3: Beauty

| Site | Score | NC-WEB-004 | Delta |
|---|---|---|---|
| Apple | 10 | 10 | — |
| National Geographic | 9 | 9 | — |
| Patagonia | 8 | 8 | — |
| Rijksmuseum | 8 | 8 | — |
| Google Arts & Culture | 7 | 7 | — |
| **NC Current** | **4** | **4** | **0** |

`font-family: Inter, ui-sans-serif, ...` is the first declaration in the body rule. It is the only typeface declaration in the file. Every h1, every story paragraph, every product title, every attribution string, every nav link renders in the same geometric sans-serif. The colour tokens (`--ink`, `--accent`, `--gold`) are good. The `.earthrise-frame` figcaption is the strongest single designed element on any page. The layout is structurally sound. Without a serif typeface, the editorial register the content is reaching for does not exist in the visual layer.

---

### Dimension 4: Storytelling

| Site | Score | NC-WEB-004 | Delta |
|---|---|---|---|
| National Geographic | 10 | 10 | — |
| Patagonia | 9 | 9 | — |
| Rijksmuseum | 8 | 8 | — |
| Google Arts & Culture | 7 | 7 | — |
| Apple | 6 | 6 | — |
| **NC Current** | **5** | **5** | **0** |

The homepage "Why Earthrise matters" section has genuine editorial content: "A photograph that turned exploration back toward home" is a real headline. The two-column narrative paragraphs are specific and correct. The story page has three paragraphs of substantive copy below the image. These represent real improvements from the original skeleton. The narrative breaks down at the "Featured collection" section on both pages — three bordered spans labelled "Story / Museum Print / Digital Edition" — which kills momentum at precisely the moment it should accelerate. The story has a beginning and a middle. The momentum collapse at the collection teaser prevents it from ever reaching a destination.

---

### Dimension 5: Commerce

| Site | Score | NC-WEB-004 | Delta |
|---|---|---|---|
| Apple | 10 | 10 | — |
| Patagonia | 9 | 9 | — |
| Rijksmuseum | 7 | 7 | — |
| National Geographic | 4 | 4 | — |
| Google Arts & Culture | 1 | 1 | — |
| **NC Current** | **3** | **3** | **0** |

`ManualPurchaseCTA` — eyebrow "Purchase inquiry", h2 "Request purchase", button "Request purchase". The eyebrow changed. The h2 and button did not. Those are the elements visitors read and click. "Request" remains. The product page edition cards are text-only with bullet lists. No illustration appears on any edition card. No price appears on any page. The path from homepage intent to purchase action is: homepage → "View editions" → product page → "Request purchase" → `mailto:` link. Three pages and an email client. The commerce architecture is correct; the commerce experience does not yet exist.

---

### Dimension 6: Discovery

| Site | Score | NC-WEB-004 | Delta |
|---|---|---|---|
| Google Arts & Culture | 10 | 10 | — |
| National Geographic | 9 | 9 | — |
| Rijksmuseum | 9 | 9 | — |
| Patagonia | 7 | 7 | — |
| Apple | 6 | 6 | — |
| **NC Current** | **3** | **3** | **0** |

Navigation: Places / Stories / Products / About. The Wireframe Constitution mandates Places / Discover / Stories / Collections / Shop. "Collections" and "Discover" are absent. The "Next journeys" place section on the homepage shows five cards — all with the same copy: "Source-led stories, collections, and editions connected to this place." Yellowstone and the Grand Canyon, two of the most visually documented landscapes in American history, have the same description as each other and as Galápagos. There are no illustrator entry points, no era-based browsing, no thematic discovery modes.

---

## III. Score Comparison

| Dimension | NC-WEB-005 | NC-WEB-004 | Delta |
|---|---|---|---|
| Wonder | 4 | 4 | **0** |
| Trust | 5 | 5 | **0** |
| Beauty | 4 | 4 | **0** |
| Storytelling | 5 | 5 | **0** |
| Commerce | 3 | 3 | **0** |
| Discovery | 3 | 3 | **0** |
| **Total /60** | **24** | **24** | **0** |
| **Average /10** | **4.0** | **4.0** | **0** |

**The NC-WEB-004 recommendations have not been implemented. No experience score has moved.**

The internal type cleanup (`phaseZeroProducts` → `earthriseProducts`) is good hygiene. It prevents the `phase: "Phase 0"` field from ever surfacing in a component. That is worth keeping. It does not change what any visitor sees or feels.

---

## IV. Top 20 Remaining Weaknesses

The NC-WEB-004 top 10 are carried forward unchanged (none implemented). Ten additional weaknesses are identified here for the first time.

### Carried Forward from NC-WEB-004

**W-01 · Hero is framed, not immersive** *(Wonder −3)*

The photograph of the whole Earth from 240,000 miles away is displayed in a grid column with a border-radius, a box-shadow, and a figcaption bar. `.hero-image-frame` has `min-height: 520px` and lives inside a two-column grid. The most important visual in NC's catalog is being presented as though it were a product thumbnail.

Every reference model that builds around a single anchor image — NatGeo, Patagonia, Apple, Rijksmuseum — places that image at full viewport scale. The hero must become `width: 100vw; height: 100svh`. The `.earthrise-frame` framing belongs on the product page detail view, not on any landing surface.

---

**W-02 · No serif typeface** *(Beauty −3, Storytelling −2)*

The entire typographic register of the site is Inter. The `body` font-family declaration lists Inter, then UI sans-serif system fonts. There is no serif fallback, no serif variable, no serif usage anywhere in the CSS file.

Serif type is not decoration. It is the visual signal that differentiates an editorial institution from a technology product. NatGeo uses a bold serif for feature headlines. The Rijksmuseum uses a refined serif for work titles and exhibition copy. Patagonia uses a humanist serif for their environmental essays. The register those typefaces create is inseparable from the trust and authority those brands hold.

NC's content — 200-year-old expedition illustrations, provenance narratives, curatorial copy — is editorial in nature. It should look editorial.

Fix: `@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap')` + `--font-serif: 'Cormorant Garamond', Georgia, serif` + apply to `h1` on story/collection/place pages and `.story-body-wide`.

---

**W-03 · "Request purchase" on every commerce CTA** *(Commerce −2)*

`ManualPurchaseCTA`: `h2 = "Request purchase"`, `button text = "Request purchase"`. These are the two elements visitors interact with. The eyebrow was updated to "Purchase inquiry" — that is the line no one reads. The h2 and button are the experience.

"Request" frames the visitor as a petitioner. "Enquire" frames them as a qualified buyer seeking information about a significant acquisition. The Rijksmuseum shop says "Add to cart." Christie's says "Register to bid." High-value art commerce says "Enquire." The word change is one line of code.

Fix: h2 → "Enquire about this edition", button → "Send enquiry".

---

**W-04 · Collection teaser is text spans** *(Storytelling −2, Commerce −1)*

Both the homepage and the story page have a "Featured collection" section that ends with `.collection-teaser` — three or four bordered `<span>` elements reading "Story / Museum Print / Digital Edition" and "NASA source / Story / Print / Digital." These look like radio buttons for a form that does not exist.

The collection feature section is the second major commercial surface on both pages. It should show the work, tell the collection thesis in one sentence, and offer a clear path. Instead it provides a text taxonomy with no visual or narrative content.

---

**W-05 · MASTERWORK quality tier badge does not exist** *(Trust −2, Desire −2)*

NC's governance system has assigned MASTERWORK status to the Earthrise photograph — the highest designation in the Asset Intelligence Constitution, required for museum print activation, mandated for curator and PA approval. No visitor sees this designation anywhere.

The badge token `--gold: #b37a2b` exists in the CSS. The value judgement has been made. The design element that communicates it has not been built. A gold MASTERWORK badge at the top of the product page commerce panel would tell the visitor — before they read a single word — that this work has been judged exceptional by people who know the field. That is a desire signal. It is not a compliance label.

---

**W-06 · No illustrations on edition or place cards** *(Commerce −2, Wonder −1)*

Edition cards on the product page: text-only bullet lists. Place cards on the homepage and places index: text-only titles with identical copy. A visual commerce platform with no visuals on its commerce surfaces is a contradiction.

The Rijksmuseum product pages lead with the work at full scale. Patagonia product cards lead with photography. Apple product cards are the product. NC's edition cards could show a thumbnail of the print. The place cards could show the best illustration from NC's governed catalog for that place.

---

**W-07 · No progressive provenance panel** *(Trust −2)*

The product page "Source record" section currently renders:
```
{EARTHRISE_RIGHTS}
Source: NASA. Asset ID: AS08-14-2383. Human reviewed: yes.
```

This is raw data. It is correct. It communicates nothing about why provenance depth is a feature rather than a requirement.

The provenance story — that this specific image was traced from NASA's archive, rights confirmed under 17 U.S.C. § 105, human-reviewed through an eight-gate process before being offered for sale — is NC's deepest commercial differentiator. It is currently hidden inside a `<p>` tag below a section heading.

---

**W-08 · Footer "manual commerce only"** *(Trust −1)*

Every page renders the footer: "Verified public-domain sources, visible attribution, manual commerce only."

"Manual commerce only" describes an operational limitation. It appears on the bottom of the homepage, the story page, the product page, and every other page. It is the last thing every visitor reads. Patagonia's footer: "We're in business to save our home planet." The Rijksmuseum footer: Rijksmuseum wordmark, open-access statement, institution links. NC's footer should say something about what NC is, not what NC cannot yet do.

---

**W-09 · Navigation missing Collections and Discover** *(Discovery −2)*

Current nav: Places / Stories / Products / About.

Wireframe Constitution v1 mandates: Places / Discover / Stories / Collections / Shop.

"Collections" is a commercial and editorial entry point that NC-WEB-004 defined a template for. "Discover" is the entry point for illustrator-led and era-led browsing — the two discovery modes that separate NC from a product catalog. Neither exists in the navigation. The navigation is the primary signal of what NC is. The current nav says: this is a publication with a shop. The correct nav says: this is a discovery platform with a commerce layer.

---

**W-10 · Place cards have identical generic copy** *(Storytelling −1, Discovery −1)*

"Source-led stories, collections, and editions connected to this place." This appears on Yellowstone. Grand Canyon. Great Barrier Reef. Galápagos. Earthrise. Identically.

Each of these places has specific, historically resonant illustrated material in NC's governed catalog. The copy should reflect that specificity:

| Place | What the copy should say |
|---|---|
| Yellowstone | Hayden Survey, 1871. The expedition that made it a national park. |
| Grand Canyon | Powell Survey, 1869. A one-armed Civil War veteran mapping 1,450 km of unmapped canyon. |
| Great Barrier Reef | Haeckel, 1899. Chromolithographs of coral that has since largely bleached. |
| Galápagos | Darwin and Gould, 1845. The finches that changed the understanding of life. |

This is a data change in `governed-content.ts` and a rendering change in the place card component. No infrastructure required.

---

### New Findings (NC-WEB-005)

**W-11 · Story page h1 fallback is a single word** *(Storytelling −1)*

When `getReviewedPageGeneration("story", "earthrise")` returns null — which it does in Phase 0 with no approved AI content — the h1 renders as `"Earthrise"`. One word.

The page has an excellent lead paragraph immediately below ("On Christmas Eve 1968, Apollo 8 rounded the Moon and revealed Earth as a blue world rising above a gray horizon."). But the headline that anchors the page, drives search indexing, and sets the editorial register is a single noun.

The fallback for `heroText` should be a real headline: "Earthrise: The Photograph That Made Earth the Subject" or "What Apollo 8 Saw Looking Back" or any specific, editorial construction. Fix: replace the fallback string in the page with a governed editorial headline stored in `governed-content.ts`.

---

**W-12 · Attribution block interrupts the story page reading flow** *(Storytelling −2, Beauty −1)*

Story page render order: header → image → `EarthriseAttributionBlock` → story body text.

The attribution block — `border: 1px solid var(--line); border-radius: 8px; background: var(--panel); padding: 22px` — is styled identically to a card. It appears as a full-width content block between the photograph and the story. A visitor who has just encountered the Earthrise image for the first time is immediately interrupted by a bordered compliance panel before the story begins.

The `EarthriseAttributionBlock` contains necessary and correct information. Its position and visual weight are wrong. On every reference model — NatGeo, Patagonia, Rijksmuseum — the photo credit is a small text line within or immediately below the image, not a full-width bordered section between the image and the story.

Fix: Move the attribution text into the `figcaption` (extend what's already there) or render it as a small muted line directly below the figure. Remove the card-styled `attribution-block` from the story body flow.

---

**W-13 · Product image is cropped square, destroying the photograph's composition** *(Beauty −2, Wonder −1)*

`.product-image-frame { aspect-ratio: 1 / 1 }` forces a square crop on the Earthrise photograph. The original AS08-14-2383 is a landscape frame — Earth and Moon occupy the right side of the frame, with black space on the left. A 1:1 crop either cuts the composition or adds black bars. Neither is correct for a museum print product page.

The product page is the one place where the photograph should be presented with maximum fidelity to the original. A square crop on a landscape photograph communicates that NC does not know what the photograph looks like. This damages both Wonder and trust simultaneously.

Fix: Remove `aspect-ratio: 1 / 1` from `.product-image-frame`. Use `aspect-ratio: 4 / 3` or `aspect-ratio: auto` and let the image determine its own proportions.

---

**W-14 · "Source-traceable" in the homepage hero lead** *(Storytelling −1)*

"Earthrise changed the scale of human imagination: a single photograph from lunar orbit, now presented as a source-traceable story and edition."

"Source-traceable" is a governance concept embedded in the primary value proposition. It describes the product's provenance architecture in technical terms. The visitor who reads "source-traceable story" has been handed a compliance certificate where they expected an invitation.

The provenance should be felt, not described. "Now presented as a story and edition, with the full source record visible." Or: "Available for the first time as a verified, museum-quality edition." The verification exists. The word "source-traceable" does not need to be in the lead.

---

**W-15 · About page is three governance cards, not a story** *(Storytelling −2, Trust −1)*

The About page currently has three cards: "Public domain first", "Rights verification", "Attribution visible." These are compliance checkboxes. They answer: "What does NC do?" They do not answer: "Why does NC exist? What was the problem before NC? What becomes possible now?"

Patagonia's About page is an essay about Yvon Chouinard building climbing equipment in a California blacksmith shop. NatGeo's About page is the story of 130 years of geographic exploration. The Rijksmuseum's About page explains the relationship between a 17th-century Dutch trading nation and the art it produced.

NC has an equivalent story: the greatest illustrated records of the natural world were made between 1750 and 1900, then entered the public domain, then sat in library archives accessible only to researchers — until now. That is a story worth telling. Three compliance cards are not.

---

**W-16 · No hover states on interactive cards** *(Beauty −1, Commerce −1)*

The `.card` class has no `:hover` pseudo-class defined. Every card on the site — edition cards, place cards, collection teasers — gives no visual affordance when hovered. The visitor does not know the card is clickable until they move their cursor and see the pointer change.

Every reference model provides immediate interactive feedback. The Rijksmuseum uses a subtle lift. Patagonia uses a slight scale and shadow. Apple uses a background-colour change. The absence of hover states makes the site feel static and unresponsive.

Fix: Add to `.card`: `transition: box-shadow 0.15s ease, transform 0.15s ease;` and `.card:hover { box-shadow: 0 8px 24px rgb(23 32 27 / 12%); transform: translateY(-2px); }`.

---

**W-17 · Two equal-weight hero CTAs create decision paralysis** *(Commerce −1)*

The homepage hero has: `[Explore Earthrise]` (solid green button) and `[View editions]` (secondary outlined button). Both are rendered as buttons at the same visual weight. A visitor who has not decided what they want — which is every first-time visitor — faces a fork with no clear direction.

Apple has one CTA above the fold. NatGeo has one. Patagonia has one. The primary CTA should dominate. The secondary should be a text link, not a button.

Fix: Remove the secondary button class from "View editions". Render as `.text-link` with a `→` arrow. This creates clear hierarchy: primary action is "Explore Earthrise", secondary option is available for those who already know they want to buy.

---

**W-18 · No Open Graph tags or structured data** *(Discovery −1)*

The `<html lang="en">` is present. There are no `og:image`, `og:title`, `og:description`, no Twitter Card meta tags, no JSON-LD structured data (Product, ImageObject, Organization).

When someone shares the Earthrise product page on social media, the preview shows the plain meta description and no image. The Earthrise photograph — one of the most reproduced images in history — is the visual anchor for the NC brand. It should be the OpenGraph image for every NC page.

Fix: Add to the Next.js `layout.tsx` metadata export: `openGraph: { images: ['/images/earthrise-as08-14-2383.jpg'] }` and page-level overrides for title and description. Add JSON-LD `Product` schema to the product page.

---

**W-19 · No keyboard navigation or focus styles beyond browser defaults** *(Trust −1)*

Tabbing through the navigation and interactive elements reveals browser-default focus rings (or in some cases no visible focus ring). There are no custom focus styles in `styles.css`. `:focus-visible` is not defined for buttons, links, or cards.

Accessibility is a trust signal. An institution that publishes verified, human-reviewed content should be as rigorous about who can access it as about the rights status of the images. The absence of visible focus styles communicates carelessness at the implementation level — the same layer where the provenance verification happens.

Fix: Add `:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 4px; }` to the global stylesheet.

---

**W-20 · No page-level `<meta name="description">` differentiation** *(Discovery −1)*

Current meta descriptions:
- Homepage: "Verified public-domain heritage stories, places, and products."
- Story page: "The Apollo 8 Earthrise photograph with NASA attribution."
- Product page: "Earthrise Museum Giclee and Digital Edition with NASA-only attribution."
- About: "Nature & Culture source, rights, and attribution commitments."

These are functional descriptions. They do not create search clickthrough. NatGeo story descriptions say things like: "Before satellite photography, before conservation movements, the Great Barrier Reef was documented by a German scientist who had never seen it." That is a description that makes you click.

NC's descriptions describe what the page contains. They should create desire to visit the page. The story page description should make you want to read the story. The product page description should make you want to see the print.

---

## V. Fastest Path to 8/10

Current score: 24/60 (4.0 avg). Target: 48/60 (8.0 avg). Gap: 24 points across six dimensions.

The fastest path is three sequential sprints. Each sprint is achievable within a single working session.

---

### Sprint 1 — Visual Foundation
**Target: 4.0 → 6.0 · Estimated time: 4–6 hours**

These are CSS and copy changes only. No new components, no new pages, no new data.

| Change | Dimensions affected | Points gained |
|---|---|---|
| Full-bleed hero: `width: 100vw; min-height: 100svh` on homepage and story page, image as background-image or positioned behind overlay | Wonder +3 | 3 |
| Add Cormorant Garamond: one `@import`, one CSS variable, apply to `h1` on story/collection pages and `.story-body-wide` | Beauty +2, Storytelling +1 | 3 |
| Fix product image aspect ratio: remove `aspect-ratio: 1 / 1` from `.product-image-frame` | Beauty +1, Wonder +1 | 2 |
| Move `EarthriseAttributionBlock` from story body flow into `figcaption` extension | Storytelling +1, Beauty +1 | 2 |
| Add `.card:hover` transition | Beauty +1 | 1 |
| Replace "source-traceable" in homepage lead | Storytelling +1 | 1 |
| Replace "View editions" secondary button with text link | Commerce +1 | 1 |

**Sprint 1 total: +13 points. New score: 37/60 (6.2 avg)**

Post-Sprint 1 by dimension: Wonder 7, Trust 5, Beauty 7, Storytelling 6, Commerce 4, Discovery 3

---

### Sprint 2 — Trust and Commerce
**Target: 6.2 → 7.2 · Estimated time: 4–6 hours**

Component changes and copy decisions. No new pages required.

| Change | Dimensions affected | Points gained |
|---|---|---|
| Add MASTERWORK badge: `<span class="badge badge--masterwork">◆ Masterwork</span>` on product page, define `.badge--masterwork` with `--gold` token | Trust +2, Commerce +1 | 3 |
| Replace "Request purchase" with "Enquire about this edition" (h2) and "Send enquiry" (button) in `ManualPurchaseCTA` | Commerce +2 | 2 |
| Replace collection teaser spans with a visual module (image thumbnail + one sentence + CTA) | Storytelling +2, Commerce +1 | 3 |
| Add provenance panel: collapsed credit line + "See full provenance" → expanded narrative panel | Trust +2 | 2 |
| Replace footer "manual commerce only" with mission-register copy | Trust +1 | 1 |
| Write specific one-sentence description for each place in `governed-content.ts` | Storytelling +1, Discovery +1 | 2 |
| Story page: replace single-word `heroText` fallback with a real editorial headline | Storytelling +1 | 1 |
| Add `:focus-visible` styles | Trust +1 | 1 |
| Add Open Graph tags and JSON-LD to product page | Discovery +1 | 1 |

**Sprint 2 total: +16 points. New score: 43/60 (7.2 avg)**

Post-Sprint 2 by dimension: Wonder 7, Trust 8, Beauty 7, Storytelling 8, Commerce 7, Discovery 4

---

### Sprint 3 — Discovery and Content
**Target: 7.2 → 8.0 · Estimated time: 6–8 hours · Requires Phase 1 content gates**

This sprint requires illustration thumbnails (governed assets per place), a collection page, and navigation changes. Some items need Phase 1 SA gates before activation; others can be built speculatively.

| Change | Dimensions affected | Points gained | Gate |
|---|---|---|---|
| Add Collections and Discover to nav | Discovery +2 | 2 | Phase 0: Collections links to `/collections/earthrise`. Discover is a stub. |
| Build `/collections/earthrise` page (NC-WEB-004 §V.4 template) | Discovery +2, Commerce +2 | 4 | NC-COLLECTIONS-001 must be drafted. Earthrise collection uses already-authorized assets. |
| Add illustration thumbnails to edition cards on product page | Commerce +2, Wonder +1 | 3 | Phase 0: Earthrise image available. |
| Add illustration thumbnails to place cards (per-place governed assets) | Wonder +1, Discovery +1 | 2 | Phase 1: requires governed assets per place to exist |
| Rebuild About page as mission narrative | Storytelling +2, Trust +1 | 3 | Phase 0: human-authored, no governance gate |

**Sprint 3 total: +14 points. New score: 48/60 (8.0 avg)**

Post-Sprint 3 by dimension: Wonder 8, Trust 9, Beauty 7, Storytelling 10, Commerce 9, Discovery 8

**Note on Sprint 3 caveats:** The illustrated place card thumbnails (Wonder +1, Discovery +1) require governed illustration assets per place, which are Phase 1 gated. If Sprint 3 proceeds without those assets, the score is approximately 7.7. The 8.0 average is achievable at Phase 1 activation.

---

## VI. The 8/10 Benchmark — What It Requires

To score 8/10 against Apple, NatGeo, Patagonia, GAC, and Rijksmuseum simultaneously across all six dimensions, NC needs to do three things that none of the reference models fully do:

1. **Illustrate the place** — NatGeo has photography. Patagonia has place photography. NC can have something neither of them has: 200-year-old expedition illustration of the exact places on the product page. Haeckel's 1899 chromolithograph of the Great Barrier Reef on the GBR place card is a more powerful discovery signal than any modern photograph, because it is unexpected.

2. **Make provenance a desire signal** — The Rijksmuseum comes closest to this. NC can exceed it because NC's provenance is constitutional, not just scholarly. The eight-gate verification process, the Human Verified mark, the MASTERWORK designation — these can be presented as marks of distinction that increase the desirability of the print, not legal disclaimers that accompany it.

3. **Complete the narrative arc** — NatGeo is the master of this. Every page has a beginning, a middle, and an end. The story leads to the image, the image leads to the meaning, the meaning leads to the desire. NC has a beginning ("Why Earthrise matters") and a middle (editorial copy). It needs to complete the arc: from story to collection to product, with each step feeling like the natural next thing rather than a navigation decision.

These three capabilities are what justify a score of 8.0+ and what no reference model fully combines in a single platform. NC's content — verified public-domain, place-anchored, historically significant illustration — is the raw material. The experience layer is the work remaining.

---

## VII. Implementation Priority

If one change is made before any other, it is **W-01: full-bleed hero**.

The entire experience of NC changes when the Earthrise photograph occupies the full viewport. Wonder moves from 4 to 7 in a single CSS edit. The headline "The world seen whole" becomes what it is meant to be: a caption for an experience, not a description of a business.

The order after that:

| Priority | Change | Why first |
|---|---|---|
| 1 | Full-bleed hero (W-01) | Highest wonder impact, lowest effort |
| 2 | Serif typeface (W-02) | Highest beauty impact, one CSS import |
| 3 | Fix product image aspect ratio (W-13) | Active error — it destroys the photograph's composition |
| 4 | Move attribution block (W-12) | Active error — interrupts story flow |
| 5 | "Enquire" replaces "Request purchase" (W-03) | Highest commerce impact on existing surface |
| 6 | MASTERWORK badge (W-05) | No new infrastructure — uses existing `--gold` token |
| 7 | Specific place card copy (W-10) | Data change only, zero dev cost |
| 8 | Collection teaser visual module (W-04) | Unlocks the commercial arc |
| 9 | Provenance panel (W-07) | Deep trust signal, medium effort |
| 10 | Collections in nav + /collections/earthrise (W-09) | Opens the discovery dimension |

The first four items can be done in under two hours. The gap between 4.0 and 6.0 is CSS edits and one copy change. That is the fastest path to a site that no longer embarrasses its governance.

---

*NC-WEB-005 Premium Experience Audit v1.0 · 2026-06-12 · Principal Architect*
