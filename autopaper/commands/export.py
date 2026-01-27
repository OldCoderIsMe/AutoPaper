"""Export PDF command."""
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
import typer
from jinja2 import Template
from PIL import Image
from rich.console import Console
from weasyprint import HTML, CSS

from autopaper.config import config
from autopaper.database import Database

console = Console()


def export_pdf(
    issue_slug: str = typer.Argument(..., help="Issue slug (e.g., 2026-W04-tech)"),
    output: str = typer.Option(None, "--output", "-o", help="Output PDF path"),
    no_card: bool = typer.Option(False, "--no-card", help="Skip InfoQ card generation (faster)"),
):
    """Export an issue to PDF.

    Args:
        issue_slug: Issue slug to export
        output: Custom output path (default: issues/{slug}.pdf)
        no_card: Skip InfoQ card generation for faster export
    """
    db = Database(config.get_database_path())

    # Get issue from database
    issue = db.get_issue_by_slug(issue_slug)

    if not issue:
        console.print(f"[red]Issue not found: {issue_slug}[/red]")
        console.print("[dim]Use 'autopaper list' to see available issues[/dim]")
        raise typer.Exit(1)

    console.print(f"[cyan]Exporting issue: {issue_slug}[/cyan]")

    # Ensure database has cover_image column
    try:
        with db.get_connection() as conn:
            # Try to alter table to add cover_image column if not exists
            conn.execute("ALTER TABLE articles ADD COLUMN cover_image TEXT")
    except Exception:
        # Column already exists or error occurred
        pass

    # Read issue markdown
    issues_dir = Path(config.get_issues_dir())
    issue_file = issues_dir / f"{issue_slug}.md"

    if not issue_file.exists():
        console.print(f"[red]Issue file not found: {issue_file}[/red]")
        raise typer.Exit(1)

    with open(issue_file, "r", encoding="utf-8") as f:
        issue_markdown = f.read()

    # Parse issue to extract sections
    parse_start = time.time()
    sections = _parse_issue_markdown(issue_markdown)
    parse_time = time.time() - parse_start

    # Convert markdown sections to HTML
    convert_start = time.time()
    if sections.get("introduction"):
        sections["introduction"] = _markdown_to_html(sections["introduction"])
    if sections.get("trends"):
        sections["trends"] = _markdown_to_html(sections["trends"])
    convert_time = time.time() - convert_start

    console.print(f"[dim]Parsed in {parse_time:.2f}s, Converted in {convert_time:.2f}s[/dim]")

    # Use local cached images (downloaded during add phase)
    images_dir = issues_dir / f"{issue_slug}_images"
    images_dir.mkdir(exist_ok=True)

    console.print("[cyan]Processing cover images...[/cyan]")

    # Create slug to article mapping from database
    articles = db.get_articles()
    slug_to_cover = {article.slug: article.cover_image for article in articles}
    slug_to_url = {article.slug: article.url for article in articles}

    # Copy cached images to issue directory
    articles_images_dir = Path(config.get_articles_images_dir())
    for block in sections.get("article_blocks", []):
        slug = block.get("slug", "")

        # Get local cover image path from database
        cover_local = slug_to_cover.get(slug, "")

        if cover_local:
            # Check if source image exists
            source_path = articles_images_dir / cover_local
            if source_path.exists():
                # Copy to issue images directory
                import shutil
                dest_path = images_dir / cover_local
                if not dest_path.exists():
                    shutil.copy2(source_path, dest_path)
                    console.print(f"  [dim]✓ Copied: {slug}[/dim]")
                else:
                    console.print(f"  [dim]✓ Using cache: {slug}[/dim]")

                block["cover_image"] = f"{images_dir.name}/{cover_local}"
            else:
                console.print(f"  [yellow]⚠ Image not found: {cover_local}[/yellow]")
                block["cover_image"] = None
        else:
            block["cover_image"] = None

        # Add URL if not present
        if not block.get("url"):
            block["url"] = slug_to_url.get(slug, "")

        # Convert markdown content to HTML
        if block.get("content"):
            block["content"] = _markdown_to_html(block["content"])

    # Determine title (needed for card generation)
    if issue.issue_type == "tech":
        title = f"本周技术精选 · {issue.slug[:8]}"
    else:
        title = f"本周行业动态 · {issue.slug[:8]}"

    # Generate InfoQ card and convert to PNG (optional, can be slow)
    card_png_path = None
    if not no_card:
        console.print("[cyan]Generating InfoQ card...[/cyan]")
        card_png_path = _generate_and_convert_card(issue_markdown, title, issue.issue_type, issues_dir, issue_slug)
    else:
        console.print("[dim]Skipping InfoQ card generation (--no-card flag)[/dim]")

    # Render HTML template
    template_path = Path(__file__).parent.parent / "templates" / "issue.html.j2"

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # Render HTML
    html_content = template.render(
        title=title,
        week_range=f"{issue.start_date} to {issue.end_date}",
        generated_at=issue.created_at.strftime("%Y-%m-%d") if issue.created_at else "",
        infoq_card=card_png_path,
        **sections,
    )

    # Generate PDF
    if output is None:
        output_path = issues_dir / f"{issue_slug}.pdf"
    else:
        output_path = Path(output)

    console.print("[cyan]Generating PDF...[/cyan]")

    try:
        # Get PDF config
        pdf_config = config.get_pdf_config()

        # Create HTML document with base URL for relative image paths
        # Use issues_dir as base URL because both infocard and images are in issues_dir
        pdf_start = time.time()
        html_doc = HTML(string=html_content, base_url=str(issues_dir))

        # CSS for PDF
        css_styles = f"""
        @page {{
            size: {pdf_config.get('page_size', 'A4')};
            margin: {pdf_config.get('margin_top', '20mm')} {pdf_config.get('margin_right', '15mm')} {pdf_config.get('margin_bottom', '20mm')} {pdf_config.get('margin_left', '15mm')};
        }}
        """

        css = CSS(string=css_styles)

        # Write PDF
        html_doc.write_pdf(str(output_path), stylesheets=[css])
        pdf_time = time.time() - pdf_start

        console.print(f"[green]✓[/green] PDF exported: {output_path}")
        console.print(f"[dim]PDF generated in {pdf_time:.2f}s[/dim]")

    except Exception as e:
        console.print(f"[red]Failed to generate PDF: {e}[/red]")
        raise typer.Exit(1)



