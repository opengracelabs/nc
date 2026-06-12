# NC-WEB-001: Website Launch Authorization

| Field | Value |
|---|---|
| Document | NC-WEB-001-LA |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | NC-WEB-001 Blueprint · NC-FIRST-SALE Authorization · NC-FIRST-SALE-VERIFY · NC-COMMERCE-001 · NC-PRODUCT-001 · SA-GEONAMES-001 · SA-OSM-001 |
| **Decision** | **PHASE 0 CONDITIONALLY AUTHORIZED — GATE E CURRENTLY INVALID** |

---

## Summary Decision

| Phase | Status | Blocking condition |
|---|---|---|
| Phase 0 (Earthrise + static pages) | **AUTHORIZED WITH CONDITIONS** | 3 blocking corrections required before Gate E re-confirmation |
| Phase 1 (Yellowstone, Grand Canyon, Places Index) | **BLOCKED** | SA-GEONAMES-001 and SA-OSM-001 not ratified |
| Phase 2 (GBR, Galápagos) | **BLOCKED** | Phase 1 prerequisites + NOAA Sprint 3 gate |
| Phase 3 (Collector Edition, Calendar) | **BLOCKED** | NARA Sprint 1 unconfirmed |
| Phase 4 (Papahānaumokuākea) | **BLOCKED** | GeoNames ID unconfirmed (Wikidata P1566 absent) |
| Phase 5 (Venice) | **BLOCKED** | No art museum DD ratified |

---

## I. Document Review Findings

### I.1 NC-WEB-001 Blueprint

**Status: APPROVED — serves as the governance foundation for this authorization.**

The Blueprint correctly synthesizes NC-PILOT-001-FRR, NC-COMMERCE-001, NC-FIRST-SALE, NC-PRODUCT-001, SA-GEONAMES-001, and SA-OSM-001 into a coherent 10-page specification. Attribution matrix (§III), copy rules (§IV), wireframe zones (§V), funnel architecture (§VI), launch phasing (§VII), and prohibited content registry (§VIII) are all correctly derived from the reference models. No conflicts found. Blueprint is adopted as the governing reference for this authorization.

**One gap to note:** NC-WEB-001 Blueprint §I asserts four invariants (IFC-1, GN-6, OS-6, federal nonendorsement). These are correctly stated. However, the blueprint does not specify which production file is the authoritative source for Earthrise copy. This authorization resolves that question in §IV below.

---

### I.2 NC-WEB-001 Technical Plan

**Status: NOT FOUND — document does not exist under this designation.**

No document titled "NC-WEB-001 Technical Plan" exists in the repository. The following predecessor documents address parts of the technical scope:

- `docs/architecture/wireframe_specifications.md` — contains domain architecture (`natureandculture.net` / `natureandculture.shop`), multilingual rules, shared page shell spec, and commerce routing. **Governance conflict:** this document references "Neo4j projection" — Neo4j is excluded from the NC stack under the Strategic Direction v1 frozen stack clause and Wireframe Constitution v1. This reference must be removed before this document is used as a technical authority for Phase 0 build.
- `docs/ux/multilingual_wireframe_requirements.md` — multilingual IA rules.

**Ruling:** The absence of a formal NC-WEB-001 Technical Plan does not block Phase 0 launch. Phase 0 pages (Home, Earthrise Product, Earthrise Story, About, Products) require no map tile integration, no GeoNames API calls, and no place-data rendering. The technical complexity gating SA-GEONAMES-001 and SA-OSM-001 only applies to Phase 1+ place pages. Phase 0 can proceed without a ratified Technical Plan. **A Technical Plan must be drafted and ratified before Phase 1 build begins.** See §VII.

---

### I.3 NC-WEB-001 Wireframe + Creative Direction

**Status: NOT FOUND as a formal NC-WEB-001 document — predecessor documents reviewed.**

No document titled "NC-WEB-001 Wireframe + Creative Direction" exists. The following predecessor documents address the creative scope:

