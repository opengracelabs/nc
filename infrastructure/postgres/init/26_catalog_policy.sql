-- v0.5.2 Phase 1 / Migration 26.
-- Catalog Intelligence policy authority.
--
-- PostgreSQL is authoritative.
-- No Shopify.
-- No Etsy.
-- No Gelato.
-- No Printful.
-- No Lulu.
-- No provider identifiers.
-- No catalog publication.

CREATE TABLE IF NOT EXISTS catalog_policy (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version              TEXT NOT NULL UNIQUE,
    status               TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value),
    effective_from       TIMESTAMPTZ,
    effective_until      TIMESTAMPTZ,
    authored_by          TEXT NOT NULL,
    approved_by          TEXT,
    approved_at          TIMESTAMPTZ,
    changelog            TEXT NOT NULL,
    previous_version_id  UUID REFERENCES catalog_policy(id),
    max_catalog_age_days INT NOT NULL DEFAULT 90 CHECK (max_catalog_age_days > 0),

    catalog_rules        JSONB NOT NULL,
    variant_rules        JSONB NOT NULL,
    pricing_rules        JSONB NOT NULL,
    eligibility_gates    JSONB NOT NULL,

    provenance           JSONB NOT NULL DEFAULT '{}',
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_catalog_policy_approval_identity CHECK (
        approved_by IS NULL OR approved_by IS DISTINCT FROM authored_by
    ),
    CONSTRAINT chk_catalog_policy_approved_status CHECK (
        status NOT IN ('active','paused','superseded')
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)
    ),
    CONSTRAINT chk_catalog_policy_effective_window CHECK (
        effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from
    ),
    CONSTRAINT chk_catalog_policy_no_channels_providers CHECK (
        catalog_rules::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
        AND variant_rules::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
        AND pricing_rules::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
        AND eligibility_gates::text !~* '(shopify|etsy|gelato|printful|lulu|provider|publication|external_product_id|external_variant_id)'
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_catalog_policy_one_active
    ON catalog_policy((status))
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_catalog_policy_status
    ON catalog_policy(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_catalog_policy_previous_version
    ON catalog_policy(previous_version_id)
    WHERE previous_version_id IS NOT NULL;

DROP TRIGGER IF EXISTS trg_catalog_policy_updated_at ON catalog_policy;
CREATE TRIGGER trg_catalog_policy_updated_at
    BEFORE UPDATE ON catalog_policy
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_catalog_policy_immutability()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.status IN ('active','paused','superseded') THEN
        IF NEW.version IS DISTINCT FROM OLD.version
           OR NEW.authored_by IS DISTINCT FROM OLD.authored_by
           OR NEW.catalog_rules IS DISTINCT FROM OLD.catalog_rules
           OR NEW.variant_rules IS DISTINCT FROM OLD.variant_rules
           OR NEW.pricing_rules IS DISTINCT FROM OLD.pricing_rules
           OR NEW.eligibility_gates IS DISTINCT FROM OLD.eligibility_gates
           OR NEW.max_catalog_age_days IS DISTINCT FROM OLD.max_catalog_age_days
        THEN
            RAISE EXCEPTION 'catalog_policy % is immutable after active, paused, or superseded status',
                OLD.id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_catalog_policy_immutability ON catalog_policy;
CREATE TRIGGER trg_catalog_policy_immutability
    BEFORE UPDATE ON catalog_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_catalog_policy_immutability();

CREATE OR REPLACE FUNCTION enforce_catalog_policy_activation()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.status = 'active' THEN
        IF NEW.approved_by IS NULL OR NEW.approved_at IS NULL THEN
            RAISE EXCEPTION 'active catalog_policy requires approved_by and approved_at';
        END IF;
        IF NEW.approved_by IS NOT DISTINCT FROM NEW.authored_by THEN
            RAISE EXCEPTION 'active catalog_policy requires second-human approval';
        END IF;
        IF NEW.effective_from IS NULL THEN
            RAISE EXCEPTION 'active catalog_policy requires effective_from';
        END IF;
        IF EXISTS (
            SELECT 1
            FROM catalog_policy p
            WHERE p.status = 'active'
              AND p.id IS DISTINCT FROM NEW.id
        ) THEN
            RAISE EXCEPTION 'only one catalog_policy may be active';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_catalog_policy_activation ON catalog_policy;
CREATE TRIGGER trg_catalog_policy_activation
    BEFORE INSERT OR UPDATE ON catalog_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_catalog_policy_activation();
