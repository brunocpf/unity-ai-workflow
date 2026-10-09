---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

Use project rules and the active OpenSpec change. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Implement the authorized feature in the existing project; do not repeat bootstrap or redesign established infrastructure.

1. Read affected capability specs, the active change and source. Use the OpenSpec propose/apply/archive operation for the phase; `spec-driven-development.md` defines the loop. Clarify only unresolved behavior or consequential choices.
2. Keep design to affected boundaries, ownership, tradeoffs and risks. Reuse architecture and verified helpers; no parallel feature brief, routine ADR or module document.
3. Implement dependency-ordered slices with affected tests. Update the owning contract only when it changes. Preserve authored content and accepted visual direction.
4. Deliver through the shared checks in verification.json (`spec-evidence.md`). Inspect/refine visual output when relevant. Report remaining manual/device verdicts honestly; no separate completion report.

Conditional references: `architecture.md` for new/unclear boundaries; `modules.md` for substantial public contracts; `reactive.md` for streams/async lifetimes; `reliability.md` for persistence/network failures; `authoring.md` for scenes/prefabs/data/generators; `dependencies.md` for package choices; `utilities.md` before adding shared infrastructure. Use the UI or asset skill only for those subtasks. Read `localization.md` when adding/changing player-facing content.
