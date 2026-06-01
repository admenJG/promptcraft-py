"""Tests for Optimizer."""

from promptcraft.optimizer import Optimizer


class TestOptimizer:
    def test_optimize_basic(self):
        optimizer = Optimizer(iterations=3)
        result = optimizer.optimize(prompt="Explain {topic}")
        assert result.original_prompt == "Explain {topic}"
        assert len(result.optimized_prompt) > 0
        assert result.iterations == 3
        assert 0.0 <= result.initial_score <= 1.0
        assert 0.0 <= result.final_score <= 1.0

    def test_optimize_improves(self):
        optimizer = Optimizer(iterations=20)
        result = optimizer.optimize(prompt="hi")
        assert result.final_score >= result.initial_score

    def test_optimize_history(self):
        optimizer = Optimizer(iterations=5)
        result = optimizer.optimize(prompt="Hello world")
        assert len(result.history) == 5
        assert all("score" in h for h in result.history)

    def test_custom_transformations(self):
        optimizer = Optimizer(iterations=3)
        result = optimizer.optimize(
            prompt="Test",
            transformations=["add_specificity"]
        )
        assert len(result.history) == 3
