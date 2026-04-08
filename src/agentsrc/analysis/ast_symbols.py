import ast
import warnings
from pathlib import Path

from agentsrc.models import ClassDef, ExceptionDef, FunctionDef, ModuleDef, SymbolMap


class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self, exclude_dirs: list[str] | None = None, plugins: list | None = None):
        self.symbol_map = SymbolMap()
        self.current_module = None
        self.exclude_dirs = exclude_dirs or []
        self.plugins = plugins or []

    def analyze_directory(self, src_dir: str) -> SymbolMap:
        src_path = Path(src_dir)
        for filepath in src_path.rglob("*.py"):
            # Check if any parent directory is in exclude_dirs
            if any(part in self.exclude_dirs for part in filepath.parts):
                continue
            self._analyze_file(filepath, src_path)

        # Run plugins to enrich the symbol_map
        for plugin in self.plugins:
            findings = plugin.analyze(src_dir, self.symbol_map)
            # For v1, we can attach findings to the symbol_map or manifest
            # Let's say we add them to a 'frameworks' field in SymbolMap
            if findings:
                if not hasattr(self.symbol_map, "framework_data"):
                    self.symbol_map.framework_data = {}
                self.symbol_map.framework_data.update(findings)

        return self.symbol_map

    def _analyze_file(self, filepath: Path, src_root: Path):
        try:
            content = filepath.read_text(encoding="utf-8")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                tree = ast.parse(content, filename=str(filepath))

            rel_path = filepath.relative_to(src_root)
            mod_name = str(rel_path.with_suffix("")).replace("\\", ".").replace("/", ".")
            if mod_name.endswith(".__init__"):
                mod_name = mod_name[:-9]

            docstring = ast.get_docstring(tree)
            self.symbol_map.modules.append(ModuleDef(name=mod_name, docstring=docstring))

            self.current_module = mod_name
            self.visit(tree)
            self.current_module = None
        except Exception:
            pass  # Skip unparseable files in v1

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        docstring = ast.get_docstring(node)
        methods = [
            m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        is_exception = (
            any("Exception" in b or "Error" in b for b in bases)
            or node.name.endswith("Error")
            or node.name.endswith("Exception")
        )

        if is_exception:
            self.symbol_map.exceptions.append(
                ExceptionDef(name=node.name, docstring=docstring, bases=bases)
            )
        else:
            self.symbol_map.classes.append(
                ClassDef(
                    name=node.name,
                    module=self.current_module,
                    docstring=docstring,
                    bases=bases,
                    methods=methods,
                )
            )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._visit_func(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._visit_func(node, is_async=True)

    def _visit_func(self, node, is_async: bool):
        # Only add module-level functions (not methods)
        # Note: in a simple visitor, everything is visited.
        # But we only want top-level. For V1, we'll accept it as heuristics.
        args = [a.arg for a in node.args.args]
        if args and args[0] in ("self", "cls"):
            pass  # Skip methods (has self/cls arg)
        else:
            self.symbol_map.functions.append(
                FunctionDef(
                    name=node.name,
                    module=self.current_module,
                    docstring=ast.get_docstring(node),
                    args=args,
                    is_async=is_async,
                )
            )
        self.generic_visit(node)
