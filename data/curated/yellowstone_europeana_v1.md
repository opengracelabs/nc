# Yellowstone Europeana Collection v1

**Role:** Chief Curator  
**Collection:** Europeana First Acquisition (Yellowstone)  
**Status:** Ingestion Ready (Phase 1)  
**Total Assets:** 25  

---

## 1. Masterpiece Tier: The Hayden Survey (1871-1872)

These assets represent the absolute "authority" of Yellowstone's discovery and are critical for the **Yellowstone Experience v1**.

| ID | Title | Institution | Rights | Rank | Reason for Inclusion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-001** | *Map of Yellowstone Lake (Bathymetric)* | National Library of France | Public Domain | 1 | The first scientific mapping of the lake by Henry Wood Elliott. |
| **EU-YEL-002** | *Grand Canyon of the Yellowstone (Chromolithograph)* | British Library | Public Domain | 2 | Thomas Moran's iconic view that defined the "Sublime West." |
| **EU-YEL-003** | *Old Faithful Geyser in Eruption (Stereoview)* | National Library of France | Public Domain | 3 | W.H. Jackson's first visual proof of the geyser's power. |
| **EU-YEL-004** | *Mammoth Hot Springs Terraces (Albumen Print)* | Rijksmuseum | Public Domain | 4 | High-fidelity photographic record of the northern entrance. |
| **EU-YEL-005** | *The Castle Geyser, Firehole Basin* | Wellcome Collection | CC BY | 5 | Detailed scientific illustration of geyserite structures. |
| **EU-YEL-006** | *Tower Falls (Pencil Sketch)* | Smithsonian (Europeana) | Public Domain | 6 | Thomas Moran's raw field sketch before the oil masterpiece. |
| **EU-YEL-007** | *General Map of the Hayden Survey Route* | National Library of France | Public Domain | 7 | Essential for the "Explorer's Lens" scrollytelling path. |

---

## 2. Tourism & Poster Tier: The Wonderland Era (1900-1940)

These assets provide the commercial and aesthetic "vibe" for the **Patronage Flow** (Shopify integration).

| ID | Title | Institution | Rights | Rank | Reason for Inclusion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-008** | *Yellowstone: The Wonderland (Railway Poster)* | National Library of Australia | Public Domain | 8 | High commercial value for vintage wall art. |
| **EU-YEL-009** | *North Coast Limited: Yellowstone Park Line* | British Library | Public Domain | 9 | Iconic NPRR branding for puzzles and calendars. |
| **EU-YEL-010** | *WPA Yellowstone Poster (1938)* | Library of Congress (EU) | Public Domain | 10 | The definitive mid-century aesthetic for premium prints. |
| **EU-YEL-011** | *Roosevelt Arch: For the Benefit of the People* | Stockholm Transport Museum | CC BY | 11 | Architectural anchor for the park's northern gateway. |
| **EU-YEL-012** | *Yellowstone Bear "Don't Feed" (Vintage Sign)* | Internet Archive (EU) | Public Domain | 12 | Educational/Humorous value for gift-shop items. |
| **EU-YEL-013** | *Grand Loop Road Map (1920)* | National Library of France | Public Domain | 13 | Shows the evolution of early automobile tourism. |

---

## 3. Scientific & Botanical Tier: The Living Frontier

Assets that link the place to the **Taxonomy & Bio** standards (Darwin Core).

| ID | Title | Institution | Rights | Rank | Reason for Inclusion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-014** | *Yellowstone Grizzly (Anatomical Plate)* | Naturalis (Europeana) | Public Domain | 14 | Connects fauna to the biological authority substrate. |
| **EU-YEL-015** | *Thermal Basin Flora (Watercolor)* | Wellcome Collection | CC BY | 15 | High educational value for "Close Look" annotations. |
| **EU-YEL-016** | *Bison Buffalo Study (19th C)* | Rijksmuseum | Public Domain | 16 | Iconic species anchor for the Yellowstone ecosystem. |
| **EU-YEL-017** | *Petrified Forest Specimen* | Smithsonian (Europeana) | Public Domain | 17 | Geological link to the "Primeval Forge" theme. |

---

## 4. Atmospheric & Ephemera Tier: The "Spirit of Place"

Stereoscopic views and hand-colored prints that define the **NC Atmosphere Runtime**.

| ID | Title | Institution | Rights | Rank | Reason for Inclusion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-018** | *The Morning Mist: Firehole River* | National Library of France | Public Domain | 18 | Perfect for the "Threshold of Wonder" hero video. |
| **EU-YEL-019** | *Yellowstone Postcard: Moonlight on the Lake* | Stockholm Transport Museum | CC BY | 19 | Defines the "Midnight Mode" UI luminescence. |
| **EU-YEL-020** | *Liberty Cap (Hand-Colored Print)* | Rijksmuseum | Public Domain | 20 | Captures the "Sublime" lighting of the northern basin. |
| **EU-YEL-021** | *Golden Gate Canyon (Stereoview)* | National Library of France | Public Domain | 21 | High depth-of-field for parallax UI effects. |
| **EU-YEL-022** | *Minerva Terrace (Detailed Photo)* | Wellcome Collection | CC BY | 22 | Extreme microscopic detail for Infinite Zoom. |
| **EU-YEL-023** | *Canyon Hotel (Vintage Interior)* | Stockholm Transport Museum | CC BY | 23 | Historical tourism context for "Atmospheric Presence." |
| **EU-YEL-024** | *Boiling River (Thermal Map)* | National Library of France | Public Domain | 24 | Thematic link to the "Chemical Frontier" intelligence. |
| **EU-YEL-025** | *First Survey Party (Group Portrait)* | Smithsonian (Europeana) | Public Domain | 25 | Human element for the "Explorer's Lens" narrative. |

---

**Next Steps:**
- Ingest via `workers/ingestion_worker/europeana_adapter.py`.
- Apply `nc:atmosphere` tags (Primeval, Volatile, Grand) in PostgreSQL.
- Map top 5 assets to Shopify Product Variants in the `natureandculture.shop` pipeline.
