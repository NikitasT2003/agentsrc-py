from typing import Dict, List, Any
from agentsrc.models import SymbolMap

class BasePlugin:
    def can_handle(self, package_name: str) -> bool:
        return True

    def analyze(self, src_dir: str, symbol_map: SymbolMap) -> Dict[str, Any]:
        return {}

class PydanticPlugin(BasePlugin):
    def can_handle(self, package_name: str) -> bool:
        # We could check if pydantic is a dependency, but for now we just run it
        return True

    def analyze(self, src_dir: str, symbol_map: SymbolMap) -> Dict[str, Any]:
        models = []
        for cls in symbol_map.classes:
            # Simple heuristic: if it inherits from BaseModel
            if any("BaseModel" in base for base in cls.bases):
                models.append({
                    "name": cls.name,
                    "module": cls.module,
                    "type": "PydanticModel"
                })
        return {"models": models}
