# AutoPaper Generate Issue

Generate weekly newspaper issue from collected articles with AI-composed editorial content.

## Description

This skill analyzes all articles in the database, groups them by themes, generates AI-written editor's notes and trend analysis, and creates a comprehensive weekly newspaper issue in Markdown format.

## Usage

### Basic Usage

```
/autopaper-generate tech
```

### With Options

```
/autopaper-generate tech --week 2026-W05 --title "AI Weekly"
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `<type>` | Issue type: `tech` or `news` | - |
| `--week <slug>` | Custom week slug (format: YYYY-W##) | Current week |
| `--title <text>` | Custom issue title | Auto-generated |
| `--no-editorial` | Skip AI editorial generation | `false` |
| `--articles <ids>` | Specific article IDs (comma-separated) | All articles |

### Examples

```bash
# Generate tech weekly for current week
/autopaper-generate tech

# Generate specific week
/autopaper-generate tech --week 2026-W04

# Generate with custom title
/autopaper-generate news --title "This Week in AI"

# Generate from specific articles only
/autopaper-generate tech --articles 123,124,125

# Generate without AI editorial
/autopaper-generate tech --no-editorial
```

## What It Does

1. **Selects Articles**: Filters articles by type and recency
2. **Groups by Themes**: Uses AI to identify common themes
3. **Generates Editorial**: Creates editor's note with:
   - Issue overview
   - Trend analysis
   - Article highlights
   - Thematic connections
4. **Composes Issue**: Formats content with:
   - Cover metadata
   - Editor's note
   - Themed article sections
   - Summary cards
5. **Saves to File**: Outputs Markdown file to `issues/` directory

## Output Format

Generated issue includes:

```markdown
---
title: AI技术周刊 · 2026年第5期
date: 2026-01-27
type: tech
slug: 2026-W05-tech
cover: 2026-W05-tech-cover.png
---

# 📰 AI技术周刊 · 第5期

## 📝 编辑寄语

[AI-generated editorial about this week's trends...]

## 🔥 热点聚焦

### [[agent-best-practices]] Agent 最佳实践

**标签**: agent, ai, llm
**作者**: Andrej Karpathy
**时间**: 2026-01-20

![Agent Best Practices](https://example.com/cover.jpg)

#### 摘要
Comprehensive guide to building AI agents...

#### 核心要点
• Start simple, iterate fast
• Focus on reliability over complexity
• Test extensively in production

---

[More articles...]
```

## Issue Types

### tech
Technology-focused newsletters featuring:
- AI and machine learning
- Programming and development
- Software architecture
- Tools and frameworks

### news
General news covering:
- Industry updates
- Company news
- Product launches
- Market trends

## AI-Generated Content

### Editor's Note

The AI analyzes all articles and generates:

- **Issue Overview**: High-level summary of this week's content
- **Trend Analysis**: Identifies recurring themes and patterns
- **Article Highlights**: Calls out must-read articles
- **Thematic Grouping**: Organizes articles into coherent sections
- **Transition Text**: Smooth flow between sections

### Example Editorial

```
本周我们看到了 Agent 开发工具的重大突破。Karpathy 分享了
20年编程经验被 AI 改变的观察，而阿里巴巴则开源了
Assistant Agent 企业级框架。这些进展不仅展示了 AI Agent
技术的成熟，也预示着软件开发范式的根本性变革...

本期的 5 篇文章可以归纳为三大主题：
1. Agent 最佳实践与范式演进
2. 企业级智能助手框架
3. AI 辅助编程的迭代方法论
```

## File Output

Issues are saved to: `issues/<slug>.md`

Example:
```
issues/
├── 2026-W05-tech.md
├── 2026-W05-tech-cover.png
├── 2026-W04-tech.md
└── 2026-W04-news.md
```

## Error Handling

- **No Articles Found**: Suggests adding articles first with `/autopaper-add`
- **AI API Error**: Shows error details, can retry with `--no-editorial` to skip AI
- **File Write Error**: Checks directory permissions and disk space

## Performance

- **Small Issue (3-5 articles)**: ~20s
- **Medium Issue (6-10 articles)**: ~30s
- **Large Issue (10+ articles)**: ~45s

## Environment Variables

Required:
- `ANTHROPIC_API_KEY`: Your Anthropic API key

Optional:
- `CACHE_ENABLED`: Enable/disable AI cache (default: `true`)
- `CACHE_TTL`: Cache time-to-live in seconds (default: `86400`)

## Related Skills

- `/autopaper-add` - Add articles to database
- `/autopaper-export-pdf` - Export issue to PDF
- `/autopaper-sync-obsidian` - Sync issue to Obsidian
