# Example: Content Curation Workflow

This example demonstrates a typical workflow using both Skills together.

## Scenario

You're building a technical newsletter and need to:
1. Extract metadata from multiple articles
2. Generate a shareable card for social media

## Workflow

```bash
# Step 1: Extract metadata from articles
echo "Extracting metadata..."
metadata1=$(python extract-metadata/main.py \
  "https://blog.example.com/ai-tool-review")

metadata2=$(python extract-metadata/main.py \
  "https://news.example.com/tech-trend-2026")

# Step 2: Generate a summary card
echo "Generating card..."

# Option A: Use metadata to create title
title=$(echo "$metadata1" | jq -r '.title')
python generate-card/main.py "$title" \
  --content article.md \
  --style tech \
  --output weekly-card.svg

# Option B: Custom weekly summary
python generate-card/main.py "本周技术精选 · 2026-W05" \
  --key-points "AI编程工具演进,Agent架构新趋势,云原生技术深化" \
  --style tech
```

## Output

You'll get:
- Structured metadata (JSON/Markdown)
- Beautiful SVG card for sharing
- Ready to publish content

## Integration with AutoPaper

```bash
# Full AutoPaper workflow
autopaper add https://example.com/article
autopaper generate tech
autopaper export-pdf 2026-W05-tech

# Or use skills standalone
python claude-skills/extract-metadata/main.py https://example.com
python claude-skills/generate-card/main.py "Title" --content article.md
```
