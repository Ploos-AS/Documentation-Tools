# Documentation-Tools

Shared documentation toolchain for Ploos-AS projects.

Markdown is the canonical source. Documentation-Tools turns it into release-ready documentation without requiring a second editable document format.

## Outputs

- **PDF** — primary user manual for modern systems and release distribution.
- **AmigaGuide (`.guide`)** — native hypertext manual for Amiga software.
- **Standalone HTML (`.html`)** — optional portable browser-readable manual generated from the same Markdown source.

DOCX is deliberately not part of the baseline toolchain. Additional formats should only be added when a concrete consumer requires them.

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

Build optional standalone HTML:

```sh
tools/build-html.sh examples/ExampleAmigaManual.md dist/ExampleAmiga-User-Manual.html ExampleAmiga 1.0.0
```

The reusable action always builds PDF and can additionally build AmigaGuide with `amiga: 'true'` and standalone HTML with `html: 'true'`.

See [docs/FORMAT.md](docs/FORMAT.md), [docs/CONSUMER_INTEGRATION.md](docs/CONSUMER_INTEGRATION.md), and [ROADMAP.md](ROADMAP.md).

## Status

- **M0 — Foundation — PASS**
- **M1 — PDF quality — PASS**
- **M2 — AmigaGuide quality — AmigaOS navigation qualification pending**
- **M3 — Consumer integration — PASS**
- **M4 — Documentation QA — PASS**
- **M5 — Extended formats — HTML PASS**
