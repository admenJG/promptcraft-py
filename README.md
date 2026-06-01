# 馃幆 PromptCraft

[![CI](https://github.com/USER/PromptCraft/actions/workflows/ci.yml/badge.svg)](https://github.com/USER/PromptCraft/actions)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/promptcraft--py.svg)](https://pypi.org/project/promptcraft/)

**A lightweight Python toolkit for prompt engineering, optimization, and evaluation.**

PromptCraft helps developers build, test, and refine prompts for LLMs with a clean, composable API.

## 鉁?Features

- **Prompt Builder** 鈥?Chain instructions, examples, and variables with a fluent API
- **Template System** 鈥?Reusable prompt templates with variable interpolation
- **Optimizer** 鈥?Automatically refine prompts using scoring and iteration
- **Evaluator** 鈥?Score prompt quality across clarity, specificity, and completeness
- **Multi-provider** 鈥?Works with OpenAI, Anthropic, and any OpenAI-compatible API
- **Zero dependencies** 鈥?Core library has no external dependencies

## 馃殌 Quick Start

```bash
pip install promptcraft-py
```

```python
from promptcraft import PromptBuilder, Template

# Build a prompt
prompt = (
    PromptBuilder()
    .system("You are a helpful coding assistant.")
    .instruction("Explain the following concept clearly.")
    .variable("concept", "dependency injection")
    .examples([
        {"input": "What is recursion?", "output": "Recursion is when a function calls itself..."}
    ])
    .build()
)

print(prompt)
```

### Using Templates

```python
from promptcraft import Template

# Define a reusable template
review_template = Template(
    name="code_review",
    system="You are a senior code reviewer.",
    instruction="Review the following {language} code for bugs and improvements.",
    variables=["language", "code"]
)

# Render with specific values
prompt = review_template.render(
    language="Python",
    code="def add(a, b): return a"
)
```

### Optimizing Prompts

```python
from promptcraft import Optimizer

optimizer = Optimizer(
    metric="relevance",
    iterations=5
)

optimized = optimizer.optimize(
    prompt="Explain {topic}",
    test_cases=[
        {"topic": "quantum computing", "expected_keywords": ["qubit", "superposition"]},
        {"topic": "machine learning", "expected_keywords": ["model", "training"]},
    ]
)

print(f"Score improved from {optimized.initial_score:.2f} to {optimized.final_score:.2f}")
```

### Evaluating Prompts

```python
from promptcraft import Evaluator

evaluator = Evaluator()
result = evaluator.score(
    prompt="Write a function that sorts a list",
    criteria=["clarity", "specificity", "completeness"]
)

print(f"Overall: {result.overall:.2f}")
print(f"Clarity: {result.scores['clarity']:.2f}")
```

## 馃摝 Installation

```bash
# From PyPI
pip install promptcraft-py

# From source
git clone https://github.com/USER/PromptCraft.git
cd PromptCraft
pip install -e .
```

## 馃И Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=promptcraft --cov-report=term-missing
```

## 馃摎 Documentation

- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Examples](docs/examples.md)
- [Contributing](CONTRIBUTING.md)

## 馃 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 馃搫 License

This project is licensed under the MIT License 鈥?see [LICENSE](LICENSE) for details.
