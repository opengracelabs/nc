# NGA Experience Blueprint v1: The American Sublime

**Asset:** *The Voyage of Life: Youth* (1842)  
**Accession Number:** 1942.8.16  
**Institution:** National Gallery of Art (NGA)  
**Focus:** Hudson River School · American Landscape · Exploration · Roots of the National Parks

---

## 1. Wonder: The Homepage Hero ("The River of Life")

**Goal:** Capture the overwhelming awe and optimism of the 19th-century American landscape.

*   **Experience:** A full-bleed, cinematic entry. The hero section opens on a massive, extreme close-up of the glowing, ethereal castle in the sky, slowly panning down the river toward the youth in the boat.
*   **Visual:** A **"Sublime Light" WebGL shader** enhances the luminosity of the clouds and the reflections on the water, creating a vibrant, almost hyper-real atmosphere that defined the Hudson River School aesthetic.
*   **Audio:** A sweeping, orchestral swell inspired by Aaron Copland, mixed with the sound of rushing river water and wind through ancient pines.
*   **Interaction:** A "Follow the River" prompt that scrolls the user down, transitioning the celestial light of the painting into the geographical reality of the Place Page.

## 2. Trust: The National Archive

**Goal:** Establish the NGA as the premier guardian of American artistic heritage.

*   **Provenance Layer:** An interactive timeline documenting the painting's history, from its creation in Cole's Catskill studio to its eventual permanent home at the National Gallery in Washington, D.C.
*   **Institutional Seal:** The **NGA Open Access** verified badge, linking to the high-resolution IIIF master file.
*   **Technical Proof:** "The Allegorical Code" overlay—a visual breakdown explaining the symbolism Cole used: the hourglass on the boat, the guardian angel left behind, and the treacherous rapids looming in the next painting (*Manhood*).

## 3. Connection: The Place Page ("The Hudson River Valley")

**Goal:** Anchor Cole's allegorical landscape to the physical geography of the American Northeast and the broader conservation movement.

*   **Geographic Anchor:** The Hudson River Valley / Catskill Mountains (New York).
*   **Virtual Window:** A split-screen interaction:
    *   *Left:* Cole's idealized, painted landscape.
    *   *Right:* Modern, high-resolution photography of the Catskill Mountains (e.g., Kaaterskill Falls), showing the real-world geology that inspired his vision.
*   **The Conservation Engine:** A narrative pathway linking the Hudson River School's veneration of nature directly to the later establishment of the **US National Parks** (connecting Cole to subsequent artists like Moran and Bierstadt who painted Yellowstone and Yosemite).

## 4. Discovery: The Media Viewer ("The Explorer's Lens")

**Goal:** Allow users to explore the extreme detail and technique of 19th-century romanticism.

*   **Interaction:** 2000% IIIF Deep-Zoom into the canvas.
*   **Guided Hotspots:**
    *   **The Botanical Detail:** Zooming into the lush, meticulously painted foliage in the foreground, demonstrating Cole's commitment to botanical accuracy amidst allegorical fantasy.
    *   **The Guardian Angel:** Highlighting the subtle, translucent paint application used for the spiritual figures.
    *   **The Horizon:** Exploring the specific glazing techniques used to create the luminous, infinite depth of the sky.

## 5. Commerce: The Pioneer Boutique ("The Sublime Collection")

**Goal:** Translate the awe of the American landscape into high-end, inspirational products.

*   **Curated Products:**
    *   **Masterwork Prints:** Massive, museum-grade canvas giclée reproductions of the entire four-part *Voyage of Life* series.
    *   **"Catskill Pine" Scent:** A room fragrance combining notes of crisp mountain air, pine needles, and fresh river water.
    *   **The Explorer's Journal:** Premium, leather-bound notebooks featuring details of Cole's sketches, designed for modern travelers and National Park visitors.
*   **CTA:** "Support the preservation of American Art at the National Gallery."

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **Shader Engine** | WebGL 2.0 (Luminosity / Bloom enhancement) |
| **Audio** | Spatialized Orchestral (Optimistic / Swelling) |
| **IIIF Engine** | NGA Image API v2 (via OpenSeadragon) |
| **Transition** | `ease-out-expo` (Sweeping/Cinematic) |
| **Fonts** | EB Garamond / Roboto (Classic American publishing) |

---
*Blueprint validated by Gemini CLI for NC Experience Lab*
