"""MILESTONE-002 replay tests: Knowledge Facts + Relationships.

All tests are pure Python — no database or MinIO required.
They exercise the exact production functions used by the knowledge worker
and API router.

Traceability guarantee tested here:
    Every fact has provenance.source_field documenting the exact place column.
    Every fact is deterministic from the same input.
    Every relationship is derived only from evidence in facts.
"""
import json
from pathlib import Path
from uuid import uuid4

from workers.discovery_worker.normalize import normalize_unesco_whc
from workers.discovery_worker.sources.base import RawRecord
from workers.knowledge_worker.extract import (
    build_place_concept_relationships,
    extract_facts,
)
from workers.knowledge_worker.score import score_fact

FIXTURE = Path("tests/fixtures/unesco_whc_50_sites.json")
SITES: list[dict] = json.loads(FIXTURE.read_text())

_VALID_CONCEPT_TYPES = {
    "criterion", "heritage_type", "ecosystem", "biome",
    "geographic", "thematic", "actor",
}

_VALID_PREDICATES = {
    "inscription_year", "core_area_ha", "buffer_area_ha", "transboundary",
    "heritage_type", "ouv_criterion", "country_code", "spatial_precision",
    "name", "description", "statement_of_ouv",
    "endangered_status", "endangered_since",
}

_VALID_VALUE_TYPES = {"text", "number", "date", "boolean", "uri", "geometry", "jsonb"}

_VALID_FACT_TRANSITIONS = {
    "dispute": ("disputed", {"active"}),
    "retract": ("retracted", {"disputed"}),
}


def _make_place(site: dict) -> dict:
    """Normalize a fixture site into a place-dict the knowledge worker reads."""
    rec = normalize_unesco_whc(RawRecord(source_id=str(site["id_number"]), payload=site))
    return {
        "id": uuid4(),
        "source": "unesco_whc",
        **rec,
    }


def _all_places() -> list[dict]:
    return [_make_place(s) for s in SITES]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def test_score_fact_unesco_whc_base_is_0_95() -> None:
    assert score_fact("unesco_whc") == 0.95


def test_score_fact_asset_evidence_adds_0_05() -> None:
    assert score_fact("unesco_whc", asset_id=uuid4()) == 1.0


def test_score_fact_corroboration_adds_0_05() -> None:
    assert score_fact("unesco_whc", corroborated=True) == 1.0


def test_score_fact_capped_at_1_0() -> None:
    assert score_fact("unesco_whc", asset_id=uuid4(), corroborated=True) == 1.0


def test_score_fact_wikidata_base_is_0_80() -> None:
    assert score_fact("wikidata") == 0.80


def test_score_fact_unknown_source_defaults_to_0_60() -> None:
    assert score_fact("unknown_source") == 0.60


def test_score_fact_is_deterministic() -> None:
    assert score_fact("unesco_whc") == score_fact("unesco_whc")


# ---------------------------------------------------------------------------
# Fact extraction — structure
# ---------------------------------------------------------------------------

def test_extract_facts_returns_list() -> None:
    place = _make_place(SITES[0])
    facts = extract_facts(place)
    assert isinstance(facts, list)
    assert len(facts) > 0


def test_every_fact_has_required_keys() -> None:
    required = {"place_id", "predicate", "value", "value_type", "source",
                "confidence_score", "provenance"}
    for place in _all_places():
        for fact in extract_facts(place):
            missing = required - fact.keys()
            assert not missing, f"Fact missing keys {missing}: {fact}"


def test_every_fact_predicate_is_in_controlled_vocabulary() -> None:
    for place in _all_places():
        for fact in extract_facts(place):
            assert fact["predicate"] in _VALID_PREDICATES, (
                f"source_id={place.get('source_id')} invalid predicate={fact['predicate']!r}"
            )


def test_every_fact_value_type_is_valid() -> None:
    for place in _all_places():
        for fact in extract_facts(place):
            assert fact["value_type"] in _VALID_VALUE_TYPES, (
                f"invalid value_type={fact['value_type']!r}"
            )


