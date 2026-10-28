# Example: Harbour Ledger (norse theme)

Harbour Ledger is a fictional product: invoicing and berth booking for small marinas, for harbour masters and marina office staff. Its stack is a .NET 9 back end (`backend/`: Core, Api, EF Core Data, two test projects), an Angular 19 front end (`frontend/`, with Playwright in `frontend/e2e/` and `en-GB` + `nb-NO` strings), Bicep in `infra/` and GitHub Actions.

This folder is what `/init-team` wrote into that project, with all 13 roles enabled, the `norse` theme and the `architect-on-merge-approval` push policy. Only the generated files are here, not the application code.

How to read it:
- Start with [INTERVIEW.md](INTERVIEW.md) (the questions and answers), then [team.config.yaml](team.config.yaml), the single input to the render.
- [CLAUDE.md](CLAUDE.md) shows the team block appended below a hand-written project note; [docs/team-roster.md](docs/team-roster.md) is the lane and review table; `.claude/agents/` holds one persona per role (the architect, Odin, lives in `CLAUDE.md`).
- `docs/conventions/` is not copied here: it is the `neutral` and `dotnet-angular` packs verbatim, already in [`packs/`](../../packs/).
