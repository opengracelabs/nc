# NC-WEB-001: Website Governance + UX Blueprint

| Field | Value |
|---|---|
| Document | NC-WEB-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | NC-PILOT-001-FRR · NC-COMMERCE-001 · NC-COMMERCE-002 · NC-FIRST-SALE · NC-PRODUCT-001 · DD-NASA-001 (pending) · SA-GEONAMES-001 · SA-OSM-001 |
| Governs | All public-facing web pages for the NC pilot launch and Phase 2+ progression |
| Scope | 10 pages: Home, Earthrise Product, Earthrise Story, Pilot Places Index, Yellowstone, Grand Canyon, Great Barrier Reef, Galápagos, About, Products |

---

## I. Purpose

This document establishes the governance framework, UX requirements, attribution obligations, copy rules, launch sequencing, and prohibited content for the NC pilot website. It translates the commercial authorization (NC-COMMERCE-001), revenue authorization (NC-COMMERCE-002), and first-sale authorization (NC-FIRST-SALE) into actionable page-level specifications.

Every page must satisfy four non-negotiable invariants before going live:
- **IFC-1:** `rights_status = verified_pd` and `human_verified = TRUE` for every displayed asset
- **GN-6:** GeoNames CC BY 4.0 attribution on every place page where GeoNames data is displayed
- **OS-6:** OSM ODbL attribution on every page rendering OSM tiles
- **Federal nonendorsement:** Exact NASA/NOAA nonendorsement text on every page displaying federal-sourced assets

Violation of any of these invariants triggers cascade deactivation of all affected products (NC-PRODUCT-001 §IV).

---

## II. Page Inventory and Launch Status

| # | Page | URL | Phase | Gate | Status |
|---|---|---|---|---|---|
| 1 | Home | `/` | Phase 0 | Gate E | Ready after Gate E |
| 2 | Earthrise Product Page | `/products/earthrise-giclée` | Phase 0 | Gate E | Ready after FS-001 + FS-002 corrected |
| 3 | Earthrise Story Page | `/stories/earthrise` | Phase 0 | Gate E | Ready after Gate E |
| 4 | Pilot Places Index | `/places` | Phase 1 | SA-GEONAMES-001 ratified | Blocked — SA gates |
| 5 | Yellowstone | `/places/yellowstone` | Phase 1 | SA-GEONAMES-001 + SA-OSM-001 ratified | Blocked — SA gates |
| 6 | Grand Canyon | `/places/grand-canyon` | Phase 1 | SA-GEONAMES-001 + SA-OSM-001 ratified | Blocked — SA gates |
| 7 | Great Barrier Reef | `/places/great-barrier-reef` | Phase 2 | SA-GEONAMES-001 + SA-OSM-001 ratified | Blocked — SA gates + NOAA gate |
| 8 | Galápagos | `/places/galapagos` | Phase 2 | SA-GEONAMES-001 + SA-OSM-001 ratified | Blocked — SA gates |
| 9 | About | `/about` | Phase 0 | Gate E | Ready after Gate E |
| 10 | Products | `/products` | Phase 0 (Earthrise only) | Gate E | Phase 0: Earthrise only |

**Phase 0** = activates at Gate E (curator + PA two-human session), no SA ratification required.
**Phase 1** = requires SA-GEONAMES-001 + SA-OSM-001 ratified.
**Phase 2** = same as Phase 1 plus NOAA Sprint 3 gate check for GBR.

---

## III. Attribution and Disclaimer Registry

This section is the single source of truth for what attribution text must appear on each page, what exact wording is required, and where it must be placed.

### III.1 Attribution Building Blocks

**NASA Nonendorsement (mandatory, exact, immutable):**
```
Image credit: NASA. NASA does not endorse this product.
```

**NASA Asset Credit (Earthrise, mandatory, exact, per FS-001):**
```
NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.
```

**NOAA Nonendorsement (mandatory, with division):**
```
Credit: NOAA/[Division]
```
For GBR: `Credit: NOAA/CRCP` (Coral Reef Conservation Program) unless a more specific division is identified in the asset record.

**GeoNames CC BY 4.0 (mandatory on all place pages, exact, immutable):**
```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
```
"GeoNames" must hyperlink to `https://www.geonames.org`.

**OSM ODbL (mandatory on all pages displaying map tiles, exact, immutable):**
```
© OpenStreetMap contributors
```
For Mapbox-served tiles, full chain:
```
© OpenStreetMap contributors   |   Map data provided by Mapbox
```
OSM attribution must appear first and must never be visually smaller than Mapbox attribution. "OpenStreetMap contributors" must hyperlink to `https://www.openstreetmap.org/copyright`.

**Co-attribution order (when multiple attributions present, per SA-GEONAMES-001 §III.1):**
1. Asset credit (NASA, NOAA, institution)
2. Geographic data: GeoNames CC BY 4.0
3. Map tiles: OSM ODbL (if map tiles present)
4. Any additional institutional credit

---

### III.2 Per-Page Attribution Matrix

#### Page 1 — Home (`/`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| NASA nonendorsement | Conditional — only if a NASA asset is featured in the hero or editorial modules | Exact standard line | Footer, adjacent to asset |
| GeoNames CC BY 4.0 | NO — Home displays no place-derived GeoNames data | — | — |
| OSM ODbL | NO — Home displays no map tiles | — | — |

**Rationale:** Earthrise (AS08-14-2383) is S-3 cosmic anchor exception — no GeoNames ID. If Earthrise appears in the hero, NASA nonendorsement is required but GeoNames and OSM are not. If no federal assets appear on the home page, no attribution is required.

**Disclaimer:** No product eligibility claims. No "collector's edition" language. No Moran references. No Venice content claims.

---

