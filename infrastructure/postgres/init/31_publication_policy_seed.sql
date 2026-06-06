-- v0.5.3 Phase 1 / Migration 31.
-- Publication Intelligence policy v1.0.0 draft seed.
--
-- PostgreSQL is authoritative.
-- No Shopify.
-- No Etsy.
-- No Gelato.
-- No Printful.
-- No Lulu.
-- No external IDs.
-- No publication execution.

INSERT INTO publication_policy (
    version, status, authored_by, changelog, max_publication_decision_age_days,
    eligibility_gates, channel_fit_rules, publication_readiness_rules,
    risk_rules, ranking_rules, staleness_rules, provenance
)
VALUES (
    '1.0.0',
    'draft',
    'commerce_migration_31',
    'Initial Publication Intelligence policy.',
    90,
    '{
      "requires_catalog_status": ["draft", "approved"],
      "requires_variant_status": ["draft", "approved"],
      "requires_product_recommendation_status": "curator_approved",
      "requires_rights_snapshot": true,
      "requires_price_snapshot": true
    }'::jsonb,
    '{
      "weights": {"family_allowed": 0.45, "quality_fit": 0.25, "commerce_fit": 0.20, "variant_fit": 0.10}
    }'::jsonb,
    '{
      "weights": {"metadata_complete": 0.25, "rights_confidence": 0.30, "media_ready": 0.20, "price_ready": 0.15, "variant_complete": 0.10}
    }'::jsonb,
    '{
      "weights": {"rights_uncertainty": 0.50, "missing_media": 0.25, "missing_metadata": 0.25},
      "block_if_risk_above": 0.700
    }'::jsonb,
    '{
      "weights": {"readiness_score": 0.45, "channel_fit_score": 0.40, "inverse_risk_score": 0.15},
      "recommend_threshold": 0.750,
      "hold_threshold": 0.500,
      "risk_recommend_max": 0.250,
      "priority_thresholds": {"high": 0.850, "medium": 0.650, "low": 0.000}
    }'::jsonb,
    '{
      "stale_parent_catalog_statuses": ["needs_revision", "blocked", "retired", "superseded"],
      "stale_variant_statuses": ["needs_revision", "blocked", "retired", "superseded"],
      "stale_on_policy_major_change": true,
      "stale_on_rights_snapshot_change": true
    }'::jsonb,
    '{"migration": "31_publication_policy_seed", "authority": "postgresql"}'::jsonb
)
ON CONFLICT (version) DO NOTHING;

INSERT INTO publication_channel_profiles (
    publication_policy_id, profile_key, label, description, status,
    allowed_product_families, required_catalog_status, required_variant_status,
    minimum_rights_confidence, minimum_catalog_quality_score,
    metadata_requirements, risk_tolerance, sort_order, provenance
)
SELECT
    p.id,
    profile.profile_key,
    profile.label,
    profile.description,
    'draft',
    profile.allowed_product_families,
    'draft',
    'draft',
    profile.minimum_rights_confidence,
    profile.minimum_catalog_quality_score,
    profile.metadata_requirements,
    profile.risk_tolerance,
    profile.sort_order,
    '{"migration": "31_publication_policy_seed", "authority": "postgresql"}'::jsonb
FROM publication_policy p
CROSS JOIN (
    VALUES
        ('editorial_catalog', 'Editorial Catalog', 'Internal editorial catalog planning surface.', ARRAY['wall_art','calendar','book','puzzle','card','museum_print','educational','institutional_license']::text[], 0.700::numeric, 0.500::numeric, '{"required_fields": ["title", "description", "price_snapshot"]}'::jsonb, 0.250::numeric, 10),
        ('collection_feature', 'Collection Feature', 'Internal collection feature planning surface.', ARRAY['wall_art','museum_print','calendar','book']::text[], 0.800::numeric, 0.650::numeric, '{"required_fields": ["title", "description", "rights_snapshot"]}'::jsonb, 0.200::numeric, 20),
        ('educational_release', 'Educational Release', 'Internal educational release planning surface.', ARRAY['educational','book','institutional_license']::text[], 0.850::numeric, 0.600::numeric, '{"required_fields": ["title", "description", "price_snapshot"]}'::jsonb, 0.200::numeric, 30)
) AS profile(profile_key, label, description, allowed_product_families, minimum_rights_confidence, minimum_catalog_quality_score, metadata_requirements, risk_tolerance, sort_order)
WHERE p.version = '1.0.0'
ON CONFLICT (publication_policy_id, profile_key) DO NOTHING;
