# AutoPaper

> AI-Powered Automated Newspaper Generation Tool 🤖📰

AutoPaper is a CLI tool that automatically generates curated weekly newspapers from article URLs. It uses Claude AI to extract metadata, compose editorial content, and export to multiple formats.

## ✨ Features

- **🤖 AI-Powered Curation** - Smart metadata extraction and issue composition using Claude
- **📰 Auto-Generated Newspapers** - Weekly tech/news issues with editor's insights
- **🏷️ Smart Tagging** - Automatic tag classification and normalization
- **📄 Multiple Export Formats** - Markdown, PDF, Obsidian vault sync, and Email delivery
- **📧 Email Distribution** - Send issues via email with AI card, PDF attachments, and HTML rendering
- **🎨 AI Card Generation** - Beautiful AI-style infographic cards for social sharing
- **⚡ High Performance** - 100x faster with AI caching and concurrent downloads
- **🛡️ Production Ready** - Robust error handling, retry logic, and comprehensive logging

## 📦 Quick Start

### Option 1: Claude Code Skills (Recommended for Claude Code Users)

If you use **Claude Code**, install AutoPaper as a skill:

```
/plugin marketplace add OldCoderIsMe/AutoPaper
```

Then use the skills:
```
/autopaper-add https://blog.example.com/article
/autopaper-generate tech
/autopaper-export-pdf 2026-W05-tech
```

📖 See [claude-skills/README.md](claude-skills/README.md) for details.

### Option 2: CLI Tool (Traditional Python Package)

#### Prerequisites

- Python 3.10+
- Anthropic API key

#### Installation

```bash
# Install
pip install -e .

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## 🚀 Quick Usage

### Complete Workflow Example

```bash
# 1. Add articles throughout the week
autopaper add https://blog.example.com/ai-tool-review
autopaper add https://news.example.com/tech-trend-2026

# 2. View all articles
autopaper list-articles

# 3. Generate weekly issue
autopaper generate tech

# 4. Export to PDF (includes AI card)
autopaper export-pdf 2026-W05-tech

# 5. Send to team via email
autopaper send-email 2026-W05-tech \
  --to team@company.com \
  --to manager@company.com \
  --to subscribers@company.com

# 6. Optionally sync to Obsidian
autopaper sync obsidian 2026-W05-tech
```

### What You Get

Each generated issue includes:

- **📄 PDF Document** - Professional layout with AI card
- **📧 Email HTML** - Rich formatted email with embedded AI card
- **📝 Markdown Source** - Plain text for version control
- **🎨 AI Card** - Shareable infographic (2400x1350px)
- **🔗 Obsidian Notes** - Integrated into your knowledge base

### Email Sending Examples

```bash
# Send to single recipient
autopaper send-email 2026-W05-tech --to user@example.com

# Send to multiple recipients
autopaper send-email 2026-W05-tech \
  --to user1@example.com \
  --to user2@example.com \
  --to user3@example.com

# Custom email subject
autopaper send-email 2026-W05-tech \
  --to user@example.com \
  --subject "本周技术精选第5期"

# Send without PDF attachment
autopaper send-email 2026-W05-tech \
  --to user@example.com \
  --no-pdf