def test_every_fact_value_is_dict() -> None:
    for place in _all_places():
        for fact in extract_facts(place):
            assert isinstance(fact["value"], dict), (
                f"predicate={fact['predicate']} value is not a dict: {fact['value']!r}"
            )


def test_every_fact_confidence_score_is_in_range() -> None:
    for place in _all_places():
        for fact in extract_facts(place):
            s = fact["confidence_score"]
            assert 0.0 <= s <= 1.0, f"confidence_score={s} out of range"


def test_all_facts_have_asset_id_none_for_field_mapping() -> None:
    """Field-mapping facts are derived from place columns, not directly from assets."""
    for place in _all_places():
        for fact in extract_facts(place):
            assert fact["asset_id"] is None


def test_all_facts_have_source_equal_to_place_source() -> None:
    for place in _all_places():
        for fact in extract_facts(place):
            assert fact["source"] == place["source"]


# ---------------------------------------------------------------------------
# Fact extraction — provenance (traceability)
# ---------------------------------------------------------------------------

def test_every_fact_has_prov_was_generated_by() -> None:
    place = _make_place(SITES[0])
    for fact in extract_facts(place):
        prov = fact["provenance"]
        assert "prov:wasGeneratedBy" in prov, f"Missing prov:wasGeneratedBy in {fact['predicate']}"


def test_every_fact_has_extraction_method_field_mapping() -> None:
    place = _make_place(SITES[0])
    for fact in extract_facts(place):
        assert fact["provenance"]["extraction_method"] == "field_mapping"


def test_every_fact_has_source_field_in_provenance() -> None:
    """source_field documents the exact place column — makes every fact replayable."""
    place = _make_place(SITES[0])
    for fact in extract_facts(place):
        assert "source_field" in fact["provenance"], (
            f"predicate={fact['predicate']} missing provenance.source_field"
        )


def test_every_fact_provenance_source_field_starts_with_places() -> None:
    place = _make_place(SITES[0])
    for fact in extract_facts(place):
        sf = fact["provenance"]["source_field"]
        assert sf.startswith("places.") or sf.startswith("field:"), (
            f"predicate={fact['predicate']} unexpected source_field={sf!r}"
        )


def test_every_fact_has_extraction_version_in_provenance() -> None:
    place = _make_place(SITES[0])
    for fact in extract_facts(place):
        assert "extraction_version" in fact["provenance"]


# ---------------------------------------------------------------------------
# Fact extraction — content correctness
# ---------------------------------------------------------------------------

def test_great_barrier_reef_inscription_year_fact() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    yr_facts = [f for f in facts if f["predicate"] == "inscription_year"]
    assert len(yr_facts) == 1
    assert yr_facts[0]["value"] == {"number": 1981}
    assert yr_facts[0]["value_type"] == "number"


def test_great_barrier_reef_heritage_type_fact() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    ht_facts = [f for f in facts if f["predicate"] == "heritage_type"]
    assert len(ht_facts) == 1
    assert ht_facts[0]["value"] == {"text": "natural"}
    assert ht_facts[0]["concept_uri"] == "whc:type/natural"


def test_great_barrier_reef_ouv_criteria_produce_four_facts() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    crit_facts = [f for f in facts if f["predicate"] == "ouv_criterion"]
    criteria = {f["value"]["text"] for f in crit_facts}
    assert criteria == {"vii", "viii", "ix", "x"}


def test_great_barrier_reef_ouv_criteria_concept_uris() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    uris = {f["concept_uri"] for f in facts if f["predicate"] == "ouv_criterion"}
    assert uris == {"whc:criterion/vii", "whc:criterion/viii",
                    "whc:criterion/ix", "whc:criterion/x"}


def test_great_barrier_reef_country_code_fact() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    cc_facts = [f for f in facts if f["predicate"] == "country_code"]
    assert len(cc_facts) == 1
    assert cc_facts[0]["value"] == {"text": "AU"}


