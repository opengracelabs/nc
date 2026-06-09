# Great Wave Experience Blueprint v1: The Crest of the World

**Asset:** *Under the Wave off Kanagawa* (The Great Wave) (c. 1830–32)  
**Institution:** The Metropolitan Museum of Art (The Met)  
**Theme:** The Ukiyo-e "Floating World" / Nature vs. Human Endeavor  
**Core Objective:** Immerse the visitor in the dynamic energy of the Edo period, the spiritual power of Mount Fuji, and the timeless struggle and beauty of the sea.

---

## 1. Homepage Hero: The Great Crest

**Emotional Goal:** Instant kinetic energy and the feeling of being "caught in the moment."

*   **Visual:** Full-screen, high-resolution crop of the **cresting wave** and its "claw-like" foam. A subtle WebGL "Fluid" shader animates the foam, making it look like it's slowly reaching out toward the user's cursor.
*   **Typography:** Playfair Display (Serif) for elegance / Noto Sans JP for cultural grounding.
    *   *Headline:* "The Crest of the World"
    *   *Sub-headline:* "Experience Hokusai's masterpiece—the wave that defined a nation and captured the soul of Mount Fuji."
*   **Atmospheric Runtime:**
    *   **Palette:** `Prussian Blue` (#003153) and `Indigo` (#4B0082) backgrounds with `Shell White` (#FFF5EE) accents.
    *   **Audio:** Binaural recording of a heavy, rolling surf (low-end thunder) mixed with the sharp "clack" of woodblocks and a distant, ethereal bamboo flute (Shakuhachi).
*   **Interaction:** A "Dive In" button that triggers a "Spray" particle effect and scrolls the user into the Place Page.

---

## 2. Place Page: Mount Fuji & The Tōkaidō

**Emotional Goal:** A sense of pilgrimage and geographical awe; "The Mountain that Watches."

*   **Geographic Anchor:** **Mount Fuji** (Fujisan).
*   **UX Mode:** **"The Traveler's Journal."** The page is styled as an Edo-period travelogue.
*   **Interaction:** A vertical **"Stations of the Tōkaidō"** rail. As the user scrolls, they "travel" from Edo to the coast, with Mount Fuji remaining a persistent, calm anchor in the background, mirroring its role in Hokusai's series.
*   **Contextual Layers:**
    *   **Travel Intelligence:** Insights into the Tōkaidō road—the "Eastern Sea Road" connecting Edo and Kyoto.
    *   **Climate & Atmosphere:** Real-time weather overlay for the Fuji-Hakone-Izu National Park, blending modern data with the print's ca. 1830 atmosphere.
*   **Trust Element:** The Met "Asian Art Department" authority seal with a direct link to the Open Access collection.

---

## 3. Media Viewer: The Master's Ink

**Emotional Goal:** Scientific appreciation of the medium; "The Soul of the Woodblock."

*   **UX Mode:** **"Carving Mode"** (Zero-UI). All UI elements dissolve. The cursor becomes a virtual "Chisel" that reveals the underlying woodgrain texture and the specific "Prussian Blue" ink layering.
*   **Interaction:** 1500% zoom into the wave's foam and the distant Mount Fuji.
*   **Close Look Hotspots:**
    *   **"The Prussian Blue":** Focus on the deep blue hues. Annotation: "Hokusai was an early adopter of imported Prussian Blue ink, which gave his landscapes a new, vibrant depth previously unseen in ukiyo-e."
    *   **"The Claws of the Sea":** Focus on the foam. Annotation: "Hokusai's 'dragon-claw' foam influenced generations of artists, from Van Gogh to modern manga illustrators."
    *   **"The Calm Center":** Focus on Mount Fuji. Annotation: "Fuji represents stability and the eternal, standing silent as the boats (Oshiokuri-bune) navigate the chaos of the sea."

---

## 4. Collection Entry: The Floating World (Ukiyo-e)

**Emotional Goal:** Intellectual discovery; "The Golden Age of Japanese Prints."

*   **Component:** **"The Ukiyo-e Gallery" Rail.**
*   **Content:** Related Met assets: Hokusai's **"Red Fuji"**, Hiroshige's **"Sudden Shower over Shin-Ōhashi"**, and Utamaro's **"Selection of Insects"**.
*   **Metadata Entry:** A digital reproduction of the **Havemeyer Collection** stamp, honoring the 1929 bequest that brought this masterpiece to The Met.

---

## 5. Commerce Entry: The Edo Merchant

**Emotional Goal:** Bringing the aesthetic of the "Floating World" into the modern home.

*   **Layout:** "The Great Wave Boutique" curated shop.
*   **Products:** 
    *   **Masterwork Prints:** Giclée reproductions on traditional washi paper textures.
    *   **The "Deep Sea & Cedar" Fragrance:** A scent profile combining salt spray with the scent of Japanese cedar (Sugi) and ink.
    *   **Edo Traveler's Kit:** High-quality stationery and woodblock-inspired textiles (Furoshiki).
*   **CTA:** "Support The Met's Open Access mission with every purchase."

---

## 6. Front-end Specifications (Summary)

| Parameter | Specification |
| :--- | :--- |
| **Transition Ease** | `cubic-bezier(0.4, 0, 0.2, 1)` (Fluid/Oceanic) |
| **Foam Shader** | WebGL particle shader for dynamic white-water effects on #FFF5EE |
| **IIIF Engine** | Leaflet with deep-zoom support for large-format ukiyo-e |
| **Luminescence** | Cool, clear "Early Morning" light (5000K color temp) |

---

**Next Steps:**
- Prototype the **"Foam Shader"** for the Homepage Hero.
- Integrate the **Met API** for real-time metadata updates.
- Design the **"Traveler's Journal"** Place Page layout.