- `docs/architecture/nature_culture_experience_wireframe_v1.md` — full UX and emotional design direction. Establishes: Baskerville serif / SF Pro utility; media-first (70/20/10); parallax reveal; dynamic luminescence by place mood. References Yosemite, Machu Picchu, Kyoto — places not in the NC pilot. This document is a creative vision spec, not a pilot-scope wireframe.
- `docs/architecture/nature_culture_wireframe_system_v1.md` — additional wireframe system reference.
- NC-WEB-001 Blueprint §V — zone-level wireframe specs for all 10 pilot pages. This is the authoritative wireframe spec for Phase 0.

**Governance conflict in experience wireframe:** The document references "Saville-Kent lithograph" and verification badges for "UNESCO, Smithsonian" — Smithsonian has no ratified DD (DD-SMITHSONIAN-001 is the highest-priority pending action). Smithsonian verification badges must not appear on Phase 0 pages. UNESCO badges may appear as place designation labels (e.g., "UNESCO World Heritage Site") but not as endorsement or verification claims.

**Ruling:** NC-WEB-001 Blueprint §V serves as the operative wireframe specification for Phase 0. The experience wireframe is adopted as creative direction for visual language (typography, spacing, parallax, luminescence) only — not for content inventory. A dedicated NC-WEB-001 Wireframe + Creative Direction document should be drafted and ratified before Phase 1 build.

---

### I.4 NC-FIRST-SALE Correction Reports

**Status: BLOCKED — critical violation found in the "Approved" production file.**

This is the most consequential finding in this review.

Four documents were reviewed:

| Document | Finding |
|---|---|
| `NC-FIRST-SALE_correction_report.md` | Reports corrections implemented, 24 tests passed |
| `NC-FIRST-SALE_correction_verification.md` | **FIRST SALE BLOCKED — 0 of 4 corrections applied** (verified 2026-06-11) |
| `NC-FIRST-SALE_verification.md` | **FIRST SALE BLOCKED — 3 blocking violations** (earlier review) |
| `NC-FIRST-SALE_activation_report.md` | Gate E metadata present, but activation is premature per NC-FIRST-SALE Authorization Art. 2 |

**The conflict:** Two files purport to be the production Earthrise copy:

1. `docs/implementation/nc_first_sale_campaign_package.md` — **CORRECTED.** NARA violations removed. Nonendorsement present on product page and social. This is the file the correction_report.md tests validate.

2. `docs/implementation/nc_first_sale_final_conversion_package_v2.md` — **VIOLATIONS REMAIN.** Titled "Approved for Final Release" (dated 2026-06-11). Contains four FS-001/FS-002 violations confirmed by direct review:

| Surface | Violation | Line |
|---|---|---|
| Product page Intelligence Stack | `"Archival Origin: Sourced from the National Archives and Records Administration (NARA)."` | 24 |
| Launch email body | `"working with the original archival records from NASA and the National Archives"` | 52 |
| Social caption | `"Sourced from the National Archives. Verified by NASA."` | 73 |
| COA body | `"Source Archive: National Archives and Records Administration (NARA)"` | 100 |

**The v2 package is labeled "Approved for Final Release" but is not approved.** It was partially corrected (nonendorsement added to product page footer and email footer, and image credit partially present) but the four core FS-001 violations were not resolved.

**Gate E validity:** The NC-FIRST-SALE Activation Report records Gate E metadata and `activation_state: activated` for both NC-PROD-001 and NC-PROD-008. Per NC-FIRST-SALE Authorization Art. 2: *"The curator and Principal Architect must confirm that copy corrections are live on the staging product page before signing Gate E. Gate E signed against uncorrected copy is invalid."* No fulfillment provider is connected, so no transaction has occurred. Gate E is invalid and must be re-confirmed against corrected staging pages after the corrections in §VI are applied.

**COA template status:** The standalone `NC-FIRST-SALE_COA_template.md` is CORRECT. It references NASA (not NARA), includes the required nonendorsement, and is properly sourced. The v2 package COA is the wrong reference for production. The COA template is the authoritative source for physical certificate printing.

---

## II. Phase 0 Launch Decision

**Phase 0 is CONDITIONALLY AUTHORIZED.** The following pages may go live at Gate E — but Gate E is currently invalid. Three corrections to the v2 production file and one file authority ruling must be completed first (see §VI).

### II.1 Pages authorized for Phase 0 launch

