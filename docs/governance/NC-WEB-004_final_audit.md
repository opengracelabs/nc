# NC-WEB-004: Final Experience Audit

| Field | Value |
|---|---|
| Document | NC-WEB-004 Appendix A |
| Version | 1.0 |
| Status | **DRAFT** |
| Date | 2026-06-12 |
| Scope | NC homepage scored against five reference models across six experience dimensions |
| Basis | Live code review of `apps/web/` — current branch `v0.4.0-collection-000001` |

---

## I. What Has Already Been Fixed

Before scoring, it is important to record what the NC homepage has already resolved since the first audit. Several critical issues are gone:

| Fixed | Evidence |
|---|---|
| CSS gradient placeholder replaced | `<img src="/images/earthrise-as08-14-2383.jpg">` is present and serving |
| "Phase 0" eyebrow removed | Replaced with "Apollo 8 · December 24, 1968" |
| Governance headline removed | Replaced with "The world seen whole." |
| "Coming soon" status labels removed | Place cards render title only, no status |
| Internal product codes removed from headings | Product cards show titles, not NC-PROD-001 |
| Attribution block moved to page footer | No longer inline with hero content |
| Editorial narrative added | "Why Earthrise matters" two-column section present |
| `ManualPurchaseCTA` eyebrow updated | Now reads "Purchase inquiry" |

These are meaningful improvements. The site has moved from a governance skeleton to a functional page. The question this audit answers is: **what is the gap between a functional page and a world-class one?**

---

## II. Benchmark Scoring

Scale: 1–10 per dimension. Scores reflect the homepage as a visitor experiences it.

### Scoring Key

| Score | Meaning |
|---|---|
| 1–3 | Absent or harmful — creates a negative impression or communicates nothing |
| 4–5 | Present but inert — the element exists but does not move the visitor |
| 6–7 | Functional — does its job, not distinguished |
| 8–9 | Strong — creates clear emotional response or converts with intention |
| 10 | Benchmark — the definitive execution of this dimension in digital commerce |

---

### Dimension 1: Wonder

*Does the page stop you? Does it create a moment of awe before you read anything?*

| Site | Score | Basis |
|---|---|---|
| **National Geographic** | **10** | Full-bleed editorial photography that defines the opening moment. The image is not decorating the page — it is the page. No text competes with it above the fold. |
| **Rijksmuseum** | **9** | Works by Rembrandt, Vermeer, and Van Gogh at scale. The cultural weight of the works creates wonder before the design does. The homepage image changes and surprises. |
| **Apple** | **9** | Cinematic full-bleed product shots. Deliberate silence — what is NOT shown creates tension. The image occupies the screen. |
| **Patagonia** | **8** | Wild-place photography: open water, rock faces, weather. The places feel dangerous and alive. The scale is correct. |
| **Google Arts & Culture** | **8** | Density creates wonder through variety — forty famous works visible at once. You have never seen all of these in the same place before. |
| **NC Current** | **4** | The Earthrise photograph is present but confined to the right column of a split-screen grid. It occupies approximately 40% of horizontal space. The `.earthrise-frame` has a border radius and a figcaption, which further frames it as an exhibit rather than an experience. The wonder is there in the image — it is being suppressed by the layout. |

---

### Dimension 2: Trust

*Do you believe this institution before you have read a word of copy?*

| Site | Score | Basis |
|---|---|---|
| **Rijksmuseum** | **10** | 200 years of institutional authority, open-access commitment, full scholarly provenance on every work. If they call it public domain, it is. |
| **Patagonia** | **10** | Every signal confirms the mission: B Corp certification, environmental litigation record, Fair Trade, Ironclad Guarantee, "Don't buy this jacket." Trust through radical transparency. |
| **National Geographic** | **9** | 130 years of editorial authority. The yellow border is the trust signal — you recognise it globally before reading anything. |
| **Apple** | **8** | Trust through design quality. A page this precise implies a product this precise. No legal copy required — the craftsmanship speaks. |
| **Google Arts & Culture** | **8** | Partner museums are the Uffizi, the Met, the British Museum. Trust by institutional association. |
| **NC Current** | **5** | Attribution text is present and accurate. Rights are stated. But trust is communicated as compliance — two lines of plain text in a bordered box at the bottom of the page. There are no quality tier badges, no Human Verified mark, no designed provenance system. The governance infrastructure is real and rigorous; the visitor sees none of it. |

