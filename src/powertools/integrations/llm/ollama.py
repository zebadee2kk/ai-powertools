import httpx
from typing import List, Dict, Any
from ...core.llm_router.base import LLMProvider
from ...core.llm_router.models import LLMResponse, ProviderType

class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self._supported_models = []

    @property
    def provider_id(self) -> str:
        return "ollama"

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.LOCAL

    async def generate(self, prompt: str, model: str, **kwargs) -> LLMResponse:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    **kwargs
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return LLMResponse(
                content=data["response"],
                model=model,
                provider=self.provider_id,
                provider_type=self.provider_type,
                usage={
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                    "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                }
            )

    async def is_healthy(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    self._supported_models = [m["name"] for m in data.get("models", [])]
                    return True
                return False
        except Exception:
            return False

    def get_supported_models(self) -> List[str]:
        return self._supported_models
