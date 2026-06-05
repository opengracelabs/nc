"""Collection #000001 replay tests."""
from pathlib import Path
from uuid import uuid4

from services.api.routers.collections import _TRANSITIONS
from workers.collection_export_worker.export import build_collection_export_manifest

MIGRATION_16 = Path("infrastructure/postgres/init/16_taxon_discovery.sql")

_COLLECTION_ID = uuid4()
_PLACE_ID = uuid4()
_ASSET_A = uuid4()
_ASSET_B = uuid4()


def _collection() -> dict:
    return {
        "id": _COLLECTION_ID,
        "slug": "great-barrier-reef-flora",
        "title": "Great Barrier Reef Flora",
        "summary": "Verified public-domain illustrations for a place-centered set.",
        "collection_type": "place_theme",
        "status": "approved",
    }


def _assets() -> list[dict]:
    return [
        {
            "asset_id": _ASSET_B,
            "sequence": 2,
            "role": "supporting",
            "title": "Plate B",
            "caption": "Second plate",
            "credit_line": "BHL",
            "rights_status": "CC0",
            "rights_source_url": None,
            "raw_path": "bhl/illustrations/b.jpg",
            "normalized_path": None,
            "checksum_sha256": "bbb",
            "source_url": "https://www.biodiversitylibrary.org/page/2",
            "bhl_page_id": "2",
        },
        {
            "asset_id": _ASSET_A,
            "sequence": 1,
            "role": "cover",
            "title": "Plate A",
            "caption": "First plate",
            "credit_line": "BHL",
            "rights_status": "Public Domain",
            "rights_source_url": "https://www.biodiversitylibrary.org/page/1",
            "raw_path": "bhl/illustrations/a.jpg",
            "normalized_path": None,
            "checksum_sha256": "aaa",
            "source_url": "https://www.biodiversitylibrary.org/page/1",
            "bhl_page_id": "1",
        },
    ]


def test_collection_schema_models_governed_commercial_sets() -> None:
    sql = MIGRATION_16.read_text()

    assert "CREATE TABLE collections" in sql
    assert "slug                TEXT NOT NULL UNIQUE" in sql
    assert "collection_type     TEXT NOT NULL DEFAULT 'place_theme'" in sql
    assert "'draft','approved','published','rejected','disputed','retracted'" in sql
    assert "reviewed_by         TEXT" in sql
    assert "published_at        TIMESTAMPTZ" in sql


def test_collection_assets_require_verified_public_domain_bhl_assets() -> None:
    sql = MIGRATION_16.read_text()

    assert "CREATE TABLE collection_assets" in sql
    assert "asset_id            UUID NOT NULL REFERENCES assets(id)" in sql
    assert "sequence            INT NOT NULL CHECK (sequence > 0)" in sql
    assert "check_collection_asset_commercial_ready" in sql
    assert "a.asset_type = 'bhl_illustration'" in sql
    assert "r.rights_status IN ('Public Domain','CC0')" in sql
    assert "does not match opportunity" in sql


def test_collection_publish_requires_place_asset_and_reviewer() -> None:
    sql = MIGRATION_16.read_text()

    assert "CREATE TABLE collection_places" in sql
    assert "UNIQUE (collection_id, place_id)" in sql
    assert "check_collection_publishable" in sql
    assert "has no place connection" in sql
    assert "has no verified assets" in sql
    assert "has no reviewer" in sql


def test_collection_exports_are_recorded_with_integrity_metadata() -> None:
    sql = MIGRATION_16.read_text()

    assert "CREATE TABLE collection_exports" in sql
    assert "export_path         TEXT NOT NULL" in sql
    assert "checksum_sha256     TEXT NOT NULL" in sql
    assert "size_bytes          BIGINT NOT NULL CHECK (size_bytes > 0)" in sql
    assert "'manifest_json','commerce_zip'" in sql


def test_collection_governance_state_machine() -> None:
    assert _TRANSITIONS["approve"] == ("approved", {"draft"})
    assert _TRANSITIONS["publish"] == ("published", {"approved"})
    assert _TRANSITIONS["reject"] == ("rejected", {"draft"})
    assert _TRANSITIONS["dispute"] == ("disputed", {"approved", "published"})
    assert _TRANSITIONS["retract"] == ("retracted", {"disputed"})


def test_collection_manifest_export_is_deterministic_and_asset_ordered() -> None:
    places = [{"place_id": _PLACE_ID, "name": {"en": "Great Barrier Reef"}, "role": "primary"}]

    first = build_collection_export_manifest(_collection(), _assets(), places)
    second = build_collection_export_manifest(_collection(), list(reversed(_assets())), places)

    assert first == second
    assert first["collection_id"] == str(_COLLECTION_ID)
    assert first["slug"] == "great-barrier-reef-flora"
    assert first["asset_count"] == 2
    assert [asset["asset_id"] for asset in first["assets"]] == [str(_ASSET_A), str(_ASSET_B)]
    assert first["assets"][0]["rights_status"] == "Public Domain"
    assert first["provenance"]["export_format"] == "collection_manifest_v1"
    assert len(first["checksum_sha256"]) == 64
