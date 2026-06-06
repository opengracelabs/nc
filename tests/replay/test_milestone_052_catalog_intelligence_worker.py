"""v0.5.2 Catalog Intelligence replay tests."""
from __future__ import annotations

import importlib.util
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from workers.catalog_intelligence_worker import WORKER_VERSION
from workers.catalog_intelligence_worker.catalog import build_catalog_candidate, build_catalog_variants
from workers.catalog_intelligence_worker.replay import verify_catalog_replay
from workers.catalog_intelligence_worker.store import claim_catalog_recommendations, write_catalog_candidate_and_variants
from workers.commerce_opportunity_worker.score import compute_scores

_PHASE3_SPEC = importlib.util.spec_from_file_location(
    "phase3_commerce_worker_fixtures",
    Path(__file__).with_name("test_milestone_050_commerce_opportunity_worker.py"),
)
assert _PHASE3_SPEC and _PHASE3_SPEC.loader
_PHASE3 = importlib.util.module_from_spec(_PHASE3_SPEC)
_PHASE3_SPEC.loader.exec_module(_PHASE3)
_benchmark_inputs = _PHASE3._benchmark_inputs
_policy = _PHASE3._policy

_CATALOG_POLICY_ID = UUID("50000000-0000-0000-0000-000000000001")


def _catalog_policy() -> dict:
    return {
        "id": _CATALOG_POLICY_ID,
        "version": "1.0.0",
        "catalog_rules": {
            "title_template": "{asset_title} - {product_family_label}",
            "description_template": "Internal catalog candidate generated from {source_title}.",
            "media_requirements_by_family": {
                "wall_art": {"min_width_px": 2000, "required_assets": ["source_image"]},
                "museum_print": {"min_width_px": 4000, "required_assets": ["source_image"]},
                "calendar": {"min_width_px": 2000, "required_assets": ["source_image"]},
            },
        },
        "variant_rules": {
            "wall_art": [
                {"variant_key": "standard_print_12x16", "product_type": "standard_print", "title_suffix": "12 x 16", "dimensions": {"width_in": 12, "height_in": 16}},
                {"variant_key": "standard_print_18x24", "product_type": "standard_print", "title_suffix": "18 x 24", "dimensions": {"width_in": 18, "height_in": 24}},
            ],
            "museum_print": [
                {"variant_key": "archival_print_16x20", "product_type": "archival_print", "title_suffix": "16 x 20", "dimensions": {"width_in": 16, "height_in": 20}},
                {"variant_key": "archival_print_24x36", "product_type": "archival_print", "title_suffix": "24 x 36", "dimensions": {"width_in": 24, "height_in": 36}},
            ],
            "calendar": [
                {"variant_key": "wall_calendar_annual", "product_type": "calendar", "title_suffix": "Annual Wall Calendar", "dimensions": {"width_in": 11, "height_in": 17}},
            ],
        },
        "pricing_rules": {
            "currency": "USD",
            "rounding": {"nearest_cents": 100, "minus_cents": 1},
            "profiles": {
                "standard_print": {"base_price_cents": 3200, "margin_floor_bps": 5500, "price_band": "standard"},
                "archival_print": {"base_price_cents": 8500, "margin_floor_bps": 6500, "price_band": "premium"},
                "calendar": {"base_price_cents": 2800, "margin_floor_bps": 5000, "price_band": "standard"},
            },
        },
        "eligibility_gates": {
            "requires_product_recommendation_status": "curator_approved",
            "requires_rights_snapshot": True,
        },
    }


def _commerce_record(name: str) -> dict:
    result = compute_scores(
        _policy(),
        _benchmark_inputs(name),
        opportunity_id=str(uuid4()),
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )
    record = dict(result.commerce_record)
    record.update(
        {
            "id": uuid4(),
            "opportunity_id": uuid4(),
            "policy_version_id": _policy()["id"],
            "curator_decision": "approved",
            "policy_stale": False,
        }
    )
    return record


def _recommendation(name: str, family: str = "wall_art") -> dict:
    return {
        "id": uuid4(),
        "opportunity_id": uuid4(),
        "commerce_opportunity_id": uuid4(),
        "policy_version_id": _policy()["id"],
        "recommended_product_family": family,
        "recommended_product_types": {"types": ["standard_print" if family == "wall_art" else "archival_print"]},
        "recommended_providers": {},
        "recommendation_confidence": 0.95,
        "recommendation_basis": {"fixture": name},
        "status": "curator_approved",
        "title": f"{name.title()} Survey Plate",
    }


def _expected_generation(policy: dict, recommendation: dict, commerce: dict) -> dict:
    candidate = build_catalog_candidate(policy, recommendation, commerce)
    variants = build_catalog_variants(policy, candidate, commerce)
    return {
        "candidate": candidate.__dict__,
        "variants": [
            {key: value for key, value in variant.__dict__.items() if key != "pricing_profile"}
            for variant in variants
        ],
    }


