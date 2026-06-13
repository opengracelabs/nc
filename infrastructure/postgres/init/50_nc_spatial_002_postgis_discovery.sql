-- NC-SPATIAL-002: PostGIS discovery runtime.
-- Dedicated spatial tables for Discover nearby, within-region, and intersects APIs.

CREATE TABLE IF NOT EXISTS region_geometry (
    slug            TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    region_type     TEXT NOT NULL,
    geom            GEOMETRY(Geometry, 4326) NOT NULL,
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS place_geometry (
    slug            TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    place_type      TEXT NOT NULL,
    region_slug     TEXT REFERENCES region_geometry(slug),
    geom            GEOMETRY(Geometry, 4326) NOT NULL,
    centroid        GEOMETRY(Point, 4326) GENERATED ALWAYS AS (ST_PointOnSurface(geom)) STORED,
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS protected_area_geometry (
    slug            TEXT PRIMARY KEY,
    place_slug      TEXT NOT NULL REFERENCES place_geometry(slug),
    name            TEXT NOT NULL,
    protected_type  TEXT NOT NULL,
    geom            GEOMETRY(Geometry, 4326) NOT NULL,
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS region_geometry_geom_gix ON region_geometry USING GIST (geom);
CREATE INDEX IF NOT EXISTS place_geometry_geom_gix ON place_geometry USING GIST (geom);
CREATE INDEX IF NOT EXISTS place_geometry_centroid_gix ON place_geometry USING GIST (centroid);
CREATE INDEX IF NOT EXISTS place_geometry_region_idx ON place_geometry (region_slug);
CREATE INDEX IF NOT EXISTS protected_area_geometry_geom_gix ON protected_area_geometry USING GIST (geom);
CREATE INDEX IF NOT EXISTS protected_area_geometry_place_idx ON protected_area_geometry (place_slug);

INSERT INTO region_geometry (slug, name, region_type, geom, provenance)
VALUES
    (
        'western-north-america',
        'Western North America',
        'terrestrial_region',
        ST_GeomFromText('POLYGON((-125 28, -100 28, -100 50, -125 50, -125 28))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"regional envelope"}'::jsonb
    ),
    (
        'coral-sea',
        'Coral Sea',
        'marine_region',
        ST_GeomFromText('POLYGON((142 -25, 156 -25, 156 -9, 142 -9, 142 -25))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"regional envelope"}'::jsonb
    ),
    (
        'lunar-orbit',
        'Lunar Orbit',
        'non_terrestrial_viewpoint_region',
        ST_GeomFromText('POLYGON((-1 -1, 1 -1, 1 1, -1 1, -1 -1))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"symbolic non-terrestrial envelope"}'::jsonb
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    region_type = EXCLUDED.region_type,
    geom = EXCLUDED.geom,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO place_geometry (slug, name, place_type, region_slug, geom, provenance)
VALUES
    (
        'yellowstone',
        'Yellowstone',
        'national_park',
        'western-north-america',
        ST_GeomFromText('POLYGON((-111.25 44.10, -109.75 44.10, -109.75 45.15, -111.25 45.15, -111.25 44.10))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"discovery envelope"}'::jsonb
    ),
    (
        'grand-canyon',
        'Grand Canyon',
        'national_park',
        'western-north-america',
        ST_GeomFromText('POLYGON((-113.35 35.75, -111.45 35.75, -111.45 36.55, -113.35 36.55, -113.35 35.75))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"discovery envelope"}'::jsonb
    ),
    (
        'great-barrier-reef',
        'Great Barrier Reef',
        'marine_protected_area',
        'coral-sea',
        ST_GeomFromText('POLYGON((143.0 -24.5, 154.0 -24.5, 154.0 -10.0, 143.0 -10.0, 143.0 -24.5))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"discovery envelope"}'::jsonb
    ),
    (
        'earthrise',
        'Earthrise',
        'orbital_viewpoint',
        'lunar-orbit',
        ST_GeomFromText('POINT(0 0)', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"symbolic non-terrestrial point"}'::jsonb
    )
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    place_type = EXCLUDED.place_type,
    region_slug = EXCLUDED.region_slug,
    geom = EXCLUDED.geom,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO protected_area_geometry (slug, place_slug, name, protected_type, geom, provenance)
VALUES
    (
        'yellowstone-national-park',
        'yellowstone',
        'Yellowstone National Park',
        'national_park',
        ST_GeomFromText('POLYGON((-111.25 44.10, -109.75 44.10, -109.75 45.15, -111.25 45.15, -111.25 44.10))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"discovery envelope"}'::jsonb
    ),
    (
        'grand-canyon-national-park',
        'grand-canyon',
        'Grand Canyon National Park',
        'national_park',
        ST_GeomFromText('POLYGON((-113.35 35.75, -111.45 35.75, -111.45 36.55, -113.35 36.55, -113.35 35.75))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"discovery envelope"}'::jsonb
    ),
    (
        'great-barrier-reef-marine-park',
        'great-barrier-reef',
        'Great Barrier Reef Marine Park',
        'marine_park',
        ST_GeomFromText('POLYGON((143.0 -24.5, 154.0 -24.5, 154.0 -10.0, 143.0 -10.0, 143.0 -24.5))', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"discovery envelope"}'::jsonb
    ),
    (
        'apollo-8-lunar-orbit-viewpoint',
        'earthrise',
        'Apollo 8 Lunar Orbit Viewpoint',
        'symbolic_viewpoint',
        ST_GeomFromText('POINT(0 0)', 4326),
        '{"source":"NC-SPATIAL-002 seed","precision":"symbolic non-terrestrial point"}'::jsonb
    )
ON CONFLICT (slug) DO UPDATE SET
    place_slug = EXCLUDED.place_slug,
    name = EXCLUDED.name,
    protected_type = EXCLUDED.protected_type,
    geom = EXCLUDED.geom,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
