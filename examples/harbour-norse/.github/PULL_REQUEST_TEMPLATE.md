<!-- agent-roundtable:generated template=pull-request version=0.1.0 -->
## Linked issue

Closes #

## Summary

<!-- What this PR does and why, in two or three sentences. -->

## Agents

<!-- docs/team-roster.md → Attribution. Matches the agent:<name> / reviewed:<name> labels. Each review states what it challenged and why it held. Delete this section for a human-authored PR. -->

- **Written by**: <!-- <agent> (<model>), one per authoring agent -->
- **Reviewed by**: <!-- <agent> (<model>) <verdict>, one per review in the gate (docs/team-roster.md → Review gate) -->

## Docs

<!-- Keep one line. -->
Docs: updated (<!-- paths -->) / not needed because <!-- reason -->

<!-- Issue bodies are snapshots: when this PR changes an open issue's facts (scope, paths, status, a decision), say so and comment on that issue. -->
Affects open issues: #N — what changed (comment posted) / none

## Impacted tests

<!-- Required on any PR that changes UI or API (docs/process/definition-of-done.md → Testing). Grep the changed components, i18n keys, test ids, routes, DTOs and endpoints, then list the impacted tests per layer and tick the outcome. -->

- **Unit**:
- **Integration**:
- **E2E** (outside your lane? signal it here):

- [ ] N/A: no UI or API change
- [ ] Impacted tests failed → updated in this PR
- [ ] No test touched the change → tests added in this PR
- [ ] Tests touched the change but nothing failed → assertions strengthened

## How it was tested

```bash
# commands run, with results
```

## Breaking changes

None

## Handoff

- **Delivered**:
- **Unblocks**: #
- **Next needs**:

## Checklist

- [ ] Every commit green (gates run before each commit; no `--no-verify`)
- [ ] Self-review lens applied (`docs/team-roster.md` → *Self-review lens*)
- [ ] Within size limits (800 lines / 25 files target; 1500 / 40 hard)
- [ ] No secrets, identifiers or PII in the diff, commit messages, fixtures or screenshots
- [ ] Contract version bumped if a contract changed; consumers still read old shapes
- [ ] Every user-facing string has keys in en-GB, nb-NO
