# Contributing to PromptCraft

Thank you for considering contributing to PromptCraft!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/PromptCraft.git
   cd PromptCraft
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request with a clear description

## Reporting Issues

Use GitHub Issues to report bugs or request features. Please include:
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior
