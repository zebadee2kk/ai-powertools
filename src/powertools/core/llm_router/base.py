from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .models import LLMResponse, ProviderType

class LLMProvider(ABC):
    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Unique identifier for the provider (e.g., 'openai', 'ollama')."""
        pass

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        """Whether the provider is local or cloud."""
        pass

    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        model: str, 
        **kwargs
    ) -> LLMResponse:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Check if the provider is currently available."""
        pass

    @abstractmethod
    def get_supported_models(self) -> List[str]:
        """List models supported by this provider."""
        pass
