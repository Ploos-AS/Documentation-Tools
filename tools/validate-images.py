#!/usr/bin/env python3
"""Validate local Markdown image assets used by documentation sources."""

from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
REMOTE_SCHEMES = {"http", "https", "data"}
SUPPORTED = {".png", ".jpg", ".jpeg", ".svg", ".pdf"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def target_path(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1:raw.index(">")]
    # Markdown permits an optional quoted title after the destination.
    return raw.split(maxsplit=1)[0]


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-images.py <manual.md>")

    source = Path(sys.argv[1])
    if not source.is_file():
        fail(f"not a file: {source}")

    text = source.read_text(encoding="utf-8")
    checked = 0
    for match in IMAGE_RE.finditer(text):
        raw = target_path(match.group(1))
        parsed = urlsplit(raw)
        if parsed.scheme.lower() in REMOTE_SCHEMES or raw.startswith("//"):
            fail(f"remote/data image is not release-reproducible: {raw}")
        if parsed.scheme:
            fail(f"unsupported image URI scheme: {raw}")

        relative = unquote(parsed.path)
        if not relative:
            fail("image target is empty")
        asset = (source.parent / relative).resolve()
        if not asset.is_file():
            fail(f"missing local image: {raw}")
        if asset.stat().st_size == 0:
            fail(f"empty local image: {raw}")
        if asset.suffix.lower() not in SUPPORTED:
            fail(f"unsupported image format {asset.suffix or '(none)'}: {raw}")
        checked += 1

    print(f"OK: {source}: local_images={checked}")


if __name__ == "__main__":
    main()
