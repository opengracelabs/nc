# NC-DATA-004: Great Barrier Reef Authority Resolution — Canonical ID Decision

**Document ID:** NC-DATA-004  
**Status:** FULL RATIFICATION (GBR-001/GBR-002 complete per NC-DATA-005)  
**Date:** 2026-06-12  
**Authority:** Principal Architect  
**Reference authority:** DD-GEONAMES-001, SA-GEONAMES-001, DD-WIKIDATA-001, NC-DATA-001, NC-DATA-003, NC-DATA-005

---

## I. Decision

**Wikidata canonical identity: RATIFIED — Q7343 (Great Barrier Reef)**  
**GeoNames canonical ID: RATIFIED — 2164628 (Great Barrier Reef, H.RF)**

NC-DATA-004 is fully ratified. GBR-001 and GBR-002 are complete (NC-DATA-005, 2026-06-12). Live GeoNames RDF confirmed 2164628 = "Great Barrier Reef" (H.RF, Queensland, Australia). Wikidata Q7343 P1566 = "2164628" confirmed live. No OS-4 concern (Q7343 has no P402).

**Great Barrier Reef place page activation unblocked** — GeoNames ID confirmed. Remaining gates per NC-PILOT-001 LA apply (SA-GEONAMES-001, SA-OSM-001 ratification, NOAA Sprint 3 gate check).

---

## II. Evidence Summary

### GeoNames IDs in contention

Three GeoNames ID claims appeared across NC governance documents:

| ID | Claim | Source document | Confirmed identity |
|----|-------|-----------------|-------------------|
| **2164628** | RFSU (claimed — incorrect) | FRR §III; migration 38; NC-WEB-001; NC-AI-004; NC-COMMERCE-001 | **Great Barrier Reef** (H.RF, Queensland, AU) — CANONICAL |
| **10288865** | `S HTL / REEF` | GeoNames Intelligence Plan v1 | **Clarion Great Barrier Reef hotel** (S.HTL, Queensland, AU) — RETIRED |
| Not specified | fcode: RFU · country: AU | Blueprint §III.3 (no ID given) | Correct feature class guessed, no ID provided — unusable |

### Wikidata QIDs in contention

| QID | Entity | Source documents | Decision |
|-----|--------|-----------------|---------|
| **Q7343** | Great Barrier Reef (coral reef ecosystem) | FRR §III; migration 38; NC-WEB-001; NC-AI-004; NC-PILOT-001 LA; NC-PILOT-001 closure | CANONICAL |
| **Q37901** | Great Barrier Reef Marine Park (GBRMPA — administrative designation) | Blueprint §III.3 only | RETIRED |

---

## III. Wikidata Canonical Identity — RATIFIED: Q7343

> **Canonical Wikidata QID: Q7343 (Great Barrier Reef)**

**Q37901** (Great Barrier Reef Marine Park) is **retired** as the NC place QID.

**Reasoning:**

Q7343 is the coral reef ecosystem — the natural feature itself. Q37901 is the Great Barrier Reef Marine Park, an administrative designation managed by the Great Barrier Reef Marine Park Authority (GBRMPA). For NC as a place-centered commerce platform, the reef system (Q7343) is the correct anchor. Illustration opportunities at the GBR are illustrations of the reef, its marine life, and its geological and ecological character — not of the administrative park boundary.

This follows the same structural logic as Yellowstone (Q351 = the national park, not a geological unit QID) and Grand Canyon (Q220289 = the national park, not Q131648 the geological canyon). In all three cases, the Blueprint misidentified an administrative entity rather than the natural/park feature as the Wikidata QID.

Q7343 evidence from live Wikidata API (2026-06-12):
- P31: Q11292 (coral reef), Q38048753 (reef), Q570116 (UNESCO World Heritage Site), Q9259 (barrier reef)
- P17: Q408 (Australia)
- P625: lat=-16.4, lon=145.8
- P1566: "2164628" — confirms 2164628 as canonical GeoNames ID
- P131: Q36074 (Queensland)
- **No P402 (OSM)** — no OS-4 concern for GBR Wikidata ingestion

---

## IV. GeoNames Canonical ID — RATIFIED: 2164628 (H.RF)

**NC-DATA-005 (2026-06-12) confirmed the following via live GeoNames RDF API:**

| ID | Actual identity | GeoNames RDF confirmed |
|----|----------------|----------------------|
| **2164628** | **Great Barrier Reef** | name="Great Barrier Reef", fcl=H, fcode=RF, AU, Queensland, Wikipedia linked |
| 10288865 | **Clarion Great Barrier Reef hotel** | fcl=S, fcode=HTL, AU, Queensland — a hotel named after the reef |

**Feature code correction:** FRR §III claimed fcode=RFSU (submerged coral reef) for 2164628. NC-WEB-001 also cited RFSU. Actual GeoNames RDF confirmed feature code = **H.RF** (reef). RFSU (H.RFSU) is a different GeoNames feature code for submerged reefs; H.RF is the feature code for reef(s) at the surface. Migration 47, authority_resolution.py, FRR §III, and NC-PILOT-001 LA have all been corrected to RF.

**Blueprint RFU claim:** Blueprint §III.3 noted "fcode: RFU · country: AU" but provided no GeoNames ID. RFU (H.RFU = underwater reef) is a different code from H.RF (reef). The Blueprint's feature class identification was directionally correct (H = hydrographic, reef-type) but the specific code was wrong, and no GeoNames ID was given — unusable as authority.

