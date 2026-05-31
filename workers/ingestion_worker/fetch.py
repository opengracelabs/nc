"""
Fetch raw evidence for an approved candidate.
Returns bytes and the final URL (after redirects).
"""
import asyncio
import logging
from pathlib import Path
from typing import Any

import httpx

from .config import settings

log = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": settings.wikimedia_user_agent,
    "Accept": "application/json",
}


def _source_url(source: str, source_id: str, config: dict[str, Any]) -> str:
    if source == "unesco_whc":
        base = config.get("api_base", "https://whc.unesco.org/api/v2")
        return f"{base}/sites/{source_id}/?format=json"
    if source == "wikidata":
        if not source_id.startswith("Q"):
            raise ValueError(f"Wikidata source_id must be a QID, got {source_id!r}")
        return f"https://www.wikidata.org/wiki/Special:EntityData/{source_id}.json"
    raise ValueError(f"No URL builder for source: {source}")


async def fetch_raw(
    source: str,
    source_id: str,
    config: dict[str, Any],
) -> tuple[bytes, str]:
    """
    Fetch the canonical source record for a candidate.
    Returns (raw_bytes, url).
    Raises httpx.HTTPError on unrecoverable failure.
    """
    if source == "unesco_whc" and settings.unesco_replay_fixture:
        raw_bytes = await asyncio.to_thread(Path(settings.unesco_replay_fixture).read_bytes)
        return raw_bytes, settings.unesco_replay_fixture

    url = _source_url(source, source_id, config)
    headers = dict(_HEADERS)
    if source == "unesco_whc" and settings.unesco_api_key:
        headers["Authorization"] = f"Token {settings.unesco_api_key}"

    last_exc: Exception | None = None
    for attempt in range(1, settings.fetch_retry_max + 1):
        try:
            async with httpx.AsyncClient(
                timeout=settings.fetch_timeout_seconds,
                follow_redirects=True,
                headers=headers,
            ) as client:
                resp = await client.get(url)
                resp.raise_for_status()

                if len(resp.content) > settings.fetch_max_bytes:
                    raise ValueError(
                        f"Response size {len(resp.content)} exceeds limit "
                        f"{settings.fetch_max_bytes}"
                    )

                log.info(
                    "Fetched source=%s source_id=%s bytes=%d",
                    source,
                    source_id,
                    len(resp.content),
                )
                return resp.content, str(resp.url)

        except (httpx.HTTPStatusError, httpx.HTTPError, ValueError) as exc:
            last_exc = exc
            if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 404:
                raise   # 404 is not retryable
            wait = 2 ** attempt
            log.warning("Fetch attempt %d/%d failed source=%s: %s (retry in %ds)",
                        attempt, settings.fetch_retry_max, source, exc, wait)
            if attempt < settings.fetch_retry_max:
                await asyncio.sleep(wait)

    raise last_exc  # type: ignore[misc]
