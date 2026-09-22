#!/usr/bin/env python3
"""Dependency-free Markdown -> AmigaGuide converter."""

from pathlib import Path
import re
import sys


def literal_text(text: str) -> str:
    """Return literal text that is safe in the generated V34-compatible subset."""
    if "@{" in text:
        raise ValueError("literal '@{' is not supported by AmigaGuide 34.x")
    return text


def body_text(text: str) -> str:
    """Keep body text from being parsed as a line-oriented AmigaGuide command."""
    text = literal_text(text)
    return f" {text}" if text.startswith("@") else text


def strip_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text


def slug(title: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", strip_inline(title)).strip("_")
    return value or "Section"


def unique_node(title: str, used: set[str]) -> str:
    base = slug(title)
    name = base
    number = 2
    while name.lower() in used:
        name = f"{base}_{number}"
        number += 1
    used.add(name.lower())
    return name


def inline(text: str, anchors: dict[str, str]) -> str:
    text = strip_inline(text)

    def link(match: re.Match[str]) -> tuple[str, bool]:
        label, target = match.group(1), match.group(2)
        if target.startswith("#"):
            key = target[1:].lower()
            node = anchors.get(key)
            if node:
                return f'@{{"{literal_text(label)}" link {node}}}', True
        return literal_text(label), False

    parts: list[str] = []
    pos = 0
    first_part_is_generated = False
    for match in re.finditer(r"\[([^]]+)\]\(([^)]+)\)", text):
        literal = literal_text(text[pos:match.start()])
        if literal:
            parts.append(literal)
        rendered_link, generated = link(match)
        if not parts:
            first_part_is_generated = generated
        parts.append(rendered_link)
        pos = match.end()
    parts.append(literal_text(text[pos:]))
    rendered = "".join(parts)
    if rendered.startswith("@") and not first_part_is_generated:
        rendered = f" {rendered}"
    return rendered


def convert(text: str) -> str:
    lines = text.splitlines()
    title = "User Manual"
    raw_sections: list[tuple[str, list[str]]] = []
    current_title = "Introduction"
    current: list[str] = []
    in_code = False

    for line in lines:
        if line.startswith("# ") and not in_code:
            title = strip_inline(line[2:].strip())
            continue
        if line.startswith("## ") and not in_code:
            if current or raw_sections:
                raw_sections.append((current_title, current))
            current_title = strip_inline(line[3:].strip())
            current = []
            continue
        if line.startswith("```"):
            in_code = not in_code
            continue
        current.append(line)

    if current or not raw_sections:
        raw_sections.append((current_title, current))

    used = {"main"}
    sections = [(unique_node(name, used), name, body) for name, body in raw_sections]
    anchors: dict[str, str] = {}
    for ident, name, _ in sections:
        anchors[slug(name).lower()] = ident
        anchors[re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")] = ident

    safe_title = literal_text(title)
    out = [
        f'@database "{safe_title}"',
        f'@node Main "{safe_title}"',
        body_text(title),
        "",
    ]
    for ident, name, _ in sections:
        out.append(f'@{{"{literal_text(name)}" link {ident}}}')
    out.extend(["", "@endnode", ""])

    for index, (ident, name, body) in enumerate(sections):
        out.append(f'@node {ident} "{literal_text(name)}"')
        nav = []
        if index > 0:
            nav.append(f'@{{"Prev" link {sections[index - 1][0]}}}')
        nav.append('@{"Contents" link Main}')
        if index + 1 < len(sections):
            nav.append(f'@{{"Next" link {sections[index + 1][0]}}}')
        out.extend(["  ".join(nav), "", body_text(name), ""])

        code = False
        for line in body:
            if line.startswith("```"):
                code = not code
                continue
            if line.startswith("### ") and not code:
                out.extend(["", body_text(strip_inline(line[4:].strip()).upper()), ""])
            elif code:
                out.append(body_text(line))
            else:
                out.append(inline(line, anchors))
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
