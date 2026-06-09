# CMA Experience Blueprint v1: Mist and Mountains

**Asset:** *Cloudy Mountains* (dated 1130)  
**Accession Number:** 1933.220  
**Institution:** Cleveland Museum of Art (CMA)  
**Focus:** China · Southern Song Dynasty · Landscape (Shanshui) · Ink Painting

---

## 1. Wonder: The Homepage Hero ("The Endless Scroll")

**Goal:** Immerse the visitor in the contemplative, continuous rhythm of the handscroll format.

*   **Experience:** A horizontal, full-bleed cinematic entry. Instead of a static image, the hero section functions as a slow, continuous pan from right to left (the traditional viewing direction for a Chinese handscroll). 
*   **Visual:** The massive 17,333-pixel TIFF master is utilized to create an infinitely looping, ultra-high-resolution panning animation. A **"Mountain Mist" WebGL shader** adds a very subtle, dynamic layer of fog over the valleys.
*   **Audio:** Ambient sounds of a high-altitude bamboo forest—wind rustling through leaves, distant bird calls, and a sparse, meditative Guqin (zither) melody.
*   **Interaction:** The user's horizontal scroll directly controls the speed and direction of the pan across the painting.

## 2. Trust: The Literati Archive

**Goal:** Establish the CMA's authority and decode the complex layers of Chinese painting history.

*   **Provenance Layer:** An interactive map of the colophons and seals (red stamps) added to the scroll over centuries. Clicking a seal reveals the Emperor or scholar who owned the painting, tracing its journey from the 12th century to Cleveland.
*   **Institutional Seal:** The **CMA Open Access** verified badge, linking to the 160MB+ source TIFF.
*   **Technical Proof:** "The Mi-Family Dots" overlay—a visual explanation of Mi Youren's signature technique of using horizontal ink dots (dian) to build forms, rather than solid outlines.

## 3. Connection: The Place Page ("The Southern Landscape")

**Goal:** Anchor the philosophical landscape of the painting to the physical geography of Southern China.

*   **Geographic Anchor:** Jiangnan region (South of the Yangtze River), China.
*   **The Geography of Mist:** A visual comparison between Mi Youren's ink-wash techniques and modern atmospheric photography of the Huangshan (Yellow Mountains) or the misty peaks of Jiangxi.
*   **Cultural Context:** "The Scholar's Retreat." Explaining the Southern Song context, where artists retreated to the southern mountains following the fall of Northern China, turning the landscape into a symbol of resilience and inner peace.

## 4. Discovery: The Media Viewer ("The Scholar's Lens")

**Goal:** Provide unprecedented access to the materiality of the 12th-century paper and ink.

*   **Interaction:** A horizontally-locked IIIF Deep-Zoom viewer (leveraging the 17k pixel width).
*   **Guided Hotspots:**
    *   **The Lead-Paper:** Zooming into the texture of the rare lead-coated paper, which gives the ink its unique, silvery luminosity.
    *   **The Hidden Inscription:** Highlighting Mi Youren's own poetic inscription hidden in the upper corners.
    *   **The Wash Technique:** A close-up on the wet-on-wet ink application that defines the misty valleys.

## 5. Commerce: The Literati Studio ("The Jiangnan Collection")

**Goal:** Translate the tranquility of the Southern Song landscape into high-end architectural and lifestyle products.

*   **Curated Products:**
    *   **Panoramic Murals:** Utilizing the 17,333px width to offer custom-sized, seamless wall murals for modern minimalist interiors.
    *   **"Mountain Mist" Scent:** A room fragrance combining notes of wet stone, pine, and high-altitude air.
    *   **The Calligrapher's Kit:** Premium ink stones, brushes, and raw xuan paper.
*   **CTA:** "Support the preservation of Asian Art at the Cleveland Museum of Art."

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **Interaction Axis** | Horizontal (Right-to-Left priority) |
| **Shader Engine** | WebGL 2.0 (Dynamic Mist Generation) |
| **Audio** | Spatialized Ambient (High Altitude) |
| **Image Delivery** | Progressive IIIF loading (due to extreme aspect ratio) |
| **Fonts** | Noto Serif SC (Traditional Chinese support) / Lato |

---
*Blueprint validated by Gemini CLI for NC Experience Lab*
