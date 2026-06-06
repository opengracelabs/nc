# Provider Routing Benchmark v1.0

This dataset provides the definitive benchmarks for validating the **Provider Routing Service** (Fulfillment Router). It maps core assets and their primary products to the optimal fulfillment providers, ensuring that production quality remains aligned with the Nature & Culture "Museum Grade" standard.

---

## 1. Provider Definitions

*   **Gelato:** Primary provider for Wall Art (Posters, Canvas), Fashion, Home Decor, Gifts, Cards, and Calendars.
*   **Lulu:** Primary provider for Books, Field Guides, Educational Folios, and Premium Bound Catalogs.

---

## 2. Provider Routing Matrix

| Asset | Primary Product | Preferred Provider | Alternative Provider | Risk Level |
| :--- | :--- | :--- | :--- | :---: |
| **Thomas Moran** | Museum Print (Canvas) | **Gelato** | None (Custom Shop) | **HIGH** |
| **Hayden Map** | Wall Art (Poster) | **Gelato** | Printful | **MEDIUM** |
| **W.H. Jackson** | Heritage Calendar | **Gelato** | Lulu | **MEDIUM** |
| **Audubon** | Giclée Print | **Gelato** | Printful | **LOW** |
| **Haeckel** | Jigsaw Puzzle | **Gelato** | None (Specialist) | **MEDIUM** |
| **Hayden Folio** | Historical Book | **Lulu** | Blurb | **HIGH** |

---

## 3. Detailed Provider Benchmarks

### 3.1 Thomas Moran: *The Grand Canyon of the Yellowstone*
*   **Production Suitability:** High-end Canvas / Archival Paper.
*   **Preferred Provider:** Gelato (Premium Canvas SKU).
*   **Alternative Provider:** None (Manual Fulfillment for "Grand Scale" 40x60").
*   **Risk Level:** **HIGH** (Color fidelity and highlight preservation in the canyon yellows/reds).
*   **Fulfillment Complexity:** High (Requires custom packaging for large-format frames).
*   **Cost Sensitivity:** Low (Premium pricing justifies higher fulfillment and insurance costs).

### 3.2 1871 Hayden Survey Map
*   **Production Suitability:** Matte Poster / Framed Paper.
*   **Preferred Provider:** Gelato (Matte 200 gsm).
*   **Alternative Provider:** Printful.
*   **Risk Level:** **MEDIUM** (Fine-line technical clarity of survey marks).
*   **Fulfillment Complexity:** Medium (Standard tube shipping).
*   **Cost Sensitivity:** Medium (Standard wall art margins).

### 3.3 William Henry Jackson: *Old Faithful Geyser*
*   **Production Suitability:** Spiral-bound Calendar / Postcard Set.
*   **Preferred Provider:** Gelato (Standard Calendar SKU).
*   **Alternative Provider:** Lulu (for high-end "Book Style" calendars).
*   **Risk Level:** **MEDIUM** (B&W contrast management on non-archival paper).
*   **Fulfillment Complexity:** Low (Standard mailers).
*   **Cost Sensitivity:** High (Volume-based pricing is critical for stationery).

### 3.4 John James Audubon: *Wildlife Series*
*   **Production Suitability:** Giclée Wall Art / Apparel.
*   **Preferred Provider:** Gelato (Enhanced Matte).
*   **Alternative Provider:** Printful (for Apparel DTG).
*   **Risk Level:** **LOW** (Well-documented lithographic colors are stable across modern POD).
*   **Fulfillment Complexity:** Low (Standard tubes/flat mailers).
*   **Cost Sensitivity:** Medium (Market-competitive pricing is required).

### 3.5 Ernst Haeckel: *Scientific Art Series*
*   **Production Suitability:** Jigsaw Puzzle / Wall Art.
*   **Preferred Provider:** Gelato (Puzzle SKU).
*   **Alternative Provider:** None (Requires specialized die-cutting).
*   **Risk Level:** **MEDIUM** (Geometric alignment and "fit" of symmetrical pieces).
*   **Fulfillment Complexity:** Medium (Boxed shipping).
*   **Cost Sensitivity:** Medium (Gift-market pricing).

### 3.6 Hayden Survey Folio (Book)
*   **Production Suitability:** Hardcover Art Book.
*   **Preferred Provider:** Lulu (Premium Color Hardcover).
*   **Alternative Provider:** Blurb.
*   **Risk Level:** **HIGH** (Binding quality and page bleed for technical maps).
*   **Fulfillment Complexity:** Medium (Book packaging).
*   **Cost Sensitivity:** Low (High-prestige "Masterwork" product).

---

## 4. Provider Selection Hard Gates

*   **Rule 1 (Format):** If product type is `BOOK`, route to **Lulu**.
*   **Rule 2 (Scale):** If dimensions > 24x36", route to **Gelato** (Premium SKU) or **Manual Review**.
*   **Rule 3 (Rights):** If rights status is not `PUBLIC_DOMAIN` or `CC0`, **BLOCK** all providers.
*   **Rule 4 (Dest):** If shipping destination is unsupported by Preferred Provider, trigger **Alternative Provider** lookup or **Curator Review**.
