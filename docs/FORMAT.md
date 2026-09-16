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
## API Reference
## ARexx Reference
## Troubleshooting
## License and Support
```

Sections that do not apply may be omitted. `ARexx Reference` is recommended for Amiga software exposing an ARexx port.

## M2 supported subset for AmigaGuide

- level-1 title (`#`);
- level-2 sections (`##`), converted to deterministic AmigaGuide nodes;
- level-3 headings, rendered as prominent subsection text;
- paragraphs and list text;
- fenced code blocks, preserved as preformatted text;
- simple inline Markdown emphasis/code converted to readable plain text;
- Markdown links to level-2 headings, for example `[Commands](#command-reference)`, converted to native AmigaGuide links;
- Latin-1 output with unsupported Unicode characters replaced rather than emitting an invalid legacy text stream.

Generated node names use ASCII letters, digits and underscores. Duplicate section names receive deterministic numeric suffixes. Literal `@` characters are escaped as `@@` so ordinary documentation text cannot accidentally become an AmigaGuide command.

## Command reference convention

Use one level-3 heading per user-visible command beneath `## Command Reference`. The heading is the command name. Follow it with a short purpose statement, then stable labels where applicable:

```markdown
### STATUS

Show current connection status.

Syntax: `STATUS [VERBOSE]`

Arguments: `VERBOSE` includes extended state.

Returns: exit code 0 on success.

Example:

```
STATUS VERBOSE
```
```

Keep syntax machine-like and examples in fenced code blocks. Document defaults, side effects and error/return behavior when relevant.

## API reference convention

Use `## API Reference` for a public programming interface. Use one level-3 heading per public function, method, message, command ID or entry point. Prefer these labels where they apply: `Prototype`, `Parameters`, `Returns`, `Errors`, `Since`, and `Example`.

Do not duplicate private implementation details in the user manual. A project may keep a separate developer/API Markdown document when the public API is large; Markdown remains canonical and the same conventions apply.

## ARexx reference convention

Use `## ARexx Reference` for applications exposing an ARexx port. Begin the section with the exact port name and availability/lifecycle rules. Use one level-3 heading per ARexx command.

Recommended entry form:

```markdown
### GETSTATUS

Query current application status.

Command: `GETSTATUS [STEM name]`

Arguments: optional `STEM` receives structured values.

Result: `RESULT` contains the primary textual result.

RC: `0` success; non-zero values are documented below.

Example:

```
ADDRESS MYAPP 'GETSTATUS'
SAY RESULT
```
```

Document `RC`, `RESULT`, stem variables, quoting rules, command availability and asynchronous behavior explicitly. Command names and port names should be written exactly as implemented.

## Cross references

Prefer links to level-2 sections because those map directly to AmigaGuide nodes:

```markdown
See [ARexx Reference](#arexx-reference).
```

External web links remain readable labels in AmigaGuide but are not converted into native browser actions. The PDF/GitHub forms may retain their normal Markdown hyperlink behavior.

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
