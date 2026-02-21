from __future__ import annotations

import time
from typing import Callable, Dict, List, Optional

from .models import BenchmarkResult, CapabilityScore, ModelEntry

# ---------------------------------------------------------------------------
# Default micro-test prompts for each capability category
# ---------------------------------------------------------------------------
DEFAULT_PROMPTS: Dict[str, str] = {
    "reasoning": (
        "A train leaves Station A at 3 pm travelling at 60 mph. "
        "Another train leaves Station B (120 miles away) at the same time "
        "travelling towards Station A at 40 mph. When do they meet?"
    ),
    "coding": "Write a Python function that returns True if a string is a palindrome.",
    "summarisation": (
        "Summarise the following in one sentence: "
        "The mitochondria is the powerhouse of the cell, responsible for "
        "producing ATP through oxidative phosphorylation."
    ),
    "structured": (
        'Return a JSON object with keys "name" and "age" '
        'for a person called John who is 30 years old.'
    ),
    "creativity": (
        "Write a two-line poem about a robot learning to feel emotions."
    ),
}

# A callable that takes (prompt, model_full_name) and returns (response_text, latency_ms)
ModelCallable = Callable[[str, str], tuple[str, float]]


def _default_call(prompt: str, model_full_name: str) -> tuple[str, float]:  # pragma: no cover
    """Placeholder caller — replace with your routing / provider call."""
    start = time.perf_counter()
    response = ""
    latency_ms = (time.perf_counter() - start) * 1000
    return response, latency_ms


def benchmark_model(
    model_full_name: str,
    call_fn: Optional[ModelCallable] = None,
    prompts: Optional[Dict[str, str]] = None,
) -> BenchmarkResult:
    """Run capability micro-tests against a single model.

    Args:
        model_full_name: Provider-qualified model name, e.g. ``"ollama:llama3"``.
        call_fn: Callable ``(prompt, model_full_name) -> (response_text, latency_ms)``.
            Defaults to a no-op placeholder; supply a real caller for live benchmarks.
        prompts: Override the default capability prompts.

    Returns:
        :class:`BenchmarkResult` with per-capability scores.
    """
    caller = call_fn or _default_call
    active_prompts = prompts or DEFAULT_PROMPTS

    scores: Dict[str, CapabilityScore] = {}
    for capability, prompt in active_prompts.items():
        try:
            response_text, latency_ms = caller(prompt, model_full_name)
            scores[capability] = CapabilityScore(
                success=bool(response_text and len(response_text.strip()) > 0),
                latency_ms=latency_ms,
            )
        except Exception as exc:
            scores[capability] = CapabilityScore(
                success=False,
                latency_ms=0.0,
                notes=str(exc),
            )

    return BenchmarkResult(model_full_name=model_full_name, scores=scores)


def benchmark_models(
    models: List[ModelEntry],
    call_fn: Optional[ModelCallable] = None,
    prompts: Optional[Dict[str, str]] = None,
) -> List[BenchmarkResult]:
    """Benchmark a list of models and return all results.

    Args:
        models: Models to benchmark.
        call_fn: See :func:`benchmark_model`.
        prompts: See :func:`benchmark_model`.

    Returns:
        List of :class:`BenchmarkResult`, one per model.
    """
    return [
        benchmark_model(entry.full_name, call_fn=call_fn, prompts=prompts)
        for entry in models
    ]
