"""Tests for Template."""

import pytest
from promptcraft.template import Template


class TestTemplate:
    def test_render_basic(self):
        t = Template(name="test", instruction="Explain {topic}")
        result = t.render(topic="AI")
        assert "AI" in result
        assert "{topic}" not in result

    def test_render_with_system(self):
        t = Template(name="test", system="Be helpful.", instruction="Do {x}")
        result = t.render(x="this")
        assert "[System]" in result
        assert "Be helpful." in result
        assert "this" in result

    def test_render_missing_variables(self):
        t = Template(name="test", instruction="{a} and {b}")
        with pytest.raises(ValueError, match="Missing variables"):
            t.render(a="1")

    def test_extract_variables(self):
        variables = Template.extract_variables("{x} and {y} and {z}")
        assert set(variables) == {"x", "y", "z"}

    def test_validate_clean(self):
        t = Template(
            name="test",
            instruction="{x} is good",
            variables=["x"]
        )
        issues = t.validate()
        assert len(issues) == 0

    def test_validate_unused(self):
        t = Template(
            name="test",
            instruction="Hello world",
            variables=["x"]
        )
        issues = t.validate()
        assert any("unused" in i for i in issues)

    def test_to_dict(self):
        t = Template(
            name="test",
            system="sys",
            instruction="Do {x}",
            variables=["x"]
        )
        d = t.to_dict()
        assert d["name"] == "test"
        assert d["system"] == "sys"

    def test_repr(self):
        t = Template(name="test", variables=["x", "y"])
        assert "test" in repr(t)

    def test_render_with_examples(self):
        t = Template(
            name="test",
            instruction="Do {x}",
            examples=[{"input": "hi", "output": "hello"}]
        )
        result = t.render(x="this")
        assert "[Examples]" in result