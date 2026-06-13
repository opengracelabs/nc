"""Asset Factory Runtime APIs for NC-ASSETS-1000000."""

from fastapi import APIRouter

from services.data.asset_factory import (
    ASSET_SOURCES_DIR,
    asset_ingestion_pipeline,
    ingest_asset_source,
    summarize_asset_factory,
)
from services.data.bhl_connector import build_bhl_runtime
from services.data.institution_factory import build_institution_factory_runtime

from ..dependencies import Auth

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/factory")
async def get_asset_factory_runtime(auth: Auth) -> dict:
    source_path = ASSET_SOURCES_DIR / "factory_smoke_assets.json"
    return asset_ingestion_pipeline([source_path])


@router.get("/factory/candidates")
async def list_asset_factory_candidates(auth: Auth) -> list[dict]:
    source_path = ASSET_SOURCES_DIR / "factory_smoke_assets.json"
    return ingest_asset_source(source_path)


@router.get("/factory/summary")
async def get_asset_factory_summary(auth: Auth) -> dict:
    source_path = ASSET_SOURCES_DIR / "factory_smoke_assets.json"
    return summarize_asset_factory(ingest_asset_source(source_path))


@router.get("/institutions/factory")
async def get_institution_factory_runtime(auth: Auth) -> dict:
    return build_institution_factory_runtime()


@router.get("/institutions/factory/summary")
async def get_institution_factory_summary(auth: Auth) -> dict:
    return build_institution_factory_runtime()["summary"]


@router.get("/bhl/runtime")
async def get_bhl_runtime(auth: Auth) -> dict:
    return build_bhl_runtime()


@router.get("/bhl/candidates")
async def list_bhl_asset_candidates(auth: Auth) -> list[dict]:
    return build_bhl_runtime()["asset_factory_feed"]["asset_candidates"]


@router.get("/bhl/summary")
async def get_bhl_summary(auth: Auth) -> dict:
    return build_bhl_runtime()["summary"]
