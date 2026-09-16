#!/usr/bin/env python3
"""Small dependency-free Markdown -> AmigaGuide converter for M0."""

from pathlib import Path
import re
import sys


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    return text.replace("@", "@@")


def node_name(title: str, used: set[str]) -> str:
    base = re.sub(r"[^A-Za-z0-9_]", "_", title).strip("_") or "Section"
    name = base
    number = 2
    while name.lower() in used:
        name = f"{base}_{number}"
        number += 1
    used.add(name.lower())
    return name


def convert(text: str) -> str:
    lines = text.splitlines()
    title = "User Manual"
    sections: list[tuple[str, list[str]]] = []
    current_title = "Introduction"
    current: list[str] = []
    in_code = False

    for line in lines:
        if line.startswith("# "):
            title = clean_inline(line[2:].strip())
            continue
        if line.startswith("## ") and not in_code:
            if current or sections:
                sections.append((current_title, current))
            current_title = clean_inline(line[3:].strip())
            current = []
            continue
        if line.startswith("```"):
            in_code = not in_code
            continue
        if line.startswith("### ") and not in_code:
            current.extend(["", clean_inline(line[4:].strip()).upper(), ""])
        else:
            current.append(line if in_code else clean_inline(line))

    if current or not sections:
        sections.append((current_title, current))

    used = {"main"}
    nodes = [(node_name(name, used), name, body) for name, body in sections]

    out = [f'@database "{title}"', f'@node Main "{title}"', title, ""]
    for ident, name, _ in nodes:
        out.append(f'@{{"{name}" link {ident}}}')
    out.extend(["", "@endnode", ""])

    for index, (ident, name, body) in enumerate(nodes):
        out.append(f'@node {ident} "{name}"')
        nav = []
        if index > 0:
            nav.append(f'@{{"Prev" link {nodes[index - 1][0]}}}')
        nav.append('@{"Contents" link Main}')
        if index + 1 < len(nodes):
            nav.append(f'@{{"Next" link {nodes[index + 1][0]}}}')
        out.extend(["  ".join(nav), "", name, ""])
        out.extend(body)
        out.extend(["", "@endnode", ""])

    return "\n".join(out)


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: build-amigaguide.py <manual.md> <output.guide>", file=sys.stderr)
        raise SystemExit(2)
    src, dst = map(Path, sys.argv[1:])
    text = src.read_text(encoding="utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(convert(text), encoding="latin-1", errors="replace", newline="\n")
    print(f"Built {dst}")


if __name__ == "__main__":
    main()
