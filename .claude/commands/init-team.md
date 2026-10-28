---
description: Interview the owner one question at a time, then generate a single-domain Claude Code agent team (personas, roster, CLAUDE.md section, PR/issue templates, briefs, pre-commit hook) from the agent-roundtable role templates. Idempotent; shows a diff before writing.
argument-hint: "[--rerender] [--non-interactive]"
---

# /init-team

You are setting up an agent-roundtable team in this repository. You **interview** the owner, write `team.config.yaml`, **render** the team from the role templates, **show a diff**, and write only after the owner approves. You never commit, push or open PRs.

Arguments: `$ARGUMENTS`
- `--rerender`: skip the interview; re-render from the existing `team.config.yaml`.
- `--non-interactive`: never ask; use the existing config (or defaults) and write the result without the approval step. Only for automation such as `/sync-team` in CI.

---

## Step 0: Find the framework

The framework is these folders: `roles/`, `themes/`, `templates/`, `packs/`, plus `scripts/render.py`, `VERSION` and `team.config.schema.yaml`.

1. Look at the repo root. If `roles/architect.md` is there, that is `FRAMEWORK`.
2. Otherwise look in `.roundtable/`.
3. Otherwise tell the owner the framework files are missing and offer: "Fetch them from github.com/rmjoia/agent-roundtable into `.roundtable/`?" On yes, run `git clone --depth 1 https://github.com/rmjoia/agent-roundtable <scratch>/roundtable` and copy `roles themes templates packs VERSION team.config.schema.yaml` and `scripts/render.py` into `.roundtable/` (keeping `scripts/`). On no, stop.

Read every file in `FRAMEWORK/roles/`, the chosen theme later, and every template you render. Don't work from memory of them.

## Step 1: Existing state

- If `team.config.yaml` exists, read it. Ask (one question): **Re-render from the current config**, **Change some answers**, or **Start over**. With `--rerender`, choose re-render. For "Change some answers", list the sections (project, stack, roles and lanes, theme, models, review gates, languages, conventions, gates) and ask which to revisit; interview only those.
- Note which output files already exist (see Step 4) and whether each carries an `agent-roundtable:generated` marker (`CLAUDE.md`: an `agent-roundtable:start` block). Files without one were written by people; you will merge or ask, never silently overwrite.

## Step 2: Look before you ask

Inspect the repo so every question can offer a sensible default the owner can accept with one word:
- Manifests and config: `package.json`, `angular.json`, `vite.config.*`, `next.config.*`, `*.csproj`, `*.sln`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `Dockerfile`, `*.tf`, `*.bicep`, `.github/workflows/*`, `playwright.config.*`, `cypress.config.*`.
- Top-level folders and the likely front-end, back-end, domain, test, e2e, infra, docs and i18n paths.
- Translation files (`**/i18n/**`, `**/locales/**`, `*.po`, `*.resx`) and the languages they contain.
- Commit style in `git log --oneline -30`, and branch names in `git branch -a`.
- Existing `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, PR and issue templates, git hooks.

Say in one or two lines what you found before the first question.

## Step 3: The interview: one question at a time

Ask **exactly one question per message** and wait for the answer. Use the AskUserQuestion tool when the answer is a choice; plain text when it is free-form. Put the detected default first, marked "(Recommended)" or "(detected)". Keep each question self-contained. If the owner says "defaults" or "you choose" at any point, take the defaults for the rest and say so.

Never ask for a person's name. The owner is a role: `owner.title` defaults to "the owner".

1. **Project.** Name and one line on what it does and for whom. Then, as a separate question, the law and standards that apply (privacy, consumer, accessibility, sector rules), default from the domain, or "none".
2. **Stack, one layer per question**: front end, back end, database, cloud or hosting, CI, unit test runner, E2E runner. Each defaults to what Step 2 found; "none" removes the layer.
3. **Roles.** Show the 13 roles (id, title, one line) and ask which to enable (multi-select). The architect is always on. Suggest a default from the stack: no front end → no `frontend`, `copy` or usability gate; one back-end project → offer `backend-app` alone (it then also owns the domain lanes); no infra → `devops` still owns CI and hooks. Small teams often start with architect, security, qa, one or two builders and steward.
4. **Lanes.** For each enabled role, one question: show its default lanes resolved against the detected paths, and ask "Accept, or edit?". Fill `paths:` from the answers. Then check the lanes yourself: two roles must not own the same path (a `!` exclusion resolves an overlap); every source folder found in Step 2 should have an owner. Report any overlap or unowned path and ask how to resolve it.
5. **Theme.** Offer the shipped themes (`neutral`, `arthurian`, `greek`, `roman`, `norse`, `egyptian`, `astronomy`), showing three example names from each, plus "my own" (then help write `themes/local/<id>.yaml`, following `themes/README.md`). Franchise names (film, TV, book franchises) are not offered; if asked, explain why (`themes/README.md`) and offer a local theme with original names.
6. **Model tiers.** Show the default tier per role and the tier → model map (`fast: haiku, balanced: sonnet, strong: opus, strongest: opus`, with the strongest set to the strongest model the owner's plan offers). Principle: the cheapest tier that does the job right first time; security stays on `strongest`. Ask: accept, or change which roles or mappings?
7. **Review gates.** Show the default matrix built from the enabled roles: architecture and contract (architect, always), security (always), plan alignment (product-owner, always), test quality (qa, code changes), docs (docs, behaviour changes), usability (frontend + copy, UI changes), product (product-manager, product changes), contract (`consumer`: the agent that consumes the changed contract, contract changes), infra (devops, infra changes). Ask: accept, or change?
8. **Languages.** If `copy` is enabled or translation files exist: the supported languages as BCP 47 tags with regional variants (`pt-PT`, not `pt`), and the source language.
9. **Conventions.** Commit style (default Conventional Commits), branch pattern (default `<type>/<issue>-<slug>`), size limits (default 800 lines / 25 files soft, 1500 / 40 hard). Then, as a separate question, the push policy: `owner-only` (default: agents and the architect never push) or `architect-on-merge-approval` (the architect pushes and opens PRs; merges only on the owner's explicit "merge #N").
10. **Gates.** Propose pre-commit gates from the stack (build, lint, unit tests per area, with a path regex and working dir), drawing on the stack pack's `gates.md` when there is one. Ask: accept, or edit?
11. **Packs.** `neutral` always; offer any stack pack in `FRAMEWORK/packs/` that matches.
12. **Retro cadence.** Default weekly.

Then show the complete `team.config.yaml` you will write and ask for a final OK, or what to change.

## Step 4: Render into a staging folder

Write the agreed config to `<scratch>/team.config.yaml` and render into a staging folder in your scratchpad, never into the repo:

```bash
python3 -I FRAMEWORK/scripts/render.py --framework FRAMEWORK --repo . \
  --config <scratch>/team.config.yaml --out <scratch>/stage [--skip <path>]... [--alongside <path>]...
