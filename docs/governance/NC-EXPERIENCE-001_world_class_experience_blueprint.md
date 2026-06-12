# NC-EXPERIENCE-001: World-Class Experience Blueprint

| Field | Value |
|---|---|
| Document | NC-EXPERIENCE-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | NC-PILOT-001 · NC-WEB-001 · NC-PRODUCT-001 · NC-AI-001–NC-AI-006 · Wireframe Constitution v1 · Strategic Direction v1 |
| Governs | User experience design, interaction patterns, information architecture, content strategy, and emotional design for all public-facing NC surfaces |
| Reference models | Apple · National Geographic · Patagonia · Google Arts & Culture · Smithsonian · Rijksmuseum |

---

## I. Purpose

This document answers nine foundational questions about the Nature & Culture user experience, scores the current site against world-class reference models, and ranks the top 50 improvements by impact.

NC-EXPERIENCE-001 does not override governance constraints — it operates within them. Every improvement must satisfy IFC-1 (rights verification), FM-4 (no AI rights determination), AI-ATT-1 (attribution retrieved, not generated), and the four NC-WEB-001 invariants. The goal is to make those constraints invisible to the visitor while making the experience exceptional.

The strategic thesis: **provenance is not a compliance burden — it is the product.** The visitor who understands that the print on their wall is a verified, human-authenticated, source-traceable public-domain work from 1878 wants it more, not less.

---

## II. Reference Model Analysis

### Apple

**What NC borrows:** Cinematic full-bleed visual language. Typography as design element. Silence — knowing what NOT to show. The product page as a desire machine. Every pixel justified. The absence of governance language from the visitor surface (legal stays legal; design stays design).

**What NC must not copy:** Apple's emotional register is aspiration through technology. NC's register is reverence through history. Different frequencies. A Haeckel plate is not an iPhone.

**Key lesson:** Trust is built through design quality, not disclaimers. The visitor who sees a flawless visual experience trusts the institution behind it before reading a single word of provenance text.

### National Geographic

**What NC borrows:** Story-first architecture. The photograph as authority, not decoration. Editorial voice that commands — not suggests — attention. Deep features, not blurbs. The yellow border as immediate trust signal. Place as protagonist.

**What NC must not copy:** NatGeo is a media company first. NC is a commerce platform with editorial depth. NatGeo's editorial exists to sustain advertising. NC's editorial exists to create desire for the illustration.

**Key lesson:** The story of who made an illustration, where they were, and what they saw is worth 1,200 words on the page. That story converts.

### Patagonia

**What NC borrows:** Mission woven into every product surface. Place as protagonist — Patagonia's places ARE Patagonia. Conservation narrative as a feature of the product, not separate from it. Radical transparency about materials and provenance that functions as a trust signal, not a burden. "Don't buy this jacket" honesty — they earned more sales with it.

**What NC must not copy:** Patagonia's mission is environmental activism. NC's mission is heritage access and commerce. The register is different. NC does not advocate; it illuminates.

**Key lesson:** The visitor who knows why provenance matters wants verified provenance. Make the governance a story, not a gate.

### Google Arts & Culture

**What NC borrows:** Discovery as experience — not as search results. Zoom as reverence (the Art Camera). Collection navigation by time, place, color, theme — multiple entry modes. Institution authority visible at every touchpoint. The idea that resolution is itself a form of access.

**What NC must not copy:** Google Arts & Culture has no commerce. It accumulates authority by accumulating everything. NC wins by curating, not accumulating. The quality tier system (MASTERWORK/FLAGSHIP/STANDARD/REFERENCE) is the anti-Google Arts & Culture move — scarcity and curation, not completeness.

**Key lesson:** Discovery is a destination, not a feature. The visitor who loses an hour exploring wants to buy something before they leave.

### Smithsonian

**What NC borrows:** Institutional authority earned through depth. Educational framing that does not condescend. Provenance and collection metadata treated as content — not footnotes. Free access as a brand position. The idea that the institution behind the asset adds value to the asset itself.

**What NC must not copy:** Smithsonian's commerce is an afterthought. Their shop exists because they have gift shops — not because commerce is constitutional. NC's commerce is constitutional.

**Key lesson:** The source institution's authority transfers to the product. Showing the NASA logo, the LOC collection number, the Smithsonian accession — these are value signals, not legal requirements.

### Rijksmuseum

**What NC borrows:** Public domain as brand identity, not a workaround. High-resolution access as product. Provenance as the lead, not the footnote. The Rijksstudio model — user can compose, collect, share. Every work with full scholarly citation visible on the product page. The idea that the masterwork anchors the entire discovery experience. A shop that serious collectors actually use.

**What NC must not copy:** Rijksmuseum's collection is fixed. NC's is growing. Rijksmuseum has institutional legitimacy from 200 years. NC earns it through governance depth. Different starting points, same destination.

**Key lesson:** The Rijksmuseum proved that a PD commerce platform can earn $20M+ in annual product revenue. The model works. The question is execution.

---

## III. The Nine Experience Questions

### Question 1: What should a visitor feel in the first 30 seconds?

