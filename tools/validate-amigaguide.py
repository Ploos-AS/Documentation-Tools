#!/usr/bin/env python3
"""Validate the structural subset of AmigaGuide emitted by Documentation-Tools."""

from pathlib import Path
import re
import sys


def fail(message: str) -> None:
    print(f"AmigaGuide validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: validate-amigaguide.py <manual.guide>", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    data = path.read_bytes()
    if not data:
        fail("file is empty")
    try:
        text = data.decode("latin-1")
    except UnicodeDecodeError:
        fail("file is not Latin-1 compatible")

    lines = text.splitlines()
    if not lines or not lines[0].startswith('@database "'):
        fail("missing @database header")

    nodes: list[str] = []
    depth = 0
    for lineno, line in enumerate(lines, 1):
        if line.startswith("@") and not (
            line.startswith('@database "')
            or line.startswith("@node ")
            or line == "@endnode"
            or line.startswith('@{"')
        ):
            fail(f"unsupported command-looking line {lineno}: {line}")
        match = re.match(r"^@node\s+(\S+)\s+", line)
        if match:
            if depth:
                fail("nested @node")
            nodes.append(match.group(1))
            depth = 1
        elif line == "@endnode":
            if not depth:
                fail("orphan @endnode")
            depth = 0
    if depth:
        fail("unterminated node")
    if not nodes or nodes[0] != "Main":
        fail("first node must be Main")
    if len(nodes) != len(set(name.lower() for name in nodes)):
        fail("duplicate node names")

    known = {name.lower() for name in nodes}
    for target in re.findall(r'@\{"[^"]*"\s+link\s+(\S+)\}', text):
        if target.lower() not in known:
            fail(f"link targets missing node: {target}")

    print(f"AmigaGuide validation passed: {len(nodes)} nodes")


if __name__ == "__main__":
    main()
