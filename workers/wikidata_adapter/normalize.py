"""Wikidata entity evidence normalization helpers."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import extract_entity, normalize_qid
from .config import SOURCE_ROLE, WIKIDATA_ENTITY_BASE_URL

EVIDENCE_FIELDS = (
    "wikidata_qid",
    "label",
    "description",
    "aliases",
    "instance_of",
    "country",
    "coordinates",
    "geonames_id",
    "osm_relation",
    "wikipedia_links",
    "commons_category",
    "source_url",
    "raw_payload_hash",
)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def canonical_json_hash(payload: Any) -> str:
    """Hash Wikidata payloads for replay-stable provenance."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _language_value(values: Any, language: str) -> str | None:
    if not isinstance(values, dict):
        return None
    preferred = values.get(language) or values.get("en")
    if isinstance(preferred, dict):
        return _string(preferred.get("value"))
    for item in values.values():
        if isinstance(item, dict):
            value = _string(item.get("value"))
            if value:
                return value
    return None


def _aliases(values: Any, language: str) -> list[str]:
    if not isinstance(values, dict):
        return []
    preferred = values.get(language) or values.get("en") or []
    if not isinstance(preferred, list):
        return []
    aliases: list[str] = []
    for item in preferred:
        if isinstance(item, dict):
            value = _string(item.get("value"))
            if value and value not in aliases:
                aliases.append(value)
    return aliases


def _claim_values(entity: dict[str, Any], property_id: str) -> list[Any]:
    claims = entity.get("claims")
    if not isinstance(claims, dict):
        return []
    statements = claims.get(property_id)
    if not isinstance(statements, list):
        return []
    values: list[Any] = []
    for statement in statements:
        if not isinstance(statement, dict):
            continue
        mainsnak = statement.get("mainsnak")
        if not isinstance(mainsnak, dict):
            continue
        datavalue = mainsnak.get("datavalue")
        if not isinstance(datavalue, dict):
            continue
        values.append(datavalue.get("value"))
    return values


def _entity_ids(entity: dict[str, Any], property_id: str) -> list[str]:
    ids: list[str] = []
    for value in _claim_values(entity, property_id):
        if isinstance(value, dict):
            numeric_id = value.get("numeric-id")
            qid = normalize_qid(f"Q{numeric_id}") if numeric_id is not None else None
            if qid and qid not in ids:
                ids.append(qid)
    return ids


def _string_claim(entity: dict[str, Any], property_id: str) -> str | None:
    for value in _claim_values(entity, property_id):
        text = _string(value)
        if text:
            return text
    return None


def _coordinates(entity: dict[str, Any]) -> dict[str, float] | None:
    for value in _claim_values(entity, "P625"):
        if not isinstance(value, dict):
            continue
        latitude = value.get("latitude")
        longitude = value.get("longitude")
        if latitude is None or longitude is None:
            continue
        try:
            return {"latitude": float(latitude), "longitude": float(longitude)}
        except (TypeError, ValueError):
            return None
    return None


def _wikipedia_links(entity: dict[str, Any]) -> dict[str, str]:
    sitelinks = entity.get("sitelinks")
    if not isinstance(sitelinks, dict):
        return {}
    links: dict[str, str] = {}
    for site, data in sorted(sitelinks.items()):
        if not site.endswith("wiki") or site == "commonswiki" or not isinstance(data, dict):
            continue
        title = _string(data.get("title"))
        url = _string(data.get("url"))
        if not title:
            continue
        language = site.removesuffix("wiki")
        links[language] = url or f"https://{language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
    return links


def build_source_url(qid: str | None) -> str | None:
    """Build a public Wikidata entity URL."""
    return f"{WIKIDATA_ENTITY_BASE_URL}/{qid}" if qid else None


def normalize_entity_payload(
    payload: dict[str, Any] | None,
    *,
    qid: str | int | None = None,
    language: str = "en",
) -> dict[str, Any]:
    """Normalize one Wikidata entity response as identity/context evidence."""
    entity = extract_entity(payload, qid)
    entity_qid = normalize_qid(entity.get("id") if entity else qid)
    evidence = {
        "wikidata_qid": entity_qid,
        "label": _language_value(entity.get("labels"), language),
        "description": _language_value(entity.get("descriptions"), language),
        "aliases": _aliases(entity.get("aliases"), language),
        "instance_of": _entity_ids(entity, "P31"),
        "country": _entity_ids(entity, "P17"),
        "coordinates": _coordinates(entity),
        "geonames_id": _string_claim(entity, "P1566"),
        "osm_relation": _string_claim(entity, "P402"),
        "wikipedia_links": _wikipedia_links(entity),
        "commons_category": _string_claim(entity, "P373"),
        "source_url": build_source_url(entity_qid),
        "raw_payload_hash": canonical_json_hash(entity),
    }
    return evidence


def build_identity_evidence(
    payload: dict[str, Any] | None,
    *,
    qid: str | int | None = None,
    language: str = "en",
) -> dict[str, Any]:
    """Build replay-stable Wikidata identity evidence."""
    return normalize_entity_payload(payload, qid=qid, language=language)


def summarize_context(evidence: dict[str, Any]) -> dict[str, Any]:
    """Build a small provenance summary for context-only use."""
    return {
        "source": "wikidata",
        "source_role": SOURCE_ROLE,
        "wikidata_qid": evidence.get("wikidata_qid"),
        "source_url": evidence.get("source_url"),
    }

