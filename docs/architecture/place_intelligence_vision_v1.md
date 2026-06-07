# Place Intelligence Vision v1

**Role:** Chief Curator  
**Objective:** Define the intelligence-driven experience of Nature & Culture—using Graph (Neo4j) and Semantic (pgvector) layers to create wonder, discovery, and connection.

---

## 1. Intelligence Philosophy: The "Discovery Flywheel"

Intelligence at Nature & Culture is not "Search." It is **Resonance.** We use technology to reveal the hidden threads that connect a species in the Galápagos to a 19th-century map in Yellowstone or a Zen garden in Kyoto.

| Layer | Technology | Experience Role | Reference Model |
| :--- | :--- | :--- | :--- |
| **Relationship** | **Neo4j (Graph)** | Connecting entities (Place -> Person -> Asset -> Concept). | Wikipedia / Wikidata |
| **Semantic** | **pgvector (Vector)** | Finding conceptual, visual, and "vibe" similarities. | Google Arts & Culture |
| **Discovery** | **Serendipity Engine** | Surfacing "Hidden Wonders" and unexpected connections. | Atlas Obscura |
| **Narrative** | **GeoStories** | Transforming data nodes into authoritative, human stories. | National Geographic |

---

## 2. Intelligence Journeys: The Six Flagships

### A. Yellowstone: The Chemical Frontier
*   **Relationship Journey:** Connecting the **Hayden Survey (1871)** to the discovery of **Thermus aquaticus (1969)**. The graph links the early maps of geyser basins to the modern DNA polymerase revolution.
*   **Discovery Journey:** "If you love the volatility of the Upper Geyser Basin, explore the **Beppu Onsen** in Japan"—connected via semantic "thermal volatility" vectors.

### B. Yosemite: The Glacial Soul
*   **Story Journey:** Following **John Muir’s "Glacial Theory"** across the graph. See how his rough field sketches predicted the modern glacial retreat models in our datasets.
*   **Educational Journey:** Linking a specific **Watkins photograph (1863)** to the exact geological coordinate in a modern 3D map, revealing the "Process of Erosion."

### C. Galápagos: The Evolutionary Web
*   **Discovery Journey (Semantic):** Visual similarity search between **Darwin’s Finch sketches** and modern citizen-science photography. "See the evolution of the beak through 200 years of media."
*   **Relationship Journey:** Linking a specific island (e.g., Floreana) to every journal entry, specimen, and map created on its shores across three centuries.

### D. Great Barrier Reef: The Marine Mosaic
*   **Relationship Journey:** Connecting **Saville-Kent’s 1893 taxonomy** to current **Coral Bleaching datasets**. The graph provides the "Authority of Time," showing what has been lost and what remains.
*   **Educational Journey:** "The Life of a Polyp"—a graph-driven tour through the biological concepts of symbiosis, linked to both 19th-century lithographs and modern 8K film.

### E. Kyoto: The Sacred Geometry
*   **Story Journey:** **"1,200 Years of Spring."** Using the Sakura bloom dataset to link woodblock prints (Hiroshige) to the specific date they were likely created based on bloom vectors.
*   **Discovery Journey:** Finding the "Zen Vibe." Using pgvector to connect the minimal spacing of the **Ryoan-ji garden** to the "Atmospheric Stillness" of a foggy morning in the **Sierra Nevada**.

### F. Machu Picchu: The Celestial Alignment
*   **Relationship Journey:** Linking the **Intihuatana Stone** to celestial events in the Inca calendar. The graph connects archaeology, astronomy, and Bingham’s discovery journals.
*   **Tourism Journey:** "Beyond the Citadel." Using Atlas Obscura-style intelligence to surface the **Vicus culture** or nearby hidden terraces that share the same "Architectural Language" as the main ruins.

---

## 3. Experience Principles: Connection over Data

1.  **"X Degrees of Place":** Every detail page features a "Connection Bridge." (e.g., "This Yosemite map is 2 degrees away from a Galápagos tortoise via the concept of 'Endangered Sanctuary'.")
2.  **The "Hidden Wonder" Filter:** Users can toggle the map between "Iconic" (National Geographic) and "Curious" (Atlas Obscura), surfacing the overlooked stories within a place.
3.  **Semantic Search as Dialogue:** Instead of keywords, users search for feelings. "Find me a place that feels like 'Sacred Stillness' at 'Golden Hour'."
4.  **Trust through Traceability:** Every connection in the graph is cited. Clicking a link reveals the source (BHL, Smithsonian, LoC), building the "Authority" required for a world-class experience.

---

**Next Steps:**
*   Implement the `RelationshipGraph` component for the Place Detail page.
*   Vectorize the *Smithsonian Top 100* assets to test semantic "vibe" discovery.
*   Map the "1,200 Years of Spring" connection for the Kyoto flagship.
