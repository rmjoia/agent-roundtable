# agent-roundtable

**A Claude Code engineering team for any project: single-domain specialist agents, an architect that designs and reviews but writes no code, and the review gates, contracts and retros that keep them honest.**

Run `/init-team` in Claude Code. It interviews you about your project, one question at a time, and generates the team: agent personas, a roster with lanes and review gates, a `CLAUDE.md` section, PR and issue templates, brief formats and a pre-commit hook.

## The idea

- **One domain per agent.** Each specialist owns a set of paths and refuses everything else: it hands the work to the owning agent instead of "just fixing it".
- **The architect writes no code.** Your main session designs the solution and its contracts, routes work to the owner, and reviews every return. It keeps its context for the whole picture.
- **Contract first.** An interface between two lanes gets a versioned contract before either side builds, so lanes run in parallel.
- **Every commit is green.** Agents run the gates before each commit and sign it with an `Agent:` trailer. Agents never push or merge: **you approve at merge**.
- **Reviews challenge, never nod.** Security, test quality, plan alignment, docs and usability gates, each with a lens.
- **The team improves itself.** Every report ends with `## Feedback`. A retro turns it into persona and template fixes.

It is extracted from a system running in production and generalised. Roles are canonical; names are a theme.

> **Requirements:** Claude Code with a Claude subscription, an Anthropic API account or a supported cloud provider, and Python 3 with PyYAML for the renderer (without it, `/init-team` renders by hand). The team runs on **subagents**, and they draw on your usage limits. A plan with generous limits (Max, Team, Enterprise) or API billing is recommended for daily use. See [requirements and cost](docs/requirements.md).

---

## Set it up in a new project (5 minutes)

1. Click **Use this template** on GitHub. Or, for an existing repo, see the next section.
2. Open Claude Code in the project.
3. Run **`/init-team`** and answer the interview. Defaults come from your repo; say "defaults" at any point to accept the rest.
4. Review the generated diff, accept it, and commit it. Then run `bash scripts/install-hooks.sh` and restart Claude Code so the agents load.

Then talk to the architect as usual: *"Add order cancellation."* It writes a design brief, dispatches the right agents, and reviews what they bring back.

## Bring it to an existing project

`/init-team` is built for existing code. It reads your repo first (manifests, folders, translation files, commit style, existing templates and hooks) and proposes lanes from what is there.

**1. Copy the framework in.** Pick one:

```bash
# a) The install script: copies roles/, themes/, templates/, packs/ into .roundtable/
#    and the three commands into .claude/commands/. It never overwrites a file of yours.
git clone --depth 1 https://github.com/rmjoia/agent-roundtable /tmp/agent-roundtable
bash /tmp/agent-roundtable/scripts/install.sh /path/to/your-project

# b) Just the command: /init-team offers to fetch the rest into .roundtable/ when it runs.
mkdir -p .claude/commands
curl -fsSL -o .claude/commands/init-team.md \
  https://raw.githubusercontent.com/rmjoia/agent-roundtable/main/.claude/commands/init-team.md
```

**2. Work on a branch:** `git switch -c chore/agent-team`.

**3. Run `/init-team`.** What it does with what you already have:

| You already have | It does |
|---|---|
| `CLAUDE.md` | adds a marked team section and leaves everything else alone |
| PR or issue templates | shows yours next to ours; you choose per file: replace, keep, or write ours alongside |
| Git hooks | offers to keep each existing check as a gate; never drops one silently |
| Agents in `.claude/agents/` | asks before replacing a hand-written persona; its project-specific content can move into the persona's local block |
| Folders no role owns | lists them and asks who owns them |

**4. Review the diff and commit.** Nothing is written before you approve, and nothing is committed or pushed for you.

**5. Start small.** On an existing codebase, enable the architect, security, QA and the one or two builders that match your stack first. Add roles later by editing `team.config.yaml` and re-running `/init-team`.

## Use it with another assistant

Built for Claude Code, but the team is plain Markdown and shell, so it can run elsewhere. Paste the **[bootstrap prompt](prompts/bootstrap.md)** into GitHub Copilot Chat, ChatGPT, Cursor, Gemini or any assistant that can read files. It reads this repo, checks what your assistant can actually do (separate agents, per-agent models, tool limits), runs the same interview, and maps the team onto your assistant. Where your assistant has no separate agents, it falls back to role files you open one chat at a time, and says what is lost.

At the end, it drafts an **adapter** for your assistant. Please PR it back: see [adapters/](adapters/README.md) for the template and the assistants we'd love adapters for.

## What you get

```
your-project/
├── team.config.yaml               # your answers; the source for every generated file
├── CLAUDE.md                      # + the team section (the architect's instructions)
├── .claude/agents/<name>.md       # one persona per enabled role
├── docs/team-roster.md            # lanes, routing, review gates, rules every persona carries
├── docs/process/                  # task, review and decision briefs; Definition of Done
├── docs/conventions/              # the coding-convention packs you chose
├── .github/PULL_REQUEST_TEMPLATE.md   # Agents, Docs, Affects open issues, Impacted tests, Handoff
├── .github/ISSUE_TEMPLATE/        # story, task, bug, retro log
└── scripts/git-hooks/             # pre-commit gates + secret scan, Conventional Commits check
```

