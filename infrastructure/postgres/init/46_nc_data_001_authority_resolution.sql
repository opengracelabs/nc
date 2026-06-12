-- NC-DATA-001 authority resolution registry.
-- One canonical place identity per anchor; multiple authority records allowed.

CREATE TABLE IF NOT EXISTS authority_resolution_registry (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    anchor_slug           TEXT NOT NULL,
    authority             TEXT NOT NULL CHECK (authority IN ('geonames','wikidata','gbif')),
    authority_record_id   TEXT NOT NULL,
    authority_role        TEXT NOT NULL CHECK (
        authority_role IN ('canonical_place_id','cross_reference','validation_only')
    ),
    confidence            NUMERIC(5,4) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    evidence              JSONB NOT NULL DEFAULT '{}',
    status                TEXT NOT NULL DEFAULT 'active' CHECK (
        status IN ('active','superseded','rejected')
    ),
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (anchor_slug, authority, authority_record_id),
    CONSTRAINT chk_authority_resolution_evidence CHECK (evidence <> '{}'::jsonb),
    CONSTRAINT chk_authority_resolution_no_gbif_canonical CHECK (
        NOT (authority = 'gbif' AND authority_role = 'canonical_place_id')
    ),
    CONSTRAINT chk_authority_resolution_no_wikidata_canonical CHECK (
        NOT (authority = 'wikidata' AND authority_role = 'canonical_place_id')
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_authority_resolution_one_canonical_place
    ON authority_resolution_registry(anchor_slug)
    WHERE authority_role = 'canonical_place_id' AND status = 'active';

CREATE TABLE IF NOT EXISTS canonical_identity (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    anchor_slug           TEXT NOT NULL UNIQUE,
    canonical_place_id    TEXT NOT NULL UNIQUE,
    canonical_authority   TEXT NOT NULL CHECK (canonical_authority IN ('geonames')),
    label                 TEXT NOT NULL,
    geonames_id           TEXT,
    wikidata_qid          TEXT,
    gbif_place_key        TEXT,
    identity              JSONB NOT NULL DEFAULT '{}',
    authority_record_ids  JSONB NOT NULL DEFAULT '[]',
    status                TEXT NOT NULL DEFAULT 'active' CHECK (
        status IN ('active','superseded','rejected')
    ),
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_canonical_identity_body CHECK (identity <> '{}'::jsonb),
    CONSTRAINT chk_canonical_identity_records CHECK (
        jsonb_array_length(authority_record_ids) > 0
    ),
    CONSTRAINT chk_canonical_identity_geonames CHECK (
        canonical_place_id = 'geonames:' || geonames_id
    )
);

CREATE INDEX IF NOT EXISTS idx_authority_resolution_anchor
    ON authority_resolution_registry(anchor_slug, authority, status);
CREATE INDEX IF NOT EXISTS idx_canonical_identity_anchor_status
    ON canonical_identity(anchor_slug, status);

DROP TRIGGER IF EXISTS trg_authority_resolution_registry_updated_at
    ON authority_resolution_registry;
CREATE TRIGGER trg_authority_resolution_registry_updated_at
BEFORE UPDATE ON authority_resolution_registry
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_canonical_identity_updated_at ON canonical_identity;
CREATE TRIGGER trg_canonical_identity_updated_at
BEFORE UPDATE ON canonical_identity
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

INSERT INTO authority_resolution_registry (
    anchor_slug, authority, authority_record_id, authority_role,
    confidence, evidence, status, provenance
)
VALUES
    (
        'yellowstone', 'geonames', '5843591', 'canonical_place_id',
        1.0000,
        '{"name":"Yellowstone National Park","feature_code":"PRKA","source_url":"https://www.geonames.org/5843591","resolution":"canonical"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-001","decision":"one canonical place ID only"}'::jsonb
    ),
    (
        'yellowstone', 'wikidata', 'Q351', 'cross_reference',
        0.9200,
        '{"label":"Yellowstone National Park","geonames_id_claim":"5844046","source_url":"https://www.wikidata.org/wiki/Q351","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-001","decision":"not canonical"}'::jsonb
    ),
    (
        'yellowstone', 'gbif', 'yellowstone-place-validation', 'validation_only',
        0.7500,
        '{"source_role":"validation_only","media_allowed":false,"resolution":"biodiversity relevance evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-001","decision":"not canonical"}'::jsonb
    )
ON CONFLICT (anchor_slug, authority, authority_record_id) DO UPDATE SET
    authority_role = EXCLUDED.authority_role,
    confidence = EXCLUDED.confidence,
    evidence = EXCLUDED.evidence,
    status = EXCLUDED.status,
    provenance = authority_resolution_registry.provenance || EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO canonical_identity (
    anchor_slug, canonical_place_id, canonical_authority, label,
    geonames_id, wikidata_qid, gbif_place_key, identity,
    authority_record_ids, status, provenance
)
VALUES (
    'yellowstone',
    'geonames:5843591',
    'geonames',
    'Yellowstone National Park',
    '5843591',
    'Q351',
    'yellowstone-place-validation',
    '{"canonical_place_id":"geonames:5843591","anchor_slug":"yellowstone","label":"Yellowstone National Park","geonames_id":"5843591","wikidata_qid":"Q351","gbif_place_key":"yellowstone-place-validation"}'::jsonb,
    '[
        {"authority":"geonames","authority_record_id":"5843591","role":"canonical_place_id"},
        {"authority":"wikidata","authority_record_id":"Q351","role":"cross_reference"},
        {"authority":"gbif","authority_record_id":"yellowstone-place-validation","role":"validation_only"}
    ]'::jsonb,
    'active',
    '{"authority":"NC-DATA-001","rule":"one canonical place ID only"}'::jsonb
)
ON CONFLICT (anchor_slug) DO UPDATE SET
    canonical_place_id = EXCLUDED.canonical_place_id,
    canonical_authority = EXCLUDED.canonical_authority,
    label = EXCLUDED.label,
    geonames_id = EXCLUDED.geonames_id,
    wikidata_qid = EXCLUDED.wikidata_qid,
    gbif_place_key = EXCLUDED.gbif_place_key,
    identity = EXCLUDED.identity,
    authority_record_ids = EXCLUDED.authority_record_ids,
    status = EXCLUDED.status,
    provenance = canonical_identity.provenance || EXCLUDED.provenance,
    updated_at = NOW();
