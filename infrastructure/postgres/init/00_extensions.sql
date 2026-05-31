-- Run once on first boot. Order matters: PostGIS before other extensions.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;      -- trigram indexes for name search
CREATE EXTENSION IF NOT EXISTS unaccent;     -- accent-insensitive search
CREATE EXTENSION IF NOT EXISTS btree_gin;    -- GIN indexes on scalar types
