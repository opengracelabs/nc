-- NC-DATA-002 authority resolution registry extension.
-- Extends canonical place identity support to pilot places while preserving one
-- active canonical place ID per anchor.

ALTER TABLE authority_resolution_registry
    DROP CONSTRAINT IF EXISTS chk_authority_resolution_no_wikidata_canonical;

CREATE UNIQUE INDEX IF NOT EXISTS uq_authority_resolution_one_canonical_place
    ON authority_resolution_registry(anchor_slug)
    WHERE authority_role = 'canonical_place_id' AND status = 'active';

ALTER TABLE canonical_identity
    DROP CONSTRAINT IF EXISTS canonical_identity_canonical_authority_check,
    DROP CONSTRAINT IF EXISTS chk_canonical_identity_geonames,
    DROP CONSTRAINT IF EXISTS chk_canonical_identity_authority,
    DROP CONSTRAINT IF EXISTS chk_canonical_identity_canonical_place_id;

ALTER TABLE canonical_identity
    ADD CONSTRAINT chk_canonical_identity_authority CHECK (
        canonical_authority IN ('geonames','wikidata')
    ),
    ADD CONSTRAINT chk_canonical_identity_canonical_place_id CHECK (
        (
            canonical_authority = 'geonames'
            AND geonames_id IS NOT NULL
            AND canonical_place_id = 'geonames:' || geonames_id
        )
        OR (
            canonical_authority = 'wikidata'
            AND wikidata_qid IS NOT NULL
            AND canonical_place_id = 'wikidata:' || wikidata_qid
        )
    );

