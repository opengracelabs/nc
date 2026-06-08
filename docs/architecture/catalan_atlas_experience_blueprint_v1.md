# Catalan Atlas Experience Blueprint v1: The Golden Threshold

**Asset:** *The Catalan Atlas* (c. 1375)  
**Institution:** Bibliothèque nationale de France (BnF) / Gallica  
**Theme:** Medieval Enlightenment / The Known World  
**Core Objective:** Transport the visitor into the golden, mythological, and commercial heart of the 14th-century worldview.

---

## 1. Homepage Hero: The Golden Threshold

**Emotional Goal:** Instant awe and the feeling of entering a "Secret Chamber" of history.

*   **Visual:** Full-bleed, high-contrast close-up of the **Mansa Musa** panel (Folio 6). The gold leaf on the king’s crown and orb has a subtle "Glimmer" shader that reacts to the mouse position.
*   **Typography:** Playfair Display (Serif) / Montserrat (Sans).
    *   *Headline:* "The Golden Worldview"
    *   *Sub-headline:* "Journey across the Silk Road through the 1375 Catalan Atlas—the masterpiece of medieval cartography."
*   **Atmospheric Runtime:**
    *   **Palette:** `Gold Leaf` (#D4AF37) accents on `Deep Vellum` (#F3E5AB) background.
    *   **Audio:** Low-frequency "Desert Wind" drone mixed with distant, rhythmic merchant bells and a faint Catalan polyphonic chant.
*   **Interaction:** A "Break the Seal" button that triggers a vellum-tearing sound effect and a transition into the Map Viewer.

---

## 2. Map Viewer: The Silk Road Journey

**Emotional Goal:** Empowerment through exploration; the feeling of "Unfolding the World."

*   **Interaction:** A horizontal-scroll **"Vellum Rail"** representing the 6 double leaves. 
*   **Transition:** As the user scrolls, the leaves "unfold" with a 3D depth effect.
*   **Discovery Paths:**
    *   **The Silk Road:** A glowing line traces the trade routes from Majorca to Cathay.
    *   **Mythological Beast Mode:** Toggling this reveals the locations of dragons, sirens, and giants described in the map’s text.
*   **Narrative Overlay:** Semi-translucent "Scroll" panels that translate the medieval Catalan text into modern prose in real-time.
*   **Trust Element:** BnF "Department of Manuscripts" authority seal with a direct IIIF link to Gallica.

---

## 3. Media Viewer: The Mansa Musa Close-up

**Emotional Goal:** Scientific and historical revelation; shifting perspectives on African history.

*   **UX Mode:** **"Illumination Mode"** (Zero-UI). All navigation fades. The cursor becomes a virtual "Magnifying Glass" that increases brightness and reveals the underlying vellum texture.
*   **Interaction:** 1200% IIIF zoom into the ink and gold leaf.
*   **Close Look Hotspots:**
    *   **"The Golden King":** Focus on Mansa Musa. Annotation: "The richest man in history, depicted here holding a gold nugget, reflecting the 14th-century's recognition of West African wealth."
    *   **"The Majorcan Ink":** Focus on the vibrant colors. Annotation: "Lapis Lazuli and Indigo were used to create the seas, signifying the immense cost and prestige of this royal commission."
    *   **"Navigation Logic":** Focus on the rhumb lines. Annotation: "These lines allowed sailors to calculate bearings, bridging the gap between medieval art and practical navigation."

---

## 4. Collection Entry: The Gallica Masterpiece

**Emotional Goal:** Deepen the academic and institutional context.

*   **Component:** **"The King's Library" Rail.**
*   **Content:** Related Gallica assets: The **Turgot Map of Paris**, **Redouté’s Roses**, and **Cassini’s Geodesic Surveys**.
*   **Metadata Entry:** A sidebar with a high-fidelity scan of the **E.30 BnF Manuscript Tag**, establishing the asset's "Institutional DNA."

---

## 5. Commerce Entry: The Merchant's Portfolio

**Emotional Goal:** Materialize the wonder into physical patronage.

*   **Layout:** "Treasures of the Atlas" curated shop.
*   **Products:** 
    *   **The 1375 Masterpiece Reprints:** High-fidelity giclée prints on textured vellum-style paper.
    *   **The Silk Road Scent:** A sensory extension (Scent: Saffron, Myrrh, Aged Paper).
    *   **Medieval Chart Puzzles:** A 2,000-piece challenge focused on the intricate cartography of the Mediterranean.
*   **CTA:** "Your purchase supports the continued digitization of the BnF Manuscript Collection."

---

## 6. Front-end Specifications (Summary)

| Parameter | Specification |
| :--- | :--- |
| **Transition Ease** | `ease-in-out-sine` (Smooth/Weighty) |
| **Glimmer Shader** | WebGL shader for specular highlights on Gold Hex #D4AF37 |
| **IIIF Engine** | OpenSeadragon with Multi-Canvas support |
| **Luminescence** | Warm "Candlelight" glow (2700K color temp) |

---

**Next Steps:**
- Prototype the **"Vellum Rail"** 3D unfolding animation.
- Configure the **Gallica IIIF Service** for multi-canvas rendering.
- Test the **"Glimmer Shader"** on high-resolution gold leaf areas.
