# Correction Report

**Authority:** NC-FIRST-SALE Copy Correction Sprint  
**Status:** Implemented

## Corrections Applied

1. Replaced first-sale non-NASA sourcing references with NASA Image and Video Library / NASA public-domain source language.
2. Removed NASA verification-claim wording from first-sale campaign copy.
3. Inserted required NASA attribution: `Image credit: NASA.`
4. Inserted NASA nonendorsement: `Image credit: NASA. NASA does not endorse this product.`
5. Created COA template for NC-PROD-001 Earthrise Museum Giclée Print.

## Corrected Files

- `docs/implementation/nc_first_sale_campaign_package.md`
- `docs/implementation/nc_first_sale_playbook.md`
- `data/exports/first_commercial_catalog.md`
- `docs/governance/NC-FIRST-SALE_COA_template.md`

## Verification

Copy verification and attribution tests cover the corrected first-sale copy surfaces, COA template, and production package SQL manifests.

- Pytest: `24 passed` for `tests/replay/test_nc_first_sale_copy_correction.py`, `tests/replay/test_nc_first_sale_production_package.py`, and `tests/unit/test_product_runtime.py`.
- Ruff: `All checks passed!` for the same Python test files.
