"""Command-line interface for PromptCraft."""

import sys
import json
from promptcraft.builder import PromptBuilder
from promptcraft.evaluator import Evaluator
from promptcraft.scorer import Scorer
from promptcraft.optimizer import Optimizer


def main():
    """Main entry point for the promptcraft CLI."""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "eval":
        handle_eval()
    elif command == "score":
        handle_score()
    elif command == "optimize":
        handle_optimize()
    elif command == "build":
        handle_build()
    elif command in ("--version", "-v"):
        from promptcraft import __version__
        print(f"promptcraft v{__version__}")
    elif command in ("--help", "-h"):
        print_usage()
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("""promptcraft - Prompt Engineering Toolkit

Usage:
  promptcraft eval <prompt>       Evaluate a prompt's quality
  promptcraft score <prompt>      Score a prompt with detailed metrics
  promptcraft optimize <prompt>   Optimize a prompt iteratively
  promptcraft build               Build a prompt interactively

Options:
  --version, -v    Show version
  --help, -h       Show this help message
""")


def handle_eval():
    """Handle the eval command."""
    if len(sys.argv) < 3:
        print("Usage: promptcraft eval <prompt>")
        sys.exit(1)
    prompt = " ".join(sys.argv[2:])
    evaluator = Evaluator()
    result = evaluator.score(prompt)
    print(f"Overall Score: {result.overall:.2f}")
    print(f"Word Count: {result.word_count}")
    print(f"Length: {result.prompt_length} chars")
    print("\nCriteria Scores:")
    for criterion, score in result.scores.items():
        print(f"  {criterion}: {score:.2f}")
    print("\nSuggestions:")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")


def handle_score():
    """Handle the score command."""
    if len(sys.argv) < 3:
        print("Usage: promptcraft score <prompt>")
        sys.exit(1)
    prompt = " ".join(sys.argv[2:])
    scorer = Scorer()
    score = scorer.score(prompt)
    print(f"Score: {score:.4f}")


def handle_optimize():
    """Handle the optimize command."""
    if len(sys.argv) < 3:
        print("Usage: promptcraft optimize <prompt>")
        sys.exit(1)
    prompt = " ".join(sys.argv[2:])
    optimizer = Optimizer(iterations=10)
    result = optimizer.optimize(prompt)
    print(f"Initial Score: {result.initial_score:.2f}")
    print(f"Final Score: {result.final_score:.2f}")
    print(f"Iterations: {result.iterations}")
    print(f"\nOptimized Prompt:\n{result.optimized_prompt}")


def handle_build():
    """Handle the build command."""
    print("Interactive Prompt Builder")
    print("=" * 40)
    system = input("System message (optional): ").strip()
    instruction = input("Instruction: ").strip()
    context = input("Context (optional): ").strip()

    builder = PromptBuilder()
    if system:
        builder = builder.system(system)
    if instruction:
        builder = builder.instruction(instruction)
    if context:
        builder = builder.context(context)

    result = builder.build()
    print(f"\nGenerated Prompt:\n{result}")


if __name__ == "__main__":
    main()