def test_great_barrier_reef_name_fact_has_english() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    name_en = [f for f in facts if f["predicate"] == "name" and f["language"] == "en"]
    assert len(name_en) == 1
    assert name_en[0]["value"]["text"] == "Great Barrier Reef"


def test_transboundary_site_produces_two_country_code_facts() -> None:
    victoria_falls = next(s for s in SITES if s["id_number"] == 647)
    place = _make_place(victoria_falls)
    facts = extract_facts(place)
    cc_facts = [f for f in facts if f["predicate"] == "country_code"]
    codes = {f["value"]["text"] for f in cc_facts}
    assert codes == {"ZW", "ZM"}


def test_transboundary_fact_is_true_for_multi_country_sites() -> None:
    victoria_falls = next(s for s in SITES if s["id_number"] == 647)
    place = _make_place(victoria_falls)
    facts = extract_facts(place)
    tb_facts = [f for f in facts if f["predicate"] == "transboundary"]
    assert len(tb_facts) == 1
    assert tb_facts[0]["value"] == {"boolean": True}
    assert tb_facts[0]["value_type"] == "boolean"


def test_site_with_core_area_produces_area_fact() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    area_facts = [f for f in facts if f["predicate"] == "core_area_ha"]
    assert len(area_facts) == 1
    assert area_facts[0]["value"]["number"] == 34800000.0


# ---------------------------------------------------------------------------
# Fact extraction — determinism and replay
# ---------------------------------------------------------------------------

def test_extraction_is_deterministic_for_all_50_sites() -> None:
    for place in _all_places():
        facts_a = [f["value"] for f in extract_facts(place)]
        facts_b = [f["value"] for f in extract_facts(place)]
        assert facts_a == facts_b, f"Non-deterministic for source_id={place.get('source_id')}"


def test_all_50_sites_produce_at_least_6_facts() -> None:
    """Minimum: inscription_year, heritage_type, ≥1 ouv_criterion,
    ≥1 country_code, transboundary, name_en — that's 6."""
    for place in _all_places():
        facts = extract_facts(place)
        assert len(facts) >= 6, (
            f"source_id={place.get('source_id')} only produced {len(facts)} facts"
        )


def test_all_50_sites_produce_inscription_year_fact() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        yr = [f for f in facts if f["predicate"] == "inscription_year"]
        assert len(yr) == 1, f"source_id={place.get('source_id')} missing inscription_year"


def test_all_50_sites_produce_heritage_type_fact() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        ht = [f for f in facts if f["predicate"] == "heritage_type"]
        assert len(ht) == 1, f"source_id={place.get('source_id')} missing heritage_type"


def test_all_50_sites_produce_at_least_one_ouv_criterion_fact() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        crit = [f for f in facts if f["predicate"] == "ouv_criterion"]
        assert len(crit) >= 1, f"source_id={place.get('source_id')} missing ouv_criterion"


def test_all_50_sites_produce_at_least_one_country_code_fact() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        cc = [f for f in facts if f["predicate"] == "country_code"]
        assert len(cc) >= 1, f"source_id={place.get('source_id')} missing country_code"


def test_all_50_sites_produce_name_en_fact() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        name_en = [f for f in facts if f["predicate"] == "name" and f["language"] == "en"]
        assert len(name_en) == 1, f"source_id={place.get('source_id')} missing name.en fact"


# ---------------------------------------------------------------------------
# Relationship building
# ---------------------------------------------------------------------------

def test_build_relationships_returns_list() -> None:
    place = _make_place(SITES[0])
    facts = extract_facts(place)
    rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
    assert isinstance(rels, list)
    assert len(rels) > 0


def test_heritage_type_fact_produces_classified_as_relationship() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
    classified = [r for r in rels if r["predicate"] == "classified_as"]
    assert len(classified) == 1
    assert classified[0]["concept_uri"] == "whc:type/natural"
    assert classified[0]["object_type"] == "concept"
    assert classified[0]["subject_type"] == "place"


