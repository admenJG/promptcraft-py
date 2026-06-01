"""Fluent API for building prompts."""

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional


class PromptBuilder:
    """Build prompts with a fluent, chainable API.

    Example:
        >>> prompt = (
        ...     PromptBuilder()
        ...     .system("You are a helpful assistant.")
        ...     .instruction("Explain {topic}")
        ...     .variable("topic", "recursion")
        ...     .build()
        ... )
    """

    def __init__(self) -> None:
        self._system: Optional[str] = None
        self._instruction: Optional[str] = None
        self._variables: Dict[str, str] = {}
        self._examples: List[Dict[str, str]] = []
        self._context: Optional[str] = None
        self._output_format: Optional[str] = None
        self._constraints: List[str] = []

    def system(self, text: str) -> PromptBuilder:
        self._system = text
        return self

    def instruction(self, text: str) -> PromptBuilder:
        self._instruction = text
        return self

    def variable(self, key: str, value: str) -> PromptBuilder:
        self._variables[key] = value
        return self

    def variables(self, vars_dict: Dict[str, str]) -> PromptBuilder:
        self._variables.update(vars_dict)
        return self

    def examples(self, examples: List[Dict[str, str]]) -> PromptBuilder:
        self._examples = examples
        return self

    def context(self, text: str) -> PromptBuilder:
        self._context = text
        return self

    def output_format(self, text: str) -> PromptBuilder:
        self._output_format = text
        return self

    def constraint(self, text: str) -> PromptBuilder:
        self._constraints.append(text)
        return self

    def build(self) -> str:
        parts: List[str] = []
        if self._system:
            parts.append(f"[System]\n{self._system}")
        if self._context:
            parts.append(f"[Context]\n{self._context}")
        instruction = self._instruction or ""
        for key, value in self._variables.items():
            placeholder = "{" + key + "}"
            instruction = instruction.replace(placeholder, value)
        if instruction:
            parts.append(f"[Instruction]\n{instruction}")
        if self._examples:
            example_strs = []
            for i, ex in enumerate(self._examples, 1):
                ex_parts = [f"Example {i}:"]
                for k, v in ex.items():
                    ex_parts.append(f"  {k.capitalize()}: {v}")
                example_strs.append("\n".join(ex_parts))
            parts.append("[Examples]\n" + "\n\n".join(example_strs))
        if self._constraints:
            constraint_text = "\n".join(f"  - {c}" for c in self._constraints)
            parts.append(f"[Constraints]\n{constraint_text}")
        if self._output_format:
            parts.append(f"[Output Format]\n{self._output_format}")
        return "\n\n".join(parts)

    def render(self) -> str:
        return self.build()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system": self._system,
            "instruction": self._instruction,
            "variables": self._variables,
            "examples": self._examples,
            "context": self._context,
            "output_format": self._output_format,
            "constraints": self._constraints,
        }

    def to_json(self, indent: int = 2) -> str:
        """Export prompt configuration as a JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PromptBuilder:
        """Create a PromptBuilder from a dictionary."""
        builder = cls()
        if data.get("system"):
            builder._system = data["system"]
        if data.get("instruction"):
            builder._instruction = data["instruction"]
        if data.get("variables"):
            builder._variables = data["variables"]
        if data.get("examples"):
            builder._examples = data["examples"]
        if data.get("context"):
            builder._context = data["context"]
        if data.get("output_format"):
            builder._output_format = data["output_format"]
        if data.get("constraints"):
            builder._constraints = data["constraints"]
        return builder

    @classmethod
    def from_json(cls, json_str: str) -> PromptBuilder:
        """Create a PromptBuilder from a JSON string."""
        return cls.from_dict(json.loads(json_str))