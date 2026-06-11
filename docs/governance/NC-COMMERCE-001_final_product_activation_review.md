# NC-COMMERCE-001: Final Product Activation Review

| Field | Value |
|---|---|
| Document | NC-COMMERCE-001 |
| Version | 1.0 |
| Status | **DRAFT** — Pending Principal Architect Ratification |
| Date | 2026-06-11 |
| **Authorization** | **COMMERCE AUTHORIZED WITH CONDITIONS** |
| Documents Reviewed | NC-PRODUCT-001 · NC-PILOT-001-LA · NC-PILOT-001 Launch Playbook |
| Asset scope | 16 confirmed product-safe assets · 9 deferred assets |
| First 10 products | Defined — see §III |
| Gate E required | Yes — per product activation event |

---

## I. Document Review Findings

### I.1 NC-PRODUCT-001 Review

NC-PRODUCT-001 establishes an 8-gate activation sequence governing 18 approved product lines (2 reserved: fashion, tote bags). Three findings with direct commerce impact:

**Finding C-001-1: NARA assets are product-safe in rights, not yet adapter-ready.**
DD-NARA-001 confirms § 105 PD for `useRestriction.status == "Unrestricted"` records. However, SA-22 (NARA Rights Matrix) and SA-23 (direct objectUrl delivery protocol) are not yet ratified. NARA assets may be manually curated into the pilot catalog using Sprint 1 API lookups with human-verified rights confirmation. Bulk adapter ingestion requires SA-22/23 ratification. The 4 NARA assets in the product-safe inventory (Hayden Map, Powell Photo, USGS Strata, Battle of Midway Map) are individually clearable through manual Sprint 1 verification.

**Finding C-001-2: NOAA Bathymetric Map carries a sprint-level write cap.**
The NOAA Bathymetric Map (Papahānaumokuākea) is product-safe. Its `license` field must be confirmed ∈ `{7, 8, 9, 10}` per SA-NOAA-001. The Sprint 3 write cap (max 7 NOAA writes) applies across all NOAA assets collectively — not per asset. With 1 NOAA asset in the current product-safe inventory, the cap is not binding at this catalog scale.

**Finding C-001-3: MIA is excluded from lines 1, 6, 20 until Sprint 1 resolution.**
MIA CDN delivers 800px maximum. No MIA assets are in the current 16-asset inventory. MIA restriction has no impact on the first commercial activation wave.

### I.2 NC-PILOT-001 Launch Authorization Review

The LA is authorized (2026-06-11). Relevant findings for commerce activation:

**Finding C-001-4: Venice carries zero product-safe assets at launch.**
Venice place page is editorial-only. No products may be listed. The Venice page may go live without products but must carry `content_status: "partial"` in its operational record. No consumer-facing "coming soon" notice is required.

**Finding C-001-5: Papahānaumokuākea GeoNames ID is unconfirmed.**
The Papahānaumokuākea place page is blocked until the GeoNames ID is confirmed via NC's application account. The 3 Papahānaumokuākea product-safe assets (Laysan Albatross BHL, Battle of Midway Map NARA, NOAA Bathymetric Map) may not activate on the place page until this is resolved. These assets may route and pass Gate 1–7 in preparation; Gate 8 (two-human activation) is blocked pending GeoNames ID confirmation.

**Finding C-001-6: Earthrise is the only single-asset, single-source, zero-complexity launch.**
NC-NASA-002 carries § 105 rights, no GeoNames dependency, no OSM requirement, and no institutional complexity. It is the lowest-risk first activation and the highest CSM tier asset in the catalog. It should activate before any other place.

### I.3 Launch Playbook Reconciliation

The Launch Playbook was produced before the governance sprint completed. Cross-referencing the Playbook's Top 10 Hero Assets and Top 10 Product Opportunities against the product-safe inventory:

**Playbook Hero Assets — Product Safety Ruling:**

| # | Playbook Asset | Source | Product-Safe? | Basis |
|---|---|---|---|---|
| 1 | NASA AS08-14-2383 "Earthrise" | NASA | ✅ SAFE | § 105; NC-NASA-002 confirmed |
| 2 | Thomas Moran *Grand Canyon of the Yellowstone* | Smithsonian | ❌ DEFERRED | No DD — DD-SMITHSONIAN-001 not drafted |
| 3 | NASA Grand Prismatic Thermal Mosaic | NASA | ✅ SAFE | § 105; NC-NASA-026 |
| 4 | Ernst Haeckel *Hexacoralla* | BHL | ✅ SAFE | Pre-1928 PD (Haeckel d. 1919) |
| 5 | Canaletto *The Grand Canal* | Museo Correr | ❌ DEFERRED | No DD — Museo Correr not in institution registry |
| 6 | John Gould *Darwin's Finches* | BHL | ✅ SAFE | Pre-1928 PD (Gould d. 1881) |
| 7 | USGS Grand Canyon Strata Cross-Section | NARA (USGS/RG 57) | ✅ SAFE | § 105; `useRestriction.status == "Unrestricted"` |
| 8 | NOAA Papahānaumokuākea Bathymetry | NOAA | ✅ SAFE | § 105; SA-NOAA-001 gate confirmed |
| 9 | Hayden Expedition Geological Map 1871 | NARA (War Dept.) | ✅ SAFE | § 105; `useRestriction.status == "Unrestricted"` |
| 10 | HMS Beagle Galápagos Chart | UKHO | ❌ DEFERRED | § 105 inapplicable (UK Crown copyright) |

