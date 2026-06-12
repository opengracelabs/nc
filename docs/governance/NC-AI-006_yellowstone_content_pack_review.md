# NC-AI-006: Yellowstone AI Content Pack Review

**Document ID:** NC-AI-006  
**Status:** BLOCKED  
**Date:** 2026-06-12  
**Reviewer:** Principal Architect  
**Reference models:** NC-AI-001, NC-AI-004, NC-AI-005, NC-WEB-001, SA-GEONAMES-001, SA-GBIF-001, SA-NARA-001, yellowstone_prototype_specification_v1.md, DD-OSM-001

---

## I. Scope

This review evaluates whether the Yellowstone place content pack is safe to proceed into the AI-grounded generation pipeline defined in NC-AI-004. Five grounding criteria are evaluated. Additional findings are documented independently of the five criteria.

The five required grounding criteria are:
1. GeoNames grounding — canonical place identity
2. NASA grounding — Yellowstone from Orbit asset
3. GBIF grounding — biological evidence
4. NARA grounding — Hayden Survey map
5. BHL grounding — historical illustration

All five must pass for the content pack to proceed to NC-AI-004 generation.

---

## II. Decision

> **BLOCKED**

Five of five grounding criteria are blocked or unresolvable without prerequisite governance actions. Three deferred asset violations are present in the current asset verification report. A Tier 1 schema defect (identified in NC-AI-005 C-1) prevents Yellowstone snapshot writes at the database level. BHL has never entered the Institution Factory onboarding process.

This content pack cannot proceed to AI generation until all conditions listed in §VII are resolved.

---

## III. Grounding Review

### Criterion 1 — GeoNames Grounding

**STATUS: BLOCKED — three-way canonical ID conflict**

The canonical GeoNames ID for Yellowstone National Park is asserted as three different values across authoritative NC governance documents and fixtures:

| Source | GeoNames ID | Document status |
|--------|-------------|-----------------|
| `tests/fixtures/geonames/place_yellowstone.json` | **5843591** | Live API response, fcode=PRKA |
| `tests/fixtures/geonames/hierarchy_yellowstone.json` | **5843591** | Live API hierarchy, confirmed |
| `docs/governance/yellowstone_prototype_specification_v1.md` Art. 4, 22 | **5843591** | Ratified 2026-06-07 |
| `tests/fixtures/wikidata/entity_yellowstone.json` P1566 | **5844046** | Live Wikidata fixture |
| `infrastructure/postgres/init/38_pilot_001_runtime.sql` line 264 | **5843642** | Production migration |
| NC-WEB-001 §III.3 + §V.5 | **5843642** | Stated "confirmed via Wikidata P1566, 2026-06-11" |

**Critical conflict:** NC-WEB-001 §V.5 asserts that ID 5843642 was "confirmed via Wikidata P1566, 2026-06-11." The actual Wikidata P1566 value in `entity_yellowstone.json` is 5844046 — not 5843642. Either the Wikidata fixture is incorrect or NC-WEB-001's confirmation claim is incorrect. Both cannot be true simultaneously.

The ratified Prototype Specification (2026-06-07) uses 5843591. The GeoNames API fixture consistently returns 5843591 for fcode=PRKA "Yellowstone National Park." The production migration uses 5843642, which does not appear in any fixture.

**Impact on grounding:** AI-generated Yellowstone page copy must cite the canonical GeoNames ID (AI-ATT-1, NC-AI-004 §II.4). With three competing values across governance documents, no safe canonical citation is possible. The generation pipeline cannot safely invoke GeoNames grounding.

**Required resolution (GEO-001):** Perform live GeoNames API calls to `/get?geonameId=5843591`, `/get?geonameId=5843642`, and `/get?geonameId=5844046`. Identify which ID maps to fcode=PRKA "Yellowstone National Park." Update `entity_yellowstone.json`, `place_yellowstone.json`, `hierarchy_yellowstone.json`, `38_pilot_001_runtime.sql`, NC-WEB-001, NC-AI-004, and the Prototype Specification to a single verified ID. GEO-001 is a prerequisite for all AI grounding.

---

### Criterion 2 — NASA Grounding

**STATUS: CONDITIONAL PASS — NC-NASA-026 activation unconfirmed**

NASA fixture `tests/fixtures/nasa/live_g6_yellowstone_sample_fixture.json`:
- Asset: `sts068-247-061` (Yellowstone Lake/National Park)
- Mission: STS-68 Endeavour, 1994-09-30
- Center: JSC
- Rights: `federal_center_clean_rights` (17 U.S.C. § 105)
- `expected_pilot_eligible: true`
- `live_verified_date: 2026-06-10`

