---
name: autopaper-sync-obsidian
description: "Sync newspaper issue to Obsidian vault with wikilinks, tags, and knowledge management integration"
license: MIT
---

# AutoPaper Sync Obsidian

Sync newspaper issue to Obsidian vault with wikilinks for knowledge management.

## Description

This skill synchronizes Markdown newspaper issues to your Obsidian vault, converting article references to wikilinks for easy cross-referencing and knowledge graph building.

## Usage

### Basic Usage

```
/autopaper-sync-obsidian 2026-W05-tech
```

### With Options

```
/autopaper-sync-obsidian 2026-W05-tech --vault ~/Documents/ObsidianVault
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `<slug>` | Issue slug (e.g., `2026-W05-tech`) | - |
| `--vault <path>` | Custom Obsidian vault path | From config.yaml |
| `--folder <name>` | Target folder in vault | `AutoPaper` |
| `--no-images` | Don't embed images (use original URLs) | `false` |

### Examples

```bash
# Sync to configured vault
/autopaper-sync-obsidian 2026-W05-tech

# Sync to custom vault
/autopaper-sync-obsidian 2026-W05-tech --vault ~/Dropbox/Obsidian

# Sync to custom folder
/autopaper-sync-obsidian 2026-W05-tech --folder Newsletters/2026

# Sync without embedding images
/autopaper-sync-obsidian 2026-W05-tech --no-images
```

## What It Does

1. **Locates Issue File**: Finds `<slug>.md` in issues directory
2. **Reads Configuration**: Gets vault path from config.yaml or command line
3. **Converts Links**: Transforms article references to Obsidian wikilinks
4. **Copies Images** (optional): Downloads and embeds cover images
5. **Creates Folder**: Organizes in vault folder structure
6. **Writes File**: Saves Markdown with proper Obsidian formatting

## Output Format

Synced file includes:

```markdown
---
title: AI技术周刊 · 2026年第5期
date: 2026-01-27
type: tech-weekly
tags: [newsletter, ai, tech]
cssclass: weekly-newsletter
---

# 📰 AI技术周刊 · 第5期

## 📝 编辑寄语

本周我们看到了 Agent 开发工具的重大突破...

## 🔥 热点聚焦

### [[agent-best-practices]] Agent 最佳实践

> [!info] 元数据
> - **作者**: Andrej Karpathy
> - **日期**: 2026-01-20
> - **标签**: #agent #ai #llm
> - **原文**: https://cursor.com/cn/blog/agent-best-practices

![Agent Best Practices](2026-W05-tech_images/agent-best-practices.jpg)

#### 摘要
Comprehensive guide to building AI agents...

#### 核心要点
• Start simple, iterate fast
• Focus on reliability over complexity

---

[More articles...]
```

## Wikilink Conversion

Article references are converted to wikilinks:

- **Before**: `<!-- SLUG:agent-best-practices -->`
- **After**: `[[agent-best-practices]]`

This enables:
- **Click Navigation**: Click to jump to article note
- **Backlinks**: See which newsletters reference this article
- **Graph View**: Visualize connections in knowledge graph
- **Unlinked References**: Find mentions without links

## Folder Structure

Files are organized in your vault:

```
ObsidianVault/
└── AutoPaper/
    ├── 2026-W05-tech.md
    ├── 2026-W05-tech_images/
    │   ├── agent-best-practices.jpg
    │   ├── assistant-enterprise-framework.jpg
    │   └── code-execution-paradigm.jpg
    ├── 2026-W04-tech.md
    └── articles/
        ├── agent-best-practices.md
        ├── assistant-enterprise-framework.md
        └── code-execution-paradigm.md
```

## Obsidian Integration Features

### Properties (YAML Frontmatter)

Each synced issue includes:
- **Title**: Issue title
- **Date**: Publication date
- **Type**: Issue type (tech/news)
- **Tags**: Searchable tags
- **CSS Classes**: Custom styling classes

### Callouts

Metadata uses Obsidian callout blocks:
- `[!info]` for article metadata
- `[!summary]` for summaries
- `[!quote]` for key points

### Tags

Automatically added tags:
- `#newsletter` - All newsletters
- `#tech` or `#news` - Issue type
- `#weekly` - Weekly frequency
- Topic-specific tags from articles

## Configuration

Set up your Obsidian vault in `config.yaml`:

```yaml
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper
```

Or override with command-line options.

## Image Handling

### With Image Embedding (Default)

Cover images are:
1. Downloaded from original URLs
2. Saved to `<slug>_images/` folder
3. Embedded as relative links

Example:
```markdown
![Agent Best Practices](2026-W05-tech_images/agent-best-practices.jpg)
```

### Without Image Embedding

Original URLs preserved:

```markdown
![Agent Best Practices](https://example.com/cover.jpg)
```

## Error Handling

- **Vault Not Found**: Suggests checking vault path in config.yaml
- **Issue Not Found**: Reminds to generate issue first with `/autopaper-generate`
- **Permission Error**: Checks write permissions for vault
- **Folder Creation Error**: Verifies parent directory exists

## Performance

- **Small Issue (3-5 articles)**: ~2s
- **Medium Issue (6-10 articles)**: ~3s
- **Large Issue (10+ articles)**: ~5s
- **With Images**: +2-5s depending on image count

## Benefits for Knowledge Management

### 1. Interlinking
- Link newsletter issues to article notes
- Create bidirectional links
- Build knowledge graph

### 2. Searchability
- Full-text search across all newsletters
- Filter by tags and properties
- Use Obsidian queries

### 3. Annotation
- Add highlights and comments
- Create personal summaries
- Connect to existing knowledge

### 4. Graph View
- Visualize newsletter network
- Discover thematic connections
- Track reading history

## Related Skills

- `/autopaper-generate` - Generate issue first
- `/autopaper-export-pdf` - Alternative export to PDF
