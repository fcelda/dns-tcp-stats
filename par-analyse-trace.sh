#!/bin/sh

script="$1"
outdir="$2"
trace="$3"

result=$(basename "$trace")
result="$outdir/${result%txt}json"

[ -z "$script" -o -z "$outdir" -o -z "$trace" ] && exit 1

set -x
"$script" "$trace" > "$result"
