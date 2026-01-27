"""PDF publisher for exporting issues to PDF."""
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from jinja2 import Template
from rich.console import Console
from weasyprint import HTML, CSS

console = Console()


class PDFPublisher:
    """Publisher for exporting issues to PDF."""

    def __init__(self, template_path: str = None, css_path: str = None):
        """Initialize PDF publisher.

        Args:
            template_path: Path to HTML template
            css_path: Path to custom CSS file
        """
        if template_path is None:
            template_path = Path(__file__).parent.parent / "templates" / "issue.html.j2"

        self.template_path = Path(template_path)
        self.css_path = css_path

    def publish(
        self,
        issue_slug: str,
        issue_markdown: str,
        start_date: str,
        end_date: str,
        issue_type: str,
        output_path: str = None,
    ) -> str:
        """Export an issue to PDF.

        Args:
            issue_slug: Issue slug
            issue_markdown: Issue markdown content
            start_date: Issue start date
            end_date: Issue end date
            issue_type: Issue type (tech or news)
            output_path: Output PDF path

        Returns:
            Path to generated PDF
        """
        # Parse issue markdown
        sections = self._parse_issue_markdown(issue_markdown)

        # Load and render template
        with open(self.template_path, "r", encoding="utf-8") as f:
            template = Template(f.read())

        # Determine title
        if issue_type == "tech":
            title = f"本周技术精选 · {issue_slug[:8]}"
        else:
            title = f"本周行业动态 · {issue_slug[:8]}"

        # Render HTML
        html_content = template.render(
            title=title,
            week_range=f"{start_date} to {end_date}",
            generated_at=datetime.now().strftime("%Y-%m-%d"),
            introduction=sections.get("introduction", ""),
            trends=sections.get("trends", ""),
            article_blocks=sections.get("article_blocks", []),
            news_briefs=sections.get("news_briefs", []),
        )

        # Generate PDF
        if output_path is None:
            output_path = f"{issue_slug}.pdf"

        console.print("[cyan]Generating PDF...[/cyan]")

        try:
            # Create HTML document
            html_doc = HTML(string=html_content, base_url=".")

            # CSS for PDF
            css_styles = """
            @page {
                size: A4;
                margin: 20mm 15mm 20mm 15mm;
            }
            """

            css = CSS(string=css_styles)

            # Add custom CSS if provided
            stylesheets = [css]
            if self.css_path:
                stylesheets.append(CSS(filename=self.css_path))

            # Write PDF
            html_doc.write_pdf(output_path, stylesheets=stylesheets)

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate PDF: {e}")

    def _parse_issue_markdown(self, markdown: str) -> Dict:
        """Parse issue markdown into sections.

        Args:
            markdown: Issue markdown content

        Returns:
            Dictionary with sections
        """
        sections = {"introduction": "", "trends": "", "article_blocks": [], "news_briefs": []}

        lines = markdown.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    if current_section == "article_blocks":
                        sections[current_section] = self._parse_article_blocks("\n".join(current_content))
                    elif current_section == "news_briefs":
                        sections[current_section] = self._parse_news_briefs("\n".join(current_content))
                    else:
                        sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                section_name = line[3:].strip()
                current_section = self._normalize_section_name(section_name)
                current_content = []

            else:
                current_content.append(line)

        # Save last section
        if current_section:
            if current_section == "article_blocks":
                sections[current_section] = self._parse_article_blocks("\n".join(current_content))
            elif current_section == "news_briefs":
                sections[current_section] = self._parse_news_briefs("\n".join(current_content))
            else:
                sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _normalize_section_name(self, name: str) -> str:
        """Normalize section name to key.

        Args:
            name: Section name from markdown

        Returns:
            Normalized key
        """
        name_map = {
            "主编导语": "introduction",
            "editor's introduction": "introduction",
            "核心趋势": "trends",
            "core trends": "trends",
            "深度文章": "article_blocks",
            "in-depth articles": "article_blocks",
            "快讯速览": "news_briefs",
            "news briefs": "news_briefs",
        }

        return name_map.get(name.lower(), name.lower().replace(" ", "_"))

    def _parse_article_blocks(self, content: str) -> List[Dict]:
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
                current_block = {"title": line[4:].strip(), "slug": "", "content": "", "tags": []}
                current_content = []

            elif line.startswith("**标签**:") or line.startswith("**Tags**:"):
                # Extract tags
                tags_line = line.split(":", 1)[1].strip()
                tags = [t.strip() for t in tags_line.split(",")]
                if current_block:
                    current_block["tags"] = tags

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

    def _parse_news_briefs(self, content: str) -> List[Dict]:
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
