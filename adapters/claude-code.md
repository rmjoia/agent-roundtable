# Adapter: Claude Code (reference)

Tested with: Claude Code, October 2026. Docs: [subagents](https://code.claude.com/docs/en/sub-agents), [slash commands](https://code.claude.com/docs/en/slash-commands), [memory (CLAUDE.md)](https://code.claude.com/docs/en/memory).

This is the target the framework renders natively; use `/init-team` rather than the bootstrap prompt.

## Capabilities
| Capability | Supported | How |
|---|---|---|
| Separate agents with own instructions | yes | `.claude/agents/<name>.md` |
| Main session can dispatch them | yes | the Agent tool, `subagent_type: <name>` |
| Model per agent | yes | `model:` front matter; overridable per dispatch |
| Tool restrictions per agent | yes | `tools:` allowlist (or `disallowed-tools`) |
| Repository-wide instructions | yes | `CLAUDE.md` |
| Path-scoped instructions | partly | nested `CLAUDE.md` files in subfolders |
| Reusable prompts / commands | yes | `.claude/commands/*.md` |
| Runs shell (render.py, hooks) | yes | Bash tool, with permission |

## Where each output goes
| Output | Path and format |
|---|---|
| Architect | `CLAUDE.md`, between `agent-roundtable:start` and `end` |
| Specialists | `.claude/agents/<name>.md` |
| Commands | `.claude/commands/{init-team,sync-team,self-review}.md` |
| Everything else | as rendered |

## Dispatching a role
The architect dispatches with a task brief (`docs/process/task-brief.md`) through the Agent tool. You can also ask directly: "Have Heimdall review PR #12."

## What is lost
Nothing; this is the reference. Subagents draw on the same usage limits as the main session: see [requirements and cost](../docs/requirements.md).
