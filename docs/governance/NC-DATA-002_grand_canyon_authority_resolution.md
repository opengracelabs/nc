# NC-DATA-002: Grand Canyon Authority Resolution — Canonical ID Decision

**Document ID:** NC-DATA-002  
**Status:** FULL RATIFICATION (upgraded 2026-06-12 — GCA-001/GCA-002 complete per NC-DATA-003)  
**Date:** 2026-06-12  
**Authority:** Principal Architect  
**Reference authority:** DD-GEONAMES-001, SA-GEONAMES-001, DD-WIKIDATA-001, NC-DATA-001, NC-DATA-003

---

## I. Decision

**Wikidata canonical identity: RATIFIED — Q220289 (Grand Canyon National Park)**  
**GeoNames canonical ID: RATIFIED — 5296401 (Grand Canyon National Park, L.PRK)**

NC-DATA-002 is fully ratified. GCA-001 and GCA-002 are complete (NC-DATA-003, 2026-06-12). Live GeoNames RDF confirmed 5296401 = "Grand Canyon National Park" (L.PRK, Arizona, Coconino County). Wikidata Q220289 P1566 = "5296401" confirmed live.

**Grand Canyon place page activation unblocked** — GeoNames ID confirmed. Remaining gates per NC-PILOT-001 LA apply (SA-GEONAMES-001, SA-OSM-001 ratification).

---

## II. Evidence Summary

### GeoNames IDs in contention

Three GeoNames IDs appear across NC governance documents:

| ID | Feature claim | Source document | Source method |
|----|--------------|-----------------|---------------|
| **5513679** | fcode=PRKA (park area) | NC-PILOT-001 Commercial Pilot Governance Blueprint §III.2 | Undocumented (implied GeoNames lookup) |
| **5296404** | `L PRK` (park) | GeoNames Intelligence Plan v1 | Undocumented (implied GeoNames lookup) |
| **5296401** | `PRKN` (claimed, non-standard) | NC-PILOT-001 FRR §III + all downstream documents | Claimed "Wikidata Q220289 P1566 lookup, 2026-06-11" — **same methodology proven wrong for Yellowstone** |

No Grand Canyon GeoNames fixtures exist. There is no `place_grand_canyon.json`, `search_grand_canyon.json`, or `hierarchy_grand_canyon.json` in `tests/fixtures/geonames/`. No fixture provides direct GeoNames API evidence for any of the three IDs.

### Wikidata QIDs in contention

Two Wikidata QIDs appear:

| QID | Entity | Source documents |
|-----|--------|-----------------|
| **Q131648** | "Grand Canyon" — the geological feature (canyon, gorge) | NC-PILOT-001 Commercial Pilot Governance Blueprint §III.2 only |
| **Q220289** | "Grand Canyon National Park" — the administrative park | GeoNames Intelligence Plan, Wikidata Intelligence Plan, FRR §III, migration 38, NC-WEB-001, NC-AI-004, NC-PILOT-001 LA, NC-PILOT-001 closure report, NC-COMMERCE-001 |

The Wikidata QID conflict is between the geological feature (Q131648) and the administrative park (Q220289). The Blueprint was the sole document using Q131648.

---

## III. Wikidata Canonical Identity — RATIFIED

> **Canonical Wikidata QID: Q220289 (Grand Canyon National Park)**

**Q131648** (Grand Canyon geological feature) is **retired** as the NC place QID.

**Reasoning:**

The NC platform anchors commerce to named places — places with administrative identity, visitation context, and defined institutional relationships. The relevant entity is the national park (Q220289), not the geological feature (Q131648). The national park has: an NPS designation, a founding date (1919), Wikidata P1566 linkage to GeoNames, NARA and NASA record associations, and a defined boundary that scopes illustration opportunities. The geological feature (Q131648) is a subordinate aspect of the park, not the commerce anchor.

Q220289 is consistent across all documents except the original Blueprint. The Blueprint also carried the wrong fcode interpretation (it noted fcode=PRKA for a GeoNames ID alongside Q131648 — a park area fcode alongside a geological feature QID is internally inconsistent). The FRR §III corrected this to Q220289 and this correction is confirmed by multiple downstream documents.

**Note on the Blueprint's Q131648 — internal inconsistency:** The Blueprint simultaneously used Q131648 (geological feature) and fcode=PRKA (park area) for GeoNames ID 5513679. The fcode PRKA designates a park boundary polygon, not a geological feature. This internal inconsistency suggests the Blueprint's GeoNames and Wikidata lookups captured two different aspects of the Grand Canyon (the park boundary vs. the geological feature) without recognizing the distinction.

---

## IV. GeoNames Canonical ID — RATIFIED: 5296401 (L.PRK)

**NC-DATA-003 (2026-06-12) confirmed the following via live GeoNames RDF API:**

| ID | Actual identity | GeoNames RDF confirmed |
|----|----------------|----------------------|
| **5296401** | **Grand Canyon National Park** | name="Grand Canyon National Park", fcl=L, fcode=PRK, AZ, Coconino, Wikipedia linked |
| 5296404 | Grand Canyon National Game Preserve (1906 Roosevelt preserve) | Distinct historical entity — NOT a typo of 5296401 |
| 5513679 | Thunder Mountain, Nye County, Nevada | T.MT (mountain), completely unrelated to Grand Canyon |

**Wikidata Q220289 P1566 = "5296401" confirmed live.** FRR §III was correct for Grand Canyon (unlike Yellowstone where it was wrong).

**Feature code correction:** FRR §III claimed fcode=PRKN for 5296401. Actual code confirmed by GeoNames RDF = **L.PRK** (park). PRKN is not a standard GeoNames feature code. Grand Canyon (5296401) and Yellowstone (5843591 = PRKA) use different but both valid park-type feature codes.