**The wrong answer:** "I have arrived at a website that has completed its attribution verification procedures."

**The right answer:** "I have arrived somewhere I didn't know existed — and I want to stay."

The first 30 seconds must deliver three sensations in sequence:

1. **Reverence** — the image stops them. Earthrise at full bleed, color-accurate, without decorative framing or overlaid text. The photograph taken on December 24, 1968, from 240,000 miles away. The visitor should feel the weight of that.

2. **Authority** — two or three words of editorial copy establish that NC is the curatorial voice, not a marketplace. Not "Shop prints here." Something like: *"The illustrated record of Earth's great places. Verified and available."*

3. **Desire** — before the fold break, one product surface. Not an add-to-cart button. A sense that this is acquirable — that the thing they are seeing exists in the world at a quality they can own.

The entire emotional architecture of the site should flow from this 30-second experience. If a visitor needs to read a sentence of governance copy to understand what NC does, the design has failed.

**Benchmark:** Apple's iPhone launch pages deliver reverence (full-bleed product), authority (one headline), and desire (one CTA) in 15 seconds. NC's subject matter is more complex but the principle is identical.

---

### Question 2: What should the homepage become?

**Current state:** Governance language as headline. Placeholder `<div>` where the hero image should be. A grid of product cards without images. A list of places with status labels. Attribution block inline in the main content flow.

**Target state:** An editorial-quality experience with four distinct sections:

**Section 1 — The Anchor (100vh, full bleed)**
- Earthrise photograph, edge to edge, no overlay text blocking the image
- One headline positioned to preserve the image: *"The world's great places, illustrated."* (or equivalent — see §V for copy principles)
- One CTA: *Explore Earthrise*
- Attribution appears as a single refined credit line at the image's lower edge: *NASA · Apollo 8 · December 24, 1968 · Public Domain*

**Section 2 — The Editorial Lead (500px)**
- Two paragraphs of editorial narrative. Not governance copy. Not feature lists. The story of why NC exists: the 250 years of expedition illustration that documented the natural world before photography, now verified and available for the first time in one place.
- This section earns the right to continue scrolling.

**Section 3 — Featured Place (full-width, rotates by phase)**
- Phase 0: Earthrise
- Phase 1: Yellowstone or Grand Canyon
- Phase 2+: rotating featured place
- Hero image + place name + best available illustration from that place + one product surface
- This is the commercial engine of the homepage — the featured place drives the primary conversion funnel

**Section 4 — Discovery Entry Points**
- Three columns: By Place / By Illustrator / By Era
- Not a product grid. An invitation to explore.
- "By Place" links to the pilot places index
- "By Illustrator" links to the six priority illustrators (Audubon, Haeckel, Gould, Merian, Redouté, Nodder)
- "By Era" links to the Golden Age 1750–1900 thematic collection

**What must not appear on the homepage:**
- Phase numbers ("Phase 0 public launch") — these are internal governance labels
- Status labels ("coming soon") — stub place cards should simply not render, not render with status
- Governance copy ("after rights, source, and attribution checks") — this belongs in the About/How We Work page
- Manual purchase language ("through manual fulfillment") — invisible to the visitor
- Inline attribution blocks — attribution lives at the image edge, not in the content flow

---

### Question 3: How should place pages work?

A place page answers one question: *What does 250 years of scientific illustration look like for this place?*

**Structure (in order of scroll):**

**1. Place Hero (100vh)**
- Best available satellite or aerial image of the place (NASA/NOAA sourced, governed)
- Place name as single typographic element
- Temporal badge: *UNESCO World Heritage Site · Est. [year]* or equivalent authority signal
- Depth prompt: *"Illustrated from [earliest illustration year] to [most recent]"*

**2. The Place Story (800–1,200 words)**
- AI-generated, graph-grounded, human-reviewed editorial narrative
- Governed by NC-AI-001: source truth from PostgreSQL, AI provides interpretation
- Covers: the place's natural and cultural history, why it was a subject of expedition illustration, the key illustrators who documented it, what changed between the first illustration and today
- No prohibited phrases validator triggers: no endorsement language, no GBIF species-count framing

**3. Featured Illustrations (horizontal scroll or masonry grid)**
- The 5–8 best-scored Illustration Opportunities connected to this place
- Each shows: illustration at full quality, illustrator name, year, quality tier badge (MASTERWORK/FLAGSHIP/STANDARD), rights badge (PD/CC0)
- Click → Media page for that illustration
- Commerce signal: "Available as [product type]" label on eligible illustrations

**4. Products from This Place**
- Contextual commerce module — not a redirect to the shop
- The Earthrise print belongs here, the Hayden Survey map belongs here
- Product cards with illustration, title, price, "Reserve" CTA for museum prints
- Attribution on every product card (one line: source · year · rights class)

**5. Place Intelligence Footer**
- GeoNames ID + CC BY 4.0 attribution (required: GN-6)
- UNESCO/World Heritage designation with link
- OSM attribution if map tiles are displayed (required: OS-6)
- Tourism CTA: *Plan your visit → [National Park Service / UNESCO / equivalent]*
- Conservation signal: brief sentence on protection status and governing body
- Educational CTA: *Use in your classroom → [educational product]*

