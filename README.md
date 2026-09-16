# Documentation-Tools

Shared documentation toolchain for Ploos-AS projects.

Markdown is the canonical source. Documentation-Tools turns it into release-ready documentation without requiring a second editable document format.

## Outputs

- **PDF** — primary user manual for modern systems and release distribution.
- **AmigaGuide (`.guide`)** — native hypertext manual for Amiga software.

DOCX is deliberately not part of the required toolchain.

## M0 scope

M0 establishes:

- repository and format conventions;
- reusable user-manual templates;
- documentation validation;
- Markdown to PDF build support;
- Markdown to AmigaGuide generation;
- a representative Amiga example;
- GitHub Actions smoke tests.

## Quick start

Validate Markdown:

```sh
python3 tools/validate-docs.py examples/ExampleAmigaManual.md
```

Build a PDF (Pandoc plus a PDF engine is required):

```sh
tools/build-pdf.sh examples/ExampleAmigaManual.md dist/ExampleAmiga-User-Manual.pdf
```

Build an AmigaGuide:

```sh
python3 tools/build-amigaguide.py examples/ExampleAmigaManual.md dist/ExampleAmiga.guide
```

See [docs/FORMAT.md](docs/FORMAT.md) for the source contract and [ROADMAP.md](ROADMAP.md) for planned milestones.

## Status

**M0 — foundation**
