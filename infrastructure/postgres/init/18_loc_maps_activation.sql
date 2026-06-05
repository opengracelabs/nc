-- LOC Maps proof-of-concept activation.
-- Scope: Library of Congress maps only.
-- Target: 1871 Hayden Survey Map / Yellowstone National Park, LOC item 97683567.
--
-- This migration is additive. It does not modify BHL acquisition, illustration
-- opportunities, collection constraints, or Collection #000001 readiness rules.

-- ---------------------------------------------------------------------------
-- 1. Register LOC
-- ---------------------------------------------------------------------------

INSERT INTO sources (
    source_id, name, institution, base_url, fetch_strategy,
    auth_type, priority, entity_types, standards, config, provenance
)
VALUES (
    'loc',
    'Library of Congress',
    'Library of Congress',
    'https://www.loc.gov',
    'api',
    'none',
    11,
    ARRAY['map','image','document'],
    ARRAY['dublin_core','mods','marcxml','iiif','premis','prov_o'],
    '{
      "api_endpoint": "https://www.loc.gov",
      "source_profile": "loc_maps",
      "iiif_base": "https://tile.loc.gov/image-services/iiif",
      "rate_limit": {"requests_per_second": 1, "burst": 3}
    }',
    '{"registered_for": "loc_maps_proof_of_concept"}'
)
ON CONFLICT (source_id) DO UPDATE SET
    name = EXCLUDED.name,
    institution = EXCLUDED.institution,
    base_url = EXCLUDED.base_url,
    fetch_strategy = EXCLUDED.fetch_strategy,
    auth_type = EXCLUDED.auth_type,
    entity_types = EXCLUDED.entity_types,
    standards = EXCLUDED.standards,
    config = EXCLUDED.config,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

-- ---------------------------------------------------------------------------
-- 2. Seed Yellowstone geographic concept
-- ---------------------------------------------------------------------------

INSERT INTO concepts (
    uri, label, description, type, status, provenance
)
VALUES (
    'nc:geo/yellowstone-national-park',
    '{"en": "Yellowstone National Park"}',
    '{"en": "Geographic concept used to anchor LOC map evidence for Yellowstone National Park."}',
    'geographic',
    'active',
    '{"seeded_for": "loc_maps_proof_of_concept"}'
)
ON CONFLICT (uri) DO UPDATE SET
    label = EXCLUDED.label,
    description = EXCLUDED.description,
    status = 'active',
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO concept_aliases (
    concept_id, alias, language, source, confidence_score
)
SELECT
    c.id,
    alias.alias,
    'en',
    'loc',
    0.980
FROM concepts c
CROSS JOIN (
    VALUES
        ('Yellowstone National Park'),
        ('United States--Wyoming--Yellowstone National Park'),
        ('Yellowstone')
) AS alias(alias)
WHERE c.uri = 'nc:geo/yellowstone-national-park'
ON CONFLICT (concept_id, alias, language) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 3. Migration 18 proof tables
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS loc_map_asset_candidates (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id           TEXT NOT NULL REFERENCES sources(source_id),
    source_profile_id   TEXT NOT NULL,
    source_adapter_id   TEXT NOT NULL,
    source_record_id    TEXT NOT NULL UNIQUE,
    loc_item_id         TEXT NOT NULL,
    loc_resource_id     TEXT NOT NULL,
    source_url          TEXT NOT NULL,
    resource_url        TEXT NOT NULL,
    asset_class         TEXT NOT NULL,
    asset_subclass      TEXT NOT NULL,
    title               JSONB NOT NULL DEFAULT '{}',
    description         JSONB NOT NULL DEFAULT '{}',
    date_display        TEXT,
    normalized_year     INT,
    source_native_ids   JSONB NOT NULL DEFAULT '{}',
    media               JSONB NOT NULL DEFAULT '{}',
    map_metadata        JSONB NOT NULL DEFAULT '{}',
    status              TEXT NOT NULL DEFAULT 'candidate',
    activated_asset_id  UUID REFERENCES assets(id),
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_loc_map_candidate_class CHECK (
        asset_class = 'map' AND asset_subclass = 'historic_map'
    ),
    CONSTRAINT chk_loc_map_candidate_status CHECK (
        status IN ('candidate','rights_review','approved','active','rejected')
    )
);

