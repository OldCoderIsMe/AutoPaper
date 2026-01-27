"""Caching service for AI calls and expensive operations."""
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Optional

from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


class CacheService:
    """Simple file-based caching service for AI calls.

    Caches results based on content hash to avoid redundant API calls.
    """

    def __init__(self, cache_dir: str = "cache"):
        """Initialize cache service.

        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Cache initialized: {self.cache_dir}")

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key.

        Args:
            key: Cache key

        Returns:
            Path to cache file
        """
        # Use hash of key as filename to avoid invalid characters
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            logger.debug(f"Cache miss: {key[:50]}...")
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check if cache is expired
            import time
            if "expires_at" in data and time.time() > data["expires_at"]:
                logger.debug(f"Cache expired: {key[:50]}...")
                cache_path.unlink()
                return None

            logger.debug(f"Cache hit: {key[:50]}...")
            return data.get("value")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error reading cache {cache_path}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 86400) -> bool:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (default: 24 hours)

        Returns:
            True if successful, False otherwise
        """
        cache_path = self._get_cache_path(key)

        try:
            import time
            data = {
                "value": value,
                "expires_at": time.time() + ttl,
                "created_at": time.time(),
            }

            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.debug(f"Cached: {key[:50]}... (TTL={ttl}s)")
            return True
        except (TypeError, json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error writing cache {cache_path}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False otherwise
        """
        cache_path = self._get_cache_path(key)

        if cache_path.exists():
            try:
                cache_path.unlink()
                logger.debug(f"Cache deleted: {key[:50]}...")
                return True
            except IOError as e:
                logger.warning(f"Error deleting cache {cache_path}: {e}")
                return False

        return False

    def clear(self) -> int:
        """Clear all cache entries.

        Returns:
            Number of cache files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except IOError as e:
                logger.warning(f"Error deleting cache file {cache_file}: {e}")

        logger.info(f"Cleared {count} cache entries")
        return count

    def get_size(self) -> int:
        """Get total cache size in bytes.

        Returns:
            Total size of all cache files
        """
        total_size = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                total_size += cache_file.stat().st_size
            except IOError:
                pass

        return total_size


def generate_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from function arguments.

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Cache key string

    Examples:
        >>> generate_cache_key("http://example.com", "content...")
        'http://example.com|content...'
    """
    key_parts = []

    # Add positional arguments
    for arg in args:
        if isinstance(arg, str):
            key_parts.append(arg)
        elif isinstance(arg, (dict, list)):
            # For complex types, use JSON
            key_parts.append(json.dumps(arg, sort_keys=True))
        else:
            key_parts.append(str(arg))

    # Add keyword arguments (sorted for consistency)
    for k in sorted(kwargs.keys()):
        v = kwargs[k]
        if isinstance(v, str):
            key_parts.append(f"{k}={v}")
        elif isinstance(v, (dict, list)):
            key_parts.append(f"{k}={json.dumps(v, sort_keys=True)}")
        else:
            key_parts.append(f"{k}={str(v)}")

    return "|".join(key_parts)


def cached_call(cache: CacheService, ttl: int = 86400):
    """Decorator for caching function results.

    Args:
        cache: CacheService instance
        ttl: Time to live in seconds

    Returns:
        Decorated function

    Examples:
        >>> cache = CacheService()
        >>>
        >>> @cached_call(cache, ttl=3600)
        >>> def expensive_function(param1, param2):
        >>>     # Expensive operation
        >>>     return result
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{generate_cache_key(*args, **kwargs)}"

            # Try to get from cache
            if result := cache.get(cache_key):
                return result

            # Call function
            result = func(*args, **kwargs)

            # Cache result
            cache.set(cache_key, result, ttl=ttl)

            return result

        return wrapper
    return decorator
