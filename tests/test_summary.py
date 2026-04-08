from agentsrc.analysis.summary import generate_summary_markdown
from agentsrc.models import ClassDef, FunctionDef, PackageManifest, SymbolMap


def test_generate_summary():
    manifest = PackageManifest(
        name="testpkg",
        version="1.0.0",
        normalized_name="testpkg",
        source_type="sdist",
        artifact_url="",
        artifact_filename="",
        artifact_hash="",
    )
    symbol_map = SymbolMap(
        classes=[ClassDef(name="TargetClient", docstring="The main client")],
        functions=[FunctionDef(name="init_app", docstring="Initialize")],
        all_exports=["TargetClient"],
    )

    md = generate_summary_markdown(manifest, symbol_map)
    assert "# testpkg (1.0.0)" in md
    assert "TargetClient" in md
    assert "init_app" in md
