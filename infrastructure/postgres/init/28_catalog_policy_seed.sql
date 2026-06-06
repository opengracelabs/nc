-- v0.5.2 Phase 1 / Migration 28.
-- Catalog Intelligence policy v1.0.0 draft seed.
--
-- PostgreSQL is authoritative.
-- No Shopify.
-- No Etsy.
-- No Gelato.
-- No Printful.
-- No Lulu.
-- No provider identifiers.
-- No catalog publication.

INSERT INTO catalog_policy (
    version,
    status,
    authored_by,
    changelog,
    max_catalog_age_days,
    catalog_rules,
    variant_rules,
    pricing_rules,
    eligibility_gates,
    provenance
)
VALUES (
    '1.0.0',
    'draft',
    'commerce_migration_28',
    'Initial Catalog Intelligence policy.',
    90,
    '{
      "slug_version": "catalog_slug_v1",
      "title_template": "{asset_title} - {product_family_label}",
      "description_template": "Internal catalog candidate generated from {source_title}.",
      "media_requirements_by_family": {
        "wall_art": {"min_width_px": 2000, "required_assets": ["source_image"]},
        "calendar": {"min_width_px": 2000, "required_assets": ["source_image"]},
        "book": {"min_width_px": 1200, "required_assets": ["source_image"]},
        "puzzle": {"min_width_px": 2000, "required_assets": ["source_image"]},
        "card": {"min_width_px": 1200, "required_assets": ["source_image"]},
        "museum_print": {"min_width_px": 4000, "required_assets": ["source_image"]},
        "educational": {"min_width_px": 1200, "required_assets": ["source_image"]},
        "institutional_license": {"min_width_px": 1200, "required_assets": ["source_image"]}
      }
    }'::jsonb,
    '{
      "wall_art": [
        {"variant_key": "standard_print_12x16", "product_type": "standard_print", "title_suffix": "12 x 16", "dimensions": {"width_in": 12, "height_in": 16}},
        {"variant_key": "standard_print_18x24", "product_type": "standard_print", "title_suffix": "18 x 24", "dimensions": {"width_in": 18, "height_in": 24}}
      ],
      "museum_print": [
        {"variant_key": "archival_print_16x20", "product_type": "archival_print", "title_suffix": "16 x 20", "dimensions": {"width_in": 16, "height_in": 20}},
        {"variant_key": "archival_print_24x36", "product_type": "archival_print", "title_suffix": "24 x 36", "dimensions": {"width_in": 24, "height_in": 36}}
      ],
      "calendar": [
        {"variant_key": "wall_calendar_annual", "product_type": "calendar", "title_suffix": "Annual Wall Calendar", "dimensions": {"width_in": 11, "height_in": 17}}
      ],
      "book": [
        {"variant_key": "book_illustration_plate", "product_type": "book_illustration", "title_suffix": "Book Plate", "dimensions": {"width_in": 8, "height_in": 10}}
      ],
      "puzzle": [
        {"variant_key": "puzzle_500_piece", "product_type": "puzzle", "title_suffix": "500 Piece", "dimensions": {"width_in": 18, "height_in": 24}}
      ],
      "card": [
        {"variant_key": "folded_card_single", "product_type": "card", "title_suffix": "Folded Card", "dimensions": {"width_in": 5, "height_in": 7}}
      ],
      "educational": [
        {"variant_key": "education_license_standard", "product_type": "education_license", "title_suffix": "Education License", "dimensions": {"digital": true}}
      ],
      "institutional_license": [
        {"variant_key": "institutional_license_standard", "product_type": "institutional_license", "title_suffix": "Institutional License", "dimensions": {"digital": true}}
      ]
    }'::jsonb,
    '{
      "currency": "USD",
      "rounding": {"nearest_cents": 100, "minus_cents": 1},
      "profiles": {
        "standard_print": {"base_price_cents": 3200, "margin_floor_bps": 5500, "price_band": "standard"},
        "archival_print": {"base_price_cents": 8500, "margin_floor_bps": 6500, "price_band": "premium"},
        "calendar": {"base_price_cents": 2800, "margin_floor_bps": 5000, "price_band": "standard"},
        "book_illustration": {"base_price_cents": 2400, "margin_floor_bps": 5000, "price_band": "standard"},
        "puzzle": {"base_price_cents": 3600, "margin_floor_bps": 5500, "price_band": "standard"},
        "card": {"base_price_cents": 700, "margin_floor_bps": 4500, "price_band": "entry"},
        "education_license": {"base_price_cents": 12000, "margin_floor_bps": 7000, "price_band": "license"},
        "institutional_license": {"base_price_cents": 25000, "margin_floor_bps": 7500, "price_band": "license"}
      }
    }'::jsonb,
    '{
      "requires_product_recommendation_status": "curator_approved",
      "requires_commerce_opportunity": {
        "curator_decision": "approved",
        "hard_gate_status": "passed",
        "policy_stale": false,
        "commerce_tier_not": "blocked"
      },
      "requires_rights_snapshot": true
    }'::jsonb,
    '{
      "migration": "28_catalog_policy_seed",
      "authority": "postgresql"
    }'::jsonb
)
ON CONFLICT (version) DO NOTHING;
