"""Reusable prompt templates with variable interpolation."""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional


class Template:
    """A reusable prompt template with variable interpolation.

    Example:
        >>> t = Template(
        ...     name="summarize",
        ...     system="You are a summarizer.",
        ...     instruction="Summarize the following text in {style} style.",
        ...     variables=["style", "text"]
        ... )
        >>> prompt = t.render(style="concise", text="Long article...")
    """

    def __init__(
        self,
        name: str,
        system: Optional[str] = None,
        instruction: str = "",
        variables: Optional[List[str]] = None,
        examples: Optional[List[Dict[str, str]]] = None,
        output_format: Optional[str] = None,
    ) -> None:
        self.name = name
        self.system = system
        self.instruction = instruction
        self.variables = variables if variables is not None else self.extract_variables(instruction)
        self.examples = examples or []
        self.output_format = output_format

    def render(self, **kwargs: Any) -> str:
        """Render the template with provided variable values."""
        required = set(self.variables)
        provided = set(kwargs.keys())
        missing = required - provided
        if missing:
            raise ValueError(
                f"Missing variables: {', '.join(sorted(missing))}"
            )

        parts: List[str] = []
        if self.system:
            parts.append(f"[System]\n{self.system}")

        instruction = self.instruction
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            instruction = instruction.replace(placeholder, str(value))
        if instruction:
            parts.append(f"[Instruction]\n{instruction}")

        if self.examples:
            example_strs = []
            for i, ex in enumerate(self.examples, 1):
                ex_parts = [f"Example {i}:"]
                for k, v in ex.items():
                    ex_parts.append(f"  {k.capitalize()}: {v}")
                example_strs.append("\n".join(ex_parts))
            parts.append("[Examples]\n" + "\n\n".join(example_strs))

        if self.output_format:
            parts.append(f"[Output Format]\n{self.output_format}")

        return "\n\n".join(parts)

    @staticmethod
    def extract_variables(text: str) -> List[str]:
        """Extract variable names from template text."""
        return list(set(re.findall(r"\{(\w+)\}", text)))

    def validate(self) -> List[str]:
        """Validate the template and return any issues found."""
        issues: List[str] = []
        found_vars = set(self.extract_variables(self.instruction))
        declared = set(self.variables)
        unused = declared - found_vars
        if unused:
            issues.append(
                f"Declared but unused variables: {', '.join(unused)}"
            )
        return issues

    def to_dict(self) -> Dict[str, Any]:
        """Export template as a dictionary."""
        return {
            "name": self.name,
            "system": self.system,
            "instruction": self.instruction,
            "variables": self.variables,
            "examples": self.examples,
            "output_format": self.output_format,
        }

    def __repr__(self) -> str:
        return f"Template(name={self.name!r}, variables={self.variables})"