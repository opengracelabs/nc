from asyncpg import PostgresError
from fastapi import APIRouter

from ..database import acquire

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    try:
        async with acquire() as conn:
            await conn.fetchval("SELECT 1")
        db_ok = True
    except PostgresError:
        db_ok = False

    return {
        "status": "ok" if db_ok else "degraded",
        "database": "ok" if db_ok else "error",
    }
