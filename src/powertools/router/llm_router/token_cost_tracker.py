from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class UsageRecord:
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class TokenCostTracker:
    """Deterministic token/cost accounting for routed LLM calls."""

    def __init__(self, pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self._pricing: Dict[str, Dict[str, float]] = pricing.copy() if pricing else {}
        self._records: List[UsageRecord] = []

    def register_model_pricing(
        self,
        model: str,
        *,
        input_cost_per_1k: float,
        output_cost_per_1k: float,
    ) -> None:
        self._pricing[model] = {
            "input_cost_per_1k": input_cost_per_1k,
            "output_cost_per_1k": output_cost_per_1k,
        }

    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        if model not in self._pricing:
            raise ValueError(f"No pricing registered for model: {model}")

        pricing = self._pricing[model]
        input_cost = (input_tokens / 1000) * pricing["input_cost_per_1k"]
        output_cost = (output_tokens / 1000) * pricing["output_cost_per_1k"]
        return input_cost + output_cost

    def record_usage(
        self,
        *,
        model: str,
        input_tokens: int,
        output_tokens: int,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UsageRecord:
        cost = self.estimate_cost(model, input_tokens, output_tokens)
        record = UsageRecord(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost=cost,
            metadata=metadata or {},
        )
        self._records.append(record)
        return record

    @property
    def records(self) -> List[UsageRecord]:
        return list(self._records)

    @property
    def total_cost(self) -> float:
        return sum(record.cost for record in self._records)

    @property
    def total_tokens(self) -> int:
        return sum(record.total_tokens for record in self._records)

    def summarize_by_model(self) -> Dict[str, Dict[str, float]]:
        summary: Dict[str, Dict[str, float]] = {}
        for record in self._records:
            row = summary.setdefault(
                record.model,
                {"calls": 0.0, "input_tokens": 0.0, "output_tokens": 0.0, "cost": 0.0},
            )
            row["calls"] += 1
            row["input_tokens"] += record.input_tokens
            row["output_tokens"] += record.output_tokens
            row["cost"] += record.cost
        return summary
