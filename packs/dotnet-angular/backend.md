# .NET back end

Sources: Microsoft's [C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions) and [.NET naming guidelines](https://learn.microsoft.com/dotnet/standard/design-guidelines/naming-guidelines).

## Build
- `TreatWarningsAsErrors=true` and `Nullable=enable` in every project; analyzers on (`AnalysisLevel=latest-recommended`).
- File-scoped namespaces; namespace = folder.
- Primary constructors for dependency injection where they fit.

## Architecture
- **Core** project: entities, value objects, domain services, port interfaces. References no infrastructure package.
- **Application / API** project: endpoints, application services, DI composition.
- **Adapters**: one project or folder per external dependency; implements core ports; thin.
- An architecture test (for example NetArchTest) pins the dependency direction.
- Constructor injection only; no service locator, no static state.

## Data
- One repository per aggregate, behind a core port. No `IQueryable<T>` leaves the repository.
- Parameterised queries only (`SqlParameter`, EF Core LINQ, or the SDK's parameter API). Never interpolated query text.
- Persisted shapes pinned by a round-trip serialisation test; property naming set once at the serialiser registration, not per property.
- Optimistic concurrency (ETag or rowversion) on read-modify-write.

## HTTP
- RFC 9457 via `ProblemDetails` / `TypedResults.Problem`, with a stable `type` per error. No exception messages in responses.
- `[Authorize]` (or the endpoint equivalent) by default; anonymous endpoints explicit and rate-limited.
- Resilience on outbound calls (`Microsoft.Extensions.Http.Resilience`): timeout, bounded retry, circuit breaker.

## Tests
- xUnit (or the project's choice), one test project per production project or a shared one with clear folders.
- Hand-written test doubles shared per port; a mocking library only if the project chose one.
- Integration tests tagged (`[Trait("Category", "Integration")]`) so the pre-commit gate can exclude them when they need live dependencies.

## Logging
- Structured logging with message templates; never log personal data, secrets or tokens. Mask or hash identifiers through one helper.
