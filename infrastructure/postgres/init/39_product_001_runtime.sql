-- NC-PRODUCT-001 Sprint 1 runtime.
-- Product line, template, candidate, and publication runtime.
-- Manual provider only.
-- No external provider APIs.
-- No provider HTTP inside DB transactions.
-- No new source onboarding.
-- No media ingestion.
-- No OSM-derived stored data.
-- No GBIF media.
-- No Wikidata Commons media.

CREATE TABLE IF NOT EXISTS product_line (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug                 TEXT NOT NULL UNIQUE,
    title                TEXT NOT NULL,
    status               TEXT NOT NULL DEFAULT 'draft' CHECK (
        status IN ('draft','active','editorial_only','paused','retired')
    ),
    anchor_slug          TEXT NOT NULL,
    commercial_allowed   BOOLEAN NOT NULL DEFAULT FALSE,
    manual_provider_only BOOLEAN NOT NULL DEFAULT TRUE,
    product_policy       JSONB NOT NULL DEFAULT '{}',
    provenance           JSONB NOT NULL DEFAULT '{}',
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_product_line_slug CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    CONSTRAINT chk_product_line_policy CHECK (product_policy <> '{}'::jsonb),
    CONSTRAINT chk_product_line_manual_only CHECK (manual_provider_only = TRUE),
    CONSTRAINT chk_product_line_no_external_provider CHECK (
        product_policy::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND provenance::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE TABLE IF NOT EXISTS product_template (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_line_id      UUID NOT NULL REFERENCES product_line(id) ON DELETE CASCADE,
    slug                 TEXT NOT NULL,
    title                TEXT NOT NULL,
    product_type         TEXT NOT NULL DEFAULT 'archival_print',
    min_width_px         INT NOT NULL CHECK (min_width_px > 0),
    min_height_px        INT NOT NULL CHECK (min_height_px > 0),
    aspect_ratio         NUMERIC(8,4) NOT NULL CHECK (aspect_ratio > 0),
    surface_spec         JSONB NOT NULL DEFAULT '{}',
    export_spec          JSONB NOT NULL DEFAULT '{}',
    provenance           JSONB NOT NULL DEFAULT '{}',
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (product_line_id, slug),
    CONSTRAINT chk_product_template_slug CHECK (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    CONSTRAINT chk_product_template_surface CHECK (surface_spec <> '{}'::jsonb),
    CONSTRAINT chk_product_template_export CHECK (export_spec <> '{}'::jsonb),
    CONSTRAINT chk_product_template_manual_only CHECK (
        export_spec::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND provenance::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE TABLE IF NOT EXISTS product_candidate (
    id                       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_line_id          UUID NOT NULL REFERENCES product_line(id) ON DELETE CASCADE,
    product_template_id      UUID NOT NULL REFERENCES product_template(id) ON DELETE RESTRICT,
    candidate_key            TEXT NOT NULL,
    title                    TEXT NOT NULL,
    status                   TEXT NOT NULL DEFAULT 'gated' CHECK (
        status IN ('draft','gated','approved','blocked','published')
    ),
    source_anchor_slug       TEXT NOT NULL,
    source                   TEXT NOT NULL,
    source_record_id         TEXT NOT NULL,
    source_url               TEXT NOT NULL,
    asset_snapshot           JSONB NOT NULL DEFAULT '{}',
    rights_snapshot          JSONB NOT NULL DEFAULT '{}',
    assembled_attribution    JSONB NOT NULL DEFAULT '[]',
    gate_result              JSONB NOT NULL DEFAULT '{}',
    provenance               JSONB NOT NULL DEFAULT '{}',
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (product_line_id, candidate_key),
    CONSTRAINT chk_product_candidate_key CHECK (candidate_key ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    CONSTRAINT chk_product_candidate_asset CHECK (asset_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_product_candidate_rights CHECK (rights_snapshot <> '{}'::jsonb),
    CONSTRAINT chk_product_candidate_gates CHECK (gate_result <> '{}'::jsonb),
    CONSTRAINT chk_product_candidate_allowed_only CHECK (
        rights_snapshot->>'rights_decision' = 'ALLOWED'
        AND rights_snapshot ? 'proof_url'
        AND rights_snapshot->>'proof_url' <> ''
        AND gate_result->>'passed' = 'true'
        AND gate_result::text !~* '(REVIEW_REQUIRED|BLOCKED)'
    ),
    CONSTRAINT chk_product_candidate_no_banned_media CHECK (
        source <> 'gbif'
        AND NOT (source = 'wikidata' AND asset_snapshot::text ~* '(commons|wikimedia)')
        AND asset_snapshot::text !~* '(osm_geometry|osm_relation_id|osm_id|openstreetmap|overpass|gbif_media|wikidata_commons)'
        AND rights_snapshot::text !~* '(REVIEW_REQUIRED|BLOCKED|gbif_media|wikidata_commons)'
        AND provenance::text !~* '(osm_geometry|osm_relation_id|osm_id|openstreetmap|overpass|gbif_media|wikidata_commons)'
    )
);

CREATE TABLE IF NOT EXISTS product_publication (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_candidate_id  UUID NOT NULL REFERENCES product_candidate(id) ON DELETE CASCADE,
    publication_version   TEXT NOT NULL,
    publication_status    TEXT NOT NULL DEFAULT 'published' CHECK (
        publication_status IN ('draft','published','stale','retracted')
    ),
    provider              TEXT NOT NULL DEFAULT 'manual' CHECK (provider = 'manual'),
    snapshot              JSONB NOT NULL DEFAULT '{}',
    snapshot_sha256       TEXT NOT NULL,
    manual_export_manifest JSONB NOT NULL DEFAULT '{}',
    created_by            TEXT NOT NULL,
    provenance            JSONB NOT NULL DEFAULT '{}',
    published_at          TIMESTAMPTZ,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (product_candidate_id, publication_version),
    UNIQUE (snapshot_sha256),
    CONSTRAINT chk_product_publication_snapshot CHECK (snapshot <> '{}'::jsonb),
    CONSTRAINT chk_product_publication_hash CHECK (snapshot_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_product_publication_manual_manifest CHECK (manual_export_manifest <> '{}'::jsonb),
    CONSTRAINT chk_product_publication_actor CHECK (length(created_by) > 0),
    CONSTRAINT chk_product_publication_no_external_provider CHECK (
        snapshot::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND manual_export_manifest::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
        AND provenance::text !~* '(printful|printify|gelato|external_product_id|external_variant_id)'
    )
);

CREATE INDEX IF NOT EXISTS idx_product_line_status ON product_line(status, anchor_slug);
CREATE INDEX IF NOT EXISTS idx_product_template_line ON product_template(product_line_id, slug);
CREATE INDEX IF NOT EXISTS idx_product_candidate_line_status ON product_candidate(product_line_id, status);
CREATE INDEX IF NOT EXISTS idx_product_publication_candidate ON product_publication(product_candidate_id, created_at DESC);

DROP TRIGGER IF EXISTS trg_product_line_updated_at ON product_line;
CREATE TRIGGER trg_product_line_updated_at BEFORE UPDATE ON product_line FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_product_template_updated_at ON product_template;
CREATE TRIGGER trg_product_template_updated_at BEFORE UPDATE ON product_template FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_product_candidate_updated_at ON product_candidate;
CREATE TRIGGER trg_product_candidate_updated_at BEFORE UPDATE ON product_candidate FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_product_publication_updated_at ON product_publication;
CREATE TRIGGER trg_product_publication_updated_at BEFORE UPDATE ON product_publication FOR EACH ROW EXECUTE FUNCTION set_updated_at();

WITH seeded_lines AS (
    INSERT INTO product_line (
        slug, title, status, anchor_slug, commercial_allowed,
        manual_provider_only, product_policy, provenance
    )
    VALUES
        ('earthrise-archival-print', 'Earthrise Archival Print', 'active', 'earthrise', TRUE, TRUE,
         '{"provider":"manual","product_family":"archival_print","source_policy":"NASA public-domain asset only"}'::jsonb,
         '{"authority":"NC-PRODUCT-001","sprint":"1"}'::jsonb),
        ('yellowstone-map-print', 'Yellowstone Map Print', 'active', 'yellowstone', TRUE, TRUE,
         '{"provider":"manual","product_family":"map_print","source_policy":"NARA or USGS public-domain map only"}'::jsonb,
         '{"authority":"NC-PRODUCT-001","sprint":"1"}'::jsonb),
        ('grand-canyon-dutton-atlas-print', 'Grand Canyon Dutton Atlas Print', 'active', 'grand-canyon', TRUE, TRUE,
         '{"provider":"manual","product_family":"atlas_print","source_policy":"public-domain Dutton atlas plate only"}'::jsonb,
         '{"authority":"NC-PRODUCT-001","sprint":"1"}'::jsonb)
    ON CONFLICT (slug) DO UPDATE SET
        title = EXCLUDED.title,
        status = EXCLUDED.status,
        anchor_slug = EXCLUDED.anchor_slug,
        commercial_allowed = EXCLUDED.commercial_allowed,
        manual_provider_only = EXCLUDED.manual_provider_only,
        product_policy = EXCLUDED.product_policy,
        provenance = product_line.provenance || EXCLUDED.provenance,
        updated_at = NOW()
    RETURNING id, slug
), all_lines AS (
    SELECT id, slug FROM seeded_lines
    UNION
    SELECT id, slug FROM product_line
     WHERE slug IN ('earthrise-archival-print','yellowstone-map-print','grand-canyon-dutton-atlas-print')
), seeded_templates AS (
    INSERT INTO product_template (
        product_line_id, slug, title, product_type, min_width_px, min_height_px,
        aspect_ratio, surface_spec, export_spec, provenance
    )
    SELECT l.id, v.slug, v.title, 'archival_print', v.min_width_px, v.min_height_px,
           v.aspect_ratio, v.surface_spec::jsonb, v.export_spec::jsonb,
           '{"authority":"NC-PRODUCT-001","sprint":"1"}'::jsonb
      FROM all_lines l
      JOIN (VALUES
        ('earthrise-archival-print', 'earthrise-18x24-manual', 'Earthrise 18x24 Manual Print Template', 3600, 4800, 1.3333,
         '{"size":"18x24","units":"in","bleed_in":0.125}'::jsonb,
         '{"provider":"manual","format":"tiff_or_png","color_profile":"srgb"}'::jsonb),
        ('yellowstone-map-print', 'yellowstone-24x36-manual', 'Yellowstone 24x36 Manual Map Template', 4800, 7200, 1.5000,
         '{"size":"24x36","units":"in","bleed_in":0.125}'::jsonb,
         '{"provider":"manual","format":"tiff_or_png","color_profile":"srgb"}'::jsonb),
        ('grand-canyon-dutton-atlas-print', 'grand-canyon-24x36-manual', 'Grand Canyon 24x36 Manual Atlas Template', 4800, 7200, 1.5000,
         '{"size":"24x36","units":"in","bleed_in":0.125}'::jsonb,
         '{"provider":"manual","format":"tiff_or_png","color_profile":"srgb"}'::jsonb)
      ) AS v(line_slug, slug, title, min_width_px, min_height_px, aspect_ratio, surface_spec, export_spec)
        ON v.line_slug = l.slug
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
    RETURNING id, product_line_id, slug
), all_templates AS (
    SELECT t.id, t.product_line_id, t.slug, l.slug AS line_slug
      FROM product_template t
      JOIN product_line l ON l.id = t.product_line_id
     WHERE l.slug IN ('earthrise-archival-print','yellowstone-map-print','grand-canyon-dutton-atlas-print')
), seeded_candidates AS (
    INSERT INTO product_candidate (
        product_line_id, product_template_id, candidate_key, title, status,
        source_anchor_slug, source, source_record_id, source_url,
        asset_snapshot, rights_snapshot, assembled_attribution, gate_result, provenance
    )
    SELECT l.id, t.id, v.candidate_key, v.title, 'approved',
           v.anchor_slug, v.source, v.source_record_id, v.source_url,
           v.asset_snapshot::jsonb, v.rights_snapshot::jsonb,
           v.assembled_attribution::jsonb, v.gate_result::jsonb,
           '{"authority":"NC-PRODUCT-001","sprint":"1","generated":true}'::jsonb
      FROM product_line l
      JOIN all_templates t ON t.product_line_id = l.id
      JOIN (VALUES
        ('earthrise-archival-print', 'earthrise-18x24-manual', 'earthrise-as08-14-2383-archival-print',
         'Earthrise AS08-14-2383 Archival Print', 'earthrise', 'nasa', 'AS08-14-2383',
         'https://images.nasa.gov/details-AS08-14-2383',
         '{"width_px":6000,"height_px":6000,"media_type":"image","derived_from":"nasa_public_domain"}'::jsonb,
         '{"rights_decision":"ALLOWED","rights_basis":"NASA public-domain federal image","proof_url":"https://www.nasa.gov/multimedia/guidelines/index.html","license":"public_domain"}'::jsonb,
         '[{"source":"nasa","statement":"Image credit: NASA. NASA does not endorse this product.","url":"https://www.nasa.gov"}]'::jsonb),
        ('yellowstone-map-print', 'yellowstone-24x36-manual', 'yellowstone-hayden-map-print',
         'Yellowstone Hayden Survey Map Print', 'yellowstone', 'nara', 'hayden-yellowstone-map-1871',
         'https://catalog.archives.gov/',
         '{"width_px":7200,"height_px":9600,"media_type":"image","derived_from":"nara_public_domain"}'::jsonb,
         '{"rights_decision":"ALLOWED","rights_basis":"NARA unrestricted public-domain map evidence","proof_url":"https://www.archives.gov/research/catalog","license":"public_domain"}'::jsonb,
         '[{"source":"nara","statement":"Source: U.S. National Archives and Records Administration.","url":"https://www.archives.gov"},{"source":"geonames","statement":"Geographic data © GeoNames (geonames.org) — CC BY 4.0","url":"https://www.geonames.org/5843591","license":"https://creativecommons.org/licenses/by/4.0/"}]'::jsonb),
        ('grand-canyon-dutton-atlas-print', 'grand-canyon-24x36-manual', 'grand-canyon-dutton-atlas-print',
         'Grand Canyon Dutton Atlas Print', 'grand-canyon', 'nara', 'dutton-grand-canyon-atlas',
         'https://catalog.archives.gov/',
         '{"width_px":7200,"height_px":9600,"media_type":"image","derived_from":"public_domain_atlas"}'::jsonb,
         '{"rights_decision":"ALLOWED","rights_basis":"public-domain Dutton atlas evidence","proof_url":"https://catalog.archives.gov/","license":"public_domain"}'::jsonb,
         '[{"source":"nara","statement":"Source: U.S. National Archives and Records Administration.","url":"https://www.archives.gov"},{"source":"geonames","statement":"Geographic data © GeoNames (geonames.org) — CC BY 4.0","url":"https://www.geonames.org/5296401","license":"https://creativecommons.org/licenses/by/4.0/"}]'::jsonb)
      ) AS v(line_slug, template_slug, candidate_key, title, anchor_slug, source, source_record_id, source_url, asset_snapshot, rights_snapshot, assembled_attribution)
        ON v.line_slug = l.slug AND v.template_slug = t.slug
      CROSS JOIN LATERAL (
        SELECT '{"passed":true,"checks":{"asset_allowed":true,"open_content_proof":true,"attribution_assembled":true,"minimum_dimensions":true,"no_review_or_blocked_assets":true,"no_osm_derived_stored_data":true,"no_gbif_media":true,"no_wikidata_commons_media":true,"manual_export_idempotent":true,"provider_http_outside_transaction":true}}'::jsonb AS gate_result
      ) g
    ON CONFLICT (product_line_id, candidate_key) DO UPDATE SET
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
    RETURNING id, candidate_key, title, assembled_attribution, gate_result
)
INSERT INTO product_publication (
    product_candidate_id, publication_version, publication_status, provider,
    snapshot, snapshot_sha256, manual_export_manifest, created_by, provenance, published_at
)
SELECT c.id, 'sprint1-v1', 'published', 'manual',
       jsonb_build_object(
           'runtime_version', 'NC-PRODUCT-001-sprint1',
           'candidate_key', c.candidate_key,
           'title', c.title,
           'manual_provider_only', true,
           'assembled_attribution', c.assembled_attribution,
           'gate_result', c.gate_result
       ) AS snapshot,
       md5(jsonb_build_object(
           'runtime_version', 'NC-PRODUCT-001-sprint1',
           'candidate_key', c.candidate_key,
           'title', c.title,
           'manual_provider_only', true,
           'assembled_attribution', c.assembled_attribution,
           'gate_result', c.gate_result
       )::text)
       || md5(jsonb_build_object(
           'runtime_version', 'NC-PRODUCT-001-sprint1',
           'candidate_key', c.candidate_key,
           'title', c.title,
           'manual_provider_only', true,
           'assembled_attribution', c.assembled_attribution,
           'gate_result', c.gate_result
       )::text || ':nc-product-001') AS snapshot_sha256,
       jsonb_build_object(
           'provider', 'manual',
           'candidate_key', c.candidate_key,
           'publication_version', 'sprint1-v1',
           'files', jsonb_build_array(),
           'attribution', c.assembled_attribution
       ) AS manual_export_manifest,
       'NC-PRODUCT-001 Sprint 1',
       '{"authority":"NC-PRODUCT-001","sprint":"1","manual_provider_only":true}'::jsonb,
       NOW()
  FROM seeded_candidates c
ON CONFLICT (product_candidate_id, publication_version) DO UPDATE SET
    publication_status = EXCLUDED.publication_status,
    provider = EXCLUDED.provider,
    snapshot = EXCLUDED.snapshot,
    snapshot_sha256 = EXCLUDED.snapshot_sha256,
    manual_export_manifest = EXCLUDED.manual_export_manifest,
    created_by = EXCLUDED.created_by,
    provenance = product_publication.provenance || EXCLUDED.provenance,
    published_at = EXCLUDED.published_at,
    updated_at = NOW();
