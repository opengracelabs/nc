-- v0.5.0 Phase 2 / Migration 22.
-- Commerce Intelligence score audit log.
--
-- PostgreSQL is authoritative.
-- No scoring worker activation.
-- No product generation.
-- No Shopify integration.
-- No Etsy integration.

CREATE TABLE IF NOT EXISTS score_audit_log (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id              UUID NOT NULL REFERENCES illustration_opportunities(id),
    policy_version_id           UUID NOT NULL REFERENCES commerce_policy(id),
    event_type                  TEXT NOT NULL REFERENCES commerce_audit_event_type_vocabulary(value),
    event_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_type                  TEXT NOT NULL REFERENCES commerce_actor_type_vocabulary(value),
    actor_id                    TEXT NOT NULL,
    actor_notes                 TEXT,
    trigger                     TEXT NOT NULL REFERENCES commerce_computation_trigger_vocabulary(value),
    score_inputs                JSONB NOT NULL DEFAULT '{}',
    score_outputs               JSONB NOT NULL DEFAULT '{}',
    previous_state              JSONB NOT NULL DEFAULT '{}',
    new_state                   JSONB NOT NULL DEFAULT '{}',
    entry_checksum_sha256       TEXT NOT NULL,
    previous_entry_checksum     TEXT,
    reason                      TEXT NOT NULL,
    generated_by                TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_score_audit_log_entry_checksum CHECK (
        entry_checksum_sha256 ~ '^[0-9a-f]{64}$'
    ),
    CONSTRAINT chk_score_audit_log_previous_checksum CHECK (
        previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
    ),
    CONSTRAINT chk_score_audit_log_distinct_checksum CHECK (
        previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
    ),
    CONSTRAINT chk_score_audit_log_actor_id CHECK (length(actor_id) > 0),
    CONSTRAINT chk_score_audit_log_reason CHECK (length(reason) > 0),
    CONSTRAINT chk_score_audit_log_generated_by CHECK (length(generated_by) > 0),
    CONSTRAINT chk_score_audit_log_curator_notes CHECK (
        actor_type <> 'curator' OR actor_notes IS NOT NULL
    )
);

CREATE INDEX IF NOT EXISTS idx_score_audit_log_opportunity_event
    ON score_audit_log(opportunity_id, event_at DESC);

CREATE INDEX IF NOT EXISTS idx_score_audit_log_policy_event
    ON score_audit_log(policy_version_id, event_at DESC);

CREATE INDEX IF NOT EXISTS idx_score_audit_log_event_type
    ON score_audit_log(event_type, event_at DESC);

CREATE INDEX IF NOT EXISTS idx_score_audit_log_actor
    ON score_audit_log(actor_type, actor_id, event_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_score_audit_log_opportunity_checksum
    ON score_audit_log(opportunity_id, entry_checksum_sha256);

CREATE OR REPLACE FUNCTION commerce_raise_exception(message TEXT)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION '%', message;
END;
$$;

CREATE OR REPLACE RULE score_audit_log_no_update AS
    ON UPDATE TO score_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no UPDATE permitted on score_audit_log');

CREATE OR REPLACE RULE score_audit_log_no_delete AS
    ON DELETE TO score_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no DELETE permitted on score_audit_log');

CREATE OR REPLACE FUNCTION enforce_score_audit_hash_chain()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
    latest_checksum TEXT;
BEGIN
    SELECT sal.entry_checksum_sha256
      INTO latest_checksum
      FROM score_audit_log sal
     WHERE sal.opportunity_id = NEW.opportunity_id
     ORDER BY event_at DESC, created_at DESC, id DESC
     LIMIT 1;

    IF latest_checksum IS NULL THEN
        IF NEW.previous_entry_checksum IS NOT NULL THEN
            RAISE EXCEPTION 'first score_audit_log entry for opportunity % must have null previous_entry_checksum',
                NEW.opportunity_id;
        END IF;
    ELSIF NEW.previous_entry_checksum IS DISTINCT FROM latest_checksum THEN
        RAISE EXCEPTION 'previous_entry_checksum must match latest score_audit_log entry for opportunity %',
            NEW.opportunity_id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_score_audit_hash_chain ON score_audit_log;
CREATE TRIGGER trg_score_audit_hash_chain
    BEFORE INSERT ON score_audit_log
    FOR EACH ROW EXECUTE FUNCTION enforce_score_audit_hash_chain();

CREATE OR REPLACE FUNCTION enforce_commerce_opportunity_audit_exists()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.commerce_opportunity_score IS NOT NULL
       AND NOT EXISTS (
           SELECT 1
             FROM score_audit_log sal
            WHERE sal.opportunity_id = NEW.opportunity_id
              AND sal.policy_version_id = NEW.policy_version_id
              AND sal.event_type IN (
                  'score_computed',
                  'hard_gate_blocked',
                  'hard_gate_passed',
                  'tier_assigned',
                  'policy_applied',
                  'eligibility_updated',
                  'replay_verified'
              )
       )
    THEN
        RAISE EXCEPTION 'commerce_opportunity % has a score but no score_audit_log entry',
            NEW.id;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_commerce_opportunities_audit_exists ON commerce_opportunities;
CREATE CONSTRAINT TRIGGER trg_commerce_opportunities_audit_exists
    AFTER INSERT OR UPDATE OF
        policy_version_id,
        commerce_opportunity_score,
        commerce_tier,
        csm_score,
        csm_tier,
        hard_gate_status
    ON commerce_opportunities
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_commerce_opportunity_audit_exists();
