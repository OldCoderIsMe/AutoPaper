# Article Metadata Extractor

自动从文章 URL 或内容中提取结构化元数据。

## 功能

- 📝 **自动提取标题、作者、来源**
- 📅 **识别发布日期**
- 🎯 **生成 2-3 句摘要**
- 🏷️ **智能标签分类**（kubernetes、llm、python 等）
- 🔤 **提取关键要点**（3-7 条）
- 📊 **自动分类**（技术类/新闻类）
- ⚡ **缓存机制**，避免重复 API 调用（7 天 TTL）

## 使用方法

### 基本用法

```bash
# 从 URL 提取元数据
python main.py https://blog.example.com/article

# 从已有内容提取（跳过网页抓取）
python main.py https://example.com --content "$(cat article.md)"

# 输出 Markdown 格式
python main.py https://example.com --output markdown

# 从管道读取 URL
echo "https://example.com" | python main.py -

# 强制刷新（不使用缓存）
python main.py https://example.com --no-cache
```

### 输出格式

**JSON 格式（默认）**:
```json
{
  "title": "文章标题",
  "author": "作者名",
  "source": "来源网站",
  "publish_date": "2026-01-15",
  "summary": "文章摘要...",
  "tags": ["kubernetes", "llm", "python"],
  "article_type": "technical",
  "key_points": [
    "要点1",
    "要点2"
  ]
}
```

**Markdown 格式**:
```bash
python main.py https://example.com --output markdown
```

输出：
```markdown
# 文章标题

**Author**: 作者名
**Source**: 来源网站
**Date**: 2026-01-15
**Type**: technical

**Tags**: kubernetes, llm, python

## Summary
文章摘要...

## Key Points
1. 要点1
2. 要点2
```

## 配置

### 环境变量

```bash
# 必需：Anthropic API Key
export ANTHROPIC_API_KEY=your_api_key_here

# 可选：自定义 API endpoint（例如使用智谱AI）
export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic

# 可选：指定模型
export ANTHROPIC_MODEL=claude-sonnet-4-5-20250929

# 可选：自定义缓存目录
export CLAUDE_SKILLS_CACHE_DIR=~/.cache/claude-skills
```

### Python 依赖

安装依赖：
```bash
pip install -r requirements.txt
```

必需的包：
- `anthropic>=0.18.0` - Anthropic Claude API
- `requests>=2.31.0` - HTTP 请求
- `readability-lxml>=0.8.1` - 网页内容提取（可选）
- `beautifulsoup4>=4.12.0` - HTML 解析（可选，fallback）

## 缓存

元数据提取结果会缓存 7 天，相同内容不会重复调用 API。

**缓存位置**: `~/.cache/claude-skills/extract-metadata/`

**清除缓存**:
```bash
# 使用 --no-cache 强制刷新
python main.py https://example.com --no-cache

# 或手动删除缓存目录
rm -rf ~/.cache/claude-skills/extract-metadata/
```

## 架构

```
extract-metadata/
├── main.py              # 主逻辑
├── SKILL.md             # 文档
└── requirements.txt     # 依赖
```

### 核心功能

1. **网页抓取** - 使用 `readability-lxml` 提取正文内容
2. **AI 分析** - 调用 Claude API 提取元数据
3. **缓存** - 避免重复 API 调用
4. **重试机制** - 自动重试失败的请求（3 次，指数退避）

## 错误处理

- **网页抓取失败**: 会显示错误并退出
- **API 调用失败**: 自动重试 3 次
- **JSON 解析失败**: 尝试多种模式解析
- **缓存读取失败**: 自动降级到 API 调用

## 使用场景

- 📰 **内容聚合** - 自动提取文章元数据构建新闻聚合
- 📚 **知识管理** - 为文章添加结构化元数据
- 🔍 **内容分析** - 分析文章类型和关键要点
- 🏷️ **标签系统** - 自动为文章打标签
- 📝 **摘要生成** - 生成文章摘要用于快速浏览

## 示例工作流

```bash
# 从多个 URL 批量提取元数据
cat urls.txt | while read url; do
  python main.py "$url"
done > metadata.json

# 提取并保存为 Markdown
python main.py https://example.com --output markdown > article.md

# 在脚本中使用
metadata=$(python main.py https://example.com)
title=$(echo "$metadata" | jq -r '.title')
echo "Title: $title"
```

## 性能

- **首次提取**: ~3-5 秒（包含网页抓取和 API 调用）
- **缓存命中**: < 0.1 秒
- **并发支持**: 可以同时运行多个实例

## 许可证

MIT License - 详见 AutoPaper 项目

## 相关

- [AI Info Card Generator](../generate-card/) - 生成 AI 风格信息卡片
- [AutoPaper](../../) - 完整的新闻周刊生成工具
