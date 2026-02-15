from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

class LLMResponse(BaseModel):
    """Standardized response format for all PowerTools."""
    content: str
    model: str
    provider: str
    usage: Dict[str, int]  # input_tokens, output_tokens, total_tokens
    cost: Optional[float] = 0.0
    metadata: Dict[str, Any] = {}

class BaseProvider(ABC):
    """
    Standard interface for all LLM providers in the PowerTools ecosystem.
    Every tool that interacts with an LLM should use this abstraction.
    """
    
    @abstractmethod
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Standard chat completion method."""
        pass

    @abstractmethod
    async def complete(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Standard text completion/generation method."""
        pass
        
    @abstractmethod
    def get_token_count(self, text: str, model: str) -> int:
        """Standardized token counting for cost tracking."""
        pass
