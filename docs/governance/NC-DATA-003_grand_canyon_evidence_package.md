# NC-DATA-003: Grand Canyon Evidence Package

**Document ID:** NC-DATA-003  
**Status:** EVIDENCE COMPLETE  
**Date:** 2026-06-12  
**Purpose:** Evidence collection for NC-DATA-002 Grand Canyon Authority Resolution (GCA-001 + GCA-002)  
**Note:** No authority decision is made in this document. Evidence only.

---

## I. Collection Method

GeoNames `getJSON` API (demo username rate-limited) → Supplemented with `sws.geonames.org` RDF linked data for each candidate ID. GeoNames RDF is the authoritative GeoNames Linked Data endpoint, published under CC BY 4.0, with identical feature identity information to the JSON API. All data was retrieved live 2026-06-12.

Wikidata entity data retrieved live via `Special:EntityData/Q220289.json` API (public, no authentication required). Live retrieval date: 2026-06-12.

GeoNames `searchJSON` and `hierarchyJSON` APIs were rate-limited. Search and hierarchy fixtures for 5296401 were constructed from the RDF parent chain and are marked accordingly.

---

## II. GeoNames Identity Results — All Three Candidates

### 5296401

| Field | Value | Source |
|-------|-------|--------|
| geonameId | 5296401 | GeoNames RDF live |
| name | **Grand Canyon National Park** | GeoNames RDF live |
| officialName | Grand Canyon National Park | GeoNames RDF live |
| alternateNames | "Marble Canyon National Monument" | GeoNames RDF live |
| featureClass | L (Area) | GeoNames RDF live |
| featureCode | **L.PRK** (park) | GeoNames RDF live |
| countryCode | US | GeoNames RDF live |
| lat | 36.10697 | GeoNames RDF live |
| lng | -112.113 | GeoNames RDF live |
| alt | 1767 m | GeoNames RDF live |
| adminName1 | Arizona | GeoNames RDF live |
| adminName2 | Coconino | GeoNames RDF live |
| Wikipedia | en.wikipedia.org/wiki/Grand_Canyon_National_Park | GeoNames RDF live |
| RDF URL | sws.geonames.org/5296401/about.rdf | — |
| Record created | 2014-05-29 | GeoNames RDF live |
| Record modified | 2018-02-02 | GeoNames RDF live |

**Verdict: This IS Grand Canyon National Park.**

### 5296404

| Field | Value | Source |
|-------|-------|--------|
| geonameId | 5296404 | GeoNames RDF live |
| name | **Grand Canyon National Game Preserve** | GeoNames RDF live |
| alternateNames | "Grand Canyon Forest Reserve", "Grand Canyon Natural Game Preserve" | GeoNames RDF live |
| featureClass | L (Area) | GeoNames RDF live |
| featureCode | L.PRK (park) | GeoNames RDF live |
| countryCode | US | GeoNames RDF live |
| lat | 36.33331 | GeoNames RDF live |
| lng | -112.50907 | GeoNames RDF live |
| alt | 1943 m | GeoNames RDF live |
| adminName1 | Arizona | GeoNames RDF live |
| adminName2 | Coconino | GeoNames RDF live |
| RDF URL | sws.geonames.org/5296404/about.rdf | — |
| Record created | 2006-01-15 | GeoNames RDF live |

**Verdict: This is the Grand Canyon National Game Preserve — a different historical entity from the national park. It predates the park designation and refers to the 1906 game preserve established by Theodore Roosevelt before the 1919 park establishment. It is NOT Grand Canyon National Park. The FRR §III claim that 5296404 was a "typo of 5296401" was incorrect — it is a distinct GeoNames record for a distinct historical entity.**

### 5513679

| Field | Value | Source |
|-------|-------|--------|
| geonameId | 5513679 | GeoNames RDF live |
| name | **Thunder Mountain** | GeoNames RDF live |
| featureClass | T (Mountain, hill, rock) | GeoNames RDF live |
| featureCode | **T.MT** (mountain) | GeoNames RDF live |
| countryCode | US | GeoNames RDF live |
| lat | 38.1716 | GeoNames RDF live |
| lng | -117.0273 | GeoNames RDF live |
| alt | 2144 m | GeoNames RDF live |
| adminName1 | **Nevada** | GeoNames RDF live |
| adminName2 | **Nye County** | GeoNames RDF live |
| RDF URL | sws.geonames.org/5513679/about.rdf | — |

**Verdict: Thunder Mountain, Nye County, Nevada. This is completely unrelated to Grand Canyon or Arizona. The NC-PILOT-001 Commercial Pilot Governance Blueprint's GeoNames ID 5513679 was wrong — it referenced a mountain in Nevada, not any Grand Canyon feature. The Blueprint's claim that it had fcode=PRKA was also wrong: the actual feature code is T.MT (mountain), not L.PRKA (park area).**

---

## III. Wikidata Q220289 Evidence

Live Wikidata API response for Q220289 (2026-06-12):

| Property | Value | Meaning |
|----------|-------|---------|
| P31 (instance of) | Q34918903 + Q46169 | "national park in the United States" + "national park" |
| P17 (country) | Q30 | United States |
| P625 (coordinates) | lat 36.0553, lon -112.122 | Grand Canyon National Park center |
| **P1566 (GeoNames ID)** | **"5296401"** | **Confirms 5296401 = canonical GeoNames ID** |
| P402 (OSM relation) | "183377" | OSM — **must not be stored per OS-4 (DD-OSM-001)** |
| P373 (Commons category) | "Grand Canyon National Park" | Wikimedia Commons category |
| P131 (located in) | Q58684 (Coconino County) + Q58696 (Mohave County) | Two-county jurisdiction |

