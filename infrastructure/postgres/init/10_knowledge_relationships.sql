-- Knowledge layer: relationships.
-- Typed edges between places and/or concepts.
-- Supports place→concept (exemplifies, classified_as) and
-- place→place (co_inscribed_with, shares_ecosystem, part_of) graphs.

CREATE TABLE relationships (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id       UUID NOT NULL,
    subject_type     TEXT NOT NULL,
    predicate        TEXT NOT NULL,
    object_id        UUID NOT NULL,
    object_type      TEXT NOT NULL,
    confidence_score NUMERIC(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    status           TEXT NOT NULL DEFAULT 'proposed',
    asset_id         UUID REFERENCES assets(id),
    provenance       JSONB NOT NULL DEFAULT '{}',
    agent_notes      JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_rel_subject_type CHECK (subject_type IN ('place','concept')),
    CONSTRAINT chk_rel_object_type  CHECK (object_type  IN ('place','concept')),
    CONSTRAINT chk_rel_predicate    CHECK (predicate IN (
        'part_of',
        'adjacent_to',
        'shares_ecosystem',
        'serial_component_of',
        'co_inscribed_with',
        'extends',
        'exemplifies',
        'classified_as',
        'broader',
        'narrower',
        'related',
        'equivalent_to'
    )),
    CONSTRAINT chk_rel_status CHECK (status IN (
        'proposed','active','disputed','retracted'
    )),
    -- Structural predicates must not be self-referential
    CONSTRAINT chk_rel_no_self_ref CHECK (
        NOT (subject_id = object_id AND subject_type = object_type)
    ),
    UNIQUE (subject_id, subject_type, predicate, object_id, object_type)
);

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX idx_rel_object ON relationships(object_id, object_type);
CREATE INDEX idx_rel_asset  ON relationships(asset_id);

-- ---------------------------------------------------------------------------
-- Triggers
-- ---------------------------------------------------------------------------

CREATE TRIGGER trg_relationships_updated_at
    BEFORE UPDATE ON relationships
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