**What must not appear on place pages:**
- Species occurrence counts (GBIF framing — wrong problem)
- "Coming soon" labels — unactivated content sections simply do not render
- Governance hold language visible to visitors
- Raw GeoNames IDs or database record numbers in the visitor layer

---

### Question 4: How should products work?

**The governing insight:** NC's product is not a print. NC's product is provenance-verified access to a specific moment in the illustrated record of a place.

The Rijksmuseum proved this model. A visitor who understands that they are acquiring a museum-quality edition of an 1878 Haeckel hexacoralla plate — verified by NC's eight-gate governance process, with the full chain from BHL through institution through rights class through curator approval documented — wants it more, not less, than a generic art print.

**Product Page Structure:**

**1. Product Hero (split screen)**
- Left: illustration at full scale, zoomable (Google Arts & Culture zoom model)
- Right: product title, quality tier badge, rights badge, price, CTA
- The illustration should dominate — 60/40 split or full screen with overlay

**2. The Illustration Story (400–600 words)**
- Who made this: illustrator name, era, expedition or publication context
- Where: the place it documents, with link to the place page
- Why it matters: what was known about this subject when it was made vs. today
- AI-generated, graph-grounded, human-reviewed

**3. Provenance Panel (progressive disclosure)**

*At a glance (always visible):*
```
NASA · Apollo 8 · December 24, 1968 · 17 U.S.C. § 105 · Human Verified
```

*Expanded (click to reveal):*
- Full attribution string per NC-WEB-001 §III
- Asset ID (e.g., AS08-14-2383)
- Rights class and legal basis
- Institution (with logo)
- Human verification date and gate number
- Source URL

*Full record (link to governance view):*
- Complete pipeline record for institutional/research purchasers
- This view is the "Rijksstudio full scholarly citation" equivalent

**4. Product Variants**
- Museum print / Framed print / Digital download — as applicable
- Quality specifications visible (dimensions, DPI, paper weight) — these are features, not fine print
- Certificate of Authenticity preview (a physical product for museum prints)
- "How this looks on a wall" — room visualization or scale reference

**5. Related Place / Related Illustrations**
- 3 related illustrations from the same place
- "Complete the collection" — if this place has multiple eligible products

**What must not appear on product pages:**
- "Manual purchase" language in the visitor layer
- Phase labels
- Internal governance codes as product titles ("NC-PROD-001" is an internal reference, not a consumer-facing name)
- NASA/NOAA endorsement language (zero tolerance)

---

### Question 5: How should AI-generated content work?

**The governing rule (FM-4, AI-ATT-1, permanent):** AI may not determine rights. AI may not generate attribution strings. AI content is interpretation, not source truth.

**The visitor experience rule:** AI content should be invisible as AI. It should be indistinguishable from excellent human editorial.

NC's AI content occupies five surfaces:
- Place stories (800–1,200 words per place)
- Product descriptions (200–400 words per product)
- Educational module copy (PDF guides, lesson packs)
- Collection narratives (300–500 words per collection)
- Multilingual equivalents of all the above

**How it works for the visitor:**
The visitor never sees "AI-generated" or "Powered by Claude" on editorial copy. The editorial voice is NC's voice — authoritative, specific, historically grounded. The AI is the writer; the governance system is the editor; the human curator is the approver.

The place story for Yellowstone reads like a National Geographic feature written by someone who has read every expedition report from 1869 to 1900. That is what NC-AI-001 + the BHL corpus + a skilled generation prompt can produce. The visitor reads it and trusts it because it is accurate and specific — not because they know the model behind it.

**Prohibited phrases validator (C-5, pre-production gate):**
Before any AI content reaches a public surface, the validator blocks:
- Any variation of "NASA endorses" / "Smithsonian recommends" / federal endorsement language
- GBIF occurrence count framing ("X species recorded at this location")
- Rights determination language ("this image is public domain because...")
- Attribution generation ("Photo credit: [generated string]")
- Content that contradicts the graph-grounded facts

**The one exception — AI content that should be labeled:**
If NC ever produces AI-generated visual content (it does not, per current governance), it must be labeled. For text and editorial copy, no AI label is required and no AI label should appear.

---

### Question 6: How should collections work?

A collection is the editorial engine of NC. It is the answer to the visitor who doesn't know what they're looking for but knows they want something significant.

**What a collection is:**
A curated grouping of Illustration Opportunities around a unifying theme — place, illustrator, era, subject, or expedition — with editorial narrative, a complete visual gallery, and a unified commerce surface.

**Initial collection set (by launch phase):**

*Phase 0 (live at Gate E):*
- **Earthrise** — NC's first collection. One illustration. One place. One moment. The proof of concept.

*Phase 1 (SA gates complete):*
- **The Golden Age of Natural History Illustration** — Audubon, Gould, Haeckel, Merian, Nodder together. 1750–1900. The defining thematic collection.
- **North American Surveys** — Hayden, Powell, the great federal surveys. Yellowstone, Grand Canyon, the canyon country.
- **Expedition Pacific** — GBR + Galápagos + Papahānaumokuākea. Cook voyages through Apollo.

