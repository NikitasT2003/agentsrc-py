import typer
from rich.console import Console

app = typer.Typer(help="Initialize agentsrc locally.")
console = Console()

@app.callback(invoke_without_command=True)
def init():
    """Create local structure and config."""
    console.print("[green]Initializing .agentsrc structure...[/green]")
    # TODO: Write instructions.md and config.toml
