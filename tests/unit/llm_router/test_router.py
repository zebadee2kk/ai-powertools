import pytest
from unittest.mock import AsyncMock, MagicMock
from powertools.router.llm_router.router import LLMRouter
from powertools.router.llm_router.base import LLMProvider
from powertools.router.llm_router.models import LLMResponse, ProviderType

@pytest.fixture
def mock_local_provider():
    provider = MagicMock(spec=LLMProvider)
    provider.provider_id = "mock_local"
    provider.provider_type = ProviderType.LOCAL
    provider.is_healthy = AsyncMock(return_value=True)
    provider.get_supported_models.return_value = ["local-model-1"]
    provider.generate = AsyncMock(return_value=LLMResponse(
        content="Local response",
        model="local-model-1",
        provider="mock_local",
        provider_type=ProviderType.LOCAL
    ))
    return provider

@pytest.fixture
def mock_cloud_provider():
    provider = MagicMock(spec=LLMProvider)
    provider.provider_id = "mock_cloud"
    provider.provider_type = ProviderType.CLOUD
    provider.is_healthy = AsyncMock(return_value=True)
    provider.get_supported_models.return_value = ["cloud-model-1"]
    provider.generate = AsyncMock(return_value=LLMResponse(
        content="Cloud response",
        model="cloud-model-1",
        provider="mock_cloud",
        provider_type=ProviderType.CLOUD
    ))
    return provider

@pytest.mark.asyncio
async def test_router_low_complexity(mock_local_provider, mock_cloud_provider):
    router = LLMRouter()
    router.register_provider(mock_local_provider)
    router.register_provider(mock_cloud_provider)
    router.set_defaults(local_model="local-model-1", cloud_model="cloud-model-1")

    response = await router.route("Hello", complexity=0.2)

    assert response.provider == "mock_local"
    assert response.content == "Local response"
    mock_local_provider.generate.assert_called_once()
    mock_cloud_provider.generate.assert_not_called()

@pytest.mark.asyncio
async def test_router_high_complexity(mock_local_provider, mock_cloud_provider):
    router = LLMRouter()
    router.register_provider(mock_local_provider)
    router.register_provider(mock_cloud_provider)
    router.set_defaults(local_model="local-model-1", cloud_model="cloud-model-1")

    response = await router.route("Explain universe", complexity=0.8)

    assert response.provider == "mock_cloud"
    assert response.content == "Cloud response"
    mock_cloud_provider.generate.assert_called_once()
    mock_local_provider.generate.assert_not_called()

@pytest.mark.asyncio
async def test_router_fallback(mock_local_provider, mock_cloud_provider):
    router = LLMRouter()
    router.register_provider(mock_local_provider)
    router.register_provider(mock_cloud_provider)
    router.set_defaults(local_model="local-model-1", cloud_model="cloud-model-1")

    # Force local to fail
    mock_local_provider.generate.side_effect = Exception("Local failed")

    response = await router.route("Hello", complexity=0.2)

    assert response.provider == "mock_cloud"
    assert response.content == "Cloud response"
    mock_local_provider.generate.assert_called_once()
    mock_cloud_provider.generate.assert_called_once()
