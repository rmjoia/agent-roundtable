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

The framework is these folders: `roles/`, `themes/`, `templates/`, `packs/`, plus `VERSION` and `team.config.schema.yaml`.

1. Look at the repo root. If `roles/architect.md` is there, that is `FRAMEWORK`.
2. Otherwise look in `.roundtable/`.
3. Otherwise tell the owner the framework files are missing and offer: "Fetch them from github.com/rmjoia/agent-roundtable into `.roundtable/`?" On yes, run `git clone --depth 1 https://github.com/rmjoia/agent-roundtable <scratch>/roundtable` and copy `roles themes templates packs VERSION team.config.schema.yaml` into `.roundtable/`. On no, stop.

Read every file in `FRAMEWORK/roles/`, the chosen theme later, and every template you render. Don't work from memory of them.

## Step 1: Existing state

- If `team.config.yaml` exists, read it. Ask (one question): **Re-render from the current config**, **Change some answers**, or **Start over**. With `--rerender`, choose re-render. For "Change some answers", list the sections (project, stack, roles and lanes, theme, models, review gates, languages, conventions, gates) and ask which to revisit; interview only those.
- Note which output files already exist (see Step 4) and whether each carries an `agent-roundtable:generated` marker. Files without the marker were written by people; you will merge or ask, never silently overwrite.

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
7. **Review gates.** Show the default matrix built from the enabled roles: self-review (architect, always), security (always), plan alignment (product-owner, always), test quality (qa, code changes), docs (docs, behaviour changes), usability (frontend + copy, UI changes), product (product-manager, product changes), contract (the consumer, contract changes), infra (devops, infra changes). Ask: accept, or change?
8. **Languages.** If `copy` is enabled or translation files exist: the supported languages as BCP 47 tags with regional variants (`pt-PT`, not `pt`), and the source language.
9. **Conventions.** Commit style (default Conventional Commits), branch pattern (default `<type>/<issue>-<slug>`), size limits (default 800 lines / 25 files soft, 1500 / 40 hard). Then, as a separate question, the push policy: `owner-only` (default: agents and the architect never push) or `architect-on-merge-approval` (the architect pushes and opens PRs; merges only on the owner's explicit "merge #N").
10. **Gates.** Propose pre-commit gates from the stack (build, lint, unit tests per area, with a path regex and working dir), drawing on the stack pack's `gates.md` when there is one. Ask: accept, or edit?
11. **Packs.** `neutral` always; offer any stack pack in `FRAMEWORK/packs/` that matches.
12. **Retro cadence.** Default weekly.

Then show the complete `team.config.yaml` you will write and ask for a final OK, or what to change.

## Step 4: Render into a staging folder

Render everything into a staging folder in your scratchpad (never into the repo yet), mirroring the repo layout. Validate the config against `team.config.schema.yaml` first. If PyYAML and `jsonschema` are available, use them (`python3 -I`); otherwise check by reading the schema.

### Names
For each enabled role: `Name` = `roles.<id>.name` if set, else the theme's name, else the `neutral` theme's. `name` (the slug) = `Name` lower-cased, accents stripped, non-alphanumerics → `-`. Slugs must be unique; if not, stop and ask.

### Placeholders
Replace every placeholder listed in `FRAMEWORK/roles/README.md`. Also:
- `{{template.version}}` → the contents of `FRAMEWORK/VERSION`; `{{template.repo}}` → `template.repo`.
- `{{role:<id>}}` → that role's display name. If the role is disabled: in a list item or table row that is only about that role, drop the line; in running text, use "{{owner}}" and keep the sentence true.
- `{{role_slug:<id>}}` → that role's slug.
- `{{lanes}}` → each lane glob, after resolving `{{paths.*}}`, as an indented bullet in code format (`  - \`web/**\``); exclusions as `  - except \`web/src/locales/**\``. Final lanes = `roles.<id>.lanes` if set, else the template's `default_lanes`; plus `extra_lanes`. A lane whose `{{paths.x}}` is undefined or "none" is dropped.
- `{{hands_over}}` → one indented bullet per entry: `  - <what> → <Name>` (`"*"` means "→ its owner"). A hand-over to a disabled role becomes `→ {{owner}} (no owner yet)`.
- `{{gates}}` → the pre-commit gates whose path regex overlaps the role's lanes, as indented bullets: `  - \`cd <cwd> && <run>\``. If none, `  - the project's checks for what you changed`.
- `{{trailer}}` → the trailer pattern with this agent's slug and model, e.g. `Agent: hermes (opus)`. `{{trailer_example}}` → the pattern as written in the config.
- `{{model}}` → `models[tier]` where tier = `roles.<id>.tier` or `default_tier`, never lower than `tier_floor`.
- `{{shared_rules}}` → the contents of `FRAMEWORK/templates/shared-rules.md`.
- `{{push_policy}}` (architect) → for `owner-only`: "You never push, open PRs or merge. When a branch is ready, give {{owner}} the summary and the exact commands; {{owner}} pushes, opens the PR and merges." For `architect-on-merge-approval`: "You push, open PRs and apply labels. You merge only on {{owner}}'s explicit \"merge #N\" for that PR; approval for one PR never extends to another. Specialists never push, open PRs or merge." `{{push_policy_short}}` (roster) → the first sentence of the same text, rewritten in the third person.
- `{{packs_path}}` → `docs/conventions/neutral`.
- `{{models.*}}`, `{{size.*}}`, `{{retro.*}}`, `{{stack.*}}`, `{{i18n.*}}` → from the config (defaults from the schema). A `stack.*` of "none" or unset renders as "the project's stack" in running text.
- `<!-- render: … -->` lines are instructions to you: carry them out and remove them from the output.

After rendering, `grep -n '{{' ` over the staging folder must find nothing. Fix any leftover before showing the diff.

### Outputs

| Output | From | Notes |
|---|---|---|
| `team.config.yaml` | the interview | |
| `.claude/agents/<name>.md` | `roles/<id>.md`, one per enabled role except the architect | format below |
| `CLAUDE.md` | `templates/claude-team-section.md.tmpl` | `{{architect_body}}` = the architect template's body, rendered. Insert or replace **only** the block between `<!-- agent-roundtable:start` and `<!-- agent-roundtable:end -->`. If `CLAUDE.md` doesn't exist, create it with a `# <project>` heading, a one-paragraph project summary and stack table from the config, then the block. |
| `docs/team-roster.md` | `templates/team-roster.md.tmpl` | |
| `docs/process/task-brief.md` | `templates/process/task-brief.md` | |
| `docs/process/definition-of-done.md` | `templates/process/definition-of-done.md` | |
| `docs/conventions/<pack>/**` | `packs/<pack>/**` | copied as-is |
| `.github/PULL_REQUEST_TEMPLATE.md` | `templates/github/PULL_REQUEST_TEMPLATE.md` | |
| `.github/ISSUE_TEMPLATE/{story,task,bug,retro-log}.md` | `templates/github/ISSUE_TEMPLATE/` | |
| `scripts/git-hooks/pre-commit`, `commit-msg` | `templates/hooks/` | `{{gates_rows}}` = one line per gate: `gate "<name>" "<paths>" "<cwd>" "<run>"`, with `"`, `$` and backticks inside each value escaped for bash. Executable. |
| `scripts/install-hooks.sh` | `templates/hooks/install-hooks.sh` | executable |

Skip the usability line, the copy and i18n lines, etc., when the roles they name are disabled. If the commit style is not Conventional Commits, don't render `commit-msg`.

### Agent file format

```markdown
---
name: <slug>
description: <Title>. <summary from the role front matter, with role ids replaced by names>. Lanes: <first three lane globs>.
model: <model>
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch        # only when the role is read_only
---
<!-- agent-roundtable:generated role=<id> role_version=<version> template=<VERSION> — edit team.config.yaml or the local section below, then re-run /init-team -->

<rendered body>

<!-- agent-roundtable:local:start -->
<!-- Project-specific additions for this agent go here; /init-team and /sync-team keep this block. -->
<!-- agent-roundtable:local:end -->
```

If the agent file already exists, carry its `agent-roundtable:local` block over unchanged. If it exists **without** the generated marker, it was hand-written: show it to the owner and ask whether to replace it (moving its project-specific content into the local block) or keep it and skip this role.

### Existing files without a marker
For `CLAUDE.md`, insert the block (above). For a PR template, issue templates or hooks that people wrote: show a side-by-side summary and ask per file: replace, keep theirs, or write ours next to it with a `.roundtable` suffix for a manual merge. For existing hooks, never drop a check they already run: offer to add it as a gate.

## Step 5: Show the diff

1. A summary table: each output file, and whether it is **new**, **changed** or **unchanged**.
2. The full diff for changed files (`git diff --no-index -- <repo file> <staged file>`), and the full content of new files, grouped: config, agents, CLAUDE.md, roster and process, templates, hooks.
3. The lane table as rendered, and any overlaps or unowned paths.

Ask: **Write these files**, **Change something** (back to the relevant question), or **Cancel**. With `--non-interactive`, write without asking.

Re-running with the same answers must produce **no changes**. If it does, that's a bug in this render: say so.

## Step 6: Write and check

1. Copy the staged files into the repo. Make the hooks executable.
2. Check: every agent file's front matter parses; every `{{role:` and `{{` is gone (`grep -rn '{{' .claude/agents docs/team-roster.md CLAUDE.md .github scripts/git-hooks`); `bash -n` on each hook; each lane in the roster matches the persona.
3. Don't install the hooks, create labels, commit or push. Tell the owner the next steps:
   - review the diff (`git status`, `git diff`) and commit it, e.g. `chore: set up the agent team (agent-roundtable <VERSION>)`;
   - run `bash scripts/install-hooks.sh`;
   - create the `agent:<name>` and `reviewed:<name>` labels (offer the exact `gh label create` commands; run them only if the owner asks);
   - open the first `Retro log — <period>` issue;
   - restart Claude Code (or run `/agents`) so the new agents load.

End with a five-line summary: the team (names and roles), the theme, the files written, and the one thing to do next.
