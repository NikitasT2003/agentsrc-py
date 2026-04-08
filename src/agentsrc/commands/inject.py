from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Inject instructions into agent guidance files.")
console = Console()


@app.callback(invoke_without_command=True)
def inject(
    file: str = typer.Option(None, "--file", help="Target file (e.g. AGENTS.md, CLAUDE.md)"),
):
    """Update agent instructions with a pointer to .agentsrc/instructions.md."""
    target_files = [file] if file else ["AGENTS.md", "CLAUDE.md", ".clauderc", "README.md"]

    instruction_pointer = """
## Dependency Source Context
This project uses `agentsrc-py` to provide deep context on Python dependencies.
Please refer to [.agentsrc/instructions.md](.agentsrc/instructions.md)
for guidance on using the indexed dependency source code and metadata.
"""

    found = False
    for filename in target_files:
        path = Path(filename)
        if path.exists():
            console.print(f"Injecting into [cyan]{filename}[/cyan]...")
            content = path.read_text(encoding="utf-8")
            if ".agentsrc/instructions.md" in content:
                console.print(f"  [yellow]Pointer already exists in {filename}.[/yellow]")
            else:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(instruction_pointer)
                console.print(f"  [bold green]Successfully updated {filename}[/bold green]")
            found = True

    if not found:
        if file:
            console.print(f"[bold red]Error:[/bold red] Target file {file} not found.")
            raise typer.Exit(1)
        else:
            console.print(
                "[yellow]No common agent guidance files found"
                " (AGENTS.md, CLAUDE.md, etc.).[/yellow]"
            )
            console.print("Creating [bold cyan]AGENTS.md[/bold cyan] with instructions...")
            Path("AGENTS.md").write_text(
                "# Agent Guidance\n" + instruction_pointer, encoding="utf-8"
            )
            console.print("[bold green]Created AGENTS.md[/bold green]")
