# Walters Experience Blueprint v1: The Gilded Word

**Asset:** *The Missal of Eberhard von Greiffenklau* (15th Century)  
**Object Number:** W.174  
**Institution:** Walters Art Museum  
**Focus:** Illuminated Manuscripts · Medieval Europe · Scriptoria · Gold Leaf · Vellum

---

## 1. Wonder: The Homepage Hero ("The Illuminated Portal")

**Goal:** Induce awe through the profound material beauty and spiritual luminosity of medieval gold leaf.

*   **Experience:** A full-bleed, cinematic entry. The hero section opens on an extreme macro-level view of the manuscript's golden halo. A custom **"Burnished Gold" WebGL shader** reacts to the user's cursor or device tilt, causing the digital gold leaf to catch the light and glint realistically, mimicking the experience of holding the physical book under candlelight.
*   **Visual:** Ultra-high-resolution crop of the intricate marginalia and the central miniature.
*   **Audio:** Ambient soundscape of a 15th-century scriptorium: the rhythmic scratching of a quill on vellum, the distant, echoing chant of monastic plainsong, and the soft turning of heavy parchment pages.
*   **Interaction:** A "Turn the Page" prompt that smoothly transitions the hero image into the deep-zoom Media Viewer, revealing the full manuscript leaf.

## 2. Trust: The Scriptorium Archive

**Goal:** Establish the Walters as a premier global authority on medieval book arts and provenance.

*   **Provenance Layer:** An interactive timeline tracing the Missal from its creation for Eberhard von Greiffenklau (Prebendary of Mainz) through centuries of European collections, culminating in its acquisition by Henry Walters.
*   **Institutional Seal:** The **Walters Open Access** verified badge, linking to the official CSV dataset and acknowledging the CC0 status.
*   **Technical Proof:** "The Material Code" overlay—a visual breakdown of the page's anatomy, identifying the ruling lines, the prick marks used for layout, the specific pigments (lapis lazuli, vermilion), and the application of gold leaf over gesso.

## 3. Discovery: The Media Viewer ("The Illuminator's Lens")

**Goal:** Provide unprecedented, tactile access to the materiality of vellum and medieval pigment.

*   **Interaction:** 2000% Deep-Zoom capability (using the direct high-res JPEG delivery from the Walters CDN).
*   **Guided Hotspots:**
    *   **The Vellum Texture:** Zooming into the unpainted margins to observe the hair follicles and follicle patterns of the animal skin, connecting the "book" back to the "nature" of its origin.
    *   **The Historiated Initial:** Deconstructing the narrative contained within the first large letter of the text.
    *   **The Marginalia:** Exploring the often humorous or bizarre creatures (drolleries) painted in the borders, discussing their role in medieval visual culture.

## 4. Collection Entry: The Medieval Treasury

**Goal:** Broaden the discovery path into the wider context of Medieval and Byzantine art.

*   **Component:** **"The Treasury" Rail.**
*   **Content:** Related Walters assets showcasing their unique strengths: **Byzantine Enamels** (e.g., Limoges chasses), **Gothic Ivory Diptychs**, and **Islamic Illuminated Manuscripts** (to show cross-cultural book arts).
*   **Metadata Entry:** A digital replica of Henry Walters' original catalog notes, grounding the collection in its historical acquisition context.

## 5. Commerce: The Master’s Guild ("The Scriptorium Collection")

**Goal:** Translate the painstaking craftsmanship of the Middle Ages into high-end, tactile lifestyle products.

*   **Curated Products:**
    *   **Premium Stationery:** High-weight, vellum-textured notebooks featuring the manuscript's marginalia and gold-foil stamped initials.
    *   **"Monastic Ink" Scent:** A room fragrance combining notes of oak gall ink, old paper, beeswax, and cold stone.
    *   **Illuminator's Kits:** Educational and artistic kits containing genuine gold leaf, burnishers, and traditional pigment recipes.
    *   **Masterwork Prints:** Giclée reproductions printed on specialized rag paper to maximize pigment depth.
*   **CTA:** "Support the preservation of the book arts at the Walters Art Museum."

---

## Technical Specifications

| Parameter | Specification |
| :--- | :--- |
| **Shader Engine** | WebGL 2.0 (Burnished Gold / Specular Reflection) |
| **Audio** | Spatialized Ambient (Scriptorium / Chant) |
| **Image Delivery** | Direct High-Res JPEG (via Walters CDN `art.thewalters.org`) |
| **Transition** | `page-turn` (3D easing) |
| **Fonts** | Uncial Antiqua / Cinzel (Medieval manuscript meets modern serif) |

---
*Blueprint validated by Gemini CLI for NC Experience Lab*