The fixture is structurally correct. Rights basis 17 U.S.C. § 105 is valid for this asset. FS-001 (NARA attribution prohibition) applies only to the Earthrise AS08-14-2383 asset and does not constrain this fixture. The NASA nonendorsement requirement (`NASA_NONENDORSEMENT`) applies to all NASA-sourced content — confirmed enforced by `PROHIBITED_PHRASES` validation in `services/ai/page_generation.py`.

**Conditional hold:** NC-WEB-001 §V.5 designates "NC-NASA-026: Yellowstone from Orbit" as the Phase 1 Yellowstone NASA asset. The fixture covers `sts068-247-061` in a G6 smoke test context. The NC-NASA-026 `source_item` record activation in the production database has not been confirmed. Until NC-NASA-026 is confirmed active in `source_items`, the NASA grounding for the Yellowstone place page cannot be asserted as production-ready.

**Required condition (NASA-001):** Confirm NC-NASA-026 is inserted and `governance_state = 'active'` in `source_items` before generating Yellowstone NASA-grounded copy.

---

### Criterion 3 — GBIF Grounding

**STATUS: BLOCKED — no Yellowstone GBIF fixture exists**

No GBIF fixture scoped to Yellowstone National Park exists in `tests/fixtures/gbif/`. The four existing GBIF fixtures are generic license-testing records (`occurrence_cc0.json`, `occurrence_cc_by.json`, `occurrence_cc_by_nc.json`, `occurrence_missing_license.json`) and a generic search page fixture (`occurrence_search_page.json` — taxonKey 5219404, not Bison bison).

NC-WEB-001 §V.5 mandates GBIF as the biological evidence source for Yellowstone wildlife claims (bison, wolf, grizzly, elk, bald eagle). SA-GBIF-001 (GBIF Evidence Authority Standard) requires that taxon evidence be grounded against GBIF occurrence data using `gbif_taxon_key` as the biological anchor.

Migration 34 (`34_asset_intelligence_place_iconic_taxa.sql`) registers five Yellowstone taxa: Bison bison (5219334, American bison), Canis lupus (Gray wolf), Ursus arctos horribilis (Grizzly bear), Cervus canadensis (Elk), Haliaeetus leucocephalus (Bald eagle). These taxa have no associated GBIF occurrence fixtures for Yellowstone grounding verification.

**Impact:** Any AI-generated Yellowstone copy referencing wildlife will be ungrounded. NC-AI-004 §II.4 (Entity ID Invariant) prohibits ungrounded claims. The `ai_grounding_source` constraint `chk_ai_grounding_no_gbif_media` blocks GBIF media use but does not enforce that GBIF occurrence evidence is present. Without a fixture, positive-path verification cannot occur.

**Required resolution (GBIF-001):** Create Yellowstone GBIF occurrence fixtures for Bison bison (taxonKey 5219334) with CC0 license (the only GBIF license class permitted per SA-GBIF-001 §Policy-4: occurrence evidence only, no media ingestion). Implement GBIF occurrence lookup in the Yellowstone retrieval package.

---

### Criterion 4 — NARA Grounding

**STATUS: BLOCKED — explicit governance hold, Sprint 1 pending**

NC-WEB-001 §V.5 designates `NARA-HAYDEN-1871: Hayden Survey Map 1871` as a Phase 1 Yellowstone asset with explicit note: *"pending NARA Sprint 1 `Unrestricted` confirmation; display as 'Coming soon — verifying archival status'."*

The NARA record fixture (`tests/fixtures/nara/record_unrestricted.json`) contains no Hayden Survey content. No Yellowstone-specific NARA fixture exists. NARA Sprint 1 has not been completed per project status.

**Governance boundary ambiguity:** The Yellowstone Prototype Specification Article 7 references "Hayden Survey maps from the Library of Congress (LOC:97683567)" — a LOC-sourced asset, not NARA. The governance boundary between NARA and LOC Hayden Survey holdings has not been resolved. LOC `governance_state = 'proposed'` (blocked by prototype spec blockers list, item 3). Neither institution is activated for Yellowstone content.

**Note on status:** This is not an unexpected deficiency. The NARA hold is explicitly documented in NC-WEB-001 as a known governance state with a defined display instruction ("Coming soon"). The NARA asset cannot be included in the active grounding set until Sprint 1 completes.

**Required condition (NARA-001):** NARA Sprint 1 must complete and confirm `useRestriction.status == "Unrestricted"` for the Hayden Survey Map. Until then, the NARA grounding criterion cannot be met. The LOC/NARA governance boundary must also be resolved before either institution's Hayden Survey holdings can be incorporated.

---

### Criterion 5 — BHL Grounding

**STATUS: BLOCKED — BHL has no Institution Factory record**

