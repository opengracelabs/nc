# NC-PILOT-001: Final Launch Governance Review

| Field | Value |
|---|---|
| Document | NC-PILOT-001-FGR |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Decision | **APPROVE WITH CONDITIONS** |
| Blocking conditions | 7 (listed in §IX) |
| Documents reviewed | NC-PILOT-001 Governance Blueprint · nc_pilot_001_experience_blueprint.md · OSM/GeoNames/Wikidata Intelligence Plans · NOAA Pilot 25 Launch Package |
| Technical Plan | **ABSENT — blocking condition #1** |

---

## I. Review Scope and Method

This review assesses readiness for public launch of the NC-PILOT-001 commercial pilot across three dimensions:

1. **Document completeness** — Are all required governance artifacts present?
2. **Cross-document consistency** — Do the Governance Blueprint, Experience Blueprint, and technical plans agree?
3. **Asset-level governance** — Are the specific assets named in the Experience Blueprint product-safe?

The review is not a re-derivation of the Governance Blueprint. Rulings already established in the Governance Blueprint and its underlying DDs are treated as settled. This review surfaces gaps, conflicts, and missing artifacts that NC-PILOT-001 did not resolve.

---

## II. Document Status

| Document | Status | Blocking? |
|---|---|---|
| NC-PILOT-001 Governance Blueprint | Present — drafted 2026-06-11 | No |
| nc_pilot_001_experience_blueprint.md | Present — approved blueprint | No |
| **NC-PILOT-001 Technical Plan** | **ABSENT** | **Yes — blocking condition #1** |
| SA-GEONAMES-001 | Not drafted | Yes — blocking condition #2 |
| SA-OSM-001 | Not drafted | Yes — blocking condition #3 |
| SA-NOAA-001 | Ratified | No |
| SA-NOAA-002 | Ratified | No |
| SA-GBIF-001 | Ratified | No |
| SA-WIKIDATA-001 | Not drafted | No (catalog scale, not pilot) |

### II.1 The Missing Technical Plan

No document named "NC-PILOT-001 Technical Plan" or equivalent exists. Four intelligence plans (GeoNames, OSM, Wikidata, GBIF) and several adapter specifications exist independently but have not been synthesized into a single technical launch document. The Technical Plan's absence creates three specific risks:

- No single document confirms that all seven place identity records have been written to the `places` table with GeoNames IDs, feature codes, and Wikidata QIDs
- No single document confirms that Asset Zero records have been written and IFC-1 human-verified for each pilot place
- No single document confirms that the attribution implementation (Gates B-1 through B-5) has been built and tested

**Required content for the Technical Plan:** canonical GeoNames IDs per place (confirmed via API); Wikidata QIDs per place; GBIF taxon key list per place; Asset Zero record identifiers (source_item UUIDs, activation_target IDs); attribution component build status; tile service selection; two-human activation gate documentation.

---

## III. Launch Readiness Assessment

### III.1 Overall Verdict

**NOT LAUNCH READY.** Seven blocking conditions exist. None requires a new governance decision — all are either missing documents or known conflicts. All are resolvable. Partial launch of individual places (per NC-PILOT-001 §VII.3) remains viable as individual place gates clear.

### III.2 Readiness by Layer

| Layer | Status | Blocking issue |
|---|---|---|
| Identity (GeoNames) | **PARTIAL** | GeoNames IDs unreconciled between documents (§III.4); SA-GEONAMES-001 not drafted |
| Identity (Wikidata) | Pending confirmation | Technical Plan absent; QIDs not confirmed as written |
| Evidence (GBIF) | Consistent | SA-GBIF-001 ratified; no conflicts |
| Content — NASA | Ready (rights) | Technical Plan absent; Asset Zero confirmation pending |
| Content — NOAA | Conditional | NOAA asset rights gate per SA-NOAA-001 not documented per asset |
| Content — NARA | Conditional | Asset Zero records not confirmed in Technical Plan |
| Content — BHL | Ready (existing pipeline) | No new governance gaps |
| Map display (OSM) | **BLOCKED** | SA-OSM-001 not drafted; OSM Intelligence Plan conflicts with DD-OSM-001 |
| Attribution | **BLOCKED** | SA-GEONAMES-001 not drafted; SA-OSM-001 not drafted |
| Asset inventory | **PARTIAL** | 9 of 25 Experience Blueprint launch assets are not product-safe (§IV) |

