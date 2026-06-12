-- NC-PILOT-001 runtime.
-- Pilot anchor registry, ingest-run state, anchor-place links, evidence links,
-- publication snapshots, and attribution metadata.
--
-- No source onboarding.
-- No external HTTP.
-- No media ingestion.
-- No OSM-derived canonical writes.

CREATE TABLE IF NOT EXISTS pilot_anchor_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO pilot_anchor_status_vocabulary (value, description, sort_order)
VALUES
    ('draft', 'Pilot anchor is registered but not public.', 10),
    ('active', 'Pilot anchor is active for internal pilot APIs.', 20),
    ('partial_launch', 'Pilot anchor may publish editorial discovery pages but cannot publish commerce or unratified assets.', 25),
    ('published', 'Pilot anchor has a publication snapshot.', 30),
    ('retired', 'Pilot anchor is no longer active.', 40)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS pilot_ingest_run_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO pilot_ingest_run_status_vocabulary (value, description, sort_order)
VALUES
    ('planned', 'Run is planned but has not started.', 10),
    ('started', 'Run has started.', 20),
    ('fetching', 'External reads are in progress outside DB transactions.', 30),
    ('normalizing', 'Fetched payloads are being normalized.', 40),
    ('committing', 'Short DB upsert transaction is in progress.', 50),
    ('completed', 'Run completed successfully.', 60),
    ('stale', 'Run exceeded its stale threshold and requires recovery.', 70),
    ('failed', 'Run failed and requires review.', 80),
    ('abandoned', 'Run was abandoned after recovery review.', 90)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS pilot_anchor (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug                       TEXT NOT NULL UNIQUE,
    title                      TEXT NOT NULL,
    anchor_type                TEXT NOT NULL CHECK (anchor_type IN ('place','asset','mission')),
    status                     TEXT NOT NULL DEFAULT 'active' REFERENCES pilot_anchor_status_vocabulary(value),
    canonical_identity         JSONB NOT NULL DEFAULT '{}',
    source_map                 JSONB NOT NULL DEFAULT '{}',
    attribution_requirements   JSONB NOT NULL DEFAULT '{}',
    sort_order                 INT NOT NULL UNIQUE,
    provenance                 JSONB NOT NULL DEFAULT '{}',
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_pilot_anchor_slug CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    CONSTRAINT chk_pilot_anchor_identity CHECK (canonical_identity <> '{}'::jsonb),
    CONSTRAINT chk_pilot_anchor_source_map CHECK (source_map <> '{}'::jsonb)
);

CREATE TABLE IF NOT EXISTS pilot_ingest_run (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    anchor_id             UUID NOT NULL REFERENCES pilot_anchor(id) ON DELETE CASCADE,
    idempotency_key       TEXT NOT NULL,
    status                TEXT NOT NULL DEFAULT 'planned' REFERENCES pilot_ingest_run_status_vocabulary(value),
    source_scope          TEXT[] NOT NULL DEFAULT '{}',
    phase                 TEXT NOT NULL DEFAULT 'planned',
    stale_after           TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '2 hours',
    started_at            TIMESTAMPTZ,
    completed_at          TIMESTAMPTZ,
    raw_payload_refs      JSONB NOT NULL DEFAULT '{}',
    normalized_refs       JSONB NOT NULL DEFAULT '{}',
    error                 JSONB NOT NULL DEFAULT '{}',
    recovery_notes        JSONB NOT NULL DEFAULT '{}',
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (anchor_id, idempotency_key),
    CONSTRAINT chk_pilot_ingest_run_idempotency CHECK (length(idempotency_key) > 0),
    CONSTRAINT chk_pilot_ingest_run_no_http CHECK (
        provenance::text !~* '(http_client|requests\.|httpx\.|urllib|external fetch inside transaction)'
    ),
    CONSTRAINT chk_pilot_ingest_run_completed_at CHECK (
        status <> 'completed' OR completed_at IS NOT NULL
    )
);

CREATE TABLE IF NOT EXISTS anchor_place (
    id                 UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    anchor_id          UUID NOT NULL REFERENCES pilot_anchor(id) ON DELETE CASCADE,
    place_id           UUID REFERENCES places(id) ON DELETE SET NULL,
    role               TEXT NOT NULL DEFAULT 'primary' CHECK (
        role IN ('primary','secondary','context','asset_subject')
    ),
    identity_snapshot  JSONB NOT NULL DEFAULT '{}',
    provenance         JSONB NOT NULL DEFAULT '{}',
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (anchor_id, place_id, role),
    CONSTRAINT chk_anchor_place_identity_present CHECK (
        place_id IS NOT NULL OR identity_snapshot <> '{}'::jsonb
    ),
    CONSTRAINT chk_anchor_place_no_osm_storage CHECK (
        identity_snapshot::text !~* '(osm_relation_id|osm_id|openstreetmap|overpass)'
        AND provenance::text !~* '(osm_relation_id|osm_id|openstreetmap|overpass)'
    )
);

