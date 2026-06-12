"""Gemini provider stub."""

from .base import ProviderStub


class GeminiProvider(ProviderStub):
    provider = "gemini"
    model_name = "gemini-narrative-stub"