---

### Dimension 3: Beauty

*Is this page beautiful? Does the visual design create pleasure independent of the content?*

| Site | Score | Basis |
|---|---|---|
| **Apple** | **10** | The gold standard. Photography, typography, whitespace, micro-interactions. Every pixel justified. The visual language is immediately recognizable and aspirational. |
| **National Geographic** | **9** | Rich visual language: bold serif typography, saturated editorial photography, the yellow border as a colour-accent system. The typeface alone communicates authority. |
| **Patagonia** | **8** | Natural-materials aesthetic. Earthy palette tied to the places in the imagery. High-quality outdoor photography with movement and weather. |
| **Rijksmuseum** | **8** | Clean, restrained museum aesthetic. The works carry the visual weight; the interface steps back. Typographic hierarchy is strong and legible. |
| **Google Arts & Culture** | **7** | Functional and clean. Not beautiful. The works are beautiful; the UI is serviceable. |
| **NC Current** | **4** | Inter is used for every text element: governance notes, editorial copy, product titles, captions, navigation. There is no typographic register — all words look identical. The `.earthrise-frame` with its dark figcaption is the strongest designed element on the page. The green-and-gold token system (`--accent`, `--gold`) is good and coherent. But without a serif typeface, the editorial register NC is reaching for does not exist in the visual layer. The layout is structurally sound but visually generic — it could be any content platform. |

---

### Dimension 4: Storytelling

*Does this page tell a story? Does it create a narrative arc that pulls you forward?*

| Site | Score | Basis |
|---|---|---|
| **National Geographic** | **10** | Story is the entire business model. Every page has a specific editorial angle, a photographer credit, and a narrative that earns your time. The homepage makes you want to read something. |
| **Patagonia** | **9** | Mission woven into every surface. "It's a long way to the bottom of the world." Place is the protagonist. Every product page contains the story of where the product was made and why. |
| **Rijksmuseum** | **8** | Scholarly depth rendered as narrative. The Night Watch conservation story. Vermeer's studio practice. The institution tells stories about its works, not just about itself. |
| **Google Arts & Culture** | **7** | Educational narrative. Curator's voice. Slightly algorithmic — curated by theme and trend as much as editorial judgment. |
| **Apple** | **6** | Product-centric narrative. "The most powerful chip we've ever built." Precise, pointed, short. The story is the product specification. |
| **NC Current** | **5** | The "Why Earthrise matters" section — "A photograph that turned exploration back toward home" — is a real headline with real editorial intent. The two-column narrative copy is substantive and specific. This is a genuine improvement. But the story has no arc: it builds, and then collapses into a "Featured collection" section that resolves to three bordered spans labelled "Story", "Museum Print", "Digital Edition." The narrative momentum dies on contact with those elements. The product cards and place cards below do not extend the story. |

---

### Dimension 5: Commerce

*Does the page create desire? Is the path to purchase clear, confident, and worth taking?*

| Site | Score | Basis |
|---|---|---|
| **Apple** | **10** | Price visible immediately. Add to bag always one click away. Cart persistent. Every element serves a specific conversion. Nothing is accidental. |
| **Patagonia** | **9** | Product with mission. The "why" is integrated with the "what." You are not buying a jacket — you are participating in something. The purchase path is confident and clean. |
| **Rijksmuseum** | **7** | The shop works. PD prints in a museum-appropriate price range. Good product photography. Clear purchase path. The Rijksstudio model creates desire through curation. |
| **National Geographic** | **4** | Subscription-driven. The magazine is the product. The shop exists but is not the primary vehicle. |
| **Google Arts & Culture** | **1** | No commerce. |
| **NC Current** | **3** | "View editions" CTA is present on the homepage. The product page has "Request purchase" — a `mailto:` link. No price appears anywhere. The edition cards on the product page are text-only with bullet lists describing the product rather than showing it. Certificate of Authenticity is a pill badge alongside "Public domain" and "17 U.S.C. § 105" — it communicates less than nothing. There is no sense of what MASTERWORK means, no scarcity signal, no designed CTA hierarchy. The visitor who wants to purchase Earthrise must navigate three pages and then send an email. |

---

### Dimension 6: Discovery

*Can you find your way deeper? Does the page invite exploration beyond the first scroll?*

