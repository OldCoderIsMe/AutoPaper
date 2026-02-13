#!/usr/bin/env python3
"""Launcher: 从 skill 根目录运行 scripts/main.py，保持「python main.py」用法不变。"""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    script = Path(__file__).resolve().parent / "scripts" / "main.py"
    sys.exit(subprocess.run([sys.executable, str(script)] + sys.argv[1:]).returncode)
