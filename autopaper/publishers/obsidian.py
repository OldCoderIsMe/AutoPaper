"""Obsidian publisher for syncing articles and issues to Obsidian vault."""
import json
from datetime import datetime
from pathlib import Path
from typing import List

from rich.console import Console

from autopaper.models import Article

console = Console()


class ObsidianPublisher:
    """Publisher for syncing content to Obsidian vault."""

    def __init__(self, vault_path: str, auto_paper_folder: str = "AutoPaper"):
        """Initialize Obsidian publisher.

        Args:
            vault_path: Path to Obsidian vault
            auto_paper_folder: Folder name for AutoPaper content
        """
        self.vault_path = Path(vault_path).expanduser()
        self.auto_paper_folder = auto_paper_folder

        # Create directories
        self.articles_dir = self.vault_path / auto_paper_folder / "Articles"
        self.issues_dir = self.vault_path / auto_paper_folder / "Issues"

        self.articles_dir.mkdir(parents=True, exist_ok=True)
        self.issues_dir.mkdir(parents=True, exist_ok=True)

    def publish_article(self, article: Article):
        """Publish an article to Obsidian.

        Args:
            article: Article object to publish
        """
        article_file = self.articles_dir / f"{article.slug}.md"

        # Generate frontmatter
        frontmatter = {
            "type": "article",
            "source": article.source,
            "author": article.author,
            "tags": article.tags,
            "publish_date": article.publish_date,
            "article_type": article.article_type,
            "url": article.url,
        }

        # Generate content
        content = self._format_article_frontmatter(frontmatter)
        content += f"\n# {article.title}\n\n"
        content += f"**原文链接**: [{article.url}]({article.url})\n\n"

        if article.summary:
            content += "## 摘要\n\n"
            content += f"{article.summary}\n\n"

        if article.key_points:
            content += "## 关键点\n\n"
            for point in article.key_points:
                content += f"- {point}\n"
            content += "\n"

        # Write to file
        with open(article_file, "w", encoding="utf-8") as f:
            f.write(content)

        console.print(f"  [dim]Published article:[/dim] {article.slug}")

    def publish_issue(self, issue_slug: str, issue_content: str, articles: List[Article]):
        """Publish an issue to Obsidian.

        Args:
            issue_slug: Issue slug
            issue_content: Issue markdown content
            articles: List of articles in the issue
        """
        # First publish all articles
        for article in articles:
            self.publish_article(article)

        # Clean up issue content: remove SLUG comments
        import re
        clean_content = re.sub(r'<!-- SLUG:[^ ]+ -->\n?', '', issue_content)

        # Parse issue slug to get metadata
        parts = issue_slug.split("-")
        if len(parts) >= 3:
            week = f"{parts[0]}-{parts[1]}"
            issue_type = parts[2] if len(parts) > 2 else "tech"
        else:
            week = ""
            issue_type = "tech"

        # Generate issue file
        issue_file = self.issues_dir / f"{issue_slug}.md"

        # Generate frontmatter
        frontmatter = {
            "type": "issue",
            "week": week,
            "category": issue_type,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "article_count": len(articles),
        }

        content = self._format_issue_frontmatter(frontmatter)
        content += "\n"
        content += clean_content

        # Write to file
        with open(issue_file, "w", encoding="utf-8") as f:
            f.write(content)

        console.print(f"  [dim]Published issue:[/dim] {issue_slug}")

    def _format_article_frontmatter(self, metadata: dict) -> str:
        """Format YAML frontmatter for article.

        Args:
            metadata: Article metadata dictionary

        Returns:
            YAML frontmatter string
        """
        lines = ["---"]
        for key, value in metadata.items():
            if key == "tags":
                lines.append(f"{key}:")
                for tag in value:
                    lines.append(f"  - {tag}")
            elif value:
                lines.append(f'{key}: "{value}"')
        lines.append("---")
        return "\n".join(lines)

    def _format_issue_frontmatter(self, metadata: dict) -> str:
        """Format YAML frontmatter for issue.

        Args:
            metadata: Issue metadata dictionary

        Returns:
            YAML frontmatter string
        """
        lines = ["---"]
        for key, value in metadata.items():
            if isinstance(value, str) and value:
                lines.append(f'{key}: "{value}"')
            elif isinstance(value, (int, float)):
                lines.append(f"{key}: {value}")
        lines.append("---")
        return "\n".join(lines)
