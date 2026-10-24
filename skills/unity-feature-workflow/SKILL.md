---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Implement the requested feature in the existing project; don't repeat bootstrap or redesign established infrastructure.

Clarify consequential unknowns, implement in bounded steps and test affected behavior using the project's existing commands (`testing.md`). Keep design to changed boundaries, ownership and risks. Preserve authored content and the approved visual direction. Follow any planning process the project already uses without installing or prescribing one. No feature brief or completion report is required.

Conditional references: `architecture.md` for new/unclear boundaries; `modules.md` for substantial public contracts; `reactive.md` for streams/async lifetimes; `reliability.md` for persistence/network failures; `authoring.md` for scenes/prefabs/data/generators; `dependencies.md` for package choices; `utilities.md` before adding shared infrastructure. Use the UI or asset skill only for those subtasks. Read `localization.md` when adding/changing player-facing content.
