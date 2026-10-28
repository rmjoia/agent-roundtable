---
description: Read-only critical review of a diff (working tree, PR number, commit range or file) against the team's self-review lens, the Definition of good code and the API, security and contract standards. Surfaces findings; never fixes.
argument-hint: "[<PR-number> | <ref>..<ref> | <path>]"
context: fork
agent: general-purpose
disallowed-tools: Edit, Write, NotebookEdit, AskUserQuestion, Agent
---

## Scope

`$ARGUMENTS`, resolved as:
- **empty**: the working tree (`git diff` and `git diff --cached` against HEAD); if clean, `git diff origin/main...HEAD`.
- **a PR number**: `gh pr view <n> --json baseRefOid,headRefOid`, then `git fetch origin` and `git diff <base>...<head>`.
- **`<ref>..<ref>`**: that range.
- **a path**: that file against HEAD.

If it is ambiguous, return one focused question instead of a report. Never assume.

**Read-only.** This command reports; fixing is a separate step the owner approves.

## Read first
- `docs/team-roster.md` → *Self-review lens* and *Lanes*.
- The Definition of good code and the API, contracts, testing and security standards under `docs/conventions/` (or `packs/neutral/` in the template repo).
- `CLAUDE.md` for project-specific decisions; they win where they differ.

## Review
Print `Reviewing: <scope>`. Read the full diff; if it is over 1000 lines, review it file by file rather than skimming.

Apply, in order, listing findings per lens (or "no issues") with `file:line`, a one-sentence problem and a severity (`blocker | major | minor | nit`):

1. **The self-review lens**, all 13 items.
2. **Architecture**: single responsibility; boundaries (UI ↔ service ↔ repository); adapters translate, never decide; no framework types across a boundary; over-engineering (an interface with one implementation and no test seam, a layer that only forwards). Name what to delete, not only what to add.
3. **Lanes**: every changed path against the lane table; out-of-lane changes named with their owner.
4. **Contracts**: a shape crossing lanes with no agreed contract is a **blocker**; the version follows the change; both sides test against the golden examples; readers accept old shapes.
5. **API standard** on every new or changed endpoint (RFC 9457, no PII or internals in errors, 404 over 403 where existence leaks). A miss is a **blocker**.
6. **Security**: OWASP Top 10 for the categories that apply.
7. **Tests**: each new or changed test would fail on a plausible wrong implementation; impacted tests listed and handled; no `.skip` / `.only`.
8. **Comments and status**: no narration, no ticket ids in code.
9. **Edge cases**: null, empty, error responses, races, large inputs, time zones, every language, cold load.
10. **Production parity**: no debug paths, environment short-circuits or leftover logging.
11. **Hygiene**: Conventional Commits, one logical change per commit, the `Agent:` trailer, size limits, boy-scout cleanups.

## Output

```markdown
# /self-review: <scope>

**Verdict**: GREEN / YELLOW / RED / BLOCKED: <check that could not run, and why>

## Blockers
- `file:line`: problem (lens). **Why it matters**: … **Suggested fix**: …
## Major
## Minor / nit
## Lanes
## Contracts and compatibility
## Security (OWASP)
## PR-body addenda
## Files to touch for blockers and majors
```

Return the report and stop. Never estimate or restate a pass you didn't check. Keep it to about 300 lines; for a large diff, prioritise blockers and majors.
