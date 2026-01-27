"""Article scraping and content extraction."""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin

import requests
from readability import Document
from rich.console import Console

from autopaper.utils.logging import get_logger
from autopaper.utils.retry import retry
from autopaper.utils.profiling import profile

console = Console()
logger = get_logger(__name__)


class ArticleScraper:
    """Scraper for fetching and extracting article content."""

    def __init__(self, raw_dir: str = "articles/raw", parsed_dir: str = "articles/parsed", images_dir: str = "articles/images"):
        """Initialize article scraper.

        Args:
            raw_dir: Directory to save raw HTML
            parsed_dir: Directory to save parsed content
            images_dir: Directory to save downloaded images
        """
        self.raw_dir = Path(raw_dir)
        self.parsed_dir = Path(parsed_dir)
        self.images_dir = Path(images_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.parsed_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    @retry(max_attempts=3, backoff_factor=2.0, exceptions=(requests.RequestException,))
    def fetch_article(self, url: str, timeout: int = 30) -> Optional[str]:
        """Fetch article HTML from URL.

        Args:
            url: Article URL
            timeout: Request timeout in seconds

        Returns:
            HTML content or None if failed
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        logger.debug(f"Successfully fetched {url} ({len(response.text)} bytes)")
        return response.text

    def extract_content(self, html: str) -> Dict[str, str]:
        """Extract main content from HTML using readability-lxml.

        Args:
            html: HTML content

        Returns:
            Dictionary with title, content, and short_excerpt
        """
        try:
            doc = Document(html)
            title = doc.title()
            content = doc.summary()

            # Get a short excerpt from the content
            import re

            text_only = re.sub(r"<[^>]+>", " ", content)
            words = text_only.split()
            short_excerpt = " ".join(words[:50]) + "..." if len(words) > 50 else text_only

            logger.debug(f"Extracted content: title='{title[:50]}...', excerpt length={len(short_excerpt)}")
            return {"title": title or "", "content": content or "", "short_excerpt": short_excerpt or ""}
        except Exception as e:
            logger.error(f"Error extracting content from HTML: {e}", exc_info=True)
            console.print(f"[red]Error extracting content: {e}[/red]")
            return {"title": "", "content": "", "short_excerpt": ""}

    def save_raw(self, url: str, html: str) -> Path:
        """Save raw HTML to file.

        Args:
            url: Article URL (used for filename)
            html: HTML content

        Returns:
            Path to saved file
        """
        filename = self._url_to_filename(url, "html")
        filepath = self.raw_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return filepath

    def save_parsed(self, url: str, parsed_data: Dict) -> Path:
        """Save parsed content to JSON file.

        Args:
            url: Article URL (used for filename)
            parsed_data: Parsed content dictionary

        Returns:
            Path to saved file
        """
        filename = self._url_to_filename(url, "json")
        filepath = self.parsed_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        return filepath

    def load_parsed(self, url: str) -> Optional[Dict]:
        """Load parsed content from JSON file.

        Args:
            url: Article URL

        Returns:
            Parsed content dictionary or None if not found
        """
        filename = self._url_to_filename(url, "json")
        filepath = self.parsed_dir / filename

        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    @profile(log_slow_calls=5.0)
    def scrape(self, url: str) -> Optional[Dict[str, str]]:
        """Scrape and extract content from URL.

        Args:
            url: Article URL

        Returns:
            Dictionary with url, title, content, short_excerpt, scraped_at
        """
        console.print(f"[cyan]Fetching article from {url}...[/cyan]")

        # Check if already parsed
        cached = self.load_parsed(url)
        if cached:
            console.print(f"[green]Using cached content for {url}[/green]")
            return cached

        # Fetch HTML
        html = self.fetch_article(url)
        if not html:
            return None

        # Save raw HTML
        self.save_raw(url, html)

        # Extract content
        extracted = self.extract_content(html)

        result = {
            "url": url,
            "title": extracted["title"],
            "content": extracted["content"],
            "short_excerpt": extracted["short_excerpt"],
            "scraped_at": datetime.now().isoformat(),
        }

        # Save parsed content
        self.save_parsed(url, result)

        console.print(f"[green]Successfully scraped: {extracted['title'][:60]}...[/green]")

        return result

    def _url_to_filename(self, url: str, extension: str) -> str:
        """Convert URL to safe filename.

        Args:
            url: Article URL
            extension: File extension

        Returns:
            Safe filename
        """
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        path = parsed.path.strip("/").replace("/", "_")

        if path:
            filename = f"{domain}_{path}.{extension}"
        else:
            filename = f"{domain}.{extension}"

        # Replace unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, "_")

        return filename

    def extract_cover_image_url(self, html: str, url: str) -> Optional[str]:
        """Extract cover image URL from HTML.

        Args:
            html: HTML content
            url: Article URL (for resolving relative paths)

        Returns:
            Cover image URL or None
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')

        for img in img_tags[:10]:  # Check first 10 images
            src = img.get('src') or img.get('data-src')

            if not src:
                continue

            # Resolve relative URLs
            absolute_url = urljoin(url, src)

            # Filter out unwanted images
            url_lower = absolute_url.lower()

            # Skip flags, icons, avatars, logos, etc.
            skip_patterns = [
                'flag', 'icon', 'logo', 'avatar', 'emoji',
                'badge', 'button', 'sprite', 'background',
                '.svg',  # Skip SVG files (usually icons)
                '/flags/',
                'favicon',
                'apple-touch',
                'loading',
                'placeholder',
                '1x1',  # Placeholder images
                'pixel',
            ]

            if any(pattern in url_lower for pattern in skip_patterns):
                continue

            # Check image dimensions if available (try to avoid very small images)
            width = img.get('width')
            height = img.get('height')
            if width and int(width) < 200:
                continue
            if height and int(height) < 200:
                continue

            # Found a suitable cover image
            return absolute_url

        return None
