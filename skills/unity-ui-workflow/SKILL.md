---
name: unity-ui-workflow
description: Design and implement game UI, custom UITK controls, MVVM/R3 presentation, USS and UI content loading under this workflow.
---

References resolve under `docs/standards/references/` (or `references/` at the kit root). Follow project rules, the active change and `context-efficiency.md`; load only sections triggered by this task.

Use `clarification.md` for ambiguous behavior, languages, visual intent or constraints. Read `localization.md` when creating/changing player-facing text/assets or locale settings; authored localized properties use native UITK bindings, with one writer per property.

For a new game/screen or substantial visual work, read `ui-art-direction.md`, `ui-advanced.md` and `ui-capabilities.md`: establish a visual target, implement rich custom rendering and coordinated motion, and realize a representative polished screen before expanding the interface. Actively use the suitable drawing/gradient/material/filter/animation mechanisms without another user request. For local fixes, preserve the established target. Source examples supply architecture, not the finished game's appearance.

For structure/loading read `ui-construction.md`; for values/input read `ui-binding.md`; for appearance read `ui-styling.md`; for modern/experimental APIs add `ui-capabilities.md`. For custom drawing, shaders/filters or LitMotion transitions add `ui-advanced.md`; for glyph effects, reveals or animated counters add `ui-text-effects.md`. Read `lifecycle.md` when touching registries, scopes, pooling or teardown.

Keep ViewModels pure; binding adapters are mechanical and no parallel Presenter layer is introduced. Apply the selected constructor-complete control pattern with UXML-owned USS. Use the project's existing implementation; if absent, adapt only the needed source from the examples linked in the construction/binding references against the pinned editor. Treat illustrative type names as design contracts, not available Unity APIs.

Use `validation.md` UI cases and gallery/player evidence. Report visual quality against the target separately from technical passes; a capture without defects is not sufficient visual acceptance. Editing ordinary USS does not require rereading asset pipelines or redesigning the template resolver. Update compatibility evidence when adopting an experimental feature.

Apply `spec-driven-development.md`; use `spec-evidence.md` when defining verification or delivering the increment.
