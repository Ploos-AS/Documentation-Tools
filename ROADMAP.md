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

## M1 — PDF quality — PASS

- [x] Ploos-AS title page and typography baseline.
- [x] Project/version metadata injection.
- [x] Table of contents and numbered sections.
- [x] Headers, footers and page numbering.
- [x] A4 release-manual defaults.
- [x] PDF qualification fixture in GitHub Actions.
- [x] Deterministic PDF builds under the reproducible-build environment used by CI/release workflows.
- [x] Rich image handling qualification with local asset validation and PDF rendering coverage.

M1 is fully qualified in GitHub Actions, including deterministic PDF generation and local rich-image assets. The same image fixture also exercises HTML rendering and readable AmigaGuide alternative-text fallback.

## M2 — AmigaGuide quality — PASS

- [x] Richer deterministic node generation and navigation.
- [x] Internal Markdown links and cross references.
- [x] Command/API/ARexx reference conventions.
- [x] AmigaGuide escaping and Latin-1 charset policy in the generator.
- [x] Dependency-free structural AmigaGuide validator.
- [x] GitHub Actions structural qualification.
- [x] Automated native AROS MultiView compatibility gate.
- [x] Visible AmigaOS 2.04+ navigation qualification.

The AROS gate provides automated, non-proprietary native compatibility coverage on GitHub Actions. The final visible gate passed on FS-UAE 3.2.35 with an A500+/68000 profile, Kickstart 2.04 revision 37.175, and AmigaGuide 34.3. All 13 checks passed for Documentation-Tools source revision `21865b1e4286b3bb96b7b7c0c6ac63a7b7002957` and guide SHA-256 `383756b99bd63a170bfdde90287a269bb0a007f2a67054f44d08a0b6d7acd8f6`. The repeatable procedure and evidence policy remain defined in `docs/M2_NATIVE_QUALIFICATION.md`.

## M3 — Consumer integration — PASS

- [x] Reusable GitHub Actions workflow/action.
- [x] Version-pinned consumption by Ploos-AS repositories.
- [x] Release asset naming convention.
- [x] Automatic PDF and `.guide` attachment to tagged releases.
- [x] Safe dry-run qualification of the reusable release workflow.
- [x] Live release-publishing qualification using a temporary prerelease, real asset upload/verification, and automatic cleanup.
- [x] Cross-repository qualification from Ploos-AS/AmiNTP using immutable Documentation-Tools commit `dc1434cd349b2681e4095ce45887d93fcbdbdb63`.

The reusable build and release workflows are qualified, including a real GitHub release upload path and an independent Ploos-AS consumer repository pinned to an immutable Documentation-Tools revision.

## M4 — Documentation QA — PASS

- [x] Broken-link checking.
- [x] Required-section policies by project type.
- [x] Deterministic spell/style checks appropriate for technical documentation.
- [x] Byte-for-byte PDF and AmigaGuide reproducibility checks.
- [x] Release manifest and SHA-256 checksums.

M4 is qualified in GitHub Actions. Release documentation now includes deterministic integrity metadata in addition to the generated manuals.

## M5 — Extended formats — HTML PASS

- [x] Add optional standalone HTML generation from canonical Markdown.
- [x] Expose HTML as an opt-in reusable-action output.
- [x] Qualify standalone HTML structure, TOC, metadata, filename, and reusable-action integration in GitHub Actions.
- [ ] Add further formats only when a concrete consumer requires them.

HTML is a supported optional output. PDF remains the primary distributed manual, and AmigaGuide remains the native Amiga format. DOCX is not a baseline target.
