"""MILESTONE-003 illustration opportunity replay tests."""
from pathlib import Path

from workers.illustration_opportunity_worker.rank import (
    score_illustration_opportunity,
    verify_commercial_rights,
)

MIGRATION_16 = Path("infrastructure/postgres/init/16_taxon_discovery.sql")
MODEL_DOC = Path("docs/architecture/bhl_illustration_asset_model.md")
README = Path("README.md")
RELEASE = Path("docs/releases/v0.3.0.md")


def _verified_opportunity() -> dict:
    return {
        "taxon_name": "Acanthaster planci",
        "publication_title": "Naturalist's Miscellany",
        "illustrator": "Nodder",
        "publication_year": 1789,
        "source_url": "https://www.biodiversitylibrary.org/page/example",
        "rights_status": "Public Domain",
        "rights_source_url": "https://www.biodiversitylibrary.org/page/example",
        "rights_verified_by": "curator",
        "illustration_quality_score": 0.94,
        "place_relevance_score": 0.91,
        "historical_significance_score": 0.88,
        "commercial_value_score": 0.93,
    }


def test_migration_16_contains_illustration_opportunity_schema() -> None:
    assert MIGRATION_16.exists()


def test_platform_identity_is_not_biodiversity_inventory() -> None:
    readme = README.read_text()
    model = MODEL_DOC.read_text()
    release = RELEASE.read_text()

    assert "not a biodiversity inventory system" in readme
    assert "place-centered public-domain illustration discovery and commerce platform" in readme
    assert "not a biodiversity inventory system" in model
    assert "Biodiversity data is used only when it helps" in model
    assert "Not a biodiversity inventory system" in release


def test_illustration_opportunity_schema_is_concept_owned_and_place_linked() -> None:
    sql = MIGRATION_16.read_text()
    assert "CREATE TABLE illustration_opportunities" in sql
    opportunity_table = sql.split("CREATE TABLE illustration_opportunities", 1)[1]
    opportunity_table = opportunity_table.split(
        "CREATE TABLE illustration_opportunity_places", 1
    )[0]
    assert "concept_id          UUID NOT NULL REFERENCES concepts(id)" in opportunity_table
    assert "place_id" not in opportunity_table
    assert "CREATE TABLE illustration_opportunity_places" in sql
    assert "UNIQUE (opportunity_id, place_id)" in sql


def test_illustration_opportunity_schema_has_worker_required_fields() -> None:
    sql = MIGRATION_16.read_text()
    for field in (
        "concept_id          UUID NOT NULL REFERENCES concepts(id)",
        "bhl_item_id         TEXT NOT NULL",
        "bhl_page_id         TEXT NOT NULL",
        "publication_year    INT",
        "illustrator         TEXT",
        "rights_status       TEXT NOT NULL",
        "opportunity_score   NUMERIC(4,3) NOT NULL",
    ):
        assert field in sql


def test_concepts_schema_allows_taxon_concepts() -> None:
    sql = Path("infrastructure/postgres/init/08_knowledge_concepts.sql").read_text()
    assert "'geographic','thematic','actor','taxon'" in sql


def test_illustration_opportunity_schema_has_governance_and_score_components() -> None:
    sql = MIGRATION_16.read_text()
    for field in (
        "reviewed_by         TEXT",
        "reviewed_at         TIMESTAMPTZ",
        "rejection_reason    TEXT",
        "score_components    JSONB NOT NULL DEFAULT '{}'",
    ):
        assert field in sql


def test_illustration_opportunity_source_urls_are_nullable() -> None:
    sql = MIGRATION_16.read_text()
    assert "source_url          TEXT,\n    bhl_item_id" in sql
    assert "source_url          TEXT,\n    payload" in sql
    assert "rights_source_url   TEXT," in sql


def test_illustration_opportunity_schema_requires_explicit_commercial_rights() -> None:
    sql = MIGRATION_16.read_text()
    assert "rights_status IN" in sql
    assert "'Public Domain','CC0'" in sql
    assert "has no explicit rights evidence" in sql


