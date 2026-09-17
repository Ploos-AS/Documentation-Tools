#!/bin/sh
set -eu

if [ "$#" -lt 2 ] || [ "$#" -gt 4 ]; then
    echo "usage: $0 <manual.md> <output.html> [project] [version]" >&2
    exit 2
fi

source=$1
output=$2
project=${3:-$(basename "$source" .md)}
version=${4:-Unreleased}

command -v pandoc >/dev/null 2>&1 || {
    echo "pandoc is required" >&2
    exit 1
}

[ -s "$source" ] || {
    echo "source not found or empty: $source" >&2
    exit 1
}

mkdir -p "$(dirname "$output")"

pandoc "$source" \
    --standalone \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --metadata "title=$project User Manual" \
    --metadata "subtitle=Version $version" \
    --metadata "generator=Documentation-Tools" \
    -o "$output"

test -s "$output"
