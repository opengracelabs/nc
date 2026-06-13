"""Real source connectors for NC-PLACES-2000 place ingestion."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from services.data.place_factory import (
    PLACE_CANDIDATES_DIR,
    PlaceFactoryCandidate,
    export_place_batch,
    normalize_place_candidate,
)

JsonFetcher = Callable[[str], Any]

UNESCO_WORLD_HERITAGE_URL = "https://whc.unesco.org/en/list/"
WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"

WORLD_HERITAGE_SPARQL = """
SELECT ?item ?itemLabel ?countryLabel ?lat ?lon WHERE {
  ?item wdt:P1435 wd:Q9259 .
  OPTIONAL { ?item wdt:P17 ?country . }
  OPTIONAL {
    ?item p:P625/psv:P625 ?coords .
    ?coords wikibase:geoLatitude ?lat ;
            wikibase:geoLongitude ?lon .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
""".strip()

BIOSPHERE_SPARQL = """
SELECT ?item ?itemLabel ?countryLabel ?lat ?lon WHERE {
  ?item wdt:P31/wdt:P279* wd:Q158454 .
  OPTIONAL { ?item wdt:P17 ?country . }
  OPTIONAL {
    ?item p:P625/psv:P625 ?coords .
    ?coords wikibase:geoLatitude ?lat ;
            wikibase:geoLongitude ?lon .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
""".strip()

GEOPARK_SPARQL = """
SELECT ?item ?itemLabel ?countryLabel ?lat ?lon WHERE {
  ?item wdt:P31/wdt:P279* wd:Q53444003 .
  OPTIONAL { ?item wdt:P17 ?country . }
  OPTIONAL {
    ?item p:P625/psv:P625 ?coords .
    ?coords wikibase:geoLatitude ?lat ;
            wikibase:geoLongitude ?lon .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
""".strip()

RAMSAR_SPARQL = """
SELECT ?item ?itemLabel ?countryLabel ?lat ?lon WHERE {
  ?item wdt:P31/wdt:P279* wd:Q19683138 .
  OPTIONAL { ?item wdt:P17 ?country . }
  OPTIONAL {
    ?item p:P625/psv:P625 ?coords .
    ?coords wikibase:geoLatitude ?lat ;
            wikibase:geoLongitude ?lon .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
""".strip()

UNESCO_ICH_SPARQL = """
SELECT ?item ?itemLabel ?countryLabel ?lat ?lon WHERE {
  ?item wdt:P31/wdt:P279* wd:Q59544 .
  OPTIONAL { ?item wdt:P17 ?country . }
  OPTIONAL {
    ?item p:P625/psv:P625 ?coords .
    ?coords wikibase:geoLatitude ?lat ;
            wikibase:geoLongitude ?lon .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}
""".strip()


@dataclass(frozen=True)
class PlaceSourceConnector:
    source_list: str
    designation_type: str
    endpoint: str
    source_url: str
    public_domain_source_hints: tuple[str, ...]
    ich_from_name: bool = False
    sparql: str | None = None

    def fetch(self, fetcher: JsonFetcher | None = None) -> Any:
        client = fetcher or fetch_json
        url = self.endpoint
        if self.sparql:
            query = urllib.parse.urlencode({"query": self.sparql, "format": "json"})
            url = f"{self.endpoint}?{query}"
        return client(url)

    def normalize(self, payload: Any, limit: int | None = None) -> list[PlaceFactoryCandidate]:
        rows = list(self.iter_records(payload))
        if limit is not None:
            rows = rows[:limit]
        return [normalize_place_candidate(row, self.source_list) for row in rows]

    def iter_records(self, payload: Any) -> Iterable[dict[str, Any]]:
        if _is_sparql_payload(payload):
            yield from _iter_wikidata_sparql(payload, self)
        elif self.source_list == "unesco_world_heritage":
            yield from _iter_unesco_world_heritage(payload, self)
        elif self.source_list == "ramsar":
            yield from _iter_ramsar(payload, self)
        else:
            yield from _iter_wikidata_sparql(payload, self)




def _is_sparql_payload(payload: Any) -> bool:
    return isinstance(payload, dict) and isinstance(payload.get("results"), dict)


def fetch_json(url: str) -> Any:
    safe_url = _validate_http_url(url)
    request = urllib.request.Request(  # noqa: S310
        safe_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "NatureCulturePlaceFactory/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _validate_http_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"unsupported source URL scheme: {parsed.scheme}")
    return url


def priority_place_source_connectors() -> list[PlaceSourceConnector]:
    return [
        PlaceSourceConnector(
            source_list="unesco_world_heritage",
            designation_type="UNESCO",
            endpoint=WIKIDATA_SPARQL_URL,
            source_url=UNESCO_WORLD_HERITAGE_URL,
            public_domain_source_hints=("unesco", "wikimedia", "europeana"),
            sparql=WORLD_HERITAGE_SPARQL,
        ),
        PlaceSourceConnector(
            source_list="biosphere_reserves",
            designation_type="Biosphere",
            endpoint=WIKIDATA_SPARQL_URL,
            source_url="https://www.unesco.org/en/mab",
            public_domain_source_hints=("nasa", "gbif", "wikimedia"),
            sparql=BIOSPHERE_SPARQL,
        ),
        PlaceSourceConnector(
            source_list="global_geoparks",
            designation_type="Geopark",
            endpoint=WIKIDATA_SPARQL_URL,
            source_url="https://www.unesco.org/en/iggp/geoparks",
            public_domain_source_hints=("europeana", "wikimedia", "usgs"),
            sparql=GEOPARK_SPARQL,
        ),
        PlaceSourceConnector(
            source_list="ramsar",
            designation_type="Ramsar",
            endpoint=WIKIDATA_SPARQL_URL,
            source_url="https://rsis.ramsar.org/",
            public_domain_source_hints=("gbif", "bhl", "wikimedia"),
            sparql=RAMSAR_SPARQL,
        ),
        PlaceSourceConnector(
            source_list="unesco_ich",
            designation_type="ICH",
            endpoint=WIKIDATA_SPARQL_URL,
            source_url="https://ich.unesco.org/",
            public_domain_source_hints=("unesco", "bhl", "wikimedia"),
            ich_from_name=True,
            sparql=UNESCO_ICH_SPARQL,
        ),
    ]


def ingest_priority_place_sources(
    fetcher: JsonFetcher | None = None,
    limit_per_source: int | None = None,
) -> list[PlaceFactoryCandidate]:
    candidates: list[PlaceFactoryCandidate] = []
    seen: set[tuple[str, str]] = set()
    for connector in priority_place_source_connectors():
        payload = connector.fetch(fetcher)
        for candidate in connector.normalize(payload, limit_per_source):
            key = (candidate["source_list"], candidate["place_slug"])
            if key in seen:
                continue
            candidates.append(candidate)
            seen.add(key)
    return candidates


def export_priority_place_candidates(
    fetcher: JsonFetcher | None = None,
    limit_per_source: int | None = None,
    output_dir: Path | str = PLACE_CANDIDATES_DIR,
    batch_name: str = "nc-places-2000-priority-sources",
) -> Path:
    candidates = ingest_priority_place_sources(fetcher, limit_per_source)
    return export_place_batch(candidates, batch_name, output_dir)


def _iter_unesco_world_heritage(
    payload: Any,
    connector: PlaceSourceConnector,
) -> Iterable[dict[str, Any]]:
    records = payload.get("features") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        return
    for item in records:
        props = item.get("properties", item) if isinstance(item, dict) else {}
        if not isinstance(props, dict):
            continue
        geometry = item.get("geometry", {}) if isinstance(item, dict) else {}
        coords = geometry.get("coordinates") if isinstance(geometry, dict) else None
        longitude = props.get("longitude") or (
            coords[0] if isinstance(coords, list) and coords else None
        )
        latitude = props.get("latitude") or (
            coords[1] if isinstance(coords, list) and len(coords) > 1 else None
        )
        name = props.get("site") or props.get("name_en") or props.get("name")
        if not name:
            continue
        category = str(props.get("category") or "")
        designation_type = (
            "UNESCO_WH_Mixed"
            if category.lower() == "mixed"
            else connector.designation_type
        )
        yield _source_record(
            connector,
            display_name=str(name),
            country=_join_country(props.get("states_parties") or props.get("country")),
            region=str(props.get("region") or "Global"),
            latitude=latitude,
            longitude=longitude,
            designation_type=designation_type,
        )


def _iter_ramsar(payload: Any, connector: PlaceSourceConnector) -> Iterable[dict[str, Any]]:
    records = payload.get("data") or payload.get("sites") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        return
    for item in records:
        if not isinstance(item, dict):
            continue
        name = item.get("Official_name") or item.get("official_name") or item.get("name")
        if not name:
            continue
        yield _source_record(
            connector,
            display_name=str(name),
            country=_join_country(item.get("country") or item.get("ISO3") or item.get("iso3")),
            region=str(item.get("region") or "Global"),
            latitude=item.get("Latitude") or item.get("latitude") or item.get("lat"),
            longitude=item.get("Longitude") or item.get("longitude") or item.get("lon"),
        )


def _iter_wikidata_sparql(
    payload: Any,
    connector: PlaceSourceConnector,
) -> Iterable[dict[str, Any]]:
    bindings = payload.get("results", {}).get("bindings", {}) if isinstance(payload, dict) else []
    if not isinstance(bindings, list):
        return
    for item in bindings:
        if not isinstance(item, dict):
            continue
        name = _binding_value(item, "name") or _binding_value(item, "itemLabel")
        if not name:
            continue
        country = (
            _binding_value(item, "countryLabel")
            or _binding_value(item, "country")
            or "Multiple"
        )
        ich_connections = [str(name)] if connector.ich_from_name else []
        yield _source_record(
            connector,
            display_name=str(name),
            country=str(country),
            region="Global",
            latitude=_binding_value(item, "lat"),
            longitude=_binding_value(item, "lon"),
            ich_connections=ich_connections,
        )


def _source_record(
    connector: PlaceSourceConnector,
    *,
    display_name: str,
    country: str,
    region: str,
    latitude: Any,
    longitude: Any,
    designation_type: str | None = None,
    ich_connections: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "source_list": connector.source_list,
        "designation_type": designation_type or connector.designation_type,
        "display_name": display_name,
        "country": country,
        "region": region,
        "latitude": latitude,
        "longitude": longitude,
        "source_url": connector.source_url,
        "authority_status": "source_observed",
        "ich_connections": ich_connections or [],
        "public_domain_source_hints": list(connector.public_domain_source_hints),
    }


def _binding_value(binding: dict[str, Any], key: str) -> str | None:
    value = binding.get(key)
    if isinstance(value, dict):
        raw = value.get("value")
        return str(raw) if raw not in (None, "") else None
    if value not in (None, ""):
        return str(value)
    return None


def _join_country(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip()) or "Multiple"
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "Multiple"
