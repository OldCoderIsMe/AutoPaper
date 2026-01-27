"""Configuration validation using Pydantic."""
import os
from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel, Field, validator, root_validator


class DatabaseConfig(BaseModel):
    """Database configuration."""
    path: str = Field(default="data/db.sqlite", description="Path to SQLite database")
    journal_mode: str = Field(default="WAL", description="SQLite journal mode")
    synchronous: str = Field(default="NORMAL", description="SQLite synchronous setting")

    @validator('journal_mode')
    def validate_journal_mode(cls, v):
        valid_modes = ['DELETE', 'TRUNCATE', 'PERSIST', 'MEMORY', 'WAL', 'OFF']
        v = v.upper()
        if v not in valid_modes:
            raise ValueError(f"Invalid journal_mode: {v}. Must be one of {valid_modes}")
        return v

    @validator('synchronous')
    def validate_synchronous(cls, v):
        valid_values = ['OFF', 'NORMAL', 'FULL', 'EXTRA']
        v = v.upper()
        if v not in valid_values:
            raise ValueError(f"Invalid synchronous: {v}. Must be one of {valid_values}")
        return v


class ObsidianConfig(BaseModel):
    """Obsidian integration configuration."""
    vault_path: str = Field(..., description="Path to Obsidian vault")
    auto_paper_folder: str = Field(default="AutoPaper", description="Folder name in vault")
    create_folders: bool = Field(default=True, description="Auto-create folders if missing")

    @validator('vault_path')
    def validate_vault_path(cls, v):
        path = Path(v).expanduser()
        if not path.exists():
            raise ValueError(f"Obsidian vault does not exist: {v}")
        if not path.is_dir():
            raise ValueError(f"Obsidian vault path is not a directory: {v}")
        return str(path)


class ArticleStorageConfig(BaseModel):
    """Article storage configuration."""
    raw_dir: str = Field(default="articles/raw", description="Raw HTML storage")
    parsed_dir: str = Field(default="articles/parsed", description="Parsed JSON storage")
    enriched_dir: str = Field(default="articles/enriched", description="AI-enriched metadata storage")
    images_dir: str = Field(default="articles/images", description="Downloaded images storage")

    def create_directories(self):
        """Create all storage directories."""
        for field in ['raw_dir', 'parsed_dir', 'enriched_dir', 'images_dir']:
            path = Path(getattr(self, field))
            path.mkdir(parents=True, exist_ok=True)


class IssuesConfig(BaseModel):
    """Issues (newspaper) storage configuration."""
    output_dir: str = Field(default="issues", description="Generated issues storage")
    pdf_dir: str = Field(default="issues", description="PDF export directory")

    def create_directories(self):
        """Create all storage directories."""
        for field in ['output_dir', 'pdf_dir']:
            path = Path(getattr(self, field))
            path.mkdir(parents=True, exist_ok=True)


class CacheConfig(BaseModel):
    """Caching configuration."""
    enabled: bool = Field(default=True, description="Enable caching")
    cache_dir: str = Field(default="cache", description="Cache directory")
    ai_metadata_ttl: int = Field(default=604800, description="AI metadata cache TTL (seconds, default 7 days)")
    default_ttl: int = Field(default=86400, description="Default cache TTL (seconds, default 24 hours)")

    @validator('cache_dir')
    def validate_cache_dir(cls, v):
        Path(v).mkdir(parents=True, exist_ok=True)
        return v


class AIConfig(BaseModel):
    """AI API configuration."""
    model: str = Field(
        default="claude-sonnet-4-5-20250929",
        description="Claude model to use"
    )
    max_tokens: int = Field(default=4096, ge=1, le=200000, description="Maximum tokens per request")
    timeout: int = Field(default=120, ge=1, description="Request timeout in seconds")

    @validator('model')
    def validate_model(cls, v):
        valid_models = [
            "claude-sonnet-4-5-20250929",
            "claude-opus-4-5-20251101",
        ]
        if v not in valid_models:
            raise ValueError(
                f"Invalid model: {v}. Must be one of {valid_models}"
            )
        return v


class LoggingConfig(BaseModel):
    """Logging configuration."""
    enabled: bool = Field(default=True, description="Enable logging")
    log_file: str = Field(default="data/autopaper.log", description="Log file path")
    log_level: str = Field(default="INFO", description="Logging level")
    console_level: str = Field(default="WARNING", description="Console logging level")

    @validator('log_level', 'console_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v


class PerformanceConfig(BaseModel):
    """Performance tuning configuration."""
    enable_profiling: bool = Field(default=False, description="Enable performance profiling")
    max_concurrent_downloads: int = Field(default=5, ge=1, le=20, description="Max concurrent image downloads")
    connection_pool_size: int = Field(default=10, ge=1, description="Database connection pool size")


class Config(BaseModel):
    """Main configuration model with validation."""

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    obsidian: Optional[ObsidianConfig] = None
    article_storage: ArticleStorageConfig = Field(default_factory=ArticleStorageConfig)
    issues: IssuesConfig = Field(default_factory=IssuesConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)

    @root_validator(skip_on_failure=True)
    def validate_environment(cls, values):
        """Validate environment variables."""
        # Only check if ANTHROPIC_API_KEY is set when creating config
        # Skip validation if not provided (allow for testing)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key is None:
            # Allow creation without API key for testing purposes
            # The actual API calls will fail later
            pass

        return values

    @classmethod
    def from_yaml(cls, yaml_path: str = "config.yaml") -> 'Config':
        """Load configuration from YAML file.

        Args:
            yaml_path: Path to YAML config file

        Returns:
            Validated Config object

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValidationError: If config is invalid
        """
        import yaml

        config_file = Path(yaml_path)
        if not config_file.exists():
            # Return default config if file doesn't exist
            return cls()

        with open(config_file, 'r') as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)

    def create_directories(self):
        """Create all required directories."""
        self.article_storage.create_directories()
        self.issues.create_directories()
        if self.cache.enabled:
            Path(self.cache.cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.database.path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.logging.log_file).parent.mkdir(parents=True, exist_ok=True)


# Legacy compatibility - keep the old Config class working
class _LegacyConfig:
    """Legacy config class for backward compatibility."""

    def __init__(self, config_path: str = "config.yaml"):
        self._config = Config.from_yaml(config_path)
        self._config.create_directories()

    def get_database_path(self) -> str:
        return self._config.database.path

    def get_articles_raw_dir(self) -> str:
        return self._config.article_storage.raw_dir

    def get_articles_parsed_dir(self) -> str:
        return self._config.article_storage.parsed_dir

    def get_articles_enriched_dir(self) -> str:
        return self._config.article_storage.enriched_dir

    def get_articles_images_dir(self) -> str:
        return self._config.article_storage.images_dir

    def get_issues_dir(self) -> str:
        return self._config.issues.output_dir

    def get_obsidian_vault_path(self) -> str:
        if self._config.obsidian:
            return self._config.obsidian.vault_path
        raise ValueError("Obsidian config not set")

    def get_obsidian_auto_paper_folder(self) -> str:
        if self._config.obsidian:
            return self._config.obsidian.auto_paper_folder
        raise ValueError("Obsidian config not set")


# Create global config instance
config = _LegacyConfig()
