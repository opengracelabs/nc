# Europeana Discovery Portfolio v1

**Role:** Chief Curator  
**Objective:** Identify the first high-fidelity, rights-cleared assets to ingest via the Europeana adapter, expanding Nature & Culture's reach beyond the BHL.

---

## 1. Portfolio Strategy: The "Masterpiece" Integration

As our first step into the Europeana ecosystem, we prioritize assets that provide **Visual Authority** and **Historical Proof** for our six flagship locations. These assets must be strictly rights-cleared (Public Domain Mark, CC0, or NoC-US).

### Ranking Criteria:
1.  **Place Relevance:** Does it define the "spirit" of the location?
2.  **Educational Value:** Does it anchor a scientific or historical narrative?
3.  **Tourism Value:** Does it inspire wonder and physical visitation?
4.  **Commercial Value:** Is the resolution and aesthetic suitable for high-end commerce?

---

## 2. Selected Masterpiece Collections

### A. Yellowstone: The Jackson Stereoviews
*   **Asset:** *U.S. Geological Survey of the Territories: Yellowstone Series* (1871).
*   **Creator:** William Henry Jackson.
*   **Institution:** National Library of France / Smithsonian.
*   **Rights:** Public Domain Mark.
*   **Reason for Selection:** These are the first-ever photographs of Yellowstone. They established the park's legitimacy and provide the primary visual proof of the "Living Frontier."
*   **Recommended Use:** The core visual anchor for the **Yellowstone Experience v1** Discovery Path. Suitable for a "3D Depth" effect in the UI.

### B. Yosemite: The Watkins Mammoth Plates
*   **Asset:** *Mammoth Views of Yosemite Valley* (c. 1861-1866).
*   **Creator:** Carleton Watkins.
*   **Institution:** Rijksmuseum / Getty.
*   **Rights:** Public Domain Mark.
*   **Reason for Selection:** Watkins’ technical mastery and the massive scale of his glass-plate negatives captured Yosemite with a fidelity that influenced Abraham Lincoln. They represent the "Sacred Stillness" of the Sierra.
*   **Recommended Use:** High-fidelity "Infinite Zoom" gallery. Primary source for **Shopify Wall Art** and **Gallery Prints**.

### C. Galápagos: The Beagle Zoology Plates
*   **Asset:** *The Zoology of the Voyage of H.M.S. Beagle* (1839).
*   **Creator:** George R. Waterhouse (Illustrator) / Charles Darwin (Editor).
*   **Institution:** British Library / Naturalis.
*   **Rights:** Public Domain Mark.
*   **Reason for Selection:** These plates represent the scientific foundation of evolutionary theory. The detailed color engravings of finches and mammals are both beautiful and academically authoritative.
*   **Recommended Use:** Interactive **"Evolutionary Bridge"** annotations. Suitable for a "Scientific Discovery" scrollytelling journey.

### D. Great Barrier Reef: The Saville-Kent Marine Plates
*   **Asset:** *The Great Barrier Reef of Australia: Its Products and Potentialities* (1893).
*   **Creator:** William Saville-Kent.
*   **Institution:** Biodiversity Heritage Library / National Library of Australia.
*   **Rights:** CC0 / Public Domain.
*   **Reason for Selection:** Saville-Kent was the first to photograph the living reef. His color lithographs and underwater-style photography are the baseline for reef health history.
*   **Recommended Use:** The "Marine Mosaic" discovery path. High commercial value for **Puzzles** and **Botanical Posters**.

---

## 3. Implementation Plan: Europeana Adapter V1

| Asset ID (Example) | Substrate Category | Ingestion Rule | NC Atmosphere Vibe |
| :--- | :--- | :--- | :--- |
| **NC-EU-YELL-001** | Photography | Tiled IIIF Image | Primeval / Volatile |
| **NC-EU-YOSE-001** | Photography | HDR WebP | Ethereal / Serene |
| **NC-EU-GALA-001** | Fine Art | Vector SVG Overlay | Scientific / Isolated |
| **NC-EU-GBR-001** | Fine Art / Photo | Deep Zoom Poster | Vibrant / Fragile |

---

**Next Steps:**
*   Develop the **Europeana Metadata Adapter** to handle `edm:ProvidedCHO` mapping.
*   Download the **high-resolution TIFF masters** for the Watkins Yosemite plates.
*   Finalize the **"Authority-Projection" sync** for these institutional assets in Neo4j.
