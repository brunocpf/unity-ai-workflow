---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

Use project rules and the active OpenSpec change. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Implement the authorized feature in the existing project; do not repeat bootstrap or redesign established infrastructure.

Use the project-generated OpenSpec skill for the current operation; it owns the lifecycle and tracking. Apply `spec-driven-development.md` only for the Unity schema/evidence additions. `context-efficiency.md#skill-ownership` resolves provider availability and operation boundaries.

Keep design to affected boundaries, ownership and risks. Reuse architecture and verified helpers, preserve authored content and accepted visual direction, and deliver through the shared verification checks (`spec-evidence.md`). Do not create a parallel feature brief or completion report.

Conditional references: `architecture.md` for new/unclear boundaries; `modules.md` for substantial public contracts; `reactive.md` for streams/async lifetimes; `reliability.md` for persistence/network failures; `authoring.md` for scenes/prefabs/data/generators; `dependencies.md` for package choices; `utilities.md` before adding shared infrastructure. Use the UI or asset skill only for those subtasks. Read `localization.md` when adding/changing player-facing content.
