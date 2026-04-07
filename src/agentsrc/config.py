from pathlib import Path
from typing import Tuple, Type

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


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
    max_jobs: int = 4
    exclude_dirs: list[str] = [
        "tests",
        "test",
        "docs",
        "benchmarks",
        "examples",
        "site-packages",
        "venv",
        ".venv",
    ]


class EnrichmentConfig(BaseModel):
    libraries_io: bool = False
    api_key: str = ""


class QueryConfig(BaseModel):
    enable_http: bool = False
    http_host: str = "127.0.0.1"
    http_port: int = 4319


class AgentSrcConfig(BaseSettings):
    model_config = SettingsConfigDict(toml_file=Path(".agentsrc/config.toml"))

    project: ProjectConfig = Field(default_factory=ProjectConfig)
    resolution: ResolutionConfig = Field(default_factory=ResolutionConfig)
    fetch: FetchConfig = Field(default_factory=FetchConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    enrichment: EnrichmentConfig = Field(default_factory=EnrichmentConfig)
    query: QueryConfig = Field(default_factory=QueryConfig)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            TomlConfigSettingsSource(settings_cls),
        )


def load_config() -> AgentSrcConfig:
    """Load configuration from .agentsrc/config.toml or environment."""
    return AgentSrcConfig()
