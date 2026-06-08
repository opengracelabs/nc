# Kyoto Asset Zero Experience v1: Kinkaku-ji in Snow

**Asset:** *Kinkaku-ji (The Golden Pavilion)*  
**Creator:** Utagawa Hiroshige (c. 1834)  
**Theme:** Sacred Stillness / The Winter Garden  
**Core Objective:** Transport the visitor into the meditative silence of Edo-period Kyoto.

---

## 1. Homepage Hero: The Threshold of Stillness

**Emotional Goal:** Instant tranquility and aesthetic awe.

*   **Visual:** Full-bleed, edge-to-edge cinematic slow-fade into the Hiroshige print. The image has a subtle "Parallax Snow" effect where the foreground snow particles drift slower than the background temple.
*   **Typography:** SF Pro Light / Baskerville Italic.
    *   *Headline:* "Kyoto: The Sacred Stillness."
    *   *Sub-headline:* "Enter the winter garden of the Golden Pavilion, through the lens of Utagawa Hiroshige."
*   **Atmospheric Runtime:**
    *   **Palette:** `Paper White` (#F4F1EA) UI with `Midnight Indigo` (#1A1A2E) shadows.
    *   **Audio:** A single, resonant temple bell strike that echoes for 15 seconds, followed by the faint sound of wind through snow-laden pines.
*   **Interaction:** A "Descend into Zen" indicator that pulses like a slowing breath.

---

## 2. Place Hero: The Geographic Portal

**Emotional Goal:** Ground the masterpiece in the sacred geography of Kyoto.

*   **Visual:** An 18th-century woodblock map of Kyoto (Edo period) is the base layer.
*   **The Reveal:** As the user scrolls, a golden pulse appears at the Kinkaku-ji coordinate. The map dissolves into the high-resolution Hiroshige print.
*   **Narrative Overlay:** "1834: Before the modern world, there was only the pavilion and the seasons. You are standing at the edge of the Mirror Pond."
*   **Trust Element:** Verification badge from the **Rijksmuseum, Amsterdam** with a direct link to the authority record.

---

## 3. Media Viewer: The Infinite Zoom of the Soul

**Emotional Goal:** Unmediated, tactile connection to 19th-century craft.

*   **UX Mode:** **Zero-UI.** All navigation and labels fade to 0% opacity.
*   **Interaction:** High-fidelity IIIF zoom into the woodblock stippling.
*   **Close Look Hotspots:**
    *   **"The Gold Leaf":** Zoom into the pavilion's upper stories. Annotation: "Hiroshige uses yellow ink to mimic the 200,000 sheets of gold leaf that cover the original structure."
    *   **"Gofun Snow":** Zoom into the white flakes. Annotation: "The 'snow' is created using a technique called *gofun*—crushed oyster shells mixed into the ink for a tactile, raised texture."
    *   **"The Zen Garden":** Zoom into the shoreline. Annotation: "The islands in the Mirror Pond represent the Crane and the Tortoise, symbols of longevity in Zen philosophy."

---

## 4. Collection Entry: The Explorer’s Lens

**Emotional Goal:** Establish academic and historical trust.

*   **Component:** **The "Kyoto Meisho" Rail.**
*   **Content:** A horizontal rail showing the other 9 prints in Hiroshige's *Famous Places in Kyoto* series, presented as a "Discovery Flywheel."
*   **Metadata:** Displayed in a semi-translucent "Glassmorphism" panel using SF Pro Mono for technical specs (Series, Date, Paper Type).

---

## 5. Commerce Placement: Patronage Flow

**Emotional Goal:** Allow the user to "bring the stillness home."

*   **Layout:** A "Curator’s Choice" spotlight at the bottom of the Place Page.
*   **Products:** 
    *   **Masterpiece Print:** Remastered, high-fidelity woodblock replica on washi-style paper.
    *   **Winter Garden Candle:** A sensory extension (Scent: Pine, Cold Air, Incense).
    *   **Kyoto Puzzle:** A 1,000-piece study of the Kinkaku-ji winter landscape.
*   **CTA:** "Support the Kyoto Preservation Fund."

---

## 6. Front-end Specifications (Summary)

| Parameter | Specification |
| :--- | :--- |
| **Transition Ease** | `cubic-bezier(0.4, 0, 0.2, 1)` (Rhythmic/Slow) |
| **UI Luminescence** | 90% (Paper White) to 10% (Indigo) |
| **Audio Bitrate** | 320kbps (Binaural Spatial Audio) |
| **Zoom Target** | 800% (Texture Visible) |

---

**Next Steps:**
- Implementation of the **"Parallax Snow"** CSS shader.
- Integration of the **Rijksmuseum IIIF Manifest** (`RP-P-1956-591`).
- Validation of the **"Temple Bell"** audio loop for seamless playback.
