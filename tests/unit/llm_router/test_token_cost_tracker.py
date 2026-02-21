import pytest

from powertools.router.llm_router import TokenCostTracker


def test_estimate_cost_uses_registered_pricing():
    tracker = TokenCostTracker({"gpt-test": {"input_cost_per_1k": 0.01, "output_cost_per_1k": 0.02}})

    cost = tracker.estimate_cost("gpt-test", input_tokens=500, output_tokens=1000)

    assert cost == pytest.approx(0.025)


def test_record_usage_updates_totals_and_summary():
    tracker = TokenCostTracker()
    tracker.register_model_pricing("local-model", input_cost_per_1k=0.0, output_cost_per_1k=0.0)
    tracker.register_model_pricing("cloud-model", input_cost_per_1k=0.005, output_cost_per_1k=0.015)

    tracker.record_usage(model="local-model", input_tokens=200, output_tokens=50)
    tracker.record_usage(model="cloud-model", input_tokens=1000, output_tokens=500)

    assert tracker.total_tokens == 1750
    assert tracker.total_cost == pytest.approx(0.0125)

    summary = tracker.summarize_by_model()
    assert summary["local-model"]["calls"] == 1
    assert summary["cloud-model"]["cost"] == pytest.approx(0.0125)


def test_estimate_cost_raises_for_unknown_model():
    tracker = TokenCostTracker()

    with pytest.raises(ValueError, match="No pricing registered"):
        tracker.estimate_cost("unknown", input_tokens=10, output_tokens=10)
