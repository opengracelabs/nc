# Scoring Validation Report v1.0

This report validates the **Commercial Success Model (CSM)** by cross-referencing the aggregate scores with expected tiers and product surfaces for our "Gold Standard" assets.

---

## 1. Asset Validation Matrix

| Asset | Expected Tier | Score Range | Primary Product Surfaces | Status |
| :--- | :--- | :---: | :--- | :--- |
| **Thomas Moran** | **MASTERWORK** | 95–100 | Museum Prints, Fine Art Books, Premium Canvas. | **VALID** |
| **Hayden Map** | **MASTERWORK** | 90–97 | Large Format Prints, Historical Folios, Wall Art. | **VALID** |
| **Audubon** | **MASTERWORK** | 90–95 | Wall Art, Calendars, Puzzles, Apparel. | **VALID** |
| **W.H. Jackson** | **FLAGSHIP** | 75–89 | Calendars, Stationery, Heritage Posters. | **VALID** |
| **Control 1 (Sparrow)**| **BLOCKED** | < 40 | None (Knowledge Base Reference Only). | **VALID** |

---

## 2. Detailed Performance Audit

### 2.1 The Masterwork Tier (90+)
*   **Moran (98.25):** Operates as the "Ideal Asset." No scoring tension. Maximum Visual Authority (VAS) and Institutional Prestige (IPS) perfectly align with premium product recommendations.
*   **Hayden Map (95.25):** Validates the **Story Strength (SSS)** multiplier. Despite lower "Universal Aesthetic" than fine art, its foundational historical narrative pulls it into Masterwork.
*   **Audubon (94.40):** Validates **Product Versatility (PVS)**. High scores in PVS (95) compensate for moderate PIS, ensuring wildlife remains a Masterwork pillar.

### 2.2 The Flagship Tier (75–89)
*   **Jackson (87.50):** The primary benchmark for "Historical Documentation." Its lower VAS (80) correctly gates it from the Masterwork tier, while its high TAS (95) ensures it remains a Hero for Calendars and Stationery.

### 2.3 The Rejection Zone (< 40)
*   **Control 1 (18.50):** Successfully triggers the "Visual Authority Hard Gate." Even with institutional provenance, low-fidelity scans are correctly blocked from all commerce surfaces.

---

## 3. Benchmark Failures & Scoring Tension

While the model is generally robust, the following areas exhibit **Scoring Tension** that requires monitoring:

1.  **The "Jackson Tension" (Historical vs. Aesthetic):**
    *   **Observation:** W.H. Jackson's Old Faithful Geyser is historically significant but visually "flatter" than hand-colored prints. 
    *   **Risk:** If VAS is weighted too heavily (>35%), iconic historical photography might fall into the **Standard** tier, devaluing its role in heritage calendars.
    *   **Resolution:** Maintain VAS at **30%** to allow Story Strength and Tourism Appeal to sustain Flagship status for historical "proof" assets.

2.  **The "Haeckel Anomaly" (Aesthetic vs. Geographic):**
    *   **Observation:** Haeckel's prints (CSP 95.50) have low **Place Identity (PIS: 60)** but maximum commercial appeal.
    *   **Risk:** A strictly "Place-Centered" model might bury high-converting scientific art.
    *   **Resolution:** Ensure **Visual Authority** and **Product Versatility** combined (40%) can override low geography scores for Masterwork-tier illustrations.

3.  **Boundary Saturation at 89.50:**
    *   **Observation:** Both **Lewis & Clark** and **Redouté** sit at 89.50 (Flagship Ceiling).
    *   **Risk:** The model currently lacks a "Tie-Breaker" for assets that are borderline Masterwork.
    *   **Resolution:** Consider adding a 5% "Curator’s Choice" modifier for v0.6.0 to manually promote high-prestige assets at this boundary.

---

## 4. Final Verdict

The **Commercial Success Model v1.0** is **PASSED** for v0.5.0 implementation. 

The engine successfully isolates "Museum Grade" Masterworks, populates the Flagship core, and rejects archive noise with 100% accuracy in the validation corpus.