| Page | URL | Gate E condition | Status |
|---|---|---|---|
| Home | `/` | Earthrise hero: use corrected campaign_package copy or equivalent | CONDITIONALLY AUTHORIZED |
| Earthrise Story Page | `/stories/earthrise` | Use corrected campaign_package copy; no NARA references | CONDITIONALLY AUTHORIZED |
| Earthrise Product Page | `/products/earthrise-giclée` | Corrections 1–3 applied to v2 package; v2 superseded or corrected | BLOCKED — corrections required |
| About | `/about` | No asset-sourcing copy violations | AUTHORIZED |
| Products | `/products` | Earthrise products only; v2 package corrections applied | BLOCKED — corrections required |

### II.2 Pages that must remain "Coming Soon" in Phase 0

| Page | Coming Soon state | Reason |
|---|---|---|
| Pilot Places Index | Stub or omit | SA-GEONAMES-001 + SA-OSM-001 not ratified |
| Yellowstone | "Explore soon" teaser card | SA gates + tile integration not built |
| Grand Canyon | "Explore soon" teaser card | SA gates + tile integration not built |
| Great Barrier Reef | "Explore soon" teaser card | SA gates + NOAA Sprint 3 gate |
| Galápagos | "Explore soon" teaser card | SA gates |
| Papahānaumokuākea | Do not show | GeoNames ID unconfirmed |
| Venice | "Coming soon — expanding" | No art museum DD ratified; zero product-safe assets |

**Teaser cards for Phase 1 places on Home page:**
- May show place name, heritage designation, and a single hero image with PD badge
- Must NOT show product counts, asset counts, or "Add to Cart" CTAs
- Must NOT show any NARA-sourced images until NARA Sprint 1 is complete
- Must NOT show any Venice art until DD-MET-001 or equivalent is ratified

---

## III. Exact Required Copy — Earthrise

This is the authoritative copy standard for all Earthrise surfaces. It supersedes the v2 package where they conflict.

### III.1 Authoritative Production File Ruling

`docs/implementation/nc_first_sale_campaign_package.md` is the **authoritative production copy file** for the Earthrise launch.

`docs/implementation/nc_first_sale_final_conversion_package_v2.md` is **SUPERSEDED** and must not be used as a production reference. Its title "Approved for Final Release" is incorrect — it was never approved under FS-001 criteria. It is retained as a historical record only. Add the following header to that file:

```
⚠ SUPERSEDED — DO NOT USE FOR PRODUCTION.
FS-001 violations present. See nc_first_sale_campaign_package.md (authoritative).
Superseded by NC-WEB-001-LA (2026-06-12).
```

---

### III.2 Product Page — Required Copy (Zone 2, per NC-WEB-001 Blueprint)

**Archival Origin line (exact, mandatory):**
```
Archival Origin: Photograph by Astronaut William Anders, NASA Apollo 8 Mission,
December 24, 1968. Frame AS08-14-2383. 17 U.S.C. § 105 — public domain.
```

**NASA attribution and nonendorsement (exact, mandatory, immutable):**
```
Image credit: NASA. NASA does not endorse this product.
```

**Rights statement (Zone 7):**
```
Rights: Public Domain — United States Government Work
Basis: 17 U.S.C. § 105 (works produced by US federal employees within scope of employment)
Source: NASA — National Aeronautics and Space Administration
Asset ID: AS08-14-2383
Human verified: ✓
```

**What must NOT appear on the product page:**
- Any reference to NARA, the National Archives, or archival records from the National Archives
- Any statement implying NASA reviewed, verified, or endorsed the NC product
- "Collector's Edition" or 30"×30" Acrylic variant until NARA Sprint 1 complete

---

### III.3 Launch Email — Required Copy (footer, mandatory)

**Email footer (exact, mandatory):**
```
Image credit: NASA. NASA does not endorse this product.
```

**Email body — required replacement (Correction 3):**

Remove:
> "working with the original archival records from NASA and the National Archives"

Replace with:
> "working from NASA's original Hasselblad film frame (AS08-14-2383)"

---

### III.4 Social Copy — Required Copy

