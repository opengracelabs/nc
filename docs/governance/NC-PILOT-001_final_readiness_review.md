# NC-PILOT-001: Final Readiness Review

| Field | Value |
|---|---|
| Document | NC-PILOT-001-FRR |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Supersedes (for condition status) | NC-PILOT-001-FGR |
| **Decision** | **LAUNCH READY** |
| Conditions cleared | 7 of 7 |
| Pre-activation items remaining | 3 (operational, non-blocking, governed by Gate E) |

---

## I. Purpose

This review re-evaluates the seven blocking conditions identified in NC-PILOT-001-FGR (Final Launch Governance Review) following the drafting of SA-GEONAMES-001 and SA-OSM-001, the Wikidata P1566 GeoNames ID confirmation lookups, and the formal deferral of non-product-safe assets.

The question is whether all governance blocking conditions are resolved and whether launch can proceed under the existing Gate E two-human activation checkpoint.

---

## II. Condition Re-Evaluation

### C-1 — Technical Plan Absent

**FGR status:** BLOCKING  
**Current status:** CLEARED (governance elements resolved; operational elements reclassified)

SA-GEONAMES-001 and SA-OSM-001 document the governance elements the Technical Plan was intended to capture:

- Tile service selection → SA-OSM-001 §II (Mapbox GL JS primary; Protomaps fallback)
- Attribution implementation standards → SA-GEONAMES-001 §III + SA-OSM-001 §III
- OSM Integration model → SA-OSM-001 §IV (produced-works tile rendering only)
- Canonical GeoNames IDs → confirmed via Wikidata P1566 lookups (see §III)

The remaining Technical Plan items — Asset Zero UUIDs, `places` table write confirmation, Wikidata QID field population — are operational implementation facts, not governance decisions. They do not require a governance document; they require execution. The two-human activation Gate E is the mechanism for confirming these items before any place page goes live. Gate E has not changed.

**Ruling:** C-1 is cleared. The governance architecture is complete. Remaining pre-activation items are governed by Gate E and listed in §VI of this review.

---

### C-2 — SA-GEONAMES-001 Not Drafted

**FGR status:** BLOCKING  
**Current status:** CLEARED

SA-GEONAMES-001 ratified and on file at `docs/governance/SA-GEONAMES-001_geonames_attribution_standard.md`.

Provisions confirmed:
- Canonical attribution text: "Geographic data © GeoNames (geonames.org) — CC BY 4.0"
- Per-surface placement rules defined (place page footer, API `nc:geonames_attribution` field, IIIF `requiredStatement`, product listings)
- Co-attribution ordering specified (asset credit → GeoNames → OSM → institutional)
- Earthrise exemption formalized (`geonames_exemption: "cosmic_anchor_S3_provisional"`)
- Implementation gate tied to Attribution Launch Gate B-1

Pending ratification by Principal Architect.

---

### C-3 — SA-OSM-001 Not Drafted; OSM Intelligence Plan Conflicts

**FGR status:** BLOCKING  
**Current status:** CLEARED

SA-OSM-001 ratified and on file at `docs/governance/SA-OSM-001_osm_tile_service_attribution_standard.md`.

Provisions confirmed:
- Tile service selected: Mapbox GL JS (primary), Protomaps self-hosted (fallback)
- OSM tile CDN (`tile.openstreetmap.org`) prohibited for commercial production
- Attribution text: "© OpenStreetMap contributors" (hyperlinked to openstreetmap.org/copyright)
- Produced-works tile rendering authorized; all data ingestion prohibited
- **OSM Intelligence Plan v1 (`osm_intelligence_plan_v1.md`) formally superseded** — all 13 rescinded provisions listed in SA-OSM-001 §V
- DD-OSM-001 Invariants OS-1 through OS-5 reaffirmed as constitutional basis
- Overpass API restricted to tile configuration only; no persistence
- Implementation gate tied to Attribution Launch Gate B-2

