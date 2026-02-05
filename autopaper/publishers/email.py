"""Email publisher for sending issues via email."""
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from pathlib import Path
from typing import List, Optional

from jinja2 import Template
from rich.console import Console

from autopaper.config import Config
from autopaper.models import Issue

console = Console()


class EmailPublisher:
    """Publisher for sending issues via email."""

    def __init__(self, config: Config):
        """Initialize email publisher.

        Args:
            config: Configuration object
        """
        self.config = config
        self.email_config = config.get_email_config()

    def publish_issue(
        self,
        issue: Issue,
        issue_markdown: str,
        recipients: List[str],
        pdf_path: Optional[str] = None,
        attach_pdf: bool = True,
        attach_markdown: bool = True,
    ) -> None:
        """Publish an issue via email.

        Args:
            issue: Issue object to publish
            issue_markdown: Issue markdown content
            recipients: List of recipient email addresses
            pdf_path: Path to PDF file (optional, will be generated if attach_pdf=True)
            attach_pdf: Whether to attach PDF file
            attach_markdown: Whether to attach Markdown file

        Raises:
            Exception: If email sending fails
        """
        # Validate email configuration
        if not self._validate_config():
            raise Exception("Email configuration is incomplete. Please set SMTP_HOST, EMAIL_USERNAME, EMAIL_PASSWORD, and EMAIL_FROM in .env file.")

        # Validate recipients
        for recipient in recipients:
            if not self._validate_email(recipient):
                raise ValueError(f"Invalid email address: {recipient}")

        # Generate PDF if needed
        if attach_pdf and not pdf_path:
            console.print("[yellow]PDF attachment requested but no path provided. Skipping PDF.[/yellow]")
            attach_pdf = False

        # Check if attachments exist
        if attach_pdf and pdf_path:
            if not Path(pdf_path).exists():
                console.print(f"[yellow]PDF file not found: {pdf_path}[/yellow]")
                attach_pdf = False

        md_path = None
        if attach_markdown:
            # Find the markdown file
            issues_dir = Path(self.config.get_issues_dir())
            md_path = issues_dir / f"{issue.slug}.md"
            if not md_path.exists():
                console.print(f"[yellow]Markdown file not found: {md_path}[/yellow]")
                attach_markdown = False

        # Build email
        email_message = self._build_email(
            issue=issue,
            issue_markdown=issue_markdown,
            pdf_path=pdf_path if attach_pdf else None,
            md_path=str(md_path) if attach_markdown else None,
            recipients=recipients,
        )

        # Send email
        self._send_email(email_message, recipients)

        console.print(f"[green]✓[/green] Email sent successfully to {len(recipients)} recipient(s)")

    def _validate_config(self) -> bool:
        """Validate email configuration.

        Returns:
            True if configuration is valid
        """
        return bool(
            self.email_config["host"]
            and self.email_config["port"]
            and self.email_config["username"]
            and self.email_config["password"]
            and self.email_config["from_addr"]
        )

    def _validate_email(self, email: str) -> bool:
        """Validate email address format.

        Args:
            email: Email address to validate

        Returns:
            True if email is valid
        """
        # Basic email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _build_email(
        self,
        issue: Issue,
        issue_markdown: str,
        pdf_path: Optional[str],
        md_path: Optional[str],
        recipients: List[str],
    ) -> MIMEMultipart:
        """Build email message.

        Args:
            issue: Issue object
            issue_markdown: Issue markdown content
            pdf_path: Path to PDF attachment (optional)
            md_path: Path to Markdown attachment (optional)
            recipients: List of recipient email addresses

        Returns:
            MIMEMultipart email message
        """
        # Create multipart message
        msg = MIMEMultipart("mixed")
        msg["Subject"] = self._get_email_subject(issue)
        msg["From"] = self.email_config["from_addr"]
        msg["To"] = ", ".join(recipients)

        # Generate HTML body
        html_body = self._generate_html_body(issue, issue_markdown)

        # Attach HTML body
        html_part = MIMEText(html_body, "html", "utf-8")
        msg.attach(html_part)

        # Attach PDF if provided
        if pdf_path:
            with open(pdf_path, "rb") as f:
                pdf_part = MIMEApplication(f.read(), _subtype="pdf")
                pdf_part.add_header("Content-Disposition", "attachment", filename=Path(pdf_path).name)
                msg.attach(pdf_part)
            console.print(f"  [dim]Attached PDF:[/dim] {Path(pdf_path).name}")

        # Attach Markdown if provided
        if md_path:
            with open(md_path, "rb") as f:
                md_part = MIMEText(f.read().decode("utf-8"), "markdown", "utf-8")
                md_part.add_header("Content-Disposition", "attachment", filename=Path(md_path).name)
                msg.attach(md_part)
            console.print(f"  [dim]Attached Markdown:[/dim] {Path(md_path).name}")

        return msg

    def _get_email_subject(self, issue: Issue) -> str:
        """Generate email subject.

        Args:
            issue: Issue object

        Returns:
            Email subject line
        """
        if issue.issue_type == "tech":
            return f"本周技术精选 · {issue.slug[:8]}"
        else:
            return f"本周行业动态 · {issue.slug[:8]}"

    def _generate_html_body(self, issue: Issue, issue_markdown: str) -> str:
        """Generate HTML email body.

        Args:
            issue: Issue object
            issue_markdown: Issue markdown content

        Returns:
            HTML email body
        """
        from rich.console import Console
        import base64

        console = Console()

        # Parse issue markdown to extract sections
        sections = self._parse_issue_markdown(issue_markdown)

        # Generate AI card and convert to base64 for email embedding
        ai_card_base64 = None
        try:
            # Import skill to generate card
            from pathlib import Path as LibPath
            from autopaper.ai import generate_infocard

            # Determine title
            if issue.issue_type == "tech":
                title = f"本周技术精选 · {issue.slug[:8]}"
            else:
                title = f"本周行业动态 · {issue.slug[:8]}"

            # Get issues directory
            issues_dir = LibPath(self.config.get_issues_dir())
            card_png_path = issues_dir / f"{issue.slug}-aicard.png"

            # Check if PNG exists
            if card_png_path.exists():
                # Convert PNG to base64
                with open(card_png_path, "rb") as img_file:
                    img_data = img_file.read()
                    ai_card_base64 = base64.b64encode(img_data).decode('utf-8')
                console.print(f"  [dim]✓ AI card converted to base64 for email[/dim]")
            else:
                # Generate SVG first
                card_svg_path = issues_dir / f"{issue.slug}-aicard.svg"
                if not card_svg_path.exists():
                    svg_code = generate_infocard.generate_infocard(
                        content=issue_markdown, title=title, style=issue.issue_type, key_points=None
                    )
                    generate_infocard.save_infocard(svg_code, str(card_svg_path))

                # Convert SVG to PNG
                try:
                    import cairosvg
                    with open(card_svg_path, "rb") as svg_file:
                        svg_data = svg_file.read()
                        png_data = cairosvg.svg2png(bytestring=svg_data, output_width=800, output_height=450)
                    with open(card_png_path, "wb") as png_file:
                        png_file.write(png_data)

                    # Convert to base64
                    ai_card_base64 = base64.b64encode(png_data).decode('utf-8')
                    console.print(f"  [dim]✓ AI card generated and converted for email[/dim]")
                except Exception as e:
                    console.print(f"  [yellow]⚠ Failed to convert AI card: {e}[/yellow]")

        except Exception as e:
            console.print(f"  [yellow]⚠ Failed to generate AI card for email: {e}[/yellow]")

        # Load template
        template_path = Path(__file__).parent.parent / "templates" / "email.html.j2"

        if not template_path.exists():
            # Fallback to simple HTML if template not found
            return self._generate_simple_html(issue, sections)

        with open(template_path, "r", encoding="utf-8") as f:
            template = Template(f.read())

        # Convert markdown sections to HTML
        if sections.get("introduction"):
            sections["introduction"] = self._markdown_to_html(sections["introduction"])
        if sections.get("trends"):
            sections["trends"] = self._markdown_to_html(sections["trends"])

        # Convert article content to HTML
        for article in sections.get("article_blocks", []):
            if article.get("content"):
                article["content_html"] = self._markdown_to_html(article.get("content", "")[:500])

        # Render template
        return template.render(
            issue_type=issue.issue_type,
            title=self._get_email_subject(issue),
            week_range=f"{issue.start_date} to {issue.end_date}",
            generated_at=issue.created_at.strftime("%Y-%m-%d") if issue.created_at else "",
            ai_card_base64=ai_card_base64,
            **sections,
        )

    def _markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown text to HTML (simplified for email).

        Args:
            markdown_text: Markdown formatted text

        Returns:
            HTML formatted string
        """
        if not markdown_text:
            return ""

        import re
        html = markdown_text

        # Convert bold text **text** to <strong>text</strong>
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

        # Convert italic text *text* to <em>text</em>
        html = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', html)

        # Convert code text `text` to <code>text</code>
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # Convert links [text](url) to <a href="url">text</a>
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

        # Split into lines and process
        lines = html.split('\n')
        result = []
        in_list = False

        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                continue

            # Numbered list items like "1. **Title**: content"
            if re.match(r'^\d+\.\s+\*\*', line):
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(f'<p>{line}</p>')
            else:
                result.append(f'<p>{line}</p>')

        return '<br>'.join(result)

    def _generate_simple_html(self, issue: Issue, sections: dict) -> str:
        """Generate simple HTML email body (fallback).

        Args:
            issue: Issue object
            sections: Parsed sections

        Returns:
            HTML email body
        """
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                .article {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #777; font-size: 12px; }}
                strong {{ font-weight: bold; }}
                em {{ font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{self._get_email_subject(issue)}</h1>
                <p><strong>日期范围:</strong> {issue.start_date} 至 {issue.end_date}</p>
        """

        if sections.get("introduction"):
            html += f"<h2>主编导语</h2><p>{self._markdown_to_html(sections['introduction'])}</p>"

        if sections.get("trends"):
            html += f"<h2>核心趋势</h2><p>{self._markdown_to_html(sections['trends'])}</p>"

        if sections.get("article_blocks"):
            html += "<h2>深度文章</h2>"
            for article in sections["article_blocks"]:
                title = article.get("title", "")
                content = article.get("content", "")[:200]
                url = article.get("url", "")
                html += f"""
                <div class="article">
                    <h3>{title}</h3>
                    <p>{self._markdown_to_html(content)}...</p>
                    {f'<p><a href="{url}">阅读原文</a></p>' if url else ''}
                </div>
                """

        html += f"""
                <div class="footer">
                    <p>本邮件由 AutoPaper 自动生成</p>
                    <p>生成时间: {issue.created_at.strftime('%Y-%m-%d %H:%M') if issue.created_at else ''}</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def _parse_issue_markdown(self, markdown: str) -> dict:
        """Parse issue markdown into sections.

        Args:
            markdown: Issue markdown content

        Returns:
            Dictionary with sections: introduction, trends, article_blocks, news_briefs
        """
        sections = {
            "introduction": "",
            "trends": "",
            "article_blocks": [],
            "news_briefs": [],
        }

        # Map Chinese section names to English keys
        section_map = {
            "主编导语": "introduction",
            "核心趋势": "trends",
            "深度文章": "article_blocks",
            "快讯速览": "news_briefs",
        }

        lines = markdown.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    if current_section == "article_blocks":
                        sections[current_section] = self._parse_article_blocks("\n".join(current_content))
                    elif current_section == "news_briefs":
                        sections[current_section] = self._parse_news_briefs("\n".join(current_content))
                    else:
                        sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                section_name = line[3:].strip()
                current_section = section_map.get(section_name, section_name.lower().replace(" ", "_"))
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            if current_section == "article_blocks":
                sections[current_section] = self._parse_article_blocks("\n".join(current_content))
            elif current_section == "news_briefs":
                sections[current_section] = self._parse_news_briefs("\n".join(current_content))
            else:
                sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _parse_article_blocks(self, content: str) -> list:
        """Parse article blocks from markdown.

        Args:
            content: Article section content

        Returns:
            List of article block dictionaries
        """
        blocks = []
        current_block = None
        current_content = []

        lines = content.split("\n")

        for line in lines:
            if line.startswith("### "):
                # Save previous block
                if current_block:
                    current_block["content"] = "\n".join(current_content).strip()
                    blocks.append(current_block)

                # Start new block
                current_block = {
                    "title": line[4:].strip(),
                    "slug": "",
                    "content": "",
                    "tags": [],
                    "url": "",
                }
                current_content = []

            elif line.startswith("**标签**:") or line.startswith("**Tags**:"):
                tags_line = line.split(":", 1)[1].strip()
                tags = [t.strip() for t in tags_line.split(",")]
                if current_block:
                    current_block["tags"] = tags

            elif line.startswith("**原文链接**:") or line.startswith("**Original URL**:"):
                url_line = line.split(":", 1)[1].strip()
                if "](" in url_line:
                    url_start = url_line.find("](") + 2
                    url_end = url_line.find(")", url_start)
                    if url_end > url_start:
                        url = url_line[url_start:url_end]
                        if current_block:
                            current_block["url"] = url

            elif line.startswith("<!-- SLUG:"):
                slug = line.replace("<!-- SLUG:", "").replace("-->", "").strip()
                if current_block:
                    current_block["slug"] = slug

            else:
                current_content.append(line)

        # Save last block
        if current_block:
            current_block["content"] = "\n".join(current_content).strip()
            blocks.append(current_block)

        return blocks

    def _parse_news_briefs(self, content: str) -> list:
        """Parse news briefs from markdown.

        Args:
            content: News briefs section content

        Returns:
            List of news brief dictionaries
        """
        briefs = []

        for line in content.split("\n"):
            if line.strip().startswith("- "):
                line = line.strip()[2:]

                if "**" in line:
                    title_end = line.find("**", 2)
                    if title_end > 0:
                        title = line[2:title_end]
                        summary = line[title_end + 2:].strip(": ").strip()
                        briefs.append({"title": title, "summary": summary, "url": ""})

        return briefs

    def _send_email(self, msg: MIMEMultipart, recipients: List[str]) -> None:
        """Send email via SMTP.

        Args:
            msg: Email message to send
            recipients: List of recipient email addresses

        Raises:
            Exception: If sending fails
        """
        host = self.email_config["host"]
        port = self.email_config["port"]
        username = self.email_config["username"]
        password = self.email_config["password"]

        console.print(f"[cyan]Connecting to SMTP server:[/cyan] {host}:{port}")

        try:
            # Create SMTP session
            if port == 465:
                # SSL connection
                server = smtplib.SMTP_SSL(host, port, timeout=30)
            else:
                # TLS connection
                server = smtplib.SMTP(host, port, timeout=30)
                server.starttls()

            # Login
            console.print("[cyan]Authenticating...[/cyan]")
            server.login(username, password)

            # Send email
            console.print(f"[cyan]Sending email to {len(recipients)} recipient(s)...[/cyan]")
            server.send_message(msg)

            # Quit
            server.quit()

        except smtplib.SMTPAuthenticationError:
            raise Exception("SMTP authentication failed. Please check your username and password.")
        except smtplib.SMTPConnectError:
            raise Exception(f"Failed to connect to SMTP server {host}:{port}")
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
