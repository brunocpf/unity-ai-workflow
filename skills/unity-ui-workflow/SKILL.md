---
name: unity-ui-workflow
description: Design and implement game UI, custom UITK controls, MVVM/R3 presentation, USS and UI content loading under this workflow.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Use the available Unity `ui-uitk` skill for UXML/USS/API mechanics, loading only its relevant references; `context-efficiency.md#skill-ownership` defines conflicts and fallback. This skill owns how UI fits the project.

These rules apply to every UI change, whatever its size:

- Display logic (formatting, ratios, enabled/busy/error/low states) lives in a pure Presentation ViewModel with no Unity references, covered by unit tests.
- The Unity side is a mechanical binding adapter: it subscribes to ViewModel state, writes element properties and forwards input as commands. It never polls gameplay objects every frame or reaches into MonoBehaviours for data.
- Layout lives in UXML and styling in USS beside the owning control or screen. Inline styles from C# are only for continuous per-instance runtime values such as a fill width or drag position (`ui-styling.md`); discrete states toggle USS classes. Reuse the project's control/content library and theme tokens.
- One owner disposes each subscription, ViewModel and binding when the screen or control goes away.

Size the reading to the task:

| Task | Read |
|---|---|
| Text, style or layout fix on existing UI | `ui-styling.md` only, and only for an unfamiliar USS question |
| New control or HUD element | `ui-construction.md`, `ui-binding.md`, `ui-styling.md` |
| New screen or substantial redesign | Above plus `ui-art-direction.md`; `ui-navigation.md` for focus/menus/screen stacks |
| Custom drawing, shaders, glyph effects, motion | `ui-advanced.md`, `ui-capabilities.md`, `ui-text-effects.md` as needed |
| Content loading, teardown/reload problems | `ui-content-loading.md`, `lifecycle.md` |

1. For new screens and substantial redesigns, set a concrete visual target and finish one representative polished screen before expanding. A new element on an existing screen follows the approved target and theme instead.
2. Authored localized properties use native bindings with one writer (`localization.md`) when the change adds player-facing text.
3. Check UI Builder, input, binding and lifecycle behavior; run the game and compare the result with the target, and keep refining.
4. Update relevant project decisions and tests; no UI status report.
