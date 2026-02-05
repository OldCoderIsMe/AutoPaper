# Extract Metadata Skill

Extract structured metadata from article URLs or content using Claude AI.

## Usage

```bash
# Extract from URL
extract-metadata <url>

# Extract from content
extract-metadata <url> --content "$(cat article.md)"

# Output as markdown
extract-metadata <url> --output markdown
```

## Configuration

Set `ANTHROPIC_API_KEY` environment variable.

## What It Does

- Extracts: title, author, source, publish date
- Generates: 2-3 sentence summary
- Identifies: 3-7 key points
- Classifies: technical vs news
- Tags: automatic keyword classification
- Caches: results for 7 days

## Output

JSON with all metadata, or formatted markdown.
