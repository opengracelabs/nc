# Commerce Intelligence Validation Dataset v1.0

This dataset serves as the primary benchmark for calibrating the **Commercial Success Model (CSM)** scoring engine. It contains "Gold Standard" evaluations for iconic heritage assets, alongside a control asset to test the model's ability to reject low-value items.

---

## 1. The Benchmark Assets

### 3.1 Thomas Moran: *The Grand Canyon of the Yellowstone* (1872)
*   **Asset Type:** Fine Art (Hand-colored Lithograph / Oil Painting)
*   **Classification:** **MASTERWORK**
*   **Aggregate CSP:** **98.25**
*   **Scoring Breakdown:**
    *   **VAS (Visual Authority):** 100/100 (Highest tier of American landscape art)
    *   **PIS (Place Identity):** 100/100 (The definitive visual record of the park)
    *   **SSS (Story Strength):** 95/100 (Instrumental in the creation of the first National Park)
    *   **TAS (Tourism Appeal):** 100/100 (Universal "Bucket List" recognition)
    *   **IPS (Institutional Prestige):** 100/100 (Smithsonian / National Gallery)
    *   **PVS (Product Versatility):** 90/100 (Exceptional for wall art and luxury books)
    *   **RCS (Rights Clarity):** 100/100 (Public Domain)

### 3.2 1871 Hayden Survey Map (Yellowstone)
*   **Asset Type:** Cartography (Lithograph)
*   **Classification:** **MASTERWORK**
*   **Aggregate CSP:** **95.25**
*   **Scoring Breakdown:**
    *   **VAS:** 95 (Exquisite technical detail and historic patina)
    *   **PIS:** 100 (The blueprint of the park's boundaries)
    *   **SSS:** 100 (Foundational document of the National Park movement)
    *   **TAS:** 85 (Strong appeal for map collectors and history buffs)
    *   **IPS:** 100 (Library of Congress GMD)
    *   **PVS:** 90 (High-resolution TIF supports large-format wall art)
    *   **RCS:** 100 (Public Domain)

### 3.3 John James Audubon: *American Bison* (1845)
*   **Asset Type:** Wildlife Illustration (Hand-colored Lithograph)
*   **Classification:** **MASTERWORK**
*   **Aggregate CSP:** **94.40**
*   **Scoring Breakdown:**
    *   **VAS:** 98 (Powerful, iconic composition by the world's most famous naturalist)
    *   **PIS:** 85 (Strong North American/Yellowstone association)
    *   **SSS:** 100 (*The Viviparous Quadrupeds of North America* series)
    *   **TAS:** 90 (Massive appeal for wildlife and conservation enthusiasts)
    *   **IPS:** 100 (Audubon heritage / Smithsonian)
    *   **PVS:** 95 (High versatility: Wall Art, Apparel, Stationery)
    *   **RCS:** 100 (Public Domain)

### 3.4 John James Audubon: *Common American Wolf* (1847)
*   **Asset Type:** Wildlife Illustration (Hand-colored Lithograph)
*   **Classification:** **MASTERWORK**
*   **Aggregate CSP:** **94.40**
*   **Scoring Breakdown:**
    *   **VAS:** 98 (Intense, dynamic wildlife portrayal)
    *   **PIS:** 85 (Central to the Yellowstone ecological narrative)
    *   **SSS:** 100 (Audubon provenance)
    *   **TAS:** 90 (High-demand charismatic megafauna)
    *   **IPS:** 100 (Institutional "Gold Standard")
    *   **PVS:** 95 (Extremely marketable across all product families)
    *   **RCS:** 100 (Public Domain)

### 3.5 William Henry Jackson: *Old Faithful Geyser* (1872)
*   **Asset Type:** Photography (Albumen Print)
*   **Classification:** **FLAGSHIP**
*   **Aggregate CSP:** **87.50**
*   **Scoring Breakdown:**
    *   **VAS:** 80 (Authentic, high-contrast B&W historical aesthetic)
    *   **PIS:** 95 (Most famous landmark in the park)
    *   **SSS:** 90 (First photographic proof of Yellowstone's geysers)
    *   **TAS:** 95 (Instant "Tourism Heritage" recognition)
    *   **IPS:** 90 (National Archives / Smithsonian)
    *   **PVS:** 85 (Excellent for heritage calendars and posters)
    *   **RCS:** 100 (Public Domain)

### 3.6 Control Asset: *Blurred Field Note Scan (Common Sparrow, 1954)*
*   **Asset Type:** Archive Ephemera (Low-res Scan)
*   **Classification:** **BLOCKED**
*   **Aggregate CSP:** **18.50**
*   **Scoring Breakdown:**
    *   **VAS:** 10 (Blurry, text-heavy, zero decorative appeal)
    *   **PIS:** 30 (Generic bird, generic location)
    *   **SSS:** 20 (Minor researcher notes with no public resonance)
    *   **TAS:** 10 (Zero tourism/giftability appeal)
    *   **IPS:** 40 (Minor regional university archive)
    *   **PVS:** 10 (Unsuitable for print-on-demand products)
    *   **RCS:** 100 (Public Domain)

---

## 2. Validation Weights & Thresholds

| Classification | CSP Range | Revenue Strategy |
| :--- | :---: | :--- |
| **MASTERWORK** | 90+ | High-margin premium editions; brand anchors. |
| **FLAGSHIP** | 75–89 | Core product catalog (Shopify/Etsy). |
| **STANDARD** | 60–74 | Automated long-tail syndication. |
| **REFERENCE** | 40–59 | Education-only; no commercial deployment. |
| **BLOCKED** | < 40 | Filtered out of the ingestion pipeline. |

---

## 3. Usage Guidelines

1.  **Engine Calibration:** When testing a new scoring algorithm, the engine's output for these assets should deviate by no more than **±3%** from the CSP benchmarks above.
2.  **Sensitivity Testing:** Use the Control Asset (3.6) to ensure the model correctly filters out "Archive Noise" from "Archive Treasure."
3.  **Tier Alignment:** Assets like Jackson (3.5) demonstrate the transition from **Masterwork** to **Flagship**, helping to define the visual threshold for premium pricing.
