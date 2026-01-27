# AutoPaper Skill

AI-powered automated newspaper generation tool for curating and publishing weekly newsletters.

## 📋 Overview

AutoPaper is an intelligent content curation skill that automates the process of creating weekly newsletters/newspapers from article URLs. It leverages Claude AI to extract metadata, compose editorial content, and export to multiple formats (Markdown, PDF, Obsidian).

## 🎯 Use Cases

- **Weekly Tech Newsletters**: Automatically curate and generate weekly tech digest for your team
- **Research Summaries**: Create research paper collections with AI-generated summaries
- **Content Curation**: Build personal knowledge bases from curated articles
- **Team Updates**: Generate automated weekly updates from shared articles
- **Knowledge Management**: Sync newsletters to Obsidian for long-term knowledge storage

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://www.anthropic.com/))
- pip package manager

### Install via pip

```bash
pip install git+https://github.com/OldCoderIsMe/AutoPaper.git
```

### Install from source

```bash
git clone https://github.com/OldCoderIsMe/AutoPaper.git
cd AutoPaper
pip install -e .
```

### Configure

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## 🚀 Usage

### Basic Workflow

```bash
# 1. Add articles from URLs
autopaper add https://blog.example.com/article1
autopaper add https://blog.example.com/article2

# 2. List all articles
autopaper list

# 3. Generate weekly issue
autopaper generate tech    # For tech newsletter
autopaper generate news    # For news newsletter

# 4. Export to PDF
autopaper export-pdf 2026-W05-tech

# 5. Sync to Obsidian
autopaper sync obsidian 2026-W05-tech
```

### Commands Reference

#### `autopaper add <url>`
Add a new article from URL to the database.

**Options:**
- `--force, -f`: Force re-scraping even if article exists

**Example:**
```bash
autopaper add https://example.com/article --force
```

#### `autopaper list`
List all articles in the database.

**Output:**
- Article ID
- Title
- URL
- Tags
- Date added

#### `autopaper generate <type>`
Generate a weekly issue from collected articles.

**Types:**
- `tech`: Technology-focused newsletter
- `news`: General news newsletter

**Output:**
- Markdown file in `issues/` directory
- AI-generated editorial content
- Article summaries and key points

#### `autopaper export-pdf <slug>`
Export an issue to PDF format.

**Example:**
```bash
autopaper export-pdf 2026-W05-tech
```

**Output:**
- Professional PDF with cover image
- Formatted content and images
- Saved in `issues/` directory

#### `autopaper sync obsidian <slug>`
Sync an issue to Obsidian vault.

**Configuration:**
Edit `config.yaml` to set your Obsidian vault path:
```yaml
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper
```

**Example:**
```bash
autopaper sync obsidian 2026-W05-tech
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
CACHE_ENABLED=true
CACHE_TTL=86400
LOG_LEVEL=INFO
```

### Config File (config.yaml)

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
  ai: [artificial intelligence, machine learning]
```

## 🤖 AI Features

### Metadata Extraction
Uses Claude AI to extract:
- Article title
- Author information
- Summary (150-200 words)
- Key points (3-5 bullet points)
- Tags/categories

### Issue Composition
AI-generated content includes:
- Editor's note
- Trend analysis
- Article groupings
- Thematic connections

### Performance Optimization
- **Caching**: AI responses cached for 100x faster duplicate processing
- **Concurrent Downloads**: Parallel image fetching (10x speedup)
- **Smart Retry**: Automatic retry with exponential backoff

## 📊 Output Formats

### Markdown
- Clean, readable format
- Obsidian-compatible links (`[[slug]]`)
- Original image URLs

### PDF
- Professional typography
- Cover image generation
- Formatted tables and lists
- Print-ready layout

### Obsidian Sync
- Markdown with wikilinks
- Image embedding
- Tag preservation
- Folder organization

## 🎨 Customization

### Templates

Edit Jinja2 templates in `autopaper/templates/`:

- `issue.md.j2`: Markdown template
- `issue.html.j2`: PDF HTML template

### Custom Prompts

Modify AI prompts in `skills/` directory:

- `extract_article_metadata.py`: Article analysis prompt
- `compose_issue.py`: Issue composition prompt

## 📈 Performance

| Metric | Value |
|--------|-------|
| Article processing (cached) | ~0.1s |
| Article processing (uncached) | ~10s |
| Issue generation | ~30s |
| PDF export | ~20s |
| Cache hit rate | 80-90% |

## ⚠️ Limitations

1. **Article Sources**: Works best with well-structured HTML content
2. **Language**: Optimized for English and Chinese content
3. **Paywalled Content**: Cannot access paywalled articles
4. **Rate Limits**: Subject to Anthropic API rate limits
5. **Image Support**: Original URLs only (no local embedding)

## 🔒 Privacy & Security

- No data sent to third parties (except Anthropic API)
- All processing done locally
- Cache stored locally
- Database stored locally
- API keys stored in `.env` (not committed to git)

## 🛠️ Development

### Project Structure

```
AutoPaper/
├── autopaper/          # Main package
│   ├── commands/        # CLI commands
│   ├── scrapers/        # Web scraping
│   ├── publishers/      # PDF/Obsidian export
│   └── utils/          # Utilities
├── skills/             # AI integration scripts
├── tests/              # Test suite
└── docs/               # Documentation
```

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
black autopaper/
isort autopaper/
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Design Document](docs/AutoPaper-Design.md)
- [API Documentation](docs/API.md) (coming soon)

## 🔗 Links

- **GitHub**: https://github.com/OldCoderIsMe/AutoPaper
- **Issues**: https://github.com/OldCoderIsMe/AutoPaper/issues
- **Documentation**: https://github.com/OldCoderIsMe/AutoPaper#readme

## 🙏 Acknowledgments

Built with:
- [Claude](https://www.anthropic.com/claude) - AI capabilities
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [WeasyPrint](https://weasyprint.org/) - PDF generation

---

**Version**: 0.1.0
**Last Updated**: 2026-01-27
**Maintainer**: OldCoderIsMe
