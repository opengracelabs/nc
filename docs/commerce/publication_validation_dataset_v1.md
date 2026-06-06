# Publication Validation Dataset v1.0

This dataset provides the definitive benchmarks for validating the **Publication Intelligence Service**. These fixtures serve as the "Gold Standard" for determining publication readiness, priority, and strategic channel routing.

---

## 1. Publication Classification Schema

Every asset is evaluated against the following publication dimensions:

*   **Publication_Priority:** 0–100 (HIGHEST | HIGH | MEDIUM | LOW).
*   **Publication_Readiness:** READY | NEEDS_RESTORATION | NEEDS_METADATA.
*   **Publication_Surface:** Shopify (Premium) | Etsy (Marketplace) | Social (Viral) | Blog (Narrative).
*   **Target_Audience:** Collector | Decorator | Traveler | Educator.
*   **Curator_Review_Requirement:** MANDATORY (High-Gate) | OPTIONAL (Standard) | NONE (Auto).
*   **Seasonal_Timing:** Optimal Go-To-Market window.
*   **Publication_Risk:** HIGH | MEDIUM | LOW (Technical, Brand, or IP).

---

## 2. Benchmark Publication Fixtures

### 2.1 Thomas Moran: *The Grand Canyon of the Yellowstone*
*   **NC_ID:** `ASSET_000001`
*   **Publication_Priority:** HIGHEST (100)
*   **Publication_Readiness:** READY
*   **Publication_Surface:** Shopify (Hero Collection)
*   **Target_Audience:** The Collector / Landscape Art Enthusiast
*   **Curator_Review_Requirement:** MANDATORY (Verification of 40x60" Grand Scale clarity)
*   **Seasonal_Timing:** March 1st (Yellowstone National Park Anniversary)
*   **Publication_Risk:** LOW (Technical: Must ensure zero pixelation at max scale)

### 2.2 1871 Hayden Survey Map
*   **NC_ID:** `ASSET_000002`
*   **Publication_Priority:** HIGHEST (95)
*   **Publication_Readiness:** NEEDS_METADATA (Full historical transcription and survey notes)
*   **Publication_Surface:** Shopify (Historical Series) / Blog (Expedition Narrative)
*   **Target_Audience:** The Historian / Cartography Collector
*   **Curator_Review_Requirement:** MANDATORY (Accuracy of technical metadata/transcription)
*   **Seasonal_Timing:** Mid-April (National Park Week)
*   **Publication_Risk:** LOW (Technical: Fine-line clarity of survey marks)

### 2.3 William Henry Jackson: *Old Faithful Geyser*
*   **NC_ID:** `ASSET_000003`
*   **Publication_Priority:** HIGH (85)
*   **Publication_Readiness:** NEEDS_RESTORATION (Removal of archive noise/foxing)
*   **Publication_Surface:** Etsy (Vintage Decor) / Social (Tourism Nostalgia)
*   **Target_Audience:** The Traveler / Vintage Photography Fan
*   **Curator_Review_Requirement:** OPTIONAL (Review of restoration quality)
*   **Seasonal_Timing:** June-August (Peak Summer Tourism)
*   **Publication_Risk:** MEDIUM (Brand: Ensuring B&W photography holds value against color art)

### 2.4 John James Audubon: *American Bison*
*   **NC_ID:** `ASSET_000004`
*   **Publication_Priority:** HIGH (90)
*   **Publication_Readiness:** READY
*   **Publication_Surface:** Etsy (Marketplace volume) / Shopify (Wildlife Collection)
*   **Target_Audience:** The Decorator / Wildlife Enthusiast
*   **Curator_Review_Requirement:** OPTIONAL (Standard quality check)
*   **Seasonal_Timing:** September (National Wildlife Day) / November (National Bison Day)
*   **Publication_Risk:** LOW (Brand: Market saturation of generic Audubon prints)

### 2.5 John James Audubon: *Common American Wolf*
*   **NC_ID:** `ASSET_000005`
*   **Publication_Priority:** HIGH (90)
*   **Publication_Readiness:** READY
*   **Publication_Surface:** Etsy (Marketplace volume) / Shopify (Wildlife Collection)
*   **Target_Audience:** The Decorator / Predator Ecology Fan
*   **Curator_Review_Requirement:** OPTIONAL (Standard quality check)
*   **Seasonal_Timing:** Fall/Winter (Wilderness aesthetic)
*   **Publication_Risk:** LOW (Brand: Aesthetic appeal vs. aggressive subject matter)

### 2.6 Ernst Haeckel: *Circogonia*
*   **NC_ID:** `ASSET_000006`
*   **Publication_Priority:** MEDIUM (80)
*   **Publication_Readiness:** READY
*   **Publication_Surface:** Social (Viral Visuals) / Shopify (Design Series)
*   **Target_Audience:** The Designer / Interior Decorator
*   **Curator_Review_Requirement:** OPTIONAL (Symmetry/tiling alignment check)
*   **Seasonal_Timing:** January-February (Interior Design Refresh Season)
*   **Publication_Risk:** LOW (Technical: Precision of geometric centering)

---

## 3. Publication Failure Fixtures (Negative Benchmarks)

### 3.1 Control Asset: *Blurred Field Note Scan*
*   **NC_ID:** `CONTROL_000001`
*   **Publication_Priority:** LOW (0)
*   **Publication_Readiness:** BLOCKED
*   **Publication_Surface:** NONE
*   **Target_Audience:** NONE
*   **Curator_Review_Requirement:** AUTOMATIC REJECTION
*   **Seasonal_Timing:** NONE
*   **Publication_Risk:** HIGH (Brand: Significant dilution of "Museum Grade" authority)
