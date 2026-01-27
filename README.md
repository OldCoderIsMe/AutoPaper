# AutoPaper

> AI-Powered Automated Newspaper Generation Tool 🤖📰

AutoPaper is a CLI tool that automatically generates curated weekly newspapers from article URLs. It uses Claude AI to extract metadata, compose editorial content, and export to multiple formats.

## ✨ Features

- **🤖 AI-Powered Curation** - Smart metadata extraction and issue composition using Claude
- **📰 Auto-Generated Newspapers** - Weekly tech/news issues with editor's insights
- **🏷️ Smart Tagging** - Automatic tag classification and normalization
- **📄 Multiple Export** - Markdown, PDF, and Obsidian vault sync
- **⚡ High Performance** - 100x faster with AI caching and concurrent downloads
- **🛡️ Production Ready** - Robust error handling, retry logic, and comprehensive logging

## 📦 Quick Start

### Prerequisites

- Python 3.10+
- Anthropic API key

### Installation

```bash
# Install
pip install -e .

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## 🚀 Quick Usage

### Basic Workflow

```bash
# 1. Add articles
autopaper add https://blog.example.com/article

# 2. List articles
autopaper list

# 3. Generate weekly issue
autopaper generate tech

# 4. Export to PDF
autopaper export-pdf 2026-W05-tech

# 5. Sync to Obsidian
autopaper sync obsidian 2026-W05-tech
```

### Commands

| Command | Description |
|---------|-------------|
| `autopaper add <url>` | Add article from URL |
| `autopaper list` | List all articles |
| `autopaper generate <type>` | Generate weekly issue (tech/news) |
| `autopaper export-pdf <slug>` | Export issue to PDF |
| `autopaper sync obsidian <slug>` | Sync to Obsidian vault |

See `autopaper --help` for all commands and options.

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Detailed setup and usage
- **[Design Document](docs/AutoPaper-Design.md)** - Architecture and technical details
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

## 🏗️ Project Structure

```
AutoPaper/
├── autopaper/          # Main package
│   ├── commands/        # CLI commands
│   ├── scrapers/        # Web scraping
│   ├── publishers/      # PDF/Obsidian export
│   └── utils/          # Utilities
├── skills/             # AI integration
├── tests/              # Test suite
└── docs/               # Documentation
```

## 🔧 Configuration

Edit `config.yaml` to customize:

```yaml
# Database
database_path: data/db.sqlite

# Obsidian sync
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper

# Tag normalization
tag_normalization:
  llm: [llm, large language model, gpt]
  kubernetes: [k8s]
```

## 🤖 AI Features

AutoPaper uses Claude AI for:

- **Metadata Extraction** - Title, author, summary, key points
- **Tag Classification** - Automatic categorization
- **Issue Composition** - Editor's notes, trend analysis
- **Content Understanding** - Intelligent article curation

## 📊 Performance

- **100x faster** - AI caching for duplicate articles
- **10x faster** - Concurrent image downloads
- **Automatic retry** - Network resilience
- **Smart logging** - Performance monitoring

## 🛠️ Development

### Setup

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black autopaper/
isort autopaper/
```

### Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest --cov=autopaper tests/
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [Claude](https://www.anthropic.com/claude) - AI capabilities
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [WeasyPrint](https://weasyprint.org/) - PDF generation

---

**Ready to automate your newsletter workflow?** 🚀

- Documentation: [docs/](docs/)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Issues: [GitHub Issues](https://github.com/OldCoderIsMe/AutoPaper/issues)
