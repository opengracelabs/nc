"""MILESTONE-003 taxon discovery replay tests.

Taxon discovery uses taxa as search handles for commercial public-domain
illustration opportunities. It must not optimize for species frequency,
popularity, or raw occurrence counts.
"""
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from services.api.routers import taxa
from workers.taxon_discovery_worker.rank import (
    build_bhl_search_targets,
    rank_taxa,
    rank_taxon_candidate,
)

MIGRATION_16 = Path("infrastructure/postgres/init/16_taxon_discovery.sql")
MODEL_DOC = Path("docs/architecture/bhl_illustration_asset_model.md")

_PLACE_ID = uuid4()
_CANDIDATE_ID = uuid4()
_RUN_ID = uuid4()


def _orchid_candidate() -> dict:
    return {
        "scientific_name": "Dendrobium bigibbum",
        "canonical_name": "Dendrobium bigibbum",
        "taxon_rank": "species",
        "gbif_taxon_key": 2809354,
        "wikidata_qid": "Q5259770",
        "common_names": ["Cooktown orchid"],
        "historic_names": ["Vappodes bigibba"],
        "genus": "Dendrobium",
        "visual_groups": ["orchid", "plant"],
        "gbif_occurrence_count": 4,
        "gbif_dataset_count": 2,
        "within_place_geometry": True,
        "wikidata_place_statement": True,
        "endemic_to_place": True,
        "threatened_status": False,
        "bhl_known_group": True,
        "pre_1931_literature_likelihood": True,
        "visually_distinctive": True,
        "collection_theme_fit": True,
    }


def _common_grass_candidate() -> dict:
    return {
        "scientific_name": "Poa annua",
        "canonical_name": "Poa annua",
        "taxon_rank": "species",
        "gbif_taxon_key": 2704179,
        "wikidata_qid": "Q157409",
        "common_names": ["annual meadow grass"],
        "historic_names": [],
        "genus": "Poa",
        "visual_groups": ["grass"],
        "gbif_occurrence_count": 10000,
        "gbif_dataset_count": 20,
        "within_place_geometry": True,
        "wikidata_place_statement": False,
        "endemic_to_place": False,
        "threatened_status": False,
        "bhl_known_group": False,
        "pre_1931_literature_likelihood": False,
        "visually_distinctive": False,
        "collection_theme_fit": False,
    }


def test_taxon_discovery_migration_exists() -> None:
    assert MIGRATION_16.exists()


def test_taxon_discovery_schema_has_ranked_candidates_and_targets() -> None:
    sql = MIGRATION_16.read_text()
    assert "CREATE TABLE taxon_discovery_runs" in sql
    assert "CREATE TABLE taxon_candidates" in sql
    assert "CREATE TABLE taxon_candidate_evidence" in sql
    assert "CREATE TABLE bhl_search_targets" in sql


def test_taxon_discovery_schema_requires_gbif_or_wikidata_source() -> None:
    sql = MIGRATION_16.read_text()
    assert "chk_taxon_candidate_source" in sql
    assert "gbif_taxon_key IS NOT NULL OR wikidata_qid IS NOT NULL" in sql
    assert "source IN ('gbif','wikidata')" in sql


def test_taxon_discovery_schema_requires_bhl_search_targets() -> None:
    sql = MIGRATION_16.read_text()
    assert "taxon candidate % has no BHL search targets" in sql
    assert "trg_taxon_candidate_supported" in sql


def test_asset_model_declares_concept_centered_assets() -> None:
    text = MODEL_DOC.read_text()
    assert "Commercial assets are concept-centered" in text
    assert "places connect to those concepts" in text
    assert "No BHL asset rights are inferred at this stage" in text


def test_asset_model_declares_opportunity_not_species_optimization() -> None:
    text = MODEL_DOC.read_text()
    assert "does not optimize for species" in text
    assert "Taxa are intermediate search handles" in text
    assert "high-value public-domain illustration opportunities" in text


def test_ranker_optimizes_illustration_opportunity_not_species() -> None:
    ranked = rank_taxa([_common_grass_candidate(), _orchid_candidate()])

    assert ranked[0]["scientific_name"] == "Dendrobium bigibbum"
    assert ranked[1]["scientific_name"] == "Poa annua"
    assert ranked[0]["total_score"] > ranked[1]["total_score"]
    assert ranked[1]["score_components"]["gbif_occurrence_count_capped"] == 100


