"""Utility functions for generating URL slugs."""
import logging
from typing import Optional

from slugify import slugify
from autopaper.database import Database
from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


def generate_unique_slug(
    title: str,
    url: str,
    db: Database,
    max_length: int = 80
) -> str:
    """Generate a unique slug from title.

    Ensures uniqueness by appending a counter if the slug already exists.

    Args:
        title: Article title
        url: Article URL (used as fallback for slug generation)
        db: Database instance for checking uniqueness
        max_length: Maximum length of base slug (default: 80)

    Returns:
        Unique slug that doesn't exist in database

    Examples:
        >>> slug = generate_unique_slug("My Article", db)
        'my-article'

        >>> # If 'my-article' exists, returns 'my-article-1'
        >>> # If 'my-article-1' exists, returns 'my-article-2'
    """
    # Generate base slug from title
    base_slug = slugify(title[:max_length])

    # Fallback: if title is empty or slug is too short, use URL
    if not base_slug or len(base_slug) < 5:
        # Extract last part of URL
        from urllib.parse import urlparse
        path = urlparse(url).path
        base_slug = slugify(path.split("/")[-1]) or slugify(url)

    # Ensure base_slug is not empty
    if not base_slug:
        base_slug = "untitled"

    slug = base_slug
    counter = 1

    # Check for uniqueness
    while db.get_article_by_slug(slug) is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
        logger.debug(f"Slug conflict detected, trying: {slug}")

        # Safety limit to prevent infinite loops
        if counter > 1000:
            raise ValueError(f"Unable to generate unique slug after 1000 attempts: {base_slug}")

    logger.debug(f"Generated unique slug: {slug}")
    return slug


def validate_slug(slug: str) -> bool:
    """Validate that a slug is well-formed.

    Args:
        slug: Slug to validate

    Returns:
        True if slug is valid, False otherwise

    Examples:
        >>> validate_slug("my-article")
        True
        >>> validate_slug("My Article!")
        False
    """
    if not slug or not isinstance(slug, str):
        return False

    # Check length
    if len(slug) > 200:
        return False

    # Check for invalid characters (only allow alphanumeric, hyphens, underscores)
    import re
    pattern = r'^[a-z0-9][a-z0-9_-]*[a-z0-9]$|^ [a-z0-9]$'
    return bool(re.match(pattern, slug))
