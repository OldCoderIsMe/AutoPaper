# AGENTS.md

Guidance for AI coding agents working in this repository. Read this before changing code.

## Project overview

AutoPaper is a Python CLI (`autopaper`) that turns saved article URLs into curated weekly
newspaper issues. It scrapes articles, extracts metadata with Claude, composes an issue, and
exports to Markdown, HTML, PDF, email, and Obsidian.

- Language: Python (`>=3.10`)
- CLI framework: Typer + Rich
- AI: Anthropic SDK (Claude-compatible endpoints supported)
- Storage: SQLite
- Templates: Jinja2
- Package entry point: `autopaper = "autopaper.main:app"` (`pyproject.toml`)

## Repository layout

```
autopaper/
  main.py              # Typer app; registers every CLI command
  config.py            # Config discovery (config.yaml/.env), paths, API key lookup
  config_validation.py # Pydantic validation helpers
  database.py          # SQLite manager (articles, issues tables)
  models.py            # Article / Issue dataclasses
  commands/            # One module per CLI command (add, generate, export, ...)
  ai/                  # Anthropic calls: metadata, compose, tags, info cards
  scrapers/            # Article scraping/parsing
  publishers/          # PDF, email, Obsidian output
  templates/           # issue.html.j2, issue.md.j2, email.html.j2
  utils/               # cache, retry, logging, slug, web, json_parser, ...
claude-skills/
  extract-metadata/    # Standalone skill: SKILL.md + main.py launcher + scripts/
  generate-card/       # Standalone skill: SKILL.md + main.py launcher + scripts/
  shared/              # Shared skill config/cache/retry/JSON parser
  plugins/             # Packaged copies of the skills for plugin distribution
tests/                 # unittest-style tests (run with pytest)
```

Generated/ignored artifacts: `data/`, `articles/`, `issues/*.{pdf,md,png,svg}`, `cache/`,
`.env`, `*.sqlite`. Never commit these.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt
cp .env.example .env   # then set ANTHROPIC_API_KEY (never commit .env)
```

Note: the README suggests `pip install -e ".[dev]"`, but `pyproject.toml` currently defines no
`dev` extra. Use `requirements-dev.txt` instead.

## Common commands

```bash
autopaper --help
autopaper add <url> [--force]
autopaper list-articles [--tag T] [--type technical|news] [--week YYYY-Www]
autopaper delete <id> [--force]
autopaper generate tech|news [--limit N] [--tag T] [--last-week]
autopaper export-pdf <slug> [-o out.pdf] [--no-card] [--html]
autopaper send-email <slug> --to a@example.com [--to b@example.com] [--no-pdf]
autopaper generate-card <title> [--content file.md] [--style tech|news]
autopaper generate-cover <slug> [--style tech|news] [--ai] [--ai-api dalle]
autopaper sync obsidian <slug>
autopaper version
```

## Testing

```bash
python -m pytest tests/ -v
# or without pytest installed:
python -m unittest discover -s tests -v
```

- Tests live in `tests/` and use `unittest.TestCase`; pytest is only the runner.
- Runtime dependencies must be installed for the full suite: `tests/test_scrapers.py` imports
  `requests` (via `autopaper.scrapers.article`) at module load, so a bare environment reports
  an import error rather than a real failure. Install with `pip install -e .` first.
- Tests must not require real network access or an API key. Use temp dirs
  (`tempfile.mkdtemp()`) and clean up in `tearDown`, following existing tests.
- Important: `.gitignore` ignores `test_*.py` and `*_test.py`. New test files are silently
  untracked unless you name them differently or `git add -f <file>`. Verify with
  `git status` before finishing.

## Formatting and linting

Configured in `pyproject.toml` (line length 100, target py310):

```bash
black autopaper tests
isort autopaper tests
flake8 autopaper          # flake8/mypy have no repo config; keep changes warning-free
mypy autopaper            # optional but preferred for touched modules
```

Match existing style: type hints, module/function docstrings, `logger = get_logger(__name__)`
from `autopaper.utils.logging`, and Rich consoles for user-facing output. Do not add comments
that restate the code.

## Architecture notes

- **Command registration**: create `autopaper/commands/<name>.py` exposing a Typer-compatible
  function, then register it in `autopaper/main.py` via `app.command()(...)`. A global
  `--config/-c` option and directory/API-key checks run in the app callback.
- **Config discovery**: `autopaper/config.py` searches upward for `config.yaml` (or
  `pyproject.toml`), honors `AUTOPAPER_CONFIG_PATH`, and loads `.env`. API key lookup prefers
  `ANTHROPIC_API_KEY`, then `ANTHROPIC_AUTH_TOKEN`. Model/base URL come from
  `ANTHROPIC_*` env vars. `config.ensure_directories()` creates all runtime dirs.
- **Database**: SQLite file at `database_path` (default from `config.yaml`:
  `~/data/db.sqlite`; `Database` constructor default is `data/db.sqlite`). Tables `articles`
  and `issues`; `tags`/`key_points` are JSON strings. `Article.from_row` supports both 13- and
  14-column schemas (legacy rows may lack `cover_image`) — preserve that compatibility.
- **AI layer**: all model calls go through `autopaper/ai/` using the Anthropic SDK. Reuse
  `utils/cache.py` (content-hash file cache), `utils/retry.py` (exponential backoff), and
  `utils/json_parser.safe_parse_json` for model output; do not hand-roll JSON parsing.
- **Slugs**: use `utils/slug.generate_unique_slug` to avoid collisions that overwrite data.
- **Export**: `commands/export.py` renders Jinja2 templates and always writes HTML; PDF is
  produced with LibreOffice (`soffice --headless`) and currently hardcodes the macOS path.
  `publishers/pdf.py` still contains a WeasyPrint path. Keep both in mind when touching PDF
  output, and prefer not to break `--html` (HTML-only debugging).
- **Scraping**: `scrapers/article.py` + `utils/web.py` (browser-like headers) and
  `readability-lxml`; Playwright is available for JS-heavy pages. Be respectful of target
  sites and keep timeouts/retries bounded.
- **Standalone skills**: `claude-skills/*/main.py` are thin launchers that delegate to
  `scripts/main.py`; shared helpers live in `claude-skills/shared/`. Keep the `plugins/`
  mirrors consistent when changing a skill's public behavior.

## Conventions and guardrails

- Branch from `main` using `feature/*`, `fix/*`, or `docs/*`. Use semantic commit messages
  (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- Never commit secrets or credentials: no API keys, SMTP passwords, tokens, or personal
  emails/URLs in tracked files. Use `.env.example` for placeholders only.
- Keep generated outputs (`issues/`, `articles/`, `data/`, `cache/`) out of version control.
- Do not add dependencies unless necessary; if you do, update both `pyproject.toml` and the
  relevant `requirements*.txt` and the skill `requirements.txt` files where applicable.
- Preserve backward compatibility with existing SQLite data and CLI flags.
- Documentation status: `README.md` links to a `docs/` directory that is not present in this
  checkout. Do not assume those files exist; update links only if you add the files.
- Run the full test suite plus `black`/`isort` checks before considering work complete, and
  report exactly which commands you ran and their results.
