"""Prompt evaluation and quality scoring."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class EvalResult:
    """Result of a prompt evaluation."""
    overall: float
    scores: Dict[str, float]
    suggestions: List[str]
    prompt_length: int
    word_count: int


class Evaluator:
    """Evaluate prompt quality across multiple dimensions.

    Example:
        >>> evaluator = Evaluator()
        >>> result = evaluator.score(
        ...     prompt="Write a Python function to sort a list",
        ...     criteria=["clarity", "specificity", "completeness"]
        ... )
        >>> print(f"Overall: {result.overall:.2f}")
    """

    CRITERIA_FUNCTIONS: Dict[str, callable] = {}

    def __init__(self, custom_criteria: Optional[Dict[str, callable]] = None):
        self.custom_criteria = custom_criteria or {}

    def score(
        self,
        prompt: str,
        criteria: Optional[List[str]] = None,
    ) -> EvalResult:
        """Score a prompt on the specified criteria.

        Args:
            prompt: The prompt to evaluate.
            criteria: List of criteria names to evaluate.

        Returns:
            EvalResult with scores and suggestions.
        """
        if criteria is None:
            criteria = ["clarity", "specificity", "completeness"]

        scores: Dict[str, float] = {}
        suggestions: List[str] = []

        for criterion in criteria:
            if criterion in self.custom_criteria:
                score = self.custom_criteria[criterion](prompt)
            elif hasattr(self, f"_eval_{criterion}"):
                score = getattr(self, f"_eval_{criterion}")(prompt)
            else:
                score = self._generic_score(prompt, criterion)
            scores[criterion] = score

        overall = sum(scores.values()) / len(scores) if scores else 0.0
        suggestions = self._generate_suggestions(scores, prompt)

        words = prompt.split()

        return EvalResult(
            overall=overall,
            scores=scores,
            suggestions=suggestions,
            prompt_length=len(prompt),
            word_count=len(words),
        )

    def _eval_clarity(self, prompt: str) -> float:
        """Evaluate prompt clarity."""
        score = 0.5

        if len(prompt.split()) < 10:
            score -= 0.2
        sentences = [s.strip() for s in prompt.split(".") if s.strip()]
        if sentences:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if 5 <= avg_length <= 25:
                score += 0.2
        if "\n" in prompt:
            score += 0.1
        if any(c in prompt for c in ["#", "1.", "-", "•"]):
            score += 0.1

        return max(0.0, min(1.0, score))

    def _eval_specificity(self, prompt: str) -> float:
        """Evaluate prompt specificity."""
        score = 0.3

        specific_markers = [
            "specific", "example", "such as", "for instance",
            "in particular", "namely", "including",
        ]
        for marker in specific_markers:
            if marker.lower() in prompt.lower():
                score += 0.1

        if "{" in prompt and "}" in prompt:
            score += 0.1
        if len(prompt) > 100:
            score += 0.1

        return max(0.0, min(1.0, score))

    def _eval_completeness(self, prompt: str) -> float:
        """Evaluate prompt completeness."""
        score = 0.3

        if any(w in prompt for w in ["role", "You are", "System"]):
            score += 0.15
        if any(w in prompt for w in ["format", "structure", "output"]):
            score += 0.15
        if any(w in prompt for w in ["constraint", "limit", "requirement"]):
            score += 0.1
        if any(w in prompt for w in ["example", "Example"]):
            score += 0.1
        if len(prompt) > 200:
            score += 0.1

        return max(0.0, min(1.0, score))

    def _generic_score(self, prompt: str, criterion: str) -> float:
        """Generic scoring fallback for unknown criteria."""
        base = 0.5
        if len(prompt) > 100:
            base += 0.1
        if "\n" in prompt:
            base += 0.05
        return min(1.0, base)

    def _generate_suggestions(
        self, scores: Dict[str, float], prompt: str
    ) -> List[str]:
        """Generate improvement suggestions based on scores."""
        suggestions: List[str] = []

        if scores.get("clarity", 1.0) < 0.5:
            suggestions.append(
                "Consider restructuring with shorter sentences and clear sections."
            )
        if scores.get("specificity", 1.0) < 0.5:
            suggestions.append(
                "Add specific examples or concrete details to improve specificity."
            )
        if scores.get("completeness", 1.0) < 0.5:
            suggestions.append(
                "Add role definition, output format, and constraints."
            )
        if not suggestions:
            suggestions.append("Prompt quality looks good!")

        return suggestions

    def compare(
        self, prompts: List[str], criteria: Optional[List[str]] = None
    ) -> List[EvalResult]:
        """Compare multiple prompts side by side."""
        return [self.score(p, criteria) for p in prompts]