def _markdown_to_html(markdown_text: str) -> str:
    """Convert markdown text to HTML.

    Args:
        markdown_text: Markdown formatted text

    Returns:
        HTML formatted string
    """
    if not markdown_text:
        return ""

    html = markdown_text

    # Convert headers first (### Title)
    html = re.sub(r'^###\s+(.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Convert bold text **text** or __text__ to <strong>text</strong>
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)

    # Convert italic text *text* or _text_ to <em>text</em>
    html = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', html)
    html = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<em>\1</em>', html)

    # Convert code text `text` to <code>text</code>
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Convert links [text](url) to <a href="url">text</a>
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Split into lines and process
    lines = html.split('\n')
    result = []
    current_paragraph = []
    in_numbered_list = False
    in_bullet_list = False

    for line in lines:
        line = line.strip()

        if not line:
            # Empty line - end current paragraph/list
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                # For long paragraphs, split into sentences
                if len(para_text) > 100:
                    # Split by punctuation for better readability
                    sentences = re.split(r'([。！？；，])', para_text)
                    para_with_breaks = []
                    for i, sent in enumerate(sentences):
                        if sent:
                            para_with_breaks.append(sent)
                            if i < len(sentences) - 1 and sent[-1] in '。！？；，':
                                para_with_breaks.append('<br/>')
                    result.append(f'<p>{"".join(para_with_breaks)}</p>')
                else:
                    result.append(f'<p>{para_text}</p>')
                current_paragraph = []
            if in_bullet_list:
                result.append('</ul>')
                in_bullet_list = False
            if in_numbered_list:
                in_numbered_list = False

        elif line.startswith('<h4>'):
            # Header - end current paragraph
            if current_paragraph:
                result.append(f'<p>{" ".join(current_paragraph)}</p>')
                current_paragraph = []
            result.append(line)

        elif re.match(r'^(\d+)\.\s+\*\*.*?\*\*:', line):
            # Numbered list with bold title like "1. **Title:** content"
            if current_paragraph:
                result.append(f'<p>{" ".join(current_paragraph)}</p>')
                current_paragraph = []

            # Extract the title and content
            match = re.match(r'^(\d+)\.\s+\*\*(.*?)\*\*:\s*(.*)', line)
            if match:
                number = match.group(1)
                title = match.group(2)
                content = match.group(3)

                # Create styled list item
                result.append(f'<div class="trend-item">')
                result.append(f'<span class="trend-number">{number}.</span>')
                result.append(f'<strong class="trend-title">{title}:</strong> {content}')
                result.append(f'</div>')

        elif re.match(r'^\d+\.\s+', line):
            # Regular numbered list
            if in_bullet_list:
                result.append('</ul>')
                in_bullet_list = False

            content = re.sub(r'^\d+\.\s*', '', line)
            result.append(f'<p class="numbered-paragraph"><strong>{line.split(".")[0]}.</strong> {content}</p>')

        elif line.startswith(('-', '*', '+')):
            # Bullet list item
            if not in_bullet_list:
                result.append('<ul>')
                in_bullet_list = True
            content = line[1:].strip()
            result.append(f'<li>{content}</li>')

        else:
            # Regular line - add to current paragraph
            current_paragraph.append(line)

    # Add last paragraph
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        if len(para_text) > 100:
            # Split long paragraphs
            sentences = re.split(r'([。！？；，])', para_text)
            para_with_breaks = []
            for i, sent in enumerate(sentences):
                if sent:
                    para_with_breaks.append(sent)
                    if i < len(sentences) - 1 and sent and sent[-1] in '。！？；，':
                        para_with_breaks.append('<br/>')
            result.append(f'<p>{"".join(para_with_breaks)}</p>')
        else:
            result.append(f'<p>{para_text}</p>')

    # Close any open lists
    if in_bullet_list:
        result.append('</ul>')

    return '\n'.join(result)