**Playbook Product Opportunities — Product Safety Ruling:**

| # | Playbook Product | Product-Safe? | Route |
|---|---|---|---|
| 1 | Earthrise: The Master Print | ✅ SAFE | `museum_print` → `museum_giclée` |
| 2 | The Moran Collection | ❌ DEFERRED | Smithsonian DD required |
| 3 | Haeckel's Marine Masterpieces | ✅ SAFE | `museum_print` → `archival_print` |
| 4 | The Strata Series | ✅ SAFE | `wall_art` → `map_print` / `print_premium` |
| 5 | The Canaletto Folio | ❌ DEFERRED | Museo Correr DD required |
| 6 | The Darwin Finches Portfolio | ✅ SAFE | `wall_art` → `print_premium` |
| 7 | Midway Archival Maps | ✅ SAFE (conditional) | NARA § 105; Sprint 1 `naId` confirmation required |
| 8 | Hayden 1871 Portfolio | ✅ SAFE (conditional) | NARA § 105; Sprint 1 `naId` confirmation required |
| 9 | Venetian Architectural Elevations | ❌ DEFERRED | Unidentified source (St. Mark's / Doge's Palace) |
| 10 | Landsat "Satellite Art" Prints | ✅ SAFE | `wall_art` → `framed`; NC-NASA-029 |

**Summary:** 7 of 10 Playbook Product Opportunities are product-safe. 3 are permanently deferred until institution DDs are ratified. The first commercial wave can proceed without any deferred assets.

---

## II. Product Catalogs

### II.1 Product-Safe Launch Catalog

Sixteen assets confirmed product-safe per NC-PILOT-001-FRR. Each asset maps to one or more eligible product lines per NC-PRODUCT-001.

| Asset ID | Asset Name | Source | Rights Basis | Place | Eligible Lines | CSM Tier |
|---|---|---|---|---|---|---|
| NC-NASA-002 | AS08-14-2383 Earthrise | NASA | § 105 | Earthrise | 1, 2, 3, 4, 8, 11, 14, 20 | MASTERWORK |
| NC-NASA-026 | Yellowstone from Orbit (Grand Prismatic) | NASA | § 105 | Yellowstone | 2, 3, 4, 8, 11, 14 | FLAGSHIP |
| NARA-HAYDEN-1871 | Hayden Survey Map 1871 | NARA (RG 57) | § 105 | Yellowstone | 5, 7, 8, 13 | FLAGSHIP |
| BHL-BISON-001 | *Bison bison* natural history illustration | BHL | Pre-1928 PD | Yellowstone | 2, 3, 8, 9, 10, 14, 15 | STANDARD |
| NARA-POWELL-1869 | Powell Expedition Photo 1869 | NARA (RG 57) | § 105 | Grand Canyon | 2, 3, 8, 9, 10, 11 | STANDARD |
| NARA-USGS-GC | USGS Grand Canyon Strata Cross-Section | NARA (RG 57) | § 105 | Grand Canyon | 5, 9, 10, 11, 13 | FLAGSHIP |
| BHL-CONDOR-001 | California Condor illustration | BHL | Pre-1928 PD | Grand Canyon | 2, 3, 9, 10, 14, 15 | STANDARD |
| BHL-HAECKEL-HC | Haeckel *Hexacoralla* | BHL | Pre-1928 PD (d. 1919) | Great Barrier Reef | 1, 6, 8, 9, 10, 11, 13 | MASTERWORK |
| NC-NASA-029 | GBR Whitsundays Landsat | NASA | § 105 | Great Barrier Reef | 2, 3, 4, 8, 14 | STANDARD |
| BHL-CHELONIA-001 | *Chelonia mydas* illustration | BHL | Pre-1928 PD | Great Barrier Reef | 2, 3, 9, 10, 15 | STANDARD |
| BHL-ALBATROSS-001 | Laysan Albatross illustration | BHL | Pre-1928 PD | Papahānaumokuākea | 2, 3, 9, 10, 14, 15 | STANDARD |
| NARA-MIDWAY-MAP | Battle of Midway Chart | NARA | § 105 | Papahānaumokuākea | 5, 8, 11 | STANDARD |
| NOAA-PAPAHANAUMOKUAKEA-BATHY | Papahānaumokuākea Bathymetric Map | NOAA | § 105 | Papahānaumokuākea | 5, 8, 11 | STANDARD |
| BHL-GOULD-FINCHES | Gould *Darwin's Finches* (1837) | BHL | Pre-1928 PD (d. 1881) | Galápagos | 1, 2, 6, 8, 9, 10, 11, 13 | FLAGSHIP |
| BHL-CHELONOIDIS-001 | *Chelonoidis niger* illustration | BHL | Pre-1928 PD | Galápagos | 2, 3, 9, 10, 15 | STANDARD |
| BHL-MONACHUS-001 | *Monachus schauinslandi* illustration | BHL | Pre-1928 PD | Galápagos | 2, 3, 9, 10, 15 | STANDARD |

