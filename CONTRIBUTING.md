# Contributing to AutoPaper

感谢你考虑为 AutoPaper 贡献！我们欢迎各种形式的贡献。

## 🚀 快速开始

### 开发环境设置

1. **Fork 并克隆仓库**
   ```bash
   git clone https://github.com/OldCoderIsMe/AutoPaper.git
   cd AutoPaper
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # 开发依赖
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，添加你的 ANTHROPIC_API_KEY
   ```

5. **运行测试**
   ```bash
   pytest
   ```

## 📋 贡献类型

我们欢迎以下类型的贡献：

- 🐛 **Bug 修复**
- ✨ **新功能**
- 📚 **文档改进**
- 🎨 **UI/UX 改进**
- ⚡ **性能优化**
- 🧪 **测试用例**
- 🌍 **国际化**

## 🔄 开发工作流

### 1. 分支策略

- `main` - 主分支，保持稳定
- `feature/*` - 新功能开发
- `fix/*` - Bug 修复
- `docs/*` - 文档更新

### 2. 提交代码

```bash
git checkout -b feature/your-feature-name
# 进行开发...
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 3. Pull Request 流程

1. 确保你的代码通过测试
   ```bash
   pytest
   ```

2. 确保代码格式符合规范
   ```bash
   black autopaper/
   isort autopaper/
   ```

3. 提交 Pull Request 到 GitHub
   - 提供清晰的标题和描述
   - 引用相关的 Issue
   - 确保 CI 检查通过

4. 等待代码审查和合并

## 📝 代码规范

### Python 代码风格

- 使用 **Black** 进行代码格式化
- 使用 **isort** 进行 import 排序
- 遵循 **PEP 8** 规范
- 添加类型提示
- 编写文档字符串

```python
from typing import List, Optional

def process_articles(articles: List[Article]) -> Optional[dict]:
    """Process a list of articles and generate issue.

    Args:
        articles: List of article objects

    Returns:
        Generated issue dictionary or None if failed
    """
    ...
```

### 测试规范

- 为新功能添加测试
- 保持测试覆盖率 > 80%
- 使用清晰的测试名称
- 添加测试文档

```python
def test_add_article_with_valid_url():
    """Test adding article with valid URL."""
    url = "https://example.com/article"
    article = add_command.add(url)
    assert article.id is not None
    assert article.slug is not None
```

### Commit 消息规范

使用语义化提交消息：

```
feat: 添加新功能
fix: 修复 Bug
docs: 更新文档
style: 代码格式调整
refactor: 重构代码
perf: 性能优化
test: 添加测试
chore: 构建/工具链更新
```

## 🐛 报告 Bug

在创建 Issue 前，请检查：

1. 问题是否已被报告
2. 提供复现步骤
3. 包含环境信息：
   - 操作系统和版本
   - Python 版本
   - 相关依赖版本

## ✨ 提出新功能

1. 先创建 Issue 讨论设计
2. 说明用例和预期行为
3. 等待维护者反馈

## 📚 文档贡献

- 修正拼写和语法错误
- 改进现有文档的清晰度
- 添加使用示例
- 翻译文档

## 🎨 设计贡献

- UI/UX 改进
- 图标和Logo设计
- PDF模板优化

## 🤝 行为准则

- 尊重不同观点
- 建设性沟通
- 关注解决问题而非人
- 接受反馈并学习

## 📧 联系方式

- **Issues**: [GitHub Issues](https://github.com/OldCoderIsMe/AutoPaper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OldCoderIsMe/AutoPaper/discussions)

## 🙏 致谢

感谢所有贡献者让 AutoPaper 变得更好！

---

**注意**: 提交代码即表示你同意你的贡献将在 [MIT License](LICENSE) 下发布。
