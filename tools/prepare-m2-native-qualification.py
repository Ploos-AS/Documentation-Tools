#!/usr/bin/env python3
"""Build the redistributable bundle for the visible M2 AmigaOS gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


SCHEMA = "ploos-as.documentation-tools.m2-native-qualification.v1"
PROFILE = "a500plus"
CHECKS = (
    ("guide_opens", "Guide opens without a parser or requester error"),
    ("main_node", "Main node renders with generated section links"),
    ("first_section", "First section link from Main works"),
    ("middle_section", "A middle section link from Main works"),
    ("last_section", "Last section link from Main works"),
    ("prev", "Prev navigation works where present"),
    ("contents", "Contents navigation returns to Main"),
    ("next", "Next navigation works where present"),
    ("internal_cross_reference", "An internal cross-reference works"),
    ("preformatted_text", "Preformatted and code text renders correctly"),
    ("literal_at", "Literal @ text renders without command interpretation"),
    ("node_names_labels", "Node names and navigation labels are valid"),
    ("viewer_closes", "Viewer closes normally"),
)


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha(repository: Path) -> str:
    return run("git", "rev-parse", "HEAD", cwd=repository)


def require_clean(repository: Path, name: str) -> None:
    if run("git", "status", "--porcelain", "--untracked-files=no", cwd=repository):
        raise SystemExit(
            f"{name} has uncommitted tracked changes; commit them before qualification"
        )


def check_runtime(runtime: Path) -> Path:
    required = (
        runtime / "bin/amiga-runtime",
        runtime / "backends/fs-uae/backend",
        runtime / f"profiles/{PROFILE}.conf",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("amiga-runtime checkout is incomplete: " + ", ".join(missing))
    values = {}
    profile = required[-1]
    for raw in profile.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    if values.get("cpu") != "68000":
        raise SystemExit(f"{profile} is not a 68000 profile")
    return profile


def write_checklist(path: Path, metadata: dict[str, object]) -> None:
    lines = [
        "# M2 visible AmigaOS qualification checklist",
        "",
        "This file is a PENDING template. Record the result only after a visible",
        "FS-UAE session using AmigaOS 2.04 or later and a native guide viewer.",
        "",
        f"- Documentation-Tools commit: `{metadata['documentation_tools_commit']}`",
        f"- amiga-runtime commit: `{metadata['amiga_runtime_commit']}`",
        f"- ExampleAmiga.guide SHA-256: `{metadata['guide_sha256']}`",
        f"- amiga-runtime profile: `{PROFILE}` (68000)",
        "- Emulator/version: PENDING",
        "- AmigaOS version: PENDING",
        "- Viewer: PENDING",
        "- Date: PENDING",
        "",
        "## Checks",
        "",
    ]
    lines.extend(f"- [ ] PENDING — {label} (`{ident}`)" for ident, label in CHECKS)
    lines.extend(
        [
            "",
            "Use `tools/record-m2-native-qualification.py` on the host to record",
            "the observed PASS/FAIL values in `qualification-result.json`.",
            "A generated bundle never changes the M2 milestone status.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=Path("examples/ExampleAmigaManual.md")
    )
    parser.add_argument(
        "--output", type=Path, default=Path("dist/m2-native-qualification/Work")
    )
    parser.add_argument("--amiga-runtime", type=Path, default=Path("../amiga-runtime"))
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    source = (root / args.source).resolve() if not args.source.is_absolute() else args.source
    output = (root / args.output).resolve() if not args.output.is_absolute() else args.output
    runtime = args.amiga_runtime.resolve()
    dist = (root / "dist").resolve()
    try:
        output.relative_to(dist)
    except ValueError:
        raise SystemExit("qualification output must be inside Documentation-Tools/dist")
    require_clean(root, "Documentation-Tools")
    require_clean(runtime, "amiga-runtime")
    profile = check_runtime(runtime)
    if not source.is_file():
        raise SystemExit(f"source file not found: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    staging = output.with_name(output.name + ".tmp")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    guide = staging / "ExampleAmiga.guide"
    try:
        run(sys.executable, str(root / "tools/validate-docs.py"), str(source))
        run(sys.executable, str(root / "tools/build-amigaguide.py"), str(source), str(guide))
        run(sys.executable, str(root / "tools/validate-amigaguide.py"), str(guide))

        metadata = {
            "documentation_tools_commit": git_sha(root),
            "amiga_runtime_commit": git_sha(runtime),
            "guide_sha256": sha256(guide),
        }
        result = {
            "schema": SCHEMA,
            "status": "PENDING",
            "gate": "visible-amigaos-navigation",
            "source": {
                "path": "examples/ExampleAmigaManual.md",
                **metadata,
            },
            "runtime": {
                "repository": "Ploos-AS/amiga-runtime",
                "profile": PROFILE,
                "profile_sha256": sha256(profile),
                "emulator": "FS-UAE",
                "emulator_version": "",
                "amiga_os_version": "",
                "viewer": "",
            },
            "qualification": {
                "date": "",
                "results": [
                    {"id": ident, "label": label, "status": "PENDING", "notes": ""}
                    for ident, label in CHECKS
                ],
                "notes": "",
            },
        }
        (staging / "qualification-result.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        write_checklist(staging / "QUALIFICATION-CHECKLIST.md", metadata)
        (staging / "START-HERE.txt").write_text(
            "M2 AmigaGuide visible qualification\n\n"
            "This Work volume contains only redistributable project files.\n"
            "Open ExampleAmiga.guide with the native AmigaGuide viewer or MultiView.\n"
            "Perform every check in QUALIFICATION-CHECKLIST.md visibly.\n"
            "Record results on the host after closing the viewer normally.\n",
            encoding="ascii",
        )
        manifest_files = ("ExampleAmiga.guide", "QUALIFICATION-CHECKLIST.md", "START-HERE.txt")
        (staging / "SHA256SUMS").write_text(
            "".join(f"{sha256(staging / name)}  {name}\n" for name in manifest_files),
            encoding="ascii",
        )
        if output.exists():
            shutil.rmtree(output)
        staging.replace(output)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    print(f"M2 native qualification bundle: {output}")
    print(f"ExampleAmiga.guide SHA-256: {sha256(output / 'ExampleAmiga.guide')}")
    print("Visible AmigaOS qualification status: PENDING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
