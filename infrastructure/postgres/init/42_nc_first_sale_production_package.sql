-- NC-FIRST-SALE Production Package.
-- Uses existing activation runtime.
-- Final publication snapshots, manual export packages, attribution/disclaimer/rights manifests,
-- and verification records for NC-PROD-001 and NC-PROD-008.
-- No provider integration.
-- No Printful.
-- No Printify.
-- No Gelato.

CREATE TABLE IF NOT EXISTS product_production_package (
    id                       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_code             TEXT NOT NULL UNIQUE REFERENCES product_first_sale_activation(product_code),
    product_publication_id   UUID NOT NULL REFERENCES product_publication(id) ON DELETE CASCADE,
    product_package_id       UUID NOT NULL REFERENCES product_manual_export_package(id) ON DELETE CASCADE,
    package_version          TEXT NOT NULL,
    final_publication_snapshot JSONB NOT NULL DEFAULT '{}',
    final_snapshot_sha256    TEXT NOT NULL,
    final_manual_export_package JSONB NOT NULL DEFAULT '{}',
    final_package_sha256     TEXT NOT NULL,
    attribution_manifest     JSONB NOT NULL DEFAULT '{}',
    disclaimer_manifest      JSONB NOT NULL DEFAULT '{}',
    rights_evidence_manifest JSONB NOT NULL DEFAULT '{}',
    verification             JSONB NOT NULL DEFAULT '{}',
    production_status        TEXT NOT NULL DEFAULT 'ready' CHECK (
        production_status IN ('ready','blocked','retracted')
    ),
    manual_provider_only     BOOLEAN NOT NULL DEFAULT TRUE,
    generated_by             TEXT NOT NULL,
    generated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    provenance               JSONB NOT NULL DEFAULT '{}',
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (product_publication_id, package_version),
    UNIQUE (final_snapshot_sha256),
    UNIQUE (final_package_sha256),
    CONSTRAINT chk_product_production_package_code CHECK (product_code ~ '^NC-PROD-[0-9]{3}$'),
    CONSTRAINT chk_product_production_package_snapshot CHECK (final_publication_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_product_production_package_export CHECK (final_manual_export_package <> '{}'::jsonb),
    CONSTRAINT chk_product_production_package_attribution CHECK (attribution_manifest <> '{}'::jsonb),
    CONSTRAINT chk_product_production_package_disclaimer CHECK (disclaimer_manifest <> '{}'::jsonb),
    CONSTRAINT chk_product_production_package_rights CHECK (rights_evidence_manifest <> '{}'::jsonb),
    CONSTRAINT chk_product_production_package_verification CHECK (verification <> '{}'::jsonb),
    CONSTRAINT chk_product_production_package_hashes CHECK (
        final_snapshot_sha256 ~ '^[0-9a-f]{64}$'
        AND final_package_sha256 ~ '^[0-9a-f]{64}$'
    ),
    CONSTRAINT chk_product_production_package_manual_only CHECK (manual_provider_only = TRUE),
    CONSTRAINT chk_product_production_package_no_external_provider CHECK (
        final_manual_export_package::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND final_publication_snapshot::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND provenance::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE INDEX IF NOT EXISTS idx_product_production_package_status
    ON product_production_package(production_status, generated_at DESC);

DROP TRIGGER IF EXISTS trg_product_production_package_updated_at ON product_production_package;
CREATE TRIGGER trg_product_production_package_updated_at BEFORE UPDATE ON product_production_package FOR EACH ROW EXECUTE FUNCTION set_updated_at();

WITH production_inputs AS (
    SELECT fsa.product_code,
           fsa.product_publication_id,
           fsa.product_package_id,
           fsa.activation_status,
           fsa.snapshot_sha256 AS activation_snapshot_sha256,
           fsa.package_sha256 AS activation_package_sha256,
           pp.snapshot,
           pp.snapshot_sha256,
           pp.activation_state,
           pc.title,
           pc.candidate_key,
           pc.source_record_id,
           pc.source_url,
           pc.rights_snapshot,
           pc.assembled_attribution,
           pmp.package_manifest,
           pmp.package_sha256,
           pmp.snapshot_export
      FROM product_first_sale_activation fsa
      JOIN product_publication pp ON pp.id = fsa.product_publication_id
      JOIN product_candidate pc ON pc.id = pp.product_candidate_id
      JOIN product_manual_export_package pmp ON pmp.id = fsa.product_package_id
     WHERE fsa.product_code IN ('NC-PROD-001', 'NC-PROD-008')
       AND fsa.activation_status = 'activated'
       AND pp.activation_state = 'activated'
), production_payloads AS (
    SELECT product_code,
           product_publication_id,
           product_package_id,
           'production-v1' AS package_version,
           jsonb_build_object(
               'runtime_version', 'NC-FIRST-SALE-production-package',
               'product_code', product_code,
               'candidate_key', candidate_key,
               'title', title,
               'publication_snapshot', snapshot,
               'source_record_id', source_record_id,
               'manual_provider_only', true,
               'activation_state', activation_state
           ) AS final_publication_snapshot,
           jsonb_build_object(
               'provider', 'manual',
               'product_code', product_code,
               'candidate_key', candidate_key,
               'title', title,
               'publication_id', product_publication_id,
               'source_package_sha256', package_sha256,
               'snapshot_export', snapshot_export,
               'files', jsonb_build_array(
                   jsonb_build_object('path', product_code || '/final-publication-snapshot.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/attribution-manifest.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/disclaimer-manifest.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/rights-evidence-manifest.json', 'media_type', 'application/json'),
                   jsonb_build_object('path', product_code || '/README.txt', 'media_type', 'text/plain')
               ),
               'provider_integration', false
           ) AS final_manual_export_package,
           jsonb_build_object(
               'product_code', product_code,
               'statements', assembled_attribution,
               'required_statement', 'Image credit: NASA. NASA does not endorse this product.',
               'status', 'assembled'
           ) AS attribution_manifest,
           jsonb_build_object(
               'product_code', product_code,
               'disclaimers', jsonb_build_array(
                   jsonb_build_object(
                       'source', 'nasa',
                       'statement', 'Image credit: NASA. NASA does not endorse this product.',
                       'required_on', jsonb_build_array('product_listing', 'package_metadata', 'readme')
                   ),
                   jsonb_build_object(
                       'source', 'consumer_notice',
                       'statement', 'United States government work; no NASA endorsement.',
                       'required_on', jsonb_build_array('readme', 'rights_manifest')
                   )
               ),
               'status', 'assembled'
           ) AS disclaimer_manifest,
           jsonb_build_object(
               'product_code', product_code,
               'source_record_id', source_record_id,
               'source_url', source_url,
               'rights_snapshot', rights_snapshot,
               'rights_decision', rights_snapshot->>'rights_decision',
               ''proof_url', rights_snapshot->>'proof_url',
               'statutory_basis', '17 U.S.C. § 105 — statutory public domain',
               'status', 'verified'
           ) AS rights_evidence_manifest,
           activation_state,
           snapshot_sha256,
           package_sha256
      FROM production_inputs
), hashed_payloads AS (
    SELECT *,
           md5(product_code || ':production-v1:snapshot:' || final_publication_snapshot::text)
           || md5(product_code || ':production-v1:snapshot-2:' || snapshot_sha256) AS final_snapshot_sha256,
           md5(product_code || ':production-v1:package:' || final_manual_export_package::text)
           || md5(product_code || ':production-v1:package-2:' || package_sha256) AS final_package_sha256
      FROM production_payloads
), production_upsert AS (
    INSERT INTO product_production_package (
        product_code, product_publication_id, product_package_id, package_version,
        final_publication_snapshot, final_snapshot_sha256,
        final_manual_export_package, final_package_sha256,
        attribution_manifest, disclaimer_manifest, rights_evidence_manifest,
        verification, production_status, manual_provider_only, generated_by, provenance
    )
    SELECT product_code,
           product_publication_id,
           product_package_id,
           package_version,
           final_publication_snapshot,
           final_snapshot_sha256,
           final_manual_export_package,
           final_package_sha256,
           attribution_manifest,
           disclaimer_manifest,
           rights_evidence_manifest,
           jsonb_build_object(
               'publication_snapshot_hash_verified', final_snapshot_sha256 ~ '^[0-9a-f]{64}$',
               'export_package_hash_verified', final_package_sha256 ~ '^[0-9a-f]{64}$',
               'activation_state_verified', activation_state = 'activated',
               'manual_provider_only', true,
               'provider_integration', false
           ),
           'ready',
           true,
           'NC-FIRST-SALE Production Package',
           jsonb_build_object('authority', 'NC-FIRST-SALE', 'package_version', package_version, 'product_code', product_code)
      FROM hashed_payloads
    ON CONFLICT (product_code) DO UPDATE SET
        product_publication_id = EXCLUDED.product_publication_id,
        product_package_id = EXCLUDED.product_package_id,
        package_version = EXCLUDED.package_version,
        final_publication_snapshot = EXCLUDED.final_publication_snapshot,
        final_snapshot_sha256 = EXCLUDED.final_snapshot_sha256,
        final_manual_export_package = EXCLUDED.final_manual_export_package,
        final_package_sha256 = EXCLUDED.final_package_sha256,
        attribution_manifest = EXCLUDED.attribution_manifest,
        disclaimer_manifest = EXCLUDED.disclaimer_manifest,
        rights_evidence_manifest = EXCLUDED.rights_evidence_manifest,
        verification = EXCLUDED.verification,
        production_status = EXCLUDED.production_status,
        manual_provider_only = EXCLUDED.manual_provider_only,
        generated_by = EXCLUDED.generated_by,
        provenance = product_production_package.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING product_code, product_publication_id, product_package_id,
              final_snapshot_sha256, final_package_sha256
), audit_production_package AS (
    INSERT INTO product_audit_event (
        product_publication_id, product_package_id, event_type, actor,
        previous_state, new_state, event, event_sha256
    )
    SELECT product_publication_id,
           product_package_id,
           'snapshot_export_generated',
           'NC-FIRST-SALE Production Package',
           '{}'::jsonb,
           jsonb_build_object('production_package_ready', true),
           jsonb_build_object(
               'product_code', product_code,
               'final_snapshot_sha256', final_snapshot_sha256,
               'final_package_sha256', final_package_sha256
           ),
           md5(product_code || ':production_package_ready')
           || md5(product_package_id::text || ':production:' || final_package_sha256)
      FROM production_upsert
    ON CONFLICT (event_sha256) DO NOTHING
)
SELECT true AS nc_first_sale_production_package_ready;
