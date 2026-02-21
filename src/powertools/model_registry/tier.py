from __future__ import annotations

from typing import List

from .models import BenchmarkResult, ModelAccreditation, ModelTier

# ---------------------------------------------------------------------------
# Tier assignment rules (ordered highest-to-lowest tier)
# ---------------------------------------------------------------------------
# A model reaches the highest tier for which ALL listed capabilities pass.
# If none of the tier conditions are met, the model is assigned Tier C.

_TIER_RULES: list[tuple[ModelTier, list[str]]] = [
    (ModelTier.S, ["reasoning"]),
    (ModelTier.A, ["coding"]),
    (ModelTier.B, ["summarisation"]),
]


def _assign_tier(scores: dict[str, bool]) -> ModelTier:
    """Determine tier from normalised boolean scores."""
    for tier, required_capabilities in _TIER_RULES:
        if all(scores.get(cap, False) for cap in required_capabilities):
            return tier
    return ModelTier.C


def tier_model(result: BenchmarkResult) -> ModelAccreditation:
    """Assign a tier and accreditation list to a single benchmarked model.

    Args:
        result: :class:`BenchmarkResult` from the benchmark engine.

    Returns:
        :class:`ModelAccreditation` with tier and earned capability badges.
    """
    # Normalise scores so we can handle both dict and CapabilityScore objects
    normalised: dict[str, bool] = {}
    for cap, score in result.scores.items():
        if hasattr(score, "success"):
            normalised[cap] = score.success
        elif isinstance(score, dict):
            normalised[cap] = bool(score.get("success"))
        else:
            normalised[cap] = False

    tier = _assign_tier(normalised)
    accreditations = [cap for cap, passed in normalised.items() if passed]

    return ModelAccreditation(
        model_full_name=result.model_full_name,
        tier=tier,
        accreditations=sorted(accreditations),
    )


def tier_models(results: List[BenchmarkResult]) -> List[ModelAccreditation]:
    """Assign tiers and accreditations to a list of benchmark results.

    Args:
        results: List of :class:`BenchmarkResult` objects.

    Returns:
        List of :class:`ModelAccreditation` objects.
    """
    return [tier_model(result) for result in results]
