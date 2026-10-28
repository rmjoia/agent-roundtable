# Angular front end

Sources: the [Angular style guide](https://angular.dev/style-guide) and [angular.dev best practices](https://angular.dev/best-practices) for the pinned version.

## Components
- Standalone components only; no NgModules in new code.
- Signals for state; `computed` for derived values; `input()` / `output()` / `model()` functions, not decorators.
- Built-in control flow (`@if`, `@for` with `track`, `@switch`), not structural directives.
- Follow the style guide's file and class naming for your version (recent versions drop the `Component` suffix).
- Zoneless change detection where the version supports it.
- No logic in templates beyond simple bindings; move it to a `computed` or a service.
- No manual `subscribe` without `takeUntilDestroyed`; prefer `toSignal` or the async pipe.

## Architecture
- Feature folders; a core layer for app-wide services; shared UI primitives in one place.
- HTTP calls live in services that map transport types to view models (an anti-corruption layer); components never see DTOs.
- The front end branches on the Problem Details `type`, mapped to an i18n key; it never shows server messages.

## UI
- The project's design-system primitives and tokens only; no hard-coded colours or one-off styles.
- Every structured page has a loading skeleton that matches its footprint (no layout shift).
- Every user-facing string through the i18n library, in every supported language.

## Tests
- Unit and component tests with the project's runner (Vitest or Jest); assert i18n keys, not sentences.
- Component harnesses (`@angular/cdk/testing`) for complex components.
- Playwright for E2E: test ids first, then role and accessible name.

## Build and lint
- `ng build` with budgets set; a budget breach fails the build.
- ESLint (`angular-eslint`) with no warnings; Prettier or the project's formatter.
- Run gate commands with `CI=1` so they don't share the build cache with a running `ng serve`.