```

`render.py` is the reference renderer: deterministic, so a re-run with the same answers changes nothing. It needs Python 3 and PyYAML. If `import yaml` fails, ask the owner once: install it (`python3 -m pip install --user pyyaml`), or render by hand. For a hand render, follow the rules in `FRAMEWORK/roles/README.md` and do what `render.py` does, reading its source as the specification.

`render.py` prints a JSON summary: the agents, the outputs, lane **overlaps**, and **notes** about existing hand-written files. It also sets `template.version` in the staged config. It stops on unrendered placeholders or duplicate agent names; fix the cause (usually a `roles.<id>.name` override) and run it again.

### Existing files written by people
Files without an `agent-roundtable:generated` marker (or, for `CLAUDE.md`, without the `agent-roundtable:start` / `end` block) were written by people:
- **`CLAUDE.md`**: the renderer appends the team block at the end and never touches the rest. On later runs it replaces only the block.
- **A hand-written agent file** with the same name as a generated one: show it, and ask: replace it (and offer to move its project-specific content into the new file's `agent-roundtable:local` block afterwards), or keep it (`--skip`).
- **PR template, issue templates, hooks**: ask per file: replace, keep theirs (`--skip`), or write ours next to it for a manual merge (`--alongside`, which writes `<file>.roundtable`). For a hand-written hook, offer to carry each of its checks into `gates.pre_commit` first, so no check is dropped.

Re-run `render.py` with the chosen flags. With `--non-interactive`, use `--alongside` for every hand-written file.

## Step 5: Show the diff

1. A summary table: each output, **new**, **changed** or **unchanged** (`diff -q` against the repo).
2. The full diff for changed files (`git diff --no-index -- <repo file> <staged file>`) and the content of new files, grouped: config, agents, CLAUDE.md, roster and process, conventions, GitHub templates, hooks. Summarise `docs/conventions/**` by file instead of printing it.
3. The lane table from the staged `docs/team-roster.md`, the overlaps from the summary, and any source folder from Step 2 that no lane covers.

Ask: **Write these files**, **Change something** (back to the relevant question), or **Cancel**. With `--non-interactive`, write without asking.

Re-rendering with the same answers must produce **no changes**. If it does, say so: it is a bug.

## Step 6: Write and check

1. Copy the staged files into the repo (`cp -R <scratch>/stage/. .`). The hooks keep their executable bit.
2. Check: every agent file's front matter parses (`python3 -I -c` with `yaml.safe_load`, or read it); no `{{` is left outside GitHub Actions expressions (`grep -rn '{{' .claude/agents docs/team-roster.md docs/process CLAUDE.md .github/PULL_REQUEST_TEMPLATE.md .github/ISSUE_TEMPLATE scripts/git-hooks`); `bash -n` on each hook.
3. Don't install hooks, create labels, commit or push. Tell the owner the next steps:
   - review the diff (`git status`, `git diff`) and commit it, for example `chore: set up the agent team (agent-roundtable <VERSION>)`;
   - run `bash scripts/install-hooks.sh`;
   - add `.scrub-patterns.local` to `.gitignore`, and list in it the names that must never be pushed (product code names, internal domains, people);
   - create the labels: `agent:<name>` and `reviewed:<name>` per agent, plus `type/story`, `type/task`, `type/bug` and `<retro.label>`. Offer the exact `gh label create` commands; run them only if the owner asks;
   - open the first `Retro log — <period>` issue;
   - restart Claude Code (or open `/agents`) so the new agents load.

End with a five-line summary: the team (names and roles), the theme, the files written, and the one thing to do next.
