# Roles

A **role** is one job on the team, defined once in [`roles/`](../roles/). A role says what the agent owns, what it refuses, which tier of model it runs on, and how it reports. A [theme](../themes/README.md) gives it a name.

## Why single-domain agents

A generalist agent that may touch anything will, sooner or later, "fix" something next to its task: a config value, a test it doesn't understand, a string in a language it doesn't speak. Each of those is a small, plausible change that nobody with the right context reviewed.

A single-domain agent has a short system prompt about one thing, a known set of paths, and a reflex to hand everything else over. That gives you:
- **better output**: the prompt is specific, so the agent applies the right standards;
- **reviewable work**: you know whose judgement each change reflects;
- **cheaper runs**: a narrow agent can often use a cheaper model.

## The architect writes no code

The architect is the main Claude Code session. It designs (a design brief with contracts on the work item), routes (a task brief to the owning agent), and reviews (every return, against the self-review lens). It writes nothing in the repo, not even a one-line fix.

This sounds wasteful until you see what it prevents. An orchestrator that also writes code reviews its own work, drifts into implementation detail, and fills its context with file dumps. One that only designs and reviews keeps its context for the whole picture and treats every return with fresh eyes.

## The roles

| Role | Owns | Reviews |
|---|---|---|
| Architect | nothing in the repo: design briefs, routing, review | every return and every delta |
| Product owner | backlog, specs, planning | plan alignment, every PR |
| Product manager | discovery, product docs | product behaviour, pricing, claims |
| Security and privacy | nothing: read-only strategies and verdicts | security and data protection, every PR |
| QA lead | E2E journeys, test docs | test quality, every code PR |
| Front-end | front-end code | usability walk on UI changes |
| Domain back-end | the domain core and ports | contracts it consumes |
| Application back-end | endpoints, adapters, composition, API contracts | contracts it consumes |
| Infra and DevOps | infra, pipelines, hooks, scripts | infra impact |
| Docs | handbook, user guides, architecture docs | docs delta on behaviour changes |
| Copy and i18n | every user-facing word, every language | language in the usability walk |
| Marketing | marketing plans | — |
| Ways-of-working steward | the roster, personas, templates, process docs | — |

Every role except the architect is optional. With a role disabled, its lanes go to another role you choose, or stay with the owner, and the review gates that name it are dropped.

## Agents never push or merge

Specialists commit their own work on their own branch, each commit green. They never push, open PRs or merge. Depending on `conventions.push_policy`, either the owner pushes and opens PRs, or the architect does and merges only on the owner's explicit "merge #N". **The owner approves at merge**, always.