#### Page 2 — Earthrise Product Page (`/products/earthrise-giclée`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| NASA Asset Credit (FS-001 exact text) | YES — mandatory | `NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.` | Zone 2 (below product title, above purchase CTA) |
| NASA nonendorsement | YES — mandatory | `Image credit: NASA. NASA does not endorse this product.` | Zone 2, immediately after asset credit |
| GeoNames CC BY 4.0 | NO — Earthrise S-3 exception | — | — |
| OSM ODbL | NO — no map tiles on Earthrise page | — | — |
| COA notice | YES — for NC-PROD-001 (museum_print) | "Includes Certificate of Authenticity" | Zone 3 (product details) |
| Rights statement | YES | "Public domain — United States Government Work, 17 U.S.C. § 105" | Zone 3 |

**Critical:** Per FS-001, the phrase "NARA: Verified archival source" must NOT appear anywhere on this page. AS08-14-2383 is a NASA photograph; NARA attribution format is reserved for NARA-sourced assets only. Any COA referencing "National Archives" for Earthrise is incorrect and must not be used.

**Prohibited on this page:**
- "Collector's Edition" listing or language (NARA Sprint 1 required)
- Price or availability for the 30"×30" Acrylic variant
- Any reference to Thomas Moran or Yellowstone paintings
- Any implication that NC is affiliated with or endorsed by NASA

---

#### Page 3 — Earthrise Story Page (`/stories/earthrise`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| NASA Asset Credit | YES — for each NASA image used in the story | Exact asset-level credit | Below each image, inline |
| NASA nonendorsement | YES | Exact standard line | Article footer |
| GeoNames CC BY 4.0 | NO — no place data | — | — |
| OSM ODbL | NO — no map tiles | — | — |

**Copy rule:** The story may describe Earthrise in its historical context (Apollo 8, December 24, 1968, William Anders) without implying NASA endorsement of NC as a business. The story is editorial — it may describe the photograph's cultural significance freely, provided the nonendorsement line appears in the footer.

**Permitted claims:** Public domain status (§ 105), historical provenance, cultural impact.

**Prohibited on this page:**
- Any claim that NASA has reviewed or approved NC editorial content
- NARA attribution for Earthrise
- References to deferred assets (Moran, ESA/Copernicus imagery)
- "Earthrise from the National Archives" or equivalent

---

#### Page 4 — Pilot Places Index (`/places`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| GeoNames CC BY 4.0 | YES — if place cards display GeoNames-derived data (name, coordinates) | Full form | Page footer |
| OSM ODbL | YES — if a global overview map is displayed | Exact attribution, map overlay bottom-right | Map widget |
| NASA nonendorsement | Conditional — if NASA thumbnail shown per place card | Standard line | Footer, or tooltip on hover |

**Gate:** This page must not go live before SA-GEONAMES-001 is ratified and SA-OSM-001 is ratified. If a simplified text-only index (no map, no GeoNames coordinates) is feasible for Phase 0, that version may launch at Gate E. The map variant requires both SAs.

**Content state rules:**
- Show 5 active places: Yellowstone, Grand Canyon, Great Barrier Reef, Galápagos, and Earthrise (as cosmic anchor)
- Venice: show as a place card with `content_status: partial` notation — "Coming soon — expanding 2026"
- Papahānaumokuākea: show as a place card with `content_status: coming_soon` — do not display until GeoNames ID confirmed
- Do not show institution thumbnails, asset counts, or product counts until each place page is fully live

---

#### Page 5 — Yellowstone (`/places/yellowstone`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| GeoNames CC BY 4.0 | YES | `Geographic data © GeoNames (geonames.org) — CC BY 4.0` | Page footer, always visible without scroll on desktop |
| OSM ODbL | YES | `© OpenStreetMap contributors \| Map data provided by Mapbox` | Map overlay, bottom-right corner |
| NASA nonendorsement | YES — for NC-NASA-026 (Yellowstone from Orbit) | `Image credit: NASA. NASA does not endorse this product.` | Adjacent to asset display, above footer |
| Rights badge | YES — on every asset card | PD badge (§ 105) | Asset card, always visible |
| Quality tier | YES — on every asset card | FLAGSHIP or STANDARD badge | Asset card |

**Canonical GeoNames ID:** 5843591 (authoritative per NC-DATA-001, 2026-06-12).
**GeoNames ID note:** Blueprint had incorrect ID 4720206. Intelligence Plan and NC-PILOT-001 FRR §III subsequently adopted 5843642, based on an erroneous Wikidata P1566 claim. NC-DATA-001 retired 5843642; 5843591 is the GeoNames direct API response for "Yellowstone National Park" (fcode=PRKA). Use 5843591 only.

**Assets approved for display (Phase 1):**
- NC-NASA-026: Yellowstone from Orbit — FLAGSHIP, § 105 (NASA)
- NARA-HAYDEN-1871: Hayden Survey Map 1871 — pending NARA Sprint 1 `Unrestricted` confirmation; display as "Coming soon — verifying archival status"
- BHL-BISON-001: American Bison illustration — pre-1928 PD

**Contextual commerce module:** NC-PROD-002 (Framed Print), NC-PROD-003 (Hayden Map — pending NARA Sprint 1), NC-PROD-010 (Calendar — Phase 4)

---

#### Page 6 — Grand Canyon (`/places/grand-canyon`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| GeoNames CC BY 4.0 | YES | Full form | Page footer |
| OSM ODbL | YES | With Mapbox chain | Map overlay |
| NASA nonendorsement | YES — for NC-NASA-027 | Standard line | Adjacent to asset |
| Rights badge | YES | PD badge | Asset card |

**Canonical GeoNames ID:** 5296401 (confirmed via Wikidata P1566, 2026-06-11).
**GeoNames ID note:** Both Blueprint and Intelligence Plan had incorrect IDs; use 5296401 only.

**Assets approved for display (Phase 1):**
- NC-NASA-027: Grand Canyon Strata — FLAGSHIP, § 105 (NASA)
- NARA-POWELL-1869: Powell Expedition Photograph — pending NARA Sprint 1 `Unrestricted` confirmation
- NARA-USGS-GC: USGS Grand Canyon Cross-Section — pending NARA Sprint 1 `Unrestricted` confirmation
- BHL-CONDOR-001: California Condor illustration — pre-1928 PD

