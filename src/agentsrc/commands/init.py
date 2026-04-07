import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="Initialize agentsrc locally.")
console = Console()


@app.callback(invoke_without_command=True)
def init():
    """Create local structure and config."""
    console.print("[green]Initializing .agentsrc structure...[/green]")
    from agentsrc.storage.writer import StorageWriter

    writer = StorageWriter()
    writer.initialize_structure()

    config_toml = """[project]
root = "."
instruction_target = "AGENTS.md"

[resolution]
prefer_active_venv = true
prefer_lockfile = true

[fetch]
prefer_sdist = true
verify_hashes = true
cache_dir = ".agentsrc/cache"

[analysis]
enable_plugins = ["fastapi", "click", "pydantic", "sqlalchemy", "django"]
max_files_per_package = 5000
max_jobs = 4
exclude_dirs = ["tests", "test", "docs", "benchmarks", "examples", "site-packages", "venv", ".venv"]

[enrichment]
libraries_io = false
api_key = ""

[query]
enable_http = false
http_host = "127.0.0.1"
http_port = 4319
"""
    instructions_md = """# Dependency Source Context

This project includes indexed source snapshots for installed Python packages under `.agentsrc/`.

When answering questions about dependency behavior:
1. Check `.agentsrc/sources.json`.
2. Read the package `summary.md` and `manifest.json` first.
3. Use `symbols.json` to find relevant modules/classes/functions.
4. Read raw source files only for the narrow area needed.
5. Prefer local source over generic docs when behavior is ambiguous.
6. Note version-specific behavior explicitly in your answer.
"""
    try:
        writer.write_config(config_toml)
        writer.write_instructions(instructions_md)
        console.print(
            Panel(
                "[bold green]Project initialized successfully.[/bold green]\n\n"
                "Next steps:\n"
                "1. Run [cyan]agentsrc sync --all[/cyan] to index dependencies.\n"
                "2. Run [cyan]agentsrc inject[/cyan] to add pointers for coding agents.",
                title="[bold blue]Agentsrc-py[/bold blue]",
                expand=False,
            )
        )
    except FileExistsError as e:
        console.print(f"[yellow]Initialization skipped:[/yellow] {str(e)}")
