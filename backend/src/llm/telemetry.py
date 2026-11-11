import time

from pydantic import BaseModel


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ProviderTelemetry(BaseModel):
    provider_name: str
    model_name: str
    latency_ms: int
    success: bool
    is_fallback: bool = False
    token_usage: TokenUsage | None = None
    error_message: str | None = None

class TelemetryContext:
    def __init__(self, provider_name: str, model_name: str):
        self.provider_name = provider_name
        self.model_name = model_name
        self.start_time = time.perf_counter()

    def end(self, success: bool, is_fallback: bool = False,
            token_usage: TokenUsage | None = None,
            error_message: str | None = None) -> ProviderTelemetry:
        latency_ms = int((time.perf_counter() - self.start_time) * 1000)
        return ProviderTelemetry(
            provider_name=self.provider_name,
            model_name=self.model_name,
            latency_ms=latency_ms,
            success=success,
            is_fallback=is_fallback,
            token_usage=token_usage,
            error_message=error_message
        )
