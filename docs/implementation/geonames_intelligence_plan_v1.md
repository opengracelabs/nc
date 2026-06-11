# GeoNames Intelligence Plan v1

**Subject:** GeoNames as the Spatial Authority
**Strategy:** Topographic Enrichment & Hierarchical Place Intelligence
**Status:** Implementation Roadmap
**Date:** June 11, 2026

---

## 1. The Strategy: "Spatial Truth" for Nature & Culture

The **GeoNames Intelligence Plan** establishes GeoNames as the primary **Spatial Authority** for the Nature & Culture platform. While Wikidata provides the semantic "What" and "Who," GeoNames provides the topographic "Where" and the administrative "Within." 

By integrating GeoNames, we transition from simple coordinates to a rich **Place Intelligence** model that understands elevation, population density, timezones, and jurisdictional hierarchies.

---

## 2. The Place Intelligence Stack

The platform's intelligence is built on five pillars, each providing a distinct layer of "Truth":

| Layer | Provider | Domain of Truth | Role in Stack |
|---|---|---|---|
| **Spatial** | **GeoNames** | Topography & Hierarchy | Defines coordinates, elevation, feature types, and administrative containment. |
| **Semantic**| **Wikidata** | Attributes & Identity | Connects places to people, events, concepts, and institutional IDs. |
| **Biological**| **GBIF** | Species & Biodiversity | Provides occurrence data and taxonomic checklists for the location. |
| **Environmental**| **NASA** | Landscape & Climate | Supplies satellite imagery, land cover data, and vegetation indices (NDVI). |
| **Marine/Atmos**| **NOAA** | Oceans & Atmosphere | Adds bathymetry (depth), weather patterns, and maritime sanctuary boundaries. |

---

## 3. High-Value Place Enrichment

GeoNames enriches our flagship locations with precise topographic and hierarchical data:

| Place | GeoNames ID | Feature Code | Enrichment Data |
|---|---|---|---|
| **Yellowstone** | `5843642` | `L PRK` | **Hierarchy:** US > WY > Park County. **Alt Names:** ~50 languages. |
| **Grand Canyon** | `5296404` | `L PRK` | **Topography:** Precise park center-point. **Hierarchy:** US > AZ > Coconino. |
| **Great Barrier Reef**| `10288865`| `S HTL` / `REEF`| **Scale:** Marine regional mapping. **Link:** Linked to Marine Regions ID. |
| **Papahānaumokuākea**| `11854341`| `L PRK` | **Remoteness:** Timezone (UTC-10). **Status:** High-seas administrative park. |
| **Venice** | `3164603` | `P PPLA` | **Human:** Pop. ~260,000. **Elevation:** 1m (Critical for NOAA sea-level). |

---

## 4. GeoNames Enrichment Vectors

### **A. Administrative Hierarchy (The "Within" Logic)**
GeoNames allows the platform to automatically resolve that an illustration of a bird in "Yellowstone" is also an asset for "Wyoming" and the "United States."
*   **Vector:** `PCLI` (Country) -> `ADM1` (State) -> `ADM2` (County) -> `PPL` (City).

### **B. Feature Classification (The "Type" Logic)**
GeoNames categorizes every place with ~650 feature codes, allowing us to filter discovery by "Type."
*   **Vector:** `L PRK` (Parks), `T REEF` (Coral Reefs), `H ISL` (Islands), `P PPL` (Cities).

### **C. Topographic Context (The "Altitude" Logic)**
GeoNames provides elevation and Digital Elevation Model (DEM) data, which enriches NASA imagery.
*   **Vector:** Elevation (meters) and GTOPO30 data.

### **D. Multilingual Identity (The "Global" Logic)**
GeoNames stores "Alternate Names" in hundreds of languages and historical variants.
*   **Vector:** `alternate_names` field for search normalization.

---

## 5. Integration Use Cases

1.  **Elevation-Corrected Ingestion:** Using GeoNames elevation to filter BHL illustrations of "Alpine" species from "Lowland" species in the same park.
2.  **Hierarchical Roll-up:** Automatically tagging a NASA image of the Grand Canyon with "Coconino County" and "Arizona" metadata.
3.  **Sea-Level Risk Assessment:** Combining Venice's GeoNames elevation (1m) with NOAA tidal surge data to contextualize historical BHL floods.
4.  **Population-Density Filter:** Using Venice population stats to distinguish "Wilderness" (Yellowstone) from "Cultural Landscapes" (Venice) in the recommendation engine.
5.  **Timezone-Aware Ingestion:** Syncing the timestamp of a NOAA weather observation in Papahānaumokuākea to the local GeoNames timezone.

---

## 6. Operational Roadmap

1.  **GeoNames Daily Sync:** Implement a worker to ingest and update the `places` table using the GeoNames daily export.
2.  **Hierarchy Indexing:** Build a recursive SQL view or Neo4j graph to enable "Upward Discovery" (Place -> Region -> Country).
3.  **Feature Filtering:** Deploy a Discovery API filter that allows users to toggle between "Natural Features" (GeoNames Class T, H, L) and "Human Features" (Class P, S).
