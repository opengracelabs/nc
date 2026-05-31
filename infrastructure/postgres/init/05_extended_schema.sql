-- Extended schema for the UNESCO WHC pipeline.
-- Adds richer fields to discovery_candidates and places identified during
-- ingestion worker development.

-- ---------------------------------------------------------------------------
-- discovery_candidates — additional WHC fields
-- ---------------------------------------------------------------------------

ALTER TABLE discovery_candidates
    ADD COLUMN IF NOT EXISTS unesco_ref_id      TEXT,
    ADD COLUMN IF NOT EXISTS statement_of_ouv   JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS justification      JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS transboundary      BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS core_area_ha       DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS buffer_area_ha     DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS spatial_precision  TEXT;

-- ---------------------------------------------------------------------------
-- places — mirror the same additional WHC fields
-- ---------------------------------------------------------------------------

ALTER TABLE places
    ADD COLUMN IF NOT EXISTS unesco_ref_id      TEXT,
    ADD COLUMN IF NOT EXISTS statement_of_ouv   JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS justification      JSONB NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS transboundary      BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS core_area_ha       DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS buffer_area_ha     DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS spatial_precision  TEXT;

-- ---------------------------------------------------------------------------
-- discovery_candidates — add 'promoted' to allowed statuses
-- ---------------------------------------------------------------------------

ALTER TABLE discovery_candidates DROP CONSTRAINT IF EXISTS chk_discovery_status;
ALTER TABLE discovery_candidates ADD CONSTRAINT chk_discovery_status
    CHECK (status IN ('pending','approved','rejected','flagged','ingesting','promoted'));
