-- Canonical Vocabulary v1.0 Seed Migration
-- Seeds institutional actors, heritage types, criteria, and multilingual labels.

-- Institutional Actors
INSERT INTO concepts (concept_type, concept_key, label, provenance)
VALUES
    ('institution', 'unesco', '{"en": "UNESCO", "fr": "UNESCO"}'::jsonb, '{"nc:version": "1.0", "nc:role": "Authority"}'::jsonb),
    ('institution', 'iucn', '{"en": "IUCN", "fr": "UICN"}'::jsonb, '{"nc:version": "1.0", "nc:role": "Advisory Body"}'::jsonb),
    ('institution', 'icomos', '{"en": "ICOMOS", "fr": "ICOMOS"}'::jsonb, '{"nc:version": "1.0", "nc:role": "Advisory Body"}'::jsonb),
    ('institution', 'iccrom', '{"en": "ICCROM", "fr": "ICCROM"}'::jsonb, '{"nc:version": "1.0", "nc:role": "Advisory Body"}'::jsonb)
ON CONFLICT (concept_type, concept_key) DO UPDATE SET
    label = EXCLUDED.label,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

-- Heritage Types
INSERT INTO concepts (concept_type, concept_key, label, provenance)
VALUES
    ('heritage_type', 'cultural', '{"en": "Cultural Heritage", "fr": "Patrimoine culturel"}'::jsonb, '{"nc:version": "1.0"}'::jsonb),
    ('heritage_type', 'natural', '{"en": "Natural Heritage", "fr": "Patrimoine naturel"}'::jsonb, '{"nc:version": "1.0"}'::jsonb),
    ('heritage_type', 'mixed', '{"en": "Mixed Heritage", "fr": "Patrimoine mixte"}'::jsonb, '{"nc:version": "1.0"}'::jsonb)
ON CONFLICT (concept_type, concept_key) DO UPDATE SET
    label = EXCLUDED.label,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

-- UNESCO Designations
INSERT INTO concepts (concept_type, concept_key, label, provenance)
VALUES
    ('designation', 'world_heritage_site', '{"en": "UNESCO World Heritage Site", "fr": "Patrimoine mondial de l''UNESCO"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q9259"}'::jsonb),
    ('designation', 'biosphere_reserve', '{"en": "UNESCO Biosphere Reserve", "fr": "Réserve de biosphère de l''UNESCO"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q158454"}'::jsonb),
    ('designation', 'ramsar_site', '{"en": "Ramsar Site", "fr": "Site Ramsar"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q170145"}'::jsonb)
ON CONFLICT (concept_type, concept_key) DO UPDATE SET
    label = EXCLUDED.label,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

-- UNESCO Criteria
INSERT INTO concepts (concept_type, concept_key, label, provenance)
VALUES
    ('ouv_criterion', 'i', '{"en": "Criterion (i)", "fr": "Critère (i)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Cultural"}'::jsonb),
    ('ouv_criterion', 'ii', '{"en": "Criterion (ii)", "fr": "Critère (ii)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Cultural"}'::jsonb),
    ('ouv_criterion', 'iii', '{"en": "Criterion (iii)", "fr": "Critère (iii)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Cultural"}'::jsonb),
    ('ouv_criterion', 'iv', '{"en": "Criterion (iv)", "fr": "Critère (iv)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Cultural"}'::jsonb),
    ('ouv_criterion', 'v', '{"en": "Criterion (v)", "fr": "Critère (v)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Cultural"}'::jsonb),
    ('ouv_criterion', 'vi', '{"en": "Criterion (vi)", "fr": "Critère (vi)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Cultural"}'::jsonb),
    ('ouv_criterion', 'vii', '{"en": "Criterion (vii)", "fr": "Critère (vii)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Natural"}'::jsonb),
    ('ouv_criterion', 'viii', '{"en": "Criterion (viii)", "fr": "Critère (viii)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Natural"}'::jsonb),
    ('ouv_criterion', 'ix', '{"en": "Criterion (ix)", "fr": "Critère (ix)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Natural"}'::jsonb),
    ('ouv_criterion', 'x', '{"en": "Criterion (x)", "fr": "Critère (x)"}'::jsonb, '{"nc:version": "1.0", "nc:domain": "Natural"}'::jsonb)
ON CONFLICT (concept_type, concept_key) DO UPDATE SET
    label = EXCLUDED.label,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

-- Sample Countries
INSERT INTO concepts (concept_type, concept_key, label, provenance)
VALUES
    ('country', 'AU', '{"en": "Australia", "fr": "Australie"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q408"}'::jsonb),
    ('country', 'FR', '{"en": "France", "fr": "France"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q142"}'::jsonb),
    ('country', 'EC', '{"en": "Ecuador", "fr": "Équateur"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q736"}'::jsonb),
    ('country', 'TZ', '{"en": "Tanzania", "fr": "Tanzanie"}'::jsonb, '{"nc:version": "1.0", "nc:wikidata_qid": "Q924"}'::jsonb)
ON CONFLICT (concept_type, concept_key) DO UPDATE SET
    label = EXCLUDED.label,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
