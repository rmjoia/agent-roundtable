# Testing

## TDD
Red → green → refactor (Kent Beck). The failing test comes first, and it fails for the right reason. Let tests drive the design: a hard-to-test unit is telling you about its dependencies (Freeman and Pryce, *GOOS*).

For existing code without tests, write characterisation tests first (Michael Feathers), then change it.

## Tests prove behaviour
For each test, ask: *which plausible wrong implementation would this fail on?* If none, it is decoration. Watch for:
- assertions on the wrong element or a constant;
- mocks that return the same value whatever the input;
- swallowed errors that make a broken path look green;
- async tests that finish before the code under test;
- time-dependent tests without fake timers.

Coverage and mutation score are read together. Coverage alone is never a gate: exercised is not verified.

## Proportions
- **Unit**: most behaviour, especially the domain core. Fast, hermetic (no network, no real clock, no shared state), deterministic.
- **Integration**: at the adapters, against real or containerised dependencies.
- **Contract**: both sides against the golden examples.
- **E2E**: the user journeys that matter, not every branch.

## Impacted tests
A change to UI or API lists its impacted tests at every layer (grep the changed components, i18n keys, test ids, routes, DTOs and endpoints):
- failing → updated in the same PR;
- none → tests added in the same PR;
- passing untouched → assertions strengthened.

## Ownership
A test belongs to the owner of the code it exercises, whatever folder it sits in. The QA lead owns E2E journeys and reviews test quality everywhere; findings go to the test's owner.

## Hygiene
- Unit and component tests assert i18n keys, not full sentences, so a copy change breaks no other lane.
- E2E locates by test id or accessible role and name; reads expected text from the translation files.
- No `.skip` or `.only` committed; no commented-out tests; delete obsolete tests.
- Test doubles are shared per port and ship in the commit of their first consumer.
