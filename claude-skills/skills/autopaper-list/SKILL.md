---
name: autopaper-list
description: "List all articles in AutoPaper database with filtering and sorting options"
license: MIT
---

# AutoPaper List Articles

List all articles in the AutoPaper database with optional filtering and detailed view.

## Description

This skill displays all articles stored in the AutoPaper database, showing key metadata including title, source, type, tags, publication date, and when the article was added. Supports filtering by tag, type, and limiting the number of results.

## Usage

### Basic Usage

```
/autopaper-list
```

### With Options

```
/autopaper-list --tag ai --limit 5 --verbose
```

### Filter by Tag

```
/autopaper-list --tag langchain
```

### Filter by Type

```
/autopaper-list --type technical
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--tag`, `-t` | Filter articles by tag | `None` (show all) |
| `--type` | Filter by article type (`technical` or `news`) | `None` (show all) |
| `--limit`, `-l` | Maximum number of articles to display | `None` (show all) |
| `--verbose`, `-v` | Show detailed information including URLs and full source names | `false` |

## Examples

```bash
# List all articles (basic view)
/autopaper-list

# Show verbose output with URLs
/autopaper-list --verbose

# Filter by tag
/autopaper-list --tag ai

# Filter by type
/autopaper-list --type news

# Show last 5 articles
/autopaper-list --limit 5

# Combine filters
/autopaper-list --tag langchain --type technical --limit 10 --verbose
```

## Output Format

### Normal Mode (default)

```
Articles
┏━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ ID ┃ Title              ┃ Source ┃ Type ┃ Tags     ┃ Pub    ┃ Added   ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ 17 │ 2026: This is AGI  │ Sequo… │ news │ AGI, AI  │ 2025-… │ 2026-0… │
│ 16 │ LangChain创始人…   │ WeChat │ news │ langch…  │ 2025-… │ 2026-0… │
└────┴────────────────────┴────────┴──────┴──────────┴────────┴─────────┘

Total: 17 article(s)
Use --verbose/-v to see URLs and more details
```

### Verbose Mode

```
Articles
┏━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ ID  ┃ Title       ┃ Source ┃ URL                  ┃ Pub     ┃ Added    ┃
┡━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 17  │ 2026: This… │ Sequo… │ https://sequoiacap.c… │ 2025-… │ 2026-01… │
│ 16  │ LangChain…  │ WeChat │ https://mp.weixin.q… │ 2025-… │ 2026-01… │
└─────┴─────────────┴────────┴──────────────────────┴────────┴──────────┘

Total: 17 article(s)
```

## Output Columns

- **ID**: Unique article identifier in the database
- **Title**: Article title (truncated in table view)
- **Source**: Article source (e.g., WeChat, GitHub, Sequoia Capital)
- **Type**: Article type (`technical` or `news`)
- **Tags**: Comma-separated tags (shows first 2, then "+N" for more)
- **Pub**: Publication date
- **Added**: When the article was added to the database (YYYY-MM-DD HH:MM)

## Use Cases

### Before Generating an Issue

Check what articles are available before generating a newspaper issue:

```
/autopaper-list
```

### Finding Articles on a Specific Topic

Find all AI-related articles:

```
/autopaper-list --tag ai
```

### Reviewing Recent Additions

See the last 10 articles added:

```
/autopaper-list --limit 10 --verbose
```

### Checking Technical vs News Articles

Filter by article type:

```
# Show only technical articles
/autopaper-list --type technical

# Show only news articles
/autopaper-list --type news
```

## Performance

- **Small database (< 50 articles)**: < 0.1s
- **Medium database (50-200 articles)**: < 0.5s
- **Large database (200+ articles)**: < 1s

## Related Commands

- `/autopaper-add` - Add a new article to the database
- `/autopaper-generate` - Generate a newspaper issue from articles
- `autopaper list-articles` - Direct CLI command equivalent

## Tips

1. **Use verbose mode** when you need to see full URLs or share article links
2. **Filter by tags** to find specific topics quickly
3. **Combine filters** for precise results (e.g., `--tag ai --type news --limit 5`)
4. **Check before generating** to ensure you have the right articles before running `/autopaper-generate`

## Article Types

- **technical**: In-depth technical articles, tutorials, research papers
- **news**: Industry news, announcements, blog posts
