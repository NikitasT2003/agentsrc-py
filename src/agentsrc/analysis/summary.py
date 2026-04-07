from agentsrc.models import PackageManifest, SymbolMap


def generate_summary_markdown(manifest: PackageManifest, symbol_map: SymbolMap) -> str:
    md = []
    md.append(f"# {manifest.name} ({manifest.version})")
    md.append("\n## Public API Exports")
    if symbol_map.all_exports:
        for exp in symbol_map.all_exports:
            md.append(f"- `{exp}`")
    else:
        md.append("_No explicit public exports detected._")

    md.append("\n## Key Classes")
    if symbol_map.classes:
        for c in symbol_map.classes:
            doc = c.docstring.split("\\n")[0] if c.docstring else "No description"
            md.append(f"- **{c.name}**: {doc}")
            if c.methods:
                md.append(f"  - Methods: {', '.join(c.methods)}")
    else:
        md.append("_No classes detected._")

    md.append("\n## Key Functions")
    if symbol_map.functions:
        for f in symbol_map.functions:
            doc = f.docstring.split("\\n")[0] if f.docstring else "No description"
            md.append(f"- **{f.name}**: {doc}")
    else:
        md.append("_No functions detected._")

    md.append("\n## Exception Model")
    if symbol_map.exceptions:
        for e in symbol_map.exceptions:
            md.append(f"- **{e.name}**")
    else:
        md.append("_No custom exceptions detected._")

    return "\n".join(md)
