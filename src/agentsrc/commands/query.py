import typer
from rich.console import Console

from agentsrc.config import load_config
from agentsrc.query.server import start_server
import json
from pathlib import Path
from rich.table import Table

app = typer.Typer(help="Query symbols and package metadata via a local API.")
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    host: str = typer.Option(
        None, "--host", help="Host to bind the server to (defaults to config)."
    ),
    port: int = typer.Option(
        None, "--port", help="Port to bind the server to (defaults to config)."
    ),
):
    """
    Start the local agentsrc query server.
    """
    if ctx.invoked_subcommand is not None:
        return

    config = load_config()
    server_host = host or config.query.http_host
    server_port = port or config.query.http_port

    console.print("[bold green]Starting Query Server...[/bold green]")
    console.print(f"Address: [cyan]http://{server_host}:{server_port}[/cyan]")
    console.print("Press [bold red]Ctrl+C[/bold red] to stop.")

    try:
        start_server(server_host, server_port)
    except Exception as e:
        console.print(f"[bold red]Error starting server:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def search(query: str = typer.Argument(..., help="Search query for symbols")):
    """
    Search for symbols across indexed packages.
    """
    from agentsrc.storage.writer import StorageWriter

    writer = StorageWriter()
    store_path = writer.pypi_dir

    if not store_path.exists():
        console.print("[yellow]No packages indexed yet.[/yellow]")
        return

    results = []
    query_lower = query.lower()

    for pkg_dir in store_path.iterdir():
        if not pkg_dir.is_dir():
            continue
        for version_dir in pkg_dir.iterdir():
            if not version_dir.is_dir():
                continue
            symbols_path = version_dir / "symbols.json"
            if not symbols_path.exists():
                continue

            try:
                with open(symbols_path, "r", encoding="utf-8") as f:
                    symbols_data = json.load(f)
                    for category in ["classes", "functions", "exceptions"]:
                        for item in symbols_data.get(category, []):
                            name = item.get("name", "")
                            if query_lower in name.lower():
                                results.append(
                                    {
                                        "package": pkg_dir.name,
                                        "version": version_dir.name,
                                        "type": category[:-1].capitalize(),
                                        "name": name,
                                    }
                                )
            except:
                continue

    if not results:
        console.print(f"No results found for '[bold]{query}[/bold]'.")
        return

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Package", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Symbol", style="bold yellow")

    for res in results[:20]:  # Limit to 20 for CLI
        table.add_row(res["package"], res["version"], res["type"], res["name"])

    console.print(table)
    if len(results) > 20:
        console.print(f"\n[dim]Showing 20 of {len(results)} results.[/dim]")