**Product line number key (NC-PRODUCT-001 Article 1):**
1=museum_print · 2=framed_print · 3=poster · 4=canvas · 5=map_print · 6=archival_collection · 7=place_portfolio · 8=digital_download · 9=pdf_guide · 10=education_pack · 11=tourism_guide · 12=conservation_pack · 13=coffee_table_book · 14=calendar · 15=postcard_card · 16=sticker · 19=notebook

**Conditional flags:**
- NARA assets (NARA-HAYDEN-1871, NARA-POWELL-1869, NARA-USGS-GC, NARA-MIDWAY-MAP): Sprint 1 `naId` confirmation and `useRestriction.status == "Unrestricted"` per-record verification required before Gate 8
- NOAA-PAPAHANAUMOKUAKEA-BATHY: Flickr `license` field confirmation ∈ `{7, 8, 9, 10}` required; Sprint 3 NOAA write cap applies (7 total NOAA writes; currently 0 used)
- Papahānaumokuākea assets (all 3): Gate 8 blocked until GeoNames ID confirmed and written to `places` table

### II.2 Product-Risk Catalog

Nine assets from the NC-PILOT-001 Experience Blueprint were deferred at FRR. Three additional assets appear in the Launch Playbook but are not in the FRR inventory.

**Deferred assets — reinstatement path:**

| Asset | Source | Deferred reason | Reinstatement path |
|---|---|---|---|
| Thomas Moran *Grand Canyon of the Yellowstone* | Smithsonian | No institution DD | DD-SMITHSONIAN-001 + ratification |
| Thomas Moran *Cliffs of the Rio Virgin, Zion* | Smithsonian | No institution DD | DD-SMITHSONIAN-001 + ratification |
| HMS Beagle Galápagos Chart | UKHO | § 105 inapplicable; no UK Crown copyright DD | DD-TNA-001 or DD-UKHO-001 |
| Canaletto *The Grand Canal* | Museo Correr | No institution DD | DD-MUSEOCORRER-001 (new) |
| de' Barbari Venice Map (c. 1500) | Museo Correr | No institution DD | DD-MUSEOKORRER-001 (new) |
| St. Mark's architectural elevation | Unidentified | Source not identified; no institution DD | Source identification + DD |
| ESA/Copernicus asset #20 | ESA | Mislabeled as "NASA/ESA"; § 105 inapplicable to ESA | DD-ESA-001 |
| HMS Beagle Darwin sketch | Cambridge University Library | No institution DD | DD-CAMBRIDGEUL-001 (new) |
| Cook's Voyage chart | UK archives | § 105 inapplicable | DD-TNA-001 |

**High-priority reinstatement (commercial impact):**
- **DD-SMITHSONIAN-001** is the highest-priority open DD. Ratification unblocks the Moran paintings — the single strongest commercial asset for Yellowstone and the hero of the Launch Playbook's "Artist's Trail" journey. Without Moran, the Yellowstone commercial tier is limited to NASA satellite prints and NARA maps.
- **DD-MET-001 ratification** (Venice): the Met's Japan pilot unblocks Venice upon ratification of any museum DD. Venice is the only place with zero products.
- **DD-TNA-001/DD-UKHO-001** (Cook/Beagle charts): unlocks Galápagos nautical heritage tier and the HMS Beagle asset from the Playbook.

**Conditional assets — at risk but product-safe pending confirmation:**

