"""v0.3.2 BHL asset ingestion replay tests."""
from pathlib import Path
from uuid import uuid4

import httpx
import pytest

from workers.bhl_asset_ingestion_worker.main import fetch_bhl_asset
from workers.bhl_asset_ingestion_worker.store import (
    bhl_asset_raw_path,
    bhl_image_url,
    checksum_sha256,
    create_bhl_asset,
    store_raw_asset,
    verify_opportunity_rights,
)

_OPPORTUNITY_ID = uuid4()
_CONCEPT_ID = uuid4()
_ASSET_ID = uuid4()


def _approved_opportunity() -> dict:
    return {
        "id": _OPPORTUNITY_ID,
        "concept_id": _CONCEPT_ID,
        "source": "bhl",
        "source_record_id": "item:12345:page:67890",
        "source_url": "https://www.biodiversitylibrary.org/page/67890",
        "bhl_item_id": "12345",
        "bhl_page_id": "67890",
        "taxon_name": "Acanthaster planci",
        "title": "Acanthaster planci plate",
        "publication_title": "Naturalist's Miscellany",
        "illustrator": "Nodder",
        "publication_year": 1789,
        "rights_status": "Public Domain",
        "rights_source_url": None,
        "rights_verified_by": "bhl_metadata",
        "rights_verified_at": "2026-06-03T00:00:00Z",
        "provenance": {},
        "score_components": {},
    }


def test_bhl_asset_ingestion_accepts_only_verified_public_domain_or_cc0() -> None:
    opportunity = _approved_opportunity()
    assert verify_opportunity_rights(opportunity) is True

    opportunity["rights_status"] = "No known copyright restrictions"
    assert verify_opportunity_rights(opportunity) is False

    opportunity = _approved_opportunity()
    opportunity["rights_verified_by"] = None
    assert verify_opportunity_rights(opportunity) is False


def test_bhl_asset_ingestion_allows_null_rights_source_url() -> None:
    opportunity = _approved_opportunity()
    opportunity["rights_source_url"] = None

    assert verify_opportunity_rights(opportunity) is True


async def test_bhl_asset_fetch_rejects_text_html_response() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            headers={"content-type": "text/html; charset=utf-8"},
            content=b"<html>not an image</html>",
            request=request,
        )
    )
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError, match="not an image: text/html"):
            await fetch_bhl_asset(client, "https://www.biodiversitylibrary.org/pageimage/1")


async def test_bhl_asset_fetch_rejects_non_image_content() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            headers={"content-type": "application/json"},
            content=b"{}",
            request=request,
        )
    )
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError, match="not an image: application/json"):
            await fetch_bhl_asset(client, "https://www.biodiversitylibrary.org/pageimage/1")


def test_bhl_asset_ingestion_builds_deterministic_image_url_and_raw_path() -> None:
    opportunity = _approved_opportunity()

    assert bhl_image_url(opportunity).endswith("/pageimage/67890")
    assert bhl_asset_raw_path(opportunity, "image/jpeg") == (
        f"bhl/illustrations/{_CONCEPT_ID}/{_OPPORTUNITY_ID}/67890.jpg"
    )


def test_bhl_asset_ingestion_preserves_webp_suffix() -> None:
    opportunity = _approved_opportunity()

    assert bhl_asset_raw_path(opportunity, "image/webp") == (
        f"bhl/illustrations/{_CONCEPT_ID}/{_OPPORTUNITY_ID}/67890.webp"
    )


class FakeMinio:
    def __init__(self) -> None:
        self.calls = []

    async def put_object(self, **kwargs):
        self.calls.append(kwargs)


async def test_bhl_asset_ingestion_stores_raw_evidence_in_minio() -> None:
    minio = FakeMinio()
    raw = b"image-bytes"
    path, checksum = await store_raw_asset(
        minio, _approved_opportunity(), raw, "image/jpeg"
    )

    assert path.endswith("/67890.jpg")
    assert checksum == checksum_sha256(raw)
    assert minio.calls[0]["object_name"] == path
    assert minio.calls[0]["content_type"] == "image/jpeg"


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeConn:
    def __init__(self) -> None:
        self.fetchrow_queries = []
        self.execute_queries = []

    def transaction(self):
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append((query, args))
        return {"id": _ASSET_ID}

    async def execute(self, query: str, *args):
        self.execute_queries.append((query, args))
        return "OK"


async def test_bhl_asset_ingestion_creates_concept_asset_rights_and_opportunity_link() -> None:
    conn = FakeConn()
    raw = b"image-bytes"
    opportunity = _approved_opportunity()

    asset_id = await create_bhl_asset(
        conn,
        opportunity,
        "bhl/illustrations/path/67890.jpg",
        raw,
        checksum_sha256(raw),
        "image/jpeg",
        "https://www.biodiversitylibrary.org/pageimage/67890",
    )

    assert asset_id == _ASSET_ID
    insert_query, insert_args = conn.fetchrow_queries[0]
    assert "INSERT INTO assets" in insert_query
    assert "concept_id" in insert_query
    assert "place_id" not in insert_query
    assert "'bhl_illustration'" in insert_query
    assert "'fetched'" in insert_query
    assert "premis_object_id" in insert_query
    assert _CONCEPT_ID in insert_args

    rights_query, rights_args = next(
        (q, args) for q, args in conn.execute_queries if "INSERT INTO asset_rights" in q
    )
    assert "INSERT INTO asset_rights" in rights_query
    assert None in rights_args
    assert any(
        "INSERT INTO illustration_opportunity_assets" in q
        for q, _ in conn.execute_queries
    )


def test_migration_links_bhl_assets_to_opportunities() -> None:
    sql = Path("infrastructure/postgres/init/16_taxon_discovery.sql").read_text()
    assert "CREATE TABLE illustration_opportunity_assets" in sql
    assert "asset_id            UUID NOT NULL REFERENCES assets(id)" in sql
    assert "UNIQUE (opportunity_id, link_type)" in sql