### III.3 Critical Conflict: OSM Intelligence Plan vs. DD-OSM-001

The OSM Intelligence Plan (osm_intelligence_plan_v1.md) was written before DD-OSM-001. It contains provisions that directly violate DD-OSM-001 Invariants OS-1 through OS-5:

| OSM Intelligence Plan provision | DD-OSM-001 ruling | Verdict |
|---|---|---|
| "OSM as primary Access & Infrastructure Authority" with data integration | Infrastructure Reference only; no data authority role | **CONFLICT** |
| OSM Relation IDs listed by name (163151, 183377, 2533338, 44118, 6411191) | No osm_id may be stored in any NC canonical field (Invariant OS-4) | **CONFLICT — violates OS-4** |
| Trails, access restrictions, infrastructure data described as intelligence vectors | No OSM data in canonical tables (Invariant OS-1); no OSM scoring input (Invariant OS-3) | **CONFLICT — violates OS-1 + OS-3** |
| "Access & Infrastructure Authority" implies data storage and querying | OSM is Infrastructure Reference only; data never enters NC pipeline | **CONFLICT — violates OS-2** |

**Immediate action required:** The OSM Intelligence Plan must be superseded by a revised OSM Integration Note that restricts NC's OSM use to the produced-works tile path only. The revision must explicitly state that OSM Relation IDs listed in the Intelligence Plan are not stored in NC tables and that the plan's "data integration" vectors are implemented via tile service rendering, not database ingestion.

This conflict does not block tile-service display of place maps. It blocks only the data-integration provisions of the Intelligence Plan.

### III.4 GeoNames ID Discrepancy

The Governance Blueprint (NC-PILOT-001 §III) and the GeoNames Intelligence Plan use different GeoNames IDs for four of five pilot places:

| Place | Governance Blueprint | Intelligence Plan | Reconciled? |
|---|---|---|---|
| Yellowstone | 4720206 | 5843642 | ☐ |
| Grand Canyon | 5513679 | 5296404 | ☐ |
| Great Barrier Reef | not specified | 10288865 | ☐ |
| Papahānaumokuākea | not specified | 11854341 | ☐ |
| Venice | 3164603 | 3164603 | ✓ |

A `geonames_id` is a constitutional fixture (Invariant S-3). Two different IDs cannot both be correct for the same place — one or both documents contain an error. GeoNames may have multiple entries for the same physical place (e.g., both a national park boundary entry and a visitor center entry). The canonical entry for NC must be the one whose `feature_code` matches the governing CI Constitution routing formula.

**Required resolution:** Confirm canonical GeoNames IDs for all seven pilot places via live GeoNames API lookup before writing any place records. The Technical Plan must contain the confirmed IDs. All governance documents must be updated to reflect the confirmed values.

---

## IV. Asset-Level Governance Audit

The Experience Blueprint defines a "Top 25 Launch Assets" list (§Top 25 Launch Assets). This section audits each asset's product-safety status against the governing DDs.

### IV.1 Product-Safe at Launch

