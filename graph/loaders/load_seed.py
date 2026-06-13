from __future__ import annotations

import os
from pathlib import Path

try:
    from neo4j import GraphDatabase
except ImportError:  # pragma: no cover - only hit without optional loader dependency
    GraphDatabase = None

from graph.seed import NODES, RELATIONSHIPS

LABELS = {
    "Place",
    "Collection",
    "Product",
    "Asset",
    "Species",
    "Person",
    "Institution",
    "Theme",
    "Event",
    "Expedition",
}

REL_TYPES = {
    "RELATED_TO",
    "PART_OF",
    "LOCATED_IN",
    "DISCOVERED_BY",
    "EXPLORED_BY",
    "ILLUSTRATED_BY",
    "INSPIRED",
    "FEATURES",
    "RECOMMENDS",
}

# Pre-build Cypher queries at import time from trusted constant sets.
# f-strings run once against known-safe values - not at query time from runtime input.
_NODE_MERGE: dict[str, str] = {
    lbl: (
        f"MERGE (n:{lbl} {{id: $id}})"
        " SET n.label = $label,"
        "     n.slug = $slug,"
        "     n.name = $name,"
        "     n.summary = $summary,"
        "     n.status = $status,"
        "     n.graph_version = $graph_version"
    )
    for lbl in LABELS
}

_REL_MERGE: dict[str, str] = {
    rt: (
        f"MATCH (source {{id: $source}})"
        f" MATCH (target {{id: $target}})"
        f" MERGE (source)-[r:{rt}]->(target)"
        f" SET r.reason = $reason,"
        f"     r.weight = $weight,"
        f"     r.graph_version = $graph_version"
    )
    for rt in REL_TYPES
}


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _run_schema(session) -> None:
    schema_path = Path(__file__).resolve().parents[1] / "schema" / "constraints.cypher"
    for statement in schema_path.read_text(encoding="utf-8").split(";"):
        statement = statement.strip()
        if statement:
            session.run(statement)


def _merge_node(tx, node: dict) -> None:
    label = node["label"]
    if label not in _NODE_MERGE:
        raise ValueError(f"Unsupported graph label: {label}")
    tx.run(
        _NODE_MERGE[label],
        id=node["id"],
        label=node["label"],
        slug=node["slug"],
        name=node["name"],
        summary=node["summary"],
        status=node["status"],
        graph_version="NC-GRAPH-003",
    )


def _merge_relationship(tx, rel: dict) -> None:
    rel_type = rel["type"]
    if rel_type not in _REL_MERGE:
        raise ValueError(f"Unsupported graph relationship: {rel_type}")
    tx.run(
        _REL_MERGE[rel_type],
        source=rel["source"],
        target=rel["target"],
        reason=rel["reason"],
        weight=rel["weight"],
        graph_version="NC-GRAPH-003",
    )


def load_seed() -> None:
    if GraphDatabase is None:
        raise RuntimeError("Install neo4j to load the graph seed")

    uri = _env("NEO4J_URI", "bolt://localhost:7687")
    user = _env("NEO4J_USER", "neo4j")
    password = _env("NEO4J_PASSWORD", "nc-dev-password")
    database = _env("NEO4J_DATABASE", "neo4j")

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            _run_schema(session)
            for node in NODES:
                session.execute_write(_merge_node, node)
            for rel in RELATIONSHIPS:
                session.execute_write(_merge_relationship, rel)

    print(f"Loaded {len(NODES)} nodes and {len(RELATIONSHIPS)} relationships into {uri}")


if __name__ == "__main__":
    load_seed()
