from agentsrc.analysis.public_api import infer_public_api
from agentsrc.models import ClassDef, ModuleDef, SymbolMap


def test_infer_public_api():
    symbol_map = SymbolMap(
        modules=[
            ModuleDef(name="init", docstring=""),
            ModuleDef(name="core.internal", docstring=""),
        ],
        classes=[ClassDef(name="PublicClass"), ClassDef(name="_PrivateClass")],
        all_exports=["PublicClass"],
    )

    enriched_map = infer_public_api(symbol_map)
    assert "PublicClass" in enriched_map.all_exports
    assert "_PrivateClass" not in enriched_map.all_exports
