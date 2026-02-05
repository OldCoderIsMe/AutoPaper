# AI Info Card Generator

生成 AI 风格的信息卡片，适合技术博客、社交媒体分享。

## 功能

- 🎨 **现代 AI 科技风格**
- 📐 **1200x675 横屏设计**（16:9）
- 🌙 **深色主题**，专业感
- 🇨🇳 **优化的中文字体支持**
- 🎯 **自动提取 4 个关键要点**
- 🎭 **支持 tech/news 两种风格**

## 使用方法

### 基本用法

```bash
# 生成简单卡片
python main.py "本周技术精选 · 2026-W05"

# 从文件生成
python main.py "文章标题" --content ./article.md

# 从管道读取内容
echo "# 文章内容..." | python main.py "标题" --content -

# 指定风格和输出
python main.py "标题" --style news --output card.svg

# 自定义关键点
python main.py "标题" --key-points "要点1,要点2,要点3,要点4"
```

### 样式选项

- **tech**: 技术风格，蓝色主题
  - 主色：#0066CC（科技蓝）
  - 适用：技术文章、架构设计、编程教程

- **news**: 新闻风格，绿色主题
  - 主色：#10B981（绿色）
  - 适用：行业动态、产品发布、新闻汇总

### 输出

- **格式**: SVG（矢量图）
- **尺寸**: 1200 x 675 (16:9)
- **用途**:
  - 博客封面图
  - 社交媒体分享（Twitter、LinkedIn、微信）
  - 演示文稿
  - 新闻周刊缩略图

## 配置

### 环境变量

```bash
# 必需：Anthropic API Key
export ANTHROPIC_API_KEY=your_key

# 可选：自定义 API endpoint
export ANTHROPIC_BASE_URL=https://api.anthropic.com

# 可选：指定模型
export ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
```

### Python 依赖

```bash
pip install -r requirements.txt
```

必需的包：
- `anthropic>=0.18.0` - Anthropic Claude API

## 示例

### 技术周刊卡片

```bash
python main.py "本周技术精选 · 第5期" \
  --content weekly-summary.md \
  --style tech \
  --output tech-week-05.svg
```

### 新闻动态卡片

```bash
python main.py "行业动态 · 2026年1月" \
  --content news.md \
  --style news \
  --output news-2026-01.svg
```

### 自定义关键点

```bash
python main.py "AI编程工具演进" \
  --key-points "从对话式到闭环式,自主Agent架构,云原生技术深化,工具链无缝集成" \
  --style tech
```

## 架构

```
generate-card/
├── main.py              # 主逻辑
├── SKILL.md             # 文档
└── requirements.txt     # 依赖
```

### 核心功能

1. **内容分析** - 从 Markdown 提取关键要点
2. **AI 生成** - 使用 Claude 创建 SVG 卡片
3. **样式系统** - 预设的配色方案
4. **中文优化** - 字体栈和布局优化

## 设计规范

### 尺寸和布局

- 总尺寸：1200 x 675px（16:9）
- 左侧区域（40%）：标题和信息
- 右侧区域（60%）：关键要点列表

### 字体要求

**标题**：
- 字号：40-48px
- 字重：粗体
- 字体：PingFang SC, system-ui

**要点**：
- 序号：24-26px，粗体，强调色
- 内容：18-20px，常规
- 行间距：1.8-2.0倍字号

### 配色方案

**Tech 风格**：
- 主背景：#0F1419
- 卡片背景：#1A1F26
- 主色：#0066CC
- 辅助色：#00A1E9

**News 风格**：
- 主背景：#0F1419
- 卡片背景：#1A1F26
- 主色：#10B981
- 辅助色：#34D399

## 使用场景

- 📱 **社交媒体分享**
  - Twitter/X
  - LinkedIn
  - 微信朋友圈

- 📝 **内容创作**
  - 博客封面图
  - 文章缩略图
  - 演示文稿

- 📰 **新闻周刊**
  - 每周技术精选
  - 行业动态汇总
  - 项目更新通告

## 高级用法

### 批量生成

```bash
# 从配置文件批量生成
while read title content_file; do
  python main.py "$title" --content "$content_file"
done < cards.txt
```

### 集成到工作流

```bash
# 在 Makefile 中
card.svg: article.md
	python claude-skills/generate-card/main.py \
		"文章标题" \
		--content article.md \
		--output card.svg
```

### 结合其他工具

```bash
# 先提取元数据，再生成卡片
metadata=$(python claude-skills/extract-metadata/main.py "$url")
title=$(echo "$metadata" | jq -r '.title')
python main.py "$title" --content article.md
```

## 性能

- **生成时间**: ~5-10 秒（AI 生成）
- **输出大小**: ~10-50 KB（SVG）
- **可缩放**: 矢量格式，任意放大不失真

## 故障排除

### 中文显示问题

如果中文显示不正确，确保：
1. SVG 中指定了中文字体栈
2. 系统安装了中文字体
3. 使用 UTF-8 编码保存

### API 调用失败

1. 检查 API Key 是否正确
2. 确认网络连接正常
3. 查看 API 配额是否用完

### 布局问题

如果关键点文字重叠：
1. 减少关键点字数
2. 手动指定关键点
3. 调整内容长度

## 许可证

MIT License - 详见 AutoPaper 项目

## 相关

- [Article Metadata Extractor](../extract-metadata/) - 提取文章元数据
- [AutoPaper](../../) - 完整的新闻周刊生成工具
