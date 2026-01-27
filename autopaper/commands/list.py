"""List articles command."""
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from autopaper.config import config
from autopaper.database import Database

console = Console()


def list_articles(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    article_type: Optional[str] = typer.Option(None, "--type", help="Filter by type (technical/news)"),
    week: Optional[str] = typer.Option(None, "--week", "-w", help="Filter by week (YYYY-Www)"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Maximum number of articles to show"),
):
    """List articles in the database.

    Args:
        tag: Filter by tag
        article_type: Filter by article type
        week: Filter by week ID
        limit: Maximum number of articles to display
    """
    db = Database(config.get_database_path())

    # Get articles
    articles = db.list_articles(tag=tag, article_type=article_type, limit=limit)

    if not articles:
        console.print("[yellow]No articles found.[/yellow]")
        raise typer.Exit(0)

    # Create table
    table = Table(title="Articles")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="cyan", no_wrap=False, width=50)
    table.add_column("Type", width=10)
    table.add_column("Tags", width=20)
    table.add_column("Date", width=12)
    table.add_column("Slug", style="dim", width=20)

    for article in articles:
        tags_str = ", ".join(article.tags[:3]) if article.tags else ""
        if len(article.tags) > 3:
            tags_str += f" +{len(article.tags) - 3}"

        table.add_row(
            str(article.id),
            article.title[:47] + "..." if len(article.title) > 50 else article.title,
            article.article_type,
            tags_str,
            article.publish_date or "",
            article.slug,
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(articles)} article(s)[/dim]")