| Asset | Risk | Condition |
|---|---|---|
| NARA-HAYDEN-1871 | `naId` not yet confirmed; Unrestricted status not verified per record | Sprint 1 API lookup required |
| NARA-POWELL-1869 | Same | Sprint 1 API lookup required |
| NARA-USGS-GC | Same | Sprint 1 API lookup required |
| NARA-MIDWAY-MAP | Same | Sprint 1 API lookup required |
| NOAA-PAPAHANAUMOKUAKEA-BATHY | Flickr `license` field not yet confirmed | SA-NOAA-001 gate check at Sprint 3 write |

---

## III. First 10 Commercial Products

These are the specific, named, shippable products authorized for the first commercial activation wave. Order reflects the phased launch sequence from NC-PILOT-001-LA Article 1. Each entry specifies all governance metadata required for Gate 7 (curator) and Gate 8 (two-human activation).

---

### Product 001 — "Earthrise" Museum Giclée Print

| Field | Value |
|---|---|
| Product name | *Earthrise* — Museum Giclée Print |
| SKU anchor | NC-PROD-001 |
| Source asset | NC-NASA-002 (AS08-14-2383) |
| Routing family | `museum_print` → `museum_giclée` |
| Rights basis | 17 U.S.C. § 105 — US federal government work |
| Rights class | § 105 |
| CSM tier | MASTERWORK |
| Commerce tier | tier_1 |
| Place anchor | Earthrise (S-3 exemption — no GeoNames ID) |
| GeoNames attribution | NOT required (S-3 cosmic anchor exception) |
| OSM attribution | NOT required (no map tiles on Earthrise page) |
| NASA nonendorsement | `Image credit: NASA. NASA does not endorse this product.` — required on product listing, print label, COA |
| Quality threshold | Minimum 6000px long edge / 300 DPI at 20"×24" — NASA original exceeds this |
| Curator required | ☑ YES — `museum_print` curator always required + MASTERWORK tier |
| PA sign-off | ☑ YES — MASTERWORK + first commercial activation |
| Manual review type | Curator rights review + PA activation sign-off |
| Gate E | Required — two-human: Rights Verifier + Principal Architect |
| Attribution stack | NASA nonendorsement only |
| Launch phase | Phase 1 — first activation |

---

### Product 002 — "Yellowstone from Orbit" Framed Print

| Field | Value |
|---|---|
| Product name | *Yellowstone from Orbit* — Framed Archival Print |
| SKU anchor | NC-PROD-002 |
| Source asset | NC-NASA-026 (Grand Prismatic Spring thermal mosaic) |
| Routing family | `wall_art` → `framed` |
| Rights basis | 17 U.S.C. § 105 |
| CSM tier | FLAGSHIP |
| Commerce tier | tier_1 |
| Place anchor | Yellowstone NP — GeoNames 5843642 / Q351 |
| GeoNames attribution | `Geographic data © GeoNames (geonames.org) — CC BY 4.0` on product listing |
| OSM attribution | `© OpenStreetMap contributors` on map tile display |
| NASA nonendorsement | Required — product listing and print label |
| Quality threshold | Minimum 3600px / 300 DPI at 12"×16" |
| Curator required | ☐ NO (standard routing; FLAGSHIP but not MASTERWORK) |
| Gate E | Required — standard two-human |
| Attribution stack | NASA nonendorsement → GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 2 |

---

### Product 003 — "Hayden Survey 1871" Map Print

| Field | Value |
|---|---|
| Product name | *Hayden Survey 1871* — Archival Map Print |
| SKU anchor | NC-PROD-003 |
| Source asset | NARA-HAYDEN-1871 (RG 57, USGS; `naId` TBC Sprint 1) |
| Routing family | `wall_art` → `map_print` |
| Rights basis | 17 U.S.C. § 105 — US federal government work |
| Rights class | § 105 / Rights Class 9 |
| CSM tier | FLAGSHIP (Historic Maps Tier 1 — CI v1.2) |
| Commerce tier | tier_1 |
| Place anchor | Yellowstone NP — GeoNames 5843642 / Q351 |
| GeoNames attribution | Required on product listing |
| OSM attribution | Required if map tile display on listing page |
| NARA credit | `Image from the National Archives (Record Group 57, Catalog ID [naId])` |
| Quality threshold | Minimum 4000px / 200 DPI at 20"×24" — NARA originals typically exceed this |
| Curator required | ☐ NO (map_print at FLAGSHIP, not MASTERWORK) |
| Conditional gate | Sprint 1 `naId` confirmed + `useRestriction.status == "Unrestricted"` per record verified before Gate 8 |
| Gate E | Required |
| Attribution stack | NARA credit → GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 2 |

---

### Product 004 — "Grand Canyon Strata" Geological Print

