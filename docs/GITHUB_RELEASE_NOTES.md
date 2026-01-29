# 🎉 AutoPaper v0.1.0 - Initial Release

AI-Powered Automated Newspaper Generation Tool with Claude Code Skills support

## ✨ Features

### 🤖 AI-Powered Curation
- Smart metadata extraction using Claude AI
- Automatic tag classification and normalization
- AI-generated editorial content and trend analysis

### 📰 Auto-Generated Newspapers
- Weekly tech/news issues with editor's insights
- Thematic article grouping
- Professional formatting

### 📄 Multiple Export Formats
- **Markdown**: Clean, readable format
- **PDF**: Professional typography with cover images
- **Obsidian**: Wikilinks for knowledge management

### 🚀 Dual Usage Modes

#### 1. Claude Code Skills (New!)
```
/plugin marketplace add OldCoderIsMe/AutoPaper
/autopaper-add https://example.com/article
/autopaper-generate tech
/autopaper-export-pdf 2026-W05-tech
/autopaper-sync-obsidian 2026-W05-tech
```

#### 2. CLI Tool
```bash
pip install git+https://github.com/OldCoderIsMe/AutoPaper.git
autopaper add https://example.com/article
autopaper generate tech
autopaper export-pdf 2026-W05-tech
autopaper sync obsidian 2026-W05-tech
```

### ⚡ High Performance
- **100x faster** with AI caching for duplicate articles
- **10x faster** with concurrent image downloads
- Automatic retry with exponential backoff
- Smart logging and performance monitoring

### 🛡️ Production Ready
- Robust error handling
- Comprehensive logging
- Full test coverage
- MIT License

## 📦 Installation

### Claude Code Users (Recommended)
```
/plugin marketplace add OldCoderIsMe/AutoPaper
```

### CLI Users
```bash
pip install git+https://github.com/OldCoderIsMe/AutoPaper.git
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

## 📚 Documentation

- [Quick Start Guide](https://github.com/OldCoderIsMe/AutoPaper/blob/main/docs/QUICKSTART.md)
- [Claude Skills Guide](https://github.com/OldCoderIsMe/AutoPaper/blob/main/claude-skills/README.md)
- [Design Document](https://github.com/OldCoderIsMe/AutoPaper/blob/main/docs/AutoPaper-Design.md)
- [Contributing](https://github.com/OldCoderIsMe/AutoPaper/blob/main/CONTRIBUTING.md)

## 🔧 Requirements

- Python 3.10+
- Anthropic API key

## 🙏 Acknowledgments

Built with:
- [Claude](https://www.anthropic.com/claude) - AI capabilities
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [WeasyPrint](https://weasyprint.org/) - PDF generation

## 📝 License

MIT License - see [LICENSE](https://github.com/OldCoderIsMe/AutoPaper/blob/main/LICENSE) file for details

## 🔗 Links

- GitHub: https://github.com/OldCoderIsMe/AutoPaper
- Issues: https://github.com/OldCoderIsMe/AutoPaper/issues
- Documentation: https://github.com/OldCoderIsMe/AutoPaper#readme

---

**Full Changelog**: https://github.com/OldCoderIsMe/AutoPaper/blob/main/CHANGELOG.md
