# Definition of good code: right first time

Every agent and contributor writes code that meets this bar **as it is written**. Review and CI are a safety net, not the fixer: a fix found there means writing it twice. Read the surrounding code and the relevant standard **before** writing, and self-review against this list before the first push.

1. **Follows the conventions.** Naming and idiom per the stack's upstream style guide, plus the project's recorded exceptions. Existing code you touch is brought into line.
2. **Well-architected.** SOLID; policy in the core, thin adapters; ports and adapters at every boundary; the right pattern for the problem and no pattern for its own sake. Every endpoint meets the [API standard](api-standard.md).
3. **Designed before it is built, against a contract.** Every interface one lane provides and another consumes has a versioned [contract](contracts.md), agreed before either side builds on it, and both sides test against it.
4. **The minimum code that does the job.** YAGNI; no speculative options, dead code or duplication.
5. **Maintainable.** Small single-purpose units, low cyclomatic complexity (early returns, no deep nesting, no flag arguments), names that explain themselves.
6. **Minimal comments.** Doc comments on public contracts, plus a short *why* where a constraint isn't obvious (a security rule, a vendor limit, a legal requirement), citing its source. No narration, no change history, no ticket ids: the PR records what changed and why.
7. **Data access in repositories.** Connections, SDK clients and query text live only in repositories behind intention-revealing methods. Parameterised queries only, never string-built.
8. **Secure.** [OWASP](security.md) Top 10 and ASVS as the checklist, with tests for authorisation and input handling. Authenticated by default; least privilege; no secrets in code; TLS everywhere.
9. **Legal.** Complies with the law that applies to the product (privacy, consumer, accessibility). The project lists it in `team.config.yaml` → `project.regulatory`.
10. **Tested in the right proportions.** [TDD](testing.md); most behaviour in unit tests, integration at the adapters, E2E for the paths that matter; tests assert behaviour, not implementation.
11. **A vertical slice that fails gracefully.** Meets the acceptance criteria end to end, error and edge paths included, and is [accessible](accessibility.md). Where a dependency can fail, the slice ships its failure strategy: what the user sees, what is logged, how it recovers.
12. **Follows the design system.** The project's UI primitives and tokens; no one-off styles.
13. **Boy-scout rule.** Whatever you touch, or find broken next to it, leaves cleaner. Fix it in the same PR within the size limits; anything larger is filed as an issue now, never left silent.

## Engineering principles

- **Adapters translate, never decide.** An adapter that re-derives an answer the core already knows is a defect, even when the dependency arrow points the right way.
- **Core logic only tests call, while an adapter reimplements it, is dead policy.** Wire the adapter to it or delete it.
- **Conventions enforced once, at the boundary** (for example at dependency registration), not repeated at every call site.
- **Maximise the code that runs under unit tests.**
- **Use the project's gates as they are.** Never substitute a hand-rolled check for lint, coverage or the project's scripts.
- **Agents install nothing** outside the project's manifests and pinned tools, and fetch nothing from the web unless the brief says so. New tooling is its own PR.
- **Incremental.** Change methods, don't rewrite files. A scope that grows becomes a new branch and PR.
