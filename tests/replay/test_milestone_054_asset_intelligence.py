"""v0.5.4 Asset Intelligence Phase 1 replay tests."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from uuid import UUID, uuid4

from tests.replay.test_milestone_050_commerce_opportunity_worker import _base_inputs, _policy
from workers.asset_intelligence_worker.resolve import (
    apply_asset_intelligence_to_score_inputs,
    recompute_after_activation,
    resolve_asset_intelligence,
    resolve_creator_authority,
    resolve_creator_prestige,
    resolve_place_iconic_taxa,
)
from workers.commerce_opportunity_worker.score import compute_scores, replay_score

MIGRATION_32 = Path("infrastructure/postgres/init/32_asset_intelligence_anchor_type.sql")
MIGRATION_33 = Path("infrastructure/postgres/init/33_asset_intelligence_creator_registries.sql")
MIGRATION_34 = Path("infrastructure/postgres/init/34_asset_intelligence_place_iconic_taxa.sql")
MIGRATION_35 = Path("infrastructure/postgres/init/35_asset_intelligence_activation_recompute.sql")

_AUDUBON_AUTHORITY_ID = UUID("54000000-0000-0000-0000-000000000001")
_AUDUBON_PRESTIGE_ID = UUID("54000000-0000-0000-0000-000000000011")
_MORAN_AUTHORITY_ID = UUID("54000000-0000-0000-0000-000000000002")
_MORAN_PRESTIGE_ID = UUID("54000000-0000-0000-0000-000000000012")
_JACKSON_AUTHORITY_ID = UUID("54000000-0000-0000-0000-000000000003")
_JACKSON_PRESTIGE_ID = UUID("54000000-0000-0000-0000-000000000013")
_BISON_ICONIC_ID = UUID("54000000-0000-0000-0000-000000000101")


def _authority_rows() -> list[dict]:
    return [
        {
            "id": _AUDUBON_AUTHORITY_ID,
            "registry_version": "1.0.0",
            "canonical_creator_key": "john-james-audubon",
            "display_name": "John James Audubon",
            "authority_confidence": 0.98,
            "attribution_risk": "medium",
            "status": "active",
        },
        {
            "id": _MORAN_AUTHORITY_ID,
            "registry_version": "1.0.0",
            "canonical_creator_key": "thomas-moran",
            "display_name": "Thomas Moran",
            "authority_confidence": 0.97,
            "attribution_risk": "low",
            "status": "active",
        },
        {
            "id": _JACKSON_AUTHORITY_ID,
            "registry_version": "1.0.0",
            "canonical_creator_key": "william-henry-jackson",
            "display_name": "William Henry Jackson",
            "authority_confidence": 0.96,
            "attribution_risk": "medium",
            "status": "active",
        },
    ]


def _alias_rows() -> list[dict]:
    return [
        {
            "creator_authority_id": _AUDUBON_AUTHORITY_ID,
            "alias": "Audubon",
            "normalized_alias": "audubon",
            "confidence_score": 0.95,
        },
        {
            "creator_authority_id": _AUDUBON_AUTHORITY_ID,
            "alias": "John James Audubon",
            "normalized_alias": "john james audubon",
            "confidence_score": 0.99,
        },
        {
            "creator_authority_id": _MORAN_AUTHORITY_ID,
            "alias": "Thomas Moran",
            "normalized_alias": "thomas moran",
            "confidence_score": 0.99,
        },
        {
            "creator_authority_id": _JACKSON_AUTHORITY_ID,
            "alias": "William Henry Jackson",
            "normalized_alias": "william henry jackson",
            "confidence_score": 0.99,
        },
    ]


def _prestige_rows() -> list[dict]:
    return [
        {
            "id": _AUDUBON_PRESTIGE_ID,
            "registry_version": "1.0.0",
            "creator_authority_id": _AUDUBON_AUTHORITY_ID,
            "prestige_score": 1.0,
            "prestige_tier": "master",
            "prestige_rationale": "Priority biological illustration creator.",
            "applies_to_anchor_types": ["biological"],
            "status": "active",
        },
        {
            "id": _MORAN_PRESTIGE_ID,
            "registry_version": "1.0.0",
            "creator_authority_id": _MORAN_AUTHORITY_ID,
            "prestige_score": 1.0,
            "prestige_tier": "master",
            "prestige_rationale": "Yellowstone cultural and geographic creator.",
            "applies_to_anchor_types": ["geographic", "cultural"],
            "status": "active",
        },
        {
            "id": _JACKSON_PRESTIGE_ID,
            "registry_version": "1.0.0",
            "creator_authority_id": _JACKSON_AUTHORITY_ID,
            "prestige_score": 0.9,
            "prestige_tier": "major",
            "prestige_rationale": "Yellowstone expedition photography creator.",
            "applies_to_anchor_types": ["geographic", "cultural"],
            "status": "active",
        },
    ]


def _iconic_rows() -> list[dict]:
    return [
        {
            "id": _BISON_ICONIC_ID,
            "registry_version": "1.0.0",
            "place_key": "yellowstone",
            "taxon_key": "bison-bison",
            "scientific_name": "Bison bison",
            "iconic_score": 1.0,
            "status": "active",
        }
    ]


def _resolve(opportunity: dict):
    return resolve_asset_intelligence(
        opportunity,
        authority_rows=_authority_rows(),
        alias_rows=_alias_rows(),
        prestige_rows=_prestige_rows(),
        iconic_taxa_rows=_iconic_rows(),
    )


def _score_with_asset_intelligence(opportunity: dict, overrides: dict | None = None):
    inputs = _base_inputs()
    inputs.update(
        {
            "illustrator_prestige": 0.0,
            "taxon_place_iconic": 0.0,
            "place_relevance_score": 0.88,
            "place_tier_score": 0.90,
            "color_score": 0.85,
        }
    )
    if overrides:
        inputs.update(overrides)
    resolution = _resolve(opportunity)
    enriched = apply_asset_intelligence_to_score_inputs(inputs, resolution)
    return compute_scores(_policy(), enriched, opportunity_id=str(uuid4())), enriched, resolution


def test_migrations_32_35_exist_and_define_phase_1_runtime() -> None:
    for migration in (MIGRATION_32, MIGRATION_33, MIGRATION_34, MIGRATION_35):
        assert migration.exists()

    assert "ADD COLUMN IF NOT EXISTS anchor_type" in MIGRATION_32.read_text()
    migration_33 = MIGRATION_33.read_text()
    assert "CREATE TABLE IF NOT EXISTS creator_authority_registry" in migration_33
    assert "CREATE TABLE IF NOT EXISTS creator_prestige_registry" in migration_33
    assert "CREATE TABLE IF NOT EXISTS asset_intelligence_audit_log" in migration_33
    assert "CREATE OR REPLACE RULE asset_intelligence_audit_log_no_update" in migration_33
    migration_34 = MIGRATION_34.read_text()
    assert "CREATE TABLE IF NOT EXISTS place_iconic_taxa_registry" in migration_34
    for place in ("yellowstone", "yosemite", "grand-canyon", "everglades", "galapagos"):
        assert f"'{place}'" in migration_34
    migration_35 = MIGRATION_35.read_text()
    assert "CREATE TABLE IF NOT EXISTS asset_intelligence_registry_activation" in migration_35
    assert "CREATE OR REPLACE FUNCTION request_asset_intelligence_recompute" in migration_35


def test_biological_asset_scoring() -> None:
    result, inputs, resolution = _score_with_asset_intelligence(
        {
            "source": "bhl",
            "source_record_id": "bhl:audubon",
            "anchor_type": "biological",
            "illustrator": "John James Audubon",
            "taxon_name": "Bison bison",
            "taxon_key": "bison-bison",
            "place_key": "yellowstone",
        }
    )

    assert inputs["anchor_type"] == "biological"
    assert inputs["illustrator_prestige"] == 1.0
    assert inputs["taxon_place_iconic"] == 1.0
    assert resolution.creator_prestige.prestige_tier == "master"
    assert result.score_outputs["commerce_tier"] == "tier_1"
    assert replay_score(_policy(), result.score_inputs, result.score_outputs)


def test_geographic_asset_scoring() -> None:
    result, inputs, resolution = _score_with_asset_intelligence(
        {
            "source": "loc",
            "source_record_id": "loc:map:yellowstone",
            "anchor_type": "geographic",
            "creator": "Thomas Moran",
            "place_key": "yellowstone",
        },
        {"identification_confidence": 0.75, "taxon_commercial_tier_score": 0.2},
    )

    assert inputs["anchor_type"] == "geographic"
    assert inputs["illustrator_prestige"] == 1.0
    assert inputs["requires_curator_review"] is True
    assert resolution.creator_authority.canonical_creator_key == "thomas-moran"
    assert result.score_outputs["commerce_tier"] != "blocked"
    assert replay_score(_policy(), result.score_inputs, result.score_outputs)


def test_cultural_asset_scoring() -> None:
    result, inputs, resolution = _score_with_asset_intelligence(
        {
            "source": "loc",
            "source_record_id": "loc:poster:yellowstone",
            "anchor_type": "cultural",
            "creator": "William Henry Jackson",
            "place_key": "yellowstone",
        },
        {
            "image_quality_score": 0.82,
            "composition_fit": 0.84,
            "taxon_commercial_tier_score": 0.15,
        },
    )

    assert inputs["anchor_type"] == "cultural"
    assert inputs["illustrator_prestige"] == 0.9
    assert resolution.creator_prestige.prestige_tier == "major"
    assert result.score_outputs["commerce_tier"] != "blocked"
    assert replay_score(_policy(), result.score_inputs, result.score_outputs)


def test_mixed_asset_scoring() -> None:
    result, inputs, resolution = _score_with_asset_intelligence(
        {
            "source": "loc",
            "source_record_id": "loc:mixed:yellowstone-bison",
            "anchor_type": "cultural",
            "creator": "Thomas Moran",
            "taxon_name": "Bison bison",
            "taxon_key": "bison-bison",
            "place_key": "yellowstone",
        }
    )

    assert inputs["anchor_type"] == "cultural"
    assert inputs["illustrator_prestige"] == 1.0
    assert inputs["taxon_place_iconic"] == 1.0
    assert resolution.place_iconic_taxa.registry_id == str(_BISON_ICONIC_ID)
    assert result.score_outputs["commerce_tier"] == "tier_1"
    assert replay_score(_policy(), result.score_inputs, result.score_outputs)


def test_creator_prestige_lookup() -> None:
    authority = resolve_creator_authority("John James Audubon", _authority_rows(), _alias_rows())
    prestige = resolve_creator_prestige(authority, "biological", _prestige_rows())

    assert authority.canonical_creator_key == "john-james-audubon"
    assert prestige.registry_id == str(_AUDUBON_PRESTIGE_ID)
    assert prestige.prestige_score == 1.0
    assert prestige.prestige_tier == "master"


def test_creator_authority_resolution() -> None:
    authority = resolve_creator_authority("Plate after Audubon", _authority_rows(), _alias_rows())

    assert authority.registry_id == str(_AUDUBON_AUTHORITY_ID)
    assert authority.registry_version == "1.0.0"
    assert authority.display_name == "John James Audubon"
    assert authority.authority_confidence == 0.98


def test_place_iconic_taxa_lookup() -> None:
    iconic = resolve_place_iconic_taxa(
        place_key="yellowstone",
        taxon_name="Bison bison",
        taxon_key=None,
        registry_rows=_iconic_rows(),
    )

    assert iconic.registry_id == str(_BISON_ICONIC_ID)
    assert iconic.registry_version == "1.0.0"
    assert iconic.iconic_score == 1.0


def test_recompute_after_activation() -> None:
    base_inputs = _base_inputs()
    base_inputs.update(
        {
            "illustrator_prestige": 0.0,
            "taxon_place_iconic": 0.0,
            "place_relevance_score": 0.70,
        }
    )
    before = compute_scores(_policy(), deepcopy(base_inputs), opportunity_id=str(uuid4()))
    resolution = _resolve(
        {
            "source": "bhl",
            "source_record_id": "bhl:activation",
            "anchor_type": "biological",
            "illustrator": "Audubon",
            "taxon_key": "bison-bison",
            "place_key": "yellowstone",
        }
    )

    recomputed_inputs = recompute_after_activation(base_inputs, resolution)
    after = compute_scores(_policy(), recomputed_inputs, opportunity_id=str(uuid4()))

    assert (
        recomputed_inputs["asset_intelligence"]["registry_version_set"][
            "creator_prestige_registry"
        ]
        == "1.0.0"
    )
    assert (
        after.score_outputs["commerce_opportunity_score"]
        > before.score_outputs["commerce_opportunity_score"]
    )
    assert replay_score(_policy(), after.score_inputs, after.score_outputs)
