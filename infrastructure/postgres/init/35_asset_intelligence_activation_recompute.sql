-- v0.5.4 Phase 1 / Migration 35.
-- Asset Intelligence activation and recompute support.
--
-- PostgreSQL is authoritative.
-- Replay-safe by request snapshots and append-only audit.
-- Versioned registries.
-- No Commerce Intelligence formula redesign.
-- No Product Routing redesign.
-- No Catalog redesign.
-- No Publication redesign.

CREATE TABLE IF NOT EXISTS asset_intelligence_registry_activation (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registry_name         TEXT NOT NULL,
    registry_version      TEXT NOT NULL,
    status                TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','paused','superseded','retired')),
    activated_by          TEXT NOT NULL,
    activated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    superseded_by         UUID REFERENCES asset_intelligence_registry_activation(id),
    activation_snapshot   JSONB NOT NULL DEFAULT '{}',
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (registry_name, registry_version),
    CONSTRAINT chk_asset_intelligence_activation_superseded CHECK (
        status <> 'superseded' OR superseded_by IS NOT NULL
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_asset_intelligence_one_active_registry
    ON asset_intelligence_registry_activation(registry_name)
    WHERE status = 'active';

CREATE TABLE IF NOT EXISTS asset_intelligence_recompute_requests (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id        UUID NOT NULL REFERENCES illustration_opportunities(id),
    requested_by          TEXT NOT NULL,
    requested_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reason                TEXT NOT NULL,
    registry_version_set  JSONB NOT NULL,
    status                TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','claimed','completed','failed','cancelled')),
    claimed_by            TEXT,
    claimed_at            TIMESTAMPTZ,
    completed_at          TIMESTAMPTZ,
    failure_reason        TEXT,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_asset_intelligence_recompute_pending
    ON asset_intelligence_recompute_requests(status, requested_at)
    WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_asset_intelligence_recompute_opportunity
    ON asset_intelligence_recompute_requests(opportunity_id, requested_at DESC);

DROP TRIGGER IF EXISTS trg_asset_intelligence_registry_activation_updated_at ON asset_intelligence_registry_activation;
CREATE TRIGGER trg_asset_intelligence_registry_activation_updated_at
    BEFORE UPDATE ON asset_intelligence_registry_activation
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_asset_intelligence_recompute_requests_updated_at ON asset_intelligence_recompute_requests;
CREATE TRIGGER trg_asset_intelligence_recompute_requests_updated_at
    BEFORE UPDATE ON asset_intelligence_recompute_requests
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION request_asset_intelligence_recompute(
    target_opportunity_id UUID,
    request_reason TEXT,
    request_actor TEXT DEFAULT 'asset_intelligence_activation'
)
RETURNS UUID LANGUAGE plpgsql AS $$
DECLARE
    request_id UUID;
    registry_versions JSONB;
BEGIN
    SELECT jsonb_object_agg(registry_name, registry_version)
      INTO registry_versions
      FROM asset_intelligence_registry_activation
     WHERE status = 'active';

    IF registry_versions IS NULL THEN
        RAISE EXCEPTION 'no active asset intelligence registries';
    END IF;

    INSERT INTO asset_intelligence_recompute_requests (
        opportunity_id, requested_by, reason, registry_version_set, provenance
    )
    VALUES (
        target_opportunity_id,
        request_actor,
        request_reason,
        registry_versions,
        '{"function": "request_asset_intelligence_recompute"}'::jsonb
    )
    RETURNING id INTO request_id;

    UPDATE commerce_opportunities
       SET policy_stale = TRUE,
           status = CASE WHEN status = 'active' THEN 'stale' ELSE status END,
           updated_at = NOW()
     WHERE opportunity_id = target_opportunity_id
       AND status NOT IN ('archived','retired');

    RETURN request_id;
END;
$$;

CREATE OR REPLACE FUNCTION complete_asset_intelligence_recompute(
    request_id UUID,
    completion_actor TEXT DEFAULT 'commerce_opportunity_worker'
)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    UPDATE asset_intelligence_recompute_requests
       SET status = 'completed',
           completed_at = NOW(),
           claimed_by = COALESCE(claimed_by, completion_actor),
           claimed_at = COALESCE(claimed_at, NOW()),
           updated_at = NOW()
     WHERE id = request_id
       AND status IN ('pending','claimed');

    IF NOT FOUND THEN
        RAISE EXCEPTION 'asset intelligence recompute request % is not pending or claimed', request_id;
    END IF;
END;
$$;

INSERT INTO asset_intelligence_registry_activation (
    registry_name, registry_version, status, activated_by, activated_at,
    activation_snapshot, provenance
)
VALUES
    ('commerce_anchor_type_vocabulary', '1.0.0', 'active', 'migration_35_asset_intelligence_activation_recompute', NOW(), '{"values": ["biological", "geographic", "cultural"]}'::jsonb, '{"migration": "35_asset_intelligence_activation_recompute"}'::jsonb),
    ('creator_authority_registry', '1.0.0', 'active', 'migration_35_asset_intelligence_activation_recompute', NOW(), '{"minimum_active_rows": 10}'::jsonb, '{"migration": "35_asset_intelligence_activation_recompute"}'::jsonb),
    ('creator_prestige_registry', '1.0.0', 'active', 'migration_35_asset_intelligence_activation_recompute', NOW(), '{"minimum_active_rows": 10}'::jsonb, '{"migration": "35_asset_intelligence_activation_recompute"}'::jsonb),
    ('place_iconic_taxa_registry', '1.0.0', 'active', 'migration_35_asset_intelligence_activation_recompute', NOW(), '{"minimum_active_places": 5, "minimum_rows_per_place": 5}'::jsonb, '{"migration": "35_asset_intelligence_activation_recompute"}'::jsonb)
ON CONFLICT (registry_name, registry_version) DO UPDATE SET
    status = EXCLUDED.status,
    activated_by = EXCLUDED.activated_by,
    activated_at = EXCLUDED.activated_at,
    activation_snapshot = EXCLUDED.activation_snapshot,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
