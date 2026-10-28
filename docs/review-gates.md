# Review gates

Every PR passes a set of reviews chosen by what it changes. The matrix lives in `team.config.yaml` → `review_gates` and is rendered into `docs/team-roster.md`.

| Gate | Default reviewer | When |
|---|---|---|
| Self-review | the authoring agent, then the architect | always |
| Security and data protection | security | always |
| Plan alignment | product owner | always |
| Test quality | QA lead | the PR changes code or tests |
| Docs | docs | the PR changes behaviour |
| Usability walk | front-end + copy | the PR changes a user-facing surface |
| Product | product manager | the PR changes product rules, pricing or claims |
| Contract | the consuming agent | the PR changes a contract |

`when` values: `always`, `code`, `behaviour`, `ui`, `product`, `contract`, `infra`.

## Challenge, never nod
A review checks the diff against the project's principles and the Definition of good code, and names a better-suited pattern where one fits, with a cited reason. An approval states what was challenged and why it held. "Looks good" is not a review and goes back.

## The self-review lens
One list, written once in the roster, applied by the author before the first push, by every reviewer within their lens, and by the architect to every delta: the exact delta; existing behaviour preserved; every caller of a changed shape; every path to an external target; edge values; antipatterns; types and conversions across boundaries; parser differentials; the API standard; audit first for privileged writes; tests that fail when the code breaks; copy consistent with its neighbours; no secrets, identifiers or PII.

`/self-review` runs the lens as a read-only forked review of any diff, PR or range.

## A different model judges
Where you can, the model that reviews a diff is not the one that wrote it. The security review runs on the strongest tier. If you also use another assistant (GitHub Copilot code review, for example), it adds a second model family.

## Findings go back to the owner
A finding goes to the agent that owns the code. The architect never fixes it. A security finding closes only when its pinning test is in the diff and fails without the control.
