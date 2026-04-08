# 🗺️ agentsrc-py Roadmap

The goal of `agentsrc-py` is to become the definitive source of truth for AI coding agents operating in the Python ecosystem.

---

## ⚡ Phase 1: Foundation (Current - v0.1.x)
- [x] **AST Analysis Engine**: Extraction of classes, functions, and docstrings.
- [x] **uv Integration**: Direct support for `uv.lock` and `uv` commands.
- [x] **Framework Plugins**: Basic support for FastAPI and Pydantic.
- [x] **Local Cache**: Content-addressed storage for package sources.

## 🚀 Phase 2: Interoperability (v0.2.x)
- [ ] **MCP Server (Model Context Protocol)**: Direct integration with Claude Code and other MCP-aware agents.
- [ ] **Lockfile Expansion**: Support for `poetry.lock`, `requirements.txt`, and `pipenv`.
- [ ] **Transitive Dependencies**: Optional recursive syncing of the full dependency tree.
- [ ] **C-Extension Support**: Fallback strategies for libraries with non-Python internals.

## 🧠 Phase 3: Semantic Intelligence (v0.3.x+)
- [ ] **Call Graph Analysis**: Mapping how symbols are used across package boundaries.
- [ ] **Exception Propagation Mapping**: Deep analysis of potential error paths.
- [ ] **Plugin Ecosystem**: Open API for community-contributed framework analyzers.
- [ ] **Agent Memory**: Local "hotspot" indexing to cache frequently asked dependency details.

---

## 🏗️ Future Vision
- Support for **TypeScript (npm)** and **Rust (cargo)**.
- Distribution as an **Agentic Action/Tool** for hosted platforms (GitHub Copilot Extensions).