**Twitter/X (exact, mandatory):**
```
The click that changed the world. 🌍 Nature & Culture launches today with the definitive 
restoration of Earthrise. Sourced from NASA public-domain material. Image credit: NASA. 
NASA does not endorse this product. Ready for your home.
[URL] #DiscoveryIntelligence #SpaceHistory
```
*(This is the corrected form already present in nc_first_sale_campaign_package.md.)*

**Instagram/Facebook:**
```
240,000 miles away. 1968. The moment we finally saw home. Our Master Restoration of 
NASA AS08-14-2383 is now live. Explore the intelligence behind the image.
Image credit: NASA. NASA does not endorse this product. Link in bio.
#NatureAndCulture #Earthrise #NASA #OverviewEffect
```

**LinkedIn:**
```
Can "Intelligence" drive commerce? Today we launch Nature & Culture. Museum-grade 
restoration of Earthrise. Image credit: NASA. NASA does not endorse this product.
#Innovation #DataStorytelling #CommerceIntelligence
```

---

### III.5 Certificate of Authenticity — Required Copy

The authoritative COA template is `docs/governance/NC-FIRST-SALE_COA_template.md`. This file is correct. Use it verbatim for physical certificate printing.

**The v2 package COA (§4 of nc_first_sale_final_conversion_package_v2.md) is NOT authoritative.** It contains "Source Archive: National Archives and Records Administration (NARA)" — this is a false attribution and must not appear on any physical or digital COA.

**Required COA attribution block (from template, exact):**
```
Image credit: NASA.
NASA does not endorse this product.
This image is a work of the United States federal government and is in the public domain
in the United States (17 U.S.C. § 105).

Source: NASA Image and Video Library
Source record: AS08-14-2383
Rights basis: 17 U.S.C. § 105
```

---

### III.6 Story Page — Required Copy

No specific copy violations found in the story page content. Story pages that describe the Apollo 8 mission, William Anders, or the cultural significance of Earthrise are permitted without restriction, provided:
- The NASA nonendorsement line appears in the article footer
- No NARA attribution appears for the photograph itself
- No claim that NASA reviewed or approved the editorial content

**Footer (mandatory):**
```
Image credit: NASA. NASA does not endorse this product.
```

---

## IV. Prohibited Copy Register

This is the exhaustive list of copy that must not appear on any public-facing NC web surface, email, social post, or physical product at any phase.

### IV.1 Federal Endorsement — Zero Tolerance

Any violation in this category triggers cascade deactivation of all NASA, NOAA, and NARA assets across the entire catalog.

| Prohibited phrase | Why | Replacement |
|---|---|---|
| "NASA-endorsed" / "NASA-certified" / "NASA-approved" | False endorsement | "NASA photograph" / "Image credit: NASA" |
| "NASA partner" / "In partnership with NASA" | False partnership | Omit entirely |
| "Verified by NASA" | Implies NASA product review | "Image credit: NASA. NASA does not endorse this product." |
| "Verified mission data from NASA Johnson Space Center" as a rights claim | This is mission context, not image credit | Use exact NASA credit format |
| "Official NASA print" / "Official NASA product" | False endorsement | "Public domain photograph, 17 U.S.C. § 105" |
| "NOAA-certified" / "NOAA-endorsed" | Same — NOAA zero tolerance | "Credit: NOAA/[Division]" |
| Any agency name + "certified" / "endorsed" / "approved" / "official" | Universal rule | Use exact nonendorsement format |

### IV.2 NARA False Attribution — Earthrise Specific

| Prohibited phrase | Why | Replacement |
|---|---|---|
| "Sourced from the National Archives and Records Administration (NARA)" (product page) | AS08-14-2383 is a NASA photograph; NARA does not hold it | "Photograph by William Anders, NASA Apollo 8 Mission, December 24, 1968. AS08-14-2383." |
| "working with the original archival records from NASA and the National Archives" (email) | Co-attributing NARA is false for this photograph | "working from NASA's original Hasselblad film frame (AS08-14-2383)" |
| "Sourced from the National Archives. Verified by NASA." (social) | Both clauses are false or constitute endorsement | "Sourced from NASA public-domain material. Image credit: NASA. NASA does not endorse this product." |
| "Source Archive: National Archives and Records Administration (NARA)" (COA) | False provenance on a legal document | Use NC-FIRST-SALE_COA_template.md verbatim |
| "NARA: Verified archival source" (any surface) | FS-001 identified violation | Remove entirely; replace with NASA credit |

