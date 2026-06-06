-- v0.5.4 Phase 1 / Migration 33.
-- Creator authority, creator prestige, and Asset Intelligence audit log.
--
-- PostgreSQL is authoritative.
-- Replay-safe by immutable registry snapshots and append-only audit.
-- Versioned registries.
-- No Commerce Intelligence formula redesign.
-- No Product Routing redesign.
-- No Catalog redesign.
-- No Publication redesign.

CREATE TABLE IF NOT EXISTS creator_authority_registry (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registry_version      TEXT NOT NULL,
    canonical_creator_key TEXT NOT NULL,
    display_name          TEXT NOT NULL,
    normalized_names      TEXT[] NOT NULL DEFAULT '{}',
    external_authorities  JSONB NOT NULL DEFAULT '{}',
    creator_roles         TEXT[] NOT NULL DEFAULT '{}',
    authority_confidence  NUMERIC(4,3) NOT NULL CHECK (authority_confidence BETWEEN 0 AND 1),
    attribution_risk      TEXT NOT NULL CHECK (attribution_risk IN ('low','medium','high','unknown')),
    status                TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by           TEXT NOT NULL,
    approved_by           TEXT,
    approved_at           TIMESTAMPTZ,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (registry_version, canonical_creator_key),
    CONSTRAINT chk_creator_authority_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);