| Field | Value |
|---|---|
| Product name | *Grand Canyon Strata Series* — Geological Cross-Section Print |
| SKU anchor | NC-PROD-004 |
| Source asset | NARA-USGS-GC (RG 57; `naId` TBC Sprint 1) |
| Routing family | `wall_art` → `print_premium` |
| Rights basis | 17 U.S.C. § 105 |
| CSM tier | FLAGSHIP |
| Commerce tier | tier_1 |
| Place anchor | Grand Canyon NP — GeoNames 5296401 / Q220289 |
| GeoNames attribution | Required on product listing |
| OSM attribution | Required if map tile display |
| NARA credit | Required — RG 57 + `naId` |
| Quality threshold | Minimum 3600px / 300 DPI |
| Curator required | ☐ NO |
| Conditional gate | Sprint 1 `naId` + Unrestricted confirmation |
| Attribution stack | NARA credit → GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 2 |

---

### Product 005 — "Darwin's Finches" Archival Portfolio Print

| Field | Value |
|---|---|
| Product name | *Darwin's Finches Portfolio* — Gould 1837 Archival Print |
| SKU anchor | NC-PROD-005 |
| Source asset | BHL-GOULD-FINCHES (Gould, *Zoology of the Voyage of H.M.S. Beagle*, 1841) |
| Routing family | `wall_art` → `print_premium` |
| Rights basis | Pre-1928 PD (Gould d. 1881; published 1841) |
| CSM tier | FLAGSHIP |
| Commerce tier | tier_1 |
| Place anchor | Galápagos Islands — GeoNames 3658931 / Q38095 |
| GeoNames attribution | Required on product listing |
| OSM attribution | Required if map tile display |
| Institutional credit | BHL — no attribution requirement (pre-1928 PD) |
| Quality threshold | Minimum 3600px / 300 DPI — BHL scan quality to be confirmed per record |
| Curator required | ☐ NO |
| Gate E | Required |
| Attribution stack | GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 3 |

---

### Product 006 — "Haeckel Hexacoralla" Archival Print

| Field | Value |
|---|---|
| Product name | *Haeckel's Marine Masterpieces: Hexacoralla* — Archival Print |
| SKU anchor | NC-PROD-006 |
| Source asset | BHL-HAECKEL-HC (*Kunstformen der Natur*, 1904) |
| Routing family | `museum_print` → `archival_print` |
| Rights basis | Pre-1928 PD (Haeckel d. 1919; published 1899–1904) |
| CSM tier | MASTERWORK |
| Commerce tier | tier_1 |
| Place anchor | Great Barrier Reef — GeoNames 2164628 / Q7343 |
| GeoNames attribution | Required on product listing |
| OSM attribution | Required if map tile display |
| Quality threshold | Minimum 6000px / 300 DPI at 20"×24" — BHL *Kunstformen* scans typically high-resolution |
| Curator required | ☑ YES — `museum_print` curator always required + MASTERWORK |
| PA sign-off | ☑ YES |
| Manual review type | Curator rights review + PA activation sign-off |
| Gate E | Required — two-human |
| Attribution stack | GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 4 |

---

### Product 007 — "GBR Whitsundays" Satellite Framed Print

| Field | Value |
|---|---|
| Product name | *Great Barrier Reef: Whitsundays from Space* — NASA Landsat Framed Print |
| SKU anchor | NC-PROD-007 |
| Source asset | NC-NASA-029 |
| Routing family | `wall_art` → `framed` |
| Rights basis | 17 U.S.C. § 105 |
| CSM tier | STANDARD |
| Commerce tier | tier_2 |
| Place anchor | Great Barrier Reef — GeoNames 2164628 / Q7343 |
| GeoNames attribution | Required on product listing |
| OSM attribution | Required if map tile display |
| NASA nonendorsement | Required — product listing and print label |
| Quality threshold | Minimum 3600px / 300 DPI |
| Curator required | ☐ NO |
| Gate E | Required |
| Attribution stack | NASA nonendorsement → GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 4 |

---

### Product 008 — "Earthrise" Digital Download

| Field | Value |
|---|---|
| Product name | *Earthrise* — High-Resolution Digital Download |
| SKU anchor | NC-PROD-008 |
| Source asset | NC-NASA-002 |
| Routing family | `institutional_license` → `digital_license` |
| Rights basis | 17 U.S.C. § 105 |
| CSM tier | MASTERWORK |
| Commerce tier | tier_1 |
| Place anchor | Earthrise (S-3 exemption) |
| GeoNames attribution | NOT required (cosmic anchor exemption) |
| OSM attribution | NOT required |
| NASA nonendorsement | Required in download package metadata |
| In-package metadata | `nc:nasa_attribution`, `nc:rights_basis`, `nc:rights_statement_uri`, consumer use rights notice |
| Quality threshold | Minimum 3000px / 300 DPI |
| Curator required | ☑ YES — `institutional_license` curator always required |
| Gate E | Required — two-human |
| Attribution stack | NASA nonendorsement only |
| Launch phase | Phase 1 (concurrent with Product 001 or immediate follow-on) |

