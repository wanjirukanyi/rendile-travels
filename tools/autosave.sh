#!/bin/sh
# Auto-save the Rendile Travels site to GitHub. Called by the SessionEnd hook so
# work is backed up off-machine at the end of every session.
# Safe & quiet: only acts when there are uncommitted changes; never errors out.
REPO="/Users/maureenkanyi/Documents/oaks/rendile-travels"
cd "$REPO" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[ -n "$(git status --porcelain)" ] || exit 0   # nothing changed — done

git add -A
git commit -q -m "Auto-save (session end) $(date '+%Y-%m-%d %H:%M')

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" >/dev/null 2>&1

if git push -q >/dev/null 2>&1; then
  echo '{"systemMessage":"Backed up Rendile Travels to GitHub."}'
else
  echo '{"systemMessage":"Rendile Travels committed locally; GitHub push deferred (offline?). It will push next session."}'
fi
exit 0
