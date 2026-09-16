# Documentation source format

Documentation-Tools uses ordinary Markdown as its canonical input.

## Design rules

1. The Markdown file must remain useful when read directly on GitHub.
2. PDF and AmigaGuide are generated artifacts, not independently edited sources.
3. A manual should not depend on DOCX-specific formatting.
4. Amiga manuals should use a conservative Markdown subset so the same source maps cleanly to AmigaGuide.

## Recommended structure

```markdown
# Project User Manual

Version: 1.0.0

## Introduction
## Requirements
## Installation
## Quick Start
## Usage
## Configuration
## Command Reference
## ARexx Reference
## Troubleshooting
## License and Support
```

Sections that do not apply may be omitted. `ARexx Reference` is recommended for Amiga software exposing an ARexx port.

## M0 supported subset for AmigaGuide

- level-1 title (`#`);
- level-2 sections (`##`), converted to AmigaGuide nodes;
- level-3 headings, rendered as emphasized section text;
- paragraphs;
- unordered and ordered list text;
- fenced code blocks, preserved as preformatted text;
- simple inline Markdown emphasis/code is stripped to readable plain text.

The M0 converter intentionally favors predictable output over complete Markdown compatibility. Rich links, images, tables, nested formatting and explicit cross references are M1/M2 work.

## File naming

Recommended source:

```text
docs/USER_MANUAL.md
```

Recommended release assets:

```text
<Project>-<version>-User-Manual.pdf
<Project>-<version>.guide
```

Only Amiga software needs the `.guide` artifact.
