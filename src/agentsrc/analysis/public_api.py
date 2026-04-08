from agentsrc.models import SymbolMap


def infer_public_api(symbol_map: SymbolMap) -> SymbolMap:
    # Heuristics:
    # 1. If explicit __all__ exports exist, trust them.
    # Otherwise, append non-underscored names as fallback.

    public_exports = set(symbol_map.all_exports)

    if not public_exports:
        for c in symbol_map.classes:
            if not c.name.startswith("_"):
                public_exports.add(c.name)
        for f in symbol_map.functions:
            if not f.name.startswith("_"):
                public_exports.add(f.name)
        for e in symbol_map.exceptions:
            if not e.name.startswith("_"):
                public_exports.add(e.name)

    symbol_map.all_exports = list(public_exports)
    return symbol_map
