# Bootstrap prompt: set up agent-roundtable with any AI assistant

Paste everything below the line into your assistant (GitHub Copilot Chat in agent mode, ChatGPT, Cursor, Gemini, Codex, Windsurf …) with your project open, or attached, if it can read files. Fill in the first line.

The prompt makes the assistant read this repo, interview you, and set up the team in whatever form your assistant supports. It ends by drafting an **adapter** for your assistant; please [contribute it back](../adapters/README.md#contribute-an-adapter) so the next person gets a tested setup.

---

```text
My assistant is: <name and version, e.g. "GitHub Copilot Chat in VS Code, agent mode">.

You are setting up "agent-roundtable" in my project: a team of single-domain AI
specialists, plus an architect that designs, routes and reviews but writes no code.
The framework lives at https://github.com/rmjoia/agent-roundtable (latest release tag).
If my workspace has a .roundtable/ folder, read the framework from there instead.

READ FIRST, in this order (fetch from
https://raw.githubusercontent.com/rmjoia/agent-roundtable/main/<path> if you can't
read my workspace copy):
  1. adapters/README.md, and adapters/<my assistant>.md if it exists
  2. .claude/commands/init-team.md      (the interview and the outputs: the specification)
  3. roles/README.md and roles/*.md     (the 13 roles; only the architect is required)
  4. themes/README.md                   (names: neutral, arthurian, greek, roman, norse,
                                         egyptian, astronomy, or my own)
  5. team.config.schema.yaml and team.config.example.yaml
  6. templates/team-roster.md.tmpl      (the rules every agent carries)
If you cannot read these files at all, say so and stop. Never reconstruct them
from memory.

STEP 1: CAPABILITIES. Before asking me anything, state in a short table what you
(this assistant, in this environment) can and cannot do, without guessing:
  - read and write files in my repo; run shell commands (python3, git)
  - separate agents/sub-assistants with their own instructions (and can you call them?)
  - choose a model per agent
  - restrict an agent's tools (e.g. read-only)
  - a repository-wide instructions file (and its path)
  - path-scoped instructions; reusable prompts or commands
If an adapter file exists for you, use its mapping and tell me where reality differs.

STEP 2: INTERVIEW. Run the interview in init-team.md Step 3: ONE question per
message, offering defaults detected from my repo. Never ask for a person's name;
the owner is a role. Then show me the complete team.config.yaml and wait for OK.

STEP 3: RENDER.
  - If you can run python3 with PyYAML: run
      python3 -I scripts/render.py --framework <framework dir> --repo . \
        --config team.config.yaml --out <scratch dir>
    (scripts/render.py lives in .roundtable/scripts/ in an installed project).
  - Otherwise render by hand, following init-team.md Step 4 and roles/README.md.
  The tool-neutral outputs are the same for every assistant and are kept as they are:
  team.config.yaml, docs/team-roster.md, docs/process/*, docs/conventions/*,
  .github/PULL_REQUEST_TEMPLATE.md, .github/ISSUE_TEMPLATE/*, scripts/git-hooks/*.

STEP 4: MAP TO MY ASSISTANT. The renderer writes Claude Code files:
  - CLAUDE.md team block   = the architect's instructions (main session)
  - .claude/agents/<name>.md = one specialist each (front matter: name, description,
                               model, optional tools allowlist; body: the persona)
  Translate them into my assistant's equivalents, following the adapter if there is
  one. Rules for the translation:
  - Keep every persona's content (lane, refuse-and-delegate, gates, report format,
    shared rules). Only the container changes.
  - If I have no separate agents: put the architect section and the roster in my
    assistant's repository-wide instructions file (AGENTS.md if nothing better
    exists), and write each specialist to its own instructions file that I attach or
    select when I want that role. Tell me plainly that reviews are then not
    independent: I should run each review in a fresh chat with only that role.
  - If I can't pick a model per agent or restrict tools: drop those fields and list
    what was lost.
  - Never invent a feature my assistant doesn't have.

STEP 5: SHOW, THEN WRITE. List every file you will create or change, with a diff for
existing files. Leave everything in an existing instructions file outside the
agent-roundtable block untouched. Write only after I say yes.
Never commit, push, merge or install anything without asking.

STEP 6: CONTRIBUTE BACK. Draft adapters/<my-assistant>.md following the template in
adapters/README.md: the capability table from Step 1, where each output went, what
was lost, and how I dispatch a role. Save it to my scratch space, not my repo, and
tell me how to open a PR with it against rmjoia/agent-roundtable.

The non-negotiables, whatever my assistant can do: one domain per agent; the
architect writes no code; contracts before parallel work; every commit green;
agents never push or merge, I approve at merge; every report ends with
"## Feedback".
```