CREATE TABLE IF NOT EXISTS loc_map_rights_evidence (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_record_id      TEXT NOT NULL REFERENCES loc_map_asset_candidates(source_record_id) ON DELETE CASCADE,
    rights_extractor_id   TEXT NOT NULL,
    rights_status         TEXT NOT NULL,
    commercial_reuse      TEXT NOT NULL,
    rights_source_url     TEXT NOT NULL,
    rights_statement      TEXT NOT NULL,
    evidence              JSONB NOT NULL DEFAULT '{}',
    requires_human_review BOOLEAN NOT NULL DEFAULT TRUE,
    status                TEXT NOT NULL DEFAULT 'pending',
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_loc_map_rights_status CHECK (
        rights_status IN ('Public Domain','CC0','review_required','blocked')
    ),
    CONSTRAINT chk_loc_map_commercial_reuse CHECK (
        commercial_reuse IN ('allowed','review_required','blocked')
    ),
    CONSTRAINT chk_loc_map_rights_evidence_status CHECK (
        status IN ('pending','approved','rejected')
    ),
    UNIQUE (source_record_id, rights_extractor_id)
);

CREATE INDEX IF NOT EXISTS idx_loc_map_candidates_status
    ON loc_map_asset_candidates(status, updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_loc_map_candidates_source_record
    ON loc_map_asset_candidates(source_record_id);

CREATE INDEX IF NOT EXISTS idx_loc_map_rights_source_record
    ON loc_map_rights_evidence(source_record_id);

DROP TRIGGER IF EXISTS trg_loc_map_asset_candidates_updated_at ON loc_map_asset_candidates;
CREATE TRIGGER trg_loc_map_asset_candidates_updated_at
    BEFORE UPDATE ON loc_map_asset_candidates
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_loc_map_rights_evidence_updated_at ON loc_map_rights_evidence;
CREATE TRIGGER trg_loc_map_rights_evidence_updated_at
    BEFORE UPDATE ON loc_map_rights_evidence
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------------------
-- 4. Create Hayden Map candidate
-- ---------------------------------------------------------------------------

INSERT INTO loc_map_asset_candidates (
    source_id,
    source_profile_id,
    source_adapter_id,
    source_record_id,
    loc_item_id,
    loc_resource_id,
    source_url,
    resource_url,
    asset_class,
    asset_subclass,
    title,
    description,
    date_display,
    normalized_year,
    source_native_ids,
    media,
    map_metadata,
    status,
    provenance
)
VALUES (
    'loc',
    'loc_maps',
    'loc_maps_asset_adapter_v1',
    'loc:97683567',
    '97683567',
    'g4262y.ye000023',
    'https://www.loc.gov/item/97683567/',
    'https://www.loc.gov/resource/g4262y.ye000023/',
    'map',
    'historic_map',
    '{"en": "Yellowstone National Park : 1871"}',
    '{"en": "1871 LOC Geography and Map Division raster map associated with the Hayden survey context."}',
    '1871',
    1871,
    '{
      "loc_lccn": "97683567",
      "loc_digital_id": "http://hdl.loc.gov/loc.gmd/g4262y.ye000023",
      "loc_call_number": "G4262.Y4 1871 .U5 TIL"
    }',
    '{
      "iiif_image_service": "https://tile.loc.gov/image-services/iiif/service:gmd:gmd426:g4262:g4262y:ye000023",
      "iiif_info_json": "https://tile.loc.gov/image-services/iiif/service:gmd:gmd426:g4262:g4262y:ye000023/info.json",
      "master_tiff": "https://tile.loc.gov/storage-services/master/gmd/gmd426/g4262/g4262y/ye000023.tif",
      "jp2": "https://tile.loc.gov/storage-services/service/gmd/gmd426/g4262/g4262y/ye000023.jp2"
    }',
    '{
      "coverage_label": "Yellowstone National Park, Wyoming, United States",
      "georeferenced": false,
      "scale": null,
      "projection": null
    }',
    'candidate',
    '{
      "prov:wasGeneratedBy": "loc_maps_asset_adapter_v1",
      "prov:wasAttributedTo": "source:loc",
      "prov:used": "https://www.loc.gov/item/97683567/?fo=json"
    }'
)
ON CONFLICT (source_record_id) DO UPDATE SET
    status = 'candidate',
    updated_at = NOW();

