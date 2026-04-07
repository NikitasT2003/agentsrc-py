# Contributing to agentsrc-py

We welcome contributions! This project uses `uv` for fast, reproducible Python development.

## Setup

1. Install [uv](https://github.com/astral-sh/uv).
2. Clone the repository: `git clone https://github.com/NikitasT2003/agentsrc-py.git`
3. Install dependencies: `uv sync`
4. Run tests to verify setup: `uv run pytest`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes.
3. Verify formatting and linting: `uv run ruff check .`
4. Run tests: `uv run pytest`
5. Push your branch and open a Pull Request.

## Pull Request Guidelines

- Ensure all tests pass.
- Add new tests for new features.
- Update documentation in `README.md` if necessary.
- We follow the [MIT License](LICENSE).
