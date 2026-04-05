import typer
from rich.console import Console
from typing import Optional

app = typer.Typer(help="Resolves dependencies and fetches them.")
console = Console()

@app.callback(invoke_without_command=True)
def sync(
    package: Optional[str] = typer.Option(None, "--package", help="Specific package to sync"),
    all: bool = typer.Option(False, "--all", help="Sync all packages"),
    force: bool = typer.Option(False, "--force", help="Force resync"),
):
    """Sync target dependencies and extract symbols."""
    if package:
        console.print(f"Syncing package: [bold blue]{package}[/bold blue]")
    elif all:
        console.print("Syncing all packages from environment/lockfile.")
    else:
        console.print("[yellow]Please specify --package or --all[/yellow]")