| Site | Score | Basis |
|---|---|---|
| **Google Arts & Culture** | **10** | Discovery is the product. Color-based, time-based, theme-based, artist-based, institution-based entry points. The homepage is an invitation to lose an hour. |
| **National Geographic** | **9** | Stories by topic, place, photographer, and region. You arrive for one thing and leave having read four others. |
| **Rijksmuseum** | **9** | Rijksstudio, collections, colour, period, technique, institution. Multiple independent discovery modes. The Night Watch is the anchor but not the ceiling. |
| **Patagonia** | **7** | Product categories are navigable. Place pages feed discovery. Sport-based filtering creates a secondary entry mode. |
| **Apple** | **6** | Discovery is limited. You see featured products and product categories. If you know what you want, Apple is flawless. Browsing is thin. |
| **NC Current** | **3** | The navigation lists Places / Stories / Products / About. "Collections" and "Discover" — the two discovery-oriented L1 items mandated by the Wireframe Constitution — are absent. The "Next journeys" section shows four place cards that link to pages which do not yet exist. The illustrator entry points (Haeckel, Gould, Audubon) do not exist. Era-based discovery (1750–1900 Golden Age) does not exist. Collection-level discovery does not exist. The site has one active story and two products — discovery, by structural necessity, is limited — but the navigation and discovery architecture should be in place before the content is, not after. |

---

## III. Summary Score Table

| Dimension | NC | Apple | NatGeo | G.A&C | Patagonia | Rijks |
|---|---|---|---|---|---|---|
| Wonder | **4** | 9 | 10 | 8 | 8 | 9 |
| Trust | **5** | 8 | 9 | 8 | 10 | 10 |
| Beauty | **4** | 10 | 9 | 7 | 8 | 8 |
| Storytelling | **5** | 6 | 10 | 7 | 9 | 8 |
| Commerce | **3** | 10 | 4 | 1 | 9 | 7 |
| Discovery | **3** | 6 | 9 | 10 | 7 | 9 |
| **Total /60** | **24** | **49** | **51** | **41** | **51** | **51** |
| **Average /10** | **4.0** | **8.2** | **8.5** | **6.8** | **8.5** | **8.5** |

**Gap to close:** NC scores 4.0 against a reference model average of 8.1. The gap is not in governance, architecture, or content rights — those are resolved. The gap is entirely in visual design, typographic language, and interaction design.

---

## IV. Top 10 Remaining Weaknesses

Ranked by impact on closing the gap between 4.0 and 8.0+.

---

### 1. The hero image is framed, not immersive

**Score impact:** Wonder −3 points

The Earthrise photograph appears inside a rounded `<figure>` element in the right column of a split-screen grid. It has a dark border, a visible figcaption, and a box shadow. It occupies roughly 40% of the horizontal viewport and sits next to a block of text copy.

Every reference model that works with a single anchor image — NatGeo, Patagonia, Apple, Rijksmuseum — places that image at full viewport scale with the text either overlaid or below. Framing the image reduces it. Full bleed elevates it.

The current layout communicates: "Here is an image we would like to show you." The required layout communicates: "This is the thing."

**What needs to change:** The hero section on the homepage (and story page, and collection page) must use `width: 100vw; height: 100svh` with the image as the background and copy overlaid at bottom-left. The border-radius, box-shadow, and figcaption belong on the product page where a framed presentation is appropriate — not on pages where the image is supposed to stop the visitor.

---

### 2. No serif typeface exists anywhere

**Score impact:** Beauty −3 points, Storytelling −2 points

Every word on every page — editorial headlines, story body, product titles, navigation, governance text — renders in Inter. Inter is an excellent sans-serif. It is not the right typeface for editorial content about 200-year-old natural history illustration.

The typographic register communicates the nature of an institution. Inter communicates: technology product, SaaS platform, startup. A serif companion (Cormorant Garamond, Tiempos, Playfair Display) applied to editorial headings, story body, and illustration titles would immediately reposition NC in the reader's perception: institutional, historical, editorial.

This is one CSS import and two variable declarations. The return-on-effort ratio is exceptional.

**What needs to change:** Add Cormorant Garamond (Google Fonts, free) as `--font-serif`. Apply to: all `h1` on story and collection pages, story body text (`.story-body`), pull quotes, illustration titles, and place names on place pages.

---

### 3. "Request purchase" remains on the primary commerce CTA

**Score impact:** Commerce −2 points, Trust −1 point

