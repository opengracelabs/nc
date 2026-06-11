import json
from pathlib import Path

from workers.gbif_adapter.identity import normalize_taxon_identity
from workers.gbif_adapter.occurrence import (
    normalize_occurrence_search_payload,
    summarize_place_relevance,
)

GBIF_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "gbif_adapter"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gbif"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_gbif_sprint1_file_boundary_is_evidence_only() -> None:
    assert (GBIF_ADAPTER / "__init__.py").exists()
    assert (GBIF_ADAPTER / "config.py").exists()
    assert (GBIF_ADAPTER / "client.py").exists()
    assert (GBIF_ADAPTER / "identity.py").exists()
    assert (GBIF_ADAPTER / "occurrence.py").exists()
    assert (GBIF_ADAPTER / "normalize.py").exists()
    assert (GBIF_ADAPTER / "rights.py").exists()
    assert not (GBIF_ADAPTER / "store.py").exists()
    assert not (GBIF_ADAPTER / "media.py").exists()


def test_gbif_sprint1_no_m36_or_media_pipeline_terms() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in GBIF_ADAPTER.glob("*.py")
    )

    assert "write_normalized_record" not in combined
    assert "source_item" not in combined
    assert "workflow_item" not in combined
    assert "M36" not in combined
    assert "media_file" not in combined


def test_gbif_sprint1_identity_replay_is_stable() -> None:
    evidence = normalize_taxon_identity(fixture_json("species_match_panthera_leo.json"))

    assert evidence["record_id"] == "5219404"
    assert evidence["source_slug"] == "gbif"
    assert evidence["schema_standard"] == "gbif_darwin_core_evidence_v1"
    assert evidence["source_url"] == "https://www.gbif.org/species/5219404"


def test_gbif_sprint1_occurrence_replay_preserves_doi_and_citation() -> None:
    evidence = normalize_occurrence_search_payload(fixture_json("occurrence_search_page.json"))

    assert [item["gbif_occurrence_key"] for item in evidence] == ["3001", "3002"]
    assert evidence[0]["dataset_doi"] == "10.15468/example.cc0"
    assert evidence[0]["citation"] == "Example Museum (2026). Open savanna observations. GBIF."
    assert evidence[1]["rights_basis"] == "cc_by_evidence_attribution_required"


def test_gbif_sprint1_occurrence_count_cap_replay_is_stable() -> None:
    summary = summarize_place_relevance(fixture_json("occurrence_search_page.json"))

    assert summary == {
        "source": "gbif",
        "source_role": "validation_only",
        "occurrence_count": 10000,
        "occurrence_count_cap": 100,
        "occurrence_count_capped": 100,
        "evidence_count": 2,
        "taxon_keys": ["5219404"],
    }

