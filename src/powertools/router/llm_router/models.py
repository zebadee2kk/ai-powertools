from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

class ProviderType(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"

class LLMResponse(BaseModel):
    content: str
    model: str
    provider: str
    provider_type: ProviderType
    usage: Dict[str, int] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    cost: float = 0.0
    latency_ms: float = 0.0

class RoutingDecision(BaseModel):
    provider_id: str
    model: str
    reason: str
    estimated_cost: float = 0.0
    estimated_latency_ms: float = 0.0
    confidence_score: float = 1.0
