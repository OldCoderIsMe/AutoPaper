# 🎉 GitHub Release 创建指南

## 方法 1：通过 GitHub 网页界面（推荐）

### 第 1 步：访问 Releases 页面
点击以下链接直接跳转到创建 Release 页面：

👉 **https://github.com/OldCoderIsMe/AutoPaper/releases/new**

### 第 2 步：填写 Release 信息

#### Tag
```
v0.1.0
```
（点击 "Choose a tag" 会自动建议创建新 tag，选择 "Create new tag: v0.1.0 on publish"）

#### Target
选择 `main` 分支

#### Release Title
```
AutoPaper v0.1.0 - Claude Code Skills Support
```

#### Description
复制以下内容到描述框：

---

```markdown
# 🎉 AutoPaper v0.1.0 - Initial Release

AI-Powered Automated Newspaper Generation Tool with Claude Code Skills support

## ✨ Features

### 🤖 AI-Powered Curation
- Smart metadata extraction using Claude AI
- Automatic tag classification and normalization
- AI-generated editorial content and trend analysis

### 📰 Auto-Generated Newspapers
- Weekly tech/news issues with editor's insights
- Thematic article grouping
- Professional formatting

### 📄 Multiple Export Formats
- **Markdown**: Clean, readable format
- **PDF**: Professional typography with cover images
- **Obsidian**: Wikilinks for knowledge management

### 🚀 Dual Usage Modes

#### 1. Claude Code Skills (New!)
```
/plugin marketplace add OldCoderIsMe/AutoPaper
/autopaper-add https://example.com/article
/autopaper-generate tech
/autopaper-export-pdf 2026-W05-tech
/autopaper-sync-obsidian 2026-W05-tech
```

#### 2. CLI Tool
```bash
pip install git+https://github.com/OldCoderIsMe/AutoPaper.git
autopaper add https://example.com/article
autopaper generate tech
autopaper export-pdf 2026-W05-tech
autopaper sync obsidian 2026-W05-tech
```

### ⚡ High Performance
- **100x faster** with AI caching for duplicate articles
- **10x faster** with concurrent image downloads
- Automatic retry with exponential backoff
- Smart logging and performance monitoring

### 🛡️ Production Ready
- Robust error handling
- Comprehensive logging
- Full test coverage
- MIT License

## 📦 Installation

### Claude Code Users (Recommended)
```
/plugin marketplace add OldCoderIsMe/AutoPaper
```

### CLI Users
```bash
pip install git+https://github.com/OldCoderIsMe/AutoPaper.git
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

## 📚 Documentation

- [Quick Start Guide](https://github.com/OldCoderIsMe/AutoPaper/blob/main/docs/QUICKSTART.md)
- [Claude Skills Guide](https://github.com/OldCoderIsMe/AutoPaper/blob/main/claude-skills/README.md)
- [Design Document](https://github.com/OldCoderIsMe/AutoPaper/blob/main/docs/AutoPaper-Design.md)
- [Contributing](https://github.com/OldCoderIsMe/AutoPaper/blob/main/CONTRIBUTING.md)

## 🔧 Requirements

- Python 3.10+
- Anthropic API key

## 🙏 Acknowledgments

Built with:
- [Claude](https://www.anthropic.com/claude) - AI capabilities
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [WeasyPrint](https://weasyprint.org/) - PDF generation

## 📝 License

MIT License - see [LICENSE](https://github.com/OldCoderIsMe/AutoPaper/blob/main/LICENSE) file for details

## 🔗 Links

- GitHub: https://github.com/OldCoderIsMe/AutoPaper
- Issues: https://github.com/OldCoderIsMe/AutoPaper/issues
- Documentation: https://github.com/OldCoderIsMe/AutoPaper#readme

---

**Full Changelog**: https://github.com/OldCoderIsMe/AutoPaper/blob/main/CHANGELOG.md
```

---

### 第 3 步：设置选项

- ✅ **Set as the latest release** (勾选)
- ❌ **Set as a pre-release** (不勾选)

### 第 4 步：发布

点击绿色按钮 **"Publish release"**

---

## 方法 2：使用 GitHub CLI（需要认证）

### 第 1 步：认证 GitHub CLI

```bash
gh auth login
```

按提示选择：
1. What account do you want to log into? → **GitHub.com**
2. What is your preferred protocol for Git operations? → **HTTPS**
3. Authenticate Git with your GitHub credentials? → **Yes**
4. How would you like to authenticate GitHub CLI? → **Login with a web browser**

然后按 Enter，浏览器会打开，完成授权。

### 第 2 步：创建 Release

认证成功后，运行以下命令创建 release：

```bash
gh release create v0.1.0 \
  --title "AutoPaper v0.1.0 - Claude Code Skills Support" \
  --notes-file GITHUB_RELEASE_NOTES.md
```

---

## ✅ 验证 Release

发布成功后，访问以下链接验证：

👉 **https://github.com/OldCoderIsMe/AutoPaper/releases**

你应该看到：
- Release 版本：v0.1.0
- 标题：AutoPaper v0.1.0 - Claude Code Skills Support
- 完整的描述内容
- "Latest release" 标签

---

## 🎯 发布后检查清单

- [ ] Release 页面显示正常
- [ ] Tag v0.1.0 已创建
- [ ] 描述内容格式正确
- [ ] 所有链接可访问
- [ ] 安装指令可以执行

---

## 📢 宣传（可选）

发布成功后，你可以：

1. **分享到社交媒体**
   - Twitter/X: "🎉 Just released AutoPaper v0.1.0 - an AI-powered newspaper generation tool with Claude Code Skills support! https://github.com/OldCoderIsMe/AutoPaper"

2. **提交到相关目录**
   - Hacker News
   - Reddit (r/Python, r/ArtificialIntelligence)
   - 技术社区

3. **更新个人博客/网站**
   - 添加项目链接
   - 写使用心得

---

**创建成功后告诉我，我可以帮你验证！**