def test_moran_creates_catalog_candidate() -> None:
    candidate = build_catalog_candidate(_catalog_policy(), _recommendation("moran"), _commerce_record("moran"))

    assert candidate.product_family == "wall_art"
    assert "Moran Survey Plate" in candidate.catalog_title
    assert candidate.rights_snapshot["hard_gate_status"] == "passed"


def test_hayden_creates_catalog_candidate() -> None:
    candidate = build_catalog_candidate(_catalog_policy(), _recommendation("hayden"), _commerce_record("hayden"))

    assert candidate.product_family == "wall_art"
    assert candidate.catalog_status == "draft"
    assert candidate.catalog_basis["catalog_policy_version"] == "1.0.0"


def test_jackson_creates_catalog_candidate() -> None:
    candidate = build_catalog_candidate(_catalog_policy(), _recommendation("jackson", "calendar"), _commerce_record("jackson"))

    assert candidate.product_family == "calendar"
    assert candidate.media_requirements["min_width_px"] == 2000


def test_variant_generation_deterministic() -> None:
    policy = _catalog_policy()
    recommendation = _recommendation("moran")
    commerce = _commerce_record("moran")
    candidate = build_catalog_candidate(policy, recommendation, commerce)

    first = build_catalog_variants(policy, candidate, commerce)
    second = build_catalog_variants(deepcopy(policy), deepcopy(candidate), deepcopy(commerce))

    assert first == second
    assert [variant.variant_key for variant in first] == ["standard_print_12x16", "standard_print_18x24"]


def test_pricing_profile_deterministic() -> None:
    policy = _catalog_policy()
    recommendation = _recommendation("hayden")
    commerce = _commerce_record("hayden")
    candidate = build_catalog_candidate(policy, recommendation, commerce)

    first = build_catalog_variants(policy, candidate, commerce)[0]
    second = build_catalog_variants(deepcopy(policy), deepcopy(candidate), deepcopy(commerce))[0]

    assert first.pricing_profile == second.pricing_profile
    assert first.price_snapshot == second.price_snapshot
    assert first.price_snapshot["currency"] == "USD"


def test_replay_worker_reproduces_identical_variants() -> None:
    policy = _catalog_policy()
    recommendation = _recommendation("moran")
    commerce = _commerce_record("moran")
    expected = _expected_generation(policy, recommendation, commerce)

    result = verify_catalog_replay(policy, recommendation, commerce, expected)

    assert result.verified is True
    assert result.expected_event_type == "catalog_replay_verified"


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeCatalogConn:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.execute_queries: list[tuple[str, tuple]] = []
        self.fetchrow_queries: list[tuple[str, tuple]] = []

    def transaction(self):
        self.calls.append("transaction")
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append((query, args))
        if "FROM catalog_audit_log" in query:
            return None
        if "INSERT INTO catalog_candidates" in query:
            self.calls.append("candidate")
            return {"id": UUID("50000000-0000-0000-0000-000000000099")}
        if "INSERT INTO catalog_pricing_profiles" in query:
            self.calls.append("pricing")
            return {"id": UUID("50000000-0000-0000-0000-000000000098")}
        if "INSERT INTO catalog_variants" in query:
            self.calls.append("variant")
            return {"id": UUID("50000000-0000-0000-0000-000000000097")}
        return None

    async def execute(self, query: str, *args):
        self.execute_queries.append((query, args))
        if "INSERT INTO catalog_audit_log" in query:
            self.calls.append("audit")
        return "OK"


async def test_audit_chain_works_and_precedes_catalog_writes() -> None:
    conn = FakeCatalogConn()

    await write_catalog_candidate_and_variants(
        conn,
        _catalog_policy(),
        _recommendation("moran"),
        _commerce_record("moran"),
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )

    assert conn.calls.index("audit") < conn.calls.index("candidate")
    audit_times = [args[5] for query, args in conn.execute_queries if "INSERT INTO catalog_audit_log" in query]
    assert audit_times == sorted(audit_times)
    assert len(set(audit_times)) == len(audit_times)


class FakeClaimConn:
    def __init__(self) -> None:
        self.query = ""

    async def fetch(self, query: str, *args):
        self.query = query
        return []


async def test_claim_query_uses_catalog_governance_gates() -> None:
    conn = FakeClaimConn()

    await claim_catalog_recommendations(conn, 10)

    assert "pr.status = 'curator_approved'" in conn.query
    assert "co.curator_decision = 'approved'" in conn.query
    assert "co.hard_gate_status = 'passed'" in conn.query
    assert "co.policy_stale = FALSE" in conn.query
    assert "co.commerce_tier <> 'blocked'" in conn.query
    assert "catalog_candidates" in conn.query
