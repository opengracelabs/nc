# Catalan Atlas Asset Zero Metadata Package v1

**Asset:** *Atlas de cartes marines, dit Atlas catalan* (The Catalan Atlas)  
**ARK Identifier:** `ark:/12148/btv1b55002481n`  
**Creator:** Abraham Cresques (1325–1387)  
**Atmosphere Target:** Golden Wonder / Medieval Enlightenment

---

## 1. Technical Metadata

| Attribute | Value |
| :--- | :--- |
| **ARK Identifier** | `ark:/12148/btv1b55002481n` |
| **Institution ID** | `Espagnol 30` |
| **Rights URI** | [https://gallica.bnf.fr/edit/und/conditions-dutilisation-des-contenus-de-gallica](https://gallica.bnf.fr/edit/und/conditions-dutilisation-des-contenus-de-gallica) (Public Domain Mark) |
| **IIIF Manifest** | `https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/manifest.json` |
| **Image Service (Folio 1)**| `https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/f1` |
| **Dimensions (Physical)** | 645 x 250 mm (6 double leaves) |
| **Media Type** | `image/tiff` (Master) / `image/jp2` (IIIF Service) |

---

## 2. Institutional Metadata

*   **Institution:** Bibliothèque nationale de France (BnF)
*   **Department:** Département des Manuscrits
*   **Creation Year:** c. 1375
*   **Object Type:** Manuscript on Vellum (Mappa Mundi / Portolan Atlas)
*   **Canonical URL:** [https://gallica.bnf.fr/ark:/12148/btv1b55002481n](https://gallica.bnf.fr/ark:/12148/btv1b55002481n)

---

## 3. Ingestion Profile (Universal Media Substrate)

1.  **Canvas Painting:** Multi-page IIIF manifest support required for 12 physical faces (6 double leaves).
2.  **Atmospheric Anchor:**
    *   **Vibe:** `Golden Wonder`
    *   **Palette:** `Gold Leaf` (#D4AF37) / `Aged Vellum` (#F3E5AB) / `Royal Indigo` (#4B0082)
    *   **Audio:** `Silk Road Sand Winds` / `Mediterranean Merchant Bells` / `Medieval Catalan Polyphony`
3.  **Intelligence Bridge:**
    *   **CIDOC CRM:** `E22 Human-Made Object`
    *   **Schema.org:** `schema:Map`
    *   **GeoNames:** `Q12555` (Timbuktu), `Q12534` (Niger River)

---

**Next Steps:**
- Execute `workers/ingestion_worker/gallica_adapter.py` for ARK `btv1b55002481n`.
- Verify **IIIF Multi-Canvas rendering** for the 6 double leaves.
- Map the **Mansa Musa focus-point** (Folio 6) to the West African Discovery Path.
