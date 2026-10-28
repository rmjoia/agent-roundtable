---
description: Pull agent-roundtable template updates into this project and re-render the team from team.config.yaml, keeping theme names, local lanes and local persona sections. Shows a diff before writing.
argument-hint: "[<tag-or-branch>] [--non-interactive]"
---

# /sync-team

You update this project's agent team to a newer version of the agent-roundtable template. Generated files are re-rendered from the new role templates plus this project's `team.config.yaml`, so theme names, lanes and `agent-roundtable:local` blocks survive. You never commit, push or open PRs yourself; in CI the calling workflow does that.

Arguments: `$ARGUMENTS`. An optional tag or branch (default: the latest release tag, else `main`). `--non-interactive`: no questions; take defaults for new config fields and write without the approval step.

## Step 1: Where we are
1. Read `team.config.yaml`. Stop if it is missing: run `/init-team` first.
2. Find the framework folder (repo root if `roles/architect.md` is there, else `.roundtable/`). Read its `VERSION`: the current version.
3. Upstream is `template.repo` (default `rmjoia/agent-roundtable`).

## Step 2: Fetch upstream
Clone into your scratchpad, never into the repo:
`git clone --depth 1 --branch <ref> https://github.com/<template.repo> <scratch>/upstream`
For the latest tag: `git ls-remote --tags --sort=-v:refname https://github.com/<template.repo>` and take the first `v*` tag.

If the upstream `VERSION` equals the current one, say "Already up to date (<version>)" and stop.

## Step 3: What changed upstream
Read the upstream `CHANGELOG.md` entries newer than the current version and summarise them in five lines or fewer. Diff upstream against the local framework folder (`git diff --no-index`) for `roles/`, `templates/`, `packs/`, `themes/` (not `themes/local/`), `team.config.schema.yaml`, `VERSION`, `scripts/render.py`, and `.claude/commands/{init-team,sync-team,self-review}.md`.

Call out:
- roles whose `version` went up (their personas will change);
- new config fields in the schema. For each, ask the owner for a value with the schema default offered, one question at a time; with `--non-interactive`, use the default;
- with `--non-interactive`, a hand-written file is never replaced: render it with `--alongside`;
- local edits to framework files (a framework file that differs from both the old and the new upstream). Never overwrite those silently: show the diff and ask whether to keep, take upstream, or merge by hand.

## Step 4: Update the framework and re-render
1. In a staging copy of the repo, replace the framework files with upstream's, leaving `themes/local/` and any file the owner chose to keep.
2. Re-render with the **new** `scripts/render.py`, exactly as `/init-team` Step 4 describes, from `team.config.yaml` and the **new** framework, carrying over every `agent-roundtable:local` block.
3. Set `template.version` (and `template.ref`) in the staged `team.config.yaml`.

## Step 5: Diff and write
Show the summary table (new / changed / unchanged) and the full diff, as `/init-team` Step 5 describes. Ask **Write**, **Change something**, or **Cancel** (or write directly with `--non-interactive`).

After writing, run the checks from `/init-team` Step 6. Then tell the owner: review and commit with a message such as `chore: sync agent team to agent-roundtable <new version>`, restart Claude Code so the agents reload, and re-run `bash scripts/install-hooks.sh` if the hooks changed.

## Report
Five lines: old → new version, roles that changed, files changed, questions answered, anything left for a manual merge.
