-- Migration 37: Gallica production deactivation.
-- Authority: DD-GALLICA-003.
--
-- Gallica is retained for research, fixtures, and dry-run adapter maintenance,
-- but retired from the production source list because BnF platform terms impose
-- a commercial reuse license fee. New ingestion is not permitted.

ALTER TABLE sources
    ADD COLUMN IF NOT EXISTS commercial_status TEXT NOT NULL DEFAULT 'unknown'
        CONSTRAINT chk_source_commercial_status CHECK (commercial_status IN (
            'unrestricted',
            'restricted',
            'unknown'
        ));

INSERT INTO sources (
    source_id,
    name,
    institution,
    base_url,
    fetch_strategy,
    auth_type,
    priority,
    entity_types,
    standards,
    governance_state,
    operational_status,
    status,
    commercial_status,
    config,
    provenance
)
VALUES (
    'bnf_gallica',
    'BnF Gallica',
    'Bibliotheque nationale de France',
    'https://gallica.bnf.fr',
    'api',
    'none',
    99,
    ARRAY['cultural_object', 'image', 'map', 'book'],
    ARRAY['iiif', 'oai_pmh', 'dc', 'prov_o', 'premis'],
    'deprecated',
    'unavailable',
    'deprecated',
    'restricted',
    '{
        "api_endpoint": "https://gallica.bnf.fr",
        "oai_endpoint": "https://oai.bnf.fr/oai2/OAIHandler",
        "adapter": "workers.gallica_adapter",
        "dry_run_only": true,
        "ingestion_enabled": false,
        "commercial_status": "restricted",
        "deactivation_authority": "DD-GALLICA-003",
        "deactivation_reason": "commercial_reuse_license_fee_required"
    }'::jsonb,
    '{
        "decision": "DD-GALLICA-003",
        "migration_note": "Gallica retired from production source list.",
        "code_retained": true,
        "tests_retained": true,
        "fixtures_retained": true
    }'::jsonb
)
ON CONFLICT (source_id) DO UPDATE SET
    governance_state = 'deprecated',
    operational_status = 'unavailable',
    status = 'deprecated',
    commercial_status = 'restricted',
    config = sources.config || EXCLUDED.config,
    provenance = sources.provenance || EXCLUDED.provenance,
    updated_at = NOW();

UPDATE sources
SET
    governance_state = 'deprecated',
    operational_status = 'unavailable',
    status = 'deprecated',
    commercial_status = 'restricted',
    config = config || '{
        "dry_run_only": true,
        "ingestion_enabled": false,
        "commercial_status": "restricted",
        "deactivation_authority": "DD-GALLICA-003",
        "deactivation_reason": "commercial_reuse_license_fee_required"
    }'::jsonb,
    provenance = provenance || '{
        "decision": "DD-GALLICA-003",
        "migration_note": "Gallica retired from production source list."
    }'::jsonb,
    updated_at = NOW()
WHERE source_id IN ('bnf_gallica', 'gallica');
