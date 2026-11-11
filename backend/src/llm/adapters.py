import builtins
import json
import logging
from typing import Any

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.llm.exceptions import (
    AuthenticationError,
    ProviderError,
    RateLimitError,
    TimeoutError,
)
from src.llm.telemetry import TokenUsage

logger = logging.getLogger(__name__)

class BaseProviderAdapter:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        raise NotImplementedError()

class SandboxAdapter(BaseProviderAdapter):
    """Deterministic zero-key sandbox for reproducible results without API calls."""

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)

    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        # Return deterministic fixture data, conforming to EvidenceClaim fields if needed,
        # but here we just return a simple fixture indicating it's a sandbox response.
        return {
            "is_sandbox_fixture": True,
            "message": "This is deterministic output from the zero-key sandbox.",
            "data": {}
        }, TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20)


class GeminiAdapter(BaseProviderAdapter):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((TimeoutError, RateLimitError)), reraise=True
    )
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        if not self.api_key:
            raise AuthenticationError("Gemini API key is required")

        url = f"{self.base_url}?key={self.api_key}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 429:
                        raise RateLimitError("Gemini rate limit exceeded")
                    if response.status in (401, 403):
                        raise AuthenticationError("Invalid Gemini API key")
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"Gemini API error: {response.status} - {error_text}")

                    data = await response.json()

                    try:
                        text_response = data['candidates'][0]['content']['parts'][0]['text']
                        if text_response.startswith('```json'):
                            text_response = text_response[7:-3]
                        elif text_response.startswith('```'):
                            text_response = text_response[3:-3]
                        result = json.loads(text_response)
                    except (KeyError, IndexError, json.JSONDecodeError) as e:
                        raise ProviderError(f"Failed to parse Gemini response as JSON: {e}. Raw: {data}")

                    usage = data.get('usageMetadata', {})
                    token_usage = TokenUsage(
                        prompt_tokens=usage.get('promptTokenCount', 0),
                        completion_tokens=usage.get('candidatesTokenCount', 0),
                        total_tokens=usage.get('totalTokenCount', 0)
                    )

                    return result, token_usage

            except builtins.TimeoutError:
                raise TimeoutError("Gemini request timed out")
            except aiohttp.ClientError as e:
                raise ProviderError(f"Network error calling Gemini: {e}")

class MistralAdapter(BaseProviderAdapter):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.base_url = "https://api.mistral.ai/v1/chat/completions"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((TimeoutError, RateLimitError)), reraise=True
    )
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        if not self.api_key:
            raise AuthenticationError("Mistral API key is required")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 429:
                        raise RateLimitError("Mistral rate limit exceeded")
                    if response.status in (401, 403):
                        raise AuthenticationError("Invalid Mistral API key")
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"Mistral API error: {response.status} - {error_text}")

                    data = await response.json()

                    try:
                        text_response = data['choices'][0]['message']['content']
                        result = json.loads(text_response)
                    except (KeyError, IndexError, json.JSONDecodeError) as e:
                        raise ProviderError(f"Failed to parse Mistral response as JSON: {e}")

                    usage = data.get('usage', {})
                    token_usage = TokenUsage(
                        prompt_tokens=usage.get('prompt_tokens', 0),
                        completion_tokens=usage.get('completion_tokens', 0),
                        total_tokens=usage.get('total_tokens', 0)
                    )

                    return result, token_usage

            except builtins.TimeoutError:
                raise TimeoutError("Mistral request timed out")
            except aiohttp.ClientError as e:
                raise ProviderError(f"Network error calling Mistral: {e}")

class GroqAdapter(BaseProviderAdapter):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((TimeoutError, RateLimitError)), reraise=True
    )
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        if not self.api_key:
            raise AuthenticationError("Groq API key is required")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 429:
                        raise RateLimitError("Groq rate limit exceeded")
                    if response.status in (401, 403):
                        raise AuthenticationError("Invalid Groq API key")
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"Groq API error: {response.status} - {error_text}")

                    data = await response.json()

                    try:
                        text_response = data['choices'][0]['message']['content']
                        result = json.loads(text_response)
                    except (KeyError, IndexError, json.JSONDecodeError) as e:
                        raise ProviderError(f"Failed to parse Groq response as JSON: {e}")

                    usage = data.get('usage', {})
                    token_usage = TokenUsage(
                        prompt_tokens=usage.get('prompt_tokens', 0),
                        completion_tokens=usage.get('completion_tokens', 0),
                        total_tokens=usage.get('total_tokens', 0)
                    )

                    return result, token_usage

            except builtins.TimeoutError:
                raise TimeoutError("Groq request timed out")
            except aiohttp.ClientError as e:
                raise ProviderError(f"Network error calling Groq: {e}")

