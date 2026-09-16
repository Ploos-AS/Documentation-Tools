#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
    echo "usage: build-pdf.sh <manual.md> <output.pdf>" >&2
    exit 2
fi

src=$1
out=$2

command -v pandoc >/dev/null 2>&1 || {
    echo "ERROR: pandoc is required" >&2
    exit 1
}

mkdir -p "$(dirname "$out")"

# Keep M0 deliberately simple. M1 will pin the complete PDF toolchain and style.
pandoc "$src" \
    --standalone \
    --toc \
    --metadata documentclass=article \
    -o "$out"

echo "Built $out"
