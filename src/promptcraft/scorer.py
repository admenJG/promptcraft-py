"""Scoring utilities for prompt quality assessment."""

from __future__ import annotations
import re
from typing import Callable, Dict, List, Optional


class Scorer:
    """Advanced prompt scoring with customizable metrics.

    Example:
        >>> scorer = Scorer()
        >>> score = scorer.score(
        ...     prompt="Explain machine learning clearly with examples",
        ...     weights={"clarity": 0.3, "specificity": 0.4, "completeness": 0.3}
        ... )
    """

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "clarity": 0.25,
        "specificity": 0.25,
        "completeness": 0.25,
        "structure": 0.25,
    }

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        custom_metrics: Optional[Dict[str, Callable[[str], float]]] = None,
    ) -> None:
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self.custom_metrics = custom_metrics or {}

    def score(
        self, prompt: str, weights: Optional[Dict[str, float]] = None
    ) -> float:
        """Compute weighted score for a prompt."""
        active_weights = weights or self.weights
        total = 0.0
        weight_sum = 0.0

        for metric, weight in active_weights.items():
            if metric in self.custom_metrics:
                metric_score = self.custom_metrics[metric](prompt)
            else:
                metric_score = self._builtin_metric(prompt, metric)
            total += metric_score * weight
            weight_sum += weight

        return total / weight_sum if weight_sum > 0 else 0.0

    def _builtin_metric(self, prompt: str, metric: str) -> float:
        """Compute built-in metric scores."""
        if metric == "clarity":
            return self._clarity_score(prompt)
        elif metric == "specificity":
            return self._specificity_score(prompt)
        elif metric == "completeness":
            return self._completeness_score(prompt)
        elif metric == "structure":
            return self._structure_score(prompt)
        return 0.5

    def _clarity_score(self, prompt: str) -> float:
        score = 0.5
        words = prompt.split()
        if 10 <= len(words) <= 100:
            score += 0.2
        sentences = [s.strip() for s in prompt.split(".") if s.strip()]
        if sentences:
            avg_words = sum(len(s.split()) for s in sentences) / len(sentences)
            if 5 <= avg_words <= 30:
                score += 0.15
        if re.search(r"[A-Z]", prompt):
            score += 0.05
        return min(1.0, score)

    def _specificity_score(self, prompt: str) -> float:
        score = 0.3
        specific_words = [
            "example", "specific", "particular", "such as",
            "include", "for instance", "e.g.",
        ]
        for word in specific_words:
            if word.lower() in prompt.lower():
                score += 0.08
        return min(1.0, score)

    def _completeness_score(self, prompt: str) -> float:
        score = 0.2
        components = {
            "role": ["You are", "Act as", "System:"],
            "task": ["explain", "write", "create", "generate", "analyze"],
            "format": ["format", "structure", "json", "markdown", "list"],
        }
        for _name, markers in components.items():
            if any(m.lower() in prompt.lower() for m in markers):
                score += 0.2
        return min(1.0, score)

    def _structure_score(self, prompt: str) -> float:
        score = 0.4
        if "\n" in prompt:
            score += 0.15
        if any(c in prompt for c in ["#", "-", "*", "1.", "2."]):
            score += 0.15
        if "[" in prompt and "]" in prompt:
            score += 0.1
        if len(prompt) > 50:
            score += 0.1
        return min(1.0, score)

    def batch_score(
        self, prompts: List[str], weights: Optional[Dict[str, float]] = None
    ) -> List[float]:
        """Score multiple prompts."""
        return [self.score(p, weights) for p in prompts]

    def rank(
        self, prompts: List[str], weights: Optional[Dict[str, float]] = None
    ) -> List[tuple[int, float]]:
        """Rank prompts by score, returning (index, score) tuples."""
        scores = self.batch_score(prompts, weights)
        ranked = sorted(
            enumerate(scores), key=lambda x: x[1], reverse=True
        )
        return ranked
