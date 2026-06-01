"""Tests for PromptBuilder."""

import json
import pytest
from promptcraft.builder import PromptBuilder


class TestPromptBuilder:
    def test_system_message(self):
        result = PromptBuilder().system("You are helpful.").build()
        assert "[System]" in result
        assert "You are helpful." in result

    def test_instruction(self):
        result = PromptBuilder().instruction("Explain recursion").build()
        assert "[Instruction]" in result

    def test_variable_interpolation(self):
        result = PromptBuilder().instruction("Explain {topic}").variable("topic", "AI").build()
        assert "AI" in result
        assert "{topic}" not in result

    def test_multiple_variables(self):
        result = PromptBuilder().instruction("{a} in {b}").variables({"a": "sort", "b": "Python"}).build()
        assert "sort" in result
        assert "Python" in result

    def test_examples(self):
        result = PromptBuilder().examples([{"input": "Hi", "output": "Hello!"}]).build()
        assert "[Examples]" in result

    def test_context(self):
        result = PromptBuilder().context("Background info").build()
        assert "[Context]" in result

    def test_output_format(self):
        result = PromptBuilder().output_format("Return as JSON").build()
        assert "[Output Format]" in result

    def test_constraints(self):
        result = PromptBuilder().constraint("Max 100 words").constraint("No code").build()
        assert "Max 100 words" in result

    def test_fluent_chaining(self):
        result = (PromptBuilder().system("Helper").instruction("Do {x}")
                  .variable("x", "this").context("ctx").constraint("brief")
                  .output_format("text").build())
        assert all(tag in result for tag in ["[System]", "[Instruction]", "[Context]", "[Constraints]", "[Output Format]"])

    def test_to_dict(self):
        d = PromptBuilder().system("test").instruction("do {x}").to_dict()
        assert d["system"] == "test"

    def test_to_json(self):
        builder = PromptBuilder().system("test").instruction("do {x}").variable("x", "this")
        json_str = builder.to_json()
        data = json.loads(json_str)
        assert data["system"] == "test"
        assert data["variables"]["x"] == "this"

    def test_from_dict(self):
        data = {"system": "You are helpful.", "instruction": "Explain {topic}", "variables": {"topic": "AI"}}
        builder = PromptBuilder.from_dict(data)
        result = builder.build()
        assert "You are helpful." in result
        assert "AI" in result

    def test_from_json(self):
        json_str = '{"system": "test", "instruction": "do {x}", "variables": {"x": "this"}}'
        builder = PromptBuilder.from_json(json_str)
        result = builder.build()
        assert "test" in result
        assert "this" in result

    def test_roundtrip(self):
        original = PromptBuilder().system("sys").instruction("do {x}").variable("x", "val")
        json_str = original.to_json()
        restored = PromptBuilder.from_json(json_str)
        assert original.build() == restored.build()

    def test_render_alias(self):
        builder = PromptBuilder().instruction("Hello")
        assert builder.render() == builder.build()

    def test_empty_build(self):
        assert PromptBuilder().build() == ""