"""Tests for article scrapers."""
import os
import tempfile
import unittest
from pathlib import Path

from autopaper.scrapers.article import ArticleScraper


class TestArticleScraper(unittest.TestCase):
    """Test cases for ArticleScraper."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.raw_dir = os.path.join(self.temp_dir, "raw")
        self.parsed_dir = os.path.join(self.temp_dir, "parsed")

        self.scraper = ArticleScraper(raw_dir=self.raw_dir, parsed_dir=self.parsed_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_content(self):
        """Test content extraction from HTML."""
        html = """
        <html>
            <head><title>Test Article</title></head>
            <body>
                <div id="main">
                    <h1>Main Content</h1>
                    <p>This is the main content of the article.</p>
                    <p>It contains multiple paragraphs.</p>
                </div>
                <div id="sidebar">Sidebar content</div>
            </body>
        </html>
        """

        extracted = self.scraper.extract_content(html)

        self.assertIsNotNone(extracted["title"])
        self.assertIn("content", extracted)
        self.assertIn("short_excerpt", extracted)

    def test_url_to_filename(self):
        """Test URL to filename conversion."""
        url1 = "https://example.com/article"
        filename1 = self.scraper._url_to_filename(url1, "html")
        self.assertTrue(filename1.endswith(".html"))
        self.assertNotIn("/", filename1)
        self.assertNotIn(":", filename1)

        url2 = "https://example.com/blog/test-post"
        filename2 = self.scraper._url_to_filename(url2, "json")
        self.assertTrue(filename2.endswith(".json"))
        self.assertIn("blog_test-post", filename2)

    def test_save_and_load_parsed(self):
        """Test saving and loading parsed content."""
        url = "https://example.com/test"
        parsed_data = {
            "url": url,
            "title": "Test Article",
            "content": "Test content",
        }

        # Save
        saved_path = self.scraper.save_parsed(url, parsed_data)
        self.assertTrue(saved_path.exists())

        # Load
        loaded = self.scraper.load_parsed(url)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["url"], url)
        self.assertEqual(loaded["title"], "Test Article")


if __name__ == "__main__":
    unittest.main()