The `ManualPurchaseCTA` component has `eyebrow: "Purchase inquiry"` but `h2: "Request purchase"` and `button: "Request purchase"`. The h2 and button are the elements visitors read and click. "Request" implies the visitor is seeking permission from NC to spend money. It implies uncertainty about whether the purchase will be accepted.

The visitor should feel they are acquiring something exceptional, not requesting something uncertain.

**What needs to change:** Replace "Request purchase" with "Enquire about this edition" (h2) and "Send enquiry" (button). "Enquire" is the correct register for high-value art commerce — it is used by galleries, auction houses, and museum shops for works above a certain threshold. It does not expose the operational mechanism while accurately describing what happens.

---

### 4. The collection teaser communicates nothing

**Score impact:** Storytelling −2 points, Discovery −1 point, Commerce −1 point

On both the homepage and the story page, the "Earthrise: The Overview Collection" feature section contains a `div.collection-teaser` that renders bordered spans: "Story" / "Museum Print" / "Digital Edition" (homepage) and "NASA source" / "Story" / "Print" / "Digital" (story page).

This is a labelled list of what exists, not an experience of what those things are. It stops the narrative dead at the moment it should accelerate.

**What needs to change:** The collection teaser needs to be a visual module. At minimum: a thumbnail of the Earthrise photograph, the collection title, one sentence of editorial copy, and a CTA. The spans should become visually differentiated cards — image, label, brief description — not plain borders around single words.

---

### 5. No quality tier system is visible to visitors

**Score impact:** Trust −2 points, Desire −2 points

MASTERWORK is the highest quality designation in NC's governance system. It is defined in the Asset Intelligence Constitution, encoded in the database, required for museum print activation, and mandated for curator approval. The Earthrise photograph (NC-NASA-002) carries it.

Visitors never see it. The product page has three pill badges: "Public domain", "17 U.S.C. § 105", "Certificate of Authenticity". None of these communicate quality tier. None communicate that this photograph has received the highest designation in NC's curation system.

MASTERWORK, displayed as a gold-badged element at the top of the commerce panel, communicates the same thing as a museum's "Highlight" designation or Apple's "Pro" label: this is the best thing here, and here is how you know.

**What needs to change:** Add `<span class="badge badge--masterwork">◆ Masterwork</span>` to the product page commerce panel, the edition cards, and every product card that displays a MASTERWORK-tier asset. Define `.badge--masterwork` in the CSS with the `--gold` color token already present.

---

### 6. Edition and place cards contain no illustrations

**Score impact:** Wonder −1 point, Commerce −2 points, Discovery −1 point

The product edition cards (Museum Print, Digital Edition) are text-only. A visitor deciding whether to purchase a museum print of Earthrise cannot see the print from those cards — they must scroll up to the product image. The cards explain the product in bullet points without showing what they are selling.

The place cards on the homepage and places index show only a title and identical generic copy. Yellowstone, Grand Canyon, Great Barrier Reef, and Galápagos each have significant illustrated material in NC's governed catalog — Hayden Survey plates, Powell expedition photography, Haeckel chromolithographs, Gould finch illustrations. None of it appears in the cards.

**What needs to change:** Edition cards need a thumbnail of the illustration above the title. Place cards need a representative illustration from NC's governed assets for that place — even a seeded static image at Phase 0. No card for a visual commerce platform should be text-only.

---

### 7. Progressive provenance does not exist

**Score impact:** Trust −2 points

The product page has a "Source record" section containing:
```
{EARTHRISE_RIGHTS}
Source: NASA. Asset ID: AS08-14-2383. Human reviewed: yes.
```

This is flat data. It is correct. It is not designed.

NC's governance system is the deepest thing that differentiates it from a generic print shop. A visitor who understands the eight-gate verification process — rights class determination, human approval, source tracing, asset ID confirmation — wants the product more, not less. That story is not being told.

NC-WEB-004 §V.3 defines a three-level provenance panel: Level 0 (credit line, always visible), Level 2 (expandable panel with narrative), Level 3 (full governance record). The current product page has a version of Level 0 (figcaption) and a version of Level 3 (raw data). Level 2 — the narrative panel that converts governance into desire — does not exist.

