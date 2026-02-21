from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from .benchmark import ModelCallable, benchmark_models
from .discover import discover_models
from .models import (
    ModelAccreditation,
    ModelEntry,
    ModelTier,
    RoutingProfile,
)
from .tier import tier_models

# Default routing profiles that map task types to preferred model tiers
DEFAULT_ROUTING_PROFILES: List[RoutingProfile] = [
    RoutingProfile(
        task_type="architecture",
        preferred_tier=ModelTier.S,
        fallback_tier=ModelTier.A,
        notes="Complex reasoning and planning; requires Tier S.",
    ),
    RoutingProfile(
        task_type="coding",
        preferred_tier=ModelTier.A,
        fallback_tier=ModelTier.S,
        notes="Code generation and debugging.",
    ),
    RoutingProfile(
        task_type="analysis",
        preferred_tier=ModelTier.A,
        fallback_tier=ModelTier.B,
        notes="Data analysis and structured output.",
    ),
    RoutingProfile(
        task_type="summarise",
        preferred_tier=ModelTier.B,
        fallback_tier=ModelTier.A,
        notes="Summarisation and extraction.",
    ),
    RoutingProfile(
        task_type="bulk",
        preferred_tier=ModelTier.C,
        fallback_tier=ModelTier.B,
        notes="Large batch tasks and preprocessing.",
    ),
]


class ModelRegistry:
    """Central registry for discovered, benchmarked and tiered AI models.

    Usage::

        registry = ModelRegistry()
        registry.discover(ollama_url="http://localhost:11434")
        registry.benchmark(call_fn=my_caller)
        registry.save("model_registry.json")

    Once populated, use :meth:`get_models_for_task` to look up the best models
    for a given task type according to the routing profiles.
    """

    def __init__(self) -> None:
        self._entries: List[ModelEntry] = []
        self._accreditations: Dict[str, ModelAccreditation] = {}
        self._routing_profiles: List[RoutingProfile] = list(DEFAULT_ROUTING_PROFILES)

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover(
        self,
        ollama_url: str = "http://localhost:11434",
        extra_endpoints: Optional[List[dict]] = None,
    ) -> List[ModelEntry]:
        """Enumerate models from all configured sources and store them.

        Args:
            ollama_url: Base URL of the local Ollama instance.
            extra_endpoints: Additional OpenAI-compatible endpoint dicts.

        Returns:
            List of discovered :class:`ModelEntry` objects.
        """
        self._entries = discover_models(
            ollama_url=ollama_url,
            extra_endpoints=extra_endpoints,
        )
        return list(self._entries)

    # ------------------------------------------------------------------
    # Benchmarking & tiering
    # ------------------------------------------------------------------

    def benchmark(
        self,
        call_fn: Optional[ModelCallable] = None,
        prompts: Optional[Dict[str, str]] = None,
    ) -> List[ModelAccreditation]:
        """Benchmark all discovered models and assign tiers.

        Args:
            call_fn: Callable ``(prompt, model_full_name) -> (text, latency_ms)``.
            prompts: Override capability prompts.

        Returns:
            List of :class:`ModelAccreditation` objects.
        """
        results = benchmark_models(self._entries, call_fn=call_fn, prompts=prompts)
        accreditations = tier_models(results)
        self._accreditations = {a.model_full_name: a for a in accreditations}
        return accreditations

    def add_accreditation(self, accreditation: ModelAccreditation) -> None:
        """Manually add or update an accreditation (e.g. from persisted data)."""
        self._accreditations[accreditation.model_full_name] = accreditation

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def set_routing_profiles(self, profiles: List[RoutingProfile]) -> None:
        """Replace the routing profiles."""
        self._routing_profiles = list(profiles)

    def get_models_for_task(self, task_type: str) -> List[ModelAccreditation]:
        """Return accredited models suitable for the given task type.

        The registry consults routing profiles to find the preferred tier
        (and fallback tier) for the task, then returns all accredited models
        at those tiers ordered preferred-first.

        Args:
            task_type: A task type string matching a :class:`RoutingProfile`.

        Returns:
            Ordered list of :class:`ModelAccreditation` objects; empty list if
            no models are available at the required tiers.
        """
        profile = next(
            (p for p in self._routing_profiles if p.task_type == task_type), None
        )
        if profile is None:
            # No specific profile: return all accreditations sorted by tier
            return sorted(
                self._accreditations.values(),
                key=lambda a: a.tier.value,
            )

        preferred = [
            a
            for a in self._accreditations.values()
            if a.tier == profile.preferred_tier
        ]
        if preferred:
            return preferred

        if profile.fallback_tier is not None:
            return [
                a
                for a in self._accreditations.values()
                if a.tier == profile.fallback_tier
            ]

        return []

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialise the registry state to a plain dict."""
        return {
            "models": [e.model_dump() for e in self._entries],
            "accreditations": {
                k: v.model_dump() for k, v in self._accreditations.items()
            },
            "routing_profiles": [p.model_dump() for p in self._routing_profiles],
        }

    def save(self, path: str) -> None:
        """Write registry state to *path* as JSON.

        Args:
            path: Destination file path (will be created or overwritten).
        """
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: str) -> "ModelRegistry":
        """Load a previously saved registry from *path*.

        Args:
            path: Path to a JSON file written by :meth:`save`.

        Returns:
            Populated :class:`ModelRegistry` instance.
        """
        data = json.loads(Path(path).read_text())
        registry = cls()
        registry._entries = [ModelEntry(**e) for e in data.get("models", [])]
        for accred_data in data.get("accreditations", {}).values():
            registry._accreditations[accred_data["model_full_name"]] = ModelAccreditation(
                **accred_data
            )
        if "routing_profiles" in data:
            registry._routing_profiles = [
                RoutingProfile(**p) for p in data["routing_profiles"]
            ]
        return registry
