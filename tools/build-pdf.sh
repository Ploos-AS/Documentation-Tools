#!/bin/sh
set -eu

usage() {
    echo "usage: build-pdf.sh <manual.md> <output.pdf> [project] [version]" >&2
    exit 2
}

[ "$#" -ge 2 ] && [ "$#" -le 4 ] || usage

src=$1
out=$2
project=${3:-$(basename "$src" .md)}
version=${4:-Unreleased}
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
header="$root/templates/pdf/header.tex"

command -v pandoc >/dev/null 2>&1 || {
    echo "ERROR: pandoc is required" >&2
    exit 1
}

[ -f "$src" ] || { echo "ERROR: source not found: $src" >&2; exit 1; }
[ -f "$header" ] || { echo "ERROR: PDF header not found: $header" >&2; exit 1; }

mkdir -p "$(dirname "$out")"
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT HUP INT TERM

# Escape the small set of TeX-special characters expected in project/version metadata.
escape_tex() {
    printf '%s' "$1" | sed -e 's/\\/\\textbackslash{}/g' -e 's/\([#$%&_{}]\)/\\\1/g'
}

project_tex=$(escape_tex "$project")
version_tex=$(escape_tex "$version")
{
    printf '\\newcommand{\\DocProject}{%s}\n' "$project_tex"
    printf '\\newcommand{\\DocVersion}{%s}\n' "$version_tex"
    cat "$header"
} > "$tmp"

# pdfTeX honours SOURCE_DATE_EPOCH for reproducible creation metadata.
# FORCE_SOURCE_DATE makes that behaviour explicit and UTC removes timezone
# dependence.  Do not pass a fixed -jobname: Pandoc relies on its temporary
# TeX basename to locate the produced PDF.
if [ -n "${SOURCE_DATE_EPOCH:-}" ]; then
    export FORCE_SOURCE_DATE=1
    export TZ=UTC
fi

pandoc "$src" \
    --standalone \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --metadata title= \
    --metadata author= \
    --metadata date= \
    --metadata documentclass=article \
    --variable papersize=a4 \
    --variable geometry:margin=25mm \
    --variable fontsize=11pt \
    --include-in-header="$tmp" \
    -o "$out"

printf 'Built %s (project=%s, version=%s)\n' "$out" "$project" "$version"
