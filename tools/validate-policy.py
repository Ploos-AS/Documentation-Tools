#!/usr/bin/env python3
"""Validate required manual sections for Documentation-Tools project profiles."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")

POLICIES = {
    "generic": {
        "required": {"introduction", "installation", "usage", "troubleshooting"},
    },
    "cli": {
        "required": {"introduction", "installation", "usage", "command reference", "troubleshooting"},
    },
    "library": {
        "required": {"introduction", "installation", "api reference", "troubleshooting"},
    },
    "amiga": {
        "required": {"introduction", "requirements", "installation", "quick start", "troubleshooting"},
    },
    "amiga-cli": {
        "required": {"introduction", "requirements", "installation", "quick start", "command reference", "troubleshooting"},
    },
    "amiga-library": {
        "required": {"introduction", "requirements", "installation", "api reference", "troubleshooting"},
    },
}


def normalize(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text.strip().lower())
    return re.sub(r"\s+", " ", text)


def sections(path: Path) -> set[str]:
    result: set[str] = set()
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 2:
            result.add(normalize(match.group(2)))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manual", type=Path)
    parser.add_argument("--profile", choices=sorted(POLICIES), required=True)
    parser.add_argument("--arexx", action="store_true", help="require an ARexx Reference section")
    args = parser.parse_args()

    if not args.manual.is_file():
        parser.error(f"manual not found: {args.manual}")

    present = sections(args.manual)
    required = set(POLICIES[args.profile]["required"])
    if args.arexx:
        if not args.profile.startswith("amiga"):
            parser.error("--arexx is only valid with an Amiga profile")
        required.add("arexx reference")

    # Usage may be represented by the more task-oriented Quick Start section.
    if "usage" in required and "usage" not in present and "quick start" in present:
        required.remove("usage")

    missing = sorted(required - present)
    if missing:
        print(f"FAIL: {args.manual}: profile={args.profile}: missing required section(s): {', '.join(missing)}")
        return 1

    print(
        f"PASS: {args.manual}: profile={args.profile}: "
        f"required sections present" + ("; ARexx documented" if args.arexx else "")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
