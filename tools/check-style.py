#!/usr/bin/env python3
"""Deterministic, dependency-free style checks for Markdown manuals."""

from __future__ import annotations

import re
import sys
from pathlib import Path

RULES = (
    ("trailing-whitespace", re.compile(r"[ \t]+$"), "trailing whitespace"),
    ("multiple-spaces", re.compile(r"(?<![.!?]) {3,}"), "three or more consecutive spaces"),
    ("todo-marker", re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE), "unfinished TODO/TBD/FIXME marker"),
)


def check(path: Path) -> list[str]:
    errors: list[str] = []
    in_code = False
    previous_blank = False
    blank_run = 0
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            previous_blank = False
            blank_run = 0
            continue
        if in_code:
            continue
        if not line:
            blank_run = blank_run + 1 if previous_blank else 1
            previous_blank = True
            if blank_run > 2:
                errors.append(f"{path}:{lineno}: excessive blank lines")
            continue
        previous_blank = False
        blank_run = 0
        for name, pattern, message in RULES:
            if pattern.search(line):
                errors.append(f"{path}:{lineno}: {name}: {message}")
        if line.startswith("#") and not re.match(r"^#{1,6} [^#]", line):
            errors.append(f"{path}:{lineno}: heading-style: ATX heading must contain one space after #")
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {Path(sys.argv[0]).name} <markdown> [<markdown> ...]", file=sys.stderr)
        return 2
    errors: list[str] = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            errors.append(f"{path}: not a file")
        else:
            errors.extend(check(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: style checked {len(sys.argv) - 1} Markdown file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