*Phase 2+:*
- **Botanical Masters** — Redouté, Ehret, the plate tradition
- **Age of Exploration Maps** — Historic Maps Tier 1 (NARA, BnF pending governance)
- **The Living Ocean** — Haeckel + GBR + marine biology illustration history

**Collection page structure:**

**1. Collection Hero**
- Single dominant illustration (the anchor work — MASTERWORK preferred)
- Collection title + one-sentence thesis

**2. Collection Editorial (500–800 words)**
- The story of why these works belong together
- AI-generated, graph-grounded, human-reviewed
- Ends with a question that the collection answers: "What did the world know about the Great Barrier Reef before 1900?"

**3. Full Collection Gallery**
- All eligible illustrations, sorted by quality tier then date
- Quality tier badge + illustrator + year + rights badge on every card
- Click → Media page

**4. Shop This Collection**
- All eligible products surfaced in-context
- Framed as "complete the collection" — encourages multi-product purchase
- No duplicate product listings — one canonical product card per product

**Rijksstudio equivalent (Phase 2):**
- Visitor-curated collections ("My NC" or equivalent)
- Save and share any illustration, build personal collections
- Privacy-first (NC-AI-001: user behavioral data permanently excluded from FM calls)

---

### Question 7: How should trust be communicated?

**The wrong model:** A paragraph of governance text explaining the verification process. The visitor who needs to read about the verification process before trusting the image is already gone.

**The right model:** A visual trust language system — badges, marks, and design elements that communicate authority without requiring text.

**The NC Trust Language System:**

**Tier 1 — Instant Signal (always visible, no hover required):**
- **Rights badge:** Color-coded pill. `PD` (navy) for §105/pre-1928. `CC0` (green) for explicit CC0 grants. Never absent from any asset surface.
- **Quality tier badge:** `MASTERWORK` (gold), `FLAGSHIP` (silver), `STANDARD` (slate), `REFERENCE` (muted). Displayed as a mark, not a technical threshold.
- **Human Verified checkmark:** A distinct iconographic mark — not a checkmark emoji, a designed symbol — that communicates human approval at Gate 7/8. This is the NC equivalent of a museum's conservation note.

**Tier 2 — On Hover / At a Glance:**
- **Source institution name + logo:** "NASA" with the NASA insignia (for §105 works). "Rijksmuseum" with their mark. "Smithsonian" when activated. The institutional logo transfers authority.
- **Year:** The date of the work, prominently placed. 1968 means something. 1878 means something different. Both mean something.

**Tier 3 — Click to Expand (progressive disclosure):**
- Full attribution string, asset ID, rights class, legal basis
- Human verification date, gate completion record
- Source URL to originating institution

**What trust must not look like:**
- A paragraph of text saying "we take provenance seriously"
- An FAQ about the verification process
- Legal copy inline with product descriptions
- NARA/NASA/NOAA badge language that reads as endorsement (FS-001)

**The Patagonia analogy:** Patagonia's "Ironclad Guarantee" is one sentence on their site. It communicates unlimited trust without explaining the returns process. NC's trust language should work the same way — the mark communicates; the detail is available but not required.

---

### Question 8: How should provenance be visible without becoming bureaucratic?

**The governing principle:** Provenance is a story, not a record. The same facts that constitute a compliance obligation can constitute a compelling narrative — the difference is framing.

**The bureaucratic version (what to avoid):**
```
Rights status: verified_pd
Human verified: TRUE
Rights class: 3 (17 U.S.C. § 105)
Asset ID: AS08-14-2383
Institution: NASA
Verification date: 2026-06-11
Gate: 7/8 complete
```

**The narrative version (what to build):**
> *This photograph was taken by William Anders aboard Apollo 8 on December 24, 1968 — the first time any human being had photographed Earth from deep space. As a work of the U.S. federal government, it entered the public domain at the moment of creation under 17 U.S.C. § 105. Nature & Culture has traced this specific image (AS08-14-2383) from NASA's archive through our eight-gate verification process. A human curator confirmed both the rights status and the source record before this print was offered for sale.*

Both versions contain the same facts. The second version makes the print more desirable.

**Progressive disclosure architecture:**

| Level | Trigger | Content | Location |
|---|---|---|---|
| 0 — Instant | Always visible | Rights badge + source name + year | Image corner or product header |
| 1 — Hover | Mouse over rights badge | One-line attribution string | Tooltip |
| 2 — Expand | Click provenance panel | Full narrative attribution, asset ID, institution, gate status | Inline panel on product/media page |
| 3 — Deep record | Click "Full record" | Database-level provenance view | Separate page, linkable, shareable |

Level 3 serves institutions, researchers, and serious collectors. Level 0 serves everyone. The design default is Level 0; Levels 1–3 exist for those who want them.

**The "certificate-as-product" principle:**
For museum prints and archival editions (NC-PROD-001, NC-PROD-006, NC-PRODUCT-020), the Certificate of Authenticity is itself a designed object — not a PDF attachment. It carries the complete Level 3 provenance in a format worthy of the print. This is the Rijksmuseum model applied to NC.

