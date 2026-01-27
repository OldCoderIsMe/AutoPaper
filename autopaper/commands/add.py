"""Add article command."""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
import typer
from rich.console import Console

from autopaper.config import config
from autopaper.database import Database
from autopaper.models import Article
from autopaper.scrapers.article import ArticleScraper
from autopaper.utils.slug import generate_unique_slug
from autopaper.utils.logging import get_logger
from autopaper.utils.profiling import profile, print_profiler_summary

# Import skills
sys_path = str(Path(__file__).parent.parent.parent / "skills")
if sys_path not in os.sys.path:
    os.sys.path.insert(0, sys_path)

import extract_article_metadata

console = Console()
logger = get_logger(__name__)


def download_image(url: str, output_dir: Path, slug: str, force: bool = False) -> str:
    """Download image from URL and save locally.

    Args:
        url: Image URL
        output_dir: Directory to save images
        slug: Article slug (for filename)
        force: Force re-download even if exists

    Returns:
        Local path relative to output_dir
    """
    try:
        # Determine filename from URL
        parsed_url = urlparse(url)
        url_path = parsed_url.path
        ext = os.path.splitext(url_path)[1] or ".jpg"

        # Clean filename
        safe_filename = f"{slug}{ext}"
        local_path = output_dir / safe_filename

        # Check if already exists
        if local_path.exists() and local_path.stat().st_size > 0 and not force:
            console.print(f"  [dim]✓ Using cached image: {safe_filename}[/dim]")
            return safe_filename

        # Download image
        console.print(f"  [dim]⬇ Downloading image: {safe_filename}[/dim]")
        response = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        response.raise_for_status()

        # Save to file
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(response.content)

        console.print(f"  [green]✓ Image saved: {safe_filename}[/green]")
        return safe_filename

    except Exception as e:
        console.print(f"  [yellow]⚠ Failed to download image: {e}[/yellow]")
        return None


@profile(log_slow_calls=15.0, log_all_calls=False)
def add(
    url: str = typer.Argument(..., help="Article URL to add"),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-download and re-extract (update existing article)")
):
    """Add a new article from URL.

    Args:
        url: Article URL to add
        force: Force re-download and re-extract (update existing article)
    """
    db = Database(config.get_database_path())

    # Check if article already exists
    existing = db.get_article_by_url(url)
    if existing and not force:
        console.print(f"[yellow]Article already exists: {existing.title}[/yellow]")
        console.print(f"[dim]ID: {existing.id} | Slug: {existing.slug}[/dim]")
        console.print("[dim]Use --force to update the article[/dim]")
        raise typer.Exit(0)
    elif existing and force:
        console.print(f"[cyan]Updating existing article: {existing.title}[/cyan]")

    # Scrape article
    scraper = ArticleScraper(
        raw_dir=config.get_articles_raw_dir(), parsed_dir=config.get_articles_parsed_dir()
    )
    scraped = scraper.scrape(url)

    if not scraped:
        console.print(f"[red]Failed to scrape article from {url}[/red]")
        raise typer.Exit(1)

    console.print("[cyan]Extracting metadata using Claude...[/cyan]")

    try:
        # Extract metadata using Claude skill
        metadata = extract_article_metadata.extract_article_metadata(url, scraped["content"])
        logger.info(f"Successfully extracted metadata for {url}")
    except Exception as e:
        logger.warning(f"Failed to extract metadata from AI: {e}", exc_info=True)
        console.print(f"[yellow]Warning: Failed to extract metadata: {e}[/yellow]")
        console.print("[dim]Using basic extracted data...[/dim]")

        # Fallback to basic extraction
        metadata = {
            "title": scraped["title"],
            "author": "Unknown",
            "source": urlparse(url).netloc,
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "summary": scraped["short_excerpt"],
            "tags": [],
            "article_type": "news",
            "key_points": [],
        }

    # Generate unique slug
    slug = generate_unique_slug(metadata["title"], url, db)
    logger.info(f"Generated slug: {slug}")

    # Extract cover image URL
    console.print("[cyan]Extracting cover image...[/cyan]")
    scraper_with_images = ArticleScraper(
        raw_dir=config.get_articles_raw_dir(),
        parsed_dir=config.get_articles_parsed_dir(),
    )

    # Fetch HTML for image extraction
    html = scraper_with_images.fetch_article(url)
    cover_image_url = None
    cover_image_local = None

    if html:
        cover_image_url = scraper_with_images.extract_cover_image_url(html, url)
        if cover_image_url:
            console.print(f"[green]✓[/green] Cover image URL found")

            # Download image during add phase
            images_dir = Path(config.get_articles_images_dir())
            cover_image_local = download_image(
                cover_image_url,
                images_dir,
                slug,
                force=force
            )

    # Create article object (store local path instead of remote URL)
    article = Article(
        url=url,
        title=metadata["title"],
        author=metadata["author"],
        source=metadata["source"],
        publish_date=metadata["publish_date"],
        added_date=datetime.now(),
        summary=metadata["summary"],
        tags=metadata["tags"],
        article_type=metadata["article_type"],
        key_points=metadata["key_points"],
        content=scraped["content"],
        slug=slug,
        cover_image=cover_image_local,  # Store local path
    )

    # Save to database (add or update)
    if existing and force:
        article.id = existing.id
        db.update_article(article)
        # Re-fetch to get the updated article object
        article = db.get_article_by_id(article.id)
    else:
        article = db.add_article(article)

    # Save enriched content to file
    enriched_dir = Path(config.get_articles_enriched_dir())
    enriched_dir.mkdir(parents=True, exist_ok=True)

    enriched_file = enriched_dir / f"{slug}.json"
    with open(enriched_file, "w", encoding="utf-8") as f:
        json.dump(article.to_dict(), f, ensure_ascii=False, indent=2, default=str)

    if existing and force:
        console.print(f"[green]✓[/green] Article updated successfully!")
    else:
        console.print(f"[green]✓[/green] Article added successfully!")
    console.print(f"  [dim]ID:[/dim] {article.id}")
    console.print(f"  [dim]Title:[/dim] {article.title}")
    console.print(f"  [dim]Type:[/dim] {article.article_type}")
    console.print(f"  [dim]Tags:[/dim] {', '.join(article.tags)}")
    console.print(f"  [dim]Slug:[/dim] {article.slug}")
    if cover_image_local:
        console.print(f"  [dim]Cover Image:[/dim] {cover_image_local}")

