-- v0.5.0 Phase 2 / Migration 23.
-- Commerce Intelligence recommendation runtime tables.
--
-- PostgreSQL is authoritative.
-- No scoring worker activation.
-- No product generation.
-- No Shopify integration.
-- No Etsy integration.

-- CV-7 governed product family vocabulary.
CREATE TABLE IF NOT EXISTS product_family_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO product_family_vocabulary (value, description, sort_order)
VALUES
    ('wall_art', 'Wall art and standard print products.', 10),
    ('calendar', 'Calendar products.', 20),
    ('book', 'Book and publication products.', 30),
    ('puzzle', 'Puzzle products.', 40),
    ('card', 'Greeting card and stationery products.', 50),
    ('museum_print', 'Museum-quality print products.', 60),
    ('educational', 'Educational and reference products.', 70),
    ('home_decor', 'Home decor products.', 80),
    ('fashion', 'Fashion and apparel products.', 90),
    ('institutional_license', 'Institutional licensing products.', 100)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

-- CV-8 downstream recommendation status values. No product generation is activated here.
INSERT INTO commerce_recommendation_status_vocabulary (value, description, sort_order)
VALUES
    ('generated', 'Recommendation has been handed to a downstream generation process.', 60),
    ('converted_to_collection', 'Recommendation has been converted to a collection planning record.', 70)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS product_recommendations (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id              UUID NOT NULL REFERENCES illustration_opportunities(id),
    commerce_opportunity_id     UUID NOT NULL REFERENCES commerce_opportunities(id),
    policy_version_id           UUID NOT NULL REFERENCES commerce_policy(id),
    recommended_product_family  TEXT NOT NULL REFERENCES product_family_vocabulary(value),
    recommended_product_types   JSONB NOT NULL DEFAULT '{}',
    recommended_providers       JSONB NOT NULL DEFAULT '{}',
    recommendation_confidence   NUMERIC(4,3),
    recommendation_basis        JSONB NOT NULL DEFAULT '{}',
    status                      TEXT NOT NULL DEFAULT 'pending_curator_review'
                                    REFERENCES commerce_recommendation_status_vocabulary(value),
    curator_reviewed_by         TEXT,
    curator_reviewed_at         TIMESTAMPTZ,
    curator_decision_notes      TEXT,
    provenance                  JSONB NOT NULL DEFAULT '{}',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (opportunity_id, recommended_product_family),
    CONSTRAINT chk_product_recommendations_confidence CHECK (
        recommendation_confidence IS NULL OR recommendation_confidence BETWEEN 0 AND 1
    ),
    CONSTRAINT chk_product_recommendations_basis CHECK (
        recommendation_basis <> '{}'::jsonb
    ),
    CONSTRAINT chk_product_recommendations_review_identity CHECK (
        status = 'pending_curator_review' OR curator_reviewed_by IS NOT NULL
    )
);

CREATE INDEX IF NOT EXISTS idx_product_recommendations_opportunity
    ON product_recommendations(opportunity_id);

CREATE INDEX IF NOT EXISTS idx_product_recommendations_commerce_opportunity
    ON product_recommendations(commerce_opportunity_id);

CREATE INDEX IF NOT EXISTS idx_product_recommendations_policy
    ON product_recommendations(policy_version_id);

CREATE INDEX IF NOT EXISTS idx_product_recommendations_status
    ON product_recommendations(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_product_recommendations_family_confidence
    ON product_recommendations(recommended_product_family, recommendation_confidence DESC);

DROP TRIGGER IF EXISTS trg_product_recommendations_updated_at ON product_recommendations;
CREATE TRIGGER trg_product_recommendations_updated_at
    BEFORE UPDATE ON product_recommendations
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_product_recommendation_parent_approved()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM commerce_opportunities co
         WHERE co.id = NEW.commerce_opportunity_id
           AND co.opportunity_id = NEW.opportunity_id
           AND co.policy_version_id = NEW.policy_version_id
           AND co.curator_decision = 'approved'
           AND co.hard_gate_status = 'passed'
           AND co.policy_stale = FALSE
           AND co.commerce_tier <> 'blocked'
    )
    THEN
        RAISE EXCEPTION 'product recommendation requires an approved, current, unblocked commerce opportunity';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_product_recommendations_parent_approved ON product_recommendations;
CREATE CONSTRAINT TRIGGER trg_product_recommendations_parent_approved
    AFTER INSERT OR UPDATE OF
        opportunity_id,
        commerce_opportunity_id,
        policy_version_id
    ON product_recommendations
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_product_recommendation_parent_approved();

CREATE OR REPLACE FUNCTION enforce_product_recommendation_gate_5()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status
       AND NEW.status IN ('assigned','generated','converted_to_collection')
       AND NOT EXISTS (
           SELECT 1
             FROM commerce_opportunities co
            WHERE co.id = NEW.commerce_opportunity_id
              AND co.curator_decision = 'approved'
       )
    THEN
        RAISE EXCEPTION 'curator_decision = approved before recommendation status transition to %',
            NEW.status;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_product_recommendations_gate_5 ON product_recommendations;
