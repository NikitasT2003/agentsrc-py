import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

import typer
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

app = typer.Typer(help="Resolves dependencies and fetches them.")
console = Console()


def _sync_package(
    package_name: str,
    version: Optional[str] = None,
    quiet: bool = False,
    exclude_dirs: Optional[List[str]] = None,
) -> bool:
    from agentsrc.analysis.ast_symbols import ASTAnalyzer
    from agentsrc.analysis.public_api import infer_public_api
    from agentsrc.analysis.summary import generate_summary_markdown
    from agentsrc.fetch.artifacts import ArtifactFetcher
    from agentsrc.fetch.cache import CacheManager
    from agentsrc.fetch.unpack import extract_archive
    from agentsrc.providers.pypi import PyPIClient
    from agentsrc.storage.writer import StorageWriter

    try:
        client = PyPIClient()
        manifest = client.get_package_metadata(package_name, version=version)
        if not quiet:
            console.print(f"Resolved [green]{package_name}@{manifest.version}[/green]")

        cache = CacheManager()
        fetcher = ArtifactFetcher(cache)
        artifact_path = fetcher.download(manifest)
        if not quiet:
            console.print(f"  Downloaded: [cyan]{artifact_path.name}[/cyan]")

        writer = StorageWriter()
        writer.write_manifest(manifest)

        unpack_dir = writer.pypi_dir / manifest.name / manifest.version / "src"
        if not unpack_dir.exists():
            extract_archive(
                str(artifact_path), str(unpack_dir), original_filename=manifest.artifact_filename
            )

        status_msg = f"  Analyzing {package_name}..."
        with (
            console.status(status_msg) if not quiet else open(os.devnull, "w")
        ):  # fallback for quiet
            from agentsrc.analysis.plugins.pydantic import PydanticPlugin
            
            plugins = [PydanticPlugin()]
            analyzer = ASTAnalyzer(exclude_dirs=exclude_dirs, plugins=plugins)
            symbol_map = analyzer.analyze_directory(str(unpack_dir))

            symbol_map = infer_public_api(symbol_map)
            summary_md = generate_summary_markdown(manifest, symbol_map)

            writer.write_analysis(manifest, symbol_map, summary_md)
        return True
    except Exception as e:
        console.print(f"  [bold red]Sync failed for {package_name}:[/bold red] {str(e)}")
        return False


@app.callback(invoke_without_command=True)
def sync(
    package: Optional[str] = typer.Option(None, "--package", help="Specific package to sync"),
    all: bool = typer.Option(False, "--all", help="Sync all packages"),
    force: bool = typer.Option(False, "--force", help="Force resync"),
    jobs: Optional[int] = typer.Option(None, "--jobs", "-j", help="Number of concurrent sync jobs"),
):
    """Sync target dependencies and extract symbols."""
    if package:
        from agentsrc.config import load_config

        config = load_config()
        console.print(f"Syncing package: [bold blue]{package}[/bold blue]")
        if _sync_package(package, exclude_dirs=config.analysis.exclude_dirs):
            console.print(f"[bold green]✓ Successfully synced {package}[/bold green]")
        else:
            raise typer.Exit(1)
    elif all:
        from agentsrc.config import load_config
        from agentsrc.resolver import ProjectResolver

        config = load_config()
        resolver = ProjectResolver()
        packages = resolver.resolve_all(
            prefer_venv=config.resolution.prefer_active_venv,
            prefer_lockfile=config.resolution.prefer_lockfile,
        )

        # resolve_all already filters out the current project, so no extra filtering is needed here.

        if not packages:
            console.print("[yellow]No packages found to sync.[/yellow]")
            return

        console.print(f"Found [bold blue]{len(packages)}[/bold blue] packages to sync.")

        exclude_dirs = config.analysis.exclude_dirs
        max_workers = jobs if jobs is not None else config.analysis.max_jobs

        success_count = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            total_task = progress.add_task("[cyan]Syncing dependencies...", total=len(packages))

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(
                        _sync_package,
                        pkg["name"],
                        pkg["version"],
                        quiet=True,
                        exclude_dirs=exclude_dirs,
                    ): pkg["name"]
                    for pkg in packages
                }

                for future in as_completed(futures):
                    pkg_name = futures[future]
                    try:
                        if future.result():
                            success_count += 1
                    except Exception as e:
                        console.print(f"[bold red]Error syncing {pkg_name}:[/bold red] {e}")

                    progress.advance(total_task)
                    # Update description with current progress
                    progress.update(
                        total_task,
                        description=f"[cyan]Syncing dependencies ({success_count}/{len(packages)})...",
                    )

        console.print(
            f"\n[bold green]Sync complete: {success_count}/{len(packages)} succeeded.[/bold green]"
        )
    else:
        console.print("[yellow]Please specify --package or --all[/yellow]")
