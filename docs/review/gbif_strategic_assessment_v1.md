# GBIF Strategic Intelligence Review v1

**Institution:** Global Biodiversity Information Facility (GBIF)
**Status:** Primary Global Biodiversity Aggregator
**Assessment Date:** June 11, 2026

---

## 1. Executive Summary

GBIF is the definitive "Knowledge Fabric" for global biodiversity. Unlike NASA or NOAA, which are primary data generators, GBIF is an **aggregator** of over 2.5 billion records from museums, herbaria, and citizen science platforms. Its strategic value lies in its role as a universal translator (via the Darwin Core standard) for biological occurrences. For the **Nature & Culture** project, GBIF provides the "Micro" and "Occurrence" depth required to validate and enrich "Macro" assets from NOAA and NASA.

### Tier Ranking & Scoring
*   **Tier:** 1 (Core Knowledge Anchor)
*   **Score:** 91/100
*   **Biodiversity Depth:** 100/100 (Unrivaled occurrence data)
*   **Media Quality:** 72/100 (Highly variable; often low-res specimen shots)
*   **Licensing Clarity:** 88/100 (Standardized but decentralized)

---

## 2. Licensing Policy Recommendation

GBIF standardized its licensing in 2014, but as an aggregator, the license is set by the **publisher**, not GBIF.

### **Allowed: Open Utilities**
*   **CC0 (Public Domain):** **Priority.** Maximum utility. waiver of all rights. Ideal for Asset Zero and high-frequency reuse.
*   **CC-BY (Attribution):** **Standard.** Use allowed with proper credit. This is the most common license for museum-grade data and is fully compatible with Nature & Culture commercial and open goals.

### **Blocked: Restrictive Licenses**
*   **CC-BY-NC (Non-Commercial):** **Blocked.** This license creates legal friction for downstream product development, commercial sponsorships, and integrated toolsets.
*   **Action:** All ingestion pipelines must filter out media and metadata records carrying the `-NC` suffix.

---

## 3. Estimated Coverage & Value

| Metric | Estimation | Strategic Value |
|:---|:---|:---|
| **Biodiversity Coverage** | 2.5B+ Records | Absolute authority on "where" and "when" of life. |
| **Specimen Media** | 100M+ Images | Critical for visual validation of species. |
| **Conservation Value** | Maximum | Primary data source for Red List assessments and MPA planning. |
| **Tourism Value** | Medium | Drives "Ecotourism" by identifying biodiversity hotspots. |

---

## 4. Strategic Ranking (Comparative)

Where GBIF sits in the "Nature & Culture" ecosystem:

1.  **NOAA:** (1st) Primary source for "Blue" Nature and Planet-scale weather. High-res imagery.
2.  **NASA:** (2nd) Primary source for "Earth Observation" and macro-scale climate. High-res imagery.
3.  **GBIF:** (3rd) **Primary source for "Species Knowledge."** Unrivaled depth but variable media quality.
4.  **Museums (AIC/Met/Smithsonian):** (4th) Primary source for "Culture" and high-art "Nature" interpretations.
5.  **NARA:** (5th) Primary source for "Heritage" and historical "Culture."

**GBIF Ranking Rationale:** GBIF outranks individual museums because it **aggregates** them. It is the "Search Engine" for the natural world. However, it ranks below NOAA and NASA for launch-phase priority because those agencies produce high-impact, "hero-ready" visual assets, whereas GBIF's strength is in the granular data layer that supports those assets.

---

## 5. Recommendation

Proceed with **restricted onboarding**. Unlike NOAA (which is a batch-ingest candidate), GBIF should be used as a **Discovery Service** to enrich existing assets.

*   **Step 1:** Use GBIF API to pull specimen validation for all **NOAA Asset Zero** marine species.
*   **Step 2:** Filter for CC0/CC-BY media to provide "Micro" views (macro photography of specimens) alongside NOAA's "Macro" views (underwater habitat shots).
*   **Step 3:** Establish a "Knowledge Link" in the Discovery Journeys between the occurrence data (GBIF) and the visual narrative (NOAA).
