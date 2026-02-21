from __future__ import annotations

from typing import List, Optional

import httpx

from .models import ModelEntry


def _get_ollama_models(base_url: str = "http://localhost:11434") -> List[ModelEntry]:
    """Discover models available from a local Ollama instance via its REST API."""
    try:
        with httpx.Client(timeout=3.0) as client:
            response = client.get(f"{base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
        return [
            ModelEntry(provider="ollama", model=m["name"], provider_type="local")
            for m in data.get("models", [])
        ]
    except Exception:
        return []


def _get_openai_compatible_models(
    endpoint: str, provider_name: str, api_key: Optional[str] = None
) -> List[ModelEntry]:
    """Discover models from any OpenAI-compatible /v1/models endpoint (e.g. LM Studio, vLLM)."""
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        with httpx.Client(timeout=3.0) as client:
            response = client.get(f"{endpoint}/v1/models", headers=headers)
            response.raise_for_status()
            data = response.json()
        provider_type = "local" if "localhost" in endpoint or "127.0.0.1" in endpoint else "remote"
        return [
            ModelEntry(provider=provider_name, model=m["id"], provider_type=provider_type)
            for m in data.get("data", [])
        ]
    except Exception:
        return []


def discover_models(
    ollama_url: str = "http://localhost:11434",
    extra_endpoints: Optional[List[dict]] = None,
) -> List[ModelEntry]:
    """Enumerate models from all configured local and remote sources.

    Args:
        ollama_url: Base URL of the local Ollama instance.
        extra_endpoints: List of dicts with keys ``endpoint``, ``name``,
            and optionally ``api_key`` for additional OpenAI-compatible hosts.

    Returns:
        Deduplicated list of :class:`ModelEntry` objects.
    """
    discovered: List[ModelEntry] = []

    # Ollama (local)
    discovered.extend(_get_ollama_models(ollama_url))

    # Additional OpenAI-compatible endpoints (e.g. LM Studio, vLLM, cloud)
    for ep in extra_endpoints or []:
        discovered.extend(
            _get_openai_compatible_models(
                ep["endpoint"],
                ep["name"],
                ep.get("api_key"),
            )
        )

    # Deduplicate by full_name
    seen: set = set()
    unique: List[ModelEntry] = []
    for entry in discovered:
        key = entry.full_name
        if key not in seen:
            seen.add(key)
            unique.append(entry)

    return unique
