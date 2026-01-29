# AutoPaper

> AI 驱动的自动化周刊生成工具 🤖📰

[English](README.md) | [简体中文](README.zh-CN.md)

AutoPaper 是一个命令行工具，可以从文章链接自动生成精选的周报。它使用 Claude AI 来提取元数据、撰写编辑内容，并导出为多种格式。

## ✨ 特性

- **🤖 AI 驱动的内容策划** - 使用 Claude 智能提取元数据和撰写期刊内容
- **📰 自动生成周刊** - 包含编辑洞察的科技/新闻周刊
- **🏷️ 智能标签** - 自动标签分类和规范化
- **📄 多种导出格式** - Markdown、PDF、Obsidian 笔记库同步、邮件发送
- **📧 邮件分发** - 通过邮件发送期刊，包含 AI 卡片、PDF 附件和 HTML 渲染
- **🎨 AI 卡片生成** - 生成精美的 AI 风格信息图卡片，便于社交分享
- **⚡ 高性能** - 通过 AI 缓存和并发下载实现 100 倍速度提升
- **🛡️ 生产就绪** - 强大的错误处理、重试逻辑和全面的日志记录

## 📦 快速开始

### 方式一：Claude Code 技能（推荐给 Claude Code 用户）

如果你使用 **Claude Code**，可以将 AutoPaper 安装为技能：

```
/plugin marketplace add OldCoderIsMe/AutoPaper
```

然后使用以下技能：
```
/autopaper-add https://blog.example.com/article
/autopaper-generate tech
/autopaper-export-pdf 2026-W05-tech
```

📖 详情请参阅 [claude-skills/README.md](claude-skills/README.md)

### 方式二：CLI 工具（传统 Python 包）

#### 前置要求

- Python 3.10+
- Anthropic API key

#### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/OldCoderIsMe/AutoPaper.git
cd AutoPaper

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 以可编辑模式安装
pip install -e .

# 配置环境
cp .env.example .env
# 编辑 .env 文件并添加你的 ANTHROPIC_API_KEY
```

#### 使 `autopaper` 命令可用

安装完成后，你有两个选择：

##### 方案 A：添加到 PATH（推荐，适合频繁使用）

在 `~/.zshrc`（或 `~/.bashrc`）中添加：

```bash
# AutoPaper 虚拟环境
export PATH="$PATH:/path/to/AutoPaper/venv/bin"
```

然后重新加载：`source ~/.zshrc`

##### 方案 B：每次使用时激活虚拟环境

```bash
cd /path/to/AutoPaper
source venv/bin/activate
autopaper --help
```

## 🚀 快速使用

### 完整工作流示例

```bash
# 1. 一周内持续添加文章
autopaper add https://blog.example.com/ai-tool-review
autopaper add https://news.example.com/tech-trend-2026

# 2. 查看所有文章
autopaper list-articles

# 3. 生成周报
autopaper generate tech

# 4. 导出为 PDF（包含 AI 卡片）
autopaper export-pdf 2026-W05-tech

# 5. 通过邮件发送给团队
autopaper send-email 2026-W05-tech \
  --to team@company.com \
  --to manager@company.com \
  --to subscribers@company.com

# 6. 可选：同步到 Obsidian
autopaper sync obsidian 2026-W05-tech
```

### 你将获得什么

每个生成的期刊包含：

- **📄 PDF 文档** - 专业排版，包含 AI 卡片
- **📧 邮件 HTML** - 富文本格式邮件，内嵌 AI 卡片
- **📝 Markdown 源文件** - 纯文本，便于版本控制
- **🎨 AI 卡片** - 可分享的信息图（2400x1350px）
- **🔗 Obsidian 笔记** - 集成到你的知识库

### 邮件发送示例

```bash
# 发送给单个收件人
autopaper send-email 2026-W05-tech --to user@example.com

# 发送给多个收件人
autopaper send-email 2026-W05-tech \
  --to user1@example.com \
  --to user2@example.com \
  --to user3@example.com

# 自定义邮件主题
autopaper send-email 2026-W05-tech \
  --to user@example.com \
  --subject "本周技术精选第5期"

# 发送时不附带 PDF
autopaper send-email 2026-W05-tech \
  --to user@example.com \
  --no-pdf
```

### 命令列表

| 命令 | 描述 |
|---------|-------------|
| `autopaper add <url>` | 从 URL 添加文章 |
| `autopaper list` | 列出所有文章 |
| `autopaper generate <type>` | 生成周刊（tech/news） |
| `autopaper export-pdf <slug>` | 导出期刊为 PDF |
| `autopaper send-email <slug>` | 通过邮件发送期刊 |
| `autopaper sync obsidian <slug>` | 同步到 Obsidian 笔记库 |

运行 `autopaper --help` 查看所有命令和选项。

## 📚 文档

- **[快速入门指南](docs/QUICKSTART.md)** - 详细的设置和使用说明
- **[邮件功能指南](docs/EMAIL_FEATURE.md)** - 邮件发送配置和使用
- **[设计文档](docs/AutoPaper-Design.md)** - 架构和技术细节
- **[贡献指南](CONTRIBUTING.md)** - 贡献指南

## 🏗️ 项目结构

```
AutoPaper/
├── autopaper/          # 主包
│   ├── commands/        # CLI 命令
│   │   ├── add.py       # 添加文章
│   │   ├── generate.py  # 生成期刊
│   │   ├── export.py    # PDF 导出
│   │   ├── email.py     # 邮件发送
│   │   └── sync.py      # Obsidian 同步
│   ├── publishers/      # 导出发布器
│   │   ├── pdf.py       # PDF 生成
│   │   ├── obsidian.py  # Obsidian 同步
│   │   └── email.py     # 邮件发布器
│   ├── scrapers/        # 网页抓取
│   ├── templates/       # Jinja2 模板
│   │   ├── issue.html.j2  # PDF 模板
│   │   └── email.html.j2  # 邮件模板
│   └── utils/          # 工具函数
├── skills/             # AI 集成
│   ├── generate_infocard.py  # AI 卡片生成
│   └── ...
├── tests/              # 测试套件
├── docs/               # 文档
│   ├── QUICKSTART.md
│   ├── EMAIL_FEATURE.md
│   └── AutoPaper-Design.md
└── issues/             # 生成的期刊
```

## 🔧 配置

### 环境变量

在项目根目录创建 `.env` 文件：

```bash
# ============================================
# API 配置
# ============================================

