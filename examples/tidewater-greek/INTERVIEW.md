# /init-team interview: Tidewater Library

A fictional owner answers `/init-team` (agent-roundtable 0.1.0). One question per message; **Q** is the command, **A** the owner.

**Step 0.** No `roles/architect.md` at the root and no `.roundtable/`.
- **Q:** The framework files are missing. Fetch them from github.com/rmjoia/agent-roundtable into `.roundtable/`? — **A:** Yes. *(Copied with `scripts/install.sh`.)*

**Step 1.** No `team.config.yaml`; none of the output files exist.

**Step 2.** *Found:* `web/` (React 19 + TypeScript + Vite, `react-i18next`, locales `en-GB`, `es-ES`), `api/` (Node 22 + Fastify + TypeScript, `pg`; `src/domain`, `src/http`, `src/adapters`, `test/domain`, `test/http`), `e2e/` (Playwright), `contracts/`, `infra/` (Dockerfile, Compose with PostgreSQL 17), GitHub Actions CI, `docs/`. Conventional Commits; branch `main` only; no CLAUDE.md, templates or hooks.

| # | Question | Answer |
|---|---|---|
| 1a | Project name and one line on what it does and for whom? | Tidewater Library: a web app for a community lending library, where members borrow books and tools. |
| 1b | Law and standards? Default (EU members, personal data, public web app): GDPR, ePrivacy, WCAG 2.2 AA | Accept. |
| 2 | Front end: React 19 + TypeScript + Vite (detected)? | Accept. |
| 2 | Back end: Node.js 22 + Fastify + TypeScript (detected)? | Accept. |
| 2 | Database: PostgreSQL 17 (detected in Compose)? | Accept. |
| 2 | Cloud or hosting: nothing detected beyond a Dockerfile. "any container host" (Recommended), or name one? | Any container host. |
| 2 | CI: GitHub Actions (detected)? | Accept. |
| 2 | Unit test runner: Vitest (detected)? | Accept. |
| 2 | E2E runner: Playwright (detected)? | Accept. |
| 3 | Which roles? (13 listed; default all) | All except product-manager and marketing. |
| 4 | Lanes, one question per role (Hestia `docs/planning/**`, no specs folder found; Argus none; Nemesis `e2e/**`, `docs/testing/**`; Iris `web/**` except `web/src/locales/**`, `e2e/**`; Atlas `api/src/domain/**`, `api/test/domain/**`; Hephaestus `api/src/http/**`, `api/src/adapters/**`, `api/test/http/**`, `contracts/**`; Hermes infra, workflows, `scripts/**`; Clio `docs/handbook|user-guide|architecture/**`; Calliope `web/src/locales/**`; Themis team files) | Accept each. |
| 4 | Unowned: `api/src/server.ts`, `api/package.json`, `api/tsconfig.json`, `docs/architecture.md`, `README.md`, `.gitignore`, `.roundtable/**`, and the `docs/conventions/**` about to be written. No overlaps. Who owns them? | API files → Hephaestus; `docs/architecture.md`, `README.md` → Clio; `.gitignore` → Hermes; `docs/conventions/**`, `.roundtable/**` → Themis. |
| 5 | Theme? neutral (Architect · Security · Frontend), arthurian (Arthur · Bors · Galahad), greek (Athena · Argus · Iris), roman, norse, egyptian, astronomy, or my own | greek. |
| 6 | Tiers: strong → opus for all, docs and steward balanced → sonnet, security strongest → opus (floor). Map fast haiku, balanced sonnet, strong opus, strongest opus. Accept? | Accept; opus is the strongest on the plan. |
| 7 | Review gates: architecture and contract (architect), security, plan alignment (product owner), test quality (QA, code), docs (behaviour), usability (front end + copy, UI), contract (the consumer), infra (devops). Product gate dropped (no product manager). Accept? | Accept. |
| 8 | Languages: en-GB and es-ES (detected), source en-GB? | Accept. |
| 9a | Conventional Commits, branch `<type>/<issue>-<slug>`, size 800 / 25 soft, 1500 / 40 hard? | Accept. |
| 9b | Push policy: owner-only (Recommended) or architect-on-merge-approval? | owner-only. |
| 10 | Gates, per area: `web`: `npm run lint`, `npx vitest run`, `npx tsc -b`; `api`: `npm run lint`, `npx vitest run`, `npm run build` (tsc). Accept or edit? | Accept. |
| 11 | Packs: neutral (always). No matching stack pack (only dotnet-angular ships). | neutral. |
| 12 | Retro cadence: weekly? | Weekly. |
| — | Here is the full `team.config.yaml`. OK? | OK. |

**Step 5.** 29 new files, 0 changed. Lane table: no overlaps, no unowned paths. — **Q:** Write these files, change something, or cancel? — **A:** Write these files.

**Step 6.** Front matter parses for all 10 agents; no `{{` left; `bash -n` passes on the hooks; roster lanes match the personas. Hooks not installed, nothing committed.

**Re-run** `/init-team --rerender`: 0 files changed.
