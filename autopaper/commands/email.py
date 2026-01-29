"""Send email command."""
import sys
from pathlib import Path

import typer
from rich.console import Console

from autopaper.config import config
from autopaper.database import Database
from autopaper.publishers.email import EmailPublisher

console = Console()


def send_email(
    issue_slug: str = typer.Argument(..., help="Issue slug (e.g., 2026-W04-tech)"),
    to: list[str] = typer.Option(..., "--to", "-t", help="Recipient email addresses (can be used multiple times)"),
    no_pdf: bool = typer.Option(False, "--no-pdf", help="Don't attach PDF file"),
    no_markdown: bool = typer.Option(False, "--no-markdown", help="Don't attach Markdown file"),
    subject: str = typer.Option(None, "--subject", help="Custom email subject"),
):
    """Send an issue via email.

    Args:
        issue_slug: Issue slug to send
        to: Recipient email addresses
        no_pdf: Don't attach PDF file
        no_markdown: Don't attach Markdown file
        subject: Custom email subject
    """
    db = Database(config.get_database_path())

    # Get issue from database
    issue = db.get_issue_by_slug(issue_slug)

    if not issue:
        console.print(f"[red]Issue not found: {issue_slug}[/red]")
        console.print("[dim]Use 'autopaper list' to see available issues[/dim]")
        raise typer.Exit(1)

    console.print(f"[cyan]Preparing to send issue:[/cyan] {issue_slug}")

    # Read issue markdown
    issues_dir = Path(config.get_issues_dir())
    issue_file = issues_dir / f"{issue_slug}.md"

    if not issue_file.exists():
        console.print(f"[red]Issue file not found: {issue_file}[/red]")
        raise typer.Exit(1)

    with open(issue_file, "r", encoding="utf-8") as f:
        issue_markdown = f.read()

    # Generate PDF if needed
    pdf_path = None
    if not no_pdf:
        console.print("[cyan]Checking for PDF attachment...[/cyan]")
        pdf_file = issues_dir / f"{issue_slug}.pdf"

        if pdf_file.exists():
            pdf_path = str(pdf_file)
            console.print(f"[dim]✓ Using existing PDF:[/dim] {pdf_path}")
        else:
            # Auto-generate PDF
            console.print("[yellow]PDF not found. Generating PDF...[/yellow]")
            try:
                pdf_path = _generate_pdf(issue_slug, issue)
                console.print(f"[green]✓ PDF generated:[/green] {pdf_path}")
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to generate PDF: {e}[/yellow]")
                console.print("[dim]Continuing without PDF attachment...[/dim]")
                pdf_path = None

    # Create email publisher
    publisher = EmailPublisher(config)

    # Send email
    console.print(f"[cyan]Sending email to {len(to)} recipient(s)...[/cyan]")
    for i, recipient in enumerate(to, 1):
        console.print(f"  [dim]{i}.[/dim] {recipient}")

    try:
        publisher.publish_issue(
            issue=issue,
            issue_markdown=issue_markdown,
            recipients=to,
            pdf_path=pdf_path,
            attach_pdf=not no_pdf,
            attach_markdown=not no_markdown,
        )
    except Exception as e:
        console.print(f"[red]Failed to send email: {e}[/red]")
        raise typer.Exit(1)


def _generate_pdf(issue_slug: str, issue) -> str:
    """Generate PDF for the issue.

    Args:
        issue_slug: Issue slug
        issue: Issue object

    Returns:
        Path to generated PDF
    """
    # Import export functionality
    from autopaper.commands import export

    # Temporarily redirect stdout to suppress export output
    import io
    from contextlib import redirect_stdout

    output_path = Path(config.get_issues_dir()) / f"{issue_slug}.pdf"

    # Capture output to avoid cluttering the console
    with io.StringIO() as buf, redirect_stdout(buf):
        # Call export_pdf function
        export.export_pdf(issue_slug, output=str(output_path), no_card=True)

    return str(output_path)
