# 📜 Changelog

All notable changes to `agentsrc-py` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-04-07
### Added
- **Core Analyzer**: AST-based extraction of functions, classes, decorators, and exceptions.
- **Project Resolver**: Sync dependencies from active `venv`, `uv.lock`, `pyproject.toml`, and `requirements.txt`.
- **Framework Plugin**: Initial plugin for **Pydantic v2** model detection.
- **Agent Instruction Layer**: Generation of `instructions.md` and `sources.json` manifests.
- **CLI**: Rich-powered interface with `init`, `sync`, `inject`, `inspect`, and `query` commands.
- **Query Server**: Local HTTP API for symbol search across indexed packages.
- **Content-Addressed Cache**: Deterministic artifact storage with SHA-256 hash verification.
- **Documentation**: Premium README, Roadmap, Contributing guide, and Code of Conduct.

### Initial Release
*Project bootstrapped with a focus on narrowing the agent hallucination gap.*
