-- Core schema for Nature & Culture.
-- PostgreSQL is the sole authority for all pipeline state.

-- ---------------------------------------------------------------------------
-- Sources
-- ---------------------------------------------------------------------------

CREATE TABLE sources (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id           TEXT NOT NULL UNIQUE,           -- "unesco_whc", "wikidata"
    name                TEXT NOT NULL,
    description         TEXT,
    institution         TEXT,
    base_url            TEXT NOT NULL,
    fetch_strategy      TEXT NOT NULL,                  -- api | file | scrape
    auth_type           TEXT NOT NULL DEFAULT 'none',
    rate_limit          JSONB NOT NULL DEFAULT '{}',
    entity_types        TEXT[] NOT NULL DEFAULT '{}',
    standards           TEXT[] NOT NULL DEFAULT '{}',
    status              TEXT NOT NULL DEFAULT 'active',
    priority            INT NOT NULL DEFAULT 99,
    schema_version      TEXT,
    schema_path         TEXT,
    last_fetched_at     TIMESTAMPTZ,
    last_error          TEXT,
    config              JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Places
-- ---------------------------------------------------------------------------

CREATE TABLE places (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- External identifiers
    wikidata_qid        TEXT UNIQUE,
    geonames_id         TEXT,
    osm_relation_id     BIGINT,
    source_id           TEXT,
    source              TEXT REFERENCES sources(source_id),

    -- Names and descriptions — {lang: value}
    name                JSONB NOT NULL DEFAULT '{}',
    description         JSONB NOT NULL DEFAULT '{}',

    -- Classification
    heritage_type       TEXT,                           -- cultural | natural | mixed
    ouv_criteria        TEXT[] NOT NULL DEFAULT '{}',  -- ["i","ii","vii"]
    category_skos       TEXT[] NOT NULL DEFAULT '{}',  -- SKOS concept URIs

    -- Geography
    country_codes       TEXT[] NOT NULL DEFAULT '{}',  -- ISO 3166-1 alpha-2
    continent           TEXT,
    centroid            GEOMETRY(Point, 4326),
    boundary            GEOMETRY(Geometry, 4326),
    area_ha             DOUBLE PRECISION,

    -- Inscription
    inscription_year    INT,
    inscription_date    DATE,
    endangered_since    DATE,

    -- Status
    status              TEXT NOT NULL DEFAULT 'candidate',
    confidence_score    DOUBLE PRECISION,
    agent_notes         JSONB NOT NULL DEFAULT '{}',

    -- Audit
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Workflow Items
-- ---------------------------------------------------------------------------

CREATE TABLE workflow_items (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    capability          TEXT NOT NULL,
    entity_type         TEXT NOT NULL,
    entity_id           UUID NOT NULL,
    parent_item_id      UUID REFERENCES workflow_items(id),

    priority            INT NOT NULL DEFAULT 50,
    scheduled_at        TIMESTAMPTZ,

    status              TEXT NOT NULL DEFAULT 'pending',
    status_reason       TEXT,

    -- Worker execution
    worker_id           TEXT,
    started_at          TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    attempt             INT NOT NULL DEFAULT 1,
    max_attempts        INT NOT NULL DEFAULT 3,
    last_error          TEXT,

    -- Human review
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    rejection_reason    TEXT,
    review_notes        TEXT,

    agent_suggestions   JSONB NOT NULL DEFAULT '{}',
    context             JSONB NOT NULL DEFAULT '{}',

    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Discovery Candidates
-- ---------------------------------------------------------------------------

CREATE TABLE discovery_candidates (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_item_id    UUID REFERENCES workflow_items(id),

    source              TEXT NOT NULL REFERENCES sources(source_id),
    source_id           TEXT NOT NULL,
    wikidata_qid        TEXT,

    name                JSONB NOT NULL DEFAULT '{}',
    description         JSONB NOT NULL DEFAULT '{}',
    country_codes       TEXT[] NOT NULL DEFAULT '{}',
    heritage_type       TEXT,
    ouv_criteria        TEXT[] NOT NULL DEFAULT '{}',
    inscription_year    INT,
    centroid            GEOMETRY(Point, 4326),
    boundary            GEOMETRY(Geometry, 4326),

    confidence_score    DOUBLE PRECISION,
    agent_suggestions   JSONB NOT NULL DEFAULT '{}',

    status              TEXT NOT NULL DEFAULT 'pending',
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    rejection_reason    TEXT,

    -- promoted_place_id set when candidate is approved and Place created
    promoted_place_id   UUID REFERENCES places(id),

    provenance          JSONB NOT NULL DEFAULT '{}',
    discovered_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (source, source_id)
);

-- ---------------------------------------------------------------------------
-- Assets (MinIO artifact registry + PREMIS)
-- ---------------------------------------------------------------------------

CREATE TABLE assets (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id                UUID NOT NULL REFERENCES places(id),
    source_id               TEXT NOT NULL REFERENCES sources(source_id),
    ingest_id               TEXT NOT NULL,
    workflow_item_id        UUID REFERENCES workflow_items(id),

    asset_type              TEXT NOT NULL DEFAULT 'unknown',
    mime_type               TEXT,
    language                TEXT,                       -- ISO 639-1

    -- MinIO paths
    raw_path                TEXT,
    normalized_path         TEXT,

    -- Integrity
    checksum_sha256         TEXT,
    size_bytes              BIGINT,

    -- PREMIS
    premis_object_id        TEXT,
    premis_original_name    TEXT,
    premis_creating_application TEXT,

    status                  TEXT NOT NULL DEFAULT 'fetched',
    validation_warnings     TEXT[] NOT NULL DEFAULT '{}',
    schema_version          TEXT,

    source_url              TEXT,
    fetched_at              TIMESTAMPTZ,
    agent_notes             JSONB NOT NULL DEFAULT '{}',

    provenance              JSONB NOT NULL DEFAULT '{}',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Ingested Records
-- ---------------------------------------------------------------------------

CREATE TABLE ingested_records (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id            UUID NOT NULL REFERENCES places(id),
    workflow_item_id    UUID REFERENCES workflow_items(id),
    ingest_id           TEXT NOT NULL UNIQUE,
    source              TEXT NOT NULL REFERENCES sources(source_id),

    status              TEXT NOT NULL DEFAULT 'staged',
    artifact_count      INT NOT NULL DEFAULT 0,
    checksum_manifest   JSONB NOT NULL DEFAULT '{}',
    schema_version      TEXT,

    activated_by        TEXT,
    activated_at        TIMESTAMPTZ,

    provenance          JSONB NOT NULL DEFAULT '{}',
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Updated-at trigger (applies to all tables)
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'sources', 'places', 'workflow_items',
        'discovery_candidates', 'assets', 'ingested_records'
    ] LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_%s_updated_at
             BEFORE UPDATE ON %s
             FOR EACH ROW EXECUTE FUNCTION set_updated_at()',
            t, t
        );
    END LOOP;
END;
$$;
