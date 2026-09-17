#!/usr/bin/env python3
"""Check local Markdown links and heading fragments without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "irc:", "tel:")


def slug(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"[- ]+", "-", text).strip("-")


def anchors(path: Path) -> set[str]:
    result: set[str] = set()
    counts: dict[str, int] = {}
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slug(match.group(1))
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        result.add(base if count == 0 else f"{base}-{count}")
    return result


def check(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    in_code = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for raw in LINK_RE.findall(line):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(EXTERNAL_SCHEMES):
                continue
            target = unquote(target)
            file_part, sep, fragment = target.partition("#")
            destination = path if not file_part else (path.parent / file_part).resolve()
            if not destination.exists():
                errors.append(f"{path}:{lineno}: missing link target: {target}")
                continue
            if sep and fragment and destination.is_file() and destination.suffix.lower() == ".md":
                if slug(fragment) not in anchors(destination):
                    errors.append(f"{path}:{lineno}: missing heading fragment: {target}")
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
            continue
        errors.extend(check(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: checked local links in {len(sys.argv) - 1} Markdown file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
