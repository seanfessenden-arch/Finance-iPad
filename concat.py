#!/bin/python3
from pathlib import Path

# Directory containing your project
SOURCE_DIR = Path(".")

# Output file
OUTPUT_FILE = Path("combined_python_files.txt")

# Directories to skip
SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
    ".mypy_cache",
    "concat.py",
    "portfolio.db",
    "test.db",
}

with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    for py_file in sorted(SOURCE_DIR.rglob("*.*")):

        # Skip unwanted directories
        if any(part in SKIP_DIRS for part in py_file.parts):
            continue

        out.write("=" * 80 + "\n")
        out.write(f"FILE: {py_file}\n")
        out.write("=" * 80 + "\n\n")

        try:
            out.write(py_file.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            out.write(py_file.read_text(encoding="utf-8", errors="replace"))

        out.write("\n\n")

print(f"Finished. Output written to {OUTPUT_FILE.resolve()}")
