from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import close_pool, init_pool
from .routers import (
    collections,
    discovery,
    health,
    knowledge,
    places,
    research,
    sources,
    taxa,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()


app = FastAPI(
    title="Nature & Culture API",
    description="Governance gateway for the Nature & Culture pipeline.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.nc_env != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.nc_env == "development" else [],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(health.router)
app.include_router(sources.router)
app.include_router(places.router)
app.include_router(knowledge.router)
app.include_router(research.router)
app.include_router(collections.router)
app.include_router(taxa.router)
app.include_router(discovery.router)