CREATE TABLE IF NOT EXISTS anchor_evidence (
    id                 UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    anchor_id          UUID NOT NULL REFERENCES pilot_anchor(id) ON DELETE CASCADE,
    source             TEXT NOT NULL,
    source_role        TEXT NOT NULL CHECK (
        source_role IN (
            'place_identity','context_only','validation_only',
            'primary_discovery','source_asset','canonical_asset','support'
        )
    ),
    evidence_type      TEXT NOT NULL,
    source_record_id   TEXT,
    source_url         TEXT,
    rights_decision    TEXT CHECK (
        rights_decision IN ('ALLOWED','REVIEW_REQUIRED','BLOCKED')
        OR rights_decision IS NULL
    ),
    raw_payload_hash   TEXT NOT NULL,
    evidence           JSONB NOT NULL DEFAULT '{}',
    attribution        JSONB NOT NULL DEFAULT '{}',
    status             TEXT NOT NULL DEFAULT 'current' CHECK (
        status IN ('current','stale','superseded','blocked')
    ),
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (anchor_id, source, raw_payload_hash),
    CONSTRAINT chk_anchor_evidence_hash CHECK (raw_payload_hash ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_anchor_evidence_no_osm_vectors CHECK (
        evidence::text !~* '(osm_geometry|osm_relation_id|osm_id|overpass|way_id|node_id)'
    )
);

CREATE TABLE IF NOT EXISTS pilot_publication_snapshot (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    anchor_id             UUID NOT NULL REFERENCES pilot_anchor(id) ON DELETE CASCADE,
    snapshot_version      TEXT NOT NULL,
    publication_status    TEXT NOT NULL DEFAULT 'draft' CHECK (
        publication_status IN ('draft','published','stale','retracted')
    ),
    snapshot              JSONB NOT NULL,
    attribution           JSONB NOT NULL DEFAULT '{}',
    snapshot_sha256       TEXT NOT NULL,
    created_by            TEXT NOT NULL,
    published_at          TIMESTAMPTZ,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (anchor_id, snapshot_version),
    UNIQUE (snapshot_sha256),
    CONSTRAINT chk_pilot_publication_snapshot_hash CHECK (snapshot_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_pilot_publication_snapshot_body CHECK (snapshot <> '{}'::jsonb),
    CONSTRAINT chk_pilot_publication_snapshot_actor CHECK (length(created_by) > 0)
);

CREATE TABLE IF NOT EXISTS pilot_launch_config (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key       TEXT NOT NULL UNIQUE,
    enabled          BOOLEAN NOT NULL DEFAULT FALSE,
    launch_stage     TEXT NOT NULL CHECK (
        launch_stage IN ('draft','activation','launched','paused')
    ),
    required_gates   TEXT[] NOT NULL DEFAULT '{}',
    monitor_window_minutes INT NOT NULL DEFAULT 120 CHECK (monitor_window_minutes > 0),
    snapshot_policy  JSONB NOT NULL DEFAULT '{}',
    provenance       JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_pilot_launch_config_key CHECK (
        config_key ~ '^[a-z0-9]+(?:_[a-z0-9]+)*$'
    )
);

CREATE TABLE IF NOT EXISTS pilot_publication_checklist (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    checklist_key    TEXT NOT NULL UNIQUE,
    label            TEXT NOT NULL,
    gate             TEXT NOT NULL CHECK (
        gate IN ('rights','source_authority','attribution','identity','review')
    ),
    required         BOOLEAN NOT NULL DEFAULT TRUE,
    sort_order       INT NOT NULL UNIQUE,
    provenance       JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_pilot_publication_checklist_key CHECK (
        checklist_key ~ '^[a-z0-9]+(?:_[a-z0-9]+)*$'
    )
);

CREATE INDEX IF NOT EXISTS idx_pilot_anchor_status ON pilot_anchor(status, sort_order);
CREATE INDEX IF NOT EXISTS idx_pilot_ingest_run_anchor_status ON pilot_ingest_run(anchor_id, status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_anchor_place_anchor ON anchor_place(anchor_id, role);
CREATE INDEX IF NOT EXISTS idx_anchor_evidence_anchor_source ON anchor_evidence(anchor_id, source, status);
CREATE INDEX IF NOT EXISTS idx_pilot_publication_snapshot_anchor ON pilot_publication_snapshot(anchor_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pilot_publication_checklist_gate ON pilot_publication_checklist(gate, sort_order);
CREATE INDEX IF NOT EXISTS idx_pilot_launch_config_stage ON pilot_launch_config(launch_stage, enabled);

DROP TRIGGER IF EXISTS trg_pilot_anchor_updated_at ON pilot_anchor;
CREATE TRIGGER trg_pilot_anchor_updated_at BEFORE UPDATE ON pilot_anchor FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_pilot_ingest_run_updated_at ON pilot_ingest_run;
CREATE TRIGGER trg_pilot_ingest_run_updated_at BEFORE UPDATE ON pilot_ingest_run FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_anchor_place_updated_at ON anchor_place;
CREATE TRIGGER trg_anchor_place_updated_at BEFORE UPDATE ON anchor_place FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_anchor_evidence_updated_at ON anchor_evidence;
CREATE TRIGGER trg_anchor_evidence_updated_at BEFORE UPDATE ON anchor_evidence FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_pilot_publication_checklist_updated_at ON pilot_publication_checklist;
CREATE TRIGGER trg_pilot_publication_checklist_updated_at BEFORE UPDATE ON pilot_publication_checklist FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_pilot_launch_config_updated_at ON pilot_launch_config;
CREATE TRIGGER trg_pilot_launch_config_updated_at BEFORE UPDATE ON pilot_launch_config FOR EACH ROW EXECUTE FUNCTION set_updated_at();

INSERT INTO pilot_launch_config (
    config_key, enabled, launch_stage, required_gates,
    monitor_window_minutes, snapshot_policy, provenance
)
VALUES (
    'nc_pilot_001_activation', TRUE, 'activation',
    ARRAY[
        'rights_verified_pd',
        'human_verified',
        'source_authority_active',
        'nasa_noaa_nonendorsement',
        'geonames_attribution',
        'osm_attribution',
        'geonames_id_written',
        'two_human_signoff'
    ]::text[],
    120,
    '{"require_snapshot_hash":true,"require_attribution":true,"allow_partial_launch_status":["partial_launch"],"publication_statuses":["draft","published"]}'::jsonb,
    '{"document":"NC-PILOT-001 Activation Sprint","rule":"metadata-only launch configuration; no source onboarding"}'::jsonb
)
ON CONFLICT (config_key) DO UPDATE SET
    enabled = EXCLUDED.enabled,
    launch_stage = EXCLUDED.launch_stage,
    required_gates = EXCLUDED.required_gates,
    monitor_window_minutes = EXCLUDED.monitor_window_minutes,
    snapshot_policy = EXCLUDED.snapshot_policy,
    provenance = pilot_launch_config.provenance || EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO pilot_anchor (
    slug, title, anchor_type, status, canonical_identity,
    source_map, attribution_requirements, sort_order, provenance
)
VALUES
    ('yellowstone', 'Yellowstone', 'place', 'active',
     '{"kind":"place","preferred_geonames_id":"5843591","preferred_wikidata_qid":"Q351","country_codes":["US"]}'::jsonb,
     '{"geonames":"canonical","wikidata":"context_only","gbif":"validation_only","nasa":"support","noaa":"support","nara":"support","bhl":"primary_discovery","museums":"support"}'::jsonb,
     '{"geonames":true,"osm_tiles":false,"source_specific":true}'::jsonb, 10,
     '{"document":"NC-PILOT-001","seeded":true}'::jsonb),
    ('grand-canyon', 'Grand Canyon', 'place', 'active',
     '{"kind":"place","preferred_geonames_id":"5296401","preferred_wikidata_qid":"Q220289","country_codes":["US"]}'::jsonb,
     '{"geonames":"canonical","wikidata":"context_only","gbif":"validation_only","nasa":"source_asset","noaa":"support","nara":"source_asset","bhl":"validation_only","museums":"source_asset"}'::jsonb,
     '{"geonames":true,"osm_tiles":false,"source_specific":true}'::jsonb, 20,
     '{"document":"NC-PILOT-001","seeded":true}'::jsonb),
    ('great-barrier-reef', 'Great Barrier Reef', 'place', 'active',
     '{"kind":"place","preferred_geonames_id":"2164628","preferred_wikidata_qid":"Q7343","country_codes":["AU"]}'::jsonb,
     '{"geonames":"canonical","wikidata":"context_only","gbif":"validation_only","nasa":"support","noaa":"source_asset","nara":"support","bhl":"primary_discovery","museums":"support"}'::jsonb,
     '{"geonames":true,"osm_tiles":false,"source_specific":true}'::jsonb, 30,
     '{"document":"NC-PILOT-001","seeded":true}'::jsonb),
    ('papahanaumokuakea', 'Papahanaumokuakea', 'place', 'active',
     '{"kind":"place","preferred_wikidata_qid":"Q787425","country_codes":["US"],"diacritics":"Papahānaumokuākea","geonames_status":"unconfirmed"}'::jsonb,
     '{"geonames":"canonical_candidate","wikidata":"context_only","gbif":"validation_only","nasa":"support","noaa":"primary_discovery","nara":"support","bhl":"validation_only","museums":"support"}'::jsonb,
     '{"geonames":false,"osm_tiles":false,"source_specific":true}'::jsonb, 40,
     '{"document":"NC-PILOT-001","seeded":true}'::jsonb),
    ('venice', 'Venice', 'place', 'partial_launch',
     '{"kind":"place","preferred_geonames_id":"3164603","preferred_wikidata_qid":"Q641","country_codes":["IT"]}'::jsonb,
     '{"geonames":"canonical","wikidata":"context_only","gbif":"low_relevance","nasa":"support","noaa":"support","nara":"support","bhl":"low_relevance","museums":"primary_discovery"}'::jsonb,
     '{"geonames":true,"osm_tiles":false,"source_specific":true}'::jsonb, 50,
     '{"document":"NC-PILOT-001","seeded":true,"partial_launch_reason":"museum DD incomplete; editorial-only until rights and source authority gates pass","excluded_assets":["copernicus_sentinel_2_lagoon_esa_only"]}'::jsonb),
    ('galapagos', 'Galapagos', 'place', 'active',
     '{"kind":"place","preferred_geonames_id":"3658931","preferred_wikidata_qid":"Q38095","country_codes":["EC"],"diacritics":"Galápagos"}'::jsonb,
     '{"geonames":"canonical","wikidata":"context_only","gbif":"validation_only","nasa":"support","noaa":"support","nara":"support","bhl":"primary_discovery","museums":"support"}'::jsonb,
     '{"geonames":true,"osm_tiles":false,"source_specific":true}'::jsonb, 60,
     '{"document":"NC-PILOT-001","seeded":true}'::jsonb),
    ('earthrise', 'Earthrise', 'asset', 'active',
     '{"kind":"asset_anchor","canonical_source":"nasa","mission":"Apollo 8","place_required":false}'::jsonb,
     '{"geonames":"not_primary","wikidata":"context_only","gbif":"none","nasa":"canonical_asset","noaa":"none","nara":"support","bhl":"none","museums":"support"}'::jsonb,
     '{"geonames":false,"osm_tiles":false,"source_specific":true}'::jsonb, 70,
     '{"document":"NC-PILOT-001","seeded":true}'::jsonb)
ON CONFLICT (slug) DO UPDATE SET
    title = EXCLUDED.title,
    anchor_type = EXCLUDED.anchor_type,
    status = EXCLUDED.status,
    canonical_identity = EXCLUDED.canonical_identity,
    source_map = EXCLUDED.source_map,
    attribution_requirements = EXCLUDED.attribution_requirements,
    sort_order = EXCLUDED.sort_order,
    provenance = pilot_anchor.provenance || EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO pilot_publication_checklist (
    checklist_key, label, gate, required, sort_order, provenance
)
VALUES
    ('rights_verified_pd', 'rights_status = verified_pd', 'rights', TRUE, 10,
     '{"document":"NC-PILOT-001 final readiness review","section":"V"}'::jsonb),
    ('human_verified', 'human_verified = TRUE', 'review', TRUE, 20,
     '{"document":"NC-PILOT-001 final readiness review","section":"V"}'::jsonb),
    ('source_authority_active', 'Source institution DD ratified and active', 'source_authority', TRUE, 30,
     '{"document":"NC-PILOT-001 final readiness review","section":"V"}'::jsonb),
    ('nasa_noaa_nonendorsement', 'NASA/NOAA nonendorsement copy present when used', 'attribution', TRUE, 40,
     '{"nasa":"Image credit: NASA. NASA does not endorse this product.","noaa":"Image: NOAA. NOAA does not endorse this product."}'::jsonb),
    ('geonames_attribution', 'GeoNames attribution present when geonames_id is used', 'attribution', TRUE, 50,
     '{"statement":"Geographic data © GeoNames (geonames.org) — CC BY 4.0"}'::jsonb),
    ('osm_attribution', 'OSM attribution present when OSM tiles are displayed', 'attribution', TRUE, 60,
     '{"statement":"© OpenStreetMap contributors"}'::jsonb),
    ('geonames_id_written', 'geonames_id written for canonical place anchors', 'identity', TRUE, 70,
     '{"document":"NC-PILOT-001 canonical place identity"}'::jsonb),
    ('two_human_signoff', 'Two-human sign-off recorded before publication', 'review', TRUE, 80,
     '{"document":"NC-PILOT-001 final readiness review","section":"V"}'::jsonb)
ON CONFLICT (checklist_key) DO UPDATE SET
    label = EXCLUDED.label,
    gate = EXCLUDED.gate,
    required = EXCLUDED.required,
    sort_order = EXCLUDED.sort_order,
    provenance = pilot_publication_checklist.provenance || EXCLUDED.provenance,
    updated_at = NOW();

