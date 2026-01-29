"""Main CLI entry point for AutoPaper."""
import sys
from pathlib import Path

import typer
from rich.console import Console

from autopaper.commands import add, card, generate, export, sync, cover, email
import autopaper.commands.list as list_cmd
from autopaper.config import config

app = typer.Typer(
    name="autopaper",
    help="AutoPaper - CLI-driven automated newspaper generation tool",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main(
    ctx: typer.Context,
    config_path: str = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """AutoPaper - Automated newspaper generation from web articles."""
    if config_path:
        # Override config path if provided
        global config
        from autopaper.config import Config

        config = Config(config_path)

    # Ensure directories exist
    config.ensure_directories()

    # Validate API key
    if not config.get_anthropic_api_key():
        console.print(
            "[yellow]Warning: ANTHROPIC_API_KEY not set. "
            "Some features may not work properly.[/yellow]"
        )
        console.print("[dim]Set it in .env file or environment variables.[/dim]\n")


# Register commands
app.command()(add.add)
app.command()(list_cmd.list_articles)
app.command()(generate.generate)
app.command()(export.export_pdf)
app.command()(sync.sync)
app.command()(cover.generate_cover)
app.command()(card.generate_card)
app.command()(email.send_email)


@app.command()
def version():
    """Show version information."""
    console.print(f"AutoPaper version [cyan]0.1.0[/cyan]")


if __name__ == "__main__":
    app()
