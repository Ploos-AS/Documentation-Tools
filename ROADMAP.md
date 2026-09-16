# Roadmap

## M0 — Foundation — PASS

- [x] Define Markdown as canonical source.
- [x] Define PDF as the primary distributed manual.
- [x] Define AmigaGuide as the native Amiga manual format.
- [x] Add generic and Amiga manual templates.
- [x] Add source validator.
- [x] Add initial PDF build wrapper.
- [x] Add initial Markdown-to-AmigaGuide generator.
- [x] Add example documentation.
- [x] Add CI smoke tests.

## M1 — PDF quality — qualification pending

- [x] Ploos-AS title page and typography baseline.
- [x] Project/version metadata injection.
- [x] Table of contents and numbered sections.
- [x] Headers, footers and page numbering.
- [x] A4 release-manual defaults.
- [x] PDF qualification fixture in GitHub Actions.
- [ ] Pin/encapsulate the complete PDF toolchain for byte-level reproducibility.
- [ ] Rich image handling qualification.

The remaining reproducibility and richer media work is intentionally carried forward rather than blocking the useful M1 layout baseline.

## M2 — AmigaGuide quality

- Richer node generation and navigation.
- Explicit links and cross references.
- Command/API/ARexx reference conventions.
- AmigaGuide escaping and charset policy.
- Native AmigaGuide validation/qualification.

## M3 — Consumer integration

- Reusable GitHub Actions workflow/action.
- Version-pinned consumption by Ploos-AS repositories.
- Release asset naming convention.
- Automatic PDF and `.guide` attachment to tagged releases.

## M4 — Documentation QA

- Broken-link checking.
- Required-section policies by project type.
- Spell/style checks where appropriate.
- Reproducibility checks.
- Release manifest/checksums.

## M5 — Extended formats

Optional outputs only when a concrete consumer needs them, for example HTML. DOCX is not a baseline target.
