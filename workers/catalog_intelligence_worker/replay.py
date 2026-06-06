"""Replay helpers for Catalog Intelligence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .catalog import replay_catalog_generation


@dataclass(frozen=True)
class CatalogReplayResult:
    verified: bool
    expected_event_type: str


def verify_catalog_replay(policy: dict[str, Any], recommendation: dict[str, Any], commerce: dict[str, Any], expected: dict[str, Any]) -> CatalogReplayResult:
    verified = replay_catalog_generation(policy, recommendation, commerce, expected)
    return CatalogReplayResult(
        verified=verified,
        expected_event_type="catalog_replay_verified" if verified else "catalog_replay_failed",
    )
