# Getty Asset Zero Experience Blueprint: The God of Flowers

**Asset:** *Vase of Flowers* (1722)  
**Institution:** J. Paul Getty Museum  
**Theme:** The Miraculous Bouquet / Dutch Golden Age Botanical Intelligence  
**Core Objective:** Immerse the visitor in the luminous, hyper-detailed world of 18th-century Dutch floriculture, revealing the "scientific fantasy" of Van Huysum’s composition.

---

## 1. Homepage Hero: The Miraculous Bloom

**Emotional Goal:** Instant awe at the "impossible" beauty and luminous detail.

*   **Visual:** A centered, high-resolution crop of the **Vase of Flowers**, specifically the central **Dark Blue Iris** and the **Cabbage Rose**. A subtle "Luminescence" shader creates a slow, rhythmic pulsing of light on the petals, as if the flowers are breathing.
*   **Typography:** Baskerville Bold for headlines / Noto Sans Dutch for historical grounding.
    *   *Headline:* "The God of Flowers"
    *   *Sub-headline:* "Enter Jan van Huysum’s miraculous 1722 bouquet—a scientific fantasy where over 30 species bloom as one."
*   **Atmospheric Runtime:**
    *   **Palette:** `Dutch Golden Age Dark` (#1A1A1A) backgrounds with `Van Huysum Gold` (#D4AF37) and `Petal Pink` (#FFB6C1) accents.
    *   **Audio:** A delicate, multi-layered soundscape: the faint "tick" of a 1700s clock, a light summer breeze rustling silk, and the microscopic "flutter" of a butterfly's wings.
*   **Interaction:** A "Witness the Bloom" button that triggers a slow-zoom into the dewdrops on a rose leaf.

---

## 2. Place Hero: The Hortus Botanicus

**Emotional Goal:** Grounding the masterpiece in the scientific and trade-rich environment of 18th-century Amsterdam.

*   **Geographic Anchor:** **Amsterdam / The Hague**.
*   **Spatial Context:** The hero is layered over a sepia-toned **1720s Map of Amsterdam**. 
*   **The Reveal:** As the user scrolls, the map cross-fades into a 360-degree high-res photograph of the **Hortus Botanicus Amsterdam** (one of the world's oldest botanical gardens), linking the painting to its real-world horticultural inspiration.
*   **Narrative Overlay:** "In 1722, Amsterdam was the center of the world's flower trade. Van Huysum didn't just paint flowers; he documented the global reach of the Dutch Golden Age."

---

## 3. Media Viewer: The Microscopic Vanitas

**Emotional Goal:** Intense, unmediated connection to the technical and biological precision.

*   **UX Mode:** **"Macro Mode" (Zero-UI).** The cursor becomes a virtual "Magnifying Glass."
*   **Interaction:** 2000% zoom into the dewdrops, insects, and petal textures.
*   **Close Look Hotspots:**
    *   **"The Dew Drop":** Focus on a single glistening drop. Annotation: "Van Huysum's dewdrops were so realistic they were said to 'tremble' on the panel. They serve as a *Vanitas* symbol—a reminder of life's transience."
    *   **"The Hidden Guest":** Focus on an ant crawling along the marble plinth. Annotation: "Notice the ant. In the Dutch tradition, insects represent the inevitable decay that follows beauty."
    *   **"The Impossible Bouquet":** Focus on the mix of spring tulips and summer poppies. Annotation: "This bouquet is a fantasy. These flowers never bloomed together in 1722. Van Huysum painted them one by one, from life, as the seasons turned."
    *   **"The Chaffinch Nest":** Focus on the nest and its eggs. Annotation: "The nest symbolizes the fragility of life and the domestic harmony of the Dutch home."

---

## 4. Collection Entry: Masters of the Low Countries

**Emotional Goal:** Intellectual discovery of the Dutch botanical tradition.

*   **Component:** **"Dutch Still Life" Gallery Rail.**
*   **Content:** Related Getty and Rijksmuseum assets: Maria Sibylla Merian's **"Insects of Surinam"**, Rachel Ruysch's **"Flower Still Life"**, and Maria van Oosterwyck's **"Vanitas Still Life"**.
*   **Metadata Entry:** A digital citation of the **Getty Open Content Program**, honoring the 2013 initiative that made this 8K masterpiece freely available.

---

## 5. Commerce Entry: The Botanical Atelier

**Emotional Goal:** Bringing the opulence of the Dutch Golden Age into the modern home.

*   **Layout:** "The Van Huysum Atelier" curated shop.
*   **Products:** 
    *   **Masterwork Prints:** Ultra-high-res Giclée prints on museum-grade wood panel textures.
    *   **The "1722 Bloom" Fragrance:** A complex scent profile of Peony, Rose, and damp earth.
    *   **Botanical Silk Collection:** Scarves and textiles featuring the "Miraculous Bouquet" patterns.
    *   **The "Vanitas" Puzzle:** A 2000-piece high-density puzzle challenging the user to reconstruct the microscopic detail of the insects and dewdrops.
*   **CTA:** "Own a piece of the Golden Age. Support the Getty Museum’s Open Access mission."

---

## 6. Front-end Specifications (Summary)

| Parameter | Specification |
| :--- | :--- |
| **Transition Ease** | `cubic-bezier(0.25, 1, 0.5, 1)` (Sophisticated/Linear) |
| **Luminescence Shader** | Fragment shader for soft light pulsing on #D4AF37 and #FFB6C1 |
| **IIIF Engine** | OpenSeadragon with 8K tiling and "Macro-Lens" cursor overlay |
| **Color Temperature** | Warm "North Light" (3500K) to mimic a Dutch painter's studio |

---

**Next Steps:**
- Prototype the **"Macro-Lens"** interaction for the Media Viewer.
- Configure the **Getty ActivityStreams** to fetch related Dutch still-life metadata.
- Design the **"Botanical Atelier"** shop layout for mobile/desktop.
