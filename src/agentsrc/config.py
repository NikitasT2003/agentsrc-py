from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ProjectConfig(BaseModel):
    root: str = "."
    instruction_target: str = "AGENTS.md"

class ResolutionConfig(BaseModel):
    prefer_active_venv: bool = True
    prefer_lockfile: bool = True

class FetchConfig(BaseModel):
    prefer_sdist: bool = True
    verify_hashes: bool = True
    cache_dir: str = ".agentsrc/cache"

class AnalysisConfig(BaseModel):
    enable_plugins: list[str] = ["fastapi", "click", "pydantic", "sqlalchemy", "django"]
    max_files_per_package: int = 5000

class EnrichmentConfig(BaseModel):
    libraries_io: bool = False
    api_key: str = ""

class QueryConfig(BaseModel):
    enable_http: bool = False
    http_host: str = "127.0.0.1"
    http_port: int = 4319

class AgentSrcConfig(BaseSettings):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    resolution: ResolutionConfig = Field(default_factory=ResolutionConfig)
    fetch: FetchConfig = Field(default_factory=FetchConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    enrichment: EnrichmentConfig = Field(default_factory=EnrichmentConfig)
    query: QueryConfig = Field(default_factory=QueryConfig)

    model_config = SettingsConfigDict(toml_file=Path(".agentsrc/config.toml"))

def load_config() -> AgentSrcConfig:
    import tomli # if python < 3.11, or use tomllib for >= 3.11
    # Actually pydantic-settings uses tomllib or tomli depending on version
    return AgentSrcConfig()