**Contextual commerce module:** NC-PROD-004 (Grand Canyon Strata Print — pending NARA Sprint 1)

---

#### Page 7 — Great Barrier Reef (`/places/great-barrier-reef`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| GeoNames CC BY 4.0 | YES | Full form | Page footer |
| OSM ODbL | YES | With Mapbox chain | Map overlay |
| NASA nonendorsement | YES — for NC-NASA-029 | Standard line | Adjacent to asset |
| NOAA nonendorsement | YES — for NOAA coral reef asset | `Credit: NOAA/CRCP` | Adjacent to NOAA asset |
| Rights badge | YES | PD badge | Asset card |

**Canonical GeoNames ID:** 2164628 (confirmed via live GeoNames RDF + Wikidata P1566, NC-DATA-005 2026-06-12). Feature code: **H.RF** (reef) — not RFSU as earlier claimed.
**GeoNames ID note:** Both prior docs had incorrect IDs (Intelligence Plan had 10288865 = Clarion hotel; Blueprint had no ID). Use 2164628 only.

**Assets approved for display (Phase 2):**
- NC-NASA-029: Great Barrier Reef Satellite — FLAGSHIP, § 105 (NASA)
- BHL-HAECKEL-HC: Haeckel Hexacoralla — MASTERWORK, pre-1928 PD (pending curator confirmation 6000px)
- BHL-CHELONIA-001: Green Sea Turtle illustration — pre-1928 PD
- NOAA coral reef asset — ALLOWED (SA-NOAA-001/002 ratified; subject to Sprint 3 ALLOWED cap, 0/7 writes used)

**NOAA write cap status:** Displaying NOAA asset on GBR page = write #1 of 7. This cap must be checked before activation. NOAA REVIEW_REQUIRED assets: 0 writes, pilot exclusion.

**Contextual commerce module:** NC-PROD-007 (GBR Satellite Print), NC-PROD-006 (Haeckel Hexacoralla — curator + 6000px confirmation required)

---

#### Page 8 — Galápagos (`/places/galapagos`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| GeoNames CC BY 4.0 | YES | Full form | Page footer |
| OSM ODbL | YES | With Mapbox chain | Map overlay |
| NASA nonendorsement | YES — for NC-NASA-042/043 | Standard line | Adjacent to asset |
| Rights badge | YES | PD badge | Asset card |
| BHL attribution | YES — for BHL-sourced assets | `Source: Biodiversity Heritage Library` | Asset credit |

**Canonical GeoNames ID:** 3658931 (confirmed).

**Assets approved for display (Phase 2):**
- NC-NASA-042/043: Galápagos from Orbit — § 105 (NASA)
- BHL-GOULD-FINCHES: Darwin's Finches — FLAGSHIP, pre-1928 PD (John Gould, 1841)
- BHL-CHELONOIDIS-001: Galápagos Tortoise — pre-1928 PD
- BHL-MONACHUS-001: Galápagos Sea Lion or equivalent — pre-1928 PD

**Platform note:** Galápagos has the richest GBIF evidence in the pilot (SA-GBIF-001 ratified). GBIF occurrence data may be displayed as evidence layer (observation counts, species counts). GBIF media is permanently excluded — display text/count data only.

