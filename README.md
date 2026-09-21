# Documentation-Tools

Shared documentation toolchain for Ploos-AS projects.

Markdown is the canonical source. Documentation-Tools turns it into release-ready documentation without requiring a second editable document format.

## Ploos-AS documentation licensing standard

Original Ploos-AS documentation, course material, tutorials, exercises, illustrations, and other educational content should use **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** by default, unless inherited or third-party licensing requires otherwise.

This complements the wider Ploos-AS licensing standard:

- software, ROM and firmware: MIT by default;
- hardware, PCB designs and HDL/gateware: CERN-OHL-P-2.0;
- documentation and educational material: CC BY-SA 4.0;
- inherited/third-party material: retain and comply with the applicable licence.

Mixed repositories should clearly identify which licence applies to each component or directory.

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

Prepare the redistributable Work volume for the human-visible M2 AmigaOS gate:

```sh
python3 tools/prepare-m2-native-qualification.py --amiga-runtime ../amiga-runtime
```

The complete FS-UAE launch, checklist, evidence-recording procedure, and strict
manual PASS rule are in [docs/M2_NATIVE_QUALIFICATION.md](docs/M2_NATIVE_QUALIFICATION.md).
M2 remains pending until that visible navigation qualification is actually run
and every item passes.

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