**What needs to change:** Replace the "Source record" section with a Provenance component that has a collapsed state (the existing credit line) and an expanded state (a narrative: who photographed it, when, where, rights basis in plain language, verification date, curator sign-off). The expand trigger is "See full provenance." The collapsed state is visible by default. The expanded state is hidden until clicked.

---

### 8. Footer exposes operational constraint

**Score impact:** Trust −1 point, Beauty −1 point

The footer reads: `"Verified public-domain sources, visible attribution, manual commerce only."`

"Manual commerce only" is an operational limitation described as a brand statement. It communicates to every visitor that NC has not yet built a checkout system. Compare to what Patagonia's footer communicates ("We're in business to save our home planet"), or what the Rijksmuseum footer communicates (institutional authority, open access, partner institution links).

The footer of every page is a low-visibility but high-frequency trust surface. Every visitor who scrolls to the bottom reads it. "Manual commerce only" is not a mission statement.

**What needs to change:** Replace with something in the register of the mission. Options: "Public domain, provenance visible, for keeps." / "The illustrated record of Earth's great places." / "Verified public domain. Human reviewed. Available." The exact copy is secondary — the register must shift from operational disclosure to institutional statement.

---

### 9. Navigation is missing two L1 items

**Score impact:** Discovery −2 points

Current navigation: `Places / Stories / Products / About`

Wireframe Constitution v1 mandates: `Places / Discover / Stories / Collections / Shop`

"Collections" and "Discover" are both absent. "Collections" is absent despite a collection (`/collections/earthrise`) being designed in NC-WEB-004 and ready to build. "Discover" is the entry point for illustrator profiles, era-based browsing, and thematic navigation — the discovery modes that separate NC from a flat product catalog.

The navigation is the frame through which visitors understand what NC is. A visitor who sees "Places / Stories / Products / About" understands NC as a publication with a shop attached. A visitor who sees "Places / Discover / Stories / Collections / Shop" understands NC as a discovery platform with a commerce layer.

**What needs to change:** Add "Collections" to the nav immediately (Phase 0: links to `/collections/earthrise`). Add "Discover" at Phase 1 when illustrator and era pages are built. Rename "Products" to "Shop" per the Wireframe Constitution.

---

### 10. Place cards on the homepage and places index are identically described

**Score impact:** Storytelling −1 point, Discovery −1 point, Wonder −1 point

The "Next journeys" section on the homepage and all cards on the places index render identical copy: "Source-led stories, collections, and editions connected to this place." / "Stories, collections, and editions connected to this place."

This copy appears on Yellowstone, Grand Canyon, Great Barrier Reef, and Galápagos. It says the same thing about all four. It says nothing specific about any of them.

Each of these places has a specific illustrated history that makes it distinct and desirable:

- **Yellowstone** — Hayden Survey, 1871. The expedition that created the world's first national park.
- **Grand Canyon** — Powell Survey, 1869. A one-armed Civil War veteran descending 1,450km of unmapped canyon.
- **Great Barrier Reef** — Haeckel, 1899. Chromolithographs of coral that have since largely bleached.
- **Galápagos** — Darwin and Gould, 1845. The finches that changed the understanding of life.

One specific sentence per place transforms a generic grid into a discovery experience.

**What needs to change:** Write a unique one-sentence editorial description for each place in `governed-content.ts` as a field on `placeTeasers`. Render it on the place card. This is a data change and a copy decision — no new infrastructure required.

---

## V. Verdict

**NC current: 4.0 / 10. Reference model average: 8.5 / 10.**

The gap is entirely recoverable. None of these ten weaknesses require new infrastructure, new governance documents, or new content rights. All ten are solvable within the current stack (`PostgreSQL / MinIO / FastAPI / Next.js`) and current governance framework.

The five highest-impact, lowest-effort changes:
1. Convert the hero to full-bleed on homepage and story page
2. Add Cormorant Garamond for editorial headlines and story body
3. Replace "Request purchase" with "Enquire" on `ManualPurchaseCTA`
4. Add MASTERWORK badge to product page and edition cards
5. Write specific one-sentence editorial copy for each place card

These five changes, implemented together, would move NC from 4.0 to approximately 6.5 — closing half the gap in a single sprint before Gate E.

The remaining five weaknesses (collection teaser, provenance panel, card illustrations, footer, navigation) move NC from 6.5 to 8.0+ and constitute the Phase 1 experience build.

---

*NC-WEB-004 Final Audit v1.0 · 2026-06-12 · Principal Architect*
