import asyncio
import time
from typing import List, Dict, Optional, Any
from .base import LLMProvider
from .models import LLMResponse, ProviderType, RoutingDecision

class LLMRouter:
    def __init__(self):
        self._providers: Dict[str, LLMProvider] = {}
        self._default_local_model: Optional[str] = None
        self._default_cloud_model: Optional[str] = None

    def register_provider(self, provider: LLMProvider):
        """Register a new LLM provider."""
        self._providers[provider.provider_id] = provider

    def set_defaults(self, local_model: str, cloud_model: str):
        """Set default models for local and cloud routing."""
        self._default_local_model = local_model
        self._default_cloud_model = cloud_model

    async def route(
        self, 
        task: str, 
        complexity: float = 0.0,
        required_model: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Intelligently route a task to the appropriate LLM provider.
        
        Args:
            task: The prompt or task description.
            complexity: Score from 0.0 to 1.0 indicating task difficulty.
            required_model: If specified, bypasses routing logic to use this model.
        """
        start_time = time.perf_counter()
        
        # 1. Decide which provider and model to use
        decision = await self._make_routing_decision(task, complexity, required_model)
        
        provider = self._providers.get(decision.provider_id)
        if not provider:
            raise ValueError(f"Provider {decision.provider_id} not found.")

        # 2. Execute the call
        try:
            response = await provider.generate(task, decision.model, **kwargs)
            response.latency_ms = (time.perf_counter() - start_time) * 1000
            return response
        except Exception as e:
            # 3. Fallback logic
            return await self._handle_fallback(task, decision, e, **kwargs)

    async def _make_routing_decision(
        self, 
        task: str, 
        complexity: float, 
        required_model: Optional[str]
    ) -> RoutingDecision:
        """
        Logic to choose the best provider/model.
        In Phase 1, this is a rule-based engine.
        """
        # If a specific model is forced
        if required_model:
            for p_id, p in self._providers.items():
                if required_model in p.get_supported_models():
                    return RoutingDecision(
                        provider_id=p_id,
                        model=required_model,
                        reason="Explicit model requested"
                    )

        # Basic complexity-based routing
        if complexity < 0.5 and self._default_local_model:
            # Check if local provider is healthy
            local_providers = [p for p in self._providers.values() if p.provider_type == ProviderType.LOCAL]
            for p in local_providers:
                if await p.is_healthy():
                    return RoutingDecision(
                        provider_id=p.provider_id,
                        model=self._default_local_model,
                        reason=f"Low complexity ({complexity}), using local model"
                    )

        # Default to cloud if local fails or complexity is high
        if self._default_cloud_model:
            cloud_providers = [p for p in self._providers.values() if p.provider_type == ProviderType.CLOUD]
            for p in cloud_providers:
                if await p.is_healthy():
                    return RoutingDecision(
                        provider_id=p.provider_id,
                        model=self._default_cloud_model,
                        reason=f"High complexity ({complexity}) or local unavailable, using cloud"
                    )

        raise RuntimeError("No healthy providers available for routing.")

    async def _handle_fallback(
        self, 
        task: str, 
        failed_decision: RoutingDecision, 
        error: Exception,
        **kwargs
    ) -> LLMResponse:
        """Handle execution failures by falling back to another provider."""
        # Simple fallback: if local failed, try cloud
        failed_provider = self._providers.get(failed_decision.provider_id)
        
        if failed_provider and failed_provider.provider_type == ProviderType.LOCAL:
            if self._default_cloud_model:
                cloud_providers = [p for p in self._providers.values() if p.provider_type == ProviderType.CLOUD]
                for p in cloud_providers:
                    if await p.is_healthy():
                        return await p.generate(task, self._default_cloud_model, **kwargs)
        
        raise error
