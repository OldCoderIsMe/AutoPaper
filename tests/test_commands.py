"""Tests for AutoPaper commands."""
import os
import tempfile
import unittest
from pathlib import Path

from autopaper.database import Database
from autopaper.models import Article, Issue


class TestCommands(unittest.TestCase):
    """Test cases for CLI commands."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary database
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.db = Database(self.db_path)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_article(self):
        """Test adding an article to database."""
        article = Article(
            url="https://example.com/test",
            title="Test Article",
            author="Test Author",
            slug="test-article",
            tags=["test"],
            article_type="technical",
        )

        saved = self.db.add_article(article)

        self.assertIsNotNone(saved.id)
        self.assertEqual(saved.url, "https://example.com/test")
        self.assertEqual(saved.title, "Test Article")

    def test_get_article_by_url(self):
        """Test retrieving article by URL."""
        article = Article(
            url="https://example.com/test",
            title="Test Article",
            slug="test-article",
        )

        self.db.add_article(article)

        retrieved = self.db.get_article_by_url("https://example.com/test")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Test Article")

    def test_list_articles(self):
        """Test listing articles."""
        # Add test articles
        for i in range(3):
            article = Article(
                url=f"https://example.com/test{i}",
                title=f"Test Article {i}",
                slug=f"test-article-{i}",
                tags=["test"],
                article_type="technical",
            )
            self.db.add_article(article)

        articles = self.db.list_articles()

        self.assertEqual(len(articles), 3)

    def test_list_articles_by_type(self):
        """Test listing articles by type."""
        # Add test articles
        technical = Article(
            url="https://example.com/tech",
            title="Technical Article",
            slug="tech-article",
            article_type="technical",
        )
        news = Article(
            url="https://example.com/news",
            title="News Article",
            slug="news-article",
            article_type="news",
        )

        self.db.add_article(technical)
        self.db.add_article(news)

        technical_articles = self.db.list_articles(article_type="technical")
        news_articles = self.db.list_articles(article_type="news")

        self.assertEqual(len(technical_articles), 1)
        self.assertEqual(len(news_articles), 1)
        self.assertEqual(technical_articles[0].article_type, "technical")
        self.assertEqual(news_articles[0].article_type, "news")

    def test_add_issue(self):
        """Test adding an issue to database."""
        issue = Issue(
            slug="2026-W04-tech",
            issue_type="tech",
            start_date="2026-01-20",
            end_date="2026-01-26",
            content="# Test Issue\n\nTest content",
        )

        saved = self.db.add_issue(issue)

        self.assertIsNotNone(saved.id)
        self.assertEqual(saved.slug, "2026-W04-tech")

    def test_get_issue_by_slug(self):
        """Test retrieving issue by slug."""
        issue = Issue(
            slug="2026-W04-tech",
            issue_type="tech",
            content="# Test Issue",
        )

        self.db.add_issue(issue)

        retrieved = self.db.get_issue_by_slug("2026-W04-tech")

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.issue_type, "tech")


if __name__ == "__main__":
    unittest.main()
