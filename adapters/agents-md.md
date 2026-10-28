# Adapter: AGENTS.md (generic fallback)

For any assistant that reads a repository-wide `AGENTS.md` and has no separate agents of its own, or whose agent feature has no adapter yet. [AGENTS.md](https://agents.md/) is an open format many coding assistants read; check that yours does.

Status: generic. It describes a pattern, not a tested integration. Prefer a specific adapter when one exists.

## Capabilities assumed
| Capability | Assumed |
|---|---|
| Separate agents | no: one assistant takes one role at a time |
| Model per agent | no |
| Tool restrictions per agent | no |
| Repository-wide instructions | yes: `AGENTS.md` |

## Where each output goes
| Output | Path |
|---|---|
| Architect section + pointer to the roster | `AGENTS.md`, inside an `agent-roundtable:start` / `end` block (the same block the renderer writes into `CLAUDE.md`) |
| Each specialist | `docs/agents/<name>.md` (the persona body; front matter dropped, `description` kept as the first paragraph) |
| Commands | `docs/agents/prompts/{init-team,sync-team,self-review}.md`, used as pasted prompts |
| Everything else | as rendered |

## Dispatching a role
Start a **new chat**, attach or reference `docs/agents/<name>.md`, and say: "Act only as this role. Here is the task brief: …". The architect's chat writes the brief; you carry it across and bring the report back.

## What is lost, and the workaround
- **Independent review.** One assistant writing and reviewing in the same chat grades its own work. Run every review in a fresh chat that has only the reviewer's role file and the diff.
- **Read-only security reviewer.** Nothing enforces it; the role file says so, and you check that the reviewing chat changed no files.
- **Per-role model.** Pick the model by hand when you open the chat, using the tier in `docs/team-roster.md` → *Model routing*.
- **Auto-routing.** You choose the role; the architect section tells the assistant which role owns which path, so it can tell you.