---

### Question 9: How should education, tourism, conservation, and commerce connect?

**The wrong model:** Four separate sections, each with its own navigation. "Education" page. "Tourism" page. "Conservation" page. "Shop" page. This is the institutional website model. It is the Smithsonian model. It works for an institution. It does not work for a commerce platform.

**The right model:** One experience — the place page — that answers all four registers simultaneously, tuned to the visitor's evident intent.

**The Place as Portal architecture:**

Every place page is simultaneously:
- A **tourist destination** (*I am going here / I want to go here*)
- A **conservation story** (*This place is protected because it is irreplaceable*)
- A **school subject** (*This place appears in biology, geography, history, and art*)
- A **collector's object** (*The illustrations that documented this place are available*)

These are not separate sections. They are the same story told through different lenses.

**How they connect:**

```
Place Story (editorial, 1,200 words)
    ↓
"What makes this place irreplaceable"
    → Conservation signal (UNESCO status, area protected, governing body)
    → Tourism CTA (Plan your visit → NPS / UNESCO / equivalent)
    ↓
"The illustrations that documented it"
    → Featured illustrations gallery (commerce signal on every card)
    → "In the classroom" (educational license CTA for illustrated plates)
    ↓
"Own a piece of its illustrated history"
    → Contextual product surface
    → "Complete the collection" for multi-product purchases
```

**The connective tissue:**
The Haeckel hexacoralla plate (BHL-HAECKEL-HC, MASTERWORK) is simultaneously:
- A product in NC-PROD-006 (museum print, £280)
- An educational resource in the marine biology curriculum
- The most beautiful documentation of Great Barrier Reef life before industrial bleaching
- The reason a tourist visiting GBR wants something on their wall

It is one illustration. It serves all four registers. The visitor who arrives as a tourist leaves as a collector. The visitor who arrives as a teacher leaves as an institutional license prospect. The commerce is not separate from the mission — it is the mission.

**B2B signal architecture (visible, non-committal):**
Place pages should carry a quiet institutional licensing inquiry CTA — not a prominent sales pitch, but a visible path:
*"Using NC content for classroom or institutional purposes? → Institutional licensing enquiry"*

This is the tourism operator and educational institution signal. It does not require a B2B commerce infrastructure in Phase 0. It requires a contact form and a tracked conversion event.

---

## IV. Current Site Score vs. Reference Models

Scores on a 10-point scale across eight experience dimensions.

| Dimension | Current NC | Apple | NatGeo | Patagonia | Google A&C | Smithsonian | Rijksmuseum | NC Target |
|---|---|---|---|---|---|---|---|---|
| **Visual Impact** | 2 | 10 | 9 | 8 | 8 | 6 | 9 | 9 |
| **Emotional Resonance** | 2 | 9 | 10 | 10 | 7 | 7 | 8 | 9 |
| **Trust Communication** | 5 | 8 | 9 | 10 | 7 | 10 | 10 | 10 |
| **Discovery Experience** | 3 | 8 | 8 | 7 | 10 | 8 | 9 | 9 |
| **Commerce Experience** | 3 | 10 | 5 | 8 | 2 | 4 | 8 | 9 |
| **Place Storytelling** | 2 | 5 | 10 | 9 | 7 | 8 | 6 | 10 |
| **Provenance Depth** | 5 | 3 | 6 | 7 | 8 | 9 | 10 | 10 |
| **Navigation Clarity** | 4 | 9 | 8 | 8 | 9 | 7 | 8 | 9 |
| **Mobile Quality** | ? | 10 | 9 | 9 | 8 | 7 | 8 | 9 |
| **AI Content Quality** | 3 | N/A | N/A | N/A | N/A | N/A | N/A | 9 |
| **TOTAL (avg)** | **3.2** | **8.0** | **8.2** | **8.5** | **7.3** | **7.3** | **8.6** | **9.3** |

**Assessment:** The current site is a functional governance skeleton. It correctly implements attribution and rights display. It does not yet deliver an experience. The gap between 3.2 and 9.3 is entirely a design and content execution gap — not a governance or architecture gap. Every point of improvement is buildable within the existing stack.

---

## V. Top 50 Improvements Ranked by Impact

Impact scores reflect combined weight of: revenue impact, trust impact, discovery impact, and experience quality improvement. Scale: Critical / Very High / High / Medium.

### Tier 1 — Critical (implement before or alongside Gate E)

| # | Improvement | Impact | Phase | Governance constraint |
|---|---|---|---|---|
| 1 | Replace homepage hero `<div>` with Earthrise photograph at full bleed | Critical | Phase 0 | IFC-1 already satisfied (NC-NASA-002, human_verified=TRUE). Image must be displayed, not a placeholder. |
| 2 | Rewrite homepage headline from governance language to editorial voice | Critical | Phase 0 | No constraint. Current copy ("after rights, source, and attribution checks are visible") belongs on the About page, not the hero. |
| 3 | Remove "Phase 0 public launch" eyebrow text from homepage hero | Critical | Phase 0 | Internal governance label. Not visitor-facing copy. |
| 4 | Replace Earthrise product page text-only layout with full illustration display | Critical | Phase 0 | NC-PROD-001, NC-PROD-008 authorized. Image must be primary. |
| 5 | Implement proper commerce flow — replace "Manual Purchase CTA" with contact-driven inquiry that doesn't expose the word "manual" to the visitor | Critical | Phase 0 | Manual fulfillment is an operational fact; "manual" is internal language. |

