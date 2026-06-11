-- NC-COMMERCE-002 Commerce Activation Sprint.
-- Product publication workflow, manual export packages, snapshot export, audit trail,
-- and activation state machine.
-- Manual provider only.
-- No Printful.
-- No Printify.
-- No Gelato.
-- No external provider HTTP.

ALTER TABLE product_publication
    ADD COLUMN IF NOT EXISTS activation_state TEXT NOT NULL DEFAULT 'ready' CHECK (
        activation_state IN ('draft','ready','packaged','activated','paused','retracted')
    );

CREATE TABLE IF NOT EXISTS product_activation_state_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO product_activation_state_vocabulary (value, description, sort_order)
VALUES
    ('draft', 'Publication exists but has not passed activation checks.', 10),
    ('ready', 'Publication passed gates and can be packaged manually.', 20),
    ('packaged', 'Manual export package has been generated.', 30),
    ('activated', 'Manual package is activated for commerce operations.', 40),
    ('paused', 'Activated package is temporarily paused.', 50),
    ('retracted', 'Publication has been retracted from commerce operations.', 60)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS product_manual_export_package (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_publication_id UUID NOT NULL REFERENCES product_publication(id) ON DELETE CASCADE,
    package_version       TEXT NOT NULL,
    package_status        TEXT NOT NULL DEFAULT 'generated' CHECK (
        package_status IN ('generated','activated','paused','retracted')
    ),
    provider              TEXT NOT NULL DEFAULT 'manual' CHECK (provider = 'manual'),
    package_manifest      JSONB NOT NULL DEFAULT '{}',
    package_sha256        TEXT NOT NULL,
    snapshot_export       JSONB NOT NULL DEFAULT '{}',
    generated_by          TEXT NOT NULL,
    provenance            JSONB NOT NULL DEFAULT '{}',
    generated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (product_publication_id, package_version),
    UNIQUE (package_sha256),
    CONSTRAINT chk_product_manual_export_package_manifest CHECK (package_manifest <> '{}'::jsonb),
    CONSTRAINT chk_product_manual_export_package_snapshot CHECK (snapshot_export <> '{}'::jsonb),
    CONSTRAINT chk_product_manual_export_package_hash CHECK (package_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_product_manual_export_package_actor CHECK (length(generated_by) > 0),
    CONSTRAINT chk_product_manual_export_package_no_external_provider CHECK (
        package_manifest::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND snapshot_export::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND provenance::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE TABLE IF NOT EXISTS product_audit_event (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_publication_id UUID REFERENCES product_publication(id) ON DELETE CASCADE,
    product_package_id    UUID REFERENCES product_manual_export_package(id) ON DELETE CASCADE,
    event_type            TEXT NOT NULL CHECK (
        event_type IN (
            'publication_verified','manual_package_generated','manual_package_activated',
            'manual_package_paused','manual_package_retracted','snapshot_export_generated'
        )
    ),
    actor                 TEXT NOT NULL,
    previous_state        JSONB NOT NULL DEFAULT '{}',
    new_state             JSONB NOT NULL DEFAULT '{}',
    event                 JSONB NOT NULL DEFAULT '{}',
    event_sha256          TEXT NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (event_sha256),
    CONSTRAINT chk_product_audit_event_target CHECK (
        product_publication_id IS NOT NULL OR product_package_id IS NOT NULL
    ),
    CONSTRAINT chk_product_audit_event_hash CHECK (event_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_product_audit_event_actor CHECK (length(actor) > 0),
    CONSTRAINT chk_product_audit_event_no_external_provider CHECK (
        event::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND previous_state::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND new_state::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE INDEX IF NOT EXISTS idx_product_publication_activation_state
    ON product_publication(activation_state, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_product_manual_export_package_publication
    ON product_manual_export_package(product_publication_id, package_status);
CREATE INDEX IF NOT EXISTS idx_product_audit_event_publication
    ON product_audit_event(product_publication_id, created_at DESC);

DROP TRIGGER IF EXISTS trg_product_manual_export_package_updated_at ON product_manual_export_package;
CREATE TRIGGER trg_product_manual_export_package_updated_at BEFORE UPDATE ON product_manual_export_package FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_product_publication_activation_transition()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.activation_state <> OLD.activation_state THEN
        IF OLD.activation_state = 'draft' AND NEW.activation_state <> 'ready' THEN
            RAISE EXCEPTION 'invalid product activation transition from draft to %', NEW.activation_state;
        ELSIF OLD.activation_state = 'ready' AND NEW.activation_state NOT IN ('packaged','retracted') THEN
            RAISE EXCEPTION 'invalid product activation transition from ready to %', NEW.activation_state;
        ELSIF OLD.activation_state = 'packaged' AND NEW.activation_state NOT IN ('activated','retracted') THEN
            RAISE EXCEPTION 'invalid product activation transition from packaged to %', NEW.activation_state;
        ELSIF OLD.activation_state = 'activated' AND NEW.activation_state NOT IN ('paused','retracted') THEN
            RAISE EXCEPTION 'invalid product activation transition from activated to %', NEW.activation_state;
        ELSIF OLD.activation_state = 'paused' AND NEW.activation_state NOT IN ('activated','retracted') THEN
            RAISE EXCEPTION 'invalid product activation transition from paused to %', NEW.activation_state;
        ELSIF OLD.activation_state = 'retracted' THEN
            RAISE EXCEPTION 'invalid product activation transition from retracted to %', NEW.activation_state;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_product_publication_activation_transition ON product_publication;
CREATE TRIGGER trg_product_publication_activation_transition
    BEFORE UPDATE OF activation_state ON product_publication
    FOR EACH ROW EXECUTE FUNCTION enforce_product_publication_activation_transition();

WITH target_publications AS (
    SELECT pp.id AS publication_id,
           pp.publication_version,
           pp.snapshot,
           pp.snapshot_sha256,
           pc.candidate_key,
           pc.title,
           pc.assembled_attribution
      FROM product_publication pp
      JOIN product_candidate pc ON pc.id = pp.product_candidate_id
     WHERE pc.candidate_key IN (
        'earthrise-as08-14-2383-archival-print',
        'yellowstone-hayden-map-print',
        'grand-canyon-dutton-atlas-print'
     )
), generated_packages AS (
    INSERT INTO product_manual_export_package (
        product_publication_id, package_version, package_status, provider,
        package_manifest, package_sha256, snapshot_export, generated_by, provenance
    )
    SELECT publication_id,
           'nc-commerce-002-v1',
           'generated',
           'manual',
           jsonb_build_object(
               'provider', 'manual',
               'publication_id', publication_id,
               'publication_version', publication_version,
               'candidate_key', candidate_key,
               'title', title,
               'files', jsonb_build_array(
                   jsonb_build_object('path', 'snapshot.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', 'attribution.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', 'README.txt', 'media_type', 'text/plain')
               ),
               'attribution', assembled_attribution
           ) AS package_manifest,
           md5((publication_id::text || ':nc-commerce-002-v1:' || candidate_key))
           || md5((publication_id::text || ':manual-export-package:' || snapshot_sha256)) AS package_sha256,
           jsonb_build_object(
               'filename', candidate_key || '-snapshot.json',
               'media_type', 'application/json',
               'snapshot', snapshot,
               'snapshot_sha256', snapshot_sha256
           ) AS snapshot_export,
           'NC-COMMERCE-002 Activation Sprint',
           '{"authority":"NC-COMMERCE-002","manual_provider_only":true,"http":"no provider api calls"}'::jsonb
      FROM target_publications
    ON CONFLICT (product_publication_id, package_version) DO UPDATE SET
        package_status = EXCLUDED.package_status,
        provider = EXCLUDED.provider,
        package_manifest = EXCLUDED.package_manifest,
        package_sha256 = EXCLUDED.package_sha256,
        snapshot_export = EXCLUDED.snapshot_export,
        generated_by = EXCLUDED.generated_by,
        provenance = product_manual_export_package.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING id, product_publication_id, package_version, package_status, package_sha256
), packaged_publications AS (
    UPDATE product_publication pp
       SET activation_state = 'packaged',
           updated_at = NOW()
      FROM generated_packages gp
     WHERE pp.id = gp.product_publication_id
       AND pp.activation_state = 'ready'
    RETURNING pp.id AS publication_id, gp.id AS package_id, gp.package_version, gp.package_sha256
), package_audits AS (
    INSERT INTO product_audit_event (
        product_publication_id, product_package_id, event_type, actor,
        previous_state, new_state, event, event_sha256
    )
    SELECT publication_id,
           package_id,
           'manual_package_generated',
           'NC-COMMERCE-002 Activation Sprint',
           '{"activation_state":"ready"}'::jsonb,
           '{"activation_state":"packaged"}'::jsonb,
           jsonb_build_object(
               'package_version', package_version,
               'package_sha256', package_sha256,
               'provider', 'manual'
           ),
           md5(publication_id::text || ':manual_package_generated:' || package_version)
           || md5(package_id::text || ':audit:' || package_sha256)
      FROM packaged_publications
    ON CONFLICT (event_sha256) DO NOTHING
)
INSERT INTO product_audit_event (
    product_publication_id, product_package_id, event_type, actor,
    previous_state, new_state, event, event_sha256
)
SELECT gp.product_publication_id,
       gp.id,
       'snapshot_export_generated',
       'NC-COMMERCE-002 Activation Sprint',
       '{}'::jsonb,
       jsonb_build_object('snapshot_exported', true),
       jsonb_build_object('package_version', gp.package_version, 'package_sha256', gp.package_sha256),
       md5(gp.product_publication_id::text || ':snapshot_export_generated:' || gp.package_version)
       || md5(gp.id::text || ':snapshot-audit:' || gp.package_sha256)
  FROM generated_packages gp
ON CONFLICT (event_sha256) DO NOTHING;
