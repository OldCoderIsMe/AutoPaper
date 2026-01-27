# AutoPaper — 自动报刊工具方案

## 一、项目目标

AutoPaper 是一个 CLI 驱动的自动报刊生成工具。

核心能力：

- 通过 URL 批量采集文章
- 自动提取文章元信息与核心内容
- 按时间 / 标签 / 作者生成技术或科技资讯报刊
- 生成 Markdown 报刊
- 导出 PDF
- 一键同步到 Obsidian Vault，形成长期知识库

定位：

Automated Editorial Agent  
From links to insights.

支持两类报刊：

- technical（技术深度）
- news（科技资讯）

设计原则：

- 极简 CLI
- 本地优先
- Markdown 即协议
- Claude 负责内容理解
- AutoPaper 负责流程编排

---

## 二、技术栈

- Python 3.11+
- Typer（CLI）
- SQLite（本地存储）
- requests + readability-lxml（正文提取）
- Jinja2（模板）
- WeasyPrint（PDF）
- PyYAML（配置）

Claude Code + Skills 用于：

- 文章结构化
- 标签归一化
- 报刊合成

---

## 三、目录结构

```
autopaper/
articles/
raw/
parsed/
enriched/
issues/
publishers/
obsidian.py

skills/

templates/
db.sqlite
config.yaml
main.py
```
---

## 四、CLI 设计

### 添加文章

```bash
autopaper add <url>
```

行为：
	•	抓取网页
	•	提取正文
	•	调用 extract_article_metadata skill
	•	存入 SQLite

⸻

### 查看文章

```
autopaper list
autopaper list --tag=ai
autopaper list --week=2026-W04
```

⸻

### 生成报刊

```
autopaper generate tech --last-week
autopaper generate news --last-week
```

### 可选：

```
autopaper generate tech --tag=k8s --limit=10
```
输出：
	•	issues/{year-week}-{type}.md

⸻

### 导出 PDF

```
autopaper export 2026-W04-tech
```

### 流程：

```
markdown → html → pdf
```
⸻

### 同步 Obsidian

```
autopaper sync obsidian 2026-W04-tech
```
或：

```
autopaper generate tech --last-week --sync-obsidian
```

⸻

## 五、配置文件 config.yaml

```
obsidian:
  vault_path: "/Users/you/ObsidianVault"
  issues_folder: "AutoPaper/Issues"
  articles_folder: "AutoPaper/Articles"
```

⸻

## 六、数据模型

### Article

字段：
	•	id
	•	url
	•	title
	•	author
	•	source
	•	publish_date
	•	added_date
	•	summary
	•	tags (json)
	•	article_type (technical/news)
	•	key_points (json)

⸻

### Issue
	•	id
	•	type
	•	start_date
	•	end_date
	•	content

⸻

## 七、Claude Skills

### 1. extract_article_metadata

输入：
	•	url
	•	article content

输出：

{
  "title": "",
  "author": "",
  "source": "",
  "publish_date": "",
  "summary": "",
  "tags": [],
  "article_type": "technical|news",
  "key_points": []
}

规则：

technical = 架构 / 原理 / 源码 / 系统设计
news = 产品 / 融资 / 行业动态

⸻

### 2. normalize_tags

统一标签：
	•	LLM / 大模型 → llm
	•	Kubernetes / K8s → kubernetes

⸻

### 3. compose_issue

输入：
	•	articles
	•	issue_type
	•	start_date
	•	end_date

输出：

{
  "issue_markdown": "",
  "article_blocks": [
    {
      "slug": "",
      "title": "",
      "content": "",
      "tags": []
    }
  ]
}

### Markdown 结构：
```

# 本周技术精选 · 2026 W04

## 主编导语

## 核心趋势

## 深度文章

## 快讯速览

```
⸻

## 八、Obsidian 同步规范

### 直接写文件到 Vault。

目录：

AutoPaper/
  Issues/
  Articles/


⸻ prompt

### Issue 文件

带 Frontmatter：


type: issue
week: 2026-W04
category: tech
generated_at: 2026-01-27



⸻

### Article 文件

每篇拆成独立文件：


type: article
source: xxx
author: xxx
tags: []

```
# 标题

原文链接：

摘要

关键点

Issue 中使用：

[[article-slug]]

形成 Obsidian Graph。
```
⸻

## 九、PDF 导出

使用 Jinja2 模板渲染 HTML。

风格参考 InfoQ 周刊：
	•	主编导语
	•	分类卡片
	•	文章摘要块

HTML → WeasyPrint → PDF。

⸻

## 十、MVP 范围

必须完成：
	•	add / list / generate
	•	extract_article_metadata
	•	compose_issue
	•	SQLite
	•	Obsidian sync
	•	PDF export

暂不实现：
	•	Web UI
	•	用户系统
	•	云同步

⸻

## 十一、开发任务

Claude Code 请：
	1.	Scaffold 项目
	2.	实现 CLI
	3.	实现 SQLite models
	4.	接入 skills
	5.	实现 Obsidian publisher
	6.	实现 PDF export
	7.	提供 README 与示例

目标：

本地 CLI 可完整跑通：

URL → 报刊 → Obsidian → PDF

---