# /init-team interview: Harbour Ledger

A fictional run of `/init-team` (template 0.1.0). Q is the session, one question per message; A is the owner.

**Found first:** a .NET 9 solution in `backend/` (Core, Api, Data, two test projects; EF Core with Npgsql), Angular 19 in `frontend/` with Karma, Playwright in `frontend/e2e/`, translations `en-GB` and `nb-NO` in `frontend/src/assets/i18n/`, Bicep in `infra/`, GitHub Actions, Conventional Commits on `main`. A hand-written `CLAUDE.md` and PR template exist; no issue templates or git hooks; no `team.config.yaml`.

## Project
1. **Q:** Project name and one line on what it does and for whom? *(detected: Harbour Ledger)* **A:** Harbour Ledger: invoicing and berth booking for small marinas, for harbour masters and marina office staff.
2. **Q:** Law and standards that apply? *(Recommended: GDPR, EU consumer law, WCAG 2.2 AA, EN 16931 e-invoicing)* **A:** Accept.

## Stack
3. **Q:** Front end? *(detected: Angular 19 + TypeScript)* **A:** Accept.
4. **Q:** Back end? *(detected: .NET 9, ASP.NET Core minimal API)* **A:** Accept.
5. **Q:** Database? *(detected: PostgreSQL via EF Core)* **A:** Accept.
6. **Q:** Cloud or hosting? *(detected: Azure, Bicep)* **A:** Accept.
7. **Q:** CI? *(detected: GitHub Actions)* **A:** Accept.
8. **Q:** Unit test runner? *(detected: xUnit for the back end, Karma + Jasmine for the front end)* **A:** Accept.
9. **Q:** E2E runner? *(detected: Playwright)* **A:** Accept.

## Roles and lanes
10. **Q:** Which of the 13 roles to enable? *(Recommended for this stack: all but product-manager and marketing)* **A:** All 13.
11. **Q:** Product owner lanes: `docs/specs/**`, `docs/planning/**` (no specs folder yet; `docs/specs` proposed). Accept, or edit? **A:** Accept.
12. **Q:** Product manager: `docs/product/**`? **A:** Accept.
13. **Q:** Security: read-only, no lanes? **A:** Accept.
14. **Q:** QA: `frontend/e2e/**`, `docs/testing/**`? **A:** Accept.
15. **Q:** Front end: `frontend/**` except `frontend/src/assets/i18n/**` and `frontend/e2e/**`? **A:** Accept.
16. **Q:** Domain back end: `backend/src/HarbourLedger.Core/**`, `backend/tests/HarbourLedger.Core.Tests/**`? **A:** Accept.
17. **Q:** Application back end: `backend/src/HarbourLedger.Api/**`, `backend/src/HarbourLedger.Data/**`, `backend/tests/HarbourLedger.Api.Tests/**`, `contracts/**`? **A:** Accept.
18. **Q:** DevOps: `infra/**`, `.github/workflows/**`, `.github/actions/**`, `scripts/**`, `.github/dependabot.yml`, `.github/CODEOWNERS`? **A:** Accept.
19. **Q:** Docs: `docs/handbook/**`, `docs/user-guide/**`, `docs/architecture/**`? **A:** Accept.
20. **Q:** Copy: `frontend/src/assets/i18n/**` (no e-mail templates found, so that lane is dropped)? **A:** Accept.
21. **Q:** Marketing: `docs/marketing/**`? **A:** Accept.
22. **Q:** Steward: the roster, `.claude/**` agents, commands and skills, `CLAUDE.md`, PR and issue templates, `docs/process/**`, `team.config.yaml`, …? **A:** Accept.
23. **Q:** Lane check: no overlaps. Unowned: `backend/HarbourLedger.sln`, `docs/README.md`, and `docs/conventions/**` (the packs this command will copy). How to resolve? *(Recommended: the .sln to the application back end, `docs/README.md` to docs, `docs/conventions/**` to the steward)* **A:** Accept.

## Theme, models, review
24. **Q:** Theme? neutral (Architect · Security · Frontend), arthurian (Arthur · Bors · Galahad), greek (Athena · Argus · Iris), roman (Vitruvius · Horatius · Ovid), norse (Odin · Heimdall · Baldr), egyptian (Imhotep · Wadjet · Hathor), astronomy (Polaris · Sirius · Vega), or your own. **A:** norse.
25. **Q:** Model tiers: docs and steward `balanced`, security `strongest` (floor), the rest `strong`; map fast haiku, balanced sonnet, strong opus, strongest opus. Accept? **A:** Accept.
26. **Q:** Review gates: architecture and contract (architect, always), security (always), plan alignment (product owner, always), test quality (QA, code), docs (behaviour), usability (front end + copy, UI), product (product manager, product), contract (the consumer: front end or application back end, contract), infra (DevOps, infra). Accept? **A:** Accept.

## Languages, conventions, gates
27. **Q:** Languages and source? *(detected: en-GB, nb-NO; source en-GB)* **A:** Accept.
28. **Q:** Conventions: Conventional Commits, branch `<type>/<issue>-<slug>`, size 800 lines / 25 files soft, 1500 / 40 hard? **A:** Accept.
29. **Q:** Push policy: `owner-only` (Recommended) or `architect-on-merge-approval`? **A:** architect-on-merge-approval.
30. **Q:** Pre-commit gates (from `packs/dotnet-angular/gates.md`; paths already `backend/` and `frontend/`): backend build and test, frontend lint, build and test. Accept, or edit? **A:** Accept.
31. **Q:** Packs: `neutral` (always) plus `dotnet-angular` (matches)? **A:** Accept.
32. **Q:** Retro cadence? *(default weekly)* **A:** Fortnightly.
33. **Q:** Here is the complete `team.config.yaml`. OK, or what to change? **A:** OK.

## Existing files and the diff
- `CLAUDE.md` has no marker: the team block is appended below the five hand-written lines (no question; the command says insert).
34. **Q:** `.github/PULL_REQUEST_TEMPLATE.md` was written by people (What / How tested). Replace, keep yours, or write ours as `.roundtable` for a manual merge? **A:** Replace.
35. **Q:** Summary: 33 new, 2 changed (`CLAUDE.md`, the PR template), full diff shown. Write these files, change something, or cancel? **A:** Write these files.

Checks after writing: front matter parses, no `{{` left, `bash -n` passes on the hooks, roster lanes match the personas. `/init-team --rerender` then produced no changes.
