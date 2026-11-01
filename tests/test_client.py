import json

import httpx
import pytest

from cover_letter_cli.client import LLMClient, LLMError


def _capture_handler(payload_capture):
    def handler(request):
        body = json.loads(request.content)
        payload_capture.append(body)
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"role": "assistant", "content": "Dear Hiring Manager,\n\nSincerely,\nDylan"}}
                ]
            },
        )

    return handler


def test_generate_posts_expected_payload():
    captured = []
    transport = httpx.MockTransport(_capture_handler(captured))
    client = LLMClient("http://localhost:11434/v1/chat/completions", "llama3", transport=transport)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a letter."},
    ]
    result = client.generate(messages)

    assert result == "Dear Hiring Manager,\n\nSincerely,\nDylan"
    assert len(captured) == 1
    assert captured[0]["model"] == "llama3"
    assert captured[0]["messages"] == messages
    assert captured[0]["stream"] is False


def test_generate_request_error():
    def failing_handler(request):
        raise httpx.ConnectError("connection refused")

    transport = httpx.MockTransport(failing_handler)
    client = LLMClient("http://localhost:11434/v1/chat/completions", "llama3", transport=transport)

    with pytest.raises(LLMError, match="Could not reach"):
        client.generate([{"role": "user", "content": "hi"}])


def test_generate_bad_status():
    def error_handler(request):
        return httpx.Response(500, text="internal error")

    transport = httpx.MockTransport(error_handler)
    client = LLMClient("http://localhost:11434/v1/chat/completions", "llama3", transport=transport)

    with pytest.raises(LLMError, match="HTTP 500"):
        client.generate([{"role": "user", "content": "hi"}])


def test_generate_bad_shape():
    def weird_handler(request):
        return httpx.Response(200, json={"not": "choices"})

    transport = httpx.MockTransport(weird_handler)
    client = LLMClient("http://localhost:11434/v1/chat/completions", "llama3", transport=transport)

    with pytest.raises(LLMError, match="Unexpected response format"):
        client.generate([{"role": "user", "content": "hi"}])


def test_client_context_manager_closes():
    captured = []
    transport = httpx.MockTransport(_capture_handler(captured))
    with LLMClient("http://localhost:11434/v1/chat/completions", "llama3", transport=transport) as client:
        client.generate([{"role": "user", "content": "hi"}])
    assert client._client.is_closed
