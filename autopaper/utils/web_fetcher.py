"""Enhanced web fetching utilities with anti-crawling support.

This module provides web fetching capabilities that are more resistant to
anti-crawling measures by using multiple strategies including:
- Playwright for JavaScript-heavy sites (WeChat, etc.)
- Enhanced requests with realistic headers
- Support for various content types
"""
import re
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests

from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


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


def is_wechat_url(url: str) -> bool:
    """Check if URL is a WeChat article.

    Args:
        url: URL to check

    Returns:
        True if WeChat URL
    """
    return "mp.weixin.qq.com" in url or "weixin.qq.com" in url


def is_javascript_heavy_site(url: str) -> bool:
    """Check if URL requires JavaScript rendering.

    Args:
        url: URL to check

    Returns:
        True if site likely requires JavaScript rendering
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    js_heavy_domains = {
        "mp.weixin.qq.com",
        "weixin.qq.com",
        "twitter.com",
        "x.com",
        "facebook.com",
        "instagram.com",
        "medium.com",
        "substack.com",
    }

    return any(d in domain for d in js_heavy_domains)


def fetch_with_playwright(url: str, timeout: int = 30000) -> Optional[str]:
    """Fetch content using Playwright (headless browser).

    This method can handle JavaScript-rendered content and is more
    resistant to anti-crawling measures.

    Args:
        url: URL to fetch
        timeout: Page load timeout in milliseconds

    Returns:
        HTML content or None if failed
    """
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={"width": 1920, "height": 1080},
                user_agent=DEFAULT_HEADERS["User-Agent"]
            )

            # Set extra headers
            page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            })

            # Navigate to URL
            page.goto(url, wait_until="networkidle", timeout=timeout)

            # Wait for content to load (especially for WeChat)
            if is_wechat_url(url):
                # WeChat articles need extra time for content to load
                page.wait_for_selector("div#js_content", timeout=10000)

            # Get the HTML content
            content = page.content()
            browser.close()

            logger.debug(f"Successfully fetched {url} with Playwright ({len(content)} bytes)")
            return content

    except ImportError:
        logger.debug("Playwright not installed, falling back to requests")
        return None
    except Exception as e:
        logger.debug(f"Playwright fetch failed: {e}")
        return None


def fetch_with_requests(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch content using requests with enhanced headers.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        HTML content or None if failed
    """
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.raise_for_status()

        logger.debug(f"Successfully fetched {url} with requests ({len(response.text)} bytes)")
        return response.text

    except Exception as e:
        logger.debug(f"Requests fetch failed: {e}")
        return None


def fetch_url_content(
    url: str,
    timeout: int = 30,
    force_playwright: bool = False
) -> str:
    """Fetch content from URL with anti-crawling resistance.

    This function tries multiple strategies to fetch content:
    1. Playwright for JavaScript-heavy sites or when forced
    2. Enhanced requests with realistic headers as fallback

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        force_playwright: Force use of Playwright

    Returns:
        Content as string

    Raises:
        RuntimeError: If all fetch methods fail
    """
    errors = []

    # Use Playwright for JavaScript-heavy sites or when forced
    if force_playwright or is_javascript_heavy_site(url):
        content = fetch_with_playwright(url, timeout * 1000)
        if content:
            return content
        errors.append("Playwright fetch failed or not available")

    # Fallback to requests
    content = fetch_with_requests(url, timeout)
    if content:
        return content

    errors.append("Enhanced requests failed")

    raise RuntimeError(f"Failed to fetch URL {url}: {'; '.join(errors)}")


def markdown_to_html(markdown_content: str) -> str:
    """Convert markdown content to basic HTML.

    This is a simple converter for cases where content
    needs to be converted from markdown to HTML.

    Args:
        markdown_content: Markdown content

    Returns:
        Basic HTML content
    """
    try:
        import markdown
        return markdown.markdown(markdown_content)
    except ImportError:
        # Fallback: simple conversion
        html = markdown_content

        # Convert headers
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

        # Convert bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # Convert links
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

        # Convert images
        html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', html)

        # Convert line breaks
        html = html.replace('\n\n', '</p><p>')
        html = f'<p>{html}</p>'

        return html


def fetch_article_content(
    url: str,
    timeout: int = 30,
    return_html: bool = True
) -> str:
    """Fetch article content, handling special cases like WeChat.

    Args:
        url: Article URL
        timeout: Request timeout in seconds
        return_html: Whether to return HTML (True) or markdown (False)

    Returns:
        Article content as HTML or markdown
    """
    content = fetch_url_content(url, timeout=timeout)

    # For WeChat URLs, the content is already HTML
    if is_wechat_url(url):
        pass

    if not return_html:
        # Convert to markdown if needed
        try:
            from html2text import HTML2Text
            h = HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            content = h.handle(content)
        except ImportError:
            # Fallback: use basic conversion
            content = markdown_to_html(content)

    return content
