# Contracts

An interface that one lane provides and another consumes gets a **versioned contract**, agreed before either side builds on it.

What counts: a front end ↔ API call, a core port ↔ its adapter, an event, a persisted document read by another component, a shared artifact (a generated file, a config format).

## What a contract holds
- **Types**, with nullability and limits (lengths, ranges, formats).
- **Errors**: codes and their meaning; for HTTP, the Problem Details `type` URIs ([API standard](api-standard.md)).
- **Golden examples**: real requests and responses, produced from the provider's real serialiser output, not hand-written.
- **A version** (semver).
- For a port: the interface in domain terms and its error semantics, plus a shared test double.
- The **names other lanes need**: i18n keys (error-code keys included), routes, event names.

## Who does what
1. The architect designs it as a design brief on the work item.
2. The **providing** agent writes the contract files and golden examples.
3. The consuming agent and the security champion review it.
4. Both sides test against it. A mocked E2E answers with the golden examples.

## Changing a contract
- **PATCH**: documentation or examples only.
- **MINOR**: additive; new fields optional; consumers read tolerantly (ignore unknown fields).
- **MAJOR**: breaking, done as expand → migrate → contract: add the new shape, move every consumer, then remove the old. No commit removes a field or key a consumer still uses.

## Prove the wire shape
Golden examples are tested on both sides: casing, nullability, enums (by name or by value, stated), dates (ISO 8601, with offset), numbers (precision, string or number). A conversion between serialisers is a boundary like any other.
