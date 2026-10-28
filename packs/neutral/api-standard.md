# API standard

Applies to every new or changed HTTP endpoint.

## Resources and methods
- Resource-oriented URLs, plural nouns, no verbs in paths (REST maturity level 2).
- Methods by their HTTP meaning: `GET` safe, `PUT` and `DELETE` idempotent, `POST` for creation or non-idempotent commands, `PATCH` for partial updates.
- Status codes by meaning: `201` with `Location` on create, `204` on no content, `409` on conflict, `412` on a failed precondition, `422` on semantically invalid input.
- Hypermedia only where it helps a client (a `Location`, a `next` link for pagination), not as ceremony.

## Errors: RFC 9457 Problem Details
Every error response is `application/problem+json`:

```json
{
  "type": "https://example.com/problems/order-not-cancellable",
  "title": "Order cannot be cancelled",
  "status": 409,
  "detail": "The order has already shipped.",
  "instance": "/orders/8f3c"
}
```

- `type` is a stable URI per error kind; clients branch on it (and the front end maps it to an i18n key).
- **Never** in an error body: personal data, echoed input, tokens, stack traces, internal messages or identifiers of other users.
- `instance` is the path, never the query string.
- Return `404` where `403` would confirm that a resource exists.
- Validation errors may add an `errors` extension listing field names and codes, not messages with input echoed.

## Security defaults
- Authenticated by default. An anonymous endpoint exists only when the feature needs it, is justified in the PR, and is rate-limited.
- The acting user comes from validated credentials, never from the request body or query.
- Concurrency control (ETags with `If-Match`) on read-modify-write of shared resources.
- Idempotency keys on payments and webhooks.

## Compatibility
- Additive changes only within a major version; see [contracts](contracts.md).
- Unknown fields in requests are ignored or rejected consistently, as the contract states.
