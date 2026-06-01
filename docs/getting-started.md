# Getting Started with PromptCraft

## Installation

```bash
pip install promptcraft
```

## Your First Prompt

```python
from promptcraft import PromptBuilder

prompt = (
    PromptBuilder()
    .system("You are a Python expert.")
    .instruction("Explain {concept} with a code example.")
    .variable("concept", "decorators")
    .build()
)

print(prompt)
```

## Creating Templates

```python
from promptcraft import Template

template = Template(
    name="explain_concept",
    system="You are a technical educator.",
    instruction="Explain {topic} to a {audience}.",
    variables=["topic", "audience"],
    output_format="Use headers and code blocks."
)

prompt = template.render(topic="APIs", audience="beginner")
```

## Evaluating Prompts

```python
from promptcraft import Evaluator

evaluator = Evaluator()
result = evaluator.score(prompt, criteria=["clarity", "specificity"])
print(f"Score: {result.overall:.2f}")
for suggestion in result.suggestions:
    print(f"  - {suggestion}")
```

## Optimizing Prompts

```python
from promptcraft import Optimizer

optimizer = Optimizer(iterations=10)
result = optimizer.optimize(
    prompt="Explain {topic}",
    test_cases=[{"topic": "AI"}]
)
print(f"Improved from {result.initial_score:.2f} to {result.final_score:.2f}")
```

## Next Steps

- Check out the [API Reference](api-reference.md) for full details
- See [Examples](examples.md) for more use cases
- Read the [Contributing Guide](../CONTRIBUTING.md) to help improve PromptCraft
