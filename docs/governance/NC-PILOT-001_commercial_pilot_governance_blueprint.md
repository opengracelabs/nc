# NC-PILOT-001: Commercial Pilot Governance Blueprint

| Field | Value |
|---|---|
| Document | NC-PILOT-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Decision | APPROVE WITH CONDITIONS |
| Conditions | SA-GEONAMES-001 · SA-OSM-001 · Earthrise cosmic-anchor exception · Venice content-layer notation |
| Pilot places | Yellowstone · Grand Canyon · Great Barrier Reef · Papahānaumokuākea · Venice · Galápagos · Earthrise |
| Authority | DD-NASA-001 · DD-NOAA-001 · DD-GBIF-001 · DD-WIKIDATA-001 · DD-GEONAMES-001 · DD-OSM-001 · DD-NARA-001 · DD-MIA-001 |

---

## I. Authority Chain

All pilot decisions are subordinate to the following hierarchy:

```
Strategic Directive + Illustration Opportunity Doctrine
        ↓
Institution Factory Constitution v1 (IFC-1–IFC-12)
        ↓
Standards Constitution v1.0 (S-1–S-7; Articles 16–17)
        ↓
Commerce Intelligence Constitution v1.2
        ↓
Foundation Model Constitution v1.0 (FM-1–FM-5)
        ↓
Individual Director Decisions (DD-NASA-001 through DD-OSM-001)
        ↓
Standards Amendments (SA-NOAA-001, SA-NOAA-002, SA-GBIF-001, and pending SAs)
        ↓
NC-PILOT-001 (this document)
```

No provision of this blueprint overrides a higher authority. Where this blueprint is silent, the governing DD or constitution applies directly.

---

## II. Governance Model

### II.1 Source Classification Summary

Seven external authorities govern the pilot. Each occupies a distinct governance class:

