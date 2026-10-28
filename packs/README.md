# Packs

A pack is a set of coding conventions the agents follow. `/init-team` copies the packs you choose into `docs/conventions/<pack>/` in your project and points `CLAUDE.md` and the personas at them.

| Pack | For | Contents |
|---|---|---|
| `neutral` | any stack | Definition of good code, contracts, API errors (RFC 9457), testing, security (OWASP), accessibility |
| `dotnet-angular` | .NET back end, Angular front end | stack conventions layered on `neutral` |

Always include `neutral`. A stack pack adds to it and never contradicts it; where a stack pack is more specific, it wins.

## Write a stack pack

Create `packs/<stack>/` with a `README.md` and one file per concern (`backend.md`, `frontend.md`, `testing.md`, …). Each rule should be checkable: name the tool, the lint rule or the pattern, and cite the upstream guide it comes from. Keep project-specific rules in your project, not in a pack.
