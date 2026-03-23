# AutoPaper [![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/OldCoderIsMe/AutoPaper)


> AI-Powered Automated Newspaper Generation Tool 🤖📰

[English](README.md) | [简体中文](README.zh-CN.md)

AutoPaper is a CLI tool that automatically generates curated weekly newspapers from article URLs. 中文用户可参阅 **[团队使用指南](TEAM_GUIDE.md)** 快速上手。 It uses Claude AI to extract metadata, compose editorial content, and export to multiple formats.

## ✨ Features

- **🤖 AI-Powered Curation** - Smart metadata extraction and issue composition using Claude
- **📰 Auto-Generated Newspapers** - Weekly tech/news issues with editor's insights
- **🏷️ Smart Tagging** - Automatic tag classification and normalization
- **📄 Multiple Export Formats** - Markdown, PDF, Obsidian vault sync, and Email delivery
- **📧 Email Distribution** - Send issues via email with AI card, PDF attachments, and HTML rendering
- **🎨 AI Card Generation** - Beautiful AI-style infographic cards for social sharing
- **🔗 Article Links Section** - Quick access to all original article URLs at the bottom
- **⚡ High Performance** - 100x faster with AI caching and concurrent downloads
- **🛡️ Production Ready** - Robust error handling, retry logic, and comprehensive logging

## 📦 Quick Start

### Option 1: CLI Tool (Traditional Python Package)

#### Prerequisites

- Python 3.10+
- Anthropic API key

#### Installation

```bash
# Clone the repository
git clone https://github.com/OldCoderIsMe/AutoPaper.git
cd AutoPaper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

#### Making `autopaper` Command Available

After installation, you have two options:

##### Option A: Add to PATH (Recommended for frequent use)

Add this to your `~/.zshrc` (or `~/.bashrc`):

```bash
# AutoPaper venv
export PATH="$PATH:/path/to/AutoPaper/venv/bin"
```

Then reload: `source ~/.zshrc`

##### Option B: Always use with venv activated

```bash
cd /path/to/AutoPaper
source venv/bin/activate
autopaper --help
```

## 🚀 Quick Usage

### Complete Workflow Example

```bash
# 1. Add articles throughout the week
autopaper add https://blog.example.com/ai-tool-review
autopaper add https://news.example.com/tech-trend-2026

# 2. View all articles
autopaper list-articles

# 3. Delete an article by ID
autopaper delete 5

# 4. Generate weekly issue
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

- **📄 PDF Document** - Professional layout with AI card and article links
- **📧 Email HTML** - Rich formatted email with embedded AI card and clickable links
- **📝 Markdown Source** - Plain text for version control with article links
- **🎨 AI Card** - Shareable infographic (2400x1350px)
- **🔗 Article Links** - All original article URLs at the bottom for quick access
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
| `autopaper list-articles` | List all articles |
| `autopaper delete <id>` | Delete article by ID |
| `autopaper generate <type>` | Generate weekly issue (tech/news) |
| `autopaper export-pdf <slug>` | Export issue to PDF (also saves HTML) |
| `autopaper export-pdf <slug> --html` | Generate HTML only, skip PDF (debug) |
| `autopaper send-email <slug>` | Send issue via email |
| `autopaper generate-card <slug>` | Generate AI summary card |
| `autopaper sync obsidian <slug>` | Sync to Obsidian vault |

See `autopaper --help` for all commands and options.

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Detailed setup and usage
- **[Team Guide (团队使用指南)](TEAM_GUIDE.md)** - 中文快速安装与使用
- **[Email Feature Guide](docs/EMAIL_FEATURE.md)** - Email sending configuration and usage
- **[Design Document](docs/AutoPaper-Design.md)** - Architecture and technical details
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

## 🏗️ Project Structure

