# NC-DATA-005: Great Barrier Reef Evidence Package

**Document ID:** NC-DATA-005  
**Status:** EVIDENCE COMPLETE  
**Date:** 2026-06-12  
**Purpose:** Evidence collection for NC-DATA-004 Great Barrier Reef Authority Resolution (GBR-001 + GBR-002)  
**Note:** No authority decision is made in this document. Evidence only.

---

## I. Collection Method

GeoNames `getJSON` API (demo username rate-limited) → Used `sws.geonames.org` RDF linked data for each candidate ID. GeoNames RDF is the authoritative GeoNames Linked Data endpoint, published under CC BY 4.0, with identical feature identity information to the JSON API. All data was retrieved live 2026-06-12.

Wikidata entity data retrieved live via `Special:EntityData/Q7343.json` API (public, no authentication required). Live retrieval date: 2026-06-12.

GeoNames `searchJSON` and `hierarchyJSON` APIs were rate-limited. Search and hierarchy fixtures for 2164628 were constructed from the RDF parent chain and are marked accordingly.

---

## II. GeoNames Identity Results — Both Candidates

### 2164628

| Field | Value | Source |
|-------|-------|--------|
| geonameId | 2164628 | GeoNames RDF live |
| name | **Great Barrier Reef** | GeoNames RDF live |
| alternateNames | "Bol'shoy Bar'yernyy Rif", "The Great Barrier Reef", "The Great Barrier Reefs" | GeoNames RDF live |
| featureClass | **H** (Hydrographic) | GeoNames RDF live |
| featureCode | **H.RF** (reef) | GeoNames RDF live |
| countryCode | AU | GeoNames RDF live |
| lat | -17.98722 | GeoNames RDF live |
| lng | 146.76979 | GeoNames RDF live |
| parentFeature | 2152274 (Queensland) | GeoNames RDF live |
| parentCountry | 2077456 (Australia) | GeoNames RDF live |
| parentADM1 | 2152274 (Queensland) | GeoNames RDF live |
| Wikipedia | en.wikipedia.org/wiki/Great_Barrier_Reef | GeoNames RDF live |
| RDF URL | sws.geonames.org/2164628/about.rdf | — |
| Record created | 2006-01-15 | GeoNames RDF live |
| Record modified | 2013-09-25 | GeoNames RDF live |

**Verdict: This IS the Great Barrier Reef natural feature. CANONICAL.**

### 10288865

| Field | Value | Source |
|-------|-------|--------|
| geonameId | 10288865 | GeoNames RDF live |
| name | **Clarion Great Barrier Reef** | GeoNames RDF live |
| featureClass | **S** (Spot, building, farm) | GeoNames RDF live |
| featureCode | **S.HTL** (hotel) | GeoNames RDF live |
| countryCode | AU | GeoNames RDF live |
| lat | -16.7507 | GeoNames RDF live |
| lng | 145.6695 | GeoNames RDF live |
| parentADM2 | 7839567 | GeoNames RDF live |
| Wikipedia | NONE | GeoNames RDF live |
| RDF URL | sws.geonames.org/10288865/about.rdf | — |
| Record created | 2015-05-26 | GeoNames RDF live |
| Record modified | 2019-05-22 | GeoNames RDF live |

**Verdict: This is the "Clarion Great Barrier Reef" hotel — a commercial lodging establishment named after the reef. Feature class S (buildings/spots), feature code HTL (hotel). This is not a reef, not a natural feature, not a hydrographic entity. The GeoNames Intelligence Plan's claim of `S HTL / REEF` was internally inconsistent notation — the `/ REEF` was misleading; the entity is purely a hotel. DISQUALIFIED.**

---

## III. Wikidata Q7343 Evidence

Live Wikidata API response for Q7343 (2026-06-12):

| Property | Value | Meaning |
|----------|-------|---------|
| P31 (instance of) | Q11292, Q38048753, Q570116, Q9259 | coral reef, reef, UNESCO World Heritage Site, barrier reef |
| P17 (country) | Q408 | Australia |
| P625 (coordinates) | lat -16.4, lon 145.8 | Great Barrier Reef centroid |
| **P1566 (GeoNames ID)** | **"2164628"** | **Confirms 2164628 = canonical GeoNames ID** |
| P131 (located in) | Q36074 | Queensland |
| P373 (Commons category) | "Great Barrier Reef" | Wikimedia Commons category |
| P18 (image) | GreatBarrierReef-EO.JPG | Earth Observatory image |
| **P402 (OSM relation)** | **NOT PRESENT** | **No OS-4 concern** |

**Wikidata P1566 = 2164628. Consistent with GeoNames RDF evidence.  
No P402 found — no OSM relation ID to suppress per DD-OSM-001 OS-4.**

Note: Wikidata coordinates (lat -16.4, lon 145.8) and GeoNames RDF coordinates (lat -17.98722, lon 146.76979) differ. The GBR extends ~2,300 km; both points are within the reef system. GeoNames coordinates are authoritative per DD-GEONAMES-001.

