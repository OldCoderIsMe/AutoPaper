# AutoPaper Documentation

Welcome to the AutoPaper documentation! This directory contains comprehensive guides and references for using and contributing to AutoPaper.

## 📚 Documentation Index

### Getting Started
- **[Quick Start Guide](QUICKSTART.md)**
  - Installation instructions
  - First-time setup
  - Basic usage examples

### Design & Architecture
- **[AutoPaper Design Document](AutoPaper-Design.md)**
  - System architecture
  - Design decisions
  - Component interactions
  - Data flow diagrams

## 📖 Reading Order

If you're new to AutoPaper, we recommend reading in this order:

1. **[README.md](../README.md)** - Project overview and features
2. **[Quick Start Guide](QUICKSTART.md)** - Get up and running quickly
3. **[Design Document](AutoPaper-Design.md)** - Understand how it works
4. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Learn how to contribute

## 🔧 Technical Details

### Core Components
- **Article Scraping** (`autopaper/scrapers/article.py`)
  - Web content extraction
  - Cover image detection
  - Metadata parsing

- **AI Integration** (`skills/`)
  - Article metadata extraction
  - Issue composition
  - Tag normalization

- **Publishing** (`autopaper/publishers/`)
  - PDF generation
  - Obsidian sync

### Utilities
- **Caching** (`autopaper/utils/cache.py`) - AI call caching
- **Retry Logic** (`autopaper/utils/retry.py`) - Retry with exponential backoff
- **Logging** (`autopaper/utils/logging.py`) - Logging system
- **Profiling** (`autopaper/utils/profiling.py`) - Performance monitoring

## 📝 Additional Resources

### Main Project Files
- [CHANGELOG.md](../CHANGELOG.md) - Version history and updates
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [LICENSE](../LICENSE) - MIT License

### Configuration
- [config.yaml](../config.yaml) - Main configuration file
- [.env.example](../.env.example) - Environment variables template

### Testing
- `tests/test_commands.py` - Command tests
- `tests/test_models.py` - Model tests
- `tests/test_scrapers.py` - Scraper tests
- `test_fixes.py` - Optimization validation tests
- `test_medium_priority.py` - Advanced feature tests

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/OldCoderIsMe/AutoPaper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OldCoderIsMe/AutoPaper/discussions)

---

**Last Updated**: 2026-01-27
