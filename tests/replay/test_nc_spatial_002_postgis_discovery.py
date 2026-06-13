from pathlib import Path

MIGRATION = Path("infrastructure/postgres/init/50_nc_spatial_002_postgis_discovery.sql")
ROUTER = Path("services/api/routers/discover.py")


def test_nc_spatial_002_migration_exists() -> None:
    assert MIGRATION.exists()


def test_nc_spatial_002_creates_required_tables() -> None:
    sql = MIGRATION.read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS place_geometry" in sql
    assert "CREATE TABLE IF NOT EXISTS region_geometry" in sql
    assert "CREATE TABLE IF NOT EXISTS protected_area_geometry" in sql
    assert "GEOMETRY(Geometry, 4326)" in sql
    assert "USING GIST" in sql


def test_nc_spatial_002_loads_required_places() -> None:
    sql = MIGRATION.read_text(encoding="utf-8")

    for slug in ("Yellowstone", "Grand Canyon", "Great Barrier Reef", "Earthrise"):
        assert slug in sql
    for slug in ("yellowstone", "grand-canyon", "great-barrier-reef", "earthrise"):
        assert slug in sql


def test_nc_spatial_002_router_exposes_required_endpoints() -> None:
    source = ROUTER.read_text(encoding="utf-8")

    assert '@router.get("/nearby")' in source
    assert '@router.get("/within-region")' in source
    assert '@router.get("/intersects")' in source


def test_nc_spatial_002_router_uses_postgis_functions() -> None:
    source = ROUTER.read_text(encoding="utf-8")

    assert "ST_DWithin" in source
    assert "ST_Distance" in source
    assert "ST_Within" in source
    assert "ST_Intersects" in source
    assert "ST_AsGeoJSON" in source
