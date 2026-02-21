import json
import tempfile
from unittest.mock import MagicMock, patch

import httpx
import pytest

from powertools.model_registry import (
    BenchmarkResult,
    CapabilityScore,
    ModelAccreditation,
    ModelEntry,
    ModelRegistry,
    ModelTier,
    RoutingProfile,
    benchmark_model,
    benchmark_models,
    discover_models,
    tier_model,
    tier_models,
)


# ---------------------------------------------------------------------------
# discover_models
# ---------------------------------------------------------------------------


def test_discover_models_ollama(respx_mock):
    """discover_models returns ModelEntry objects for Ollama models."""
    respx_mock.get("http://localhost:11434/api/tags").mock(
        return_value=httpx.Response(
            200,
            json={"models": [{"name": "llama3"}, {"name": "mistral"}]},
        )
    )

    entries = discover_models(ollama_url="http://localhost:11434")

    assert len(entries) == 2
    assert entries[0].provider == "ollama"
    assert entries[0].model == "llama3"
    assert entries[0].provider_type == "local"
    assert entries[1].model == "mistral"


def test_discover_models_deduplicates():
    """duplicate full_names are removed."""
    with patch(
        "powertools.model_registry.discover._get_ollama_models",
        return_value=[
            ModelEntry(provider="ollama", model="llama3", provider_type="local"),
            ModelEntry(provider="ollama", model="llama3", provider_type="local"),
        ],
    ):
        entries = discover_models()

    assert len(entries) == 1


def test_discover_models_returns_empty_on_connection_error():
    """No exception propagates if Ollama is unavailable."""
    entries = discover_models(ollama_url="http://127.0.0.1:9")
    assert entries == []


def test_discover_models_extra_endpoint(respx_mock):
    """OpenAI-compatible extra endpoints are queried."""
    respx_mock.get("http://localhost:1234/v1/models").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "phi-3"}, {"id": "gemma-2b"}]},
        )
    )

    entries = discover_models(
        ollama_url="http://127.0.0.1:9",  # unavailable
        extra_endpoints=[{"endpoint": "http://localhost:1234", "name": "lmstudio"}],
    )

    assert len(entries) == 2
    assert entries[0].provider == "lmstudio"
    assert entries[0].model == "phi-3"
    assert entries[0].provider_type == "local"


# ---------------------------------------------------------------------------
# benchmark_model / benchmark_models
# ---------------------------------------------------------------------------


def _fake_call(prompt: str, model_full_name: str) -> tuple[str, float]:
    """Always returns a non-empty response in ~0 ms."""
    return "This is a valid response.", 5.0


def _failing_call(prompt: str, model_full_name: str) -> tuple[str, float]:
    raise RuntimeError("model offline")


def test_benchmark_model_success():
    result = benchmark_model(
        "ollama:llama3",
        call_fn=_fake_call,
        prompts={"reasoning": "What is 2+2?", "coding": "Write a hello world."},
    )

    assert result.model_full_name == "ollama:llama3"
    assert result.scores["reasoning"].success is True
    assert result.scores["coding"].latency_ms == pytest.approx(5.0)


def test_benchmark_model_handles_call_exception():
    result = benchmark_model(
        "ollama:broken",
        call_fn=_failing_call,
        prompts={"reasoning": "fail me"},
    )

    assert result.scores["reasoning"].success is False
    assert "model offline" in result.scores["reasoning"].notes


def test_benchmark_models_returns_one_result_per_entry():
    entries = [
        ModelEntry(provider="ollama", model="llama3", provider_type="local"),
        ModelEntry(provider="lmstudio", model="phi-3", provider_type="local"),
    ]
    results = benchmark_models(entries, call_fn=_fake_call, prompts={"coding": "test"})

    assert len(results) == 2
    assert results[0].model_full_name == "ollama:llama3"
    assert results[1].model_full_name == "lmstudio:phi-3"


# ---------------------------------------------------------------------------
# tier_model / tier_models
# ---------------------------------------------------------------------------


def _make_result(model: str, **capabilities: bool) -> BenchmarkResult:
    scores = {
        cap: CapabilityScore(success=passed) for cap, passed in capabilities.items()
    }
    return BenchmarkResult(model_full_name=model, scores=scores)


def test_tier_model_s_tier_on_reasoning():
    result = _make_result("m", reasoning=True, coding=True)
    accred = tier_model(result)
    assert accred.tier == ModelTier.S
    assert "reasoning" in accred.accreditations


def test_tier_model_a_tier_on_coding_only():
    result = _make_result("m", reasoning=False, coding=True)
    accred = tier_model(result)
    assert accred.tier == ModelTier.A


def test_tier_model_b_tier_on_summarisation_only():
    result = _make_result("m", reasoning=False, coding=False, summarisation=True)
    accred = tier_model(result)
    assert accred.tier == ModelTier.B


