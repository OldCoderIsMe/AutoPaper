"""Tests for AutoPaper models."""
import unittest
from datetime import datetime

from autopaper.models import Article, Issue


class TestArticle(unittest.TestCase):
    """Test cases for Article model."""

    def test_article_creation(self):
        """Test creating an article."""
        article = Article(
            url="https://example.com/article",
            title="Test Article",
            author="Test Author",
            tags=["test", "sample"],
        )

        self.assertEqual(article.url, "https://example.com/article")
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.author, "Test Author")
        self.assertEqual(article.tags, ["test", "sample"])

    def test_article_to_dict(self):
        """Test converting article to dictionary."""
        article = Article(
            id=1,
            url="https://example.com/article",
            title="Test Article",
            tags=["test"],
        )

        data = article.to_dict()

        self.assertEqual(data["id"], 1)
        self.assertEqual(data["url"], "https://example.com/article")
        self.assertEqual(data["title"], "Test Article")

    def test_article_from_dict(self):
        """Test creating article from dictionary."""
        data = {
            "id": 1,
            "url": "https://example.com/article",
            "title": "Test Article",
            "tags": ["test"],
            "key_points": ["point1", "point2"],
        }

        article = Article.from_dict(data)

        self.assertEqual(article.id, 1)
        self.assertEqual(article.url, "https://example.com/article")
        self.assertEqual(article.tags, ["test"])
        self.assertEqual(article.key_points, ["point1", "point2"])


class TestIssue(unittest.TestCase):
    """Test cases for Issue model."""

    def test_issue_creation(self):
        """Test creating an issue."""
        issue = Issue(
            slug="2026-W04-tech",
            issue_type="tech",
            start_date="2026-01-20",
            end_date="2026-01-26",
        )

        self.assertEqual(issue.slug, "2026-W04-tech")
        self.assertEqual(issue.issue_type, "tech")
        self.assertEqual(issue.start_date, "2026-01-20")
        self.assertEqual(issue.end_date, "2026-01-26")

    def test_issue_to_dict(self):
        """Test converting issue to dictionary."""
        issue = Issue(
            id=1,
            slug="2026-W04-tech",
            issue_type="tech",
        )

        data = issue.to_dict()

        self.assertEqual(data["id"], 1)
        self.assertEqual(data["slug"], "2026-W04-tech")
        self.assertEqual(data["issue_type"], "tech")


if __name__ == "__main__":
    unittest.main()