```

### Commands

| Command | Description |
|---------|-------------|
| `autopaper add <url>` | Add article from URL |
| `autopaper list` | List all articles |
| `autopaper generate <type>` | Generate weekly issue (tech/news) |
| `autopaper export-pdf <slug>` | Export issue to PDF |
| `autopaper send-email <slug>` | Send issue via email |
| `autopaper sync obsidian <slug>` | Sync to Obsidian vault |

See `autopaper --help` for all commands and options.

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Detailed setup and usage
- **[Email Feature Guide](docs/EMAIL_FEATURE.md)** - Email sending configuration and usage
- **[Design Document](docs/AutoPaper-Design.md)** - Architecture and technical details
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

## 🏗️ Project Structure

```
AutoPaper/
├── autopaper/          # Main package
│   ├── commands/        # CLI commands
│   │   ├── add.py       # Add articles
│   │   ├── generate.py  # Generate issues
│   │   ├── export.py    # PDF export
│   │   ├── email.py     # Email sending
│   │   └── sync.py      # Obsidian sync
│   ├── publishers/      # Export publishers
│   │   ├── pdf.py       # PDF generation
│   │   ├── obsidian.py  # Obsidian sync
│   │   └── email.py     # Email publisher
│   ├── scrapers/        # Web scraping
│   ├── templates/       # Jinja2 templates
│   │   ├── issue.html.j2  # PDF template
│   │   └── email.html.j2  # Email template
│   └── utils/          # Utilities
├── skills/             # AI integration
│   ├── generate_infocard.py  # AI card generation
│   └── ...
├── tests/              # Test suite
├── docs/               # Documentation
│   ├── QUICKSTART.md
│   ├── EMAIL_FEATURE.md
│   └── AutoPaper-Design.md
└── issues/             # Generated issues
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# ============================================
# API Configuration
# ============================================

# API Key - supports both ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN
ANTHROPIC_API_KEY=your_api_key_here

# API Base URL (optional - for custom endpoints or proxy)
# Default: https://api.anthropic.com
# Example for 智谱AI (GLM-4):
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic

# Model Configuration (optional)
# ANTHROPIC_MODEL - default model for all requests
# ANTHROPIC_DEFAULT_SONNET_MODEL - for Sonnet-specific requests
# ANTHROPIC_DEFAULT_OPUS_MODEL - for Opus-specific requests
# ANTHROPIC_DEFAULT_HAIKU_MODEL - for Haiku-specific requests
#
# Example for GLM-4 (智谱AI):
ANTHROPIC_MODEL=glm-4.7
ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7
#
# Example for Claude (Anthropic):
# ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
# ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5-20250929

# ============================================
# Email Configuration (SMTP)
# ============================================

# SMTP Server Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=AutoPaper <your_email@gmail.com>

# Common SMTP Servers:
# - Gmail: smtp.gmail.com:587
# - Outlook: smtp-mail.outlook.com:587
# - QQ Mail: smtp.qq.com:587
# - 163 Mail: smtp.163.com:465

# Note: For Gmail, use App Password instead of regular password
# Get it from: Google Account > Security > 2-Step Verification > App passwords
```

### config.yaml

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
- **AI Card Generation** - Beautiful infographic cards with key highlights

### AI Card

AutoPaper automatically generates AI-style infographic cards for each issue:

- **1200x675** landscape format (16:9)
- Modern dark theme with gradient accents
- Smart summary of 4 key points
- Professional design for sharing on social media
- Embedded in both PDF and email

**Example cards:**
```bash
# Generate standalone card
autopaper generate-card 2026-W05-tech

# Card is automatically included in:
# - PDF export
# - Email HTML body (as base64 image)
```

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
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [aiosmtplib](https://github.com/cole/aiosmtplib) - Async SMTP client

## 📧 Email Delivery

AutoPaper supports sending generated issues via email with:

- **Rich HTML emails** - Rendered markdown with AI card embedded
- **PDF attachments** - High-quality PDF with AI card
- **Markdown attachments** - Source files for archiving
- **Multiple recipients** - Send to unlimited recipients at once
- **Major providers** - Gmail, Outlook, QQ Mail, 163 Mail, and more

**Quick Start:**
```bash
# 1. Configure SMTP in .env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=AutoPaper <your@gmail.com>

# 2. Send email
autopaper send-email 2026-W05-tech --to recipient@example.com
```

📖 See [docs/EMAIL_FEATURE.md](docs/EMAIL_FEATURE.md) for detailed email setup guide.

---

**Ready to automate your newsletter workflow?** 🚀

- Documentation: [docs/](docs/)
- Email Guide: [docs/EMAIL_FEATURE.md](docs/EMAIL_FEATURE.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Issues: [GitHub Issues](https://github.com/OldCoderIsMe/AutoPaper/issues)