def test_tier_model_c_tier_when_nothing_passes():
    result = _make_result("m", reasoning=False, coding=False, summarisation=False)
    accred = tier_model(result)
    assert accred.tier == ModelTier.C
    assert accred.accreditations == []


def test_tier_models_processes_all():
    results = [
        _make_result("ollama:llama3", reasoning=True),
        _make_result("ollama:mistral", coding=True),
    ]
    accreditations = tier_models(results)
    assert len(accreditations) == 2
    assert accreditations[0].tier == ModelTier.S
    assert accreditations[1].tier == ModelTier.A


# ---------------------------------------------------------------------------
# ModelRegistry
# ---------------------------------------------------------------------------


def test_registry_discover_populates_entries(respx_mock):
    respx_mock.get("http://localhost:11434/api/tags").mock(
        return_value=httpx.Response(
            200,
            json={"models": [{"name": "llama3"}]},
        )
    )

    registry = ModelRegistry()
    entries = registry.discover(ollama_url="http://localhost:11434")

    assert len(entries) == 1
    assert entries[0].full_name == "ollama:llama3"


def test_registry_benchmark_assigns_accreditations():
    registry = ModelRegistry()
    registry._entries = [ModelEntry(provider="ollama", model="llama3", provider_type="local")]

    registry.benchmark(
        call_fn=_fake_call,
        prompts={"reasoning": "test"},
    )

    accred = registry._accreditations.get("ollama:llama3")
    assert accred is not None
    assert accred.tier == ModelTier.S


def test_registry_get_models_for_task_returns_correct_tier():
    registry = ModelRegistry()
    registry.add_accreditation(
        ModelAccreditation(
            model_full_name="ollama:llama3",
            tier=ModelTier.S,
            accreditations=["reasoning"],
        )
    )
    registry.add_accreditation(
        ModelAccreditation(
            model_full_name="ollama:mistral",
            tier=ModelTier.A,
            accreditations=["coding"],
        )
    )

    # "architecture" profile prefers Tier S
    models = registry.get_models_for_task("architecture")
    assert len(models) == 1
    assert models[0].model_full_name == "ollama:llama3"


def test_registry_get_models_for_task_uses_fallback():
    registry = ModelRegistry()
    registry.add_accreditation(
        ModelAccreditation(
            model_full_name="ollama:mistral",
            tier=ModelTier.A,
            accreditations=["coding"],
        )
    )

    # "architecture" prefers Tier S; none available → falls back to Tier A
    models = registry.get_models_for_task("architecture")
    assert len(models) == 1
    assert models[0].tier == ModelTier.A


def test_registry_save_and_load(tmp_path):
    registry = ModelRegistry()
    registry._entries = [ModelEntry(provider="ollama", model="llama3", provider_type="local")]
    registry.add_accreditation(
        ModelAccreditation(
            model_full_name="ollama:llama3",
            tier=ModelTier.S,
            accreditations=["reasoning"],
        )
    )

    path = str(tmp_path / "registry.json")
    registry.save(path)

    loaded = ModelRegistry.load(path)
    assert len(loaded._entries) == 1
    assert "ollama:llama3" in loaded._accreditations
    assert loaded._accreditations["ollama:llama3"].tier == ModelTier.S


def test_registry_to_dict_structure():
    registry = ModelRegistry()
    registry._entries = [ModelEntry(provider="ollama", model="llama3", provider_type="local")]
    data = registry.to_dict()

    assert "models" in data
    assert "accreditations" in data
    assert "routing_profiles" in data
    assert data["models"][0]["provider"] == "ollama"


# ---------------------------------------------------------------------------
# LLMRouter tier-aware routing integration
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_router_uses_tier_aware_routing_when_registry_attached():
    from unittest.mock import AsyncMock
    from powertools.router.llm_router.router import LLMRouter
    from powertools.router.llm_router.base import LLMProvider
    from powertools.router.llm_router.models import LLMResponse, ProviderType

    provider = MagicMock(spec=LLMProvider)
    provider.provider_id = "ollama"
    provider.provider_type = ProviderType.LOCAL
    provider.is_healthy = AsyncMock(return_value=True)
    provider.get_supported_models.return_value = ["llama3"]
    provider.generate = AsyncMock(
        return_value=LLMResponse(
            content="Tier-S response",
            model="llama3",
            provider="ollama",
            provider_type=ProviderType.LOCAL,
        )
    )

    registry = ModelRegistry()
    registry.add_accreditation(
        ModelAccreditation(
            model_full_name="ollama:llama3",
            tier=ModelTier.S,
            accreditations=["reasoning"],
        )
    )

    router = LLMRouter()
    router.register_provider(provider)
    router.set_defaults(local_model="llama3", cloud_model="gpt-4")
    router.set_model_registry(registry)

    response = await router.route("Plan the system architecture", task_type="architecture")

    assert response.content == "Tier-S response"
    provider.generate.assert_called_once_with("Plan the system architecture", "llama3")