No BHL (Biodiversity Heritage Library) directory exists in `tests/fixtures/`. No BHL adapter, no DD-BHL-001, no BHL rights matrix, no BHL pilot authorization, and no BHL `source_institution` record exists in the codebase.

NC-WEB-001 §V.5 references `BHL-BISON-001: American Bison illustration — pre-1928 PD` as a Phase 1 Yellowstone asset. BHL has never entered the Institution Factory onboarding process (IFC v1, Stage 1: Discovery). Per IFC-1, no asset from an institution that has not completed Stage 7 (Asset Zero) can be included in a production content pack.

**Required resolution (BHL-001):** File DD-BHL-001 (BHL Audit). BHL must complete Institution Factory Stages 1–7 minimum (Discovery → Asset Zero) before any BHL asset can appear in a content pack. A BHL-BISON-001 fixture scoped to an activated BHL asset record must be created. BHL pre-1928 rights determination must be documented in a BHL Rights Matrix.

---

## IV. Additional Findings

### F-1 — Deferred Asset EU-YEL-002 (Thomas Moran — FS-002 Violation)

`reports/yellowstone_asset_verification_report.md` lists EU-YEL-002: "Thomas Moran's definitive view of the Grand Canyon of the Yellowstone" (sourced from British Library via Europeana). Thomas Moran is a permanently deferred asset pending DD-SMITHSONIAN-001.

**Active blocks:** (a) `PROHIBITED_PHRASES` in `services/ai/page_generation.py:33` includes `"Moran"` — any generated copy containing "Moran" will raise `PageGenerationError`. (b) The asset verification report input contains the Moran asset, meaning the content pack inputs are contaminated at source.

**Required action:** EU-YEL-002 must be removed from the Yellowstone content pack before any generation attempt. The asset verification report must be revised.

---

### F-2 — Prohibited Asset EU-YEL-025 (Smithsonian Attribution)

EU-YEL-025 is attributed to "Smithsonian (Europeana)" in the asset verification report. `PROHIBITED_PHRASES:34` includes `"Smithsonian"`. The page generation service will reject any copy containing this attribution.

**Required action:** EU-YEL-025 must be removed from the content pack. A Smithsonian-sourced asset cannot appear in any content pack until DD-SMITHSONIAN-001 is filed and ratified.

---

### F-3 — Asset Verification Report Is Preliminary — Source Links and Rights URIs Missing

`reports/yellowstone_asset_verification_report.md` is explicitly labeled "Preliminary (Awaiting Source Links)." Canonical Europeana source URLs and specific rights URIs are absent for all EU-YEL-* assets.

NC-AI-004 §II.4 (Entity ID Invariant) requires that all retrieval packages include verified canonical source URLs and `rights_status = 'verified_pd'`. A preliminary report without source links cannot serve as the grounding basis for AI generation. This is independent of the Moran and Smithsonian violations.

**Required action (REPORT-001):** Complete the asset verification report. For each retained asset: confirm canonical source URL, confirm rights URI, confirm `rights_status = 'verified_pd'` or equivalent PD-clear designation.

---

### F-4 — Prototype Specification Contradicts Asset Verification Report

The Yellowstone Prototype Specification (ratified 2026-06-07) mandates LOC-only assets for Yellowstone Phase 1 (Articles 2, 3, 6, 7). The Asset Verification Report uses Europeana-sourced assets (EU-YEL-001 to EU-YEL-025) from the British Library, Smithsonian, and other institutions. These documents are contradictory.

Either the Prototype Specification was superseded by the Asset Verification Report, or the Asset Verification Report was produced outside of NC governance. Neither document currently governs the other. The content pack cannot proceed with two contradictory source-authority documents.

**Required action (PROTO-001):** Resolve the contradiction. Either (a) file a Director Decision superseding the LOC-only constraint in the Prototype Specification, or (b) discard the Europeana asset set and produce a LOC-based asset set per the ratified Prototype Specification. One document must have explicit precedence.

---

### F-5 — Tier 1 Schema Defect Blocks Yellowstone Snapshot Writes

`infrastructure/postgres/init/44_nc_ai_004_page_generation.sql:49–51` contains:

```sql
CONSTRAINT chk_ai_page_snapshot_attribution CHECK (
    attribution_block LIKE '%Image credit: NASA. NASA does not endorse this product.%'
)
```

This constraint applies to ALL `ai_page_generation_snapshot` rows unconditionally — not just NASA-sourced pages. Any Yellowstone place page snapshot that does not contain the NASA nonendorsement string will fail this check at the database level.

This defect was documented as C-1 in NC-AI-005, with Migration 45 specified as the fix. Migration 45 has not been written or applied.

**Blocking consequence:** Even if all five grounding criteria were resolved, the Yellowstone content pack could not produce a persisted snapshot under the current schema.

