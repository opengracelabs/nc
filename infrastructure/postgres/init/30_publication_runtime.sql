-- v0.5.3 Phase 1 / Migration 30.
-- Publication Intelligence decision runtime.
--
-- PostgreSQL is authoritative.
-- Append-only audit.
-- No Shopify.
-- No Etsy.
-- No Gelato.
-- No Printful.
-- No Lulu.
-- No external IDs.
-- No publication execution.

CREATE TABLE IF NOT EXISTS publication_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO publication_status_vocabulary (value, description, sort_order)
VALUES
    ('draft', 'Publication decision candidate has been drafted.', 10),
    ('pending_curator_review', 'Publication decision candidate awaits curator review.', 20),
    ('approved_for_planning', 'Publication decision candidate is approved for internal planning only.', 30),
    ('needs_revision', 'Publication decision candidate requires revision.', 40),
    ('blocked', 'Publication decision candidate is blocked.', 50),
    ('stale', 'Publication decision candidate is stale.', 60),
    ('retired', 'Publication decision candidate is retired.', 70),
    ('superseded', 'Publication decision candidate is superseded.', 80)
ON CONFLICT (value) DO UPDATE SET description = EXCLUDED.description, sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS publication_decision_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO publication_decision_vocabulary (value, description, sort_order)
VALUES
    ('recommend', 'Recommended for internal publication planning.', 10),
    ('hold', 'Hold for more evidence or revision.', 20),
    ('block', 'Blocked from internal publication planning.', 30)
ON CONFLICT (value) DO UPDATE SET description = EXCLUDED.description, sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS publication_audit_event_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO publication_audit_event_type_vocabulary (value, description, sort_order)
VALUES
    ('publication_candidate_created', 'Publication candidate decision created.', 10),
    ('publication_decision_computed', 'Publication decision scores computed.', 20),
    ('publication_candidate_stale', 'Publication candidate marked stale.', 30),
    ('publication_replay_verified', 'Publication replay reproduced identical output.', 40),
    ('publication_replay_failed', 'Publication replay detected non-identical output.', 50)
ON CONFLICT (value) DO UPDATE SET description = EXCLUDED.description, sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS publication_channel_profiles (
    id                            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    publication_policy_id          UUID NOT NULL REFERENCES publication_policy(id),
    profile_key                    TEXT NOT NULL,
    label                          TEXT NOT NULL,
    description                    TEXT NOT NULL,
    status                         TEXT NOT NULL DEFAULT 'draft' REFERENCES publication_status_vocabulary(value),
    allowed_product_families       TEXT[] NOT NULL DEFAULT '{}',
    required_catalog_status        TEXT NOT NULL DEFAULT 'draft' REFERENCES catalog_status_vocabulary(value),
    required_variant_status        TEXT NOT NULL DEFAULT 'draft' REFERENCES catalog_status_vocabulary(value),
    minimum_rights_confidence      NUMERIC(4,3) NOT NULL DEFAULT 0.700 CHECK (minimum_rights_confidence BETWEEN 0 AND 1),
    minimum_catalog_quality_score  NUMERIC(4,3) NOT NULL DEFAULT 0.500 CHECK (minimum_catalog_quality_score BETWEEN 0 AND 1),
    metadata_requirements          JSONB NOT NULL DEFAULT '{}',
    risk_tolerance                 NUMERIC(4,3) NOT NULL DEFAULT 0.250 CHECK (risk_tolerance BETWEEN 0 AND 1),
    sort_order                     INT NOT NULL,
    provenance                     JSONB NOT NULL DEFAULT '{}',
    created_at                     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (publication_policy_id, profile_key),
    CONSTRAINT chk_publication_channel_profiles_no_external CHECK (
        profile_key !~* '(shopify|etsy|gelato|printful|lulu|external|api|provider|execution)'
        AND label !~* '(shopify|etsy|gelato|printful|lulu|external|api|provider|execution)'
        AND description !~* '(shopify|etsy|gelato|printful|lulu|external|api|provider|execution)'
        AND metadata_requirements::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND provenance::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
    )
);

