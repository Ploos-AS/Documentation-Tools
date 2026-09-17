# Consumer integration

Ploos-AS repositories can consume Documentation-Tools either as a version-pinned reusable GitHub Actions workflow or as the lower-level composite action.

## Recommended: reusable workflow

The reusable workflow is the simplest consumer interface because it installs the PDF dependencies, builds the requested formats and uploads the result as a GitHub Actions artifact.

```yaml
name: Documentation

on:
  push:
  workflow_dispatch:

jobs:
  docs:
    uses: Ploos-AS/Documentation-Tools/.github/workflows/build-docs.yml@<pinned-ref>
    with:
      source: docs/USER_MANUAL.md
      project: ExampleProject
      version: 1.0.0
```

For an Amiga project:

```yaml
jobs:
  docs:
    uses: Ploos-AS/Documentation-Tools/.github/workflows/build-docs.yml@<pinned-ref>
    with:
      source: docs/USER_MANUAL.md
      project: AmiExample
      version: 1.0.0
      amiga: true
      artifact-name: AmiExample-documentation
```

The workflow preserves the caller's Documentation-Tools ref when it checks out the tool repository, so a consumer pinned to a release tag or commit SHA builds with that same revision.

The default artifact contains:

- `<Project>-<version>-User-Manual.pdf`
- `<Project>-<version>.guide` when `amiga: true`

## Release asset publishing

`release-docs.yml` builds the documentation and uploads the PDF and optional AmigaGuide directly to an existing GitHub release. The caller must grant `contents: write` permission.

```yaml
name: Release documentation

on:
  release:
    types: [published]

permissions:
  contents: write

jobs:
  docs:
    uses: Ploos-AS/Documentation-Tools/.github/workflows/release-docs.yml@<pinned-ref>
    with:
      source: docs/USER_MANUAL.md
      project: AmiExample
      version: ${{ github.event.release.tag_name }}
      amiga: true
      tag: ${{ github.event.release.tag_name }}
```

The target release must already exist. Existing documentation assets with the same filenames are replaced, making a rerun idempotent. Other project release assets such as `.lha`, `.readme` and checksums are left untouched.

## Lower-level composite action

Use the composite action when the consumer needs control over dependency installation, artifact handling or integration into a larger job.

### Consumer prerequisites

The runner must provide Python 3, Pandoc and a LaTeX engine (`pdflatex`). On `ubuntu-latest`, install the PDF dependencies before invoking the action:

```yaml
- name: Install documentation dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y pandoc texlive-latex-base texlive-latex-recommended texlive-latex-extra
```

### Generic project

```yaml
- uses: Ploos-AS/Documentation-Tools@<pinned-ref>
  with:
    source: docs/USER_MANUAL.md
    project: ExampleProject
    version: 1.0.0
```

This produces:

- `dist/ExampleProject-1.0.0-User-Manual.pdf`

### Amiga project

```yaml
- uses: Ploos-AS/Documentation-Tools@<pinned-ref>
  with:
    source: docs/USER_MANUAL.md
    project: AmiExample
    version: 1.0.0
    amiga: 'true'
```

This produces and validates:

- `dist/AmiExample-1.0.0-User-Manual.pdf`
- `dist/AmiExample-1.0.0.guide`

## Pinning policy

Consumer repositories should use a release tag or immutable commit SHA. Do not consume `main` in release workflows. A major-version convenience tag may be introduced after the first stable Documentation-Tools release, but immutable pins remain preferred for reproducible releases.
