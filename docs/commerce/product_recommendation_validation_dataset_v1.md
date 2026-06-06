# Product Recommendation Validation Dataset v1.0

This dataset provides the definitive benchmarks for validating the **Product Recommendation Engine** and **Collection Routing Logic**. It maps specific assets to their optimal commercial "Product Families" and "Collection Clusters" based on the Commercial Success Model (CSM) v1.0.

---

## 1. Recommendation Logic & Scoring Ranges

The engine is expected to generate a **Recommendation Score (RS)** for each Asset-Product pairing.

| Recommendation Tier | RS Range | Action |
| :--- | :---: | :--- |
| **HERO** | 90–100 | Priority 1: Mandatory for this product family. |
| **STRONG** | 75–89 | Priority 2: Recommended for catalog expansion. |
| **VIABLE** | 60–74 | Priority 3: Automated deployment only. |
| **WEAK** | 40–59 | Discard: Ingest as Reference only. |
| **REJECTED** | < 40 | Hard Block: Do not generate products. |

---

## 2. Asset Benchmark Fixtures

### 2.1 Thomas Moran: *The Grand Canyon of the Yellowstone*
*   **Classification:** MASTERWORK (CSP: 98.25)
*   **Expected Product Recommendations:**
    *   **Museum Prints:** HERO (RS: 98) - Archival Linen / Heavyweight Cotton.
    *   **Wall Art:** HERO (RS: 95) - Premium Framed Canvas.
    *   **Books:** HERO (RS: 92) - Coffee Table Book Cover / Feature Plate.
*   **Expected Collection Recommendations:**
    *   Yellowstone Heritage Collection
    *   American Landscape Masterworks

### 2.2 1871 Hayden Survey Map (Yellowstone)
*   **Classification:** MASTERWORK (CSP: 95.25)
*   **Expected Product Recommendations:**
    *   **Museum Prints:** HERO (RS: 96) - Large Format Archival Paper.
    *   **Wall Art:** HERO (RS: 92) - "Surveyor" Style Wooden Framed Prints.
    *   **Books:** HERO (RS: 90) - "Expedition 1871" Commemorative Folio.
*   **Expected Collection Recommendations:**
    *   Yellowstone Heritage Collection
    *   The Blueprint of Wilderness (Historical Cartography)

### 2.3 John James Audubon: *American Bison*
*   **Classification:** MASTERWORK (CSP: 94.40)
*   **Expected Product Recommendations:**
    *   **Wall Art:** HERO (RS: 94) - Premium Giclée Prints.
    *   **Calendars:** HERO (RS: 90) - "North American Giants" Series.
    *   **Books:** STRONG (RS: 88) - Wildlife Portfolio Books.
*   **Expected Collection Recommendations:**
    *   The Viviparous Quadrupeds of North America
    *   Great Plains Heritage

### 2.4 John James Audubon: *Common American Wolf*
*   **Classification:** MASTERWORK (CSP: 94.40)
*   **Expected Product Recommendations:**
    *   **Wall Art:** HERO (RS: 94) - Premium Giclée Prints.
    *   **Apparel:** STRONG (RS: 85) - Heritage Wildlife Series (Embroidery/DTG).
    *   **Puzzles:** HERO (RS: 90) - 1,000 Piece "Apex Predator" Series.
*   **Expected Collection Recommendations:**
    *   The Viviparous Quadrupeds of North America
    *   Yellowstone Heritage Collection (Predator/Prey Series)

### 2.5 Ernst Haeckel: *Kunstformen der Natur* (Circogonia)
*   **Classification:** MASTERWORK (CSP: 95.50)
*   **Expected Product Recommendations:**
    *   **Wall Art:** HERO (RS: 95) - Modern Symmetrical Framed Prints.
    *   **Home Decor:** HERO (RS: 92) - Tiled Pattern Pillows / Textiles.
    *   **Puzzles:** HERO (RS: 94) - Complex Geometric Puzzles.
*   **Expected Collection Recommendations:**
    *   Biological Forms & Geometry
    *   Scientific Art Masterworks

### 2.6 Lewis & Clark Map (1814)
*   **Classification:** FLAGSHIP (CSP: 89.50)
*   **Expected Product Recommendations:**
    *   **Wall Art:** HERO (RS: 88) - Vintage Expedition Posters.
    *   **Stationery:** HERO (RS: 85) - "Explorer" Journal Covers.
    *   **Books:** STRONG (RS: 80) - American West History Folios.
*   **Expected Collection Recommendations:**
    *   American Exploration & Discovery
    *   Historical Cartography

### 2.7 Pierre-Joseph Redouté: *Les Roses*
*   **Classification:** FLAGSHIP (CSP: 89.50)
*   **Expected Product Recommendations:**
    *   **Wall Art:** HERO (RS: 88) - Botanical Gallery Sets.
    *   **Home Decor:** HERO (RS: 85) - Floral Textiles / Kitchenware.
    *   **Calendars:** HERO (RS: 90) - "A Year in Roses" Series.
*   **Expected Collection Recommendations:**
    *   The Queen of Flowers (Botanical Series)
    *   French Natural History Heritage

### 2.8 William Henry Jackson: *Old Faithful Geyser* (1872)
*   **Classification:** FLAGSHIP (CSP: 87.50)
*   **Expected Product Recommendations:**
    *   **Calendars:** HERO (RS: 92) - Yellowstone Heritage Calendar.
    *   **Wall Art:** STRONG (RS: 84) - Sepia Toned Historical Posters.
    *   **Stationery:** HERO (RS: 88) - "National Park Pioneer" Postcards.
*   **Expected Collection Recommendations:**
    *   Yellowstone Heritage Collection
    *   The First Photographers of the West

### 2.9 Control Assets (Blurred Scans / Archive Ephemera)
*   **Classification:** BLOCKED (CSP: < 40)
*   **Expected Recommendations:**
    *   **All Products:** REJECTED (RS: < 40).
    *   **All Collections:** REJECTED.
*   **Reasoning:** Fails Visual Authority (VAS) and Product Versatility (PVS) hard gates.

---

## 3. Product Family Summary Matrix

| Asset | Museum Print | Wall Art | Calendar | Book | Home Decor | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Moran** | HERO | HERO | STRONG | HERO | VIABLE | Deploy Premium |
| **Hayden Map** | HERO | HERO | VIABLE | HERO | WEAK | Deploy Premium |
| **Audubon** | STRONG | HERO | HERO | STRONG | VIABLE | Deploy Standard |
| **Haeckel** | HERO | HERO | VIABLE | STRONG | HERO | Deploy Standard |
| **Lewis & Clark** | VIABLE | HERO | VIABLE | STRONG | WEAK | Deploy Standard |
| **Redouté** | STRONG | HERO | HERO | VIABLE | HERO | Deploy Standard |
| **Jackson** | WEAK | STRONG | HERO | VIABLE | WEAK | Deploy Standard |
| **Controls** | REJECT | REJECT | REJECT | REJECT | REJECT | **BLOCKED** |
