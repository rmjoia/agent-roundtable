# Contributing

PRs are welcome: role fixes, new public-domain themes, stack packs, better templates and docs.

## Before you start
- For anything beyond a typo, open an issue first and say what problem it solves.
- Every PR needs a review from the maintainer (`.github/CODEOWNERS`) before it merges.
- **This repo runs no GitHub Actions.** Run the checks locally before you open the PR:
  ```bash
  bash scripts/validate.sh     # roles, themes, configs, examples, shell syntax, scrub check
  ```
  `validate.sh` needs Python 3 with PyYAML (`jsonschema` too, if you have it).

## Rules for each kind of change

**A role change** (`roles/*.md`)
- Give the rationale: the failure it prevents, ideally a retro finding from a real project (paraphrased; no project details).
- Keep the role single-domain. A change that makes two roles own the same path, or makes the architect write in the repo, won't be accepted.
- Bump the role's `version` and add a CHANGELOG line. Adopters see both in `/sync-team`.
- If a template placeholder changes, update `roles/README.md` and `.claude/commands/init-team.md` in the same PR.

**A theme** (`themes/*.yaml`)
- Every name must come from a **public-domain source**; cite it in `source:`.
- No franchise names (film, TV, games, modern books), no living people, no trademarks.
- One name per role, unique within the theme; one-sentence flavour that sets tone and never changes the role.

**A pack** (`packs/<stack>/`)
- Layer on `neutral`; don't contradict it.
- Each rule is checkable and cites its upstream guide.
- No project-specific rules.

**Templates and commands** (`templates/`, `.claude/commands/`)
- Re-generate the examples if the output changes (run `/init-team --rerender` in a copy of each example's sample project, or ask in the PR and a maintainer will).
- Rendering must stay idempotent: the same config renders the same files.

## Contributing from your own project

If an improvement came out of your team's retro, see [docs/sync.md → Upstream](docs/sync.md#upstream-your-project--template). In short: keep only the generic part, map your theme names back to role ids, and **run the scrub check**. Put your product name, domains and people's names in a git-ignored `.scrub-patterns.local` (one regex per line); `scripts/scrub-check.sh --history` must come back clean.

## Commits
Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:` …), one logical change per commit. If an agent wrote the commit, add the trailer `Agent: <name> (<model>)`.

## Conduct
This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
