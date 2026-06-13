from graph.loaders.load_seed import (
    _NODE_MERGE,
    _REL_MERGE,
    _merge_node,
    _merge_relationship,
)
from graph.seed import NODES, RELATIONSHIPS, journey_for, recommendations_for


def test_graph_seed_contains_required_labels_and_relationships():
    labels = {node["label"] for node in NODES}
    relationship_types = {relationship["type"] for relationship in RELATIONSHIPS}

    assert labels == {
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
    assert relationship_types == {
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


def test_graph_seed_loads_four_required_places():
    place_slugs = {node["slug"] for node in NODES if node["label"] == "Place"}

    assert {"earthrise", "yellowstone", "grand-canyon", "great-barrier-reef"}.issubset(
        place_slugs
    )


def test_graph_seed_recommendations_and_journey():
    recommendations = recommendations_for("earthrise-collection")
    journey = journey_for("earthrise-collection")

    assert [item["node"]["slug"] for item in recommendations] == [
        "earthrise-museum-print",
        "earthrise-digital-edition",
        "great-barrier-reef-collection",
        "yellowstone-collection",
    ]
    assert any(node["slug"] == "great-barrier-reef-collection" for node in journey["nodes"])
    assert any(rel["type"] == "FEATURES" for rel in journey["relationships"])


class _FakeTx:
    def __init__(self):
        self.query = None
        self.params = None

    def run(self, query, **params):
        self.query = query
        self.params = params


def test_graph_loader_uses_explicit_node_parameters():
    tx = _FakeTx()
    node = dict(NODES[0])
    node["shopify_variant_id"] = "must-not-pass"
    node["rights"] = "must-not-pass"

    _merge_node(tx, node)

    assert tx.params == {
        "id": node["id"],
        "label": node["label"],
        "slug": node["slug"],
        "name": node["name"],
        "summary": node["summary"],
        "status": node["status"],
        "graph_version": "NC-GRAPH-003",
    }


def test_graph_loader_uses_explicit_relationship_parameters():
    tx = _FakeTx()
    rel = dict(RELATIONSHIPS[0])
    rel["rights"] = "must-not-pass"
    rel["shopify_variant_id"] = "must-not-pass"

    _merge_relationship(tx, rel)

    assert tx.params == {
        "source": rel["source"],
        "target": rel["target"],
        "reason": rel["reason"],
        "weight": rel["weight"],
        "graph_version": "NC-GRAPH-003",
    }


def test_graph_loader_merge_contract_does_not_use_source_table_columns():
    assert all("$id" in query and "{id:" in query for query in _NODE_MERGE.values())
    assert all("place_id" not in query for query in _NODE_MERGE.values())
    assert all("place_id" not in query for query in _REL_MERGE.values())

