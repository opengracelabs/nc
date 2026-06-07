# Global Collection Coverage Audit v1

**Role:** Chief Curator  
**Objective:** Assess the ability of current institutional partners to support diverse world-class designations and identify critical gaps in global coverage.

---

## 1. Institutional Support Matrix

| Designation Type | Primary Institutional Support | Coverage Depth |
| :--- | :--- | :--- |
| **UNESCO World Heritage** | Wikidata (Metadata/IDs), Europeana (Regional Maps), Smithsonian (Research) | High (Site-level) |
| **Biosphere Reserves** | Wikidata (ID Mapping), Smithsonian (Biodiversity Specimens/Research) | Medium (Species-heavy) |
| **Ramsar Wetlands** | Wikidata (RSIS Links), BHL (Taxonomy), LOC (Geospatial) | High (Taxonomic focus) |
| **Geoparks** | Wikidata (IDs), Smithsonian (Geological Specimens) | Low (Significant gap) |
| **Marine Protected Areas** | Smithsonian (MarineGEO), British Library (Historical Charts) | High (Marine-heavy) |
| **Dark Sky Places** | Wikidata (Emerging IDs) | **Very Low (Critical Gap)** |
| **Intangible Heritage** | Smithsonian (Folklife/Folkways), British Library (Sound Archive) | High (Auditory-heavy) |

---

## 2. Gap Analysis

### 2.1 Regional Gaps: The Global South
*   **Africa:** Significant lack of high-fidelity visual and cartographic assets in Western repositories, despite high Wikidata metadata coverage.
*   **Southeast Asia:** Thematic focus is often on colonial-era records rather than contemporary indigenous-led conservation data.
*   **Latin America:** Strong biodiversity data (Smithsonian/BHL) but a lack of integrated Intangible Heritage documentation beyond major centers.

### 2.2 Heritage Gaps: The "Invisible" Designations
*   **Geoparks:** There is no single institutional authority for geological heritage assets. Collections are fragmented across national geological surveys.
*   **Dark Sky Places:** Virtually no dedicated digital asset collections exist within the current repository network for astronomical heritage or night-sky preservation.
*   **Intangible Heritage:** While sound is well-covered (Smithsonian/BL), **visual documentation of craft and ritual** is often siloed in non-interoperable local archives.

### 2.3 Media Gaps: Beyond the Static
*   **Real-time Data:** Current repositories are static. There is a total lack of integration for real-time monitoring (acoustic sensors, satellite feeds) of protected areas.
*   **3D/Spatial:** Outside of the Smithsonian, 3D documentation of world heritage sites and artifacts is rare and lacks a unified substrate.

---

## 3. Recommended Institutional Expansion

To achieve near-complete global coverage, the following institutions are prioritized for integration.

| Institution | Role / Expertise | Rank |
| :--- | :--- | :--- |
| **UNESCO "Dive into Heritage"** | Official 3D and site-management records for World Heritage. | **Critical** |
| **UNEP-WCMC (WDPA)** | The authoritative source for Marine and Terrestrial Protected Area boundaries. | **Critical** |
| **International Dark-Sky Association** | Deep-sky photography and light-pollution datasets. | **Important** |
| **Global Biodiversity Information Facility (GBIF)** | 2.5B+ occurrence records to ground Biosphere and Ramsar sites. | **Important** |
| **Endangered Archives Programme (EAP)** | Rare, local archives from the Global South (British Library partner). | **Important** |
| **Troove (Australia)** | Deep coverage of the Great Barrier Reef and indigenous heritage. | **Optional** |
| **Digital Library of the Middle East (DLME)** | Specialized coverage of Middle Eastern cultural heritage. | **Optional** |

---

## 4. Final Conclusion: The Path to Completion

Current coverage is **Metadata Rich but Asset Lean**. We have the "IDs" to 90% of the world's heritage (via Wikidata), but we have "Atmospheric Media" for less than 10%. 

To succeed, Nature & Culture must bridge the gap between **Semantic IDs** and **Atmospheric Assets** by integrating the **UNESCO/UNEP management portals** and expanding into **Indigenous-led digital archives**.

---

**Next Steps:**
*   Establish the **Wikidata-to-WDPA** reconciliation worker.
*   Map the **Smithsonian Folkways** API for Intangible Heritage integration.
*   Audit the **UNEP-WCMC** data schema for PostGIS/Spatial alignment.