def _parse_issue_markdown(markdown: str) -> dict:
    """Parse issue markdown into sections.

    Args:
        markdown: Issue markdown content

    Returns:
        Dictionary with sections: introduction, trends, article_blocks, news_briefs
    """
    sections = {
        "introduction": "",
        "trends": "",
        "article_blocks": [],
        "news_briefs": [],
    }

    # Map Chinese section names to English keys
    section_map = {
        "主编导语": "introduction",
        "核心趋势": "trends",
        "深度文章": "article_blocks",
        "快讯速览": "news_briefs",
    }

    lines = markdown.split("\n")
    current_section = None
    current_content = []

    for line in lines:
        if line.startswith("## "):
            # Save previous section
            if current_section:
                if current_section == "article_blocks":
                    # Parse article blocks
                    sections[current_section] = _parse_article_blocks("\n".join(current_content))
                elif current_section == "news_briefs":
                    # Parse news briefs
                    sections[current_section] = _parse_news_briefs("\n".join(current_content))
                else:
                    sections[current_section] = "\n".join(current_content).strip()

            # Start new section
            section_name = line[3:].strip()
            # Map Chinese/English names to keys
            current_section = section_map.get(section_name, section_name.lower().replace(" ", "_"))
            current_content = []

        else:
            current_content.append(line)

    # Save last section
    if current_section:
        if current_section == "article_blocks":
            sections[current_section] = _parse_article_blocks("\n".join(current_content))
        elif current_section == "news_briefs":
            sections[current_section] = _parse_news_briefs("\n".join(current_content))
        else:
            sections[current_section] = "\n".join(current_content).strip()

    return sections


