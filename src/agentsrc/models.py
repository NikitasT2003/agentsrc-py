from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PackageManifest(BaseModel):
    name: str
    version: str
    normalized_name: str
    ecosystem: str = "pypi"
    source_type: str
    artifact_url: str
    artifact_filename: str
    artifact_hash: str
    resolved_from: str = "manual"
    requires_python: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = None
    project_urls: Dict[str, str] = {}
    top_level_modules: List[str] = []
    entrypoints_detected: List[str] = []
    frameworks_detected: List[str] = []
    generated_at: str = ""


class ModuleDef(BaseModel):
    name: str
    docstring: Optional[str] = None


class ClassDef(BaseModel):
    name: str
    module: Optional[str] = None
    docstring: Optional[str] = None
    bases: List[str] = []
    methods: List[str] = []


class FunctionDef(BaseModel):
    name: str
    module: Optional[str] = None
    docstring: Optional[str] = None
    args: List[str] = []
    is_async: bool = False


class ExceptionDef(BaseModel):
    name: str
    docstring: Optional[str] = None
    bases: List[str] = []


class SymbolMap(BaseModel):
    modules: List[ModuleDef] = []
    classes: List[ClassDef] = []
    functions: List[FunctionDef] = []
    exceptions: List[ExceptionDef] = []
    constants: List[str] = []
    reexports: List[str] = []
    all_exports: List[str] = []
    framework_data: Dict[str, Any] = {}


class ProjectPackage(BaseModel):
    name: str
    version: str
    ecosystem: str = "pypi"
    path: str
    manifest: str
    summary: str
    symbols: str


class ProjectIndex(BaseModel):
    version: int = 1
    generated_at: str
    packages: List[ProjectPackage] = []
