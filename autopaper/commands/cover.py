"""Generate cover image command."""
from pathlib import Path

import typer
from rich.console import Console

from autopaper.config import config

console = Console()


def generate_cover(
    issue_slug: str = typer.Argument(..., help="Issue slug (e.g., 2026-W04-tech)"),
    style: str = typer.Option("tech", help="Color scheme (tech or news)"),
    ai: bool = typer.Option(False, help="Use AI API to generate cover"),
    ai_api: str = typer.Option("dalle", help="AI API to use (dalle)"),
):
    """Generate infographic cover for an issue.

    Args:
        issue_slug: Issue slug
        style: Color scheme (tech or news)
        ai: Use AI API generation
        ai_api: Which AI API to use

    Note: This command is deprecated. Use `autopaper generate-card` instead.
    """
    console.print("[yellow]This command is deprecated.[/yellow]")
    console.print("[cyan]Please use `autopaper generate-card` instead to generate AI cards.[/cyan]")
    console.print("\n[dim]Example:[/dim]")
    console.print(f"  autopaper generate-card {issue_slug}")
    raise typer.Exit(0)