| # | Asset | Source | Rights basis | Status |
|---|---|---|---|---|
| 3 | Bison bison historical illustration | BHL | PD — pre-1928 | ✓ Product-safe |
| 4 | NASA Thermal Map of Yellowstone | NASA | § 105 | ✓ Product-safe |
| 5 | Powell Expedition Photograph | NARA | § 105 — federal employee | ✓ Pending `Unrestricted` confirmation |
| 6 | USGS Grand Canyon Strata Cross-Section | NARA | § 105 — USGS federal work | ✓ Pending `Unrestricted` confirmation |
| 7 | California Condor anatomical drawing | BHL | PD — pre-1928 | ✓ Product-safe |
| 9 | Ernst Haeckel, Hexacoralla | BHL | PD — Haeckel died 1919 | ✓ Product-safe |
| 11 | NASA Landsat 8 Coral Reef Mosaic | NASA | § 105 | ✓ Product-safe |
| 12 | Chelonia mydas historic plate | BHL | PD — pre-1928 | ✓ Product-safe |
| 13 | Laysan Albatross courtship illustration | BHL | PD — pre-1928 | ✓ Product-safe |
| 14 | Battle of Midway Tactical Map, 1942 | NARA | § 105 — military federal work | ✓ Pending `Unrestricted` confirmation |
| 15 | NOAA Bathymetric Map, Hawaiian Ridge | NOAA | § 105 | ✓ Pending SA-NOAA-001 gate |
| 16 | Hawaiian Monk Seal historical sketch | BHL | PD — pre-1928 | ✓ Product-safe |
| 21 | John Gould, Darwin's Finches | BHL | PD — Gould died 1881 | ✓ Product-safe |
| 23 | Chelonoidis niger anatomical plate | BHL | PD — pre-1928 | ✓ Product-safe |
| 25 | NASA AS08-14-2383, Earthrise | NASA | § 105 | ✓ Product-safe |

### IV.2 Not Product-Safe at Launch — Institutional Governance Gap

Nine of 25 assets name institutions with no active NC Director Decision. These assets may not enter the commercial pipeline until a governing DD is ratified for the relevant institution.

| # | Asset | Source institution | Problem | Resolution path |
|---|---|---|---|---|
| **1** | Thomas Moran, *Grand Canyon of the Yellowstone* | Smithsonian NMAA | No DD-SMITHSONIAN-001 | Commission DD-SMITHSONIAN-001; Smithsonian OpenAccess (CC0) is a strong candidate |
| **8** | Moran, *Chasm of the Colorado* | Smithsonian / Dept. of Interior | No DD-SMITHSONIAN-001 | Same as #1 |
| **10** | Cook's Endeavour Chart of the Reef | UK Hydrographic Office / TNA (UK) | **Not NARA.** UK government record — NARA § 105 does not apply | Commission DD-TNA-001 or DD-UKHO-001 |
| **17** | Canaletto, *The Grand Canal* | Multiple (Met, NGA, N. Gallery London) | No ratified museum DD yet | Met DD-MET-001 ratification unblocks most Canaletto holdings |
| **18** | Jacopo de' Barbari, Venice map 1500 | Museo Correr, Venice | No DD-MUSEOCORRER-001 | Commission or substitute with another institution's scan |
| **19** | Architectural elevation, St. Mark's | Institution not specified | No institutional anchor; not product-safe | Identify institution, commission DD |
| **20** | Copernicus Sentinel-2, Venice Lagoon | ESA | **Mislabeled "NASA/ESA" — ESA only.** No DD-ESA-001. ESA data policy ≠ NASA § 105 | Commission DD-ESA-001 or substitute NASA Sentinel-3 alternative |
| **22** | HMS Beagle Navigational Chart | UK Hydrographic Office | **Not NARA.** British Crown copyright / PD analysis differs from § 105 | Commission DD-UKHO-001 or source from an institution with confirmed PD scan |
| **24** | Darwin's "I Think" sketch | Cambridge University Library | No DD-CAMBRIDGE-001; Cambridge digitization terms require separate governance | Commission DD-CAMBRIDGE-001 (long path) or remove from launch list |

**Net product-safe at launch:** 16 of 25 confirmed or conditionally safe (pending Unrestricted/NOAA gate confirmation). 9 of 25 not product-safe.

### IV.3 Additional Asset Governance Notes

