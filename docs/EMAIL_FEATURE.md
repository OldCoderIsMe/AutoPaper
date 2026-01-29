# Email Sending Feature

AutoPaper supports sending generated newspaper issues via email using SMTP.

## Features

- ✅ Send issues with HTML email body
- ✅ Attach PDF file (auto-generated if needed)
- ✅ Attach Markdown source file
- ✅ Support multiple recipients
- ✅ Custom email subjects
- ✅ Responsive HTML email templates
- ✅ Support for all standard SMTP servers (Gmail, Outlook, QQ, 163, etc.)

## Configuration

### 1. Set up SMTP environment variables

Add the following to your `.env` file:

```bash
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=AutoPaper <your_email@gmail.com>
```

### 2. Common SMTP Servers

#### Gmail
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Note**: Gmail requires an App Password instead of your regular password:
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable 2-Step Verification
3. Go to Security > 2-Step Verification > App passwords
4. Generate a new app password and use it as `EMAIL_PASSWORD`

#### Outlook
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

#### QQ Mail
```bash
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
```

**Note**: QQ Mail requires an authorization code. Enable SMTP service in QQ Mail settings and use the authorization code as password.

#### 163 Mail
```bash
SMTP_HOST=smtp.163.com
SMTP_PORT=465
```

**Note**: 163 Mail uses SSL on port 465 (not TLS).

#### Other SMTP Services

For other email providers, check their SMTP settings:
- Host: usually `smtp.provider.com`
- Port: 587 (TLS) or 465 (SSL)
- Username: your full email address
- Password: your password or app-specific password

## Usage

### Basic Usage

Send an issue to a single recipient:

```bash
autopaper send-email 2026-W04-tech --to user@example.com
```

### Multiple Recipients

Send to multiple recipients:

```bash
autopaper send-email 2026-W04-tech --to user1@example.com --to user2@example.com --to user3@example.com
```

### Without PDF Attachment

Skip PDF attachment (faster):

```bash
autopaper send-email 2026-W04-tech --to user@example.com --no-pdf
```

### Without Markdown Attachment

Skip Markdown attachment:

```bash
autopaper send-email 2026-W04-tech --to user@example.com --no-markdown
```

### Custom Email Subject

Use a custom email subject:

```bash
autopaper send-email 2026-W04-tech --to user@example.com --subject "本周技术精选"
```

### Combined Options

```bash
autopaper send-email 2026-W04-tech \
  --to user1@example.com \
  --to user2@example.com \
  --subject "技术周报第4期" \
  --no-markdown
```

## How It Works

1. **Load Issue**: Reads issue information from the database
2. **Read Markdown**: Loads the issue markdown file from `issues/` directory
3. **Generate PDF** (optional): If PDF doesn't exist and `--no-pdf` is not set, automatically generates PDF
4. **Build Email**: Creates HTML email body using Jinja2 template
5. **Attach Files**: Attaches PDF and/or Markdown files
6. **Send Email**: Connects to SMTP server and sends the email

## Email Template

The email template is located at `autopaper/templates/email.html.j2`. It includes:

- Responsive design for mobile and desktop
- Styled headers and sections
- Article previews with tags
- Read more links
- Professional footer

You can customize the template by editing this file.

## Troubleshooting

### Authentication Failed

**Error**: `SMTP authentication failed`

**Solution**:
- Check your username and password
- For Gmail, use an App Password (not your regular password)
- For QQ/163 mail, use the authorization code

### Connection Failed

**Error**: `Failed to connect to SMTP server`

**Solution**:
- Check SMTP_HOST and SMTP_PORT
- Verify your network connection
- Check if firewall blocks SMTP ports

### PDF Generation Failed

**Error**: `Failed to generate PDF`

**Solution**:
- Use `--no-pdf` flag to skip PDF attachment
- Check if WeasyPrint is installed correctly
- Verify issue markdown file exists

### Email Not Received

**Solution**:
- Check spam/junk folder
- Verify recipient email address is correct
- Check SMTP server logs
- Try sending to yourself first

## Testing

Test your email configuration:

```bash
python test_email.py
```

This will check:
- Email configuration is complete
- Email validation works correctly
- Email template exists

## Security Best Practices

1. **Never commit `.env` file to Git**
   - The `.env` file contains sensitive credentials
   - It's already in `.gitignore`

2. **Use App-Specific Passwords**
   - For Gmail, use App Passwords instead of regular password
   - For other providers, use authorization codes when available

3. **Use TLS/SSL**
   - Always use encrypted connections (port 587 for TLS, 465 for SSL)
   - Never use port 25 without encryption

4. **Limit Access**
   - Only send to intended recipients
   - Double-check email addresses before sending

## Examples

### Example 1: Weekly Tech Newsletter

Send weekly tech newsletter to team:

```bash
autopaper send-email 2026-W04-tech \
  --to team@company.com \
  --to manager@company.com \
  --subject "Weekly Tech Newsletter - Week 4"
```

### Example 2: Quick Update (No Attachments)

Send quick update without attachments:

```bash
autopaper send-email 2026-W04-tech \
  --to user@example.com \
  --no-pdf \
  --no-markdown
```

### Example 3: Full Newsletter with All Attachments

Send full newsletter with PDF and Markdown:

```bash
autopaper send-email 2026-W04-tech \
  --to subscriber1@example.com \
  --to subscriber2@example.com \
  --to subscriber3@example.com
```

## Advanced Usage

### Programmatic Usage

You can also use the EmailPublisher class directly in Python:

```python
from autopaper.config import config
from autopaper.database import Database
from autopaper.publishers.email import EmailPublisher

# Load issue
db = Database(config.get_database_path())
issue = db.get_issue_by_slug("2026-W04-tech")

# Read markdown
with open("issues/2026-W04-tech.md", "r") as f:
    markdown = f.read()

# Create publisher and send
publisher = EmailPublisher(config)
publisher.publish_issue(
    issue=issue,
    issue_markdown=markdown,
    recipients=["user@example.com"],
    pdf_path="issues/2026-W04-tech.pdf",
    attach_pdf=True,
    attach_markdown=True,
)
```

## Future Enhancements

Planned features for future releases:

- [ ] Support for email API services (SendGrid, Mailgun)
- [ ] Custom email templates
- [ ] Email sending logs
- [ ] Bulk email sending (mailing lists)
- [ ] Scheduled email sending
- [ ] Email preview before sending
- [ ] BCC/CC support

## Support

For issues or questions:

1. Check this documentation
2. Run `python test_email.py` to verify configuration
3. Check error messages carefully
4. Open an issue on [GitHub](https://github.com/OldCoderIsMe/AutoPaper/issues)
