# GBR Dependency Report (NC-DATA-004)

This report identifies the identifiers and source dependencies for the **Great Barrier Reef**, evaluating conflicts across GeoNames, Wikidata, NASA, NOAA, and GBIF.

---

## 1. Identity Anchors (GeoNames & Wikidata)

### 1.1 Wikidata QID (Identity Anchor)
| ID | Entity | Status | Reasoning |
| :--- | :--- | :--- | :--- |
| **Q7343** | Great Barrier Reef | **RATIFIED** | Represents the coral reef ecosystem—the natural feature itself. |
| **Q37901** | Great Barrier Reef Marine Park | **RETIRED** | Represents an administrative designation; the ecosystem is the preferred commerce anchor. |

### 1.2 GeoNames ID (Identity Anchor)
| ID | Source Document | Status | Note |
| :--- | :--- | :--- | :--- |
| **2164628** | FRR §III / Production | **RATIFIED** | **Great Barrier Reef** (H.RF, Queensland, AU). Verified via GeoNames RDF. |
| **10288865** | Intelligence Plan | **RETIRED** | **Clarion Great Barrier Reef hotel**. Commercial lodging; not a natural feature. |

---

## 2. Source Dependencies (NASA, NOAA, GBIF)

| Authority | Reference ID | Content Type | Status |
| :--- | :--- | :--- | :--- |
| **NASA** | NC-NASA-011 | Landsat 8 Coral Reef Mosaic | Grounded (Product-safe) |
| **NOAA** | NC-NOAA-015 | Bathymetric Map, Hawaiian Ridge (related GBR) | Grounded (Pending SA-NOAA-001) |
| **GBIF** | Marine Records | Coral and Marine Species occurrences | Grounded (Verified per SA-GBIF-001) |
| **BHL** | Haeckel Series | Ernst Haeckel, *Hexacoralla* | Grounded (Historical Record) |
| **BHL** | Saville-Kent | *The Great Barrier Reef of Australia* | Grounded (Historical Context) |

---

## 3. Identity and Authority Conflicts

1.  **Administrative vs. Ecological Anchor:** The Blueprint erroneously used the administrative park QID (Q37901). This has been corrected to the ecological system QID (Q7343) to align with NC's place-centered commerce strategy.
2.  **Commercial Identity Error:** The GeoNames Intelligence Plan v1 used ID 10288865, which refers to a hotel. This has been retired and replaced by the authoritative reef record 2164628.
3.  **Coordinate Consistency:** Coordinates for the reef system are consistent across GeoNames and Wikidata within the expected spatial extent of the reef (~14° latitude).

---

## 4. Retirement Candidates

| ID/QID | Entity | Retirement Basis |
| :--- | :--- | :--- |
| **Q37901** | GBR Marine Park | Administrative designation; superseded by ecological anchor Q7343. |
| **10288865** | Clarion GBR Hotel | Commercial building; not a geographic/natural place anchor. |

---
*GBR Dependency Report (NC-DATA-004) produced by Gemini CLI*
