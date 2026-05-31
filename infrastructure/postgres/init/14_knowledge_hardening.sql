-- MILESTONE-2.6 Knowledge Hardening.
-- Upgrade path for deployments already running migrations 08-13.
-- All statements are idempotent (IF EXISTS / IF NOT EXISTS / CREATE OR REPLACE).

-- ---------------------------------------------------------------------------
-- B1: Drop GIN provenance index (259 MB at 50K sites, zero WHERE-clause uses)
-- ---------------------------------------------------------------------------

DROP INDEX IF EXISTS idx_facts_provenance;

-- ---------------------------------------------------------------------------
-- B1: Drop full-table composite indexes superseded by partial indexes in 13
-- ---------------------------------------------------------------------------

DROP INDEX IF EXISTS idx_facts_place_pred;
DROP INDEX IF EXISTS idx_facts_status;
DROP INDEX IF EXISTS idx_rel_subject;
DROP INDEX IF EXISTS idx_rel_predicate;
DROP INDEX IF EXISTS idx_rel_status;
DROP INDEX IF EXISTS idx_places_knowledge_queue;

-- ---------------------------------------------------------------------------
-- B1: Reduce B-tree fragmentation from UUID v4 inserts
-- ---------------------------------------------------------------------------

ALTER TABLE facts         SET (fillfactor = 70);
ALTER TABLE relationships SET (fillfactor = 70);

-- ---------------------------------------------------------------------------
-- H5: Remove dead 'draft' status — worker always inserts as 'active'
-- ---------------------------------------------------------------------------

ALTER TABLE facts DROP CONSTRAINT IF EXISTS chk_fact_status;
ALTER TABLE facts ADD CONSTRAINT chk_fact_status CHECK (status IN (
    'active', 'disputed', 'superseded', 'retracted'
));
ALTER TABLE facts ALTER COLUMN status SET DEFAULT 'active';

-- ---------------------------------------------------------------------------
-- M2: Add updated_at to concept_aliases (only table without it)
-- ---------------------------------------------------------------------------

ALTER TABLE concept_aliases
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

DROP TRIGGER IF EXISTS trg_concept_aliases_updated_at ON concept_aliases;
CREATE TRIGGER trg_concept_aliases_updated_at
    BEFORE UPDATE ON concept_aliases
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------------------
-- H2: Stale facts trigger — force re-queue when authority fields change
-- Previously only wrote to agent_notes; worker would not re-extract until
-- rescore_interval_days elapsed, leaving stale facts active for days.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION flag_stale_facts_on_place_update()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.inscription_year IS DISTINCT FROM OLD.inscription_year
       OR NEW.heritage_type   IS DISTINCT FROM OLD.heritage_type
       OR NEW.ouv_criteria    IS DISTINCT FROM OLD.ouv_criteria
       OR NEW.country_codes   IS DISTINCT FROM OLD.country_codes
       OR NEW.core_area_ha    IS DISTINCT FROM OLD.core_area_ha
       OR NEW.buffer_area_ha  IS DISTINCT FROM OLD.buffer_area_ha
       OR NEW.transboundary   IS DISTINCT FROM OLD.transboundary
    THEN
        NEW.agent_notes = NEW.agent_notes || jsonb_build_object(
            'stale_facts_flagged_at',
            to_char(NOW(), 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
        );
        NEW.last_knowledge_extracted_at = NULL;
        NEW.knowledge_extracting = FALSE;
    END IF;
    RETURN NEW;
END;
$$;

-- ---------------------------------------------------------------------------
-- H4: Retract co_inscribed_with relationships when inscription_year supersedes.
-- Without this, stale co_inscribed_with pairs remain active after a year correction.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION retract_stale_co_inscribed()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.predicate = 'inscription_year'
       AND OLD.status = 'active'
       AND NEW.status = 'superseded'
    THEN
        UPDATE relationships
        SET status      = 'retracted',
            agent_notes = agent_notes || jsonb_build_object(
                'retraction_reason', 'inscription_year_superseded',
                'retracted_at',      to_char(NOW(), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
                'superseded_fact_id', NEW.id::text
            ),
            updated_at  = NOW()
        WHERE predicate = 'co_inscribed_with'
          AND status    = 'active'
          AND (subject_id = NEW.place_id OR object_id = NEW.place_id);
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_facts_retract_co_inscribed ON facts;
CREATE TRIGGER trg_facts_retract_co_inscribed
    AFTER UPDATE ON facts
    FOR EACH ROW EXECUTE FUNCTION retract_stale_co_inscribed();
