from pathlib import Path

from services.data.place_seed import export_candidate_summary, load_first_100_candidates

SEED = Path("data/curated/places/first_100_places_seed.json")
GRAPH_DIR = Path("graph")


def test_nc_places_001_seed_file_exists():
    assert SEED.exists()


def test_nc_places_001_loads_exactly_100_unverified_candidates():
    records = load_first_100_candidates(SEED)

    assert len(records) == 100
    assert all(record["candidate_status"] == "candidate" for record in records)
    assert all(record["authority_status"] == "unverified" for record in records)
    assert all(record["source_hints"] for record in records)


def test_nc_places_001_required_launch_places_are_candidate_only():
    records = {record["place_slug"]: record for record in load_first_100_candidates(SEED)}

    for slug in ("earthrise", "yellowstone", "grand-canyon", "great-barrier-reef"):
        assert records[slug]["candidate_status"] == "candidate"
        assert records[slug]["authority_status"] == "unverified"


def test_nc_places_001_seed_does_not_create_canonical_authority_fields():
    forbidden = {
        "canonical_identity",
        "canonical_place_id",
        "geonames_id",
        "geonames_place_id",
        "wikidata_qid",
        "gbif_place_key",
        "product_page_slug",
        "neo4j_node_id",
    }

    for record in load_first_100_candidates(SEED):
        assert forbidden.isdisjoint(record)


def test_nc_places_001_summary_reports_no_downstream_writes():
    summary = export_candidate_summary(load_first_100_candidates(SEED))

    assert summary["canonical_identity_written"] is False
    assert summary["product_pages_created"] is False
    assert summary["neo4j_canonical_nodes_created"] is False


def test_nc_places_001_does_not_add_candidateplace_graph_nodes():
    graph_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in GRAPH_DIR.rglob("*.py")
    )

    assert "CandidatePlace" not in graph_sources
