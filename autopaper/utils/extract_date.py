"""Extract publish date from HTML and URL using multiple strategies."""
import re
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


def extract_date_from_html(html: str, url: str = "") -> Optional[str]:
    """Extract publish date from HTML using multiple strategies.

    Priority order:
    1. JSON-LD structured data (most reliable)
    2. Meta tags (article:published_time, datePublished, etc.)
    3. <time> elements
    4. Semantic HTML (date published classes)
    5. URL pattern matching
    6. HTTP headers (if available)

    Args:
        html: HTML content
        url: Article URL (for fallback extraction)

    Returns:
        Date string in YYYY-MM-DD format, or None if not found
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Strategy 1: JSON-LD structured data
    date = extract_from_json_ld(soup)
    if date:
        logger.debug(f"Found date in JSON-LD: {date}")
        return date

    # Strategy 2: Meta tags
    date = extract_from_meta_tags(soup)
    if date:
        logger.debug(f"Found date in meta tags: {date}")
        return date

    # Strategy 3: <time> elements
    date = extract_from_time_elements(soup)
    if date:
        logger.debug(f"Found date in <time> elements: {date}")
        return date

    # Strategy 4: Semantic HTML (common class names)
    date = extract_from_semantic_html(soup)
    if date:
        logger.debug(f"Found date in semantic HTML: {date}")
        return date

    # Strategy 5: URL pattern matching
    if url:
        date = extract_from_url(url)
        if date:
            logger.debug(f"Found date in URL: {date}")
            return date

    logger.debug("No date found in HTML or URL")
    return None


def extract_from_json_ld(soup: BeautifulSoup) -> Optional[str]:
    """Extract date from JSON-LD structured data."""
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            import json
            data = json.loads(script.string)
            # Handle both single object and array
            items = [data] if isinstance(data, dict) else data

            for item in items:
                # Try various date fields
                for field in ['datePublished', 'dateCreated', 'publishDate', 'date']:
                    if field in item and item[field]:
                        parsed = parse_date_string(item[field])
                        if parsed:
                            return parsed
        except (json.JSONDecodeError, TypeError, KeyError):
            continue
    return None


def extract_from_meta_tags(soup: BeautifulSoup) -> Optional[str]:
    """Extract date from meta tags.

    Common meta tags for publish date:
    - <meta property="article:published_time" content="..." />
    - <meta itemprop="datePublished" content="..." />
    - <meta name="date" content="..." />
    - <meta name="pubdate" content="..." />
    - <meta name="publish_date" content="..." />
    """
    meta_selectors = [
        ('meta[property="article:published_time"]', 'content'),
        ('meta[property="article:published"]', 'content'),
        ('meta[itemprop="datePublished"]', 'content'),
        ('meta[itemprop="datecreated"]', 'content'),
        ('meta[name="date"]', 'content'),
        ('meta[name="pubdate"]', 'content'),
        ('meta[name="publish_date"]', 'content'),
        ('meta[name="publish-date"]', 'content'),
        ('meta[name="sailthru.date"]', 'content'),
        ('meta[name="DC.date"]', 'content'),
        ('meta[name="DC.date.issued"]', 'content'),
    ]

    for selector, attr in meta_selectors:
        meta = soup.select_one(selector)
        if meta:
            date_str = meta.get(attr)
            if date_str:
                parsed = parse_date_string(date_str)
                if parsed:
                    return parsed

    return None


def extract_from_time_elements(soup: BeautifulSoup) -> Optional[str]:
    """Extract date from <time> elements."""
    time_tags = soup.find_all('time')
    for time_tag in time_tags:
        # Try datetime attribute first
        date_str = time_tag.get('datetime') or time_tag.get('content') or time_tag.get_text(strip=True)
        if date_str:
            parsed = parse_date_string(date_str)
            if parsed:
                return parsed
    return None


def extract_from_semantic_html(soup: BeautifulSoup) -> Optional[str]:
    """Extract date from common semantic class names.

    Look for elements with class names like:
    - publish-date, published, date, post-date
    - entry-date, article-date
    - byline-date, timestamp
    """
    class_patterns = [
        r'publish',
        r'post[_-]?date',
        r'entry[_-]?date',
        r'article[_-]?date',
        r'byline[_-]?date',
        r'timestamp',
        r'^date$',
    ]

    for pattern in class_patterns:
        elements = soup.find_all(class_=re.compile(pattern, re.I))
        for elem in elements[:5]:  # Check first 5 matches
            # Try attributes first
            date_str = (
                elem.get('datetime') or
                elem.get('content') or
                elem.get('title') or
                elem.get_text(strip=True)
            )
            if date_str:
                parsed = parse_date_string(date_str)
                if parsed:
                    return parsed

    return None


def extract_from_url(url: str) -> Optional[str]:
    """Extract date from URL pattern.

    Common URL patterns:
    - /2024/03/01/slug
    - /2024/03/slug
    - /20240301-slug
    """
    parsed = urlparse(url)
    path = parsed.path

    # Pattern 1: /YYYY/MM/DD/slug or /YYYY/MM/DD/
    match = re.search(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', path)
    if match:
        year, month, day = match.groups()
        try:
            date = datetime(int(year), int(month), int(day))
            return date.strftime('%Y-%m-%d')
        except ValueError:
            pass

    # Pattern 2: /YYYY/MM/slug or /YYYY/MM/
    match = re.search(r'/(\d{4})/(\d{1,2})/', path)
    if match:
        year, month = match.groups()
        try:
            date = datetime(int(year), int(month), 1)
            return date.strftime('%Y-%m-%d')
        except ValueError:
            pass

    # Pattern 3: /YYYYMMDD-slug
    match = re.search(r'/(\d{4})(\d{2})(\d{2})', path)
    if match:
        year, month, day = match.groups()
        try:
            date = datetime(int(year), int(month), int(day))
            return date.strftime('%Y-%m-%d')
        except ValueError:
            pass

    return None


def parse_date_string(date_str: str) -> Optional[str]:
    """Parse date string in various formats and return YYYY-MM-DD.

    Supports ISO 8601, RFC 2822, and common date formats.
    """
    if not date_str or not date_str.strip():
        return None

    date_str = date_str.strip()

    # If already in YYYY-MM-DD format, validate and return
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            pass

    # Try parsing with dateutil
    try:
        parsed_dt = date_parser.parse(date_str, fuzzy=False)
        # Sanity check: date should be in the past and not too old
        now = datetime.now()
        if parsed_dt > now:
            logger.warning(f"Future date detected: {date_str} -> {parsed_dt}")
            return None

        # Don't accept dates before 1990 (probably misparsed)
        if parsed_dt.year < 1990:
            logger.warning(f"Suspicious old date: {date_str} -> {parsed_dt}")
            return None

        return parsed_dt.strftime('%Y-%m-%d')
    except (ValueError, TypeError) as e:
        logger.debug(f"Failed to parse date string '{date_str}': {e}")
        return None
