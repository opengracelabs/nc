# Wikidata Intelligence Plan v1

**Subject:** Wikidata as the Identity Authority
**Strategy:** Semantic Reconciliation & Cross-Institutional Linkage
**Status:** Implementation Roadmap
**Date:** June 11, 2026

---

## 1. The Strategy: "Identity Truth" for Nature & Culture

The **Wikidata Intelligence Plan** establishes Wikidata as the primary **Identity Authority** for the Nature & Culture platform. While GBIF provides biological truth and NASA provides environmental truth, Wikidata provides the **Semantic Glue** that connects Places, Persons, Species, Artworks, and Events across disparate institutional silos (NASA, NOAA, NARA, BHL, GBIF, and Museums). 

By anchoring every entity in a persistent Wikidata QID, we move from "Search by Keyword" to "Discovery by Relationship."

---

## 2. Institutional Linkage Framework

Wikidata serves as the "Rosetta Stone" for the following authorities:

### **A. NASA (Space & Remote Sensing)**
*   **The Link:** Spacecraft (P8913), Astronomical Objects (P2956), and Mission Events (P184201).
*   **Intelligence Layer:** Links a NASA satellite image of a "Place" (e.g., Yellowstone) to the specific "Event" (e.g., Apollo 8) and the "Person" (e.g., Bill Anders) who captured it.

### **B. NOAA (Ocean & Atmosphere)**
*   **The Link:** Marine Species (P5951), Weather Stations (P3005), and Marine Protected Areas (P757/P1340334).
*   **Intelligence Layer:** Connects NOAA fisheries data to the "Species Identity" (QID) and the "Place Identity" (QID) of the coral reef where it was collected.

### **C. NARA (Archival & Policy)**
*   **The Link:** National Archives Identifier (P1225).
*   **Intelligence Layer:** Anchors historical federal records (maps, photos, treaties) to modern "Place" and "Person" identities, allowing a search for "Yellowstone" to surface the 1872 Act of Dedication (NARA) alongside modern GBIF biodiversity stats.

### **D. BHL (Biodiversity Literature)**
*   **The Link:** BHL Creator (P4081), BHL Page (P687), and Scientific Name (P4327).
*   **Intelligence Layer:** Bridges "Species Identity" (QID) and "Person Identity" (QID). It links the author of a 19th-century botanical illustration to the modern taxonomic record and the specific museum specimen.

### **E. Museums (Art & Culture)**
*   **The Link:** AIC (P6295), MET (P3634), CMA (P5271), Getty (P2432).
*   **Intelligence Layer:** Resolves "Artwork Identity" (QID) to its depicted "Place" and "Creator," allowing users to see Thomas Moran’s paintings of the Grand Canyon alongside the park’s current GBIF species list.

### **F. GBIF (Biological Science)**
*   **The Link:** GBIF Taxon ID (P846) and Dataset ID (P12382).
*   **Intelligence Layer:** Acts as the bridge between "Scientific Truth" and "Cultural Context." Every GBIF taxon is mapped to a Wikidata QID to enable retrieval of common names, descriptions, and cultural significance.

---

## 3. High-Value Identity Assessment

| Entity | Wikidata QID | Key Links | Identity Type |
|---|---|---|---|
| **Yellowstone** | `Q351` | UNESCO 28, NARA 10048491, GBIF Dataset | Place |
| **Grand Canyon** | `Q220289` | UNESCO 75, NARA 10048491, BHL Agency | Place |
| **Great Barrier Reef** | `Q7344` | UNESCO 154, GBIF Dataset | Place |
| **Papahānaumokuākea**| `Q1340334` | UNESCO 1326, NARA 10045298, OBIS/GBIF | Place |
| **Earthrise** | `Q843864` | NASA AS08-14-2383, MET 2019.440, NARA 16670351| Artwork/Event |

---

## 4. Top 25 Entity-Resolution Use Cases