---

## IV. Coordinate Comparison

| Source | Latitude | Longitude | Authority |
|--------|----------|-----------|-----------|
| GeoNames 2164628 RDF | -17.98722 | 146.76979 | Primary (DD-GEONAMES-001) |
| Wikidata Q7343 P625 | -16.4 | 145.8 | Secondary |

Both coordinates fall within the Great Barrier Reef system (eastern Queensland coast). The 1.6° difference is within the reef's ~14° latitudinal extent. No conflict.

---

## V. GeoNames Hierarchy Chain (from RDF parent links)

The GeoNames RDF for 2164628 defines the following parent chain:

```
parentADM1     → 2152274  (Queensland — A.ADM1)
parentCountry  → 2077456  (Australia — A.PCLI)
```

The `hierarchyJSON` API was rate-limited. The constructed hierarchy fixture (`hierarchy_great_barrier_reef.json`) mirrors the Grand Canyon hierarchy structure, derived from the RDF parent chain.

---

## VI. Feature Code Analysis

| ID | fcode (RDF confirmed) | Description |
|----|----------------------|-------------|
| 2164628 | **H.RF** | Reef(s) — hydrographic feature class |
| 10288865 | **S.HTL** | Hotel — spot/building feature class |
| Yellowstone 5843591 | L.PRKA | Park area |
| Grand Canyon 5296401 | L.PRK | Park |

Three different governance documents claimed three different feature codes for 2164628:
- Blueprint §III.3: "RFU" (H.RFU = underwater reef) — directionally correct class, wrong code
- FRR §III + most downstream docs: "RFSU" (H.RFSU = submerged coral reef) — wrong code
- GeoNames RDF confirmed: **H.RF** (reef)

GeoNames feature code taxonomy (relevant H-class reef codes):
- `RF` — reef(s) — surface or near-surface reef
- `RFSU` — submerged reef — reef below navigational surface
- `RFU` — underwater reef — reef below low-water mark

The Great Barrier Reef is designated H.RF. This is the correct code for the feature as GeoNames defines it.

---

## VII. Fixtures Created

| Fixture file | Content | Collection method |
|-------------|---------|-------------------|
| `tests/fixtures/geonames/place_great_barrier_reef.json` | GeoNames format for 2164628 | Derived from RDF live response |
| `tests/fixtures/geonames/search_great_barrier_reef.json` | GeoNames search format | Derived from RDF (searchJSON rate-limited) |
| `tests/fixtures/geonames/hierarchy_great_barrier_reef.json` | GeoNames hierarchy for 2164628 | Derived from RDF parent chain (hierarchyJSON rate-limited) |
| `tests/fixtures/wikidata/entity_great_barrier_reef.json` | Wikidata Q7343 full entity | Live Wikidata API response |
| `tests/fixtures/wikidata/search_great_barrier_reef.json` | Wikidata search result for Q7343 | Live Wikidata API response |

### Note on GeoNames fixtures derived from RDF

The `place_great_barrier_reef.json`, `search_great_barrier_reef.json`, and `hierarchy_great_barrier_reef.json` fixtures were constructed from the GeoNames RDF Linked Data API (`sws.geonames.org/2164628/about.rdf`) rather than the JSON API (`api.geonames.org/getJSON`). The RDF endpoint carries identical authoritative data. Future resolution: register an NC application GeoNames account and collect the raw `getJSON` response to replace these derived fixtures.

---

## VIII. Disqualified IDs

| ID | Actual identity | Disqualification basis |
|----|----------------|------------------------|
| 10288865 | Clarion Great Barrier Reef (hotel, Queensland, AU) | Commercial hotel named after the reef. fcl=S (buildings), fcode=HTL. Not a natural feature. Intelligence Plan only. Three-for-three wrong across resolved places. |

---

## IX. OS-4 Status (Q7343)

Wikidata Q7343 has **no P402 property** (OSM relation ID). This is in contrast to Yellowstone (P402 = 1453307) and Grand Canyon (P402 = 183377), both of which required OS-4 suppression on ingest. The Great Barrier Reef Wikidata ingest path requires no OS-4 filter for P402.

---

## X. RFSU Correction Cascade

This session identified that "RFSU" was incorrectly used as the GBR feature code in four production locations. All corrected to "RF":

| Location | Status |
|----------|--------|
| `infrastructure/postgres/init/47_nc_data_002_authority_resolution_pilot_places.sql` | CORRECTED |
| `services/data/authority_resolution.py` | CORRECTED |
| `docs/governance/NC-PILOT-001_final_readiness_review.md` | CORRECTED |
| `docs/governance/NC-PILOT-001_launch_authorization.md` | CORRECTED |

Similarly, Grand Canyon PRKN was corrected to PRK across the same file set (NC-DATA-003 evidence confirmed L.PRK; NC-DATA-005 applied the corrections).

---

*NC-DATA-005 — Great Barrier Reef Evidence Package — EVIDENCE COMPLETE — 2026-06-12*
