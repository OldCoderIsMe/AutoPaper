#!/usr/bin/env python3
"""发送测试邮件"""
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autopaper.config import config
from autopaper.publishers.email import EmailPublisher
from autopaper.models import Issue
from rich.console import Console

console = Console()


def create_test_issue() -> Issue:
    """创建测试用的 Issue 对象"""
    return Issue(
        id=1,
        slug="test-email-001",
        issue_type="tech",
        start_date=datetime.now().strftime("%Y-%m-%d"),
        end_date=datetime.now().strftime("%Y-%m-%d"),
        content="",
        created_at=datetime.now(),
    )


def create_test_markdown() -> str:
    """创建测试用的 Markdown 内容"""
    return """# 本周技术精选 - 测试邮件

## 主编导语
这是一封来自 AutoPaper 的测试邮件，用于验证邮件发送功能是否正常工作。

## 核心趋势

1. **人工智能**: AI 技术持续发展，在各种应用场景中展现出强大的能力。
2. **云计算**: 云原生技术成为企业数字化转型的关键驱动力。
3. **开源生态**: 开源项目蓬勃发展，社区活跃度持续提升。

## 深度文章

### AI 辅助编程的新范式

**标签**: AI, 编程, 效率

随着 Claude、GPT 等大语言模型的发展，AI 辅助编程正在改变开发者的工作方式。本文探讨如何利用 AI 工具提高编程效率。

**原文链接**: [阅读全文](https://example.com)

<!-- SLUG: ai-assisted-coding -->

### 云原生架构设计最佳实践

**标签**: 云原生, 微服务, 架构

本文总结了云原生架构设计的最佳实践，包括服务拆分、数据一致性、服务治理等方面的经验分享。

**原文链接**: [阅读全文](https://example.com)

<!-- SLUG: cloud-native-best-practices -->

## 快讯速览

- **GitHub 推出新功能**: GitHub 发布了新的 AI 编程助手功能
- **Kubernetes 更新**: K8s 最新版本增强了安全性特性
- **Python 3.13 发布**: Python 3.13 带来性能提升和新特性
"""


def main():
    """主函数"""
    console.print("[bold cyan]AutoPaper 测试邮件发送[/bold cyan]\n")

    # 创建测试 issue
    test_issue = create_test_issue()
    test_markdown = create_test_markdown()

    # 获取收件人
    recipient = config.get_email_config()["from_addr"]
    # 提取邮箱地址（去掉 "AutoPaper <..." 格式）
    if "<" in recipient and ">" in recipient:
        start = recipient.find("<") + 1
        end = recipient.find(">")
        recipient = recipient[start:end]

    console.print(f"[cyan]发送测试邮件到:[/cyan] {recipient}")
    console.print(f"[dim]主题: {test_issue.slug}[/dim]\n")

    # 创建邮件发布器
    publisher = EmailPublisher(config)

    try:
        # 发送邮件（不附加 PDF 和 Markdown）
        publisher.publish_issue(
            issue=test_issue,
            issue_markdown=test_markdown,
            recipients=[recipient],
            pdf_path=None,
            attach_pdf=False,
            attach_markdown=False,
        )

        console.print(f"\n[green]✓ 测试邮件发送成功！[/green]")
        console.print(f"[dim]请检查邮箱 {recipient} 查看测试邮件[/dim]")

    except Exception as e:
        console.print(f"\n[red]✗ 发送失败: {e}[/red]")
        console.print("[dim]请检查:[/dim]")
        console.print("  1. SMTP 配置是否正确")
        console.print("  2. 授权码是否正确（QQ 邮箱需要使用授权码）")
        console.print("  3. 网络连接是否正常")
        sys.exit(1)


if __name__ == "__main__":
    main()