**Intelligence Plan 10288865 disqualified:** The actual entity is the Clarion hotel ("Clarion Great Barrier Reef"), feature class S (Spot/building), feature code HTL (hotel). The intelligence plan notation `S HTL / REEF` was partially correct in noting `S HTL` but the split notation `/ REEF` implied a reef-type record, which it is not. The intelligence plan was three-for-three wrong across Yellowstone (5843642), Grand Canyon (5296404), and GBR (10288865).

**Wikidata P1566 route was correct for GBR:** Unlike Yellowstone (where FRR §III P1566 was wrong), the FRR §III claim of Q7343 P1566 = 2164628 was confirmed correct by live API. The production value in migration 38 was already correct.

---

## V. Retirement Decisions

### RETIRED

| ID/QID | Retirement basis |
|--------|-----------------|
| **Q37901** (Wikidata) | Great Barrier Reef Marine Park — administrative designation (GBRMPA), not the reef ecosystem. Blueprint-only provenance. Correct anchor is Q7343. |
| **10288865** (GeoNames) | "Clarion Great Barrier Reef" hotel (S.HTL, Queensland). Named after the reef but is a commercial lodging establishment. Intelligence Plan only. Three-for-three wrong across resolved places. |

### CONFIRMED CANONICAL

| ID/QID | Canonical | Status |
|--------|-----------|--------|
| **Q7343** | Great Barrier Reef (coral reef ecosystem) | RATIFIED |
| **2164628** | Great Barrier Reef (H.RF, Queensland, AU) | RATIFIED |

---

## VI. Authority Hierarchy

1. **GeoNames direct API fixture** — `tests/fixtures/geonames/place_great_barrier_reef.json` (CREATED, NC-DATA-005)
2. **Wikidata Q7343 P1566** — confirmed "2164628" live 2026-06-12 — `tests/fixtures/wikidata/entity_great_barrier_reef.json` (CREATED, NC-DATA-005)
3. FRR §III Wikidata lookup — correct for GBR (2164628), consistent with fixture
4. Intelligence Plan — 10288865 was wrong; disqualified
5. Blueprint §III.3 — no GeoNames ID given; RFU feature class guess was directionally correct; Q37901 was wrong

---

## VII. Canonical Place Record

| Field | Value | Status |
|-------|-------|--------|
| Slug | `great-barrier-reef` | Confirmed |
| Name | Great Barrier Reef | Confirmed |
| Wikidata QID | **Q7343** | RATIFIED |
| GeoNames ID | **2164628** | RATIFIED |
| Feature class | H (Hydrographic) | CONFIRMED |
| Feature code | **H.RF** (reef) | CONFIRMED — was incorrectly cited as RFSU in production docs |
| Country | AU | Confirmed |
| State/Territory | Queensland | Confirmed |
| Coordinates (GeoNames) | lat -17.98722, lon 146.76979 | CONFIRMED |
| Coordinates (Wikidata P625) | lat -16.4, lon 145.8 | Secondary |
| OSM P402 | NOT PRESENT in Q7343 | No OS-4 action required |
| Place page activation | Unblocked (GeoNames gate passed) | SA-GEONAMES-001 + SA-OSM-001 + NOAA gate still required |

---

## VIII. Feature Code Errata Cascade

The incorrect RFSU claim appeared in four locations. All corrected:

| File | Old value | New value | Correction method |
|------|-----------|-----------|------------------|
| `infrastructure/postgres/init/47_nc_data_002_authority_resolution_pilot_places.sql` | `"feature_code":"RFSU"` | `"feature_code":"RF"` | Direct edit |
| `services/data/authority_resolution.py` | `feature_code="RFSU"` | `feature_code="RF"` | Direct edit |
| `docs/governance/NC-PILOT-001_final_readiness_review.md` | `RFSU (coral reef)` | `RF (reef)` | Direct edit |
| `docs/governance/NC-PILOT-001_launch_authorization.md` | `RFSU` | `RF (H.RF)` | Direct edit |

---

## IX. Errata: NC-PILOT-001 Commercial Pilot Governance Blueprint §III.3

> **ERRATA — 2026-06-12 — NC-DATA-004:**  
> Blueprint §III.3 lists Wikidata QID Q37901 for Great Barrier Reef. Q37901 is the Great Barrier Reef Marine Park (administrative designation); Q7343 is the Great Barrier Reef ecosystem. Q37901 is retired as the NC place QID. Canonical Wikidata identity = Q7343.  
> Blueprint §III.3 noted fcode: RFU but provided no GeoNames ID. Canonical GeoNames ID = 2164628 (H.RF, confirmed via live GeoNames RDF 2026-06-12). Actual feature code is H.RF, not RFU.

---

## X. Production State

`pilot_anchor` migration 38 records `preferred_geonames_id: "2164628"` and `preferred_wikidata_qid: "Q7343"` for `great-barrier-reef` — both confirmed correct. No corrective migration required. Migration 47 feature code was RFSU (corrected to RF in this session).

The Great Barrier Reef place page is Phase 2 in governed-content.ts. Production blockers are SA-GEONAMES-001 and SA-OSM-001 ratification, and the NOAA Sprint 3 gate check (per NC-WEB-001 §III.7) — not GeoNames identity.

---

*NC-DATA-004 — Great Barrier Reef Authority Resolution — FULL RATIFICATION — 2026-06-12*
