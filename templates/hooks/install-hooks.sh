#!/usr/bin/env bash
# agent-roundtable:generated template=install-hooks version={{template.version}}
# Points git at the version-controlled hooks. Run once after cloning.
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
chmod +x "$REPO_ROOT"/scripts/git-hooks/*
git -C "$REPO_ROOT" config core.hooksPath scripts/git-hooks
echo "Git hooks installed (core.hooksPath=scripts/git-hooks)."