**NOAA "Key Largo 360° Virtual Dive" (NOAA Pilot 25, #4):** This asset is a 360°/VR immersive experience. Phase 2-4 media types are governed by Media Substrate Constitution v1.2 §5.8 phase gating. 360°/VR content is not a Phase 1 media type. It may not enter the pilot as a commercial product without a Phase gate authorization. It may be used for editorial/discovery page display purposes only in Phase 1.

**"Apollo flight plan documents" (Experience Blueprint §7.6, Earthrise):** Referenced but not assigned an asset number or institution. Apollo 8 mission documents are held at both NASA and NARA. If NASA-held: § 105, product-safe. If NARA-held: Rights Class 9, requires `Unrestricted` confirmation. The specific document, asset ID, and institutional source must be defined before this asset enters the pipeline.

**Asset #20 (ESA/Copernicus) provenance error:** The label "NASA/ESA" for Copernicus Sentinel-2 is factually incorrect. The Copernicus programme is the European Union Space Programme operated by ESA; NASA has no role in Copernicus satellite data production. All references to "NASA/ESA" for Copernicus assets must be corrected to "ESA / Copernicus" before any public-facing content uses this attribution.

---

## V. Attribution Requirements

The Governance Blueprint §IV establishes the complete attribution matrix. This review confirms its accuracy and notes three gaps introduced by the Experience Blueprint:

### V.1 Confirmed Attribution Requirements (from Governance Blueprint)

All four attribution obligations in §IV.2 are confirmed:
- GeoNames CC BY 4.0 — on all 6 terrestrial place pages
- NASA nonendorsement — on all NASA-sourced product listings
- NOAA nonendorsement — on all NOAA-sourced asset pages
- OSM ODbL — "© OpenStreetMap contributors" on all map tile displays

### V.2 Additional Attribution — Not in Governance Blueprint

**ESA/Copernicus (if retained):** If asset #20 is retained under a future DD-ESA-001, the Copernicus data policy requires: "Contains modified Copernicus Sentinel data [YEAR]" on any product or page incorporating ESA satellite data. This is a separate attribution obligation from NASA. It cannot be satisfied by the NASA nonendorsement line.

**Museum institutional credit:** Assets sourced from art museums (Moran/Smithsonian, Canaletto/Met, etc.) require institutional attribution per the relevant institution's access policy. These are governed per institution, not universally. Museum attribution must be confirmed when each institution's DD is ratified.

**UK Crown works / PD declaration:** Assets from UK government archives (Cook's chart, HMS Beagle chart) require a provenance statement confirming PD status under UK law. The legal analysis differs from § 105 and must be conducted per asset when the relevant UK institution DD is ratified.

### V.3 Attribution Implementation Status

Neither SA-GEONAMES-001 nor SA-OSM-001 has been drafted. Until both are ratified:
- GeoNames CC BY 4.0 attribution is a governance commitment without an implemented standard
- OSM tile display attribution is a governance commitment without a governed implementation format

Attribution gates B-1 and B-2 in the Governance Blueprint §VII cannot be confirmed cleared.

---

## VI. Publication Policy

**No publication policy document exists.** The Governance Blueprint §VII defines launch gates; it does not define a publication policy. Publication policy governs what happens after an asset passes the activation gate and before a consumer can purchase it.

A publication policy must address:

| Element | Current status | Required |
|---|---|---|
| Activation-to-visibility pipeline | Not documented | Required |
| SEO indexing gate (when do place pages become crawlable?) | Not documented | Required |
| Attribution compliance checkpoint before page goes live | Implied by Gates B-1/B-2 but not formalized | Required |
| Federal nonendorsement copy review process | Not documented; implied by Boundary C-2 | Required |
| Product listing review checklist | Not documented | Required |
| Takedown / retraction procedure for erroneously activated assets | Not documented | Required |

**Minimum required for launch:** A one-page publication checklist that confirms attribution is present, nonendorsement copy review is complete, and IFC-1 status is verified before any product listing is made publicly visible. This does not require a full constitution — a governed checklist with a two-human sign-off is sufficient.

---

## VII. Pilot Success Metrics Review

The Governance Blueprint §VIII defines success metrics across four categories. This review confirms the metrics are well-structured and adds two gaps:

### VII.1 Confirmed Metrics (from Governance Blueprint §VIII)

All metrics in §VIII.1 (rights compliance), §VIII.2 (attribution compliance), §VIII.3 (commercial performance), and §VIII.4 (governance health) are confirmed. No changes required.

### VII.2 Additional Metrics — Not in Governance Blueprint

**NOAA per-asset rights gate confirmation metric:** The NOAA Pilot 25 Launch Package names 25 specific assets. For NOAA assets, the SA-NOAA-001 gate (Flickr license integer or credit field check) must be confirmed per asset, not per institution. Success metric: 100% of NOAA assets in the pilot have documented SA-NOAA-001 gate confirmation results (ALLOWED / BLOCKED) on record before activation.

**GeoNames ID reconciliation metric:** Canonical GeoNames IDs confirmed via API lookup for all 7 pilot places before any place record is written to the canonical `places` table. This is a pre-pilot infrastructure metric, not a post-launch metric.

**Asset governance coverage metric:** % of planned launch assets that are product-safe at launch (target: 100% of activated assets; the non-product-safe assets are excluded from launch, not activated with a flag). At current inventory audit: 16 of 25 assets are product-safe pending final confirmation; 9 are excluded. The launch metric should be: "All activated assets are product-safe; no non-product-safe asset is in the active pipeline."

---

## VIII. OSM Integration Plan — Supersession Required

The OSM Intelligence Plan must be formally superseded. A one-page OSM Integration Note is required that:

1. States that DD-OSM-001 governs all NC OSM interaction
2. Revises the "Access & Infrastructure Authority" role to "Infrastructure Reference" per DD-OSM-001 Article 1
3. Explicitly prohibits storage of all OSM Relation IDs listed in the Intelligence Plan
4. Confirms that trail networks, access restrictions, and infrastructure data are consumed only as produced-works tile rendering — they are never stored in NC canonical tables
5. Maps each "intelligence vector" from the old plan to its governed equivalent: `highway=path` trail display → tile rendering; `access=*` restriction display → tile rendering; `tourism=viewpoint` → tile rendering

The revised OSM Integration Note does not require a full DD. It is a governed amendment to the Intelligence Plan. It should be issued as part of SA-OSM-001.

---

## IX. Conditions Register

Seven conditions must be satisfied before public launch authorization. Conditions are independent — resolving one does not unblock others.

| # | Condition | Authority | Blocking what? | Complexity |
|---|---|---|---|---|
| **C-1** | Technical Plan drafted and confirmed: canonical GeoNames IDs, Wikidata QIDs, GBIF taxon keys, Asset Zero IDs, attribution build status, tile service selection | NC-PILOT-001-FGR §II.1 | Full launch readiness confirmation | Low — synthesis of existing docs |
| **C-2** | SA-GEONAMES-001 ratified: CC BY 4.0 attribution standard, API governance, attribution checklist §XII.2 confirmed | DD-GEONAMES-001 Art. 13 | All public place page launches | Medium — draft + ratification |
| **C-3** | SA-OSM-001 ratified: tile service selected, "© OpenStreetMap contributors" attribution implemented, OSM Intelligence Plan superseded | DD-OSM-001 Art. 10 | All map tile displays | Medium — tile service selection required |
| **C-4** | GeoNames IDs reconciled: canonical ID confirmed via API for all 7 pilot places; all governance documents updated to reflect confirmed values | DD-GEONAMES-001 Invariant GN-1 | `places` table write; all downstream identity | Low — API lookup only |
| **C-5** | Non-product-safe assets (§IV.2) removed from launch plan: 9 assets either replaced with product-safe alternatives or deferred to post-ratification sprints | IFC-1; NC-PILOT-001 §V.1 | Product inventory integrity | Low — curation decision |
| **C-6** | Asset #20 ESA/Copernicus provenance corrected: "NASA/ESA" label removed; asset either deferred pending DD-ESA-001 or replaced with confirmed NASA asset for Venice | IFC-1; DD-NASA-001 | Venice asset integrity | Low — content decision |
| **C-7** | Minimum publication checklist created: attribution present, nonendorsement copy reviewed, IFC-1 verified, two-human sign-off documented | NC-PILOT-001-FGR §VI | Public product listing visibility | Low — one-page checklist |

### IX.1 Conditions by Place Impact

| Condition | Yellowstone | Grand Canyon | GBR | Papahānaumokuākea | Venice | Galápagos | Earthrise |
|---|---|---|---|---|---|---|---|
| C-1 (Technical Plan) | Blocks | Blocks | Blocks | Blocks | Blocks | Blocks | Blocks |
| C-2 (SA-GEONAMES-001) | Blocks | Blocks | Blocks | Blocks | Blocks | Blocks | No effect |
| C-3 (SA-OSM-001) | Blocks map | Blocks map | Blocks map | Blocks map | Blocks map | Blocks map | No effect |
| C-4 (GeoNames IDs) | Blocks | Blocks | Blocks | Blocks | No effect | — | No effect |
| C-5 (non-safe assets) | #1 removed | #8 removed | #10 removed | — | #17–20 removed | #22, 24 removed | — |
| C-6 (ESA correction) | — | — | — | — | #20 corrected | — | — |
| C-7 (pub checklist) | Blocks | Blocks | Blocks | Blocks | Blocks | Blocks | Blocks |

**Earthrise is the closest to launch-ready.** C-1 and C-7 are its only blocking conditions. Both are document-creation tasks, not governance decisions. Earthrise can launch independently once C-1 and C-7 are satisfied — it requires no GeoNames resolution (cosmic anchor exception), no map tile display, no NOAA assets, and has no non-product-safe assets in its inventory.

---

## X. Decision

**APPROVE WITH CONDITIONS.**

The pilot governance architecture established by NC-PILOT-001 and its underlying DDs is sound. The IFC-1 hard gate, the federal nonendorsement doctrine, the CC BY 4.0 attribution obligation, and the ODbL produced-works path are all correctly identified and governed. No new governance decisions are required to resolve any of the seven blocking conditions.

The conditions are execution gaps, not governance gaps — they require document creation, API lookup, content curation decisions, and one standards amendment ratification sequence. None requires a new DD or constitutional amendment.

**Recommended resolution sequence:**

| Step | Action | Unblocks | Time estimate |
|---|---|---|---|
| 1 | Resolve C-4: confirm GeoNames IDs via API | C-4 | 1 hour |
| 2 | Resolve C-5: remove 9 non-product-safe assets from launch list | C-5 | 1 hour |
| 3 | Resolve C-6: correct ESA/Copernicus label; defer asset | C-6 | 30 min |
| 4 | Draft SA-GEONAMES-001 | Enables C-2 ratification | 1 session |
| 5 | Draft SA-OSM-001 with OSM Intelligence Plan supersession | Enables C-3 ratification; resolves OSM conflict | 1 session |
| 6 | Draft Technical Plan from existing intelligence plans | C-1 | 1 session |
| 7 | Create publication checklist | C-7 | 30 min |
| 8 | Ratify SA-GEONAMES-001 | C-2 cleared | Principal Architect |
| 9 | Ratify SA-OSM-001 | C-3 cleared | Principal Architect |
| 10 | Confirm two-human activation gate (NC-PILOT-001 §VII Gate E) | Full launch authorization | Human sign-off |

At step 3, Earthrise can launch (C-1 + C-7 cleared). At step 9, all seven places can launch.

---

## XI. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☑ APPROVE WITH CONDITIONS | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-PILOT-001-FGR — drafted 2026-06-11*  
*Documents reviewed: NC-PILOT-001 Governance Blueprint · nc_pilot_001_experience_blueprint.md · osm_intelligence_plan_v1.md · geonames_intelligence_plan_v1.md · wikidata_intelligence_plan_v1.md · noaa_pilot_25_launch_package.md · nasa_pilot_75_plan.md*  
*Decision: APPROVE WITH CONDITIONS — 7 conditions — Earthrise launch-ready pending C-1 + C-7 only*
