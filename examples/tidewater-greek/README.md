# Example: Tidewater Library, greek theme

Tidewater Library is a fictional web app for a community lending library: members borrow books and tools. It has a React 19 + Vite front end (`web/`, en-GB and es-ES), a Node 22 + Fastify API with a hexagonal layout (`api/src/domain`, `http`, `adapters`), Playwright E2E, PostgreSQL 17 in Docker, and GitHub Actions.

These files are what `/init-team` (agent-roundtable 0.1.0) wrote for it: 11 roles (no product manager, no marketing), the greek theme, owner-only push policy, and pre-commit gates for lint, Vitest and tsc in each area.

How to read it:
- `INTERVIEW.md`: the questions asked and the owner's answers, in order.
- `team.config.yaml`: the answers as config; everything else is rendered from it.
- `CLAUDE.md` (the architect, Athena) and `.claude/agents/*.md` (the specialists); then `docs/team-roster.md` for lanes, model routing and the review gate.
- `docs/process/`, `.github/` and `scripts/` are the briefs, Definition of Done, PR and issue templates and git hooks.
- Not included: `docs/conventions/neutral/`, a verbatim copy of `packs/neutral/` in this repo.
