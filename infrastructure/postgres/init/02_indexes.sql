-- Performance indexes. All FK columns, common filter columns, and search columns.

-- ---------------------------------------------------------------------------
-- sources
-- ---------------------------------------------------------------------------
CREATE INDEX idx_sources_status       ON sources(status);
CREATE INDEX idx_sources_priority     ON sources(priority);

-- ---------------------------------------------------------------------------
-- places
-- ---------------------------------------------------------------------------
CREATE INDEX idx_places_status        ON places(status);
CREATE INDEX idx_places_source        ON places(source);
CREATE INDEX idx_places_heritage_type ON places(heritage_type);
CREATE INDEX idx_places_inscription   ON places(inscription_year);
CREATE INDEX idx_places_country_codes ON places USING GIN(country_codes);
CREATE INDEX idx_places_ouv_criteria  ON places USING GIN(ouv_criteria);
CREATE INDEX idx_places_centroid      ON places USING GIST(centroid);
CREATE INDEX idx_places_boundary      ON places USING GIST(boundary);

-- Multilingual name search (trigram across all language values)
CREATE INDEX idx_places_name_trgm
    ON places USING GIN((name::TEXT) gin_trgm_ops);

-- ---------------------------------------------------------------------------
-- workflow_items
-- ---------------------------------------------------------------------------
CREATE INDEX idx_workflow_capability  ON workflow_items(capability);
CREATE INDEX idx_workflow_entity      ON workflow_items(entity_type, entity_id);
CREATE INDEX idx_workflow_status      ON workflow_items(status);
CREATE INDEX idx_workflow_priority    ON workflow_items(priority, scheduled_at);
CREATE INDEX idx_workflow_parent      ON workflow_items(parent_item_id);

-- Queue poll index: find the next claimable item fast
CREATE INDEX idx_workflow_queue
    ON workflow_items(capability, priority, created_at)
    WHERE status = 'pending';

-- ---------------------------------------------------------------------------
-- discovery_candidates
-- ---------------------------------------------------------------------------
CREATE INDEX idx_discovery_source     ON discovery_candidates(source, source_id);
CREATE INDEX idx_discovery_status     ON discovery_candidates(status);
CREATE INDEX idx_discovery_qid        ON discovery_candidates(wikidata_qid);
CREATE INDEX idx_discovery_country    ON discovery_candidates USING GIN(country_codes);
CREATE INDEX idx_discovery_centroid   ON discovery_candidates USING GIST(centroid);
CREATE INDEX idx_discovery_place      ON discovery_candidates(promoted_place_id);
CREATE INDEX idx_discovery_workflow   ON discovery_candidates(workflow_item_id);

-- ---------------------------------------------------------------------------
-- assets
-- ---------------------------------------------------------------------------
CREATE INDEX idx_assets_place         ON assets(place_id);
CREATE INDEX idx_assets_source        ON assets(source_id);
CREATE INDEX idx_assets_ingest        ON assets(ingest_id);
CREATE INDEX idx_assets_type          ON assets(asset_type);
CREATE INDEX idx_assets_status        ON assets(status);
CREATE INDEX idx_assets_checksum      ON assets(checksum_sha256);
CREATE INDEX idx_assets_workflow      ON assets(workflow_item_id);

-- ---------------------------------------------------------------------------
-- ingested_records
-- ---------------------------------------------------------------------------
CREATE INDEX idx_ingested_place       ON ingested_records(place_id);
CREATE INDEX idx_ingested_source      ON ingested_records(source);
CREATE INDEX idx_ingested_status      ON ingested_records(status);
CREATE INDEX idx_ingested_workflow    ON ingested_records(workflow_item_id);
