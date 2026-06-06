-- v0.5.2 Phase 1 / Migration 27.
-- Catalog Intelligence runtime tables.
--
-- PostgreSQL is authoritative.
-- Append-only audit.
-- No Shopify.
-- No Etsy.
-- No Gelato.
-- No Printful.
-- No Lulu.
-- No provider identifiers.
-- No catalog publication.

CREATE TABLE IF NOT EXISTS catalog_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO catalog_status_vocabulary (value, description, sort_order)
VALUES
    ('draft', 'Internal catalog object has been drafted.', 10),
    ('pending_curator_review', 'Internal catalog object awaits curator review.', 20),
    ('approved', 'Internal catalog object has curator approval.', 30),
    ('needs_revision', 'Internal catalog object requires revision.', 40),
    ('blocked', 'Internal catalog object is blocked.', 50),
    ('retired', 'Internal catalog object has been retired.', 60),
    ('superseded', 'Internal catalog object has been superseded.', 70)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS catalog_audit_event_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO catalog_audit_event_type_vocabulary (value, description, sort_order)
VALUES
    ('catalog_candidate_created', 'Catalog candidate created from approved product recommendation.', 10),
    ('catalog_variant_created', 'Catalog variant created from catalog candidate.', 20),
    ('catalog_pricing_applied', 'Catalog pricing profile applied to a variant.', 30),
    ('catalog_replay_verified', 'Catalog replay reproduced identical output.', 40),
    ('catalog_replay_failed', 'Catalog replay detected non-identical output.', 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS catalog_pricing_profiles (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    catalog_policy_id     UUID NOT NULL REFERENCES catalog_policy(id),
    profile_key           TEXT NOT NULL,
    product_family        TEXT NOT NULL REFERENCES product_family_vocabulary(value),
    product_type          TEXT NOT NULL,
    currency              TEXT NOT NULL DEFAULT 'USD',
    base_price_cents      INT NOT NULL CHECK (base_price_cents > 0),
    margin_floor_bps      INT NOT NULL DEFAULT 5000 CHECK (margin_floor_bps BETWEEN 0 AND 10000),
    complexity_multiplier NUMERIC(6,3) NOT NULL DEFAULT 1.000 CHECK (complexity_multiplier > 0),
    prestige_multiplier   NUMERIC(6,3) NOT NULL DEFAULT 1.000 CHECK (prestige_multiplier > 0),
    size_multiplier_rules JSONB NOT NULL DEFAULT '{}',
    rounding_rule         JSONB NOT NULL DEFAULT '{}',
    price_band            TEXT NOT NULL,
    pricing_basis         JSONB NOT NULL DEFAULT '{}',
    status                TEXT NOT NULL DEFAULT 'draft' REFERENCES catalog_status_vocabulary(value),
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (catalog_policy_id, profile_key),
    CONSTRAINT chk_catalog_pricing_profile_basis CHECK (pricing_basis <> '{}'::jsonb),
    CONSTRAINT chk_catalog_pricing_no_provider_identifiers CHECK (
        profile_key !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND product_type !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND size_multiplier_rules::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND pricing_basis::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
    )
);

CREATE TABLE IF NOT EXISTS catalog_candidates (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_recommendation_id  UUID NOT NULL UNIQUE REFERENCES product_recommendations(id),
    commerce_opportunity_id    UUID NOT NULL REFERENCES commerce_opportunities(id),
    opportunity_id             UUID NOT NULL REFERENCES illustration_opportunities(id),
    catalog_policy_id          UUID NOT NULL REFERENCES catalog_policy(id),
    product_family             TEXT NOT NULL REFERENCES product_family_vocabulary(value),
    catalog_title              TEXT NOT NULL,
    catalog_description        TEXT NOT NULL,
    catalog_slug               TEXT NOT NULL UNIQUE,
    catalog_status             TEXT NOT NULL DEFAULT 'draft' REFERENCES catalog_status_vocabulary(value),
    curator_decision           TEXT NOT NULL DEFAULT 'pending' REFERENCES commerce_curator_decision_vocabulary(value),
    curator_reviewed_by        TEXT,
    curator_reviewed_at        TIMESTAMPTZ,
    catalog_basis              JSONB NOT NULL DEFAULT '{}',
    source_snapshot            JSONB NOT NULL DEFAULT '{}',
    media_requirements         JSONB NOT NULL DEFAULT '{}',
    rights_snapshot            JSONB NOT NULL DEFAULT '{}',
    provenance                 JSONB NOT NULL DEFAULT '{}',
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_catalog_candidates_title CHECK (length(catalog_title) > 0),
    CONSTRAINT chk_catalog_candidates_description CHECK (length(catalog_description) > 0),
    CONSTRAINT chk_catalog_candidates_basis CHECK (catalog_basis <> '{}'::jsonb),
    CONSTRAINT chk_catalog_candidates_source_snapshot CHECK (source_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_catalog_candidates_media_requirements CHECK (media_requirements <> '{}'::jsonb),
    CONSTRAINT chk_catalog_candidates_rights_snapshot CHECK (rights_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_catalog_candidates_review_identity CHECK (
        curator_decision = 'pending' OR curator_reviewed_by IS NOT NULL
    ),
    CONSTRAINT chk_catalog_candidates_no_provider_publication CHECK (
        catalog_basis::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
        AND source_snapshot::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
        AND media_requirements::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
        AND provenance::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
    )
);

CREATE TABLE IF NOT EXISTS catalog_variants (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    catalog_candidate_id  UUID NOT NULL REFERENCES catalog_candidates(id),
    catalog_policy_id     UUID NOT NULL REFERENCES catalog_policy(id),
    pricing_profile_id    UUID NOT NULL REFERENCES catalog_pricing_profiles(id),
    variant_key           TEXT NOT NULL,
    variant_title         TEXT NOT NULL,
    product_family        TEXT NOT NULL REFERENCES product_family_vocabulary(value),
    product_type          TEXT NOT NULL,
    variant_options       JSONB NOT NULL DEFAULT '{}',
    surface_spec          JSONB NOT NULL DEFAULT '{}',
    format_spec           JSONB NOT NULL DEFAULT '{}',
    dimension_spec        JSONB NOT NULL DEFAULT '{}',
    asset_requirements    JSONB NOT NULL DEFAULT '{}',
    price_snapshot        JSONB NOT NULL DEFAULT '{}',
    variant_status        TEXT NOT NULL DEFAULT 'draft' REFERENCES catalog_status_vocabulary(value),
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (catalog_candidate_id, variant_key),
    CONSTRAINT chk_catalog_variants_title CHECK (length(variant_title) > 0),
    CONSTRAINT chk_catalog_variants_options CHECK (variant_options <> '{}'::jsonb),
    CONSTRAINT chk_catalog_variants_surface CHECK (surface_spec <> '{}'::jsonb),
    CONSTRAINT chk_catalog_variants_format CHECK (format_spec <> '{}'::jsonb),
    CONSTRAINT chk_catalog_variants_dimensions CHECK (dimension_spec <> '{}'::jsonb),
    CONSTRAINT chk_catalog_variants_assets CHECK (asset_requirements <> '{}'::jsonb),
    CONSTRAINT chk_catalog_variants_price CHECK (price_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_catalog_variants_no_provider_identifiers CHECK (
        variant_key !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND product_type !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND variant_options::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND surface_spec::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND format_spec::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND dimension_spec::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND asset_requirements::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND price_snapshot::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
        AND provenance::text !~* '(shopify|etsy|gelato|printful|lulu|provider|sku|external)'
    )
);

CREATE TABLE IF NOT EXISTS catalog_audit_log (
    id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_recommendation_id UUID REFERENCES product_recommendations(id),
    catalog_candidate_id      UUID REFERENCES catalog_candidates(id),
    catalog_variant_id        UUID REFERENCES catalog_variants(id),
    catalog_policy_id         UUID NOT NULL REFERENCES catalog_policy(id),
    event_type                TEXT NOT NULL REFERENCES catalog_audit_event_type_vocabulary(value),
    event_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_type                TEXT NOT NULL REFERENCES commerce_actor_type_vocabulary(value),
    actor_id                  TEXT NOT NULL,
    trigger                   TEXT NOT NULL REFERENCES commerce_computation_trigger_vocabulary(value),
    input_snapshot            JSONB NOT NULL DEFAULT '{}',
    output_snapshot           JSONB NOT NULL DEFAULT '{}',
    previous_state            JSONB NOT NULL DEFAULT '{}',
    new_state                 JSONB NOT NULL DEFAULT '{}',
    entry_checksum_sha256     TEXT NOT NULL,
    previous_entry_checksum   TEXT,
    reason                    TEXT NOT NULL,
    generated_by              TEXT NOT NULL,
    created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_catalog_audit_log_target CHECK (
        product_recommendation_id IS NOT NULL
        OR catalog_candidate_id IS NOT NULL
        OR catalog_variant_id IS NOT NULL
    ),
    CONSTRAINT chk_catalog_audit_log_entry_checksum CHECK (
        entry_checksum_sha256 ~ '^[0-9a-f]{64}$'
    ),
    CONSTRAINT chk_catalog_audit_log_previous_checksum CHECK (
        previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
    ),
    CONSTRAINT chk_catalog_audit_log_distinct_checksum CHECK (
        previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
    ),
    CONSTRAINT chk_catalog_audit_log_actor_id CHECK (length(actor_id) > 0),
    CONSTRAINT chk_catalog_audit_log_reason CHECK (length(reason) > 0),
    CONSTRAINT chk_catalog_audit_log_generated_by CHECK (length(generated_by) > 0)
);

CREATE INDEX IF NOT EXISTS idx_catalog_pricing_profiles_policy
    ON catalog_pricing_profiles(catalog_policy_id, product_family, product_type);

CREATE INDEX IF NOT EXISTS idx_catalog_candidates_policy_status
    ON catalog_candidates(catalog_policy_id, catalog_status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_catalog_candidates_recommendation
    ON catalog_candidates(product_recommendation_id);

CREATE INDEX IF NOT EXISTS idx_catalog_variants_candidate
    ON catalog_variants(catalog_candidate_id, variant_key);

CREATE INDEX IF NOT EXISTS idx_catalog_variants_policy
    ON catalog_variants(catalog_policy_id, product_family, product_type);

CREATE INDEX IF NOT EXISTS idx_catalog_audit_log_candidate_event
    ON catalog_audit_log(catalog_candidate_id, event_at DESC);

CREATE INDEX IF NOT EXISTS idx_catalog_audit_log_variant_event
    ON catalog_audit_log(catalog_variant_id, event_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_catalog_audit_log_checksum_target
    ON catalog_audit_log(entry_checksum_sha256);

DROP TRIGGER IF EXISTS trg_catalog_pricing_profiles_updated_at ON catalog_pricing_profiles;
CREATE TRIGGER trg_catalog_pricing_profiles_updated_at
    BEFORE UPDATE ON catalog_pricing_profiles
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_catalog_candidates_updated_at ON catalog_candidates;
CREATE TRIGGER trg_catalog_candidates_updated_at
    BEFORE UPDATE ON catalog_candidates
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_catalog_variants_updated_at ON catalog_variants;
CREATE TRIGGER trg_catalog_variants_updated_at
    BEFORE UPDATE ON catalog_variants
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_catalog_candidate_parent_approved()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM product_recommendations pr
          JOIN commerce_opportunities co ON co.id = pr.commerce_opportunity_id
         WHERE pr.id = NEW.product_recommendation_id
           AND pr.commerce_opportunity_id = NEW.commerce_opportunity_id
           AND pr.opportunity_id = NEW.opportunity_id
           AND pr.recommended_product_family = NEW.product_family
           AND pr.status = 'curator_approved'
           AND co.curator_decision = 'approved'
           AND co.hard_gate_status = 'passed'
           AND co.policy_stale = FALSE
           AND co.commerce_tier <> 'blocked'
    )
    THEN
        RAISE EXCEPTION 'catalog candidate requires curator-approved product recommendation and approved current commerce opportunity';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_catalog_candidate_parent_approved ON catalog_candidates;
CREATE CONSTRAINT TRIGGER trg_catalog_candidate_parent_approved
    AFTER INSERT OR UPDATE OF
        product_recommendation_id,
        commerce_opportunity_id,
        opportunity_id,
        product_family
    ON catalog_candidates
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_catalog_candidate_parent_approved();

CREATE OR REPLACE FUNCTION enforce_catalog_variant_parent_consistency()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM catalog_candidates cc
         WHERE cc.id = NEW.catalog_candidate_id
           AND cc.catalog_policy_id = NEW.catalog_policy_id
           AND cc.product_family = NEW.product_family
    )
    THEN
        RAISE EXCEPTION 'catalog variant must match candidate policy and product family';
    END IF;

    IF NOT EXISTS (
        SELECT 1
          FROM catalog_pricing_profiles cpp
         WHERE cpp.id = NEW.pricing_profile_id
           AND cpp.catalog_policy_id = NEW.catalog_policy_id
           AND cpp.product_family = NEW.product_family
           AND cpp.product_type = NEW.product_type
    )
    THEN
        RAISE EXCEPTION 'catalog variant must reference matching pricing profile';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_catalog_variant_parent_consistency ON catalog_variants;
CREATE CONSTRAINT TRIGGER trg_catalog_variant_parent_consistency
    AFTER INSERT OR UPDATE OF
        catalog_candidate_id,
        catalog_policy_id,
        pricing_profile_id,
        product_family,
        product_type
    ON catalog_variants
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_catalog_variant_parent_consistency();

CREATE OR REPLACE RULE catalog_audit_log_no_update AS
    ON UPDATE TO catalog_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no UPDATE permitted on catalog_audit_log');

CREATE OR REPLACE RULE catalog_audit_log_no_delete AS
    ON DELETE TO catalog_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no DELETE permitted on catalog_audit_log');

CREATE OR REPLACE FUNCTION enforce_catalog_audit_hash_chain()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
    latest_checksum TEXT;
BEGIN
    SELECT cal.entry_checksum_sha256
      INTO latest_checksum
      FROM catalog_audit_log cal
     WHERE COALESCE(cal.product_recommendation_id, cal.catalog_candidate_id, cal.catalog_variant_id)
           IS NOT DISTINCT FROM COALESCE(NEW.product_recommendation_id, NEW.catalog_candidate_id, NEW.catalog_variant_id)
     ORDER BY event_at DESC, created_at DESC, id DESC
     LIMIT 1;

    IF latest_checksum IS NULL THEN
        IF NEW.previous_entry_checksum IS NOT NULL THEN
            RAISE EXCEPTION 'first catalog_audit_log entry for target must have null previous_entry_checksum';
        END IF;
    ELSIF NEW.previous_entry_checksum IS DISTINCT FROM latest_checksum THEN
        RAISE EXCEPTION 'previous_entry_checksum must match latest catalog_audit_log entry for target';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_catalog_audit_hash_chain ON catalog_audit_log;
CREATE TRIGGER trg_catalog_audit_hash_chain
    BEFORE INSERT ON catalog_audit_log
    FOR EACH ROW EXECUTE FUNCTION enforce_catalog_audit_hash_chain();
