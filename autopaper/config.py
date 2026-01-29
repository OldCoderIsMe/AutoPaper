"""Configuration management for AutoPaper."""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv


def find_project_root() -> Path:
    """Find the project root directory by searching for config.yaml.

    Searches upward from current directory until config.yaml is found.
    If not found, returns current directory.

    Returns:
        Path to project root directory
    """
    current = Path.cwd()

    # Check if config path is explicitly set via environment variable
    explicit_path = os.getenv("AUTOPAPER_CONFIG_PATH")
    if explicit_path:
        explicit_config = Path(explicit_path)
        if explicit_config.is_absolute():
            return explicit_config.parent
        return current / explicit_config.parent

    # Search upward for config.yaml
    while current != current.parent:
        if (current / "config.yaml").exists():
            return current
        # Also check for pyproject.toml as a project marker
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent

    # Fallback to current directory
    return Path.cwd()


def get_default_config_path() -> str:
    """Get the default configuration file path.

    First checks AUTOPAPER_CONFIG_PATH environment variable.
    Then searches for config.yaml in project root.
    Falls back to 'config.yaml' in current directory.

    Returns:
        Path to config file as string
    """
    # Check environment variable first
    explicit_path = os.getenv("AUTOPAPER_CONFIG_PATH")
    if explicit_path:
        return explicit_path

    # Find project root and check for config.yaml
    project_root = find_project_root()
    config_path = project_root / "config.yaml"

    if config_path.exists():
        return str(config_path)

    # Fallback to default
    return "config.yaml"


class Config:
    """Configuration manager for AutoPaper."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to configuration file. If None, uses get_default_config_path()
        """
        # Load environment variables from .env file
        load_dotenv()

        if config_path is None:
            config_path = get_default_config_path()

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
            Anthropic API key from environment (supports ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN)
        """
        return os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN", "")

    def get_anthropic_base_url(self) -> str:
        """Get Anthropic API base URL.

        Returns:
            Custom base URL from environment (e.g., for proxy), or default
        """
        return os.getenv("ANTHROPIC_BASE_URL", "")

    def get_anthropic_model(self) -> str:
        """Get default Anthropic model.

        Returns:
            Model name from ANTHROPIC_MODEL environment variable
        """
        return os.getenv("ANTHROPIC_MODEL", "")

    def get_anthropic_sonnet_model(self) -> str:
        """Get Anthropic Sonnet model.

        Returns:
            Sonnet model name from ANTHROPIC_DEFAULT_SONNET_MODEL environment variable
        """
        return os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL", "")

    def get_anthropic_opus_model(self) -> str:
        """Get Anthropic Opus model.

        Returns:
            Opus model name from ANTHROPIC_DEFAULT_OPUS_MODEL environment variable
        """
        return os.getenv("ANTHROPIC_DEFAULT_OPUS_MODEL", "")

    def get_anthropic_haiku_model(self) -> str:
        """Get Anthropic Haiku model.

        Returns:
            Haiku model name from ANTHROPIC_DEFAULT_HAIKU_MODEL environment variable
        """
        return os.getenv("ANTHROPIC_DEFAULT_HAIKU_MODEL", "")

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

    def get_smtp_host(self) -> str:
        """Get SMTP host.

        Returns:
            SMTP host address
        """
        return os.getenv("SMTP_HOST", "")

    def get_smtp_port(self) -> int:
        """Get SMTP port.

        Returns:
            SMTP port number
        """
        port = os.getenv("SMTP_PORT", "587")
        try:
            return int(port)
        except ValueError:
            return 587

    def get_smtp_username(self) -> str:
        """Get SMTP username.

        Returns:
            SMTP username (usually email address)
        """
        return os.getenv("EMAIL_USERNAME", "")

    def get_smtp_password(self) -> str:
        """Get SMTP password.

        Returns:
            SMTP password or app-specific password
        """
        return os.getenv("EMAIL_PASSWORD", "")

    def get_email_from(self) -> str:
        """Get sender email address.

        Returns:
            Sender email address (e.g., "AutoPaper <email@example.com>")
        """
        return os.getenv("EMAIL_FROM", "")

    def get_email_config(self) -> Dict[str, Any]:
        """Get complete email configuration.

        Returns:
            Email configuration dictionary
        """
        return {
            "host": self.get_smtp_host(),
            "port": self.get_smtp_port(),
            "username": self.get_smtp_username(),
            "password": self.get_smtp_password(),
            "from_addr": self.get_email_from(),
        }

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
