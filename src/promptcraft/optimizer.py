"""Prompt optimization through iterative refinement."""

from __future__ import annotations
import re
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class OptimizationResult:
    """Result of a prompt optimization run."""
    original_prompt: str
    optimized_prompt: str
    iterations: int
    initial_score: float
    final_score: float
    history: List[Dict[str, Any]] = field(default_factory=list)


class Optimizer:
    """Optimize prompts through iterative refinement and scoring.

    The optimizer applies transformations to a prompt, scores each variant,
    and keeps the best-performing version.

    Example:
        >>> optimizer = Optimizer(metric="relevance", iterations=10)
        >>> result = optimizer.optimize(
        ...     prompt="Explain {topic}",
        ...     test_cases=[{"topic": "AI", "expected_keywords": ["model"]}]
        ... )
    """

    TRANSFORMATIONS: List[str] = [
        "add_specificity",
        "add_examples",
        "restructure",
        "add_constraints",
        "clarify_role",
    ]

    def __init__(
        self,
        metric: str = "overall",
        iterations: int = 5,
        scoring_fn: Optional[Callable[[str], float]] = None,
    ) -> None:
        self.metric = metric
        self.iterations = iterations
        self.scoring_fn = scoring_fn or self._default_scoring

    def optimize(
        self,
        prompt: str,
        test_cases: Optional[List[Dict[str, Any]]] = None,
        transformations: Optional[List[str]] = None,
    ) -> OptimizationResult:
        """Optimize a prompt through iterative refinement.

        Args:
            prompt: The initial prompt template to optimize.
            test_cases: Optional test cases for evaluation.
            transformations: Specific transformations to apply.

        Returns:
            OptimizationResult with original, optimized, scores, and history.
        """
        transformations = transformations or self.TRANSFORMATIONS
        best_prompt = prompt
        best_score = self._score_prompt(prompt, test_cases)
        initial_score = best_score
        history: List[Dict[str, Any]] = []

        for i in range(self.iterations):
            variant = self._apply_transformation(
                best_prompt, random.choice(transformations)
            )
            score = self._score_prompt(variant, test_cases)
            history.append({
                "iteration": i + 1,
                "transformation": "applied",
                "score": score,
                "prompt_preview": variant[:100],
            })
            if score > best_score:
                best_prompt = variant
                best_score = score

        return OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=best_prompt,
            iterations=self.iterations,
            initial_score=initial_score,
            final_score=best_score,
            history=history,
        )

    def _apply_transformation(self, prompt: str, transformation: str) -> str:
        """Apply a specific transformation to a prompt."""
        if transformation == "add_specificity":
            return self._add_specificity(prompt)
        elif transformation == "add_examples":
            return self._add_examples(prompt)
        elif transformation == "restructure":
            return self._restructure(prompt)
        elif transformation == "add_constraints":
            return self._add_constraints(prompt)
        elif transformation == "clarify_role":
            return self._clarify_role(prompt)
        return prompt

    def _add_specificity(self, prompt: str) -> str:
        """Add more specific instructions."""
        suffixes = [
            "\nBe precise and detailed in your response.",
            "\nProvide specific examples to support your explanation.",
            "\nFocus on practical, actionable information.",
            "\nExplain step by step.",
        ]
        return prompt + random.choice(suffixes)

    def _add_examples(self, prompt: str) -> str:
        """Add few-shot example placeholders."""
        example_block = (
            "\n\nHere is an example of a good response:\n"
            "[Provide a well-structured example answer]"
        )
        return prompt + example_block

    def _restructure(self, prompt: str) -> str:
        """Restructure the prompt with clear sections."""
        if "[System]" not in prompt and "[Instruction]" not in prompt:
            return f"[Role]\nYou are a helpful assistant.\n\n[Task]\n{prompt}"
        return prompt

    def _add_constraints(self, prompt: str) -> str:
        """Add output constraints."""
        constraints = [
            "\n\nKeep your response under 500 words.",
            "\n\nUse bullet points for clarity.",
            "\n\nInclude a brief summary at the end.",
            "\n\nStructure your response with clear headings.",
        ]
        return prompt + random.choice(constraints)

    def _clarify_role(self, prompt: str) -> str:
        """Add or clarify the assistant's role."""
        if "You are" not in prompt:
            return (
                "You are a knowledgeable expert who provides clear, "
                "accurate, and helpful responses.\n\n" + prompt
            )
        return prompt

    def _score_prompt(
        self, prompt: str, test_cases: Optional[List[Dict[str, Any]]]
    ) -> float:
        """Score a prompt using the configured scoring function."""
        return self.scoring_fn(prompt)

    @staticmethod
    def _default_scoring(prompt: str) -> float:
        """Default heuristic-based scoring."""
        score = 0.0

        if "You are" in prompt or "[System]" in prompt:
            score += 0.2
        if "{" in prompt and "}" in prompt:
            score += 0.1
        if len(prompt) > 50:
            score += 0.1
        if len(prompt) > 150:
            score += 0.1
        if "Example" in prompt or "example" in prompt:
            score += 0.15
        if any(w in prompt.lower() for w in ["step", "detail", "specific"]):
            score += 0.1
        if "\n" in prompt:
            score += 0.05
        if any(w in prompt for w in ["#", "-", "*"]):
            score += 0.05

        return min(score, 1.0)