def _parse_article_blocks(content: str) -> list:
    """Parse article blocks from markdown.

    Args:
        content: Article section content

    Returns:
        List of article block dictionaries
    """
    blocks = []
    current_block = None
    current_content = []

    lines = content.split("\n")

    for line in lines:
        if line.startswith("### "):
            # Save previous block
            if current_block:
                current_block["content"] = "\n".join(current_content).strip()
                blocks.append(current_block)

            # Start new block
            current_block = {
                "title": line[4:].strip(),
                "slug": "",
                "content": "",
                "tags": [],
                "url": "",
                "cover_image": None
            }
            current_content = []

        elif line.startswith("**标签**:") or line.startswith("**Tags**:"):
            # Extract tags
            tags_line = line.split(":", 1)[1].strip()
            tags = [t.strip() for t in tags_line.split(",")]
            if current_block:
                current_block["tags"] = tags

        elif line.startswith("**原文链接**:") or line.startswith("**Original URL**:"):
            # Extract URL
            url_line = line.split(":", 1)[1].strip()
            # Extract URL from markdown format: [text](url)
            if "](" in url_line:
                url_start = url_line.find("](") + 2
                url_end = url_line.find(")", url_start)
                if url_end > url_start:
                    url = url_line[url_start:url_end]
                    if current_block:
                        current_block["url"] = url

        elif line.startswith("<!-- SLUG:"):
            # Extract hidden slug
            slug = line.replace("<!-- SLUG:", "").replace("-->", "").strip()
            if current_block:
                current_block["slug"] = slug

        elif line.startswith("!["):
            # Extract cover image
            if "](" in line:
                img_start = line.find("](") + 2
                img_end = line.find(")", img_start)
                if img_end > img_start:
                    img_url = line[img_start:img_end]
                    if current_block:
                        current_block["cover_image"] = img_url

        elif "(See:" in line or "[[" in line:
            # Extract slug reference
            if "[[" in line and "]]" in line:
                start = line.find("[[") + 2
                end = line.find("]]", start)
                if current_block:
                    current_block["slug"] = line[start:end]

        else:
            current_content.append(line)

    # Save last block
    if current_block:
        current_block["content"] = "\n".join(current_content).strip()
        blocks.append(current_block)

    return blocks


def _parse_news_briefs(content: str) -> list:
    """Parse news briefs from markdown.

    Args:
        content: News briefs section content

    Returns:
        List of news brief dictionaries
    """
    briefs = []

    for line in content.split("\n"):
        if line.strip().startswith("- "):
            line = line.strip()[2:]  # Remove "- "

            # Parse "**Title**: summary" format
            if "**" in line:
                title_end = line.find("**", 2)
                if title_end > 0:
                    title = line[2:title_end]
                    summary = line[title_end + 2:].strip(": ").strip()
                    briefs.append({"title": title, "summary": summary, "url": ""})

    return briefs


def _generate_and_convert_card(
    issue_markdown: str, title: str, issue_type: str, issues_dir: Path, issue_slug: str
) -> str:
    """Generate InfoQ card SVG and convert to PNG.

    Args:
        issue_markdown: Issue markdown content
        title: Issue title
        issue_type: Issue type (tech/news)
        issues_dir: Issues directory path
        issue_slug: Issue slug

    Returns:
        Path to generated PNG file (relative to images_dir)
    """
    try:
        # Import skill
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skills"))
        import generate_infocard

        # Generate SVG card
        card_svg_path = issues_dir / f"{issue_slug}-infocard.svg"
        svg_code = generate_infocard.generate_infocard(
            content=issue_markdown, title=title, style=issue_type, key_points=None
        )

        # Save SVG
        generate_infocard.save_infocard(svg_code, str(card_svg_path))

        # Convert SVG to PNG using cairosvg (with better font handling)
        card_png_path = issues_dir / f"{issue_slug}-infocard.png"

        try:
            import cairosvg

            with open(card_svg_path, "rb") as svg_file:
                svg_data = svg_file.read()
                # Use renderbytes for better font support
                png_data = cairosvg.svg2png(bytestring=svg_data, output_width=2400, output_height=1350)

            with open(card_png_path, "wb") as png_file:
                png_file.write(png_data)

        except Exception as e:
            console.print(f"[yellow]Warning: cairosvg conversion failed: {e}[/yellow]")
            console.print("[dim]Trying alternative conversion method...[/dim]")

            # Fallback: Try svglib + reportlab
            try:
                import svglib.renderlib
                import reportlab.graphics.renderPM

                drawing = svglib.renderlib.svg2rlg(str(card_svg_path))
                svglib.renderlib.pm_to_png(drawing, write_to=str(card_png_path))
            except Exception as e2:
                console.print(f"[yellow]Warning: Alternative method also failed: {e2}[/yellow]")
                console.print("[dim]SVG file saved, but PNG conversion skipped[/dim]")
                return card_svg_path.name

        console.print(f"  [dim]✓ InfoQ card generated: {card_png_path.name}[/dim]")
        return card_png_path.name

    except Exception as e:
        console.print(f"[yellow]Warning: Failed to generate InfoQ card: {e}[/yellow]")
        return None
