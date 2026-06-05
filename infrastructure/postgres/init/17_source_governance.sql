-- Migration 17: Source governance lifecycle.
--
-- Separates governance state (human-managed lifecycle) from operational status
-- (system-monitored health). The existing `status` column remains for backward
-- compatibility with workers that have not yet been updated.
--
-- governance_state is the authoritative gate for commercial pipeline access.
-- Workers MUST check governance_state = 'active' before ingesting or ranking.

-- ---------------------------------------------------------------------------
-- Governance fields
-- ---------------------------------------------------------------------------

ALTER TABLE sources
    ADD COLUMN IF NOT EXISTS governance_state TEXT NOT NULL DEFAULT 'proposed'
        CONSTRAINT chk_source_governance_state CHECK (governance_state IN (
            'proposed',     -- registered, under review, no ingestion permitted
            'approved',     -- human-approved, adapter in development
            'active',       -- adapter validated, ingestion permitted
            'suspended',    -- temporarily halted, rights or legal review
            'deprecated',   -- replaced by another source, no new ingestion
            'retired'       -- permanently removed from pipeline
        ));

ALTER TABLE sources
    ADD COLUMN IF NOT EXISTS operational_status TEXT NOT NULL DEFAULT 'unavailable'
        CONSTRAINT chk_source_operational_status CHECK (operational_status IN (
            'healthy',      -- last fetch succeeded within expected window
            'degraded',     -- reachable but returning errors or partial data
            'unavailable'   -- unreachable or no fetch attempted yet
        ));

-- ---------------------------------------------------------------------------
-- Backfill: all existing seeded sources are live production sources.
-- governance_state = 'active'; operational_status = 'healthy'.
-- ---------------------------------------------------------------------------

UPDATE sources
SET
    governance_state   = 'active',
    operational_status = 'healthy'
WHERE source_id IN (
    'unesco_whc',
    'unesco_ich',
    'wikidata',
    'wikimedia_commons',
    'osm',
    'geonames',
    'gbif',
    'iucn',
    'europeana',
    'bhl'
);

-- ---------------------------------------------------------------------------
-- Gate 1: Register Library of Congress.
-- governance_state = 'proposed'. No ingestion permitted until Gate 2 schema
-- work is complete and Gate 3 adapter is validated.
-- ---------------------------------------------------------------------------

INSERT INTO sources (
    source_id,
    name,
    institution,
    base_url,
    fetch_strategy,
    auth_type,
    priority,
    entity_types,
    standards,
    governance_state,
    operational_status,
    status,
    config
)
VALUES (
    'loc',
    'Library of Congress',
    'Library of Congress',
    'https://www.loc.gov',
    'api',
    'none',
    7,
    ARRAY['cartographic_record'],
    ARRAY['premis', 'prov_o', 'cidoc_crm', 'schema_org'],
    'proposed',
    'unavailable',
    'active',
    '{
        "api_endpoint": "https://www.loc.gov/search/",
        "item_endpoint": "https://www.loc.gov/{item_id}/?fo=json",
        "iiif_endpoint": "https://tile.loc.gov/image-services/iiif",
        "scope": "public_domain_cartographic",
        "divisions": ["geography_and_map"],
        "profiles": ["loc_maps"],
        "rights_strategy": "date_based_pre_1928",
        "rights_fallback": "loc_rights_statement",
        "rate_limit": {"requests_per_second": 1, "burst": 5, "timeout_seconds": 30}
    }'::jsonb
)
ON CONFLICT (source_id) DO NOTHING;
