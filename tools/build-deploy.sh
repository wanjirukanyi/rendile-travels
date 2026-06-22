#!/bin/sh
# Build the deploy artifact (rendile-travels-site.zip) for Cloudflare Pages or any
# static host. Zips ONLY the public site — exclusions are baked in here so they can't
# be forgotten:
#   tools/                 internal helper scripts (this folder)
#   README.md , STATUS.md  internal project notes
#   assets/Layer 1 (2).png hi-res logo source (kept on disk, never deployed)
#   *.zip                  never nest the artifact inside itself
#   .git/ , *.DS_Store , __MACOSX/  vcs + macOS junk
# Usage: sh rendile-travels/tools/build-deploy.sh
set -e
SITE="/Users/maureenkanyi/Documents/oaks/rendile-travels"
OUT="$SITE/rendile-travels-site.zip"
cd "$SITE"
rm -f "$OUT"
zip -r -X "$OUT" . \
  -x 'tools/*' \
  -x 'README.md' \
  -x 'STATUS.md' \
  -x 'assets/Layer 1 (2).png' \
  -x '*.zip' \
  -x '.git/*' \
  -x '*.DS_Store' \
  -x '__MACOSX/*' >/dev/null
echo "Built: $OUT  ($(du -h "$OUT" | cut -f1))"
echo "Top-level entries:"
unzip -Z1 "$OUT" | sed 's#/.*##' | sort -u