```
AutoPaper/
├── autopaper/          # Main package
│   ├── ai/             # AI integration modules
│   │   ├── compose_issue.py        # Issue composition
│   │   ├── extract_article_metadata.py  # Metadata extraction
│   │   ├── generate_infocard.py    # AI card generation
│   │   └── normalize_tags.py       # Tag normalization
│   ├── commands/       # CLI commands
│   │   ├── add.py       # Add articles
│   │   ├── generate.py  # Generate issues
│   │   ├── export.py    # PDF export
│   │   ├── email.py     # Email sending
│   │   └── sync.py      # Obsidian sync
│   ├── publishers/     # Export publishers
│   │   ├── pdf.py       # PDF generation
│   │   ├── obsidian.py  # Obsidian sync
│   │   └── email.py     # Email publisher
│   ├── scrapers/       # Web scraping
│   ├── templates/      # Jinja2 templates
│   │   ├── issue.html.j2  # PDF template
│   │   └── email.html.j2  # Email template
│   └── utils/          # Utilities
├── tests/              # Test suite
├── docs/               # Documentation
│   ├── QUICKSTART.md
│   ├── EMAIL_FEATURE.md
│   └── AutoPaper-Design.md
├── claude-skills/      # Standalone Claude Code Skills
│   ├── shared/         # Shared config, cache, retry, JSON parser
│   ├── generate-card/  # AI info card generator
│   │   ├── SKILL.md
│   │   ├── main.py     # Launcher
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   └── extract-metadata/ # Article metadata extractor
│       ├── SKILL.md
│       ├── main.py
│       ├── scripts/
│       ├── references/
│       └── assets/
├── TEAM_GUIDE.md       # 团队使用指南（中文）
└── issues/             # Generated issues
```

## 🧩 Standalone Claude Code Skills

AutoPaper's core AI capabilities are also available as **standalone Claude Code Skills** that can be used independently. Each skill follows the official layout: `SKILL.md`, `scripts/`, `references/`, `assets/`.

### Available Skills

1. **📝 Article Metadata Extractor** (`extract-metadata/`)
   - Extract structured metadata from article URLs or content
   - Auto-generate summaries, tags, and key points
   - Classify articles (technical vs news)

2. **🎨 AI Info Card Generator** (`generate-card/`)
   - Generate beautiful SVG infographic cards (1200x675)
   - Modern AI tech style with Chinese font support
   - Perfect for blog covers, social media, presentations

### Quick Start

Run from the **skill root** (no `PYTHONPATH` needed):

```bash
cd claude-skills

# Extract article metadata
python extract-metadata/main.py https://blog.example.com/article

# Generate info card
python generate-card/main.py "本周技术精选" --content article.md
```

Each skill's `main.py` is a launcher that runs `scripts/main.py`. See [generate-card/SKILL.md](claude-skills/generate-card/SKILL.md) and [extract-metadata/SKILL.md](claude-skills/extract-metadata/SKILL.md) for full usage and options.

## 🔧 Configuration

AutoPaper supports two modes with **identical configuration features**:

- **CLI Mode**: Use `autopaper` command directly
- **Skill Mode**: Use via Claude Code (`/autopaper-*` commands)

Both modes support full configuration through `config.yaml` and `.env` files.

### Configuration Discovery

**CLI Mode**: Loads configuration from the current working directory.

**Skill Mode**: Automatically discovers project configuration by:
1. Searching upward for `config.yaml` from the current directory
2. Using `AUTOPAPER_CONFIG_PATH` environment variable (if set)
3. Falling back to sensible defaults

This means skills work from any directory while respecting your project configuration.

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

#### Example cards

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
- [LibreOffice](https://www.libreoffice.org/) - PDF generation (replaces WeasyPrint for better CJK support)
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [aiosmtplib](https://github.com/cole/aiosmtplib) - Async SMTP client

## 📧 Email Delivery

AutoPaper supports sending generated issues via email with:

- **Rich HTML emails** - Rendered markdown with AI card embedded
- **PDF attachments** - High-quality PDF with AI card
- **Markdown attachments** - Source files for archiving
- **Article links section** - Quick access to all original article URLs
- **Multiple recipients** - Send to unlimited recipients at once
- **Major providers** - Gmail, Outlook, QQ Mail, 163 Mail, and more

### Quick Start

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
