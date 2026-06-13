from services.api.routers.graph import graph_journey, graph_place, graph_recommendations, graph_related


def test_graph_place_endpoint_uses_seed_fallback():
    payload = graph_place("earthrise")

    assert payload["place"]["label"] == "Place"
    assert payload["place"]["slug"] == "earthrise"
    assert payload["source"] in {"seed", "neo4j"}


def test_graph_recommendations_endpoint_uses_seed_fallback():
    payload = graph_recommendations("earthrise-collection")

    assert payload["subject"]["label"] == "Collection"
    assert any(
        item["node"]["slug"] == "great-barrier-reef-collection"
        for item in payload["recommendations"]
    )
    assert all(item["node"]["label"] != "Product" for item in payload["recommendations"])


def test_graph_journey_endpoint_uses_seed_fallback():
    payload = graph_journey("earthrise-collection")

    assert any(node["label"] == "Asset" for node in payload["nodes"])
    assert any(rel["type"] == "RECOMMENDS" for rel in payload["relationships"])


def test_graph_related_endpoint_uses_seed_fallback():
    payload = graph_related("earthrise")

    assert payload["subject"]["label"] == "Place"
    assert any(item["relationship"]["type"] == "LOCATED_IN" for item in payload["related"])


def test_graph_runtime_strips_product_status_from_serialized_nodes():
    from services.api.graph_runtime import _serialize_node

    payload = _serialize_node(
        {
            "id": "product:test",
            "slug": "test-product",
            "label": "Product",
            "name": "Test Product",
            "summary": "A graph product node.",
            "status": "live",
        }
    )

    assert payload["label"] == "Product"
    assert "status" not in payload
