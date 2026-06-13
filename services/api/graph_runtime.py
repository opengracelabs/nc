from __future__ import annotations

from contextlib import contextmanager
from typing import Any

from graph.seed import NODE_BY_ID, node_by_slug, recommendations_for, relationships_for, journey_for

from .config import settings

try:
    from neo4j import GraphDatabase
except ImportError:  # pragma: no cover - exercised only when optional driver is absent
    GraphDatabase = None  # type: ignore[assignment]

_RELATED_TYPES = {
    "RELATED_TO",
    "PART_OF",
    "LOCATED_IN",
    "DISCOVERED_BY",
    "EXPLORED_BY",
    "ILLUSTRATED_BY",
    "INSPIRED",
    "FEATURES",
}

# Labels whose status field is a commerce gate - must not be served from graph.
# Callers must recheck availability from PostgreSQL using the returned slug.
_COMMERCE_LABELS = {"Product"}


def _serialize_node(record: Any) -> dict:
    node = record if isinstance(record, dict) else dict(record)
    label = node.get("label") or next(iter(getattr(record, "labels", [])), None)
    result: dict = {
        "id": node.get("id"),
        "slug": node.get("slug"),
        "label": label,
        "name": node.get("name"),
        "summary": node.get("summary"),
    }
    if label not in _COMMERCE_LABELS:
        result["status"] = node.get("status")
    return result


def _static_place(slug: str) -> dict | None:
    node = node_by_slug(slug)
    if not node or node["label"] != "Place":
        return None
    rels = relationships_for(node["id"])
    connected_ids = {
        rel["target"] if rel["source"] == node["id"] else rel["source"] for rel in rels
    }
    return {
        "place": node,
        "relationships": rels,
        "connected": [NODE_BY_ID[node_id] for node_id in connected_ids],
        "source": "seed",
    }


def _static_recommendations(slug: str) -> dict | None:
    node = node_by_slug(slug)
    if not node:
        return None
    recs = [
        item for item in recommendations_for(slug)
        if item["node"]["label"] not in _COMMERCE_LABELS
    ]
    return {
        "subject": node,
        "recommendations": recs,
        "source": "seed",
    }


def _static_journey(slug: str) -> dict | None:
    node = node_by_slug(slug)
    if not node:
        return None
    journey = journey_for(slug)
    return {"subject": node, **journey, "source": "seed"}


def _static_related(slug: str) -> dict | None:
    node = node_by_slug(slug)
    if not node:
        return None
    related = []
    for rel in relationships_for(node["id"]):
        if rel["type"] not in _RELATED_TYPES:
            continue
        related_id = rel["target"] if rel["source"] == node["id"] else rel["source"]
        related.append({"node": NODE_BY_ID[related_id], "relationship": rel})
    return {"subject": node, "related": related, "source": "seed"}


@contextmanager
def _driver():
    if GraphDatabase is None or not settings.neo4j_uri:
        yield None
        return
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    try:
        driver.verify_connectivity()
        yield driver
    except Exception:
        yield None
    finally:
        driver.close()


def get_graph_place(slug: str) -> dict | None:
    with _driver() as driver:
        if driver is None:
            return _static_place(slug)
        with driver.session(database=settings.neo4j_database) as session:
            result = session.run(
                """
                MATCH (p:Place {slug: $slug})
                OPTIONAL MATCH (p)-[r]-(connected)
                RETURN p, collect({
                  source: startNode(r).id,
                  target: endNode(r).id,
                  type: type(r),
                  reason: r.reason,
                  weight: r.weight
                }) AS relationships,
                collect(DISTINCT connected) AS connected
                """,
                slug=slug,
            ).single()
            if not result or result["p"] is None:
                return None
            return {
                "place": _serialize_node(result["p"]),
                "relationships": [rel for rel in result["relationships"] if rel["type"]],
                "connected": [_serialize_node(node) for node in result["connected"]],
                "source": "neo4j",
            }


def get_graph_recommendations(slug: str) -> dict | None:
    with _driver() as driver:
        if driver is None:
            return _static_recommendations(slug)
        with driver.session(database=settings.neo4j_database) as session:
            result = session.run(
                """
                MATCH (subject {slug: $slug})
                OPTIONAL MATCH (subject)-[r:RECOMMENDS]->(target)
                WHERE NOT 'Product' IN labels(target)
                RETURN subject, collect({
                  node: target,
                  relationship: {
                    source: subject.id,
                    target: target.id,
                    type: type(r),
                    reason: r.reason,
                    weight: r.weight
                  }
                }) AS recommendations
                """,
                slug=slug,
            ).single()
            if not result or result["subject"] is None:
                return None
            recommendations = []
            for item in result["recommendations"]:
                if item["node"] is None:
                    continue
                recommendations.append(
                    {"node": _serialize_node(item["node"]), "relationship": item["relationship"]}
                )
            recommendations.sort(
                key=lambda item: item["relationship"].get("weight") or 0,
                reverse=True,
            )
            return {
                "subject": _serialize_node(result["subject"]),
                "recommendations": recommendations,
                "source": "neo4j",
            }


def get_graph_journey(slug: str) -> dict | None:
    with _driver() as driver:
        if driver is None:
            return _static_journey(slug)
        with driver.session(database=settings.neo4j_database) as session:
            result = session.run(
                """
                MATCH (subject {slug: $slug})
                OPTIONAL MATCH path = (subject)-[*1..2]-(node)
                WITH subject, collect(path) AS paths
                UNWIND paths AS path
                UNWIND nodes(path) AS n
                UNWIND relationships(path) AS r
                RETURN subject,
                       collect(DISTINCT n) AS nodes,
                       collect(DISTINCT {
                         source: startNode(r).id,
                         target: endNode(r).id,
                         type: type(r),
                         reason: r.reason,
                         weight: r.weight
                       }) AS relationships
                """,
                slug=slug,
            ).single()
            if not result or result["subject"] is None:
                return None
            return {
                "subject": _serialize_node(result["subject"]),
                "nodes": [_serialize_node(node) for node in result["nodes"]],
                "relationships": [rel for rel in result["relationships"] if rel["type"]],
                "source": "neo4j",
            }


def get_graph_related(slug: str) -> dict | None:
    with _driver() as driver:
        if driver is None:
            return _static_related(slug)
        with driver.session(database=settings.neo4j_database) as session:
            result = session.run(
                """
                MATCH (subject {slug: $slug})
                OPTIONAL MATCH (subject)-[r]-(related)
                WHERE type(r) IN $related_types
                RETURN subject, collect({
                  node: related,
                  relationship: {
                    source: startNode(r).id,
                    target: endNode(r).id,
                    type: type(r),
                    reason: r.reason,
                    weight: r.weight
                  }
                }) AS related
                """,
                slug=slug,
                related_types=sorted(_RELATED_TYPES),
            ).single()
            if not result or result["subject"] is None:
                return None
            related = []
            for item in result["related"]:
                if item["node"] is None:
                    continue
                related.append({"node": _serialize_node(item["node"]), "relationship": item["relationship"]})
            return {
                "subject": _serialize_node(result["subject"]),
                "related": related,
                "source": "neo4j",
            }
