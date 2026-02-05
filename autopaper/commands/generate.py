"""Generate issue command."""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from jinja2 import Template
from rich.console import Console

from autopaper.ai import compose_issue
from autopaper.config import config
from autopaper.database import Database
from autopaper.utils.date import get_week_id, get_last_week_id, get_week_range
from autopaper.utils.logging import get_logger
from autopaper.utils.json_parser import safe_parse_json

console = Console()
logger = get_logger(__name__)


def generate(
    issue_type: str = typer.Argument(..., help="Issue type: 'tech' or 'news'"),
    last_week: bool = typer.Option(False, "--last-week", help="Use last week instead of current week"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of articles"),
    slug: Optional[str] = typer.Option(None, "--slug", "-s", help="Custom slug for the issue"),
    sync_obsidian: bool = typer.Option(False, "--sync-obsidian", help="Sync to Obsidian after generation"),
):
    """Generate a newspaper issue from articles.

    Args:
        issue_type: Type of issue (tech or news)
        last_week: Use last week's date range
        tag: Filter articles by tag
        limit: Maximum number of articles to include
        slug: Custom issue slug
        sync_obsidian: Sync to Obsidian after generating
    """
    # Validate issue_type
    if issue_type not in ["tech", "news"]:
        console.print(f"[red]Invalid issue type: {issue_type}. Must be 'tech' or 'news'[/red]")
        raise typer.Exit(1)

    db = Database(config.get_database_path())

    # Determine week
    week_id = get_last_week_id() if last_week else get_week_id()
    start_date, end_date = get_week_range()

    console.print(f"[cyan]Generating {issue_type} issue for {week_id}[/cyan]")
    console.print(f"[dim]Week range: {start_date} to {end_date}[/dim]\n")

    # Query articles
    article_type_filter = "technical" if issue_type == "tech" else None
    articles = db.list_articles(tag=tag, article_type=article_type_filter, limit=limit)

    if not articles:
        console.print("[yellow]No articles found matching criteria[/yellow]")
        raise typer.Exit(0)

    console.print(f"[cyan]Found {len(articles)} article(s)[/cyan]")

    # Prepare articles for composition
    articles_data = [article.to_dict() for article in articles]

    console.print("[cyan]Composing issue using Claude...[/cyan]")

    try:
        # Compose issue using Claude skill
        issue_data = compose_issue.compose_issue(articles_data, issue_type=issue_type)
    except Exception as e:
        console.print(f"[red]Failed to compose issue: {e}[/red]")
        raise typer.Exit(1)

    # Ensure URLs and tags are included in article_blocks
    # Create a mapping from slug to URL, cover_image, and tags
    slug_to_url = {article.slug: article.url for article in articles}
    slug_to_cover = {article.slug: article.cover_image for article in articles}
    slug_to_tags = {article.slug: article.tags for article in articles}

    # Add URLs, cover images, and fix tags to article_blocks if missing
    for block in issue_data.get("article_blocks", []):
        if "url" not in block or not block["url"]:
            block["url"] = slug_to_url.get(block.get("slug", ""), "")
        if "cover_image" not in block or not block["cover_image"]:
            block["cover_image"] = slug_to_cover.get(block.get("slug", ""))
        # Ensure tags is a list, not a string
        if "tags" in block and isinstance(block["tags"], str):
            try:
                block["tags"] = json.loads(block["tags"])
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse tags as JSON for {block.get('slug')}: {e}")
                block["tags"] = [block["tags"]]
        # If tags is empty or missing, use original article tags
        if not block.get("tags"):
            block["tags"] = slug_to_tags.get(block.get("slug", ""), [])

    # Generate slug
    if slug is None:
        slug = f"{week_id}-{issue_type}"
    else:
        slug = slug

    # Render Markdown template
    template_path = Path(__file__).parent.parent / "templates" / "issue.md.j2"

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # Determine title
    if issue_type == "tech":
        title = f"本周技术精选 · {week_id}"
    else:
        title = f"本周行业动态 · {week_id}"

    # Render issue
    issue_markdown = template.render(
        title=title,
        introduction=issue_data.get("introduction", ""),
        trends=issue_data.get("trends", ""),
        article_blocks=issue_data.get("article_blocks", []),
        news_briefs=issue_data.get("news_briefs", []),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    # Save issue markdown
    issues_dir = Path(config.get_issues_dir())
    issues_dir.mkdir(parents=True, exist_ok=True)

    issue_file = issues_dir / f"{slug}.md"
    with open(issue_file, "w", encoding="utf-8") as f:
        f.write(issue_markdown)

    console.print(f"[green]✓[/green] Issue generated: {issue_file}")

    # Save to database
    from autopaper.models import Issue

    issue = Issue(
        slug=slug, issue_type=issue_type, start_date=start_date, end_date=end_date, content=issue_markdown
    )
    db.add_issue(issue)

    console.print(f"  [dim]Slug:[/dim] {slug}")
    console.print(f"  [dim]Articles:[/dim] {len(articles)}")

    # Sync to Obsidian if requested
    if sync_obsidian:
        console.print("\n[cyan]Syncing to Obsidian...[/cyan]")
        from autopaper.publishers.obsidian import ObsidianPublisher

        publisher = ObsidianPublisher(
            vault_path=config.get_obsidian_vault_path(),
            auto_paper_folder=config.get_obsidian_auto_paper_folder(),
        )
        publisher.publish_issue(slug, issue_markdown, articles)

        console.print(f"[green]✓[/green] Synced to Obsidian")
