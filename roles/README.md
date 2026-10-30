# Role templates

Each file here is one **canonical role**. A role is a job on the team: what it owns, what it refuses, how it reports. A role has no name. Names come from a [theme](../themes/README.md).

`/init-team` takes each role you enable, combines it with your theme and `team.config.yaml`, and writes `.claude/agents/<name>.md`. The architect is the exception: it is the main Claude Code session, so it is written into the team section of `CLAUDE.md` instead of an agent file.

| Role id | Title | Required | Default tier | Writes in the repo |
|---|---|---|---|---|
| `architect` | Architect and orchestrator | **yes** | strong | nothing: designs, routes and reviews |
| `product-owner` | Product owner | no | strong | backlog, specs, planning ledgers |
| `product-manager` | Product manager | no | strong | discovery notes, product docs |
| `security` | Security and privacy champion | no | strongest | nothing: strategies and verdicts only |
| `qa` | QA lead | no | strong | E2E journeys, test docs |
| `frontend` | Front-end engineer | no | strong | front-end code and its tests |
| `backend-domain` | Domain back-end engineer | no | strong | the domain core, ports and their tests |
| `backend-app` | Application back-end engineer | no | strong | adapters, endpoints, composition |
| `devops` | Infra and DevOps | no | strong | infra, pipelines, hooks, scripts |
| `docs` | Documentation | no | balanced | the solution documentation |
| `copy` | Copy and i18n | no | strong | user-facing text in every language |
| `marketing` | Marketing | no | strong | marketing plans |
| `steward` | Ways-of-working steward | no | balanced | the team's rules, personas, templates |

## File format

Front matter (YAML), then a Markdown body with placeholders.

```yaml
---
id: frontend                  # stable identifier; never rename
title: Front-end engineer
version: 1                    # bump when the body changes meaningfully; /sync-team reads it
required: false
default_tier: strong          # fast | balanced | strong | strongest
read_only: false              # true → the agent gets a read-only tool allowlist
default_lanes:                # path globs; "!" excludes; {{paths.x}} resolves from team.config.yaml
  - "{{paths.frontend}}/**"
  - "!{{paths.i18n}}/**"
hands_over:                   # role id → what goes to it; "*" → a full sentence ("… goes to its owner")
  copy: wording and translations
tagline: "Front-end code: ..."  # one line for the roster and CLAUDE.md lists
summary: >-                   # the agent's `description` (drives auto-routing); starts with the title
  Front-end engineer: owns the front-end code ... Wording goes to {{role:copy}}.
---
```

## Placeholders in the body

| Placeholder | Resolves to |
|---|---|
| `{{name}}` / `{{Name}}` | the agent's slug / display name from the theme |
| `{{flavour}}` | the theme's one-line flavour for this role |
| `{{project}}` | `project.name` |
| `{{owner}}` | `owner.title` (a role label such as "Owner", never a person) |
| `{{lanes}}` | the role's lane globs as a bullet list |
| `{{personality}}` | the theme's optional personality for this role (a working trait and an off-duty love); with none, the *Your personality* section is dropped |
| `{{hands_over}}` | the hand-over list, each target rendered as its themed name |
| `{{gates}}` | the pre-commit gates whose paths overlap this role's lanes |
| `{{trailer}}` | the commit trailer, e.g. `Agent: hermes (opus)` |
| `{{role:<id>}}` | the themed display name of another role (or "the owner" if that role is disabled) |
| `{{stack.<layer>}}` | the stack entry for that layer |
| `{{paths.<key>}}` | a path from `paths:` in `team.config.yaml` (used in lanes) |
| `{{i18n.languages}}` / `{{i18n.source}}` | the language list / source language |
| `{{shared_rules}}` | the fixed pointer to *Rules every persona carries* (see `templates/shared-rules.md`) |
| `{{push_policy}}` | the paragraph for `conventions.push_policy` (architect only) |

Rendering is done by [`scripts/render.py`](../scripts/render.py), which is the specification: `{{owner}}` is capitalised at the start of a sentence, list item or table cell; a lane whose `{{paths.x}}` is unset or `none` is dropped; an exclusion outside every included path is dropped; a hand-over to a disabled role goes to the owner. In review gates, the reviewer `consumer` means the agent that consumes the changed contract.

Other front-matter keys: `tier_floor` (the tier is never set lower, used by `security`), `renders_to: claude-md` (the architect goes into `CLAUDE.md`, not an agent file).

A line that mentions only a disabled role is dropped. A hand-over to a disabled role goes to the owner as a gap.

## Changing a role

A role change affects every project that adopts the template. See [CONTRIBUTING.md](../CONTRIBUTING.md): state the problem it fixes (ideally a retro finding), keep the role single-domain, and bump `version`.