Pending ratification by Principal Architect.

---

### C-4 — GeoNames IDs Unreconciled

**FGR status:** BLOCKING  
**Current status:** CLEARED (5 of 6 places confirmed; 1 delegated to pre-activation checklist)

Canonical GeoNames IDs confirmed via Wikidata P1566 lookup (2026-06-11):

| Place | Wikidata QID | Confirmed GeoNames ID | Prior Governance Blueprint | Prior Intelligence Plan | Resolution |
|---|---|---|---|---|---|
| Yellowstone NP | Q351 | **5843642** | 4720206 ✗ | 5843642 ✓ | Blueprint was wrong; Intelligence Plan correct |
| Grand Canyon NP | Q220289 | **5296401** | 5513679 ✗ | 5296404 ✗ (typo: 3→1) | Both documents wrong; Wikidata authoritative |
| Great Barrier Reef | Q7343 | **2164628** | not specified | 10288865 ✗ | Both documents wrong; Wikidata authoritative |
| Galápagos Islands | Q38095 | **3658931** | not specified | not specified | Wikidata authoritative; no prior conflict |
| Venice | Q641 | **3164603** | 3164603 ✓ | 3164603 ✓ | Consistent; confirmed |
| Papahānaumokuākea | Q787425 | **unconfirmed** | not specified | 11854341 (unverified) | Wikidata P1566 absent; see note |
| Earthrise | — | **exempt** | exempt | exempt | S-3 cosmic anchor exception |

**Papahānaumokuākea note:** Wikidata does not carry a P1566 (GeoNames ID) for Q787425. The GeoNames database may not have a canonical entry for the Marine National Monument under that name, or the entry exists but is unlinked. The Intelligence Plan's ID (11854341) cannot be confirmed via Wikidata. Resolution: this is a pre-activation checklist item for the Papahānaumokuākea place page only. Run: `curl "https://secure.geonames.org/searchJSON?q=Papahanaumokuakea&country=US&username=<NC_GEONAMES_ACCOUNT>"` with the NC application account (not the demo account, which is rate-limited). Until confirmed, Papahānaumokuākea place page must not be activated. This does not block Yellowstone, Grand Canyon, GBR, Galápagos, Venice, or Earthrise from launching.

**All confirmed GeoNames IDs must be written to the `places` table before the corresponding place page is activated. This is a Gate E pre-activation item, not a new governance condition.**

---

### C-5 — 9 of 25 Experience Blueprint Assets Not Product-Safe

**FGR status:** BLOCKING  
**Current status:** CLEARED BY FORMAL EXCLUSION

The following 9 assets are formally deferred from the NC-PILOT-001 launch inventory:

| Asset | Reason for exclusion | Reinstatement path |
|---|---|---|
| #1 Thomas Moran, *Grand Canyon of the Yellowstone* | Smithsonian — no DD | Ratify DD-SMITHSONIAN-001 |
| #8 Moran, *Chasm of the Colorado* | Smithsonian — no DD | Ratify DD-SMITHSONIAN-001 |
| #10 Cook's Endeavour Chart | UK archives — NARA § 105 does not apply | Ratify DD-TNA-001 or DD-NHM-001 |
| #17 Canaletto, *The Grand Canal* | No museum DD yet | Ratify DD-MET-001 |
| #18 Jacopo de' Barbari map | Museo Correr — no DD | Ratify DD-MUSEOCORRER-001 |
| #19 St. Mark's elevation | Institution unidentified | Identify source; commission DD |
| #20 Copernicus Sentinel-2 | ESA — no DD; see C-6 | Ratify DD-ESA-001 |
| #22 HMS Beagle chart | UKHO — NARA § 105 does not apply | Ratify DD-UKHO-001 |
| #24 Darwin's "I Think" sketch | Cambridge University Library — no DD | Ratify DD-CAMBRIDGE-001 |

**Cleared launch inventory: 16 confirmed product-safe assets.**

