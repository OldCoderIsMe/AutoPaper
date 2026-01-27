"""Configuration management for AutoPaper."""
import os
from pathlib import Path
from typing import Any, Dict, List

import yaml
from dotenv import load_dotenv


class Config:
    """Configuration manager for AutoPaper."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize configuration.

        Args:
            config_path: Path to configuration file
        """
        # Load environment variables from .env file
        load_dotenv()

        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.

        Args:
            key: Configuration key (supports dot notation, e.g., 'obsidian.vault_path')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            # Substitute environment variables
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                value = os.getenv(env_var, default)

            if value is None:
                return default

        return value

    def get_database_path(self) -> str:
        """Get database path.

        Returns:
            Path to SQLite database
        """
        return self.get("database_path", "data/db.sqlite")

    def get_obsidian_vault_path(self) -> str:
        """Get Obsidian vault path.

        Returns:
            Path to Obsidian vault
        """
        path = self.get("obsidian.vault_path", "")
        # Expand ~ to home directory
        return os.path.expanduser(path)

    def get_obsidian_auto_paper_folder(self) -> str:
        """Get AutoPaper folder name in Obsidian vault.

        Returns:
            Folder name for AutoPaper in Obsidian vault
        """
        return self.get("obsidian.auto_paper_folder", "AutoPaper")

    def get_articles_raw_dir(self) -> str:
        """Get raw articles directory.

        Returns:
            Path to raw articles directory
        """
        return self.get("articles.raw_dir", "articles/raw")

    def get_articles_parsed_dir(self) -> str:
        """Get parsed articles directory.

        Returns:
            Path to parsed articles directory
        """
        return self.get("articles.parsed_dir", "articles/parsed")

    def get_articles_enriched_dir(self) -> str:
        """Get enriched articles directory.

        Returns:
            Path to enriched articles directory
        """
        return self.get("articles.enriched_dir", "articles/enriched")

    def get_articles_images_dir(self) -> str:
        """Get images directory for downloaded article images.

        Returns:
            Path to images directory
        """
        return self.get("articles.images_dir", "articles/images")

    def get_issues_dir(self) -> str:
        """Get issues directory.

        Returns:
            Path to issues directory
        """
        return self.get("issues_dir", "issues")

    def get_anthropic_api_key(self) -> str:
        """Get Anthropic API key.

        Returns:
            Anthropic API key from environment
        """
        return os.getenv("ANTHROPIC_API_KEY", "")

    def get_model(self) -> str:
        """Get Claude model to use.

        Returns:
            Model name
        """
        return self.get("api.model", "claude-sonnet-4-20250514")

    def get_max_tokens(self) -> int:
        """Get max tokens for API calls.

        Returns:
            Maximum tokens
        """
        return self.get("api.max_tokens", 4096)

    def get_tag_normalization_rules(self) -> Dict[str, List[str]]:
        """Get tag normalization rules.

        Returns:
            Dictionary mapping normalized tags to their variants
        """
        return self.get("tag_normalization", {})

    def get_pdf_config(self) -> Dict[str, Any]:
        """Get PDF export configuration.

        Returns:
            PDF configuration dictionary
        """
        return self.get("pdf", {})

    def ensure_directories(self):
        """Ensure all required directories exist."""
        dirs = [
            self.get_articles_raw_dir(),
            self.get_articles_parsed_dir(),
            self.get_articles_enriched_dir(),
            self.get_articles_images_dir(),
            self.get_issues_dir(),
            Path(self.get_database_path()).parent,
        ]

        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


# Global configuration instance
config = Config()
