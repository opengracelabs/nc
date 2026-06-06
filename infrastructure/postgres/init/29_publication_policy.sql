-- v0.5.3 Phase 1 / Migration 29.
-- Publication Intelligence policy authority.
--
-- PostgreSQL is authoritative.
-- No Shopify.
-- No Etsy.
-- No Gelato.
-- No Printful.
-- No Lulu.
-- No external IDs.
-- No publication execution.

CREATE TABLE IF NOT EXISTS publication_policy (
    id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version                         TEXT NOT NULL UNIQUE,
    status                          TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value),
    effective_from                  TIMESTAMPTZ,
    effective_until                 TIMESTAMPTZ,
    authored_by                     TEXT NOT NULL,
    approved_by                     TEXT,
    approved_at                     TIMESTAMPTZ,
    changelog                       TEXT NOT NULL,
    previous_version_id             UUID REFERENCES publication_policy(id),
    max_publication_decision_age_days INT NOT NULL DEFAULT 90 CHECK (max_publication_decision_age_days > 0),

    eligibility_gates               JSONB NOT NULL,
    channel_fit_rules               JSONB NOT NULL,
    publication_readiness_rules     JSONB NOT NULL,
    risk_rules                      JSONB NOT NULL,
    ranking_rules                   JSONB NOT NULL,
    staleness_rules                 JSONB NOT NULL,

    provenance                      JSONB NOT NULL DEFAULT '{}',
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_publication_policy_approval_identity CHECK (
        approved_by IS NULL OR approved_by IS DISTINCT FROM authored_by
    ),
    CONSTRAINT chk_publication_policy_approved_status CHECK (
        status NOT IN ('active','paused','superseded')
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)
    ),
    CONSTRAINT chk_publication_policy_effective_window CHECK (
        effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from
    ),
    CONSTRAINT chk_publication_policy_no_external_execution CHECK (
        eligibility_gates::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND channel_fit_rules::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND publication_readiness_rules::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND risk_rules::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND ranking_rules::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND staleness_rules::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_publication_policy_one_active
    ON publication_policy((status))
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_publication_policy_status
    ON publication_policy(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_publication_policy_previous_version
    ON publication_policy(previous_version_id)
    WHERE previous_version_id IS NOT NULL;

DROP TRIGGER IF EXISTS trg_publication_policy_updated_at ON publication_policy;
CREATE TRIGGER trg_publication_policy_updated_at
    BEFORE UPDATE ON publication_policy
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_publication_policy_immutability()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.status IN ('active','paused','superseded') THEN
        IF NEW.version IS DISTINCT FROM OLD.version
           OR NEW.authored_by IS DISTINCT FROM OLD.authored_by
           OR NEW.eligibility_gates IS DISTINCT FROM OLD.eligibility_gates
           OR NEW.channel_fit_rules IS DISTINCT FROM OLD.channel_fit_rules
           OR NEW.publication_readiness_rules IS DISTINCT FROM OLD.publication_readiness_rules
           OR NEW.risk_rules IS DISTINCT FROM OLD.risk_rules
           OR NEW.ranking_rules IS DISTINCT FROM OLD.ranking_rules
           OR NEW.staleness_rules IS DISTINCT FROM OLD.staleness_rules
           OR NEW.max_publication_decision_age_days IS DISTINCT FROM OLD.max_publication_decision_age_days
        THEN
            RAISE EXCEPTION 'publication_policy % is immutable after active, paused, or superseded status', OLD.id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_publication_policy_immutability ON publication_policy;
CREATE TRIGGER trg_publication_policy_immutability
    BEFORE UPDATE ON publication_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_publication_policy_immutability();

CREATE OR REPLACE FUNCTION enforce_publication_policy_activation()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.status = 'active' THEN
        IF NEW.approved_by IS NULL OR NEW.approved_at IS NULL THEN
            RAISE EXCEPTION 'active publication_policy requires approved_by and approved_at';
        END IF;
        IF NEW.approved_by IS NOT DISTINCT FROM NEW.authored_by THEN
            RAISE EXCEPTION 'active publication_policy requires second-human approval';
        END IF;
        IF NEW.effective_from IS NULL THEN
            RAISE EXCEPTION 'active publication_policy requires effective_from';
        END IF;
        IF EXISTS (
            SELECT 1 FROM publication_policy p
            WHERE p.status = 'active' AND p.id IS DISTINCT FROM NEW.id
        ) THEN
            RAISE EXCEPTION 'only one publication_policy may be active';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_publication_policy_activation ON publication_policy;
CREATE TRIGGER trg_publication_policy_activation
    BEFORE INSERT OR UPDATE ON publication_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_publication_policy_activation();
