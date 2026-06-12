"""Deterministic prompt templates."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .grounding import GroundingSource


@dataclass(frozen=True)
class PromptTemplate:
    template_key: str
    template_version: str
    task_type: str
    body: str

    @property
    def template_sha256(self) -> str:
        return stable_hash(
            {
                "template_key": self.template_key,
                "template_version": self.template_version,
                "task_type": self.task_type,
                "body": self.body,
            }
        )

    def render(self, inputs: dict[str, Any], sources: list[GroundingSource]) -> str:
        sorted_sources = sorted(
            sources,
            key=lambda item: (item.source_type, item.source_record_id),
        )
        source_lines = [
            f"- {source.source_type}:{source.source_record_id} | {source.title}"
            for source in sorted_sources
        ]
        return "\n".join(
            [
                self.body,
                "",
                "INPUT:",
                json.dumps(inputs, sort_keys=True, separators=(",", ":"), default=str),
                "",
                "GROUNDING SOURCES:",
                "\n".join(source_lines) if source_lines else "- none",
                "",
                "RULES:",
                "- Cite source records.",
                "- Do not invent rights status.",
                "- Do not publish without human review.",
            ]
        )


DEFAULT_TEMPLATES: dict[str, PromptTemplate] = {
    task_type: PromptTemplate(
        template_key=f"{task_type}_v1",
        template_version="1",
        task_type=task_type,
        body=f"Generate advisory {task_type.replace('_', ' ')} content for Nature & Culture.",
    )
    for task_type in (
        "rights_governance",
        "place_story",
        "product_copy",
        "education_module",
        "code_generation",
        "public_website_copy",
        "user_assistant",
    )
}


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def get_prompt_template(task_type: str) -> PromptTemplate:
    return DEFAULT_TEMPLATES[task_type]
