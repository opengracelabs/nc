-- Full-text search and preservation status extensions.

-- ---------------------------------------------------------------------------
-- assets: add 'preserving' so the preservation worker can claim rows atomically
-- ---------------------------------------------------------------------------

ALTER TABLE assets DROP CONSTRAINT IF EXISTS chk_asset_status;
ALTER TABLE assets ADD CONSTRAINT chk_asset_status
    CHECK (status IN ('fetched','preserving','valid','normalized','active',
                      'quarantined','superseded','missing'));

-- ---------------------------------------------------------------------------
-- places: full-text search vector
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

CREATE TRIGGER trg_places_search_vector
    BEFORE INSERT OR UPDATE ON places
    FOR EACH ROW EXECUTE FUNCTION update_place_search_vector();

-- Backfill any existing rows (no-op on a fresh database).
UPDATE places SET updated_at = NOW() WHERE search_vector IS NULL;
