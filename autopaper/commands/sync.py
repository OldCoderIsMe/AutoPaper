"""Sync to Obsidian command."""
import sys
from pathlib import Path

import typer
from rich.console import Console

from autopaper.config import config
from autopaper.database import Database

console = Console()


def sync(
    target: str = typer.Argument(..., help="Sync target (currently only 'obsidian')"),
    issue_slug: str = typer.Argument(..., help="Issue slug to sync"),
):
    """Sync an issue to external platform.

    Args:
        target: Platform to sync to (obsidian)
        issue_slug: Issue slug to sync
    """
    if target != "obsidian":
        console.print(f"[red]Unsupported sync target: {target}[/red]")
        console.print("[dim]Currently only 'obsidian' is supported[/dim]")
        raise typer.Exit(1)

    db = Database(config.get_database_path())

    # Get issue from database
    issue = db.get_issue_by_slug(issue_slug)

    if not issue:
        console.print(f"[red]Issue not found: {issue_slug}[/red]")
        raise typer.Exit(1)

    # Get articles for this issue
    # Extract article slugs from issue content
    import re

    article_slugs = re.findall(r"\[\[([^\]]+)\]\]", issue.content)

    if not article_slugs:
        console.print("[yellow]No articles found in issue[/yellow]")
        raise typer.Exit(0)

    console.print(f"[cyan]Found {len(article_slugs)} article(s) in issue[/cyan]")

    # Get article objects
    articles = []
    for slug in article_slugs:
        article = db.get_article_by_slug(slug)
        if article:
            articles.append(article)

    if not articles:
        console.print("[yellow]No valid articles found[/yellow]")
        raise typer.Exit(0)

    # Import publisher
    from autopaper.publishers.obsidian import ObsidianPublisher

    console.print("[cyan]Syncing to Obsidian...[/cyan]")

    publisher = ObsidianPublisher(
        vault_path=config.get_obsidian_vault_path(), auto_paper_folder=config.get_obsidian_auto_paper_folder()
    )

    # Publish articles and issue
    publisher.publish_issue(issue_slug, issue.content, articles)

    console.print(f"[green]✓[/green] Synced {len(articles)} article(s) and issue to Obsidian")
    console.print(f"  [dim]Vault:[/dim] {config.get_obsidian_vault_path()}")
    console.print(f"  [dim]Folder:[/dim] {config.get_obsidian_auto_paper_folder()}")
