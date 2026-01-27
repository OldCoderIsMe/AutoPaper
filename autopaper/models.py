"""Data models for AutoPaper."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class Article:
    """Article model representing a saved article."""

    id: Optional[int] = None
    url: str = ""
    title: str = ""
    author: str = ""
    source: str = ""
    publish_date: str = ""
    added_date: Optional[datetime] = None
    summary: str = ""
    tags: List[str] = field(default_factory=list)
    article_type: str = ""  # 'technical' or 'news'
    key_points: List[str] = field(default_factory=list)
    content: str = ""
    slug: str = ""
    cover_image: Optional[str] = None  # Path to cover image

    def to_dict(self) -> dict:
        """Convert article to dictionary."""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "author": self.author,
            "source": self.source,
            "publish_date": self.publish_date,
            "added_date": self.added_date.isoformat() if self.added_date else None,
            "summary": self.summary,
            "tags": json.dumps(self.tags),
            "article_type": self.article_type,
            "key_points": json.dumps(self.key_points),
            "content": self.content,
            "slug": self.slug,
            "cover_image": self.cover_image,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Article":
        """Create article from dictionary."""
        tags = json.loads(data["tags"]) if isinstance(data.get("tags"), str) else data.get("tags", [])
        key_points = (
            json.loads(data["key_points"]) if isinstance(data.get("key_points"), str) else data.get("key_points", [])
        )

        return cls(
            id=data.get("id"),
            url=data.get("url", ""),
            title=data.get("title", ""),
            author=data.get("author", ""),
            source=data.get("source", ""),
            publish_date=data.get("publish_date", ""),
            added_date=datetime.fromisoformat(data["added_date"]) if data.get("added_date") else None,
            summary=data.get("summary", ""),
            tags=tags,
            article_type=data.get("article_type", ""),
            key_points=key_points,
            content=data.get("content", ""),
            slug=data.get("slug", ""),
            cover_image=data.get("cover_image"),
        )

    @classmethod
    def from_row(cls, row: tuple) -> "Article":
        """Create article from database row."""
        # Handle both old (13 columns) and new (14 columns) schemas
        if len(row) == 14:
            (
                article_id,
                url,
                title,
                author,
                source,
                publish_date,
                added_date,
                summary,
                tags,
                article_type,
                key_points,
                content,
                slug,
                cover_image,
            ) = row
        else:
            (
                article_id,
                url,
                title,
                author,
                source,
                publish_date,
                added_date,
                summary,
                tags,
                article_type,
                key_points,
                content,
                slug,
            ) = row
            cover_image = None

        tags_list = json.loads(tags) if tags else []
        key_points_list = json.loads(key_points) if key_points else []

        return cls(
            id=article_id,
            url=url,
            title=title or "",
            author=author or "",
            source=source or "",
            publish_date=publish_date or "",
            added_date=datetime.fromisoformat(added_date) if added_date else None,
            summary=summary or "",
            tags=tags_list,
            article_type=article_type or "",
            key_points=key_points_list,
            content=content or "",
            slug=slug or "",
            cover_image=cover_image,
        )


@dataclass
class Issue:
    """Issue model representing a generated newspaper issue."""

    id: Optional[int] = None
    slug: str = ""
    issue_type: str = ""  # 'tech' or 'news'
    start_date: str = ""
    end_date: str = ""
    content: str = ""
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert issue to dictionary."""
        return {
            "id": self.id,
            "slug": self.slug,
            "issue_type": self.issue_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Issue":
        """Create issue from dictionary."""
        return cls(
            id=data.get("id"),
            slug=data.get("slug", ""),
            issue_type=data.get("issue_type", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            content=data.get("content", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
        )

    @classmethod
    def from_row(cls, row: tuple) -> "Issue":
        """Create issue from database row."""
        issue_id, slug, issue_type, start_date, end_date, content, created_at = row

        return cls(
            id=issue_id,
            slug=slug,
            issue_type=issue_type,
            start_date=start_date or "",
            end_date=end_date or "",
            content=content or "",
            created_at=datetime.fromisoformat(created_at) if created_at else None,
        )
