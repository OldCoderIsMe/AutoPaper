# Generate Card Skill

Generate AI-style infographic cards for technical content.

## Usage

```bash
# Generate from content
generate-card "Title" --content article.md

# Specify style
generate-card "Title" --style tech --output card.svg

# Custom key points
generate-card "Title" --key-points "Point 1,Point 2"
```

## Configuration

Set `ANTHROPIC_API_KEY` environment variable.

## What It Does

- Generates: 1200x675 SVG card (16:9 landscape)
- Style: Modern AI tech aesthetic
- Theme: Dark background with gradient accents
- Fonts: Optimized Chinese support
- Formats: tech (blue) or news (green)

## Output

SVG file ready for use in blogs, social media, presentations.
