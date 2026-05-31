import json
import logging
from typing import Any

import httpx

from ..config import settings
from .base import BaseSource, FetchResult, RawRecord

log = logging.getLogger(__name__)

# World Heritage Sites (Q9259) with labels, country, coordinates, and WHC ID
_SPARQL = """
SELECT ?site ?siteLabel ?whc_id ?countryCode ?lat ?lon ?inscriptionYear WHERE {
  ?site wdt:P31 wd:Q9259 .
  OPTIONAL { ?site wdt:P757  ?whc_id }
  OPTIONAL { ?site wdt:P17   ?country .
             ?country wdt:P297 ?countryCode }
  OPTIONAL { ?site wdt:P625  ?coord .
             BIND(geof:latitude(?coord)  AS ?lat)
             BIND(geof:longitude(?coord) AS ?lon) }
  OPTIONAL { ?site wdt:P571  ?inception .
             BIND(YEAR(?inception) AS ?inscriptionYear) }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,fr,es,ar,zh,ru" }
}
ORDER BY ?site
"""

_CHUNK = 500


class WikidataSource(BaseSource):
    source_id = "wikidata"

    async def fetch(self, config: dict[str, Any], run_id: str) -> FetchResult:
        endpoint = config.get("sparql_endpoint", settings.wikidata_sparql_endpoint)
        headers = {
            "Accept": "application/sparql-results+json",
            "User-Agent": settings.wikimedia_user_agent,
        }

        all_bindings: list[dict] = []
        errors: list[str] = []
        offset = 0

        async with httpx.AsyncClient(
            timeout=settings.fetch_timeout_seconds,
            headers=headers,
        ) as client:
            while True:
                paginated = _SPARQL.strip() + f"\nLIMIT {_CHUNK} OFFSET {offset}"
                try:
                    resp = await client.get(
                        endpoint,
                        params={"query": paginated, "format": "json"},
                    )
                    resp.raise_for_status()
                except httpx.HTTPError as exc:
                    errors.append(f"offset {offset}: {exc}")
                    log.error("Wikidata SPARQL error offset=%d: %s", offset, exc)
                    break

                bindings = resp.json().get("results", {}).get("bindings", [])
                if not bindings:
                    break
                all_bindings.extend(bindings)
                log.info("Wikidata fetched offset=%d records=%d", offset, len(bindings))

                if len(bindings) < _CHUNK:
                    break
                offset += _CHUNK

        raw_bytes = json.dumps(all_bindings, ensure_ascii=False).encode()
        records = [
            RawRecord(
                source_id=b["site"]["value"].split("/")[-1],  # QID
                payload=b,
            )
            for b in all_bindings
        ]

        return FetchResult(
            source=self.source_id,
            run_id=run_id,
            records=records,
            raw_bytes=raw_bytes,
            total=len(all_bindings),
            errors=errors,
        )
