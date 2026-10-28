# Lanes

A **lane** is the set of paths an agent may write. Lanes are path globs in `team.config.yaml`, rendered into each persona and into the lane table in `docs/team-roster.md`.

## One owner per path
Every path has exactly one owning role. `/init-team` checks for overlaps (two roles owning the same path; use `!` exclusions to resolve them) and gaps (a source folder with no owner). A gap is the owner's decision, never quietly absorbed by the architect.

## Refuse and delegate
Before writing to any path, an agent checks it against its lane. Outside its lane it doesn't write, even a one-liner, even when the brief asks. It hands the work over in its report: the owning agent, what is needed, why. A brief that asks for out-of-lane work is the architect's error, and the agent says so.

This is a prompt rule, not a CI gate. A CI gate would catch the slip after the work is done, and the work would be redone by the right agent. Prevention is cheaper.

## A slip is tracked, not thrown away
When out-of-lane work happens anyway and the result is sound, keep it: the owning agent reviews the out-of-lane part. The architect logs the slip on the retro issue with a short post-mortem (what happened, why the persona or brief allowed it, the prompt change proposed). The retro turns that into a persona fix.

## Tests follow the code
A test belongs to the owner of the code it exercises, whatever folder it sits in. The QA lead owns end-to-end journeys and reviews test quality everywhere, sending findings to each test's owner.

## Contracts let lanes run in parallel
When one lane provides an interface and another consumes it, the architect designs a versioned contract first; the provider writes it; both build against it. The contract also fixes the names other lanes need (i18n keys, port interfaces), so copy is written while the UI is built and adapters are built while the core is. See [`packs/neutral/contracts.md`](../packs/neutral/contracts.md).

## One agent, one PR
Each agent works on its own branch, cut from main per work item, and its PR is green on its own. Across lanes, the provider merges first. The only exception, a change that can't be green split across lanes, ships in one PR with each commit by its owner, recorded on the parent item.

## Every commit is green
Before each commit, the agent runs the gates for what it changed: build, its new and changed tests plus that project's full suite, and lint. Never `--no-verify`. The generated pre-commit hook runs the same gates as a safety net; a hook failure means a gate was skipped.