**Wikidata P1566 = 5296401. This is consistent with the GeoNames RDF evidence that 5296401 = "Grand Canyon National Park."**

Note: Wikidata coordinates (36.0553, -112.122) and GeoNames RDF coordinates (36.10697, -112.113) differ slightly — this is expected. Wikidata uses a manually-entered centroid, GeoNames uses the authoritative feature centroid. GeoNames coordinates are authoritative per DD-GEONAMES-001.

---

## IV. Coordinate Comparison

| Source | Latitude | Longitude | Authority |
|--------|----------|-----------|-----------|
| GeoNames 5296401 RDF | 36.10697 | -112.113 | Primary (DD-GEONAMES-001) |
| GeoNames 5296401 HTML | 36.1069652 | -112.1129972 | Primary (HTML meta ICBM) |
| Wikidata Q220289 P625 | 36.0553 | -112.122 | Secondary |

GeoNames and Wikidata coordinates agree to within ~0.05 degrees (~5km). Both place the feature in Coconino County, Arizona — consistent with Grand Canyon National Park.

---

## V. GeoNames Hierarchy Chain (from RDF parent links)

The GeoNames RDF for 5296401 defines the following parent chain:

```
parentFeature  → 5290307  (Coconino County, AZ — A.ADM2)
parentCountry  → 6252001  (United States — A.PCLI)
parentADM1     → 5551752  (Arizona — A.ADM1)
parentADM2     → 5290307  (Coconino County — A.ADM2)
```

The `hierarchyJSON` API was rate-limited. The constructed hierarchy fixture (`hierarchy_grand_canyon.json`) mirrors the Yellowstone hierarchy fixture structure (Earth → country → place), derived from the RDF parent chain.

---

## VI. Feature Code Analysis

| ID | fcode (RDF confirmed) | Description |
|----|----------------------|-------------|
| 5296401 | **L.PRK** | Park (named park entity) |
| 5296404 | L.PRK | Park (a different park entity — the Game Preserve) |
| 5513679 | **T.MT** | Mountain (not a park at all) |
| 5843591 (Yellowstone) | L.PRKA | Park area |

Grand Canyon National Park (5296401) has feature code **L.PRK**, not L.PRKA. This differs from Yellowstone (5843591 = L.PRKA). Both are valid GeoNames feature codes for national parks — they are different entries in the GeoNames feature taxonomy. PRK and PRKA both fall under feature class L (Area).

The FRR §III claimed feature code "PRKN" for 5296401. This is incorrect — the actual code is L.PRK. The same FRR §III claimed "PRKN" for Yellowstone (5843591), which is actually L.PRKA. The FRR §III feature code claims for national parks were consistently wrong. There is no L.PRKN in the GeoNames ontology at `www.geonames.org/ontology#L.PRKN`.

---

## VII. Fixtures Created

| Fixture file | Content | Collection method |
|-------------|---------|-------------------|
| `tests/fixtures/geonames/place_grand_canyon.json` | GeoNames getJSON format for 5296401 | Derived from RDF live response |
| `tests/fixtures/geonames/search_grand_canyon.json` | GeoNames searchJSON format for "Grand Canyon National Park" | Derived from RDF (searchJSON rate-limited) |
| `tests/fixtures/geonames/hierarchy_grand_canyon.json` | GeoNames hierarchyJSON format for 5296401 | Derived from RDF parent chain (hierarchyJSON rate-limited) |
| `tests/fixtures/wikidata/entity_grand_canyon.json` | Wikidata Q220289 full entity | Live Wikidata API response |
| `tests/fixtures/wikidata/search_grand_canyon.json` | Wikidata search result for Q220289 | Live Wikidata API response |

### Note on GeoNames fixtures derived from RDF

The `place_grand_canyon.json` and `hierarchy_grand_canyon.json` fixtures were constructed from the GeoNames RDF Linked Data API (`sws.geonames.org/5296401/about.rdf`) rather than the JSON API (`api.geonames.org/getJSON`). The RDF endpoint carries identical authoritative data — same geonameId, name, featureClass, featureCode, coordinates, parent chain, CC BY 4.0 license, and attribution. The difference is format, not authority. Future resolution: register an NC application GeoNames account and collect the raw `getJSON` response to replace these derived fixtures.

---

## VIII. Disqualified IDs

| ID | Actual identity | Disqualification basis |
|----|----------------|------------------------|
| 5296404 | Grand Canyon National Game Preserve (AZ) | Not the national park — different named entity. Historical predecessor, superseded by 1919 park designation. |
| 5513679 | Thunder Mountain (Nevada) | Completely unrelated to Grand Canyon. Mountain in Nye County, Nevada. Blueprint's fcode=PRKA claim was also wrong (actual: T.MT). |

---

## IX. OSM OS-4 Note

Wikidata Q220289 P402 = "183377" (OSM relation ID for Grand Canyon National Park boundary). Per DD-OSM-001 OS-4, OSM identifiers must never be stored in canonical NC tables. The Wikidata ingestion path must drop P402 on ingest for Grand Canyon exactly as it must for Yellowstone (P402 = "1453307").

---

*NC-DATA-003 — Grand Canyon Evidence Package — EVIDENCE COMPLETE — 2026-06-12*
