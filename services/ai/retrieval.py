"""Deterministic retrieval context assembly."""

from __future__ import annotations

from typing import Any

from .grounding import GroundingSource


def assemble_context(
    sources: list[GroundingSource],
    *,
    task_type: str | None = None,
    inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "task_type": task_type,
        "inputs": inputs or {},
        "source_count": len(sources),
        "source_references": [source.to_reference() for source in sources],
        "source_evidence": [
            {
                **source.to_reference(),
                "evidence": source.evidence,
                "attribution": source.attribution,
            }
            for source in sources
        ],
        "evidence_authority": "Graph and source evidence are authoritative.",
    }
