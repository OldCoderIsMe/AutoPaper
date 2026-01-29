# AutoPaper Quick Start Guide

## Installation

1. **Clone and install dependencies:**
```bash
cd AutoPaper
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your API configuration
```

Example `.env` configuration:

```bash
# For Anthropic Claude (default):
ANTHROPIC_API_KEY=sk-ant-xxxxx
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929

# For 智谱AI (GLM-4):
# ANTHROPIC_API_KEY=your_glm_api_key
# ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
# ANTHROPIC_MODEL=glm-4.7
# ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7
```

## Basic Usage

### 1. Add an Article

```bash
autopaper add https://example.com/article
```

This will:
- Fetch and extract the article content
- Use Claude AI to extract metadata (title, author, summary, tags)
- Save to database and `articles/enriched/` directory

### 2. List Articles

```bash
# List all articles
autopaper list-articles

# Filter by tag
autopaper list-articles --tag=ai

# Filter by type
autopaper list-articles --type=technical

# Limit results
autopaper list-articles --limit=5
```

### 3. Generate an Issue

```bash
# Generate technical issue for current week
autopaper generate tech

# Generate news issue for last week
autopaper generate news --last-week

# Generate with filters
autopaper generate tech --tag=kubernetes --limit=10

# Generate and sync to Obsidian
autopaper generate tech --sync-obsidian
```

This creates:
- Markdown file in `issues/` directory
- Database record
- Optional: Obsidian vault files

### 4. Export to PDF

```bash
autopaper export-pdf 2026-W04-tech
```

### 5. Sync to Obsidian

```bash
autopaper sync obsidian 2026-W04-tech
```

This creates:
- Article files in `{vault}/AutoPaper/Articles/`
- Issue file in `{vault}/AutoPaper/Issues/`
- Wiki-link references between files

## Configuration

Edit `config.yaml` to customize:

```yaml
# Obsidian vault path
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper

# Database location
database_path: data/db.sqlite

# Directories
articles:
  raw_dir: articles/raw
  parsed_dir: articles/parsed
  enriched_dir: articles/enriched

issues_dir: issues
```

## Complete Workflow Example

```bash
# 1. Add articles throughout the week
autopaper add https://blog.example.com/deep-dive-1
autopaper add https://news.example.com/update-1
autopaper add https://example.com/tutorial

# 2. Review collected articles
autopaper list-articles --type=technical

# 3. Generate weekly issue
autopaper generate tech --last-week

# 4. Preview the generated issue
cat issues/2026-W04-tech.md

# 5. Export to PDF
autopaper export-pdf 2026-W04-tech

# 6. Sync to Obsidian
autopaper sync obsidian 2026-W04-tech
```

## Testing

Run tests to verify installation:

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
Add your API key to `.env` file:
```bash
# Option 1: Use ANTHROPIC_API_KEY
ANTHROPIC_API_KEY=your_key_here

# Option 2: Use ANTHROPIC_AUTH_TOKEN (alternative)
ANTHROPIC_AUTH_TOKEN=your_token_here
```

### API request failed
If using a custom API endpoint or proxy, configure `ANTHROPIC_BASE_URL`:
```bash
# For example, using 智谱AI:
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-4.7
```

### "Module not found" error
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
pip install -e .
```

### Obsidian sync fails
Check `vault_path` in `config.yaml`:
```bash
# Expand ~ to full path
obsidian:
  vault_path: /Users/yourname/Documents/ObsidianVault
```

## Tips

1. **Batch add articles**: Add URLs throughout the week, then generate issue at week end
2. **Use tags**: Filter articles by tag when generating focused issues
3. **Custom slugs**: Use `--slug` flag to customize issue identifiers
4. **Preview first**: Always preview generated Markdown before exporting to PDF
5. **Version control**: Consider adding `issues/*.md` to Git for tracking

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Explore `skills/` directory to understand AI features
- Customize templates in `autopaper/templates/`
- Adjust tag normalization rules in `config.yaml`
