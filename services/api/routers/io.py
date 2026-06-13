"""Illustration Opportunity Runtime APIs."""

from fastapi import APIRouter

from services.data.io_factory import build_io_factory_runtime

from ..dependencies import Auth

router = APIRouter(prefix="/io", tags=["io"])


@router.get("/factory")
async def get_io_factory_runtime(auth: Auth) -> dict:
    return build_io_factory_runtime()


@router.get("/candidates")
async def list_io_candidates(auth: Auth) -> list[dict]:
    return build_io_factory_runtime()["illustration_opportunities"]


@router.get("/summary")
async def get_io_summary(auth: Auth) -> dict:
    return build_io_factory_runtime()["summary"]
