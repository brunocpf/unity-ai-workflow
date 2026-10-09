---
name: unity-ui-workflow
description: Design and implement game UI, custom UITK controls, MVVM/R3 presentation, USS and UI content loading under this workflow.
---

Use project rules and the active OpenSpec change. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Use the available Unity `ui-uitk` skill for UXML/USS/API mechanics, loading only its relevant references; `context-efficiency.md#skill-ownership` defines conflicts and fallback. This skill owns project integration and acceptance.

Build on pure MVVM/R3 ViewModels with mechanical Unity binding adapters. Reuse the project's control/content library; adapt tested examples only for needed consumers.

1. For new/substantial screens, establish a concrete visual target and finish a representative polished screen before expanding (`ui-art-direction.md`, `ui-advanced.md`). Local fixes preserve the accepted target.
2. Load the reference for the changed concern: `ui-construction.md` for constructor-complete Builder-compatible controls and UXML-owned USS; `ui-binding.md` for small state projections/property writers; `ui-styling.md` for USS; `ui-navigation.md` for native Move/Submit, Cancel ownership and screen/modal lifetimes.
3. Use modern drawing/gradients/materials/filters and coordinated motion where they serve the visual target. `ui-capabilities.md` qualifies APIs; `ui-text-effects.md` covers glyph effects; `lifecycle.md` covers teardown/reload. Don't reload these for an unrelated text/style fix.
4. Authored localized properties use native bindings with one writer (`localization.md`). Verify affected Builder, input, binding and lifecycle behavior; inspect fresh rendered output against the target and iterate. A successful capture alone is not visual acceptance.
5. Update the active OpenSpec artifacts and shared checks, not a second UI design/status report. Keep required user/device verdicts pending until obtained.
