-- Knowledge layer: concepts and concept_aliases.
-- Concepts form the controlled vocabulary for facts and relationships.
-- Every OUV criterion, heritage type, and thematic category is a concept.

CREATE TABLE concepts (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    uri         TEXT NOT NULL UNIQUE,          -- e.g. "whc:criterion/vii"
    label       JSONB NOT NULL DEFAULT '{}',   -- {"en": "Superlative Natural Phenomena"}
    description JSONB NOT NULL DEFAULT '{}',
    type        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'active',
    broader_id  UUID REFERENCES concepts(id),  -- SKOS broader (hierarchy)
    provenance  JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_concept_type   CHECK (type IN (
        'criterion','heritage_type','ecosystem','biome',
        'geographic','thematic','actor'
    )),
    CONSTRAINT chk_concept_status CHECK (status IN ('active','deprecated'))
);

-- Synonym / cross-source alias map. Enables deduplication when Wikidata
-- labels differ from UNESCO canonical labels.
CREATE TABLE concept_aliases (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id       UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    alias            TEXT NOT NULL,
    language         TEXT,
    source           TEXT NOT NULL,
    confidence_score NUMERIC(4,3) CHECK (confidence_score BETWEEN 0 AND 1),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (concept_id, alias, language)
);

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX idx_concepts_uri     ON concepts(uri);
CREATE INDEX idx_concepts_type    ON concepts(type);
CREATE INDEX idx_concepts_status  ON concepts(status);
CREATE INDEX idx_concepts_broader ON concepts(broader_id);
CREATE INDEX idx_aliases_concept  ON concept_aliases(concept_id);
CREATE INDEX idx_aliases_alias    ON concept_aliases(alias);

-- ---------------------------------------------------------------------------
-- Triggers
-- ---------------------------------------------------------------------------

CREATE TRIGGER trg_concepts_updated_at
    BEFORE UPDATE ON concepts
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_concept_aliases_updated_at
    BEFORE UPDATE ON concept_aliases
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Anti-cycle guard: walk the broader_id chain before any insert/update.
-- Rejects if NEW.id appears in its own ancestry or depth exceeds 20.
CREATE OR REPLACE FUNCTION check_concept_no_cycle()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
    v_current UUID := NEW.broader_id;
    v_depth   INT  := 0;
BEGIN
    WHILE v_current IS NOT NULL LOOP
        IF v_current = NEW.id THEN
            RAISE EXCEPTION 'Cycle detected in concept hierarchy: id=%', NEW.id;
        END IF;
        v_depth := v_depth + 1;
        IF v_depth > 20 THEN
            RAISE EXCEPTION 'Concept hierarchy exceeds 20 levels: id=%', NEW.id;
        END IF;
        SELECT broader_id INTO v_current FROM concepts WHERE id = v_current;
    END LOOP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_concepts_no_cycle
    BEFORE INSERT OR UPDATE ON concepts
    FOR EACH ROW WHEN (NEW.broader_id IS NOT NULL)
    EXECUTE FUNCTION check_concept_no_cycle();
