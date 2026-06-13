from services.data.masterpiece_registry import (
    MASTERPIECE_RUNTIME_VERSION,
    build_masterpiece_collections,
    build_masterpiece_registry,
    build_masterpiece_runtime,
    score_masterpiece,
)


def test_score_masterpiece_is_bounded_and_rewards_ready_public_domain_records() -> None:
    score = score_masterpiece(
        {
            "base_score": 58,
            "readiness_state": "ready",
            "collection_slugs": ["earthrise", "space-earth-observation"],
            "product_types": ["fine_art_print", "digital_download"],
            "rights_status": "public_domain",
        }
    )

    assert 0 <= score <= 100
    assert score > 80


def test_masterpiece_registry_ranks_published_and_candidate_records() -> None:
    registry = build_masterpiece_registry()

    assert len(registry) == 3
    assert registry[0]["masterpiece_slug"] == "earthrise"
    assert registry[0]["registry_status"] == "published"
    assert {record["registry_status"] for record in registry} == {"published", "candidate"}
    assert all("masterpiece_score" in record for record in registry)
    assert all(record["canonical_publication_created"] is False for record in registry[1:])


def test_masterpiece_collections_groups_registry_by_collection_slug() -> None:
    collections = build_masterpiece_collections(build_masterpiece_registry())

    assert "earthrise" in collections
    assert "biodiversity-library" in collections
    assert "yellowstone" in collections
    assert collections["earthrise"][0]["title"] == "Earthrise"


def test_masterpiece_runtime_returns_required_surfaces() -> None:
    runtime = build_masterpiece_runtime()

    assert runtime["runtime_version"] == MASTERPIECE_RUNTIME_VERSION
    assert runtime["io_runtime_version"] == "NC-IO-001-v1"
    assert set(runtime) >= {
        "masterpiece_score",
        "masterpiece_registry",
        "masterpiece_collections",
        "summary",
    }
    assert runtime["summary"] == {
        "runtime_version": "NC-MASTERPIECES-001-v1",
        "total_masterpieces": 3,
        "top_100_count": 3,
        "registry_status_counts": {"candidate": 2, "published": 1},
        "source_system_counts": {"BHL": 2, "NASA": 1},
        "collection_count": 6,
        "candidate_count": 2,
        "published_count": 1,
    }
