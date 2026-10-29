---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Implement the requested feature in the existing project; don't repeat bootstrap or redesign established infrastructure.

Clarify consequential unknowns, implement in bounded steps and test affected behavior using the project's existing commands (`testing.md`). Keep design to changed boundaries, ownership and risks. Preserve authored content and the approved visual direction. Follow any planning process the project already uses without installing or prescribing one. No feature brief or completion report is required.

These rules apply to every feature, and need no reference lookup:

- Game rules and state transitions go in plain C# types with no UnityEngine dependency (Core/Application), so they can be unit tested without the engine. MonoBehaviours only adapt engine events (collisions, input, frames) into commands on those types.
- State has one owner that publishes changes; consumers observe it instead of polling or mutating it directly. Wire objects explicitly through the composition root, not through singletons, static instances or scene searches (static resolution needs an ADR).
- Unit tests cover the rules at their edges (limits, overflow, invalid input) and the failure paths the feature introduces.
- Every subscription and async operation has an owner that releases or cancels it.
- Persistent data carries a schema version with tested migrations, handles a missing or corrupt file without crashing or silently overwriting it, and writes through a temporary file and atomic replace (`reliability.md` for details).

Conditional references: `architecture.md` for new/unclear boundaries; `modules.md` for substantial public contracts; `reactive.md` for streams/async lifetimes; `reliability.md` for persistence/network failures; `authoring.md` for scenes/prefabs/data/generators; `dependencies.md` for package choices; `utilities.md` before adding shared infrastructure. Use the UI or asset skill only for those subtasks. Read `localization.md` when adding/changing player-facing content.