**Contextual commerce module:** NC-PROD-005 (Darwin's Finches Archival Print — FLAGSHIP), NC-PROD-009 (Galápagos Education Pack)

---

#### Page 9 — About (`/about`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| GeoNames CC BY 4.0 | NO — no place data on About | — | — |
| OSM ODbL | NO — no map tiles | — | — |
| NASA nonendorsement | Conditional — only if a NASA asset is used on the page | Standard line | Adjacent to asset |

**Purpose:** Mission, doctrine, provenance standards, team (if applicable). Trust-building for first-time buyers. Not a commerce page.

**Required elements:**
- Public domain commitment statement: NC sells only works that are verifiably in the public domain (PD/CC0)
- Rights verification statement: All assets are individually verified; rights are governed by institution-specific decision documents
- Attribution statement: NC credits all source institutions, creators, and data providers on every product and page

**Prohibited on this page:**
- Specific product pricing
- Claims of institutional endorsement or partnership with NASA, NOAA, or any federal agency
- Claims of institutional affiliation with Smithsonian, British Museum, or similar

---

#### Page 10 — Products (`/products`)

| Attribution | Required | Form | Placement |
|---|---|---|---|
| NASA nonendorsement | YES — on every product listing card where a NASA asset is the featured image | Standard line (compact form permitted in card layout) | Below product thumbnail |
| GeoNames CC BY 4.0 | Conditional — required on listing pages that surface geo-anchored product data | Full form | Page footer |
| OSM ODbL | NO — product listings do not display map tiles | — | — |

**Phase 0 content (Gate E):**
- NC-PROD-001: Earthrise Museum Giclée — LIVE
- NC-PROD-008: Earthrise Digital Download — LIVE

**Phase 1 additions (SA ratified):**
- NC-PROD-002: Yellowstone from Orbit Framed Print
- NC-PROD-005: Darwin's Finches Archival Print (BHL scan ≥ 3600px confirmed)
- NC-PROD-007: GBR Whitsundays Satellite Print
- NC-PROD-009: Galápagos Education Pack

**Phase 2 additions (NARA Sprint 1 complete):**
- NC-PROD-003: Hayden Survey 1871 Map Print
- NC-PROD-004: Grand Canyon Strata Print

**Phase 3 additions (curator + quality gate):**
- NC-PROD-006: Haeckel Hexacoralla Archival Print (6000px confirmed)
- NC-PROD-010: Yellowstone Wildlife Calendar (12-panel attribution audit)

**Content state rules:**
- Products with status `coming_soon` may show a card with "Notify me" CTA — no price, no "add to cart"
- Products with status `pending_review` must not appear on the public listing
- RESERVED product lines (fashion, apparel) must not appear in any form

---

## IV. Product-Safe Copy Rules

These rules govern what language may appear anywhere on the public website. They are derived from NC-FIRST-SALE (FS-001, FS-002), NC-PRODUCT-001 §IV nonendorsement doctrine, and the deferred asset catalog in NC-COMMERCE-001.

### IV.1 Federal Agency Nonendorsement (zero-tolerance)

**Rule:** No copy on any page may state or imply that NASA, NOAA, or any other US federal agency endorses, approves of, certifies, or partners with Nature & Culture.

**Allowed formulations:**
- "Earthrise — NASA photograph, § 105 public domain"
- "Image credit: NASA" (with nonendorsement line)
- "A photograph taken during the Apollo 8 mission"
- "From the NASA image archive"
- "Original source: NASA Earth Observatory"

**Prohibited formulations:**
- "NASA-certified" / "NASA-approved" / "NASA-endorsed"
- "In partnership with NASA"
- "Official NASA print" / "Official NASA product"
- "Verified by NASA" / "NASA archival quality"
- "NOAA-certified" or any NOAA endorsement equivalent
- Any copy suggesting federal agency review of NC's product quality

**Consequence of violation:** Cascade deactivation of ALL federal-source assets across the entire catalog (NC-PRODUCT-001 §IV).

### IV.2 Rights and Provenance Claims

**Rule:** Every rights claim must correspond to a verified, human-reviewed record in the NC catalog. No speculative rights claims permitted.

**Allowed formulations:**
- "Public domain — United States Government Work (17 U.S.C. § 105)"
- "Published prior to 1928 — US public domain"
- "CC0 — No Rights Reserved"
- "Source: [Institution name]"

**Prohibited formulations:**
- "Rights-free" (not a recognized rights status)
- "License-free"
- "Royalty-free" (this describes licensing terms, not PD status; it is misleading in the NC context)
- Any rights claim for an asset whose `human_verified` = FALSE or `rights_status` ≠ `verified_pd`

### IV.3 Deferred Asset Copy Rule (per FS-002)

**Rule:** No deferred asset may appear in any public-facing copy, including product descriptions, editorial stories, email campaigns, social copy, or landing pages, in a way that implies the asset is available for purchase or that NC has product rights to it.

**Deferred assets (must not appear as available products):**
- Thomas Moran paintings (Smithsonian — DD-SMITHSONIAN-001 required)
- Canaletto Venice paintings (Museo Correr — no DD)
- HMS Beagle chart (UKHO — DD-TNA-001/UKHO-001 required)
- de' Barbari 1500 Venice map (Museo Correr — no DD)
- St. Mark's Basilica elevation (unidentified institution)
- ESA/Copernicus imagery (DD-ESA-001 required)
- Darwin's sketch notebook (Cambridge UL — no DD)
- Cook's Pacific chart (UK archives — DD-TNA-001 required)

**Email campaign rule (FS-002):** Email 3 (Thomas Moran painting) is permanently held pending DD-SMITHSONIAN-001. Only Email 1 and Email 2 are authorized for the Phase 0 launch campaign.

### IV.4 Quality and Edition Claims

**Rule:** Edition claims (e.g., "limited edition", "museum-grade") must be technically correct and correspond to the product specification in the NC-COMMERCE-001 record.

**Allowed for NC-PROD-001:**
- "310gsm Hahnemühle Photo Rag" (technically specified)
- "Museum-grade giclée print" (print line: `museum_print`, correct)
- "Archival pigment inks" (if printer specification confirms this)
- "Includes Certificate of Authenticity"

**Collector Edition (30"×30" Acrylic):**
- Must not be listed, pre-sold, or teased until NARA Apollo 8 Mission Plan naId is confirmed (NARA Sprint 1)
- No "collector's edition" language anywhere until Phase 1b is cleared

### IV.5 Earthrise Sourcing (FS-001)

**Rule:** Earthrise (AS08-14-2383) source attribution is NASA only. NARA attribution is prohibited.

**Exact required copy:**
```
NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.
```

**Prohibited:** "National Archives", "NARA archival source", "Archives verified", or any copy implying NARA as source or verifier for Earthrise.

### IV.6 Venice Content-Thin Notation

**Rule:** Venice is `content_status: partial` at launch. The Venice place page (if shown) must not display asset counts or product counts until at least one art museum DD is ratified (DD-MET-001, DD-AIC-001, or DD-CMA-001).

**Venice placeholder copy (permitted):** "Venice — expanding collection. Full digital archive launching [year]."

**Prohibited:** Any reference to Canaletto, de' Barbari, or other Venice art works in any commercial context until the relevant DD is ratified.

---

## V. Wireframe Requirements

Per the Wireframe Constitution v1, all page designs must comply with the content state rules (Articles 15–18), rights visibility rules (Article 16), quality signal rules (Article 17), and the contextual commerce doctrine. Commerce must appear on every page where contextually relevant — it is not siloed to `/products`.

### V.1 Global Requirements (all pages)

**Navigation:**
- L1: Places / Discover / Stories / Collections / Shop
- Utility: Search / Account / Cart
- Active state on current section
- Cart icon shows count when items present

**Rights visibility:**
- PD badge (or CC0 badge) on every asset appearance, on every page, always
- Badge must be visible without hover or interaction — not behind a tooltip

**Quality tier:**
- MASTERWORK / FLAGSHIP / STANDARD / REFERENCE badge on every asset card
- Raw scores (COS, TAS) are hidden from public surfaces — tier label only

**Phase 2–4 content types:**
- Books, eBooks, Audiobooks, Audio, Film, 3D, Datasets: show as "Coming Soon" stubs
- No counts, no thumbnails for unavailable types
- Stub cards link to a waitlist or notification form

### V.2 Page-Level Wireframe Specifications

---

#### Home (`/`)

**Priority:** Highest. First impression and primary acquisition surface.

**Zones:**
```
[Hero — full-width, editorial image + headline + CTA]
[Featured Place Strip — 3–4 place cards: Yellowstone, Grand Canyon, Galápagos, GBR]
[Featured Story — Earthrise story card with "Read the Story" CTA]
[Featured Product — NC-PROD-001 or NC-PROD-008 with "Shop" CTA]
[Content Type Navigator — Places / Photography / Botanical Art / Maps / Fine Art + Coming Soon stubs]
[About Strip — 2-sentence mission + "About NC" link]
[Footer — attribution block (conditional) + nav links]
```

**Hero rules:**
- Phase 0 hero: Earthrise (AS08-14-2383) or NASA Earth asset
- NASA nonendorsement line required if NASA asset is hero
- No GeoNames or OSM attribution required on Home
- CTA options: "Explore Earthrise" (→ story page) or "Shop Earthrise" (→ product page)

**Featured Place Strip:**
- Phase 0: 1–2 place teaser cards (Yellowstone, Grand Canyon) with "Coming Soon" state
- Phase 1: Full place cards with asset previews and "Explore" CTAs
- Each place card must show PD badge on any asset thumbnail

**Commerce module:**
- Featured product card: product name, price, product tier badge, PD badge, "Shop now" CTA
- No non-endorsed product copy

---

#### Earthrise Product Page (`/products/earthrise-giclée`)

**Priority:** Highest — primary revenue conversion surface for Phase 0.

**Zones:**
```
[Zone 1 — Hero image: AS08-14-2383, full-bleed or large]
[Zone 2 — Attribution block (FS-001 exact text + nonendorsement line)]
[Zone 3 — Product title, edition, product tier badge (MASTERWORK), PD badge (§ 105)]
[Zone 4 — Product variants: NC-PROD-001 (Museum Giclée) / NC-PROD-008 (Digital Download)]
[Zone 5 — Price + "Add to Cart" CTA]
[Zone 6 — Product details: paper spec, dimensions, ink type, COA notice]
[Zone 7 — Rights details: "Public domain — US Government Work, 17 U.S.C. § 105"]
[Zone 8 — Story link: "Read the Earthrise story →"]
[Zone 9 — Footer attribution block]
```

**Zone 2 exact copy (FS-001):**
```
NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.
Image credit: NASA. NASA does not endorse this product.
```

**Zone 4 variants:**
- NC-PROD-001: "Earthrise Museum Giclée — 24"×20", 310gsm Hahnemühle Photo Rag, archival pigment, COA included"
- NC-PROD-008: "Earthrise Digital Download — High-resolution TIFF, 3000px / 300 DPI, institutional license"
- "Collector's Edition" variant: DO NOT show — NARA Sprint 1 required

**Zone 7 rights display:**
```
Rights: Public Domain — United States Government Work
Basis: 17 U.S.C. § 105 (works of US federal employees, within scope of employment)
Source: NASA — National Aeronautics and Space Administration
Asset ID: AS08-14-2383
Human verified: ✓
```

---

#### Earthrise Story Page (`/stories/earthrise`)

**Priority:** High — engagement and trust-building; feeds product page conversion.

**Zones:**
```
[Zone 1 — Story header: title, byline, date]
[Zone 2 — Hero image with inline asset credit]
[Zone 3 — Long-form editorial narrative (scrollytelling or standard article)]
[Zone 4 — Inline images with per-asset credits and PD badges]
[Zone 5 — Product CTA module: "Own Earthrise — Shop the collection →"]
[Zone 6 — Related stories (if available)]
[Zone 7 — Footer: NASA nonendorsement line + footer nav]
```

**Story content rules:**
- May describe the photograph's cultural and historical significance without restriction
- May reference the Apollo 8 mission, William Anders, Frank Borman, Jim Lovell
- Must not claim NASA endorsement of NC editorial voice
- Must not reference deferred assets or future product lines not yet live

**Zone 5 CTA:**
- Links to `/products/earthrise-giclée`
- Shows NC-PROD-001 and NC-PROD-008 product thumbnails with tier + PD badges
- Price displayed

**Footer attribution (Zone 7):**
```
Image credit: NASA. NASA does not endorse this product.
```

---

#### Pilot Places Index (`/places`)

**Priority:** Medium — discovery hub; blocks until Phase 1.

**Zones:**
```
[Zone 1 — Page header: "Explore the World's Natural and Cultural Heritage"]
[Zone 2 — Optional: World overview map (Mapbox GL JS, with OSM attribution)]
[Zone 3 — Place grid: 6 place cards (Earthrise, Yellowstone, Grand Canyon, GBR, Galápagos, Venice)]
[Zone 4 — Coming Soon cards: Papahānaumokuākea + additional places]
[Zone 5 — Footer: GeoNames CC BY 4.0 + OSM ODbL (if map shown)]
```

**Place card content:**
- Place name, heritage type badge (UNESCO WHS / Marine Park / National Park / etc.)
- Featured asset thumbnail with PD badge
- Asset count (once place page is live)
- "Explore" CTA (→ place page)
- "Coming soon" state for locked places: no asset count, no thumbnail of deferred assets

**Map zone:** Optional for Phase 1 launch. If displayed: Mapbox GL JS required; OSM attribution mandatory; no OSM data stored in NC tables.

**Earthrise card:** Cosmic anchor exception — show Earthrise as a special "cosmic place" card distinct from terrestrial place cards. No GeoNames attribution for Earthrise card itself.

---

#### Place Pages — Yellowstone, Grand Canyon, Great Barrier Reef, Galápagos

**Shared wireframe (all 4 place pages):**

```
[Zone 1 — Place header: Name, heritage designation, GeoNames-derived metadata]
[Zone 2 — Place map (Mapbox GL JS, with OSM attribution)]
[Zone 3 — Featured asset (hero, full-width, with PD badge + asset credit)]
[Zone 4 — Asset gallery: grid of approved assets, each with PD badge + quality tier + source credit]
[Zone 5 — Story module: linked story cards (if editorial story published)]
[Zone 6 — Evidence layer: GBIF observation count, species count (text only, no GBIF thumbnails)]
[Zone 7 — Commerce module: product cards for assets anchored to this place]
[Zone 8 — Institution credits: NASA, NOAA (if applicable), BHL, NARA (if applicable)]
[Zone 9 — Footer: GeoNames CC BY 4.0 + OSM ODbL + federal nonendorsement lines]
```

**Zone 2 map requirements:**
- Mapbox GL JS primary; Protomaps PMTiles fallback
- OSM tile CDN prohibited
- No OSM data stored in NC tables (OS-1 invariant)
- Attribution "© OpenStreetMap contributors | Map data provided by Mapbox" bottom-right, always visible

**Zone 4 asset gallery:**
- NARA-pending assets (Hayden, Powell, USGS): show as "Coming soon — pending archival verification" until NARA Sprint 1 confirms `Unrestricted` status
- Do not show NARA assets with a live "Add to Cart" CTA until Sprint 1 complete
- PD badge required on every card; quality tier badge required on every card

**Zone 6 evidence layer:**
- GBIF: display occurrence count + species count as text stats — "1,247 documented observations" — no GBIF thumbnails, no GBIF media
- GBIF media is permanently excluded (SA-GBIF-001 media exclusion, unconditional)

**Zone 7 commerce module:**
- Shows only products in current activated phase for this place
- "Notify me" placeholder card for products still in pre-activation state
- NASA nonendorsement line adjacent to each NASA-sourced product card

**Zone 9 footer attribution (per place):**

Yellowstone/Grand Canyon:
```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
© OpenStreetMap contributors | Map data provided by Mapbox
Image credit: NASA. NASA does not endorse this product.
```

GBR:
```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
© OpenStreetMap contributors | Map data provided by Mapbox
Image credit: NASA. NASA does not endorse this product.
Credit: NOAA/CRCP
```

Galápagos:
```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
© OpenStreetMap contributors | Map data provided by Mapbox
Image credit: NASA. NASA does not endorse this product.
Source: Biodiversity Heritage Library
```

---

#### About (`/about`)

**Priority:** Medium — trust and credibility for first-time buyers.

**Zones:**
```
[Zone 1 — Mission statement]
[Zone 2 — Public domain doctrine: what we sell and why]
[Zone 3 — Rights verification process: how assets are verified]
[Zone 4 — Source institutions: list of content institution logos/names + links]
[Zone 5 — Attribution standards: brief explanation of CC BY, § 105, pre-1928 PD]
[Zone 6 — Contact / press]
[Zone 7 — Footer: no special attribution required]
```

**Mission statement copy (recommended):**
> "Nature & Culture is a commerce platform for the world's public-domain natural and cultural heritage. Every asset we sell is individually verified as genuinely in the public domain. Every product we offer comes with complete provenance."

**Source institution list (Phase 0):** NASA, BHL (Biodiversity Heritage Library), GeoNames (place data)
**Source institution list (Phase 1 additions):** NARA, NOAA
**Do not list:** Institutions with pending DDs (Smithsonian, Met, etc.) — listing implies product availability

---

#### Products (`/products`)

**Priority:** High — catalog hub; scales with each product phase.

**Zones:**
```
[Zone 1 — Page header: "The NC Collection"]
[Zone 2 — Filter bar: Place / Content Type / Product Line / Quality Tier / Price]
[Zone 3 — Product grid: approved product cards]
[Zone 4 — Coming Soon grid: pre-launch product cards with "Notify me" CTA]
[Zone 5 — Footer: GeoNames CC BY 4.0 (if geo-anchored products present) + NASA nonendorsement]
```

**Product card required elements:**
- Product image (asset thumbnail)
- PD badge
- Quality tier badge (MASTERWORK / FLAGSHIP / STANDARD)
- Product line label (Museum Print / Archival Print / Digital Download / etc.)
- Price
- NASA nonendorsement compact form — below thumbnail, for NASA-sourced products
- "Add to Cart" CTA (active) or "Notify me" CTA (pre-launch)

---

## VI. Conversion Funnel Architecture

The NC conversion funnel has three branches, reflecting the platform's contextual commerce doctrine (commerce on every page, not siloed).

### VI.1 Primary Funnel — Earthrise (Phase 0)

```
Awareness
└── External: social, PR, direct URL
    │
    ▼
Discovery
└── Home (hero: Earthrise) → "Read the Story" or "Shop Earthrise"
    │
    ▼
Engagement
└── Earthrise Story Page → reads narrative, sees cultural significance, CTA at bottom
    │
    ▼
Intent
└── Earthrise Product Page (Zone 5: Add to Cart)
    │
    ▼
Conversion
└── Cart → Checkout → Confirmation
    └── NC-PROD-008 first (digital, no fulfillment risk)
    └── NC-PROD-001 second (physical, museum giclée + COA)
```

**Key CTA points:**
- Home → Story: "Read the Earthrise story"
- Story → Product: "Own Earthrise — Shop the collection →"
- Product page: "Add to Cart" (primary), "Download instantly" (NC-PROD-008)
- Footer on story page: persistent product link strip

### VI.2 Secondary Funnel — Place Discovery (Phase 1+)

```
Awareness
└── External: editorial, search, social
    │
    ▼
Discovery
└── Home → Place Strip → "Explore [Place]"
   OR Places Index → place card → "Explore"
    │
    ▼
Engagement
└── Place Page (Zone 3–6: asset gallery, stories, GBIF evidence)
    │
    ▼
Intent
└── Place Page → Zone 7: Commerce Module → product card → "Shop"
   OR Place Page → Story Module → Story Page → product CTA
    │
    ▼
Conversion
└── Product Page → Cart → Checkout
```

**Key insight:** The place page is the primary commerce surface after Phase 0. Every place page carries a commerce module contextually — buyers discover through geography, not through a product catalog.

### VI.3 Browse Funnel — Catalog Discovery (Phase 1+)

```
Awareness
└── Direct URL: /products
    │
    ▼
Discovery
└── Products page → filter by Place / Type / Tier
    │
    ▼
Intent
└── Product card → "Add to Cart" or click → Product Page
    │
    ▼
Conversion
└── Cart → Checkout
```

### VI.4 Funnel Metrics Framework

| Funnel Stage | Page | KPI |
|---|---|---|
| Awareness | External | Traffic source, landing page distribution |
| Discovery | Home, Places Index | Bounce rate, place card CTR |
| Engagement | Story Page, Place Page | Time on page, scroll depth, story completion rate |
| Intent | Product Page | Add-to-cart rate, product page sessions |
| Conversion | Cart → Checkout | Cart abandonment rate, checkout completion rate |
| Retention | Confirmation, COA | Repeat visit rate, email open rate (Email 1 + 2) |

---

## VII. Launch Order and Phase Gates

### Phase 0 — Gate E (immediate, no SA required)

**Prerequisite:** FS-001 and FS-002 copy corrections complete + two-human Gate E session (curator + PA).

**Pages live:**
1. Home (Earthrise hero, minimal place teaser)
2. Earthrise Story Page
3. Earthrise Product Page (NC-PROD-001 + NC-PROD-008 only)
4. About
5. Products page (Earthrise products only)

**Products live:** NC-PROD-008 (activate first — digital, zero fulfillment risk), then NC-PROD-001 (museum giclée + COA).

**Emails authorized:** Email 1 + Email 2 only. Email 3 (Moran) held indefinitely.

**60-day cosmic anchor clock starts at first sale.** Earthrise S-3 provisional exception must be resolved (Standards Constitution amendment OR proxy-place resolution) within 60 days of NC-PROD-001 or NC-PROD-008 first transaction.

---

### Phase 1 — SA Gates (SA-GEONAMES-001 + SA-OSM-001 ratified)

**Prerequisites:** Both SAs ratified. NARA Sprint 1 complete for map products (NC-PROD-003, 004).

**Pages live (add):**
1. Pilot Places Index (`/places`)
2. Yellowstone place page
3. Grand Canyon place page

**Products activated:**
- NC-PROD-002: Yellowstone from Orbit Framed Print (§ 105, no NARA dependency)
- NC-PROD-005: Darwin's Finches Archival Print (BHL scan ≥ 3600px confirmed)
- NC-PROD-003: Hayden Survey Map Print (NARA Sprint 1 complete — `Unrestricted` confirmed)
- NC-PROD-004: Grand Canyon Strata Print (NARA Sprint 1 complete)

**Note:** Galápagos is next after Yellowstone/Grand Canyon even though it shares the Phase 1 SA requirement — GBR requires an additional NOAA gate check. Activate Galápagos concurrently with Phase 1 or immediately after.

---

### Phase 2 — NOAA Gate + BHL Quality Gate

**Prerequisites:** Phase 1 complete. NOAA Sprint 3 gate check (NOAA write cap at 0/7; GBR display = write #1). BHL 6000px confirmed for Haeckel.

**Pages live (add):**
1. Great Barrier Reef place page
2. Galápagos place page (if not activated in Phase 1)

**Products activated:**
- NC-PROD-007: GBR Whitsundays Satellite Print (§ 105)
- NC-PROD-009: Galápagos Education Pack
- NC-PROD-006: Haeckel Hexacoralla Archival Print (MASTERWORK — curator + PA + 6000px required)

---

### Phase 3 — NARA Sprint 1 + Collector Edition

**Prerequisites:** NARA Sprint 1 complete (naId + Unrestricted per-record confirmation for Apollo 8 Mission Plan).

**Unlocks:**
- Collector Edition (30"×30" Acrylic, $850, 50 units) — add to Earthrise Product Page as variant
- NC-PROD-010: Yellowstone Wildlife Calendar (12-panel attribution audit required before live)

---

### Phase 4 — Papahānaumokuākea

**Prerequisites:** GeoNames ID confirmed for Papahānaumokuākea (P1566 absent; requires NC GeoNames account lookup). All SAs ratified.

**Pages live (add):**
1. Papahānaumokuākea place page (only after GeoNames ID confirmed)

**Products activated:**
- NOAA-PAPAHANAUMOKUAKEA-BATHY: Flickr license gate check (license ∈ {7,8,9,10})
- Products pending Sprint 3 NOAA write cap audit

---

### Phase 5 — Venice

**Prerequisites:** At least one art museum DD ratified (DD-MET-001, DD-AIC-001, or DD-CMA-001).

**Pages live (add):**
1. Venice place page (upgrades from `content_status: partial` to full)

**Note:** Venice has zero product-safe assets at launch. Phase 5 is entirely gated on DD ratification. No Venice products may be listed or teased until a DD is ratified.

---

## VIII. Prohibited Content Registry

The following content must not appear anywhere on the public website in any phase, unless the specific gate listed is cleared.

### VIII.1 Prohibited Assets (no public display, no product listing, no story reference as available)

| Asset | Reason | Unblocking gate |
|---|---|---|
| Thomas Moran paintings (Smithsonian) | No DD-SMITHSONIAN-001 | DD-SMITHSONIAN-001 ratification |
| Canaletto Venice paintings (Museo Correr) | No DD | New DD required |
| HMS Beagle chart (UKHO) | DD-TNA-001/UKHO-001 required | Those DDs ratified |
| de' Barbari Venice map (Museo Correr) | No DD | New DD required |
| St. Mark's Basilica elevation | Institution unidentified | Institution ID + new DD |
| ESA/Copernicus imagery (mislabeled as NASA) | DD-ESA-001 required; ESA ≠ § 105 | DD-ESA-001 ratification |
| Darwin's sketch notebook (Cambridge UL) | No DD | New DD required |
| Cook's Pacific chart (UK archives) | DD-TNA-001 required | DD-TNA-001 ratification |
| Haeckel Hexacoralla (NC-PROD-006) as museum_print | 6000px unconfirmed | BHL scan ≥ 6000px confirmed |
| Papahānaumokuākea place page | GeoNames ID unconfirmed | GeoNames ID confirmed |
| Venice assets (any) | No art museum DD ratified | First art museum DD ratified |
| NOAA REVIEW_REQUIRED assets | Pilot exclusion; 0 writes authorized | Post-pilot DD revision |

### VIII.2 Prohibited Product Lines

| Line | Reason | Unblocking gate |
|---|---|---|
| Fashion / Apparel (lines 17, 18) | Routing policy v2.0 required | Policy v2.0 adopted |
| Collector Edition (30"×30" Acrylic) | NARA Sprint 1 unconfirmed | NARA Sprint 1 complete |
| New NASA product type additions | DD-NASA-001 not filed | DD-NASA-001 filed |
| MIA assets in lines 1, 6, 20 | Full-resolution unconfirmed (CDN max 800px) | MIA Sprint 1 confirms full-res path |

### VIII.3 Prohibited Copy

| Copy type | Reason |
|---|---|
| "NASA-endorsed" / "NASA-certified" / "NASA partner" | Federal nonendorsement doctrine — zero tolerance |
| "NOAA-endorsed" or any NOAA endorsement variant | Same |
| "NARA: Verified archival source" for Earthrise | FS-001: AS08-14-2383 is NASA, not NARA |
| "Collector's Edition" until NARA Sprint 1 | Phase 1b prerequisite |
| Email 3 (Thomas Moran) in any campaign | FS-002: deferred asset |
| Any price or availability claim for RESERVED product lines | Fashion not activated |
| Venice product claims before DD ratification | No product-safe Venice assets exist |
| GBIF thumbnails or GBIF media on any page | SA-GBIF-001: media permanently excluded |
| OSM data in any NC database-backed display | OS-1 invariant: permanent ban |
| Personal names from NOAA credits as selling points | SA-NOAA-001: personal names permanently blocked |

---

## IX. Governance Obligations and Open Items

### IX.1 Pre-Launch Requirements (must be complete before Gate E)

| # | Action | Owner | Status |
|---|---|---|---|
| PRE-1 | FS-001: Remove NARA attribution from Earthrise product page | Curator | Required |
| PRE-2 | FS-002: Hold Email 3 (Thomas Moran painting) | PA | Required |
| PRE-3 | Gate E two-human session (curator + PA) | Curator + PA | Required |
| PRE-4 | NC-PROD-008 activate first (digital pipeline validation) | PA | Required |
| PRE-5 | NC-PROD-001 activate second | Curator + PA | Required |

### IX.2 Phase 1 Prerequisites

| # | Action | Owner | Priority |
|---|---|---|---|
| SA-1 | SA-GEONAMES-001 ratification | PA | CRITICAL |
| SA-2 | SA-OSM-001 ratification | PA | CRITICAL |
| SA-3 | NARA Sprint 1: naId + Unrestricted for Hayden, Powell, USGS GC | Engineering | HIGH |
| SA-4 | GeoNames account registration (OQ-2) | PA | HIGH |
| SA-5 | Mapbox GL JS integration + custom NC style | Engineering | HIGH |

### IX.3 Post-Launch Obligations

| # | Obligation | Deadline |
|---|---|---|
| POST-1 | T+30: Attribution audit of all live products | 30 days after Phase 0 launch |
| POST-2 | T+60: Earthrise cosmic anchor resolution (S-3 provisional exception) | 60 days after first sale |
| POST-3 | T+60: DD-SMITHSONIAN-001 commission (highest revenue impact) | 60 days after Phase 0 launch |
| POST-4 | T+90: NOAA write cap audit (7-write limit) | 90 days after Phase 2 launch |
| POST-5 | T+180: Phase review — Venice upgrade assessment | 180 days after Phase 0 launch |

### IX.4 Open Governance Items Affecting Website

| OQ | Description | Impact |
|---|---|---|
| OQ-PILOT-3 | Papahānaumokuākea GeoNames ID (Wikidata P1566 absent) | Blocks place page launch entirely |
| OQ-OSM-3 | DD-OVERTURE-001 (Overture Maps CC BY 4.0) | Would allow polygon geometry storage in places table |
| OQ-GN-2 | GeoNames account registration | Required for CC BY 4.0 compliance at scale |
| OQ-NASA-1 | DD-NASA-001 formal filing | Governance debt; blocks new NASA product types |
| OQ-SMITH-1 | DD-SMITHSONIAN-001 | Highest revenue impact unblocking action; Moran Collection |
| OQ-MET-1 | DD-MET-001 ratification | Unblocks Venice; unlocks Japan (ukiyo-e) products |

---

## X. Summary Reference Card

| Page | Phase | SA Required | GeoNames | OSM | NASA Nonendorse | NOAA Nonendorse |
|---|---|---|---|---|---|---|
| Home | 0 | No | No | No | Conditional | No |
| Earthrise Product | 0 | No | No | No | YES (FS-001 exact) | No |
| Earthrise Story | 0 | No | No | No | YES (footer) | No |
| Pilot Places Index | 1 | YES | YES | Conditional | No | No |
| Yellowstone | 1 | YES | YES | YES | YES | No |
| Grand Canyon | 1 | YES | YES | YES | YES | No |
| Great Barrier Reef | 2 | YES | YES | YES | YES | YES |
| Galápagos | 2 | YES | YES | YES | YES | No |
| About | 0 | No | No | No | Conditional | No |
| Products | 0→+ | Conditional | Conditional | No | YES (per product card) | Conditional |

**Attribution trigger:** "YES" = always required. "Conditional" = required only if the relevant content (NASA asset, map tile, place data) is present on the page. "No" = never required on this page regardless of content.

---

*NC-WEB-001 v1.0 — drafted 2026-06-12. Ratification required before Phase 0 launch.*
*Reference models: NC-PILOT-001-FRR · NC-COMMERCE-001 · NC-COMMERCE-002 · NC-FIRST-SALE · NC-PRODUCT-001 · SA-GEONAMES-001 · SA-OSM-001 · Wireframe Constitution v1 · NASA Collection Assessment*
