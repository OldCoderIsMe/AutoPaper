# AutoPaper Skills - Quick Start

AI-powered content tools for Claude Code - extract article metadata and generate info cards.

## 🚀 Quick Start

### 1. Configuration

```bash
# Set API Key (required)
export ANTHROPIC_API_KEY=your_api_key_here

# Optional: Custom endpoint (e.g., 智谱AI)
export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
```

### 2. Usage

#### In Claude Code (Recommended)

```
帮我提取 https://example.com 的文章元数据
```

```
为 article.md 生成一张技术风格的卡片
```

#### As CLI Tools

```bash
cd /Users/smzdm/work/claude/AutoPaper/claude-skills

# Extract metadata
PYTHONPATH=. python3 extract-metadata/main.py https://blog.example.com/article

# Generate card
PYTHONPATH=. python3 generate-card/main.py "本周技术精选" --content article.md
```

#### Add Aliases (Optional)

Add to `~/.zshrc`:
```bash
alias extract-metadata='cd /Users/smzdm/work/claude/AutoPaper/claude-skills && PYTHONPATH=. python3 extract-metadata/main.py'
alias generate-card='cd /Users/smzdm/work/claude/AutoPaper/claude-skills && PYTHONPATH=. python3 generate-card/main.py'
```

Then use from anywhere:
```bash
extract-metadata https://example.com
generate-card "标题" --content article.md
```

## 📦 Skills

### 1. Extract Metadata

Extract structured metadata from articles:
- Title, author, source, date
- Summary (2-3 sentences)
- Tags and classification
- Key points (3-7 items)

**Usage:**
```bash
python main.py https://example.com
python main.py https://example.com --output markdown
```

### 2. Generate Card

Generate AI-style infographic cards (1200x675 SVG):
- Modern tech aesthetic
- Dark theme
- Chinese font optimized
- tech/news styles

**Usage:**
```bash
python main.py "本周技术精选" --content article.md
python main.py "标题" --style news --output card.svg
```

## 📁 Structure

```
claude-skills/
├── extract-metadata/    # Skill 1
│   ├── main.py
│   └── requirements.txt
├── generate-card/       # Skill 2
│   ├── main.py
│   └── requirements.txt
├── shared/              # Shared utilities
├── plugins/             # Claude Code plugins
└── QUICKSTART.md        # This file
```

## 🔧 Plugin Management

```bash
# List plugins
claude plugin list

# Enable/disable
claude plugin enable extract-metadata@autopaper-skills
claude plugin disable generate-card@autopaper-skills

# Update
claude plugin marketplace update autopaper-skills
```

## 📖 Examples

```bash
# Extract metadata
extract-metadata https://blog.example.com/article

# Generate tech card
generate-card "AI编程工具演进" --style tech

# From file
generate-card "标题" --content examples/sample-article.md
```

## 🐛 Troubleshooting

**Plugin not visible?**
```bash
claude plugin marketplace update autopaper-skills
```

**API error?**
```bash
echo $ANTHROPIC_API_KEY
```

**Import error?**
```bash
PYTHONPATH=. python3 extract-metadata/main.py --help
```

## 📚 More

- [AutoPaper Project](../README.md) - Full newsletter tool
- [GitHub](https://github.com/OldCoderIsMe/AutoPaper) - Source code

---

**Ready?** Set your API key and start using! 🚀
