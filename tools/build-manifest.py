#!/usr/bin/env python3
"""Generate deterministic documentation release checksums and manifest."""

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--tool-ref", required=True)
    args = parser.parse_args()

    source = Path(args.source)
    output_dir = Path(args.output_dir)
    if not source.is_file():
        parser.error(f"source not found: {source}")
    if not output_dir.is_dir():
        parser.error(f"output directory not found: {output_dir}")

    assets = sorted(
        (path for path in output_dir.iterdir() if path.is_file() and path.suffix in {".pdf", ".guide"}),
        key=lambda path: path.name,
    )
    if not assets:
        parser.error("no PDF or AmigaGuide assets found")

    entries = [{"file": path.name, "sha256": sha256(path), "size": path.stat().st_size} for path in assets]
    source_hash = sha256(source)

    checksum_path = output_dir / "SHA256SUMS"
    checksum_path.write_text(
        "".join(f"{entry['sha256']}  {entry['file']}\n" for entry in entries),
        encoding="ascii",
        newline="\n",
    )

    manifest = {
        "schema": 1,
        "project": args.project,
        "version": args.version,
        "source": {"path": source.as_posix(), "sha256": source_hash},
        "documentation_tools_ref": args.tool_ref,
        "assets": entries,
        "checksums": checksum_path.name,
    }
    manifest_path = output_dir / "documentation-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"Generated {checksum_path}")
    print(f"Generated {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
