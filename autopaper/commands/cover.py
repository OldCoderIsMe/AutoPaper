"""Generate cover image command."""
import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

from autopaper.config import config

# Import the cover generators
# Add project root to path for imports
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))
from scripts.generate_simple_cover import generate_cover_image

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
    """
    # Find markdown file
    issues_dir = Path(config.get_issues_dir())
    markdown_file = issues_dir / f"{issue_slug}.md"

    if not markdown_file.exists():
        console.print(f"[red]Markdown file not found: {markdown_file}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Generating cover for {issue_slug}[/cyan]")
    console.print(f"[dim]Style: {style}[/dim]")
    if ai:
        console.print(f"[dim]AI Generation: {ai_api}[/dim]\n")

    # Generate cover using selected generator
    output_file = issues_dir / f"{issue_slug}-cover.png"

    # Extract title and key points
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    title = "Weekly Review"
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break

    console.print(f"[dim]Title: {title}[/dim]")

    if ai and ai_api == "dalle":
        # Use DALL-E API
        try:
            from generate_ai_cover import generate_dalle_cover

            # Extract key points
            key_points = []
            in_articles = False
            for line in content.split('\n'):
                if line.startswith('## 深度文章'):
                    in_articles = True
                    continue
                if in_articles and line.startswith('### '):
                    # Extract article titles as key points
                    article_title = line[4:].strip()
                    if len(article_title) < 100:
                        key_points.append(article_title)
                    if len(key_points) >= 4:
                        break

            success = generate_dalle_cover(
                title=title,
                key_points=key_points,
                output_file=str(output_file),
                style=style,
            )

            if success:
                console.print(f"\n[green]✓ AI Cover image generated successfully![/green]")
                console.print(f"  📁 {output_file}")
                console.print(f"\n[cyan]You can use this image for:[/cyan]")
                console.print(f"  • Social media sharing")
                console.print(f"  • Newsletter thumbnail")
                console.print(f"  • Blog post cover")
            else:
                raise typer.Exit(1)

        except ImportError:
            console.print("[yellow]openai package not installed. Falling back to simple generator.[/yellow]")
            success = generate_cover_image(str(markdown_file), str(output_file), style)
        except Exception as e:
            console.print(f"[yellow]AI generation failed: {e}. Falling back to simple generator.[/yellow]")
            success = generate_cover_image(str(markdown_file), str(output_file), style)
    else:
        # Use built-in generator
        success = generate_cover_image(str(markdown_file), str(output_file), style)

    if success:
        console.print(f"\n[green]✓ Cover image generated successfully![/green]")
        console.print(f"  📁 {output_file}")
        console.print(f"\n[cyan]You can use this image for:[/cyan]")
        console.print(f"  • Social media sharing")
        console.print(f"  • Newsletter thumbnail")
        console.print(f"  • Blog post cover")
    else:
        raise typer.Exit(1)