### IV.3 Deferred Assets — Must Not Appear as Available

| Asset | Prohibited copy | Reason |
|---|---|---|
| Thomas Moran paintings | Any product listing, price, "available", story CTA implying purchase | No DD-SMITHSONIAN-001 |
| Canaletto paintings | Any product listing, "available Venice art", story CTA | No DD for Museo Correr |
| HMS Beagle chart | "Own the chart that mapped the voyage" or any product CTA | DD-TNA-001/UKHO-001 required |
| de' Barbari Venice map | Any product listing | No DD |
| ESA/Copernicus imagery | Any display or product claim | Mislabeled "NASA/ESA"; DD-ESA-001 required |
| Darwin's sketch notebook | Any product listing | Cambridge UL — no DD |
| Cook's Pacific chart | Any product listing | DD-TNA-001 required |

**Email 3 hold:** The Playbook's Email 3 featuring Thomas Moran's *Grand Canyon of the Yellowstone* must not be sent. Add the following note to `docs/implementation/nc_first_sale_playbook.md`:

```
Email 3 — HELD INDEFINITELY:
Thomas Moran Grand Canyon of the Yellowstone is a deferred asset (DD-SMITHSONIAN-001 required).
This email must not be sent until after Moran Collection product activation.
Superseded by NC-WEB-001-LA (2026-06-12).
```

### IV.4 Premature Commerce Claims

| Prohibited | Reason |
|---|---|
| "Collector's Edition" or 30"×30" Acrylic variant, price, or "pre-order" | NARA Sprint 1 required |
| "Limited edition" without a specified edition size that has been set and locked | Misleading; edition specs must be confirmed before claim |
| Fashion / apparel product listings (lines 17, 18) | Routing policy v2.0 required |
| Collector bundle listings (line 20) | MASTERWORK + PA sign-off required per NC-PRODUCT-001 |
| Venice product listings of any kind | No product-safe Venice assets |
| "Coming soon" pricing or pre-sale for any Phase 1+ product before SA gates cleared | SA gates are pre-commerce gates |

### IV.5 Quality and Provenance Misrepresentation

| Prohibited | Reason |
|---|---|
| UNESCO / Smithsonian / NHM "verification" badges on Phase 0 pages | No institutional partnership or endorsement relationship |
| "Saville-Kent lithograph" product availability (experience wireframe reference) | No Saville-Kent asset in NC catalog at launch |
| GBIF thumbnails or species images | SA-GBIF-001: media permanently excluded |
| Wikidata Commons images in product pipeline | W-6 Commons boundary doctrine — permanently prohibited |
| OSM boundary data cited as a place attribute | OS-1–OS-5: OSM data permanently banned from NC tables |
| Personal names from NOAA credits (e.g., individual NOAA scientist names) | SA-NOAA-001: permanent hard block |

---

## V. Prohibited Pages and Features

### V.1 Pages that must not go live before their gate