**Required action (SCHEMA-001):** Write and apply Migration 45 per NC-AI-005 §V.4 spec before any non-NASA page generation is attempted.

---

### F-6 — OSM P402 in Wikidata Fixture Must Not Be Stored

`tests/fixtures/wikidata/entity_yellowstone.json` includes `"P402": "1453307"` (OSM relation ID for Yellowstone). Per OS-4 (DD-OSM-001), OSM identifiers must never be stored in canonical tables. If the Wikidata ingestion path writes P402 values to any NC table, this is a constitutional violation.

**Required action (OSM-001):** Explicitly exclude P402 from the Wikidata ingestion path. Add a DB-level constraint or ingestion filter confirming OSM IDs are dropped on ingest. Document in SA-WIKIDATA-001 Amendment 1.

---

## V. Grounding Criteria Summary

| Criterion | Status | Condition |
|-----------|--------|-----------|
| 1. GeoNames | BLOCKED | Three-way ID conflict — GEO-001 required |
| 2. NASA | CONDITIONAL PASS | NC-NASA-026 activation unconfirmed — NASA-001 required |
| 3. GBIF | BLOCKED | No Yellowstone GBIF fixture — GBIF-001 required |
| 4. NARA | BLOCKED | Sprint 1 pending, LOC boundary unresolved — NARA-001 |
| 5. BHL | BLOCKED | No Institution Factory record — BHL-001 required |

**Verdict: BLOCKED (4 of 5 criteria failed; 1 conditional)**

---

## VI. Deferred Asset and Prohibited Content Summary

| Asset | Violation | Status |
|-------|-----------|--------|
| EU-YEL-002: Thomas Moran (British Library) | FS-002, PROHIBITED_PHRASES:33 | Remove from content pack |
| EU-YEL-025: Smithsonian (Europeana) | PROHIBITED_PHRASES:34 | Remove from content pack |
| NARA-HAYDEN-1871 | On governance hold | Display as "Coming soon" only |

---

## VII. Resolution Path (Ordered by Dependency)

The following conditions must be satisfied before this review can be re-submitted as APPROVED. Conditions are ordered by dependency chain.

**Tier 1 — Prerequisite to all generation (must complete first):**

1. **SCHEMA-001**: Apply Migration 45 (NC-AI-005 §V.4). Fix `chk_ai_page_snapshot_attribution` Tier 1 defect. Without this, no Yellowstone snapshot can be written to the database.

2. **ASSET-001**: Remove EU-YEL-002 (Moran) and EU-YEL-025 (Smithsonian) from the content pack. Revise `reports/yellowstone_asset_verification_report.md`.

3. **PROTO-001**: Resolve contradiction between Prototype Specification (LOC-only) and Asset Verification Report (Europeana sources). File superseding DD or produce LOC-based asset set.

**Tier 2 — Grounding resolution (GEO-001 is a dependency for all others):**

4. **GEO-001**: Resolve three-way GeoNames ID conflict via live API calls. Update all affected documents and migrations to a single verified ID. This is a dependency for all AI grounding in Yellowstone.

5. **GBIF-001**: Create Yellowstone GBIF occurrence fixtures for Bison bison (taxonKey 5219334, CC0). Implement GBIF occurrence lookup in the Yellowstone retrieval package.

6. **OSM-001**: Exclude P402 from Wikidata ingestion path. Add ingestion filter and document in SA-WIKIDATA-001.

**Tier 3 — Institution Factory (BHL):**

7. **BHL-001**: File DD-BHL-001 (BHL Audit). Complete Institution Factory Stages 1–7. Create BHL Rights Matrix and BHL-BISON-001 fixture. BHL-001 is a long-horizon prerequisite; Yellowstone content pack may be split into an interim version (without BHL) pending BHL-001 completion.

**Tier 4 — Conditional (active governance holds):**

8. **NARA-001**: NARA Sprint 1 completes and confirms `Unrestricted` status for Hayden Survey holdings. LOC/NARA governance boundary resolved. NARA-HAYDEN-1871 may remain on "Coming soon" hold until Sprint 1 completes — this does not block other content pack criteria.

9. **NASA-001**: Confirm NC-NASA-026 source_item is active in production before generating Yellowstone NASA-grounded copy.

---

## VIII. Scope Notes

This review does not evaluate the correctness of the AI-generated text itself. The content pack review assesses grounding infrastructure, source evidence, rights status, and prohibited content — preconditions to AI generation, not the generation output. NC-AI-004 §VIII defines the five-step human review workflow that governs the generated output after these preconditions are met.

NC-AI-006 will require re-submission as a new Director Decision review once all Tier 1 and Tier 2 resolution conditions are satisfied.

---

*NC-AI-006 — Yellowstone AI Content Pack Review — BLOCKED — 2026-06-12*
