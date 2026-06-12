# Yellowstone Content Dependency Report (NC-DATA-001)

This report identifies all references to the three GeoNames IDs evaluated in the **NC-DATA-001 Yellowstone Authority Resolution**. Per the ratified decision, **5843591** is the authoritative canonical ID for Yellowstone National Park. **5843642** is retired/erroneous, and **5844046** is restricted to Wikidata evidence records.

---

## 1. Dependencies on 5843591 (Authoritative / Canonical)

These references are correct and align with the authoritative GeoNames API fixtures.

| Category | File Path | Reference Detail |
| :--- | :--- | :--- |
| **Governance** | `docs/governance/NC-DATA-001_yellowstone_authority_resolution.md` | Defined as the canonical ID for Yellowstone National Park. |
| **Governance** | `docs/governance/NC-WEB-001_website_governance_ux_blueprint.md` | Adopted as authoritative (superseding 5843642). |
| **Governance** | `docs/governance/yellowstone_prototype_specification_v1.md` | Used as the foundational ID (Ratified 2026-06-07). |
| **Governance** | `docs/decisions/DD-EUR-001_europeana_production_activation.md` | Used for Yellowstone place association. |
| **Governance** | `docs/governance/europeana_activation_checklist_v1.md` | Confirmed as the place identifier for Yellowstone. |
| **Infrastructure** | `infrastructure/postgres/init/38_pilot_001_runtime.sql` | Corrected to 5843591 in line 264. |
| **Infrastructure** | `infrastructure/postgres/init/46_nc_data_001_authority_resolution.sql` | Migration script establishing 5843591 as canonical. |
| **Fixtures** | `tests/fixtures/geonames/place_yellowstone.json` | Direct `/get` API response for Yellowstone National Park. |
| **Fixtures** | `tests/fixtures/geonames/hierarchy_yellowstone.json` | Hierarchy response mapping to 5843591. |
| **Fixtures** | `tests/fixtures/geonames/search_yellowstone.json` | Search response confirming 5843591 as the singular result. |
| **Tests** | `tests/replay/test_nc_pilot_001_runtime.py` | Asserts 5843591 is present in the database. |
| **Tests** | `tests/unit/test_pilot_api.py` | Asserts 5843591 and its URL are present in API responses. |
| **Tests** | `tests/unit/test_geonames_place.py` | Unit tests for resolving 5843591. |

---

## 2. Dependencies on 5843642 (Erroneous / Retired)

These references must be updated to **5843591** per the NC-DATA-001 mandate.

| Category | File Path | Reference Detail |
| :--- | :--- | :--- |
| **Content Pack** | `Yellowstone AI Content Pack.md` | Header metadata (`GeoNames ID: 5843642`). |
| **Governance** | `docs/governance/NC-PILOT-001_final_readiness_review.md` | Used in the Yellowstone row of §III (Errata note added). |
| **Governance** | `docs/governance/NC-PILOT-001_launch_authorization.md` | Used in the C-1 condition table for Yellowstone NP. |
| **Governance** | `docs/governance/NC-PILOT-001_closure_report.md` | Listed as the Yellowstone identifier. |
| **Governance** | `docs/governance/NC-COMMERCE-001_final_product_activation_review.md` | Used in three place anchor tables for Yellowstone. |
| **Governance** | `docs/governance/NC-COMMERCE-002_first_revenue_authorization.md` | Used in the NC-PROD-002 row. |
| **Planning** | `docs/implementation/geonames_intelligence_plan_v1.md` | Original source of the 5843642 error. |
| **Infrastructure** | `infrastructure/postgres/init/39_product_001_runtime.sql` | Used in the `assembled_attribution` field for NC-PROD-002. |
| **Infrastructure** | `infrastructure/postgres/init/46_nc_data_001_yellowstone_geonames_correction.sql` | Targeted for correction (WHERE clause). |

---

## 3. Dependencies on 5844046 (Wikidata Evidence Only)

These references are correct within the scope of Wikidata evidence and should remain unchanged.

| Category | File Path | Reference Detail |
| :--- | :--- | :--- |
| **Governance** | `docs/governance/NC-DATA-001_yellowstone_authority_resolution.md` | Identified as the Wikidata P1566 claim for Q351. |
| **Fixtures** | `tests/fixtures/wikidata/entity_yellowstone.json` | The P1566 value returned by Wikidata for Q351. |
| **Tests** | `tests/unit/test_wikidata_normalize.py` | Asserts the Wikidata normalizer extracts 5844046. |
| **Tests** | `tests/replay/test_wikidata_evidence_sprint1.py` | Asserts the Wikidata evidence record contains 5844046. |
| **Infrastructure** | `infrastructure/postgres/init/46_nc_data_001_authority_resolution.sql` | Stored as a Wikidata claim in the `identity_evidence` role. |

---
*Yellowstone Content Dependency Report (NC-DATA-001) produced by Gemini CLI*
