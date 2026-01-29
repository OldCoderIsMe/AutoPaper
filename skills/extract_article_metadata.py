"""Skill: Extract article metadata using Claude AI."""
import hashlib
import os
import sys
from typing import Any, Dict

from anthropic import Anthropic
from anthropic import APIError, APITimeoutError

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopaper.config import config
from autopaper.utils.json_parser import parse_ai_json_response
from autopaper.utils.cache import CacheService, generate_cache_key
from autopaper.utils.retry import retry
from autopaper.utils.logging import get_logger

# Initialize cache and logger
cache = CacheService(cache_dir="cache/ai_metadata")
logger = get_logger(__name__)


def extract_article_metadata(url: str, content: str) -> Dict[str, Any]:
    """Extract metadata from article content using Claude.

    Args:
        url: Article URL
        content: Article content (HTML or plain text)

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
    # Check cache first
    # Use content hash for cache key to avoid redundant API calls
    content_hash = hashlib.md5(content[:10000].encode()).hexdigest()
    cache_key = generate_cache_key("extract_metadata", url, content_hash)

    if cached := cache.get(cache_key):
        print(f"[CACHE HIT] Using cached metadata for {url}", file=sys.stderr)
        return cached

    # Get API key from config (supports both ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN)
    api_key = config.get_anthropic_api_key()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN environment variable not set")

    # Get optional custom base URL from config (for proxy/custom endpoint)
    base_url = config.get_anthropic_base_url()
    # Get model from config (supports ANTHROPIC_MODEL, ANTHROPIC_DEFAULT_SONNET_MODEL, or default)
    model = config.get_anthropic_model() or config.get_anthropic_sonnet_model() or config.get_model()

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = Anthropic(**client_kwargs)

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
            max_tokens=config.get_max_tokens(),
            messages=[{"role": "user", "content": prompt}],
        )

    try:
        response = call_claude()

        # Parse JSON response using unified parser
        metadata = parse_ai_json_response(response.content[0].text)

        # Validate required fields
        required_fields = ["title", "author", "source", "publish_date", "summary", "tags", "article_type", "key_points"]
        for field in required_fields:
            if field not in metadata:
                metadata[field] = "" if field != "tags" and field != "key_points" else []

        # Ensure article_type is valid
        if metadata["article_type"] not in ["technical", "news"]:
            metadata["article_type"] = "news"

        # Cache the result (7 days TTL)
        cache.set(cache_key, metadata, ttl=604800)
        print(f"[CACHE] Stored metadata for {url}", file=sys.stderr)

        return metadata

    except Exception as e:
        raise RuntimeError(f"Failed to extract metadata: {e}")


if __name__ == "__main__":
    # Test the skill
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_article_metadata.py <url> [content_file]")
        sys.exit(1)

    url = sys.argv[1]

    if len(sys.argv) >= 3:
        with open(sys.argv[2], "r") as f:
            content = f.read()
    else:
        content = "Article content would go here..."

    try:
        metadata = extract_article_metadata(url, content)
        print(json.dumps(metadata, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
