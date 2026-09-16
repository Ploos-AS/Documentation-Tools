# Consumer integration

Ploos-AS repositories can consume Documentation-Tools as a version-pinned composite GitHub Action.

## Consumer prerequisites

The runner must provide Python 3, Pandoc and a LaTeX engine (`pdflatex`). On `ubuntu-latest`, install the PDF dependencies before invoking the action:

```yaml
- name: Install documentation dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y pandoc texlive-latex-base texlive-latex-recommended texlive-latex-extra
```

## Generic project

```yaml
- uses: Ploos-AS/Documentation-Tools@<pinned-ref>
  with:
    source: docs/USER_MANUAL.md
    project: ExampleProject
    version: 1.0.0
```

This produces:

- `dist/ExampleProject-1.0.0-User-Manual.pdf`

## Amiga project

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

## Release publishing

The action builds files only. Consumer release workflows remain responsible for attaching the generated PDF and optional `.guide` to the GitHub release alongside the project's normal release artifacts. A reusable release-publishing workflow is a later M3 item.
