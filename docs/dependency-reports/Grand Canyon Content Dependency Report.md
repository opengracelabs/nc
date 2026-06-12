# Grand Canyon Content Dependency Report (NC-DATA-002)

This report identifies the identifiers and source dependencies for **Grand Canyon National Park**, evaluating conflicts across GeoNames, Wikidata, NASA, NARA, and the BHL.

---

## 1. Identity Anchors (GeoNames & Wikidata)

### 1.1 Wikidata QID (Identity Anchor)
| ID | Entity | Status | Reasoning |
| :--- | :--- | :--- | :--- |
| **Q220289** | Grand Canyon National Park | **RATIFIED** | Represents the administrative park, tourism anchor, and conservation entity. |
| **Q131648** | Grand Canyon (Geological Feature) | **RETIRED** | Represents the physical gorge; subordinate to the park's administrative identity for NC commerce. |

### 1.2 GeoNames ID (Identity Anchor) - **CONFLICT DETECTED**
Three competing IDs exist with no fixture support. Identification of the canonical ID is **PENDING** verification via live API fixture (GCA-001).

| ID | Source Document | Status | Note |
| :--- | :--- | :--- | :--- |
| **5296401** | FRR §III / Production | **PROVISIONAL** | Adopted via unverified methodology; currently on production hold. |
| **5513679** | Governance Blueprint | **UNVERIFIED** | Linked to fcode=PRKA; potentially the authoritative boundary record. |
| **5296404** | Intelligence Plan | **UNVERIFIED** | Linked to fcode=L PRK; identity unknown. |

---

## 2. Source Dependencies (NASA, NARA, BHL)

| Authority | Reference ID | Content Type | Status |
| :--- | :--- | :--- | :--- |
| **NASA** | NC-NASA-006 | Grand Canyon Elevation (ASTER/Terra) | Grounded (Product-safe) |
| **NASA** | NC-NASA-014 | Grand Canyon Perspective (3D) | Grounded (Tourism Waypoint) |
| **NASA** | NC-NASA-031 | Grand Canyon Elevation Map (JPL) | Grounded (Education Anchor) |
| **NARA** | NC-NARA-002 | 1882 Dutton Grand Canyon Atlas (Sheet XIV) | Grounded (Asset Zero) |
| **NARA** | Powell Series | 1869 Powell Expedition Photography | Grounded (Historical Record) |
| **BHL** | Condor Study | California Condor (*Gymnogyps californianus*) | Grounded (Biological Anchor) |
| **BHL** | Powell Notes | John Wesley Powell Exploration Journals | Grounded (Historical Context) |

---

## 3. Critical Conflicts & Risks

1.  **GeoNames Resolution (Blocking):** The three-way conflict between 5296401, 5513679, and 5296404 must be resolved via live API fixture. Until then, any `places` table write or place page activation is blocked.
2.  **Feature Code Mismatch:** The production record (5296401) is associated with the non-standard fcode `PRKN`. The Blueprint (5513679) uses the standard `PRKA`. This discrepancy confirms that the current production ID is unverified.
3.  **Wikidata Inconsistency:** Earlier documents (Blueprint) linked the Grand Canyon to the geological feature (Q131648) rather than the park (Q220289). This has been corrected in NC-DATA-002 errata, but legacy copy may still contain references to the canyon-as-feature rather than canyon-as-park.

---

## 4. Required Action
*   **GCA-001:** Create GeoNames fixtures for all three IDs (5296401, 5513679, 5296404).
*   **GCA-002:** Create Wikidata fixture for Q220289 to verify its P1566 claim.
*   **Correction Migration:** Once the canonical ID is confirmed, a migration must be executed to align the `pilot_anchor` and `places` records.

---
*Grand Canyon Content Dependency Report (NC-DATA-002) produced by Gemini CLI*