---

### Product 009 — "Galápagos Discovery" Education Pack

| Field | Value |
|---|---|
| Product name | *Galápagos: Darwin's Living Laboratory* — Educational Lesson Pack |
| SKU anchor | NC-PROD-009 |
| Source assets | BHL-GOULD-FINCHES + BHL-CHELONOIDIS-001 + BHL-MONACHUS-001 |
| Routing family | `educational` → `classroom_poster` + `reference_sheet` |
| Rights basis | Pre-1928 PD (all BHL assets; Gould d. 1881) |
| CSM tier | REFERENCE (educational floor) |
| Commerce tier | tier_3 |
| Place anchor | Galápagos Islands — GeoNames 3658931 / Q38095 |
| GeoNames attribution | Required in PDF document credits section |
| OSM attribution | Required if document includes map imagery |
| Quality threshold | Minimum 1200px / 150 DPI body illustrations |
| Curator required | ☐ NO |
| Gate E | Required |
| Multi-asset note | Each of the 3 source assets must individually clear IFC-1 before pack activation |
| Attribution stack | GeoNames CC BY 4.0 → OSM ODbL (in-document) |
| Launch phase | Phase 3 |

---

### Product 010 — "Yellowstone Wildlife" Wall Calendar

| Field | Value |
|---|---|
| Product name | *Yellowstone Wildlife* — 12-Month Wall Calendar |
| SKU anchor | NC-PROD-010 |
| Source assets | BHL-BISON-001 + NC-NASA-026 (mixed: BHL + NASA) |
| Routing family | `calendar` → `wall_calendar` |
| Rights basis | Pre-1928 PD (Bison bison, BHL) + 17 U.S.C. § 105 (NC-NASA-026) |
| CSM tier | STANDARD |
| Commerce tier | tier_2 |
| Place anchor | Yellowstone NP — GeoNames 5843642 / Q351 |
| GeoNames attribution | Required on product listing (calendar is physical; digital listing requires it) |
| OSM attribution | Required if listing page shows map tiles |
| NASA nonendorsement | Required for NASA-sourced months (NC-NASA-026 pages) — individual month captions |
| Quality threshold | Minimum 2400px / 200 DPI at 11"×8.5" per month panel |
| Curator required | ☐ NO |
| Mixed-source note | NASA nonendorsement applies only to calendar months using NASA-sourced images; BHL months do not require NASA text |
| Gate E | Required |
| Attribution stack | NASA nonendorsement (NASA months) → GeoNames CC BY 4.0 → OSM ODbL |
| Launch phase | Phase 2 |

---

## IV. Products Requiring Manual Review

### IV.1 Curator-Always-Required Products

The following products require curator review as a constitutional condition (NC-PRODUCT-001 Article 11, Gate 7), regardless of routing score.

| Product | Asset | Review type | Reviewer requirement | Blocking condition |
|---|---|---|---|---|
| NC-PROD-001 Earthrise Museum Giclée | NC-NASA-002 | Curator rights review + COA preparation | Curator + Principal Architect (separate persons) | MASTERWORK tier + `museum_print` family |
| NC-PROD-006 Haeckel Archival Print | BHL-HAECKEL-HC | Curator rights review + COA preparation | Curator + Principal Architect | MASTERWORK tier + `museum_print` family |
| NC-PROD-008 Earthrise Digital Download | NC-NASA-002 | Curator review | Curator | `institutional_license` family always requires curator |
| Any premium collector bundle (line 20) | Multiple | Curator bundle review + COA per plate | Curator + Principal Architect | NC-PRODUCT-001 Art. 17(20) |

### IV.2 MASTERWORK Tier — All Routing Paths

Any asset with `csm_tier = 'MASTERWORK'` requires curator review regardless of product family (NC-PRODUCT-001 Article 11, Gate 7, condition 2). Current MASTERWORK assets:
- NC-NASA-002 (Earthrise)
- BHL-HAECKEL-HC (Haeckel *Hexacoralla*)

### IV.3 NARA Assets — Sprint 1 Verification Required

All four NARA assets in the product-safe catalog require human rights verification at the record level before Gate 8:

| Asset | Required verification | Verifier | Blocking? |
|---|---|---|---|
| NARA-HAYDEN-1871 | `naId` confirmed; `useRestriction.status == "Unrestricted"` confirmed via API | Rights Verifier | ☑ Gates 1–8 blocked until confirmed |
| NARA-POWELL-1869 | Same | Rights Verifier | ☑ Same |
| NARA-USGS-GC | Same | Rights Verifier | ☑ Same |
| NARA-MIDWAY-MAP | Same | Rights Verifier | ☑ Same |

