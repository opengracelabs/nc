"""NC-DATA-002 authority resolution schema replay tests."""

from pathlib import Path

MIGRATION_47 = Path(
    "infrastructure/postgres/init/47_nc_data_002_authority_resolution_pilot_places.sql"
)


REQUIRED_IDENTITIES = {
    "grand-canyon": ("geonames:5296401", "5296401", "Q220289"),
    "great-barrier-reef": ("geonames:2164628", "2164628", "Q7343"),
    "galapagos": ("geonames:3658931", "3658931", "Q38095"),
    "venice": ("geonames:3164603", "3164603", "Q641"),
    "papahanaumokuakea": ("wikidata:Q787425", "11854341", "Q787425"),
}


def test_nc_data_002_migration_exists() -> None:
    assert MIGRATION_47.exists()


def test_nc_data_002_preserves_one_canonical_place_id_index() -> None:
    sql = MIGRATION_47.read_text(encoding="utf-8")

    assert "uq_authority_resolution_one_canonical_place" in sql
    assert "WHERE authority_role = 'canonical_place_id' AND status = 'active'" in sql
    assert "canonical_place_id    TEXT NOT NULL UNIQUE" not in sql
    assert "canonical_place_id = 'geonames:' || geonames_id" in sql
    assert "canonical_place_id = 'wikidata:' || wikidata_qid" in sql


def test_nc_data_002_extends_supported_canonical_authorities() -> None:
    sql = MIGRATION_47.read_text(encoding="utf-8")

    assert "DROP CONSTRAINT IF EXISTS chk_authority_resolution_no_wikidata_canonical" in sql
    assert "canonical_authority IN ('geonames','wikidata')" in sql
    assert "authority = 'gbif' AND authority_role = 'canonical_place_id'" not in sql


def test_nc_data_002_seeds_required_pilot_places() -> None:
    sql = MIGRATION_47.read_text(encoding="utf-8")

    for slug, (canonical_place_id, geonames_id, wikidata_qid) in REQUIRED_IDENTITIES.items():
        assert f"'{slug}'" in sql
        assert f"'{canonical_place_id}'" in sql
        assert f"'{geonames_id}'" in sql
        assert f"'{wikidata_qid}'" in sql


def test_nc_data_002_keeps_papahanaumokuakea_geonames_unconfirmed() -> None:
    sql = MIGRATION_47.read_text(encoding="utf-8")

    assert "'papahanaumokuakea', 'wikidata', 'Q787425', 'canonical_place_id'" in sql
    assert "'papahanaumokuakea', 'geonames', '11854341', 'cross_reference'" in sql
    assert "geonames_status" in sql
    assert "unconfirmed" in sql


def test_nc_data_002_uses_idempotent_upserts() -> None:
    sql = MIGRATION_47.read_text(encoding="utf-8")

    assert "ON CONFLICT (anchor_slug, authority, authority_record_id) DO UPDATE" in sql
    assert "ON CONFLICT (anchor_slug) DO UPDATE" in sql
