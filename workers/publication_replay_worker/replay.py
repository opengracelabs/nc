"""Replay helpers for Publication Intelligence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from workers.publication_worker.publication import replay_publication_candidate


@dataclass(frozen=True)
class PublicationReplayResult:
    verified: bool
    expected_event_type: str


def verify_publication_replay(policy: dict[str, Any], channel_profile: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any], commerce: dict[str, Any], expected: dict[str, Any]) -> PublicationReplayResult:
    verified = replay_publication_candidate(policy, channel_profile, catalog_candidate, catalog_variant, commerce, expected)
    return PublicationReplayResult(
        verified=verified,
        expected_event_type="publication_replay_verified" if verified else "publication_replay_failed",
    )
