-- v0.5.4 Phase 1 / Migration 32.
-- Asset Intelligence anchor_type support.
--
-- PostgreSQL is authoritative.
-- Replay-safe by pinning anchor_type into score_inputs.
-- No Commerce Intelligence formula redesign.
-- No Product Routing redesign.
-- No Catalog redesign.
-- No Publication redesign.

ALTER TABLE illustration_opportunities
    ADD COLUMN IF NOT EXISTS anchor_type TEXT REFERENCES commerce_anchor_type_vocabulary(value);

ALTER TABLE illustration_opportunities
    ADD COLUMN IF NOT EXISTS anchor_type_verified_by TEXT;

ALTER TABLE illustration_opportunities
    ADD COLUMN IF NOT EXISTS anchor_type_verified_at TIMESTAMPTZ;

ALTER TABLE illustration_opportunities
    ADD COLUMN IF NOT EXISTS anchor_type_provenance JSONB NOT NULL DEFAULT '{}';

UPDATE illustration_opportunities
   SET anchor_type = 'biological',
       anchor_type_verified_by = COALESCE(anchor_type_verified_by, 'migration_32_asset_intelligence_anchor_type'),
       anchor_type_verified_at = COALESCE(anchor_type_verified_at, NOW()),
       anchor_type_provenance = CASE
           WHEN anchor_type_provenance = '{}'::jsonb THEN
               '{"migration": "32_asset_intelligence_anchor_type", "rule": "existing_bhl_opportunities_default_biological"}'::jsonb
           ELSE anchor_type_provenance
       END
 WHERE source = 'bhl'
   AND anchor_type IS NULL;

ALTER TABLE illustration_opportunities
    DROP CONSTRAINT IF EXISTS chk_illustration_opportunities_anchor_type_verified;

ALTER TABLE illustration_opportunities
    ADD CONSTRAINT chk_illustration_opportunities_anchor_type_verified CHECK (
        anchor_type IS NULL
        OR (anchor_type_verified_by IS NOT NULL AND anchor_type_verified_at IS NOT NULL)
    );

CREATE INDEX IF NOT EXISTS idx_illustration_opportunities_anchor_type
    ON illustration_opportunities(anchor_type, status, updated_at DESC)
    WHERE anchor_type IS NOT NULL;
