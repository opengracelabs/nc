"""Provider base classes."""

from __future__ import annotations

from typing import Any


class ProviderUnavailableError(RuntimeError):
    """Raised by Sprint 1 provider stubs if generation is attempted."""


class ProviderStub:
    provider = "stub"
    model_name = "stub"
    external_calls_allowed = False

    def generate(self, prompt: str, context: dict[str, Any]) -> dict[str, Any]:
        raise ProviderUnavailableError(
            f"{self.provider} is a Sprint 1 registry stub and cannot call external APIs"
        )