| Authority | Governance class | Governs | Rights basis | Commercial use |
|---|---|---|---|---|
| NASA | Content Institution (#20) | Planetary + national park imagery | 17 U.S.C. § 105 | Permitted; nonendorsement applies |
| NOAA | Content Institution (#21) | Marine + coastal imagery | 17 U.S.C. § 105 | Permitted; nonendorsement applies |
| NARA | Content Institution (#18) | Historic maps + expedition cartography | 17 U.S.C. § 105 | Permitted |
| MIA | Content Institution (#19) | Fine art + natural history collections | Rights Class 3B (`rights_type` gate) | Permitted for PD-confirmed records |
| GBIF | Identity + Evidence Authority | Taxon anchoring, place-relevance scoring | CC0 (Backbone) | Permitted; capped occurrence evidence only |
| Wikidata | Identity + Evidence Authority | Entity identity (QIDs), crosswalks | CC0 | Permitted; read-only |
| GeoNames | Place Identity + Evidence Authority | Place identity, feature codes, coordinates | CC BY 4.0 | Permitted; attribution required |
| OSM | Infrastructure Reference | Map tile display only | ODbL 1.0 (produced works) | Permitted via tile service; no data storage |

### II.2 IFC-1 Hard Gate

Every asset entering the commercial pipeline must pass the IFC-1 hard gate regardless of source:

```
rights_status = 'verified_pd'
    AND rights_basis ∈ {17_usc_105, cc0, pd_confirmed}
    AND human_verified = TRUE
    AND activation_target.status = 'activated'
```

No Foundation Model determination alone may set `rights_status`. FM-4 invariant is active across all seven pilot places. Human rights verifier confirmation is required before any asset appears in a product.

### II.3 Nonendorsement Doctrine

Three pilot content institutions — NASA, NOAA, and NARA — are US federal agencies. The nonendorsement doctrine applies to all three:

**Prohibited in all NC product copy, marketing, and UI involving these assets:**
- "Official NASA", "NASA Approved", "NASA Partner"
- "Official NOAA", "NOAA Endorsed", "NOAA Certified"
- "Official National Archives", "NARA Approved"
- Any display of NOAA circular seal, NASA insignia ("meatball"), or NARA seal
- Any statement suggesting US government backing, endorsement, or recommendation of NC

**Permitted:**
- "Image credit: NASA. NASA does not endorse this product." — governed NASA attribution line
- "Credit: NOAA/[division]" — governed NOAA attribution line
- "Image from the National Archives" — factual provenance attribution for NARA

The nonendorsement doctrine is a brand constraint, not a rights constraint. It does not affect IFC-1 status or commercial sale authorization.

### II.4 Source Role Provenance

Every illustration opportunity record produced by this pilot must carry:

```json
{
  "source_roles": {
    "bhl": "primary_discovery",
    "gbif": "validation_only",
    "wikidata": "context_only"
  }
}
```

For pilot assets sourced from NASA, NOAA, NARA, or MIA, the source role is `"primary_discovery"` for the originating institution. GBIF and Wikidata retain their governed roles regardless of the primary source.

---

## III. Data Architecture per Place

### III.1 Place 1 — Yellowstone National Park

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | GeoNames | geonames_id: 4720206 · fcode: PRKA · country: US | S-3; DD-GEONAMES-001 Art. 2 |
| **Crosswalk** | Wikidata | Q17108 | DD-WIKIDATA-001 §VI.3 |
| **Biological evidence** | GBIF | Bison bison (gbif_taxon_key: 2441176), Canis lupus, Ursus arctos, Cygnus buccinator, thermophilic archaea | SA-GBIF-001 — occurrence count capped at 100 |
| **Orbital imagery** | NASA | NC-NASA-026 "Yellowstone from Orbit" (ID-543) | DD-NASA-001; § 105 |
| **Cartographic** | NARA | Hayden Survey maps 1871–1878 (first national park surveys); Yellowstone River expedition records | DD-NARA-001; Rights Class 9; `useRestriction.status == "Unrestricted"` required |
| **Place display** | OSM tile service | Park boundary polygon | DD-OSM-001 Art. 3; produced works path |
| **Attribution** | GeoNames + NASA | CC BY 4.0 place data; NASA nonendorsement line | DD-GEONAMES-001 Art. 3; DD-NASA-001 |

**Yellowstone content verdict:** Strongest pilot place. NASA orbital imagery provides immediate product inventory. NARA holds the original Hayden Survey cartography — the maps that led directly to Yellowstone's 1872 designation as the world's first national park. Both sources are PD under § 105 with clean commercial authorization.

**Minimum viable asset set:** 1× NASA orbital (NC-NASA-026) + 1× NARA Hayden Survey map, both IFC-1 human-verified.

---

### III.2 Place 2 — Grand Canyon National Park

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | GeoNames | geonames_id: 5513679 · fcode: PRKA · country: US (**ERRATA NC-DATA-002:** 5513679 unverified — awaiting GCA-001 fixture) | S-3; DD-GEONAMES-001 Art. 2 |
| **Crosswalk** | Wikidata | ~~Q131648~~ **Q220289** (**ERRATA NC-DATA-002:** Q131648 = geological canyon feature, not the park; Q220289 = Grand Canyon National Park) | DD-WIKIDATA-001 §VI.3 |
| **Biological evidence** | GBIF | Gymnogyps californianus (California condor, gbif_taxon_key: 2481789), Oncorhynchus clarki (cutthroat trout), canyon wren | SA-GBIF-001 — occurrence count capped at 100 |
| **Orbital imagery** | NASA | NC-NASA-027 "Grand Canyon Depth" (ASTER-GC) | DD-NASA-001; § 105 |
| **Cartographic** | NARA | Powell Colorado River Survey 1869–1872; Wheeler Survey maps 1871–1879; USGS canyon cross-sections | DD-NARA-001; Rights Class 9 |
| **Place display** | OSM tile service | Park and canyon rim boundary | DD-OSM-001 Art. 3 |
| **Attribution** | GeoNames + NASA | CC BY 4.0; NASA nonendorsement | DD-GEONAMES-001 Art. 3 |

**Grand Canyon content verdict:** Strong pilot place. NARA holds the Powell and Wheeler surveys — the definitive 19th-century American exploration records that document the canyon for the first time. These are the NC golden-age illustration equivalent for a geologic subject. NASA's ASTER thermal imagery complements the geologic story.

**Minimum viable asset set:** 1× NASA orbital (NC-NASA-027) + 1× NARA Powell Survey map/illustration, both IFC-1 human-verified.

---

### III.3 Place 3 — Great Barrier Reef

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | GeoNames | ~~fcode: RFU~~ **fcode: RF (H.RF) · GeoNames 2164628** (NC-DATA-005) · country: AU | S-3; DD-GEONAMES-001 Art. 2 |
| **Crosswalk** | Wikidata | ~~Q37901~~ **Q7343** (NC-DATA-005) | DD-WIKIDATA-001 §VI.3 |
| **Biological evidence** | GBIF | Acropora spp. (coral), Chelonia mydas (green turtle), Dugong dugon, Hemiscyllium ocellatum | SA-GBIF-001 — occurrence count capped at 100 |
| **Orbital imagery** | NASA | NC-NASA-029 "GBR Whitsundays" (ISS-GBR) | DD-NASA-001; § 105 |
| **Marine imagery** | NOAA | NOAA coral reef collections; marine species from NOAA fisheries — federal-employee credit images only | DD-NOAA-001; SA-NOAA-001 §I.1 Gate: license 8 or 7 only |
| **Place display** | OSM tile service | Reef extent and marine park boundary | DD-OSM-001 Art. 3 |
| **Attribution** | GeoNames + NASA + NOAA | CC BY 4.0; NASA nonendorsement; NOAA nonendorsement | DD-GEONAMES-001; DD-NOAA-001 §II.5 |

**Great Barrier Reef content verdict:** High-value pilot place. The first pilot place to activate both NASA and NOAA content simultaneously. NOAA's coral reef photography fills a content gap that no other current NC institution addresses. The GBR's RFU (reef) feature code triggers CI Constitution marine routing formulas.

**NOAA pilot restriction:** Per DD-NOAA-001 Sprint 3 authorization, REVIEW_REQUIRED records receive 0 writes in the pilot (NASA model precedent). Only ALLOWED records (license 8, 7, or equivalent confirmed federal-employee credit) are written.

**Minimum viable asset set:** 1× NASA ISS (NC-NASA-029) + 1× NOAA federal-employee coral reef image (SA-NOAA-001 gate passed), both IFC-1 human-verified.

---

### III.4 Place 4 — Papahānaumokuākea Marine National Monument

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | GeoNames | Northwestern Hawaiian Islands · fcode: MAR (marine area) | S-3; DD-GEONAMES-001 Art. 2 |
| **Crosswalk** | Wikidata | Q1311349 | DD-WIKIDATA-001 §VI.3 |
| **Biological evidence** | GBIF | Neomonachus schauinslandi (Hawaiian monk seal), Chelonia mydas, Phoebastria immutabilis (Laysan albatross), Hawaiian coral endemics | SA-GBIF-001 — occurrence count capped at 100 |
| **Orbital/EO imagery** | NASA | Northwestern Hawaiian Islands ISS imagery; Pacific atoll orbits | DD-NASA-001; § 105 |
| **Marine imagery** | NOAA | NOAA Pacific marine life, Hawaiian coral reef collections; NOAA PIFSC (Pacific Islands Fisheries Science Center) — federal-employee images only | DD-NOAA-001; SA-NOAA-001 §I.1 Gate |
| **Place display** | OSM tile service | Atoll chain and monument boundary | DD-OSM-001 Art. 3 |
| **Attribution** | GeoNames + NASA + NOAA | CC BY 4.0; NASA nonendorsement; NOAA nonendorsement | |

**Papahānaumokuākea content verdict:** Pilot place fills Pacific geographic gap identified in Institution Coverage Audit v1. The Hawaiian monk seal and Laysan albatross are Priority Illustrator-era subjects present in BHL (Rothschild's Avifauna of Laysan). NOAA PIFSC imagery provides contemporary scientific context. NASA provides the orbital perspective for this remote monument.

**Minimum viable asset set:** 1× NASA EO (Pacific atoll) + 1× NOAA PIFSC marine life (gate confirmed), both IFC-1 human-verified.

---

### III.5 Place 5 — Venice

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | GeoNames | geonames_id: 3164603 · fcode: PPLA (administrative capital of Venice Province) | S-3; DD-GEONAMES-001 Art. 2 |
| **Crosswalk** | Wikidata | Q641 | DD-WIKIDATA-001 §VI.3 |
| **Biological evidence** | GBIF | Phalacrocorax carbo (cormorant, lagoon), Ardea cinerea (grey heron), Mugil cephalus (lagoon mullet) | SA-GBIF-001 — occurrence count capped at 100 |
| **Orbital imagery** | NASA | NC-NASA-025 "Mediterranean Dusk" (ISS-Med) · NC-NASA-018 "Mount Etna Ash" (EO-Etna) as Italian context | DD-NASA-001; § 105 |
| **Cultural content** | Pending | Met, AIC, CMA, SMK — all pending ratification; Venetian masters (Canaletto, Bellini, Titian) require art museum content pipeline | DDs pending ratification |
| **Place display** | OSM tile service | Venice lagoon and canal system boundary | DD-OSM-001 Art. 3 |
| **Attribution** | GeoNames + NASA | CC BY 4.0; NASA nonendorsement | |

**Venice content verdict: CONDITIONAL — weakest pilot place at launch.** Venice's commercial identity is cultural (Canaletto's vedute, Bellini's altarpieces, Titian's portraits) — not orbital imagery. The art museum institutions that hold this content (Met #7, AIC #8, CMA #9) are all pending ratification. NASA Mediterranean imagery provides only contextual coverage; it does not satisfy Venice's primary illustration demand.

**Pilot recommendation:** Venice launches as a **partial pilot place** — identity and evidence layers complete, content layer limited to NASA contextual assets until art museum DD ratifications complete. Venice is not excluded from the pilot; it is flagged as content-thin at launch. This is noted explicitly in §VII (Launch Gates) as a Venice-specific condition.

**Minimum viable asset set (partial):** 1× NASA Mediterranean contextual asset (IFC-1 verified). Full content loading deferred to post-ratification art museum sprint.

---

### III.6 Place 6 — Galápagos Islands

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | GeoNames | geonames_id: 2759969 · fcode: ISLS (islands) · country: EC | S-3; DD-GEONAMES-001 Art. 2 |
| **Crosswalk** | Wikidata | Q25479 | DD-WIKIDATA-001 §VI.3 |
| **Biological evidence** | GBIF | Geospiza magnirostris (large ground finch), Conolophus subcristatus (land iguana), Chelonoidis niger (giant tortoise), Amblyrhynchus cristatus (marine iguana) — Darwin's taxa | SA-GBIF-001 — occurrence count capped at 100 |
| **Orbital imagery** | NASA | NC-NASA-042 "Galapagos Islands" (EO-Galapagos) · NC-NASA-043 "Tortoise Habitat" (EO-Isabela, Albemarle Island) | DD-NASA-001; § 105 |
| **Natural history content** | BHL (existing) | Darwin's Voyage of the Beagle plates; Gould's Birds of the Galápagos (contributor to Darwin's Beagle specimens) | BHL pipeline; existing NC source |
| **Place display** | OSM tile service | Island group geometry | DD-OSM-001 Art. 3 |
| **Attribution** | GeoNames + NASA | CC BY 4.0; NASA nonendorsement | |

**Galápagos content verdict:** Strongest natural history pilot place. The Galápagos Islands are the most illustration-rich location in NC's entire catalog — Darwin's Beagle voyage (1831–1836) produced the defining natural history illustrations of the 19th century. GBIF occurrence evidence for Darwin taxa (finches, iguanas, giant tortoises) provides the richest place-relevance scoring signal of any pilot place. NASA EO imagery covers both the archipelago and Isabela Island specifically. BHL's existing pipeline holds the Gould/Darwin plates that are NC's canonical golden-age content for this place.

**Minimum viable asset set:** 1× NASA EO (NC-NASA-042) + 1× BHL natural history plate (Darwin/Gould Galápagos species), both IFC-1 human-verified.

---

### III.7 Place 7 — Earthrise (Cosmic Anchor)

| Layer | Source | Data | Governance |
|---|---|---|---|
| **Identity** | SPECIAL — see §IX.1 | Cosmic anchor: Earth/Moon orbital perspective; no GeoNames terrestrial entry | S-3 provisional exception — see §IX.1 |
| **Crosswalk** | Wikidata | Q1163059 (Earthrise, the photograph) | DD-WIKIDATA-001 §VI.3 |
| **Evidence** | N/A | No biological or geographic occurrence scoring applicable to lunar orbit | — |
| **Primary asset** | NASA | NC-NASA-002 "Earthrise" (AS08-14-2383) · Apollo 8 · December 24, 1968 · photographer: William Anders | DD-NASA-001; § 105 |
| **Supporting asset** | NASA | NC-NASA-001 "The Blue Marble" (AS17-148-22727) · Apollo 17 · December 7, 1972 | DD-NASA-001; § 105 |
| **Place display** | None applicable | No terrestrial boundary to display | — |
| **Attribution** | NASA | "Image credit: NASA. NASA does not endorse this product." | DD-NASA-001; nonendorsement doctrine |

**Earthrise content verdict:** Highest COS potential of any pilot asset. AS08-14-2383 is the most commercially significant single image in the NC catalog — the foundational conservation image of the 20th century. It is clean under § 105 with no rights complexity. Attribution is simple. The governance challenge is the place anchor: Earthrise has no GeoNames terrestrial feature. See §IX.1 for the cosmic anchor exception.

**Minimum viable asset set:** NC-NASA-002 "Earthrise" (AS08-14-2383), IFC-1 human-verified. Single-asset place by design.

---

## IV. Attribution Obligation Matrix

### IV.1 Per-Institution Attribution Requirements

All attribution obligations are cumulative. A single place page may carry multiple attribution requirements simultaneously.

| Source | Attribution required? | Governing authority | Mandatory form | Surfaces |
|---|---|---|---|---|
| **NASA** | Yes — nonendorsement policy | DD-NASA-001 | "Image credit: NASA. NASA does not endorse this product." | Product label · asset page · print packaging |
| **NOAA** | Yes — nonendorsement policy | DD-NOAA-001 §II.5 | "Credit: NOAA/[Division]" or "Image: NOAA" | Asset page · product metadata |
| **NARA** | Advisory | DD-NARA-001 §II.3 | "National Archives [catalog number]" | Provenance record · asset page |
| **MIA** | Institutional credit | DD-MIA-001 | "Minneapolis Institute of Art" | Asset page · product metadata |
| **GeoNames** | **Yes — CC BY 4.0** | DD-GEONAMES-001 Art. 3 | "Geographic data © GeoNames (geonames.org) — CC BY 4.0" | Place page footer · place API response · IIIF `requiredStatement` |
| **Wikidata** | No — CC0 | DD-WIKIDATA-001 §III.1 | — | — |
| **GBIF** | Advisory (CC0 Backbone) | SA-GBIF-001 §4.4 | GBIF citation for bulk download use | Provenance record |
| **OSM** | **Yes — ODbL produced works** | DD-OSM-001 Art. 7 | "© OpenStreetMap contributors" | Any page/product rendering OSM tiles |

### IV.2 Attribution Stacking by Place

For each pilot place page, the following attributions are active simultaneously:

| Place | GeoNames (CC BY) | NASA | NOAA | OSM (map) | Net attribution count |
|---|---|---|---|---|---|
| Yellowstone | ✓ | ✓ | — | ✓ | 3 |
| Grand Canyon | ✓ | ✓ | — | ✓ | 3 |
| Great Barrier Reef | ✓ | ✓ | ✓ | ✓ | 4 |
| Papahānaumokuākea | ✓ | ✓ | ✓ | ✓ | 4 |
| Venice | ✓ | ✓ | — | ✓ | 3 |
| Galápagos | ✓ | ✓ | — | ✓ | 3 |
| Earthrise | — | ✓ | — | — | 1 |

### IV.3 Attribution Implementation Rules

**Rule ATT-1 — Place page footer.** Every place page that displays GeoNames-sourced data must include a persistent data sources footer: "Geographic data © GeoNames (geonames.org) — CC BY 4.0". This is a SA-GEONAMES-001 prerequisite gate.

**Rule ATT-2 — Map tile display.** Every page that renders OSM-based map tiles must display "© OpenStreetMap contributors" adjacent to or overlaid on the map. This is a SA-OSM-001 prerequisite gate.

**Rule ATT-3 — Asset-level NASA attribution.** Every product, product listing, and product print derived from a NASA image must carry the nonendorsement line. This is enforced at the `media_rights` record level — the governed attribution string is stored alongside the rights_status.

**Rule ATT-4 — Asset-level NOAA attribution.** Every NOAA-sourced image in NC must carry NOAA attribution in the asset page metadata. NOAA attribution is not required on print products unless the product's marketing copy references NOAA by name.

**Rule ATT-5 — NARA attribution.** NARA attribution is not legally required but is NC's standard practice for provenance integrity. NARA catalog numbers must appear in `source_item` provenance fields.

**Rule ATT-6 — Attribution cannot substitute for rights clearance.** Carrying attribution for a source does not mean the asset is rights-cleared. Attribution is a separate obligation from IFC-1 rights verification. Both must be satisfied independently.

---

## V. Product-Safe Asset Selection

### V.1 Product-Safety Test

An asset is **product-safe** — eligible for activation and commercial sale — if and only if all six conditions are satisfied:

| Gate | Condition | Authority |
|---|---|---|
| **P-1 Rights status** | `media_rights.rights_status = 'verified_pd'` | IFC-1; Foundation Model Constitution FM-4 |
| **P-2 Human verification** | `media_rights.human_verified = TRUE` | Foundation Model Constitution FM-4 |
| **P-3 Activation status** | `activation_target.status = 'activated'` | IFC v1 Art. 7 |
| **P-4 Nonendorsement compliance** | Product copy reviewed; no federal endorsement claim | DD-NASA-001; DD-NOAA-001; DD-NARA-001 |
| **P-5 Attribution implementable** | All required attribution strings are present and deployable on the product and its page | DD-GEONAMES-001 Art. 3; DD-OSM-001 Art. 7 |
| **P-6 Source gate passed** | Rights gate specific to source institution confirmed | SA-NOAA-001 (NOAA); DD-NARA-001 §II.2 (NARA); DD-MIA-001 (MIA) |

### V.2 Product-Safe Asset Inventory by Source

**NASA (all pilot places):**
- All NASA images from the Pilot 75 plan are product-safe by definition: 17 U.S.C. § 105 federal works are PD at creation. No per-record rights clearance is needed beyond confirming the NASA ID matches an actual federal work.
- Product-safety gate for NASA: confirm asset is published on images.nasa.gov or the NASA Image and Video Library under a NASA-attributed record. No third-party credit indicators.
- Blocked assets: any NASA page image with a third-party photographer credit (e.g., "Photo: [Name]/NASA") — the copyright rests with the photographer, not NASA.

**NOAA (Great Barrier Reef, Papahānaumokuākea):**
- Product-safe: Flickr license integer ∈ {7, 8} AND credit field contains "NOAA", "NOAA/OAR", "NOAA/NMFS", "NOAA/NOS", "NOAA/PIFSC", or predecessor agency ("ESSA", "USCGS", "Bureau of Commercial Fisheries") — no personal name in credit.
- Blocked (pilot): all REVIEW_REQUIRED records — personal name in credit, "[Name]/NOAA" pattern, international partner credits, "Courtesy of" — receive 0 pilot writes per DD-NOAA-001 Sprint 3 authorization.
- Blocked (permanent): all records failing SA-NOAA-001 §I.1 license gate.

**NARA (Yellowstone, Grand Canyon):**
- Product-safe: `useRestriction.status == "Unrestricted"` on the NARA catalog record. This is the sole gate; no secondary rights check is required for confirmed federal expedition records.
- Blocked: any NARA record with any other `useRestriction.status` value, or any record where the creator is not a federal employee (donated materials, presidential records, purchased commercial content).

**MIA (Venice — partial):**
- Product-safe: `rights_type` field passes SA-MIA-RIGHTS-001 gate. `restricted=0` alone is NOT sufficient — the DD-MIA-001 critical finding applies. The gate is `rights_type`, not `restricted`.
- Venice-specific: MIA holdings for Venice content are likely limited. MIA product-safety must be confirmed per-record; no batch assumption applies.

### V.3 Asset Tier Assignment

Assets passing the product-safety test receive CSM tier assignment per the Commerce Intelligence Constitution v1.2:

| Asset | Expected tier | Basis |
|---|---|---|
| Earthrise (AS08-14-2383) | MASTERWORK | Highest cultural significance; unique single-image conservation icon |
| Blue Marble (AS17-148-22727) | MASTERWORK | Co-equal planetary significance |
| Yellowstone from Orbit | FLAGSHIP | National park + orbital significance |
| GBR Whitsundays (ISS) | FLAGSHIP | Marine park + biological richness |
| Grand Canyon Depth (ASTER) | FLAGSHIP | Geologic significance + NARA cartographic pairing |
| Galápagos EO | FLAGSHIP | Highest GBIF biological evidence score in pilot |
| NARA Hayden Survey maps | FLAGSHIP to MASTERWORK | Historical significance; rarity; direct founding document status |
| NOAA coral reef imagery | STANDARD | Scientific but not Golden Age illustration; high place relevance |
| All other pilot assets | STANDARD to FLAGSHIP | Per CI Constitution scoring formula |

Tier assignments are advisory at launch. CI Constitution formula produces the final COS; tiers follow.

---

## VI. Commercial-Use Boundaries

### VI.1 Universal Boundaries (All Pilot Places)

The following boundaries apply to every product sold through the pilot regardless of source institution:

**Boundary C-1 — PD-only commercial inventory.** No product may enter commercial sale without `rights_status = 'verified_pd'` on its underlying asset. This is IFC-1 and is not subject to exception.

**Boundary C-2 — Federal nonendorsement.** Products incorporating NASA, NOAA, or NARA imagery may not claim US government endorsement, affiliation, or approval. The nonendorsement line is required in product metadata; it must not be suppressed in any distribution channel (NC website, partner API, third-party marketplace).

**Boundary C-3 — GeoNames attribution cannot be suppressed.** Any product or product page that includes GeoNames-sourced place data must carry CC BY 4.0 attribution. Attribution suppression — including suppression for aesthetic reasons on printed products — is a licensing compliance violation under DD-GEONAMES-001 Art. 3.

**Boundary C-4 — OSM data never in products.** No product metadata, packaging, or digital download may include OSM-sourced geometry or place data. OSM attribution ("© OpenStreetMap contributors") applies only to map tile display on web pages; it does not attach to print products unless those products incorporate rendered map imagery.

**Boundary C-5 — No GBIF evidence in consumer-facing copy.** GBIF occurrence data is internal evidence metadata. `gbif_occurrence_count`, `place_relevance_score`, and related fields are commercial intelligence inputs; they are not consumer-facing product copy.

### VI.2 Source-Specific Boundaries

| Source | Permitted commercial use | Hard boundary |
|---|---|---|
| NASA | Sale of products incorporating NASA images; no restriction on product types | No federal endorsement claim; no NASA logo/seal/insignia on products |
| NOAA | Sale of products incorporating confirmed § 105 NOAA images | No federal endorsement claim; REVIEW_REQUIRED images excluded from pilot products |
| NARA | Sale of products incorporating Unrestricted federal records | No NARA-restricted records; no claim of NARA reproduction rights |
| MIA | Sale of products incorporating `rights_type`-cleared MIA records | `restricted=0` alone insufficient; `rights_type` gate required |
| GeoNames | Use of GeoNames data on commercial place pages and in commercial API | Attribution required; no claim that NC is GeoNames or licensed by GeoNames |
| Wikidata | Use of Wikidata entity data in commercial pipeline | CC0 — no restrictions; rights exclusion invariant W-4 active |
| GBIF | Internal scoring use only | No GBIF media in products; `"validation_only"` source role immutable |
| OSM | Map tile display on commercial place pages | No OSM geometry or data in products, databases, or APIs |

### VI.3 The Earthrise Commercial Opportunity

Earthrise (AS08-14-2383) represents NC's highest-value pilot asset. Its commercial boundaries are simple:
- § 105 confirms PD — no copyright
- NOAA nonendorsement does not apply (NASA asset)
- Attribution: "Image credit: NASA. NASA does not endorse this product."
- No GeoNames CC BY obligation (cosmic anchor — no terrestrial place data)
- No OSM obligation (no map tile display for Earthrise)

**Net result:** Earthrise is the pilot's most commercially unencumbered flagship asset. The only binding constraint is the NASA nonendorsement line, which is a one-sentence label requirement.

---

## VII. Launch Gates

### VII.1 Pre-Launch Gates — By Category

Pilot launch is blocked until all applicable gates are confirmed. Gates are organized by category; each must be checked and confirmed in sequence.

**Category A — Identity Infrastructure Gates (all places)**

| Gate | Condition | Authority | Status |
|---|---|---|---|
| A-1 | GeoNames ID confirmed for each pilot place (6 terrestrial) | DD-GEONAMES-001 Art. 2; S-3 | ☐ |
| A-2 | Wikidata QID resolved and resolution_date recorded for each place | DD-WIKIDATA-001 Invariant W-7 | ☐ |
| A-3 | Feature codes verified — each place has a confirmed GeoNames fcode | DD-GEONAMES-001 Invariant GN-2 | ☐ |
| A-4 | Earthrise cosmic-anchor exception documented (see §IX.1) | NC-PILOT-001 §IX.1 | ☐ |

**Category B — Attribution Implementation Gates**

| Gate | Condition | Authority | Status |
|---|---|---|---|
| B-1 | GeoNames CC BY 4.0 attribution present on all 6 terrestrial place pages | DD-GEONAMES-001 §XII.2; **SA-GEONAMES-001 prerequisite** | ☐ |
| B-2 | OSM attribution "© OpenStreetMap contributors" present on all map tile displays | DD-OSM-001 Art. 7; **SA-OSM-001 prerequisite** | ☐ |
| B-3 | NASA nonendorsement line present on all NASA-sourced product listings | DD-NASA-001; Rule ATT-3 | ☐ |
| B-4 | NOAA nonendorsement line present on all NOAA-sourced asset pages | DD-NOAA-001 §II.5; Rule ATT-4 | ☐ |
| B-5 | NARA attribution present in provenance records for NARA-sourced assets | DD-NARA-001 §II.3; Rule ATT-5 | ☐ |

**Category C — Rights Clearance Gates (per place)**

| Gate | Condition | Authority | Status |
|---|---|---|---|
| C-1 | Yellowstone: ≥1 NASA Asset Zero + ≥1 NARA Asset Zero, both IFC-1 human-verified | IFC v1; DD-NASA-001; DD-NARA-001 | ☐ |
| C-2 | Grand Canyon: ≥1 NASA Asset Zero + ≥1 NARA Asset Zero, both IFC-1 human-verified | IFC v1; DD-NASA-001; DD-NARA-001 | ☐ |
| C-3 | Great Barrier Reef: ≥1 NASA Asset Zero + ≥1 NOAA Asset Zero (SA-NOAA-001 gate confirmed), both IFC-1 human-verified | IFC v1; DD-NASA-001; DD-NOAA-001; SA-NOAA-001 | ☐ |
| C-4 | Papahānaumokuākea: ≥1 NASA Asset Zero + ≥1 NOAA PIFSC Asset Zero, both IFC-1 human-verified | IFC v1; DD-NASA-001; DD-NOAA-001 | ☐ |
| C-5 | Venice: ≥1 NASA contextual Asset Zero, IFC-1 human-verified; content-thin notation recorded | IFC v1; DD-NASA-001; NC-PILOT-001 §III.5 | ☐ |
| C-6 | Galápagos: ≥1 NASA Asset Zero + ≥1 BHL natural history plate, both IFC-1 human-verified | IFC v1; DD-NASA-001 | ☐ |
| C-7 | Earthrise: NC-NASA-002 (AS08-14-2383) IFC-1 human-verified; cosmic-anchor exception documented | IFC v1; DD-NASA-001; §IX.1 | ☐ |

**Category D — Standards Amendment Gates**

| Gate | Condition | Authority | Status |
|---|---|---|---|
| D-1 | SA-GEONAMES-001 ratified | DD-GEONAMES-001 Art. 13; §XII.1 | ☐ |
| D-2 | SA-OSM-001 ratified | DD-OSM-001 Art. 10 | ☐ |
| D-3 | SA-NOAA-001 ratified (already RATIFIED per DD-NOAA-001) | DD-NOAA-001 | ☑ |
| D-4 | SA-NOAA-002 ratified (already RATIFIED per DD-NOAA-001) | DD-NOAA-001 | ☑ |
| D-5 | SA-GBIF-001 ratified (already RATIFIED per DD-GBIF-001) | DD-GBIF-001 | ☑ |

**Category E — Two-Human Activation Gate**

| Gate | Condition | Authority | Status |
|---|---|---|---|
| E-1 | Rights verifier #1 has confirmed IFC-1 for all pilot Asset Zero records | IFC v1 | ☐ |
| E-2 | Principal Architect has confirmed activation authorization for each pilot place | IFC v1; NC-PILOT-001 ratification | ☐ |

### VII.2 Blocking vs. Non-Blocking Gates

| Category | Blocking for public launch? | Can proceed in staging? |
|---|---|---|
| A (Identity) | Yes — all gates block | A-1 through A-3 can be resolved in staging |
| B (Attribution) | **Yes — all gates block public launch** | Can be developed in staging |
| C (Rights clearance) | Yes — each place blocks independently | Can be cleared incrementally per place |
| D-1, D-2 (SAs pending) | **Yes — block public launch** | Can be tested in staging before ratification |
| D-3, D-4, D-5 (ratified) | No — already satisfied | — |
| E (Two-human activation) | Yes — required for activation | Cannot be bypassed |

### VII.3 Partial Launch Authorization

Places may launch independently as their own gates clear. The pilot does not require all seven places to launch simultaneously:

- Yellowstone and Grand Canyon can launch together (same source types: NASA + NARA)
- Great Barrier Reef and Papahānaumokuākea can launch together (same source types: NASA + NOAA)
- Earthrise can launch as a single-asset standalone the moment C-7 and D-3/D-4 are confirmed — it has the fewest dependencies
- Galápagos can launch with BHL + NASA whenever C-6 is cleared
- Venice launches partial (NASA only) and upgrades to full when art museum DDs are ratified

**Recommended launch sequence:** Earthrise → Yellowstone + Grand Canyon → Galápagos → Great Barrier Reef + Papahānaumokuākea → Venice (partial) → Venice (full, post-museum ratification).

---

## VIII. Pilot Success Metrics

### VIII.1 Rights Compliance Metrics (Zero Tolerance)

| Metric | Target | Measurement |
|---|---|---|
| IFC-1 compliance rate | 100% of activated assets pass rights gate | Audit of `media_rights.rights_status` across all pilot activation_target records |
| FM-4 compliance | 0 assets with FM-only rights determination | Audit of `human_verified` flag on all pilot `media_rights` records |
| NOAA gate compliance | 0 REVIEW_REQUIRED records in pilot products | Audit of SA-NOAA-001 gate status on all NOAA source records |
| NARA gate compliance | 0 non-Unrestricted records in products | Audit of `useRestriction.status` on all NARA source records |
| Federal endorsement violations | 0 endorsement claims in any product copy | Manual review of all product listings for NASA/NOAA/NARA names with endorsement framing |

### VIII.2 Attribution Compliance Metrics

| Metric | Target | Measurement |
|---|---|---|
| GeoNames CC BY attribution | Present on 100% of public place pages (6 terrestrial places) | Automated spot-check of `<footer>` or attribution component on each place page URL |
| OSM attribution | Present on 100% of map tile displays | Automated check of "© OpenStreetMap contributors" presence on pages with map tile elements |
| NASA nonendorsement line | Present on 100% of NASA-sourced product listings | Audit of product metadata for governed attribution string |
| NOAA nonendorsement line | Present on 100% of NOAA-sourced asset pages | Audit of asset page metadata |
| Attribution audit score | Pass on all 6 attribution categories above | Combined score; any failure blocks scale authorization |

### VIII.3 Commercial Performance Metrics (90-Day Pilot)

| Metric | Baseline | Target | Notes |
|---|---|---|---|
| Activated assets | 0 | ≥7 (≥1 per pilot place) | Minimum one product-safe activated asset per place |
| Product listings live | 0 | ≥7 | One activated product per place minimum |
| First commercial transaction | 0 | ≥1 | Any pilot place, any product type |
| Earthrise product revenue | 0 | Lead indicator | Earthrise is the highest-COS asset; its first sale validates the federal-works commercial model |
| Place page views (organic) | 0 | Measured, not targeted | Establishes baseline for v0.5.0 scale decisions |
| GBIF evidence score coverage | 0% | ≥80% of pilot place-taxon pairs have `gbif_taxon_key` resolved | SA-GBIF-001 evidence policy in effect |

### VIII.4 Governance Health Metrics

| Metric | Target | Notes |
|---|---|---|
| Pending SA ratifications | SA-GEONAMES-001 and SA-OSM-001 ratified within 30 days of pilot launch | These are attribution infrastructure; their absence blocks scale |
| Earthrise cosmic-anchor amendment | Standards Constitution amendment drafted within 60 days of pilot launch | §IX.1 provisional exception is time-limited |
| Venice content upgrade | At least one art museum DD ratified within pilot period | Unblocks Venice from content-thin status |
| NOAA Path B evaluation | Sprint 1 Photo Library access path evaluation completed | DD-NOAA-001 Article 11 prerequisite for Sprint 2 production |
| Rights audit clean | 0 governance violations detected in 30-day post-launch rights audit | Formal audit by Principal Architect |

---

## IX. Special Cases

### IX.1 Earthrise — Cosmic Anchor Exception

**The governance problem:** Standards Constitution v1.0 Invariant S-3 requires every NC place entity to have a GeoNames ID. GeoNames is a terrestrial gazetteer. The Moon — the foreground of the Earthrise photograph — has no GeoNames entry in the standard feature hierarchy. The Earth as a whole-planet perspective is not a GeoNames geographic feature.

**Provisional resolution (pilot scope):** Earthrise is activated as a **cosmic anchor** — a special place classification not governed by S-3's terrestrial requirement. The cosmic anchor is provisionally defined as:

```
place_type: 'cosmic_anchor'
place_name: 'Earth/Moon Orbital Perspective'
geonames_id: NULL  ← S-3 provisional exception, documented
wikidata_qid: Q1163059  ← Earthrise photograph Q-item
cosmic_anchor_note: 'Non-terrestrial perspective; S-3 exception authorized by NC-PILOT-001 §IX.1'
```

This provisional exception is time-limited. Within 60 days of pilot launch, the Principal Architect must either:
1. Draft a Standards Constitution amendment defining the `cosmic_anchor` place type formally (adding it as a fifth fclass alongside the GeoNames hierarchy, exempt from S-3's geonames_id requirement), **or**
2. Assign a GeoNames ID for a valid proxy place (e.g., the Pacific Ocean — the ocean surface visible in the Earthrise photograph — as the terrestrial anchor), which satisfies S-3 without requiring a constitutional amendment

If neither condition is satisfied within 60 days, Earthrise is demoted from canonical place status to a promotional/standalone asset without a place page anchor, pending resolution.

**What this exception does NOT affect:** Earthrise as an asset is product-safe regardless of the cosmic anchor resolution. The § 105 rights clearance, the NASA attribution requirement, and the IFC-1 gate are all independent of the place governance question. Earthrise can be sold from a product page even if the place anchor governance is unresolved — it simply does not appear on a "place" page until the anchor is established.

### IX.2 Venice — Content Layer Gap

Venice's primary commercial identity (Venetian vedute, 16th–18th century masters, lagoon natural history) is held by art museums whose DDs are pending ratification. This gap is structural at pilot launch.

**Documentation requirement:** The Venice place page at launch must carry an internal notation: `content_status: 'partial — art museum pipeline pending'`. This notation is operational, not consumer-facing. It triggers automatic upgrade review when the first applicable art museum DD (Met #7, AIC #8, CMA #9) is ratified.

**What Venice CAN deliver at launch:** GeoNames identity, Wikidata QID, GBIF lagoon-species evidence, and NASA Mediterranean contextual imagery. A Venice place page is valid at launch — it is simply content-thin.

### IX.3 NOAA Pilot Scope Restriction

DD-NOAA-001 Sprint 3 authorization limits NOAA pilot writes:
- ALLOWED records → 7 writes maximum (pilot cap)
- REVIEW_REQUIRED → 0 writes (pilot exclusion, NASA model)
- Personal name in credit → permanent hard block

This restriction applies to Great Barrier Reef and Papahānaumokuākea NOAA assets. The pilot cap does not prevent NOAA from becoming a full production source in Sprint 4; it governs the pilot sprint specifically.

### IX.4 Overture Maps — Pending DD

DD-OSM-001 OQ-3 identified Overture Maps Foundation (CC BY 4.0, no share-alike) as a potential future source for polygon geometry storage in the `places` table. If DD-OVERTURE-001 is ratified before the pilot's public launch, the OSM tile-only constraint for boundary display could be upgraded to stored polygon geometry from Overture Maps, eliminating the OSM-produced-works dependency for place pages.

This is a future optimization, not a pilot prerequisite. DD-OVERTURE-001 is not on the critical path for pilot launch.

---

## X. Decision Articles

**Article 1 — Pilot Authorization.** The seven-place commercial pilot (Yellowstone, Grand Canyon, Great Barrier Reef, Papahānaumokuākea, Venice, Galápagos, Earthrise) is authorized to proceed subject to the conditions in §VII. Partial launch per §VII.3 is authorized — places may launch independently as their gates clear.

**Article 2 — Governing Authority Chain.** NC-PILOT-001 is subordinate to all constitutions and individual DDs listed in §I. Conflicts between this blueprint and a higher-authority document are resolved in favor of the higher authority.

**Article 3 — IFC-1 Non-Negotiable.** The IFC-1 hard gate applies without exception across all seven pilot places and all source institutions. No product may enter commercial sale without `rights_status = 'verified_pd'` and `human_verified = TRUE`. FM-4 is active.

**Article 4 — Federal Nonendorsement Doctrine.** Products incorporating NASA, NOAA, or NARA imagery must carry the governed nonendorsement line. No product copy, marketing material, or UI element may claim US government endorsement. This doctrine applies to all three federal institutions simultaneously and cannot be satisfied by satisfying only one.

**Article 5 — Attribution Is Not Optional.** GeoNames CC BY 4.0 attribution and OSM ODbL produced-works attribution are licensing obligations, not styling preferences. SA-GEONAMES-001 and SA-OSM-001 ratification gates (D-1, D-2) block public launch. Attribution compliance is a zero-tolerance metric (§VIII.2).

**Article 6 — NOAA Pilot Restriction.** NOAA pilot assets are governed by DD-NOAA-001 Sprint 3 authorization: ALLOWED records only, 7-write pilot cap, REVIEW_REQUIRED records excluded. This restriction is not waivable within the pilot period.

**Article 7 — Earthrise Cosmic Anchor.** The S-3 provisional exception for Earthrise is authorized for the pilot period. The Standards Constitution amendment or proxy-place resolution (§IX.1) must be completed within 60 days of pilot launch. Earthrise's commercial sale authorization is independent of this governance question.

**Article 8 — Venice Partial Designation.** Venice launches as a content-thin pilot place. This is not a disqualification. The Venice `content_status: 'partial'` notation is required. Upgrade is triggered automatically upon first art museum DD ratification.

**Article 9 — OSM Data Prohibition Active.** DD-OSM-001 Invariants OS-1 through OS-5 are in full effect for the pilot. No OSM geometry or data enters any NC canonical table during the pilot or after. The tile-service produced-works path is the sole authorized OSM use.

**Article 10 — Success Metrics Are Governance.** The metrics in §VIII are not aspirational targets — they are governance commitments. The zero-tolerance rights compliance and attribution metrics constitute the minimum standard for declaring the pilot a governance success. Commercial performance metrics (§VIII.3) are supplementary. A pilot that achieves commercial performance but fails rights or attribution compliance is not a governance success.

**Article 11 — Pilot Upgrade Path.** The pilot is designed for incremental upgrade: additional places, additional institutions, and additional asset types may be added per place as pending DDs are ratified. Each upgrade follows the IFC v1 onboarding path. Venice's upgrade from partial to full is the first planned upgrade event.

---

## XI. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☑ APPROVE WITH CONDITIONS | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-PILOT-001 — drafted 2026-06-11*  
*Authority: DD-NASA-001 · DD-NOAA-001 · DD-GBIF-001 · DD-WIKIDATA-001 · DD-GEONAMES-001 · DD-OSM-001 · DD-NARA-001 · DD-MIA-001*  
*Standards: IFC v1 · Standards Constitution v1.0 · CI Constitution v1.2 · Foundation Model Constitution v1.0*  
*Decision: APPROVE WITH CONDITIONS — SA-GEONAMES-001 · SA-OSM-001 required before public launch · Earthrise cosmic-anchor exception authorized for pilot period · Venice launches content-thin*
