import logging
from typing import Any

from pydantic import BaseModel

from src.llm.adapters import (
    BaseProviderAdapter,
    GeminiAdapter,
    GroqAdapter,
    HuggingFaceAdapter,
    MistralAdapter,
    OllamaAdapter,
    OpenRouterAdapter,
    SandboxAdapter,
)
from src.llm.exceptions import (
    AuthenticationError,
    ProviderError,
    RateLimitError,
    TimeoutError,
)
from src.llm.telemetry import ProviderTelemetry, TelemetryContext

logger = logging.getLogger(__name__)

class LLMResponse(BaseModel):
    data: dict[str, Any]
    telemetry: ProviderTelemetry

class LLMRouter:
    def __init__(self, default_provider: str = "sandbox_zero_key"):
        self.default_provider = default_provider
        self.providers: dict[str, type[BaseProviderAdapter]] = {
            "sandbox_zero_key": SandboxAdapter,
            "gemini": GeminiAdapter,
            "mistral": MistralAdapter,
            "groq": GroqAdapter,
            "ollama": OllamaAdapter,
            "openrouter": OpenRouterAdapter,
            "huggingface": HuggingFaceAdapter
        }

    def _get_adapter_info(self, provider_name: str, api_key: str | None = None) -> tuple[BaseProviderAdapter, str]:
        adapter_cls = self.providers.get(provider_name)
        if not adapter_cls:
            logger.warning(f"Provider '{provider_name}' not found, falling back to sandbox_zero_key")
            return SandboxAdapter(), "sandbox_zero_key"
        return adapter_cls(api_key=api_key), provider_name

    async def generate_structured(self,
                                  prompt: str,
                                  schema: dict[str, Any],
                                  provider: str | None = None,
                                  api_key: str | None = None) -> LLMResponse:

        target_provider = provider or self.default_provider
        adapter, resolved_provider_name = self._get_adapter_info(target_provider, api_key)

        telemetry_ctx = TelemetryContext(provider_name=resolved_provider_name, model_name="default")

        try:
            data, token_usage = await adapter.generate_structured(prompt, schema)
            telemetry = telemetry_ctx.end(success=True, token_usage=token_usage)
            return LLMResponse(data=data, telemetry=telemetry)

        except (ProviderError, TimeoutError, AuthenticationError, RateLimitError) as e:
            logger.error(f"Error calling provider {resolved_provider_name}: {e}")
            telemetry_ctx.end(success=False, error_message=str(e))

            # Fallback to sandbox
            logger.info("Falling back to sandbox_zero_key")
            fallback_ctx = TelemetryContext(provider_name="sandbox_zero_key", model_name="default")
            fallback_adapter = SandboxAdapter()

            data, token_usage = await fallback_adapter.generate_structured(prompt, schema)
            telemetry = fallback_ctx.end(success=True, is_fallback=True, token_usage=token_usage)

            return LLMResponse(data=data, telemetry=telemetry)