**5296404 "typo" claim was wrong:** FRR §III claimed 5296404 was a typo of 5296401 (last digit 3→1). In reality, 5296404 is the Grand Canyon National Game Preserve — a distinct historical entity established by Theodore Roosevelt in 1906, predating the 1919 national park designation. Both records exist independently in GeoNames.

**5513679 (Blueprint) was completely unrelated:** Thunder Mountain, Nye County, Nevada (T.MT). Not in Arizona, not a park. Blueprint fcode=PRKA claim was also wrong (actual: T.MT).

---

## V. Retirement Candidates

### RETIRED

| ID/QID | Retirement basis |
|--------|-----------------|
| **Q131648** (Wikidata) | Geological canyon feature — not the NC place anchor. Blueprint-only, superseded by Q220289 consensus. Retire from all canonical records. |

### PROVISIONAL — production hold pending verification

| ID | Status | Production location |
|----|--------|---------------------|
| **5296401** | Unverified provisional | `pilot_anchor.canonical_identity` (migration 38). Must not be written to `places` table or used in any place page activation until fixture-confirmed. |

### UNVERIFIED — not in production, identity unknown

| ID | Status |
|----|--------|
| **5513679** | Unverified. fcode=PRKA claim is credible but unsupported by fixtures. Cannot be adopted without GeoNames API confirmation. |
| **5296404** | Unverified. May be a distinct GeoNames record for a Grand Canyon feature, not a typo. Cannot be ruled in or out without fixtures. |

---

## VI. Authority Hierarchy

Per DD-GEONAMES-001, the binding authority order for place identity is:

1. **GeoNames direct API fixture** — authoritative and binding. Does not currently exist for Grand Canyon. Must be created before canonical ID can be determined.

2. **Wikidata Q220289 P1566** — secondary reference. Subject to GeoNames authority override (per DD-GEONAMES-001 Invariant S-3). A Wikidata fixture for Q220289 does not exist in the test suite (`entity_grand_canyon.json` is absent). No fixture verifies what Wikidata currently says Q220289 P1566 is.

3. **FRR §III Wikidata lookup** — documented as a live lookup performed 2026-06-11. Proven unreliable for Yellowstone. Provides provisional value (5296401) only.

4. **Intelligence Plan** — non-ratified implementation document. Provided 5296404. Lower authority than direct fixture.

5. **Commercial Pilot Blueprint** — ratified governance document but contained wrong Wikidata QID (Q131648). Provided 5513679. Lower confidence than direct fixture due to internal inconsistency.

The correct resolution path is strictly top-down: create fixture, determine canonical ID, update all downstream records.

---

## VII. Canonical Place Record (Interim)

The Grand Canyon canonical place record as of this document:

| Field | Value | Status |
|-------|-------|--------|
| Slug | `grand-canyon` | Confirmed |
| Name | Grand Canyon National Park | Confirmed |
| Wikidata QID | Q220289 | RATIFIED |
| GeoNames ID | **5296401** | RATIFIED (NC-DATA-003) |
| Feature code | **L.PRK** (park) | CONFIRMED (NC-DATA-003 GeoNames RDF) |
| Country | US | Confirmed |
| State | AZ (Arizona) | Confirmed |
| County | Coconino County | Confirmed |
| Coordinates (GeoNames) | lat 36.10697, lon -112.113 | CONFIRMED (NC-DATA-003 GeoNames RDF) |

---

## VIII. Completed Actions (NC-DATA-003)

GCA-001 and GCA-002 completed 2026-06-12. See NC-DATA-003 for full evidence package.

| Action | Status |
|--------|--------|
| GCA-001: Grand Canyon GeoNames fixtures (place/search/hierarchy) | COMPLETE |
| GCA-002: Grand Canyon Wikidata fixture (entity_grand_canyon.json) | COMPLETE |
| GCA-003: Production value 5296401 confirmed — no corrective migration needed | COMPLETE |
| GCA-004: Q131648 retired from Blueprint §III.2 | COMPLETE |
| Feature code PRKN corrected to PRK in migration 47 + authority_resolution.py | COMPLETE (NC-DATA-005 session) |
| OS-4 note: P402=183377 must not be stored on Wikidata ingest | DOCUMENTED |

---

## IX. Errata: NC-PILOT-001 Commercial Pilot Governance Blueprint §III.2

> **ERRATA — 2026-06-12 — NC-DATA-002:** Blueprint §III.2 lists Wikidata QID Q131648 for Grand Canyon. Q131648 is the geological canyon feature; Q220289 is Grand Canyon National Park. Q131648 is retired as the NC place QID. Canonical Wikidata identity = Q220289. GeoNames ID 5513679 listed in Blueprint is unverified pending GCA-001 fixture creation.

---

## X. Production State

`pilot_anchor` migration 38 currently records `preferred_geonames_id: "5296401"` and `preferred_wikidata_qid: "Q220289"` for `grand-canyon`. The Wikidata QID is confirmed correct. The GeoNames ID is provisional — migration 46 (NC-DATA-001) does not touch Grand Canyon. A new corrective migration will be required once GCA-001/GCA-002 confirm the canonical GeoNames ID.

The Grand Canyon place page is **"Coming soon"** in governed-content.ts and has no active public surface. The provisional GeoNames ID causes no immediate user impact. However, GCA-001 and GCA-002 must be completed before any of the following:

- Grand Canyon place page phase activation (Gate E pre-activation)
- Grand Canyon product activation (NC-PROD-002, NC-PROD-003)
- Grand Canyon content pack AI generation (requires confirmed grounding per NC-AI-004 §II.4)
- `places.geonames_id` write for Grand Canyon

---

*NC-DATA-002 — Grand Canyon Authority Resolution — FULL RATIFICATION — 2026-06-12*
