---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

References resolve under `docs/standards/references/` (or `references/` at the kit root). Follow project rules, the active change and `context-efficiency.md`; load only sections triggered by this task.

Apply `clarification.md` when behavior, scope or consequential choices are unclear; preserve previous answers and continue independent work. Read `localization.md` when adding/changing player-facing text, language settings or localized content.

Use the project architecture/source map; read `architecture.md` for a new boundary or an unclear invariant. Add `modules.md` for public/cross-module changes and `reliability.md` for storage/network/failure contracts; read `reactive.md` when changing state streams or async behavior. Read `authoring.md` when changing scenes, prefab spawning, tuning definitions or generators; runtime factories consume authored assets by default. Read `dependencies.md` only when choosing/changing packages and `utilities.md` when adding shared infrastructure.

Implement the feature's next playable acceptance slice without weakening project standards. Keep existing approved profile exceptions. For UI work use the UI skill and the project's visual target; new/substantial visual work follows `ui-art-direction.md`. For art use the asset skill/reference. Apply existing code-organization conventions/checks; read `code-organization.md` when adding types or changing organization/quality coverage. Run changed-boundary checks from `validation.md`, record behavior/evidence and update the affected feature contract. Do not turn a local feature into a template/toolchain overhaul.

Apply `spec-driven-development.md`; use `spec-evidence.md` when defining verification or delivering the increment.
