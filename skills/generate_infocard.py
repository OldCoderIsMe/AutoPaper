"""Generate AI-style SVG card for weekly summary."""
import os
import sys
from pathlib import Path
from typing import Dict

from anthropic import Anthropic

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopaper.config import config


def generate_infocard(
    content: str,
    title: str,
    style: str = "tech",
    key_points: list = None,
) -> str:
    """Generate an AI-style SVG card for technical content summary.

    Args:
        content: Weekly issue content or summary
        title: Card title (e.g., "本周技术精选 · 2026-W04")
        style: Card style ("tech" or "news")
        key_points: List of key points to highlight

    Returns:
        SVG code as string
    """
    # Get API key from config (supports both ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN)
    api_key = config.get_anthropic_api_key()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN environment variable not set")

    # Get optional custom base URL from config (for proxy/custom endpoint)
    base_url = config.get_anthropic_base_url()
    # Get model from config (supports ANTHROPIC_MODEL, ANTHROPIC_DEFAULT_SONNET_MODEL, or default)
    model = config.get_anthropic_model() or config.get_anthropic_sonnet_model() or config.get_model()

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = Anthropic(**client_kwargs)

    # Define color schemes
    if style == "tech":
        primary_color = "#0066CC"  # Tech blue
        secondary_color = "#00A1E9"
        bg_main = "#0F1419"  # Dark background
        bg_card = "#1A1F26"  # Card background
        text_primary = "#FFFFFF"
        text_secondary = "#A0AEC0"
        accent_colors = ["#0066CC", "#00A1E9", "#4FD1C5"]
    else:  # news
        primary_color = "#10B981"  # Green
        secondary_color = "#34D399"
        bg_main = "#0F1419"
        bg_card = "#1A1F26"
        text_primary = "#FFFFFF"
        text_secondary = "#A0AEC0"
        accent_colors = ["#10B981", "#34D399", "#6EE7B7"]

    # Prepare key points text
    key_points_text = ""
    if key_points:
        key_points_text = "\n".join([f"{i+1}. {point}" for i, point in enumerate(key_points[:4])])
    else:
        key_points_text = """1. AI编程工具从对话式向闭环式演进
2. 自主Agent架构成为新趋势
3. 云原生技术持续深化
4. 开发者工具链无缝集成"""

    prompt = f"""你是一个专业的技术内容设计师，擅长制作AI风格的技术信息图卡片。

# 任务
根据以下技术周刊内容，生成一张适合技术社交平台发布的精美SVG卡片代码。

# 输入信息
**标题**: {title}
**风格**: AI技术风格
**核心要点**:
{key_points_text}

**完整内容**:
{content[:2000]}

# 设计要求
1. **尺寸**: 1200 x 675 (横屏，16:9，适合PC阅读)
2. **风格**: AI技术风格 - 现代、智能、高颜值
3. **配色方案**:
   - 主背景: {bg_main} (深色背景，专业感)
   - 卡片背景: {bg_card} (略浅的深色)
   - 主色: {primary_color} (科技蓝/绿)
   - 辅助色: {secondary_color}
   - 主文字: {text_primary} (白色)
   - 次要文字: {text_secondary} (灰色)
   - 强调色: {", ".join(accent_colors)}

4. **视觉元素**:
   - 深色专业背景
   - AI科技感装饰元素（网格、点阵、线条、电路纹理）
   - 渐变色彩增加层次
   - 简洁的未来感图标或符号
   - 现代AI科技设计

5. **内容布局** (16:9横屏):
   - 左侧区域 (40%): 标题 + 周刊信息
   - 右侧区域 (60%): 核心要点列表 (4条)
   - 顶部: 品牌标识
   - 底部: 日期/期数信息

6. **字体要求**:
   - 标题: 粗体，大字号（40-48px）
   - 副标题: 中等字号（24-28px）
   - 要点标题: 粗体（28-32px）
   - 要点序号: 粗体（24-26px）
   - 要点内容: 常规字号（18-20px）
   - **重要**: 使用支持中文的字体栈
     - macOS: "PingFang SC", "Hiragino Sans GB", "STHeiti", "Heiti SC"
     - 通用: "system-ui", "-apple-system", "Segoe UI", "Microsoft YaHei", "SimHei"
     - 字体族: `font-family="PingFang SC, Hiragino Sans GB, STHeiti, Microsoft YaHei, SimHei, system-ui, sans-serif"`

7. **右侧要点列表布局要求**（重要！）:
   - "本周核心看点" 标题与第一个要点之间至少留 50px 空隙
   - 每个要点独立成块，使用 `<text>` 标签的 `dy` 属性分行
   - 序号单独一行，使用强调色，字号 24-26px
   - 要点内容如果超过 20 个字，必须换行显示
   - 行间距设置为 1.8-2.0 倍字号（每个要点内部行间距）
   - 每个要点之间留出 40-45px 的垂直间距
   - 参考示例：
   ```xml
   <text x="40" y="0" font-size="26" fill="{primary_color}" font-weight="bold">1.</text>
   <text x="70" y="0" font-size="20" fill="{text_primary}">AI编程工具从对话式</text>
   <text x="70" y="28" font-size="20" fill="{text_primary}">向闭环式演进</text>
   ```

8. **设计原则**:
   - AI科技专业感
   - 信息层次清晰
   - 视觉重点突出
   - 色彩对比明显
   - 适合PC端阅读
   - 可作为技术博客封面
   - **文字可读性优先**：确保右侧要点不拥挤，分行清晰

# SVG模板结构
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <!-- 定义渐变和图案 -->
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_main};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1A202C;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{primary_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{secondary_color};stop-opacity:1" />
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{primary_color}" stroke-width="0.5" opacity="0.1"/>
    </pattern>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- 主背景 -->
  <rect width="1200" height="675" fill="url(#bgGradient)"/>
  <rect width="1200" height="675" fill="url(#grid)"/>

  <!-- 顶部装饰条 -->
  <rect x="0" y="0" width="1200" height="4" fill="url(#accentGradient)"/>

  <!-- 左侧区域: 标题和品牌 -->
  <g transform="translate(60, 80)">
    <!-- 标题卡片 -->
    <rect x="0" y="0" width="420" height="200" rx="16" fill="{bg_card}" filter="url(#glow)"/>
    <text x="30" y="55" font-family="system-ui, sans-serif" font-size="42" font-weight="bold" fill="{text_primary}">{title}</text>
    <text x="30" y="100" font-family="system-ui, sans-serif" font-size="22" fill="{text_secondary}">技术周刊 · 深度解读</text>
    <rect x="30" y="130" width="80" height="4" rx="2" fill="{primary_color}"/>
    <text x="30" y="165" font-family="system-ui, sans-serif" font-size="18" fill="{text_secondary}">Generated by AutoPaper</text>
  </g>

  <!-- 右侧区域: 核心要点 -->
  <g transform="translate(540, 80)">
    <rect x="0" y="0" width="600" height="500" rx="16" fill="{bg_card}" opacity="0.8"/>
    <text x="40" y="55" font-family="system-ui, sans-serif" font-size="32" font-weight="bold" fill="{primary_color}">本周核心看点</text>

    <!-- 要点列表 - 从 y=120 开始，确保与标题有足够间距 -->
    <g transform="translate(40, 120)">
      <!-- 动态生成4个要点，每个要点间隔 50px -->
    </g>
  </g>

  <!-- 底部信息 -->
  <text x="60" y="640" font-family="system-ui, sans-serif" font-size="14" fill="{text_secondary}">2026 Week 04</text>
  <text x="1140" y="640" font-family="system-ui, sans-serif" font-size="14" fill="{text_secondary}" text-anchor="end">AI.style</text>
</svg>
```

# 要点列表样式
每个要点包含：
- 序号 (1. 2. 3. 4.) 使用强调色
- 要点内容，简洁明了（不超过30字）
- 上下间距充足

# 输出要求
1. 只输出完整的SVG代码（XML格式）
2. 不要有任何额外解释
3. SVG代码必须格式正确，可以直接保存为.svg文件
4. 确保中文字符正确显示（使用UTF-8编码）
5. 横屏设计，视觉重心合理分布
6. 信息层次清晰，一目了然

请现在生成AI风格的SVG代码：
"""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )

        svg_code = response.content[0].text

        # Clean up response if needed
        if "```xml" in svg_code:
            svg_code = svg_code.split("```xml")[1].split("```")[0].strip()
        elif "```svg" in svg_code:
            svg_code = svg_code.split("```svg")[1].split("```")[0].strip()
        elif "```" in svg_code:
            svg_code = svg_code.split("```")[1].split("```")[0].strip()

        return svg_code

    except Exception as e:
        raise RuntimeError(f"Failed to generate AI card: {e}")


def save_infocard(svg_code: str, output_path: str):
    """Save AI card to file.

    Args:
        svg_code: SVG code string
        output_path: Path to save SVG file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_code)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python generate_infocard.py <title> <output_path> [style]")
        print("Example: python generate_infocard.py '本周技术精选·2026-W04' card.svg tech")
        sys.exit(1)

    title = sys.argv[1]
    output_path = sys.argv[2]
    style = sys.argv[3] if len(sys.argv) > 3 else "tech"

    # Read content from stdin or use sample
    if sys.stdin.isatty():
        content = """
本周的技术焦点集中在 AI 编程范式的演进与传统工程深度的结合上。
我们看到了从简单的代码补全向自主 Agent 和自我参照迭代的跨越。
        """
        key_points = [
            "AI编程工具从对话式向闭环式演进",
            "Ralph Loop引入自我参照迭代机制",
            "传统基础设施精细化治理备受关注",
            "开发者工具链无缝集成趋势明显",
        ]
    else:
        content = sys.stdin.read()
        key_points = []

    try:
        svg = generate_infocard(content, title, style, key_points)
        save_infocard(svg, output_path)
        print(f"✓ AI card generated: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

