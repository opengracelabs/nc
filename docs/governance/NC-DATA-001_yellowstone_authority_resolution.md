# NC-DATA-001: Yellowstone Authority Resolution — Canonical GeoNames ID Decision

**Document ID:** NC-DATA-001  
**Status:** RATIFIED  
**Date:** 2026-06-12  
**Authority:** Principal Architect  
**Supersedes:** NC-PILOT-001 Final Readiness Review §III (Yellowstone row only)  
**Reference authority:** DD-GEONAMES-001, SA-GEONAMES-001, yellowstone_prototype_specification_v1.md

---

## I. Decision

> **Canonical GeoNames ID for Yellowstone National Park: 5843591**

All NC governance documents, migrations, tests, and source code using 5843642 or 5844046 as the place identifier for Yellowstone National Park must be corrected to 5843591.

5843642 is retired as a place identifier for Yellowstone. 5844046 is retained only in Wikidata evidence records (see §VI).

---

## II. Evidence Summary

Three GeoNames IDs appeared across NC governance documents and fixtures:

| ID | Feature | Source |
|----|---------|--------|
| **5843591** | fcode=PRKA, "Yellowstone National Park" | GeoNames API fixtures (3 files); ratified Prototype Spec; all GeoNames unit tests |
| **5843642** | Claimed fcode=`L PRK` (intel plan) / `PRKN` (readiness review) | Intelligence Plan v1; NC-PILOT-001 FRR §III; production migrations 38 and 39 |
| **5844046** | Wikidata Q351 P1566 value | Wikidata entity fixture; Wikidata normalizer tests |

### GeoNames fixture record for 5843591

Three independent fixtures all return 5843591 for Yellowstone National Park:

- `tests/fixtures/geonames/place_yellowstone.json` — direct `/get` API response: `geonameId: 5843591`, `name: "Yellowstone National Park"`, `fcl: L`, `fcode: PRKA`, `adminCode1: WY`
- `tests/fixtures/geonames/hierarchy_yellowstone.json` — `/hierarchy` response: Earth → United States → 5843591 (fcode=PRKA)
- `tests/fixtures/geonames/search_yellowstone.json` — `/searchJSON` response: `totalResultsCount: 1`, single result = 5843591 (fcode=PRKA)

The `totalResultsCount: 1` is determinative: the GeoNames API returns exactly one record for "Yellowstone National Park." That record is 5843591.

---

## III. Root Cause: The 5843642 Error Chain

5843642 was never confirmed by a GeoNames API response. Its adoption followed a four-step error chain:

**Step 1 — GeoNames Intelligence Plan v1** (`docs/implementation/geonames_intelligence_plan_v1.md`): Listed 5843642 for Yellowstone with feature code `L PRK`. This is a non-ratified implementation planning document. The source of 5843642 is unrecorded — it was not validated against a fixture or live API call.

**Step 2 — NC-PILOT-001 Final Readiness Review §II.C-4**: Attempted to "confirm" the intelligence plan's IDs by performing "Wikidata P1566 lookups (2026-06-11)." The review table recorded Yellowstone as Q351 → P1566 = 5843642, and declared this "confirmed via Wikidata P1566."

**Step 3 — The false claim**: The Wikidata fixture for Q351 (`tests/fixtures/wikidata/entity_yellowstone.json`) shows `P1566 = "5844046"`, not 5843642. The final readiness review's Wikidata P1566 lookup produced a result inconsistent with the fixture. The confirmation claim is false. Either the lookup was performed against a different Wikidata item, the Wikidata data differed at the time of the lookup, or the result was recorded incorrectly.

**Step 4 — Downstream inheritance**: The NC-PILOT-001 FRR §III declared itself "the canonical reference" and stated all prior conflicting IDs were superseded. Production migrations 38 and 39, NC-WEB-001, NC-COMMERCE-001, NC-COMMERCE-002, and NC-AI-004 all inherited 5843642 from this declaration — without any GeoNames fixture support.

The Prototype Specification (ratified 2026-06-07, the same date as the final readiness review) was never updated and continued to carry 5843591 — preserving the correct value in the oldest and most directly reasoned governance document.

---

## IV. Why 5843591 Is Authoritative

Per DD-GEONAMES-001, GeoNames is the Place Identity and Evidence Authority. GeoNames data is authoritative over Wikidata for place identity (Invariant S-3). The NC authority hierarchy for place identity is:

> GeoNames direct API > Wikidata P1566 > implementation plan references

**5843591 satisfies the GeoNames direct API criterion.** Three GeoNames fixtures return it, the search fixture confirms it is the singular canonical record (totalResultsCount: 1), and all GeoNames unit and sprint replay tests assert it.

**5843642 does not satisfy any GeoNames fixture criterion.** Its feature code description is internally inconsistent (intelligence plan: `L PRK`; final readiness review: `PRKN`). `PRKN` is not present in the standard GeoNames feature code taxonomy for class L. No GeoNames fixture has ever returned 5843642 for a Yellowstone lookup. Its identity in GeoNames is unknown.

