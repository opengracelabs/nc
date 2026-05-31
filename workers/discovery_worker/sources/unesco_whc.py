import asyncio
import json
import logging
from pathlib import Path
from typing import Any

import httpx

from ..config import settings
from .base import BaseSource, FetchResult, RawRecord

log = logging.getLogger(__name__)

_API_BASE = "https://whc.unesco.org/api/v2"
_PAGE_SIZE = 100


class UnescoWHCSource(BaseSource):
    source_id = "unesco_whc"

    async def fetch(self, config: dict[str, Any], run_id: str) -> FetchResult:
        if settings.unesco_replay_fixture:
            raw_bytes = await asyncio.to_thread(Path(settings.unesco_replay_fixture).read_bytes)
            all_sites = json.loads(raw_bytes)
            records = [
                RawRecord(source_id=str(s.get("id_number", s.get("id", i))), payload=s)
                for i, s in enumerate(all_sites)
            ]
            return FetchResult(
                source=self.source_id,
                run_id=run_id,
                records=records,
                raw_bytes=raw_bytes,
                total=len(records),
                errors=[],
            )

        headers = {"Accept": "application/json"}
        if settings.unesco_api_key:
            headers["Authorization"] = f"Token {settings.unesco_api_key}"

        all_sites: list[dict] = []
        errors: list[str] = []
        page = 1

        async with httpx.AsyncClient(
            timeout=settings.fetch_timeout_seconds,
            headers=headers,
        ) as client:
            while True:
                try:
                    resp = await client.get(
                        f"{_API_BASE}/sites/",
                        params={"format": "json", "page": page, "page_size": _PAGE_SIZE},
                    )
                    resp.raise_for_status()
                except httpx.HTTPError as exc:
                    errors.append(f"page {page}: {exc}")
                    log.error("UNESCO WHC fetch error page=%d: %s", page, exc)
                    break

                data = resp.json()
                sites = data.get("sites", data if isinstance(data, list) else [])
                if not sites:
                    break
                all_sites.extend(sites)
                log.info("UNESCO WHC fetched page=%d records=%d", page, len(sites))

                if len(sites) < _PAGE_SIZE:
                    break
                page += 1

        raw_bytes = json.dumps(all_sites, ensure_ascii=False).encode()
        records = [
            RawRecord(source_id=str(s.get("id_number", s.get("id", i))), payload=s)
            for i, s in enumerate(all_sites)
        ]

        return FetchResult(
            source=self.source_id,
            run_id=run_id,
            records=records,
            raw_bytes=raw_bytes,
            total=len(all_sites),
            errors=errors,
        )