1.  **Place-to-NARA:** Reconciling a historical NARA map of Yellowstone to its modern Wikidata-defined boundaries.
2.  **Species-to-BHL:** Linking a BHL scientific name for a species found in the Grand Canyon to its Wikidata QID for multilingual common names.
3.  **Artwork-to-Place:** Mapping a Thomas Moran painting (Artwork) to the specific QID of the location it depicts.
4.  **Satellite-to-Species:** Connecting a NASA satellite image of the Great Barrier Reef (Place) to Wikidata-linked GBIF coral occurrences.
5.  **Creator-to-BHL:** Identifying the creator (Person) of a public-domain illustration in a BHL book via BHL Creator ID (P4081).
6.  **UNESCO-Aggregate:** Aggregating all assets from NASA, NARA, and BHL for a specific UNESCO site (P757).
7.  **Geospatial Disambiguation:** Distinguishing "Grand Canyon" (Park) from "Grand Canyon" (Geological Feature) using QID-specific coordinates.
8.  **Specimen-to-Literature:** Linking Smithsonian specimens to the Wikidata-resolved BHL publication where they were first described.
9.  **Admin-vs-Nature:** Resolving "Yellowstone" as both an Administrative Entity and a Natural Protected Area.
10. **Historical-to-Modern:** Connecting a historical NARA expedition photo to modern GBIF biodiversity observations at that coordinate.
11. **Inscription-to-Evidence:** Mapping UNESCO criteria for site inscription to specific visual evidence (Assets) in NARA/NASA.
12. **Taxon-Intersection:** Identifying taxon candidates for a place by intersecting GBIF occurrences with Wikidata species lists.
13. **Image-to-Mission:** Linking the "Earthrise" (Artwork) to the "Apollo 8" (Event) and "NASA" (Institution).
14. **Agency-Resolution:** Resolving institutional creators (e.g., "National Park Service") to their Wikidata QID for provenance tracking.
15. **Cross-Museum Sync:** Mapping "Grand Canyon" artworks across MET, AIC, and CMA using a single Wikidata QID.
16. **Vernacular Normalization:** Normalizing "Papahānaumokuākea" across different source spellings and synonyms via Wikidata aliases.
17. **Multilingual Taxonomy:** Linking a species' vernacular name in 50+ languages to a single scientific identity (QID).
18. **Bathymetry-to-Entity:** Mapping NOAA bathymetric data to the Great Barrier Reef's Wikidata entity.
19. **NARA-to-Institution:** Reconciling NARA agency codes to Wikidata institution QIDs (e.g., NPS, USGS).
20. **Conservation-Link:** Connecting a BHL illustration of a plant to its Wikidata/IUCN conservation status.
21. **Disturbance-History:** Linking a specific event (e.g., 1988 fires) to the long-term recovery illustrations in BHL publications.
22. **Photographer-Identity:** Resolving the "Photographer of the Earth" identity (Bill Anders) across NASA, NARA, and Museum records.
23. **Citation-Mapping:** Linking GBIF occurrence records to the specific BHL page where the specimen was cited.
24. **Economic-Botany:** Connecting BHL historical uses of a plant (Culture) to its modern GBIF distribution (Nature).
25. **Unified Discovery:** Using the QID as the "Universal Join Key" to surface "Nature" (Species/Place) and "Culture" (Artwork/Person/Event) in a single view.

---

## 5. Identity Types in Action

*   **Place Identity:** `Q351` (Yellowstone) - The spatial anchor.
*   **Person Identity:** `Q313583` (Thomas Moran) - The creative witness.
*   **Species Identity:** `Q193581` (*Ursus arctos horribilis*) - The biological resident.
*   **Artwork Identity:** `Q843864` (Earthrise) - The cultural artifact.
*   **Event Identity:** `Q184201` (Apollo 8) - The temporal context.

---

## 6. Operational Roadmap

1.  **QID Normalization:** Implement a worker to assign a Wikidata QID to every record in the `places` and `creators` tables.
2.  **SPARQL Enrichment:** Use the Wikidata Query Service to pull missing attributes (coordinates, descriptions, external IDs) into the PostgreSQL authority.
3.  **Graph Linking:** Use Neo4j to store the `SAME_AS` and `DEPICTS` relationships derived from Wikidata.
