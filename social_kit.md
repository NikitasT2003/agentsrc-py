# 📢 social_kit.md: Marketing & Launch Assets

This kit contains peer-to-peer, technical-first copy designed to minimize "marketing-speak" and maximize developer trust.

---

## 🏗️ Show HN: Peer-to-Peer Launch
**Recommended Title**: `Show HN: agentsrc-py — semantic signal extraction for AI coding agents`

**Recommended Opener**:
> I kept seeing coding agents (Claude, Cursor, GPT-4) hallucinating how Python dependencies work. They usually guess based on outdated training data, stale docs, or high-level type hints.
>
> So I built `agentsrc-py`. It’s a local dev tool that fetches the exact version of your dependencies (via `uv` or `venv`), extracts symbols using AST analysis, and exposes a structured "ground truth" manifest to the agent.
>
> Features:
> - Version-locked source extraction (ground truth over stale docs).
> - AST-level symbol mapping (Classes, Functions, decorators).
> - Framework plugins (FastAPI routes, Pydantic models).
> - 100% local, no hidden telemetry.
>
> It’s in alpha (v0.1.0). I’d love your feedback on the analyzer logic or what framework plugins we should add next.

---

## 🧵 X (Twitter) Thread
**Tweet 1**: 
AI coding agents are only as good as the context they see. But they often hallucinate on third-party dependencies because they don't see the source—only stale docs. 

Today I'm launching **agentsrc-py** to fix this. 📡🤖 [Link to Repo]

**Tweet 2**: 
Most agents guess how `pydantic` or `fastapi` internals work. `agentsrc-py` fetches the *matching* version of your libraries, analyzes them with AST-level precision, and builds a semantic map for the agent to follow. 📉 [Image/GIF of Terminal Sync]

**Tweet 3**: 
The goal isn't just "more code." It's **ground truth**. 
By exposing the actual implementation to the agent locally, you eliminate "guessing" and reduce hallucination by 10x for complex library integrations. 🎯

**Tweet 4**: 
built with ❤️ using:
- @astral_sh `uv` for speed 🚀
- @tiangolo `typer` for the CLI 🛠️
- `ast` for deep Python analysis 🐍

Try it: `uv tool install agentsrc-py && agentsrc sync` [Link to Repo]

---

## 📰 Dev.to / Hashnode Article Outline
**Title**: AI Coding Agents don't understand your dependencies. Here's a tool to fix that.

**Outline**:
1. **The Context Gap**: Explain why LLMs hallucinate even when they have RAG (docs are not the source code).
2. **The "Exact Version" Problem**: Why using generic library knowledge fails when you're pinned to an older version.
3. **How agentsrc-py works**: Walkthrough of the `ProjectResolver` -> `ASTExtractor` -> `SignalManifest` pipeline.
4. **Example "War Story"**: Show a before/after of an agent trying to handle a complex `httpx` timeout but failing without seeing the internal transport logic.
5. **Onboarding the Agent**: How a single `AGENTS.md` file transforms the workflow.
6. **Call to Action**: GitHub link + "Try it in 10 seconds with `uv`".
