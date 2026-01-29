# AutoPaper Skills

AI-powered automated newspaper generation skills for Claude Code.

## 🚀 Quick Start

### Installation

#### Method 1: Via Marketplace (Recommended)

Run in Claude Code:

```
/plugin marketplace add OldCoderIsMe/AutoPaper
```

Then browse and install skills:
```
/plugin
```

#### Method 2: Direct Install

```
/plugin install autopaper-add@autopaper-skills
/plugin install autopaper-generate@autopaper-skills
/plugin install autopaper-export-pdf@autopaper-skills
/plugin install autopaper-sync-obsidian@autopaper-skills
```

#### Method 3: Ask Claude Code

Just tell Claude Code:
> Please install AutoPaper skills from github.com/OldCoderIsMe/AutoPaper

## 📋 Available Skills

| Skill | Description | Command |
|-------|-------------|---------|
| **AutoPaper Add** | Add article from URL with AI metadata extraction | `/autopaper-add` |
| **AutoPaper Generate** | Generate weekly issue with AI editorial | `/autopaper-generate` |
| **AutoPaper Export PDF** | Export issue to professional PDF | `/autopaper-export-pdf` |
| **AutoPaper Sync Obsidian** | Sync issue to Obsidian vault | `/autopaper-sync-obsidian` |

## 🎯 Usage Workflow

### Complete Workflow

```bash
# 1. Add articles
/autopaper-add https://blog.example.com/article1
/autopaper-add https://blog.example.com/article2

# 2. Generate weekly issue
/autopaper-generate tech

# 3. Export to PDF (optional)
/autopaper-export-pdf 2026-W05-tech

# 4. Sync to Obsidian (optional)
/autopaper-sync-obsidian 2026-W05-tech
```

### Quick Examples

```bash
# Add article with force re-scraping
/autopaper-add https://example.com/article --force

# Generate custom week
/autopaper-generate tech --week 2026-W04 --title "AI Weekly"

# Export with custom output
/autopaper-export-pdf 2026-W05-tech --output ~/Documents/weekly.pdf

# Sync to custom vault
/autopaper-sync-obsidian 2026-W05-tech --vault ~/Documents/ObsidianVault
```

## ⚙️ Configuration

### Overview

AutoPaper skills support **complete configuration system** just like CLI mode:

- ✅ `.env` file support
- ✅ `config.yaml` file support
- ✅ Automatic project root discovery
- ✅ Environment variable overrides
- ✅ All configuration options available

### Configuration Discovery

Skills automatically load configuration from:

1. **Project Root** (auto-discovered)
   - Searches upward from current directory for `config.yaml`
   - Stops at project root when found
   - Fallback to current directory if not found

2. **Custom Path** (optional override)
   ```bash
   export AUTOPAPER_CONFIG_PATH=/path/to/custom-config.yaml
   /autopaper-add https://example.com/article
   ```

This means you can run skills from **any directory** and they will automatically find and use your project configuration.

### Environment Variables (.env)

Create `.env` file in your project root:

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
```

### Configuration File (config.yaml)

Edit `config.yaml` in your project root:

```yaml
# Database
database_path: data/db.sqlite

# Article storage
articles:
  raw_dir: articles/raw
  parsed_dir: articles/parsed
  enriched_dir: articles/enriched
  images_dir: articles/images

# Issues storage
issues_dir: issues

# Obsidian sync
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper

# Tag normalization rules
tag_normalization:
  llm: [llm, large language model, gpt]
  kubernetes: [k8s]
  ai: [ai, artificial intelligence, 人工智能]

# API settings
api:
  model: claude-sonnet-4-5-20250929
  max_tokens: 4096

# PDF export settings
pdf:
  page_size: A4
  margin_top: 20mm
  margin_bottom: 20mm
  margin_left: 15mm
  margin_right: 15mm
```

### Priority Order

Configuration is loaded in this priority order (highest to lowest):

1. **Environment Variables** - Direct overrides (e.g., `ANTHROPIC_API_KEY`)
2. **config.yaml** - Project configuration file
3. **Defaults** - Built-in sensible defaults

### Example: Multiple Projects

You can maintain different configurations for different projects:

```
~/projects/tech-weekly/
  ├── config.yaml      # Custom config for tech weekly
  ├── .env             # Project-specific API keys
  └── articles/

~/projects/news-digest/
  ├── config.yaml      # Different config for news digest
  ├── .env             # Different API keys
  └── articles/
```

Skills will automatically use the correct configuration based on your current working directory.

## 🎨 Customization

All skills support customization via `EXTEND.md` files.

### Extension Paths (priority order)

1. `.autopaper-skills/<skill-name>/EXTEND.md` - Project-level
2. `~/.autopaper-skills/<skill-name>/EXTEND.md` - User-level

### Example: Custom Editorial Style

Create `.autopaper-skills/autopaper-generate/EXTEND.md`:

```markdown
## Custom Editorial Style

### Tone
- Professional but conversational
- Use "我们" (we) instead of passive voice
- Include actionable insights

### Structure
- Always start with "本周亮点" (Weekly Highlights)
- End with "下周预告" (Next Week Preview)

### Themes
- Focus on practical applications
- Highlight code examples and tutorials
- Call out beginner-friendly content
```

## 📚 Documentation

- **[Main README](../README.md)** - Project overview
- **[Quick Start](../docs/QUICKSTART.md)** - Detailed setup guide
- **[Design Document](../docs/AutoPaper-Design.md)** - Architecture details
- **[CLI Usage](../README.md#quick-usage)** - Command-line interface

## 🔧 Installation (Full CLI Tools)

Want to use AutoPaper as a CLI tool outside Claude Code?

```bash
# Install
pip install -e .

# Use CLI
autopaper add https://example.com/article
autopaper list
autopaper generate tech
autopaper export-pdf 2026-W05-tech
autopaper sync obsidian 2026-W05-tech
```

See [main README](../README.md) for details.

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](../CONTRIBUTING.md).

## 📝 License

MIT License - see [LICENSE](../LICENSE) file for details.

## 🔗 Links

- **GitHub**: https://github.com/OldCoderIsMe/AutoPaper
- **Issues**: https://github.com/OldCoderIsMe/AutoPaper/issues
- **Documentation**: https://github.com/OldCoderIsMe/AutoPaper#readme

---

**Version**: 0.1.0
**Last Updated**: 2026-01-27
**Maintainer**: OldCoderIsMe
