import typer

from agentsrc.commands import init, sync, inject, query, inspect

app = typer.Typer(
    help="[bold cyan]agentsrc-py[/bold cyan] - Extract source code signals from installed Python packages",
    rich_markup_mode="rich",
)

app.add_typer(init.app, name="init")
app.add_typer(sync.app, name="sync")
app.add_typer(inject.app, name="inject")
app.add_typer(query.app, name="query")
app.add_typer(inspect.app, name="inspect")

if __name__ == "__main__":
    app()
