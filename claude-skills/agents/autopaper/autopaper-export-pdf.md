# AutoPaper Export PDF

Export newspaper issue to professional PDF format with cover image.

## Description

This skill converts a Markdown newspaper issue into a beautifully formatted PDF document with professional typography, cover image, and print-ready layout.

## Usage

### Basic Usage

```
/autopaper-export-pdf 2026-W05-tech
```

### With Options

```
/autopaper-export-pdf 2026-W05-tech --output /path/to/output.pdf
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `<slug>` | Issue slug (e.g., `2026-W05-tech`) | - |
| `--output <path>` | Custom output path | `issues/<slug>.pdf` |
| `--no-cover` | Skip cover image generation | `false` |
| `--style <name>` | Visual style: `clean`, `elegant`, `modern` | `elegant` |

### Examples

```bash
# Export existing issue
/autopaper-export-pdf 2026-W05-tech

# Export with custom output path
/autopaper-export-pdf 2026-W05-tech --output ~/Documents/weekly.pdf

# Export without cover
/autopaper-export-pdf 2026-W05-tech --no-cover

# Export with specific style
/autopaper-export-pdf 2026-W05-tech --style modern
```

## What It Does

1. **Locates Issue File**: Finds `<slug>.md` in issues directory
2. **Parses Markdown**: Converts Markdown to HTML
3. **Generates Cover** (optional): Creates AI-generated cover image
4. **Applies Styling**: Uses CSS for professional typography
5. **Renders PDF**: Converts HTML to PDF using WeasyPrint
6. **Saves File**: Outputs PDF to specified location

## Output

The skill will display:

```
✅ PDF exported successfully!

Issue: 2026-W05-tech
Output: issues/2026-W05-tech.pdf
Size: 393 KB
Pages: 8

Cover: issues/2026-W05-tech-cover.png
```

## PDF Features

### Typography
- Professional fonts (Serif for body, Sans-serif for headings)
- Optimized line height and spacing
- Print-ready margins

### Layout
- Cover page with title and date
- Table of contents
- Article sections with clear hierarchy
- Image support (embedded)
- Footer with page numbers

### Styles

#### elegant (Default)
- Classic newspaper aesthetic
- Serif fonts (Georgia, Times)
- Traditional layouts
- Black and white with subtle accents

#### clean
- Minimalist design
- Sans-serif fonts (Helvetica, Arial)
- Modern layout
- Ample white space

#### modern
- Contemporary design
- Mix of serif and sans-serif
- Bold headings
- Color accents

## Cover Image

Auto-generated cover includes:
- Issue title
- Date/Week number
- Type indicator (tech/news)
- AI-generated illustration

Example: `2026-W05-tech-cover.png`

## File Size

Typical PDF sizes:
- **Text-only**: ~200 KB
- **With images**: ~400-600 KB
- **Large issues (10+ articles)**: ~1 MB

## Error Handling

- **Issue Not Found**: Suggests generating issue first with `/autopaper-generate`
- **Markdown Parse Error**: Shows specific line and character with error
- **PDF Generation Error**: Checks WeasyPrint installation and CSS
- **File Write Error**: Verifies directory permissions and disk space

## Dependencies

Required system packages:
- **WeasyPrint**: PDF generation engine
- **Fonts**: Professional fonts installed on system

Install on macOS:
```bash
brew install weasyprint
```

Install on Ubuntu/Debian:
```bash
sudo apt-get install python3-weasyprint
```

Install on Windows:
```bash
pip install weasyprint
```

## Performance

- **Small Issue (3-5 articles)**: ~10s
- **Medium Issue (6-10 articles)**: ~15s
- **Large Issue (10+ articles)**: ~25s

## Output Quality

- **Resolution**: 300 DPI (print quality)
- **Color**: CMYK color space for printing
- **Compatibility**: PDF/A standard for archiving
- **Size**: A4 page size (210 × 297 mm)

## Related Skills

- `/autopaper-generate` - Generate issue first
- `/autopaper-sync-obsidian` - Alternative export to Obsidian
