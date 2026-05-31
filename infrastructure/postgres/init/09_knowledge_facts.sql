-- Knowledge layer: facts.
-- Each fact is an atomic, sourced, evidence-linked claim about a place.
-- Predicates are a closed vocabulary enforced by CHECK constraint.
-- New predicates require a migration — intentional, not a restriction.

CREATE TABLE facts (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id         UUID NOT NULL REFERENCES places(id),
    predicate        TEXT NOT NULL,
    value            JSONB NOT NULL,   -- {"number":1981} | {"text":"vii"} | {"boolean":true}
    value_type       TEXT NOT NULL,
    language         TEXT,             -- ISO 639-1; NULL for language-neutral facts
    concept_id       UUID REFERENCES concepts(id),
    asset_id         UUID REFERENCES assets(id),   -- evidence; NULL when derived from places.*
    source           TEXT NOT NULL,
    confidence_score NUMERIC(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    status           TEXT NOT NULL DEFAULT 'draft',
    provenance       JSONB NOT NULL DEFAULT '{}',   -- PROV-O lineage on every row
    agent_notes      JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_fact_predicate CHECK (predicate IN (
        'inscription_year',
        'core_area_ha',
        'buffer_area_ha',
        'transboundary',
        'heritage_type',
        'ouv_criterion',
        'country_code',
        'spatial_precision',
        'name',
        'description',
        'statement_of_ouv',
        'endangered_status',
        'endangered_since'
    )),
    CONSTRAINT chk_fact_value_type CHECK (value_type IN (
        'text','number','date','boolean','uri','geometry','jsonb'
    )),
    CONSTRAINT chk_fact_status CHECK (status IN (
        'draft','active','disputed','superseded','retracted'
    ))
);

-- Content-addressable uniqueness: (place, predicate, language, value) is globally unique
-- across all statuses. This prevents exact duplicates and makes facts reactivatable
-- rather than re-insertable when a superseded value reappears.
CREATE UNIQUE INDEX uniq_facts_slot
    ON facts(place_id, predicate, COALESCE(language, ''), (value::text));

-- ---------------------------------------------------------------------------
-- Performance indexes
-- ---------------------------------------------------------------------------

CREATE INDEX idx_facts_place      ON facts(place_id);
CREATE INDEX idx_facts_predicate  ON facts(predicate);
CREATE INDEX idx_facts_status     ON facts(status);
CREATE INDEX idx_facts_concept    ON facts(concept_id);
CREATE INDEX idx_facts_asset      ON facts(asset_id);
CREATE INDEX idx_facts_place_pred ON facts(place_id, predicate, status);
CREATE INDEX idx_facts_provenance ON facts USING GIN(provenance);

-- ---------------------------------------------------------------------------
-- Triggers
-- ---------------------------------------------------------------------------

CREATE TRIGGER trg_facts_updated_at
    BEFORE UPDATE ON facts
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- When a place's authority fields change, mark it so the knowledge worker
-- knows to supersede derived facts on its next extraction pass.
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
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_places_stale_facts
    BEFORE UPDATE ON places
    FOR EACH ROW EXECUTE FUNCTION flag_stale_facts_on_place_update();
