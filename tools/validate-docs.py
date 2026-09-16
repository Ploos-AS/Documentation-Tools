#!/usr/bin/env python3
"""Minimal M0 validation for Documentation-Tools Markdown sources."""

from pathlib import Path
import re
import sys


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-docs.py <manual.md>")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"not a file: {path}")
    if path.suffix.lower() != ".md":
        fail("manual source must use the .md extension")

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail("manual is empty")

    titles = re.findall(r"^# (.+)$", text, flags=re.MULTILINE)
    if len(titles) != 1:
        fail("manual must contain exactly one level-1 title")

    sections = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
    if not sections:
        fail("manual must contain at least one level-2 section")

    if "\t" in text:
        fail("tabs are not allowed; use spaces for reproducible rendering")

    print(f"OK: {path}: title={titles[0]!r}, sections={len(sections)}")


if __name__ == "__main__":
    main()
