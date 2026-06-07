# Asset Zero Experience Build: Jackson Photograph

**Asset:** *Old Faithful Geyser in Eruption* (1871)  
**Creator:** William Henry Jackson  
**Medium:** Albumen Print / Stereoview  
**Core Theme:** The Mechanical Witness (Trust & Proof)

---

## 1. Homepage Hero: The Threshold of Proof

**Emotional Goal:** Transition from skepticism to undeniable truth.

*   **Visual:** A large, centered, hand-colored stereoview (Asset Zero) against a deep obsidian background. The image has a subtle "breathe" animation.
*   **Typography:** Baskerville Bold.
    *   *Headline:* "1871: The Moment Rumor Became Reality."
    *   *Sub-headline:* "William Henry Jackson’s camera provided the first mechanical proof of Yellowstone’s wonders."
*   **Trust Anchor:** A prominent, semi-translucent badge: **“Institutional Record: National Library of France.”**
*   **Interaction:** A "Witness the Discovery" button that initiates a slow-zoom into the geyser's steam.

---

## 2. Place Hero: The Geographic Anchor

**Emotional Goal:** Ground the asset in its specific geological and historical coordinate.

*   **Spatial Context:** The hero is layered over a desaturated version of **Henry Elliott’s 1871 Map**.
*   **The Reveal:** As the user scrolls into the "Upper Geyser Basin" coordinate, the map blurs, and the Jackson photograph cross-fades into focus.
*   **Atmospheric Runtime:**
    *   **Palette:** "Wet-Plate Grey" (#2F2F2F) with "Parchment White" (#F4F1EA) accents.
    *   **Audio:** The low-frequency, rhythmic "hiss" of a 19th-century steam geyser, captured as a binaural field recording.
*   **Narrative Overlay:** "You are standing where Jackson stood in September 1871. At this moment, the world changed."

---

## 3. Media Viewer: The Infinite Zoom of Discovery

**Emotional Goal:** Unmediated connection to the tactile reality of the discovery.

*   **UX Mode:** **Zero-UI.** All text, buttons, and margins fade to 0% opacity upon interaction.
*   **Fidelity Target:** 8K Tiled IIIF delivery.
*   **The "Discovery" Interactions:**
    *   **Grain Investigation:** The user zooms past the image into the actual silver gelatin grain of the 1871 plate.
    *   **Stereoview Depth:** A toggle allows the user to see the "Left" and "Right" eye views simultaneously, mimicking the 19th-century 3D experience.
*   **Annotated Proof (Close Look):**
    *   **Hotspot A: "The Signature."** Zoom into Jackson’s etched survey number (#127) on the bottom right corner of the glass plate.
    *   **Hotspot B: "Geyserite Texture."** An extreme macro view of the mineral deposits at the geyser's base, linked to the modern **Darwin Core** mineralogy dataset.
    *   **Hotspot C: "The Steam Column."** Explains the 1871 exposure time required to capture the moving water, linking technology to the "Spirit of Place."

---

## 4. Experience Validation: Trust, Proof, Discovery

| Component | Trust Strategy | Discovery Result |
| :--- | :--- | :--- |
| **Homepage** | Institutional Citation | Skepticism is replaced by institutional authority. |
| **Place Hero** | Spatial Grounding | The asset is a "witness" to a specific coordinate. |
| **Media Viewer** | Tactile Fidelity | The user "discovers" the microscopic truth of the artifact. |

---

**Next Steps:**
*   Configure the **IIIF Manifest** to support the 3D Stereoview toggle.
*   Coordinate with the **Atmospheric Worker** to isolate the "1871 Steam Hiss" audio track.
*   Implement the **"Institutional Badge"** CSS component for the Homepage.
