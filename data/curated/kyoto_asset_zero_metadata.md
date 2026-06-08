# Kyoto Asset Zero Metadata Package v1

**Asset:** *Kinkaku-ji* (The Golden Pavilion)  
**Series:** *Famous Views of Kyoto* (Kyōto meisho no uchi)  
**Creator:** Utagawa Hiroshige (1797–1858)  
**Atmosphere Target:** Sacred Stillness / Zen Motion

---

## 1. Technical Metadata

| Attribute | Value |
| :--- | :--- |
| **OAI Identifier** | `oai:rijksmuseum.nl:RP-P-1956-591` |
| **Rijksmuseum ID** | `RP-P-1956-591` |
| **Rights URI** | [http://creativecommons.org/publicdomain/zero/1.0/](http://creativecommons.org/publicdomain/zero/1.0/) |
| **IIIF Manifest** | `https://data.rijksmuseum.nl/api/iiif/manifests/RP-P-1956-591` |
| **Image Service** | `https://www.rijksmuseum.nl/api/iiif/RP-P-1956-591` |
| **Dimensions** | 5600 x 3600 pixels (8K Tiled Master) |
| **Media Type** | `image/jp2` (JPEG2000) / `image/webp` (HDR Derivative) |

---

## 2. Institutional Metadata

*   **Institution:** Rijksmuseum, Amsterdam
*   **Collection:** Rijksprentenkabinet (Print Room)
*   **Creation Year:** c. 1834
*   **Object Type:** Woodblock print (*nishiki-e*)
*   **Canonical URL:** [https://www.rijksmuseum.nl/en/collection/RP-P-1956-591](https://www.rijksmuseum.nl/en/collection/RP-P-1956-591)

---

## 3. Ingestion Profile (Universal Media Substrate)

1.  **Canvas Painting:** Paint to a 2D Canvas with a resolution of 5600x3600.
2.  **Atmospheric Anchor:**
    *   **Vibe:** `Sacred Stillness`
    *   **Palette:** `Paper White` (#F4F1EA) / `Moss Green` (#8A9A5B)
    *   **Audio:** `Temple Bell Echo` / `Wind through Pine`
3.  **Intelligence Bridge:**
    *   **CIDOC CRM:** `E22 Human-Made Object`
    *   **Schema.org:** `schema:VisualArtwork`
    *   **GeoNames:** `Q1207577` (Kinkaku-ji)

---

**Next Steps:**
- Execute `workers/ingestion_worker/rijksmuseum_adapter.py` for ID `RP-P-1956-591`.
- Verify the **Infinite Zoom** on the woodblock stippling.
- Map the **Temple Bell** audio trigger to the scrollytelling path.
