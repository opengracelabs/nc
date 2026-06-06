# Routing Validation Report v1.0

This report validates the **Product Routing Benchmark** for the v0.5.0 fulfillment and generation services. It defines the expected confidence levels and curator intervention flags for the core Nature & Culture asset fixtures.

---

## 1. Routing Validation Matrix

| Asset | Primary Route | Routing Confidence | Curator Review Flags | Status |
| :--- | :--- | :---: | :--- | :--- |
| **Thomas Moran** | **Museum Print** | **Absolute (98)** | High-Res Verification (24x36") | **VALID** |
| **Hayden Map** | **Museum Print** | **Absolute (96)** | Technical Detail/Transcription Review | **VALID** |
| **W.H. Jackson** | **Calendar** | **High (92)** | Nostalgia/Heritage Context Review | **VALID** |
| **Audubon** | **Wall Art** | **High (94)** | Aesthetic Restoration Review | **VALID** |
| **Haeckel** | **Wall Art** | **High (95)** | Geometric/Tile Alignment Review | **VALID** |

---

## 2. Detailed Validation Audit

### 2.1 Confidence Calibration
*   **Absolute Confidence (95+):** Reserved for "Masterwork" assets (Moran, Hayden) where the routing to premium surfaces is unambiguous. The system should bypass manual routing for these assets, moving directly to print-ready generation.
*   **High Confidence (85–94):** Applies to "Flagship" assets (Jackson, Audubon, Haeckel). These assets are commercially robust but require a "Curator Gate" to confirm the specific aesthetic restoration or cropping for the target product.

### 2.2 Curator Intervention Flags
*   **High-Res Verification:** Mandatory for Moran/Hayden when routing to **Museum Prints**. Ensures the TIFF source can survive large-scale expansion without pixelation.
*   **Aesthetic Restoration:** Triggered for Audubon/Jackson to remove historical "Archive Noise" (foxing, tears) before product generation.
*   **Geometric Alignment:** Specific to Haeckel; ensures symmetrical patterns are correctly centered for **Puzzles** and **Home Decor**.

---

## 3. Benchmark Failures & Routing Tension

### 3.1 The "Masterwork Overlap" Failure
*   **Issue:** Assets like **Moran** and **Hayden** score "HERO" (90+) for 3 or more product families simultaneously (Museum Print, Wall Art, Book).
*   **Risk:** The automated router may "over-publish" these assets, causing catalog clutter or cannibalizing premium sales with standard wall art.
*   **Resolution:** Implement a "Tier-Down" rule: If an asset is a **Museum Print Hero**, suppress **Standard Wall Art** generation for the first 30 days of a collection launch to preserve exclusivity.

### 3.2 The "Jackson Aesthetic Floor" Failure
*   **Issue:** **W.H. Jackson's** photography sits at the edge of the **Wall Art** viability threshold (RS: 84).
*   **Risk:** Without the "Heritage Context" multiplier, the router might demote iconic photography to **Stationery** only, missing the wall-art revenue opportunity.
*   **Resolution:** Introduce a **Historical Identity Multiplier (HIM)** that boosts routing scores for assets with high Story Strength (SSS > 90), ensuring they reach the "Strong" Wall Art tier.

---

## 4. Final Verdict

The **Product Routing Benchmark v1.0** is **PASSED** for v0.5.0 implementation. 

The routing logic effectively separates "Premium" from "Volume" assets and correctly identifies the necessary human-in-the-loop flags for high-value restorations.
