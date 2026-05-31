-- MILESTONE-001 idempotent schema repair.
-- This keeps existing Docker Compose volumes compatible with the first
-- UNESCO pipeline without introducing another datastore or runtime.

-- ---------------------------------------------------------------------------
-- UNESCO discovery and place fields
-- ---------------------------------------------------------------------------

ALTER TABLE discovery_candidates
    ADD COLUMN IF NOT EXISTS unesco_ref_id      TEXT,
    ADD COLUMN IF NOT EXISTS statement_of_ouv   JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS justification      JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS transboundary      BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS core_area_ha       DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS buffer_area_ha     DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS spatial_precision  TEXT,
    ADD COLUMN IF NOT EXISTS promoted_place_id  UUID REFERENCES places(id);

ALTER TABLE places
    ADD COLUMN IF NOT EXISTS unesco_ref_id      TEXT,
    ADD COLUMN IF NOT EXISTS statement_of_ouv   JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS justification      JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS transboundary      BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS core_area_ha       DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS buffer_area_ha     DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS spatial_precision  TEXT;


-- Backfill UNESCO reference identifiers for rows created before this schema
-- repair existed.
UPDATE discovery_candidates
SET unesco_ref_id = source_id
WHERE source = 'unesco_whc'
  AND unesco_ref_id IS NULL;

UPDATE places
SET unesco_ref_id = source_id
WHERE source = 'unesco_whc'
  AND unesco_ref_id IS NULL;

-- ---------------------------------------------------------------------------
-- Preservation fields and statuses
-- ---------------------------------------------------------------------------

ALTER TABLE assets
    ADD COLUMN IF NOT EXISTS validation_warnings TEXT[] NOT NULL DEFAULT '{}';

ALTER TABLE assets DROP CONSTRAINT IF EXISTS chk_asset_status;
ALTER TABLE assets ADD CONSTRAINT chk_asset_status
    CHECK (status IN ('fetched','preserving','valid','normalized','active',
                      'quarantined','superseded','missing'));

ALTER TABLE discovery_candidates DROP CONSTRAINT IF EXISTS chk_discovery_status;
ALTER TABLE discovery_candidates ADD CONSTRAINT chk_discovery_status
    CHECK (status IN ('pending','approved','rejected','flagged','ingesting','promoted'));

-- ---------------------------------------------------------------------------
-- PostgreSQL-only search support
-- ---------------------------------------------------------------------------

ALTER TABLE places ADD COLUMN IF NOT EXISTS search_vector tsvector;

CREATE INDEX IF NOT EXISTS idx_places_search ON places USING GIN(search_vector);

CREATE OR REPLACE FUNCTION update_place_search_vector()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.search_vector := to_tsvector('simple',
        coalesce(NEW.name->>'en', '') || ' ' ||
        coalesce(NEW.name->>'fr', '') || ' ' ||
        coalesce(NEW.name->>'es', '') || ' ' ||
        coalesce(NEW.name->>'ar', '') || ' ' ||
        coalesce(NEW.description->>'en', '') || ' ' ||
        coalesce(NEW.description->>'fr', '')
    );
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_places_search_vector ON places;
CREATE TRIGGER trg_places_search_vector
    BEFORE INSERT OR UPDATE ON places
    FOR EACH ROW EXECUTE FUNCTION update_place_search_vector();

UPDATE places SET updated_at = NOW() WHERE search_vector IS NULL;