### Tier 2 — Very High (implement in Phase 1)

| # | Improvement | Impact | Phase | Governance constraint |
|---|---|---|---|---|
| 6 | Build Yellowstone place page with full editorial narrative, hero illustration, product surface | Very High | Phase 1 | SA-GEONAMES-001 + SA-OSM-001 required. NC-AI-006 SCHEMA-001 + ASSET-001 required before AI generation. |
| 7 | Build Grand Canyon place page with full editorial narrative, hero illustration, product surface | Very High | Phase 1 | SA-GEONAMES-001 + SA-OSM-001 required. GeoNames ID: 5296401 (canonical per NC-DATA-002). |
| 8 | Build Great Barrier Reef place page with full editorial narrative, hero illustration, product surface | Very High | Phase 2 | SA-GEONAMES-001 + NOAA Sprint 3 gate check. GeoNames ID: 2164628 (canonical per NC-DATA-004). |
| 9 | Implement typography system: serif (Freight Text / Tiempos / equivalent) for editorial, geometric sans for UI | Very High | Phase 0 | No constraint. Current CSS has no typography system. |
| 10 | Implement illustrated-gallery component: masonry or horizontal scroll with quality tier badge + rights badge on every card | Very High | Phase 1 | Rights badge always visible on every asset appearance (Wireframe Constitution Article 16). |
| 11 | Add "Discover" and "Collections" to L1 navigation (per Wireframe Constitution §II.1) | Very High | Phase 1 | Wireframe Constitution already mandates this. Current nav missing two of five L1 items. |
| 12 | Replace place cards with "status: coming soon" labels with empty/non-rendering cards | Very High | Phase 1 | Internal governance status labels must not be visitor-facing text. |
| 13 | Implement progressive provenance disclosure (3-level: badge → one-line → full record) | Very High | Phase 0 | Provenance must be present. Level of prominence is design decision. |
| 14 | Implement zoom/full-resolution view on all illustration assets | Very High | Phase 1 | Quality tier gates apply — MASTERWORK must support 6000px+ delivery. |
| 15 | Build first editorial collection: "Earthrise" (Phase 0), "Golden Age of Natural History" (Phase 1) | Very High | Phase 0/1 | No governance block for collection creation. |

### Tier 3 — High (Phase 1–2 execution)

| # | Improvement | Impact | Phase | Governance constraint |
|---|---|---|---|---|
| 16 | Build Illustration Opportunity gallery component: illustrator, year, place relevance score, quality tier | High | Phase 1 | Quality tier displayed as badge, raw scores hidden (Wireframe Constitution Article 17). |
| 17 | Upgrade Earthrise story page: full-bleed hero, 800-word editorial narrative, "Related place" and "Related illustrations" modules | High | Phase 0 | AI-generated narrative permitted per NC-AI-001. Prohibited phrases validator (C-5) required before deployment. |
| 18 | Build illustrator profile pages for the 8 priority illustrators (Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf) | High | Phase 1 | Creator Page is architecturally defined (Wireframe Constitution OQ-1) — recommended for v1.1. |
| 19 | Design and implement Certificate of Authenticity as a first-class designed object for museum prints (NC-PROD-001, NC-PROD-006) | High | Phase 0 | NC-PRODUCT-001 already defines CoA as a product feature. |
| 20 | Implement site-wide search with typeahead: place names, illustrator names, quality tier filter | High | Phase 1 | pg_trgm trigram search (PostgreSQL, already in stack). No new database required. |
| 21 | Add source institution badges (NASA insignia, LOC mark, etc.) to all product and media pages | High | Phase 0 | Institutional logos require rights-to-use confirmation per institution. NASA logo: public domain for informational use. |
| 22 | Add quality tier badging system: MASTERWORK (gold), FLAGSHIP (silver), STANDARD (slate), REFERENCE (muted) as visual design elements | High | Phase 0 | Per Wireframe Constitution Article 17: displayed as badge, raw scores hidden. |
| 23 | Add "Human Verified" iconographic mark (distinct designed symbol, not emoji checkmark) | High | Phase 0 | IFC-1 requirement. Must be visible but must not constitute endorsement language (FS-001). |
| 24 | Build About page with "How We Work" editorial section explaining governance as story, not process document | High | Phase 0 | No constraint. Current About page not inspected — likely stub. |
| 25 | Implement responsive mobile layout (currently untested — no mobile-specific CSS observed) | High | Phase 0 | No constraint. Critical for all phases. |
| 26 | Add tourism CTA to place pages: "Plan your visit → [NPS/UNESCO link]" | High | Phase 1 | External links to NPS/UNESCO have no governance constraint. Federal nonendorsement applies only to asset attribution, not to general informational links. |
| 27 | Add conservation signal to place pages: UNESCO/World Heritage status, protection area, governing body | High | Phase 1 | GeoNames fcode provides place type (PRKA = national park, RF = reef). UNESCO data is public. |
| 28 | Add educational CTA to place pages and product pages: "Use in your classroom → [educational product link]" | High | Phase 1 | NC-PROD-009 (Galápagos Education Pack) is an authorized product. |
| 29 | Implement "Complete the Collection" cross-sell on product pages: 3 related illustrations from the same place | High | Phase 1 | No governance constraint. Commerce is contextual per Wireframe Constitution. |
| 30 | Add institutional licensing inquiry CTA (quiet, non-committal) to place pages and collection pages | High | Phase 1 | B2B licensing is a Strategic Direction v1 target (Era 2). CTA can precede the infrastructure. |