class OllamaAdapter(BaseProviderAdapter):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.base_url = "http://localhost:11434/api/generate"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((TimeoutError, RateLimitError)), reraise=True
    )
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "format": "json",
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"Ollama API error: {response.status} - {error_text}")

                    data = await response.json()

                    try:
                        text_response = data['response']
                        result = json.loads(text_response)
                    except (KeyError, json.JSONDecodeError) as e:
                        raise ProviderError(f"Failed to parse Ollama response as JSON: {e}")

                    token_usage = TokenUsage(
                        prompt_tokens=data.get('prompt_eval_count', 0),
                        completion_tokens=data.get('eval_count', 0),
                        total_tokens=data.get('prompt_eval_count', 0) + data.get('eval_count', 0)
                    )

                    return result, token_usage

            except builtins.TimeoutError:
                raise TimeoutError("Ollama request timed out")
            except aiohttp.ClientError as e:
                raise ProviderError(f"Network error calling Ollama: {e}")

class OpenRouterAdapter(BaseProviderAdapter):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((TimeoutError, RateLimitError)), reraise=True
    )
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        if not self.api_key:
            raise AuthenticationError("OpenRouter API key is required")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": prompt}],
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 429:
                        raise RateLimitError("OpenRouter rate limit exceeded")
                    if response.status in (401, 403):
                        raise AuthenticationError("Invalid OpenRouter API key")
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"OpenRouter API error: {response.status} - {error_text}")

                    data = await response.json()

                    try:
                        text_response = data['choices'][0]['message']['content']
                        # Attempt to parse as JSON, even if not explicitly forced
                        if text_response.startswith('```json'):
                            text_response = text_response[7:-3]
                        result = json.loads(text_response)
                    except (KeyError, IndexError, json.JSONDecodeError) as e:
                        raise ProviderError(f"Failed to parse OpenRouter response as JSON: {e}")

                    usage = data.get('usage', {})
                    token_usage = TokenUsage(
                        prompt_tokens=usage.get('prompt_tokens', 0),
                        completion_tokens=usage.get('completion_tokens', 0),
                        total_tokens=usage.get('total_tokens', 0)
                    )

                    return result, token_usage

            except builtins.TimeoutError:
                raise TimeoutError("OpenRouter request timed out")
            except aiohttp.ClientError as e:
                raise ProviderError(f"Network error calling OpenRouter: {e}")

class HuggingFaceAdapter(BaseProviderAdapter):
    def __init__(self, api_key: str | None = None):
        super().__init__(api_key)
        self.base_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((TimeoutError, RateLimitError)), reraise=True
    )
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> tuple[dict[str, Any], TokenUsage]:
        if not self.api_key:
            raise AuthenticationError("Hugging Face API key is required")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "return_full_text": False
            }
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 429:
                        raise RateLimitError("Hugging Face rate limit exceeded")
                    if response.status in (401, 403):
                        raise AuthenticationError("Invalid Hugging Face API key")
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"Hugging Face API error: {response.status} - {error_text}")

                    data = await response.json()

                    try:
                        if isinstance(data, list):
                            text_response = data[0].get('generated_text', '')
                        else:
                            text_response = data.get('generated_text', '')

                        if text_response.startswith('```json'):
                            text_response = text_response[7:-3]
                        result = json.loads(text_response)
                    except (KeyError, IndexError, json.JSONDecodeError, AttributeError) as e:
                        raise ProviderError(f"Failed to parse Hugging Face response as JSON: {e}")

                    # Hugging Face Inference API often doesn't return detailed token usage
                    token_usage = TokenUsage(
                        prompt_tokens=0,
                        completion_tokens=0,
                        total_tokens=0
                    )

                    return result, token_usage

            except builtins.TimeoutError:
                raise TimeoutError("Hugging Face request timed out")
            except aiohttp.ClientError as e:
                raise ProviderError(f"Network error calling Hugging Face: {e}")
