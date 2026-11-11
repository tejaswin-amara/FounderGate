import os
import sys
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.llm.adapters import GeminiAdapter, GroqAdapter, MistralAdapter, SandboxAdapter
from src.llm.exceptions import (
    AuthenticationError,
    RateLimitError,
)


@pytest.fixture
def gemini():
    return GeminiAdapter(api_key="fake-key")

@pytest.fixture
def mistral():
    return MistralAdapter(api_key="fake-key")

@pytest.fixture
def groq():
    return GroqAdapter(api_key="fake-key")

@pytest.mark.asyncio
async def test_sandbox_adapter():
    adapter = SandboxAdapter()
    result, usage = await adapter.generate_structured("prompt", {})
    assert result["is_sandbox_fixture"] is True
    assert usage.total_tokens == 20

@pytest.mark.asyncio
async def test_gemini_success(gemini):
    with patch('src.llm.adapters.aiohttp.ClientSession.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": '{"result": "success"}'}]}}],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 20, "totalTokenCount": 30}
        }
        mock_post.return_value.__aenter__.return_value = mock_response

        result, usage = await gemini.generate_structured("prompt", {})

        assert result == {"result": "success"}
        assert usage.total_tokens == 30

@pytest.mark.asyncio
async def test_gemini_rate_limit(gemini):
    with patch('src.llm.adapters.aiohttp.ClientSession.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 429
        mock_post.return_value.__aenter__.return_value = mock_response

        with pytest.raises(RateLimitError):
            await gemini.generate_structured("prompt", {})

@pytest.mark.asyncio
async def test_gemini_auth_error():
    adapter = GeminiAdapter(api_key=None)
    with pytest.raises(AuthenticationError):
        await adapter.generate_structured("prompt", {})

@pytest.mark.asyncio
async def test_mistral_success(mistral):
    with patch('src.llm.adapters.aiohttp.ClientSession.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"result": "success"}'}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }
        mock_post.return_value.__aenter__.return_value = mock_response

        result, usage = await mistral.generate_structured("prompt", {})

        assert result == {"result": "success"}
        assert usage.total_tokens == 30

@pytest.mark.asyncio
async def test_groq_success(groq):
    with patch('src.llm.adapters.aiohttp.ClientSession.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"result": "success"}'}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }
        mock_post.return_value.__aenter__.return_value = mock_response

        result, usage = await groq.generate_structured("prompt", {})

        assert result == {"result": "success"}
        assert usage.total_tokens == 30
