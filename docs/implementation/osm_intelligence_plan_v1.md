# OSM Intelligence Plan v1

**Subject:** OpenStreetMap (OSM) as the Access & Infrastructure Authority
**Strategy:** Ground Truth for Human Navigation & Tourism Intelligence
**Status:** Implementation Roadmap
**Date:** June 11, 2026

---

## 1. The Strategy: "Operational Truth" for Nature & Culture

The **OSM Intelligence Plan** establishes OpenStreetMap as the primary **Access & Infrastructure Authority** for the Nature & Culture platform. While GeoNames provides the topographic "Where" and Wikidata the semantic "What," OSM provides the operational **"How."** 

OSM data allows the platform to understand how a human actually experiences a place: where the trails are, how to access them, where the infrastructure (visitor centers, hotels) is located, and where the specific viewpoints are that capture the "Hero Shots" of Nature.

---

## 2. The Integrated Place Intelligence Stack

OSM completes the stack by adding the **Human Layer**:

| Layer | Provider | Domain of Truth | Role in Stack |
|---|---|---|---|
| **Spatial** | **GeoNames** | Topography & Hierarchy | Coordinates, elevation, and administrative containment. |
| **Semantic**| **Wikidata** | Attributes & Identity | Cross-institutional links (NASA, NOAA, NARA) and concepts. |
| **Operational**| **OSM** | **Access & Infrastructure** | **Trails, roads, buildings, and tourism amenities.** |
| **Biological**| **GBIF** | Species & Biodiversity | Occurrence data and taxonomic checklists. |
| **Environmental**| **NASA/NOAA** | Landscape & Climate | Remote sensing, imagery, and atmospheric state. |

---

## 3. High-Value Operational Enrichment

OSM provides the following "Ground Truth" for our flagship locations:

| Place | OSM Relation | Primary Feature | Tourism Intelligence |
|---|---|---|---|
| **Yellowstone** | `163151` | `boundary=national_park` | **Trails:** ~1,000 miles of `highway=path`. **Access:** `fee=yes`. |
| **Grand Canyon** | `183377` | `boundary=national_park` | **Infrastructure:** `tourism=hotel` (El Tovar). **View:** `tourism=viewpoint`. |
| **Great Barrier Reef**| `2533338`| `boundary=protected_area`| **Marine:** `seamark:type=restricted_area`. **Access:** Boat routes. |
| **Venice** | `44118` | `admin_level=8` | **Urban:** `waterway=canal`, `route=ferry`. **Detail:** `bridge=yes`. |
| **Papahānaumokuākea**| `6411191`| `boundary=protected_area`| **Access:** `access=restricted`. **Infrastructure:** Midway runway. |

---

## 4. OSM Intelligence Vectors

### **A. Trails & Navigation (The "Activity" Logic)**
OSM provides the high-fidelity path network that connects cultural assets to natural features.
*   **Vector:** `highway=path`, `route=hiking`, `sac_scale` (difficulty), `trail_visibility`.

### **B. Access & Governance (The "Rules" Logic)**
OSM captures the real-world restrictions and costs associated with a place.
*   **Vector:** `access=*`, `fee=yes/no`, `opening_hours=*`, `operator=*`.

### **C. Infrastructure & Amenities (The "Utility" Logic)**
OSM maps the buildings and services that support the discovery experience.
*   **Vector:** `amenity=visitor_centre`, `tourism=museum`, `tourism=camp_site`, `aeroway=runway`.

### **D. Tourism Intelligence (The "Experience" Logic)**
OSM identifies the specific spots that are optimized for human observation.
*   **Vector:** `tourism=viewpoint`, `tourism=information`, `historic=shipwreck`, `natural=viewpoint`.

---

## 5. Integration Use Cases

1.  **Trail-to-Taxon Intersection:** Overlaying GBIF species observations with OSM `highway=path` data to show users what species they are likely to see while hiking a specific trail.
2.  **Viewpoint Asset Discovery:** Using OSM `tourism=viewpoint` coordinates to find NARA historical photos or NASA high-res imagery captured from that exact perspective.
3.  **Vaporetto Navigation (Venice):** Linking BHL illustrations of Venetian palaces to the specific OSM `route=ferry` (Vaporetto) lines that pass by them.
4.  **Access-Aware Recommendations:** Filtering "Adventure" suggestions in Papahānaumokuākea based on OSM `access=restricted` and `access=private` tags.
5.  **Infrastructure Proximity:** Ranking discovery opportunities (e.g., a specific BHL plant illustration) higher if they are within 1km of an OSM `amenity=visitor_centre`.

---

## 6. Operational Roadmap

1.  **Overpass API Integration:** Build a service to query OSM data via the Overpass API for real-time enrichment of flagship sites.
2.  **Tag-to-Concept Mapping:** Map OSM tags (e.g., `leisure=nature_reserve`) to the platform’s Canonical Vocabulary (v1).
3.  **Vector Tile Generation:** Generate custom vector tiles showing the intersection of OSM trails and GBIF "Hotspots" for the map interface.
