-- Seed the source registry with all registered institutional sources.
-- Priority: lower number = higher authority.

INSERT INTO sources (source_id, name, institution, base_url, fetch_strategy, auth_type, priority, entity_types, standards, config)
VALUES
    (
        'unesco_whc',
        'UNESCO World Heritage Centre',
        'UNESCO',
        'https://whc.unesco.org',
        'api',
        'api_key',
        1,
        ARRAY['site'],
        ARRAY['prov_o', 'premis', 'iso_8601', 'iso_3166'],
        '{"api_version": "v2", "rate_limit": {"requests_per_second": 2, "burst": 5}}'
    ),
    (
        'unesco_ich',
        'UNESCO Intangible Cultural Heritage',
        'UNESCO',
        'https://ich.unesco.org',
        'api',
        'api_key',
        2,
        ARRAY['ich_element'],
        ARRAY['prov_o', 'premis', 'iso_8601', 'iso_3166'],
        '{"rate_limit": {"requests_per_second": 2, "burst": 5}}'
    ),
    (
        'wikidata',
        'Wikidata',
        'Wikimedia Foundation',
        'https://www.wikidata.org',
        'api',
        'none',
        3,
        ARRAY['site', 'ich_element', 'person', 'organization', 'taxon'],
        ARRAY['prov_o', 'skos', 'schema_org'],
        '{"sparql_endpoint": "https://query.wikidata.org/sparql", "entity_endpoint": "https://www.wikidata.org/wiki/Special:EntityData", "rate_limit": {"requests_per_second": 1, "burst": 3, "timeout_seconds": 60}}'
    ),
    (
        'wikimedia_commons',
        'Wikimedia Commons',
        'Wikimedia Foundation',
        'https://commons.wikimedia.org',
        'file',
        'none',
        4,
        ARRAY['image', 'video', 'audio'],
        ARRAY['prov_o', 'premis'],
        '{"api_endpoint": "https://commons.wikimedia.org/w/api.php", "rate_limit": {"requests_per_second": 1, "burst": 5}}'
    ),
    (
        'osm',
        'OpenStreetMap',
        'OpenStreetMap Foundation',
        'https://www.openstreetmap.org',
        'api',
        'none',
        5,
        ARRAY['geometry'],
        ARRAY['prov_o', 'premis'],
        '{"overpass_endpoint": "https://overpass-api.de/api/interpreter", "rate_limit": {"requests_per_second": 0.5, "burst": 2}}'
    ),
    (
        'geonames',
        'GeoNames',
        'GeoNames',
        'https://www.geonames.org',
        'api',
        'api_key',
        6,
        ARRAY['place'],
        ARRAY['prov_o', 'iso_3166'],
        '{"api_endpoint": "http://api.geonames.org", "rate_limit": {"requests_per_second": 1, "burst": 5}}'
    ),
    (
        'gbif',
        'Global Biodiversity Information Facility',
        'GBIF',
        'https://www.gbif.org',
        'api',
        'none',
        7,
        ARRAY['occurrence'],
        ARRAY['darwin_core', 'prov_o', 'premis'],
        '{"api_endpoint": "https://api.gbif.org/v1", "rate_limit": {"requests_per_second": 2, "burst": 10}}'
    ),
    (
        'iucn',
        'IUCN Red List',
        'IUCN',
        'https://www.iucnredlist.org',
        'api',
        'api_key',
        8,
        ARRAY['species'],
        ARRAY['darwin_core', 'prov_o'],
        '{"api_endpoint": "https://apiv3.iucnredlist.org/api/v3", "rate_limit": {"requests_per_second": 1, "burst": 3}}'
    ),
    (
        'europeana',
        'Europeana',
        'Europeana Foundation',
        'https://www.europeana.eu',
        'api',
        'api_key',
        9,
        ARRAY['cultural_object'],
        ARRAY['cidoc_crm', 'skos', 'prov_o', 'premis'],
        '{"api_endpoint": "https://api.europeana.eu/record/v2", "rate_limit": {"requests_per_second": 2, "burst": 10}}'
    )
ON CONFLICT (source_id) DO NOTHING;
