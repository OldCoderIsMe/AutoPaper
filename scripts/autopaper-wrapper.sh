#!/bin/bash
# AutoPaper wrapper script
# Ensures commands run from the project directory

PROJECT_DIR="/Users/smzdm/work/claude/AutoPaper"

cd "$PROJECT_DIR" || exit 1
/Users/smzdm/work/claude/AutoPaper/venv/bin/python -m autopaper.main "$@"
