---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Implement the authorized feature in the existing project; do not repeat bootstrap or redesign established infrastructure.

Clarify consequential unknowns, implement in bounded slices and verify affected behavior using existing project commands. Keep design to changed boundaries, ownership and risks. Preserve authored content and accepted visual direction; use `validation.md` for checks. Follow any independently adopted planning process without installing or prescribing one. No routine feature brief or completion report is required.

Conditional references: `architecture.md` for new/unclear boundaries; `modules.md` for substantial public contracts; `reactive.md` for streams/async lifetimes; `reliability.md` for persistence/network failures; `authoring.md` for scenes/prefabs/data/generators; `dependencies.md` for package choices; `utilities.md` before adding shared infrastructure. Use the UI or asset skill only for those subtasks. Read `localization.md` when adding/changing player-facing content.
