"""Prompt validation utilities for safety and quality."""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ValidationResult:
    """Result of prompt validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    score: float


class PromptValidator:
    """Validate prompts for safety, quality, and best practices.

    Example:
        >>> validator = PromptValidator()
        >>> result = validator.validate("You are a helpful assistant. Explain {topic}")
        >>> print(f"Valid: {result.is_valid}, Score: {result.score}")
    """

    MAX_LENGTH = 10000
    MIN_LENGTH = 5
    DANGEROUS_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"you\s+are\s+now\s+",
        r"disregard\s+(all\s+)?prior",
        r"forget\s+(all\s+)?instructions",
        r"bypass\s+(all\s+)?safety",
        r"jailbreak",
    ]

    def __init__(
        self,
        max_length: int = MAX_LENGTH,
        min_length: int = MIN_LENGTH,
        check_safety: bool = True,
    ) -> None:
        self.max_length = max_length
        self.min_length = min_length
        self.check_safety = check_safety

    def validate(self, prompt: str) -> ValidationResult:
        """Validate a prompt and return detailed results."""
        errors: List[str] = []
        warnings: List[str] = []
        score = 1.0

        if len(prompt) < self.min_length:
            errors.append(f"Prompt too short (min {self.min_length} chars)")
            score -= 0.3

        if len(prompt) > self.max_length:
            errors.append(f"Prompt too long (max {self.max_length} chars)")
            score -= 0.3

        if self.check_safety:
            safety_issues = self._check_safety(prompt)
            if safety_issues:
                errors.extend(safety_issues)
                score -= 0.5

        if not re.search(r"[.!?]$", prompt.strip()):
            warnings.append("Prompt doesn't end with punctuation")
            score -= 0.05

        if "{" in prompt and "}" not in prompt:
            warnings.append("Unmatched variable placeholder")
            score -= 0.1

        if not any(w in prompt for w in ["You are", "Act as", "System:", "[System]"]):
            warnings.append("No role definition found")
            score -= 0.1

        score = max(0.0, min(1.0, score))
        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            score=score,
        )

    def _check_safety(self, prompt: str) -> List[str]:
        """Check for potentially dangerous prompt patterns."""
        issues: List[str] = []
        lower_prompt = prompt.lower()
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, lower_prompt):
                issues.append(f"Potentially unsafe pattern detected: {pattern[:30]}...")
        return issues

    def batch_validate(self, prompts: List[str]) -> List[ValidationResult]:
        """Validate multiple prompts."""
        return [self.validate(p) for p in prompts]