CREATE TABLE IF NOT EXISTS creator_authority_aliases (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_authority_id  UUID NOT NULL REFERENCES creator_authority_registry(id) ON DELETE CASCADE,
    alias                 TEXT NOT NULL,
    normalized_alias      TEXT NOT NULL,
    alias_source          TEXT NOT NULL,
    confidence_score      NUMERIC(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (creator_authority_id, normalized_alias)
);

CREATE TABLE IF NOT EXISTS creator_prestige_registry (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registry_version        TEXT NOT NULL,
    creator_authority_id    UUID NOT NULL REFERENCES creator_authority_registry(id),
    prestige_score          NUMERIC(4,3) NOT NULL CHECK (prestige_score BETWEEN 0 AND 1),
    prestige_tier           TEXT NOT NULL CHECK (prestige_tier IN ('master','major','notable','standard','none')),
    prestige_rationale      TEXT NOT NULL,
    applies_to_anchor_types TEXT[] NOT NULL DEFAULT ARRAY['biological','geographic','cultural'],
    status                  TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by             TEXT NOT NULL,
    approved_by             TEXT,
    approved_at             TIMESTAMPTZ,
    provenance              JSONB NOT NULL DEFAULT '{}',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (registry_version, creator_authority_id),
    CONSTRAINT chk_creator_prestige_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);

CREATE TABLE IF NOT EXISTS asset_intelligence_signal_snapshots (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id        UUID NOT NULL REFERENCES illustration_opportunities(id),
    resolved_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_by           TEXT NOT NULL,
    registry_version_set  JSONB NOT NULL,
    anchor_type           TEXT REFERENCES commerce_anchor_type_vocabulary(value),
    creator_authority_id  UUID REFERENCES creator_authority_registry(id),
    creator_prestige_id   UUID REFERENCES creator_prestige_registry(id),
    place_iconic_taxa_id  UUID,
    resolved_signals      JSONB NOT NULL,
    input_snapshot        JSONB NOT NULL,
    input_hash_sha256     TEXT NOT NULL,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (opportunity_id, input_hash_sha256),
    CONSTRAINT chk_asset_intelligence_snapshot_hash CHECK (input_hash_sha256 ~ '^[0-9a-f]{64}$')
);

CREATE TABLE IF NOT EXISTS asset_intelligence_audit_log (
    id                       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id           UUID REFERENCES illustration_opportunities(id),
    signal_snapshot_id       UUID REFERENCES asset_intelligence_signal_snapshots(id),
    event_type               TEXT NOT NULL CHECK (event_type IN (
        'creator_authority_resolved',
        'creator_prestige_resolved',
        'place_iconic_taxa_resolved',
        'anchor_type_resolved',
        'registry_activated',
        'recompute_requested',
        'recompute_completed',
        'replay_verified',
        'replay_failed'
    )),
    event_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor_type               TEXT NOT NULL REFERENCES commerce_actor_type_vocabulary(value),
    actor_id                 TEXT NOT NULL,
    registry_version_set     JSONB NOT NULL DEFAULT '{}',
    input_snapshot           JSONB NOT NULL DEFAULT '{}',
    output_snapshot          JSONB NOT NULL DEFAULT '{}',
    previous_state           JSONB NOT NULL DEFAULT '{}',
    new_state                JSONB NOT NULL DEFAULT '{}',
    entry_checksum_sha256    TEXT NOT NULL,
    previous_entry_checksum  TEXT,
    reason                   TEXT NOT NULL,
    generated_by             TEXT NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_asset_intelligence_audit_checksum CHECK (entry_checksum_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_asset_intelligence_audit_previous_checksum CHECK (
        previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'
    ),
    CONSTRAINT chk_asset_intelligence_audit_checksum_distinct CHECK (
        previous_entry_checksum IS NULL OR previous_entry_checksum <> entry_checksum_sha256
    ),
    CONSTRAINT chk_asset_intelligence_audit_actor CHECK (length(actor_id) > 0),
    CONSTRAINT chk_asset_intelligence_audit_reason CHECK (length(reason) > 0),
    CONSTRAINT chk_asset_intelligence_audit_generated_by CHECK (length(generated_by) > 0)
);

CREATE INDEX IF NOT EXISTS idx_creator_authority_registry_active
    ON creator_authority_registry(registry_version, canonical_creator_key)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_creator_authority_aliases_normalized
    ON creator_authority_aliases(normalized_alias);

CREATE INDEX IF NOT EXISTS idx_creator_prestige_registry_active
    ON creator_prestige_registry(registry_version, creator_authority_id)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_asset_intelligence_snapshot_opportunity
    ON asset_intelligence_signal_snapshots(opportunity_id, resolved_at DESC);

CREATE INDEX IF NOT EXISTS idx_asset_intelligence_audit_opportunity
    ON asset_intelligence_audit_log(opportunity_id, event_at DESC)
    WHERE opportunity_id IS NOT NULL;

DROP TRIGGER IF EXISTS trg_creator_authority_registry_updated_at ON creator_authority_registry;
CREATE TRIGGER trg_creator_authority_registry_updated_at
    BEFORE UPDATE ON creator_authority_registry
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_creator_prestige_registry_updated_at ON creator_prestige_registry;
CREATE TRIGGER trg_creator_prestige_registry_updated_at
    BEFORE UPDATE ON creator_prestige_registry
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE RULE asset_intelligence_audit_log_no_update AS
    ON UPDATE TO asset_intelligence_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no UPDATE permitted on asset_intelligence_audit_log');

CREATE OR REPLACE RULE asset_intelligence_audit_log_no_delete AS
    ON DELETE TO asset_intelligence_audit_log
    DO INSTEAD SELECT commerce_raise_exception('no DELETE permitted on asset_intelligence_audit_log');

CREATE OR REPLACE FUNCTION enforce_asset_intelligence_audit_hash_chain()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
    latest_checksum TEXT;
BEGIN
    SELECT aial.entry_checksum_sha256
      INTO latest_checksum
      FROM asset_intelligence_audit_log aial
     WHERE COALESCE(aial.opportunity_id, aial.signal_snapshot_id)
           IS NOT DISTINCT FROM COALESCE(NEW.opportunity_id, NEW.signal_snapshot_id)
     ORDER BY event_at DESC, created_at DESC, id DESC
     LIMIT 1;

    IF latest_checksum IS NULL THEN
        IF NEW.previous_entry_checksum IS NOT NULL THEN
            RAISE EXCEPTION 'first asset_intelligence_audit_log entry for target must have null previous_entry_checksum';
        END IF;
    ELSIF NEW.previous_entry_checksum IS DISTINCT FROM latest_checksum THEN
        RAISE EXCEPTION 'previous_entry_checksum must match latest asset_intelligence_audit_log entry';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_asset_intelligence_audit_hash_chain ON asset_intelligence_audit_log;
CREATE TRIGGER trg_asset_intelligence_audit_hash_chain
    BEFORE INSERT ON asset_intelligence_audit_log
    FOR EACH ROW EXECUTE FUNCTION enforce_asset_intelligence_audit_hash_chain();

WITH creators(canonical_creator_key, display_name, normalized_names, external_authorities, creator_roles, authority_confidence, attribution_risk, prestige_score, prestige_tier, prestige_rationale) AS (
    VALUES
        ('john-james-audubon', 'John James Audubon', ARRAY['audubon','john james audubon'], '{"wikidata_qid": "Q185281"}'::jsonb, ARRAY['illustrator','naturalist'], 0.980::numeric, 'medium', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('elizabeth-gould', 'Elizabeth Gould', ARRAY['gould','elizabeth gould'], '{"wikidata_qid": "Q5366536"}'::jsonb, ARRAY['illustrator'], 0.920::numeric, 'medium', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('maria-sibylla-merian', 'Maria Sibylla Merian', ARRAY['merian','maria sibylla merian'], '{"wikidata_qid": "Q57235"}'::jsonb, ARRAY['illustrator','naturalist'], 0.970::numeric, 'low', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('pierre-joseph-redoute', 'Pierre-Joseph Redoute', ARRAY['redoute','redouté','pierre joseph redoute'], '{"wikidata_qid": "Q315496"}'::jsonb, ARRAY['illustrator'], 0.970::numeric, 'low', 1.000::numeric, 'master', 'Priority botanical illustrator in governed commerce benchmarks.'),
        ('edward-lear', 'Edward Lear', ARRAY['lear','edward lear'], '{"wikidata_qid": "Q191490"}'::jsonb, ARRAY['illustrator'], 0.950::numeric, 'medium', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('frederick-polydore-nodder', 'Frederick Polydore Nodder', ARRAY['nodder','frederick nodder','frederick polydore nodder'], '{}'::jsonb, ARRAY['illustrator'], 0.900::numeric, 'medium', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('ernst-haeckel', 'Ernst Haeckel', ARRAY['haeckel','ernst haeckel'], '{"wikidata_qid": "Q1043"}'::jsonb, ARRAY['illustrator','naturalist'], 0.980::numeric, 'low', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('joseph-wolf', 'Joseph Wolf', ARRAY['wolf','joseph wolf'], '{"wikidata_qid": "Q63283"}'::jsonb, ARRAY['illustrator'], 0.940::numeric, 'medium', 1.000::numeric, 'master', 'Priority natural history illustrator in governed commerce benchmarks.'),
        ('thomas-moran', 'Thomas Moran', ARRAY['moran','thomas moran'], '{"wikidata_qid": "Q505765"}'::jsonb, ARRAY['artist'], 0.970::numeric, 'low', 1.000::numeric, 'master', 'Yellowstone landscape creator benchmark for cultural and geographic anchors.'),
        ('william-henry-jackson', 'William Henry Jackson', ARRAY['jackson','william henry jackson'], '{"wikidata_qid": "Q1355638"}'::jsonb, ARRAY['photographer'], 0.960::numeric, 'medium', 0.900::numeric, 'major', 'Yellowstone historical photography benchmark creator.')
)
INSERT INTO creator_authority_registry (
    registry_version, canonical_creator_key, display_name, normalized_names,
    external_authorities, creator_roles, authority_confidence, attribution_risk,
    status, authored_by, approved_by, approved_at, provenance
)
SELECT
    '1.0.0',
    canonical_creator_key,
    display_name,
    normalized_names,
    external_authorities,
    creator_roles,
    authority_confidence,
    attribution_risk,
    'active',
    'migration_33_asset_intelligence_creator_registries',
    'migration_33_second_human',
    NOW(),
    '{"migration": "33_asset_intelligence_creator_registries"}'::jsonb
FROM creators
ON CONFLICT (registry_version, canonical_creator_key) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    normalized_names = EXCLUDED.normalized_names,
    external_authorities = EXCLUDED.external_authorities,
    creator_roles = EXCLUDED.creator_roles,
    authority_confidence = EXCLUDED.authority_confidence,
    attribution_risk = EXCLUDED.attribution_risk,
    status = EXCLUDED.status,
    approved_by = EXCLUDED.approved_by,
    approved_at = EXCLUDED.approved_at,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

WITH aliases AS (
    SELECT car.id, alias.normalized_alias
      FROM creator_authority_registry car
      CROSS JOIN LATERAL unnest(car.normalized_names) AS alias(normalized_alias)
     WHERE car.registry_version = '1.0.0'
)
INSERT INTO creator_authority_aliases (
    creator_authority_id, alias, normalized_alias, alias_source, confidence_score, provenance
)
SELECT
    id,
    normalized_alias,
    lower(regexp_replace(unaccent(normalized_alias), '[^a-z0-9]+', ' ', 'g')),
    'migration_33_seed',
    0.950,
    '{"migration": "33_asset_intelligence_creator_registries"}'::jsonb
FROM aliases
ON CONFLICT (creator_authority_id, normalized_alias) DO UPDATE SET
    alias = EXCLUDED.alias,
    confidence_score = EXCLUDED.confidence_score,
    provenance = EXCLUDED.provenance;

WITH prestige(canonical_creator_key, prestige_score, prestige_tier, prestige_rationale, applies_to_anchor_types) AS (
    VALUES
        ('john-james-audubon', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('elizabeth-gould', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('maria-sibylla-merian', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('pierre-joseph-redoute', 1.000::numeric, 'master', 'Priority botanical illustrator.', ARRAY['biological']),
        ('edward-lear', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('frederick-polydore-nodder', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('ernst-haeckel', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('joseph-wolf', 1.000::numeric, 'master', 'Priority natural history illustrator.', ARRAY['biological']),
        ('thomas-moran', 1.000::numeric, 'master', 'Yellowstone landscape creator benchmark.', ARRAY['geographic','cultural']),
        ('william-henry-jackson', 0.900::numeric, 'major', 'Yellowstone historical photography benchmark.', ARRAY['geographic','cultural'])
)
INSERT INTO creator_prestige_registry (
    registry_version, creator_authority_id, prestige_score, prestige_tier,
    prestige_rationale, applies_to_anchor_types, status, authored_by,
    approved_by, approved_at, provenance
)
SELECT
    '1.0.0',
    car.id,
    p.prestige_score,
    p.prestige_tier,
    p.prestige_rationale,
    p.applies_to_anchor_types,
    'active',
    'migration_33_asset_intelligence_creator_registries',
    'migration_33_second_human',
    NOW(),
    '{"migration": "33_asset_intelligence_creator_registries"}'::jsonb
FROM prestige p
JOIN creator_authority_registry car
  ON car.registry_version = '1.0.0'
 AND car.canonical_creator_key = p.canonical_creator_key
ON CONFLICT (registry_version, creator_authority_id) DO UPDATE SET
    prestige_score = EXCLUDED.prestige_score,
    prestige_tier = EXCLUDED.prestige_tier,
    prestige_rationale = EXCLUDED.prestige_rationale,
    applies_to_anchor_types = EXCLUDED.applies_to_anchor_types,
    status = EXCLUDED.status,
    approved_by = EXCLUDED.approved_by,
    approved_at = EXCLUDED.approved_at,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
