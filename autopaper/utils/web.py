"""Web fetching utilities."""
import requests
from typing import Optional


def fetch_url_content(url: str, timeout: int = 30) -> str:
    """Fetch content from URL.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Content as string
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Try to decode as UTF-8
        return response.content.decode("utf-8", errors="ignore")

    except Exception as e:
        raise RuntimeError(f"Failed to fetch URL {url}: {e}")