def test_illustration_opportunity_schema_requires_evidence_and_place_connection() -> None:
    sql = MIGRATION_16.read_text()
    assert "has no illustration evidence" in sql
    assert "is not connected to any place" in sql
    assert "trg_illustration_opportunity_supported" in sql


def test_doctrine_declares_source_roles_and_taxon_role() -> None:
    text = MODEL_DOC.read_text()
    assert "BHL: Primary Discovery Source" in text
    assert "GBIF: Validation Source" in text
    assert "Wikidata: Context Source" in text
    assert "Taxa are metadata, semantic anchors, and search handles" in text
    assert "not species-centered and not art-centered" in text


def test_doctrine_declares_golden_age_and_priority_illustrators() -> None:
    text = MODEL_DOC.read_text()
    assert "1750 through 1900" in text
    for illustrator in (
        "Audubon",
        "Gould",
        "Merian",
        "Redouté",
        "Lear",
        "Nodder",
        "Haeckel",
        "Wolf",
    ):
        assert illustrator in text


def test_doctrine_declares_roadmap_order() -> None:
    text = MODEL_DOC.read_text()
    assert "Migration 16 → Illustration Opportunity Discovery" in text
    assert "Human Approval → BHL Asset Ingestion → Collections → Products" in text


def test_directive_declares_opportunity_not_species_success_metric() -> None:
    text = MODEL_DOC.read_text()
    assert "The success metric is not `Species`; it is `Illustration Opportunity`" in text
    assert "One illustration can support many places" in text
    assert "must not be duplicated per place" in text


def test_verified_public_domain_opportunity_scores() -> None:
    result = score_illustration_opportunity(_verified_opportunity())

    assert result is not None
    assert result["taxon_name"] == "Acanthaster planci"
    assert result["publication_title"] == "Naturalist's Miscellany"
    assert result["illustrator"] == "Nodder"
    assert result["publication_year"] == 1789
    assert result["rights_status"] == "Public Domain"
    assert result["opportunity_score"] > 0.9
    assert result["score_components"]["rights_certainty_score"] == 1.0
    assert result["provenance"]["optimization_target"] == (
        "high_value_public_domain_illustration_opportunity"
    )


def test_unverified_rights_cannot_enter_opportunity_pipeline() -> None:
    candidate = _verified_opportunity()
    candidate["rights_verified_by"] = None

    assert verify_commercial_rights(candidate) is False
    assert score_illustration_opportunity(candidate) is None


def test_rights_source_url_is_nullable_without_weakening_rights_status() -> None:
    candidate = _verified_opportunity()
    candidate["rights_source_url"] = None

    assert verify_commercial_rights(candidate) is True
    assert score_illustration_opportunity(candidate) is not None


def test_cc0_is_allowed_but_ambiguous_rights_are_not() -> None:
    candidate = _verified_opportunity()
    candidate["rights_status"] = "CC0"
    assert verify_commercial_rights(candidate) is True

    candidate["rights_status"] = "No known copyright restrictions"
    assert verify_commercial_rights(candidate) is False


def test_golden_age_priority_and_priority_illustrator_are_scored() -> None:
    candidate = _verified_opportunity()
    result = score_illustration_opportunity(candidate)

    assert result is not None
    assert result["golden_age_priority_score"] == 1.0
    assert result["priority_illustrator_score"] == 1.0
    assert result["provenance"]["taxon_role"] == "metadata_semantic_anchor_search_handle"


def test_outside_golden_age_has_lower_historical_score() -> None:
    golden = score_illustration_opportunity(_verified_opportunity())
    later_candidate = _verified_opportunity()
    later_candidate["publication_year"] = 1940
    later_candidate["illustrator"] = "Unknown"
    later = score_illustration_opportunity(later_candidate)

    assert golden is not None
    assert later is not None
    assert golden["historical_significance_score"] > later["historical_significance_score"]
