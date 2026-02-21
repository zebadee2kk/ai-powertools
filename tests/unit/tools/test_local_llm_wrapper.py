import json

import httpx
import pytest

from powertools.tools.local_llm_wrapper import (
    LocalLLMRequestWrapper,
    WrappedLLMRequest,
)


def test_build_and_unwrap_transfer_payload_round_trip():
    wrapper = LocalLLMRequestWrapper(base_url="http://localhost:11434", model="llama3")
    request = WrappedLLMRequest(
        task="summarize",
        user_prompt="Summarize the notes",
        system_prompt="You are concise.",
        rules=["Keep to 3 bullets", "No markdown tables"],
        context={"notes": ["one", "two"]},
        metadata={"source": "vscode"},
    )

    payload = wrapper.build_transfer_payload(request)
    parsed = LocalLLMRequestWrapper.unwrap_transfer_payload(payload)

    assert parsed["schema"] == "powertools.local_llm_wrapper.v1"
    assert parsed["target"]["model"] == "llama3"
    assert parsed["request"]["task"] == "summarize"
    assert parsed["request"]["metadata"]["source"] == "vscode"


def test_unwrap_transfer_payload_from_markdown_json_block():
    wrapped = """Here you go:\n```json
    {"schema": "powertools.local_llm_wrapper.v1", "request": {"task": "test"}}
    ```"""
    parsed = LocalLLMRequestWrapper.unwrap_transfer_payload(wrapped)
    assert parsed["request"]["task"] == "test"


@pytest.mark.asyncio
async def test_execute_calls_local_openai_compatible_endpoint():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["json"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            status_code=200,
            json={
                "model": "llama3",
                "choices": [{"message": {"content": "done"}}],
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        wrapper = LocalLLMRequestWrapper(base_url="http://localhost:11434", model="llama3")
        response = await wrapper.execute(
            WrappedLLMRequest(task="lint", user_prompt="Check code quality"),
            client=client,
        )

    assert captured["url"] == "http://localhost:11434/v1/chat/completions"
    assert captured["json"]["model"] == "llama3"
    assert captured["json"]["messages"][0]["role"] == "user"
    assert "Task: lint" in captured["json"]["messages"][0]["content"]
    assert response.content == "done"