**5844046 is a Wikidata claim, not a GeoNames confirmation.** Per DD-GEONAMES-001, the Wikidata P1566 property is a secondary reference to a GeoNames ID — it is not authoritative over a direct GeoNames API response. The Wikidata normalizer correctly extracts P1566=5844046 as what Wikidata asserts; this value belongs in Wikidata evidence records, not in the `places` canonical identifier.

---

## V. Which IDs Must Be Retired

### ID 5843642 — RETIRED as a Yellowstone place identifier

No NC canonical record (places table, pilot_anchor, product attribution, governance document, or code) may use 5843642 as the Yellowstone GeoNames ID. This ID has no GeoNames fixture support. Its feature identity in GeoNames is unknown and unverified.

All code and governance documents must be corrected per §VII.

### ID 5844046 — RETAINED in Wikidata evidence scope only

5844046 is what Wikidata Q351 P1566 currently asserts. This is correct Wikidata data and the Wikidata normalizer is correct to extract it. 5844046 must be stored in Wikidata evidence records (`wikidata_evidence.geonames_id`, `identity_snapshot.geonames_id` for Wikidata-sourced records) and must never be written to `places.geonames_id` or `pilot_anchor.canonical_identity.preferred_geonames_id`.

The Wikidata test assertions for P1566=5844046 (`test_wikidata_normalize.py:28`, `test_wikidata_evidence_sprint1.py:40`) are correct and must not be changed.

---

## VI. Wikidata P1566 Discrepancy

The Wikidata fixture shows P1566=5844046 for Q351. The final readiness review claimed P1566=5843642. These cannot both be correct.

Per DD-GEONAMES-001, this discrepancy is resolved by GeoNames authority: neither Wikidata value overrides the GeoNames direct API response (5843591). However, the discrepancy itself may indicate either:

(a) Wikidata Q351 P1566 was 5843642 at the time of the final readiness review lookup and was later corrected to 5844046, or

(b) The final readiness review lookup was incorrect.

Resolution of the discrepancy between Wikidata P1566 (5844046) and GeoNames direct (5843591) is a Wikidata data quality matter. It does not change the NC canonical determination. The correct action is to store both values in their respective authority layers — 5843591 in the GeoNames canonical layer, 5844046 in the Wikidata evidence layer — and let the GeoNames value govern all production place pages.

A separate live GeoNames lookup against geonameId=5844046 is recommended (but not required before this decision takes effect) to identify what feature 5844046 represents. This lookup should be recorded in a maintenance note to this document.

---

## VII. Required Corrections

### Code corrections (blocking — apply via Migration 46)

| Item | Current value | Corrected value | File |
|------|--------------|-----------------|------|
| `pilot_anchor.canonical_identity.preferred_geonames_id` (slug=yellowstone) | 5843642 | 5843591 | Migration 46 (UPDATE) |
| `product_candidate.assembled_attribution` GeoNames URL (anchor=yellowstone) | `.../5843642` | `.../5843591` | Migration 46 (UPDATE) |

### Test corrections (blocking)

| Test | Line | Current assertion | Corrected assertion |
|------|------|-------------------|---------------------|
| `tests/replay/test_nc_pilot_001_runtime.py` | 71 | `"preferred_geonames_id":"5843642"` | `"preferred_geonames_id":"5843591"` |
| `tests/replay/test_nc_pilot_001_runtime.py` | 79 | `"preferred_geonames_id":"5843591" not in sql` | Remove this assertion |
| `tests/unit/test_pilot_api.py` | 55–58 | `geonames_id: "5843642"`, URL `.../5843642` | `geonames_id: "5843591"`, URL `.../5843591` |

### Governance document corrections (informational — superseded by this document)

This document supersedes the Yellowstone row in NC-PILOT-001 FRR §III. Downstream documents that inherited 5843642 are corrected by reference to NC-DATA-001. The following documents carry the erroneous ID and should be updated on next scheduled revision:

- NC-WEB-001 §III.3, §V.5 (canonical GeoNames ID note)
- NC-AI-004 §V.5 canonical IDs table
- NC-PILOT-001 Final Readiness Review §III (Yellowstone row — add errata note)
- NC-PILOT-001 Final Governance Review §C-4 table
- NC-PILOT-001 Launch Authorization §III
- NC-PILOT-001 Closure Report
- NC-COMMERCE-001 (three place anchor tables)
- NC-COMMERCE-002 (NC-PROD-002 row)
- `Yellowstone AI Content Pack.md` (header GeoNames ID)

---

## VIII. Do Not Update (Correct by Design)

| Item | ID | Reason |
|------|----|--------|
| `entity_yellowstone.json` P1566 | 5844046 | Correct Wikidata data; leave unchanged |
| `test_wikidata_normalize.py:28` | 5844046 | Wikidata normalizer behavior is correct |
| `test_wikidata_evidence_sprint1.py:40` | 5844046 | Wikidata sprint replay is correct |
| `place_yellowstone.json`, `hierarchy_yellowstone.json`, `search_yellowstone.json` | 5843591 | Already correct |
| All `test_geonames_*.py` | 5843591 | Already correct |

---

*NC-DATA-001 — Yellowstone Authority Resolution — RATIFIED — 2026-06-12*