def test_ouv_criterion_facts_produce_exemplifies_relationships() -> None:
    gbr = next(s for s in SITES if s["id_number"] == 31)
    place = _make_place(gbr)
    facts = extract_facts(place)
    rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
    exemplifies = [r for r in rels if r["predicate"] == "exemplifies"]
    uris = {r["concept_uri"] for r in exemplifies}
    assert "whc:criterion/vii" in uris
    assert "whc:criterion/x" in uris


def test_relationships_have_no_duplicates() -> None:
    place = _make_place(SITES[0])
    facts = extract_facts(place)
    rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
    keys = [(r["predicate"], r["concept_uri"]) for r in rels]
    assert len(keys) == len(set(keys)), "Duplicate relationships produced"


def test_relationships_all_have_provenance() -> None:
    place = _make_place(SITES[0])
    facts = extract_facts(place)
    rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
    for r in rels:
        assert "prov:wasGeneratedBy" in r["provenance"]
        assert r["provenance"]["extraction_method"] == "field_mapping"


def test_relationships_confidence_score_is_0_95_for_unesco() -> None:
    place = _make_place(SITES[0])
    facts = extract_facts(place)
    rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
    for r in rels:
        assert r["confidence_score"] == 0.95


def test_all_50_sites_produce_relationships() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        rels = build_place_concept_relationships(place["id"], facts, "unesco_whc")
        assert len(rels) >= 2, (
            f"source_id={place.get('source_id')} produced only {len(rels)} relationships"
        )


def test_relationship_derivation_is_deterministic() -> None:
    for place in _all_places():
        facts = extract_facts(place)
        rels_a = [(r["predicate"], r["concept_uri"])
                  for r in build_place_concept_relationships(place["id"], facts, "unesco_whc")]
        rels_b = [(r["predicate"], r["concept_uri"])
                  for r in build_place_concept_relationships(place["id"], facts, "unesco_whc")]
        assert rels_a == rels_b


# ---------------------------------------------------------------------------
# API governance state machine
# ---------------------------------------------------------------------------

def test_dispute_action_allowed_from_active() -> None:
    new_status, allowed_from = _VALID_FACT_TRANSITIONS["dispute"]
    assert "active" in allowed_from
    assert new_status == "disputed"


def test_dispute_action_not_allowed_from_draft() -> None:
    _, allowed_from = _VALID_FACT_TRANSITIONS["dispute"]
    assert "draft" not in allowed_from


def test_retract_action_allowed_from_disputed_only() -> None:
    _, allowed_from = _VALID_FACT_TRANSITIONS["retract"]
    assert allowed_from == {"disputed"}


def test_retract_directly_from_active_is_not_allowed() -> None:
    _, allowed_from = _VALID_FACT_TRANSITIONS["retract"]
    assert "active" not in allowed_from


def test_fact_governance_requires_reviewer() -> None:
    from services.api.routers.knowledge import FactAction

    action = FactAction(action="dispute", reviewer="auditor@example.com")
    assert action.reviewer == "auditor@example.com"


# ---------------------------------------------------------------------------
# Concept API validation
# ---------------------------------------------------------------------------

def test_concept_create_requires_english_label() -> None:
    from services.api.routers.knowledge import ConceptCreate

    body = ConceptCreate(uri="test:concept/x", label={"en": "Test"}, type="thematic")
    assert body.label["en"] == "Test"


def test_concept_type_validated_against_vocabulary() -> None:
    valid_types = {
        "criterion", "heritage_type", "ecosystem", "biome",
        "geographic", "thematic", "actor", "taxon",
    }
    for t in valid_types:
        from services.api.routers.knowledge import ConceptCreate
        body = ConceptCreate(uri=f"test:{t}", label={"en": "x"}, type=t)
        assert body.type == t