### Tier 4 — High–Medium (Phase 2+)

| # | Improvement | Impact | Phase | Governance constraint |
|---|---|---|---|---|
| 31 | Build Collections index page (Phase 1: 2 collections; Phase 2+: growing catalog) | High | Phase 1 | No governance block. Collections architecture is constitutionally defined. |
| 32 | Implement AI-generated place stories for Yellowstone (after NC-AI-006 SCHEMA-001 + ASSET-001 resolved) | High | Phase 1 | NC-AI-006: Migration 45 required before Yellowstone AI writes. |
| 33 | Implement AI-generated place stories for Grand Canyon, GBR (post-SA gates) | High | Phase 1/2 | NC-AI-001 C-7 (first model activation gate) required before production AI use. |
| 34 | Build "Room visualization" for wall art products: illustration shown at scale on a room background | Medium-High | Phase 1 | No constraint. Industry standard for wall art commerce. |
| 35 | Build era-based discovery entry point: "Golden Age 1750–1900" as a browsable timeline | Medium-High | Phase 1 | Golden Age 1750–1900 is a constitutional priority (Wireframe Constitution + Illustration Opportunity Doctrine). |
| 36 | Add BHL-style deep-zoom for MASTERWORK illustrations (Google Arts & Culture zoom model) | Medium-High | Phase 1 | MASTERWORK quality tier requires 6000px+ delivery. Deep-zoom is a natural feature of that resolution. |
| 37 | Implement "Add to my collection" (Rijksstudio equivalent): visitor-curated collections | Medium-High | Phase 2 | NC-AI-001: user behavioral data excluded from FM calls. Privacy architecture required first. |
| 38 | Build PDF discovery guide product pages (NC-PROD-009: Galápagos Education Pack) | Medium-High | Phase 2 | SA-GEONAMES-001 required (Galápagos: Phase 3 in NC-COMMERCE-001). |
| 39 | Implement multilingual content: Spanish, French for top place pages (Galápagos, GBR) | Medium-High | Phase 2 | NC-AI-001 classifies multilingual translation as a permitted task. Qwen 2.5 (local) for CJK; Mistral (local preferred) for European languages. |
| 40 | Add calendar product page (NC-PROD-010: Yellowstone Wildlife Calendar, 12-panel attribution audit required) | Medium | Phase 2 | 12-panel NASA nonendorsement attribution audit required before activation (NC-COMMERCE-002). |

### Tier 5 — Medium (Phase 2–3)

| # | Improvement | Impact | Phase | Governance constraint |
|---|---|---|---|---|
| 41 | Build Institution pages for source institutions: NASA, LOC, Smithsonian (post-DD ratification), Rijksmuseum, BHL | Medium | Phase 2 | Institution page is architecturally defined (Wireframe Constitution). Each institution requires a ratified DD. |
| 42 | Implement color/theme-based discovery (Google Arts & Culture color picker model) | Medium | Phase 2 | pg_trgm handles text search. Color-based search requires a color extraction pipeline — new worker, existing stack. |
| 43 | Add audio narration to place stories (future Phase 3 media type expansion) | Medium | Phase 3 | Phase 3 media activation requires Amendment P3-1. Audio must be authorized before display. |
| 44 | Implement print-on-demand API integration (Prodigi / Fine Art America / equivalent) for automated fulfillment | Medium | Phase 1 | Replaces manual purchase path. Commerce execution constitution governs payment and fulfillment architecture. |
| 45 | Build "Gift" experience for high-value museum prints: packaging, message card, gift receipt | Medium | Phase 1 | No governance constraint. Enhances NC-PROD-001 commerce experience. |
| 46 | Add social sharing with correct attribution pre-populated in share text | Medium | Phase 1 | AI-ATT-1: attribution strings retrieved, never generated. Share text must pull from canonical attribution record. |
| 47 | Implement "Recently verified" feed: new illustrations passing Gate 8 shown as editorial discovery | Medium | Phase 2 | IFC-1 gate is the prerequisite. "Recently verified" communicates the governance process as a feature. |
| 48 | Build press/institutional download page with correct license terms for each rights class | Medium | Phase 1 | Attribution registry (NC-WEB-001 §III) governs what must appear in press materials. |
| 49 | Implement cookie-free analytics (Plausible / Fathom) — no behavioral data to FM calls per NC-AI-001 | Medium | Phase 0 | NC-AI-001: user behavioral data permanently excluded from all FM calls. Privacy-first analytics is a constitutional requirement. |
| 50 | Add "What's coming" editorial preview: upcoming place activations shown as editorial narrative, not governance timeline | Medium | Phase 1 | No constraint. Replaces "Phase X status" labels with editorial anticipation. |

