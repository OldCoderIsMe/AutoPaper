#!/bin/bash
# Quick publish script - Push to GitHub

echo "=========================================="
echo "AutoPaper - Quick Publish to GitHub"
echo "=========================================="
echo ""

# Check if user has set up their GitHub username
read -p "Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

echo ""
echo "Updating repository URLs with your username..."
# Update pyproject.toml
sed -i.bak "s|your-username|$username|g" pyproject.toml
echo "✓ Updated pyproject.toml"

# Update CONTRIBUTING.md
sed -i.bak "s|your-username|$username|g" CONTRIBUTING.md
echo "✓ Updated CONTRIBUTING.md"

# Update GITHUB_RELEASE_CHECKLIST.md
sed -i.bak "s|your-username|$username|g" GITHUB_RELEASE_CHECKLIST.md
echo "✓ Updated GITHUB_RELEASE_CHECKLIST.md"

# Clean up backup files
rm -f pyproject.toml.bak CONTRIBUTING.md.bak GITHUB_RELEASE_CHECKLIST.md.bak

echo ""
echo "Review the changes:"
git status

echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    rm -f pyproject.toml.bak CONTRIBUTING.md.bak GITHUB_RELEASE_CHECKLIST.md.bak
    exit 0
fi

# Add all files
echo ""
echo "Adding files to Git..."
git add .

# Commit
echo ""
echo "Creating initial commit..."
git commit -m "feat: initial release of AutoPaper v0.1.0

- AI-powered article curation with Claude
- Automatic weekly newspaper generation
- PDF export and Obsidian sync
- High performance with caching and concurrent downloads
- Comprehensive logging and error handling
- Full test coverage

Co-authored-by: AutoPaper Contributors"

# Add remote if not exists
if ! git remote get-origin &> /dev/null; then
    echo ""
    echo "Adding remote origin..."
    git remote add origin "https://github.com/$username/AutoPaper.git"
fi

# Push
echo ""
echo "Pushing to GitHub..."
echo "  Repository: https://github.com/$username/AutoPaper"
echo ""
read -p "Press Enter to push to GitHub (or Ctrl+C to cancel)..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✓ Published successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Visit your repository:"
echo "     https://github.com/$username/AutoPaper"
echo ""
echo "  2. Create a Release:"
echo "     https://github.com/$username/AutoPaper/releases/new"
echo "     Tag: v0.1.0"
echo ""
echo "  3. Add a star badge to your README (optional)"
echo ""
