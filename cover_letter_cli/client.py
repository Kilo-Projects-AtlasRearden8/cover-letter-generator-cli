"""Client for the OpenAI-compatible chat completions endpoint."""

from __future__ import annotations

import httpx

DEFAULT_TIMEOUT = 60.0


class LLMError(Exception):
    """Raised when the LLM endpoint cannot be used."""


class LLMClient:
    def __init__(self, endpoint, model, transport=None, timeout=DEFAULT_TIMEOUT):
        self.endpoint = endpoint
        self.model = model
        self._client = httpx.Client(transport=transport, timeout=timeout)

    def generate(self, messages):
        """Send a chat completion request and return the assistant's text."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        try:
            response = self._client.post(self.endpoint, json=payload)
        except httpx.RequestError as exc:
            raise LLMError(f"Could not reach {self.endpoint}: {exc}") from exc

        if response.status_code >= 400:
            raise LLMError(
                f"Endpoint returned HTTP {response.status_code}: {response.text[:200]}"
            )

        try:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError) as exc:
            raise LLMError(f"Unexpected response format: {exc}") from exc

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
