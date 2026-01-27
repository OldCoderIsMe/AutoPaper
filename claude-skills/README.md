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

### Environment Variables

Create `.env` file in your project root:

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
CACHE_ENABLED=true
CACHE_TTL=86400
LOG_LEVEL=INFO
```

### Obsidian Configuration

Edit `config.yaml`:

```yaml
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper
```

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
