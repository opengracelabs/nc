# Nature & Culture Experience Wireframe v1

**Role:** Chief Curator  
**Objective:** Design the "Ideal Emotional Journey" for the Nature & Culture digital portal, focusing on Wonder, Trust, Atmosphere, and Place.

---

## 1. Visual & Experience Principles: The "Atmospheric Runtime"

| Principle | Strategic Execution | Reference Model |
| :--- | :--- | :--- |
| **Typography** | **Baskerville** (Serif) for narrative/headers; **SF Pro** (Sans) for utility/data. | Apple / NatGeo |
| **Spacing** | **Negative Space as Luxury.** Wide margins and generous gutters to let media "breathe." | Rijksmuseum |
| **Atmosphere** | **Dynamic Luminescence.** UI background shifts based on the "mood" of the hero asset (e.g., Midnight, Golden Hour). | Apple TV+ |
| **Motion** | **The Parallax Reveal.** Subtle depth layers that shift as the user scrolls, creating a "portal" effect. | Apple / BBC Earth |
| **Hierarchy** | **Media-First.** 70% visual, 20% narrative, 10% utility/data. | Google Arts & Culture |

---

## 2. The Homepage: The Threshold of Wonder

**Emotional Goal:** Instant awe and the feeling of starting an "Expedition."

### Layout Blocks:
1.  **The Threshold (Hero):** 
    *   **Visual:** Full-bleed, edge-to-edge cinematic video (silent, slow-motion) of a flagship location (e.g., Yellowstone Geyser).
    *   **Overlay:** Minimalist typography centered: "Nature & Culture." Sub-headline: "The World, Curated."
    *   **Interaction:** A "Scroll to Descend" indicator that pulses like a heartbeat.
2.  **The Expedition Rail (Places):**
    *   **Visual:** A horizontal, high-inertia carousel of Flagship Places.
    *   **Behavior:** As a place enters the center, the background luminescence of the entire page shifts to match that place's "Mood Palette."
3.  **The Story Flywheel (Process):**
    *   **Visual:** A vertical scrollytelling section showing an **Asset** (Darwin Sketch) -> **Opportunity** (The Voyage) -> **Place** (Galápagos) -> **Collection** (The Darwin Archive).
    *   **Goal:** Build trust by showing the academic and custodial pipeline.
4.  **The Patronage Spotlight (Shop):**
    *   **Visual:** "The Curator's Choice"—a high-fidelity product render (e.g., a framed Saville-Kent lithograph) floating in a void-space with a direct shop CTA.

---

## 3. Flagship Place Journey (Yellowstone to Machu Picchu)

### 3.1 First Impression: The "Genius Loci" Hero
*   **Layout:** A large, high-res historical map (e.g., Elliott's 1871 Yellowstone) that slowly fades into a contemporary 8K vista as the user scrolls.
*   **Atmosphere:** Spatial audio begins at 10% volume—a "whisper of the place."

### 3.2 Discovery Flow: The Spatial Dive
*   **Interaction:** Users scroll "down" into the map. As they zoom, "Atmospheric Pins" appear.
*   **Behavior:** Hovering over a pin reveals a microscopic preview of the asset (Photo or Art) and increases the local audio volume (e.g., the sound of a geyser becomes more distinct).

### 3.3 Story Flow: The Explorer’s Lens
*   **Component:** The **"Journal Rail"**. 
*   **UI:** Semi-translucent "Glassmorphism" panels float over the media. Typography is Baskerville Italic, mimicking a handwritten field note.
*   **Narrative Voice:** The text is always first-person (Darwin, Muir, Bird, Bingham), establishing an intimate, human connection.

### 3.4 Media Flow: The "Infinite Zoom" Gallery
*   **UX:** Selecting an asset triggers a **"Zero-UI" transition**. All navigation and text fade away.
*   **Interaction:** High-fidelity deep zoom. "Close Look" annotations appear as subtle, glowing points that expand into narrative captions only when tapped.

### 3.5 Tourism Flow: The Mindful Gateway
*   **Section:** "Presence & Preservation."
*   **Visual:** A stark, beautiful film segment highlighting the site's current vulnerability.
*   **Trust Element:** Verification badges (UNESCO, Smithsonian, etc.) are displayed with academic citations.

### 3.6 Patronage Flow: Remastered Appreciation
*   **Section:** "Own the Story."
*   **UX:** A curated rail of Shopify products derived *only* from the assets just viewed. 
*   **Messaging:** "Support this Sanctuary through Patronage."

---

## 4. Emotional Journey Map by Place

| Place | Emotional Core | Mood Palette | Key Experience Moment |
| :--- | :--- | :--- | :--- |
| **Yellowstone** | Primeval Wonder | Sulfur / Deep Forest | The "Thermal Audio" geyser trigger. |
| **Yosemite** | Divine Serenity | Granite / Golden Hour | The "Watkins Parallax" granite zoom. |
| **Galápagos** | Scientific Mystery | Pacific / Volcanic | The "Darwin Journal" sketch reveal. |
| **G.B. Reef** | Fragile Vibrancy | Aquamarine / Coral | The "Saville-Kent" underwater bloom. |
| **Kyoto** | Sacred Stillness | Moss / Paper White | The "Zen Motion" blossom fade. |
| **Machu Picchu** | Celestial Grandeur | Mist / Sky Blue | The "Andean Flyover" cloud-break. |

---

## 5. Front-end Principles for Experience Fidelity

1.  **Motion Blur & Inertia:** All transitions (zooms, scrolls, fades) must have a "Physicality." Avoid abrupt cuts; use 300ms-600ms easements.
2.  **Sensory Synchronization:** If the user zooms into a waterfall in Yosemite, the audio volume of the water must increase in logarithmic sync with the zoom level.
3.  **Temporal Fluidity:** If the user is browsing at 10:00 PM local time, the UI should default to "Midnight Mode," with lower contrast and deeper, more nocturnal soundscapes.

---

**Next Steps:**
*   Prototype the "Thermal Audio" logarithmic sync for Yellowstone.
*   Finalize the "Baskerville Field Note" CSS styling for the Journal Rail.
*   Coordinate with the Ingestion Worker to ensure all assets have "Atmospheric Anchors" (Vibe, Lighting, Sound).
