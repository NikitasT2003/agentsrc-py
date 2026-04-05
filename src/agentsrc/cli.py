import typer

from agentsrc.commands import init, sync

app = typer.Typer(help="agentsrc-py - Extract source code signals from installed Python packages")

app.add_typer(init.app, name="init")
app.add_typer(sync.app, name="sync")

if __name__ == "__main__":
    app()
