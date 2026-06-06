-- v0.5.1 Phase 1 / Migration 24.
-- Product routing policy authority.
--
-- PostgreSQL is authoritative.
-- No catalog generation.
-- No provider integration.

CREATE TABLE IF NOT EXISTS product_routing_policy (
    id                           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version                      TEXT NOT NULL UNIQUE,
    status                       TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value),
    effective_from               TIMESTAMPTZ,
    effective_until              TIMESTAMPTZ,
    authored_by                  TEXT NOT NULL,
    approved_by                  TEXT,
    approved_at                  TIMESTAMPTZ,
    changelog                    TEXT NOT NULL,
    previous_version_id          UUID REFERENCES product_routing_policy(id),
    max_route_age_days           INT NOT NULL DEFAULT 90 CHECK (max_route_age_days > 0),

    product_surface_requirements JSONB NOT NULL,
    routing_formula_spec         JSONB NOT NULL,
    family_caps                  JSONB NOT NULL DEFAULT '{}',
    curator_gate_spec            JSONB NOT NULL DEFAULT '{}',

    provenance                   JSONB NOT NULL DEFAULT '{}',
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_product_routing_policy_approval_identity CHECK (
        approved_by IS NULL OR approved_by IS DISTINCT FROM authored_by
    ),
    CONSTRAINT chk_product_routing_policy_approved_status CHECK (
        status NOT IN ('active','paused','superseded')
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)
    ),
    CONSTRAINT chk_product_routing_policy_effective_window CHECK (
        effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from
    ),
    CONSTRAINT chk_product_routing_policy_no_catalog_provider CHECK (
        product_surface_requirements::text !~* '(catalog|provider)'
        AND routing_formula_spec::text !~* '(catalog|provider)'
        AND family_caps::text !~* '(catalog|provider)'
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_product_routing_policy_one_active
    ON product_routing_policy((status))
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_product_routing_policy_status
    ON product_routing_policy(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_product_routing_policy_previous_version
    ON product_routing_policy(previous_version_id)
    WHERE previous_version_id IS NOT NULL;

DROP TRIGGER IF EXISTS trg_product_routing_policy_updated_at ON product_routing_policy;
CREATE TRIGGER trg_product_routing_policy_updated_at
    BEFORE UPDATE ON product_routing_policy
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_product_routing_policy_immutability()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.status IN ('active','paused','superseded') THEN
        IF NEW.version IS DISTINCT FROM OLD.version
           OR NEW.authored_by IS DISTINCT FROM OLD.authored_by
           OR NEW.product_surface_requirements IS DISTINCT FROM OLD.product_surface_requirements
           OR NEW.routing_formula_spec IS DISTINCT FROM OLD.routing_formula_spec
           OR NEW.family_caps IS DISTINCT FROM OLD.family_caps
           OR NEW.curator_gate_spec IS DISTINCT FROM OLD.curator_gate_spec
           OR NEW.max_route_age_days IS DISTINCT FROM OLD.max_route_age_days
        THEN
            RAISE EXCEPTION 'product_routing_policy % is immutable after active, paused, or superseded status',
                OLD.id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_product_routing_policy_immutability ON product_routing_policy;
CREATE TRIGGER trg_product_routing_policy_immutability
    BEFORE UPDATE ON product_routing_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_product_routing_policy_immutability();

CREATE OR REPLACE FUNCTION enforce_product_routing_policy_activation()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.status = 'active' THEN
        IF NEW.approved_by IS NULL OR NEW.approved_at IS NULL THEN
            RAISE EXCEPTION 'active product_routing_policy requires approved_by and approved_at';
        END IF;
        IF NEW.approved_by IS NOT DISTINCT FROM NEW.authored_by THEN
            RAISE EXCEPTION 'active product_routing_policy requires second-human approval';
        END IF;
        IF NEW.effective_from IS NULL THEN
            RAISE EXCEPTION 'active product_routing_policy requires effective_from';
        END IF;
        IF EXISTS (
            SELECT 1
            FROM product_routing_policy p
            WHERE p.status = 'active'
              AND p.id IS DISTINCT FROM NEW.id
        ) THEN
            RAISE EXCEPTION 'only one product_routing_policy may be active';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_product_routing_policy_activation ON product_routing_policy;
CREATE TRIGGER trg_product_routing_policy_activation
    BEFORE INSERT OR UPDATE ON product_routing_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_product_routing_policy_activation();

INSERT INTO product_routing_policy (
    version,
    status,
    authored_by,
    changelog,
    max_route_age_days,
    product_surface_requirements,
    routing_formula_spec,
    family_caps,
    curator_gate_spec,
    provenance
)
VALUES (
    '1.0.0',
    'draft',
    'commerce_migration_24',
    'Initial Product Routing policy.',
    90,
    '{
      "wall_art": {
        "required_flags": ["eligible_wall_art_standard"],
        "min_cos": 0.65,
        "min_image_width_px": 2000,
        "min_quality_score": 0.55,
        "basis_model": "retail_score",
        "recommended_product_types": ["standard_print"]
      },
      "calendar": {
        "required_flags": ["eligible_calendar"],
        "min_cos": 0.65,
        "min_composition_fit": 0.60,
        "basis_model": "tourism_score",
        "recommended_product_types": ["calendar"]
      },
      "book": {
        "required_flags": ["eligible_book_illustration"],
        "min_publishing_score": 0.70,
        "min_identification_confidence": 0.85,
        "basis_model": "publishing_score",
        "recommended_product_types": ["book_illustration"]
      },
      "puzzle": {
        "required_flags": ["eligible_puzzle"],
        "min_cos": 0.60,
        "min_composition_fit": 0.65,
        "basis_model": "retail_score",
        "recommended_product_types": ["puzzle"]
      },
      "card": {
        "required_flags": ["eligible_card"],
        "min_cos": 0.55,
        "min_image_width_px": 1200,
        "min_quality_score": 0.50,
        "basis_model": "retail_score",
        "recommended_product_types": ["card"]
      },
      "museum_print": {
        "required_flags": ["eligible_museum_print"],
        "min_museum_score": 0.80,
        "basis_model": "museum_score",
        "recommended_product_types": ["archival_print"]
      },
      "educational": {
        "required_flags": ["eligible_educational"],
        "min_reference_score": 0.65,
        "basis_model": "reference_score",
        "recommended_product_types": ["education_license"]
      },
      "institutional_license": {
        "required_flags": ["eligible_institutional_license"],
        "min_museum_score": 0.80,
        "basis_model": "museum_score",
        "recommended_product_types": ["institutional_license"]
      }
    }'::jsonb,
    '{
      "version": "1.0.0",
      "routing_scorer_version": "product_routing_weighted_threshold_v1",
      "status_on_create": "pending_curator_review",
      "rounding": "3_decimal_places",
      "confidence_weights": {
        "commerce_opportunity_score": 0.45,
        "basis_model_score": 0.35,
        "csm_score": 0.20
      }
    }'::jsonb,
    '{
      "max_recommendations_per_opportunity": 8
    }'::jsonb,
    '{
      "requires_commerce_opportunity": {
        "curator_decision": "approved",
        "hard_gate_status": "passed",
        "policy_stale": false,
        "commerce_tier_not": "blocked"
      }
    }'::jsonb,
    '{
      "migration": "24_product_routing_policy",
      "authority": "postgresql"
    }'::jsonb
)
ON CONFLICT (version) DO NOTHING;
