# 🤖 AI Agent Instructions (AGENTS.md)

This project, `agentsrc-py`, provides high-fidelity source context for AI coding agents. It extracts semantic signals (symbols, relationships, behavioral logic) from Python dependencies.

## 🏗️ Technical Stack
- **Language**: Python 3.11+
- **Dev Tool**: [uv](https://github.com/astral-sh/uv) (Use `uv sync`, `uv run`, `uv tool install`)
- **CLI Framework**: Typer & Rich
- **Analysis**: AST-level parsing (`ast`) with plugin-based framework support (FastAPI, Pydantic).

## 🛠️ Project Source Context
Source-level context for all dependencies is stored locally under `.agentsrc/`.

### 🧭 Key Information Sources
- **`.agentsrc/sources.json`**: Global index of all fetched packages.
- **`.agentsrc/pypi/{package}/{version}/`**:
    - `summary.md`: High-level behavior overview.
    - `symbols.json`: AST-extracted classes, functions, and metadata.
    - `src/`: Raw source code of the dependency.
    - `manifest.json`: Version-locked metadata.

## 🚀 Execution Commands
When helping the user, use these commands:
- **`agentsrc init`**: Bootstrap the project-local context.
- **`agentsrc sync`**: Resolve and index all dependencies (runs `ProjectResolver` + `PackageFetcher`).
- **`agentsrc query "..."`**: Perform a semantic search across the generated index.
- **`uv run pytest`**: Run the test suite.

## ⚠️ Boundaries & Constraints
- **DO NOT** modify files in the `.agentsrc/` directory manually; they are tool-generated.
- **DO NOT** commit the `.agentsrc/` directory to Git (should be in `.gitignore`).
- **DO NOT** modify `pyproject.toml` without verifying dependency compatibility via `uv sync`.

## 🧠 Code Style & Patterns
- Follow **Pydantic v2** patterns for all data models (`src/agentsrc/models.py`).
- Use **Typer** for all CLI interaction (`src/agentsrc/cli.py`).
- Maintain **AST-walking pure logic** in `src/agentsrc/analysis/`.
- Ensure all new features are testable via `pytest` (`tests/`).

---
*This file is the single source of truth for AI agents (Claude, GPT, Cursor, Roo-Code).*
