"""Skill: Extract article metadata using Claude AI."""
import hashlib
import os
import sys
from datetime import datetime
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


def extract_article_metadata(url: str, content: str, pre_extracted_title: str = "", force: bool = False) -> Dict[str, Any]:
    """Extract metadata from article content using Claude.

    Args:
        url: Article URL
        content: Article content (HTML or plain text)
        pre_extracted_title: Pre-extracted title from scraper (for better accuracy)
        force: Force re-extraction even if cached metadata exists

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
    # Check cache first (skip if force=True)
    # Use content hash for cache key to avoid redundant API calls
    content_hash = hashlib.md5(content[:10000].encode()).hexdigest()
    cache_key = generate_cache_key("extract_metadata", url, content_hash)

    if not force and (cached := cache.get(cache_key)):
        print(f"[CACHE HIT] Using cached metadata for {url}", file=sys.stderr)
        return cached

    # For WeChat articles, pre-extract metadata for better accuracy
    wechat_metadata = {}
    is_wechat = "mp.weixin.qq.com" in url or "weixin.qq.com" in url
    if is_wechat:
        try:
            from autopaper.scrapers.article import extract_wechat_metadata
            wechat_metadata = extract_wechat_metadata(content, url)
            if wechat_metadata.get("author"):
                print(f"[WECHAT] Extracted author: {wechat_metadata['author']}", file=sys.stderr)
            if wechat_metadata.get("source"):
                print(f"[WECHAT] Extracted source: {wechat_metadata['source']}", file=sys.stderr)
            if wechat_metadata.get("publish_date"):
                print(f"[WECHAT] Extracted publish date: {wechat_metadata['publish_date']}", file=sys.stderr)
        except Exception as e:
            logger.warning(f"Failed to extract WeChat metadata: {e}")

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

    # Determine content length - use more for WeChat articles as they have verbose HTML
    content_length = 20000 if is_wechat else 8000

    # Build prompt with pre-extracted metadata if available
    title_context = f"\nPre-extracted Title: {pre_extracted_title}\n" if pre_extracted_title else ""
    wechat_context = ""
    if wechat_metadata:
        wechat_context = "\nPre-extracted WeChat Metadata:\n"
        if wechat_metadata.get("author"):
            wechat_context += f"- Author: {wechat_metadata['author']}\n"
        if wechat_metadata.get("source"):
            wechat_context += f"- Source: {wechat_metadata['source']}\n"
        if wechat_metadata.get("publish_date"):
            wechat_context += f"- Publish Date: {wechat_metadata['publish_date']}\n"

    prompt = f"""You are an article metadata extractor. Analyze the following article and extract metadata.

Article URL: {url}{title_context}{wechat_context}
Article Content:
{content[:content_length]}

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

IMPORTANT:
- If pre-extracted metadata is provided above, use it as the primary source for author, source, and publish_date
- If no publish_date is available, use the current date: {datetime.now().strftime("%Y-%m-%d")}
- Respond with ONLY the JSON object, no additional text."""

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

        # Use pre-extracted WeChat metadata if AI didn't find it
        if is_wechat and wechat_metadata:
            if not metadata.get("author") or metadata["author"] == "Unknown":
                metadata["author"] = wechat_metadata.get("author", "Unknown")
            if not metadata.get("source"):
                metadata["source"] = wechat_metadata.get("source", "")
            if not metadata.get("publish_date"):
                metadata["publish_date"] = wechat_metadata.get("publish_date", "")

        # Ensure publish_date has a value (use current date if still empty)
        if not metadata.get("publish_date") or metadata["publish_date"].strip() == "":
            metadata["publish_date"] = datetime.now().strftime("%Y-%m-%d")
            print(f"[INFO] Using current date as publish_date: {metadata['publish_date']}", file=sys.stderr)

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
