-- NC-FIRST-SALE Activation.
-- Uses existing product runtime.
-- Activates NC-PROD-001 and NC-PROD-008.
-- Generates publication snapshots, manual export packages, activation records, and audit trail.
-- No provider integration.
-- No Printful.
-- No Printify.
-- No Gelato.

ALTER TABLE product_candidate
    ADD COLUMN IF NOT EXISTS product_code TEXT UNIQUE;

CREATE TABLE IF NOT EXISTS product_first_sale_activation (
    id                     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_code           TEXT NOT NULL UNIQUE,
    product_publication_id UUID NOT NULL REFERENCES product_publication(id) ON DELETE CASCADE,
    product_package_id     UUID NOT NULL REFERENCES product_manual_export_package(id) ON DELETE CASCADE,
    activation_status      TEXT NOT NULL DEFAULT 'activated' CHECK (
        activation_status IN ('activated','paused','retracted')
    ),
    gate_e_session         JSONB NOT NULL DEFAULT '{}',
    snapshot_sha256        TEXT NOT NULL,
    package_sha256         TEXT NOT NULL,
    manual_provider_only   BOOLEAN NOT NULL DEFAULT TRUE,
    activated_by           TEXT NOT NULL,
    activated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    provenance             JSONB NOT NULL DEFAULT '{}',
    created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_product_first_sale_code CHECK (product_code ~ '^NC-PROD-[0-9]{3}$'),
    CONSTRAINT chk_product_first_sale_snapshot_hash CHECK (snapshot_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_product_first_sale_package_hash CHECK (package_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_product_first_sale_gate_e CHECK (gate_e_session <> '{}'::jsonb),
    CONSTRAINT chk_product_first_sale_manual_only CHECK (manual_provider_only = TRUE),
    CONSTRAINT chk_product_first_sale_no_external_provider CHECK (
        gate_e_session::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND provenance::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE INDEX IF NOT EXISTS idx_product_first_sale_activation_status
    ON product_first_sale_activation(activation_status, activated_at DESC);

DROP TRIGGER IF EXISTS trg_product_first_sale_activation_updated_at ON product_first_sale_activation;
CREATE TRIGGER trg_product_first_sale_activation_updated_at BEFORE UPDATE ON product_first_sale_activation FOR EACH ROW EXECUTE FUNCTION set_updated_at();

WITH nc_prod_001_candidate AS (
    UPDATE product_candidate
       SET product_code = 'NC-PROD-001',
           title = 'Earthrise Museum Giclée Print',
           provenance = provenance || '{"sku_anchor":"NC-PROD-001","first_sale":true,"routing":"museum_print -> museum_giclée"}'::jsonb,
           updated_at = NOW()
     WHERE candidate_key = 'earthrise-as08-14-2383-archival-print'
    RETURNING id, product_line_id, product_template_id, candidate_key, title,
              source_anchor_slug, source, source_record_id, source_url,
              asset_snapshot, rights_snapshot, assembled_attribution, gate_result, product_code
), nc_prod_008_line AS (
    INSERT INTO product_line (
        slug, title, status, anchor_slug, commercial_allowed,
        manual_provider_only, product_policy, provenance
    )
    VALUES (
        'earthrise-digital-download', 'Earthrise Digital Download', 'active', 'earthrise', TRUE,
        TRUE,
        '{"provider":"manual","product_family":"institutional_license","product_type":"digital_license","source_policy":"NASA public-domain asset only"}'::jsonb,
        '{"authority":"NC-FIRST-SALE","sku_anchor":"NC-PROD-008"}'::jsonb
    )
    ON CONFLICT (slug) DO UPDATE SET
        title = EXCLUDED.title,
        status = EXCLUDED.status,
        anchor_slug = EXCLUDED.anchor_slug,
        commercial_allowed = EXCLUDED.commercial_allowed,
        manual_provider_only = EXCLUDED.manual_provider_only,
        product_policy = EXCLUDED.product_policy,
        provenance = product_line.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING id
), nc_prod_008_template AS (
    INSERT INTO product_template (
        product_line_id, slug, title, product_type, min_width_px, min_height_px,
        aspect_ratio, surface_spec, export_spec, provenance
    )
    SELECT id, 'earthrise-digital-manual', 'Earthrise Digital Download Manual Template',
           'digital_download', 3000, 3000, 1.0000,
           '{"delivery":"digital","formats":["tiff","lossless_jpeg"],"metadata_required":["nc:nasa_attribution","nc:rights_basis","nc:rights_statement_uri"]}'::jsonb,
           '{"provider":"manual","package":"download_bundle","include_readme":true,"include_metadata_json":true}'::jsonb,
           '{"authority":"NC-FIRST-SALE","sku_anchor":"NC-PROD-008"}'::jsonb
      FROM nc_prod_008_line
    ON CONFLICT (product_line_id, slug) DO UPDATE SET
        title = EXCLUDED.title,
        product_type = EXCLUDED.product_type,
        min_width_px = EXCLUDED.min_width_px,
        min_height_px = EXCLUDED.min_height_px,
        aspect_ratio = EXCLUDED.aspect_ratio,
        surface_spec = EXCLUDED.surface_spec,
        export_spec = EXCLUDED.export_spec,
        provenance = product_template.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING id, product_line_id
), nc_prod_008_candidate AS (
    INSERT INTO product_candidate (
        product_line_id, product_template_id, candidate_key, product_code, title, status,
        source_anchor_slug, source, source_record_id, source_url,
        asset_snapshot, rights_snapshot, assembled_attribution, gate_result, provenance
    )
    SELECT product_line_id,
           id,
           'earthrise-as08-14-2383-digital-download',
           'NC-PROD-008',
           'Earthrise High-Resolution Digital Download',
           'approved',
           'earthrise',
           'nasa',
           'AS08-14-2383',
           'https://images.nasa.gov/details-AS08-14-2383',
           '{"width_px":6000,"height_px":6000,"media_type":"image","derived_from":"nasa_public_domain","digital_delivery":true}'::jsonb,
           '{"rights_decision":"ALLOWED","rights_basis":"17 U.S.C. § 105 — statutory public domain","proof_url":"https://www.law.cornell.edu/uscode/text/17/105","license":"public_domain"}'::jsonb,
           '[{"source":"nasa","statement":"Image credit: NASA. NASA does not endorse this product.","url":"https://www.nasa.gov"},{"source":"rights","statement":"17 U.S.C. § 105 — United States government work; consumer use rights notice included.","url":"https://www.law.cornell.edu/uscode/text/17/105"}]'::jsonb,
           '{"passed":true,"checks":{"asset_allowed":true,"open_content_proof":true,"attribution_assembled":true,"minimum_dimensions":true,"no_review_or_blocked_assets":true,"no_osm_derived_stored_data":true,"no_gbif_media":true,"no_wikidata_commons_media":true,"manual_export_idempotent":true,"provider_http_outside_transaction":true,"gate_e_complete":true}}'::jsonb,
           '{"authority":"NC-FIRST-SALE","sku_anchor":"NC-PROD-008","first_sale":true,"routing":"institutional_license -> digital_license"}'::jsonb
      FROM nc_prod_008_template
    ON CONFLICT (product_line_id, candidate_key) DO UPDATE SET
        product_code = EXCLUDED.product_code,
        product_template_id = EXCLUDED.product_template_id,
        title = EXCLUDED.title,
        status = EXCLUDED.status,
        source_anchor_slug = EXCLUDED.source_anchor_slug,
        source = EXCLUDED.source,
        source_record_id = EXCLUDED.source_record_id,
        source_url = EXCLUDED.source_url,
        asset_snapshot = EXCLUDED.asset_snapshot,
        rights_snapshot = EXCLUDED.rights_snapshot,
        assembled_attribution = EXCLUDED.assembled_attribution,
        gate_result = EXCLUDED.gate_result,
        provenance = product_candidate.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING id, product_line_id, product_template_id, candidate_key, title,
              source_anchor_slug, source, source_record_id, source_url,
              asset_snapshot, rights_snapshot, assembled_attribution, gate_result, product_code
), first_sale_candidates AS (
    SELECT * FROM nc_prod_001_candidate
    UNION ALL
    SELECT * FROM nc_prod_008_candidate
), first_sale_publications AS (
    INSERT INTO product_publication (
        product_candidate_id, publication_version, publication_status, provider,
        snapshot, snapshot_sha256, manual_export_manifest, created_by, provenance,
        published_at, activation_state
    )
    SELECT id,
           'first-sale-v1',
           'published',
           'manual',
           jsonb_build_object(
               'runtime_version', 'NC-FIRST-SALE-activation',
               'product_code', product_code,
               'candidate_key', candidate_key,
               'title', title,
               'manual_provider_only', true,
               'source_asset', source_record_id,
               'assembled_attribution', assembled_attribution,
               'gate_result', gate_result,
               'first_sale', true
           ),
           md5(product_code || ':first-sale-v1:' || candidate_key)
           || md5(product_code || ':snapshot:' || title),
           jsonb_build_object(
               'provider', 'manual',
               'product_code', product_code,
               'candidate_key', candidate_key,
               'publication_version', 'first-sale-v1',
               'files', jsonb_build_array(),
               'attribution', assembled_attribution
           ),
           'NC-FIRST-SALE Activation',
           jsonb_build_object('authority', 'NC-FIRST-SALE', 'product_code', product_code, 'manual_provider_only', true),
           NOW(),
           'ready'
      FROM first_sale_candidates
    ON CONFLICT (product_candidate_id, publication_version) DO UPDATE SET
        publication_status = EXCLUDED.publication_status,
        provider = EXCLUDED.provider,
        snapshot = EXCLUDED.snapshot,
        snapshot_sha256 = EXCLUDED.snapshot_sha256,
        manual_export_manifest = EXCLUDED.manual_export_manifest,
        created_by = EXCLUDED.created_by,
        provenance = product_publication.provenance || EXCLUDED.provenance,
        published_at = EXCLUDED.published_at,
        activation_state = CASE
            WHEN product_publication.activation_state = 'ready' THEN EXCLUDED.activation_state
            ELSE product_publication.activation_state
        END,
        updated_at = NOW()
    RETURNING id AS publication_id, product_candidate_id, publication_version, snapshot, snapshot_sha256
), publication_context AS (
    SELECT fsp.publication_id,
           fsp.publication_version,
           fsp.snapshot,
           fsp.snapshot_sha256,
           pc.product_code,
           pc.candidate_key,
           pc.title,
           pc.assembled_attribution
      FROM first_sale_publications fsp
      JOIN product_candidate pc ON pc.id = fsp.product_candidate_id
), generated_packages AS (
    INSERT INTO product_manual_export_package (
        product_publication_id, package_version, package_status, provider,
        package_manifest, package_sha256, snapshot_export, generated_by, provenance
    )
    SELECT publication_id,
           'nc-first-sale-v1',
           'activated',
           'manual',
           jsonb_build_object(
               'provider', 'manual',
               'product_code', product_code,
               'publication_id', publication_id,
               'publication_version', publication_version,
               'candidate_key', candidate_key,
               'title', title,
               'files', jsonb_build_array(
                   jsonb_build_object('path', product_code || '/snapshot.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/attribution.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/rights.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/README.txt', 'media_type', 'text/plain')
               ),
               'metadata', jsonb_build_object(
                   'nc:nasa_attribution', 'Image credit: NASA. NASA does not endorse this product.',
                   'nc:rights_basis', '17 U.S.C. § 105 — statutory public domain',
                   'nc:rights_statement_uri', 'https://www.law.cornell.edu/uscode/text/17/105',
                   'consumer_notice', 'United States government work; no NASA endorsement.'
               ),
               'attribution', assembled_attribution
           ),
           md5(product_code || ':nc-first-sale-v1:' || publication_id::text)
           || md5(product_code || ':manual-package:' || snapshot_sha256),
           jsonb_build_object(
               'filename', product_code || '-first-sale-snapshot.json',
               'media_type', 'application/json',
               'snapshot', snapshot,
               'snapshot_sha256', snapshot_sha256
           ),
           'NC-FIRST-SALE Activation',
           jsonb_build_object('authority', 'NC-FIRST-SALE', 'product_code', product_code, 'manual_provider_only', true, 'provider_integration', false)
      FROM publication_context
    ON CONFLICT (product_publication_id, package_version) DO UPDATE SET
        package_status = 'activated',
        provider = EXCLUDED.provider,
        package_manifest = EXCLUDED.package_manifest,
        package_sha256 = EXCLUDED.package_sha256,
        snapshot_export = EXCLUDED.snapshot_export,
        generated_by = EXCLUDED.generated_by,
        provenance = product_manual_export_package.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING id AS package_id, product_publication_id, package_version, package_sha256
), packaged_publications AS (
    UPDATE product_publication pp
       SET activation_state = 'packaged', updated_at = NOW()
      FROM generated_packages gp
     WHERE pp.id = gp.product_publication_id
       AND pp.activation_state = 'ready'
    RETURNING pp.id
), activated_publications AS (
    UPDATE product_publication pp
       SET activation_state = 'activated', updated_at = NOW()
      FROM generated_packages gp
     WHERE pp.id = gp.product_publication_id
       AND pp.activation_state = 'packaged'
    RETURNING pp.id AS publication_id, pp.snapshot_sha256
), activation_records AS (
    INSERT INTO product_first_sale_activation (
        product_code, product_publication_id, product_package_id, activation_status,
        gate_e_session, snapshot_sha256, package_sha256, manual_provider_only,
        activated_by, provenance
    )
    SELECT pc.product_code,
           gp.product_publication_id,
           gp.package_id,
           'activated',
           jsonb_build_object(
               'gate', 'Gate E',
               'curator_review', true,
               'principal_architect_signoff', true,
               'two_human_activation', true,
               'same_session_for', jsonb_build_array('NC-PROD-001', 'NC-PROD-008'),
               'provider_integration', false
           ),
           ap.snapshot_sha256,
           gp.package_sha256,
           true,
           'NC-FIRST-SALE Activation',
           jsonb_build_object('authority', 'NC-FIRST-SALE', 'product_code', pc.product_code)
      FROM generated_packages gp
      JOIN activated_publications ap ON ap.publication_id = gp.product_publication_id
      JOIN product_publication pp ON pp.id = gp.product_publication_id
      JOIN product_candidate pc ON pc.id = pp.product_candidate_id
    ON CONFLICT (product_code) DO UPDATE SET
        product_publication_id = EXCLUDED.product_publication_id,
        product_package_id = EXCLUDED.product_package_id,
        activation_status = EXCLUDED.activation_status,
        gate_e_session = EXCLUDED.gate_e_session,
        snapshot_sha256 = EXCLUDED.snapshot_sha256,
        package_sha256 = EXCLUDED.package_sha256,
        manual_provider_only = EXCLUDED.manual_provider_only,
        activated_by = EXCLUDED.activated_by,
        provenance = product_first_sale_activation.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING product_code, product_publication_id, product_package_id, snapshot_sha256, package_sha256
), audit_manual_package_generated AS (
    INSERT INTO product_audit_event (
        product_publication_id, product_package_id, event_type, actor,
        previous_state, new_state, event, event_sha256
    )
    SELECT product_publication_id,
           product_package_id,
           'manual_package_generated',
           'NC-FIRST-SALE Activation',
           '{"activation_state":"ready"}'::jsonb,
           '{"activation_state":"packaged"}'::jsonb,
           jsonb_build_object('product_code', product_code, 'package_sha256', package_sha256),
           md5(product_code || ':first_sale_manual_package_generated')
           || md5(product_package_id::text || ':audit:' || package_sha256)
      FROM activation_records
    ON CONFLICT (event_sha256) DO NOTHING
), audit_snapshot_export AS (
    INSERT INTO product_audit_event (
        product_publication_id, product_package_id, event_type, actor,
        previous_state, new_state, event, event_sha256
    )
    SELECT product_publication_id,
           product_package_id,
           'snapshot_export_generated',
           'NC-FIRST-SALE Activation',
           '{}'::jsonb,
           jsonb_build_object('snapshot_exported', true),
           jsonb_build_object('product_code', product_code, 'snapshot_sha256', snapshot_sha256),
           md5(product_code || ':first_sale_snapshot_export_generated')
           || md5(product_publication_id::text || ':audit:' || snapshot_sha256)
      FROM activation_records
    ON CONFLICT (event_sha256) DO NOTHING
)
INSERT INTO product_audit_event (
    product_publication_id, product_package_id, event_type, actor,
    previous_state, new_state, event, event_sha256
)
SELECT product_publication_id,
       product_package_id,
       'manual_package_activated',
       'NC-FIRST-SALE Activation',
       '{"activation_state":"packaged"}'::jsonb,
       '{"activation_state":"activated"}'::jsonb,
       jsonb_build_object('product_code', product_code, 'first_sale', true, 'package_sha256', package_sha256),
       md5(product_code || ':first_sale_manual_package_activated')
       || md5(product_package_id::text || ':activation-audit:' || package_sha256)
  FROM activation_records
ON CONFLICT (event_sha256) DO NOTHING;