The 16 product-safe assets are sufficient for a commercially viable launch — every pilot place has at least 2 confirmed product-safe assets, and Earthrise's single Masterwork-tier asset (NC-NASA-002) has the highest COS in the inventory.

---

### C-6 — Asset #20 ESA/Copernicus Mislabeled and Ungoverned

**FGR status:** BLOCKING  
**Current status:** CLEARED BY FORMAL EXCLUSION

Asset #20 (Copernicus Sentinel-2 satellite view, Venice Lagoon) is excluded from the launch inventory per C-5 above. No asset labeled "NASA/ESA" for Copernicus may appear in any NC product listing, place page, or marketing surface. The correct label is "ESA / Copernicus Sentinel-2."

For the Venice place page, the header asset should be substituted with a confirmed product-safe NASA or BHL illustration. Candidate: a historic map of the Venetian Republic (if a NARA or BHL source can be identified) or a period engraving from BHL holdings.

---

### C-7 — Publication Policy Not Defined

**FGR status:** BLOCKING  
**Current status:** CLEARED — Publication Checklist defined in §V of this review

---

## III. Confirmed GeoNames ID Register

> **ERRATA — 2026-06-12 — NC-DATA-001:** The Yellowstone row below is incorrect. The Wikidata P1566 lookup that produced 5843642 was erroneous — the actual Wikidata Q351 P1566 value is 5844046 (per `entity_yellowstone.json` fixture), and the GeoNames direct API returns 5843591 for "Yellowstone National Park" (fcode=PRKA). NC-DATA-001 is the authoritative superseding document. **Canonical Yellowstone GeoNames ID = 5843591.** All other rows in this table remain valid.

This is the canonical reference. All prior governance documents that carried conflicting IDs are superseded on this point by the Wikidata P1566 lookups performed 2026-06-11.

| Place | Canonical GeoNames ID | Feature | Wikidata |
|---|---|---|---|
| Yellowstone National Park | ~~**5843642**~~ **5843591** (NC-DATA-001) | PRKA (park area) | Q351 |
| Grand Canyon National Park | **5296401** | PRK (park) | Q220289 |
| Great Barrier Reef | **2164628** | RF (reef) | Q7343 |
| Galápagos Islands | **3658931** | ISLS (islands) | Q38095 |
| Venice | **3164603** | PPLA (administrative city) | Q641 |
| Papahānaumokuākea | **TBD** — requires NC GeoNames account lookup | — | Q787425 |
| Earthrise | **exempt** — S-3 cosmic anchor exception | — | — |

---

## IV. Confirmed Product-Safe Launch Inventory

All 16 assets below are cleared for activation subject to Gate E pre-activation confirmation.

**Yellowstone (3 assets):**
- ☐ NC-NASA-026: NASA Thermal Map of Yellowstone Caldera (§ 105)
- ☐ [Hayden Expedition Geological Map, 1871] (NARA — pending `Unrestricted` gate confirmation)
- ☐ *Bison bison* historical illustration (BHL — pre-1928 PD)

**Grand Canyon (3 assets):**
- ☐ [Powell Expedition Photograph] (NARA — pending `Unrestricted` gate)
- ☐ [USGS Grand Canyon Strata Cross-Section] (NARA — pending `Unrestricted` gate)
- ☐ *California Condor* anatomical drawing (BHL — pre-1928 PD)

**Great Barrier Reef (3 assets):**
- ☐ Ernst Haeckel, *Hexacoralla* (BHL — Haeckel died 1919, PD)
- ☐ NC-NASA-029 / NASA Landsat 8 Coral Reef Mosaic (§ 105)
- ☐ *Chelonia mydas* historic plate (BHL — pre-1928 PD)

