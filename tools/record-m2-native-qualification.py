#!/usr/bin/env python3
"""Interactively record the human-visible M2 AmigaOS qualification."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "result",
        type=Path,
        nargs="?",
        default=Path("dist/m2-native-qualification/Work/qualification-result.json"),
    )
    args = parser.parse_args()
    path = args.result
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") != "PENDING":
        raise SystemExit("refusing to overwrite a completed qualification result")

    guide = path.parent / "ExampleAmiga.guide"
    actual = hashlib.sha256(guide.read_bytes()).hexdigest()
    expected = data["source"]["guide_sha256"]
    if actual != expected:
        raise SystemExit("ExampleAmiga.guide SHA-256 does not match the bundle metadata")

    runtime = data["runtime"]
    runtime["emulator_version"] = prompt("FS-UAE version")
    runtime["amiga_os_version"] = prompt("AmigaOS version")
    runtime["viewer"] = prompt("Native viewer", "MultiView")
    if not all(runtime[key] for key in ("emulator_version", "amiga_os_version", "viewer")):
        raise SystemExit("emulator version, AmigaOS version, and viewer are required")

    qualification = data["qualification"]
    qualification["date"] = prompt("Qualification date", dt.date.today().isoformat())
    try:
        dt.date.fromisoformat(qualification["date"])
    except ValueError:
        raise SystemExit("qualification date must use YYYY-MM-DD")
    any_failure = False
    for check in qualification["results"]:
        while True:
            value = prompt(f"{check['label']} (PASS/FAIL)").upper()
            if value in {"PASS", "FAIL"}:
                break
            print("Enter PASS or FAIL.")
        check["status"] = value
        check["notes"] = prompt("  Notes", "")
        any_failure = any_failure or value == "FAIL"
    qualification["notes"] = prompt("Overall notes", "")
    data["status"] = "FAIL" if any_failure else "PASS"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Visible AmigaOS qualification: {data['status']}")
    print("M2 milestone status was not changed; update it only after reviewing all gates.")
    return 1 if any_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
