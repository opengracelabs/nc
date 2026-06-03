"""MILESTONE-003 BHL illustration focus tests."""
from pathlib import Path

from schemas.core.asset import AssetType

MODEL_DOC = Path("docs/architecture/bhl_illustration_asset_model.md")
SOURCE_SEED = Path("infrastructure/postgres/init/03_seed.sql")
README = Path("README.md")
RELEASE = Path("docs/releases/v0.3.0.md")


def test_bhl_illustration_model_is_asset_first() -> None:
    text = MODEL_DOC.read_text()
    assert "Illustration Asset" in text
    assert "Species" in text
    assert "Place" in text
    assert "not a book ingestion program" in text
    assert "not a full literature graph" in text


def test_bhl_commercial_product_surfaces_are_declared() -> None:
    text = MODEL_DOC.read_text()
    for product in ("Collections", "Wall Art", "Calendars", "Cards", "Puzzles", "Books"):
        assert product in text
    assert "commercial reuse" in text
    assert "public-domain" in text


def test_bhl_source_registry_is_narrowly_scoped() -> None:
    sql = SOURCE_SEED.read_text()
    assert "'bhl'" in sql
    assert "Biodiversity Heritage Library" in sql
    assert "public_domain_illustrations" in sql


def test_bhl_illustration_asset_type_exists() -> None:
    assert AssetType.BHL_ILLUSTRATION == "bhl_illustration"


def test_milestone_direction_mentions_bhl_asset_reuse() -> None:
    readme = README.read_text()
    assert "public-domain illustration opportunity discovery" in readme
    assert "Taxa from GBIF and Wikidata are search handles" in readme
    release = RELEASE.read_text()
    assert "Optimize for commercial public-domain asset reuse" in release
    assert "Not a full literature graph" in release
