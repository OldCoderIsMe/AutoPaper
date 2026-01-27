"""Database connection and operations management."""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from autopaper.models import Article, Issue
from autopaper.utils.logging import get_logger

logger = get_logger(__name__)


class Database:
    """Database manager for AutoPaper."""

    def __init__(self, db_path: str = "data/db.sqlite"):
        """Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Get database connection with context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            # Articles table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    author TEXT,
                    source TEXT,
                    publish_date TEXT,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    summary TEXT,
                    tags TEXT,
                    article_type TEXT,
                    key_points TEXT,
                    content TEXT,
                    slug TEXT,
                    cover_image TEXT
                )
                """
            )

            # Issues table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE NOT NULL,
                    issue_type TEXT NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Create indexes for better query performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_slug ON articles(slug)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_type ON articles(article_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_issues_slug ON issues(slug)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_issues_type ON issues(issue_type)")

    # Article operations

    def add_article(self, article: Article) -> Article:
        """Add a new article to the database.

        Args:
            article: Article object to add

        Returns:
            Article with assigned ID
        """
        import json

        logger.debug(f"Adding article: {article.slug} - {article.title[:50]}")

        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO articles (
                        url, title, author, source, publish_date, added_date,
                        summary, tags, article_type, key_points, content, slug, cover_image
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article.url,
                        article.title,
                        article.author,
                        article.source,
                        article.publish_date,
                        article.added_date.isoformat() if article.added_date else datetime.now().isoformat(),
                        article.summary,
                        json.dumps(article.tags) if article.tags else "[]",
                        article.article_type,
                        json.dumps(article.key_points) if article.key_points else "[]",
                        article.content,
                        article.slug,
                        article.cover_image,
                    ),
                )
                article.id = cursor.lastrowid
                logger.info(f"Article added successfully: ID={article.id}, slug={article.slug}")
        except sqlite3.IntegrityError as e:
            logger.error(f"Failed to add article (duplicate?): {e}")
            raise

        return article

    def get_articles(self) -> List[Article]:
        """Get all articles.

        Returns:
            List of all Article objects
        """
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles ORDER BY added_date DESC").fetchall()
            return [Article.from_row(tuple(row)) for row in rows]

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """Get article by ID.

        Args:
            article_id: Article ID

        Returns:
            Article object or None if not found
        """
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
            if row:
                return Article.from_row(tuple(row))
        return None

    def get_article_by_url(self, url: str) -> Optional[Article]:
        """Get article by URL.

        Args:
            url: Article URL

        Returns:
            Article object or None if not found
        """
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM articles WHERE url = ?", (url,)).fetchone()
            if row:
                return Article.from_row(tuple(row))
        return None

    def get_article_by_slug(self, slug: str) -> Optional[Article]:
        """Get article by slug.

        Args:
            slug: Article slug

        Returns:
            Article object or None if not found
        """
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM articles WHERE slug = ?", (slug,)).fetchone()
            if row:
                return Article.from_row(tuple(row))
        return None

    def list_articles(
        self, tag: Optional[str] = None, article_type: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Article]:
        """List articles with optional filters.

        Args:
            tag: Filter by tag
            article_type: Filter by article type ('technical' or 'news')
            limit: Maximum number of articles to return

        Returns:
            List of Article objects
        """
        query = "SELECT * FROM articles WHERE 1=1"
        params = []

        if tag:
            query += " AND tags LIKE ?"
            params.append(f"%{tag}%")

        if article_type:
            query += " AND article_type = ?"
            params.append(article_type)

        query += " ORDER BY added_date DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [Article.from_row(tuple(row)) for row in rows]

    def update_article(self, article: Article) -> bool:
        """Update an existing article.

        Args:
            article: Article object with updated fields

        Returns:
            True if updated, False if not found
        """
        import json

        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE articles SET
                    title = ?, author = ?, source = ?, publish_date = ?,
                    summary = ?, tags = ?, article_type = ?, key_points = ?,
                    content = ?, slug = ?, cover_image = ?
                WHERE id = ?
                """,
                (
                    article.title,
                    article.author,
                    article.source,
                    article.publish_date,
                    article.summary,
                    json.dumps(article.tags) if article.tags else "[]",
                    article.article_type,
                    json.dumps(article.key_points) if article.key_points else "[]",
                    article.content,
                    article.slug,
                    article.cover_image,
                    article.id,
                ),
            )
            return cursor.rowcount > 0

    def delete_article(self, article_id: int) -> bool:
        """Delete an article.

        Args:
            article_id: Article ID to delete

        Returns:
            True if deleted, False if not found
        """
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            return cursor.rowcount > 0

    # Issue operations

    def add_issue(self, issue: Issue) -> Issue:
        """Add a new issue to the database.

        Args:
            issue: Issue object to add

        Returns:
            Issue with assigned ID
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO issues (slug, issue_type, start_date, end_date, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    issue.slug,
                    issue.issue_type,
                    issue.start_date,
                    issue.end_date,
                    issue.content,
                    issue.created_at.isoformat() if issue.created_at else datetime.now().isoformat(),
                ),
            )
            issue.id = cursor.lastrowid
        return issue

    def get_issue_by_slug(self, slug: str) -> Optional[Issue]:
        """Get issue by slug.

        Args:
            slug: Issue slug

        Returns:
            Issue object or None if not found
        """
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM issues WHERE slug = ?", (slug,)).fetchone()
            if row:
                return Issue.from_row(tuple(row))
        return None

    def list_issues(self, issue_type: Optional[str] = None, limit: Optional[int] = None) -> List[Issue]:
        """List issues with optional filters.

        Args:
            issue_type: Filter by issue type ('tech' or 'news')
            limit: Maximum number of issues to return

        Returns:
            List of Issue objects
        """
        query = "SELECT * FROM issues WHERE 1=1"
        params = []

        if issue_type:
            query += " AND issue_type = ?"
            params.append(issue_type)

        query += " ORDER BY created_at DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [Issue.from_row(tuple(row)) for row in rows]

    def update_issue(self, issue: Issue) -> bool:
        """Update an existing issue.

        Args:
            issue: Issue object with updated fields

        Returns:
            True if updated, False if not found
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE issues SET
                    issue_type = ?, start_date = ?, end_date = ?, content = ?
                WHERE id = ?
                """,
                (issue.issue_type, issue.start_date, issue.end_date, issue.content, issue.id),
            )
            return cursor.rowcount > 0
