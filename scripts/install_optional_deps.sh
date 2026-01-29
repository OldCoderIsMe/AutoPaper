#!/bin/bash
# Installation script for optional dependencies

echo "AutoPaper - Installing optional dependencies"
echo "=========================================="
echo ""

echo "Installing aiohttp and pillow for concurrent image downloads..."
pip install aiohttp pillow

echo ""
echo "Installing pydantic for configuration validation..."
pip install pydantic

echo ""
echo "✓ Optional dependencies installed!"
echo ""
echo "You can now run full tests:"
echo "  python3 test_fixes.py           # High-priority fixes"
echo "  python3 test_medium_priority.py  # Medium-priority optimizations"
