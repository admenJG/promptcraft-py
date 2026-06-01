"""Tests for prompt template library."""

import pytest
from promptcraft.library import get_template, list_templates, get_template_names, TEMPLATES


class TestLibrary:
    def test_list_templates(self):
        templates = list_templates()
        assert len(templates) > 0
        assert "code_review" in templates

    def test_get_template(self):
        t = get_template("code_review")
        assert t is not None
        assert t.name == "code_review"

    def test_get_nonexistent(self):
        t = get_template("nonexistent")
        assert t is None

    def test_template_names(self):
        names = get_template_names()
        assert isinstance(names, list)
        assert len(names) >= 5

    def test_render_template(self):
        t = get_template("explain")
        result = t.render(topic="recursion", audience="beginner")
        assert "recursion" in result
        assert "beginner" in result

    def test_all_templates_valid(self):
        for name, template in TEMPLATES.items():
            issues = template.validate()
            assert len(issues) == 0, f"Template {name} has issues: {issues}"