"""Configuration management for Claude Code Skills."""

import os
from pathlib import Path
from typing import Optional


class SkillConfig:
    """Simple configuration management for skills using environment variables."""

    @staticmethod
    def get_api_key() -> str:
        """Get Anthropic API key from environment.

        Supports both ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN.

        Returns:
            API key string

        Raises:
            ValueError: If no API key is found
        """
        key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN environment variable not set. "
                "Please set your API key."
            )
        return key

    @staticmethod
    def get_base_url() -> Optional[str]:
        """Get custom API base URL (optional).

        Useful for using custom endpoints or proxies.

        Returns:
            Base URL string or None
        """
        return os.getenv("ANTHROPIC_BASE_URL")

    @staticmethod
    def get_model() -> str:
        """Get model name from environment.

        Returns:
            Model name (defaults to claude-sonnet-4-5-20250929)
        """
        return (
            os.getenv("ANTHROPIC_MODEL")
            or os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL")
            or "claude-sonnet-4-5-20250929"
        )

    @staticmethod
    def get_max_tokens() -> int:
        """Get max tokens setting.

        Returns:
            Max tokens (defaults to 8192)
        """
        return int(os.getenv("ANTHROPIC_MAX_TOKENS", "8192"))

    @staticmethod
    def get_cache_dir() -> Path:
        """Get cache directory path.

        Returns:
            Path to cache directory
        """
        cache_path = os.getenv("CLAUDE_SKILLS_CACHE_DIR")
        if cache_path:
            return Path(cache_path)
        return Path.home() / ".cache" / "claude-skills"

    @staticmethod
    def get_user_agent() -> str:
        """Get user agent for web requests.

        Returns:
            User agent string
        """
        return os.getenv(
            "USER_AGENT",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
        )