| Page | Gate | Current status |
|---|---|---|
| Pilot Places Index | SA-GEONAMES-001 + SA-OSM-001 ratified | BLOCKED |
| Yellowstone | SA gates + Mapbox GL JS integration | BLOCKED |
| Grand Canyon | SA gates + Mapbox GL JS integration | BLOCKED |
| Great Barrier Reef | SA gates + NOAA Sprint 3 gate (write #1 of 7) | BLOCKED |
| Galápagos | SA gates | BLOCKED |
| Papahānaumokuākea | GeoNames ID confirmed + SA gates | BLOCKED |
| Venice (full) | First art museum DD ratified | BLOCKED |

### V.2 Features that must not go live at any phase without their prerequisite

| Feature | Prerequisite |
|---|---|
| Map tile display (any page) | SA-OSM-001 ratified + Mapbox GL JS integration complete |
| GeoNames-derived data rendered in public pages | SA-GEONAMES-001 ratified |
| NARA asset display with "Add to Cart" | NARA Sprint 1 complete (per-record `Unrestricted` confirmed) |
| Haeckel print as museum_print product | BHL scan ≥ 6000px confirmed by curator |
| Collector Edition listing | NARA Sprint 1 complete |
| NOAA-sourced products on GBR page | NOAA Sprint 3 ALLOWED cap check (first write authorization) |
| New NASA product types beyond NC-PROD-001, 008 | DD-NASA-001 formally filed |

---

## VI. Final Launch Checklist — Phase 0

This checklist must be completed in order before Gate E re-confirmation. Each item is a hard gate — no item may be skipped.

### Block A — Production File Corrections (< 1 hour)

**A-1.** Add supersession header to `docs/implementation/nc_first_sale_final_conversion_package_v2.md`:
```
⚠ SUPERSEDED — DO NOT USE FOR PRODUCTION.
FS-001 violations present. See nc_first_sale_campaign_package.md (authoritative).
Superseded by NC-WEB-001-LA (2026-06-12).
```

**A-2.** Confirm that `docs/implementation/nc_first_sale_campaign_package.md` Intelligence Stack reads:
```
Archival Origin: Sourced from NASA Image and Video Library record AS08-14-2383.
```
(Current state: CORRECTED — verify it remains unchanged.)

**A-3.** Confirm email body in campaign_package.md reads:
```
working from NASA public-domain source material
```
(Current state: CORRECTED — verify.)

**A-4.** Confirm Twitter/X caption in campaign_package.md reads:
```
Sourced from NASA public-domain material. Image credit: NASA. NASA does not endorse this product.
```
(Current state: CORRECTED — verify.)

**A-5.** Add Email 3 hold note to `docs/implementation/nc_first_sale_playbook.md` (see §IV.3 above).

### Block B — Staging Page Verification (curator + PA, same session)

**B-1.** Product page staging URL: verify "Archival Origin" line reads the NASA version (not NARA).

**B-2.** Product page staging URL: verify "Image credit: NASA. NASA does not endorse this product." is visible on the page without scrolling past the purchase CTA zone.

**B-3.** Product page staging URL: verify no "Collector's Edition" variant appears.

**B-4.** Story page staging URL: verify NASA nonendorsement appears in the footer.

**B-5.** Products listing staging URL: verify only NC-PROD-001 and NC-PROD-008 appear as "Add to Cart" items; all other products show "Coming Soon" or are absent.

**B-6.** Home page staging URL: verify no NARA attribution for Earthrise appears anywhere on the page.

**B-7.** About page staging URL: verify no Smithsonian, UNESCO, or institutional partnership claim appears.

### Block C — COA Verification (curator, before NC-PROD-001 physical fulfillment)

**C-1.** Confirm physical COA template for printing matches `NC-FIRST-SALE_COA_template.md` verbatim — specifically: no NARA reference, no "National Archives", NASA nonendorsement present.

**C-2.** Confirm COA includes curator signature + PA sign-off lines (not pre-signed).

**C-3.** Confirm COA does not reference Collector Edition or 30"×30" Acrylic.

### Block D — Gate E Re-Confirmation (two-human session: curator + PA)

**D-1.** Curator confirms Blocks A, B, C complete and staging copy is product-safe.

**D-2.** Principal Architect confirms Blocks A, B, C complete and no governance violations remain.

**D-3.** Both confirm: nc_first_sale_final_conversion_package_v2.md is marked SUPERSEDED and will not be used for dispatch.

**D-4.** Gate E session formally recorded with corrected-copy confirmation note:
```
Gate E re-confirmed 2026-06-12. Corrections verified against staging.
Prior Gate E (from activation_report.md) is superseded — it was signed against uncorrected copy.
```

### Block E — Product Activation Sequence (PA, after Gate E)

**E-1.** Activate NC-PROD-008 (digital download) first — validates pipeline with zero fulfillment risk.

**E-2.** Confirm NC-PROD-008 delivery pipeline functional (buyer receives correct file, correct attribution, nonendorsement).

**E-3.** Activate NC-PROD-001 (museum giclée) — triggers physical fulfillment readiness check.

**E-4.** Send Email 1 (Teaser) and Email 2 (Launch) using campaign_package.md copy only.

**E-5.** Do NOT send Email 3 (Moran) — held indefinitely per FS-002 and §IV.3 above.

### Block F — 60-Day Clock Obligations (PA)

**F-1.** Record first sale date — 60-day cosmic anchor resolution clock starts.

**F-2.** Calendar T+30: attribution audit of NC-PROD-001 and NC-PROD-008.

**F-3.** Calendar T+60: Earthrise S-3 provisional exception resolution deadline (Standards Constitution amendment OR proxy-place resolution).

**F-4.** Calendar T+60: Commission DD-SMITHSONIAN-001 (highest-priority revenue unblocking action).

---

## VII. Post-Phase-0 Prerequisites

For the record, the following items must be completed before Phase 1 work begins — they do not block Phase 0 Gate E.

| Item | Priority | Blocks |
|---|---|---|
| SA-GEONAMES-001 ratification | CRITICAL | All place pages, all geo-anchored products |
| SA-OSM-001 ratification | CRITICAL | All map tile display |
| NC-WEB-001 Technical Plan — draft and ratify | HIGH | Phase 1 build |
| NC-WEB-001 Wireframe + Creative Direction — draft and ratify | HIGH | Phase 1 build |
| GeoNames account registration (OQ-GN-2) | HIGH | GeoNames CC BY 4.0 compliance at scale |
| Mapbox GL JS integration + custom NC map style | HIGH | Phase 1 map display |
| NARA Sprint 1 (naId + Unrestricted per-record) | HIGH | NC-PROD-003, 004, Collector Edition |
| Remove Neo4j reference from wireframe_specifications.md | MEDIUM | Prevents stack confusion in Phase 1 build |
| DD-NASA-001 filing | MEDIUM | New NASA product types in Phase 3+ |
| DD-SMITHSONIAN-001 | HIGH — revenue | Moran Collection, highest commercial impact |

---

## VIII. Decision Table

| Decision | Ruling |
|---|---|
| Phase 0 authorized? | YES — conditionally, pending Blocks A–E |
| Gate E valid? | NO — invalid; re-confirmation required after Blocks A–C |
| nc_first_sale_final_conversion_package_v2.md authorized? | NO — SUPERSEDED; FS-001 violations present on 4 surfaces |
| nc_first_sale_campaign_package.md authorized? | YES — authoritative production file |
| NC-FIRST-SALE_COA_template.md authorized? | YES — authoritative for physical COA printing |
| Place pages authorized for Phase 0? | NO — all 5 place pages blocked (SA gates) |
| Collector Edition authorized? | NO — NARA Sprint 1 required |
| Email 3 (Moran) authorized? | NO — held indefinitely (FS-002, deferred asset) |
| Venice content authorized? | NO — zero product-safe assets; art museum DD required |
| Experience wireframe creative language (typography, motion)? | YES — adopted for Phase 0 |
| Experience wireframe content inventory (Saville-Kent, Machu Picchu, etc.)? | NO — pilot scope only; non-pilot content prohibited |
| Neo4j in wireframe_specifications.md? | NOT AUTHORIZED — frozen stack; must be removed before Phase 1 |

---

## IX. Authorization

Phase 0 launch is **AUTHORIZED** upon completion of Blocks A–E in §VI.

Gate E re-confirmation (Block D) is required. The prior activation record in `NC-FIRST-SALE_activation_report.md` does not constitute a valid Gate E for revenue purposes — it was signed against uncorrected copy. The first valid revenue transaction may occur only after Gate E is re-confirmed per Block D above.

All Phase 1+ pages remain blocked until SA-GEONAMES-001 and SA-OSM-001 are ratified and Blocks are cleared per NC-WEB-001 Blueprint §VII.

---

*NC-WEB-001-LA v1.0 — drafted 2026-06-12.*
*Authority: NC-WEB-001 Blueprint · NC-FIRST-SALE Authorization Art. 2 · NC-FIRST-SALE-VERIFY · NC-PRODUCT-001 §IV · NC-PILOT-001-FRR · SA-GEONAMES-001 · SA-OSM-001*
*Governing invariants: IFC-1 · GN-6 · OS-6 · Federal nonendorsement zero-tolerance*