CREATE TABLE IF NOT EXISTS publication_candidates (
    id                             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    catalog_candidate_id            UUID NOT NULL REFERENCES catalog_candidates(id),
    catalog_variant_id              UUID NOT NULL REFERENCES catalog_variants(id),
    publication_policy_id           UUID NOT NULL REFERENCES publication_policy(id),
    publication_channel_profile_id  UUID NOT NULL REFERENCES publication_channel_profiles(id),
    product_recommendation_id       UUID NOT NULL REFERENCES product_recommendations(id),
    commerce_opportunity_id         UUID NOT NULL REFERENCES commerce_opportunities(id),
    opportunity_id                  UUID NOT NULL REFERENCES illustration_opportunities(id),
    publication_status              TEXT NOT NULL DEFAULT 'draft' REFERENCES publication_status_vocabulary(value),
    publication_priority            TEXT NOT NULL,
    readiness_score                 NUMERIC(4,3) NOT NULL CHECK (readiness_score BETWEEN 0 AND 1),
    channel_fit_score               NUMERIC(4,3) NOT NULL CHECK (channel_fit_score BETWEEN 0 AND 1),
    risk_score                      NUMERIC(4,3) NOT NULL CHECK (risk_score BETWEEN 0 AND 1),
    publication_score               NUMERIC(4,3) NOT NULL CHECK (publication_score BETWEEN 0 AND 1),
    decision                        TEXT NOT NULL REFERENCES publication_decision_vocabulary(value),
    decision_basis                  JSONB NOT NULL DEFAULT '{}',
    input_snapshot                  JSONB NOT NULL DEFAULT '{}',
    staleness_status                TEXT NOT NULL DEFAULT 'current',
    curator_decision                TEXT NOT NULL DEFAULT 'pending' REFERENCES commerce_curator_decision_vocabulary(value),
    curator_reviewed_by             TEXT,
    curator_reviewed_at             TIMESTAMPTZ,
    provenance                      JSONB NOT NULL DEFAULT '{}',
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (catalog_variant_id, publication_channel_profile_id),
    CONSTRAINT chk_publication_candidates_basis CHECK (decision_basis <> '{}'::jsonb),
    CONSTRAINT chk_publication_candidates_input CHECK (input_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_publication_candidates_staleness CHECK (staleness_status IN ('current','stale')),
    CONSTRAINT chk_publication_candidates_review_identity CHECK (curator_decision = 'pending' OR curator_reviewed_by IS NOT NULL),
    CONSTRAINT chk_publication_candidates_no_external_state CHECK (
        publication_priority !~* '(shopify|etsy|gelato|printful|lulu|external|api|provider|execution)'
        AND decision_basis::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND input_snapshot::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
        AND provenance::text !~* '(shopify|etsy|gelato|printful|lulu|external[_ -]?id|api|provider|execution|sync|publish_url)'
    )
);

CREATE TABLE IF NOT EXISTS publication_audit_log (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    publication_candidate_id   UUID REFERENCES publication_candidates(id),
    catalog_candidate_id       UUID REFERENCES catalog_candidates(id),
    catalog_variant_id         UUID REFERENCES catalog_variants(id),
    publication_policy_id      UUID NOT NULL REFERENCES publication_policy(id),
    event_type                 TEXT NOT NULL REFERENCES publication_audit_event_type_vocabulary(value),
    event_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_type                 TEXT NOT NULL REFERENCES commerce_actor_type_vocabulary(value),
    actor_id                   TEXT NOT NULL,
    trigger                    TEXT NOT NULL REFERENCES commerce_computation_trigger_vocabulary(value),
    input_snapshot             JSONB NOT NULL DEFAULT '{}',
    output_snapshot            JSONB NOT NULL DEFAULT '{}',
    previous_state             JSONB NOT NULL DEFAULT '{}',
    new_state                  JSONB NOT NULL DEFAULT '{}',
    entry_checksum_sha256      TEXT NOT NULL,
    previous_entry_checksum    TEXT,
    reason                     TEXT NOT NULL,
    generated_by               TEXT NOT NULL,
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_publication_audit_log_target CHECK (
        publication_candidate_id IS NOT NULL OR catalog_candidate_id IS NOT NULL OR catalog_variant_id IS NOT NULL
    ),
    CONSTRAINT chk_publication_audit_log_entry_checksum CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_publication_audit_log_previous_checksum CHECK (previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_publication_audit_log_distinct_checksum CHECK (previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256),
    CONSTRAINT chk_publication_audit_log_actor_id CHECK (length(actor_id) > 0),
    CONSTRAINT chk_publication_audit_log_reason CHECK (length(reason) > 0),
    CONSTRAINT chk_publication_audit_log_generated_by CHECK (length(generated_by) > 0)
);

CREATE INDEX IF NOT EXISTS idx_publication_channel_profiles_policy ON publication_channel_profiles(publication_policy_id, status, sort_order);
CREATE INDEX IF NOT EXISTS idx_publication_candidates_policy_status ON publication_candidates(publication_policy_id, publication_status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_publication_candidates_catalog_variant ON publication_candidates(catalog_variant_id);
CREATE INDEX IF NOT EXISTS idx_publication_candidates_channel ON publication_candidates(publication_channel_profile_id, publication_score DESC);
CREATE INDEX IF NOT EXISTS idx_publication_audit_log_candidate_event ON publication_audit_log(publication_candidate_id, event_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS uniq_publication_audit_log_checksum ON publication_audit_log(entry_checksum_sha256);

DROP TRIGGER IF EXISTS trg_publication_channel_profiles_updated_at ON publication_channel_profiles;
CREATE TRIGGER trg_publication_channel_profiles_updated_at BEFORE UPDATE ON publication_channel_profiles FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_publication_candidates_updated_at ON publication_candidates;
CREATE TRIGGER trg_publication_candidates_updated_at BEFORE UPDATE ON publication_candidates FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_publication_candidate_parent_approved()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM catalog_candidates cc
          JOIN catalog_variants cv ON cv.id = NEW.catalog_variant_id AND cv.catalog_candidate_id = cc.id
          JOIN product_recommendations pr ON pr.id = cc.product_recommendation_id
          JOIN commerce_opportunities co ON co.id = cc.commerce_opportunity_id
          JOIN publication_channel_profiles pcp ON pcp.id = NEW.publication_channel_profile_id
         WHERE cc.id = NEW.catalog_candidate_id
           AND cc.product_recommendation_id = NEW.product_recommendation_id
           AND cc.commerce_opportunity_id = NEW.commerce_opportunity_id
           AND cc.opportunity_id = NEW.opportunity_id
           AND cc.product_family = cv.product_family
           AND cc.catalog_status IN ('draft','approved')
           AND cv.variant_status IN ('draft','approved')
           AND pr.status = 'curator_approved'
           AND co.curator_decision = 'approved'
           AND co.hard_gate_status = 'passed'
           AND co.policy_stale = FALSE
           AND co.commerce_tier <> 'blocked'
           AND cv.product_family = ANY(pcp.allowed_product_families)
    ) THEN
        RAISE EXCEPTION 'publication candidate requires approved catalog, recommendation, and commerce parents';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_publication_candidate_parent_approved ON publication_candidates;
CREATE CONSTRAINT TRIGGER trg_publication_candidate_parent_approved
    AFTER INSERT OR UPDATE OF catalog_candidate_id, catalog_variant_id, publication_channel_profile_id, product_recommendation_id, commerce_opportunity_id, opportunity_id
    ON publication_candidates
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_publication_candidate_parent_approved();

CREATE OR REPLACE RULE publication_audit_log_no_update AS
    ON UPDATE TO publication_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no UPDATE permitted on publication_audit_log');
CREATE OR REPLACE RULE publication_audit_log_no_delete AS
    ON DELETE TO publication_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no DELETE permitted on publication_audit_log');

CREATE OR REPLACE FUNCTION enforce_publication_audit_hash_chain()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE latest_checksum TEXT;
BEGIN
    SELECT pal.entry_checksum_sha256 INTO latest_checksum
      FROM publication_audit_log pal
     WHERE COALESCE(pal.publication_candidate_id, pal.catalog_variant_id, pal.catalog_candidate_id)
           IS NOT DISTINCT FROM COALESCE(NEW.publication_candidate_id, NEW.catalog_variant_id, NEW.catalog_candidate_id)
     ORDER BY event_at DESC, created_at DESC, id DESC
     LIMIT 1;

    IF latest_checksum IS NULL THEN
        IF NEW.previous_entry_checksum IS NOT NULL THEN
            RAISE EXCEPTION 'first publication_audit_log entry for target must have null previous_entry_checksum';
        END IF;
    ELSIF NEW.previous_entry_checksum IS DISTINCT FROM latest_checksum THEN
        RAISE EXCEPTION 'previous_entry_checksum must match latest publication_audit_log entry for target';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_publication_audit_hash_chain ON publication_audit_log;
CREATE TRIGGER trg_publication_audit_hash_chain BEFORE INSERT ON publication_audit_log FOR EACH ROW EXECUTE FUNCTION enforce_publication_audit_hash_chain();
