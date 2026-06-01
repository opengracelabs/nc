"""Fact and relationship extraction from place records.

All functions are pure (no I/O). The store module handles DB writes.
Every fact carries a PROV-O provenance object recording worker version,
source authority, extraction method, and the specific place field used.
"""
import json
from datetime import UTC, datetime
from typing import Any

from .config import settings
from .score import score_fact

_WORKER_ID = "knowledge_worker:v0.2.0"


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _prov(source: str, source_field: str) -> dict:
    return {
        "prov:wasGeneratedBy": _WORKER_ID,
        "prov:wasAttributedTo": f"source:{source}",
        "prov:used": f"field:{source_field}",
        "prov:generatedAtTime": _now_iso(),
        "extraction_method": "field_mapping",
        "extraction_version": settings.extraction_version,
        "source_field": source_field,
    }


def _coerce_dict(val: Any) -> dict:
    if isinstance(val, str):
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return {}
    return val or {}


def extract_facts(place: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract atomic facts from a place record.

    Returns FactDraft dicts ready for store.upsert_facts().
    asset_id is always None: field-mapping extraction traces to the place
    row (itself the product of the upstream ingestion + preservation workers).
    provenance.source_field records the exact column so any fact is replayable.
    """
    place_id = place["id"]
    source = place.get("source") or "unknown"
    confidence = score_fact(source)

    def fact(predicate, value, value_type, *, language=None, concept_uri=None, sf=None):
        return {
            "place_id": place_id,
            "predicate": predicate,
            "value": value,
            "value_type": value_type,
            "language": language,
            "concept_uri": concept_uri,
            "asset_id": None,
            "source": source,
            "confidence_score": confidence,
            "provenance": _prov(source, sf or f"places.{predicate}"),
        }

    facts: list[dict] = []

    if (yr := place.get("inscription_year")) is not None:
        facts.append(fact("inscription_year", {"number": yr}, "number"))

    if (ca := place.get("core_area_ha")) is not None:
        facts.append(fact("core_area_ha", {"number": ca}, "number"))

    if (ba := place.get("buffer_area_ha")) is not None:
        facts.append(fact("buffer_area_ha", {"number": ba}, "number"))

    if (tb := place.get("transboundary")) is not None:
        facts.append(fact("transboundary", {"boolean": bool(tb)}, "boolean"))

    if sp := place.get("spatial_precision"):
        facts.append(fact("spatial_precision", {"text": sp}, "text"))

    if ht := place.get("heritage_type"):
        facts.append(fact("heritage_type", {"text": ht}, "text",
                          concept_uri=f"whc:type/{ht}"))

    for crit in place.get("ouv_criteria") or []:
        facts.append(fact("ouv_criterion", {"text": crit}, "text",
                          concept_uri=f"whc:criterion/{crit}",
                          sf="places.ouv_criteria"))

    for code in place.get("country_codes") or []:
        facts.append(fact("country_code", {"text": code}, "text",
                          sf="places.country_codes"))

    name = _coerce_dict(place.get("name"))
    for lang, val in name.items():
        if val:
            facts.append(fact("name", {"text": val}, "text",
                              language=lang, sf="places.name"))

    desc = _coerce_dict(place.get("description"))
    for lang, val in desc.items():
        if val:
            facts.append(fact("description", {"text": val}, "text",
                              language=lang, sf="places.description"))

    ouv = _coerce_dict(place.get("statement_of_ouv"))
    for lang, val in ouv.items():
        if val:
            facts.append(fact("statement_of_ouv", {"text": val}, "text",
                              language=lang, sf="places.statement_of_ouv"))

    return facts


def build_place_concept_relationships(
    place_id: Any,
    facts: list[dict],
    source: str,
) -> list[dict]:
    """Derive place→concept relationships from concept-linked facts.

    heritage_type facts → classified_as whc:type/{value}
    ouv_criterion facts → exemplifies whc:criterion/{value}
    """
    seen: set[str] = set()
    rels: list[dict] = []

    for f in facts:
        uri = f.get("concept_uri")
        if not uri:
            continue
        key = f"{place_id}:{f['predicate']}:{uri}"
        if key in seen:
            continue
        seen.add(key)

        predicate = "classified_as" if f["predicate"] == "heritage_type" else "exemplifies"

        rels.append({
            "subject_id": place_id,
            "subject_type": "place",
            "predicate": predicate,
            "object_type": "concept",
            "concept_uri": uri,
            "object_id": None,   # resolved in store.upsert_relationships
            "asset_id": None,
            "confidence_score": score_fact(source),
            "status": "active",
            "provenance": {
                "prov:wasGeneratedBy": _WORKER_ID,
                "prov:wasAttributedTo": f"source:{source}",
                "prov:generatedAtTime": _now_iso(),
                "extraction_method": "field_mapping",
                "extraction_version": settings.extraction_version,
                "derived_from_predicate": f["predicate"],
            },
        })

    return rels
