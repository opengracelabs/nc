# Yellowstone Top 25 Collection v1

**Role:** Chief Curator  
**Objective:** Expand the Yellowstone collection to 25 assets, ranked by ingestion priority and experience impact.

---

## 1. Must Ingest (Critical Path)
*Core assets required for the primary launch experience (Threshold, Discovery, Story, and Patronage).*

| ID | Title | Category | Institution | Rights | Reason for Selection |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-001** | *Map of Yellowstone Lake* | Map | National Library of France | Public Domain | The foundational spatial authority (Bathymetric, 1871). |
| **EU-YEL-007** | *Hayden Survey Route Map* | Map | National Library of France | Public Domain | Guides the narrative journey along the actual expedition path. |
| **EU-YEL-002** | *Grand Canyon (Moran)* | Fine Art | British Library | Public Domain | The definitive visual icon that established Yellowstone's majesty. |
| **EU-YEL-018** | *The Morning Mist, Firehole River* | Photo | National Library of France | Public Domain | The primeval "Threshold" asset for the intro experience. |
| **EU-YEL-003** | *Old Faithful Geyser in Eruption* | Photo | National Library of France | Public Domain | W.H. Jackson's first photographic proof (Stereoview, 1871). |
| **EU-YEL-004** | *Mammoth Terraces (Watkins)* | Photo | Rijksmuseum | Public Domain | High-fidelity photographic authority from a 19th C master. |
| **EU-YEL-016** | *Bison Buffalo Study* | Fine Art | Rijksmuseum | Public Domain | Anchors the ecosystem and biological soul of the park. |
| **EU-YEL-008** | *Yellowstone: The Wonderland* | Poster | National Library of Australia | Public Domain | Primary commerce driver for vintage railway aesthetics. |
| **EU-YEL-010** | *WPA Yellowstone Poster* | Poster | Library of Congress (EU) | Public Domain | Essential mid-century aesthetic for high-velocity commerce. |
| **EU-YEL-025** | *First Survey Party* | Photo | Smithsonian (Europeana) | Public Domain | Humanizes the expedition and builds "Explorer's Lens" trust. |

---

## 2. Should Ingest (Deep Experience)
*Assets that provide depth to education, science, and the "Atmospheric Runtime."*

| ID | Title | Category | Institution | Rights | Reason for Selection |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-005** | *The Castle Geyser* | Fine Art | Wellcome Collection | CC BY | Detailed scientific/botanical illustration of geyserite. |
| **EU-YEL-006** | *Tower Falls (Sketch)* | Fine Art | Smithsonian (Europeana) | Public Domain | Shows Moran's field process before the final oil works. |
| **EU-YEL-014** | *Yellowstone Grizzly Plate* | Fine Art | Naturalis (Europeana) | Public Domain | Critical for biological taxonomy (Darwin Core) integration. |
| **EU-YEL-015** | *Thermal Basin Flora* | Fine Art | Wellcome Collection | CC BY | Anchors the "Close Look" educational layer for botany. |
| **EU-YEL-009** | *North Coast Limited* | Poster | British Library | Public Domain | Adds depth to the "Wonderland" era commerce rail. |
| **EU-YEL-011** | *Roosevelt Arch* | Photo | Stockholm Transport Museum | CC BY | Provides a geographic and architectural "Gateway" anchor. |
| **EU-YEL-019** | *Moonlight on the Lake* | Photo | Stockholm Transport Museum | CC BY | Perfect for testing the "Midnight Mode" UI theme. |
| **EU-YEL-022** | *Minerva Terrace (Macro)* | Photo | Wellcome Collection | CC BY | Demonstrates extreme microscopic fidelity for Infinite Zoom. |

---

## 3. Optional (Supporting Content)
*Long-tail assets for niche exploration and future collections.*

| ID | Title | Category | Institution | Rights | Reason for Selection |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-012** | *Yellowstone Bear Sign* | Photo | Internet Archive (EU) | Public Domain | Educational/humorous context for early tourism. |
| **EU-YEL-013** | *Grand Loop Road Map* | Map | National Library of France | Public Domain | Shows the transition from survey expedition to auto-tourism. |
| **EU-YEL-017** | *Petrified Forest Specimen* | Photo | Smithsonian (Europeana) | Public Domain | Geological depth for the "Primeval Forge" narrative. |
| **EU-YEL-020** | *Liberty Cap (Color)* | Fine Art | Rijksmuseum | Public Domain | Adds hand-colored "sublime" aesthetic to northern entrance. |
| **EU-YEL-021** | *Golden Gate Stereoview* | Photo | National Library of France | Public Domain | High depth-of-field for parallax UI effect testing. |
| **EU-YEL-023** | *Canyon Hotel Interior* | Photo | Stockholm Transport Museum | CC BY | Historical "Atmospheric Presence" for luxury tourism. |
| **EU-YEL-024** | *Boiling River Map* | Map | National Library of France | Public Domain | Thematic link for "Relationship Intelligence" (Chemistry). |

---

## 4. Implementation Readiness

*   **10 Must Ingest:** Immediate target for `europeana_adapter.py`.
*   **8 Should Ingest:** Scheduled for Phase 1.5 (Experience Deepening).
*   **7 Optional:** Backlog for Phase 2 (Long-tail Discovery).

---

**Next Steps:**
*   Validate the **Record URLs** for the "Must Ingest" Top 10 in the `yellowstone_launch_metadata_v1.md` package.
*   Assign `nc:atmosphere` presets (Primeval, Volatile, Grand) to all 25 assets.
*   Initiate high-resolution derivative generation (TIFF to HDR WebP).
