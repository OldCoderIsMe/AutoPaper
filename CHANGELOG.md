# Changelog

All notable changes to AutoPaper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- AI call caching system (100x speedup for duplicate articles)
- Concurrent image downloading (10x speedup)
- Retry mechanism with exponential backoff
- Performance profiling tools
- Configuration validation with Pydantic
- Comprehensive logging system
- Unified JSON parsing utilities
- Unique slug generation to prevent conflicts

### Changed
- Updated AI model to `claude-sonnet-4-5-20250929`
- Improved error handling and exception management
- Enhanced article metadata extraction

### Fixed
- Slug conflict issues that could cause data overwrite
- JSON parsing robustness for AI responses
- Network request failures now retry automatically

## [0.1.0] - 2026-01-27

### Added
- Initial release of AutoPaper
- Article management system
  - Add articles from URLs
  - AI-powered metadata extraction using Claude
  - Automatic cover image detection
  - Tag and category management

- AI-powered newspaper generation
  - Weekly tech/news issues
  - Intelligent article curation
  - Editor's introduction and trend analysis
  - InfoQ-style summary cards

- Export capabilities
  - PDF export with WeasyPrint
  - Markdown export
  - Obsidian vault sync

- CLI interface
  - `autopaper add` - Add articles from URLs
  - `autopaper list-articles` - List articles in database
  - `autopaper generate` - Generate newspaper issues
  - `autopaper export-pdf` - Export issues to PDF
  - `autopaper sync` - Sync to Obsidian
  - `autopaper generate-cover` - Generate infographic covers
  - `autopaper generate-card` - Generate InfoQ-style cards

- Scraping system
  - Support for multiple websites (WeChat, Cursor Blog, Claude docs)
  - Content extraction with readability-lxml
  - Cover image extraction

- Database
  - SQLite storage for articles and issues
  - Flexible querying and filtering

- Configuration
  - YAML-based configuration
  - Environment variable support
  - Obsidian integration settings

### Architecture
- Modular command structure
- Service layer for business logic
- Utility functions for reusability
- Skills-based AI integration

### Documentation
- Comprehensive README
- Quick start guide
- Design documentation
- Installation instructions

### Dependencies
- typer >= 0.9.0 (CLI framework)
- rich >= 13.7.0 (Terminal output)
- requests >= 2.31.0 (HTTP client)
- readability-lxml >= 0.8.1 (Content extraction)
- anthropic >= 0.18.0 (Claude AI)
- jinja2 >= 3.1.3 (Template engine)
- weasyprint >= 60.0 (PDF generation)
- pyyaml >= 6.0.1 (Configuration)
- python-slugify >= 8.0.0 (URL slugs)
- beautifulsoup4 >= 4.12.0 (HTML parsing)

### Python Support
- Python 3.10+
- Tested on macOS and Linux

---

## Version History Format

Each version section includes:
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes
