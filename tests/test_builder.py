"""Tests for PromptBuilder."""

import pytest
from promptcraft.builder import PromptBuilder


class TestPromptBuilder:
    def test_system_message(self):
        builder = PromptBuilder()
        result = builder.system("You are helpful.").build()
        assert "[System]" in result
        assert "You are helpful." in result

    def test_instruction(self):
        builder = PromptBuilder()
        result = builder.instruction("Explain recursion").build()
        assert "[Instruction]" in result
        assert "Explain recursion" in result

    def test_variable_interpolation(self):
        builder = PromptBuilder()
        result = (
            PromptBuilder()
            .instruction("Explain {topic}")
            .variable("topic", "AI")
            .build()
        )
        assert "AI" in result
        assert "{topic}" not in result

    def test_multiple_variables(self):
        result = (
            PromptBuilder()
            .instruction("{action} in {language}")
            .variables({"action": "sort", "language": "Python"})
            .build()
        )
        assert "sort" in result
        assert "Python" in result

    def test_examples(self):
        examples = [{"input": "Hi", "output": "Hello!"}]
        result = PromptBuilder().examples(examples).build()
        assert "[Examples]" in result
        assert "Example 1:" in result

    def test_context(self):
        result = PromptBuilder().context("Background info here").build()
        assert "[Context]" in result

    def test_output_format(self):
        result = PromptBuilder().output_format("Return as JSON").build()
        assert "[Output Format]" in result

    def test_constraint(self):
        result = (
            PromptBuilder()
            .constraint("Max 100 words")
            .constraint("No code")
            .build()
        )
        assert "Max 100 words" in result
        assert "No code" in result

    def test_fluent_chaining(self):
        result = (
            PromptBuilder()
            .system("You are a helper.")
            .instruction("Do {thing}")
            .variable("thing", "this")
            .context("Some context")
            .constraint("Be brief")
            .output_format("Plain text")
            .build()
        )
        assert "[System]" in result
        assert "[Instruction]" in result
        assert "[Context]" in result
        assert "[Constraints]" in result
        assert "[Output Format]" in result

    def test_to_dict(self):
        builder = PromptBuilder().system("test").instruction("do {x}")
        d = builder.to_dict()
        assert d["system"] == "test"
        assert d["instruction"] == "do {x}"

    def test_render_alias(self):
        builder = PromptBuilder().instruction("Hello")
        assert builder.render() == builder.build()

    def test_empty_build(self):
        result = PromptBuilder().build()
        assert result == ""
