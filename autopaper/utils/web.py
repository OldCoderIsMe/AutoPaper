"""Web fetching utilities.

This module provides enhanced web fetching capabilities with better
anti-crawling resistance through realistic browser headers.
"""
import requests
from typing import Optional


# Enhanced headers that mimic a real browser
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
}


def fetch_url_content(url: str, timeout: int = 30) -> str:
    """Fetch content from URL with enhanced anti-crawling headers.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Content as string

    Raises:
        RuntimeError: If fetch fails
    """
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.raise_for_status()

        # Try to decode as UTF-8
        return response.content.decode("utf-8", errors="ignore")

    except Exception as e:
        raise RuntimeError(f"Failed to fetch URL {url}: {e}")
