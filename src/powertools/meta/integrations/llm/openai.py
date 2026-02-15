import httpx
import os
from typing import List, Dict, Any, Optional
from ...core.llm_router.base import LLMProvider
from ...core.llm_router.models import LLMResponse, ProviderType

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self._models = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"]

    @property
    def provider_id(self) -> str:
        return "openai"

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.CLOUD

    async def generate(self, prompt: str, model: str, **kwargs) -> LLMResponse:
        if not self.api_key:
            raise ValueError("OpenAI API key not provided.")

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    **kwargs
                }
            )
            response.raise_for_status()
            data = response.json()
            
            choice = data["choices"][0]
            usage = data.get("usage", {})
            
            return LLMResponse(
                content=choice["message"]["content"],
                model=model,
                provider=self.provider_id,
                provider_type=self.provider_type,
                usage={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                }
            )

    async def is_healthy(self) -> bool:
        # For cloud providers, 'healthy' usually means API key is present
        # We could also do a ping, but this is simpler for now
        return bool(self.api_key)

    def get_supported_models(self) -> List[str]:
        return self._models
