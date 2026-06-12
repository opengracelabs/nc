-- NC-DATA-004 fixture-backed authority ratification.
-- Ratification requires fixture-backed evidence. No provisional promotion.

-- Great Barrier Reef has captured GeoNames and Wikidata fixture bundles and can remain ratified.
UPDATE authority_resolution_registry
SET evidence = evidence || '{
        "fixture_backed": true,
        "fixture_manifest_paths": [
            "tests/fixtures/geonames/great_barrier_reef/manifest.json",
            "tests/fixtures/wikidata/great_barrier_reef/manifest.json"
        ],
        "ratification_status": "ratified_fixture_backed",
        "resolution": "canonical"
    }'::jsonb,
    provenance = provenance || '{"authority":"NC-DATA-004","decision":"fixture-backed ratification"}'::jsonb,
    updated_at = NOW()
WHERE anchor_slug = 'great-barrier-reef'
  AND authority = 'geonames'
  AND authority_record_id = '2164628';

UPDATE canonical_identity
SET identity = identity || '{
        "fixture_backed": true,
        "fixture_manifest_paths": [
            "tests/fixtures/geonames/great_barrier_reef/manifest.json",
            "tests/fixtures/wikidata/great_barrier_reef/manifest.json"
        ],
        "ratification_status": "ratified_fixture_backed"
    }'::jsonb,
    provenance = provenance || '{"authority":"NC-DATA-004","rule":"fixture-backed evidence before ratification"}'::jsonb,
    updated_at = NOW()
WHERE anchor_slug = 'great-barrier-reef'
  AND canonical_place_id = 'geonames:2164628';

-- Galapagos and Venice have authority evidence but no NC-DATA-004 fixture bundle yet.
UPDATE authority_resolution_registry
SET authority_role = 'cross_reference',
    confidence = LEAST(confidence, 0.8200),
    evidence = evidence || '{
        "fixture_backed": false,
        "ratification_status": "blocked_missing_fixture",
        "resolution": "evidence only; not ratified"
    }'::jsonb,
    provenance = provenance || '{"authority":"NC-DATA-004","decision":"demoted until fixture-backed"}'::jsonb,
    updated_at = NOW()
WHERE anchor_slug IN ('galapagos','venice')
  AND authority = 'geonames'
  AND authority_role = 'canonical_place_id';

DELETE FROM canonical_identity
WHERE anchor_slug IN ('galapagos','venice');

-- Papahanaumokuakea must not be provisionally promoted from Wikidata while GeoNames is unconfirmed.
UPDATE authority_resolution_registry
SET authority_role = 'cross_reference',
    confidence = LEAST(confidence, 0.7200),
    evidence = evidence || '{
        "fixture_backed": false,
        "geonames_status": "unconfirmed",
        "ratification_status": "blocked_missing_fixture",
        "resolution": "no provisional promotion"
    }'::jsonb,
    provenance = provenance || '{"authority":"NC-DATA-004","decision":"no provisional promotion"}'::jsonb,
    updated_at = NOW()
WHERE anchor_slug = 'papahanaumokuakea'
  AND authority = 'wikidata'
  AND authority_role = 'canonical_place_id';

UPDATE authority_resolution_registry
SET evidence = evidence || '{
        "fixture_backed": false,
        "geonames_status": "unconfirmed",
        "ratification_status": "blocked_missing_fixture",
        "resolution": "candidate only; not ratified"
    }'::jsonb,
    provenance = provenance || '{"authority":"NC-DATA-004","decision":"candidate only"}'::jsonb,
    updated_at = NOW()
WHERE anchor_slug = 'papahanaumokuakea'
  AND authority = 'geonames';

DELETE FROM canonical_identity
WHERE anchor_slug = 'papahanaumokuakea';

-- Keep evidence rows present for all NC-DATA-004 anchors, without creating canonical identities.
INSERT INTO authority_resolution_registry (
    anchor_slug, authority, authority_record_id, authority_role,
    confidence, evidence, status, provenance
)
VALUES
    (
        'galapagos', 'geonames', '3658931', 'cross_reference',
        0.8200,
        '{"name":"Galapagos Islands","feature_code":"ISLS","source_url":"https://www.geonames.org/3658931","fixture_backed":false,"ratification_status":"blocked_missing_fixture","resolution":"evidence only; not ratified"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-004","decision":"fixture required before ratification"}'::jsonb
    ),
    (
        'galapagos', 'wikidata', 'Q38095', 'cross_reference',
        0.8200,
        '{"label":"Galapagos Islands","geonames_id_claim":"3658931","source_url":"https://www.wikidata.org/wiki/Q38095","fixture_backed":false,"ratification_status":"blocked_missing_fixture","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-004","decision":"not canonical"}'::jsonb
    ),
    (
        'venice', 'geonames', '3164603', 'cross_reference',
        0.8200,
        '{"name":"Venice","feature_code":"PPLA","source_url":"https://www.geonames.org/3164603","fixture_backed":false,"ratification_status":"blocked_missing_fixture","resolution":"evidence only; not ratified"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-004","decision":"fixture required before ratification"}'::jsonb
    ),
    (
        'venice', 'wikidata', 'Q641', 'cross_reference',
        0.8200,
        '{"label":"Venice","geonames_id_claim":"3164603","source_url":"https://www.wikidata.org/wiki/Q641","fixture_backed":false,"ratification_status":"blocked_missing_fixture","resolution":"identity evidence only"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-004","decision":"not canonical"}'::jsonb
    ),
    (
        'papahanaumokuakea', 'wikidata', 'Q787425', 'cross_reference',
        0.7200,
        '{"label":"Papahanaumokuakea Marine National Monument","diacritics":"Papahānaumokuākea","geonames_status":"unconfirmed","fixture_backed":false,"ratification_status":"blocked_missing_fixture","resolution":"no provisional promotion"}'::jsonb,
        'active',
        '{"authority":"NC-DATA-004","decision":"not canonical"}'::jsonb
    )
ON CONFLICT (anchor_slug, authority, authority_record_id) DO UPDATE SET
    authority_role = EXCLUDED.authority_role,
    confidence = EXCLUDED.confidence,
    evidence = authority_resolution_registry.evidence || EXCLUDED.evidence,
    status = EXCLUDED.status,
    provenance = authority_resolution_registry.provenance || EXCLUDED.provenance,
    updated_at = NOW();