# API Key - 支持 ANTHROPIC_API_KEY 和 ANTHROPIC_AUTH_TOKEN
ANTHROPIC_API_KEY=your_api_key_here

# API Base URL（可选 - 用于自定义端点或代理）
# 默认：https://api.anthropic.com
# 智谱AI (GLM-4) 示例：
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic

# 模型配置（可选）
# ANTHROPIC_MODEL - 所有请求的默认模型
# ANTHROPIC_DEFAULT_SONNET_MODEL - Sonnet 专用请求
# ANTHROPIC_DEFAULT_OPUS_MODEL - Opus 专用请求
# ANTHROPIC_DEFAULT_HAIKU_MODEL - Haiku 专用请求
#
# GLM-4（智谱AI）示例：
ANTHROPIC_MODEL=glm-4.7
ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.7
#
# Claude（Anthropic）示例：
# ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
# ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5-20250929

# ============================================
# 邮件配置 (SMTP)
# ============================================

# SMTP 服务器配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=AutoPaper <your_email@gmail.com>

# 常用 SMTP 服务器：
# - Gmail: smtp.gmail.com:587
# - Outlook: smtp-mail.outlook.com:587
# - QQ 邮箱: smtp.qq.com:587
# - 163 邮箱: smtp.163.com:465

# 注意：Gmail 需要使用应用专用密码，不是普通密码
# 获取方式：Google 账户 > 安全性 > 两步验证 > 应用专用密码
```

### config.yaml

编辑 `config.yaml` 进行自定义：

```yaml
# 数据库
database_path: data/db.sqlite

# Obsidian 同步
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper

# 标签规范化
tag_normalization:
  llm: [llm, large language model, gpt]
  kubernetes: [k8s]
```

## 🤖 AI 功能

AutoPaper 使用 Claude AI 实现：

- **元数据提取** - 标题、作者、摘要、关键点
- **标签分类** - 自动分类
- **期刊撰写** - 编辑评论、趋势分析
- **内容理解** - 智能文章策划
- **AI 卡片生成** - 精美的信息图卡片，包含关键要点

### AI 卡片

AutoPaper 会自动为每个期刊生成 AI 风格的信息图卡片：

- **1200x675** 横版格式（16:9）
- 现代深色主题，渐变强调色
- 智能总结 4 个关键点
- 专业设计，适合社交媒体分享
- 内嵌于 PDF 和邮件中

#### 示例卡片

```bash
# 生成独立卡片
autopaper generate-card 2026-W05-tech

# 卡片自动包含在：
# - PDF 导出
# - 邮件 HTML 正文（作为 base64 图片）
```

## 📊 性能

- **100 倍更快** - AI 缓存重复文章
- **10 倍更快** - 并发图片下载
- **自动重试** - 网络弹性
- **智能日志** - 性能监控

## 🛠️ 开发

### 设置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black autopaper/
isort autopaper/
```

### 测试

```bash
# 运行所有测试
pytest tests/

# 带覆盖率
pytest --cov=autopaper tests/
```

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

构建于以下工具：
- [Claude](https://www.anthropic.com/claude) - AI 能力
- [Typer](https://typer.tiangolo.com/) - CLI 框架
- [Rich](https://rich.readthedocs.io/) - 终端格式化
- [WeasyPrint](https://weasyprint.org/) - PDF 生成
- [Jinja2](https://jinja.palletsprojects.com/) - 模板引擎
- [aiosmtplib](https://github.com/cole/aiosmtplib) - 异步 SMTP 客户端

## 📧 邮件发送

AutoPaper 支持通过邮件发送生成的期刊：

- **富文本邮件** - 渲染 markdown，内嵌 AI 卡片
- **PDF 附件** - 高质量 PDF，包含 AI 卡片
- **Markdown 附件** - 源文件归档
- **多收件人** - 一次发送给无限数量的收件人
- **主流服务商** - Gmail、Outlook、QQ 邮箱、163 邮箱等

### 快速开始

```bash
# 1. 在 .env 中配置 SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=AutoPaper <your@gmail.com>

# 2. 发送邮件
autopaper send-email 2026-W05-tech --to recipient@example.com
```

📖 详细的邮件设置指南请参阅 [docs/EMAIL_FEATURE.md](docs/EMAIL_FEATURE.md)

---

**准备好自动化你的简报工作流了吗？** 🚀

- 文档：[docs/](docs/)
- 邮件指南：[docs/EMAIL_FEATURE.md](docs/EMAIL_FEATURE.md)
- 贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md)
- 问题反馈：[GitHub Issues](https://github.com/OldCoderIsMe/AutoPaper/issues)
