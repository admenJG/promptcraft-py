# Changelog

All notable changes to PromptCraft will be documented in this file.

## [0.2.0] - 2026-06-01

### Added
- CLI tool with `eval`, `score`, `optimize`, and `build` commands
- Built-in prompt template library (8 templates: code review, summarize, explain, translate, debug, write tests, API docs, refactor)
- Prompt safety validator with injection detection
- Batch validation support
- Entry point configuration for `promptcraft` command

### Changed
- Renamed package to `promptcraft-py` (original name unavailable on PyPI)
- Updated all templates with output format specifications

## [0.1.0] - 2026-06-01

### Added
- PromptBuilder with fluent API for prompt construction
- Template system with variable interpolation and validation
- Optimizer for iterative prompt refinement
- Evaluator with multi-criteria quality assessment
- Scorer with weighted scoring and customizable metrics
- Comprehensive test suite (36 tests)
- GitHub Actions CI/CD pipeline
- Documentation: README, Getting Started, Contributing guide
- MIT License