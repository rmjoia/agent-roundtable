#!/usr/bin/env bash
# Fails if tracked content (and, with --history, every commit) holds identifiers that
# must never be published: GUIDs, e-mail addresses, tokens, private keys, plus any
# patterns listed in .scrub-patterns.local (git-ignored, one extended regex per line;
# put the names of private source projects, people and domains there).
#
# Usage: scripts/scrub-check.sh [--history]
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

PATTERNS=(
  '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'AKIA[0-9A-Z]{16}'
  'gh[pousr]_[A-Za-z0-9]{36}'
  'github_pat_[A-Za-z0-9_]{50,}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  'sk-(ant-)?[A-Za-z0-9_-]{32,}'
)
# Addresses that are fine to publish.
ALLOW='noreply@anthropic\.com|@example\.(com|org)|user@host|git@github\.com'

if [ -f .scrub-patterns.local ]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    PATTERNS+=("$line")
  done < .scrub-patterns.local
fi

joined="$(IFS='|'; echo "${PATTERNS[*]}")"
found=0

hits="$(git grep -n -I -i -E -- "$joined" -- . ':!scripts/scrub-check.sh' ':!templates/hooks/pre-commit' | grep -v -i -E "$ALLOW" || true)"
if [ -n "$hits" ]; then
  echo "✗ Tracked files:"; echo "$hits" | cut -c1-160; found=1
fi

if [ "${1:-}" = "--history" ]; then
  hist="$(git log -p --all --format='commit %H%n%B' | grep -i -E -- "$joined" | grep -v -i -E "$ALLOW" | grep -v -E '^\+?(SCAN_PATTERNS=|  .\[0-9a-fA-F\]|  .AKIA|  .gh\[|  .github_pat|  .xox|  .sk-|  .-----BEGIN|  .\[A-Za-z0-9\._%)' || true)"
  if [ -n "$hist" ]; then
    echo "✗ History (content or messages):"; echo "$hist" | cut -c1-160; found=1
  fi
fi

if [ "$found" -eq 0 ]; then echo "✓ Scrub check clean"; else exit 1; fi
