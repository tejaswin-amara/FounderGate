import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.llm.exceptions import (
    TimeoutError,
)
from src.llm.router import LLMRouter


@pytest.fixture
def router():
    return LLMRouter()

@pytest.mark.asyncio
async def test_sandbox_zero_key(router: LLMRouter):
    response = await router.generate_structured(
        prompt="Test",
        schema={"type": "object"},
        provider="sandbox_zero_key"
    )

    assert response.telemetry.success is True
    assert response.telemetry.provider_name == "sandbox_zero_key"
    assert response.telemetry.is_fallback is False
    assert response.data.get("is_sandbox_fixture") is True
    assert response.telemetry.token_usage is not None and response.telemetry.token_usage.total_tokens == 20

@pytest.mark.asyncio
async def test_fallback_on_missing_api_key(router: LLMRouter):
    response = await router.generate_structured(
        prompt="Test",
        schema={"type": "object"},
        provider="gemini",
        api_key=None
    )

    assert response.telemetry.success is True
    assert response.telemetry.provider_name == "sandbox_zero_key"
    assert response.telemetry.is_fallback is True
    assert response.data.get("is_sandbox_fixture") is True

@pytest.mark.asyncio
async def test_fallback_on_timeout(router: LLMRouter):
    with patch('src.llm.adapters.GeminiAdapter.generate_structured') as mock_generate:
        mock_generate.side_effect = TimeoutError("Simulated timeout")

        response = await router.generate_structured(
            prompt="Test",
            schema={"type": "object"},
            provider="gemini",
            api_key="fake-key"
        )

        assert response.telemetry.success is True
        assert response.telemetry.provider_name == "sandbox_zero_key"
        assert response.telemetry.is_fallback is True

@pytest.mark.asyncio
async def test_unknown_provider_fallback(router: LLMRouter):
    response = await router.generate_structured(
        prompt="Test",
        schema={"type": "object"},
        provider="nonexistent_provider"
    )

    assert response.telemetry.success is True
    assert response.telemetry.provider_name == "sandbox_zero_key"
