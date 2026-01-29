"""Skill: Compose issue from articles using Claude AI."""
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

from anthropic import Anthropic

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopaper.config import config
from autopaper.utils.json_parser import parse_ai_json_response


def compose_issue(
    articles: List[Dict[str, Any]], issue_type: str = "tech", start_date: str = "", end_date: str = ""
) -> Dict[str, Any]:
    """Compose a newspaper issue from articles using Claude AI.

    Args:
        articles: List of article dictionaries with metadata
        issue_type: Type of issue ('tech' or 'news')
        start_date: Issue start date (ISO format)
        end_date: Issue end date (ISO format)

    Returns:
        Dictionary with:
        {
            "issue_markdown": str,  # Full issue content in Markdown
            "introduction": str,  # Editor's introduction
            "trends": str,  # Core trends analysis
            "article_blocks": List[Dict],  # Article summaries with references
            "news_briefs": List[Dict]  # Quick news items
        }
    """
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

    # Format articles for the prompt
    articles_text = json.dumps(
        [
            {
                "slug": a.get("slug", ""),
                "title": a.get("title", ""),
                "summary": a.get("summary", ""),
                "tags": a.get("tags", []),
                "key_points": a.get("key_points", []),
                "url": a.get("url", ""),
            }
            for a in articles
        ],
        ensure_ascii=False,
        indent=2,
    )

    # Determine title based on type
    if issue_type == "tech":
        issue_title = "技术精选"
        guidance = "Focus on deep technical insights, architecture, implementation details, and technical trends."
    else:
        issue_title = "行业动态"
        guidance = (
            "Focus on industry news, product launches, funding, company updates, and market trends."
        )

    # Calculate week ID
    if start_date:
        try:
            dt = datetime.fromisoformat(start_date)
            week_id = dt.strftime("%Y-W%U")
        except:
            week_id = datetime.now().strftime("%Y-W%U")
    else:
        week_id = datetime.now().strftime("%Y-W%U")

    week_title = week_id

    prompt = f"""You are a technical newsletter editor. Compose a newspaper issue from the following articles.

Issue Title: 本周{issue_title} · {week_title}
Issue Type: {issue_type}
Guidance: {guidance}

Articles:
{articles_text}

Create a compelling newsletter issue with the following structure:

1. **主编导语 (Editor's Introduction)**: 2-3 sentences setting the theme and highlighting what's special about this week's content.

2. **核心趋势 (Core Trends)**: Analyze the key trends across these articles. What patterns do you see? What technologies or topics are emerging? Group by theme.

3. **深度文章 (In-depth Articles)**: For 5-7 best technical articles, create engaging summaries that:
   - Start with the article title and a brief one-line hook
   - Follow with a 2-3 sentence summary of key insights
   - End with "Why it matters" and "Key takeaways"
   - Include the article slug in a reference like: (See: [[article-slug]])
   - IMPORTANT: Preserve the cover_image, url, and tags fields from the article metadata exactly as provided

4. **快讯速览 (News Briefs)**: For news items, create 1-2 sentence bullet points with essential info.

IMPORTANT: Use [[article-slug]] format to reference articles. The slug is provided in each article's metadata.

Respond with valid JSON in this format:
{{
    "issue_markdown": "Full markdown content of the issue",
    "introduction": "Editor's introduction text",
    "trends": "Core trends analysis",
    "article_blocks": [
        {{
            "slug": "article-slug",
            "title": "Article Title",
            "content": "Article summary with hook, insights, why it matters, and takeaways",
            "tags": ["tag1", "tag2"],
            "url": "original-article-url"
        }}
    ],
    "news_briefs": [
        {{
            "title": "News item title",
            "summary": "1-2 sentence summary",
            "url": "original-url"
        }}
    ]
}}

Keep the tone professional yet engaging. Be specific and technical, not generic.
IMPORTANT: Respond with ONLY the JSON object, no additional text.
IMPORTANT: Include the "url" field in article_blocks using the url from the article metadata."""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=config.get_max_tokens() * 2,  # Issue generation needs more tokens
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response using unified parser
        result = parse_ai_json_response(response.content[0].text)

        # Validate structure
        if "issue_markdown" not in result:
            result["issue_markdown"] = ""
        if "introduction" not in result:
            result["introduction"] = ""
        if "trends" not in result:
            result["trends"] = ""
        if "article_blocks" not in result:
            result["article_blocks"] = []
        if "news_briefs" not in result:
            result["news_briefs"] = []

        return result

    except Exception as e:
        raise RuntimeError(f"Failed to compose issue: {e}")


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python compose_issue.py <articles_json_file>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        articles = json.load(f)

    try:
        issue = compose_issue(articles, issue_type="tech")
        print(json.dumps(issue, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
