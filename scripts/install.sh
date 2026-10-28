#!/usr/bin/env bash
# Copies the agent-roundtable framework into an existing project, without overwriting.
# Also copies adapters/ and prompts/ so other assistants can read them locally.
# Usage: scripts/install.sh <path-to-your-project> [--into-root]
#   default: framework folders go to <project>/.roundtable/, commands to <project>/.claude/commands/
#   --into-root: framework folders go to the project root (roles/, themes/, templates/, packs/)
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:?usage: scripts/install.sh <project> [--into-root]}"
[ -d "$DEST/.git" ] || { echo "✗ $DEST is not a git repository"; exit 1; }
TARGET="$DEST/.roundtable"; [ "${2:-}" = "--into-root" ] && TARGET="$DEST"

mkdir -p "$TARGET" "$DEST/.claude/commands"
for d in roles themes templates packs adapters prompts; do
  if [ -e "$TARGET/$d" ] && [ "$TARGET" = "$DEST" ]; then
    echo "✗ $TARGET/$d already exists; use the default .roundtable/ location"; exit 1
  fi
  rm -rf "${TARGET:?}/$d.tmp"; cp -R "$SRC/$d" "$TARGET/$d.tmp"
  [ -d "$TARGET/$d/local" ] && cp -R "$TARGET/$d/local" "$TARGET/$d.tmp/" 2>/dev/null || true
  rm -rf "${TARGET:?}/$d"; mv "$TARGET/$d.tmp" "$TARGET/$d"
done
cp "$SRC/VERSION" "$SRC/team.config.schema.yaml" "$SRC/team.config.example.yaml" "$TARGET/"
mkdir -p "$TARGET/scripts" && cp "$SRC/scripts/render.py" "$TARGET/scripts/render.py"
for c in init-team sync-team self-review; do
  if [ -e "$DEST/.claude/commands/$c.md" ] && ! cmp -s "$SRC/.claude/commands/$c.md" "$DEST/.claude/commands/$c.md"; then
    echo "… $DEST/.claude/commands/$c.md exists and differs; kept yours, wrote $c.md.roundtable"
    cp "$SRC/.claude/commands/$c.md" "$DEST/.claude/commands/$c.md.roundtable"
  else
    cp "$SRC/.claude/commands/$c.md" "$DEST/.claude/commands/$c.md"
  fi
done
echo "✓ agent-roundtable $(cat "$SRC/VERSION") copied into $TARGET"
echo "Next: open Claude Code in $DEST and run /init-team"
