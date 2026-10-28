# Adapters

agent-roundtable is built and tested on **Claude Code**. An adapter records how to run the same team on another AI assistant: where each generated file goes, which features exist, and what is lost.

The team itself is tool-neutral: roles, lanes, review gates, briefs, the Definition of Done, PR and issue templates, and the git hooks are plain Markdown and shell. Only the container for the instructions changes from one assistant to another.

## Status

| Assistant | Adapter | Status |
|---|---|---|
| Claude Code | [claude-code.md](claude-code.md) | **reference**, tested |
| Any assistant that reads `AGENTS.md` | [agents-md.md](agents-md.md) | generic fallback, single assistant |
| GitHub Copilot (VS Code, coding agent) | — | **wanted** |
| Cursor | — | **wanted** |
| OpenAI Codex | — | **wanted** |
| Gemini CLI / Code Assist | — | **wanted** |
| Windsurf | — | **wanted** |
| ChatGPT (projects, no repo access) | — | **wanted** |

Until there is an adapter for your assistant, use the [bootstrap prompt](../prompts/bootstrap.md). It works from the capabilities your assistant reports and drafts the adapter for you.

## What an adapter maps

| agent-roundtable output | Claude Code | Your assistant |
|---|---|---|
| The architect (main session) | `CLAUDE.md` team block | repository-wide instructions |
| Each specialist | `.claude/agents/<name>.md` | a custom agent, mode, or instructions file |
| `description` (auto-routing) | front matter | the agent's summary, if routing exists |
| `model` per agent | front matter | per-agent model, if supported |
| `tools` allowlist (read-only security role) | front matter | tool restrictions, if supported |
| `/self-review`, `/init-team`, `/sync-team` | `.claude/commands/*.md` | reusable prompts or commands |
| Dispatching a specialist | Agent tool (subagent) | how a role is invoked |
| Lanes | prompt rule in each persona | the same, plus path-scoped instructions if supported |
| Roster, process docs, templates, hooks | unchanged | unchanged |

## Contribute an adapter

1. Run the [bootstrap prompt](../prompts/bootstrap.md) with your assistant on a real or sample project. It drafts `adapters/<assistant>.md` at the end.
2. Check the draft against your assistant's **current** official docs, and link them. Formats change; an adapter cites the version it was tested on.
3. Fill in this template:

```markdown
# Adapter: <assistant>

Tested with: <assistant and version>, on <date>. Docs: <links>.

## Capabilities
| Capability | Supported | How |
|---|---|---|
| Separate agents with own instructions | yes / no | |
| Main session can dispatch them | yes / no | |
| Model per agent | yes / no | |
| Tool restrictions per agent | yes / no | |
| Repository-wide instructions | yes / no | path |
| Path-scoped instructions | yes / no | |
| Reusable prompts / commands | yes / no | |
| Runs shell (render.py, hooks) | yes / no | |

## Where each output goes
| Output | Path and format |
|---|---|

## Dispatching a role
<how the owner or the architect invokes a specialist>

## What is lost, and the workaround
<e.g. no independent reviewer: run each review in a fresh chat with only that role>

## Setup steps
<numbered, from an empty repo to a working team>
```

4. Open a PR. Name the assistant and version in the title, and say what you tested (a sample project is fine; never include project details). Run `bash scripts/validate.sh` first. This repo runs no CI.

An adapter that changes how files are rendered (a new output format) can also add a `--target <assistant>` mode to `scripts/render.py`; discuss it in an issue first.
