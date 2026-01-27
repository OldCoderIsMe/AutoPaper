"""Generate InfoQ-style summary card command."""
import sys
from pathlib import Path

import typer
from rich.console import Console

from autopaper.config import config

# Import skill
sys_path = str(Path(__file__).parent.parent.parent / "skills")
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

import generate_infocard

console = Console()


def generate_card(
    title: str = typer.Argument(..., help="Card title (e.g., '本周技术精选 · 2026-W04')"),
    output: str = typer.Option(None, "--output", "-o", help="Output SVG path"),
    style: str = typer.Option("tech", help="Card style (tech or news)"),
    content: str = typer.Option(None, "--content", "-c", help="Content file path (markdown)"),
):
    """Generate InfoQ-style technical summary card (landscape, 16:9).

    Args:
        title: Card title
        output: Output SVG path (default: issues/{title}-infocard.svg)
        style: Card style (tech or news)
        content: Path to markdown file with content
    """
    # Determine output path
    if output is None:
        issues_dir = Path(config.get_issues_dir())
        safe_title = title.replace(" ", "-").replace("/", "-")[:50]
        output = str(issues_dir / f"{safe_title}-infocard.svg")

    # Get content
    if content:
        # Read from file
        content_path = Path(content)
        if not content_path.exists():
            console.print(f"[red]Content file not found: {content_path}[/red]")
            raise typer.Exit(1)

        with open(content_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

    else:
        # Use sample content
        markdown_content = f"""# {title}

本周技术精选汇总，涵盖AI编程、云原生、系统架构等前沿技术话题。

## 核心要点
- AI编程工具从对话式向闭环式演进
- 自主Agent架构成为新趋势
- 云原生技术持续深化
- 开发者工具链无缝集成
"""

    console.print(f"[cyan]Generating InfoQ-style technical card...[/cyan]")
    console.print(f"[dim]Title: {title}[/dim]")
    console.print(f"[dim]Style: {style}[/dim]")
    console.print(f"[dim]Output: {output}[/dim]")
    console.print(f"[dim]Format: 1200x675 (16:9 landscape)[/dim]\n")

    try:
        # Generate InfoQ card
        svg_code = generate_infocard.generate_infocard(
            content=markdown_content,
            title=title,
            style=style,
            key_points=None,  # Let the skill extract from content
        )

        # Save to file
        generate_infocard.save_infocard(svg_code, output)

        console.print(f"[green]✓[/green] InfoQ card generated successfully!")
        console.print(f"  📁 {output}")
        console.print(f"\n[cyan]Usage:[/cyan]")
        console.print(f"  • Technical blog cover")
        console.print(f"  • Social media sharing (Twitter, LinkedIn)")
        console.print(f"  • Presentation slide")
        console.print(f"  • Newsletter thumbnail")

    except Exception as e:
        console.print(f"[red]Failed to generate card: {e}[/red]")
        raise typer.Exit(1)
