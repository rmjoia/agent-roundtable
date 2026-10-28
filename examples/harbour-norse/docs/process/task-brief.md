<!-- agent-roundtable:generated template=task-brief version=0.1.0 -->
# Briefs

Every dispatch from the architect to an agent uses one of these formats. They exist because a retold finding loses its conditions, and a guessed premise costs a rework loop.

## Task brief: every dispatch

```markdown
**Task: <title>** (to <agent>, <model>)
- **Goal**: the outcome, in one or two sentences
- **Work item**: #<issue> — its current state quoted
- **Source**: the finding, issue or ruling, quoted word for word or linked, never retold
- **Contract**: <name> v<X.Y.Z>, or the design brief on #<issue>
- **Paths**: the paths this agent owns for this task (checked against the lane table)
- **Branch**: <branch> from main
- **Verified at**: main <sha> — only what was checked against the code just before dispatch
  (git log since the issue's date, grep for callers and owners)
- `inference:` anything believed but not checked, marked as such
- **Owner-approved actions**: what exactly, each cited (issue and date, or a dated quote), or "none".
  An approval that can't be traced is a premise mismatch: stop and report.
- **Acceptance criteria**: Given / When / Then, including an edge or error case; for a defect, the failing scenario
- `suggestion:` the architect's idea for the fix, if any. The design inside the agent's lane is the agent's.
- **Constraints**: the security strategy where the task touches auth, data or PII (a control from it is a
  constraint, never a suggestion); the performance budget
- **Existing behaviour**: what the code and its tests do today in this area, read, not remembered
- **Definition of done**: the gates to run (the project's own scripts, never a subset) and the self-review lens
- **Out of scope**: what not to touch
- **Hand-overs expected**: <agent → agent>
- **Docs impact (required)**: the report says what changed for the docs, or "none"
- **Feedback (required)**: end the report with `## Feedback`, "None" if none
```

**Premise check.** Issue bodies and briefs are snapshots. If the brief's premise differs from the code (a path, symbol, issue or status), the agent stops and reports first; it never builds on or around it. An `inference:` or `suggestion:` is a claim to check, not a premise.

## Review brief: every review dispatch

```markdown
**Review: PR #<N> <title>** (to <reviewer>, <model>)
- **Head**: <head-sha>; **base**: <base-sha>, both recorded at dispatch: review that commit, not a later one
- **Diff**: `git fetch origin`, then `git diff <base-sha>...<head-sha>` (not moving remote-tracking refs)
- **Story**: #<issue>, and the whole stack if the PR is stacked
- **Lens**: the reviewer's row in the review gate, plus the self-review lens
- **Running tests**: in a throwaway worktree at the head SHA, removed afterwards; never in a builder's worktree
- **Body check**: does the PR body describe every head commit?
- **Verdict**: findings with `file:line`, each to its owning agent; what was challenged and why it held
- **Feedback (required)**: end the report with `## Feedback`, "None" if none
```

## Decision brief: anything for the owner

```markdown
**Decision needed: <title>** (from <agent>)
- **Context**: what we are building and the constraint involved
- **Current situation**: what exists now, with evidence (file:line, issue, PR)
- **Impact**: who or what is affected, and what happens if we do nothing
- **Options**: each with trade-offs (cost, risk, performance, security, time, reversibility)
- **Recommendation**: the agent's pick and why
```

The architect relays it verbatim, then adds a view labelled as the architect's.

## Return summary: architect to owner

> **<agent>** (<model>) returned. **Commit**: <sha>. **Scope**: X files, Y lines. **Tests**: <count>. **Lint and build**: <result>. **Hand-overs raised**: <list>. **Decision briefs**: <relayed verbatim>. **Docs impact**: <what, or none>. **Feedback**: <verbatim, or none; logged on the retro issue>.

## Dispatch line: architect to owner

> Sending **<agent>** to do **<task>** against **<contract vX.Y.Z>**, in **<paths>**. Hand-overs expected: <agent → agent>.
