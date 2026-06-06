# Creator Authority and Prestige Benchmark v1

| Field | Value |
|---|---|
| Version | v1.0.0 |
| Status | Approved — Seed Data Authority |
| Role | Chief Curator |
| Date | 2026-06-06 |

---

## 1. Purpose

This benchmark establishes the baseline prestige and commercial rankings for foundational creators in the Nature & Culture platform. These values provide the seed data for the **Visual Authority Score (VAS)** and **Story Strength Score (SSS)** dimensions defined in the Commercial Success Model (CSM).

## 2. Prestige Tier Definitions

- **Tier 1 — Global Masterwork:** Highest historical and commercial prestige. Assets by these creators are primary candidates for "MASTERWORK" classification.
- **Tier 2 — Flagship Authority:** High prestige with strong regional or thematic identity. Primary candidates for "FLAGSHIP" classification.
- **Tier 3 — Standard Reference:** Reliable historical and scientific authority. Primarily for "STANDARD" or "REFERENCE" classification.

---

## 3. Natural History Benchmarks

| Creator | Prestige Tier | Comm | Edu | Tour | Pub | Rationale |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **John James Audubon** | Tier 1 | 10 | 10 | 9 | 10 | The gold standard for American wildlife art; *Birds of America* is a global icon. |
| **John Gould** | Tier 1 | 9 | 10 | 8 | 10 | The "Audubon of Australia"; vast output of high-quality lithographs. |
| **Ernst Haeckel** | Tier 1 | 10 | 9 | 7 | 10 | *Kunstformen der Natur* bridges science and Art Nouveau; extreme commercial decor appeal. |
| **Pierre-Joseph Redouté** | Tier 1 | 10 | 9 | 8 | 10 | The "Raphael of Flowers"; defines the botanical masterwork. |
| **Maria Sibylla Merian** | Tier 1 | 9 | 10 | 7 | 10 | Pioneer of entomology and early woman of science; high prestige and story strength. |

## 4. Fine Art Benchmarks

| Creator | Prestige Tier | Comm | Edu | Tour | Pub | Rationale |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Thomas Moran** | Tier 1 | 9 | 9 | 10 | 9 | The visual architect of the American West; essential for Yellowstone/UNESCO identity. |
| **Albert Bierstadt** | Tier 1 | 9 | 8 | 10 | 9 | Grandeur of the Rocky Mountains; direct bridge to National Park tourism. |
| **J.M.W. Turner** | Tier 1 | 10 | 9 | 9 | 10 | Atmospheric brilliance; global institutional prestige and museum-level value. |
| **Frederic Edwin Church** | Tier 1 | 9 | 8 | 9 | 9 | Scientific realism in landscape; high value for "Visual Authority" (VAS). |

## 5. Photography Benchmarks

| Creator | Prestige Tier | Comm | Edu | Tour | Pub | Rationale |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **William Henry Jackson** | Tier 1 | 8 | 10 | 10 | 9 | Hayden Survey photographer; provided the visual proof for Yellowstone's protection. |
| **Carleton Watkins** | Tier 1 | 9 | 9 | 10 | 9 | Mammoth-plate pioneer; established the visual iconography of Yosemite. |
| **Edward S. Curtis** | Tier 1 | 10 | 10 | 9 | 10 | *The North American Indian*; unparalleled story strength and commercial folio value. |

## 6. Map Benchmarks

| Creator | Prestige Tier | Comm | Edu | Tour | Pub | Rationale |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Hayden Survey** | Tier 1 | 8 | 10 | 10 | 9 | Foundational place identity for the US West; high tourism and educational value. |
| **Joan Blaeu** | Tier 1 | 10 | 9 | 8 | 10 | The pinnacle of cartographic artistry; *Atlas Maior* is the most prestigious atlas. |
| **John Tallis** | Tier 1 | 10 | 8 | 7 | 9 | Illustrated "Vignette" maps; highest decorative appeal for commercial products. |
| **Aaron Arrowsmith** | Tier 1 | 8 | 10 | 8 | 9 | The hydrographer to the King; scientific accuracy and expansion-era prestige. |

---

## 7. Scoring Guidelines for Curators

1.  **Attribution Bonus:** Confirmed attribution to a Tier 1 creator provides a +0.200 boost to the `visual_quality_score` (VAS).
2.  **Series Multiplier:** Assets that are part of a famous series (e.g., *Viviparous Quadrupeds*, *Atlas Maior*) receive a +0.150 boost to `provenance_score` (SSS).
3.  **Place Lock:** When a Tier 1 creator is historically linked to a specific Place (Moran/Yellowstone, Watkins/Yosemite), the `place_relevance_score` (PIS) is set to a minimum of 0.900 for that association.
