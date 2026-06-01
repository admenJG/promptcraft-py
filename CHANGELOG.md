# Changelog

All notable changes to PromptCraft will be documented in this file.

## [0.2.1] - 2026-06-01

### Added
- PromptBuilder.to_json() for JSON serialization
- PromptBuilder.from_dict() and from_json() for deserialization
- Roundtrip support (build -> to_json -> from_json -> build)
- Additional edge case tests

## [0.2.0] - 2026-06-01

### Added
- CLI tool with eval, score, optimize, and build commands
- Built-in prompt template library (8 templates)
- Prompt safety validator with injection detection
- Batch validation support

## [0.1.0] - 2026-06-01

### Added
- PromptBuilder with fluent API
- Template system with variable interpolation
- Optimizer for iterative prompt refinement
- Evaluator with multi-criteria quality assessment
- Scorer with weighted scoring
- Comprehensive test suite
- GitHub Actions CI/CD