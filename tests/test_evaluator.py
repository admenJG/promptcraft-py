"""Tests for Evaluator and Scorer."""

import pytest
from promptcraft.evaluator import Evaluator, EvalResult
from promptcraft.scorer import Scorer


class TestEvaluator:
    def test_basic_score(self):
        evaluator = Evaluator()
        result = evaluator.score("Explain machine learning clearly")
        assert isinstance(result, EvalResult)
        assert 0.0 <= result.overall <= 1.0

    def test_detailed_criteria(self):
        evaluator = Evaluator()
        result = evaluator.score(
            "You are a helpful assistant. Explain {topic} with examples.",
            criteria=["clarity", "specificity", "completeness"]
        )
        assert "clarity" in result.scores
        assert "specificity" in result.scores
        assert "completeness" in result.scores

    def test_suggestions(self):
        evaluator = Evaluator()
        result = evaluator.score("hi")
        assert len(result.suggestions) > 0

    def test_compare(self):
        evaluator = Evaluator()
        prompts = ["Short", "A much longer and more detailed prompt with context"]
        results = evaluator.compare(prompts)
        assert len(results) == 2

    def test_prompt_stats(self):
        evaluator = Evaluator()
        result = evaluator.score("Hello world test prompt")
        assert result.word_count == 4
        assert result.prompt_length > 0

    def test_custom_criteria(self):
        custom = {"length": lambda p: min(len(p) / 100, 1.0)}
        evaluator = Evaluator(custom_criteria=custom)
        result = evaluator.score("A prompt", criteria=["length"])
        assert "length" in result.scores


class TestScorer:
    def test_basic_score(self):
        scorer = Scorer()
        score = scorer.score("Explain machine learning with examples")
        assert 0.0 <= score <= 1.0

    def test_weighted_score(self):
        scorer = Scorer(weights={"clarity": 1.0})
        score = scorer.score("You are helpful. Explain things clearly.")
        assert 0.0 <= score <= 1.0

    def test_batch_score(self):
        scorer = Scorer()
        scores = scorer.batch_score(["prompt one", "prompt two"])
        assert len(scores) == 2
        assert all(0.0 <= s <= 1.0 for s in scores)

    def test_rank(self):
        scorer = Scorer()
        prompts = [
            "Short",
            "You are an expert. Explain machine learning with detailed examples.",
            "Medium length prompt here",
        ]
        ranked = scorer.rank(prompts)
        assert len(ranked) == 3
        assert all(isinstance(r, tuple) for r in ranked)

    def test_custom_metric(self):
        custom = {"my_metric": lambda p: 0.75}
        scorer = Scorer(custom_metrics=custom, weights={"my_metric": 1.0})
        score = scorer.score("anything")
        assert score == 0.75
