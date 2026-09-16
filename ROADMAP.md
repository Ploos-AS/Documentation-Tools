# Roadmap

## M0 — Foundation

- [x] Define Markdown as canonical source.
- [x] Define PDF as the primary distributed manual.
- [x] Define AmigaGuide as the native Amiga manual format.
- [x] Add generic and Amiga manual templates.
- [x] Add source validator.
- [x] Add initial PDF build wrapper.
- [x] Add initial Markdown-to-AmigaGuide generator.
- [x] Add example documentation.
- [x] Add CI smoke tests.

## M1 — PDF quality

- Reproducible PDF container/toolchain.
- Ploos-AS title page and typography.
- Automatic metadata/version injection.
- Table of contents, headers/footers and page numbering.
- Link and image handling.
- PDF qualification fixtures.

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