Review type: Sprint 1 API lookup with record-level rights confirmation. Reviewer writes `media_rights.human_verified = TRUE` and `rights_status = "pending_verification"` → human upgrade path per SA-22 (pending ratification).

### IV.4 NOAA Asset — Sprint 3 Gate Check

| Asset | Required verification | Cap status |
|---|---|---|
| NOAA-PAPAHANAUMOKUAKEA-BATHY | Flickr `license` field confirmed ∈ `{7, 8, 9, 10}` per SA-NOAA-001; `credit_line` field scanned for personal names | Sprint 3 cap: 0 of 7 NOAA writes used; this asset = write #1 |

### IV.5 Papahānaumokuākea Gate E Block

All three Papahānaumokuākea products (Laysan Albatross, Battle of Midway Map, NOAA Bathymetric Map) are blocked at Gate 8 until the GeoNames ID is confirmed. All other gates (1–7) may be completed in advance.

**Action required:** Run the following against NC's GeoNames application account (not the demo account):
```
curl "https://secure.geonames.org/searchJSON?q=Papahanaumokuakea&country=US&username=<NC_GEONAMES_ACCOUNT>"
```
Write confirmed ID to `places.geonames_id` and set `places.s3_status = 'confirmed'` before Gate 8 for any Papahānaumokuākea product.

---

## V. Commerce Authorization

### V.1 Authorization

**NC-COMMERCE-001 COMMERCE AUTHORIZED WITH CONDITIONS.**

The first wave of NC commercial products is authorized to proceed. The 16 confirmed product-safe assets are cleared for commercial activation through the 8-gate sequence defined in NC-PRODUCT-001. The first 10 commercial products defined in §III are authorized for routing, curator review, and Gate E activation in the launch phase sequence indicated.

### V.2 Phase Activation Sequence

| Phase | Products | Activation condition |
|---|---|---|
| Phase 1 — Earthrise | NC-PROD-001, NC-PROD-008 | SA-GEONAMES-001 and SA-OSM-001 not required (Earthrise exempt). Only NASA nonendorsement and IFC-1 required. Gate E immediately activable. |
| Phase 2 — Yellowstone + Grand Canyon | NC-PROD-002, NC-PROD-003, NC-PROD-004, NC-PROD-010 | SA-GEONAMES-001 ratified. NARA Sprint 1 `naId` verification complete. GeoNames ID 5843642 (Yellowstone) and 5296401 (Grand Canyon) written to `places` table. |
| Phase 3 — Galápagos | NC-PROD-005, NC-PROD-009 | SA-GEONAMES-001 ratified. GeoNames ID 3658931 (Galápagos) written to `places` table. BHL scan quality confirmed. |
| Phase 4 — Great Barrier Reef | NC-PROD-006, NC-PROD-007 | SA-GEONAMES-001 ratified. GeoNames ID 2164628 (GBR) written to `places` table. Haeckel BHL scan resolution confirmed. NOAA Sprint 3 gate check complete. |
| Phase 5 — Papahānaumokuākea | Future products | GeoNames ID for Papahānaumokuākea confirmed and written. All 3 assets cleared through Gate 7. |
| Phase 6 — Venice (no products yet) | Future products | Triggered by first art museum DD ratification (DD-MET-001 or DD-AIC-001). |

### V.3 Blocking Conditions (must clear before public launch)

| Condition | Authority | Blocking phase(s) |
|---|---|---|
| SA-GEONAMES-001 ratified | NC-PILOT-001-LA Art. 3 | Phases 2–6 (all geo-anchored products) |
| SA-OSM-001 ratified | NC-PILOT-001-LA Art. 3 | All phases with map tile display |
| NARA Sprint 1 `naId` verification complete | DD-NARA-001 Art. 12; NC-PRODUCT-001 Gate 6 | Phases 2 (Products 003, 004), 5 (NARA-MIDWAY-MAP) |
| GeoNames IDs written to `places` table | S-3 Invariant; NC-PILOT-001-LA §C | Per-place |
| Papahānaumokuākea GeoNames ID confirmed | NC-PILOT-001-LA Art. 6 | Phase 5 |
| Gate E two-human sign-off | IFC v1; NC-PILOT-001-LA Art. 2 | Per product activation |

### V.4 Non-Blocking Advisory Items

The following are required for full catalog operations but do not block the first 10 products:

