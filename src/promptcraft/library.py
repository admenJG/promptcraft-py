"""Built-in prompt template library for common use cases."""

from __future__ import annotations
from typing import Dict, Optional
from promptcraft.template import Template


TEMPLATES: Dict[str, Template] = {
    "code_review": Template(
        name="code_review",
        system="You are a senior software engineer conducting a thorough code review.",
        instruction="Review the following {language} code for bugs, performance issues, and style improvements:\n\n```{language}\n{code}\n```",
        variables=["language", "code"],
        output_format="Provide feedback in sections: Bugs, Performance, Style, Suggestions."
    ),
    "summarize": Template(
        name="summarize",
        system="You are a professional summarizer.",
        instruction="Summarize the following text in {style} style:\n\n{text}",
        variables=["style", "text"],
        output_format="Provide a clear, concise summary."
    ),
    "explain": Template(
        name="explain",
        system="You are a patient teacher who explains concepts clearly.",
        instruction="Explain the concept of {topic} to a {audience}. Use simple language and provide examples.",
        variables=["topic", "audience"],
        output_format="Use headers, bullet points, and code examples where appropriate."
    ),
    "translate": Template(
        name="translate",
        system="You are a professional translator.",
        instruction="Translate the following text from {source_lang} to {target_lang}:\n\n{text}",
        variables=["source_lang", "target_lang", "text"],
        output_format="Provide only the translation, maintaining the original tone and style."
    ),
    "debug": Template(
        name="debug",
        system="You are an expert debugger.",
        instruction="Help me debug the following {language} code. The expected behavior is {expected}, but the actual behavior is {actual}.\n\n```{language}\n{code}\n```",
        variables=["language", "expected", "actual", "code"],
        output_format="1. Identify the bug\n2. Explain why it occurs\n3. Provide the fix\n4. Show corrected code"
    ),
    "write_tests": Template(
        name="write_tests",
        system="You are a QA engineer writing comprehensive tests.",
        instruction="Write unit tests for the following {language} function:\n\n```{language}\n{code}\n```\n\nCover edge cases and use {framework} for assertions.",
        variables=["language", "code", "framework"],
        output_format="Provide test functions with clear names and comments."
    ),
    "api_docs": Template(
        name="api_docs",
        system="You are a technical writer specializing in API documentation.",
        instruction="Write API documentation for the following function:\n\n```{language}\n{code}\n```\n\nInclude description, parameters, return value, and usage examples.",
        variables=["language", "code"],
        output_format="Use Markdown with code blocks and tables."
    ),
    "refactor": Template(
        name="refactor",
        system="You are a software architect focused on clean code.",
        instruction="Refactor the following {language} code to improve readability, maintainability, and performance:\n\n```{language}\n{code}\n```",
        variables=["language", "code"],
        output_format="1. Show refactored code\n2. List changes made\n3. Explain improvements"
    ),
}


def get_template(name: str) -> Optional[Template]:
    """Get a built-in template by name."""
    return TEMPLATES.get(name)


def list_templates() -> Dict[str, str]:
    """List all available built-in templates."""
    return {name: template.instruction[:50] + "..." for name, template in TEMPLATES.items()}


def get_template_names() -> list:
    """Get list of all template names."""
    return list(TEMPLATES.keys())