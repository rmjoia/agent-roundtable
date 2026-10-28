# Sync

Your project's team is **generated**: role templates + your theme + `team.config.yaml`. That is what makes two-way sync possible without losing your names or lanes.

What survives a re-render:
- everything in `team.config.yaml` (theme, names, lanes, tiers, gates, review matrix);
- `themes/local/`;
- the `<!-- agent-roundtable:local:start -->` … `end` block in each agent file;
- everything in `CLAUDE.md` outside the `agent-roundtable:start` … `end` block.

Hand edits elsewhere in generated files are shown in the diff on the next render, so nothing is lost silently, but they will be replaced if you accept it. Put project-specific additions in the local block or in the config.

## Downstream: template → your project

Run `/sync-team` in Claude Code. It:
1. fetches the template at the latest release tag (or the ref you name) into a scratch folder;
2. summarises the CHANGELOG since your version and lists roles whose `version` went up;
3. asks for values of any new config fields;
4. updates the framework folders (never `themes/local/`; asks about any framework file you edited);
5. re-renders from your `team.config.yaml`, keeping local blocks;
6. shows the diff and writes on your approval. You review and commit.

### Automated
[`templates/workflows/sync-team.yml`](../templates/workflows/sync-team.yml) runs `/sync-team --non-interactive` weekly through `anthropics/claude-code-action` and opens a PR in your project. It needs an `ANTHROPIC_API_KEY` secret. It is a template: copy it into your project's `.github/workflows/` only if you want it. Nothing in this repo runs it.

## Upstream: your project → template

Improvements discovered in a project (a better rule, a missing hand-over, a persona fix from a retro) can benefit everyone. The upstream flow turns them into a PR against the template **without leaking anything about your project**.

### Design
Trigger: a push to your main branch that changes `.claude/agents/**`, `docs/team-roster.md` or `docs/process/**`, or a manual run.

1. **Diff** the framework paths since the last upstream sync (tag `roundtable-upstream-<n>` in your repo).
2. **Classify** each hunk: generic (a rule, a principle, a hand-over, a format) or project-specific (anything naming your product, stack details, cloud resources, people, identifiers, issue numbers, dates of rulings). Only generic hunks continue.
3. **Map names back to roles.** Using `team.config.yaml` and your theme file, replace every themed name with its role id or `{{role:<id>}}`; replace resolved lanes with their `{{paths.*}}` placeholders.
4. **Express the change in template terms**: as a patch to `roles/<id>.md` or `templates/**`, with the role's `version` bumped.
5. **Scrub**: run `scripts/scrub-check.sh` (with your private `.scrub-patterns.local` listing your product name, domains and people) on the patch. Any hit stops the flow.
6. **Open a draft PR** from your fork of the template, with the rationale and the retro finding that motivated it, paraphrased. Never raw project text.

### Guardrails
- It runs in a GitHub **environment with required reviewers**, so a human approves before anything leaves the repo.
- The token is fine-grained and scoped to your fork of the template only.
- Owner rulings are kept as rules; their citations (who, when, which issue) are dropped.
- The PR is a draft; a maintainer of the template decides whether it lands.

A reference workflow is in [`templates/workflows/upstream-contribution.yml`](../templates/workflows/upstream-contribution.yml). It is a design reference, not installed anywhere. Adapt it, read it end to end, and test it on a fork before enabling it.

### By hand
You can do the same without automation: copy the generic part of your change into a fork of the template, replace names with role ids, run `scripts/scrub-check.sh`, and open a PR. See [CONTRIBUTING.md](../CONTRIBUTING.md).
