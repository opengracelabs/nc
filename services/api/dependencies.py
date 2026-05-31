from typing import Annotated

import asyncpg
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings
from .database import get_pool

_bearer = HTTPBearer(auto_error=False)


async def db() -> asyncpg.Connection:
    async with get_pool().acquire() as conn:
        yield conn


async def require_auth(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Security(_bearer)],
) -> str:
    if credentials is None or credentials.credentials != settings.nc_secret_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return credentials.credentials


DB = Annotated[asyncpg.Connection, Depends(db)]
Auth = Annotated[str, Depends(require_auth)]