def test_ranker_does_not_infer_bhl_rights() -> None:
    result = rank_taxon_candidate(_orchid_candidate())

    assert result["public_domain_path_score"] > 0
    assert (
        result["provenance"]["rights_rule"]
        == "No BHL asset rights inferred at taxon discovery stage."
    )


def test_bhl_search_targets_include_names_synonyms_and_genus() -> None:
    targets = build_bhl_search_targets(_orchid_candidate())
    queries = [target["query"] for target in targets]

    assert "Dendrobium bigibbum" in queries
    assert "Vappodes bigibba" in queries
    assert "Cooktown orchid" in queries
    assert "Dendrobium" in queries


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeTaxaConn:
    def __init__(self, status: str = "candidate") -> None:
        self.status = status
        self.fetchrow_queries: list[str] = []
        self.executed: list[tuple[str, tuple]] = []

    def transaction(self):
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append(query)
        if "SELECT status FROM taxon_candidates" in query:
            return {"status": self.status}
        if "FROM taxon_candidates" in query:
            return {
                "id": _CANDIDATE_ID,
                "run_id": _RUN_ID,
                "place_id": _PLACE_ID,
                "concept_id": None,
                "scientific_name": "Dendrobium bigibbum",
                "canonical_name": "Dendrobium bigibbum",
                "taxon_rank": "species",
                "gbif_taxon_key": "2809354",
                "wikidata_qid": "Q5259770",
                "common_names": ["Cooktown orchid"],
                "status": self.status,
                "place_relevance_score": 0.9,
                "source_agreement_score": 1.0,
                "illustration_likelihood_score": 0.9,
                "public_domain_path_score": 0.8,
                "commercial_value_score": 0.95,
                "searchability_score": 1.0,
                "total_score": 0.91,
                "score_components": json.dumps({}),
                "provenance": json.dumps({}),
                "agent_notes": json.dumps({}),
                "created_at": "2026-06-01T00:00:00Z",
                "updated_at": "2026-06-01T00:00:00Z",
            }
        return None

    async def fetch(self, query: str, *args):
        if "FROM taxon_candidate_evidence" in query:
            return [
                {
                    "id": uuid4(),
                    "candidate_id": _CANDIDATE_ID,
                    "source": "gbif",
                    "evidence_type": "occurrence_summary",
                    "source_record_id": "2809354",
                    "source_url": "https://www.gbif.org/species/2809354",
                    "payload": json.dumps({"occurrence_count": 4}),
                    "provenance": json.dumps({}),
                    "created_at": "2026-06-01T00:00:00Z",
                }
            ]
        if "FROM bhl_search_targets" in query:
            return [
                {
                    "id": uuid4(),
                    "candidate_id": _CANDIDATE_ID,
                    "sequence": 1,
                    "query": "Dendrobium bigibbum",
                    "target_type": "scientific_name",
                    "status": "pending",
                    "provenance": json.dumps({}),
                    "created_at": "2026-06-01T00:00:00Z",
                }
            ]
        return []

    async def execute(self, query: str, *args):
        self.executed.append((query, args))
        return "UPDATE 1"


async def test_get_taxon_candidate_returns_evidence_and_targets() -> None:
    result = await taxa.get_taxon_candidate(
        candidate_id=UUID(str(_CANDIDATE_ID)),
        auth="dev-secret",
        conn=FakeTaxaConn(),
    )

    assert result["scientific_name"] == "Dendrobium bigibbum"
    assert result["evidence"][0]["source"] == "gbif"
    assert result["bhl_search_targets"][0]["query"] == "Dendrobium bigibbum"


async def test_taxon_candidate_governance_locks_before_approval() -> None:
    conn = FakeTaxaConn(status="candidate")
    result = await taxa.act_on_taxon_candidate(
        candidate_id=UUID(str(_CANDIDATE_ID)),
        body=taxa.TaxonCandidateAction(action="approve", reviewer="curator"),
        auth="dev-secret",
        conn=conn,
    )

    assert result["status"] == "approved"
    assert any("FOR UPDATE" in query for query in conn.fetchrow_queries)
    assert any("UPDATE taxon_candidates" in query for query, _ in conn.executed)


async def test_taxon_candidate_reject_requires_reason() -> None:
    with pytest.raises(Exception) as exc_info:
        await taxa.act_on_taxon_candidate(
            candidate_id=UUID(str(_CANDIDATE_ID)),
            body=taxa.TaxonCandidateAction(action="reject", reviewer="curator"),
            auth="dev-secret",
            conn=FakeTaxaConn(status="candidate"),
        )
    assert getattr(exc_info.value, "status_code", None) == 422