-- ---------------------------------------------------------------------------
-- 5. Create rights evidence
-- ---------------------------------------------------------------------------

INSERT INTO loc_map_rights_evidence (
    source_record_id,
    rights_extractor_id,
    rights_status,
    commercial_reuse,
    rights_source_url,
    rights_statement,
    evidence,
    requires_human_review,
    status,
    provenance
)
VALUES (
    'loc:97683567',
    'loc_maps_rights_extractor_v1',
    'Public Domain',
    'allowed',
    'https://www.loc.gov/item/97683567/',
    'LOC Geography and Map Division rights text indicates Map Collection materials are free to use/reuse unless a Rights Advisory states otherwise; item date is 1871.',
    '{
      "item_date": "1871",
      "source_rights_field": "item.rights",
      "credit_line": "Library of Congress, Geography and Map Division.",
      "no_adverse_rights_advisory_found": true
    }',
    true,
    'approved',
    '{
      "prov:wasGeneratedBy": "loc_maps_rights_extractor_v1",
      "prov:wasAttributedTo": "source:loc"
    }'
)
ON CONFLICT (source_record_id, rights_extractor_id) DO UPDATE SET
    rights_status = EXCLUDED.rights_status,
    commercial_reuse = EXCLUDED.commercial_reuse,
    evidence = EXCLUDED.evidence,
    status = EXCLUDED.status,
    updated_at = NOW();

-- ---------------------------------------------------------------------------
-- 6. Activate asset
-- ---------------------------------------------------------------------------

WITH candidate AS (
    SELECT *
    FROM loc_map_asset_candidates
    WHERE source_record_id = 'loc:97683567'
),
rights AS (
    SELECT *
    FROM loc_map_rights_evidence
    WHERE source_record_id = 'loc:97683567'
      AND status = 'approved'
      AND rights_status = 'Public Domain'
),
existing_asset AS (
    SELECT a.id
    FROM assets a
    WHERE a.source_id = 'loc'
      AND a.ingest_id = 'loc_maps:97683567'
),
inserted_asset AS (
    INSERT INTO assets (
        concept_id,
        source_id,
        ingest_id,
        asset_type,
        mime_type,
        raw_path,
        normalized_path,
        checksum_sha256,
        size_bytes,
        status,
        source_url,
        fetched_at,
        premis_object_id,
        premis_original_name,
        premis_creating_application,
        provenance
    )
    SELECT
        c_geo.id,
        'loc',
        'loc_maps:97683567',
        'unknown',
        'image/tiff',
        'raw/loc/maps/loc_maps:97683567/97683567/ye000023.tif',
        'normalized/loc/maps/loc_maps:97683567/97683567/canonical_asset_record.json',
        NULL,
        NULL,
        'active',
        candidate.source_url,
        NOW(),
        'loc:maps:97683567',
        'ye000023.tif',
        'loc_maps_asset_adapter_v1',
        jsonb_build_object(
            'asset_class', 'map',
            'asset_subclass', 'historic_map',
            'source_profile_id', 'loc_maps',
            'source_adapter_id', 'loc_maps_asset_adapter_v1',
            'source_record_id', 'loc:97683567',
            'loc_item_id', '97683567',
            'loc_resource_id', 'g4262y.ye000023',
            'rights_extractor_id', 'loc_maps_rights_extractor_v1',
            'prov:wasGeneratedBy', 'loc_maps_asset_adapter_v1',
            'prov:wasAttributedTo', 'source:loc'
        )
    FROM candidate
    JOIN rights ON rights.source_record_id = candidate.source_record_id
    JOIN concepts c_geo ON c_geo.uri = 'nc:geo/yellowstone-national-park'
    WHERE NOT EXISTS (SELECT 1 FROM existing_asset)
    RETURNING id
),
asset_to_activate AS (
    SELECT id FROM inserted_asset
    UNION ALL
    SELECT id FROM existing_asset
)
UPDATE loc_map_asset_candidates
SET status = 'active',
    activated_asset_id = asset_to_activate.id,
    updated_at = NOW()
FROM asset_to_activate
WHERE loc_map_asset_candidates.source_record_id = 'loc:97683567';

-- Deliberately no insert into collection_assets. Collection #000001 remains
-- constrained to verified Public Domain/CC0 BHL illustration assets.