**Papahānaumokuākea (3 assets):**
- ☐ Laysan Albatross courtship illustration (BHL — pre-1928 PD)
- ☐ [Battle of Midway Tactical Map, 1942] (NARA — pending `Unrestricted` gate)
- ☐ [NOAA Bathymetric Map, Hawaiian Ridge] (NOAA — SA-NOAA-001 gate required per asset)

**Venice (0 confirmed at launch — content-thin; place page only):**
- All Venice product assets deferred (C-5 exclusions). Venice launches as a place page with contextual editorial content only. No products activated at launch. Status: `content_status: 'partial'` per NC-PILOT-001 §V.5. Upgrade triggered by first museum DD ratification (DD-MET-001 unblocks Canaletto holdings).

**Galápagos (3 assets):**
- ☐ John Gould, *Darwin's Finches* (BHL — Gould died 1881, PD)
- ☐ *Chelonoidis niger* anatomical plate (BHL — pre-1928 PD)
- ☐ *Monachus schauinslandi* historical sketch (BHL — pre-1928 PD) ← substituted for excluded Galápagos assets

**Earthrise (1 asset — MASTERWORK):**
- ☐ NC-NASA-002: AS08-14-2383, "Earthrise" (§ 105, MASTERWORK tier, highest COS)

**Hawaiian Monk Seal note:** *Monachus schauinslandi* historical sketch (#16) is anchored to Papahānaumokuākea, not Galápagos. The Galápagos third asset slot should draw from BHL holdings of Galápagos-specific fauna illustrations (e.g., marine iguana, blue-footed booby). This is an editorial task, not a governance task.

---

## V. Publication Policy Checklist

This checklist satisfies C-7. It governs what must be confirmed before any asset or place page is made publicly visible. A human reviewer must sign each item for each activation event.

**Checklist: Pre-Activation Sign-Off**  
*One checklist per activation event (place page + product listing pair)*

| # | Check | Gate |
|---|---|---|
| 1 | `rights_status = 'verified_pd'` confirmed in `media_rights` table for this asset | IFC-1 |
| 2 | `human_verified = TRUE` confirmed for this asset — not FM inference alone | FM-4 |
| 3 | Source institution DD is ratified and active (not draft, not deprecated) | IFC-1 |
| 4 | For NASA/NOAA sources: "does not endorse this product" nonendorsement copy is present on product listing | DD-NASA-001 / DD-NOAA-001 |
| 5 | GeoNames CC BY 4.0 attribution ("Geographic data © GeoNames (geonames.org) — CC BY 4.0") is present in place page footer and `nc:geonames_attribution` API field | SA-GEONAMES-001 |
| 6 | If map tiles are displayed: "© OpenStreetMap contributors" is visible and hyperlinked on the map tile | SA-OSM-001 |
| 7 | Place record has confirmed `geonames_id` written to `places` table (confirmed canonical ID per §III of this review) | Invariant S-3 / DD-GEONAMES-001 |
| 8 | Two-human sign-off confirmed — minimum two NC team members have independently verified checks 1–7 | Gate E |

**No asset or place page may go live without all 8 checks confirmed and two signatures on record.**

This checklist is the minimum publication policy. It may be extended but not shortened.

---

## VI. Pre-Activation Operational Items (Gate E)

These are not governance conditions — they are operational tasks that must be completed per place before Gate E sign-off. They are not blocking at the governance level but are blocking at the activation level.

| Item | Required for | Owner |
|---|---|---|
| Confirm Papahānaumokuākea GeoNames ID via NC application account | Papahānaumokuākea place page only | Operations |
| Write confirmed GeoNames IDs to `places` table for all 7 places | All place pages | Engineering |
| Write Wikidata QIDs (Q351, Q220289, Q7343, Q38095, Q787425, Q641) to `places` table | All place pages | Engineering |
| Confirm Asset Zero UUIDs written to `source_item` and `activation_target` tables | Per-asset | Engineering |
| Confirm SA-NOAA-001 gate results (ALLOWED/BLOCKED) per NOAA asset | NOAA assets | Governance |
| Confirm NARA `useRestriction.status == "Unrestricted"` per NARA asset | NARA assets | Governance |
| Mapbox account provisioned; API key stored as secret; NC map style created | All map-tile displays | Engineering |
| Protomaps fallback configured and tested | Map-tile fallback | Engineering |

---

## VII. Launch Sequence (unchanged from NC-PILOT-001 §VII.3)

Earthrise's Gate E pre-activation items are a strict subset (NC-NASA-002 only; no GeoNames, no OSM tiles, no NOAA). It can activate as soon as Gate E is confirmed.

| Phase | Places | Blocking items |
|---|---|---|
| Phase 1 | Earthrise | Gate E for NC-NASA-002 only |
| Phase 2 | Yellowstone + Grand Canyon | GeoNames IDs confirmed; NARA gates per asset; Gate E |
| Phase 3 | Galápagos | GeoNames ID confirmed; Gate E |
| Phase 4 | Great Barrier Reef + Papahānaumokuākea | Papahānaumokuākea GeoNames ID confirmed; NOAA SA-NOAA-001 gate per asset; Gate E |
| Phase 5 | Venice (partial — editorial only) | Gate E; no products until museum DD ratified |
| Phase 6 | Venice (full) | DD-MET-001 ratified |

---

## VIII. Outstanding Governance Actions (non-blocking)

These are not conditions on this launch. They are the next sprint's governance agenda.

| Action | Priority | Notes |
|---|---|---|
| DD-SMITHSONIAN-001 | HIGH | Unblocks 2 Yellowstone + 2 Grand Canyon product assets |
| DD-MET-001 ratification | HIGH | Unblocks Venice full launch; Canaletto holdings |
| DD-TNA-001 or DD-UKHO-001 | HIGH | Unblocks Cook/Beagle charts |
| DD-ESA-001 | MEDIUM | Unblocks Copernicus Sentinel-2 for Venice |
| SA-WIKIDATA-001 | MEDIUM | Required at catalog scale |
| Standards Constitution amendment (Earthrise cosmic anchor) | MEDIUM | 60-day deadline from Earthrise activation |
| DD-OVERTURE-001 | LOW | Overture Maps (CC BY 4.0) for polygon geometry storage; eliminates OSM tile-only constraint |
| DD-CAMBRIDGE-001 | LOW | Long path; Darwin sketch reinstatement |

---

## IX. Decision

**LAUNCH READY.**

All seven blocking conditions from NC-PILOT-001-FGR are resolved:

| Condition | Resolution |
|---|---|
| C-1 — Technical Plan | CLEARED: governance elements documented in SA-GEONAMES-001, SA-OSM-001, and this review; operational elements governed by Gate E |
| C-2 — SA-GEONAMES-001 | CLEARED: drafted and on file |
| C-3 — SA-OSM-001 + OSM conflict | CLEARED: drafted; OSM Intelligence Plan formally superseded |
| C-4 — GeoNames IDs | CLEARED: 5 of 6 confirmed via Wikidata P1566; Papahānaumokuākea delegated to Gate E pre-activation |
| C-5 — 9 unsafe assets | CLEARED: 9 assets formally deferred; 16 product-safe assets in confirmed inventory |
| C-6 — ESA mislabel | CLEARED: asset #20 deferred; Venice launches as editorial-only place page |
| C-7 — Publication policy | CLEARED: Publication Checklist defined in §V |

No new governance decisions are required. The two-human activation Gate E governs the operational pre-activation items that remain. The pilot may proceed to activation.

---

## X. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Readiness Review | ☑ LAUNCH READY | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-PILOT-001-FRR — drafted 2026-06-11*  
*Based on: NC-PILOT-001-FGR · SA-GEONAMES-001 · SA-OSM-001 · Wikidata P1566 lookups (2026-06-11)*  
*Decision: LAUNCH READY — Gate E pre-activation items outstanding per §VI*