---

## VI. Five Governing Experience Principles

These principles constrain and guide all NC experience decisions. They do not override governance rules — they translate governance rules into design intent.

### XP-1: Provenance as Desire Signal
Provenance information increases purchase intent. Every provenance element that appears on a product or media page should be designed to make the visitor want the work more, not merely to satisfy a compliance requirement. If provenance text reads like a legal notice, redesign it.

### XP-2: Quality Is a Curation Signal, Not a Technical Threshold
MASTERWORK, FLAGSHIP, STANDARD, and REFERENCE are not database scores — they are editorial marks. A visitor who sees MASTERWORK on an Earthrise print understands that this is the best available version of the most significant image in this collection. The badge communicates curatorial intent.

### XP-3: Commerce Is Contextual, Never Siloed
Products must be discoverable at the point of desire — on the place page, on the illustration gallery, on the story page — not only in the Shop section. The visitor who is moved by the Hayden Survey of Yellowstone should be able to acquire that print without leaving the story.

### XP-4: The Illustration Is the Content
NC is not a website that sells products that happen to be illustrations. NC is an illustrated record of the world's great places that also happens to be shoppable. The hierarchy is: illustration first, story second, product third. Commerce serves discovery; discovery does not serve commerce.

### XP-5: Invisible Governance, Visible Authority
The visitor should never encounter governance language, internal codes, phase labels, or status terminology. The governance system should be invisible at the visitor surface but completely legible at the institutional/research surface (Level 3 provenance view). NC's authority comes from the depth of its verification system — that depth should be present and accessible without being foregrounded.

---

## VII. Phase Activation Alignment

This section maps experience improvements to the existing phase activation gates to prevent design work being blocked by governance prerequisites.

| Phase | Gate | Experience work authorized |
|---|---|---|
| **Phase 0** | Gate E (two-human curator + PA session) | Improvements #1–5, #9, #13, #17, #19, #22, #23, #24, #25, #49 |
| **Phase 1** | SA-GEONAMES-001 + SA-OSM-001 ratified | Improvements #6, #7, #10, #11, #15, #16, #18, #20, #21, #26–31, #35 |
| **Phase 1 + NC-AI-006 unblocked** | Migration 45 + ASSET-001 + PROTO-001 | Improvement #32 (Yellowstone AI stories) |
| **Phase 1 + NC-AI-001 C-7** | First model activation gate | Improvements #33, #39 (AI content at scale) |
| **Phase 2** | NOAA Sprint 3 gate check | Improvements #8, #34, #36–38, #40–44 |
| **Phase 3+** | Amendment P3-1 | Improvement #43 (audio narration) |

**Phase 0 experience target:** After Gate E, the site should score 6.5+ on all dimensions. The critical gap to close before Gate E is visual (replacing `<div>` placeholders with actual imagery) and copy (replacing governance language with editorial voice). This is entirely within current authorization.

---

## VIII. Success Metrics

These are visitor experience metrics, not governance metrics. They complement the governance KPIs in NC-PILOT-001.

| Metric | Phase 0 target | Phase 1 target | Phase 2 target |
|---|---|---|---|
| Time on Earthrise story page | > 90 seconds | — | — |
| Earthrise product page → inquiry conversion | > 3% | — | — |
| Homepage → place page click-through | — | > 25% | — |
| Place page → product page click-through | — | > 15% | — |
| Average pages per session | > 2.5 | > 3.5 | > 4.5 |
| Return visitor rate (30 days) | > 20% | > 30% | > 35% |
| Institutional licensing inquiry rate | — | > 1 per month | > 5 per month |
| Mobile session share | > 40% | > 45% | > 50% |

---

## IX. Ratification Conditions

Before NC-EXPERIENCE-001 is ratified, the following must be confirmed:

**C-1:** NC-WEB-001 ratified (NC-EXPERIENCE-001 operates within NC-WEB-001's attribution and copy constraints).

**C-2:** Wireframe Constitution v1 remains authoritative for L1 navigation structure (Places / Discover / Stories / Collections / Shop).

**C-3:** Improvement #1 (Earthrise image in homepage hero) classified as a Phase 0 authorized action — the image (NC-NASA-002) already has human_verified=TRUE and rights_status=verified_pd. Displaying it requires no new governance action, only design execution.

**C-4:** "Discover" and "Collections" L1 nav items (#11) authorized for Phase 1 build (no governance block identified — Wireframe Constitution already mandates them).

**C-5:** B2B institutional licensing inquiry CTA (#30) is classified as a marketing inquiry surface, not a commerce surface. No Commerce Execution Constitution provisions apply until an actual transaction is contemplated.

---

*NC-EXPERIENCE-001 v1.0 · Drafted 2026-06-12 · Pending ratification · Principal Architect*
