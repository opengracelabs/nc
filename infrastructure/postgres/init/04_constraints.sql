-- Constitutional constraints.
-- Applied after tables and indexes. Extended schema (05) runs after this.

-- ---------------------------------------------------------------------------
-- Status CHECK constraints — invalid states rejected at the DB boundary
-- discovery_candidates gets its constraint in 05_extended_schema.sql after
-- the 'promoted' status is added.
-- ---------------------------------------------------------------------------

ALTER TABLE places ADD CONSTRAINT chk_place_status
    CHECK (status IN ('candidate','active','endangered','delisted','deprecated'));

ALTER TABLE assets ADD CONSTRAINT chk_asset_status
    CHECK (status IN ('fetched','valid','normalized','active','quarantined','superseded','missing'));

ALTER TABLE ingested_records ADD CONSTRAINT chk_ingested_status
    CHECK (status IN ('staged','active','failed','superseded'));

ALTER TABLE sources ADD CONSTRAINT chk_source_status
    CHECK (status IN ('active','degraded','unavailable','deprecated'));

ALTER TABLE workflow_items ADD CONSTRAINT chk_workflow_status
    CHECK (status IN ('pending','in_progress','awaiting_review','approved','rejected',
                      'flagged','completed','failed','cancelled'));

-- ---------------------------------------------------------------------------
-- Remove NULL FK columns — workflow_items is deferred, not yet wired.
-- These columns are always NULL and create model confusion.
-- ---------------------------------------------------------------------------

ALTER TABLE discovery_candidates DROP COLUMN IF EXISTS workflow_item_id;
ALTER TABLE assets               DROP COLUMN IF EXISTS workflow_item_id;
ALTER TABLE ingested_records     DROP COLUMN IF EXISTS workflow_item_id;

DROP INDEX IF EXISTS idx_discovery_workflow;
DROP INDEX IF EXISTS idx_assets_workflow;
DROP INDEX IF EXISTS idx_ingested_workflow;

-- ---------------------------------------------------------------------------
-- Remove ingested_records.checksum_manifest — duplicated by assets.checksum_sha256
-- ---------------------------------------------------------------------------

ALTER TABLE ingested_records DROP COLUMN IF EXISTS checksum_manifest;
