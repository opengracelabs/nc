-- Add knowledge extraction tracking columns to places.
-- knowledge_extracting: claimed by the knowledge worker (prevents double-processing).
-- last_knowledge_extracted_at: controls rescore interval.
-- knowledge_score: mean confidence of active facts; denormalized for fast ordering.

ALTER TABLE places
    ADD COLUMN IF NOT EXISTS knowledge_extracting        BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS last_knowledge_extracted_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS knowledge_score             DOUBLE PRECISION;

-- Queue index: fast lookup of places needing extraction.
CREATE INDEX IF NOT EXISTS idx_places_knowledge_queue
    ON places(last_knowledge_extracted_at NULLS FIRST, created_at)
    WHERE status = 'active' AND knowledge_extracting = FALSE;
