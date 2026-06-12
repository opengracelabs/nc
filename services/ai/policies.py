"""Task policies and provider routing for NC-AI-001."""

from __future__ import annotations

from dataclasses import dataclass


class PolicyError(ValueError):
    """Raised when a task policy is unknown or violated."""


@dataclass(frozen=True)
class AITaskPolicy:
    task_type: str
    provider_policy: str
    default_provider: str
    default_model: str
    human_review_required: bool
    grounding_required: bool
    publication_allowed_by_default: bool
    cite_sources_required: bool


TASK_POLICIES: dict[str, AITaskPolicy] = {
    "rights_governance": AITaskPolicy(
        task_type="rights_governance",
        provider_policy="claude_policy",
        default_provider="claude",
        default_model="claude-policy-stub",
        human_review_required=True,
        grounding_required=True,
        publication_allowed_by_default=False,
        cite_sources_required=True,
    ),
    "place_story": AITaskPolicy(
        task_type="place_story",
        provider_policy="narrative_policy",
        default_provider="gemini",
        default_model="gemini-narrative-stub",
        human_review_required=True,
        grounding_required=True,
        publication_allowed_by_default=False,
        cite_sources_required=True,
    ),
    "product_copy": AITaskPolicy(
        task_type="product_copy",
        provider_policy="narrative_policy",
        default_provider="openai",
        default_model="gpt-copy-stub",
        human_review_required=True,
        grounding_required=True,
        publication_allowed_by_default=False,
        cite_sources_required=True,
    ),
    "education_module": AITaskPolicy(
        task_type="education_module",
        provider_policy="narrative_policy",
        default_provider="gemini",
        default_model="gemini-narrative-stub",
        human_review_required=True,
        grounding_required=True,
        publication_allowed_by_default=False,
        cite_sources_required=True,
    ),
    "code_generation": AITaskPolicy(
        task_type="code_generation",
        provider_policy="codex_policy",
        default_provider="codex",
        default_model="codex-policy-stub",
        human_review_required=True,
        grounding_required=False,
        publication_allowed_by_default=False,
        cite_sources_required=False,
    ),
    "public_website_copy": AITaskPolicy(
        task_type="public_website_copy",
        provider_policy="narrative_policy",
        default_provider="openai",
        default_model="gpt-copy-stub",
        human_review_required=True,
        grounding_required=True,
        publication_allowed_by_default=False,
        cite_sources_required=True,
    ),
    "user_assistant": AITaskPolicy(
        task_type="user_assistant",
        provider_policy="assistant_policy",
        default_provider="openai",
        default_model="gpt-copy-stub",
        human_review_required=True,
        grounding_required=True,
        publication_allowed_by_default=False,
        cite_sources_required=True,
    ),
}


def route_task_policy(task_type: str) -> AITaskPolicy:
    try:
        return TASK_POLICIES[task_type]
    except KeyError as exc:
        raise PolicyError(f"Unknown AI task type: {task_type}") from exc


def route_decision(task_type: str) -> dict[str, object]:
    policy = route_task_policy(task_type)
    return {
        "task_type": policy.task_type,
        "selected_provider": policy.default_provider,
        "selected_model": policy.default_model,
        "execution_provider": "local",
        "provider_policy": policy.provider_policy,
        "human_review_required": policy.human_review_required,
        "grounding_required": policy.grounding_required,
        "publication_allowed": policy.publication_allowed_by_default,
        "reason": "Sprint 1 records policy route but executes deterministic local mock only.",
    }
