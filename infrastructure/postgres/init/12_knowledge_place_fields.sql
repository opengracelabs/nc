-- Add knowledge extraction tracking columns to places.
-- knowledge_extracting: claimed by the knowledge worker (prevents double-processing).
-- last_knowledge_extracted_at: controls rescore interval.
-- knowledge_score: mean confidence of active facts; denormalized for fast ordering.

ALTER TABLE places
    ADD COLUMN IF NOT EXISTS knowledge_extracting        BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS last_knowledge_extracted_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS knowledge_score             DOUBLE PRECISION;

-- Queue index is in 13_knowledge_performance_indexes.sql (idx_places_knowledge_claim_active).
