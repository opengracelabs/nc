-- NC-DATA-001: Correct Yellowstone canonical GeoNames ID from 5843642 to 5843591.
-- 5843642 was adopted based on an erroneous Wikidata P1566 confirmation claim.
-- The authoritative ID is 5843591, returned by three independent GeoNames API fixtures.
-- See docs/governance/NC-DATA-001_yellowstone_authority_resolution.md.

-- 1. Fix pilot_anchor canonical identity for Yellowstone.
UPDATE pilot_anchor
SET
    canonical_identity = jsonb_set(
        canonical_identity,
        '{preferred_geonames_id}',
        '"5843591"'
    ),
    updated_at = NOW()
WHERE slug = 'yellowstone'
  AND canonical_identity->>'preferred_geonames_id' = '5843642';

-- 2. Fix product_candidate assembled_attribution GeoNames URL for Yellowstone.
UPDATE product_candidate
SET assembled_attribution = (
    SELECT jsonb_agg(
        CASE
            WHEN elem->>'source' = 'geonames'
            THEN jsonb_set(elem, '{url}', '"https://www.geonames.org/5843591"')
            ELSE elem
        END
    )
    FROM jsonb_array_elements(assembled_attribution) AS elem
)
WHERE source_anchor_slug = 'yellowstone'
  AND assembled_attribution::text LIKE '%geonames.org/5843642%';
