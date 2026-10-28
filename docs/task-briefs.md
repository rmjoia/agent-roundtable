# Task briefs

Every dispatch from the architect uses a fixed format, rendered into your project as `docs/process/task-brief.md`. The format exists because of two failure modes:

1. **A retold finding loses its conditions.** "Fix the null check in the handler" drops *which* handler, *which* input and *why it matters*. The brief quotes or links its source; it never retells it.
2. **A guessed premise costs a rework loop.** Issue bodies are snapshots. The brief separates what the architect **checked** from what it **believes**.

## The fields that matter most

- **`Verified at: main <sha>`**: only facts checked against the code just before dispatch (git log since the issue's date, grep for callers and owners).
- **`inference:`**: anything believed but not checked, marked so the agent checks it.
- **`Owner-approved actions`**: what exactly the owner approved, each with a citation, or "none". An approval that can't be traced is a premise mismatch.
- **`suggestion:`**: the architect's idea for the fix. The design inside an agent's lane belongs to that agent.
- **Existing behaviour**: what the code and its tests do today, read, not remembered.
- **Definition of done**: the project's own gates, never a hand-picked subset.

## The premise check
If the brief's premise differs from the code (a path, symbol, issue or status), the agent stops and reports first. It never builds on or around a wrong premise.

## Reports
Every report is ≤ 300 words (a review ≤ 200 per PR), with details on the issue or PR. It has a `Docs impact` line and ends with `## Feedback`. A gate the agent couldn't run is reported as `blocked: <reason>`, never as passed.

## Work items are the shared state
Agents coordinate through the backlog, not through chat. Every brief starts from a work item; every agent writes status and a Handoff block (`Delivered:`, `Unblocks:`, `Next needs:`) back to it. The next agent starts from that record.
