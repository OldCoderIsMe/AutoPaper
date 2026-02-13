# AutoPaper 团队使用指南

> AI 驱动的自动化周刊生成工具 - 快速安装和使用指南

## 📖 简介

AutoPaper 是一个命令行工具，可以从文章链接自动生成技术周刊。它使用 Claude AI 进行智能元数据提取、内容编撰，并支持多种导出格式（PDF、Markdown、邮件、Obsidian）。

### 核心功能

- 🤖 **AI 智能提取** - 自动提取标题、作者、摘要、标签
- 📰 **自动生成周刊** - 主编导语、核心趋势、深度文章
- 📄 **多种导出格式** - PDF、Markdown、邮件、Obsidian
- 🎨 **AI 封面卡片** - 现代科技风格的信息图
- 📧 **邮件分发** - 一键发送给团队或订阅者

---

## 🛠️ 安装步骤

### 系统要求

- **Python**: 3.10 或更高版本
- **操作系统**: macOS / Linux / Windows
- **API Key**: Anthropic API Key（必需）

### Step 1: 获取 API Key

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制保存（只显示一次）

### Step 2: 安装 AutoPaper

```bash
# 克隆仓库
git clone https://github.com/OldCoderIsMe/AutoPaper.git
cd AutoPaper

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -e .
```

### Step 3: 配置环境

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用你喜欢的编辑器
```

在 `.env` 文件中添加：

```bash
# 必需配置
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxx

# 可选：使用国内 API（如智谱AI）
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-4.7
```

### Step 4: 设置全局命令

**方式 A: 添加到 PATH（推荐）**

编辑 `~/.zshrc`（macOS）或 `~/.bashrc`（Linux）：

```bash
# AutoPaper 命令路径
export PATH="$PATH:/Users/你的用户名/AutoPaper/venv/bin"
```

重新加载配置：
```bash
source ~/.zshrc
```

**方式 B: 每次手动激活**

```bash
cd /path/to/AutoPaper
source venv/bin/activate
autopaper --help
```

### 验证安装

```bash
autopaper --help
```

如果看到命令帮助信息，说明安装成功！

---

## 🚀 快速上手

### 1. 添加文章

```bash
# 添加单篇文章
autopaper add https://mp.weixin.qq.com/s/xxxxx
autopaper add https://blog.example.com/article

# 更新已存在的文章
autopaper add <URL> --force
```

### 2. 查看文章列表

```bash
autopaper list-articles
```

### 3. 生成周刊

```bash
# 生成技术类周刊
autopaper generate tech

# 生成新闻类周刊
autopaper generate news

# 自定义参数
autopaper generate tech --limit 15           # 最多15篇文章
autopaper generate tech --tag "AI"            # 只包含 AI 标签的文章
autopaper generate tech --last-week           # 生成上周的周刊
```

### 4. 导出 PDF

```bash
# 导出为 PDF（自动包含 AI 卡片）
autopaper export-pdf 2026-W07-tech

# 自定义输出路径
autopaper export-pdf 2026-W07-tech -o ~/Documents/周报.pdf

# 快速导出（不生成卡片）
autopaper export-pdf 2026-W07-tech --no-card
```

### 5. 发送邮件

**首先配置邮件设置**（在 `.env` 文件中）：

```bash
# Gmail 配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=AutoPaper <your_email@gmail.com>

# QQ 邮箱配置
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@qq.com
EMAIL_PASSWORD=你的授权码
EMAIL_FROM=AutoPaper <your_email@qq.com>

# 企业邮箱配置（示例）
SMTP_HOST=smtp.company.com
SMTP_PORT=587
EMAIL_USERNAME=yourname@company.com
EMAIL_PASSWORD=your_password
EMAIL_FROM=AutoPaper <yourname@company.com>
```

**发送邮件**：

```bash
# 发送给单人
autopaper send-email 2026-W07-tech --to user@example.com

# 发送给多人
autopaper send-email 2026-W07-tech \
  --to user1@example.com \
  --to user2@example.com \
  --to user3@example.com

# 自定义主题
autopaper send-email 2026-W07-tech \
  --to user@example.com \
  --subject "本周技术精选第7期"

# 不附加 PDF
autopaper send-email 2026-W07-tech \
  --to user@example.com \
  --no-pdf
```

### 6. 同步到 Obsidian（可选）

在 `.env` 或 `config.yaml` 中配置：

```yaml
# config.yaml
obsidian:
  vault_path: ~/Documents/ObsidianVault
  auto_paper_folder: AutoPaper
```

同步命令：

```bash
autopaper sync obsidian 2026-W07-tech
```

---

## 📂 目录结构

```
AutoPaper/
├── .env                    # 环境配置文件
├── config.yaml             # 应用配置
├── data/
│   └── db.sqlite         # 文章数据库
├── issues/                 # 生成的周刊
│   ├── 2026-W07-tech.md     # Markdown 源文件
│   ├── 2026-W07-tech.pdf     # PDF 导出
│   └── 2026-W07-tech-aicard.png  # AI 卡片
├── articles/
│   ├── raw/             # 原始文章内容
│   ├── parsed/          # 解析后的内容
│   ├── enriched/        # AI 增强的元数据
│   └── images/         # 封面图片
└── venv/                   # Python 虚拟环境
```

---

## 💡 使用技巧

### 提高效率

1. **每周固定时间添加文章** - 随时随手添加，周末统一生成
2. **使用标签分类** - 添加时注意标签准确性，便于后续筛选
3. **批量操作** - 先添加多篇，再一次性生成周刊

### 标签管理

在 `.env` 或 `config.yaml` 中配置标签规范化：

```yaml
# config.yaml
tag_normalization:
  llm: [llm, large language model, gpt, 大模型]
  ai-agent: [ai agent, agent, 智能体, 代理]
  k8s: [kubernetes, k8s]
```

### 定制周刊模板

编辑模板文件：
- `autopaper/templates/issue.md.j2` - Markdown 模板
- `autopaper/templates/issue.html.j2` - PDF 模板

---

## 🐛 常见问题

### Q: 提示 API Key 无效？

A: 检查以下几点：
- API Key 是否正确复制（无多余空格）
- 账户是否有余额
- 是否使用了正确的端点（国内用户可能需要代理）

### Q: 邮件发送失败？

A: Gmail 用户需要：
1. 开启两步验证
2. 生成应用专用密码
3. 使用应用密码而非登录密码

### Q: 命令找不到？

A: 确认：
- 虚拟环境已激活：`source venv/bin/activate`
- 或 PATH 已正确配置

### Q: 封面图片下载失败？

A: 可能是网络问题或图片链接无效，可以：
- 使用 `--force` 重新添加
- 手动指定图片

---

## 📚 更多资源

- **GitHub**: https://github.com/OldCoderIsMe/AutoPaper
- **问题反馈**: [GitHub Issues](https://github.com/OldCoderIsMe/AutoPaper/issues)
- **Claude Skills**: 支持 `/autopaper` 命令快捷调用

---

**祝使用愉快！** 🎉

如有问题，请在团队群内提问或提交 Issue。