| Advisory | Impact if delayed |
|---|---|
| DD-SMITHSONIAN-001 not drafted | Moran paintings (Yellowstone hero assets) remain deferred indefinitely |
| SA-WIKIDATA-001 not ratified | Wikidata identity writes not governed at catalog scale; acceptable for pilot |
| SA-9 overdue | Bulk adapter rights classification not extended to nara, mia, noaa slugs; manual Sprint 1 path covers the pilot |
| DD-MET-001 ratification | Venice remains at 0 products; no timeline pressure |
| DD-OVERTURE-001 not commissioned | OSM tile-only constraint on boundary geometry; acceptable for pilot scope |

### V.5 Post-Activation Obligations

1. **T+30 commerce review:** First 10 products must be audited for attribution compliance — 100% of product listings verified for NASA nonendorsement text, GeoNames attribution, and consumer use rights notice.
2. **NOAA write count tracking:** Operations must maintain a running count of NOAA writes in Sprint 3. Current count: 0. Cap: 7. Each NOAA-sourced product activation = 1 write. Do not activate more than 7 NOAA products without Sprint 4 authorization.
3. **Earthrise 60-day deadline:** Standards Constitution amendment or proxy-place GeoNames ID resolution must be completed within 60 days of NC-PROD-001 activation. Failure requires Earthrise demotion from place page to standalone product page.
4. **NARA tier upgrade request:** Submit tier upgrade request to Catalog_API@nara.gov before Sprint 2 begins (DD-NARA-001 Art. 8). The AWS S3 bulk snapshot path must be evaluated as the primary harvest path for catalog scale.
5. **DD-SMITHSONIAN-001 priority:** The Moran Collection is the highest commercial-impact blocked product. Initiating DD-SMITHSONIAN-001 immediately after the Phase 2 launch is the fastest path to unlocking Yellowstone's hero product tier.

### V.6 Decision Articles

**Article 1 — Commerce Authorization.** The NC commercial product pipeline is authorized to activate. The 16 confirmed product-safe assets defined in §II.1 may proceed through the 8-gate activation sequence in NC-PRODUCT-001. The first 10 products defined in §III are the authorized first activation wave.

**Article 2 — Earthrise First.** NC-PROD-001 (*Earthrise* Museum Giclée) and NC-PROD-008 (*Earthrise* Digital Download) are the first authorized commercial activations. They have the cleanest rights path (§ 105 only), the highest CSM tier (MASTERWORK), and no GeoNames or OSM dependency. Phase 1 may begin immediately upon Gate E confirmation.

**Article 3 — Deferred Assets Remain Deferred.** The 9 deferred assets from NC-PILOT-001-FRR Article 5 are not reinstated by this authorization. The 3 Playbook assets flagged as deferred in §I.3 (Moran, Canaletto, HMS Beagle) are also not reinstated. No deferred asset may enter any pipeline stage without a formal Principal Architect reinstatement event following DD ratification.

**Article 4 — NARA Manual Path.** Pending SA-22/SA-23 ratification, NARA assets enter the catalog via a Sprint 1 manual verification path: API record lookup, rights field confirmation, human_verified = TRUE set by Rights Verifier. This path is authorized for the 4 NARA pilot assets. Bulk NARA ingestion requires SA-22/SA-23 ratification.

**Article 5 — NOAA Write Cap is Operational.** The NOAA Sprint 3 write cap (7 writes) is an operational constraint that must be tracked by the operations team, not encoded as a DB constraint. The 1 NOAA product in the first 10 (NOAA Bathymetric Map, Papahānaumokuākea) uses write #1. No further NOAA products may activate without explicit Sprint 4 authorization once the cap is reached.

**Article 6 — Venice Patience Holds.** Venice has zero products at launch. No commerce authorization exists for Venice until at least one art museum DD is ratified. Venice place page (editorial) may activate independently on the standard GA timeline.

**Article 7 — DD-SMITHSONIAN-001 is the Highest-Priority Unblocking Action.** The Moran Collection is the Playbook's strongest commercial product. It is blocked entirely by the absence of DD-SMITHSONIAN-001. This DD should be commissioned as the next governance sprint after Phase 2 launch.

**Article 8 — Zero Tolerance Cascade Applies.** A single confirmed federal endorsement violation in any product copy, listing, or marketing material triggers immediate deactivation of all federal-sourced products (NASA, NOAA, NARA separately per agency). This cascade is unconditional per NC-PILOT-001-LA Article 8. Copy review (NC-PILOT-001-LA §F) must be completed for all 10 products before Gate E.

---

## VI. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Commerce Authorization Review | ☑ AUTHORIZED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-COMMERCE-001 — drafted 2026-06-11*
*Reviews: NC-PRODUCT-001 · NC-PILOT-001-LA · NC-PILOT-001 Launch Playbook*
*Authorizes: 16-asset product-safe catalog · First 10 commercial products · Phase 1–4 activation sequence*
