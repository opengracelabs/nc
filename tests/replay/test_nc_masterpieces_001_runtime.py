"""NC-MASTERPIECES-001 replay tests."""

from services.data.masterpiece_registry import build_masterpiece_runtime


def test_nc_masterpieces_001_runtime_exposes_registry_surfaces() -> None:
    runtime = build_masterpiece_runtime()

    assert runtime["runtime_version"] == "NC-MASTERPIECES-001-v1"
    assert len(runtime["masterpiece_registry"]) == 3
    assert len(runtime["masterpiece_score"]) == 3
    assert runtime["summary"]["top_100_count"] == 3
    assert runtime["masterpiece_registry"][0]["masterpiece_slug"] == "earthrise"


def test_nc_masterpieces_001_candidate_records_do_not_publish() -> None:
    runtime = build_masterpiece_runtime()
    candidates = [record for record in runtime["masterpiece_registry"] if record["candidate_only"]]

    assert len(candidates) == 2
    assert all(record["registry_status"] == "candidate" for record in candidates)
    assert all(record["canonical_publication_created"] is False for record in candidates)
