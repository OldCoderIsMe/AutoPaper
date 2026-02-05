#!/usr/bin/env python3
"""
Generate AI-style SVG info cards for technical content.

This skill creates beautiful, modern infographic cards (1200x675, 16:9)
suitable for:
- Technical blog cover images
- Social media sharing (Twitter, LinkedIn)
- Presentation slides
- Newsletter thumbnails
"""

import re
import sys
from pathlib import Path
from typing import List, Optional

from anthropic import Anthropic

# Add shared tools to path
shared_path = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from shared.config import SkillConfig

# Initialize
config = SkillConfig()

# Color schemes
COLOR_SCHEMES = {
    "tech": {
        "primary": "#0066CC",
        "secondary": "#00A1E9",
        "bg_main": "#0F1419",
        "bg_card": "#1A1F26",
        "text_primary": "#FFFFFF",
        "text_secondary": "#A0AEC0",
        "accents": ["#0066CC", "#00A1E9", "#4FD1C5"],
    },
    "news": {
        "primary": "#10B981",
        "secondary": "#34D399",
        "bg_main": "#0F1419",
        "bg_card": "#1A1F26",
        "text_primary": "#FFFFFF",
        "text_secondary": "#A0AEC0",
        "accents": ["#10B981", "#34D399", "#6EE7B7"],
    },
}


def extract_key_points(content: str, max_points: int = 4) -> List[str]:
    """Extract key points from markdown content.

    Simple heuristic extraction - looks for bullet points, numbered lists,
    or short paragraphs.

    Args:
        content: Markdown content
        max_points: Maximum number of points to extract

    Returns:
        List of key points
    """
    points = []

    # Try to find bullet points
    for line in content.split("\n"):
        line = line.strip()
        # Match bullet points: -, *, •
        if re.match(r"^[\-\*\•]\s+\S+", line):
            point = re.sub(r"^[\-\*\•]\s+", "", line).strip()
            if 10 <= len(point) <= 100:  # Filter by length
                points.append(point)
                if len(points) >= max_points:
                    break

    # If no bullet points, try numbered lists
    if not points:
        for line in content.split("\n"):
            line = line.strip()
            if re.match(r"^\d+\.\s+\S+", line):
                point = re.sub(r"^\d+\.\s+", "", line).strip()
                if 10 <= len(point) <= 100:
                    points.append(point)
                    if len(points) >= max_points:
                        break

    # If still no points, try short paragraphs
    if not points:
        for line in content.split("\n"):
            line = line.strip()
            if 15 <= len(line) <= 80 and not line.startswith("#"):
                points.append(line)
                if len(points) >= max_points:
                    break

    return points[:max_points]


def generate_card(
    title: str,
    content: str = "",
    style: str = "tech",
    key_points: Optional[List[str]] = None,
) -> str:
    """Generate AI-style SVG card.

    Args:
        title: Card title
        content: Markdown content (for extracting key points)
        style: Card style ("tech" or "news")
        key_points: List of key points (auto-extracted if None)

    Returns:
        SVG code as string
    """
    # Get API configuration
    api_key = config.get_api_key()
    base_url = config.get_base_url()
    model = config.get_model()

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = Anthropic(**client_kwargs)

    # Get color scheme
    colors = COLOR_SCHEMES.get(style, COLOR_SCHEMES["tech"])

    # Prepare key points
    if key_points is None:
        if content:
            key_points = extract_key_points(content)
        else:
            key_points = [
                "AI编程工具从对话式向闭环式演进",
                "自主Agent架构成为新趋势",
                "云原生技术持续深化",
                "开发者工具链无缝集成",
            ]

    # Ensure we have exactly 4 points
    while len(key_points) < 4:
        key_points.append("更多精彩内容...")

    key_points_text = "\n".join([f"{i + 1}. {point}" for i, point in enumerate(key_points[:4])])

    # Build prompt
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
   - 主背景: {colors['bg_main']} (深色背景，专业感)
   - 卡片背景: {colors['bg_card']} (略浅的深色)
   - 主色: {colors['primary']} (科技蓝/绿)
   - 辅助色: {colors['secondary']}
   - 主文字: {colors['text_primary']} (白色)
   - 次要文字: {colors['text_secondary']} (灰色)
   - 强调色: {', '.join(colors['accents'])}

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

8. **设计原则**:
   - AI科技专业感
   - 信息层次清晰
   - 视觉重点突出
   - 色彩对比明显
   - 适合PC端阅读
   - 可作为技术博客封面
   - **文字可读性优先**：确保右侧要点不拥挤，分行清晰

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


def save_card(svg_code: str, output_path: str) -> None:
    """Save AI card to file.

    Args:
        svg_code: SVG code string
        output_path: Path to save SVG file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_code)

    print(f"[INFO] Card saved to: {output_file}", file=sys.stderr)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate AI-style info cards for technical content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate simple card
  python main.py "本周技术精选 · 2026-W05"

  # Generate from content file
  python main.py "文章标题" --content article.md

  # Specify style and output
  python main.py "标题" --style news --output card.svg

  # Custom key points
  python main.py "标题" --key-points "要点1,要点2,要点3,要点4"

  # Read content from stdin
  echo "# Content..." | python main.py "标题" --content -
        """,
    )

    parser.add_argument("title", help="Card title")
    parser.add_argument("--content", help="Content file or markdown text (use '-' for stdin)")
    parser.add_argument("--style", choices=["tech", "news"], default="tech", help="Card style")
    parser.add_argument("--output", help="Output SVG path (default: auto-generated)")
    parser.add_argument("--key-points", help="Comma-separated key points")

    args = parser.parse_args()

    # Prepare content
    content = ""
    if args.content:
        if args.content == "-":
            # Read from stdin
            content = sys.stdin.read()
        else:
            content_path = Path(args.content)
            if content_path.exists():
                content = content_path.read_text(encoding="utf-8")
            else:
                # Treat as raw text
                content = args.content

    # Prepare key points
    key_points = None
    if args.key_points:
        key_points = [p.strip() for p in args.key_points.split(",")]

    # Generate card
    try:
        print(f"[INFO] Generating {args.style} style card...", file=sys.stderr)
        print(f"[INFO] Title: {args.title}", file=sys.stderr)

        svg = generate_card(
            title=args.title,
            content=content,
            style=args.style,
            key_points=key_points,
        )

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            safe_title = re.sub(r'[^\w\s-]', '', args.title).strip()[:50]
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            output_path = f"{safe_title}-card.svg"

        # Save
        save_card(svg, output_path)

        print(f"✓ Card generated successfully!", file=sys.stderr)
        print(f"  📁 {output_path}")
        print(f"\nUsage:", file=sys.stderr)
        print(f"  • Technical blog cover", file=sys.stderr)
        print(f"  • Social media sharing", file=sys.stderr)
        print(f"  • Presentation slide", file=sys.stderr)
        print(f"  • Newsletter thumbnail", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
