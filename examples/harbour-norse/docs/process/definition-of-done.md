<!-- agent-roundtable:generated template=definition-of-done version=0.1.0 -->
# Definition of Done

A change is done when it is complete, tested and safe to ship today. The PR merges when every item holds; "we'll fix it later" is a new work item, filed now, not a gap left open.

## 1. It does what it should
- [ ] Every acceptance criterion is met, end to end (a vertical slice unless a documented exception).
- [ ] Error and edge paths are handled: the user sees a designed message, never a blank page or a dead control; failures are logged.
- [ ] Accessible: keyboard reachable, labelled, focus managed.

## 2. It meets the bar as written
- [ ] The Definition of good code (`docs/conventions/neutral/definition-of-good-code.md`).
- [ ] Zero build warnings and lint errors.
- [ ] No dead code, no commented-out blocks, no narrating comments, no ticket ids in code.
- [ ] Boy-scout rule: what was touched, or found broken next to it, is left cleaner; anything larger is filed.

## 3. Testing
- [ ] **Test first.** New behaviour has a test that went red before going green.
- [ ] **Tests prove behaviour.** Each would fail on a plausible wrong implementation. Coverage and mutation score are read together; coverage alone is never a gate.
- [ ] **Impacted tests found first.** A PR that changes UI or API lists its impacted unit, integration and E2E tests in the PR body, found by grepping the changed components, i18n keys, test ids, routes, DTOs and endpoints:
  - impacted tests fail → updated in the same PR, never as a follow-up;
  - no test touches the change → tests added in the same PR;
  - tests touch it but nothing fails → assertions strengthened (exercised is not verified).
- [ ] **Who does what.** The developer updates the tests in their own lane; a test outside it (typically E2E) is signalled in the PR's `Impacted tests` section for the QA lead, who checks the tests test the real code.
- [ ] No `.skip` or `.only` shipped. Unit tests are hermetic and deterministic.

## 4. Safe to ship
- [ ] Security review GREEN, or every finding fixed or tracked with the owner's agreement. A security finding closes only when its pinning test is in the diff and fails without the control.
- [ ] No secrets, identifiers or personal data in the diff, commit messages, fixtures, logs or screenshots.
- [ ] Contracts: version bumped per semver; additions optional; readers accept old shapes.
- [ ] Performance: no N+1 queries, no unbounded reads; front-end bundle within budget.
- [ ] Every user-facing string has keys in every supported language.

## 5. Recorded
- [ ] Every commit green, one logical change, Conventional Commits, with the `Agent:` trailer when an agent wrote it.
- [ ] PR body complete: linked issue, `## Agents`, `Docs:`, `Affects open issues:`, `Impacted tests`, Handoff.
- [ ] Docs delta in the same PR, or `Docs: not needed because …`.
- [ ] Work item updated: status, what was delivered, what the next task needs.
- [ ] Every review in the gate has landed and states what it challenged.
