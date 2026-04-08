import typer
from rich.console import Console
from rich.markdown import Markdown

from agentsrc.storage.writer import StorageWriter

app = typer.Typer(help="Show summary for an indexed package.")
console = Console()


@app.callback(invoke_without_command=True)
def main(package_name: str = typer.Argument(..., help="Name of the package to inspect")):
    """
    Show the semantic summary for a synced package.
    """
    writer = StorageWriter()
    store_path = writer.pypi_dir

    # Logic to find the package directory (latest version)
    pkg_dir = store_path / package_name
    if not pkg_dir.exists():
        console.print(
            f"[bold red]Error:[/bold red] Package [cyan]{package_name}[/cyan] is not synced."
        )
        console.print("Run [bold]agentsrc sync --package " + package_name + "[/bold] first.")
        raise typer.Exit(code=1)

    # Find latest version
    versions = [d for d in pkg_dir.iterdir() if d.is_dir()]
    if not versions:
        console.print(
            f"[bold red]Error:[/bold red] No versions found for [cyan]{package_name}[/cyan]."
        )
        raise typer.Exit(code=1)

    versions.sort(reverse=True)
    latest_version = versions[0]

    summary_path = latest_version / "summary.md"
    if not summary_path.exists():
        console.print(f"[yellow]No summary found for {package_name}@{latest_version.name}[/yellow]")
        return

    console.print(f"[bold blue]Inspection: {package_name}@{latest_version.name}[/bold blue]\n")
    with open(summary_path, "r", encoding="utf-8") as f:
        md = Markdown(f.read())
        console.print(md)
