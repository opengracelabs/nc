"""Pure research composition from governed knowledge rows.

The worker is intentionally template-based: it only emits statements that can be
backed by one source asset, one fact, and one relationship.
"""
from __future__ import annotations

from typing import Any

_WORKER_ID = "research_worker:v0.3.0"


def _text(value: Any, language: str = "en") -> str | None:
    if isinstance(value, dict):
        selected = value.get(language) or value.get("en")
        if selected:
            return str(selected)
        for candidate in value.values():
            if candidate:
                return str(candidate)
        return None
    if value is None:
        return None
    return str(value)


def _fact_value(fact: dict[str, Any]) -> str:
    value = fact.get("value")
    if isinstance(value, dict):
        for key in ("text", "number", "date", "boolean", "uri"):
            if key in value:
                return str(value[key])
    return str(value)


def _relationship_fact_predicate(rel: dict[str, Any]) -> str | None:
    provenance = rel.get("provenance") or {}
    if not isinstance(provenance, dict):
        return None
    return provenance.get("derived_from_predicate") or provenance.get("source_field")


def _asset_id(fact: dict[str, Any], rel: dict[str, Any]) -> Any | None:
    return fact.get("asset_id") or rel.get("asset_id")


def _relationship_touches_place(rel: dict[str, Any], place_id: Any) -> bool:
    return (
        rel.get("subject_type") == "place" and rel.get("subject_id") == place_id
    ) or (
        rel.get("object_type") == "place" and rel.get("object_id") == place_id
    )


def _supporting_fact(rel: dict[str, Any], facts: list[dict[str, Any]]) -> dict[str, Any] | None:
    predicate = _relationship_fact_predicate(rel)
    if not predicate:
        return None
    for fact in facts:
        if fact.get("status") != "active":
            continue
        if fact.get("predicate") != predicate:
            continue
        if _asset_id(fact, rel):
            return fact
    return None


def _statement_body(
    place_name: str,
    place_id: Any,
    fact: dict[str, Any],
    rel: dict[str, Any],
) -> tuple[str, str] | None:
    value = _fact_value(fact)
    predicate = rel.get("predicate")
    if predicate == "classified_as":
        return "classification", f"{place_name} is classified as {value} heritage."
    if predicate == "exemplifies":
        return "criterion", f"{place_name} exemplifies UNESCO criterion {value}."
    if predicate == "co_inscribed_with":
        other_id = (
            rel.get("object_id")
            if rel.get("subject_id") == place_id
            else rel.get("subject_id")
        )
        return "co_inscription", f"{place_name} is co-inscribed with place {other_id} in {value}."
    return None


def build_research_output(
    place: dict[str, Any],
    facts: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    *,
    output_version: str = "1",
    output_type: str = "place_brief",
) -> dict[str, Any] | None:
    """Return a research output draft, or None when support is insufficient."""
    place_id = place["id"]
    place_name = _text(place.get("name")) or f"Place {place_id}"
    statements: list[dict[str, Any]] = []

    active_facts = [f for f in facts if f.get("status") == "active"]
    active_relationships = [
        r for r in relationships
        if r.get("status") == "active" and _relationship_touches_place(r, place_id)
    ]

    seen: set[tuple[str, str, str]] = set()
    for rel in sorted(
        active_relationships,
        key=lambda r: (r.get("predicate", ""), str(r.get("id"))),
    ):
        fact = _supporting_fact(rel, active_facts)
        if fact is None:
            continue
        asset_id = _asset_id(fact, rel)
        statement = _statement_body(place_name, place_id, fact, rel)
        if statement is None or asset_id is None:
            continue
        statement_type, body = statement
        key = (statement_type, body, str(rel["id"]))
        if key in seen:
            continue
        seen.add(key)
        confidence = min(float(fact["confidence_score"]), float(rel["confidence_score"]))
        statements.append({
            "sequence": len(statements) + 1,
            "statement_type": statement_type,
            "body": body,
            "status": "pending_review",
            "confidence_score": confidence,
            "provenance": {
                "prov:wasGeneratedBy": _WORKER_ID,
                "research_version": output_version,
                "composition_method": "template_from_active_fact_and_relationship",
            },
            "evidence": [{
                "asset_id": asset_id,
                "fact_id": fact["id"],
                "relationship_id": rel["id"],
                "evidence_role": "supporting",
                "provenance": {
                    "fact_predicate": fact["predicate"],
                    "relationship_predicate": rel["predicate"],
                },
            }],
        })

    if not statements:
        return None

    confidence = min(s["confidence_score"] for s in statements)
    return {
        "place_id": place_id,
        "output_type": output_type,
        "output_version": output_version,
        "title": place_name,
        "summary": f"Research brief for {place_name} with {len(statements)} supported statements.",
        "status": "pending_review",
        "confidence_score": confidence,
        "provenance": {
            "prov:wasGeneratedBy": _WORKER_ID,
            "research_version": output_version,
            "composition_method": "deterministic_templates",
        },
        "statements": statements,
    }
