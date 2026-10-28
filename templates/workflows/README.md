# Workflow templates (inert)

These files are **not** under `.github/workflows/`, so GitHub never runs them in this repo. Copy one into your own project's `.github/workflows/` only if you want it there. Both need an `ANTHROPIC_API_KEY` repository secret and use [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action); check that action's README for the current inputs before you enable them.

| File | Runs in | Does |
|---|---|---|
| `sync-team.yml` | your project | weekly (or on demand), runs `/sync-team` and opens a PR with template updates |
| `upstream-contribution.yml` | your project | when framework files change on main, maps names back to roles, scrubs, and opens a PR against the template. **Design reference**: see `docs/sync.md` before enabling |