INSERT INTO authority_resolution_registry (
    anchor_slug, authority, authority_record_id, authority_role,
    confidence, evidence, status, provenance
)
VALUES
    (
        'grand-canyon', 'geonames', '5296401', 'canonical_place_id',
        1.0000,
        '{"name":"Grand Canyon National Park","feature_code":"PRK","source_url":"https://www.geonames.org/5296401","resolution":"canonical"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"one canonical place ID only"}'::jsonb
    ),
    (
        'grand-canyon', 'wikidata', 'Q220289', 'cross_reference',
        0.9700,
        '{"label":"Grand Canyon National Park","geonames_id_claim":"5296401","source_url":"https://www.wikidata.org/wiki/Q220289","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'grand-canyon', 'gbif', 'grand-canyon-place-validation', 'validation_only',
        0.7000,
        '{"source_role":"validation_only","media_allowed":false,"resolution":"biodiversity relevance evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'great-barrier-reef', 'geonames', '2164628', 'canonical_place_id',
        1.0000,
        '{"name":"Great Barrier Reef","feature_code":"RF","source_url":"https://www.geonames.org/2164628","resolution":"canonical"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"one canonical place ID only"}'::jsonb
    ),
    (
        'great-barrier-reef', 'wikidata', 'Q7343', 'cross_reference',
        0.9700,
        '{"label":"Great Barrier Reef","geonames_id_claim":"2164628","source_url":"https://www.wikidata.org/wiki/Q7343","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'great-barrier-reef', 'gbif', 'great-barrier-reef-place-validation', 'validation_only',
        0.7000,
        '{"source_role":"validation_only","media_allowed":false,"resolution":"biodiversity relevance evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'galapagos', 'geonames', '3658931', 'canonical_place_id',
        1.0000,
        '{"name":"Galapagos Islands","feature_code":"ISLS","source_url":"https://www.geonames.org/3658931","resolution":"canonical"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"one canonical place ID only"}'::jsonb
    ),
    (
        'galapagos', 'wikidata', 'Q38095', 'cross_reference',
        0.9700,
        '{"label":"Galapagos Islands","geonames_id_claim":"3658931","source_url":"https://www.wikidata.org/wiki/Q38095","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'galapagos', 'gbif', 'galapagos-place-validation', 'validation_only',
        0.7000,
        '{"source_role":"validation_only","media_allowed":false,"resolution":"biodiversity relevance evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'venice', 'geonames', '3164603', 'canonical_place_id',
        1.0000,
        '{"name":"Venice","feature_code":"PPLA","source_url":"https://www.geonames.org/3164603","resolution":"canonical"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"one canonical place ID only"}'::jsonb
    ),
    (
        'venice', 'wikidata', 'Q641', 'cross_reference',
        0.9700,
        '{"label":"Venice","geonames_id_claim":"3164603","source_url":"https://www.wikidata.org/wiki/Q641","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'venice', 'gbif', 'venice-place-validation', 'validation_only',
        0.5500,
        '{"source_role":"validation_only","media_allowed":false,"resolution":"biodiversity relevance evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'papahanaumokuakea', 'wikidata', 'Q787425', 'canonical_place_id',
        1.0000,
        '{"name":"Papahanaumokuakea Marine National Monument","diacritics":"Papahānaumokuākea","geonames_status":"unconfirmed","source_url":"https://www.wikidata.org/wiki/Q787425","resolution":"canonical until GeoNames ID is confirmed"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"one canonical place ID only"}'::jsonb
    ),
    (
        'papahanaumokuakea', 'geonames', '11854341', 'cross_reference',
        0.3500,
        '{"name":"Papahanaumokuakea candidate","source_url":"https://www.geonames.org/11854341","geonames_status":"unconfirmed","resolution":"candidate only; not canonical until confirmed by NC GeoNames account lookup"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
    ),
    (
        'papahanaumokuakea', 'gbif', 'papahanaumokuakea-place-validation', 'validation_only',
        0.7000,
        '{"source_role":"validation_only","media_allowed":false,"resolution":"biodiversity relevance evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","decision":"not canonical"}'::jsonb
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
VALUES
    (
        'grand-canyon', 'geonames:5296401', 'geonames', 'Grand Canyon National Park',
        '5296401', 'Q220289', 'grand-canyon-place-validation',
        '{"canonical_place_id":"geonames:5296401","anchor_slug":"grand-canyon","label":"Grand Canyon National Park","geonames_id":"5296401","wikidata_qid":"Q220289","gbif_place_key":"grand-canyon-place-validation"}'::jsonb,
        '[{"authority":"geonames","authority_record_id":"5296401","role":"canonical_place_id"},{"authority":"wikidata","authority_record_id":"Q220289","role":"cross_reference"},{"authority":"gbif","authority_record_id":"grand-canyon-place-validation","role":"validation_only"}]'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","rule":"one canonical place ID only"}'::jsonb
    ),
    (
        'great-barrier-reef', 'geonames:2164628', 'geonames', 'Great Barrier Reef',
        '2164628', 'Q7343', 'great-barrier-reef-place-validation',
        '{"canonical_place_id":"geonames:2164628","anchor_slug":"great-barrier-reef","label":"Great Barrier Reef","geonames_id":"2164628","wikidata_qid":"Q7343","gbif_place_key":"great-barrier-reef-place-validation"}'::jsonb,
        '[{"authority":"geonames","authority_record_id":"2164628","role":"canonical_place_id"},{"authority":"wikidata","authority_record_id":"Q7343","role":"cross_reference"},{"authority":"gbif","authority_record_id":"great-barrier-reef-place-validation","role":"validation_only"}]'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","rule":"one canonical place ID only"}'::jsonb
    ),
    (
        'galapagos', 'geonames:3658931', 'geonames', 'Galapagos Islands',
        '3658931', 'Q38095', 'galapagos-place-validation',
        '{"canonical_place_id":"geonames:3658931","anchor_slug":"galapagos","label":"Galapagos Islands","geonames_id":"3658931","wikidata_qid":"Q38095","gbif_place_key":"galapagos-place-validation"}'::jsonb,
        '[{"authority":"geonames","authority_record_id":"3658931","role":"canonical_place_id"},{"authority":"wikidata","authority_record_id":"Q38095","role":"cross_reference"},{"authority":"gbif","authority_record_id":"galapagos-place-validation","role":"validation_only"}]'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","rule":"one canonical place ID only"}'::jsonb
    ),
    (
        'venice', 'geonames:3164603', 'geonames', 'Venice',
        '3164603', 'Q641', 'venice-place-validation',
        '{"canonical_place_id":"geonames:3164603","anchor_slug":"venice","label":"Venice","geonames_id":"3164603","wikidata_qid":"Q641","gbif_place_key":"venice-place-validation"}'::jsonb,
        '[{"authority":"geonames","authority_record_id":"3164603","role":"canonical_place_id"},{"authority":"wikidata","authority_record_id":"Q641","role":"cross_reference"},{"authority":"gbif","authority_record_id":"venice-place-validation","role":"validation_only"}]'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","rule":"one canonical place ID only"}'::jsonb
    ),
    (
        'papahanaumokuakea', 'wikidata:Q787425', 'wikidata', 'Papahanaumokuakea Marine National Monument',
        NULL, 'Q787425', 'papahanaumokuakea-place-validation',
        '{"canonical_place_id":"wikidata:Q787425","anchor_slug":"papahanaumokuakea","label":"Papahanaumokuakea Marine National Monument","diacritics":"Papahānaumokuākea","wikidata_qid":"Q787425","geonames_status":"unconfirmed","gbif_place_key":"papahanaumokuakea-place-validation"}'::jsonb,
        '[{"authority":"wikidata","authority_record_id":"Q787425","role":"canonical_place_id"},{"authority":"geonames","authority_record_id":"11854341","role":"cross_reference"},{"authority":"gbif","authority_record_id":"papahanaumokuakea-place-validation","role":"validation_only"}]'::jsonb,
        'active',
        '{"authority":"NC-DATA-002","rule":"one canonical place ID only","geonames_status":"unconfirmed"}'::jsonb
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
