# AutoPaper Skills Extension

This file allows you to customize AutoPaper skills behavior without modifying the core code.

## How It Works

Create `EXTEND.md` files in:
- **Project-level**: `.autopaper-skills/<skill-name>/EXTEND.md`
- **User-level**: `~/.autopaper-skills/<skill-name>/EXTEND.md`

User-level extensions override project-level ones.

## Extension Sections

### 1. Editorial Guidelines (for autopaper-generate)

```markdown
## Editorial Style

### Tone
- Professional yet accessible
- Data-driven insights
- Actionable recommendations

### Structure
- Start with key statistics
- Group by themes
- End with forward-looking statements
```

### 2. Article Analysis (for autopaper-add)

```markdown
## Metadata Extraction

### Title Preferences
- Prefer descriptive titles over catchy ones
- Remove platform prefixes (e.g., "LinkedIn: ")
- Keep technical terms in English

### Summary Length
- Target 150-200 words
- 3-5 paragraphs
- Include key statistics

### Key Points
- Maximum 5 bullet points
- Start with action verbs
- Include specific examples
```

### 3. PDF Styling (for autopaper-export-pdf)

```markdown
## PDF Styles

### Custom Fonts
- Headings: Inter Bold
- Body: Georgia Regular
- Code: JetBrains Mono

### Colors
- Primary: #1a73e8
- Secondary: #34a853
- Accent: #fbbc04

### Layout
- Margin: 2cm
- Line height: 1.6
- Paragraph spacing: 12pt
```

### 4. Obsidian Sync (for autopaper-sync-obsidian)

```markdown
## Obsidian Integration

### Tag Strategy
- Add weekly tags: `#2026-W05`
- Add topic tags from content
- Always include `#newsletter`

### Folder Structure
- By year: `AutoPaper/2026/`
- By type: `AutoPaper/Tech/` and `AutoPaper/News/`
- Flat: All in `AutoPaper/`

### Wikilink Format
- Use descriptive anchors: `[[article-slug|Article Title]]`
- Add metadata blocks
- Include callout boxes
```

## Example Extensions

### Example 1: Chinese-First Editorial Style

```markdown
## Editorial Guidelines

### Language
- Primary: 中文 (Simplified Chinese)
- Technical terms: Keep in English with explanation
- Quotes: Preserve original language

### Tone
- 专业但不失亲和力
- 用数据说话
- 提供实用建议

### Structure
- 本周亮点 (Highlights)
- 深度阅读 (Deep Dive)
- 实战指南 (Practical Guide)
- 下周预告 (Preview)
```

### Example 2: Developer-Focused Content

```markdown
## Content Curation

### Article Selection
- Prioritize tutorials with code examples
- Include architecture diagrams
- Focus on production best practices
- Add difficulty levels

### Summary Format
- Start with "TL;DR"
- Key technologies mentioned
- Code language/framework
- Link to documentation

### Key Points
- Code snippets with syntax
- Performance considerations
- Common pitfalls
- Alternative approaches
```

### Example 3: Minimalist PDF Style

```markdown
## PDF Design

### Typography
- Font: Helvetica (all)
- Minimal hierarchy
- Black and white only

### Layout
- Single column
- No sidebars
- Minimal decorations
- Clear sections

### Images
- Original URLs only (no embedding)
- Caption below image
- Max width: 100%
```

## Testing Extensions

After creating an `EXTEND.md` file:

1. **Verify syntax**: Ensure valid Markdown
2. **Test skill**: Run the skill to check if extensions are applied
3. **Iterate**: Adjust based on output
4. **Share**: Commit project-level extensions for team use

## Troubleshooting

### Extensions Not Loading

Check:
1. File path is correct
2. Filename is exactly `EXTEND.md` (uppercase)
3. Markdown syntax is valid
4. Section headers match expected format

### Conflicting Extensions

If both project and user-level extensions exist:
- User-level takes priority
- Merge sections manually if needed
- Use `<!-- Original: -->` comments to track

## Getting Help

- See main [README](../README.md)
- Check [Design Document](../docs/AutoPaper-Design.md)
- Open [GitHub Issue](https://github.com/OldCoderIsMe/AutoPaper/issues)

---

**Note**: This is a template file. Copy it to your skill directory and customize as needed.
