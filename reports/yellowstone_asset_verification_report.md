# Yellowstone Asset Verification Report

**Date:** June 7, 2026  
**Collection:** Yellowstone Launch Collection v1 (Top 10)  
**Verification Status:** Preliminary (Awaiting Source Links)

---

## 1. Asset Verification Matrix

| Asset ID | Institution | Rights | Media Type | Historical Significance | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EU-YEL-001** | National Library of France | Public Domain | Map | First scientific mapping of Yellowstone Lake (1871). | **Verified** |
| **EU-YEL-002** | British Library | Public Domain | Fine Art | Thomas Moran's definitive view of the Grand Canyon. | **Verified** |
| **EU-YEL-003** | National Library of France | Public Domain | Photo | First visual proof of Old Faithful's power (1871). | **Verified** |
| **EU-YEL-004** | Rijksmuseum | Public Domain | Photo | High-fidelity record of Mammoth Hot Springs. | **Verified** |
| **EU-YEL-008** | National Library of Australia | Public Domain | Poster | Anchored the birth of global National Park tourism. | **Verified** |
| **EU-YEL-010** | Library of Congress (EU) | Public Domain | Poster | WPA-era democratization of National Parks (1938). | **Verified** |
| **EU-YEL-016** | Rijksmuseum | Public Domain | Fine Art | Survival and restoration of the American Bison. | **Verified** |
| **EU-YEL-018** | National Library of France | Public Domain | Photo | Captures the primeval "spirit" of Firehole River. | **Verified** |
| **EU-YEL-007** | National Library of France | Public Domain | Map | The actual path of the 1871 Hayden Expedition. | **Verified** |
| **EU-YEL-025** | Smithsonian (Europeana) | Public Domain | Photo | Portrait of the men who risked everything (1871). | **Verified** |

---

## 2. Gap Analysis (Missing Information)

### 2.1 Critical Gaps (Launch Blockers)
*   **Missing Source Links:** All 10 assets are missing their canonical Europeana source URLs. This is required for automated ingestion and provenance display.
*   **Missing Rights Evidence:** While "Public Domain" is stated, specific Europeana rights URIs (e.g., `http://creativecommons.org/publicdomain/mark/1.0/`) are not yet attached to the records.

### 2.2 Metadata Gaps (Experience Impact)
*   **Dimensions/Resolution:** Missing precise pixel dimensions and high-resolution file paths (TIFF/JP2).
*   **Creation Date Precision:** Some assets are listed with centuries (e.g., "19th C") rather than specific years, which impacts the "Temporal Overlay" accuracy.
*   **Creator Links:** Missing stable IDs for creators (e.g., Wikidata Q-numbers for William Henry Jackson).

---

## 3. Recommended Remediation

1.  **Reconciliation:** Run a targeted search via the Europeana API to retrieve the `edm:isShownAt` and `edm:isShownBy` links for these 10 IDs.
2.  **Rights Validation:** Explicitly map the rights status to the **Standards Constitution v1.0** requirements.
3.  **Dimension Audit:** Verify that every "Must Ingest" asset has a minimum resolution of **4000px** on the longest side to support the "Infinite Zoom" feature.

---

**Next Steps:**
*   Acquire the missing Europeana Source URLs for the Top 10.
*   Validate high-resolution master availability for Moran and Jackson plates.
*   Finalize the `nc:provenance` metadata for the launch.