CREATE TRIGGER trg_product_recommendations_gate_5
    BEFORE UPDATE OF status ON product_recommendations
    FOR EACH ROW EXECUTE FUNCTION enforce_product_recommendation_gate_5();

CREATE TABLE IF NOT EXISTS collection_recommendations (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id              UUID NOT NULL REFERENCES illustration_opportunities(id),
    commerce_opportunity_id     UUID NOT NULL REFERENCES commerce_opportunities(id),
    policy_version_id           UUID NOT NULL REFERENCES commerce_policy(id),
    recommended_collection_id   UUID REFERENCES collections(id),
    new_collection_proposal     JSONB NOT NULL DEFAULT '{}',
    fit_score                   NUMERIC(4,3) NOT NULL,
    fit_basis                   JSONB NOT NULL DEFAULT '{}',
    collection_gap_type         TEXT NOT NULL DEFAULT 'none'
                                    REFERENCES commerce_collection_gap_type_vocabulary(value),
    status                      TEXT NOT NULL DEFAULT 'pending_curator_review'
                                    REFERENCES commerce_recommendation_status_vocabulary(value),
    curator_reviewed_by         TEXT,
    curator_reviewed_at         TIMESTAMPTZ,
    curator_decision_notes      TEXT,
    provenance                  JSONB NOT NULL DEFAULT '{}',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_collection_recommendations_target CHECK (
        recommended_collection_id IS NOT NULL OR new_collection_proposal <> '{}'::jsonb
    ),
    CONSTRAINT chk_collection_recommendations_fit_score CHECK (
        fit_score BETWEEN 0 AND 1
    ),
    CONSTRAINT chk_collection_recommendations_fit_basis CHECK (
        fit_basis <> '{}'::jsonb
    ),
    CONSTRAINT chk_collection_recommendations_review_identity CHECK (
        status = 'pending_curator_review' OR curator_reviewed_by IS NOT NULL
    )
);

CREATE INDEX IF NOT EXISTS idx_collection_recommendations_opportunity
    ON collection_recommendations(opportunity_id);

CREATE INDEX IF NOT EXISTS idx_collection_recommendations_commerce_opportunity
    ON collection_recommendations(commerce_opportunity_id);

CREATE INDEX IF NOT EXISTS idx_collection_recommendations_policy
    ON collection_recommendations(policy_version_id);

CREATE INDEX IF NOT EXISTS idx_collection_recommendations_status
    ON collection_recommendations(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_collection_recommendations_gap_fit
    ON collection_recommendations(collection_gap_type, fit_score DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_collection_recommendations_existing_target
    ON collection_recommendations(opportunity_id, recommended_collection_id)
    WHERE recommended_collection_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uniq_collection_recommendations_new_proposal
    ON collection_recommendations(opportunity_id, (md5(new_collection_proposal::text)))
    WHERE recommended_collection_id IS NULL;

DROP TRIGGER IF EXISTS trg_collection_recommendations_updated_at ON collection_recommendations;
CREATE TRIGGER trg_collection_recommendations_updated_at
    BEFORE UPDATE ON collection_recommendations
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_collection_recommendation_parent_approved()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM commerce_opportunities co
         WHERE co.id = NEW.commerce_opportunity_id
           AND co.opportunity_id = NEW.opportunity_id
           AND co.policy_version_id = NEW.policy_version_id
           AND co.curator_decision = 'approved'
           AND co.hard_gate_status = 'passed'
           AND co.policy_stale = FALSE
           AND co.commerce_tier <> 'blocked'
    )
    THEN
        RAISE EXCEPTION 'collection recommendation requires an approved, current, unblocked commerce opportunity';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_collection_recommendations_parent_approved ON collection_recommendations;
CREATE CONSTRAINT TRIGGER trg_collection_recommendations_parent_approved
    AFTER INSERT OR UPDATE OF
        opportunity_id,
        commerce_opportunity_id,
        policy_version_id
    ON collection_recommendations
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_collection_recommendation_parent_approved();

CREATE OR REPLACE FUNCTION enforce_collection_recommendation_gate_5()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status
       AND NEW.status IN ('assigned','generated','converted_to_collection')
       AND NOT EXISTS (
           SELECT 1
             FROM commerce_opportunities co
            WHERE co.id = NEW.commerce_opportunity_id
              AND co.curator_decision = 'approved'
       )
    THEN
        RAISE EXCEPTION 'curator_decision = approved before recommendation status transition to %',
            NEW.status;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_collection_recommendations_gate_5 ON collection_recommendations;
CREATE TRIGGER trg_collection_recommendations_gate_5
    BEFORE UPDATE OF status ON collection_recommendations
    FOR EACH ROW EXECUTE FUNCTION enforce_collection_recommendation_gate_5();
