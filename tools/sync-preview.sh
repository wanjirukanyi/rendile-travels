#!/bin/sh
# Mirror the live source into the persistent, sandbox-readable preview copy.
# The preview server (sandboxed) cannot read ~/Documents (macOS TCC), so it
# serves this copy instead. Run this after editing the site, then refresh
# http://localhost:4321/. Uses rsync so only changed files are copied.
SRC="/Users/maureenkanyi/Documents/oaks/rendile-travels/"
DST="/Users/maureenkanyi/.rendile-preview/"
mkdir -p "$DST"
rsync -a --delete --exclude '.git' --exclude 'tools' "$SRC" "$DST"
echo "Synced site -> $DST"
