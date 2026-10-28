# Accessibility

Target: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) level AA, plus any national standard the project lists in `project.regulatory`.

## Every user-facing change
- **Keyboard**: every control reachable and operable; visible focus; no traps; logical order.
- **Semantics**: native elements first; every control has an accessible name; headings in order; landmarks.
- **Focus management**: dialogs trap and return focus; route changes move focus to the new content.
- **Contrast**: 4.5:1 for text, 3:1 for large text and UI components.
- **Reflow**: usable at 320 CSS px wide and 400% zoom without horizontal scrolling.
- **Motion**: respect `prefers-reduced-motion`.
- **Forms**: labels, not placeholders; errors announced and tied to their field.
- **Language**: `lang` set per page and per passage in another language.

## The usability walk
Before the PR, on every change to a user-facing surface: a real browser, narrow and desktop widths, keyboard only, every supported language, cold load included. Findings are fixed in the PR or filed.

## Tests
Automated checks (for example axe) in component and E2E tests catch some issues; they don't replace the walk.