See it before you run it: [`examples/`](examples/) holds real `/init-team` output for two fictional projects:
- [`tidewater-greek`](examples/tidewater-greek/): React + Fastify, Greek theme, owner-only pushes;
- [`harbour-norse`](examples/harbour-norse/): .NET + Angular, Norse theme, all 13 roles.

## The roles

Architect (required) · product owner · product manager · security and privacy champion · QA lead · front-end · domain back-end · application back-end · infra and DevOps · docs · copy and i18n · marketing · ways-of-working steward. Details: [docs/roles.md](docs/roles.md) and [`roles/`](roles/).

## Pick a theme

Names make the team easier to talk to ("send it to Heimdall"). They don't change what a role does.

| Theme | Architect · Security · Front end |
|---|---|
| `neutral` | Architect · Security · Frontend |
| `arthurian` | Arthur · Bors · Galahad |
| `greek` | Athena · Argus · Iris |
| `roman` | Vitruvius · Horatius · Ovid |
| `norse` | Odin · Heimdall · Baldr |
| `egyptian` | Imhotep · Wadjet · Hathor |
| `astronomy` | Polaris · Sirius · Vega |

**Your own theme:** put a YAML file in `themes/local/` and choose it in the interview. See [themes/README.md](themes/README.md).

**Why no Star Wars, Star Trek, Game of Thrones or Lord of the Rings?** Those names are trademarks and copyrighted characters. An open-source template shouldn't hand that risk to everyone who adopts it, so every shipped theme comes from public-domain sources. What you put in your own private `themes/local/` is your call.

## Keep it updated

Run **`/sync-team`**. It fetches the latest template release, summarises what changed, re-renders your team from `team.config.yaml` (keeping your names, lanes and each persona's local block), and shows the diff before writing. A [workflow template](templates/workflows/sync-team.yml) can do it weekly as a PR. See [docs/sync.md](docs/sync.md).

## Contribute back

Found a better rule in your retro? The upstream flow maps your theme names back to roles, scrubs anything project-specific, and opens a PR against this template. It is designed in [docs/sync.md](docs/sync.md#upstream-your-project--template). You can also do it by hand: see [CONTRIBUTING.md](CONTRIBUTING.md).

## FAQ

**What does it cost?**
Each specialist is a subagent run, and a reviewed change runs several. Every role names a tier (`fast`, `balanced`, `strong`, `strongest`); you map tiers to models in `team.config.yaml`. The rule is the cheapest tier that gets the task right first time: rework costs more than a stronger model. Security reviews stay on the strongest tier. Log the tier per dispatch on the retro issue and adjust. More in [requirements and cost](docs/requirements.md).

**Can I use it without some roles?**
Yes. Only the architect is required. A disabled role's paths go to another role you choose, or stay with you; review gates that name it are dropped; hand-overs to it go to you. A two-person project might run architect, security, QA and one full-stack builder (`backend-app` with wider lanes).

**Can I use it with GitHub Copilot or other agents?**
Yes: start with the [bootstrap prompt](prompts/bootstrap.md) and the [adapters](adapters/README.md). Beyond that, a mixed team works too. The roster, briefs, lanes and gates are plain Markdown, so any agent or human can follow them. Point `.github/copilot-instructions.md` or `AGENTS.md` at `docs/team-roster.md`; a human or another assistant takes a lane like any agent and follows the same review gate. Copilot code review makes a useful extra reviewer: a different model family on the same diff.

**Does it need GitHub?**
The issue and PR templates, labels and the backlog-as-shared-state flow assume GitHub. The agents, lanes, hooks and briefs work with any Git host; adapt the templates.

**Will it push or merge for me?**
Never without you. Specialists only commit. With `push_policy: owner-only` (the default), you push and merge. With `architect-on-merge-approval`, the architect pushes and opens PRs, and merges only on your explicit "merge #N".

**Does this repo run GitHub Actions?**
No. Actions are disabled here, and the workflow files ship as inert templates under `templates/workflows/`. Validate changes locally with `scripts/validate.sh`.

## Repository layout

| Path | What |
|---|---|
| `roles/` | the 13 canonical role templates |
| `themes/` | public-domain name sets; `themes/local/` for yours |
| `packs/` | coding conventions: `neutral`, plus a `.NET + Angular` example |
| `templates/` | the files `/init-team` renders: roster, CLAUDE section, PR/issue templates, briefs, hooks, workflow templates |
| `.claude/commands/` | `/init-team`, `/sync-team`, `/self-review` |
| `team.config.schema.yaml` | the config schema; `team.config.example.yaml` is an annotated example |
| `docs/` | one page per concept |
| `examples/` | generated output for two fictional projects |
| `prompts/` | the bootstrap prompt for other assistants |
| `adapters/` | how the team maps onto each assistant; contributions welcome |
| `scripts/` | `render.py` (the renderer `/init-team` uses), `install.sh`, `validate.sh`, `scrub-check.sh` |

## Support

If agent-roundtable saves your team time, you can [sponsor its development](https://github.com/sponsors/rmjoia). Issues, PRs and new public-domain themes help just as much.

## License

[Apache-2.0](LICENSE). Contributions welcome: see [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Security issues: [SECURITY.md](SECURITY.md).
