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
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information including URL and source"),
):
    """List articles in the database.

    Args:
        tag: Filter by tag
        article_type: Filter by article type
        week: Filter by week ID
        limit: Maximum number of articles to display
        verbose: Show detailed information including URL and source
    """
    db = Database(config.get_database_path())

    # Get articles
    articles = db.list_articles(tag=tag, article_type=article_type, limit=limit)

    if not articles:
        console.print("[yellow]No articles found.[/yellow]")
        raise typer.Exit(0)

    # Create table
    if verbose:
        # Verbose mode: wider table with URL
        table = Table(title="Articles", width=None)
        table.add_column("ID", style="dim", width=5)
        table.add_column("Title", style="cyan", no_wrap=False)
        table.add_column("Source", style="green", width=10)
        table.add_column("URL", style="blue", no_wrap=False)
        table.add_column("Pub", width=10)
        table.add_column("Added", style="yellow", width=14)
    else:
        # Normal mode: concise view
        table = Table(title="Articles")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Title", style="cyan", no_wrap=False, width=40)
        table.add_column("Source", style="green", width=12)
        table.add_column("Type", width=8)
        table.add_column("Tags", width=15)
        table.add_column("Pub", width=10)
        table.add_column("Added", style="yellow", width=14)

    for article in articles:
        tags_str = ", ".join(article.tags[:2]) if article.tags else ""
        if len(article.tags) > 2:
            tags_str += f" +{len(article.tags) - 2}"

        # Format added date
        if article.added_date:
            added_str = article.added_date.strftime("%Y-%m-%d %H:%M")
        else:
            added_str = ""

        if verbose:
            # Verbose mode: show all details including URL
            title_short = article.title[:30] + "..." if len(article.title) > 33 else article.title
            url_short = article.url[:40] + "..." if len(article.url) > 43 else article.url
            source_short = article.source[:8] + ".." if len(article.source) > 10 else article.source

            table.add_row(
                str(article.id),
                title_short,
                source_short,
                url_short,
                article.publish_date or "",
                added_str,
            )
        else:
            # Normal mode: concise view
            table.add_row(
                str(article.id),
                article.title[:37] + "..." if len(article.title) > 40 else article.title,
                article.source[:10] + ".." if len(article.source) > 12 else article.source,
                article.article_type,
                tags_str,
                article.publish_date or "",
                added_str,
            )

    console.print(table)
    console.print(f"\n[dim]Total: {len(articles)} article(s)[/dim]")
    if not verbose:
        console.print("[dim]Use --verbose/-v to see URLs and more details[/dim]")
