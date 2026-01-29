---
name: autopaper-add
description: "Add article from URL to AutoPaper database with AI-powered metadata extraction and content analysis"
license: MIT
---

# AutoPaper Add Article

Add article from URL to AutoPaper database with AI-powered metadata extraction.

## Description

This skill extracts article content from URL, uses Claude AI to analyze and extract metadata (title, author, summary, key points, tags), and stores it in the database for later use in generating newspaper issues.

## Usage

### Basic Usage

```
/autopaper-add https://example.com/article
```

### With Options

```
/autopaper-add https://example.com/article --force
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--force`, `-f` | Force re-scraping even if article exists | `false` |
| `--no-cache` | Skip AI response cache | `false` |

### Examples

```bash
# Add new article
/autopaper-add https://blog.example.com/tech-trends-2024

# Force re-scraping existing article
/autopaper-add https://blog.example.com/tech-trends-2024 --force

# Add without using cache
/autopaper-add https://blog.example.com/ai-breakthrough --no-cache
```

## What It Does

1. **Fetches Article Content**: Downloads HTML from the URL
2. **Extracts Main Content**: Uses readability-lxml to extract article body
3. **AI-Powered Analysis**: Calls Claude AI to extract:
   - Title (optimized, not just HTML title)
   - Author information
   - Summary (150-200 words)
   - Key points (3-5 bullet points)
   - Tags/categories
4. **Detects Cover Image**: Finds the main cover image
5. **Stores in Database**: Saves all metadata to SQLite database

## Output

The skill will display:

```
✅ Article added successfully!

Title: AI Trends in 2024
Author: John Doe
URL: https://blog.example.com/tech-trends-2024

Summary:
A comprehensive analysis of artificial intelligence trends
shaping the technology landscape in 2024...

Key Points:
• Generative AI adoption accelerates
• Multimodal models become mainstream
• AI regulation and ethics take center stage

Tags: ai, technology, trends, 2024

Article ID: 123
Slug: ai-trends-2024
```

## Error Handling

- **Invalid URL**: Will show error and suggest checking URL format
- **Paywalled Content**: Will extract available content only
- **Network Error**: Automatic retry with exponential backoff
- **AI API Error**: Will show error details and suggest checking API key

## Performance

- **Cached Article**: ~0.1s (if previously processed)
- **New Article**: ~10s (AI processing time)
- **Cache Hit Rate**: 80-90% for duplicate URLs

## Environment Variables

Required:
- `ANTHROPIC_API_KEY`: Your Anthropic API key

Optional:
- `CACHE_ENABLED`: Enable/disable AI cache (default: `true`)
- `CACHE_TTL`: Cache time-to-live in seconds (default: `86400`)

## Related Skills

- `/autopaper-generate` - Generate newspaper issue from articles
- `/autopaper-list` - List all articles in database
