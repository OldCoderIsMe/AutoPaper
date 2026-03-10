"""Delete article command."""
from pathlib import Path

import typer
from rich.console import Console

from autopaper.config import config
from autopaper.database import Database

console = Console()


def delete(
    article_id: int = typer.Argument(..., help="Article ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt"),
):
    """Delete an article by ID.

    This will remove the article from the database and optionally clean up
    associated files (enriched JSON, images, raw HTML, parsed content).

    Args:
        article_id: Article ID to delete
        force: Skip confirmation prompt
    """
    db = Database(config.get_database_path())

    # Get article first to show info and get slug for file cleanup
    article = db.get_article_by_id(article_id)

    if not article:
        console.print(f"[red]Article with ID {article_id} not found.[/red]")
        raise typer.Exit(1)

    # Show article info
    console.print(f"\n[cyan]Article to delete:[/cyan]")
    console.print(f"  [dim]ID:[/dim] {article.id}")
    console.print(f"  [dim]Title:[/dim] {article.title}")
    console.print(f"  [dim]Source:[/dim] {article.source}")
    console.print(f"  [dim]URL:[/dim] {article.url}")
    console.print(f"  [dim]Slug:[/dim] {article.slug}")

    # Confirm deletion
    if not force:
        console.print("\n[yellow]This will delete the article and its metadata from the database.[/yellow]")
        console.print("[dim]Associated files (enriched JSON, images, cached content) will remain.[/dim]")
        confirm = typer.confirm("Do you want to continue?")
        if not confirm:
            console.print("[dim]Deletion cancelled.[/dim]")
            raise typer.Exit(0)

    # Delete from database
    success = db.delete_article(article_id)

    if success:
        console.print(f"[green]✓ Article deleted from database[/green]")

        # Optional: Clean up associated files
        slug = article.slug

        # Clean up enriched JSON
        enriched_dir = Path(config.get_articles_enriched_dir())
        enriched_file = enriched_dir / f"{slug}.json"
        if enriched_file.exists():
            try:
                enriched_file.unlink()
                console.print(f"  [dim]✓ Deleted enriched JSON[/dim]")
            except Exception as e:
                console.print(f"  [yellow]⚠ Could not delete enriched JSON: {e}[/yellow]")

        # Clean up cover image
        if article.cover_image:
            images_dir = Path(config.get_articles_images_dir())
            image_file = images_dir / article.cover_image
            if image_file.exists():
                try:
                    image_file.unlink()
                    console.print(f"  [dim]✓ Deleted cover image[/dim]")
                except Exception as e:
                    console.print(f"  [yellow]⚠ Could not delete cover image: {e}[/yellow]")

        # Clean up raw HTML
        raw_dir = Path(config.get_articles_raw_dir())
        raw_file = raw_dir / f"{slug}.html"
        if raw_file.exists():
            try:
                raw_file.unlink()
                console.print(f"  [dim]✓ Deleted raw HTML[/dim]")
            except Exception as e:
                console.print(f"  [yellow]⚠ Could not delete raw HTML: {e}[/yellow]")

        # Clean up parsed content
        parsed_dir = Path(config.get_articles_parsed_dir())
        parsed_file = parsed_dir / f"{slug}.json"
        if parsed_file.exists():
            try:
                parsed_file.unlink()
                console.print(f"  [dim]✓ Deleted parsed content[/dim]")
            except Exception as e:
                console.print(f"  [yellow]⚠ Could not delete parsed content: {e}[/yellow]")

        console.print(f"\n[green]Article deleted successfully![/green]")
    else:
        console.print(f"[red]Failed to delete article[/red]")
        raise typer.Exit(1)
