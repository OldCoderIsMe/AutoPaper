#!/bin/bash
# AutoPaper GitHub Release Preparation Script
# This script helps prepare the project for GitHub release

set -e

echo "=========================================="
echo "AutoPaper GitHub Release Preparation"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository not found. Initializing..."
    git init
    echo -e "${GREEN}✓${NC} Git repository initialized"
else
    echo -e "${YELLOW}!${NC} Git repository already exists"
fi

# Check for sensitive files
echo ""
echo "Checking for sensitive files..."

if [ -f ".env" ] && grep -q "ANTHROPIC_API_KEY=sk-ant-" .env 2>/dev/null; then
    echo -e "${RED}✗ CRITICAL: .env contains real API key!${NC}"
    echo "  Please remove the API key before committing:"
    echo "  Edit .env and replace the key with: ANTHROPIC_API_KEY=your_key_here"
    exit 1
else
    echo -e "${GREEN}✓${NC} No real API keys in .env"
fi

# Check for database and cache files
echo ""
echo "Checking for generated files..."

if [ -d "data" ] && [ -f "data/db.sqlite" ]; then
    echo -e "${YELLOW}!${NC} Database file exists (should be in .gitignore)"
fi

if [ -d "cache" ]; then
    echo -e "${YELLOW}!${NC} Cache directory exists (should be in .gitignore)"
fi

# Check if all required files exist
echo ""
echo "Checking required files..."

required_files=(
    "LICENSE"
    "README.md"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    ".gitignore"
    "pyproject.toml"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (missing)"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo -e "${RED}Some required files are missing. Please create them first.${NC}"
    exit 1
fi

# Run tests if pytest is available
echo ""
echo "Running tests..."
if command -v pytest &> /dev/null; then
    if pytest test_*.py -v --tb=short 2>&1 | tee /tmp/pytest_output.txt; then
        echo -e "${GREEN}✓${NC} All tests passed"
    else
        echo -e "${YELLOW}!${NC} Some tests failed. Check output above."
    fi
else
    echo -e "${YELLOW}!${NC} pytest not found. Skipping tests."
fi

# Code formatting check
echo ""
echo "Checking code formatting..."
if command -v black &> /dev/null; then
    if black --check autopaper/ 2>&1 | head -1; then
        echo -e "${GREEN}✓${NC} Code formatting looks good"
    else
        echo -e "${YELLOW}!${NC} Code needs formatting. Run: black autopaper/"
    fi
else
    echo -e "${YELLOW}!${NC} black not found. Skipping format check."
fi

# Create .env.example if it doesn't exist
if [ ! -f ".env.example" ]; then
    echo ""
    echo "Creating .env.example..."
    cat > .env.example << 'EOF'
# AutoPaper Environment Variables
# Copy this file to .env and add your actual API keys

# Anthropic API Key (required)
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_api_key_here
EOF
    echo -e "${GREEN}✓${NC} .env.example created"
fi

# Create requirements-dev.txt if it doesn't exist
if [ ! -f "requirements-dev.txt" ]; then
    echo ""
    echo "Creating requirements-dev.txt..."
    cat > requirements-dev.txt << 'EOF'
# Development dependencies for AutoPaper

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0

# Code formatting and linting
black>=23.0.0
isort>=5.0.0
flake8>=6.0.0

# Type checking
mypy>=1.0.0
EOF
    echo -e "${GREEN}✓${NC} requirements-dev.txt created"
fi

# Summary
echo ""
echo "=========================================="
echo "Preparation Summary"
echo "=========================================="
echo ""
echo -e "${GREEN}✓${NC} Project is ready for GitHub release!"
echo ""
echo "Next steps:"
echo "  1. Review the changes:"
echo "     git status"
echo ""
echo "  2. Add all files:"
echo "     git add ."
echo ""
echo "  3. Create initial commit:"
echo "     git commit -m \"feat: initial release of AutoPaper v0.1.0\""
echo ""
echo "  4. Create repository on GitHub"
echo "     https://github.com/new"
echo ""
echo "  5. Push to GitHub:"
echo "     git remote add origin https://github.com/your-username/autopaper.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""
echo -e "${YELLOW}Important reminders:${NC}"
echo "  - Never commit .env with real API keys"
echo "  - Update 'your-username' in URLs to your GitHub username"
echo "  - Review LICENSE and CONTRIBUTING.md before publishing"
echo ""
