"""OpenAI and Codex provider stubs."""

from .base import ProviderStub


class OpenAIProvider(ProviderStub):
    provider = "openai"
    model_name = "gpt-copy-stub"


class CodexProvider(ProviderStub):
    provider = "codex"
    model_name = "codex-policy-stub"
