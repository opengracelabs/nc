# Grand Canyon Provenance Report (NC-DATA-003)

This report details the origin, adoption, and downstream impact of the three conflicting GeoNames IDs identified for Grand Canyon National Park.

---

## 1. ID Audit & Provenance

### 1.1 ID 5296401 (Canonical)
*   **Identity:** **Grand Canyon National Park** (Coconino County, AZ).
*   **Source Document:** NC-PILOT-001 Final Readiness Review §III.
*   **Date Introduced:** 2026-06-11.
*   **Downstream References:**
    *   `pilot_anchor` migration 38 (Production).
    *   `NC-WEB-001 Website Wireframe + Creative Direction.md`
    *   `NC-AI-004 Earthrise AI Page Copy Pack.md`
    *   `Grand Canyon AI Content Pack.md`
*   **Status:** **CONFIRMED**. Verified via GeoNames RDF live evidence and Wikidata P1566 cross-reference.
*   **Risk if wrong:** None. This is the correct identifier for the national park.

### 1.2 ID 5296404 (Retired)
*   **Identity:** **Grand Canyon National Game Preserve** (AZ).
*   **Source Document:** GeoNames Intelligence Plan v1.
*   **Date Introduced:** 2026-06-11 (Pre-readiness).
*   **Downstream References:**
    *   `NC-PILOT-001-FGR` (Listed as unverified).
    *   `Grand Canyon Content Dependency Report.md` (Flagged as conflict).
*   **Status:** **DISQUALIFIED**. Refers to a historical predecessor of the park (established 1906), not the modern 1919 National Park entity.
*   **Risk if wrong:** Narrative error (incorrect historical context) and potential boundary discrepancies for mapping.

### 1.3 ID 5513679 (Retired)
*   **Identity:** **Thunder Mountain** (Nye County, Nevada).
*   **Source Document:** NC-PILOT-001 Commercial Pilot Governance Blueprint §III.2.
*   **Date Introduced:** 2026-06-11.
*   **Downstream References:**
    *   `NC-PILOT-001-FGR` (Listed as unverified).
    *   `Grand Canyon Content Dependency Report.md` (Flagged as conflict).
*   **Status:** **DISQUALIFIED**. Completely unrelated to the Grand Canyon or Arizona. The Blueprint's claim of fcode=PRKA was also incorrect (actual: T.MT).
*   **Risk if wrong:** Critical geographic failure. Anchoring the "Grand Canyon" to a mountain in Nevada would break search, mapping, and product attribution.

---

## 2. Methodology & Findings

The audit confirms an **error chain** similar to the Yellowstone (NC-DATA-001) resolution:
1.  **Original Error:** The Blueprint (5513679) and Intelligence Plan (5296404) adopted unverified IDs without fixture support.
2.  **Correction:** The Final Readiness Review (2026-06-11) correctly identified 5296401 via Wikidata P1566, but failed to provide the necessary fixture evidence to validate it against the "incorrect typo" claims.
3.  **Validation:** Live RDF evidence from `sws.geonames.org/5296401/about.rdf` definitively confirms that 5296401 is Grand Canyon National Park (fcode=L.PRK).

---

## 3. Risk Assessment Summary

| ID | Geographic Risk | Governance Risk | Technical Risk |
| :--- | :--- | :--- | :--- |
| **5296401** | **Low** | **Low** | None (Correct ID) |
| **5296404** | **Medium** | **High** | Incorrect historical anchor; boundary mismatch. |
| **5513679** | **Critical** | **Critical** | Complete geographic failure; invalid metadata mapping. |

---
*Grand Canyon Provenance Report (NC-DATA-003) produced by Gemini CLI*
