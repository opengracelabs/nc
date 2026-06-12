"""Claude provider stub."""

from .base import ProviderStub


class ClaudeProvider(ProviderStub):
    provider = "claude"
    model_name = "claude-policy-stub"
