from agentsrc.models import SymbolMap, ClassDef, FunctionDef, ExceptionDef, ModuleDef

def test_symbol_map_serialization():
    symbol_map = SymbolMap(
        modules=[ModuleDef(name="core", docstring="Core module")],
        classes=[ClassDef(name="Client", bases=["object"], methods=["__init__"])],
        functions=[FunctionDef(name="run", args=["self", "cmd"])],
        exceptions=[ExceptionDef(name="FetchError", bases=["Exception"])],
        constants=["VERSION"],
        reexports=["retry"],
        all_exports=["Client", "run"]
    )
    
    data = symbol_map.model_dump()
    assert data["classes"][0]["name"] == "Client"
    assert data["exceptions"][0]["bases"] == ["Exception"]
