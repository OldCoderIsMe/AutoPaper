#!/usr/bin/env python3
"""
Extract article metadata using Claude AI.

This skill extracts structured metadata from article URLs or content including:
- Title, author, source, publish date
- Summary (2-3 sentences)
- Tags and classification
- Key points (3-7 items)
"""

import hashlib
import sys
from pathlib import Path
from typing import Dict, Any, Optional

import requests
from anthropic import Anthropic
from anthropic import APIError, APITimeoutError

# Add shared tools to path
shared_path = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from shared.config import SkillConfig
from shared.cache import CacheService, generate_cache_key
from shared.retry import retry
from shared.json_parser import parse_ai_json_response

# Initialize
config = SkillConfig()
cache = CacheService(cache_dir=config.get_cache_dir() / "extract-metadata")


def scrape_article(url: str) -> str:
    """Scrape article content from URL.

    Args:
        url: Article URL

    Returns:
        Article content as plain text
    """
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": config.get_user_agent()},
        )
        response.raise_for_status()

        # Try to extract readable content
        try:
            from readability import Document

            # Use response.text instead of response.content to avoid bytes/str issues
            doc = Document(response.text)
            return doc.summary()
        except (ImportError, Exception) as e:
            # Fallback: just return text content
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()

    except Exception as e:
        raise RuntimeError(f"Failed to scrape article from {url}: {e}")


def extract_metadata(url: str, content: Optional[str] = None) -> Dict[str, Any]:
    """Extract metadata from article URL or content.

    Args:
        url: Article URL
        content: Article content (optional, will scrape if not provided)

    Returns:
        Dictionary with extracted metadata:
        {
            "title": str,
            "author": str,
            "source": str,
            "publish_date": str,
            "summary": str,
            "tags": List[str],
            "article_type": "technical" | "news",
            "key_points": List[str]
        }
    """
    # Scrape content if not provided
    if content is None:
        print(f"[INFO] Scraping content from {url}...", file=sys.stderr)
        content = scrape_article(url)

    # Check cache first
    content_hash = hashlib.md5(content[:10000].encode()).hexdigest()
    cache_key = generate_cache_key("extract_metadata", url, content_hash)

    if cached := cache.get(cache_key):
        print(f"[CACHE HIT] Using cached metadata for {url}", file=sys.stderr)
        return cached

    # Get API configuration
    api_key = config.get_api_key()
    base_url = config.get_base_url()
    model = config.get_model()
    max_tokens = config.get_max_tokens()

    # Initialize client
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = Anthropic(**client_kwargs)

    # Build prompt
    prompt = f"""You are an article metadata extractor. Analyze the following article and extract metadata.

Article URL: {url}

Article Content:
{content[:8000]}

Please extract the following information and respond ONLY with valid JSON in this format:
{{
    "title": "article title",
    "author": "author name (or 'Unknown' if not found)",
    "source": "website/publication name",
    "publish_date": "YYYY-MM-DD format (or best estimate)",
    "summary": "2-3 sentence summary of the article",
    "tags": ["tag1", "tag2", "tag3"],
    "article_type": "technical" or "news",
    "key_points": ["point1", "point2", "point3"]
}}

Article type classification:
- Use "technical" for: architecture, implementation details, source code analysis, system design, tutorials, technical deep-dives
- Use "news" for: product launches, funding announcements, industry updates, company news, market trends

Tags should be relevant technical or topic keywords (e.g., kubernetes, llm, python, security).
Extract 3-7 key points as bullet points.

IMPORTANT: Respond with ONLY the JSON object, no additional text."""

    # Create AI call with retry
    @retry(max_attempts=3, backoff_factor=2.0, exceptions=(APIError, APITimeoutError, ConnectionError))
    def call_claude():
        return client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )

    try:
        print(f"[INFO] Calling Claude API...", file=sys.stderr)
        response = call_claude()

        # Parse JSON response
        metadata = parse_ai_json_response(response.content[0].text)

        # Validate required fields
        required_fields = [
            "title",
            "author",
            "source",
            "publish_date",
            "summary",
            "tags",
            "article_type",
            "key_points",
        ]
        for field in required_fields:
            if field not in metadata:
                metadata[field] = "" if field not in ["tags", "key_points"] else []

        # Ensure article_type is valid
        if metadata["article_type"] not in ["technical", "news"]:
            metadata["article_type"] = "news"

        # Ensure tags and key_points are lists
        if not isinstance(metadata.get("tags"), list):
            metadata["tags"] = []
        if not isinstance(metadata.get("key_points"), list):
            metadata["key_points"] = []

        # Cache the result (7 days TTL)
        cache.set(cache_key, metadata, ttl=604800)
        print(f"[INFO] Metadata extracted and cached", file=sys.stderr)

        return metadata

    except Exception as e:
        raise RuntimeError(f"Failed to extract metadata: {e}")


def format_markdown(metadata: Dict[str, Any]) -> str:
    """Format metadata as Markdown.

    Args:
        metadata: Metadata dictionary

    Returns:
        Formatted Markdown string
    """
    lines = [
        f"# {metadata['title']}",
        "",
        f"**Author**: {metadata['author']}",
        f"**Source**: {metadata['source']}",
        f"**Date**: {metadata['publish_date']}",
        f"**Type**: {metadata['article_type']}",
        "",
        f"**Tags**: {', '.join(metadata['tags'])}",
        "",
        "## Summary",
        metadata['summary'],
        "",
        "## Key Points",
    ]

    for i, point in enumerate(metadata['key_points'], 1):
        lines.append(f"{i}. {point}")

    return "\n".join(lines)


def main():
    """CLI entry point."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Extract article metadata using Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from URL
  python main.py https://blog.example.com/article

  # Extract from content (skip scraping)
  python main.py https://example.com --content "$(cat article.md)"

  # Output as Markdown
  python main.py https://example.com --output markdown

  # Read URL from stdin
  echo "https://example.com" | python main.py -
        """,
    )

    parser.add_argument(
        "url",
        help="Article URL (use '-' to read from stdin)",
    )
    parser.add_argument(
        "--content",
        help="Article content (skips web scraping if provided)",
    )
    parser.add_argument(
        "--output",
        choices=["json", "markdown"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable cache and force fresh extraction",
    )

    args = parser.parse_args()

    # Handle stdin input
    url = args.url
    if url == "-":
        url = sys.stdin.readline().strip()
        if not url:
            print("Error: No URL provided via stdin", file=sys.stderr)
            sys.exit(1)

    # Clear cache if requested
    if args.no_cache:
        cache.clear()

    # Extract metadata
    try:
        metadata = extract_metadata(url, args.content)

        if args.output == "json":
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
        else:
            print(format_markdown(metadata))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
