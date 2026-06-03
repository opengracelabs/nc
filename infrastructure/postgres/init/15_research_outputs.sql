-- MILESTONE-003 Research outputs.
-- Research turns governed evidence and knowledge into human-readable outputs.
-- Architecture remains frozen: PostgreSQL is the authority; assets point to MinIO evidence.

CREATE TABLE research_outputs (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id         UUID NOT NULL REFERENCES places(id),
    output_type      TEXT NOT NULL DEFAULT 'place_brief',
    output_version   TEXT NOT NULL DEFAULT '1',
    title            TEXT NOT NULL,
    summary          TEXT,
    status           TEXT NOT NULL DEFAULT 'pending_review',
    confidence_score NUMERIC(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    reviewed_by      TEXT,
    reviewed_at      TIMESTAMPTZ,
    published_at     TIMESTAMPTZ,
    provenance       JSONB NOT NULL DEFAULT '{}',
    agent_notes      JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_research_output_type CHECK (output_type IN ('place_brief')),
    CONSTRAINT chk_research_output_status CHECK (status IN (
        'pending_review','approved','published','rejected','disputed','retracted'
    )),
    UNIQUE (place_id, output_type, output_version)
);

CREATE TABLE research_statements (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    output_id        UUID NOT NULL REFERENCES research_outputs(id) ON DELETE CASCADE,
    place_id         UUID NOT NULL REFERENCES places(id),
    sequence         INT NOT NULL CHECK (sequence > 0),
    statement_type   TEXT NOT NULL,
    body             TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'pending_review',
    confidence_score NUMERIC(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    provenance       JSONB NOT NULL DEFAULT '{}',
    agent_notes      JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_research_statement_type CHECK (statement_type IN (
        'classification','criterion','co_inscription'
    )),
    CONSTRAINT chk_research_statement_status CHECK (status IN (
        'pending_review','approved','published','rejected','disputed','retracted'
    )),
    UNIQUE (output_id, sequence)
);

CREATE TABLE research_statement_evidence (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    statement_id    UUID NOT NULL REFERENCES research_statements(id) ON DELETE CASCADE,
    asset_id        UUID NOT NULL REFERENCES assets(id),
    fact_id         UUID NOT NULL REFERENCES facts(id),
    relationship_id UUID NOT NULL REFERENCES relationships(id),
    evidence_role   TEXT NOT NULL DEFAULT 'supporting',
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_research_evidence_role CHECK (evidence_role IN ('supporting')),
    UNIQUE (statement_id, asset_id, fact_id, relationship_id)
);

CREATE INDEX idx_research_outputs_place_status
    ON research_outputs(place_id, status, updated_at DESC);
CREATE INDEX idx_research_statements_output_sequence
    ON research_statements(output_id, sequence);
CREATE INDEX idx_research_evidence_fact
    ON research_statement_evidence(fact_id);
CREATE INDEX idx_research_evidence_relationship
    ON research_statement_evidence(relationship_id);
CREATE INDEX idx_research_evidence_asset
    ON research_statement_evidence(asset_id);

CREATE TRIGGER trg_research_outputs_updated_at
    BEFORE UPDATE ON research_outputs
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_research_statements_updated_at
    BEFORE UPDATE ON research_statements
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION assert_research_statement_supported(statement_uuid UUID)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM research_statements WHERE id = statement_uuid)
       AND NOT EXISTS (
           SELECT 1
           FROM research_statement_evidence e
           WHERE e.statement_id = statement_uuid
       )
    THEN
        RAISE EXCEPTION 'research statement % has no source evidence/fact/relationship support',
            statement_uuid;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION check_research_statement_supported()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    PERFORM assert_research_statement_supported(NEW.id);
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION check_research_statement_still_supported()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    PERFORM assert_research_statement_supported(OLD.statement_id);
    RETURN OLD;
END;
$$;

CREATE OR REPLACE FUNCTION assert_research_evidence_coherent(
    statement_uuid UUID,
    asset_uuid UUID,
    fact_uuid UUID,
    relationship_uuid UUID
)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    statement_place UUID;
    fact_place UUID;
    fact_asset UUID;
    rel_asset UUID;
    rel_subject_id UUID;
    rel_subject_type TEXT;
    rel_object_id UUID;
    rel_object_type TEXT;
BEGIN
    SELECT s.place_id INTO statement_place
    FROM research_statements s
    WHERE s.id = statement_uuid;

    SELECT f.place_id, f.asset_id INTO fact_place, fact_asset
    FROM facts f
    WHERE f.id = fact_uuid;

    SELECT r.asset_id, r.subject_id, r.subject_type, r.object_id, r.object_type
      INTO rel_asset, rel_subject_id, rel_subject_type, rel_object_id, rel_object_type
    FROM relationships r
    WHERE r.id = relationship_uuid;

    IF fact_place IS DISTINCT FROM statement_place THEN
        RAISE EXCEPTION 'fact place does not match research statement place';
    END IF;

    IF NOT (
        (rel_subject_type = 'place' AND rel_subject_id = statement_place)
        OR (rel_object_type = 'place' AND rel_object_id = statement_place)
    ) THEN
        RAISE EXCEPTION 'relationship does not support research statement place';
    END IF;

    IF asset_uuid IS DISTINCT FROM fact_asset
       AND asset_uuid IS DISTINCT FROM rel_asset
    THEN
        RAISE EXCEPTION 'asset does not match supporting fact or relationship evidence';
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION check_research_evidence_coherent()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    PERFORM assert_research_evidence_coherent(
        NEW.statement_id, NEW.asset_id, NEW.fact_id, NEW.relationship_id
    );
    RETURN NEW;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_research_statement_supported
    AFTER INSERT OR UPDATE ON research_statements
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_research_statement_supported();

CREATE CONSTRAINT TRIGGER trg_research_evidence_delete_supported
    AFTER DELETE ON research_statement_evidence
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_research_statement_still_supported();

CREATE CONSTRAINT TRIGGER trg_research_evidence_coherent
    AFTER INSERT OR UPDATE ON research_statement_evidence
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_research_evidence_coherent();

CREATE OR REPLACE FUNCTION check_research_output_publishable()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.status IN ('approved', 'published') THEN
        IF NOT EXISTS (
            SELECT 1
            FROM research_statements s
            WHERE s.output_id = NEW.id
        ) THEN
            RAISE EXCEPTION 'research output % cannot be % without statements',
                NEW.id, NEW.status;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM research_statements s
            WHERE s.output_id = NEW.id
              AND s.status <> NEW.status
        ) THEN
            RAISE EXCEPTION 'research output % cannot be % with unsynchronized statements',
                NEW.id, NEW.status;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_research_output_publishable
    AFTER INSERT OR UPDATE OF status ON research_outputs
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_research_output_publishable();
