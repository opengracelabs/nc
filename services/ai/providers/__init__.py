"""Provider registry stubs for NC-AI-001."""

from .claude import ClaudeProvider
from .deepseek import DeepSeekProvider
from .gemini import GeminiProvider
from .gemma import GemmaProvider
from .local import DeterministicMockProvider
from .mistral import MistralProvider
from .openai import CodexProvider, OpenAIProvider
from .qwen import QwenProvider

PROVIDER_CLASSES = {
    "claude": ClaudeProvider,
    "gemini": GeminiProvider,
    "openai": OpenAIProvider,
    "codex": CodexProvider,
    "qwen": QwenProvider,
    "deepseek": DeepSeekProvider,
    "mistral": MistralProvider,
    "gemma": GemmaProvider,
    "local": DeterministicMockProvider,
}


def get_provider_class(provider: str):
    return PROVIDER_CLASSES[provider]
