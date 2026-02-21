from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ModelTier(str, Enum):
    """Performance tier for a model.

    S — Strategic Intelligence: complex reasoning, planning, final synthesis.
    A — Specialist Execution: coding, analysis, structured output.
    B — Utility Workers: summarisation, classification, extraction.
    C — Bulk Processing: large batch tasks, embedding, preprocessing.
    """

    S = "S"
    A = "A"
    B = "B"
    C = "C"


class Capability(str, Enum):
    """Benchmark capability categories."""

    REASONING = "reasoning"
    CODING = "coding"
    SUMMARISATION = "summarisation"
    STRUCTURED = "structured"
    CREATIVITY = "creativity"


class ModelEntry(BaseModel):
    """A discovered model from a local or remote provider."""

    provider: str
    model: str
    provider_type: str  # "local" | "remote"

    @property
    def full_name(self) -> str:
        return f"{self.provider}:{self.model}"


class CapabilityScore(BaseModel):
    """Result of a single capability micro-test."""

    success: bool
    latency_ms: float = 0.0
    notes: str = ""


class BenchmarkResult(BaseModel):
    """Aggregated benchmark scores for one model."""

    model_full_name: str
    scores: Dict[str, CapabilityScore] = Field(default_factory=dict)


class ModelAccreditation(BaseModel):
    """Tier assignment and accreditations for a model."""

    model_full_name: str
    tier: ModelTier
    accreditations: List[str] = Field(default_factory=list)


class RoutingProfile(BaseModel):
    """Maps task types to the preferred model tier and optional explicit model."""

    task_type: str
    preferred_tier: ModelTier
    fallback_tier: Optional[ModelTier] = None
    notes: str = ""
